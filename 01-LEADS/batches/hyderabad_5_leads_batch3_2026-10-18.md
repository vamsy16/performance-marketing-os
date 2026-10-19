# Batch 3: Solar Hyderabad — 5 NEW Leads from the Live Meta Ad Library

Pulled **2026-10-18** from the **live Meta Ad Library** (India, active ads), using the
same discovery flow `discover_leads.py` implements — start from the ads, not from a
name list.

## How these 5 were found

| Probe (Ad Library, India, active ads) | What the library said |
|---|---|
| `solar Hyderabad` (sorted by total impressions) | ~330 results; read every card on the page: Venus, Sri Balaji, ORBIT SOLAR, AB Solar, Suryon, Mahadev Enterprises, Green Carbon Hub, mrsolar.in, ARKA SOLAR POWER, Shreepad Avenue, Mahaveer Constructions, Hi Kanpur + FreyrEnergy |
| `rooftop solar installation Hyderabad` | ~40 results: mrsolar.in, ARKA SOLAR POWER, Hysunsolarhyderabad |
| `solar subsidy Telangana` | ~60 results: Sri Balaji Solar Energies |
| company-name probes | `Evergrid Energy`, `Solox Energies`, `Truzon Solar`, `Punarvi Energies`, `Kondaas`, `Maa Solar Energy Solutions`, `Varahi Energies`, `Mamindla Energy Solutions`, `SAS Energy`, `Greentek solar`, `Sri Ishaan Solar`, `Avghni Solar`, `Naira Solar`, `Zenith Energy Hyderabad solar` |

**Excluded — already audited / drafted / staged in this repo:** Ksquare Energy,
Sri Balaji Solar Energies, Venus home appliances, ORBIT SOLAR, AB Solar Power
Systems, Suryon, mrsolar.in, The ARKA SOLAR POWER, Hysun Solar, Krisol Solar,
3S Solutions, Shree Adithya Solar, Mahesh Solar Solutions (batches 1 & 2), plus the
`leads.csv` Hyderabad pool: Samraj Solar, Mr Solar, Zenith Energy, bharatcharge.in,
Sri Ishaan Solar, Avghni Solar, Naira Solar, SquareYards, Arkahub.

**Excluded — keyword noise (match "solar"/"Hyderabad" but are not rooftop-solar
installers to pitch):** Shreepad Avenue (3BHK bungalows, Bharuch, Gujarat),
Mahaveer Constructions (villa plots, Dundigal — "solar fencing" in copy), Hi Kanpur
+ FreyrEnergy (national brand, ad targets Kanpur), Utsav App Pujas (Varahi temple
puja), EnergyWise (BESS monitoring), Friendly Wings Traders (solar CCTV, Tamil
Nadu), Solar Point (Bhubaneswar), Sonatech Solar, Trontek (inverters), Alibaba.com.

**Deferred from batch 2 (still not pitched):** Green Carbon Hub (solar O&M/AMC
only), Mahadev Enterprises (solar street lights only).

## The 5 leads

