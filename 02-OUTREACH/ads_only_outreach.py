#!/usr/bin/env python3
"""
Ads-Only Outreach Engine — cold emails that deliver the LIVE-AD report.

For leads whose website audit has not run yet (no Playwright / no reachable
site), `01-LEADS/ads_only_report.py` produces an honest live-ad PDF. This
script turns those reports into the initial outreach email + the same
4-step threaded follow-up sequence used for full audits, so nothing about
the cadence changes — only the attachment does.

Usage:
  python ads_only_outreach.py --list                  # which leads have a report
  python ads_only_outreach.py --only "Truzon Solar"   # one lead
  python ads_only_outreach.py --export                # write generated_emails/*.txt

With --export this also refreshes generated_emails/sequence_manifest.json
(see GMAIL_DRAFT_WORKFLOW.md). Each sequence is tagged report_kind=ads_only,
which tells the Gmail workflow to attach 02-OUTREACH/ads_only_pdfs/*.pdf
instead of a full audit PDF.

Honesty rule baked in: every claim in these emails comes from the Meta Ad
Library data in 01-LEADS/ads_only_results/*.json. There is no website score,
no pixel/tracking claim and no page-speed number anywhere — the report the
lead receives says so on page 1, and so does the email.
"""

import argparse
import json
import os
import sys
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LEADS_DIR = os.path.join(os.path.dirname(BASE_DIR), "01-LEADS")
ADS_ONLY_JSON_DIR = os.path.join(LEADS_DIR, "ads_only_results")
ADS_ONLY_PDF_DIR = os.path.join(BASE_DIR, "ads_only_pdfs")
EMAILS_DIR = os.path.join(BASE_DIR, "generated_emails")

sys.path.insert(0, BASE_DIR)
import sequence as seq_engine
from audit_outreach import YOUR_SIGNATURE, YOUR_NAME, YOUR_AGENCY

# Words that must never appear in an ads-only email: they would claim a
# website audit that was never run.
FORBIDDEN = ["/100", "pagespeed", "page speed", "meta pixel", "google analytics",
             "no website found", "audit score", "website score", "seo score"]


def safe_name(name):
    return "".join(c if c.isalnum() else "_" for c in name)[:40]


def pdf_name(company):
    return f"audit_{safe_name(company)}.pdf"


