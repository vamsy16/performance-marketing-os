# Agent handoff — run a Smart Pursuit audit cleanly

Give the agent **these four files together**. Do not give it only the PDF.

1. `AGENT_HANDOFF.md` — this run sheet
2. `MANDATORY_AUDIT_CHECKS.md` — the mandatory-check contract
3. `EXAMPLE_AUDIT_REFERENCE.md` — the worked example
4. `02-OUTREACH/audit_pdfs/audit_SunSolar_Power_Systems.pdf` — the branded reference PDF

The agent must also read `AGENTS.md` at the repo root. It is the standing contract.

## 0. Environment — non-negotiable

- Runs on the **owner's Windows machine** (or GitHub Actions runner) with **Google Chrome + live internet**.
- If Chrome, the website, Meta Ad Library, Google Transparency, or W3C cannot be reached, **stop and say so**. Never build an "internal draft" PDF.
- From the repo root, first sync:
  ```powershell
  git pull origin main
  ```
- Dependencies (one time):
  ```powershell
  python -m pip install -r 01-LEADS/requirements.txt
  ```

## 1. Before touching a lead — dedup check

Skip the lead if **any** of these show it was already audited or emailed:

1. `01-LEADS/leads.csv` — `audit_score` filled or `status = audited`
2. Existing `audit_*.json` / `audit_*.pdf` in `01-LEADS/ads_only_results/`,
   `01-LEADS/audit_results/`, `02-OUTREACH/ads_only_pdfs/`, `02-OUTREACH/audit_pdfs/`
3. Gmail sent mail to that domain, **including spam and trash**

Re-audit only on explicit owner instruction (e.g. a DRIFT re-run). A lead already emailed is already audited even if `leads.csv` says `new`.

## 2. Run the real pipeline

From the repo root:

```powershell
cd 01-LEADS
python run_pipeline.py <website> "<Company Name>" --city <City>
```

Example:

```powershell
python run_pipeline.py https://www.sunsolar.info/ "SunSolar Power Systems" --city Hyderabad
```

This does the live website audit, live Meta/Google ad research, branded PDF, and the delivery gate. If it exits non-zero, **there is no report** — fix the source and re-run.

Never:
- hand-roll a PDF or monkeypatch the renderer
- use one sample ad with no score
- copy/reuse an old PDF for new outreach
- hand-edit a JSON or PDF to satisfy a gate

## 3. Mandatory completeness — the rule that keeps failing

A full audit is **not complete** until every check in `MANDATORY_AUDIT_CHECKS.md` has a real observed value. `None`, missing keys, `Not found`, and `Not checked in this pass` are **FAIL**, not honest gaps.

Check it explicitly:

```powershell
python -c "import json,audit_completeness; a=json.load(open(r'audit_results/audit_<slug>.json',encoding='utf-8')); print(audit_completeness.unresolved(a))"
```

It must print `[]`.

If it does not: re-read the live page through direct fetch → W3C Nu `showsource=yes` → an inner page, then re-run `run_pipeline.py`. Still unreadable = **held draft, do not deliver**.

Allowed unclaimed values are **only**:
- PageSpeed/Lighthouse 429 → `Not available at audit time (API returned 429)`
- Account-only Meta controls → `UNKNOWN` with reason
- Ad destination not stated on the live ad card → `Not confirmed from the ad card in this pass`
- Pure ads-only report with no website audit → `WEBSITE AUDIT NOT RUN` and no score/website table

If W3C returns HTTP 429 while capturing validator counts, wait and retry. If it stays 429, the report is held — never downgrade the gate.

## 4. Gates — all mandatory, in this order

From `01-LEADS/`, every command must exit `0`:

```powershell
python tests_batch14.py
python verify_report.py "<Company Name>"
python delivery_gate.py "<Company Name>"
python verify_live.py --company "<Company Name>" --timeout 25 --retries 2
```

`verify_live.py --offline` exits `4` and is **not** a live pass. Exit `1` = DRIFT, `2` = UNREACHABLE, `3` = nothing to check — none are deliverable.

Then invoke the two agents:

- `report-reviewer` → must return `REPORT REVIEW: PASS`
- `live-data-auditor` → must return `LIVE-DATA CHECK: PASS`

A mandatory website check shown as `NOT_CLAIMED` / "Not checked in this pass" makes both agents **FAIL**.

## 5. Deliverable

The only client-facing file is:

```text
02-OUTREACH/audit_pdfs/audit_<Slug>.pdf
```

Do **not** send, schedule, or un-trash anything. The owner sends and schedules every draft.

## 6. Branding check

The PDF must show `Vamsi | Smart Pursuit | +91 70950 24220`, `ADS AUDIT REPORT` header/footer, and the logo directly on the navy band. No `YOUR NAME`, no `Website & Ads Audit`, no white logo panel. The reference PDF shows the exact result.
