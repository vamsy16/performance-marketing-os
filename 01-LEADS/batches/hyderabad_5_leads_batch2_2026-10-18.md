# Batch 2: Solar Hyderabad — 5 NEW Leads from the Live Meta Ad Library

Pulled 2026-10-18 from the **live Meta Ad Library** (India, active ads), using
the same discovery flow `discover_leads.py` implements — start from the ads,
not from a name list.

Two market probes were run (the market, not one keyword):

| Probe query | Ad Library says | Advertisers read from the DOM |
|---|---|---|
| `solar Hyderabad` | ~330 results | 11 advertisers (Venus, Sri Balaji, ORBIT, AB Solar, Suryon, **Mahadev Enterprises**, **Green Carbon Hub**, mrsolar.in, ARKA, Shreepad Avenue, Mahaveer Constructions, Hi Kanpur+Freyr) |
| `rooftop solar installation Hyderabad` | active results | **Hysun Solar**, **3S Solutions**, **Shree Adithya Solar**, ORBIT, **Krisol Solar**, **Mahesh Solar Solutions** |

Excluded because they are already audited/drafted in this repo: Ksquare
Energy, Sri Balaji Solar Energies, Venus home appliances, ORBIT SOLAR,
AB Solar Power Systems, Suryon, mrsolar.in, The ARKA SOLAR POWER.

Excluded as keyword noise (they match "solar"/"Hyderabad" but are not solar
installers to pitch): Shreepad Avenue (3BHK bungalows, Bharuch, Gujarat),
Mahaveer Constructions (villa plots, Dundigal — "solar fencing" in copy),
Hi Kanpur + FreyrEnergy (national brand, ad targets Kanpur).

**Ad → advertiser pairing was verified, not assumed.** Each ad card was
confirmed through its own permalink (`facebook.com/ads/library/?id=<id>`),
which returns the single card with its page name: Library ID 1645269633918455
→ Krisol Solar (page 434211683116209), Library ID 1283230217176481 → 3S
Solutions (page 106719394141333). The remaining IDs come from the same card
ordering that those two checks confirmed.

## The 5 leads

| # | Advertiser (lead) | Live ad evidence | Conversion destination | Website | Contact (verified live) |
|---|---|---|---|---|---|
| 1 | **Hysun Solar Pvt. Ltd.** (FB: Hysunsolarhyderabad) | Library ID 39155815814063400 (started Oct 14, 2026) + 1205044528744768 (Oct 14, 2026, "2 ads use this creative") | WhatsApp (`api.whatsapp.com` / "Send WhatsApp message") + FB forms | https://www.hysunsolar.com | info@hysunsolar.com · +91 7573999966 (site) · toll-free 1800-270-0025 · ad phone +91 7573999960 |
| 2 | **Krisol Solar Infra Pvt. Ltd.** (FB: krisolsolar) | Library ID 1645269633918455 — started Oct 16, 2026 (permalink-verified) | FB lead form: "Claim ₹22,000 Solar Discount" → Get offer | https://www.krisolsolar.com | sales@krisolsolar.com · krisolsolarinfra@gmail.com · +91 7337337677 · Fairmount Square 3rd Flr, Unit 312, Kompally, Medchal-Malkajgiri 500014 |
| 3 | **3S Solutions India Pvt. Ltd.** (FB: 3SSolutionsSolarServices) | Library ID 1283230217176481 — started Sep 11, 2026 (permalink-verified) | Messenger ("Send message") | https://3ssol.in | praveen@3ssol.in · +91 9581177119 · 3rd Flr, Plot 196, Rd No 20, Vivekananda Nagar, Kukatpally 500072 (FB page also lists info@3ssol.in / +91 9000121084) |
| 4 | **Shree Adithya Solar** (FB: shreeadithyasolar) | Library ID 1489241276343354 — started Sep 10, 2026 | FB lead form: "Hyderabad Homes: Get Up to ₹78,000 Subsidy" → Get quote | **none found** | none public — FB page/Messenger only |
| 5 | **Mahesh Solar Solutions** (FB page 61595199461723, ads signed "Mahesh Solar & Renewables") | Library ID 1442761614256484 — started Oct 16, 2026 | FB lead form: "Go Solar, Save on Electricity Bills" → Get Quote | **none found** | +91 7330917033 (from ad copy) — Hyderabad \| Secunderabad & nearby |

### Per-lead notes (all read live today)

