# Smart Pursuit OS — Your One-Person Solar Marketing Agency

A zero-budget, maximum-automation operating system for a solo digital marketing agency serving the **solar energy niche**.

## What this is

Everything you need to run a full-service digital marketing agency alone, using only:
- **Arena Agent Mode** (free AI brain) — for content, research, proposals, ad copy
- **OpenCode** (free engineer) — for building/running the automation scripts here

## The folders

| Folder | What it is | How to use |
|---|---|---|
| `00-PLAYBOOK` | Your positioning, offers, pricing | Read first. This is your business brain. |
| `01-LEADS` | Lead generation + scraper | Run to find solar companies to pitch |
| `02-OUTREACH` | Email/call templates + sequences | Copy-paste + personalize |
| `02-OUTREACH/ads_only_pdfs/` | Live-ad-activity PDFs (no website audit) | Built by `python 01-LEADS/ads_only_report.py` when the full pipeline can't run; each report says so on page 1 |
| `03-CONTENT` | Arena prompt library + content calendar | Paste prompts into Arena to generate |
| `04-DELIVERY` | Client work playbooks + audit tools | How to actually deliver each service |
| `05-CRM` | Free local CRM (Python) | Track every lead & client |
| `06-AUTOMATION` | Automation blueprints (scheduling/workflows) | Wire these up when you have volume |
| `07-DAILY-SYSTEM` | Daily/weekly checklists | Your operating routine for inconsistent hours |

## Your tech stack (all ₹0)

| Need | Free tool |
|---|---|
| AI writing/research | Arena Agent Mode |
| Code automation | OpenCode + these scripts |
| Website | GitHub Pages |
| Email | Gmail (500/day) or Brevo (300/day free) |
| Scheduling | Cal.com free |
| Social posting | Buffer free / Meta Business Suite |
| SEO data | Google Keyword Planner + Arena |
| Reports | Google Looker Studio |
| Forms | Google Forms |
| Storage | GitHub + Google Drive |

## Quick start (do this today)

1. Read `00-PLAYBOOK/positioning.md` (15 min)
2. Run `python 05-CRM/crm.py` to start your CRM (5 min)
3. Ask Arena to run the ads-audit skill (discovery from the live Meta Ad Library) — or run `python 01-LEADS/discover_leads.py "solar <city>"` (10 min)
4. Copy 1 email from `02-OUTREACH/templates/` and send 5 today (30 min)

That's it. You're now a solar marketing agency.

## Two kinds of audit PDF

| Report | Contains | Built by |
|---|---|---|
| **Full audit** (`02-OUTREACH/audit_pdfs/`) | Website score, tracking/pixels, PageSpeed, conversion checklist **+** live Meta/Google ads | `python 01-LEADS/run_pipeline.py <site> "<Company>" --city <City>` |
| **Live ad activity** (`02-OUTREACH/ads_only_pdfs/`) | Live ads only: Library IDs, start dates, ad copy, live permalinks, funnel, action plan. **States on page 1 that no website audit was run** | `python 01-LEADS/ads_only_report.py` |

**All audits follow the Ksquare format** — see `AUDIT_FORMAT_STANDARD.md` for
the standing format rule (reference: `audit_Ksquare_Energy.pdf`) and the
section-by-section template every new audit must match.

For a current, fully gated worked example, give an agent
`EXAMPLE_AUDIT_REFERENCE.md` together with
`02-OUTREACH/audit_pdfs/audit_SunSolar_Power_Systems.pdf`. That reference shows
the live-ad attribution, honest PageSpeed handling, Smart Pursuit branding,
verification table, and the exact commands every new report must pass.

**No incomplete audits:** `MANDATORY_AUDIT_CHECKS.md` is the definitive list of
website checks that must be resolved from live evidence before an audit is
complete. `None` / "Not found" / "Not checked in this pass" is a FAIL in a full
audit — the run must be re-done, never delivered. The only exceptions are the
four listed in that file (PageSpeed 429, account-only Meta controls, an ad
destination the card does not state, and a pure ads-only report with no website
audit).

Each report kind has its own outreach path — `audit_outreach.py --export` for
full audits, `ads_only_outreach.py --export` for live-ad reports. Both write
the same `sequence_manifest.json` (4 steps per lead), and every sequence is
tagged `report_kind` so the Gmail workflow knows which PDF to attach.

Always gate before delivering, from `01-LEADS/`:

1. `python verify_report.py --all` (full) and `--ads-only` (live-ad reports) —
   structural honesty gate. It now rejects internal-draft markers, held
   reports, unreachable sources, and zero-ad reports.
2. `python delivery_gate.py "<Company>"` — completeness gate. Proves the report
   is fresh, has a numeric score and attributed live ads, and was actually
   built by the repo pipeline. A hand-rolled PDF fails here.
3. `python verify_live.py --company "<Company>"` — third check. Re-fetches the
   live Meta Ad Library through Chrome and the lead's live website and confirms
   every stored figure is still real, live data. `--offline` is only a
   consistency check (exit 4) and is **not** a pass.

**`AGENTS.md` at the repo root is the standing contract for every agent working
here** — format rules, real-data rules, lead qualification, Gmail rules, and the
gates. Read it first.

---

*Built for inconsistent schedules — every system here is designed to work in 30-minute bursts.*
