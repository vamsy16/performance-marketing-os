#!/usr/bin/env python3
"""Batch 15 - Telangana leads: build five audited PDFs from measured data.

Data source: batch15_telangana_data.py (every figure read live on 2026-11-28).
Renderer:    ads_only_report.build_measured() -> audit_pdf.generate_ads_only_pdf()

Usage (from 01-LEADS/):
    python3 build_batch15_telangana.py [--only "Galaxy"]
"""
import argparse
import sys

import ads_only_report as aos
from batch15_telangana_data import LEADS


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    args = ap.parse_args()

    leads = LEADS
    if args.only:
        leads = [l for l in LEADS if args.only.lower() in l["company"].lower()]
        if not leads:
            sys.exit(f"No lead matches {args.only!r}")

    print("=" * 70)
    print(f"BATCH 15 TELANGANA - {len(leads)} lead(s)")
    print("=" * 70)
    for lead in leads:
        json_path, pdf_path = aos.build_measured(lead)
        score = aos.__dict__.get("_last_score")
        print(f"[OK] {lead['company']:<24} {json_path}")
        print(f"     {'':<24} {pdf_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
