# Audit format standard — Ksquare format (standing instruction)

**Owner instruction, 2026-10-21:** "Audits should be prepared like that, same as
`audit_Ksquare_Energy.pdf`. For all audits from now, in repo."

Every audit PDF built from now on (full audits **and** the live-ad reports that
carry an audit panel) must follow the **Ksquare format** below — the same
sections, same order, same tone as `02-OUTREACH/audit_pdfs/audit_Ksquare_Energy.pdf`
(the 5-page, 18 Oct 2026 build). That PDF is the reference; when in doubt, match
it.

## Build command

```bash
cd 01-LEADS
PYTHONPATH=/tmp/pdflibs python3 audit_pdf.py "<Company>"
PYTHONPATH=/tmp/pdflibs python3 verify_report.py --all   # structural gate
PYTHONPATH=/tmp/pdflibs python3 delivery_gate.py "<Company>"   # completeness gate
```

`audit_pdf.py` (Ksquare `build_story()` engine) already produces this format.
Never hand-roll a different layout, and never feed a partial audit JSON into
`build_story()`. A PDF with no `provenance`, a `review_pending` flag, one
sample ad, `NOT SCORED`, or `SOURCE DATE NOT VERIFIED` is an internal hold and
fails `delivery_gate.py` regardless of how close its layout looks.

## The Ksquare layout, page by page

**Page 1 — cover + executive summary + score panel**
- Header band: SMART PURSUIT / SOLAR GROWTH PARTNER / ADS AUDIT REPORT / date;
  "Prepared by Vamsi | Smart Pursuit | +91 70950 24220"
- "DIGITAL MARKETING & PAID ADS AUDIT", company name, city · URL · "Audited
  <timestamp>"
- Executive summary (3–4 sentences, live numbers only)
- Score panel: **AUDIT SCORE (lower is better)** + ISSUES FOUND, TRACKING GAPS,
  LIVE ADS RUNNING + one-line interpretation
- "Top priorities — what to fix first": top 3 issues, each with a concrete fix

**Page 2 — your live ads**
- "Your live ads — Meta (Facebook / Instagram)": every live ad with advertiser
  name, "Running since <date> (<n> days) | Library ID <id>", ad copy (or the
  regional-language note), "Open the live ad" link
- "Your live ads — Google (Search / YouTube / Display)": Transparency Center
  result — advertiser + live ad count, or the explicit no-record finding

**Page 3 — competitor ad activity**
- "who is buying attention in your market": sample competitor Meta ads (name,
  running-since, Library ID, copy, live link)
- Google: Indian solar advertisers currently active in the transparency centre
  with ~live ad counts and "View ads" links

**Page 4 — website health**
- "Website tracking & pixels": all 8 tools (Meta Pixel, Google Ads conversion
  tag, GA4, old GA, LinkedIn Insight, Clarity, Hotjar, GTM) as OK/MISSING +
  the "X of 8 missing" summary line
- "Conversion readiness": form, click-to-call, WhatsApp, CTA count, live chat,
  popup, testimonials, pricing — OK/MISSING
- "What is already working": the OK items restated as wins
- "Technical snapshot": SSL, server response time, mobile page speed, LCP,
  page title, meta description, H1, structured data, Open Graph, images
  (total + missing alt), indexed pages (sitemap)

**Page 5 — next steps + CTA**
- "Google Maps / local SEO" finding
- "Recommended next steps — your 30-day action plan": numbered actions tied to
  the found gaps
- Closing CTA: free 10-minute walkthrough offer, no pitch
- Footer: auto-generation note + "Website findings reflect the homepage at the
  time of the audit; ad-library data is live public data from Meta and Google."

## Ads-only reports use the SAME 5-page Ksquare layout (standing instruction, 2026-10-24)

**Owner instruction:** "New batch Ad audit pdf is not that good. Generate like
this audit_Ksquare_Energy pdf. You also check all these things and keep the
pdf's like that strictly. No stimulate or some demo data what you found keep
that data only audit like that everything should be with real live data."

An ads-only report is no longer a short ad-activity sheet. When the lead's
website has actually been read, the report is the **full Ksquare 5-page audit**:

- `build_ads_only_story()` in `01-LEADS/audit_pdf.py` detects
  `audit["site_audit"]` and delegates to `build_story()` — the exact same
  engine that renders `audit_Ksquare_Energy.pdf`. Same sections, same order,
  same wording, same CTA. Never hand-roll a second layout.
- Website findings live **nested under `site_audit`** in the JSON
  (`pixels`, `seo`, `conversion`, `pagespeed`, `page_count`,
  `local_signals`, `score`, `ssl`, `final_url`, `audit_date`) so an ads-only
  record never masquerades as a full-audit JSON.
- A green **"WHAT WAS READ LIVE FOR THIS REPORT"** panel is inserted under the
  title rule, naming the ad-library read date, the website read method, and
  everything that was **not** measured. Where a specific lead has rows that
  could not be checked, a `site_audit.scope_note` explains why.
- Reports with **no** `site_audit` keep the old short layout and its
  "WEBSITE AUDIT NOT RUN" banner — that path is unchanged.
- The claude-ads control review is still included (see below); real page-source
  evidence now upgrades `M01 Meta Pixel installed` from `unknown` to a graded
  pass/fail.

### How the live website data is actually obtained

`ad_library.py` cannot reach arbitrary sites from the sandbox. The working
channel is the **W3C Nu HTML Checker with `showsource=yes`**:

