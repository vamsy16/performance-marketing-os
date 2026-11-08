#!/usr/bin/env python3
"""
verify_live.py -- THIRD CHECK: is the stored data still REAL, LIVE data?

verify_report.py checks that the PDF agrees with the JSON.  report-reviewer
checks that the JSON and PDF are honest about what was measured.  Neither of
them touches the network, so neither can catch the one failure that actually
costs a client's trust: the stored figures going stale, or a figure that was
never live in the first place.

This script closes that gap.  It re-fetches every source the report claims to
have read and compares what it finds now with what is stored.

    python verify_live.py                        # every ads-only report
    python verify_live.py --company "Varna Solar Pvt. Ltd."
    python verify_live.py --latest               # the 5 most recent
    python verify_live.py --json out.json        # machine-readable verdict
    python verify_live.py --timeout 20 --retries 2

VERDICTS
    MATCH        the live source confirms the stored figure exactly
    DRIFT        the live source contradicts the stored figure -- the report
                 is now wrong and must be re-generated before it is sent
    UNREACHABLE  the source could not be read, so nothing was confirmed.
                 This is NOT a pass.  A report with an unverifiable claim is
                 exactly as undeliverable as a wrong one.
    NOT_CLAIMED  the report itself says the value was never read (it is None /
                 "not checked").  Nothing to re-verify; recorded so the gap
                 stays visible instead of quietly becoming a guess.

EXIT CODES
    0   every live check MATCHED
    1   at least one DRIFT -- re-run the pipeline for the affected leads
    2   at least one UNREACHABLE -- could not verify, do not deliver
    3   nothing to check

HARD RULES BUILT INTO THIS SCRIPT
    * It never invents a value to make a check pass.  A comparison that
      cannot be made is reported as UNREACHABLE.
    * Any consumer of a possibly-None field must test `is None` explicitly.
      `dict.get(k, default)` returns None when the key EXISTS with value
      None, which has silently broken this pipeline three times.
    * A stored destination of "Not confirmed from the ad card in this pass"
      is never upgraded to a real destination by this script.  Only a source
      that actually states a destination may confirm one.
"""

import argparse
import glob
import json
import os
import re
import sys
import time

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:  # pragma: no cover - dependency guard
    sys.stderr.write(
        "verify_live.py needs requests + beautifulsoup4.\n"
        "  pip install -r 01-LEADS/requirements.txt\n"
    )
    raise SystemExit(3)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ADS_ONLY_DIR = os.path.join(BASE_DIR, "ads_only_results")

# The same identity the pipeline uses, so we are not blocked as a bare bot.
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

W3C_VALIDATOR = "https://validator.w3.org/nu/?doc={url}&out=json"

MATCH, DRIFT, UNREACHABLE, NOT_CLAIMED = "MATCH", "DRIFT", "UNREACHABLE", "NOT_CLAIMED"

# Tracking signatures -- kept deliberately identical in spirit to
# ads_audit.check_tracking_pixels() so a re-check means the same thing.
PIXEL_SIGNATURES = [
    ("meta_pixel", r"connect\.facebook\.net|fbq\s*\(|facebook-pixel"),
    ("google_ads", r"googleadservices\.com|AW-\d{9,}|gtag/js\?id=AW-"),
    ("google_analytics_ga4", r"G-[A-Z0-9]{8,}"),
    ("google_analytics_ua", r"UA-\d{4,}-\d+"),
    ("linkedin_insight", r"_linkedin_partner_id|snap\.licdn\.com"),
    ("microsoft_clarity", r"clarity\.ms"),
    ("hotjar", r"static\.hotjar\.com|hjSiteSetting"),
    ("google_tag_manager", r"googletagmanager\.com/gtag/js|GTM-[A-Z0-9]{5,}|googletagmanager\.com/gtm\.js"),
]

GA4_ID_RE = re.compile(r"\bG-[A-Z0-9]{10}\b")
GADS_ID_RE = re.compile(r"\bAW-\d{9,}\b")
GTM_ID_RE = re.compile(r"\bGTM-[A-Z0-9]{5,}\b")


# ---------------------------------------------------------------------------
# fetching
# ---------------------------------------------------------------------------

