# Follow-up reconciliation — 2026-11-21

## What was wrong

`sequence_manifest.json` listed **33 sequences with a follow-up due**, many
weeks overdue. Checking them against Gmail one recipient at a time showed that
list was mostly fiction:

- **42 of 43** probed sequences had the wrong `mails_sent` count.
- Every one of the 33 "overdue" rows turned out to be either **already
  finished** or **never started**.
- The manifest carried no record of the 10, 14, 16 or 21 November send waves,
  so it was reporting Oct-dated follow-ups as overdue against prospects who had
  been emailed four times since.
- Three sequences sat at "1 sent, follow-up drafted" when **no first email had
  ever gone out**. One of them (Valcan Solar) was the opposite: recorded as
  "1 sent", actually never followed up.

The manifest is a ledger. Gmail is the source of truth. It had drifted far
enough that scheduling from it would have meant emailing finished prospects a
fifth time.

## Method

Per recipient, `to:<address>` against labels `SENT` **and** `TRASH`, with
`include_spam_trash: true`, reading `subject`, `date` and `message_id_header`.
Then `reconcile_manifest.py` rewrote `mails_sent`, `next_step`,
`next_followup_date`, `state` and each step's `status`/`sent_at` from the dates
observed. Nothing was guessed: 57 of 60 sequences were verified individually,
and the script prints the 3 it could not verify rather than assuming.

Three traps this caught, all of which had produced wrong answers earlier:

1. **Truncation.** A `to:3ssol.in` query returned 3 sends when there were 4 —
   the newest was cut off. Only results marked `complete: true` were used.
2. **Drafts read as sends.** A label-agnostic `to:x` search returns the unsent
   draft too. Only SENT-labelled messages count.
3. **Trash hides real sends — and fake ones.** Valcan Solar's 21 Oct email is
   `TRASH + SENT` because the thread was trashed; it was delivered, so it
   counts. Its 22 Oct follow-up is `DRAFT + TRASH + SENT`, was *never* sent,
   and an early SENT-only query read it as a send.

## Result

| state | count | meaning |
|---|---|---|
| `finished` | 35 | all four steps delivered, nothing owed |
| `live-due` | 13 | real next step outstanding (see below) |
| `never-sent` | 9 | verified zero sends |
| unverified | 3 | no recipient address on file |

### Genuinely due, with a draft ready

| company | real sends | last send | step drafted | draft |
|---|---|---|---|---|
| Aadithya Solar Energies | 3 | 16 Nov | 3 — breakup | `r5067403905562748229` |
| Eagle Solar Systems | 1 | 16 Nov | 1 — follow-up | `r-3851312299244953189` |
| Hindusthan Solar Energy Enterprise | 1 | 8 Nov | 1 — follow-up | `r6889605370398384279` |
| Kypas Solar Power Pvt Ltd | 1 | 8 Nov | 1 — follow-up | `r2849407659705663626` |
| Valcan Solar | 1 | 21 Oct | 1 — follow-up | `r5009590912788668518` |

All five carry the real PDF (18–27 KB, verified through `get_draft`), sit in
their existing thread, and quote a finding from that company's own audit.

### Due on 23 Nov (not drafted — inside the 2-day window)

Green Carbon Hub (step 2), Sri Balaji (step 2), Kakatiya Energies (step 2),
Visiontek (step 2), Laxmi Narayana Solar (step 1), Envious Energy (step 1),
Four Solar (step 2), Origian Power (step 2).

### Never sent (9)

Griffin, Nova Solar, Sri Narayana, Junna Solar, Mamindla, Growcell, Roof Rays,
Akhil Electrical, Manasaa. The last four have step-0 drafts from batch 15,
already built and unsent.

## Content corrections

Reconciling dates was not enough — several stored records disagreed with the
delivered email. See `fix_manifest_content.py`:

- **Sri Balaji** — manifest said 2 live ads; the delivered subject says 6.
- **Envious Energy** — manifest said "Hyderabad"; delivered says "Begumpet".
- **Visiontek** — manifest said 5 ads; the audit counted 11 and the 15 Nov
  email said 11. The 21 Nov subject said 5. Recorded as delivered, gap flagged.
- **Eagle Solar** — manifest said 3 ads; delivered said 2 (a third ad started
  21 Nov).
- **Green Carbon Hub** — the stored step-1 body promised *"the full report …
  attached to my first email"*. No attachment was ever sent on that thread, and
  the first email has none. Rewritten without the claim.

## Two things that need your eye

1. **Green Carbon Hub's 14 Nov subject** read *"14 live Google ads booked under
   Ecoila Private Limited"*. Its own audit contradicts that: ~9 Meta ads, every
   one pointing at `fb.me`, and the record lists **no website at all**. The
   delivered wording is recorded in the manifest, but I would not send another
   email resting on that Google-ads claim.
2. **Today's 21 Nov wave double-sent three prospects.** Kakatiya Energies,
   Visiontek and Sri Balaji each received the same subject twice, 32, 37 and 49
   minutes apart (15:13/15:45, 14:52/15:29, 13:13/16:02). Worth a look at
   whatever drove the batch before the next run.
