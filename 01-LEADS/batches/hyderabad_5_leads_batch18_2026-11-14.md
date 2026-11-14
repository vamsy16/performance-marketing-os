# Batch 18: Solar Hyderabad — 5 NEW Active-Advertiser Leads (live-verified 2026-11-14)

Pulled **2026-11-14**. Same rule as every batch since the de-dup guard was
built: every candidate was checked against the whole known-leads registry
(`known_leads.py`, 271 entries across 14 sources) **before** it could be rowed,
and anything already in the pipeline was skipped and reported.

**5 new leads rowed into `01-LEADS/leads.csv` (57 → 62 rows):**

| # | Lead | Live ad evidence (all read 2026-11-14) | Conversion destination | Website | Contact (verified live 2026-11-14) |
|---|---|---|---|---|---|
| 1 | **KehanSri Technologies & Service Pvt Ltd** | **24 live Google ads** under identity-verified advertiser `AR07894673884648046593` — Display images plus a YouTube video creative | kehansrisolar.com (the site itself) | https://kehansrisolar.com/ | **info@kehansri.com** · +91 888 628 6000 / +91 9985408601 · 2-55, Opposite Ingenium School, Sri Shyam Nagar, Telecom Nagar, Gachibowli, Hyderabad 500032 (regd. office 472 Rohit Nagar Phase-1, Bavadiakala, Bhopal 462039) |
| 2 | **Hysun Solar Pvt. Ltd.** | **1 live Google ad** under identity-verified advertiser `AR08880526109242818561`, plus live Meta ads | WhatsApp / Facebook lead form — every click bypasses hysunsolar.com | https://www.hysunsolar.com | **info@hysunsolar.com** · +91 7573999966 · toll-free 1800-270-0025 (the Meta ads carry a second number, +91 7573999960) · Suncity, Bandlaguda Jagir, Hyderabad 500091 |
| 3 | **V1 Solar Solutions** | **4 live Google ads** under identity-verified advertiser `AR09270299175948386305` (VIJAYA KUMAR) pointing at v1solarsolutions.com, **plus** a live Meta ad (Library ID 1446165934284837, started Oct 12 2026) run by the agency 99Ad Solutions | api.whatsapp.com (Meta) / the .com site (Google) | https://www.v1solarsolutions.com/ | **info@v1solarsolutions.com** · +91 9066631441 · 7, Magadi Main Rd, Asthagrama Layout, Kamakshipalya, Bengaluru 560079 |
| 4 | **Mega Solar India (Mega Creations)** | **2 live Google ads** under identity-verified advertiser `AR09804983159320739841` (VELPULA INDIRA NIRMALA), creatives CR16648633552560193537 and CR04546876387859890177 | megasolarindia.com | https://megasolarindia.com/ | **none published** — see blocked note below |
| 5 | **PNR Sunrise Energies Pvt Ltd** | Live Meta ad, Library ID **28807326382303186**, started **Nov 12 2026** (two days old when swept) | api.whatsapp.com | https://sunriseenergies.in/ | **none published** — see blocked note below |

## How the 5 were found

| Source | What it gave |
|---|---|
| Google Ads Transparency `?domain=` probes (7 run today) | **KehanSri** (24 ads — the largest live Google ad count found in any sweep so far), **Hysun Solar** (1), **V1 Solar Solutions** (4), **Mega Solar India** (2). Zero ads for sriishaansolar.com, solluz.co.in, greensolarpower.in, slrsurabhi.com, assureenergy.in, somayasolar.com, sunsolarpowersystems.in/.com, sunsolarhyd.com, sunriseenergies.in |
| Meta Ad Library `solar panel Hyderabad`, `solar pump Hyderabad`, `solar AMC Hyderabad`, `solar installation Hyderabad` (~83 results), `solar service Hyderabad` (~30), `solar EPC Telangana`, `solar subsidy Telangana` (~62), `solar water heater Hyderabad`, `solar company Kukatpally` (0), `solar EMI Hyderabad`, `rooftop solar Telangana`, `solar company Secunderabad` | **Surya Shakti Solar Energy**, **PNR Sunrise Energies**, **V1 Solar Solutions** (via 99Ad Solutions), plus re-confirmation that Sri Balaji, SunSolarhyd, Valcan, Teramor, SolarSquare, Krisol, Kypas, Varna, Orbit, Lumisun, Big G, Venus, mrsolar.in, Manasa Enterprises, Sunova, Wisda, Lotus Industries, Eastman and Wisda are all already rowed |
| Each company's own site, fetched today | Every email/phone/address in the table above was read off the live page today |

