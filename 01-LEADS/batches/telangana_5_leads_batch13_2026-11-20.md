# Telangana (state-wide) — 5 new leads — Batch 13 — 2026-11-20

Search brief: solar installers in **Telangana State outside Hyderabad**.
All 5 are in Warangal / Nizamabad / Karimnagar — no overlap with the 46 leads
already in `leads.csv` (checked by host, not by name).

## Verification method — read this before using any number below

Every site below was fetched live on 2026-11-20 with a real page fetch. Each
field is labelled with **how** it was confirmed:

- **[LIVE]** — read off the company's own page during this session's fetch.
- **[SEARCH]** — appeared in a search-index excerpt of the company's own page,
  but the direct fetch of that specific page failed. Treated as *probable*,
  not confirmed.
- **[GOVT]** — appears on the official TGREDCO empanelled-supplier list
  (`tgredco.telangana.gov.in/Updates_2026/List_of_Empanelled_Suppliers_2026.pdf`),
  read via a search-index excerpt of that PDF. The PDF itself would not fetch
  directly in this environment, so this is an excerpt read, not a full-document
  read.

**No audit was run.** The audit pipeline (`run_pipeline.py`) needs Chrome +
Playwright + outbound network and cannot execute in this sandbox. There are no
audit scores, no ad counts, no PageSpeed numbers and no PDFs for these 5 leads.
Anything below that looks like a "finding" is quoted from the company's own
published page — it is what their site says, not a measurement I took.

---

## 1. Orugallu Solar Energies — Hanamkonda / Warangal

| Field | Value | Source |
|---|---|---|
| Website | https://www.orugallusolar.com/ | **[LIVE]** fetched, 2 chunks |
| Phone | +91 90597 00497 (tel: and wa.me/919059700497) | **[LIVE]** |
| Email | orugallusolarenergies@gmail.com | **[SEARCH]** — on their own `/subsidy/` page; direct fetch of that page failed. The pages I *did* fetch publish **no email at all** — phone/WhatsApp and a callback form only. |
| Address | G-20/21, KRMS Reddy Complex, 6-2-91/A, Kakaji Colony, Hanamkonda 506001 | **[LIVE]** (Maps deep link) |
| GST / TSRE | GST 36ALEPM3018K2Z3 · TSRE250763 | **[LIVE]** printed on their homepage |
| Founder | Mendu Raghu, Founder & MD | **[LIVE]** |

Claims on their own site, quoted not verified: MNRE + TSREDCO approved,
PM Surya Ghar authorised vendor; panels Adani/Waaree/Vikram/Premier, inverters
Deye/Sofar/Servotech; live savings calculator stating its own assumptions
(₹7.5/unit rising 3%/yr, 1450 units/kW/yr, 0.5% ageing, ₹60,000/kW system cost).

Why this is a good lead: the site is genuinely strong — 12 named installations
with dates and localities (Nellikuduru 13 Oct, Kishanpura 10 Nov, Bhupalpally
8 Oct, Gopalapuram 26 Oct, Teachers Colony 15 Oct, Elukurthy 16 Oct, Reddy
Colony 5 Oct, Gorrekunta 9 Sep, Shiva Nagar 16 Sep, Warangal-506005 15 Sep,
Chennaraopet 13 Oct) and it shows its calculator maths. **The gap is that the
pages I fetched publish no email address** — enquiry depends on a phone call or
a form that "also goes to us on WhatsApp". Confirm the email before mailing.

---

## 2. Green Solar Energys — Hanamkonda / Warangal

| Field | Value | Source |
|---|---|---|
| Website | https://www.greensolarenergys.com/ | **[LIVE]** fetched |
| Email | greensolarenergy.wgl@gmail.com | **[LIVE]** — homepage top bar *and* contact page |
| Phone | +91 95739 08852 | **[LIVE]** |
| Address | 2-5-57, Opposite AR Takeaway, KLN Reddy Colony, Subedari, Hanamkonda 506001 | **[LIVE]** contact page |

Since 2019 per their own site. Services: residential / commercial / industrial,
on-grid, off-grid, hybrid.

Two things visible on the live page worth raising with them, both quoted from
their own markup rather than measured by me:

1. The contact page's "Maps" link is `https://www.google.com/maps/undefined` —
   the map deep link is not built, so the location link is dead.
2. The headline counters read **122+ Projects Completed / 147+ Satisfied
   People / 104+ Team Members / 134+ Award Winning**. 134 awards and 104 staff
   for a company that says it started in 2019 reads as template filler rather
   than fact. Also present: stray `BESbswy` text (an animation-library
   artefact) leaking into the rendered page, and the About/Why-Us headings
   render letter-spaced ("B e s t   S o l a r ...").

---

## 3. Sravanthi Solar — Nizamabad

| Field | Value | Source |
|---|---|---|
| Website | https://sravanthisolar.in/ | **[LIVE]** fetched |
| Email | **sravanthisolar34@gmail.com** | **[LIVE]** — contact page "Email Us" |
| Phone | +91 98667 63371 / +91 95504 68021 | **[LIVE]** contact page |
| Address | H.No. 6-2-333, Near SBI Bank, Subhash Nagar, Nizamabad 503002 | **[LIVE]** contact page |

**Real inconsistency found on the live site:** the structured data (JSON-LD)
declares `contact@sravanthisolar.in` while the contact page a human reads
publishes `sravanthisolar34@gmail.com`. Two different inboxes on one site.
Use the Gmail one for outreach; the mismatch is itself the talking point.

