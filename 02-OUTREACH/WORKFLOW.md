# Ads Audit → Outreach System — Step by Step

This is your complete workflow: find companies → audit their ads/website → send personalized emails → book calls → close clients.

---

## The Whole Flow (Visual)

```
┌─────────────────────────────────────────────────────────────────┐
│                    YOUR WEEKLY PIPELINE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  STEP 1: DISCOVER (once/week, one command)                      │
│  $ python 01-LEADS/discover_leads.py "solar Mumbai" --limit 5   │
│    → Finds ACTIVE advertisers in the live Meta Ad Library      │
│    → Pulls each ad's real conversion page destination          │
│    → Writes clean leads (lead_data.py guards the data)         │
│                                                                  │
│  STEP 2: AUDIT (runs automatically in discovery, 30-60 sec each)│
│    For each new lead, checks:                                   │
│    ✅ Meta Pixel installed? (needed for retargeting ads)         │
│    ✅ Google Ads tracking? (needed for conversion tracking)      │
│    ✅ Google Analytics? (needed to measure traffic)              │
│    ✅ Contact form? WhatsApp link? CTAs?                        │
│    ✅ Mobile speed score (Google PageSpeed)                      │
│    ✅ SEO basics (title, meta, schema, OG tags)                 │
│    ✅ SSL, page count, local SEO signals                        │
│    → Scores each company 0-100 (higher = more issues = better)  │
│    → Saves detailed audit as JSON                               │
│                                                                  │
│  STEP 3: RANK (automatic)                                       │
│    → Sorts by opportunity (most issues = best sales pitch)      │
│    → Built on demand from the audit JSONs                       │
│                                                                  │
│  STEP 4: GENERATE EMAILS (once/week, 10 min)                    │
│  $ python 02-OUTREACH/audit_outreach.py --top 10 --export       │
│    → Reads audit findings for each lead                         │
│    → Auto-picks best email template based on their weaknesses   │
│    → Fills in company name, city, specific issues               │
│    → Saves ready-to-send emails as .txt files                   │
│                                                                  │
│  STEP 5: DRAFT IN GMAIL (agent does this — GMAIL_DRAFT_WORKFLOW)│
│    → ONLY the initial draft is created (audit PDF attached)     │
│    → Tracked columns: thread_id, mails_sent, next_followup_date │
│    → You review in Gmail and SEND manually (never auto-sent)    │
│    → Tell Arena "I sent <company>" → send is recorded           │
│                                                                  │
│  STEP 6: FOLLOW UP (+2 days after previous send, same thread)   │
│  $ python 02-OUTREACH/sequence.py due                           │
│    → On the due day, agent creates the follow-up draft IN the   │
│      recorded thread (never in advance, never a new mail)       │
│    → You review + send; mails_sent +1, next date moves +2 days  │
│    → 3 follow-ups max (last one is the breakup email)           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## What Gets Audited (The 10 Checks)

| Check | Why It Matters | Your Pitch Angle |
|---|---|---|
| **Meta Pixel** | Without it, can't run retargeting ads or track conversions | "You're paying for ads blind" |
| **Google Ads / GTM** | Without it, can't measure which campaigns work | "You don't know your cost per lead" |
| **Google Analytics** | Without it, don't know traffic volume or sources | "You're flying blind on your own website" |
| **Contact form** | Main lead capture mechanism | "Visitors can't easily reach you" |
| **WhatsApp link** | #1 conversion channel for Indian home services | "Losing mobile leads to competitors" |
| **CTA buttons** | Guide visitors to take action | "No clear next step for visitors" |
| **Mobile speed** | 60%+ of solar searches are on mobile | "Slow site = lost customers" |
| **SEO (title/meta)** | Determines Google ranking | "Invisible in local search results" |
| **Schema markup** | Enables rich results in Google | "Missing premium Google listings" |
| **Open Graph tags** | How links look when shared | "Links look broken on social/WhatsApp" |

---

## Email Strategy

### Which email gets sent (auto-selected based on audit):

| Situation | Template Used | Angle |
|---|---|---|
| Mobile speed < 40/100 | `speed_urgent` | "You're losing X% of mobile visitors" |
| Low score + no Meta Pixel | `competitor_gap` | "Your competitors are tracking, you're not" |
| General issues found | `audit_hook` | "I found these specific issues on your site" |
| High score (well-optimized) | `competitor_gap` | "You're doing well but missing advanced tactics" |

### Why audit-based outreach works better than generic:

| Generic Cold Email | Audit Email |
|---|---|
| "Hi, I do digital marketing" | "Hi, I noticed your Meta Pixel isn't installed" |
| Sounds like everyone else | Shows you actually looked at THEIR business |
| 1-2% reply rate | 8-15% reply rate |
| "Not interested" | "Send me the video" |

---

## Zero Duplicate Guarantee

The system checks THREE layers before adding any lead:

```
Layer 1: Company name (normalized)
  "SunTech Solar Pvt Ltd" ≡ "Suntech Solar" ≡ "SUNTECH"
  Strips: pvt, ltd, limited, solar, energy, solutions, etc.