## De-dup guard — what it caught this run

The registry (`python known_leads.py`) is now built from **14 sources** and
holds **271 entries / 63 domains / 118 names / 26 active vetoes**:
`leads.csv` (62), `sequence_manifest.json` (57), audit + ads-only JSONs (60),
`known_leads_extra.json` (8) and **11 batch-log discovery logs (84 names)** —
the logs were added this session because a business vetted and rejected in a
log never entered `leads.csv` and so resurfaced on every sweep.

Skipped as already-known during this run: **Twilight Solar** (already in
`leads.csv` as twilightsolar.com), **Manasa Enterprises** (batch logs),
**Shree Adithya Solar** (batch log hyderabad_5_leads_batch2, vetted 2026-10-18),
**Sri Balaji Solar Energies**, **Valcan Solar**, **Eastman New Energy**,
**Sunova Green Energy**, **Big G Industries** (vetoed), **Lumisun**,
**Krisol Solar**, **Kypas Solar**, **Varna Solar**, **Orbit Solar**,
**mrsolar.in**, **Venus home appliances**, **SolarSquare Energy**,
**Lotus Industries**, **Wisda Energy**.

### Two real bugs fixed in the guard this session

1. **`Surya Shakti Solar Energy` was being reported KNOWN against
   `Shakti On Roof`.** A single shared freq-1 token (`shakti`) was enough to
   declare a match, and `shakti` is one of the commonest words in Indian solar
   company names. Added a `NON_IDENTIFYING` set (solar, power, energy, green,
   sun, shakti, surya, tech, solutions, systems, services, enterprises,
   industries, india, mega, …) that can support a match alongside a real brand
   word but never identify a business alone. `Surya Shakti Solar Energy` now
   correctly reports NEW.
2. **`Adithya Solar Works` was being auto-cleared as KNOWN against
   `Adithya Solar Tech`.** `norm_name()` strips `tech` as generic, so
   "adithya solar tech" normalised to "adithya solar" and looked like a prefix
   of "adithya solar works". Name containment now defers to the same
   token-rarity rules as everything else, so near-miss Adithya names report
   **REVIEW** and are never silently cleared — matching your standing
   instruction. `Adithya`/`Aditya` were deliberately kept out of
   `NON_IDENTIFYING` so the family of Adithya businesses keeps flagging for
   review rather than passing.

`cd 01-LEADS && PYTHONPATH=<pdflibs> python3 tests.py` → **31/31 OK** after
both fixes.

## Blocked — rowed but NOT emailable

| Lead | Why blocked |
|---|---|
| **Mega Solar India (Mega Creations)** | `megasolarindia.com/contact/` is an **unedited WordPress demo**: `info@example.com`, `enrollment@example.com`, `collab@example.com`, the address "Demo St, Brooklyn, NY 11223, United States", the phone `+1 123-456-7890`, and form fields "Parent's Name" / "Questions Parent's" with Infant / Toddler / Preschool options. The only live contact path on the whole site is a WhatsApp chat widget. 2 live Google ads, real Hyderabad residential-installer copy (₹78,000 PM Surya Ghar, no-upfront-cost, pay-as-you-save, 7-day install, 25-year warranty, Waaree/Adani/Premier/Panasonic/Polycab/Microtek) — and nothing to send it to. The demo contact page is itself the pitch. |
| **PNR Sunrise Energies Pvt Ltd** | No email anywhere on sunriseenergies.in — only the request-assessment form, `wa.me/+916304587145` and `tel:+916304587145`. Real, well-built EPC site (working solar calculator, six-step process, project showcase, three named testimonials, MNRE-grade management bios) and a two-day-old Meta ad, but phone/WhatsApp only. |

