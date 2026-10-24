# Pending sends 2026-10-24 — owner schedules in the Gmail UI

Gmail currently holds **8 drafts** (verified live). Everything else has been
sent. Gmail's scheduled send is UI-only, so pick a time on each draft.

## Step-2 follow-ups due today (8) — threaded `Re:` replies, no attachment

Second follow-up, each already a reply inside its original thread. Suggested
evening slots (12-minute gaps, same pattern as last night):

| # | Company | To | Draft ID | Suggested send (IST) |
|---|---|---|---|---|
| 1 | Evergrid Energy | contact@evergridenergy.in | r-1616060442534136137 | 19:05 |
| 2 | Ksquare Energy | info@ksquareenergy.com | r-325979824391751070 | 19:17 |
| 3 | Punarvi Energies | solar@punarvienergies.com | r-924935629236002471 | 19:29 |
| 4 | Solox Energies | contact@solox.in | r650655381105518856 | 19:41 |
| 5 | AB Solar Power Systems | sales@absolar.in | r-7867665252532371964 | 19:53 |
| 6 | Truzon Solar | info@truzonsolar.com | r3858809555228656443 | 20:05 |
| 7 | Varahi Energies | varahienergies@gmail.com | r-8400391796335018476 | 20:17 |
| 8 | Venus home appliances | enquiry@venushomeappliances.com | r627125041477903852 | 20:29 |

## Sent 2026-10-23 by the owner (reconciled in the manifest)

**Step 0 — first contacts (12), all with PDF attached:**

| Time (IST) | Company | To |
|---|---|---|
| 10:26 | Arkahub | care@arkahub.in |
| 10:42 | Arcedo Systems | info@arcedo.net |
| 10:54 | MrSolar | info@mrsolar.in |
| 11:02 | Krisol Solar | sales@krisolsolar.com |
| 11:13 | PMP Solar Power | sreepooji27@gmail.com |
| 11:26 | Dakshin Solar Power Systems | dakshinsolar@gmail.com |
| 11:41 | 3S Solutions | praveen@3ssol.in |
| 11:52 | Hydromo | info@hydromo.in |
| 12:04 | VajraSimha Industries | info@vajrasimhaindustries.com |
| 12:17 | Freyr Energy | info@freyrenergy.com |
| 12:33 | Vanguard Energy | info@vanguardenergysystems.com |
| 12:45 | Bhanu PV Solar | info@bhanupvsolar.in |

**Step 1 — follow-ups (8):** Ray On 08:20, Orizen 08:36, Ecolt 08:52, Solar6
09:08, Kapil 09:23, Ellvin 09:37, Eastman 09:52, Twilight 10:11.

**Step 1 fired 2026-10-22 (8, marked earlier):** Ksquare 18:50, Venus 19:02,
AB Solar 19:13, Evergrid 19:27, Punarvi 19:41, Solox 19:58, Truzon 20:03,
Varahi 20:17 — these are the 8 step-2 drafts at the top of this page.

## Heads-up — Valcan Solar

The Valcan step-1 draft (`r-4135467498809954457`, due 2026-10-23) is **in
Gmail trash** — it is no longer in drafts and nothing was sent. It looks
deleted rather than sent. If you still want it, say the word and it gets
re-created; the manifest still shows it as a draft.

## Next dues (nothing to prepare yet)

- **2026-10-25 — step 1** for the 12 first contacts sent 2026-10-23
  (Arkahub, Arcedo, MrSolar, Krisol, PMP, Dakshin, 3S, Hydromo, VajraSimha,
  Freyr, Vanguard, Bhanu).
- **2026-10-25 — step 2** for the 8 step-1 sends of 2026-10-23
  (Ray On, Orizen, Ecolt, Solar6, Kapil, Ellvin, Eastman, Twilight).

## Not in drafts — and why

- **Orbit Solar** — no email published anywhere on its site; phone/WhatsApp
  (+91 9059806772) and the site form only. Cannot be emailed.
- **Green Carbon Hub, Sri Balaji Solar Energies, Suryon** — their audit PDFs are
  the old, wrong "no website" versions (all three DO have live sites). Need a
  re-audit before any email; drafting against a wrong report would be dishonest.
- **Four Solar, Junna Solar, Mamindla, Origian Power** — no live ads; per your
  standing rule these are not pitched.

## After each send

Mark it so the next step dates correctly (next follow-up = send date + 2 days):

```
cd 02-OUTREACH
python sequence.py mark-sent --company "<Company>" --step <1|2> --date 2026-10-24
```

## Batch 10 — 4 new step-0 drafts ready (created 2026-10-24, NOT yet sent)

First contact for the four new leads, each with its live-ad PDF attached
(ads-only report + claude-ads control review). Suggested slots below.

| # | Company | To | Draft ID | Suggested send (IST) |
|---|---|---|---|---|
| 1 | Sunova Green Energy | sunovagreenenergy@gmail.com | r8672245658090296228 | 21:30 |
| 2 | Wisda Energy | connect@wisda.in | r-6911418009660809427 | 21:42 |
| 3 | SolarSquare Energy | welisten@solarsquare.in | r-1045940870714107417 | 21:54 |
| 4 | Rayzon Solar | contact@rayzonenergies.com | r-2836600481260964329 | 22:06 |

Gmail now holds **12 drafts** in total (the 8 step-2 follow-ups above plus
these 4). Once these are sent, step 1 for each falls due **2026-10-26** and
the batch-10 sequence runs on the same 2-day cadence.