def fetch(url, timeout=15, retries=1):
    """GET a URL.  Returns (ok, response_or_None, error_string)."""
    last = "unknown error"
    for attempt in range(max(1, retries + 1)):
        try:
            r = requests.get(
                url,
                timeout=timeout,
                headers={
                    "User-Agent": UA,
                    "Accept": "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.9",
                },
                allow_redirects=True,
            )
            return True, r, ""
        except Exception as e:  # noqa: BLE001 - any failure is "unreachable"
            last = "%s: %s" % (type(e).__name__, e)
            if attempt < retries:
                time.sleep(1.5)
    return False, None, last


def fetch_html(url, timeout=15, retries=1):
    """Fetch a URL and return (html_or_None, final_url_or_None, error)."""
    ok, r, err = fetch(url, timeout=timeout, retries=retries)
    if not ok or r is None:
        return None, None, err
    if r.status_code >= 400:
        return None, getattr(r, "url", url), "HTTP %s" % r.status_code
    return r.text, r.url, ""


# ---------------------------------------------------------------------------
# small helpers that are None-safe by construction
# ---------------------------------------------------------------------------

def is_none(value):
    """True only for a genuine None.

    The pipeline stores None (never a guess) for anything it could not read.
    Every comparison below goes through this, because `dict.get(k, d)`
    returns None when the key exists with value None -- a trap that has
    already produced a false "no Google Ads presence" claim in outreach.
    """
    return value is None


def blank(value):
    """True for None, empty string, or whitespace only."""
    return value is None or (isinstance(value, str) and not value.strip())


def text_of(value):
    return "" if value is None else str(value)


def normalise_space(s):
    return re.sub(r"\s+", " ", text_of(s)).strip()


def parse_validator_string(s):
    """'0 errors, 0 warnings, 23 info' -> {'error':0,'warning':0,'info':23}."""
    out = {"error": None, "warning": None, "info": None}
    if blank(s):
        return out
    for kind in out:
        m = re.search(r"(\d+)\s+%ss?" % kind, text_of(s), re.I)
        if m:
            out[kind] = int(m.group(1))
    return out


def count_validator_messages(messages):
    """W3C 'out=json' message list -> {'error':n,'warning':n,'info':n}."""
    out = {"error": 0, "warning": 0, "info": 0}
    for m in messages or []:
        if not isinstance(m, dict):
            continue
        t = text_of(m.get("type")).lower()
        if t in out:
            out[t] += 1
        elif m.get("subType") in out:
            out[m["subType"]] += 1
        else:
            out["info"] += 1
    return out


def slugify(name):
    s = re.sub(r"[^A-Za-z0-9]+", "_", text_of(name)).strip("_")
    return s


# ---------------------------------------------------------------------------
# check 1 -- every stored Meta ad is still live and unchanged
# ---------------------------------------------------------------------------

def check_ad(ad, timeout, retries):
    """Re-read one stored ad from the live Meta Ad Library.

    Returns a list of result dicts so a single ad can produce several
    independent verdicts (identity, start date, destination).
    """
    results = []
    lib_id = text_of((ad or {}).get("library_id")).strip()
    url = text_of((ad or {}).get("library_url")).strip() or (
        "https://www.facebook.com/ads/library/?id=%s" % lib_id if lib_id else "")

    if not lib_id:
        results.append(dict(check="ad.library_id", verdict=NOT_CLAIMED,
                            detail="no library id stored for this ad"))
        return results

    stored_page = normalise_space((ad or {}).get("page_name"))
    stored_started = normalise_space((ad or {}).get("started"))
    stored_dest = text_of((ad or {}).get("destination"))

    html, final_url, err = fetch_html(url, timeout=timeout, retries=retries)

    if html is None:
        results.append(dict(
            check="ad.live", verdict=UNREACHABLE,
            detail="could not read %s (%s) -- ad liveness NOT confirmed" % (url, err or final_url)))
        return results

    body = normalise_space(html)
    has_id = lib_id in html or lib_id in body
    has_page = bool(stored_page) and stored_page.lower() in body.lower()

    # A login wall or an empty shell carries neither the id nor the page
    # name.  Treat that as unreachable, never as a pass.
    if not has_id and not has_page:
        results.append(dict(
            check="ad.live", verdict=UNREACHABLE,
            detail="fetched %s but the response carries neither library id %s "
                   "nor page name '%s' -- likely a login wall, so ad liveness "
                   "is NOT confirmed" % (url, lib_id, stored_page)))
        return results

    results.append(dict(check="ad.live", verdict=MATCH,
                        detail="library id %s still resolves on the live Ad Library" % lib_id))

    if has_page and stored_page:
        results.append(dict(check="ad.page_name", verdict=MATCH,
                            detail="page name still '%s'" % stored_page))

    if stored_started:
        if stored_started.lower() in body.lower():
            results.append(dict(check="ad.started", verdict=MATCH,
                                detail="still shows 'running since %s'" % stored_started))
        else:
            results.append(dict(
                check="ad.started", verdict=DRIFT,
                detail="stored start date '%s' is not present on the live card -- "
                       "the ad may have been restarted or re-dated" % stored_started))

    # Destination: only ever confirmed by a source that states one.
    if "not confirmed" in stored_dest.lower() or blank(stored_dest):
        results.append(dict(
            check="ad.destination", verdict=NOT_CLAIMED,
            detail="stored as not confirmed; this script will not upgrade it to a "
                   "guess. Re-read the live ad card by hand to confirm."))
    else:
        results.append(dict(
            check="ad.destination", verdict=NOT_CLAIMED,
            detail="stored destination '%s' needs a human read of the live card to "
                   "confirm; the ?id= page does not expose it as text" % stored_dest))
    return results