```
https://validator.w3.org/nu/?doc=<url>&showsource=yes
```

It returns the raw served HTML with `<script>` tags intact, which is what makes
Meta Pixel / GA4 / GTM / Clarity / Hotjar / Google Ads tag detection real rather
than assumed. Caveats: the error list precedes the source, chunk counts vary
wildly by site (Wisda 21 chunks, Sunova 94, SolarSquare 31, Rayzon 13), and each
chunk returns only ~1,500 characters — budget 3–6 chunk fetches per site and
probe indices to find where the source starts. A direct page fetch of the same
URL supplies headings, forms, links, CTAs, testimonials, pricing and image alt
text.

Batch 10 was rebuilt this way by `01-LEADS/build_batch10_ksquare.py` (real data
for Sunova, Wisda, SolarSquare and Rayzon is recorded in that file with the
source of every value).

### Never guess a value — measured states vs held drafts

`calculate_audit_score()` in `01-LEADS/ads_audit.py` still distinguishes a
check recorded as `None` (**not measured**) from `False` (**measured absence**).
That distinction matters while a page is being read, but **a deliverable full
audit may not contain `None`**. `MANDATORY_AUDIT_CHECKS.md` is the definitive
list of website checks that must resolve to `True` / `False`, a count, or
observed text before the report is complete. `None`, missing keys, "Not found"
and "Not checked in this pass" are a HELD DRAFT and FAIL `delivery_gate.py`
and both review agents. `run_pipeline.py` refuses to render such a report.

- PageSpeed mobile score + LCP → "Not available at audit time (API returned 429)"
  (the keyless API's quota is 0/day — the same failure the reference Ksquare PDF
  reports). This is an allowed exception: never a guessed score or LCP.
- Server response time, SSL, final URL, all tracking tags, conversion elements,
  SEO fields, image counts, sitemap and local signals are **mandatory resolved
  checks**. If a direct page fetch leaves one unreadable, re-read through W3C
  Nu Checker `showsource=yes` or an inner page; if still unreadable, hold the
  report. Do not ship "Not checked in this pass".
- Google Ads Transparency records and competitor sections: `build_story()`
  distinguishes "checked, none found" from "not checked"; an empty
  `google_own` / `meta_competitors` dict must never render as a "no record
  found" claim. Account-only Meta controls stay `UNKNOWN` with the reason.
- An ad destination not stated on the live ad card stays "Not confirmed from
  the ad card in this pass" — an allowed exception, and no email may claim it.
- A pure ads-only report with no `site_audit` must show `WEBSITE AUDIT NOT RUN`
  and carry no website score or check table at all. That is the fourth allowed
  exception; it is not a full audit.
- `verify_report.py --ads-only` enforces the flip: with `site_audit` present the
  report must prove it is the full 5-page layout and carry no placeholder values;
  without it, the old "WEBSITE AUDIT NOT RUN" rules apply unchanged.

## Ads-audit control review — claude-ads methodology (standing instruction, 2026-10-24)

**Owner instruction:** "from now please be strictly there ads audit in this repo
<https://github.com/vamsy16/claude-ads> use those as well while preparing audit…
don't miss ads audit pdf format like audit_Ksquare_Energy… keep that ads audit
from claude ads as well in those audit pdf."

Every audit PDF (full audits **and** ads-only reports) now carries an extra
section — **"Ads audit - control review"** — rendered by
`ads_control_section()` in `01-LEADS/audit_pdf.py` from data produced by
`01-LEADS/ads_audit_controls.py`.

- Control IDs and intents come from the claude-ads Meta Ads audit catalog
  (`ads/references/meta-audit.md`, registry M01–M72). The repo is cloned at
  `/tmp/claude-ads` for reference.
- Only controls that **public evidence** can grade are graded: the Meta Ad
  Library ad cards (copy, formats, start dates, destinations) plus the lead's
  own landing page when its source was pulled (`site_evidence.pixel`).
- The catalog's own contract is followed: a control with no evidence is
  `unknown`, never guessed; no platform-wide thresholds or broad benchmarks
  are applied. Account-only controls (CAPI, EMQ, bidding, budgets, audiences,
  learning phase, frequency…) are listed as one explicit "needs account
  access" row.
- `evaluate(lead, site_evidence)` runs inside `ads_only_report.py build()` and
  is stored in the JSON as `ads_audit`, so the grading is inspectable.
- The Ksquare layout above is unchanged — the section is inserted after the
  live-ads / funnel content, before findings (ads-only) or before competitor
  activity (full audits).

## Honesty rules (unchanged — they apply to every Ksquare-format audit)

- Live data only. No invented audit scores, pixel counts, PageSpeed numbers or
  Google Transparency figures.
- Anything unverifiable at build time renders honestly: PageSpeed/Lighthouse →
  "Not available at audit time (API returned …)"; no ad record → the explicit
  no-record finding, never a guess.
- The score uses the repo formula in `01-LEADS/ads_audit.py` — never hand-set.
- Ad-creative thumbnails: the owner's local build embeds them (reports run
  ~300–590 KB). Sandbox builds cannot fetch creatives (fbcdn unreachable) and
  stay ~18–20 KB — `verify_report.py`'s 30 KB size check then fails on the size
  heuristic only; do NOT weaken the gate, the owner rebuilds locally to embed
  creatives.
- Outreach built off a Ksquare-format audit uses `audit_outreach.py --export`
  (full-audit templates); the ads-only path stays `ads_only_outreach.py`.
