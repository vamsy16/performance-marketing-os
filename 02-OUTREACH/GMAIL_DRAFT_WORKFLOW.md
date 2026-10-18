# Gmail Draft Workflow — Audit Emails + Threaded Follow-Ups

How audit emails become Gmail drafts, and how follow-ups land **in the same
thread, 2 days after the previous email was sent** — never as new mails.

Gmail account: `smartpursuit3@gmail.com` (via the Gmail connector in Arena).

---

## The sequence (per lead)

| Step | What | When | Where it lands |
|---|---|---|---|
| 0 | Initial audit email (+ audit PDF attached) | Draft created right after the audit | New draft — becomes the thread when sent |
| 1 | Follow-up 1 | Draft pre-created **inside step 0's thread** (`Re:` + In-Reply-To); **send due 2 days after step 0 is SENT** | Same thread |
| 2 | Follow-up 2 | **2 days after step 1 is SENT** | Same thread |
| 3 | Breakup email | **2 days after step 2 is SENT** | Same thread |

Rules enforced by `sequence.py` (not by memory):

- The 2-day clock starts on the **sent date**, not the draft date. A draft
  sitting in Gmail for a week does not trigger follow-ups.
- A follow-up draft is **refused** until the previous step is recorded as
  sent with its Gmail `thread_id` + Message-ID. When created, it reuses
  that exact `thread_id` and sets `In-Reply-To`/`References` to the
  previous message — Gmail shows it as a reply in the same conversation.
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
                - creates the step-0 Gmail draft with the audit PDF attached
                - creates follow-up drafts 1-3 INSIDE that draft's thread
                  (same thread_id, In-Reply-To/References = previous message)
                - records each: python sequence.py mark-draft --company "<X>" \
                      --step N --draft-id <id> --thread-id <id> --message-id <id>
              Leads without an email are skipped (find the email first).
4. YOU        Review the draft in Gmail → personalize → SEND (manually, always).
5. RECORD     Tell Arena: "I sent <company>"
              Agent finds the sent message in Gmail, then:
                python sequence.py mark-sent --company "<X>" --step 0 \
                    --thread-id <sent thread> --message-id <sent Message-ID>
              -> follow-up 1 due date = sent date + 2 days.
6. FOLLOW-UP  Anytime after that, ask Arena: "check follow-ups due"
              Agent runs `python sequence.py due`. For each due item the
              threaded draft already exists (action=send_draft): you open
              it in Gmail (inside the original conversation), review, SEND.
              Then repeat step 5 for that step. If a draft is missing
              (action=create_draft), the agent creates it in the recorded
              thread first — never as a new mail.
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
