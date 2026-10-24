# Batch 10 — 4 new Hyderabad solar leads (2026-10-24)

User ask: **"Find leads: solar Hyderabad, 5 leads."** Discovery ran ~60 Meta Ad
Library queries across Telugu (`సోలార్ ఆఫర్`, `సోలార్ సబ్సిడీ`) and English
(`solar panels/company/rooftop/installation/commercial/EPC/home/subsidy/panel
price/AMC/apartment Hyderabad`, `PM Surya Ghar Hyderabad`, `solar panels
Secunderabad`) plus named probes. **4 leads verified and approved** (the user
chose to proceed with 4 rather than hunt for a 5th local installer).

Every lead here runs live ads with a resolvable website, per the standing rule
("if 0 live ads means what is the use of audit pdf?").

## Leads (all audited as ads-only reports + claude-ads control review)

| Company | Website | Email | Phone | Live ad(s) | Destination |
|---|---|---|---|---|---|
| Sunova Green Energy | sunovagreenenergy.com | sunovagreenenergy@gmail.com | +91 99128 48596 / 98497 63391 | 1091780746736140 (Aug 31) | fb.me lead form |
| Wisda Energy | wisda.in | connect@wisda.in | +91 91000 47301 / 91001 26750 | 1653176663099926 (Oct 10) | fb.me lead form |
| SolarSquare Energy | solarsquare.in/rooftop-solar-in-hyderabad-1 | welisten@solarsquare.in | +91 98300 03000 / 70300 03000 | 2146365376089965 (Oct 12), 1472241928117694 (Oct 13), 2463859894143954 (Oct 16) | own Hyderabad landing page |
| Rayzon Solar | rayzonsolar.com | contact@rayzonenergies.com | +91 96380 00461 / 00462 | 2046407626037554 (Oct 13) | instagram.com/rayzon_solar |

Two are national brands (SolarSquare — 36,000+ homes, 31 cities; Rayzon —
Surat module manufacturer, 6 GW, ALMM) whose Hyderabad-relevant ads were
included after the user approved proceeding with 4.

## Ad-ID attribution corrections (important)

The Ad Library's metadata block precedes its ad card, and chunk boundaries
misattribute IDs. Two traps were hit and resolved:

- **Sunova = 1091780746736140 (Aug 31)**, not 1041272661680963. The Jun-20 ID
  belongs to **Orbit Solar's** apartment ad (confirmed by opening both IDs
  directly). Sunova's ID was confirmed three times: rooftop-query chunk,
  `solar AMC Hyderabad` query, and the Telugu-subsidy query.
- **Rayzon = 2046407626037554 (Oct 13)**, not 2518444838650356. The Sep-23 ID
  belongs to **Arcedo Systemss** (Telugu subsidy-eligibility ad) — confirmed by
  opening both IDs directly.

## Reports built

- `01-LEADS/ads_only_report.py` — LEADS 31 → 35 entries, each with
  `site_evidence` (what the landing-page check could and could not establish).
- `01-LEADS/ads_only_results/audit_*.json` — 31 → 35.
- `02-OUTREACH/ads_only_pdfs/audit_*.pdf` — 31 → 35, all carrying the
  **claude-ads control review** (per the 2026-10-24 standing instruction) on
  top of the Ksquare ads-only layout.
- `01-LEADS/leads.csv` — 37 → 41 rows (CRLF).
- `02-OUTREACH/generated_emails/sequence_manifest.json` — 37 → 41 sequences.
- Gate: `verify_report.py --ads-only` — **ALL 35 PASS**.

Control-review results (pass / fail / unknown — unknown means "needs account
access, never guessed"):

| Company | Controls graded | Pass | Fail | Unknown |
|---|---|---|---|---|
| Sunova Green Energy | 15 | 4 | 2 | 9 |
| Wisda Energy | 15 | 2 | 5 | 8 |
| SolarSquare Energy | 15 | 4 | 1 | 10 |
| Rayzon Solar | 15 | 2 | 2 | 11 |

The Meta Pixel control (M01) is honestly **unknown** for all four: the
landing pages were read through a text proxy that strips scripts, so pixel
code could not be confirmed either way. The catalog's runtime contract forbids
guessing it.

## Drops this batch (do not retry)

- **Solaronics Green Energy** (Jeedimetla, info@solaronicsgreenenergy.com) —
  0 live ads.
- **Nisha Solar** — 2 live ads (1074205295187882 Sep 7 residential 3 kW
  ₹1,31,999; 951181501381704 Sep 27 commercial 20 KW+) but **nishasolar.in and
  nishasolar.com do not resolve** → no website → no audit.
- **Surana Solar** (suranasolar.com, 040 44665729) — 0 live ads.
- **Mahesh Solar Solutions** (FB 61595199461723) — 1 live ad
  (1365559998797681, Oct 22) but no website (batch-9 drop reconfirmed).
- **Greentek India** — only Kerala landscaping / O-Homes farming ads, no solar
  ads.

## Outreach — 4 step-0 drafts created 2026-10-24 (UNSENT, owner to send)

| Company | To | Draft ID | Thread ID |
|---|---|---|---|
| Sunova Green Energy | sunovagreenenergy@gmail.com | r8672245658090296228 | 1a16c5ada8854291 |
| Wisda Energy | connect@wisda.in | r-6911418009660809427 | 1a16c5afd49e13ca |
| SolarSquare Energy | welisten@solarsquare.in | r-1045940870714107417 | 1a16c5b20d3ee424 |
| Rayzon Solar | contact@rayzonenergies.com | r-2836600481260964329 | 1a16c5b42b8b0477 |

Each carries its own ads-only PDF (never a full audit PDF), all verified via
`gmail list_drafts`. Step 1 for each falls due **2026-10-26** (2-day cadence)
once the owner sends.

Gmail now holds **12 unsent drafts**: 8 step-2 follow-ups + these 4 step-0s.
Suggested slots for the batch-10 four: 21:30 / 21:42 / 21:54 / 22:06 IST.