Layer 2: Website domain
  "www.suntech.com/about" ≡ "suntech.com" ≡ "suntech.in"

Layer 3: Email domain
  "info@suntech.com" already seen → skip
  (Personal emails like gmail.com are not used for domain matching)
```

Data checked against:
- ✅ Existing `leads.csv` (cleaned by `lead_data.py` — junk hosts and garbled contacts rejected)
- ✅ CRM data (`crm_data.json`)
- ✅ Results within the same run (double safety)

---

## Command Reference

```bash
# === DISCOVER + AUDIT + RANK + PDF (one command) ===
python 01-LEADS/discover_leads.py "solar Mumbai" --limit 5
python 01-LEADS/discover_leads.py "solar Delhi" --limit 10 --competitors 3

# === AUDIT ONE KNOWN WEBSITE ===
python 01-LEADS/run_pipeline.py https://example.com "SunTech Solar" --city Mumbai

# === CLEAN LEAD DATA ===
python 01-LEADS/lead_data.py           # repair/filter/sanitize leads.csv
python 01-LEADS/lead_data.py --check   # dry run

# === TESTS ===
python 01-LEADS/tests.py

# === VERIFY A REPORT BEFORE DELIVERY ===
python 01-LEADS/verify_report.py --latest

# === SINGLE AUDIT (one company) ===
python 01-LEADS/ads_audit.py https://example.com
python 01-LEADS/ads_audit.py "SunTech Solar" --city Mumbai

# === GENERATE EMAILS + FOLLOW-UP SEQUENCE ===
python 02-OUTREACH/audit_outreach.py --top 10
python 02-OUTREACH/audit_outreach.py --top 10 --export   # Files + sequence_manifest.json
python 02-OUTREACH/audit_outreach.py --name "SunTech"    # Specific company
python 02-OUTREACH/audit_outreach.py --template speed_urgent  # Force template

# === GMAIL DRAFTS + THREADED FOLLOW-UPS (+2 days, same thread) ===
python 02-OUTREACH/sequence.py status    # all sequences, draft/sent state, due dates
python 02-OUTREACH/sequence.py due       # follow-ups due to send today
python 02-OUTREACH/tests_sequence.py     # sequence engine tests
# Agent runbook: 02-OUTREACH/GMAIL_DRAFT_WORKFLOW.md

# === CRM ===
python 05-CRM/crm.py                        # Interactive
python 05-CRM/crm.py import ../01-LEADS/leads.csv
python 05-CRM/crm.py followup               # Who to follow up with
python 05-CRM/crm.py pipeline               # Sales pipeline view
```

---

## Weekly Schedule (Inconsistent Hours Friendly)

| Day | Task | Time |
|---|---|---|
| **Monday** | Run pipeline → generate emails → send 10 | 45 min |
| **Tuesday** | Follow up with non-repliers from last week | 20 min |
| **Wednesday** | Send 10 more new emails | 30 min |
| **Thursday** | Follow ups + book any calls | 20 min |
| **Friday** | Weekly review + plan next week | 30 min |
| **Weekend** | REST (or batch content via Arena if energized) | 0-60 min |

**Weekly total: ~3-4 hours for a complete outreach engine.**

---

## What To Do When...

### "No one is replying"
- Send more volume (20/day instead of 5)
- Check spam folder setup: add SPF/DKIM to your email
- The "breakup" follow-up (template 3) gets the highest reply rate

### "They replied but aren't interested"
- Reply: "Understood. Can I check back in 6 months?"
- Add to CRM with 6-month follow-up
- They may need you during slow season

### "They want to know more"
- Send the audit video (record with Loom — free)
- Offer free 15-min call
- Use Cal.com for scheduling (free)

### "They want a proposal"
- Use `02-OUTREACH/templates/proposal.md`
- Send within 24 hours (speed wins)

### "I don't know how to deliver the service"
- Read `04-DELIVERY/playbooks/` for step-by-step guides
- Use Arena to generate content drafts
- Start with the easiest service (usually SEO content or social)

---

## Free Tools You'll Need

| Tool | Purpose | Link |
|---|---|---|
| **Gmail** | Send emails | mail.google.com |
| **Google Ads Transparency** | Check if they run Google ads | adstransparency.google.com |
| **Meta Ad Library** | Check if they run Facebook/Instagram ads | facebook.com/ads/library |
| **Loom** (free) | Record audit videos | loom.com |
| **Cal.com** (free) | Schedule calls | cal.com |
| **Canva** (free) | Design content | canva.com |
| **Buffer** (free) | Schedule social posts | buffer.com |
| **Google PageSpeed** | Website speed testing | pagespeed.web.dev |
