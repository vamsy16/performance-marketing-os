# Batch 15 — 5 solar leads, Telangana — 2026-11-21

Builder: [`build_batch15_5leads_telangana.py`](build_batch15_5leads_telangana.py)
Reports: `01-LEADS/ads_only_results/audit_*.json` → `02-OUTREACH/ads_only_pdfs/audit_*.pdf`
Second pass: [`verify_batch_claims.py`](verify_batch_claims.py)

Every fact below was read at its own source on 2026-11-21. Where a fact could not be
re-confirmed it is **not** in the report. Where two sources disagree, both are recorded
and neither is reconciled by guesswork.

---

## The five leads

| # | Company | City | Site | Ads | Score | Funnel |
|---|---|---|---|---|---|---|
| 1 | Growcell Solar Energy | Hyderabad (Banjara Hills) | `growcellenergy.in` live | 2 | **3/100** | FB lead form |
| 2 | SunSolar Power Systems | Hyderabad (Narsingi) | none — NXDOMAIN | 4 | ads-only | FB lead form |
| 3 | Roof Rays Solar Solutions | Hyderabad (Tellapur) | `roofrays.in` live | 3 | **5/100** | FB lead form |
| 4 | Akhil Electrical Works | Suryapet | none | 4 | ads-only | WhatsApp |
| 5 | Manasaa Enterprises | Hyderabad (Miyapur) | none — did not load | 1 | ads-only | WhatsApp |

Scores exist only for the two leads whose website was actually read and scored.
The three without a website carry no score, because a score would have to be invented.

---

## Verified ad inventory

Each Library ID below was opened **at its own permalink** and its page name, start date
and copy re-read. That matters: the Ad Library's rendered HTML puts the "Library ID"
label between two creatives, so a page listing read naively shifts every ID by one.

**Growcell Solar Energy** — 2 live ads, both 15 Nov 2026
- `2267587767143531` — Hinglish, "₹78,000 TAK SUBSIDY", placed *Growcell Solar Energy with Growcell Energy LLP*, carries the qualifying line "subject to government guidelines and approval"
- `1171646568632890` — English, "How much solar does your home need?", card headline "₹5K–₹10K Bill? Go Solar!"
- A direct Ad Library lookup of the **brand page 61591290572665 returns no active ads.** The spend sits on the **Growcell Energy LLP page 1244655595388630**.

**SunSolar Power Systems** — 4 live ads
- `2413566255849370` — 21 Nov 2026 — 5 kW ₹2,18,999 (₹2,96,999 − ₹78,000) — prints **98666 20001**
- `1866738597708833` — 21 Nov 2026 — 4 kW ₹1,71,999 — prints 98666 02001
- `2576227376137902` — 22 Oct 2026 — 3 kW ₹1,31,999, Hyderabad — prints 98666 02001
- `2285688872164421` — 23 Oct 2026 — same 3 kW creative re-addressed to Ananthapur, hashtags still `#Hyderabad`

**Roof Rays Solar Solutions** — 3 live ads
- `1825502928519547` — 16 Nov 2026 — solar + EV, 2,000 km, 600 units/mo, "up to ₹20,000/month on fuel"
- `1635924467937920` — 4 Nov 2026 — "Ready to cut down your electricity bills?", subsidy up to ₹78,000
- `1184145723936677` — 4 Nov 2026 — "Turn Sunshine into Savings!", subsidy up to ₹78,000

**Akhil Electrical Works** — 4 live ads, all WhatsApp-only
- `997508846276370` — 21 Nov 2026 — Telugu, "subsidy details, prices and installation information — contact us now"
- `1677824443701148` — 17 Nov 2026 — "Go Solar, Save More!"
- `1387795526583908` — 17 Nov 2026 — "3KW & 5KW Solar Systems | Subsidy Assistance | Call Now." (only ad naming a size)
- `1680326913622219` — 14 Nov 2026 — "Go Solar, Save More!"

**Manasaa Enterprises** — 1 live ad
- `826884287112902` — started 22 Aug 2026, unchanged since. 3 kW ₹2,05,000\* / 5 kW ₹3,10,000\* / 10 kW ₹5,92,000\*, "GOVT. SUBSIDY UP TO ₹78,000\*", 7901253949 | 8074507650, "Kakinada | Hyderabad", `manasaaenterprises2024@gmail.com`.

---

## What the second pass changed

The user's instruction was to run a third eye over the audit before any of it reached a
lead. It caught six things. All six were fixed **before** the PDFs were rebuilt and
**before** any draft was written.

1. **A SunSolar "ad" was not SunSolar's.** Library ID `1443902311044175` had been
   recorded in an earlier pass as a fifth SunSolar creative. Opened at its permalink, it
   resolves to a **Venus home appliances** ad (page 254386191238752). It was removed and
   `2285688872164421` — a real SunSolar ad, verified at its own permalink — took its place.