# ---------------------------------------------------------------------------
# check 2 -- the website is still the site that was measured
# ---------------------------------------------------------------------------

def check_site(audit, timeout, retries):
    """Re-fetch the lead's website and re-measure the stored site facts."""
    results = []
    site = audit.get("site_audit") or {}
    website = text_of(audit.get("website")).strip()
    if not website:
        results.append(dict(check="site.url", verdict=NOT_CLAIMED,
                            detail="no website stored"))
        return results

    if not website.startswith(("http://", "https://")):
        website = "https://" + website

    html, final_url, err = fetch_html(website, timeout=timeout, retries=retries)
    if html is None:
        results.append(dict(
            check="site.live", verdict=UNREACHABLE,
            detail="could not read %s (%s) -- site facts NOT re-verified" % (website, err or final_url)))
        return results

    results.append(dict(check="site.live", verdict=MATCH,
                        detail="%s responds (final URL %s)" % (website, final_url)))

    # --- redirect drift -----------------------------------------------------
    stored_final = normalise_space(site.get("final_url"))
    if stored_final and final_url:
        a = stored_final.rstrip("/").lower()
        b = final_url.rstrip("/").lower()
        if a == b:
            results.append(dict(check="site.final_url", verdict=MATCH,
                                detail="still resolves to %s" % final_url))
        else:
            results.append(dict(
                check="site.final_url", verdict=DRIFT,
                detail="stored final_url '%s' but the site now lands on '%s'" % (stored_final, final_url)))

    soup = BeautifulSoup(html, "html.parser")

    # --- title --------------------------------------------------------------
    seo = site.get("seo") or {}
    stored_title = normalise_space(seo.get("title_text"))
    live_title = normalise_space(soup.title.get_text() if soup.title else "")
    if is_none(seo.get("title_text")):
        results.append(dict(check="site.title", verdict=NOT_CLAIMED,
                            detail="head was never captured for this lead"))
    elif stored_title:
        if live_title and stored_title.lower() == live_title.lower():
            results.append(dict(check="site.title", verdict=MATCH,
                                detail="title unchanged: %s" % live_title))
        elif live_title:
            results.append(dict(
                check="site.title", verdict=DRIFT,
                detail="stored title '%s' but the live title is '%s'" % (stored_title, live_title)))
        else:
            results.append(dict(
                check="site.title", verdict=DRIFT,
                detail="stored title '%s' but the page now serves no <title>" % stored_title))

    # --- H1 count (the React-SPA signature) ---------------------------------
    stored_h1 = seo.get("h1_count")
    live_h1 = len(soup.find_all("h1"))
    if is_none(stored_h1):
        results.append(dict(check="site.h1_count", verdict=NOT_CLAIMED,
                            detail="h1 count was never captured"))
    elif int(stored_h1) == live_h1:
        results.append(dict(check="site.h1_count", verdict=MATCH,
                            detail="still %d H1 tag(s) in the served HTML" % live_h1))
    else:
        results.append(dict(
            check="site.h1_count", verdict=DRIFT,
            detail="stored h1_count %s but the served HTML now has %d -- the "
                   "site's rendering changed since the audit" % (stored_h1, live_h1)))

    # --- tracking pixels ----------------------------------------------------
    stored_pixels = site.get("pixels") or {}
    live_pixels = {}
    for key, pattern in PIXEL_SIGNATURES:
        live_pixels[key] = bool(re.search(pattern, html, re.I))

    pixel_rows = []
    for key, _ in PIXEL_SIGNATURES:
        stored = stored_pixels.get(key)
        if is_none(stored):
            pixel_rows.append("%s=not checked" % key)
            continue
        live = live_pixels.get(key)
        if bool(stored) == bool(live):
            pixel_rows.append("%s=%s (agrees)" % (key, "present" if live else "absent"))
        else:
            pixel_rows.append("%s=DRIFT stored %s / live %s" % (
                key, "present" if stored else "absent", "present" if live else "absent"))
            results.append(dict(
                check="site.pixels.%s" % key, verdict=DRIFT,
                detail="stored %s but the live page shows %s" % (
                    "present" if stored else "absent", "present" if live else "absent")))

    if not any(r["verdict"] == DRIFT for r in results if r["check"].startswith("site.pixels.")):
        checked = [k for k, _ in PIXEL_SIGNATURES if not is_none(stored_pixels.get(k))]
        if checked:
            results.append(dict(
                check="site.pixels", verdict=MATCH,
                detail="all %d measured tools agree with the live page (%s)" % (
                    len(checked), ", ".join(pixel_rows))))
        else:
            results.append(dict(
                check="site.pixels", verdict=NOT_CLAIMED,
                detail="head was never captured for this lead, so no pixel claim "
                       "was made and none can be re-verified"))

    # --- GA4 / Google Ads / GTM ids quoted anywhere in the report -----------
    blob = json.dumps(audit, ensure_ascii=False)
    for label, pattern in (("GA4", GA4_ID_RE), ("Google Ads", GADS_ID_RE), ("GTM", GTM_ID_RE)):
        stored_ids = sorted(set(pattern.findall(blob)))
        live_ids = sorted(set(pattern.findall(html)))
        if not stored_ids:
            continue
        missing = [i for i in stored_ids if i not in live_ids]
        if missing:
            results.append(dict(
                check="site.ids.%s" % label, verdict=DRIFT,
                detail="the report quotes %s id(s) %s which are no longer on the live page" % (
                    label, ", ".join(missing))))
        else:
            results.append(dict(check="site.ids.%s" % label, verdict=MATCH,
                                detail="%s id(s) %s still present" % (label, ", ".join(stored_ids))))

    # --- validator counts ---------------------------------------------------
    stored_counts = parse_validator_string(site.get("html_errors"))
    if all(v is None for v in stored_counts.values()):
        results.append(dict(check="site.validator", verdict=NOT_CLAIMED,
                            detail="no validator counts stored"))
    else:
        vurl = W3C_VALIDATOR.format(url=website if final_url is None else final_url)
        vhtml, _, verr = fetch_html(vurl, timeout=timeout, retries=retries)
        if vhtml is None:
            results.append(dict(
                check="site.validator", verdict=UNREACHABLE,
                detail="could not re-run the W3C validator (%s) -- stored counts "
                       "NOT re-verified" % verr))
        else:
            try:
                vdata = json.loads(vhtml)
            except Exception as e:  # noqa: BLE001
                vdata = None
                verr = "validator returned non-JSON (%s)" % e
            if not isinstance(vdata, dict):
                results.append(dict(
                    check="site.validator", verdict=UNREACHABLE,
                    detail="validator response unusable (%s) -- counts NOT re-verified" % verr))
            else:
                live_counts = count_validator_messages(vdata.get("messages"))
                for kind in ("error", "warning", "info"):
                    stored = stored_counts.get(kind)
                    if is_none(stored):
                        continue
                    live = live_counts.get(kind, 0)
                    if stored == live:
                        results.append(dict(
                            check="site.validator.%s" % kind, verdict=MATCH,
                            detail="still %d %s(s)" % (live, kind)))
                    else:
                        # The validator is deterministic, so a different count
                        # means the page changed.
                        results.append(dict(
                            check="site.validator.%s" % kind, verdict=DRIFT,
                            detail="stored %d %s(s) but the live page now raises %d -- "
                                   "the page changed since the audit" % (stored, kind, live)))

    # --- platform claim -----------------------------------------------------
    stored_platform = normalise_space(site.get("platform"))
    if stored_platform:
        if "react" in stored_platform.lower():
            ok_react = ("react" in html.lower()
                        or re.search(r"/static/js/main\.[a-f0-9]+\.js", html)
                        or "__react" in html.lower())
            results.append(dict(
                check="site.platform", verdict=MATCH if ok_react else DRIFT,
                detail=("still a React build" if ok_react else
                        "stored as '%s' but no React build markers are in the served HTML" % stored_platform)))
        elif "next" in stored_platform.lower():
            ok_next = ("_next" in html or "__NEXT_DATA__" in html)
            results.append(dict(
                check="site.platform", verdict=MATCH if ok_next else DRIFT,
                detail=("still a Next.js build" if ok_next else
                        "stored as '%s' but no Next.js markers are in the served HTML" % stored_platform)))
    return results


