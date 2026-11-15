# Batch 20: Solar Hyderabad — 2 NEW Active-Advertiser Leads (live-verified 2026-11-15)

Pulled **2026-11-15**, second discovery run of the day (batch 19 already rowed 4
leads earlier the same day). Same rule as every batch since the de-dup guard was
built: every candidate was checked against the whole known-leads registry
(`known_leads.py`, now **305 entries / 69 domains / 131 names / 57 active
vetoes**) **before** it could be rowed, and anything already in the pipeline
was skipped and reported.

**This batch asked for 5 leads and delivered 2. The gap is real and is stated
here rather than papered over.** The Hyderabad/Telangana solar segment has been
swept hard — `leads.csv` went from 62 to 68 rows across batches 18, 19 and 20 —
and the pools that used to yield 5 leads per run are now returning
re-confirmations of advertisers already in the pipeline. Every source that
could still be reached was reached; the full accounting of what was tried and
what it returned is in the "What was searched" section below.

**2 new leads rowed into `01-LEADS/leads.csv` (66 → 68 rows):**

| # | Lead | Live ad evidence (all read 2026-11-15) | Conversion destination | Website | Contact (verified live 2026-11-15) |
|---|---|---|---|---|---|
| 1 | **Meissa Reeve** | Live **Meta** ad, Library ID **1691922249204293**, started **Nov 14 2026** (one day old when swept) — found in the `solar net metering Hyderabad` keyword sweep | api.whatsapp.com (WhatsApp deep link — the ad never lands on the website) | https://meissareeve.com/ | **info@meissareeve.com** (also enquiry@meissareeve.com on the solar division) · +91 7893088071 · Saptagiri Nagar, Retibowli, Mehdipatnam, Hyderabad |
| 2 | **Visiontek Solar Energy** | **4 live Meta ads** on the `Visionteknewenergy` page — Library IDs **1133037052650969**, **1138341982459373**, **1449750756945639** (all started **Nov 12 2026**) and **2319725685441877** (started Sep 4 2026) — found in the `solar panels Telangana` keyword sweep | instagram.com (a generic Instagram root link — the ads drive no site traffic) | https://visiontek.solar/ | **info@visiontek.com** · +91 9701601421 · Linkwell Telesystems Pvt. Ltd., 1-11-252/1B, Behind Shoppers' Stop, Begumpet, Hyderabad 500016 |

Both are **Meta-only** advertisers. The Google Ads Transparency `?domain=`
probe under `region=IN` returns **0 ads** for meissareeve.com and for
visiontek.solar, and that is recorded as such in each leads.csv snippet rather
than being rounded up into "live ads" of unspecified platform.

## Third-eye re-verification pass (run after discovery, as required)

The owner asked for a re-verification pass that runs **even after auditing**,
because a wrong email or a dead ad destroys trust in the agency. It was run
here, and it is what the two rows above rest on.

| Check | Meissa Reeve | Visiontek Solar Energy |
|---|---|---|
| Ad seen live in the Meta Ad Library today | Yes — Library ID 1691922249204293, "Active", started Nov 14 2026 | Yes — four Library IDs, all "Active", three started Nov 12 2026 |
| Ad re-read a second time after the first sighting | Yes | Yes |
| Email read off the company's **own** site today | Yes — meissareeve.com/contacts/ | Yes — visiontek.solar/contact-us/ |
| Email exists anywhere else (cross-check) | Yes — info@meissareeve.com and enquiry@meissareeve.com both appear on re.meissareeve.com | Yes — info@visiontek.com on visiontek.solar, and info@visiontek.co.in on the parent visiontek.co.in contact page |
| Phone read off the company's own site today | Yes — +91 7893088071 (also the WhatsApp link target on the homepage) | Yes — +91 9701601421 (also the WhatsApp link target on the homepage) |
| Address read off the company's own site today | Yes — Saptagiri Nagar, Retibowli, Mehdipatnam, Hyderabad | Yes — Begumpet, Hyderabad 500016 |
| In `leads.csv` before this run | No | No |
| In `known_leads_extra.json` before this run | No | No |
| Solar EPC / solar business, in segment | Yes — rooftop plants, residential/commercial/industrial/agricultural | Yes — on-grid/hybrid inverters, LFP storage, residential solar systems |

**One thing worth flagging for the outreach, not a disqualifier:** both
companies' ads point at a dead-end destination — Meissa Reeve's at a WhatsApp
deep link, Visiontek's at a bare `instagram.com` root. That is a concrete,
verifiable finding for a performance-marketing pitch and is written into both
leads.csv snippets.

