#!/usr/bin/env python3
"""
Smart Pursuit Ads Audit Pipeline — one command, live data, branded PDF.

Runs the full chain end-to-end:
  1. Website audit  (ads_audit.py)    — fetches the lead's live website
  2. Ad research    (ad_library.py)   — pulls LIVE Meta + Google ad-library data
  3. PDF report     (audit_pdf.py)    — builds the branded Smart Pursuit PDF

Every run fetches fresh live data — nothing is cached or reused. The PDF
always reflects the lead's website and ad activity at the moment you run it.

Usage:
  python run_pipeline.py <website> "<Company Name>" --city <City>
  python run_pipeline.py https://www.ksquareenergy.com/solar-company-in-hyderabad "Ksquare Energy" --city Hyderabad
"""

import argparse
import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ads_audit import run_audit, save_audit, print_audit_report
from ad_library import run_research, save_audit as save_merged
from audit_completeness import unresolved as unresolved_checks
from audit_pdf import generate_pdf


def _parsed_stamp(value):
    """Parse the timestamp formats this repo has historically written."""
    if not value:
        return None
    text = str(value).strip()
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        pass
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d", "%d %b %Y"):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    return None


def _fresh(value, max_age_minutes=1440):
    dt = _parsed_stamp(value)
    if dt is None:
        return False
    if dt.tzinfo is not None:
        dt = dt.replace(tzinfo=None)
    return abs((datetime.now() - dt).total_seconds()) <= max_age_minutes * 60


def _numeric_score(audit):
    site = audit.get("site_audit") or audit
    score = (site.get("score") or {}).get("score")
    return isinstance(score, (int, float)) and not isinstance(score, bool)