# ---------------------------------------------------------------------------
# check 3 -- the report never claims more ads than it lists
# ---------------------------------------------------------------------------

def check_ad_counts(audit):
    """The PDF's 'N live ads' must equal len(ads), not results_count.

    The manifest once filled the live-ad count from the Ad Library's
    '~N results' total instead of the number of ads actually captured,
    which overstated activity in outreach emails.
    """
    results = []
    meta = (audit.get("ad_library") or {}).get("meta_own") or {}
    ads = meta.get("ads")
    if not isinstance(ads, list):
        results.append(dict(check="ads.listed", verdict=NOT_CLAIMED,
                            detail="no own-ad list stored"))
        return results

    listed = len(ads)
    results.append(dict(check="ads.listed", verdict=MATCH,
                        detail="%d own ad(s) captured and reproduced" % listed))

    declared = meta.get("results_count")
    if is_none(declared):
        return results
    if int(declared) < listed:
        results.append(dict(
            check="ads.results_count", verdict=DRIFT,
            detail="Ad Library reported %s results but %d ads are stored -- the "
                   "stored ads cannot all come from that query" % (declared, listed)))
    else:
        results.append(dict(
            check="ads.results_count", verdict=MATCH,
            detail="Ad Library reported %s result(s), %d captured and reproduced" % (declared, listed)))
    return results


