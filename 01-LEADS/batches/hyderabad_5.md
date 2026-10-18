# Batch: Solar Hyderabad — 5 Leads (staged 2026-10-18)

## Correct flow: leads come from the AD LIBRARY, not from search

```
python discover_leads.py "solar Hyderabad" --limit 5
  1. Searches the LIVE Meta Ad Library for ACTIVE solar advertisers in Hyderabad
  2. One lead per advertiser; takes the ad's real destination/conversion page
     (the exact URL the ad sends customers to, or WhatsApp if that's the funnel)
  3. Audits THAT conversion page — only because that's where ad clicks land,
     so pixel/tracking/CTA/speed on it decide whether ad spend converts
  4. Pulls full live ad activity: Meta own ads + Meta competitors + Google
     Ads Transparency (own + competitors)
  5. Builds the branded Ads Audit PDF (ad sections are the headline;
     the conversion-page score is one panel in it)
```

The 5 companies below are a FALLBACK seed list from the cleaned `leads.csv`
pool (Ksquare Energy excluded — already audited + drafted), in case the ad
library returns fewer than 5 usable advertisers. The discovery run decides
the real 5 — it may legitimately return different companies.

| # | Company | Website | Email | Phone | Notes (verified from live site) |
|---|---|---|---|---|---|
| 1 | Samraj Solar | https://samrajsolar.com | samrajsolar@gmail.com | +91 8121005746 | Solar EPC, Hyderabad, since 2014. Residential + commercial, AP & Telangana. |
| 2 | Sri Ishaan Solar | https://sriishaansolar.com | info@sriishaansolar.com | +91 7842461888 | Rooftop installer since 2017, 100+ installs, TGREDCO TSRE260936, PM Surya Ghar support. |
| 3 | Avghni Solar | https://augnisolar.com | support@avghnisolar.com | +91 9949216282 | EPC (Avghni Renewable Energy System India Pvt Ltd), govt/industrial rooftop projects. |
| 4 | Naira Solar | https://nairasolar.com | nairasolars@gmail.com | +91 7997116161 | Rooftop solar Hyderabad, WhatsApp funnel (+91 7997116161), subsidy guidance. |
| 5 | Arkahub | https://www.arkahub.in | NO EMAIL | — | MNRE-approved residential rooftop (Interglacial Renewable Technologies), operates in Hyderabad. Find email before drafting. |

## ⚠️ Why these are staged, not audited yet

The audit pipeline (`discover_leads.py` / `run_pipeline.py`) must fetch live
websites and drive headless Chrome against the Meta Ad Library. The Arena
sandbox cannot do either (outbound web is restricted and no Chrome is
available/installable there), so audits run on the owner's machine via
OpenCode — exactly as the ads-audit skill was designed.

> **Correction (2026-10-18):** the paragraph above is half wrong. The Arena
> sandbox has no Chrome/Playwright and its bash has no outbound TLS, but the
> Arena agent's own page-fetch tooling **can** read the live Meta Ad Library
> and lead websites — that is how
> `batches/hyderabad_5_leads_batch2_2026-10-18.md` was built (library IDs,
> start dates, destinations and contacts all read live). What still requires
> the owner's machine is the pipeline itself: website audit, creative
> downloads, Google Ads Transparency and the branded PDF.

A sandbox test run against samrajsolar.com failed to fetch the site; the
empty PDF it produced was deleted rather than kept, and `verify_report.py`
would have failed it anyway. No fabricated audits, ever.

## Run this on your machine (one block)

```bash
cd performance-marketing-os
pip install -r 01-LEADS/requirements.txt

cd 01-LEADS
# PRIMARY: leads discovered from the live Meta Ad Library, ads audited
python discover_leads.py "solar Hyderabad" --limit 5

# QA gate — must print ALL REPORTS PASS before anything is delivered
python verify_report.py --all

cd ../02-OUTREACH
python audit_outreach.py --export   # emails + sequence_manifest.json
```

Only if discovery returns too few advertisers, top up individually with
`python run_pipeline.py <ad destination URL> "<Advertiser Name>" --city Hyderabad`
(do NOT pass --skip-ads; the ad research is the point of the report).

Then commit + push (audit JSONs, PDFs, generated emails, manifest).

## What Arena does next (after you push)

1. Re-runs `verify_report.py --all` on the pushed reports.
2. Creates ONE initial Gmail draft per lead **with an email** (PDF attached),
   records `thread_id` / `mails_sent` / `next_followup_date` via
   `sequence.py` (see `GMAIL_DRAFT_WORKFLOW.md`).
3. Reports back the draft list. You review + send in Gmail, say
   "I sent <company>", and follow-ups are drafted in-thread on their
   +2-day due dates — never as new mails, never pre-created.
