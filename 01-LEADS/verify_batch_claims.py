#!/usr/bin/env python3
"""3rd-eye check: print every checkable claim in a batch's JSONs on one sheet.

Run this AFTER the reports are built and BEFORE anything is emailed. It does
not prove anything by itself - it exists so each claim can be re-opened at its
source (the Ad Library card, the live page) and ticked off one at a time.

    cd 01-LEADS && python3 verify_batch_claims.py Growcell_Solar_Energy ...

Prints, per lead: every ad ID + the started date + page name recorded, every
contact fact, every price/phone/email-looking string in the ad copy, and every
finding sentence that contains a number. Exit code 1 if an ad ID is not a
15-19 digit string or a JSON is missing a required key.
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
AUDIT_DIR = os.path.join(BASE, "ads_only_results")
REQUIRED = ["company", "city", "checked_on", "ad_library", "funnel",
            "findings", "next_steps", "contact_facts", "contact", "audit_date"]

NUM = re.compile(r"(?:Rs\.?\s?[\d,]+|₹\s?[\d,]+|\+?91[\s-]?\d[\d\s-]{7,}|\b\d[\d,]{4,}\b|\b\d{2,4}\s?(?:kW|kWp)\b)")


def load(slug):
    path = os.path.join(AUDIT_DIR, f"audit_{slug}.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main(slugs):
    problems = []
    for slug in slugs:
        try:
            d = load(slug)
        except OSError:
            problems.append(f"{slug}: no JSON")
            continue
        print("=" * 78)
        print(f"{d.get('company')}  |  {d.get('city')}  |  read {d.get('checked_on')}")
        print(f"website: {d.get('website') or '(none)'}   site_audit: {bool(d.get('site_audit'))}")
        for k in REQUIRED:
            if k not in d:
                problems.append(f"{slug}: missing key {k}")
        ads = ((d.get("ad_library") or {}).get("meta_own") or {}).get("ads") or []
        print(f"\n-- ADS ({len(ads)}) : re-open each one and check ID + page + date")
        for a in ads:
            lid = str(a.get("library_id", ""))
            if not re.fullmatch(r"\d{15,19}", lid):
                problems.append(f"{slug}: bad library_id {lid!r}")
            print(f"  {lid:<18} {a.get('started','?'):<14} {a.get('page_name','?')}")
            for tok in sorted(set(NUM.findall(a.get("text", "")))):
                print(f"        copy number: {tok.strip()}")
        print("\n-- CONTACT FACTS : confirm each at its own source")
        for pair in d.get("contact_facts") or []:
            k, v = pair[0], pair[1] if len(pair) > 1 else ""
            print(f"  {k}: {v}")
        c = d.get("contact") or {}
        if not c.get("phone"):
            problems.append(f"{slug}: no contact.phone")
        print("\n-- FINDINGS CONTAINING A NUMBER : the sentences most likely to be wrong")
        for f in d.get("findings") or []:
            if NUM.search(f):
                print(f"  * {f}")
        if len(d.get("findings") or []) < 5:
            problems.append(f"{slug}: fewer than 5 findings")
        print()
    print("=" * 78)
    if problems:
        print("PROBLEMS:")
        for p in problems:
            print("  !", p)
        return 1
    print(f"OK: {len(slugs)} report(s) structurally complete. Claims still need "
          f"re-opening at source.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