## What was searched

| Source | What it gave |
|---|---|
| Meta Ad Library keyword sweeps, **country=IN** (14 sweeps run today) | **Meissa Reeve** (`solar net metering Hyderabad`) and **Visiontek Solar Energy** (`solar panels Telangana`). Everything else surfaced was already rowed, already vetoed, or out of segment. |
| Google Ads Transparency `?domain=` probes, **region=IN** (20 run today) | **0 ads on every domain probed.** gigawattsolar.in, greentekindia.co.in, solaridea.com, zytechsolar.co.in, amplussolar.com, solarbull.in, naturalenergies.in, naturalenergiess.com, novasolar.in, renewsolar.in, accutech.co.in, coolkaru.com, emugenergy.com, sunenergysystems.com, cubeforesolutions.in, creativeenergysolutions.in, suntek.co.in, absolar.in, sunupsolarpower.com, sunpowersolarsolutions.com, sunpowersolarservices.co.in, sunsolarsystems.in, visiontek.solar, meissareeve.com |
| Meta sweeps for named PM Surya Ghar vendors | `Sirius Solar Energy` → "No ads match your search criteria"; `Greentek India solar` → "No ads match your search criteria" |
| PM Surya Ghar Yojana Telangana vendor lists (Northern 84 + Southern 89) | the candidate pool for the Google domain probes above — every name on them was cross-checked against the 66 existing rows and the 32 existing vetoes before probing |
| Web search (2 calls) | Meissa Reeve's site, email and address; the Visiontek solar division and its contacts. Also surfaced four unrelated Hyderabad solar domains (Sunup, Sunpower ×2, Sun Solar Systems), all probed and all 0 ads |

**Explicitly not re-tried, because batch 19 exhausted them:** `solar Suryapet`,
`solar Siddipet`, `solar Nizamabad`, `solar Karimnagar`, `solar Khammam`,
`solar Warangal`.

## Rejected this run — and why (all recorded as vetoes)

| Candidate | Live ads | Why it was not rowed |
|---|---|---|
| **Ohmhydrasolutions** | Meta Library ID 1160240256472893, Nov 12 2026 | **Out of segment.** Malayalam-language electrical/plumbing ad with KSEB connection assistance — a Kerala local-services business. |
| **Mocaup** | Meta Library ID 1540056057821006, Aug 5 2026 | **Out of segment.** Resells solar enquiries *to* EPCs — a lead-generation agency, i.e. a competitor, not a prospect. |
| **Alsaa D Global Real Estate** | Meta Library ID 2160085101235277, Aug 13 2026 | **Out of segment.** Real-estate investment scheme selling panel-ownership leases on the Kapil Solar Energy site at Sangareddy. |
| **Go Rewatt** | Meta Library ID 1498216172114493, Sep 30 2026 | **Out of segment.** Distributor recruitment for Karnataka and Tamil Nadu. |
| **BoxBee** | Meta Library ID 990388019982431, Oct 16 2026 | **Out of segment.** E-commerce seller of a Rs.1,999 solar-panel cleaning brush. |
| **SunSolarhyd** | 3 live Meta ads, Oct 2026 | **No published email.** Suite 312, Kokapet Terminal Complex, Narsingi, Hyderabad and +91 98666 02001 are in the ad copy, but no email is published anywhere and the domain could not be identified — sunsolarpowersystems.com is a different, Ramanathapuram business. |
| **Sirius Solar Energy** | none | **No live ads.** 0 Google ads and 0 Meta ads, both probed today. |
| **Greentek India Pvt Ltd** | none | **No live ads.** 0 Google ads and 0 Meta ads, both probed today. |
| **Gigawatt Solar**, **Solar Idea**, **Zytech Solar India**, **Amplus KN One Power**, **Solar Bull Enegy**, **Natural Energies**, **Nova Solar Solutions**, **Renew Solar**, **Accutech Infosystems**, **Coolkaru Info Solutions**, **E Mug Energy**, **Sun Energy Systems**, **CubeFore Solutions**, **Creative Energy Solutions**, **Suntek Energy** | none | **No live ads.** 0 Google ads each under region=IN. |
| **Sunup Solar Power**, **Sunpower Solar Solutions**, **Sunpower Solar Services**, **Sun Solar Systems** | none | **No live ads.** 0 Google ads each under region=IN, despite each publishing an email address. |

