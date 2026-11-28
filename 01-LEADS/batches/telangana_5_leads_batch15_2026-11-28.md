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
| Galaxy Dental Care | `02-OUTREACH/ads_only_pdfs/audit_Galaxy_Dental_Care.pdf` | `01-LEADS/ads_only_results/audit_Galaxy_Dental_Care.json` | 9/100 *(measured-only)* | 5 | ~300 (advertiser **"Jaydeep"** — flagged, not asserted) |

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

## Second pass — D'LIFE and Galaxy "not checked" rows closed (2026-11-28, 13:5x UTC)

The first pass recorded both sites' tag layer as unreadable because their caches
(NitroPack on D'LIFE, WP Rocket on Galaxy) defer and rewrite every script. That was a **coverage
failure, not an unreadable site**: the tag IDs sit in the document in plain text, and the W3C
checker's `showsource=yes` view returns the file line by line. Re-reading it properly changed the
picture on both leads.

**Galaxy Dental Care** (1,997-line document, head and footer read in full):

| Row | Was | Now | Evidence |
|---|---|---|---|
| Google Tag Manager | not checked | **present** | `GTM-TRRMQGQ`, head lines 11-17, deferred by WP Rocket to first interaction |
| Meta description | not checked | **present, 113 chars** | line 63 |
| Open Graph / Twitter card | not checked | **present** | lines 65-76, incl. `og:image` = a 512×512 favicon, not a clinic photo |
| Favicon | not checked | **present** | `favicon.ico` + 32/192 px webp icons, lines 20, 118-120 |
| Structured data | not checked | **absent** | Yoast SEO 28.9 is installed (line 49) but emits no JSON-LD on this URL |
| Contact form | confirmed by markup | **confirmed + reCAPTCHA v3** | `dental-appointment-ajax`, honeypot field `website`, reCAPTCHA key `6Ldtm0At…` |
| Meta Pixel / Clarity / Google Ads | not checked | **still account-only** | WP Rocket preconnects to `connect.facebook.net`, `scripts.clarity.ms`, `googleads.g.doubleclick.net` and `clickcease.com`, but no `fbq`/`gtag`/`G-`/`AW-` id exists in the page — the tags run inside GTM-TRRMQGQ |

New findings from the read: **ClickCease** (click-fraud protection) is preconnected; the popup fires at
50% page depth; `DAAFormConfig` is declared **three times** verbatim (lines 1908-1910); the trust badges
are lazy-loaded images with real `noscript` fallbacks (the first pass called them "SVG placeholders",
which was wrong — corrected in the summary).

**D'LIFE Home Interiors** (head behind a 300 KB inline stylesheet; body opening + tail + Microlink's
headless fetch used for metadata):

| Row | Was | Now | Evidence |
|---|---|---|---|
| Meta Pixel | not checked | **present** | id `215010909028561`, noscript image at the top of the body |
| Google Tag Manager | not checked | **present** | `GTM-K9FB6G2`, head |
| Contact form | unknown | **present** | Contact Form 7, `form_id 40457`, Name field, conditional-logic add-on, reCAPTCHA field |
| Meta description | not checked | **present, 157 chars** | Microlink headless fetch of the same URL |
| Open Graph | not checked | **present** | `og:image` = `Interior_designers_in_hyderabad_web.jpg` (1920×670) |
| GA4 / Google Ads / Clarity / LinkedIn / Hotjar / UA | not checked | **still account-only** | no `G-`, `AW-`, `fbq`, `clarity` id in the HTML; GTM-K9FB6G2 and **Cloudflare Zaraz** (`/cdn-cgi/zaraz/s.js`) both run, so the tag inventory lives inside them |
| JSON-LD, favicon, image count | not checked | still unread | head block not reached inside the fetch budget |

New findings: **Cloudflare Zaraz** server-side tag runner plus the **Cloudflare Web Analytics** beacon
(token `773966fb…`) are both live; the Hyderabad page carries `class="locationPage location-bangalore"`
on its wrapper — a copy-paste from the Bangalore template; and the packages render ₹8.85 L → ₹6.37 L
(Essential, 2BHK) as claimed.

