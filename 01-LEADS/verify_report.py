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
  python verify_report.py --ads-only      # ads-only (live ad activity) reports
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
ADS_ONLY_DIR = os.path.join(BASE_DIR, "ads_only_results")
ADS_ONLY_PDF_DIR = os.path.join(os.path.dirname(BASE_DIR), "02-OUTREACH", "ads_only_pdfs")

BRAND_NAME = os.environ.get("SP_NAME", "Vamsi")
BRAND_AGENCY = os.environ.get("SP_AGENCY", "Smart Pursuit")
BRAND_PHONE_TAIL = os.environ.get("SP_PHONE", "+91 70950 24220").replace("+91 ", "")
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


# ---------------------------------------------------------------------------
# Ads-only reports (live ad activity, website audit NOT run)
#
# Built by ads_only_report.py when the website half of the audit cannot run
# (no Playwright/Chrome). The gate here is deliberately strict in the opposite
# direction to the full reports: they must carry the live ad evidence AND must
# not pretend to be a website audit.
# ---------------------------------------------------------------------------

ADS_ONLY_LABEL = "LIVE AD ACTIVITY"
ADS_ONLY_PENDING = "WEBSITE AUDIT NOT RUN"
FORBIDDEN_IN_ADS_ONLY = ("/100", "MISSING", "NO WEBSITE FOUND", "YOUR NAME", "XXXXX")


def check_ads_only_json(audit, errs):
    if not audit.get("ads_only"):
        errs.append("JSON: ads_only flag missing - is this really an ads-only report?")
    if audit.get("website_audit_run"):
        errs.append("JSON: website_audit_run is True but no website audit data is present")
    if not audit.get("checked_on"):
        errs.append("JSON: checked_on missing - when was the ad data read?")
    if not audit.get("website", "").startswith("http"):
        errs.append("JSON: website missing - an ads-only lead still needs a live site URL")
    if audit.get("no_website"):
        errs.append("JSON: no_website set on a lead that has a website")

    # No website-audit sections at all - their absence is the honesty guarantee.
    for k in ("score", "pixels", "seo", "pagespeed", "conversion", "page_count"):
        if k in audit:
            errs.append(f"JSON: ads-only report carries a '{k}' section "
                        "(website audit data it cannot have)")

    adlib = audit.get("ad_library")
    if not adlib:
        errs.append("JSON: ad_library missing")
        return
    if not adlib.get("summary"):
        errs.append("JSON: ad_library.summary missing")
    meta_own = adlib.get("meta_own") or {}
    ads = meta_own.get("ads") or []
    if meta_own.get("found") and not ads:
        errs.append("JSON: meta_own.found is True but no ads are attached")
    if not meta_own.get("found") and ads:
        errs.append("JSON: ads attached but meta_own.found is False")
    for ad in ads:
        if not ad.get("library_id"):
            errs.append(f"JSON: ad missing library_id ({ad.get('page_name')})")
        if not ad.get("library_url"):
            errs.append(f"JSON: ad missing library_url live link ({ad.get('page_name')})")
        if not ad.get("text"):
            errs.append(f"JSON: ad missing copy ({ad.get('page_name')})")
    if not audit.get("funnel"):
        errs.append("JSON: funnel section missing (where the ad clicks land)")


