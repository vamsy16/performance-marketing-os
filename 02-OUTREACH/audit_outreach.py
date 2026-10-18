#!/usr/bin/env python3
"""
Audit Outreach Engine — Generates personalized cold emails from audit findings.
Takes your audit results and writes ready-to-send emails.

Usage:
  python audit_outreach.py                          # Generate emails for all audited leads
  python audit_outreach.py --top 5                  # Only top 5 by opportunity
  python audit_outreach.py --name "SunTech Solar"   # Specific company
  python audit_outreach.py --export emails          # Save as .txt files for copy-paste
"""

import argparse
import io
import json
import os
import re
import sys
from datetime import datetime

# Fix Windows console encoding for Unicode
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = os.path.dirname(__file__)
LEADS_DIR = os.path.join(os.path.dirname(BASE_DIR), "01-LEADS")
AUDIT_DIR = os.path.join(LEADS_DIR, "audit_results")
LEADS_CSV = os.path.join(LEADS_DIR, "leads.csv")
EMAILS_DIR = os.path.join(BASE_DIR, "generated_emails")

# Your details — override with env vars SP_NAME / SP_AGENCY / SP_PHONE
YOUR_NAME = os.environ.get("SP_NAME", "Vamsi")
YOUR_AGENCY = os.environ.get("SP_AGENCY", "Smart Pursuit")
YOUR_PHONE = os.environ.get("SP_PHONE", "+91 70950 24220")
YOUR_SIGNATURE = f"{YOUR_NAME}\n{YOUR_AGENCY}\n{YOUR_PHONE}"


# ---------------------------------------------------------------------------
# Email Templates (3 variants — pick based on situation)
# ---------------------------------------------------------------------------

def template_audit_hook(lead, audit):
    """
    Template 1: The Audit Hook (best for companies with LOW scores = lots of issues)
    Lead with specific findings. No pitch. Just value.
    """
    name = lead.get("name", "there")
    city = lead.get("city", "")
    issues = audit.get("score", {}).get("issues", [])
    score = audit.get("score", {}).get("score", 0)

    # Pick the 2 most impactful issues
    top_issues = issues[:2] if issues else ["a few things I noticed"]
    issue_bullets = "\n".join(f"  • {issue}" for issue in top_issues)

    subject = f"Quick question about {name}'s website"

    body = f"""Hi,

I was looking at solar companies in {city} and came across {name}.

I ran a quick check on your website and found a couple of things that might be costing you leads:

{issue_bullets}

Your current website score is {score}/100 — there's some quick wins available that could help convert more visitors into enquiries.

I recorded a short video walking through exactly what I found and what I'd fix. Want me to send it over?

No strings attached — it's yours to keep whether we ever work together or not.

Best,
{YOUR_SIGNATURE}
"""
    return subject, body, "audit_hook"


def template_competitor_gap(lead, audit):
    """
    Template 2: The Competitor Gap (best when they're missing tracking/ads)
    Frame it as: your competitors are doing X, you're not.
    """
    name = lead.get("name", "there")
    city = lead.get("city", "")
    issues = audit.get("score", {}).get("issues", [])
    pixels = audit.get("pixels", {})

    # Determine the "gap"
    gaps = []
    if not pixels.get("meta_pixel"):
        gaps.append("not being able to run retargeting ads to people who visited their site")
    if not pixels.get("google_ads") and not pixels.get("google_tag_manager"):
        gaps.append("having no way to measure which marketing is actually working")
    if not pixels.get("google_analytics_ga4") and not pixels.get("google_analytics_ua"):
        gaps.append("not knowing how many people visit their website each month")

    if not gaps:
        gaps = ["a few missed opportunities in their online setup"]

    gap_list = "\n".join(f"  • {g}" for g in gaps[:2])

    subject = f"Noticed something about {name}'s online presence"

    body = f"""Hi,

I specialize in helping solar companies in {city} get more installation enquiries.

When I looked at {name}'s online setup, I noticed a few gaps that are pretty common (but costly):

{gap_list}

Most solar companies I work with fix these in the first week — and immediately know whether their marketing is working or not.

Would you be open to a free 10-minute call where I walk you through exactly what I found and what I'd recommend? No pitch — just useful info.

Either way, keep up the good work with solar in {city}.

Best,
{YOUR_SIGNATURE}
"""
    return subject, body, "competitor_gap"


