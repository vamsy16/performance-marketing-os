# Batch 6: Solar Hyderabad — 3 NEW Active-Advertiser Leads (live-verified 2026-10-21)

Pulled **2026-10-21**. Same rule as batch 5 — every lead was found **by its running
Meta ads**, verified live today, and its report is built from real Library IDs.

| Source | What it gave |
|---|---|
| Meta Ad Library (India, active ads), Telugu query `సోలార్ సిస్టమ్`, ~53 results across 4 chunks | The main vein: **Ecolt Energy**, **Orizen Solar Innovations**, **Ray On Solar Systems** — all Telugu advertisers with live ads. |
| Meta Ad Library (India, active ads), `solar Kukatpally`, ~9 results | 3S Solutions (already in `leads.csv`, more ads since), **Oorza Solar Solutions** (no verifiable website — held), **NESS Surveillance and Solar** (CCTV business, no site — excluded). |
| Meta Ad Library, `solar Gachibowli` / `solar Begumpet` | Zero solar advertisers — real-estate noise only. Confirms locality probes are close to exhausted. |
| Each company's own website, fetched today (2026-10-21) | Every email/phone/address below was read off the live page today. |

## Why the batch is 3 leads, not 5

Discovery was honest this round: the three verified, website-live advertisers below
are what the Ad Library actually surfaced that wasn't already in `leads.csv`. Two
more advertisers — **Oorza Solar Solutions** (KTR Colony, Kukatpally, 9966991621,
Library ID 1637195787866967, Oct 13) and **Ss solar solutions** (Library ID
1097618436576477, Oct 10) — run live ads but have **no verifiable website**, so
per the repo's lead-hygiene rule (rows need a resolvable website) they are held,
not added. NESS (Kukatpally) is a CCTV shop with solar as a side line and no site —
excluded.

## The 3 leads

| # | Lead | Live ad evidence | Conversion destination | Website | Contact (verified live 2026-10-21) |
|---|---|---|---|---|---|
| 1 | **Ecolt Energy** | 2 live Telugu ads, one creative: Library ID 1405421181747986 (started Oct 13, 2026). 3KW at ₹1,90,000, ₹33,000 off, ₹78,000 PM Surya Ghar subsidy, "AP & Telangana" | **Facebook lead form only** (fb.me 'Sign up') | https://www.ecoltenergy.com/ | Contact@ecoltenergy.com · +91 83411 13782 (site) / +91 82475 37597 (ad) · 8-1-87/4/7/2, Vinayak Nagar Colony, Shaikpet, Hyderabad 500033 (reg. Narasaraopet, AP) |
| 2 | **Orizen Solar Innovations** | Live Telugu ad: Library ID 3529873930505195 (started Sep 18, 2026, multiple versions). Dussehra & Deepavali Dhamaka: ₹78,000 subsidy, 3KW + ₹10,000 off, 5KW + ₹20,000 off, WAAREE channel partner | **WhatsApp only** | https://www.orizensolar.com/ | info.orizensolar@gmail.com · +91 9962039859 (site) / 8374 670 999, 8374 683 999 (ad) · Ring Road, Chandramouli Nagar, Vidyanagar, Guntur 522007 (+ Vijayawada & Tirupati offices) |
| 3 | **Ray On Solar Systems** | Live ad: Library ID 1107666674962232 (started Oct 13, 2026). 3kW at a special price with subsidy and long-term warranty | **Instagram** (ad links to instagram.com/ray_on_solar_systems_; Get Quote → fb.me) | https://www.rayonsolarsystems.in/ | rayonsolars@gmail.com · +91 8500976346 / +91 9703774654 · Ravi Nagar, Naidu Thota, Visakhapatnam 530029 |

### Per-lead notes (all read live 2026-10-21)