def check_ads_only_pdf(audit, pdf_path, errs):
    company = audit.get("company") or ""
    if not os.path.exists(pdf_path):
        errs.append(f"PDF: not found at {pdf_path}")
        return
    size = os.path.getsize(pdf_path)
    # Ads-only reports carry no ad creatives (they cannot be downloaded without
    # a browser), so a text-only branded report is ~10-14 KB.
    if size < 8_000:
        errs.append(f"PDF: only {size} bytes - likely broken/empty render")

    try:
        from pypdf import PdfReader
        reader = PdfReader(pdf_path)
    except Exception as e:
        errs.append(f"PDF: cannot parse ({e})")
        return

    if len(reader.pages) < 2:
        errs.append(f"PDF: only {len(reader.pages)} pages - expected >= 2")

    meta = getattr(reader, "metadata", None) or {}
    try:
        author = str(meta.get("/Author") or "")
    except Exception:
        author = ""
    if BRAND_NAME not in author:
        errs.append(f"PDF: author metadata '{author}' missing '{BRAND_NAME}'")

    text = " ".join((p.extract_text() or "") for p in reader.pages)
    flat = " ".join(text.split())

    for needle, label in [
        (BRAND_NAME, "brand name"),
        (BRAND_AGENCY, "agency"),
        (BRAND_PHONE_TAIL, "phone tail"),
        ("ADS AUDIT REPORT", "header 'ADS AUDIT REPORT'"),
        ("Prepared by", "footer 'Prepared by'"),
        (ADS_ONLY_LABEL, "label 'LIVE AD ACTIVITY'"),
        (ADS_ONLY_PENDING, "honesty panel 'WEBSITE AUDIT NOT RUN'"),
    ]:
        if needle not in flat:
            errs.append(f"PDF: missing {label}")

    if company and company not in flat:
        errs.append(f"PDF: company name '{company}' not found in text")

    ads = (audit.get("ad_library") or {}).get("meta_own", {}).get("ads") or []
    for ad in ads[:3]:
        if ad.get("library_id") and ad["library_id"] not in flat:
            errs.append(f"PDF: Library ID {ad['library_id']} missing from the report")
    if ads and "Open the live ad" not in flat:
        errs.append("PDF: live ads present but no 'Open the live ad' link text")

    for artifact in FORBIDDEN_IN_ADS_ONLY:
        if artifact in flat:
            errs.append(f"PDF: forbidden in an ads-only report: '{artifact}' "
                        "(would imply a website audit that was not run)")


def verify_ads_only(audit_path, audit):
    errs = []
    company = audit.get("company") or audit_path
    check_ads_only_json(audit, errs)
    pdf_path = os.path.join(ADS_ONLY_PDF_DIR, f"audit_{slug(company)}.pdf")
    check_ads_only_pdf(audit, pdf_path, errs)
    return company, pdf_path, errs


def run_ads_only():
    files = sorted(glob.glob(os.path.join(ADS_ONLY_DIR, "audit_*.json")),
                   key=os.path.getmtime, reverse=True)
    audits = []
    for path in files:
        try:
            with open(path, "r", encoding="utf-8") as f:
                audits.append((path, json.load(f)))
        except Exception:
            continue
    if not audits:
        print(f"FAIL: no ads-only reports found in {ADS_ONLY_DIR}")
        print("Build them with:  python ads_only_report.py")
        sys.exit(1)

    any_fail = False
    print("=" * 60)
    print(f"ADS-ONLY REPORT VERIFICATION ({len(audits)} report(s))")
    print("=" * 60)
    for path, audit in audits:
        company, pdf_path, errs = verify_ads_only(path, audit)
        status = "PASS" if not errs else "FAIL"
        if errs:
            any_fail = True
        print(f"\n[{status}] {company}")
        print(f"  json: {os.path.basename(path)}")
        print(f"  pdf:  {os.path.basename(pdf_path)}")
        for e in errs:
            print(f"  x {e}")
        if not errs:
            print("  all checks passed: live ad evidence, branding, honesty panel, "
                  "no fake website-audit data")
    print("\n" + "=" * 60)
    print("VERIFICATION:", "FAILED - fix issues above before delivering" if any_fail
          else "ALL ADS-ONLY REPORTS PASS - safe to deliver as live-ad reports")
    print("=" * 60)
    sys.exit(1 if any_fail else 0)


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
    parser.add_argument("--ads-only", action="store_true", dest="ads_only",
                        help="verify the ads-only (live ad activity) reports instead")
    args = parser.parse_args()

    if args.ads_only:
        run_ads_only()

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