| # | Advertiser (lead) | Live ad evidence | Conversion destination | Website | Contact (verified live) |
|---|---|---|---|---|---|
| 1 | **Evergrid Energy** (Evergrid Energy Pvt Ltd) | Library ID 1642242114211409 (started Oct 16, 2026) + 1079793338257084 (Oct 17, 2026), FB page 61593038197988 | Facebook lead form (`fb.me` "Get quote") — **not** their site | https://www.evergridenergy.in | contact@evergridenergy.in · +91 7330777310 · WhatsApp 917330777310 · Harmony Heights, Rd 9, Park View Enclave Road, Jubilee Hills, Hyderabad 500034 · GST 36AAJCE8588K1ZS |
| 2 | **Solox Energies Private Limited** | Library ID 2023601181805342 (started Oct 17, 2026, "multiple versions"), FB page `soloxenergies` | https://solox.in/ ("Book Now") — one of the few that sends traffic to its own site | https://solox.in | contact@solox.in · +91 9988133789 · Flat 401, Ace Krisna Prime, 11-9-50, Rd 1, Prabhat Nagar, Laxmi Nagar Colony, Kothapet, Hyderabad 500102 · Vijayawada branch |
| 3 | **Truzon Solar** | Library ID 1522258176260844 (started May 20, 2026 — "7 ads use this creative"), 1399945148943213 (Aug 25, 2026 — "6 ads"), 1001393986178171 (May 20, 2026), FB page `truzonsolar` | Facebook lead form (`fb.me` "Call Now +91 9030032222") | https://www.truzonsolar.com | info@truzonsolar.com · +91-9030032222 · 5A, Astral Heights, Road No-1, Banjara Hills, Hyderabad 500034 |
| 4 | **Punarvi Energies Limited** | Library ID 1122725223617884 (started Oct 13, 2026) + 994804120334409 (Oct 13, 2026), FB page `punarvisolarenergies` | Facebook lead form (`fb.me` "Get quote") | https://www.punarvienergies.com | solar@punarvienergies.com · +91 7799757777 · landline +91 40 49941999 · Plot 5, Chandragiri Colony, Above SBI Bank, 3rd Flr, Tirmulgherry, Hyderabad 500015 · factory Cherlapally 500051 · Vijayawada branch |
| 5 | **Varahi Energies** | **No active Meta ads found** (Ad Library probe `Varahi Energies`, 2026-10-18) | WhatsApp only (`wa.me/919666120045` on every CTA) | https://varahienergies.in | varahienergies@gmail.com · +91 9666120045 · HO Kanteshwar, Nizamabad 503002 · Branch: Lane 4, Panchasheel Enclave St, Kompally, Hyderabad-Secunderabad 500067 |

### Per-lead notes (all read live today)

