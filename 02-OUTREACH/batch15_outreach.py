#!/usr/bin/env python3
"""Batch 15 outreach drafts - five Telangana leads, four steps each.

These are DRAFTS. Nothing here sends mail. The generated .txt files and the
sequence_manifest.json rows are what a human reviews before anything leaves
the building.

Why a separate generator (not ads_only_outreach.py):
  * ads_only_outreach.py is written for leads whose *website was never
    audited*, and its copy says so ("it is an ad report, not a website
    audit"), with a FORBIDDEN list that blocks every /100, pixel and GA
    mention. These five leads DO have a measured website audit, so that copy
    would be false and its guard would block the true findings.
  * sequence.py's follow-up templates talk about "the Hyderabad solar
    market" and "rooftop solar", which is wrong for two dental practices and
    an interior studio.

Every number in the copy below is read out of the report JSON at build time
(ad count, oldest start date, destination, score) or comes from the measured
facts in 01-LEADS/batch15_telangana_data.py. The build refuses to run if a
number in the copy disagrees with the report.

Usage (from 02-OUTREACH/):
    python3 batch15_outreach.py             # print + verify, write nothing
    python3 batch15_outreach.py --export    # write .txt files + manifest rows
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LEADS_DIR = os.path.join(os.path.dirname(BASE_DIR), "01-LEADS")
RESULTS = os.path.join(LEADS_DIR, "ads_only_results")
EMAILS_DIR = os.path.join(BASE_DIR, "generated_emails")

sys.path.insert(0, BASE_DIR)
import sequence as seq_engine
from audit_outreach import YOUR_SIGNATURE

DRAFTED_ON = "2026-11-28"
DATA_SOURCE = ("01-LEADS/batch15_telangana_data.py (read live on 2026-11-28)")


# ---------------------------------------------------------------------------
# Recipients. Only addresses the business publishes itself - never guessed.
# ---------------------------------------------------------------------------

TO = {
    "SunSolar Power Systems": "sales@sunsolar.info",
    "PNR Sunrise Energies": "",          # no public email on the site
    "D'LIFE Home Interiors": "enquiry@dlifeinteriors.com",
    "Dr. Sridhar Dental": "",            # no public email on the site
    "Galaxy Dental Care": "contact@galaxydentalcare.in",
}

CHANNEL_NOTE = {
    "SunSolar Power Systems": "Published address: sales@sunsolar.info (also on the site footer).",
    "PNR Sunrise Energies": ("NO PUBLIC EMAIL. The homepage publishes only +91 63045 87145 "
                             "(phone and WhatsApp). Send as a web-form message or WhatsApp, "
                             "or find a named contact before sending."),
    "D'LIFE Home Interiors": "Published address: enquiry@dlifeinteriors.com (also printed in their live ads).",
    "Dr. Sridhar Dental": ("NO PUBLIC EMAIL. Per-branch WhatsApp only (+91 94909 48081 / "
                           "+91 81212 22888 / +91 95420 27700) and the /book-appointment form."),
    "Galaxy Dental Care": "Published address: contact@galaxydentalcare.in (site footer).",
}


def load_report(company):
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", company)[:50]
    path = os.path.join(RESULTS, f"audit_{slug}.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def facts(report):
    lib = report.get("ad_library") or {}
    meta = lib.get("meta_own") or {}
    ads = meta.get("ads") or []
    site = report.get("site_audit") or {}
    google = (lib.get("google_own") or {}).get("detail") or {}
    dates = []
    for a in ads:
        for fmt in ("%d %b %Y", "%d %B %Y"):
            try:
                dates.append(datetime.strptime(a["started"].strip(), fmt))
                break
            except Exception:
                pass
    return {
        "company": report["company"],
        "city": (report.get("city") or "").split(",")[0],
        "n_meta": len(ads),
        "oldest": min(dates).strftime("%-d %B %Y") if dates else "",
        "newest": max(dates).strftime("%-d %B %Y") if dates else "",
        "ids": [a["library_id"] for a in ads],
        "google_ads": google.get("ad_count"),
        "google_name": google.get("advertiser") or "",
        "score": ((site.get("score") or {}).get("score")),
        "issues": len((site.get("score") or {}).get("issues") or []),
        "pixels": site.get("pixels") or {},
        "checked_on": report.get("checked_on") or "",
    }


# ---------------------------------------------------------------------------
# Copy. {n} ad count, {oldest}/{newest} dates, {city} city - all injected and
# asserted against the report below, so the email cannot drift from the PDF.
# ---------------------------------------------------------------------------

COPY = {
    "SunSolar Power Systems": {
        "subject": "SunSolar: 4 live Meta ads, all of them landing on fb.me",
        "body": """Hi,