## Dead ends closed today (do not retry)

- **`sunsolarpowersystems.com` is NOT the Hyderabad SunSolarhyd advertiser.** The FB page (SunSolar Power Systems, Suite 312, Kokapet Terminal Complex, Gandipet Main Road, Narsingi, +91 98666 02001) shares **no** contact detail with that site — sunsolarpowersystems.com publishes wa.me/919489231133 and tel:+917708001737, the same numbers as the Tamil Nadu company sunsolarps.com (Karaikudi/Ramanathapuram, GST-based). The Hyderabad SunSolarhyd has **no findable website or email**.
- **Surya Shakti Solar Energy** (2 live Meta ads, IDs 2216955152329459 and 1842297396946112, both started Nov 11 2026, +91 8106659816 / +91 9885349010, Hyderabad) has no web footprint — a 2026-11-14 search returned only unrelated businesses: Surya Shakti (India) Pvt Ltd, Chandigarh (suryashakti.biz), a Kathua J&K retailer, Surya Shakti Switch On The Sun (B.N. Reddy Nagar, Hyderabad) and Surya Shakti Traders (L.B. Nagar). Needs an independent email source before it can be rowed.
- **Solar Power Experts** (Meta, heat-resistant panels, fb.me) — a 2026-11-14 search found no such company. No website, no email.
- **Teramor Developers** (Meta ID 1176536348031731, Nov 12 2026) is a **real-estate developer** (teramor.in, sales@teramor.in, +91 88851 33939, Madhapur/Shamirpet/Kompally/Hafeezpet) — out of segment, do not row.
- **Cygni Energy** (cygni.com, 1 Google ad) is an LFP **battery/BESS maker**, not a rooftop installer — out of segment.
- **Zero-ad domains re-confirmed today:** sriishaansolar.com, solluz.co.in, greensolarpower.in, slrsurabhi.com, assureenergy.in, somayasolar.com, sunsolarpowersystems.in, sunsolarpowersystems.com, sunsolarhyd.com, sunriseenergies.in.
- **`solar company Kukatpally` returns 0 Meta ads.** `solar EPC Telangana` returns only Lotus Industries (already rowed). `solar AMC Hyderabad` returns only Sunova (already rowed).

## Not done — sandbox limits, needs a machine with a browser

- **No audit scores, no PDFs, no Gmail drafts were produced for this batch.**
  `discover_leads.py` steps 2–3 (live ad activity + branded PDF) drive
  Playwright, and this sandbox has no Chromium: `playwright install chromium`
  fails on the CDN download and there is no system Chrome for
  `channel="chrome"`.
- **De-dup and grouping were still run end-to-end.** `discover_leads.py` now
  takes `--feed <json>` to replay a live-captured ad feed instead of launching
  Playwright, so the discovery + duplicate-guard half runs identically
  headless. Today's run
  (`python discover_leads.py "solar panel Hyderabad" --limit 5 --city Hyderabad --feed feeds/solar_hyderabad_2026-11-14.json`)
  printed the registry summary, skipped 6 known advertisers with their matched
  sources, and reported the new ones. The captured feed is saved at
  `01-LEADS/feeds/solar_hyderabad_2026-11-14.json`.
- **3 of the 5 leads have a verified email**, so 3 drafts can be created once
  the PDF step runs: KehanSri, Hysun Solar, V1 Solar Solutions.
- **Deps for local runs:** `pip install --target <dir> requests beautifulsoup4
  lxml reportlab playwright` then `PYTHONPATH=<dir>`.

## Still waiting on you

- 25 follow-ups are past due as of 2026-11-14 (12 step-3 breakups, 7 step-2
  follow-ups, 6 step-1 follow-ups) — see the pending schedule table. Nothing
  has been sent since 2026-11-10.
- Valcan Solar step-1 is still unresolved (draft r-4135467498809954457,
  trashed + bounced).
- Tell me if you want Mega Solar India and PNR Sunrise Energies approached by
  phone/WhatsApp instead of email, or held until an address turns up.
