# Pending sends 2026-11-01 — owner schedules in the Gmail UI

Gmail now holds **23 drafts** (verified live this session: 19 new threaded follow-ups
+ the 4 batch-10 first contacts). Gmail's scheduled send is UI-only, so pick a time
on each draft.

## What this run found

1. **The 8 step-2 follow-ups recorded as `draft` on 2026-10-24 were already SENT**
   that morning (10:20–11:59 IST). `send_draft` removes a draft once it is sent, so they
   had vanished from the draft list — the manifest was stale. All 8 are now reconciled
   with `mark-sent`, using the real Gmail Message-IDs.

2. **Only one lead replied** out of the 29 contacted: **Arkahub** sent an auto-
   acknowledgement on 22 Oct (“we will respond within 1 business day”) and never followed
   up. Arkahub is **held** — no follow-up drafted. Decide whether to send anyway or close.

3. **Valcan Solar's step-1 draft `r-4135467498809954457` is still in Gmail trash** — left
   untouched as agreed. It has to be untrashed and re-created before it can be sent.

4. **Five follow-up bodies carried the wrong live-ad count** (a template filled
   `results_count` — the Ad Library's *total page results* — instead of the tracked
   Hyderabad ads). Corrected against `ads_only_results/` before drafting:

   3S Solutions 7→4 · Hydromo 170→2 · Dakshin 4→1 · PMP 5→1 · Freyr 300→9.

## Step-1 follow-ups due 2026-10-25 (11) — threaded `Re:` replies, no attachment

First follow-up, each a reply inside its original thread. Suggested slots,
10-minute gaps starting 19:00 IST:

| # | Company | To | Draft ID | Thread | Suggested send (IST) |
|---|---|---|---|---|---|
| 1 | 3S Solutions | praveen@3ssol.in | `r6397784173831779964` | `1a166b32ae127c61` | 19:00 |
| 2 | Arcedo Systems | info@arcedo.net | `r-2181479242357173233` | `1a163e5661ececcb` | 19:10 |
| 3 | MrSolar | info@mrsolar.in | `r8560132172193023567` | `1a163e53b42765d9` | 19:20 |
| 4 | Krisol Solar | sales@krisolsolar.com | `r-9203193995202302192` | `1a166b0f94c4086c` | 19:30 |
| 5 | Hydromo | info@hydromo.in | `r-2856305988064251806` | `1a166b3641cd2487` | 19:40 |
| 6 | Dakshin Solar Power Systems | dakshinsolar@gmail.com | `r8713060942401927599` | `1a166b20e9febcaf` | 19:50 |
| 7 | PMP Solar Power | sreepooji27@gmail.com | `r-2541826676909045158` | `1a166b1353d6dd55` | 20:00 |
| 8 | Freyr Energy | info@freyrenergy.com | `r4584898575890334462` | `1a166d20b4fc0c5d` | 20:10 |
| 9 | Bhanu PV Solar | info@bhanupvsolar.in | `r7089982008769408237` | `1a166d20de09bd9f` | 20:20 |
| 10 | VajraSimha Industries | info@vajrasimhaindustries.com | `r-1843515129432486710` | `1a166d20a867560a` | 20:30 |
| 11 | Vanguard Energy | info@vanguardenergysystems.com | `r7631925188687984557` | `1a166d20c6b73541` | 20:40 |

## Step-2 follow-ups due 2026-10-25 (8) — threaded `Re:` replies, no attachment

Second follow-up, each a reply inside its original thread:

| # | Company | To | Draft ID | Thread | Suggested send (IST) |
|---|---|---|---|---|---|
| 1 | Twilight Solar | Prabhakar.katkam@gmail.com | `r-2110915721965915820` | `1a159024db4302f5` | 20:50 |
| 2 | Eastman New Energy | support@eaplworld.com | `r2808759547035506534` | `1a15c27f27ae66ca` | 21:00 |
| 3 | Ellvin Energy | info@ellvinenergy.com | `r-3166587118059409100` | `1a15c27f322d91c0` | 21:10 |
| 4 | Kapil Power & Infra | info@kapilpower.com | `r8552279280765444541` | `1a15c27f25ceb58a` | 21:20 |
| 5 | Solar6 | info@solar6.in | `r-8670428499399651021` | `1a15c27f4479f7da` | 21:30 |
| 6 | Ecolt Energy | Contact@ecoltenergy.com | `r-5803861967741783515` | `1a15c77bbccbd363` | 21:40 |
| 7 | Orizen Solar Innovations | info.orizensolar@gmail.com | `r-1098130070009235802` | `1a15c78051e8aee2` | 21:50 |
| 8 | Ray On Solar Systems | rayonsolars@gmail.com | `r-692434448095830709` | `1a15c7825fac6b5f` | 22:00 |

## Not drafted — needs a decision

| Company | Step | State | Note |
|---|---|---|---|
| Arkahub | 1 | **HELD** | Replied 22 Oct with an auto-acknowledgement, no follow-up since. |
| Valcan Solar | 1 | **IN TRASH** | Draft `r-4135467498809954457` sits in Gmail trash; must be restored before sending. |

## Newly surfaced — step-3 breakup emails, due 2026-10-26 (8)

Because the 8 step-2s turned out to be sent, their **breakup** step (the 3rd and final
follow-up) is now due tomorrow. Not drafted yet — confirm before I create them:

AB Solar Power Systems · Evergrid Energy · Ksquare Energy · Punarvi Energies ·
Solox Energies · Truzon Solar · Varahi Energies · Venus home appliances

## Reconciliation log (2026-10-24, from Gmail SENT labels)

| Time (IST) | Company | Step | Gmail Message-ID |
|---|---|---|---|
| 10:20 | AB Solar Power Systems | 2 (breakup-preceding) | 1a16c3e88e212459 |
| 10:32 | Evergrid Energy | 2 (breakup-preceding) | 1a16c4984e108cfd |
| 10:59 | Ksquare Energy | 2 (breakup-preceding) | 1a16c623df567d5a |
| 11:14 | Punarvi Energies | 2 (breakup-preceding) | 1a16c6ff86eb0f92 |
| 11:28 | Solox Energies | 2 (breakup-preceding) | 1a16c7ccaa05e44c |
| 11:42 | Varahi Energies | 2 (breakup-preceding) | 1a16c899baf9a498 |
| 11:59 | Truzon Solar | 2 (breakup-preceding) | 1a16c992a0d3d7ad |
| 10:47 | Venus home appliances | 2 (breakup-preceding) | 1a16c574038d7f34 |

Step-0 and step-1 Message-IDs were also missing from the manifest for Arcedo Systems,
MrSolar, and the eight step-2 leads; the real Gmail Message-IDs have now been recorded
so follow-up threading is enforced by the tool rather than assumed.
