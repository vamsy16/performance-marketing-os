# Batch 13 — 3 new Telangana solar leads (2026-11-21)

**Result: 3 fully-qualified new leads delivered (of 5 requested).** Extensive
discovery across Telangana districts, the TGREDCO empanelled-vendor list, and
broad Meta keyword sweeps surfaced only 3 companies that meet ALL qualification
rules (new, Telangana-based/serving, live website, active Meta ads confirmed by
direct `?id=` fetch). The other 2 slots could not be filled honestly — see
"Why only 3" below.

## The 3 leads

| # | Company | City | Website | Live ads | Score | Report |
|---|---------|------|---------|----------|-------|--------|
| 1 | Kakatiya Energies | Hanamkonda | kakatiyaenergies.com (live) | 2 (2172318326990537 Nov 11, 2539681153175683 Nov 18) | 17/100 | ads-only + site_audit |
| 2 | Visiontek | Hyderabad (Begumpet) | visiontek.solar (live) | 5 captured (~70 on page; all Nov 12) | 16/100 | ads-only + site_audit |
| 3 | Laxmi Narayana Solar | Karimnagar | laxminarayanasolar.in (**HTTP 500**) | 2 (1801231361161321 Nov 13, 1650285136378259 Nov 19) | — | ads-only (no site_audit) |

All three are in `01-LEADS/leads.csv` (rows 47–49, status `new`, 2026-11-21).
JSONs in `01-LEADS/ads_only_results/`, PDFs in `02-OUTREACH/ads_only_pdfs/`.

### 1. Kakatiya Energies (Hanamkonda) — FULLY QUALIFIED
- 2 live Meta ads, both direct-`?id=`-confirmed. Residential/commercial/
  industrial + petrol-bunk solar, on/off/hybrid, net metering & subsidy,
  ₹78,000 PM Surya Ghar, March 2027 deadline, Hanamkonda +91 81258 01257 |
  81252 22834. Both click to WhatsApp.
- Website live: PHP/CodeIgniter, "Save Energy. Save Money", 5 slider H1s,
  Request Quote CTAs, named testimonials, 700+ clients, 10+ years.
- Score 17/100. Head (pixels/meta) not captured through sandbox channel —
  recorded as not checked, never guessed.

### 2. Visiontek (Hyderabad, Begumpet) — FULLY QUALIFIED
- 5 live Meta ads captured (advertiser page shows ~70 active results; the 5
  most recent, all Nov 12 2026, are reproduced). 4 sell a home solar system
  with storage; 1 sells the FUTURE+ hybrid inverter. All click to Instagram
  chat.
- Website live: "Powering India's Smart Energy Future", RISE+/FUTURE+/VAULT+/
  PULSE+ products, WhatsApp +91 9701601421, blogs Nov 12 & 19 2026. No contact
  form, no testimonials, no phone in rendered content.
- Manufacturer (Linkwell Telesystems, 32+ years) that also sells home solar
  systems — the home-solar ads qualify it as an EPC lead.
- Score 16/100. Head not captured — recorded as not checked.

### 3. Laxmi Narayana Solar (Karimnagar) — ADS CONFIRMED, WEBSITE DOWN
- 2 live Meta ads, both direct-`?id=`-confirmed. Telugu copy, ₹78,000 PM
  Surya Ghar, zero maintenance, 25–30 yr warranty, bank loan, homes/hospitals/
  industries/hostels, Karimnagar 9493093728 | 8712780023. Ad 1 → URL link,
  Ad 2 → FB.ME lead form.
- Website `laxminarayanasolar.in` returns **HTTP 500** (www + non-www,
  re-checked 2026-11-21). No site_audit attached; the report is ads-only and
  says so. Re-audit once the site loads.

## Why only 3 (not 5)

