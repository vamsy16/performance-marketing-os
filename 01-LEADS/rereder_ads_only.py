#!/usr/bin/env python3
"""Re-render every ads-only PDF from the measured data already in its JSON.

The measured site data, ad-library cards, scores and control review all live in
``01-LEADS/ads_only_results/audit_<Company>.json``. Re-rendering from those files
needs no network and no browser, so the layout fixes (the verbatim ad-evidence
table, the verification log, the rupee-sign and ad-copy fixes) can be applied
to every existing report without re-measuring anything. Legacy ad-activity
sheets with no website read are re-rendered too - they carry the same live
ad data, and the same truncation bug was hiding their copy.

Run:  cd 01-LEADS && PYTHONPATH=/tmp/pdflibs python3 rereder_ads_only.py
"""
import glob
import json
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

from audit_pdf import generate_ads_only_pdf          # noqa: E402


def main():
    out = []
    for path in sorted(glob.glob(os.path.join(BASE, "ads_only_results",
                                              "audit_*.json"))):
        with open(path, encoding="utf-8") as f:
            audit = json.load(f)
        pdf = generate_ads_only_pdf(audit)
        out.append(pdf)
        print(f"  -> {os.path.basename(pdf)}")
    print(f"\nRe-rendered {len(out)} reports.")
    return out


if __name__ == "__main__":
    main()
