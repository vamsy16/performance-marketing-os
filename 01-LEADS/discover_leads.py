#!/usr/bin/env python3
"""
Lead Discovery Engine — starts from the Meta Ad Library, not from you.

Give ONE input: your market (e.g. "solar Hyderabad"). The pipeline then:
  1. Loads the known-leads registry (leads.csv + sequence manifest + audit JSONs)
     and drops every advertiser we have already touched — a re-run of the same
     market therefore returns NEW businesses only, never duplicates
  2. Searches the LIVE Meta Ad Library for active advertisers in that market
  3. Extracts each advertiser's real destination/conversion page from their ad
     (the exact URL the ad sends customers to - or WhatsApp if that's the funnel)
  4. Audits that conversion page + pulls their full live ad activity (Meta + Google)
  5. Generates a branded Smart Pursuit PDF per lead

No website URLs, no company names, no city typing — all derived from the ads.

Duplicate guard:
  ON by default. Override with --allow-known (useful for re-auditing a lead
  whose site changed) or inspect any candidate first with:
      python 01-LEADS/known_leads.py "Some Company" theirsite.in

Usage:
  python discover_leads.py "solar Hyderabad"
  python discover_leads.py "rooftop solar Delhi" --limit 5
  python discover_leads.py "solar Hyderabad" --city Hyderabad --competitors 3
  python discover_leads.py "solar Hyderabad" --limit 5 --pool 60
"""

import argparse
import io
import json
import os
import re
import sys
from collections import OrderedDict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ad_library import meta_search, run_research, save_audit, UA
from ads_audit import run_audit, print_audit_report
from audit_pdf import generate_pdf
from known_leads import KnownLeads
from state_cities import cities_for, filter_leads, in_state, states

MARKET_WORDS = {
    "solar", "panel", "panels", "rooftop", "company", "companies", "installer",
    "installers", "near", "me", "in", "for", "and", "the", "best", "top",
    "quotes", "quote", "price", "prices", "cost", "installation", "install",
    "systems", "system", "energy", "electrical", "solution", "solutions",
    "services", "service", "provider", "providers", "dealers", "dealer",
    "shop", "store", "india", "online", "good", "trusted",
}

SOCIAL_HOSTS = (
    "facebook", "instagram", "youtube", "twitter", "linkedin", "google",
    "whatsapp", "wa.me", "t.me", "maps.app", "goo.gl", "bit.ly", "paypal",
    "fb.me", "m.me", "instagr.am",
)


def city_from_query(query):
    """Derive the city from the market query: 'rooftop solar Delhi' -> 'Delhi'."""
    tokens = [t for t in re.findall(r"[A-Za-z]+", query or "")
              if t.lower() not in MARKET_WORDS]
    return " ".join(tokens).title() if tokens else ""


def website_from_text(text):
    """Fallback: pull a real company domain out of the ad copy itself."""
    for m in re.finditer(r"(?:https?://)?(?:www\.)?([a-z0-9-]+\.[a-z]{2,10}(?:\.[a-z]{2,10})?)",
                         text or "", re.I):
        host = m.group(1).lower()
        if any(s in host for s in SOCIAL_HOSTS):
            continue
        if not re.search(r"\.(com|in|net|org|online|site|shop|tech|info|co\.in)$", host):
            continue
        url = m.group(0)
        if not url.startswith("http"):
            url = "https://" + url
        return url
    return ""


def resolve_website(ad):
    """The conversion page: ad destination first, domain in ad copy second."""
    dest = (ad.get("destination") or "").strip()
    if dest.startswith("http"):
        host_match = re.match(r"https?://([^/]+)", dest, re.I)
        host = (host_match.group(1) if host_match else "").lower()
        plausible = (host and "." in host
                     and not any(s in host for s in SOCIAL_HOSTS)
                     and re.search(r"\.(com|in|net|org|online|site|shop|tech|info)$", host))
        if plausible:
            return dest
    return website_from_text(ad.get("text", ""))