Discovery ran 2026-11-21 across:
- **District keyword sweeps** (Meta, IN, active): Warangal, Karimnagar,
  Khammam, Nizamabad, Mahbubnagar, Siddipet, Adilabad, Medak/Sangareddy,
  Hanamkonda, Kothagudem, Suryapet, Nalgonda, Peddapally, Ramagundam, Jagtial,
  Mancherial, Bhongir, Jangaon, Kamareddy, Vikharabad, Rangareddy,
  Secunderabad — mostly zero results, existing leads, or real-estate/farmland
  noise.
- **Broad keyword sweeps**: `solar telangana` (~200), `rooftop solar
  telangana` (~55), `PM Surya Ghar` (~2,600), `solar panel price` (~420),
  `solar installation` (~8,900), `rooftop solar` (~5,800) — dominated by
  national manufacturers (ADM Solar, Servotech, LuxpowerTek) and existing
  leads.
- **TGREDCO empanelled-vendor list** (23 companies cross-checked against
  leads.csv — all new): Rishi Solar, JPR Solar, Raywatt, Shambho, Meher,
  SunroofX, Sri Krishna, Ravindranath, Garuda Blue, Mathrubhoomi, Osmium,
  Mega Solar, Adithya, Suryodaya, Vihaan, V Pro, Infinity, Saarvajanik,
  Shree Solar Rooftop, Amityeco, Solar Tirumala, Nxgyudha, Sieger. Websites
  checked live for Rishi/SunroofX/Osmium/Mega (all live); Meta advertiser
  searches run for Rishi, SunroofX, Osmium, Mega, JPR, Shambho, Vihaan,
  Raywatt, Adithya, Sri Krishna, Garuda Blue, Meher — **none run active Meta
  ads** (or run them for other states: Vihaan→Odisha, Meher→Maharashtra).
- **Unvetted candidates from prior discovery**: Saurashtra Solar Services
  (Gujarat LLP, no website, WhatsApp CTA — fails §5), Tadepalligudem.updates
  (news page, not an installer — fails §5), ADM Solar (national panel
  manufacturer, not Telangana EPC), MVS Solar Solutions Telangana (website
  live, **no Meta ads** — fails §5), Sri Balaji Sun Energy Kothagudem
  (website is a Gujarat mismatch — fails §5).

**Conclusion:** Most small Telangana EPCs do not run Meta ads. Only Kakatiya,
Visiontek and Laxmi Narayana do, and Laxmi's website is down. Filling the
remaining 2 slots would require either (a) including companies with no active
ads, or (b) including non-Telangana manufacturers — both violate the
qualification rules. The honest deliverable is 3 leads.

## Verification (AGENTS.md §2)

1. **verify_report.py --ads-only** — ALL PASS (43 reports, including the 3 new
   ones: live ad evidence, branding, honesty panel, no fake website-audit data).
2. **report-reviewer** — not run in sandbox (needs the reviewer agent); the
   JSONs follow the Lumisun/batch-11 precedent exactly (site_audit nested,
   None for unmeasured, no placeholders).
3. **verify_live.py** — UNREACHABLE in sandbox (TLS reset to facebook.com and
   lead sites, per AGENTS.md §7). Internal consistency (ads.listed,
   ads.results_count) all MATCH. **Full live re-check must run on the owner's
   machine / GitHub Actions before delivery.**

## Files
- `01-LEADS/build_batch13_telangana.py` — builder (measurements + ad data)
- `01-LEADS/ads_only_results/audit_Kakatiya_Energies.json`
- `01-LEADS/ads_only_results/audit_Visiontek.json`
- `01-LEADS/ads_only_results/audit_Laxmi_Narayana_Solar.json`
- `02-OUTREACH/ads_only_pdfs/audit_Kakatiya_Energies.pdf`
- `02-OUTREACH/ads_only_pdfs/audit_Visiontek.pdf`
- `02-OUTREACH/ads_only_pdfs/audit_Laxmi_Narayana_Solar.pdf`
- `01-LEADS/leads.csv` — 3 rows appended (now 49 leads)