**1. Ecolt Energy** — the only genuinely Hyderabad-headquartered advertiser of the
batch (Shaikpet office; registered in Narasaraopet, AP), with the best-built site
of the three: an interactive bill-vs-solar comparison, a savings calculator, a
project map across AP & Telangana, a WhatsApp chat and a multi-step quote form.
And yet both live Telugu ads dump the click into a Facebook lead form. Three
quotable breaks on the live site: the "Real projects, real power" counters all
read **0** (0 MW installed, 0 projects, 0 CO₂ offset) while the hero claims
**2,000+ systems installed** and **95% avg. bill reduction**; the weather widget
reads "Right now in **Virginia Beach**: 16°C, clear skies" — hardcoded to a US
city on a Hyderabad solar homepage; and the ad's WhatsApp number (+91 82475 37597)
differs from the site's (+91 83411 13782). Angle: they already have the machinery —
it just isn't in the paid path.

**2. Orizen Solar Innovations** — a Guntur EPC (three AP offices: Guntur,
Vijayawada, Tirupati) advertising the Dussehra & Deepavali offer into Telangana in
Telugu, with every click going to WhatsApp. The site is a template build that was
never finished: the PM Surya Ghar blurb reads "At **Your Solar Partner**, we are
proud to support this initiative" (company name never filled in), the features
heading says "Features of **Origin** Solar Panels" (typo for Orizen), and every
"Read More" service link points at "#" — the homepage anchor — so the on-grid,
off-grid and hybrid pages are unreachable from the homepage flow. Claims 456+
projects, 513+ happy customers, 10+ years. Three phone numbers across the funnel
(ad 8374 670 999 / 8374 683 999 vs site +91 9962039859). Angle: build an owned
offer page, finish the template, unify the numbers.

**3. Ray On Solar Systems** — a Visakhapatnam installer advertising into Telangana
with one live ad — and the ad's creative link goes to **Instagram**, while its
"Get Quote" button goes to a generic fb.me link. The click never touches
rayonsolarsystems.in, which is a clean WordPress site with a free-quote form,
PM Surya Ghar subsidy assistance and a monitoring-app section. One ad, no second
creative, no retargeting. Angle: point the ad at the site's own quote page (or a
dedicated 3kW offer page), capture before the chat, add Telangana-local proof.

## Excluded — already staged, drafted or sent

All of batch 5 (Valcan Solar, Eastman New Energy, Ellvin Energy, Kapil Power &
Infra, Solar6), 3S Solutions (in `leads.csv` with a live-ad row — 5+ ads seen this
round, incl. one pointing at 3scalculator.vercel.app), plus the whole existing
pool (Twilight, Evergrid, Solox, Truzon, Punarvi, Varahi, Ksquare, Venus, Sri
Balaji, ORBIT, AB Solar, Suryon/Arcedo, Green Carbon Hub, mrsolar.in, ARKA, Hysun,
Krisol).

**Held — live ads but no verifiable website (revisit if they get one):**
Oorza Solar Solutions (KTR Colony, Kukatpally, 9966991621, Library ID
1637195787866967, Oct 13), Ss solar solutions (Library ID 1097618436576477, Oct 10).

**Keyword noise in the Telugu feed:** G Interiors (Kadapa interiors shop selling
panels), MRK Associates / Bezawada Realty / Golden Green Farms / Siva kumar page
(plots & agro ventures), NESS Surveillance (CCTV business), FreyrEnergy and Rayzon
(too large), national brands.

## Notes for whoever picks this up

- All 3 leads have their ads-only reports — built 2026-10-21, each with real
  Library IDs, `checked_on: 2026-10-21`, and the `WEBSITE AUDIT NOT RUN` panel.
  18/18 ads-only reports pass `verify_report.py --ads-only`.
  Reports: `02-OUTREACH/ads_only_pdfs/audit_Ecolt_Energy.pdf`,
  `audit_Orizen_Solar_Innovations.pdf`, `audit_Ray_On_Solar_Systems.pdf`
  (+ JSONs in `01-LEADS/ads_only_results/`).