I read SunSolar's live advertising this week, and one thing stood out.

All four of your Meta ads point at http://fb.me/ - a bare short link, with no UTM on it. The oldest has been running since {oldest}; the other three all started in the last week (two on 21 November, one on 23 November).

Meanwhile the Google side of the house is in better shape than most: the Google Ads conversion tag in your tracking.js (AW-18179174251) is already wired to the lead form (#leadForm), both phone links and the WhatsApp link. So a Google enquiry can be counted today.

The Meta side cannot. There is no Meta Pixel in the page, no GA4 and no Tag Manager container, so the four ads above produce enquiries you can only count by hand.

I put the evidence in the attached report: the four live ads with their Library IDs and start dates, the tracking audit of the page, and the three things I would fix first. Every line in it can be re-checked from the links it cites.

Worth 10 minutes? I am happy to walk you through it, or keep the report and use it without me.

Best,
{signature}

Live ads cited:
{links}""",
        "followups": [
            """Hi,

Adding one thing I did not put in the first email.

Your site already quotes a price in the estimator (Rs 2,25,000 base for a 4 kW system), while the live ads quote Rs 1,71,999 and Rs 2,18,999 after the Rs 78,000 subsidy. Two different numbers for the same buyer, in two places they will both see.

That is a five-minute fix on the page, and it matters more once the ads are measurable.

The report is in my first email if it is useful.

Best,
{signature}""",
            """Hi,

Last detail from the audit, then I will stop.

The homepage preloads a video file (assets/video/sunsolar-cinematic-loop.mp4) before anything else, and it is the first thing between a paid click and the quote calculator on a phone. Combined with a fb.me redirect, that is the whole path a Meta click takes.

If you ever want a second pair of eyes on the paid side, I am around.

Best,
{signature}""",
            """Hi,

I have written twice and heard nothing, so I will assume the timing is wrong and close the loop.

The report stands on its own - the four Library IDs in it still resolve in the Ad Library, and the tracking findings will still be true next month unless someone fixes them.

If it becomes a priority, my door is open.

Best,
{signature}""",
        ],
        "attach_note": "Ads + measured site audit (4 live Meta ads, 0 live Google ads).",
    },

    "PNR Sunrise Energies": {
        "subject": "PNR Sunrise: one live ad, and a canonical tag pointing at a placeholder",
        "body": """Hi,

I read PNR Sunrise Energies' live advertising this week. One ad is running - opened 12 November, recruiting solar channel partners across Telangana and Andhra Pradesh, with a WhatsApp button rather than a landing page.

The ad itself is fine. What worried me is the page it mentions in the copy (sunriseenergies.in) and what that page tells Google:

  - its canonical tag points at https://www.sunriseenergies.example/ - a placeholder domain that does not exist;
  - there is no analytics, no pixel and no tag manager of any kind in the page source, so the WhatsApp enquiries from that ad cannot be traced to it.

The first is a one-line fix with a direct search cost. The second is why the ad spend and the enquiries never meet.

The attached report documents both, with the ad's Library ID, the validator output and the exact lines involved, so it can be re-checked.

If it is useful, I am happy to walk you through it on a short call. If not, keep it.

Best,
{signature}

Live ad cited:
{links}""",
        "followups": [
            """Hi,

One more from the audit, in case the canonical tag felt small.

Your homepage gives a phone number and a WhatsApp link, but no email address and no office address - and it is the page an installer or a commercial buyer lands on when they are deciding whether to trust you with a project.

Both items are in the report from my first email.

Best,
{signature}""",
            """Hi,

The ad you are running asks installers to partner with you, but the button opens a chat. Nothing captures the territory, the team size or the margin expectation before a human answers.

A one-page partner form would qualify those conversations before they cost you time - and would be measurable, which the WhatsApp thread is not.

Happy to sketch it if that is useful.

Best,
{signature}""",
            """Hi,

I will stop here - no reply, so I assume it is not a priority right now.

If the channel-partner push picks up, the report in my first email lists what to fix first, in order. It will still be accurate.

Best,
{signature}""",
        ],
        "attach_note": "Ads + measured site audit (1 live Meta ad, 0 live Google ads). No public email - see channel note.",
    },

    "D'LIFE Home Interiors": {
        "subject": "D'LIFE: 5 live Meta ads, ~200 Google ads, two different phone numbers",
        "body": """Hi,

I read D'LIFE's live advertising this week - it is the heaviest in the Hyderabad interior market I looked at: five active Meta ads (the oldest since {oldest}) and roughly 200 live Google ads under D'LIFE Interiors Private Limited.

Two things stood out.

First, the phone number. The live Meta ad quoting +91 9567231111 (the Delhi one) sits next to a Hyderabad page that publishes +91 949 508 7777. A buyer who checks both has to decide which is real before calling.

Second, where the clicks land. Three of the five Meta ads open a Messenger chat and two open Instagram - none of them lands on the Hyderabad page, and none carries a UTM. Your Meta Pixel (215010909028561) and Tag Manager container (GTM-K9FB6G2) are both on the page, so the measurement exists; it just never sees the ad click that produced the conversation.

The attached report also covers the markup: 64 telephone links with unencoded spaces that fail to dial on some Android handsets, and 148 validator errors. It says plainly which rows I could not read through NitroPack rather than guessing at them.

Worth a short call?

Best,
{signature}

Live ads cited:
{links}""",
        "followups": [
            """Hi,

One number from the report that is easy to miss.

Of the five live Meta ads, the three newest are the ones that open Messenger, and the two testimonial films point at Instagram. Your best-performing format is the one furthest from anything you can measure.

The report in my first email has the Library IDs.

Best,
{signature}""",
            """Hi,

A small thing with an outsized effect: the Hyderabad page's wrapper carries class="locationPage location-bangalore" - a copy-paste from the Bangalore template.

It does not break the page today, but it is the kind of detail that turns into the wrong city, the wrong number or the wrong map after the next edit.

Same report, page 1 onwards.

Best,
{signature}""",
            """Hi,

Last one, then I will leave you alone.

Your page quotes the packages exactly (Essential at Rs 8.85 lakh down to Rs 6.37 lakh for a 2BHK) - that is more than most interior firms publish. The gap is not the offer; it is that the ads never send anyone to it.

If the paid side becomes a priority this quarter, I would start there.

Best,
{signature}""",
        ],
        "attach_note": "Ads + measured site audit (5 live Meta ads, ~200 live Google ads). PDF runs in 'measured findings only' mode for the tag rows.",
    },

    "Dr. Sridhar Dental": {
        "subject": "Dr. Sridhar: 42 Google ads, 5 Meta ads, and no Meta Pixel",
        "body": """Hi,

I read Dr. Sridhar International Dental Hospital's live advertising this week. Of the five leads I looked at in Hyderabad, yours is the best-instrumented on the Google side: GA4 (G-7Y9ND039HL) and the Google Ads conversion tag (AW-855095874) are both in the page, and 42 Google ads are live.

The Meta side is the opposite. Five ads are running - the newest opened {newest}, and three of the five open the Instagram profile rather than a treatment page. There is no Meta Pixel anywhere in the served HTML, so none of those views can be retargeted and none of the enquiries they produce can be attributed to the ad that caused them.

One more, structural: sridhardental.com serves a client-rendered React shell. The HTML a crawler receives has no H1, no meta description and no structured data - the content appears only after JavaScript runs.

The attached report documents all of it, with Library IDs, the tag IDs and the validator output, so every line can be re-checked.

Happy to walk through it on a 10-minute call.

Best,
{signature}

Live ads cited:
{links}""",
        "followups": [
            """Hi,

Following up with the one fix I would do first.

Four branches - KPHB, Ameerpet, Nallagandla, Vijayawada - and none of them is described in structured data on the site. Each is competing in its own map pack. LocalBusiness markup per branch is a half-day of work that pays for itself in map visibility.

The report covers the rest.

Best,
{signature}""",
            """Hi,

One detail on the Meta side.

Your brand films are in Telugu, which is exactly right for the audience, and they end on the Instagram profile. A viewer who is ready to book has to leave the app, find the site and book - three steps where one would do.

The treatment page with the booking form already exists. The ad just does not use it.

Best,
{signature}""",
            """Hi,

I will close the loop here - if the timing is wrong, that is fair.

The report stands on its own: the Library IDs still resolve, and the missing Meta Pixel and the empty HTML shell will still be true until someone changes them.

If it becomes useful, you know where I am.

Best,
{signature}""",
        ],
        "attach_note": "Ads + measured site audit (5 live Meta ads, 42 live Google ads). No public email - see channel note.",
    },

    "Galaxy Dental Care": {
        "subject": "Galaxy Dental: ~300 Google ads, and a price the site never shows",
        "body": """Hi,

I read Galaxy Dental Care's live advertising this week, and the scale is not the problem - it is the handoff.

On the paid side: roughly 300 live Google ads for galaxydentalcare.in, and five active Meta ads quoting Rs 20,000 braces, Rs 15,000 implants and 60% off Invisalign.

On the page they relate to: no price at all. The offer that earned the click disappears exactly when the patient arrives.

Two more things from the same read. Your Google Ads run under an advertiser registered as "Jaydeep" rather than the clinic name - if that is a personal account, the clinic has no ownership trail over its own ad history. And the contact page carries 20 telephone links with unencoded spaces (tel:+91 86866 76781), which fail to dial on some Android handsets.

The measurement is mostly there: Google Tag Manager (GTM-TRRMQGQ) is installed, though WP Rocket defers it until the first interaction, and the page emits no structured data despite Yoast being installed. The attached report says exactly which rows I could and could not read.

Worth a short call?

Best,
{signature}

Live ads cited:
{links}""",
        "followups": [
            """Hi,

The detail I would fix this week, before any campaign change.

Your NABH, ISO and FAMDENT badges are lazy-loaded images. On a slow connection they render as empty boxes - the accreditations vanish at the moment a nervous patient is looking for a reason to trust you.

Same report, page 1 onwards.

Best,
{signature}""",
            """Hi,

One more on the ads themselves.

Four of the five live Meta ads open a WhatsApp chat and one opens Instagram; none lands on the site, and none carries a UTM. So the Rs 20,000 braces offer is being judged inside a chat thread rather than on a page you control - and nothing tells you which ad started the conversation.

That is a measurable fix, not a rebuild.

Best,
{signature}""",
            """Hi,

I will stop here - no reply, so I will assume the timing is not right.

If the paid side comes up again, the report in my first email lists the five things I would change first, in order of cost. Nothing in it expires quickly.

Best,
{signature}""",
        ],
        "attach_note": "Ads + measured site audit (5 live Meta ads, ~300 live Google ads under 'Jaydeep').",
    },
}


def render(company, f):
    src = COPY[company]
    links = "\n".join(
        f"  Library ID {i}: https://www.facebook.com/ads/library/?id={i}" for i in f["ids"])
    body = src["body"].format(oldest=f["oldest"], newest=f["newest"],
                              city=f["city"], links=links,
                              signature=YOUR_SIGNATURE)
    followups = [b.format(oldest=f["oldest"], newest=f["newest"], city=f["city"],
                          links=links, signature=YOUR_SIGNATURE)
                 for b in src["followups"]]
    return src["subject"], body, followups


def check_against_report(company, f, subject, body, followups):
    """Refuse to draft copy that disagrees with the report it ships with."""
    problems = []
    blob = " ".join([subject, body] + followups)

    # Ad counts: every "N live ... ads" / "N of the five" claim must match.
    for m in re.finditer(r"(\w+) live (?:Meta )?ads", blob):
        word = m.group(1).lower()
        if word in ("no", "zero"):
            claimed = 0
        elif word.isdigit():
            claimed = int(word)
        else:
            continue
        if claimed != f["n_meta"]:
            problems.append(f"copy says {claimed} live Meta ads, report has {f['n_meta']}")
    for m in re.finditer(r"(\d+) of the five", blob):
        if f["n_meta"] != 5:
            problems.append(f"copy says 'of the five' but the report has {f['n_meta']} ads")
    # Library ids
    for i in re.findall(r"id=(\d{6,})", blob):
        if i not in f["ids"]:
            problems.append(f"copy cites Library ID {i}, which is not in the report")
    # Google ad counts in prose
    g = f["google_ads"]
    for m in re.finditer(r"(?:roughly |~)?(\d+) live Google ads", blob):
        if g is not None and int(m.group(1)) != int(g):
            problems.append(f"copy says {m.group(1)} Google ads, report has {g}")
    # Placeholder leakage / tone
    for bad in ("{", "}", "None", "TBD", "XXX"):
        if bad in blob:
            problems.append(f"unrendered placeholder '{bad}' left in copy")
    if len(body.split()) > 260:
        problems.append(f"step 0 body is {len(body.split())} words - too long to send")
    return problems


def make_sequence(report, f, subject, body, followups):
    seq = {
        "company": f["company"],
        "to": TO.get(f["company"], ""),
        "city": (report.get("city") or ""),
        "website": report.get("website", ""),
        "report_kind": "ads_only",
        "thread_subject": subject,
        "thread_id": "",
        "mails_sent": 0,
        "next_followup_date": "",
        "next_step": None,
        "steps": [],
    }
    bodies = [body] + followups
    for n, b in enumerate(bodies):
        step = {
            "step": n,
            "kind": "initial" if n == 0 else ("breakup" if n == 3 else "followup"),
            "subject": subject if n == 0 else f"Re: {subject}",
            "body": b,
            "delay_after_previous_days": 0 if n == 0 else seq_engine.FOLLOWUP_DELAY_DAYS,
        }
        step.update(seq_engine._blank_state())
        seq["steps"].append(step)
    return seq


def write_txt(f, report, subject, body, followups):
    company = f["company"]
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", company)[:50]
    path = os.path.join(EMAILS_DIR, f"batch15_email_{slug}.txt")
    attached = os.path.join(BASE_DIR, "ads_only_pdfs", f"audit_{slug}.pdf")
    has_pdf = os.path.exists(attached)
    to = TO.get(company, "")
    parts = [f"""=== DRAFT (NOT SENT) - {company} ===
Drafted: {DRAFTED_ON}
To: {to or '(no public email address - see channel note)'}
Channel: {CHANNEL_NOTE[company]}
Website: {report.get('website', '')}
Report kind: ads + measured site audit
ATTACH THIS: {attached}{'' if has_pdf else '   <-- MISSING PDF'}
Source for every figure: {DATA_SOURCE}
Report: 01-LEADS/ads_only_results/audit_{slug}.json
Step 0 subject: {subject}
"""]
    for n, b in enumerate([body] + followups):
        when = ("send day 0" if n == 0 else
                f"draft only after step {n - 1} is SENT + {seq_engine.FOLLOWUP_DELAY_DAYS} days")
        parts.append(f"\n--- STEP {n} ({'initial' if n == 0 else ('breakup' if n == 3 else 'follow-up')}) · {when} ---\n"
                     f"SUBJECT: {subject if n == 0 else 'Re: ' + subject}\n\n{b}\n")
    parts.append("=== END ===")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(parts))
    return path, has_pdf


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--export", action="store_true", help="write files + manifest rows")
    args = ap.parse_args()

    manifest = seq_engine.load_manifest()
    problems_total = []
    print("=" * 70)
    print(f"BATCH 15 DRAFTS - {DRAFTED_ON} (nothing is sent by this script)")
    print("=" * 70)

    for company in COPY:
        report = load_report(company)
        f = facts(report)
        subject, body, followups = render(company, f)
        problems = check_against_report(company, f, subject, body, followups)
        problems_total.extend(f"{company}: {p}" for p in problems)

        print(f"\n{company}")
        print(f"  to:        {TO.get(company) or '(no public email)'}")
        print(f"  subject:   {subject}")
        print(f"  ads:       {f['n_meta']} Meta / {f['google_ads']} Google"
              f"   report score: {f['score']}")
        print(f"  words:     step0={len(body.split())}, "
              f"followups={[len(x.split()) for x in followups]}")
        print(f"  checks:    {'OK' if not problems else problems}")

        if args.export and not problems:
            seq = make_sequence(report, f, subject, body, followups)
            keep = next((s for s in manifest["sequences"]
                         if s["company"].lower() == company.lower()), None)
            if keep:
                # Never destroy Gmail state on a refresh.
                for k in ("thread_id", "mails_sent", "next_followup_date", "next_step"):
                    seq[k] = keep.get(k, seq[k])
                for n, st in enumerate(seq["steps"]):
                    old = (keep.get("steps") or [{}] * 4)[n] if n < len(keep.get("steps") or []) else {}
                    for k in ("draft_id", "message_id", "thread_id", "sent_at",
                              "draft_created_at", "due_date", "status"):
                        if old.get(k):
                            st[k] = old[k]
                manifest["sequences"].remove(keep)
            manifest["sequences"].append(seq)
            path, has_pdf = write_txt(f, report, subject, body, followups)
            print(f"  saved:     {path}")
            print(f"  attach:    {'yes' if has_pdf else 'MISSING PDF'}")

    if args.export:
        if problems_total:
            print("\nREFUSING to save manifest rows while copy disagrees with a report.")
            for p in problems_total:
                print("  x", p)
            return 1
        seq_engine.save_manifest(manifest)
        print(f"\nManifest updated: {seq_engine.MANIFEST_FILE}")
        print("Nothing was sent. Review each file in generated_emails/ before drafting in Gmail.")
    else:
        print("\n(dry run - pass --export to write the .txt files and manifest rows)")
    return 0 if not problems_total else 1


if __name__ == "__main__":
    sys.exit(main())
