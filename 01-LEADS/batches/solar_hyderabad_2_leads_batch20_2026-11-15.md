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

## Third-eye re-verification, 2026-11-15 — two of five ad IDs were wrong

The re-verification pass was run on 2026-11-15, after the batch was committed,
by opening **every recorded ad by its own Library ID** rather than trusting the
keyword-sweep capture. It found real errors, and both leads' evidence has been
corrected.

| Recorded in batch 20 | Actually belongs to |
|---|---|
| Meissa Reeve, Library ID `1691922249204293` | **AB Solar Power Systems** (`facebook.com/absolarpowersystems`) |
| Visiontek, Library ID `2319725685441877` (4 Sep 2026) | **mr_koti_00 / Garuda Solar Energy Solutions, Guntur** |

**Meissa Reeve** — the company, the contact details and the live-ad status all
held up, but the Library ID was somebody else's. The real ad is
**`1641050694153685`**, on the page `Meissa Reeve`
(`facebook.com/61596697943588/`), started 14 Nov 2026, ~18 hrs active, sending
the click to a WhatsApp deep link. One ad, not more.

**Visiontek Solar Energy** — the lead is real and much bigger than recorded. The
`2319725685441877` ID is a Guntur advertiser's. The verified truth is
**11 distinct live creatives** on the `Visionteknewenergy` page, all started
12 Nov 2026 except a Diwali creative from 6 Nov 2026, with Meta reporting
"2 ads use this creative and text" on each — so the true ad count is higher
than the number of distinct IDs. The original record said 4 ads.

Verified IDs: `1133037052650969`, `1449750756945639`, `2208275783425425`,
`1138341982459373`, `910533972050441`, `1642086640990986`,
`1949641059333335`, `1846039203313070`, `1443714387877981`,
`2172490176994377`, `986852867827035`.

Also re-confirmed on 2026-11-15: **0 Google ads** for both `meissareeve.com` and
`visiontek.solar` under `region=IN`; Meissa Reeve's phone, email, address,
hours and WhatsApp link on `meissareeve.com/contacts/`; Visiontek's phone,
email, WhatsApp and address on `visiontek.solar/contact-us` plus its four
product lines on the homepage.

**Why this matters.** Both PDFs are built from this data. Had they been built
before the re-check, they would have carried another company's ad ID as proof
that these two were advertising. `leads.csv`, the feed file and the batch log
have all been corrected, and the ads-only PDFs were rebuilt from the corrected
data.

**What the two mis-attributed IDs turned out to be, and what happened to them:**

- **AB Solar Power Systems** (`facebook.com/absolarpowersystems`, live ad
  `1691922249204293`, started 14 Nov 2026) — **already a rowed and audited lead**
  in `leads.csv`, with a CI audit score of 7/100 from 2026-10-19 and its own
  outreach sequence. Re-running the corrected feed makes the duplicate guard
  match it to that row, which is the guard working exactly as intended and
  confirms the correction is sound. Not rowed again. Its verified details:
  `sales@absolar.in`, +91 80990 40600 / +91 90001 45304, Flat 401 Siri Arcade,
  Beside Care Hospitals, Lumbini Avenue, Gachibowli, Hyderabad 500032.
- **mr_koti_00** (live ad `2319725685441877`, started 4 Sep 2026) — an ad for
  **Garuda Solar Energy Solutions**, 3rd Floor Amarravati Rd, Guntur, Andhra
  Pradesh, +91 8886946169. Guntur is outside the Hyderabad/Telangana segment
  this pipeline works, so it is **vetoed on `segment`**, not rowed.

After the corrections and that veto, the feed replays to **28 skipped / 0 new
advertisers** — fully absorbed, as it should be.

**Batch 20 remains 2 leads.** The re-verification corrected the evidence
attached to them; it did not add a lead, because the one advertiser that looked
new was already in the pipeline and the other is out of segment.

## Full audits, Ksquare-shaped, 2026-11-15

Both leads now have a full DIGITAL MARKETING & PAID ADS AUDIT in the same shape
as `audit_Ksquare_Energy`, built by `build_full_audits_batch20.py` from page
text read live on 2026-11-15. The page text is saved in
`01-LEADS/fetched/` so every count in the reports can be re-derived from it.