**1. Hysun Solar** — the biggest, most obvious gap in this batch. Their Meta
ads sell Hyderabad ("Suncity, Bandlaguda Jagir, Hyderabad – 500091",
+91 7573999960, PM Surya Ghar ₹78,000, on-grid/off-grid/hybrid, EMI), but
`hysunsolar.com` is an unmodified template: the header block opens with
leftover insurance boilerplate ("The insurance company assumes the financial
risk of covering these events…"), the office address is **Ahmedabad**
("10 Radhekrishna Ind Hub, B/H Hinglaj Mata Mandir, Vill: Ahmedabad (M
Corp.+OG)"), the team page lists Gujarat-based directors, and the phone on
the site (+91 75739 99966) does not match the phone in the ad (7573999960).
Every rupee of ad spend is landing on a page that says another city. Pitch:
landing page + city-consistent conversion page + pixel/lead tracking.

**2. Krisol Solar** — Krisol Solar Infra Pvt. Ltd., a subsidiary of Satya
Enterprises, serving Telangana / AP / Karnataka / Maharashtra. Real, complete
website (products, FAQ, subsidy content, quote form) and two public emails.
Ad angle is pure discount ("₹1 Lakh off: ₹78,000 subsidy + ₹22,000 Krisol
discount"), and the CTA dumps the click into a Facebook lead form instead of
their own quote form — so no pixel ownership of the conversion. Pitch:
send ad traffic to their own tracked quote page, retargeting, and local SEO
for "solar company Hyderabad/Telangana".

**3. 3S Solutions** — distributor (Growatt / Vikram, AP + TG) *and* rooftop
installer, TGREDCO-empanelled (TSRE240328 in the 2026 supplier list),
11–25 staff, Kukatpally. The site ranks for blog queries but the homepage is
wall-to-wall keyword-stuffed article text rather than a conversion page, and
contact details are inconsistent across their own pages (contact page:
praveen@3ssol.in / +91 9581177119; FB page: info@3ssol.in / +91 9000121084;
an older blog footer: +91 7075441637). Ad runs to Messenger. Pitch:
homepage conversion rebuild + call/email tracking + separate distributor vs
installer funnels.

**4. Shree Adithya Solar** — active since Sep 10, 2026 with a clean
residential offer (free site visit, loan assistance, 25-year panel warranty,
₹78,000 subsidy, "Serving Hyderabad & surrounding areas") but **no website,
no email and no phone in the ad** — 100% Facebook lead form. Web search
returns similarly named but *different* Hyderabad companies (Shree Solar
Rooftop Solutions, Aadithya Solar Energies, Adithya Solar Tech); none is
confirmed as this advertiser, so no website is claimed here. Pitch: they are
paying Meta for leads with no owned destination — website + landing page +
Google Business Profile. Reach via Messenger/FB page; find an email or phone
before drafting (see workflow below).

**5. Mahesh Solar Solutions** — active since Oct 16, 2026, bilingual
Telugu/English creative, same residential subsidy/loan offer, phone
+91 7330917033 in the copy, FB lead form only, no website found. Note: an MCA
entity "Mahesh Solar Solution Private Limited" (CIN U35105AS2024PTC027345)
exists but is registered under RoC-Guwahati (Assam) — **not** confirmed to be
this Hyderabad advertiser, so it is deliberately not attached to the lead.
Pitch: same as #4, plus Telugu-language landing page/ads, which is a real
edge in this market.

## Also seen today (next batch, not counted in the 5)

| Advertiser | Library ID | Started | Why deferred |
|---|---|---|---|
| Green Carbon Hub | 1387783212859779 | Aug 30, 2026 | Solar O&M / AMC ("lifetime maintenance"), Hyderabad, FB lead form — different service line than the installer offers |
| Mahadev Enterprises | 1584651429611307 | Oct 14, 2026 | Solar *street lights* only (Troop Bazar \| Jambagh, +91 8686285272), ad destination is an Instagram profile |

## What is verified vs not

- **Verified live today (2026-10-18)**: every library ID, "started running"
  date, destination type, ad angle, website, email, phone and address above —
  read from the Meta Ad Library and from each company's own live site.
- **Not verified**: audit scores, pixel/tracking presence, PageSpeed and
  Google Ads Transparency data. Those need the pipeline (Chrome + Playwright),
  which cannot run in the Arena sandbox — no `playwright` module, no
  chrome/chromium binary, and sandbox bash has no outbound TLS
  (`curl https://www.krisolsolar.com` → SSL_ERROR_SYSCALL). No scores are
  guessed anywhere in this file.
- **Correction to an earlier note** (`hyderabad_5.md` claimed the Arena
  sandbox cannot reach the ad library): the *Ad Library data itself is
  reachable* from Arena via its page-fetch tooling — that is how this batch
  was built. What still requires the owner's machine is the Playwright-driven
  pipeline: website audit, creative downloads, Google transparency, PDF build.

## Run this on your machine to turn these into deliverable PDFs

```bash
cd performance-marketing-os
pip install -r 01-LEADS/requirements.txt

cd 01-LEADS
# The 3 leads that have a website — full audit + live ad research + PDF
python run_pipeline.py https://www.hysunsolar.com "Hysun Solar" --city Hyderabad
python run_pipeline.py https://www.krisolsolar.com "Krisol Solar" --city Hyderabad
python run_pipeline.py https://3ssol.in "3S Solutions" --city Hyderabad

# Leads 4 & 5 have no website — discovery mode handles the lead-form funnel
# honestly (report shows NO WEBSITE FOUND instead of a fake score).
python discover_leads.py "rooftop solar installation Hyderabad" --limit 8

# QA gate — must print ALL REPORTS PASS before anything is sent
python verify_report.py --all

cd ../02-OUTREACH
python audit_outreach.py --export   # emails + sequence_manifest.json
```

Then commit + push (audit JSONs, PDFs, generated emails, manifest).

## What Arena does next

1. Re-runs `verify_report.py --all` on the pushed reports.
2. Creates ONE initial Gmail draft per lead **that has an email** (Krisol
   `sales@krisolsolar.com` and 3S Solutions `praveen@3ssol.in` first, PDF
   attached), then records `thread_id` / `mails_sent` / `next_followup_date`
   via `sequence.py` (see `GMAIL_DRAFT_WORKFLOW.md`).
3. Hysun Solar's email (`info@hysunsolar.com`) is on a site whose address
   says Ahmedabad — worth a phone/WhatsApp first touch (+91 7573999966) to
   confirm you have the right desk before emailing.
4. Shree Adithya Solar and Mahesh Solar Solutions need a contact channel
   found (Messenger DM or the ad's phone) before any draft is created.
   Follow-ups are drafted in-thread on their +2-day due dates — never as new
   mails, never pre-created.
