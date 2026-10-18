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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ads_audit import run_audit, save_audit, print_audit_report
from ad_library import run_research, save_audit as save_merged
from audit_pdf import generate_pdf


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

    print("=" * 60)
    print(f"SMART PURSUIT ADS AUDIT PIPELINE: {args.company}")
    print("=" * 60)

    # --- Step 1: Website audit (live fetch) ---
    if args.skip_audit:
        print("\n[1/3] Website audit SKIPPED (--skip-audit)")
        audit_path, audit = None, None
        from ad_library import find_audit, all_audits
        audit_path, audit = find_audit(args.company)
        if not audit:
            print("ERROR: no existing audit found to reuse. Run without --skip-audit first.")
            sys.exit(1)
        print(f"  Reusing: {audit_path}")
    else:
        print(f"\n[1/3] Auditing website: {args.website}")
        audit = run_audit(args.website, company_name=args.company, city=args.city)
        if "error" in audit:
            print(f"  Website audit error: {audit['error']}")
            print("  Continuing with ad research only...")
        else:
            print_audit_report(audit)
        audit_path = save_audit(audit)

    # --- Step 2: Live ad-library research (Meta + Google) ---
    if args.skip_ads:
        print("\n[2/3] Ad-library research SKIPPED (--skip-ads)")
    else:
        print(f"\n[2/3] Pulling LIVE ad data for: {args.company}")
        ad_data = run_research(args.company, city=args.city,
                               website=args.website, competitors=args.competitors)
        audit["ad_library"] = ad_data
        audit_path = save_merged(audit, audit_path)
        print(f"\n  SUMMARY: {ad_data.get('summary', '')}")
        print(f"  Meta own ads:     {ad_data['meta_own']['results_label'] or 'none'}")
        g_det = ad_data["google_own"].get("detail") or {}
        print(f"  Google own ads:   {g_det.get('ad_count', 'none found')}")
        print(f"  Competitor ads:   meta={len(ad_data['meta_competitors']['ads'])}, "
              f"google advertisers={len(ad_data['google_competitors']['advertisers'])}")

    # --- Step 3: Branded PDF ---
    print(f"\n[3/3] Generating branded PDF...")
    pdf_path = generate_pdf(audit)
    size_kb = os.path.getsize(pdf_path) // 1024 if os.path.exists(pdf_path) else 0

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