2. **Roof Rays "publishes no price anywhere" was false.** Its residential guide carries a
   kW price table (3 kW ₹1,45,000–2,10,000; 5 kW ₹2,30,000–3,50,000; 10 kW ₹4,80,000–7,20,000)
   and a units-to-kW table. The finding was rewritten into what is actually true and more
   useful: the site owns the one comparison asset in the market and none of the three ads
   uses it or links to it.
3. **Akhil's ad set was described from a stale read.** The 17 Nov creative `1387795526583908`
   has its own copy ("3KW & 5KW Solar Systems | Subsidy Assistance") and was not a duplicate
   of the other 17 Nov ad. The findings now say only one of the four ads names a system size,
   rather than claiming none do.
4. **The control engine was reading the analyst's notes as the advertiser's copy.** Batch
   builders append commentary to `text` after an "Ad Library note:" marker. A keyword pass
   over that string saw "no warranty is stated" and credited the ad with a warranty.
   `_ad_copy()` now truncates at the marker, and M26/M30 are graded only from angles and
   social-proof flags the lead **declares**, never from keyword hits.
5. **Dates were compared as strings.** `max(["Nov 21, 2026", "Oct 23, 2026"])` returns
   `Oct 23`. Freshness now sorts on parsed dates, and M-CR1 only passes when a full page
   listing was actually read — otherwise it is `unknown`, not a pass on a guess.
6. **A single-ad lead was being scored on coverage.** Manasaa has one live ad; M26 returned
   `pass` off one creative. With fewer than two readable ads it is now `unknown`.

The verifier prints, per lead, every ad ID with its date, every contact fact, and every
finding that contains a number — the sentences most likely to be wrong. It exits non-zero
if a report is structurally incomplete.

Run it before any batch is emailed:

```
cd 01-LEADS && python3 verify_batch_claims.py Growcell_Solar_Energy SunSolar_Power_Systems \
  Roof_Rays_Solar_Solutions Akhil_Electrical_Works Manasaa_Enterprises
```

---

## Conflicts recorded, not resolved

- **Akhil Electrical Works has two published door numbers** for the same Sajjapuram /
  Palakeedu location: **2-30** on the TGREDCO empanelled-supplier list (TSRE250617) and
  **H.No. 1-26** on the TSSPDCL registered-contractor list. Both are on the record; the
  report says so and does not pick one.
- **Roof Rays' advertiser page id differs by source.** The Facebook profile URL carries
  `61587695438410`; the Ad Library reports the advertiser as `997092546826993`. Recorded
  as-is.
- **SunSolar prints its own phone number two ways** — `98666 20001` on the 5 kW ad,
  `98666 02001` on the other three. Both are quoted; which is right is not knowable from
  outside the business.
- **Manasaa's Justdial listing** (Miyapur, behind RBR1 Complex, 4 years, "starts from
  ₹40/watt") is a directory record, not the advertiser's own statement, and is labelled as
  such in the report.

## Not checked — and therefore not claimed

- Meta Pixel, GA4, GTM, Google Ads, meta description, OG tags and JSON-LD need the raw
  served HTML. The fetch channel used here renders the page, so these are `None`
  ("not checked") on every report — never "absent".
- PageSpeed returned **HTTP 429** on every attempt, so no speed score exists for Growcell
  or Roof Rays. The reports say so.
- No Ads Manager data (spend, bids, audiences, frequency, EMQ) was available for any of the
  five, so those controls are `unknown` throughout.

## Outreach

Four step-0 Gmail drafts were created on 2026-11-21 and **not sent**:

| Company | To | Draft ID | Report attached |
|---|---|---|---|
| Growcell Solar Energy | sales@growcellenergy.in | `r5061649286227555027` | audit_Growcell_Solar_Energy.pdf (26 KB) |
| Roof Rays Solar Solutions | support@roofrays.in | `r5965019761585299951` | audit_Roof_Rays_Solar_Solutions.pdf (28 KB) |
| Akhil Electrical Works | narasimhayaragorla2@gmail.com | `r-2221174036565104944` | audit_Akhil_Electrical_Works.pdf (21 KB) |
| Manasaa Enterprises | manasaaenterprises2024@gmail.com | `r1297571565926609327` | audit_Manasaa_Enterprises.pdf (19 KB) |

Each draft's Gmail `size_estimate` was checked against its PDF on disk after creation
(38.9 KB / 41.2 KB / 32.1 KB / 28.7 KB encoded), because an earlier attempt attached a
67-byte placeholder stub instead of the report. The four text-only drafts from that
attempt were deleted, not left alongside these.

**SunSolar Power Systems has no email on file and no website.** Its sequence is in the
manifest with `to` empty and no draft created — it needs a number-first approach, not a
guessed address. `sunsolarpowersolutions.in` does not resolve and no address appears in any
of the four ads.