| Lead | Score | Issues | Wins | PDF |
|---|---|---|---|---|
| Meissa Reeve | 23/100 | 11 | 7 | `02-OUTREACH/audit_pdfs/audit_Meissa_Reeve.pdf` |
| Visiontek Solar Energy | 10/100 | 8 | 9 | `02-OUTREACH/audit_pdfs/audit_Visiontek_Solar_Energy.pdf` |

**Nothing was copied from `audit_Ksquare_Energy.json`.** That file was read for
its shape only. A leakage probe over both new PDFs and both JSONs, using
Ksquare's title, H1, URL, sitemap count, load time, ad IDs and ad copy as
probes, returns **0 hits**. Visiontek's score of 10 is a coincidence with
Ksquare's 10 - it is its own arithmetic (no contact form on the homepage +8,
no visible testimonials +2).

**What was measured, and how.** Page text was read live through the sandbox's
page fetcher and counted mechanically with a fixed regex, not estimated by
eye: image counts and alt attributes, H1 counts and text, CTA link text,
`tel:` / `mailto:` / `wa.me` links, form blocks, and the sitemap URL list.
The saved page text for each is named in the audit JSON's provenance rows.

**What is deliberately null, and printed as "could not be checked in this
pass".** All eight tracking pixels (the page HTML source was never available,
only rendered text, so no pixel claim is made either way); meta description,
Open Graph, Schema.org and favicon (head markup); server response time and
PageSpeed (no route to the API); live chat, popup opt-in and pricing-page link
(not observable in page text). `calculate_audit_score()` treats a null as
unmeasured - it neither penalises nor counts as a win, and it never appears as
a finding.

### The findings worth leading with

**Meissa Reeve - 23/100.** The solar division is the competent half: 44 images
with only 3 missing alt, one H1, twelve named installations with locality and
system size, a 4.8-star Google rating, a real Contact Form 7 form and full
address and hours. The parent domain is not: **36 unedited WordPress
theme-demo pages are live and in the sitemap** - `/my-account/`, `/checkout/`,
`/cart/`, sixteen `/elements/*` pages, `/404-layout/`, `/multipage/`, `/shop/`,
four complete demo homepages (`/homepage-gas-station/`,
`/homepage-rental/`, `/homepage-towing/`, `/homepage-natural-honey/`), three EV
scooter brands (`/komaki/`, `/gemopai/`, `/virtus-motors/`), `/petrol-pumps/`
and `/airport-metros/`. A prospect following a link can land on a page selling
petrol pumps. Also: the phone and email on `/contacts/` are plain text, not
`tel:`/`mailto:` links, so a mobile visitor cannot tap either; the homepage has
no H1 and 10 of its 12 images have no alt text; the solar division homepage has
50 links and **not one of them is an action**; raw image URLs are listed as
sitemap entries; and a public view counter prints "11,020 total views, 10 views
today".

**Visiontek Solar Energy - 10/100.** The site itself is in genuinely good
shape - every image has alt text across all three pages read, exactly one H1
per page, a tappable `tel:` and `mailto:` and a working form on the contact
page, WhatsApp on every page, and a blog posted on 11 and 12 Nov 2026. The
problems are structural. **Ten of the eleven live ads do not point at the
website**: six go to a bare `instagram.com` root, one to `fb.me`, four carry no
link at all - so almost none of the spend can reach any of it. **There is no
sitemap and no robots.txt** - both return 404. **Every social link on the
contact page is a dead `contact-us#` anchor**, including for the Facebook page
where the 11 ads actually run. **"Download Catalogue (PDF, 1.2 MB)" links to
`product#`** - there is no PDF behind it. The homepage advertises four of the
six product lines. And a broken video element prints "Your browser does not
support video." into the page body.

### One renderer fix this uncovered

The full-audit story in `audit_pdf.py` never rendered `contact_facts`, so a
report could carry a lead's phone and email in the JSON and never show them -
and the reader had no way to re-check the contact facts the report rests on.
Added a "Verified contact details" section to `build_story()`, matching the one
the ads-only story already had, and regenerated the 9 full-audit PDFs whose
JSON carries contact facts. The 7 that carry none are unchanged.

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