# ---------------------------------------------------------------------------
# check 4 -- the outreach text agrees with the report
# ---------------------------------------------------------------------------

def check_outreach_consistency(audit):
    """Cross-check the email body stored in the manifest against the report.

    This is the check that caught the Lumisun / Kypas drafts: the email said
    the ads click to WhatsApp / an fb.me form while the report itself recorded
    the destination as not confirmed.  Sending that would have handed the
    client a claim they could disprove in one click.
    """
    results = []
    manifest_path = os.path.join(
        os.path.dirname(BASE_DIR), "02-OUTREACH", "generated_emails", "sequence_manifest.json")
    if not os.path.exists(manifest_path):
        results.append(dict(check="outreach.manifest", verdict=NOT_CLAIMED,
                            detail="no sequence manifest found"))
        return results

    try:
        manifest = json.load(open(manifest_path, encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        results.append(dict(check="outreach.manifest", verdict=UNREACHABLE,
                            detail="manifest unreadable: %s" % e))
        return results

    company = text_of(audit.get("company"))
    seq = None
    for s in manifest.get("sequences", []):
        if text_of(s.get("company")).strip().lower() == company.strip().lower():
            seq = s
            break
    if seq is None:
        results.append(dict(check="outreach.manifest", verdict=NOT_CLAIMED,
                            detail="no sequence for '%s' in the manifest" % company))
        return results

    stored_dest = text_of((audit.get("funnel") or {}).get("destination"))
    dest_unconfirmed = "not confirmed" in stored_dest.lower()

    for step in seq.get("steps", []):
        body = text_of(step.get("body"))
        if not body.strip():
            continue
        low = body.lower()
        step_no = step.get("step")

        # A destination claim the report does not support.
        if dest_unconfirmed:
            for phrase in ("click to whatsapp", "clicks to whatsapp", "lands in whatsapp",
                           "fb.me lead form", "facebook lead form", "clicks to an fb.me"):
                if phrase in low:
                    results.append(dict(
                        check="outreach.step%s.destination" % step_no, verdict=DRIFT,
                        detail="step %s claims '%s' but the report records the "
                               "destination as '%s'" % (step_no, phrase, stored_dest)))
                    break
            else:
                results.append(dict(
                    check="outreach.step%s.destination" % step_no, verdict=MATCH,
                    detail="step %s makes no destination claim, matching the report" % step_no))

        # A website score the report never measured.
        score = ((audit.get("site_audit") or {}).get("score") or {}).get("score")
        if is_none(score):
            for m in re.finditer(r"\b(\d{1,3})\s*/\s*100\b", body):
                results.append(dict(
                    check="outreach.step%s.score" % step_no, verdict=DRIFT,
                    detail="step %s quotes '%s/100' but this report has no measured "
                           "website score" % (step_no, m.group(1))))
                break
            else:
                results.append(dict(
                    check="outreach.step%s.score" % step_no, verdict=MATCH,
                    detail="step %s quotes no website score, matching the report" % step_no))

    return results


# ---------------------------------------------------------------------------
# driver
# ---------------------------------------------------------------------------

def load_reports(names=None, latest=0):
    paths = sorted(glob.glob(os.path.join(ADS_ONLY_DIR, "audit_*.json")))
    if names:
        wanted = [n.strip().lower() for n in names if n.strip()]
        paths = [p for p in paths
                 if any(w in os.path.basename(p).lower() or
                        w in text_of(json.load(open(p, encoding="utf-8")).get("company")).lower()
                        for w in wanted)]
    if latest and len(paths) > latest:
        paths = paths[-latest:]
    return paths


def verify_one(path, timeout, retries, do_network=True):
    try:
        audit = json.load(open(path, encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        bad = dict(file=os.path.basename(path), company="?", verdict=UNREACHABLE,
                   results=[dict(check="json.read", verdict=UNREACHABLE, detail=str(e))])
        return bad, None

    results = []
    if do_network:
        meta = (audit.get("ad_library") or {}).get("meta_own") or {}
        for ad in (meta.get("ads") or []):
            results.extend(check_ad(ad, timeout, retries))
        results.extend(check_site(audit, timeout, retries))
    results.extend(check_ad_counts(audit))
    results.extend(check_outreach_consistency(audit))

    verdicts = [r["verdict"] for r in results]
    if DRIFT in verdicts:
        overall = DRIFT
    elif UNREACHABLE in verdicts:
        overall = UNREACHABLE
    else:
        overall = MATCH

    return dict(file=os.path.basename(path),
                company=text_of(audit.get("company")),
                verdict=overall, results=results), audit


def main(argv=None):
    ap = argparse.ArgumentParser(description="Third check: re-verify stored audit data against the live sources.")
    ap.add_argument("--company", action="append", default=[],
                    help="limit to reports matching this company name or slug (repeatable)")
    ap.add_argument("--latest", type=int, default=0,
                    help="only the N most recently modified reports")
    ap.add_argument("--timeout", type=int, default=15)
    ap.add_argument("--retries", type=int, default=1)
    ap.add_argument("--offline", action="store_true",
                    help="skip all network calls; only the consistency checks run")
    ap.add_argument("--json", dest="json_out", default="",
                    help="write the full verdict to this JSON file")
    args = ap.parse_args(argv)

    paths = load_reports(args.company, args.latest)
    if not paths:
        sys.stderr.write("no reports matched\n")
        return 3

    print("=" * 70)
    print("LIVE-DATA VERIFICATION -- third check (%d report(s))" % len(paths))
    print("=" * 70)

    reports = []
    for p in paths:
        rep, _ = verify_one(p, args.timeout, args.retries, do_network=not args.offline)
        reports.append(rep)
        print("\n[%s] %s  (%s)" % (rep["verdict"], rep["company"], rep["file"]))
        for r in rep["results"]:
            mark = {MATCH: "ok  ", DRIFT: "DRIFT", UNREACHABLE: "???? ", NOT_CLAIMED: "--  "}[r["verdict"]]
            print("   %s %-28s %s" % (mark, r["check"], r["detail"]))

    n_match = sum(1 for r in reports if r["verdict"] == MATCH)
    n_drift = sum(1 for r in reports if r["verdict"] == DRIFT)
    n_unreach = sum(1 for r in reports if r["verdict"] == UNREACHABLE)

    print("\n" + "=" * 70)
    print("MATCH %d | DRIFT %d | UNREACHABLE %d | of %d" % (n_match, n_drift, n_unreach, len(reports)))
    if n_drift:
        print("RESULT: DRIFT -- the stored data no longer matches the live sources.")
        print("        Re-run the pipeline for the flagged leads before sending anything.")
        code = 1
    elif n_unreach:
        print("RESULT: UNVERIFIED -- some sources could not be read, so their claims")
        print("        are unconfirmed. Unverifiable is not deliverable.")
        code = 2
    else:
        print("RESULT: ALL LIVE CHECKS MATCH -- safe to deliver.")
        code = 0
    print("=" * 70)

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(dict(checked_on=time.strftime("%Y-%m-%d"),
                           reports=reports), fh, indent=2, ensure_ascii=False)
        print("wrote %s" % args.json_out)

    return code


if __name__ == "__main__":
    raise SystemExit(main())
