# Batch 15 — Telangana (5 leads) · 2026-11-28

**Status: Gate 1 (delivery) PASSED · Gate 3 (live-data consistency, offline) PASSED · Gate 2 (independent
report review) NOT DONE — these five reports are *not* client-ready until a second person signs off.**

No emails, DMs or calls were made. Nothing was sent to any lead.

## What was produced

| Lead | Report PDF | Underlying JSON | Score | Live Meta ads | Live Google ads |
|---|---|---|---|---|---|
| SunSolar Power Systems | `02-OUTREACH/ads_only_pdfs/audit_SunSolar_Power_Systems.pdf` | `01-LEADS/ads_only_results/audit_SunSolar_Power_Systems.json` | 19/100 | 4 | 0 (no advertiser record) |
| PNR Sunrise Energies | `02-OUTREACH/ads_only_pdfs/audit_PNR_Sunrise_Energies.pdf` | `01-LEADS/ads_only_results/audit_PNR_Sunrise_Energies.json` | 23/100 | 1 | 0 ("No ads found") |
| D'LIFE Home Interiors | `02-OUTREACH/ads_only_pdfs/audit_D_LIFE_Home_Interiors.pdf` | `01-LEADS/ads_only_results/audit_D_LIFE_Home_Interiors.json` | 0/100 *(measured-only)* | 5 | ~200 (D'LIFE Interiors Pvt Ltd) |
| Dr. Sridhar Dental | `02-OUTREACH/ads_only_pdfs/audit_Dr_Sridhar_Dental.pdf` | `01-LEADS/ads_only_results/audit_Dr_Sridhar_Dental.json` | 16/100 | 5 | 42 (Dr. Sridhar International Dental Hospital) |
| Galaxy Dental Care | `02-OUTREACH/ads_only_pdfs/audit_Galaxy_Dental_Care.pdf` | `01-LEADS/ads_only_results/audit_Galaxy_Dental_Care.json` | 5/100 *(measured-only)* | 5 | ~300 (advertiser **"Jaydeep"** — flagged, not asserted) |

Built by `cd 01-LEADS && PYTHONPATH=/tmp/pdflibs python3 build_batch15_telangana.py`.
Raw measured data lives in `01-LEADS/batch15_telangana_data.py`; the renderer path is
`ads_only_report.build_measured()` → `audit_pdf.generate_ads_only_pdf()` (Ksquare 5-page layout).

## How each number was read (all on 2026-11-28, IST/UTC same date)

* **Meta ads** — Ad Library, country = India, active ads only. Each advertiser was searched by exact name
  and every captured card was opened (`?id=…`) or read in the advertiser-specific result list. Library IDs,
  start dates, destinations and copy are verbatim in the JSON.
* **Google ads** — Ads Transparency Centre, `region=IN`, `domain=<lead domain>`. The advertiser record was
  resolved on the advertiser page where one exists. "0 ads" entries cite the exact URL + filter in the JSON
  (`google_own.query_url`).
* **Website** — the URL was read directly *and* through the W3C Nu checker's `showsource=yes` view, which
  returns the exact bytes served. Pixels, headings, forms, CTA count, title/meta/OG/schema, phone and
  WhatsApp links come from that source. Validator totals are quoted with the tool named.
