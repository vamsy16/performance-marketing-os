# AGENTS.md — Standing instructions for every agent working in this repo

This file is the **contract**. Anything an agent does here — discovering leads,
running an audit, building a PDF, drafting an email — must follow it. It
distils every rule the owner has stated and every defect this pipeline has
actually produced. Read it before you start, not after.

**The one rule underneath all the others:** these PDFs and emails go straight
to real businesses. A single fabricated, stale, or unverifiable figure costs
the client's trust, and the owner's. When in doubt, report the gap — never
fill it.

---

## 1. What this repo produces

Per lead, one client-ready audit PDF plus a 4-step outreach sequence
(initial + 3 threaded follow-ups). State lives in:

| File | What |
|---|---|
| `01-LEADS/leads.csv` | every lead (CRLF line endings) |
| `01-LEADS/ads_only_results/audit_*.json` | live-ad reports (source of truth) |
| `01-LEADS/audit_results/audit_*.json` | full website audits |
| `02-OUTREACH/ads_only_pdfs/audit_*.pdf` | live-ad report PDFs |
| `02-OUTREACH/audit_pdfs/audit_*.pdf` | full audit PDFs |
| `02-OUTREACH/generated_emails/sequence_manifest.json` | 46 sequences / 184 steps |
| `02-OUTREACH/AUDIT_PDF_INDEX.md` | index of every PDF shipped |

---

## 2. The three checks — all mandatory, in this order

Nothing is delivered to a client until all three pass.

### Check 1 — automated verifier
```
cd 01-LEADS && PYTHONPATH=/tmp/pdflibs python3 verify_report.py --ads-only
```
Exit 0 required. `--all` for full audits, a company name for one report.
Every `x` line is a defect. Fix by **re-running the pipeline**, never by
editing a PDF or JSON by hand.

### Check 2 — report-reviewer agent
`.opencode/agent/report-reviewer.md`. Re-reads JSON + PDF for branding,
live-data honesty, ad links, score consistency, no-website handling, and
staleness. Needs a `REPORT REVIEW: PASS` verdict.

### Check 3 — live-data-auditor agent (the third check)
`.opencode/agent/live-data-auditor.md`, running `01-LEADS/verify_live.py`.

Checks 1 and 2 only compare files against each other. Check 3 goes to the
**live** Meta Ad Library and the lead's **live** website and re-verifies every
stored figure. It is the only gate that can catch a figure that was never
live, or one that went stale.

```
cd 01-LEADS && PYTHONPATH=/tmp/pdflibs python3 verify_live.py --offline   # consistency only
cd 01-LEADS && PYTHONPATH=/tmp/pdflibs python3 verify_live.py             # full live re-check
```

Exit codes: `0` all matched · `1` DRIFT (stored data is now wrong) ·
`2` UNREACHABLE (could not verify) · `3` nothing to check.
**A non-zero exit means do not deliver.** "Could not check" is exactly as
undeliverable as "checked and wrong".

---

## 3. Real live data — the hard rules

**Never invent, estimate, paraphrase, or "fill in" a number.** Every figure in
a PDF or email must trace to a source that was actually read.

- **No invented audit scores, pixel counts, PageSpeed or Google Transparency
  numbers.** Unverifiable data is marked `not available` / `not checked` /
  `pending` — never guessed.
- **PageSpeed / Lighthouse is keyless-quota-blocked (HTTP 429).** Report it
  exactly as the Ksquare reference does: *"Not available at audit time (API
  returned 429)"*. Never fabricate a speed score or LCP.
- **Ad copy is reproduced verbatim.** If the live ad says ₹1,001, the report
  says ₹1,001. Paraphrasing ad copy into a PDF was a real defect here.
- **A destination is only "confirmed" if the ad card states one.** If it does
  not, it is *"Not confirmed from the ad card in this pass"* — and **no email
  may claim a destination the report does not support.** This exact mismatch
  reached the Lumisun and Kypas step-1 drafts before check 3 caught it.
- **Never upgrade a `None` to a guess.** `dict.get(k, default)` returns `None`
  when the key *exists* with value `None`. Any consumer must test `is None`
  explicitly. This single trap has produced three separate crashes and one
  false "No Google Ads presence was found" claim in outreach.
- **The live-ad count in an email must equal the number of ads actually
  captured**, not the Ad Library's "~N results" total. The manifest once
  overstated activity this way.
- **A report whose page head could not be read says so.** Kypas and Lumisun
  heads were unreachable; their tracking is "not checked", not absent.

---

## 4. Audit format

- **All audits follow the Ksquare 5-page format** — reference
  `02-OUTREACH/audit_pdfs/audit_Ksquare_Energy.pdf`, spec in
  `AUDIT_FORMAT_STANDARD.md`.
- **Every audit PDF — full and ads-only — carries the claude-ads
  control-review section** alongside the Ksquare layout. Ksquare layout
  unchanged; the control review is added, not substituted.
- `audit_pdf.py` on Linux falls back to the base-14 fonts, so every non-cp1252
  glyph must go through `_SAFE_MAP` / `latin_safe()`. ₹ renders as "Rs. ".
  Indic-script ad copy is replaced with an explicit placeholder — do not try
  to translate it.
- **No white gaps.** Mid-document page breaks use `CondPageBreak`
  (`_AD_SECTION_MIN=100`, `_WEBSITE_SECTION_MIN=108`), not `PageBreak()`.
  Measure with `01-LEADS/measure_gaps.py`; a tail over 12% is flagged.
- `promise_gap_table()` is deliberately gated to reports with ≤1 ad. Ungating
  it pushed reports to 6 pages with an 86%-empty final page. Do not retry.

---

## 5. Lead qualification

- **A lead must run live ads with a resolvable website.** A zero-live-ad lead
  gets **no audit PDF and no outreach** — there is nothing to audit.