All were written into `known_leads_extra.json` as `vetted` entries so they are
skipped automatically on the next sweep rather than re-litigated. The registry
now holds **57 vetoes: 45 `live-ads`, 5 `published-email`, 7 `segment`.**

## Guard gaps found and closed

After the two were rowed, the feed was replayed a second time and the guard
reported **2 advertisers still "new"**:

- **`Visionteknewenergy`** was not matched to the rowed **Visiontek Solar
  Energy**. The cause is the same class of miss fixed for *Telangana Solar* in
  batch 19: "Visionteknewenergy" is a single concatenated token, so the
  matcher cannot link it to the three-token rowed name.
- **`FreyrEnergy`** was not matched to the rowed **Freyr Energy** (lead 34).
  Same cause — one concatenated token, and "Energy" is on the `NON_IDENTIFYING`
  list, leaving zero identifying shared tokens.

Both were fixed by adding explicit `known` entries with notes saying why (the
registry's `known` list went 9 → 12). Re-running the feed after that gives
**0 new advertisers** — every one of the 39 cards in the file is absorbed.

## Guard fix found while closing this batch

Writing up the rejected candidates in the table above exposed a real bug in the
duplicate guard, fixed in `known_leads.py` and covered by three new tests.

**The bug.** `_load_batch_logs()` registers the leading cells of *every* table
row in every batch log, including the "candidates rejected this run" rows. So
every rejected candidate acquires a permanent `batch_log:` entry. `verdict()`
consulted that general index **before** the vetoes, which meant a veto could
never lapse: the veto would expire, and the name would immediately be reported
`known` again by the batch-log prose describing its own rejection. Zytech was
vetoed on 2026-11-15 and, before the fix, would have been treated as "already
seen" forever — with the batch log, not the veto, given as the reason.

**The fix.** An active veto is now consulted first, and it is the strongest
statement the registry can make, so it outranks a batch-log mention. Matching
is tried strongest-signal-first across all active vetoes (exact normalised
name, then domain, then containment, then shared tokens) so the weakest signal
cannot win by coming first. Only if no active veto matches are the expired ones
consulted; if one of those matches, the result is a non-verdict
(`VETO_EXPIRED`), so the name becomes eligible again rather than being pinned
by the prose that described its rejection. Independent evidence — a
`leads.csv` row, a sequence, an audit, an explicit `known` entry — still wins
over a batch-log mention, so nothing already in the pipeline can be re-offered
as new.

**Two test expectations changed, deliberately.** `Shree Adithya Solar` was
asserted to be `known` from a batch log. It is now `review`: "Adithya" is a
trading name shared by three separate Hyderabad businesses, and the owner ruled
these are distinct companies and that the guard must report REVIEW and never
auto-clear. The old assertion auto-cleared exactly the collision the owner said
must not be auto-cleared. Both tests were updated and the reason recorded in a
comment.

**Regression tests added** (all three fail if the precedence is reverted):
`test_batch_log_prose_cannot_pin_an_expired_veto`,
`test_active_veto_wins_over_batch_log_prose`,
`test_no_rowed_lead_is_shadowed_by_an_active_veto`.

## Honesty notes

- **This batch is 2 leads, not the 5 that were asked for.** Nothing was padded,
  renamed or re-used to make the number up. The two that are here each clear
  every gate on live, freshly-read evidence.
- **No audit was run for either lead.** Audits need a browser, which this
  sandbox does not have — the same limitation as batches 18 and 19.
  `audit_score` / `audit_issues_count` are left empty rather than filled with
  guesses. Both companies' sites *were* read live today with a plain fetch,
  which is where the contact details and the ad-destination findings come
  from; the full pixel/score/speed audit is what is missing.
- **Both leads are Meta-only.** Their Google Ads Transparency counts are 0, and
  the snippets say so plainly. Do not describe them as "running Google ads".
- **Visiontek Solar Energy is a manufacturer, not an installer.** Its solar
  division launched in 2025 inside VISIONTEK Linkwell Telesystems Pvt Ltd and
  sells inverters, LFP batteries and optimisers, though its ads do sell
  residential solar systems to homeowners. That is the honest characterisation
  to use in outreach.
- **Meissa Reeve is a multi-division company.** The parent site also runs EV
  charging stations and retrofitting; the solar division is
  re.meissareeve.com. Both inboxes published on the solar division are recorded
  (info@ and enquiry@).
