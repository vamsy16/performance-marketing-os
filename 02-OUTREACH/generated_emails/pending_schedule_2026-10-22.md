# Pending send schedule — 2026-10-22 (owner schedules in Gmail UI)

The Gmail connector/API has **no scheduled send** (send_draft accepts only a
draft ID and sends immediately). Gmail's "Schedule send" is a UI-only feature,
so the owner schedules these in Gmail: open each draft → **▼ next to Send** →
**Schedule send** → **Pick date & time** → enter the time below.

These are the 8 step-1 follow-up drafts (threaded `Re:` replies, due 2026-10-22).
12-minute gaps, 19:05–20:29 IST.

| # | Time (IST) | Company | Draft ID | Thread |
|---|---|---|---|---|
| 1 | 19:05 | Ksquare Energy | r-8292260654144352221 | 1a14f7346f5232f1 |
| 2 | 19:17 | Venus home appliances | r-940394346038524194 | 1a1548e33069b440 |
| 3 | 19:29 | AB Solar Power Systems | r-7275176065916553057 | 1a1548778b6c59c4 |
| 4 | 19:41 | Evergrid Energy | r2655231626867408902 | 1a1548250791ea62 |
| 5 | 19:53 | Punarvi Energies | r-6242315279930009856 | 1a15482b564e18fd |
| 6 | 20:05 | Solox Energies | r-8263102418285004760 | 1a15482ea841990b |
| 7 | 20:17 | Truzon Solar | r-3424819755560992643 | 1a1548288ba322d4 |
| 8 | 20:29 | Varahi Energies | r6019480240701992362 | 1a15483125a2db5c |

## After they fire

Scheduled sends land in Sent automatically. For each one, record it so the
step-2 clock starts (step 2 due = send date + 2 days):

```bash
cd 02-OUTREACH
python sequence.py mark-sent --company "<Company>" --step 1 \
    --thread-id <thread> --message-id <sent Message-ID>
```

Ask Arena "check follow ups dues" any time to reconcile — the sent messages can
also be found in Gmail directly (they appear in the same threads as the
originals).

## Still unscheduled (owner's queue, unchanged)

Step-0 drafts awaiting their own schedule: Eastman New Energy, Ellvin Energy,
Kapil Power & Infra, Solar6 (batch 5); Twilight Solar; Ecolt Energy, Orizen
Solar Innovations, Ray On Solar Systems (batch 6).