- **Ad-ID attribution is the #1 trap.** Confirm every library ID with a direct
  `https://www.facebook.com/ads/library/?id=<ID>` fetch. Confirmed
  misattributions include ads belonging to Ecolt, Orbit, Arcedo Systemss,
  Wisda, and Nisha Solar. Never trust a search-engine cache — a parked GoDaddy
  domain once returned full cached company content while serving a parking
  page.
- **Probe alternates before dropping a domain.** `lumisun.in` and
  `lumisunsolar.in` do not resolve; the live domain is `lumisunsolar.com`.
- Same-name traps are real: "Mr.Solar" is Nagpur, "Orbit Solar Power" is Tamil
  Nadu, "Lotus Industries" also hits a Salem TN EPC. Verify the city.

---

## 6. Outreach and Gmail

- **The owner sends and schedules every draft.** Agents create step-0 drafts
  only. Gmail has no scheduled send — scheduling is UI-only.
- **Check Gmail for replies before drafting.** Search the lead's domain,
  including spam and trash.
- **`list_drafts` excludes trash by default** — re-check with
  `include_spam_trash: true` before recreating, or you will duplicate.
- **Never draft for a lead with no email address in the manifest.** Find one
  first. Both batch-11 "no email" leads turned out to have one on their
  contact page.
- **Every follow-up threads onto the original.** Use the `thread_id` recorded
  by `sequence.py mark-draft`.
- **Parallel `create_draft` calls return responses out of order.** Always map
  the returned `thread_id` back to the lead — never trust call order.
- **`send_draft` deletes the draft after sending.** A missing draft is not
  evidence a follow-up was never sent; cross-check `list_messages` for the
  `SENT`-labelled copy.
- Record every created draft:
  `python sequence.py mark-draft --company "<Co>" --step 0 --draft-id <id> --thread-id <tid> --message-id <mid>`
- `sequence.py mark-draft` refuses step ≥1 unless the previous step is `sent`
  **and** has a non-empty `thread_id` + `message_id`. When an `&&` chain stops
  early, re-run the whole chain.

---

## 7. Environment

- **`/tmp/pdflibs` degrades between turns** (it has been wiped outright at
  least twice). Reinstall and always run with `PYTHONPATH=/tmp/pdflibs`:
  ```
  pip install --break-system-packages --target /tmp/pdflibs --upgrade \
      pypdf pypdfium2 pillow reportlab requests beautifulsoup4 lxml
  ```
  `pip` can fail transiently with `SSL: DECRYPTION_FAILED_OR_BAD_RECORD_MAC` —
  retry.
- **`pip install` is PEP-668 blocked** — always `--break-system-packages`.
- The sandbox has **no outbound access to lead websites or facebook.com**
  (only github/npm/pypi). Live re-verification of ads and sites must run on
  the owner's machine or the GitHub Actions runner. `verify_live.py` reports
  UNREACHABLE rather than passing in that case — that is correct behaviour.
- The sandbox cannot fetch ad-creative thumbnails or run headless Chrome. The
  owner rebuilds PDFs locally via `run_pipeline.py` to embed screenshots.
- **The harness resets the local branch between turns.** Detect with
  `git log --oneline -1`; recover with
  `git fetch origin arena/de53294b-performance-marketing-os && git reset --hard FETCH_HEAD`.
  Never force-push.
- **The only raw-source channel that survives** is
  `https://validator.w3.org/nu/?doc=<url>&showsource=yes`. CORS proxies are
  dead. The error list precedes the source, so pages with hundreds of errors
  have an unreachable source — use an inner page instead.
- **`edit_file` params are `path`/`new_text`/`old_text`.** It rejects large
  multi-line patches — patch Python via a `python3 - <<'PYEOF'` heredoc with
  asserts on the old block.

---

## 8. Rebuild commands

```
cd 01-LEADS
PYTHONPATH=/tmp/pdflibs python3 build_batch11_ksquare.py   # batch-11 measured data -> JSON + PDF
PYTHONPATH=/tmp/pdflibs python3 build_batch10_ksquare.py   # batch-10
PYTHONPATH=/tmp/pdflibs python3 rereder_ads_only.py        # re-render ALL 40 ads-only PDFs
PYTHONPATH=/tmp/pdflibs python3 measure_gaps.py <pdf>...   # white-gap measurement
PYTHONPATH=/tmp/pdflibs python3 verify_report.py --ads-only
PYTHONPATH=/tmp/pdflibs python3 verify_live.py --offline

cd 02-OUTREACH
python3 sequence.py status | due | mark-draft | mark-sent
python3 tests_sequence.py
```

`build_batch11_ksquare.py` is the single source of truth for batch-11 measured
site data — **re-run it, never re-fetch and re-type the numbers.**

---

## 9. Do not

- Do not hardcode, estimate, or "fill in" any audit number or ad count.
- Do not reuse a previous PDF for new outreach — re-run so data is live as of
  the send date.
- Do not weaken a verification gate to make a report pass. Fix the rendered
  fact. (`FORBIDDEN_IN_ADS_ONLY` contains a literal `/100` that false-positives
  on Facebook page IDs starting with 100 — fix the contact fact, not the gate.)
- Do not apply legacy-only checks (`LIVE AD ACTIVITY`, `WEBSITE AUDIT NOT RUN`,
  `/100`, `MISSING`) to reports that carry a `site_audit`.
- Do not modify the ad-extraction JS selectors unless the platforms change
  their markup.
- Do not create follow-up steps ahead of time. A sequence advances only after
  the previous step is actually sent.
- Do not send, schedule, or un-trash anything. Valcan's trashed step-1 draft
  `r-4135467498809954457` is parked by owner decision — leave it.
