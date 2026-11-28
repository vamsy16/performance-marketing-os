---
name: ads-audit
description: Use when the user wants a live ads/website audit PDF for a lead, or wants leads discovered from the ad library — runs a real website audit, pulls LIVE Meta Ad Library + Google Ads Transparency Center data (including each ad's destination/conversion page), and builds branded Smart Pursuit PDF reports. Trigger on "audit this lead", "generate ads report", "ad library research", "discover leads", "find advertisers", "audit PDF", "run the pipeline", or any request to produce a client-ready audit for a business.
---

# Smart Pursuit Ads Audit

Generates a client-ready, branded PDF audit for any lead. Every run fetches
**live data** — the lead's actual website, the live Meta Ad Library, and the
live Google Ads Transparency Center. No cached or hardcoded numbers: run it
today or next month and the PDF always reflects the real state at that moment.

## Prerequisites (one-time setup)

```
pip install -r 01-LEADS/requirements.txt
```

- Python 3.11+ with `pip` on PATH.
- Google Chrome installed (the pipeline launches headless Chrome via
  Playwright's `channel="chrome"` — no separate browser download needed).
- Internet access (both ad libraries are queried live at run time).
- On first run, Playwright may need: `playwright install chromium`
  (harmless if Chrome channel is already used).

**Run this skill only where Chrome + live internet are available** (the owner's
machine or the GitHub Actions runner). If the website, Meta, or Google source
is unreachable, `run_pipeline.py` now exits non-zero and writes **no PDF**.
That is the correct result. **Never hand-roll a PDF from partial fetch
results** — an "internal draft" with one sample ad, no score, or "source date
not verified" is a held artefact, not this skill's output.

**Read `MANDATORY_AUDIT_CHECKS.md` at the repo root before every run.** It is
the definitive list of website checks that must resolve to a real observed
value. A full audit that says "Not found" or "Not checked in this pass" for any
of them is a HELD DRAFT — the audit is **not complete** and must never be
reported as done or delivered. `audit_completeness.py` is the single source of
truth; `run_pipeline.py` refuses to render and `delivery_gate.py` refuses to
pass any report with an unresolved check.

## Pre-flight — audit dedup check (owner rule, 2026-11-23, never skip)

Before taking ANY lead for audit — in discovery mode or direct mode — check
whether that lead has **already been audited**. Only leads with no audit done
are taken for audit. Check all three sources:

1. `01-LEADS/leads.csv` — `audit_score` filled or `status` = `audited`
2. Existing files — `audit_*.json` in `01-LEADS/ads_only_results/` or
   `01-LEADS/audit_results/`, and `audit_*.pdf` in `02-OUTREACH/ads_only_pdfs/`
   or `02-OUTREACH/audit_pdfs/`
3. Gmail — sent mail to that domain (search inbox + spam + trash). A lead
   already emailed is already audited, even if `leads.csv` still says `new`.

If any of the three shows a prior audit, **skip the lead**. Re-audit only on
explicit owner instruction (e.g. a DRIFT re-run). This rule exists because
Visiontek was re-audited in batch 13 although a full-audit email had already
been sent on 2026-11-15 — `leads.csv` alone did not catch it.

## Discovery mode — ONE input, leads found automatically (preferred)

When you do NOT already have a specific lead's URL, start from the Meta Ad
Library itself. Give only your market:

```
cd 01-LEADS
python discover_leads.py "solar Hyderabad"
python discover_leads.py "rooftop solar Delhi" --limit 5
```

What it does with just that one input:

1. Searches the **live Meta Ad Library** for active advertisers in the market
2. Extracts each advertiser's **real destination/conversion page** straight
   from their ad (`l.facebook.com/l.php?u=` redirect → the exact URL the ad
   sends customers to; WhatsApp ads are detected as WhatsApp conversions)
3. City is derived from the query (`solar Hyderabad` → Hyderabad; override
   with `--city`)
4. Per lead: audits that conversion page → pulls full live ad activity
   (Meta own + competitors + Google) → generates a branded PDF per lead
5. Prints a summary table with each lead's site, score, and PDF path

Flags: `--limit N` (leads, default 3), `--city X`, `--competitors N`,
`--pool N` (ad cards scanned in discovery).

**Website resolution chain** (in order): ad destination URL → company domain
found in the ad copy → none. Facebook/WhatsApp/Instagram destinations are
NOT audited as websites. If no website exists, the report honestly shows
`NO WEBSITE FOUND / N/A` with the WhatsApp-funnel pitch — this is a feature,
many local advertisers convert entirely in chat.

Outputs land in the same places as below: `audit_results/audit_<slug>.json`
and `02-OUTREACH/audit_pdfs/audit_<slug>.pdf`.

## Direct mode — when the lead already has a known URL

### One-command run

From the `01-LEADS` folder:

```
python run_pipeline.py <website> "<Company Name>" --city <City>
```

Example:

```
python run_pipeline.py https://www.ksquareenergy.com/solar-company-in-hyderabad "Ksquare Energy" --city Hyderabad
```

This does everything end-to-end and prints the final PDF path:

1. **Website audit** — fetches the live site, checks tracking pixels,
   conversion elements, SEO basics, PageSpeed, saves `audit_results/audit_<slug>.json`
2. **Live ad research** — queries the Meta Ad Library (own ads + competitor
   ads for `<city>`) and Google Ads Transparency Center (own advertiser +
   Indian competitor advertisers), downloads ad creatives to
   `audit_results/ad_images/<slug>/`, merges into the same JSON
3. **Branded PDF** — builds the Smart Pursuit report at
   `02-OUTREACH/audit_pdfs/audit_<slug>.pdf`

Flags: `--skip-audit` (reuse an existing audit, only refresh ads + PDF),
`--skip-ads` (website audit only), `--competitors N` (default 3).

### Mandatory website completeness — resolve every check or stop

If the page fetch leaves a tracking tag, conversion element, SEO field, image
count, sitemap, local signal, SSL, or server response time unresolved, **do not
accept it as "honestly unavailable"**. Re-read the page through another public
source first:

1. direct fetch with a browser user-agent (already tried by `ads_audit.py`);
2. W3C Nu HTML Checker `https://validator.w3.org/nu/?doc=<url>&showsource=yes`;
3. an inner page (e.g. `/contact-us/`) that carries the same head/template;
4. only then, if still unreadable, hold the report — never deliver it.

`None`, missing keys, "Not found" and "Not checked in this pass" are FAIL for
a deliverable full audit. The only allowed unclaimed values are the four in
`MANDATORY_AUDIT_CHECKS.md`: PageSpeed/Lighthouse 429 or unreachable API,
account-only Meta controls, an ad destination the live card does not state,
and a pure ads-only report with no website audit at all. Never hand-edit a JSON
or PDF to satisfy a gate — fix the source data and re-run `run_pipeline.py`.

### Manual 3-step run (same result)

```
cd 01-LEADS
python ads_audit.py <website> "<Company>" --city <City>
python ad_library.py "<Company>" --city <City>
python audit_pdf.py "<Company>"
```

## Branding (edit once, applies to every future PDF)

In `01-LEADS/audit_pdf.py`, top constants:

```
YOUR_NAME    = "Vamsi"
YOUR_AGENCY  = "Smart Pursuit"
YOUR_PHONE   = "+91 70950 24220"
```

Logo: put `smart pursuit logo.png` in the project root (already there).
The pipeline auto-recolours the dark logo to white for the navy header —
no white box is drawn behind it.

## Output files

| File | What |
|---|---|
| `01-LEADS/audit_results/audit_<slug>.json` | Full audit + ad-library data |
| `01-LEADS/audit_results/ad_images/<slug>/*.jpg` | Downloaded ad creatives |
| `02-OUTREACH/audit_pdfs/audit_<slug>.pdf` | Final client-ready PDF |

## MANDATORY final step — review gate (never skip)

After ANY discovery/pipeline run, before reporting done or delivering, run
these three gates from `01-LEADS/` in this order:

1. **Structural gate**
   ```
   python verify_report.py --all                 # full audits
   python verify_report.py --ads-only            # ads-only reports
   ```
   Exit 0 required. Every `x` line is a defect. This gate now rejects draft
   markers (`INTERNAL DRAFT`, `NOT SCORED`, `SCORE NOT ASSIGNED`, ...),
   `review_pending`, unreachable ad sources, and zero-ad reports.

2. **Delivery gate — new, mandatory**
   ```
   python delivery_gate.py "Company Name"
   # or: python delivery_gate.py --latest
   ```
   Exit 0 required. This is the gate that proves the report is complete,
   freshly measured, and actually built by `run_pipeline.py`. A hand-rolled
   PDF has no `provenance` and fails here. It also fails any full audit with
   unresolved mandatory website checks or "NOT CHECKED IN THIS PASS" in the
   PDF text. `run_pipeline.py` calls this gate itself and refuses to print
   `DONE` when it fails.

3. **Independent human/agent gates**
   - Invoke the **report-reviewer** agent
     (`.opencode/agent/report-reviewer.md`). Only `REPORT REVIEW: PASS` counts.
   - Invoke the **live-data-auditor** agent
     (`.opencode/agent/live-data-auditor.md`) and run
     ```
     python verify_live.py --company "Company Name"   # NOT --offline
     ```
     Exit 0 required: 1 = DRIFT, 2 = UNREACHABLE, 4 = offline (not a pass).
     Gate 3 re-fetches ads through Chrome (bare `requests` gets a 403 challenge)
     and the lead's live website, then cross-checks outreach text against the
     report.

A report that has not passed all gates must not be sent to anyone.

**Every rule above is written up in `AGENTS.md` at the repo root — read it
before starting any run.** Also read `MANDATORY_AUDIT_CHECKS.md`; it is the
definitive list of checks that must be resolved before an audit is complete.
An audit with "Not found" or "Not checked in this pass" in a mandatory check
must not be completed, reported as done, or delivered.

## The output (what you produce / what gets delivered)

Per lead, the deliverable is **one PDF**:

```
02-OUTREACH/audit_pdfs/audit_<Slug>.pdf
```

Supporting files (internal — not sent to the client):

| File | What |
|---|---|
| `01-LEADS/audit_results/audit_<slug>.json` | Full audit + live ad-library data (source of truth) |
| `01-LEADS/audit_results/ad_images/<slug>/*.jpg` | Downloaded ad creatives embedded in the PDF |

Each run's console summary ends with the exact PDF path(s) — that path list
is the run's output. Client outreach = attach that PDF to the email/message
built from `02-OUTREACH/templates/`.

## Output quality bar (enforced by the review gate)

- Branded: Vamsi / Smart Pursuit / +91 70950 24220, logo on navy header,
  header reads "ADS AUDIT REPORT"
- Live: every number traces to today's JSON; every ad card links to the
  real Meta/Google library page
- Honest: unavailable data labeled unavailable; social-only leads show
  "NO WEBSITE FOUND"; no placeholder text or rendering artifacts
- Complete: >= 3 pages, logo + ad creative images embedded, executive
  summary present

## What is real / live vs unavailable

- Meta ads, run dates, library IDs, creatives: **live** from Meta Ad Library.
- Google advertiser status and ad counts: **live** from Ads Transparency Center.
- Tracking/SEO/conversion findings: **live** fetch of the lead's website.
- PageSpeed may return 429 (rate-limited) — the PDF honestly labels it
  "Not available at audit time"; never fabricate a score.
- Google ad creatives often lazy-load and cannot be scraped — the Google
  section shows advertiser name + ad count + link only. Do not invent images.

## Troubleshooting

- **Meta shows more results than ad cards parsed**: the results list is
  virtualized; the engine extracts every card present in the DOM over
  several scroll rounds. Fewer cards than "~N results" is normal and honest.
- **Indic-script ad copy**: Arial cannot render Gujarati/Hindi etc. The PDF
  auto-swaps non-Latin copy for "[Ad copy in regional language - open the ad
  via the link below]". Leave this behaviour — do not try to translate.
- **Chrome not found**: install Google Chrome, or edit `ad_library.py` to
  remove `channel="chrome"` so Playwright's bundled Chromium is used
  (requires `playwright install chromium`).
- **`leads.csv` looks garbled after a bulk import**: run
  `python lead_data.py` — it repairs structure, sanitizes emails/phones,
  and drops directory/blog/listicle URLs. `python lead_data.py --check`
  is a dry run. `python tests.py` covers the hygiene rules.

## Do not

- Do not audit a lead that has already been audited. Run the pre-flight dedup
  check first (leads.csv + existing JSON/PDF + Gmail sent history); only
  unaudited leads are taken for audit.
- Do not hardcode, estimate, or "fill in" any audit numbers or ad counts.
- Do not reuse a previous PDF for a new outreach — always re-run the
  pipeline so the data is live as of the send date.
- Do not modify the ad-extraction JS selectors unless the platforms change
  their markup; they are tuned to the current Meta/Google DOM.