Claims: established 2010 / "16+ years", TGREDCO channel partner, MNRE
certified, 5 years free service & maintenance, 25-year panel warranty. Their
own calculator default shows 2 kW → ₹23,040 annual savings, 2,880 units,
160 sq ft, ₹1,50,000 install, ₹60,000 subsidy, ₹90,000 effective, with
"Taxes + Net-metering Extra".

---

## 4. MVS Solar Solutions — Nizamabad branch / Uppal, Hyderabad HQ

| Field | Value | Source |
|---|---|---|
| Website | https://mvssolarsolutions.com/ | **[LIVE]** fetched |
| Email | naveen@mvssolarsolutions.com | **[LIVE]** + **[SEARCH]** JSON-LD |
| Phone | +91 99665 31819 (Naveen Maggidi) | **[LIVE]** |
| Branch | 11-1-926, New NGOS Colony, Kanteshwar, Nizamabad 503002 | **[SEARCH]** |
| HQ | Plot 115, L N Colony, near Sri Krishna Pharma, Nagole Metro, Uppal, Hyderabad 500039 | **[SEARCH]** |
| TGREDCO | TSRE261006, listed with phone 9966531819 and the same email | **[GOVT]** |

This is the strongest pitch of the five, because the contradictions are on one
page and are unambiguous:

1. **The same page carries two different sets of counters.** Near the top:
   "250+ Projects Completed / 220+ Satisfied Customers / 5+ MW / 7+ Years".
   Lower down: "9+ Projects Completed / 8+ Satisfied Customers / 1+ MW /
   1+ Years in Solar EPC". Both are on the live homepage.
2. **Free vs paid survey.** The badges say "Free Site Survey — No obligation,
   no cost" and "Free On-Site Survey … at zero cost", while step 02 of their
   own "How We Work" says **"Paid Site Survey"**.
3. **"Online Presence Snapshot"** claims 24.8K Facebook, 18.2K Instagram,
   9.6K LinkedIn, 12.4K YouTube, 7.1K X, 4.3K WhatsApp, plus 78,936 website
   visitors, 234,917 page views, 12,083 inquiry clicks and 1,545 contact-form
   leads — with the note that these are "maintained through our internal
   dashboard and database records". Every one of those six social numbers is a
   link to `#`, i.e. no profile is actually linked to back it up.

I did **not** verify the social follower counts, the visitor numbers, or the
project counts. I am reporting that the page asserts them and that the
assertions contradict each other.

---

## 5. Abhi Solar Solutions — Karimnagar

| Field | Value | Source |
|---|---|---|
| Website | https://www.abhisolarsolutions.com/ | **[LIVE]** fetched |
| Email | abhisolorsolutions@gmail.com (note the "solor" spelling) | **[SEARCH]** + **[GOVT]** — identical address on the TGREDCO list |
| Phone | 8977007778 | **[SEARCH]** + **[GOVT]** — same number on the TGREDCO list |
| Address | Road No. 6, Theegalaguttapalli, Karimnagar 505001 | **[SEARCH]** + **[GOVT]** (TGREDCO: H. No. 4-69/46/3/A, Manikeshwari Nagar, Road No.6, Thegalaguttapalli) |
| Contact person | Srinivas Reddy | **[GOVT]** TGREDCO list |

The website fetch and the government list independently agree on phone and
address, which is why this one is safe to use despite the contact-page fetch
failing.

Found on the live homepage, quoted from their own markup:

- The "Our PV Partners" logo row is **hotlinked from third-party sites** —
  citizensolar.com, static.wixstatic.com, mma.prnewswire.com,
  tatapowersolar.com, solarquarter.com, goldisolar.com, upload.wikimedia.org,
  industrialpunch.com, media.licdn.com. Same for the inverter row. If any of
  those hosts changes or blocks hotlinking, the logos break.
- The **"Our Financial Partners"** row is worse: alongside SBI/Union Bank
  logos from 1000logos.net and pinimg.com, it includes
  `deccanchronicle.com/.../6857743-newyearcelebrationsrestrictions1.jpg` (a
  news photo about New Year celebration restrictions) and an
  `img.autocarpro.in` image. Those are not bank logos.
- Hero image is hotlinked from citizensolar.com.
- Footer reads "Copyright © 2024 Brandbez IT Solutions Pvt Ltd" — the agency,
  not Abhi Solar.

Coverage claimed: Karimnagar, Warangal, Jagtial, Siddipet, Mancherial,
Peddapalli.

---

## What I could not do, and what you must do before mailing

1. **No audits exist for these 5.** Run on your machine:
   `python 01-LEADS/run_pipeline.py` (Chrome + Playwright + internet), then
   `python 01-LEADS/verify_report.py --all` must exit 0 before anything is sent.
   Do not reuse an existing PDF for any of these.
2. **No Meta Ad Library probe was run for this batch**, so there is no claim
   here about whether any of the 5 is currently advertising. Earlier batches
   recorded "Active Meta advertiser / No active Meta ads (Ad Library probe
   DATE)" — this batch deliberately records neither.
3. **Confirm Orugallu's email** (orugallusolarenergies@gmail.com) before
   mailing — it is the one address in this batch that I could not read off a
   page I successfully fetched. Their fetched pages publish no email at all.
4. Two fetches failed in this environment (`abhisolarsolutions.com/contact.php`
   and `orugallusolar.com/subsidy/`), and `laxminarayanasolar.in` returned
   **HTTP 500** — which is why Laxmi Narayana Solar (Karimnagar) was *not*
   included despite appearing in search.
