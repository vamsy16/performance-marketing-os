# Gmail Draft Workflow — Audit Emails + Threaded Follow-Ups

How audit emails become Gmail drafts, and how follow-ups land **in the same
thread, 2 days after the previous email was sent** — never as new mails.

Gmail account: `smartpursuit3@gmail.com` (via the Gmail connector in Arena).

---

## The sequence (per lead)

| Step | What | When | Where it lands |
|---|---|---|---|
| 0 | Initial audit email (+ audit PDF attached) | Draft created right after the audit | New draft — becomes the thread when sent |
| 1 | Follow-up 1 | Draft created **on the due day** (2 days after step 0 is SENT), **inside step 0's thread** (`Re:` + In-Reply-To) | Same thread |
| 2 | Follow-up 2 | **2 days after step 1 is SENT** | Same thread |
| 3 | Breakup email | **2 days after step 2 is SENT** | Same thread |

Rules enforced by `sequence.py` (not by memory):

- **Only one draft exists at a time.** Follow-up drafts are never
  pre-created — each is created on its due day, and only then.
- The 2-day clock starts on the **sent date**, not the draft date. A draft
  sitting in Gmail for a week does not trigger follow-ups.
- A follow-up draft is **refused** before its due date, and refused until
  the previous step is recorded as sent with its Gmail `thread_id` +
  Message-ID. When created, it reuses that exact `thread_id` and sets
  `In-Reply-To`/`References` — Gmail shows it as a reply in the same
  conversation, never a new mail.
- Each sequence row tracks: `thread_id`, `mails_sent` (how many emails
  actually sent), `next_followup_date` (previous sent date + 2 days).
- Max 3 follow-ups (step 3 = breakup). Then the sequence stops.
- State lives in `generated_emails/sequence_manifest.json` and survives
  re-running the generator.

## Flow

```
1. AUDIT      python 01-LEADS/discover_leads.py "solar Hyderabad"   (or run_pipeline.py)
2. GENERATE   python 02-OUTREACH/audit_outreach.py --export
              -> email_*.txt + sequence_manifest.json (4 steps per lead)
3. DRAFT      Ask Arena: "create Gmail drafts from the sequence manifest"
              Agent, per lead WITH an email address:
                - creates ONLY the step-0 Gmail draft (audit PDF attached)
                - records it: python sequence.py mark-draft --company "<X>" --step 0 \
                      --draft-id <id> --thread-id <id> --message-id <id>
                - follow-up drafts are NOT created yet — see step 6
              Leads without an email are skipped (find the email first).
4. YOU        Review the draft in Gmail → personalize → SEND (manually, always).
5. RECORD     Tell Arena: "I sent <company>"
              Agent finds the sent message in Gmail, then:
                python sequence.py mark-sent --company "<X>" --step 0 \
                    --thread-id <sent thread> --message-id <sent Message-ID>
              -> follow-up 1 due date = sent date + 2 days.
6. FOLLOW-UP  On/after next_followup_date, ask Arena: "check follow-ups due"
              Agent runs `python sequence.py due`, and for each due item
              creates the follow-up draft THAT DAY inside the recorded
              thread_id (Re: + In-Reply-To to the previous sent message),
              records it with mark-draft, and tells you. You review + send
              it in Gmail, then repeat step 5 for that step (mails_sent
              increments, next_followup_date moves +2 days).
```

## Commands

```bash
cd 02-OUTREACH
python audit_outreach.py --export     # generate emails + sequence manifest
python sequence.py status             # every lead, every step, due dates
python sequence.py due                # follow-ups ready to draft today
python sequence.py mark-sent --company "Ksquare Energy" --step 0
```

Change the gap anytime: `SP_FOLLOWUP_DELAY_DAYS=3` (default 2).

## What the agent must never do

- Never send a draft — sending is always the owner's manual click in Gmail.
- Never create a follow-up as a new standalone mail, and never before the
  previous step is sent + recorded.
- Never draft for a lead with no email address in the manifest.
