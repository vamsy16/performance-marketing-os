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
PYTHONPATH=/tmp/pdflibs python3 verify_report.py --all   # honesty gate
```

`audit_pdf.py` (Ksquare `build_story()` engine) already produces this format.
Never hand-roll a different layout, and never feed a partial audit JSON into
`build_story()`.

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