def template_speed_urgent(lead, audit):
    """
    Template 3: Speed / Mobile Urgency (best when mobile score is very low)
    Data shows slow sites lose 50%+ of mobile visitors.
    """
    name = lead.get("name", "there")
    city = lead.get("city", "")
    perf = audit.get("pagespeed", {}).get("mobile_performance_score")
    lcp = audit.get("pagespeed", {}).get("largest_contentful_paint", "N/A")

    if perf is None:
        perf = 45  # default if no data

    lost_pct = max(20, min(60, 100 - perf))  # rough estimate

    subject = f"{name} may be losing {lost_pct}% of mobile visitors"

    body = f"""Hi,

Quick data point: {name}'s website scores {perf}/100 on Google's mobile speed test.

Studies show that for every second a page takes to load, conversions drop by ~7%. At {perf}/100, you're likely losing a significant chunk of mobile visitors before they ever see your offer.

For a solar company in {city}, where most people research on their phones — that's real money left on the table.

I've helped solar companies fix exactly this. The good news? It's usually fixable in days, not months.

Worth a 10-minute call this week to walk through what I found?

Best,
{YOUR_SIGNATURE}
"""
    return subject, body, "speed_urgent"


# ---------------------------------------------------------------------------
# Email Generator
# ---------------------------------------------------------------------------

def pick_best_template(audit):
    """
    Auto-select the best email template based on audit findings.
    """
    score = audit.get("score", {}).get("score", 50)
    perf = audit.get("pagespeed", {}).get("mobile_performance_score")
    pixels = audit.get("pixels", {})
    conversion = audit.get("conversion", {})

    # Very slow site → speed template
    if perf is not None and perf < 40:
        return "speed_urgent"

    # Low score + missing pixels → competitor gap
    if score < 40 and not pixels.get("meta_pixel"):
        return "competitor_gap"

    # Default → audit hook (works for everyone)
    if score < 60:
        return "audit_hook"

    # If score is high (well-optimized), use competitor gap anyway
    return "competitor_gap"


def generate_email(lead, audit, template_name=None):
    """Generate a personalized email for a lead."""
    if template_name is None:
        template_name = pick_best_template(audit)

    templates = {
        "audit_hook": template_audit_hook,
        "competitor_gap": template_competitor_gap,
        "speed_urgent": template_speed_urgent,
    }

    template_fn = templates.get(template_name, template_audit_hook)
    subject, body, used_template = template_fn(lead, audit)

    return {
        "company": lead.get("name", ""),
        "city": lead.get("city", ""),
        "email": lead.get("email", ""),
        "phone": lead.get("phone", ""),
        "website": lead.get("website", ""),
        "audit_score": audit.get("score", {}).get("score", ""),
        "template": used_template,
        "subject": subject,
        "body": body,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }


def contact_lookup():
    """host -> (email, phone) from the cleaned leads.csv, for enrichment."""
    lookup = {}
    if not os.path.exists(LEADS_CSV):
        return lookup
    import csv as _csv
    with open(LEADS_CSV, "r", encoding="utf-8") as f:
        for row in _csv.DictReader(f):
            site = (row.get("website") or "").strip()
            m = re.search(r"https?://(?:www\.)?([^/]+)", site)
            if m:
                lookup[m.group(1).lower()] = (
                    (row.get("email") or "").strip(),
                    (row.get("phone") or "").strip())
    return lookup


