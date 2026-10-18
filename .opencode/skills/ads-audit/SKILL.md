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

After ANY discovery/pipeline run, before reporting done or delivering:

1. Run the automated verifier from `01-LEADS/`:
   ```
   python verify_report.py --all
   ```
   Exit code must be 0. Every `x` line is a defect — fix by re-running the
   pipeline (fresh live data), never by editing PDF/JSON by hand.
2. Invoke the **report-reviewer** agent (`.opencode/agent/report-reviewer.md`)
   on the generated reports. It re-checks branding, live-data honesty, ad
   links, score consistency, no-website handling, and staleness. Only a
   `REPORT REVIEW: PASS` verdict means the output is deliverable.

A report that has not passed both gates must not be sent to anyone.

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

- Do not hardcode, estimate, or "fill in" any audit numbers or ad counts.
- Do not reuse a previous PDF for a new outreach — always re-run the
  pipeline so the data is live as of the send date.
- Do not modify the ad-extraction JS selectors unless the platforms change
  their markup; they are tuned to the current Meta/Google DOM.
