# Batch 19: Solar Hyderabad — 4 NEW Active-Advertiser Leads (live-verified 2026-11-15)

Pulled **2026-11-15**. Same rule as every batch since the de-dup guard was
built: every candidate was checked against the whole known-leads registry
(`known_leads.py`, now **301 entries / 67 domains / 128 names / 32 active
vetoes**) **before** it could be rowed, and anything already in the pipeline
was skipped and reported.

**4 new leads rowed into `01-LEADS/leads.csv` (62 → 66 rows):**

| # | Lead | Live ad evidence (all read 2026-11-15) | Conversion destination | Website | Contact (verified live 2026-11-15) |
|---|---|---|---|---|---|
| 1 | **Kakatiya Energies** | Live **Meta** ad, Library ID **1893246231838609**, started **Nov 13 2026** (two days old when swept) — found in the `solar Warangal` keyword sweep | api.whatsapp.com | https://www.kakatiyaenergies.com/ | **kakatiyasolarenergies@gmail.com** (also info@kakatiyaenergies.com) · +91 8801549199 / +91 8125801257 · 1-7-895 Hunter Rd, above Union Bank, near Kakatiya Zoological Park, Sri Ram Colony, Subedari, Hanamkonda 506009 (a Hyderabad address is also listed) |
| 2 | **Green Secure Energy Pvt Ltd** | **23 live Google ads** under identity-verified advertiser **AR08755770391764402177** (Green Secure Energy private ltd), domain greensecure.in, region=IN — the largest live Google ad count in this sweep | greensecure.in (the site itself) | https://greensecure.in/ | **sales@greensecure.in** · +91 9618888430 / 8019525206 / 8019525209 |
| 3 | **Comuti Energy Private Limited** | **1 live Google ad** under identity-verified advertiser **AR14841886882970730497** (Comuti Energy), domain comuti.in, region=IN | comuti.in (the site itself) | https://comuti.in/ | **enquiry@comuti.in** (published on the contact page) · +91 8977036018 · F-5/A, Road No 16, Phase I, IDA Jeedimetla, Hyderabad 500 055 |
| 4 | **Telangana Solar Energy** | Live **Meta** ad seen in the `PM Surya Ghar Telangana` keyword sweep (FB page 61589077441645). **Library ID not captured** — see the honesty note below | fb.me/ | https://www.telanganasolarenergy.com/ | **Info@telanganasolarenrgy.com** · +91 8555986188 / 8639111695 / 9700152279 · 6-2-113 Nakha Chowrasta, Karimnagar 505001 |

## How the 4 were found

| Source | What it gave |
|---|---|
| Google Ads Transparency `?domain=` probes, **region=IN** (30 run today) | **Green Secure Energy** (23 ads), **Comuti Energy** (1), **Silres/Fenice** (4). Zero ads for rishisolar.com, v3electricals.com, e-greensolutions.in, cloudjetsolar.com, petawattssolar.com, iliospower.com, akonisolar.com, telanganasolarenergy.com, avghnisolar.com, beplindia.net, cubeforesolutions.in, rurayenergies.com, vamanaenergy.com, shaatitsolar.com, arkawaaree.com, griinergy.com, enviousenergy.com, buddingleafinfra.com, srisparks.in, asthraprojects.com, sunfield.energy, akshayasolar2023.com, sssenergys3.com, sunfieldenergy.in, vprosolarsystems.com, sungrace.net, scubeenergyinfra.com, amigoenergies.com, suntechnologiesindia.com, gles.in, srisaisolarsystems.com, vprosolarsystem.com, feniceenergy.com(→ Silres), osmiumenergy.in, ecotonic.in, anisunsolar.in, raywattsolar.in, accesssolar.in, inanisolar.in, srisolar.co.in |
| Meta Ad Library keyword sweeps, **country=IN**: `solar Hyderabad` (~370), `solar installation Telangana` (~62), `solar subsidy Hyderabad` (~73), `solar Warangal` (~30), `PM Surya Ghar Telangana` (~17), `solar Karimnagar` (~12), `solar Khammam` (~7), `solar Nizamabad` (0), `solar Nalgonda` (0) | **Kakatiya Energies** (Warangal sweep), **Laxminarayana Solar Solutions** and **Telangana Solar** (PM Surya Ghar Telangana sweep) |
| The PM Surya Ghar Yojana Telangana vendor lists (Southern + Northern) | the candidate pool for the Google domain probes — this is where Green Secure, Comuti and Silres were picked up |
| Each company's own site, fetched today | every email/phone/address in the table above was read off the live page today |

## De-dup guard — what it caught this run

Replayed the saved feed (`01-LEADS/feeds/solar_hyderabad_2026-11-15.json`,
20 cards) through `discover_leads.py --feed`. The guard reported:

```
[dedupe] 12 advertiser(s) skipped — already in the pipeline:
  Sri Balaji Solar Energies  (matches 'Sri Balaji Solar Energies' in leads.csv)
  ORBIT SOLAR               (matches 'Orbit Solar' in leads.csv)
  Suryon                    (matches 'Suryon' in leads.csv)
  SolarSquare Energy        (matches 'SolarSquare Energy' in leads.csv)
  Lumisun solar             (matches 'Lumisun Solar' in leads.csv)
  Green Carbon Hub          (matches 'Green Carbon Hub' in leads.csv)
  mrsolar.in                (matches 'mrsolar.in' in batch_log:...batch9_2026-10-23)
  Sunova Green Energy ...   (matches 'Sunova Green Energy' in leads.csv)
  Ecolt Energy              (matches 'Ecolt Energy' in leads.csv)
  Varna Solar Pvt. Ltd.     (matches 'Varna Solar Pvt. Ltd.' in leads.csv)
  Solox Energies Pvt Ltd    (matches 'Solox Energies Private Limited' in leads.csv)
  Big G Industries          (matches 'Big G Industries' in vetted:live-ads)
```

8 new advertisers surfaced; **4 were rowed**, 4 were rejected (see below).

## Rejected this run — and why (all recorded as vetoes)

| Candidate | Live ads | Why it was not rowed |
|---|---|---|
| **Laxminarayana Solar Enterprises** | Meta Library ID 1963245304346857, started Oct 1 2026, Karimnagar | **No published email.** Justdial and the ad itself list phone only (07041658904 / 9493093728 / 8712780023). Same rule that blocked Mega Solar India and PNR Sunrise. |
| **Silres Energy Solutions Pvt Ltd** (trades as **Fenice Energy**) | 4 live Google ads, AR03821416193491730433, feniceenergy.com | **No email on its own site.** silres@feniceenergy.com and sales@feniceenergy.com exist only on third-party lists (the PM Surya Ghar vendor list and Crunchbase); feniceenergy.com publishes only toll-free 1800 889 8457. It is also a 251–500 employee Chennai-HQ company, a different profile from the local EPCs this pipeline targets. |
| **ktmsolarsolutions** | Meta Library ID 971947288860777, started Nov 5 2026 | **Out of segment.** HQ is Matlampatti, Dharmapuri, Tamil Nadu, advertising across TN/AP/Karnataka/Telangana/Pondicherry/Kerala. Same class as Teramor Developers and Cygni Energy. No published email either. |
| **Sahasra Enclave** | Meta Library ID 988627010433216, started Nov 11 2026 | **Out of segment.** A farmland / villa-plot real-estate project at Malkapur, Choutuppal — not a solar EPC. |

All four were written into `known_leads_extra.json` as `vetted` entries so
they are skipped automatically on the next sweep rather than re-litigated.
Two new gate values were introduced for them: **`published-email`** and
**`segment`** (the existing gate was only `live-ads`). The registry now holds
32 vetoes: 26 `live-ads`, 4 `published-email`, 2 `segment`.

## One guard gap found and closed

After the four were rowed, the feed was replayed a second time and the guard
reported **1 advertiser still "new"**: the Meta page name **"Telangana Solar"**
was not matched to the rowed **"Telangana Solar Energy"**. The cause is that
both *Solar* and *Energy* sit on the guard's `NON_IDENTIFYING` list — they are
too generic to match on, which is exactly what stops "Shree Adithya Solar"
colliding with "Adithya Solar Tech". So the only tokens the two names share are
non-identifying ones and the matcher declines.

Fixed by adding an explicit `known` entry for `Telangana Solar` →
telanganasolarenergy.com in `known_leads_extra.json`, with a note saying why.
Re-running the feed after that gives **0 new advertisers** — every card in the
file is now absorbed into the registry.

## Honesty notes

- **Telangana Solar Energy's Meta Library ID is deliberately blank.** The ad
  was seen live in the `PM Surya Ghar Telangana` sweep, but the Library ID
  line was cut off in the captured page, and a follow-up
  `view_all_page_id=61589077441645` lookup returned *no ads*. Rather than
  guess an ID, it is recorded as not captured. The ad evidence is the live
  sweep itself; the contact evidence is the company's own contact page.
- **Green Secure Energy's homepage counters are placeholders**, not claims to
  quote back at them: "1864+ Years of Experience", "1870+ Happy Clients",
  "1870+ Projects", "1864MWp+ Projects Across India". Recorded in the
  leads.csv snippet so no future audit quotes them as fact.
- **Kakatiya Energies is Warangal-based, not Hyderabad.** It was rowed because
  its own site lists a Hyderabad address and it advertises into the
  Hyderabad/Telangana market; the city column says so plainly rather than
  calling it a Hyderabad company.
- No audit was run for any of these four. Audits need a browser, which this
  sandbox does not have — the same limitation as batch 18. Every value in the
  table above was read live on 2026-11-15, and `audit_score` /
  `audit_issues_count` are left empty rather than filled with guesses.