def discover(query, max_ads, feed=None):
    """One Meta Ad Library search — returns ads with destinations attached.

    With `feed`, cards captured live from the Meta Ad Library are replayed from
    disk instead of launching Playwright, so discovery + the duplicate guard
    run identically in a headless sandbox with no browser. The cards themselves
    were still captured from the live library.
    """
    if feed:
        with open(feed, encoding="utf-8") as fh:
            result = json.load(fh)
        result.setdefault("ads", [])
        print("\n[discover] replaying saved ad feed: %s (%d cards, "
              "captured for '%s')" % (feed, len(result["ads"]), query))
        print("  -> %s, %d ad cards with destination data"
              % (result.get("results_label") or "no results",
                 len(result["ads"])))
        return result

    from playwright.sync_api import sync_playwright

    print(f"\n[discover] Meta Ad Library search: '{query}'")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, channel="chrome")
        ctx = browser.new_context(user_agent=UA, locale="en-US",
                                  viewport={"width": 1400, "height": 1000})
        page = ctx.new_page()
        try:
            result = meta_search(page, query, max_ads=max_ads)
        finally:
            browser.close()

    print(f"  -> {result.get('results_label') or 'no results'}, "
          f"{len(result['ads'])} ad cards with destination data")
    return result


def group_leads(ads, limit, known=None):
    """One lead per advertiser (page name), keeping the first ad seen.

    Duplicate guard: any advertiser already in the known-leads registry is
    skipped and reported, and the scan keeps going until `limit` genuinely new
    advertisers have been collected. Returns (leads, skipped) where skipped is
    an OrderedDict of name -> (source, matched_name).
    """
    leads = OrderedDict()
    skipped = OrderedDict()
    for ad in ads:
        name = (ad.get("page_name") or "").strip()
        if not name or name in leads or name in skipped:
            continue
        if known is not None:
            verdict, source, matched = known.verdict(
                name=name, website=resolve_website(ad), email=ad.get("email", ""))
            if verdict:
                skipped[name] = (verdict, source, matched or name)
                continue
        leads[name] = ad
        if len(leads) >= limit:
            break
    return leads, skipped