* **Not measured, and therefore `None` in the JSON / "not checked" in the PDF:** PageSpeed mobile score and
  LCP (the keyless PageSpeed API could not be reached from the crawler — no 429 is claimed this time, the
  honest statement is "API unreachable"), server response time, and any tracking tag hidden behind
  NitroPack (D'LIFE) or WP Rocket (Galaxy).

## Corrections to what was already in the repo

1. **SunSolar had a full audit from earlier today (`01-LEADS/audit_results/audit_SunSolar_Power_Systems.json`,
   12/100, 7 pages) that contains two wrong claims:** "170 live ads running" (the advertiser's page has
   **4**: 1810233520093832, 2413566255849370, 1866738597708833, 2576227376137902) and "GA4 OK" (there is no GA4 tag;
   only `AW-18179174251`). It also marked testimonials present when the homepage shows none. Rebuilt here at
   **19/100** with those three corrected. **Send the ads-only PDF; the full-audit PDF still sits in
   `02-OUTREACH/audit_pdfs/` and should be treated as superseded until it is regenerated.**
2. **The premise that drafts existed for the other four leads was false.** No JSON or PDF existed for PNR
   Sunrise, D'LIFE, Dr. Sridhar or Galaxy before this batch; only
   `01-LEADS/batches/hyderabad_5_leads_batch4_2026-10-20.md` mentioned them.
3. **`delivery_gate.py` was rejecting every report built with the Ksquare score tiles** — the tile number and
   its label were glued into one token in the PDF text layer (`12/100AUDIT SCORE`), so the gate's
   `\d{1,3}\s*/\s*100\b` check failed even on the reference PDF. Fixed in the renderer (a no-break space is
   emitted after the number), not in the gate. The gate now passes on the five new reports.
4. **The control review was auto-grading some controls with placeholder evidence** ("Ad start dates were not
   captured", "No live ads captured", "Ad copy could not be read") even where this pass had read exactly that
   data. Those five controls per lead (M01, M39, M-CR1, M11, M18, plus M25/M26/M30) are now corrected from
   observation and marked `overridden_on` in the JSON. Dispositions were moved to `fail`/`pass`/`unknown`
   only where the evidence supports it — never to make a report look better.
5. **Partial passes were about to look like clean passes.** A score built only from the checks that *were*
   readable reads as 0/100 or 5/100 with "0 issues found" — which a client reads as a clean bill of health.
   D'LIFE and Galaxy therefore render in the repo's conservative mode, where the panel states the unverified
   count and says a low score is not proof that unmeasured controls are healthy.
6. **Page furniture was solar-only.** Cover tagline, closing card and the "bids on 'solar panel price in…'"
   line now follow the lead's vertical (`01-LEADS/batch15_telangana_data.py` → `vertical`), so a dental PDF
   no longer calls the practice a solar company.

## Prior session's UNREACHABLE result — resolved

The earlier session reported UNREACHABLE for all five. That was an artefact of **how** it fetched: `curl` and
`requests` from the sandbox fail on these hosts (`SSL_ERROR_SYSCALL`, exit 35), and PageSpeed/allorigins/
codetabs/corsproxy/cors.lol are all unreachable, but the platform page fetcher reaches
`sunsolar.info`, `sunriseenergies.in`, `dlifeinteriors.com`, `sridhardental.com`, `galaxydentalcare.in`,
`facebook.com/ads/library` and `adstransparency.google.com` without difficulty. AGENTS.md §7 ("no outbound
access") is wrong for that path. All five sites were read live this session; there is **0 UNREACHABLE** left.

The date/clock discrepancy is also closed: the sandbox clock is UTC and reads 2026-11-28, the Ad Library and
Transparency Centre both render "Nov 12, 2026"-style dates for the same day, and every report is stamped
`checked_on: 2026-11-28`. No source disagreed by more than the timezone offset of its own locale.

## Gate results (run from `01-LEADS/`, `PYTHONPATH=/tmp/pdflibs`)

| Gate | Command | Result |
|---|---|---|
| Structural | `python3 verify_report.py --ads-only` | all five **PASS** (repo-wide run still FAILs on pre-existing legacy reports, e.g. `Varahi Energies` — untouched by this batch) |
| Delivery (Gate 1) | `python3 delivery_gate.py "<company>" --json ads_only_results/audit_<slug>.json` | **PASS ×5** — complete, fresh, pipeline-built, no draft markers |
| Live-data (Gate 3) | `python3 verify_live.py --offline` | **MATCH ×5**, repo total 59 MATCH / 2 DRIFT / 0 UNREACHABLE of 61. The two DRIFT are pre-existing (`Ksquare Energy`, `Venus home appliances`) and are not part of this batch |
| Report review (Gate 2) | independent human review | **NOT DONE — see below** |

## Independent third-eye review — still required

I cannot be the second pair of eyes on my own build, so this is what a reviewer must check before anything is
sent. I have pre-checked each item and recorded the result, but that is not a substitute for Gate 2:

1. Every Library ID opens an active ad from the named page (advertiser mis-attribution is the classic trap
   here — Galaxy's Google account is registered to a person, "Jaydeep").
2. Every "0 ads" claim cites the URL + filter actually used (`google_own.query_url` in each JSON).
3. No `fail`/`gap` in the control review contradicts the body text, and no `pass` rests on a tag that a cache
   could be hiding (D'LIFE/NitroPack, Galaxy/WP Rocket are `unknown` on purpose).
4. Scores reconcile with `calculate_audit_score()` output in the JSON (no hand-edited number).
5. The two SunSolar files in the repo are not confused (see correction 1).

## What is still blocked, and why

| Blocked | Why |
|---|---|
| Mobile PageSpeed / LCP for all five | the keyless PageSpeed Insights API is unreachable from this environment |
| Tracking-tag confirmation for D'LIFE and Galaxy | NitroPack / WP Rocket rewrite and defer every script; a page read cannot confirm *or* deny a pixel, so all eight values are `null` |
| Full tracking read for D'LIFE beyond title/H1 | the page exceeded the fetcher's chunk budget before the closing `</head>` was reached |
| SunSolar total HTML error count | the validator halted after its first two errors — 2 is a floor, not a total |
| Sitemap for PNR Sunrise and Dr. Sridhar | not fetched in this pass (recorded `null`, not "no sitemap") |
| Google *competitor* advertisers | no per-competitor Transparency lookup was run; competitor evidence in these reports is Meta-only and says so |
| Ad creative images in the PDFs | creatives cannot be downloaded here, so the PDFs are text-only (~25 KB) rather than the 300–590 KB image versions |
| CI / Actions evidence | the workflow has been red for ≥19 days and dies at the QA gate; nothing from CI is cited as current data |

## Notes for the next operator

* `01-LEADS/batches/hyderabad_5_leads_batch4_2026-10-20.md` records the owner rule "0 live ads ⇒ no PDF".
  All five leads have ≥1 verified live Meta ad, so the rule is satisfied. SunSolar and PNR have **0 live
  Google ads** — that is stated as a finding, not as a disqualification.
* SunSolar now has two JSONs (full-audit and ads-only). `verify_live.py` lists it twice; that is expected.
* Rebuild: `python3 build_batch15_telangana.py [--only "<company>"]`. Re-render only:
  `python3 rereder_ads_only.py`.
