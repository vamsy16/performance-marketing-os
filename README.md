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

Each report kind has its own outreach path — `audit_outreach.py --export` for
full audits, `ads_only_outreach.py --export` for live-ad reports. Both write
the same `sequence_manifest.json` (4 steps per lead), and every sequence is
tagged `report_kind` so the Gmail workflow knows which PDF to attach.

Always gate before delivering: `python 01-LEADS/verify_report.py --all` for full
reports, `python 01-LEADS/verify_report.py --ads-only` for the live-ad ones.

---

*Built for inconsistent schedules — every system here is designed to work in 30-minute bursts.*