def main():
    parser = argparse.ArgumentParser(
        description="Full audit: website + live ad libraries + branded PDF")
    parser.add_argument("website", help="Lead website URL (https://...)")
    parser.add_argument("company", help="Company name as it appears in ads")
    parser.add_argument("--city", default="", help="City for competitor research")
    parser.add_argument("--competitors", type=int, default=3, help="Competitor ads to keep")
    parser.add_argument("--skip-audit", action="store_true",
                        help="Skip website audit, only refresh ad data + PDF")
    parser.add_argument("--skip-ads", action="store_true",
                        help="Skip ad-library research, only website audit + PDF")
    args = parser.parse_args()

    if args.skip_audit and args.skip_ads:
        print("ERROR: --skip-audit and --skip-ads together cannot produce a fresh "
              "full audit. Refusing to generate a PDF from nothing.")
        sys.exit(1)

    print("=" * 60)
    print(f"SMART PURSUIT ADS AUDIT PIPELINE: {args.company}")
    print("=" * 60)

    # --- Step 1: Website audit (live fetch) ---
    if args.skip_audit:
        print("\n[1/3] Website audit SKIPPED (--skip-audit)")
        from ad_library import find_audit
        audit_path, audit = find_audit(args.company)
        if not audit:
            print("ERROR: no existing audit found to reuse. Run without --skip-audit first.")
            sys.exit(1)
        if "error" in audit or audit.get("review_pending"):
            print("ERROR: the reuse candidate is an errored/held audit. Refresh it live.")
            sys.exit(1)
        if not _fresh(audit.get("audit_date")) or not _numeric_score(audit):
            print("ERROR: the reuse candidate is stale or has no measured score. "
                  "Run without --skip-audit to re-read the live site.")
            sys.exit(1)
        missing = unresolved_checks(audit)
        if missing:
            print("ERROR: the reuse candidate has unresolved website checks: "
                  + ", ".join(missing))
            print("Run without --skip-audit to re-read the live site.")
            sys.exit(1)
        print(f"  Reusing: {audit_path}")
    else:
        print(f"\n[1/3] Auditing website: {args.website}")
        audit = run_audit(args.website, company_name=args.company, city=args.city)
        # Fail closed. A site that could not be read must never be turned into
        # a polished 0/100 report or an ad-only PDF that looks like a full audit.
        if "error" in audit:
            print(f"  Website audit error: {audit['error']}")
            print("  ERROR: no live website data was read. No PDF was generated.")
            sys.exit(1)
        if not _numeric_score(audit):
            print("  ERROR: website audit produced no measurable score. No PDF was generated.")
            sys.exit(1)
        missing = unresolved_checks(audit)
        if missing:
            print("  ERROR: website audit left mandatory checks unresolved: "
                  + ", ".join(missing))
            print("  Re-read the live page (direct fetch / W3C showsource) and re-run. "
                  "A full audit with 'Not checked in this pass' is a hold, not a deliverable.")
            sys.exit(1)
        print_audit_report(audit)
        audit["site_evidence"] = {
            "pixel": (audit.get("pixels") or {}).get("meta_pixel"),
            "checked_on": audit.get("audit_date"),
            "note": "Read from the audited page source.",
        }
        audit_path = save_audit(audit)

    # --- Step 2: Live ad-library research (Meta + Google) ---
    if args.skip_ads:
        print("\n[2/3] Ad-library research SKIPPED (--skip-ads)")
        ad_data = (audit.get("ad_library") or {})
        if not ad_data.get("meta_own", {}).get("ads") or not _fresh(ad_data.get("checked_at")):
            print("ERROR: --skip-ads requires a fresh ad_library with attributed live ads "
                  "already in the audit. Run without --skip-ads.")
            sys.exit(1)
    else:
        print(f"\n[2/3] Pulling LIVE ad data for: {args.company}")
        ad_data = run_research(args.company, city=args.city,
                               website=args.website, competitors=args.competitors)
        meta = ad_data.get("meta_own") or {}
        if meta.get("error") or meta.get("status") == "unreachable":
            print(f"  ERROR: Meta Ad Library was unreachable ({meta.get('error')}). "
                  "No absence claim, no PDF.")
            sys.exit(1)
        if not meta.get("ads"):
            print("  ERROR: no live ads could be attributed to this advertiser. "
                  "A zero-Live-ad lead gets no audit PDF (owner rule).")
            sys.exit(1)
        google = ad_data.get("google_own") or {}
        if google.get("error") or google.get("status") == "unreachable":
            print(f"  ERROR: Google Ads Transparency was unreachable ({google.get('error')}). "
                  "No PDF with an unverified Google claim.")
            sys.exit(1)
        audit["ad_library"] = ad_data
        audit["checked_on"] = ad_data.get("checked_at") or audit.get("audit_date")
        destinations = [ad.get("destination") for ad in meta.get("ads") or []
                        if ad.get("destination")]
        if destinations:
            destination = destinations[0]
            audit["funnel"] = {
                "type": ("Lead form / off-site" if ("fb.me" in destination.lower()
                                                    or "lead form" in destination.lower())
                         else "Website"),
                "destination": destination,
            }
        audit["provenance"] = {
            "generator": "run_pipeline.py",
            "run_at": datetime.now().isoformat(timespec="seconds"),
            "python": sys.version.split()[0],
            "browser": "chrome",
            "live_reads": {
                "website": audit.get("audit_date"),
                "ads": ad_data.get("checked_at"),
            },
        }
        audit_path = save_merged(audit, audit_path)
        print(f"\n  SUMMARY: {ad_data.get('summary', '')}")
        print(f"  Meta own ads:     {ad_data['meta_own']['results_label'] or 'none'}")
        g_det = ad_data["google_own"].get("detail") or {}
        print(f"  Google own ads:   {g_det.get('ad_count', 'none found')}")
        print(f"  Competitor ads:   meta={len(ad_data['meta_competitors']['ads'])}, "
              f"google advertisers={len(ad_data['google_competitors']['advertisers'])}")

    # A report with no verified source date is an internal hold, never an
    # audit. The delivery gate checks this too; fix the data, not the gate.
    checked_on = (ad_data.get("checked_at") or audit.get("checked_on")
                  or audit.get("audit_date"))
    if not _fresh(checked_on):
        print("ERROR: no fresh, verified source date for this report. "
              "Re-run the full pipeline; no PDF was generated.")
        sys.exit(1)
    if audit.get("checked_on") != checked_on:
        audit["checked_on"] = checked_on
        save_merged(audit, audit_path)

    # --- Step 3: Branded PDF ---
    # Guard: never build a report out of nothing. If the website fetch
    # failed AND we have no live ad data, a PDF would be an empty shell —
    # refuse loudly instead of producing a deliverable-looking fake.
    has_ads = bool((audit.get("ad_library") or {}).get("meta_own", {}).get("found")
                   or (audit.get("ad_library") or {}).get("google_own", {}).get("found"))
    if "error" in audit and not has_ads:
        print("\nERROR: website audit failed and no live ads were found — "
              "refusing to generate an empty PDF.")
        print(f"  Fetch error: {audit['error']}")
        print("  Check the URL / network and re-run. Nothing was delivered.")
        sys.exit(1)

    print(f"\n[3/3] Generating branded PDF...")
    pdf_path = generate_pdf(audit)
    size_kb = os.path.getsize(pdf_path) // 1024 if os.path.exists(pdf_path) else 0

    # The pipeline itself refuses to print DONE unless the PDF passes the
    # delivery gate. This is what stops a partial/ad-hoc draft from being
    # mistaken for a finished report.
    from delivery_gate import gate_company
    ok, lines = gate_company(args.company, pdf_path=pdf_path)
    print("\n  DELIVERY GATE:")
    for line in lines:
        print(f"    {line}")
    if not ok:
        print("\n  ERROR: delivery gate FAILED. The PDF is NOT deliverable.")
        print("  Fix the cause and re-run; do not hand-edit the PDF or JSON.")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("DONE")
    print("=" * 60)
    print(f"  Company:  {audit.get('company')}")
    print(f"  Score:    {audit.get('score', {}).get('score', '?')}/100")
    print(f"  Audit:    {audit_path}")
    print(f"  PDF:      {pdf_path}  ({size_kb} KB)")
    print(f"\n  Attach the PDF to your outreach (templates in 02-OUTREACH/templates/)")


if __name__ == "__main__":
    main()