- **Full audits BUILT 2026-10-21 with real live data** (see section below). The
  owner-side pipeline remains the way to embed ad-creative thumbnails; everything
  else is already verified live:
  - `python run_pipeline.py https://www.ecoltenergy.com/ "Ecolt Energy" --city Hyderabad`
  - `python run_pipeline.py https://www.orizensolar.com/ "Orizen Solar Innovations" --city Hyderabad`
  - `python run_pipeline.py https://www.rayonsolarsystems.in/ "Ray On Solar Systems" --city Hyderabad`
- All 3 rows are appended to `01-LEADS/leads.csv` with `status: new` (→ 76 rows).
- **Discovery recipe status:** Telugu `సోలార్ సబ్సిడీ` and `సోలార్ సిస్టమ్` are now
  both fully mined, and locality probes (`solar Secunderabad`, `solar Kukatpally`,
  `solar Gachibowli`, `solar Begumpet`) are exhausted. Next batch will need fresh
  queries — e.g. `solar LB Nagar`, `solar Kompally`, Telugu `రూఫ్‌టాప్ సోలార్`, or
  name probes against the TGREDCO 2026 alternates (Gigawatt, Green Secure, Solar
  Idea, Helios, Axis, Bandaru, Aditi, E-Mug, Envious, A&T Power).

## Full website audits — built 2026-10-21 (real live data)

All three sites were audited line-by-line from their live source (fetched via the
W3C Nu Html Checker source view — head, wp_head, body, footer, sitemaps, wp-json
and Google/Meta transparency centres all read in full). JSONs:
`01-LEADS/audit_results/audit_{Ecolt_Energy,Orizen_Solar_Innovations,Ray_On_Solar_Systems}.json`
(builder: `01-LEADS/build_batch6_full_audits.py`, reproducible). PDFs:
`02-OUTREACH/audit_pdfs/audit_{same}.pdf` — 4 pages each, same format as
audit_Ksquare_Energy.pdf. Scores use the repo's own formula (higher = more problems).

| Lead | Score | Live Meta ads | Google ads | Tracking | Biggest verified findings |
|---|---|---|---|---|---|
| Ecolt Energy | 15/100 | 2 ads, 1 creative (ID 1405421181747986, Oct 13) | none (0 in transparency centre) | none of 8 tools | Project map explicitly labelled "placeholder EXAMPLES only" in its own source; stat counters render 0 without JS; quote popup re-opens every 30s; everything else (form, WhatsApp, chat, meta/OG/schema, 18-page sitemap + Telugu version) is in place |
| Orizen Solar Innovations | 23/100 | 1 ad, multiple versions (ID 3529873930505195, Sep 18) | 1 ad (verified advertiser Palisetty Ranadheer Kumar) | Meta Pixel only (ID 1655381782019850, PageView only — no Lead event) | Hero carousel H1s commented out; "At Your Solar Partner" placeholder live; floating email icon → mailto:example@example.com; "Features of Origin Solar Panels" (Origin ≠ Orizen); no OG tags, no schema, no sitemap (404); 10+ vs 17+ years contradiction on the same page |
| Ray On Solar Systems | 31/100 | 1 ad (ID 1107666674962232, Oct 13) — click goes to Instagram | none (0 in transparency centre) | none of 8 tools (HFCM plugin carries only a Search Console tag) | All "Get Started" buttons → /contact/ (404); phone numbers are plain text (no tap-to-call); schema uses invalid https://schema.org URLs (12 errors); title says "Suryodhya ghar" and never names the company; WordPress version exposed |

Honesty notes: PageSpeed/Lighthouse was unavailable in the build environment, so
it renders "Not available at audit time" (Ksquare precedent). Ad-creative
thumbnails could not be downloaded in the build environment (ad-library CDN
blocked) — the reports carry the live ad copy, Library IDs and links instead; the
same text-only format the repo documents for ads-only reports (12-14KB). Rebuild
locally with `python audit_pdf.py "<Company>"` from 01-LEADS to embed creatives
(owner-built full reports run 300-590KB). Every number in the JSONs was verified
live on 2026-10-21; competitor Meta ads (~180 results) and WAAREE's Google ads
were verified the same day (Venus + Orbit Solar verified 2026-10-18, noted in the JSONs).
