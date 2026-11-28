# Mandatory audit checks — no incomplete audit may be delivered

This is the definitive list for **every agent** building, reviewing, or live-checking an audit in this repo. It overrides any older builder script that stored `None` and rendered “Not checked in this pass”.

The failure you must prevent is the one in `C:\Users\hp\Downloads\audit_D_LIFE_Home_Interiors.pdf`: a report that claims to be a full audit but leaves tracking tags, live chat, schema, image counts, and server response time as **“Not checked in this pass”**. That is a held draft, not a client-ready audit.

## The rule

A full audit is **not complete** until every website check below has a real observed value from the live page:

- `True` / `False` — measured presence or measured absence
- an integer/count — measured count
- a string with the observed value — observed text

`None`, missing keys, “Not found”, and “Not checked in this pass” are **not findings**. For a deliverable full audit they are a **FAIL**.

If a check cannot be read from the direct page fetch, the agent must re-read the page through another public source (W3C Nu checker `showsource=yes`, an inner page, or another live fetch) before deciding. If it is still unreadable, **stop and hold the report**. Do not guess, do not reuse a previous value, and do not hand-build a PDF.

## Mandatory resolved website checks

### Tracking (`pixels`)
`meta_pixel`, `google_ads`, `google_analytics_ga4`, `google_analytics_ua`, `linkedin_insight`, `microsoft_clarity`, `hotjar`, `google_tag_manager`

### Conversion (`conversion`)
`has_contact_form`, `has_phone_click`, `has_whatsapp_link`, `has_cta_buttons`, `has_live_chat`, `has_popup_optin`, `has_testimonials`, `has_pricing_page_link`

### SEO / page facts (`seo`)
`has_title`, `has_meta_description`, `h1_count`, `has_schema`, `has_og_tags`, `has_favicon`, `image_count`, `images_without_alt`

### Page / site facts
- `ssl`
- `load_time_seconds`
- `final_url`
- `html_errors` — the stored W3C Nu checker count string, e.g.
  `2 errors, 0 warnings, 42 info on the homepage`
- `page_count.has_sitemap`
- `local_signals.has_google_maps_embed`

`01-LEADS/audit_completeness.py` is the single source of truth for this list. `run_pipeline.py` refuses to render a PDF when any of these is unresolved, and `delivery_gate.py` refuses any report — including one made by another agent — that contains them.

## Legitimate exceptions — NOT failures

These are allowed because no public page measurement can resolve them:

1. **PageSpeed / Lighthouse unavailable (HTTP 429 or API unreachable).** Render exactly: `Not available at audit time (API returned 429)` — never a guessed score or LCP.
2. **Account-only Meta controls** (CAPI, event deduplication, EMQ, budgets, audiences, learning phase, frequency caps, hook rate, etc.) — render as `UNKNOWN` with the reason that Ads Manager access is required.
3. **Ad destination not stated on the live ad card.** Render `Not confirmed from the ad card in this pass`; no email may claim a confirmed destination.
4. **A pure ads-only report with no website audit.** It must show `WEBSITE AUDIT NOT RUN` and must not carry a score or website-check table at all.

Everything else must be resolved. “The page cache made this hard” is not an exception — use another source or hold the report.

## Agent workflow — all mandatory, in order

1. Read `AGENTS.md`, `AUDIT_FORMAT_STANDARD.md`, and this file before touching a lead.
2. Confirm the lead has not already been audited or emailed (`leads.csv`, existing JSON/PDF, Gmail including spam/trash).
3. Run the real pipeline from `01-LEADS/` on a machine with Chrome and live internet:
   ```powershell
   python run_pipeline.py <website> "<Company Name>" --city <City>
   ```
   Never hand-build a PDF, never use one sample ad, never copy an old PDF.
4. Confirm the JSON has all mandatory website checks resolved and all own ads attributed by direct Library ID fetch.
5. Run the gates from `01-LEADS/`:
   ```powershell
   python verify_report.py "<Company Name>"
   python delivery_gate.py "<Company Name>"
   python verify_live.py --company "<Company Name>" --timeout 25 --retries 2
   ```
   Exit `0` on all three. `verify_live.py --offline` exits `4` and is **not** a live pass.
6. `report-reviewer` must return `REPORT REVIEW: PASS`. It must fail any unresolved website check.
7. `live-data-auditor` must return `LIVE-DATA CHECK: PASS`. It must fail any mandatory check shown as `NOT_CLAIMED`.
8. If any gate fails: fix the source data and **re-run the pipeline**. Never edit a PDF or JSON by hand to make a gate pass.
9. Only the owner sends or schedules drafts. Agents create step-0 drafts only.

## Golden reference

`02-OUTREACH/audit_pdfs/audit_SunSolar_Power_Systems.pdf` is the current worked example. Give it to an agent together with `EXAMPLE_AUDIT_REFERENCE.md` and this file. It has every mandatory website check resolved, real live ads, honest PageSpeed handling, Smart Pursuit branding, and all gates passed.
