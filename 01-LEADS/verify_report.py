#!/usr/bin/env python3
"""
Report Verifier — automated quality gate for generated audit reports.

Checks the audit JSON and its PDF for everything that must be true before a
report is delivered: branding present, live ad data attached, honest
no-website handling, no placeholder text, no rendering artifacts, links intact.

Exit code 0 = PASS, 1 = FAIL. Run it after ANY pipeline/discovery run.

Usage:
  python verify_report.py --latest
  python verify_report.py --all
  python verify_report.py "Ksquare Energy"
"""

import argparse
import glob
import json
import os
import re
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = os.path.dirname(__file__)
AUDIT_DIR = os.path.join(BASE_DIR, "audit_results")
PDF_DIR = os.path.join(os.path.dirname(BASE_DIR), "02-OUTREACH", "audit_pdfs")

BRAND_NAME = "Vamsi"
BRAND_AGENCY = "Smart Pursuit"
BRAND_PHONE_TAIL = "70950 24220"
HEADER_LABEL = "ADS AUDIT REPORT"

SOCIAL_WEBSITE_RE = re.compile(r"facebook\.com|fb\.me|instagram\.com|whatsapp\.com", re.I)


def slug(name):
    return re.sub(r"[^a-zA-Z0-9]+", "_", name)[:50]


def all_audits():
    files = sorted(glob.glob(os.path.join(AUDIT_DIR, "audit_*.json")),
                   key=os.path.getmtime, reverse=True)
    out = []
    for path in files:
        try:
            with open(path, "r", encoding="utf-8") as f:
                out.append((path, json.load(f)))
        except Exception:
            continue
    return out


def find(target):
    tl = target.lower()
    for path, audit in all_audits():
        if tl in (audit.get("company") or "").lower():
            return path, audit
    return None, None


def check_json(audit, errs):
    company = audit.get("company") or ""
    if not company:
        errs.append("JSON: missing company name")
    if not audit.get("audit_date") and not audit.get("discovery"):
        errs.append("JSON: missing audit_date (stale/templated data?)")

    website = audit.get("website") or ""
    if SOCIAL_WEBSITE_RE.search(website):
        errs.append(f"JSON: '{website}' is a social/chat URL, not a website - "
                    "must be flagged no_website=True (fb.me audit bug)")
    if audit.get("no_website"):
        for k in ("pixels", "seo", "pagespeed", "conversion"):
            if k in audit:
                errs.append(f"JSON: no_website lead still carries a '{k}' section "
                            "(leftover fake website audit)")

    adlib = audit.get("ad_library")
    if not adlib:
        errs.append("JSON: ad_library missing - PDF would show NO live ad data. "
                    "Re-run ad_library.py / discover_leads.py")
        return
    if not adlib.get("summary"):
        errs.append("JSON: ad_library.summary missing (executive summary would be generic)")
    meta_own = adlib.get("meta_own") or {}
    if meta_own.get("ads"):
        for ad in meta_own["ads"][:3]:
            if not ad.get("library_id"):
                errs.append(f"JSON: meta ad missing library_id ({ad.get('page_name')})")
            if not ad.get("library_url"):
                errs.append(f"JSON: meta ad missing library_url live link ({ad.get('page_name')})")
    google = adlib.get("google_own") or {}
    if google.get("found") and not (google.get("detail") or {}).get("url"):
        errs.append("JSON: Google advertiser marked found but has no transparency URL")
    for key in ("meta_competitors", "google_competitors"):
        if key not in adlib:
            errs.append(f"JSON: ad_library.{key} missing")


