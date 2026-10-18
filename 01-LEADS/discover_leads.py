#!/usr/bin/env python3
"""
Lead Discovery Engine — starts from the Meta Ad Library, not from you.

Give ONE input: your market (e.g. "solar Hyderabad"). The pipeline then:
  1. Searches the LIVE Meta Ad Library for active advertisers in that market
  2. Extracts each advertiser's real destination/conversion page from their ad
     (the exact URL the ad sends customers to - or WhatsApp if that's the funnel)
  3. Audits that conversion page + pulls their full live ad activity (Meta + Google)
  4. Generates a branded Smart Pursuit PDF per lead

No website URLs, no company names, no city typing — all derived from the ads.

Usage:
  python discover_leads.py "solar Hyderabad"
  python discover_leads.py "rooftop solar Delhi" --limit 5
  python discover_leads.py "solar Hyderabad" --city Hyderabad --competitors 3
"""

import argparse
import os
import re
import sys
from collections import OrderedDict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ad_library import meta_search, run_research, save_audit, UA
from ads_audit import run_audit, print_audit_report
from audit_pdf import generate_pdf

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


def discover(query, max_ads):
    """One Meta Ad Library search — returns ads with destinations attached."""
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


def group_leads(ads, limit):
    """One lead per advertiser (page name), keeping the first ad seen."""
    leads = OrderedDict()
    for ad in ads:
        name = (ad.get("page_name") or "").strip()
        if not name:
            continue
        if name not in leads:
            leads[name] = ad
        if len(leads) >= limit:
            break
    return leads


def main():
    parser = argparse.ArgumentParser(
        description="Discover advertisers from the live Meta Ad Library and audit each end-to-end")
    parser.add_argument("query", help="Market to hunt in, e.g. 'solar Hyderabad'")
    parser.add_argument("--city", default="", help="City override (default: derived from query)")
    parser.add_argument("--limit", type=int, default=3, help="Leads to audit (default 3)")
    parser.add_argument("--competitors", type=int, default=3, help="Competitor ads per report")
    parser.add_argument("--pool", type=int, default=0,
                        help="Ad cards to scan in discovery (default: limit x 5)")
    args = parser.parse_args()

    city = args.city or city_from_query(args.query)
    pool = args.pool or args.limit * 5

    print("=" * 60)
    print(f"SMART PURSUIT LEAD DISCOVERY: {args.query}")
    print(f"City: {city or '(derived per lead)'} | Leads: {args.limit}")
    print("=" * 60)

    search = discover(args.query, max_ads=pool)
    if not search["ads"]:
        print("No active ads found for this market — try a broader query.")
        sys.exit(1)

    leads = group_leads(search["ads"], args.limit)
    print(f"\n[discover] {len(leads)} unique advertisers found:")
    for name, ad in leads.items():
        site = resolve_website(ad) or ("WhatsApp conversion" if ad.get("whatsapp")
                                       else "no website in ad")
        print(f"  - {name}  ->  {site}")

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