**What this changed in the numbers:** Galaxy 5/100 → **9/100** (schema now measured as missing);
D'LIFE stays **0/100** but with 2 of 8 tags verified instead of 0, and its "Top priorities" block now
says *"6 of 8 tracking checks could not be read through the page cache"* instead of the renderer's old
fallback, which congratulated the client on "clean tracking in place" — a sentence that would have been
false here. Both reports stay in measured-findings mode (Galaxy 4 unchecked, D'LIFE 6).

**Still blocked, honestly:** GA4 / Google Ads / Meta-on-Galaxy ids live inside the two GTM containers and
are account-only; D'LIFE's JSON-LD/favicon need the part of its head this pass could not reach. PageSpeed
remains unreachable from this crawler.

**Gates re-run after the second pass:** `delivery_gate.py` PASS ×5 · `verify_report.py --ads-only` PASS ×5
· `verify_live.py --offline` MATCH ×5 (repo 59 MATCH / 2 pre-existing DRIFT / 0 UNREACHABLE). Gate 2 is
still outstanding.

## Drafts (2026-11-28) — written, not sent

The four-step outreach sequence for each lead is generated by `02-OUTREACH/batch15_outreach.py`
(`--export`). The script reads every figure back out of `ads_only_results/audit_<slug>.json` and refuses
to export if the copy disagrees with the report — ad counts, Library IDs, Google ad counts, and the
step-0 word budget (≤260).

| Lead | To | Subject (step 0) | Step 0 words |
|---|---|---|---|
| SunSolar Power Systems | `sales@sunsolar.info` | 4 live Meta ads, all of them landing on fb.me | 226 |
| PNR Sunrise Energies | **no public email** — phone / WhatsApp only | one live ad, and a canonical tag pointing at a placeholder | 184 |
| D'LIFE Home Interiors | `enquiry@dlifeinteriors.com` | 5 live Meta ads, ~200 Google ads, two different phone numbers | 222 |
| Dr. Sridhar Dental | **no public email** — per-branch WhatsApp + booking form | 42 Google ads, 5 Meta ads, and no Meta Pixel | 208 |
| Galaxy Dental Care | `contact@galaxydentalcare.in` | ~300 Google ads, and a price the site never shows | 211 |

Files: `02-OUTREACH/generated_emails/batch15_email_<slug>.txt` (each holds all four steps plus the
"attach this" path and the cited Library IDs). Manifest: `sequence_manifest.json`, `report_kind:
ads_only`, 2-day delay between steps, no `sent_at` and no `thread_id` — nothing has been sent and no
thread exists yet.

Deliberate choices:

- **No score is quoted.** D'LIFE measures 0/100 and Galaxy 9/100 because the reports are partial; the
  copy talks about findings (missing pixel, placeholder canonical, split phone numbers) and never
  about the number. `verify_live.py` checks this.
- **No destination claim is made for the two leads without a public address.** PNR and Dr. Sridhar are
  written to be sent through the channel their site actually publishes.
- **The PNR follow-up was rewritten** during drafting: the earlier version said the homepage counters
  "stay at zero", which this crawler can only see as placeholder markup, so it now cites the verified
  fact (no email or office address published) instead. The same wording was corrected in
  `batch15_telangana_data.py`'s recommended steps; the PNR PDF was rebuilt behind it.

Gates after the drafts were exported: `delivery_gate.py` PASS ×5 · `verify_report.py --ads-only`
PASS ×5 · `verify_live.py --offline` MATCH ×5 (repo 59 MATCH / 2 pre-existing DRIFT / 0 UNREACHABLE).

### Gmail drafts (2026-11-28, unsent)

Three drafts exist in `smartpursuit3@gmail.com`, each with its report attached and the cited Library IDs
inline. They are drafts only — nothing has been sent and no thread has been opened.

| Lead | Gmail draft id | Attached |
|---|---|---|
| SunSolar Power Systems | `r-7973512065332472767` | `audit_SunSolar_Power_Systems.pdf` |
| D'LIFE Home Interiors | `r6853723717860708364` | `audit_D_LIFE_Home_Interiors.pdf` |
| Galaxy Dental Care | `r-7134646595645752516` | `audit_Galaxy_Dental_Care.pdf` |

PNR Sunrise Energies and Dr. Sridhar Dental have **no Gmail draft by design** — neither publishes an
email address, and inventing one is not an option. Their copy stays in
`generated_emails/batch15_email_<slug>.txt` for WhatsApp / the site's booking form.

When a draft is actually sent, record its `thread_id` and `sent_at` in `sequence_manifest.json`; until
then `mails_sent` stays 0 and no follow-up date is due.

## Reconciled with main (2026-11-28)

`main`'s tip (`810d589`) shares no history with this branch, so GitHub refused the merge
("unrelated histories"). It was reconciled locally with `git merge --allow-unrelated-histories`,
using `5cd85be` — the tree `main`'s snapshot came from — as the 3-way base for every conflicted path.

Only three files had genuinely changed on both sides; the rest were one-sided.

| Path | Kept |
|---|---|
| `audit_live_*`/`.opencode/*`, `AGENTS.md`, `README.md`, `AUDIT_FORMAT_STANDARD.md`, `EXAMPLE_AUDIT_REFERENCE.md`, `ads_audit.py`, `delivery_gate.py`, `run_pipeline.py`, `verify_live.py`, `tests_batch14.py`, ad-creative JPGs, `MANDATORY_AUDIT_CHECKS.md` | **main's** — this branch never touched them |
| `ads_only_report.py`, `AUDIT_PDF_INDEX.md`, `sequence_manifest.json`, `logo_white.png` | **branch's** — main's copy was identical to base |
| `audit_pdf.py` | 3-way merge: main's `validator_where/validator_when` row plus this branch's `_html_error_source()`, with the dict branch extended so a stored counts dict renders "2 errors; …" instead of main's "Not available at audit time" |

Five PDFs were rebuilt on the merged renderer; the verification log still prints the real
W3C counts.

**Gates after the merge:** `verify_report.py --ads-only` PASS ×5 · `verify_live.py --offline`
MATCH ×5 (59 MATCH / 2 pre-existing DRIFT) · **`delivery_gate.py` now HOLDS all five.**

That last one is a policy collision, not a regression in the reports. `audit_completeness.py`
(added on `main`) treats an ads report in the Ksquare layout as a full audit and refuses any
report with an unresolved mandatory website check — `html_errors` for SunSolar,
`pixels.google_analytics_ga4` for D'LIFE, `seo.has_title` for Galaxy, and so on. Those are
exactly the rows this batch deliberately left `null` because they sit behind GTM, a NitroPack
cache or a validator that halted; asserting them would be fabrication. Open decision, not
something to settle silently: scope the completeness rule to full audits, or resolve the
remaining checks from live evidence and re-gate.