def load_reports():
    """Every ads-only report, in a stable order (most live ads first)."""
    reports = []
    if not os.path.isdir(ADS_ONLY_JSON_DIR):
        return reports
    for filename in sorted(os.listdir(ADS_ONLY_JSON_DIR)):
        if not (filename.startswith("audit_") and filename.endswith(".json")):
            continue
        try:
            with open(os.path.join(ADS_ONLY_JSON_DIR, filename), "r",
                      encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue
        # Only ever treat a JSON that is explicitly ads-only as ads-only.
        if not data.get("ads_only"):
            continue
        company = (data.get("company") or "").strip()
        if not company:
            continue
        reports.append(data)
    reports.sort(key=lambda r: -(len((((r.get("ad_library") or {}).get(
        "meta_own") or {}).get("ads")) or [])))
    return reports


def meta_ads(report):
    return (((report.get("ad_library") or {}).get("meta_own") or {})
            .get("ads")) or []


def oldest_started(ads):
    """Oldest 'Started running on' date across a lead's live ads."""
    parsed = []
    for a in ads:
        raw = (a.get("started") or "").strip()
        for fmt in ("%d %b %Y", "%d %B %Y", "%b %d, %Y", "%B %d, %Y"):
            try:
                parsed.append(datetime.strptime(raw, fmt).date())
                break
            except ValueError:
                continue
    return min(parsed) if parsed else None


def lead_dict(report):
    return {
        "name": report["company"],
        "city": report.get("city", ""),
        "email": (report.get("contact") or {}).get("email", ""),
        "phone": (report.get("contact") or {}).get("phone", ""),
        "website": report.get("website", ""),
    }


# ---------------------------------------------------------------------------
# The initial email
# ---------------------------------------------------------------------------

def build_email(report):
    company = report["company"]
    city = report.get("city", "") or "your city"
    ads = meta_ads(report)
    funnel = (report.get("funnel") or {})
    findings = report.get("findings") or []
    checked = report.get("checked_on", "")

    bullets = []
    if ads:
        oldest = oldest_started(ads)
        since = oldest.strftime("%d %B %Y") if oldest else "recently"
        bullets.append(
            f"{len(ads)} live {'ad' if len(ads) == 1 else 'ads'} on Meta, "
            f"running since {since}")
        bullets.append(f"every click lands in {funnel.get('type', 'a paid funnel')}")
        for f in findings[:2]:
            bullets.append(f)
        # Only claim what the paid clicks are doing when there ARE paid clicks.
        scope = ("only what your paid clicks are doing, and where they are "
                 "being lost")
    else:
        # findings[0] already states the verified "no active ads" fact.
        for f in findings[:2]:
            bullets.append(f)
        scope = ("only what your ad presence is - and is not - doing in this "
                 "market")

    bullet_block = "\n".join(f"  - {b}" for b in bullets)

    if ads:
        links = "\n".join(
            f"  Library ID {a['library_id']}: {a['library_url']}"
            for a in ads[:3] if a.get("library_id") and a.get("library_url"))
        subject = (f"{company}: {len(ads)} live {city} "
                   f"{'ad' if len(ads) == 1 else 'ads'}, one funnel")
    else:
        links = ("  Meta Ad Library search: "
                 "https://www.facebook.com/ads/library/?active_status=active"
                 "&ad_type=all&country=IN&q=" + company.replace(" ", "%20"))
        subject = (f"{company}: no live ads while {city} competitors buy "
                   f"the same homeowner")

    body = f"""Hi,

I spend my week reading the public Meta Ad Library for the {city} solar market, and I put together a short report on what {company} is doing right now.

What it covers (pulled from the Ad Library on {checked or 'today'}):

{bullet_block}

You can verify every line yourself:

{links}

To be clear about what this is: it is an ad report, not a website audit. I have not audited your website, so there are no website findings in it - {scope}.

If any of it is useful I am happy to walk you through it on a 10-minute call. If not, the report is yours to keep.

Best,
{YOUR_SIGNATURE}
"""
    return subject, body, "ads_only_live_ad_report"


# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------

def export_email(report, subject, body, template):
    company = report["company"]
    os.makedirs(EMAILS_DIR, exist_ok=True)
    filepath = os.path.join(EMAILS_DIR, f"ads_only_email_{safe_name(company)}.txt")
    attachment = os.path.join(ADS_ONLY_PDF_DIR, pdf_name(company))
    has_pdf = os.path.exists(attachment)

    content = f"""=== EMAIL FOR: {company} ===
City: {report.get('city', '')}
To: {(report.get('contact') or {}).get('email', '') or '(no email found)'}
Phone: {(report.get('contact') or {}).get('phone', '') or 'N/A'}
Website: {report.get('website', '')}
Report kind: LIVE AD ACTIVITY (no website audit was run - the PDF says so on page 1)
ATTACH THIS: {attachment}{'' if has_pdf else '   <-- MISSING: run python 01-LEADS/ads_only_report.py first'}
Template: {template}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

--- SUBJECT ---
{subject}

--- BODY ---
{body}

=== END ===
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filepath, has_pdf


def check_honesty(company, subject, body):
    """Fail loudly if an ads-only email claims website-audit data."""
    blob = f"{subject}\n{body}".lower()
    bad = [w for w in FORBIDDEN if w in blob]
    if bad:
        raise SystemExit(
            f"REFUSING to generate '{company}': the email claims website "
            f"audit data that was never collected ({', '.join(bad)}). "
            "Ads-only emails may reference live ads only.")


def main():
    parser = argparse.ArgumentParser(
        description="Generate outreach emails for ads-only (live-ad) reports")
    parser.add_argument("--list", action="store_true",
                        help="List the ads-only reports available")
    parser.add_argument("--only", type=str, help="Specific company name")
    parser.add_argument("--export", action="store_true",
                        help="Save emails as .txt files + refresh the manifest")

    args = parser.parse_args()

    reports = load_reports()
    if not reports:
        print(f"No ads-only reports in {ADS_ONLY_JSON_DIR}.")
        print("Build them first: python ../01-LEADS/ads_only_report.py")
        return

    if args.list:
        print(f"{len(reports)} ads-only report(s):")
        for r in reports:
            n = len(meta_ads(r))
            print(f"  {r['company'][:34]:34} {n} live ad(s)   "
                  f"{(r.get('contact') or {}).get('email', '')}")
        return

    if args.only:
        reports = [r for r in reports
                   if args.only.lower() in r["company"].lower()]
        if not reports:
            print(f"No ads-only report matching '{args.only}'")
            return

    print("=" * 60)
    print(f"GENERATING {len(reports)} LIVE-AD OUTREACH EMAIL(S)")
    print("=" * 60)

    manifest = seq_engine.load_manifest()
    generated = 0
    missing_pdf = 0
    for i, report in enumerate(reports, 1):
        company = report["company"]
        print(f"\n[{i}/{len(reports)}] {company[:40]}")

        subject, body, template = build_email(report)
        check_honesty(company, subject, body)

        seq = seq_engine.upsert_sequence(
            manifest, lead_dict(report), report, subject, body, ads_only=True)
        print(f"  Sequence: {len(seq['steps'])} emails "
              f"(report_kind=ads_only, follow-ups every "
              f"{seq_engine.FOLLOWUP_DELAY_DAYS}d after previous send)")
        print(f"  Subject:  {subject}")
        print(f"  To:       {(report.get('contact') or {}).get('email', '') or '(no email - need to find)'}")

        if args.export:
            filepath, has_pdf = export_email(report, subject, body, template)
            generated += 1
            if not has_pdf:
                missing_pdf += 1
            print(f"  Saved:    {filepath}")
            print(f"  Attach:   {pdf_name(company)}"
                  f"{'' if has_pdf else '  <-- MISSING PDF'}")
        else:
            print(f"\n--- SUBJECT ---\n{subject}\n\n--- BODY ---\n{body}")

    if args.export:
        seq_engine.save_manifest(manifest)

    print(f"\n{'=' * 60}")
    print("SUMMARY")
    print("=" * 60)
    print(f"Emails generated:   {len(reports)}")
    print(f"With email address: {sum(1 for r in reports if (r.get('contact') or {}).get('email'))}")
    if args.export:
        print(f"Files saved to:     {EMAILS_DIR}")
        print(f"Sequence manifest:  {seq_engine.MANIFEST_FILE}")
    if missing_pdf:
        print(f"\nWARNING: {missing_pdf} report(s) have no PDF yet — run "
              "python ../01-LEADS/ads_only_report.py before drafting in Gmail.")

    print("\nNext steps:")
    print("1. Ask Arena: 'create Gmail drafts from the sequence manifest' "
          "(GMAIL_DRAFT_WORKFLOW.md)")
    print("2. The agent attaches the LIVE-AD PDF "
          "(02-OUTREACH/ads_only_pdfs/), never a full audit PDF, "
          "for report_kind=ads_only rows.")
    print("3. Review each draft in Gmail -> personalize -> SEND (manually).")
    print("4. When the full audit runs later, re-generate with "
          "audit_outreach.py --export to swap in the audited copy.")
    print(f"5. Track state: python sequence.py status | due")


if __name__ == "__main__":
    main()