def check_pdf(audit, pdf_path, errs):
    company = audit.get("company") or ""
    if not os.path.exists(pdf_path):
        errs.append(f"PDF: not found at {pdf_path}")
        return
    size = os.path.getsize(pdf_path)
    if size < 30_000:
        errs.append(f"PDF: only {size} bytes - likely broken/empty render")

    try:
        from pypdf import PdfReader
        reader = PdfReader(pdf_path)
    except Exception as e:
        errs.append(f"PDF: cannot parse ({e})")
        return

    pages = len(reader.pages)
    if pages < 3:
        errs.append(f"PDF: only {pages} pages - expected >= 3 for a full report")

    meta = getattr(reader, "metadata", None) or getattr(reader, "meta", None) or {}
    try:
        author = str(meta.get("/Author") or "")
    except Exception:
        author = str(getattr(meta, "author", "") or "")
    if BRAND_NAME not in author:
        errs.append(f"PDF: author metadata '{author}' missing '{BRAND_NAME}'")

    text = " ".join((p.extract_text() or "") for p in reader.pages)
    flat = " ".join(text.split())

    for needle, label in [
        (BRAND_NAME, "brand name 'Vamsi'"),
        (BRAND_AGENCY, "agency 'Smart Pursuit'"),
        (BRAND_PHONE_TAIL, "phone tail '70950 24220'"),
        (HEADER_LABEL, f"header '{HEADER_LABEL}'"),
        ("Prepared by", "footer 'Prepared by'"),
    ]:
        if needle not in flat:
            errs.append(f"PDF: missing {label}")

    if company and company not in flat:
        errs.append(f"PDF: company name '{company}' not found in text")

    for artifact in ("&amp;", "&lt;", "&gt;", "YOUR NAME", "YOUR_AGENCY", "XXXXX"):
        if artifact in flat:
            errs.append(f"PDF: rendering artifact/placeholder found: '{artifact}'")

    if "\ufffd" in text:
        errs.append("PDF: replacement chars () present - encoding problem")

    adlib = audit.get("ad_library") or {}
    meta_ads = (adlib.get("meta_own") or {}).get("ads") or []
    comp_ads = (adlib.get("meta_competitors") or {}).get("ads") or []

    if meta_ads and "Library ID" not in flat:
        errs.append("PDF: has live Meta ads in data but no 'Library ID' in PDF")
    if (meta_ads or comp_ads) and "Open the live ad" not in flat:
        errs.append("PDF: ad creatives present but no 'Open the live ad' link text")
    if adlib and "Executive summary" not in flat:
        errs.append("PDF: missing executive summary")

    if audit.get("no_website"):
        if "NO WEBSITE FOUND" not in flat:
            errs.append("PDF: no_website lead must show 'NO WEBSITE FOUND' panel")
    else:
        if "/100" not in flat:
            errs.append("PDF: missing audit score display")

    try:
        images = []
        for p in reader.pages:
            images.extend(list(p.images))
        expected_min = 1 if meta_ads or comp_ads else 1
        if len(images) < expected_min:
            errs.append(f"PDF: only {len(images)} images - logo (and ad creatives) missing")
        if meta_ads and len(images) < 2:
            errs.append("PDF: has Meta ads but < 2 images - ad creative likely missing")
    except Exception as e:
        errs.append(f"PDF: image check failed ({e})")


def verify(audit_path, audit):
    errs = []
    company = audit.get("company") or audit_path
    check_json(audit, errs)
    pdf_path = os.path.join(PDF_DIR, f"audit_{slug(company)}.pdf")
    check_pdf(audit, pdf_path, errs)
    return company, pdf_path, errs


def main():
    parser = argparse.ArgumentParser(description="Verify generated audit reports")
    parser.add_argument("target", nargs="?", help="Company name")
    parser.add_argument("--latest", action="store_true")
    parser.add_argument("--all", action="store_true", dest="all")
    args = parser.parse_args()

    audits = all_audits()
    if not audits:
        print("FAIL: no audit JSONs found in audit_results/")
        sys.exit(1)

    if args.all:
        jobs = audits
    elif args.latest:
        jobs = audits[:1]
    elif args.target:
        path, audit = find(args.target)
        if not audit:
            print(f"FAIL: no audit matches '{args.target}'")
            sys.exit(1)
        jobs = [(path, audit)]
    else:
        jobs = audits[:1]

    any_fail = False
    print("=" * 60)
    print(f"REPORT VERIFICATION ({len(jobs)} report(s))")
    print("=" * 60)
    for path, audit in jobs:
        company, pdf_path, errs = verify(path, audit)
        status = "PASS" if not errs else "FAIL"
        if errs:
            any_fail = True
        print(f"\n[{status}] {company}")
        print(f"  json: {os.path.basename(path)}")
        print(f"  pdf:  {os.path.basename(pdf_path)}")
        for e in errs:
            print(f"  x {e}")
        if not errs:
            print("  all checks passed: branding, live ad links, score panel, "
                  "images, no placeholder text")

    print("\n" + "=" * 60)
    print("VERIFICATION:", "FAILED - fix issues above before delivering" if any_fail
          else "ALL REPORTS PASS - safe to deliver")
    print("=" * 60)
    sys.exit(1 if any_fail else 0)


if __name__ == "__main__":
    main()
