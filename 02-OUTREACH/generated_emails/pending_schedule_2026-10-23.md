# Pending sends 2026-10-23 — owner schedules in the Gmail UI

Everything below is **in Gmail as drafts right now** (21 drafts, all verified
live). Nothing has been sent. Gmail's scheduled send is UI-only, so pick a time
on each draft — suggested slots follow last night's pattern (12-minute gaps).

## Step-1 follow-ups due today (9) — threaded `Re:` replies, no attachment

Each is already a reply inside the original thread (thread_id + In-Reply-To set).
Suggested evening slots:

| # | Company | To | Draft ID | Suggested send (IST) |
|---|---|---|---|---|
| 1 | Twilight Solar | Prabhakar.katkam@gmail.com | r-6240091710688519130 | 19:05 |
| 2 | Valcan Solar | info@valcansolar.com | r-4135467498809954457 | 19:17 |
| 3 | Eastman New Energy | support@eaplworld.com | r-4784469455772552442 | 19:29 |
| 4 | Ellvin Energy | info@ellvinenergy.com | r204611243871433289 | 19:41 |
| 5 | Kapil Power & Infra | info@kapilpower.com | r-6483424029239870774 | 19:53 |
| 6 | Solar6 | info@solar6.in | r2311677648781836733 | 20:05 |
| 7 | Ecolt Energy | Contact@ecoltenergy.com | r-6348310474821914853 | 20:17 |
| 8 | Orizen Solar Innovations | info.orizensolar@gmail.com | r3495773383773156031 | 20:29 |
| 9 | Ray On Solar Systems | rayonsolars@gmail.com | r-6651475767359469637 | 20:41 |

## Batch-7 first contacts (3) — new threads, PDF attached

First contact works better in the morning; send whenever suits:

| Company | To | Draft ID | PDF attached |
|---|---|---|---|
| MrSolar | info@mrsolar.in | r-1164586820850053341 | audit_MrSolar.pdf |
| Arcedo Systems | info@arcedo.net | r-315798432579919374 | audit_Arcedo_Systems.pdf |
| Arkahub | care@arkahub.in | r-3781039558763888632 | audit_Arkahub.pdf |

## Batch-8 first contacts (5) — new threads, PDF attached

Added 2026-10-23 after this evening's table was written. All five are
ads-only live-ad reports (no website audit run — the PDF says so on page 1):

| Company | To | Draft ID | PDF attached |
|---|---|---|---|
| Krisol Solar | sales@krisolsolar.com | r-8249548030083204998 | audit_Krisol_Solar.pdf |
| PMP Solar Power | sreepooji27@gmail.com | r6071778764438726540 | audit_PMP_Solar_Power.pdf |
| Dakshin Solar Power Systems | dakshinsolar@gmail.com | r1833948473957777594 | audit_Dakshin_Solar_Power_Systems.pdf |
| 3S Solutions | praveen@3ssol.in | r1459020982860151007 | audit_3S_Solutions.pdf |
| Hydromo | info@hydromo.in | r-490954975402821851 | audit_Hydromo.pdf |

## Batch-9 first contacts (4) — new threads, PDF attached

Added 2026-10-23 (batch 9). All four are ads-only live-ad reports (no website
audit run — the PDF says so on page 1). Freyr Energy is the big one: a
~300-result Ad Library set with 9 live Telugu ads, all clicking out to fb.me.

| Company | To | Draft ID | PDF attached |
|---|---|---|---|
| Freyr Energy | info@freyrenergy.com | r4073229830171604447 | audit_Freyr_Energy.pdf |
| Vanguard Energy | info@vanguardenergysystems.com | r-5519094373057590916 | audit_Vanguard_Energy.pdf |
| Bhanu PV Solar | info@bhanupvsolar.in | r-8589525829074466851 | audit_Bhanu_PV_Solar.pdf |
| VajraSimha Industries | info@vajrasimhaindustries.com | r4471985646435117683 | audit_VajraSimha_Industries.pdf |

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
python sequence.py mark-sent --company "<Company>" --step <0|1> --date 2026-10-23
```

Last night's 8 follow-ups (Ksquare, Venus, AB Solar, Evergrid, Punarvi, Solox,
Truzon, Varahi) all fired and are already marked — step 2 for those is due
2026-10-24.