**1. Evergrid Energy** — the cleanest "paying Meta, owning nothing" case in this
batch. Two Dussehra-offer ads are live ("₹22,000 OFF rooftop solar + up to ₹78,000
govt subsidy, EMIs from ₹1,900/month, installed in 21 days, up to 30-year panel
warranty", creative line "Ravan = your electricity bill. Time to end it.") and
**both send the click into a Facebook lead form**, not their own site. So they own
no pixel, no retargeting pool and no page they can A/B test. The site itself is a
modern Framer build with a real quote form (name, phone, installation type, monthly
bill, location), a projects page (Kukatpally 6 kW residential, Shamshabad 120 kW
commercial, Nacharam 20 kW commercial) and a blog — good raw material that paid
traffic never sees. Pitch: owned landing page + pixel/CAPI + retargeting, and
reuse the project page as proof.

**2. Solox Energies** — the only lead in this batch whose ad points at its own
website (`solox.in`), ISO 9001:2015, "leading Solar EPC in Hyderabad, Telangana &
Andhra Pradesh", Australian Premium Solar panels, ₹0-down/EMI messaging, live solar
calculator, Google Analytics already installed (MonsterInsights). Two concrete
defects on the page that receives the paid click: the homepage trust counters still
read **"0+ MW" installed, "1+ projects", "1+ years of cumulative team experience"**
(placeholders never filled in), and the contact page shows `contact@solox.in` while
the actual `mailto:` still points at **Sungosolarenergy@gmail.com** (leftover from
the template's previous brand). One live ad, one creative, one audience — no
testing structure. Pitch: fix the proof/numbers + email plumbing, then creative and
audience testing around "zero down payment".

**3. Truzon Solar** — Hyderabad-headquartered (Banjara Hills corporate office) with
a long-running, multi-creative Meta programme (7 ads sharing one creative since May
2026, 6 more since August). Every creative is **Hindi or Marathi**
("अब सोलर लगाना मुश्किल नहीं रहा", "आता सोलर बसवणे अवघड राहिलेले नाही") with a
"Call Now +91 9030032222" button into a Facebook form — in a market where the
winning language is Telugu (Sri Balaji and ARKA both run Telugu creative). Pitch:
Telugu creative + Telugu landing page, and move the CTA from a Facebook form to
their own tracked quote page.

**4. Punarvi Energies** — the heavyweight of this batch: MNRE-approved EPC, 79 MW
installed, 2,400+ projects, clients incl. IIIT Hyderabad, TGSPDCL, TSREDCO, HPCL,
Marino Foods, Sri Salasar Balaji Textiles (3 MW, Jadcherla), 11 MW ground-mount in
Khammam, 5 MW in Parigi, Google 5.0★ (26 reviews), live solar calculator, landline
+ mobile on the contact page. They are spending on Meta right now with a Navaratri
offer (3 kW ₹1,02,000 / 5 kW ₹2,10,000 + ₹78,000 subsidy + free cleaning kit,
"valid until October 20th") — and **both ads dump the click into a Facebook lead
form**, while the phone number in the ad (**7997667677**) is a transposition of the
number on their own site (**+91 7799757777**). That is a call-tracking and
lead-ownership gap on the biggest spender in the market. Pitch: owned quote page +
call tracking + one number everywhere, then scale creative around the MW-scale
proof they already have.

**5. Varahi Energies** — the only lead here with **no paid acquisition at all**:
no active Meta ads under their name, and every CTA on the site is a WhatsApp deep
link (`wa.me/919666120045` with prefilled text). They are a genuine MNRE-approved
vendor with 250+ projects, 700 kW+ of PM Surya Ghar work (1 MW pipeline), a 545 kW
commercial rice-industry plant (45 MW pipeline) and 80 MW of PM-KUSUM assistance,
plus a live generation widget (8.4 kW, 94%, 32 units today). Their head office is
in Nizamabad with the Hyderabad branch in Kompally, so the Hyderabad-branded
content is thin. Pitch: while the four advertisers above buy the same Hyderabad
homeowner every day, Varahi is invisible on paid — offer Meta lead gen + a
Hyderabad landing page, and keep WhatsApp as the follow-up channel.

## Also seen today (next batch, not counted in the 5)

| Advertiser | Evidence | Why deferred |
|---|---|---|
| Kondaas (Kondaas solar) | Active advertiser: Library ID 1122229007117188 (Sep 22, 2026), 1461065955884011 (Oct 1, 2026), 1045095875272121 (Oct 1, 2026) — but creatives are Tamil/Malayalam regional pages ("Kondaas solar", "Kondaas solar kerala") | National brand; Hyderabad is one location page among many — different pitch (multi-city), not a Hyderabad-local lead |
| Maa Solar Energy Solutions | maasolar.in, info@maasolar.in, +91 8019 182 249, Hyderabad — no active Meta ads found | Same profile as Varahi; keep as a second no-ads lead |
| Mamindla Energy Solutions LLP | m-e-solutions.co.in, Hyderabad & Warangal, govt-empanelled — no active Meta ads found | Website-only lead, no ad evidence |
| SAS Energy (Sri Associates) Pvt. Ltd. | sasenergy.in, Old Alwal, Secunderabad 500010 — no active Meta ads found | Website-only lead, no ad evidence |
| Greentek India Limited | greentekindia.co.in, EPC since 1997, Adani channel partner — no active Meta ads found | Large/listed-style EPC, different buying cycle |

## What is verified vs not

- **Verified live today (2026-10-18):** every Library ID, "started running" date,
  ad copy, page name/URL, destination type, website, email, phone and address above
  — read from the Meta Ad Library and from each company's own live site.
- **Not verified:** audit scores, pixel/tracking presence, PageSpeed and Google Ads
  Transparency data. Google's Ads Transparency Center is a JavaScript app — a plain
  page fetch returns only the shell, so **no Google ad counts are claimed anywhere
  in this file**. Those numbers need the Playwright pipeline, which cannot run in
  the Arena sandbox (no `playwright` module, no chrome/chromium binary, and sandbox
  bash has no outbound TLS: `curl https://example.com` → `SSL_ERROR_SYSCALL`).
  No scores are guessed here.

## Run this on your machine to turn these into deliverable PDFs

```bash
cd performance-marketing-os
pip install -r 01-LEADS/requirements.txt

cd 01-LEADS
# The 4 active Meta advertisers — full website audit + live ad research + PDF
python run_pipeline.py https://www.evergridenergy.in "Evergrid Energy" --city Hyderabad
python run_pipeline.py https://solox.in "Solox Energies" --city Hyderabad
python run_pipeline.py https://www.truzonsolar.com "Truzon Solar" --city Hyderabad
python run_pipeline.py https://www.punarvienergies.com "Punarvi Energies" --city Hyderabad

# Varahi has no Meta ads — expected, not a failure: the report will honestly show
# "no active Meta ads" plus the website audit, Google transparency and competitors.
python run_pipeline.py https://varahienergies.in "Varahi Energies" --city Hyderabad

# QA gate — must print ALL REPORTS PASS before anything is delivered
python verify_report.py --all

cd ../02-OUTREACH
python audit_outreach.py --export   # emails + sequence_manifest.json
```

Then commit + push (audit JSONs, PDFs, generated emails, manifest).

## Pre-audit outreach copy is already written

`../02-OUTREACH/pre_audit_drafts/hyderabad_batch3_2026-10-18.md` holds a full
4-step sequence (initial + 2 follow-ups + breakup) per lead, built **only** from
facts verified live today — live ad copy, Library IDs, funnels and the specific
defects found (Evergrid's FB-form-only ads, Solox's "0+ MW" counters and stale
`mailto:`, Truzon's missing Telugu creative, Punarvi's ad/site phone mismatch,
Varahi's zero paid acquisition). It deliberately contains **no website scores or
pixel/PageSpeed claims**, because those don't exist until the pipeline runs.
Use it to start outreach today if you want; `audit_outreach.py --export` will
produce the audit-personalized versions once the reports are pushed.

## Live-ad PDFs are already generated (website audit still pending)

Because the website half of the audit needs Playwright + Chrome (not available in
the Arena sandbox), these 5 leads now have **live-ad-activity PDFs** built only
from public Meta Ad Library data — with the limitation printed on page 1 of every
report:

```
02-OUTREACH/ads_only_pdfs/
├── audit_Evergrid_Energy.pdf      (2 pages)
├── audit_Solox_Energies.pdf       (2 pages)
├── audit_Truzon_Solar.pdf         (3 pages)
├── audit_Punarvi_Energies.pdf     (2 pages)
└── audit_Varahi_Energies.pdf      (2 pages)
```

Each report contains: the live ads with real **Library IDs**, start dates, ad copy
and clickable "Open the live ad" permalinks · where the clicks land (Facebook lead
form vs own site) · what that costs · the findings read live today · a 30-day
action plan · verified contact details. Each one states in an amber panel that
**no website audit, tracking check or page-speed test was run**, and prints the
exact `run_pipeline.py` command that produces the full report.

Rebuild / re-verify anytime:

```bash
cd 01-LEADS
python ads_only_report.py            # rebuilds JSON + PDF from the verified data
python verify_report.py --ads-only   # QA gate - must print ALL ADS-ONLY REPORTS PASS
```

The gate refuses to pass a report that carries a fake score, a fake pixel
finding, or a missing Library ID. The **full** audit PDFs (with website score,
pixels, PageSpeed) still need the five `run_pipeline.py` commands below.

### The outreach emails for these 5 are already written too

```bash
cd 02-OUTREACH
python ads_only_outreach.py --export   # rebuilds the emails + sequence manifest
```

Writes `generated_emails/ads_only_email_<Company>.txt` (one per lead, each with
the PDF to attach named at the top) and registers all five in
`generated_emails/sequence_manifest.json` as `report_kind=ads_only`, so the
Gmail workflow attaches the **live-ad PDF**, not a full audit. Every line comes
from the Ad Library data above — the emails say out loud that they are an ad
report, not a website audit.

## What Arena does next (after you push)

1. Re-runs `verify_report.py --all` on the pushed reports.
2. Creates ONE initial Gmail draft per lead **with an email** — all five have one
   (Evergrid first: `contact@evergridenergy.in`) — with the PDF attached, then
   records `thread_id` / `mails_sent` / `next_followup_date` via `sequence.py`
   (see `GMAIL_DRAFT_WORKFLOW.md`).
3. Two contact details to confirm before/while sending:
   - Evergrid's page shows `contact@evergridenergy.in` but its `mailto:` points at
     `hello@evergridenergy.in` — if the first draft bounces, retry the second.
   - Solox's `mailto:` points at `Sungosolarenergy@gmail.com`; the displayed
     address is `contact@solox.in`. Phone/WhatsApp (+91 9988133789) is the safer
     first touch if email bounces.
4. Truzon and Punarvi convert on Facebook lead forms, so a Messenger/phone touch
   alongside the email is worth it — Punarvi's ad phone (7997667677) and site phone
   (7799757777) differ; try the site number first.
5. Varahi converts on WhatsApp only, so lead with a WhatsApp/phone touch
   (+91 9666120045) and use email as backup.
6. Follow-ups are drafted in-thread on their +2-day due dates — never as new mails,
   never pre-created.