def load_rankings():
    """Build ranked leads directly from audit JSONs (highest score = best
    opportunity). Contacts are enriched from leads.csv by domain match."""
    contacts = contact_lookup()
    rows = []
    if not os.path.isdir(AUDIT_DIR):
        print(f"No audit directory at {AUDIT_DIR}")
        return rows
    for filename in sorted(os.listdir(AUDIT_DIR)):
        if not (filename.startswith("audit_") and filename.endswith(".json")):
            continue
        try:
            with open(os.path.join(AUDIT_DIR, filename), "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue
        name = (data.get("company") or "").strip()
        if not name:
            continue
        score = data.get("score", {}).get("score", 0)
        issues = data.get("score", {}).get("issues", []) or []
        site = (data.get("website") or data.get("final_url") or "").strip()
        email = phone = ""
        m = re.search(r"https?://(?:www\.)?([^/]+)", site)
        if m and m.group(1).lower() in contacts:
            email, phone = contacts[m.group(1).lower()]
        rows.append({
            "rank": 0, "name": name, "city": data.get("city", ""),
            "website": site, "email": email, "phone": phone,
            "audit_score": score if isinstance(score, int) else 0,
            "top_issues": issues[:3],
        })
    rows.sort(key=lambda r: r["audit_score"], reverse=True)
    for i, r in enumerate(rows, 1):
        r["rank"] = i
    if not rows:
        print("No audits found. Run discovery first: "
              "python ../01-LEADS/discover_leads.py \"solar <city>\"")
    return rows


def load_audit_for_lead(lead_name):
    """Load the audit JSON for a specific lead."""
    safe_name = "".join(c if c.isalnum() else "_" for c in lead_name)[:50]
    # Try exact match first
    for filename in os.listdir(AUDIT_DIR):
        if filename.startswith("audit_") and filename.endswith(".json"):
            filepath = os.path.join(AUDIT_DIR, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if data.get("company", "").lower() == lead_name.lower():
                    return data
            except:
                continue
    return None


def export_email(email_data, export_dir):
    """Save an email as a text file for easy copy-paste."""
    os.makedirs(export_dir, exist_ok=True)
    safe_name = "".join(c if c.isalnum() else "_" for c in email_data["company"])[:40]
    filepath = os.path.join(export_dir, f"email_{safe_name}.txt")

    content = f"""=== EMAIL FOR: {email_data['company']} ===
City: {email_data['city']}
To: {email_data['email'] or '(no email found)'}
Phone: {email_data['phone'] or 'N/A'}
Website: {email_data['website']}
Audit Score: {email_data['audit_score']}/100
Template: {email_data['template']}
Generated: {email_data['generated_at']}

--- SUBJECT ---
{email_data['subject']}

--- BODY ---
{email_data['body']}

--- MANUAL AD CHECK URLS ---
Open these to see if they're running ads:
  Google: https://adstransparency.google.com/?region=anywhere&q={email_data['website'].replace('https://', '').replace('http://', '').split('/')[0]}&country=IN
  Meta:   https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=IN&q={email_data['company']}

=== END ===
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filepath


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Generate audit outreach emails")
    parser.add_argument("--top", type=int, default=10, help="Generate emails for top N leads")
    parser.add_argument("--name", type=str, help="Specific company name")
    parser.add_argument("--export", action="store_true", help="Save emails as .txt files")
    parser.add_argument("--template", type=str, choices=["audit_hook", "competitor_gap", "speed_urgent"],
                        help="Force a specific template")

    args = parser.parse_args()

    # Load rankings
    rankings = load_rankings()
    if not rankings:
        return

    # Filter to specific company if requested
    if args.name:
        rankings = [r for r in rankings if args.name.lower() in r["name"].lower()]
        if not rankings:
            print(f"No lead found matching '{args.name}'")
            return

    # Take top N
    rankings = rankings[:args.top]

    print("=" * 60)
    print(f"GENERATING {len(rankings)} PERSONALIZED EMAILS")
    print("=" * 60)

    emails = []
    for i, lead in enumerate(rankings, 1):
        print(f"\n[{i}/{len(rankings)}] {lead['name'][:40]}")

        # Load full audit data
        audit = load_audit_for_lead(lead["name"])
        if not audit:
            print(f"  WARNING: No audit found for {lead['name']}. Skipping.")
            continue

        # Generate email
        email = generate_email(lead, audit, args.template)
        emails.append(email)

        print(f"  Template: {email['template']}")
        print(f"  Subject:  {email['subject'][:60]}")
        print(f"  To:       {email['email'] or '(no email - need to find)'}")

        # Export if requested
        if args.export:
            filepath = export_email(email, EMAILS_DIR)
            print(f"  Saved:    {filepath}")

    # Print all emails in console if not exporting
    if not args.export:
        print(f"\n{'='*60}")
        print("ALL GENERATED EMAILS (copy-paste ready):")
        print(f"{'='*60}")
        for email in emails:
            print(f"\n{'-'*50}")
            print(f"TO: {email['company']} ({email['email'] or 'NO EMAIL'})")
            print(f"SUBJECT: {email['subject']}")
            print(f"{'-'*50}")
            print(email["body"])

    # Summary
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Emails generated: {len(emails)}")
    with_email = sum(1 for e in emails if e["email"])
    print(f"With email address: {with_email}")
    print(f"Need manual email find: {len(emails) - with_email}")
    if args.export:
        print(f"Files saved to: {EMAILS_DIR}")

    print(f"\nNext steps:")
    print(f"1. For leads without email → Google their name + 'contact'")
    print(f"2. Open the ad check URLs to verify their ad presence")
    print(f"3. Send emails ONE BY ONE via Gmail (personalize further if possible)")
    print(f"4. Track responses in CRM: python ../05-CRM/crm.py")


if __name__ == "__main__":
    main()