def _audit_existing_state(state):
    """Report which rowed leads are inside / outside / unresolved for `state`.

    The ad cards carry no city, so the only city on record for a lead is the
    one written into leads.csv when it was rowed. That means a state guard can
    only be proved retrospectively: this reads the pipeline and shows exactly
    which leads would be kept, which would be refused, and which have a city
    string the configuration cannot resolve. Run it before trusting a new
    state on a live sweep - it is what would have caught V1 Solar Solutions
    (Bengaluru, advertising into Hyderabad) and mr_koti_00 (Guntur).
    """
    import csv

    from state_cities import check_rows, cities_for, states
    if state not in states():
        print("%r is not a configured state." % state)
        near = [x for x in states() if state.lower()[:4] in x.lower()]
        if near:
            print("Did you mean: %s" % ", ".join(near))
        return 1

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "leads.csv")
    if not os.path.exists(path):
        print("leads.csv not found at %s" % path)
        return 1
    with io.open(path, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    inside, outside, unresolved = check_rows(rows, state)
    print("=" * 66)
    print("PIPELINE vs %s — %d rowed leads" % (state, len(rows)))
    print("=" * 66)
    print("\nINSIDE %s (%d):" % (state, len(inside)))
    for name, city, why in inside:
        print("  + %-44s %s" % (name, why))
    print("\nOUTSIDE %s (%d) — these would be refused:" % (state, len(outside)))
    for name, city, why in outside:
        print("  - %-44s %s" % (name, why))
    print("\nUNRESOLVED (%d) — city string matches no configured city:" % len(unresolved))
    for name, city, why in unresolved:
        print("  ? %-44s %r" % (name, city))
    if unresolved:
        print("\n  Unresolved is not the same as outside. Add the locality to")
        print("  LOCALITIES or the city to STATE_CITIES in state_cities.py,")
        print("  then re-run — an unresolved city must never be waved through.")
    print("\n%s: %d inside, %d outside, %d unresolved"
          % (state, len(inside), len(outside), len(unresolved)))
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Discover advertisers from the live Meta Ad Library and audit each end-to-end")
    parser.add_argument("query", help="Market to hunt in, e.g. 'solar Hyderabad'")
    parser.add_argument("--city", default="", help="City override (default: derived from query)")
    parser.add_argument("--limit", type=int, default=3, help="Leads to audit (default 3)")
    parser.add_argument("--competitors", type=int, default=3, help="Competitor ads per report")
    parser.add_argument("--pool", type=int, default=0,
                        help="Ad cards to scan in discovery (default: limit x 5)")
    parser.add_argument("--feed", default="",
                        help="Replay a saved JSON ad feed instead of launching "
                             "Playwright (same shape as meta_search() output). "
                             "Useful when no browser is available, or to re-run a "
                             "captured sweep deterministically.")
    parser.add_argument("--allow-known", action="store_true",
                        help="Include advertisers already in the pipeline "
                             "(re-audit an existing lead)")
    parser.add_argument("--state", default="",
                        help="Restrict this sweep to one Indian state. Only "
                             "leads whose city resolves to a city inside that "
                             "state are kept; anything else is reported and "
                             "dropped. Run with --list-states to see the "
                             "configured states, or --list-cities STATE to "
                             "see a state's cities.")
    parser.add_argument("--list-states", action="store_true",
                        help="Print every configured state and exit")
    parser.add_argument("--list-cities", default="",
                        help="Print every city inside STATE and exit")
    parser.add_argument("--audit-state", default="",
                        help="Check the EXISTING pipeline (leads.csv) against "
                             "STATE and report which rowed leads are inside "
                             "it, outside it, or unresolved. Reads nothing "
                             "from the network. Use this before trusting a "
                             "new state on live sweeps.")
    args = parser.parse_args()

    # Listing flags short-circuit before any network work.
    if args.list_states:
        print("Configured states (%d):" % len(states()))
        for st in states():
            print("  %-34s %d cities" % (st, len(cities_for(st))))
        return 0
    if args.audit_state:
        return _audit_existing_state(args.audit_state)
    if args.list_cities:
        st = args.list_cities
        if st not in states():
            print("%r is not a configured state." % st)
            near = [x for x in states() if st.lower()[:4] in x.lower()]
            if near:
                print("Did you mean: %s" % ", ".join(near))
            return 1
        print("%s (%d cities):" % (st, len(cities_for(st))))
        for c in cities_for(st):
            print("  ", c)
        return 0
    if args.state and args.state not in states():
        print("--state %r is not a configured state." % args.state)
        near = [x for x in states() if args.state.lower()[:4] in x.lower()]
        if near:
            print("Did you mean: %s" % ", ".join(near))
        return 1

    city = args.city or city_from_query(args.query)
    pool = args.pool or args.limit * 5

    print("=" * 60)
    print(f"SMART PURSUIT LEAD DISCOVERY: {args.query}")
    print(f"City: {city or '(derived per lead)'} | Leads: {args.limit}")
    print("=" * 60)

    # State guard, part 1 - refuse the sweep before it costs anything.
    # The Meta Ad Library cards carry no city or location field (only page
    # name, creative text and destination), so an individual advertiser's city
    # cannot be known until their own site is read. What CAN be checked before
    # any network work is the market the sweep is pointed at, and that is the
    # guard: a sweep whose own city resolves outside the configured state is
    # refused here rather than after a paid-for crawl.
    if args.state:
        ok, why = in_state(city, args.state)
        print(f"[state] restricting this sweep to {args.state} "
              f"({len(cities_for(args.state))} configured cities)")
        if not ok:
            print(f"[state] REFUSED — {why}")
            print(f"[state] the market '{args.query}' resolves to "
                  f"{city or 'no city'}, which is not inside {args.state}.")
            print(f"[state] re-run with a city inside {args.state}, or with "
                  f"--state set to the state you actually want. Use "
                  f"--list-cities '{args.state}' to see the allowed cities.")
            return 1
        print(f"[state] sweep city OK — {why}")

    # ---- duplicate guard: never re-fetch a business we already touched -------
    known = None
    if not args.allow_known:
        known = KnownLeads(quiet=True)
        stats = known.summary()
        print(f"[dedupe] known-leads registry: {stats['total']} entries "
              f"({stats['unique_domains']} domains, {stats['unique_names']} names) "
              f"from {', '.join(sorted(stats['by_source']))}")
    else:
        print("[dedupe] --allow-known set: existing pipeline leads will be included")

    search = discover(args.query, max_ads=pool, feed=args.feed or None)
    if not search["ads"]:
        print("No active ads found for this market — try a broader query.")
        sys.exit(1)

    leads, skipped = group_leads(search["ads"], args.limit, known=known)
    if skipped:
        print(f"\n[dedupe] {len(skipped)} advertiser(s) skipped — already in the pipeline:")
        for name, (verdict, source, matched) in skipped.items():
            flag = "" if verdict == "known" else "  [REVIEW — confirm before clearing]"
            print(f"  - {name}  (matches '{matched}' in {source}){flag}")

    print(f"\n[discover] {len(leads)} NEW advertisers found:")
    for name, ad in leads.items():
        site = resolve_website(ad) or ("WhatsApp conversion" if ad.get("whatsapp")
                                       else "no website in ad")
        print(f"  - {name}  ->  {site}")
    if not leads:
        print("\nNo new advertisers in this sweep — every active advertiser for "
              f"'{args.query}' is already in the pipeline. Raise --pool to scan "
              "more ad cards, or move to a different market.")
        sys.exit(0)

    results = []
    for i, (name, ad) in enumerate(leads.items(), 1):
        print("\n" + "-" * 60)
        print(f"[{i}/{len(leads)}] {name}")
        print("-" * 60)

        website = resolve_website(ad)
        lead_city = city or city_from_query(args.query)

        # Step 1: audit the conversion page the ad actually sends customers to
        if website:
            print(f"  [1/3] Auditing conversion page: {website}")
            audit = run_audit(website, company_name=name, city=lead_city)
            if "error" in audit:
                print(f"    audit error: {audit['error']} (continuing with ad data)")
            else:
                print_audit_report(audit)
        else:
            print("  [1/3] No website in ad (WhatsApp/Facebook conversion) — "
                  "skipping website audit")
            audit = {"company": name, "city": lead_city, "website": "",
                     "no_website": True, "audit_date": ad.get("started", "")}
            audit["score"] = {"score": 0, "issues": [], "wins": []}

        audit["discovery"] = {"market_query": args.query, "city": lead_city,
                              "source_ad": ad.get("library_id", ""),
                              "destination": ad.get("destination", ""),
                              "whatsapp": ad.get("whatsapp", "")}

        # Step 2: full live ad activity (Meta own + competitors + Google)
        print(f"  [2/3] Pulling live ad activity for: {name}")
        ad_data = run_research(name, city=lead_city, website=website,
                               competitors=args.competitors)
        audit["ad_library"] = ad_data
        audit_path = save_audit(audit)
        print(f"    meta own: {ad_data['meta_own']['results_label'] or 'none'} | "
              f"competitors meta={len(ad_data['meta_competitors']['ads'])} "
              f"google={len(ad_data['google_competitors']['advertisers'])}")

        # Step 3: branded PDF (needs at least a website or live ads to be meaningful)
        pdf_path = None
        if website or ad_data["meta_own"].get("found"):
            print(f"  [3/3] Generating PDF")
            try:
                pdf_path = generate_pdf(audit)
            except Exception as e:
                print(f"    PDF error: {e}")
        else:
            print("  [3/3] Skipped PDF — no website and no live ads found")

        results.append((name, website, audit.get("score", {}).get("score"), pdf_path))

    print("\n" + "=" * 60)
    print(f"DISCOVERY COMPLETE — {len(results)} lead(s)")
    print("=" * 60)
    for name, site, score, pdf in results:
        print(f"  {name}")
        print(f"    site:  {site or 'WhatsApp-only conversion'}")
        print(f"    score: {score if score is not None else 'n/a'}/100")
        print(f"    pdf:   {pdf or 'not generated'}")


if __name__ == "__main__":
    main()
