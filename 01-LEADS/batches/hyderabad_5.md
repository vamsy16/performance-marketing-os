# Batch: Solar Hyderabad — 5 Leads (staged 2026-10-18)

Selected from the cleaned `leads.csv` Hyderabad pool (Ksquare Energy excluded —
already audited + drafted). Every website below was fetched and verified
live on 2026-10-18; all are real Hyderabad solar installers/EPCs.

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

A sandbox test run against samrajsolar.com failed to fetch the site; the
empty PDF it produced was deleted rather than kept, and `verify_report.py`
would have failed it anyway. No fabricated audits, ever.

## Run this on your machine (one block)

```bash
cd performance-marketing-os
pip install -r 01-LEADS/requirements.txt

cd 01-LEADS
python run_pipeline.py https://samrajsolar.com "Samraj Solar" --city Hyderabad
python run_pipeline.py https://sriishaansolar.com "Sri Ishaan Solar" --city Hyderabad
python run_pipeline.py https://augnisolar.com "Avghni Solar" --city Hyderabad
python run_pipeline.py https://nairasolar.com "Naira Solar" --city Hyderabad
python run_pipeline.py https://www.arkahub.in "Arkahub" --city Hyderabad

# QA gate — must print ALL REPORTS PASS before anything is delivered
python verify_report.py --all

cd ../02-OUTREACH
python audit_outreach.py --export   # emails + sequence_manifest.json
```

Then commit + push (audit JSONs, PDFs, generated emails, manifest).

## What Arena does next (after you push)

1. Re-runs `verify_report.py --all` on the pushed reports.
2. Creates ONE initial Gmail draft per lead **with an email** (PDF attached),
   records `thread_id` / `mails_sent` / `next_followup_date` via
   `sequence.py` (see `GMAIL_DRAFT_WORKFLOW.md`).
3. Reports back the draft list. You review + send in Gmail, say
   "I sent <company>", and follow-ups are drafted in-thread on their
   +2-day due dates — never as new mails, never pre-created.
