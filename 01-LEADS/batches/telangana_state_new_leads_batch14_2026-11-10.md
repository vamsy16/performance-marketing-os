# Batch 14 — Telangana State (beyond Hyderabad) solar lead discovery (2026-11-10)

## Result

**5 qualifying leads found** — every one runs live Meta ads, has a live
resolvable website and a published email address. The ask was for 5.

| # | Company | City | Website | Email | Confirmed Library IDs | Started |
|---|---|---|---|---|---|---|
| 1 | **Laxmi Narayana Enterprises** (FB: Laxminarayanasolarsolutions) | Karimnagar | laxminarayanasolar.in | laxminarayanaenterprisess@gmail.com | 1180974161286784, 1815605862989998 | Nov 6, 2026 |
| 2 | **Solar Apex Pvt Ltd** (FB: Solar Apex Khammam) | Khammam | solarapex.in | info@solarapex.in | 1143855195267637 | Nov 4, 2026 |
| 3 | **GLO LED Private Limited** (FB: GloledKhammam) | Khammam | gloled.co | info.gloled@gmail.com / orders@gloled.co | 2177815426280429 | Oct 29, 2026 |
| 4 | **UDK Electrical Industries Pvt Ltd** (IG: udk_industries) | Sangareddy | udkindustries.com | contact@udkindustries.com / sales@udkindustries.com | 877640172078183 | Nov 9, 2026 |
| 5 | **MICROB Energies** (IG: microb_energies) | Hyderabad (installs across Telangana) | microbenergies.com | Info@microbenergies.com | 2147291065897730, 1867351030942485 | Nov 5 / Nov 6, 2026 |

**Attribution rule applied to every row.** Ad Library metadata sits *above* its
ad card, and a chunk boundary can split the two. Only IDs whose metadata and card
are adjacent **in the same chunk** were treated as candidates; every candidate was
then resolved with a direct `?id=<LibraryID>` fetch and the page name read off the
page. Confirmation status per lead is recorded in the table below so the
third-eye check can see exactly how strong each attribution is.

### Attribution strength (third-eye view)

| Lead | `?id=` confirmation | Page name read off page | Destination |
|---|---|---|---|
| Laxmi Narayana Enterprises | **CONFIRMED — ad card rendered** on both IDs | Laxminarayanasolarsolutions (61583798920523) | `fb.me` (off-site) on both |
| Solar Apex | **Page resolved** to Solar Apex Khammam (61596329420215); **ad card did not render** on two attempts | Solar Apex Khammam | **UNCONFIRMED — WhatsApp (`api.whatsapp.com`) per the search card** |
| GLO LED | **CONFIRMED — ad card rendered** | GloledKhammam (61574417949137) | `https://gloled.co/` |
| UDK Electrical Industries | **Page resolved** to udk_industries (1156566704214778); **ad card did not render** on two attempts | udk_industries (Instagram) | **UNCONFIRMED — `api.whatsapp.com` per the search card** |
| MICROB Energies | **CONFIRMED — ad card rendered** on both IDs | microb_energies (803439429518905) | `instagram.com/microb_energies` |

**Two of the five (Solar Apex, UDK) have an unconfirmed ad destination.** Their
page attribution is solid but the click-through target is not verified. Do not
state a destination for these two in any audit or email until it is confirmed.

## What was searched

**Ad Library keyword queries (all `active_status=active`, `country=IN`):**

| Query | Result |
|---|---|
| solar Warangal | ~29 results — Lumisun, Krisol, Sri Balaji-Rajahmundry, Solar Apex, Gloled; **no new local EPC** |
| solar Karimnagar | ~16 results — Laxmi Narayana Solar, Krisol, Lumisun, Solar Apex |
| solar Khammam | ~7 results — Solar Apex, Gloled |
| solar Nizamabad | **0 ads** |
| solar Mahbubnagar | **0 ads** |
| solar Nalgonda | **0 ads** |
| solar Miryalaguda | **0 ads** |
| solar Suryapet | ~3 results — Lumisun only |
| solar Sangareddy | ~11 results — land sellers + UDK |
| solar Siddipet | ~2 results — microb_energies |
| solar Adilabad | ~3 results — Sri Narayana Enterprise Solar Energies (= Sri Balaji) |
| solar Kamareddy | ~1 result — Solar Apex **hiring** ad |
| solar Bodhan | **0 ads** |
| solar Ramagundam | **0 ads** |
| solar Huzurabad | **0 ads** |
| solar Sircilla | **0 ads** |
| solar Kothagudem | **0 ads** |
| solar Jangaon | ~14 results — land sellers |
| solar Mancherial | **0 ads** |
| solar Zaheerabad | **0 ads** |
| solar Bhongir | **0 ads** |
| solar Gadwal | **0 ads** |
| solar Korutla | **0 ads** |
| solar Metpally | **0 ads** |
| solar Vikarabad | ~2 results — land sellers |

**Company-name queries against the TGREDCO register (all zero ads — do not
retry):** Seven Star Solar Suryapet, Ravindranath Solar Warangal, Kakatiya
Energies Hanamkonda, Solar Guru Khammam, Sravanthi Solar, Solar Universe
Khammam, Joshii Solar Warangal, Avanthika Solar, Evergreen Energies Khammam,
Green Solar Hasanparthy.

**TGREDCO empanelled-supplier register 2026** —
`tgredco.telangana.gov.in/Updates_2026/List_of_Empanelled_Suppliers_2026.pdf`,
all 8 chunks read. This remains the highest-yield source and the independent
third-party confirmation for the third-eye check. Non-Hyderabad EPCs it lists
that were probed for live ads are in the zero-ads list above; the two that
turned out to already be leads are **Arka Solar Power (TSRE240412)** and
**Varahi Energies (TSRE240436)**.

## The five leads in detail

### 1. Laxmi Narayana Enterprises — Karimnagar

- Website `https://laxminarayanasolar.in/` — live. Positions as "Solar Panel
  Installation in Karimnagar", on-grid and off-grid rooftop solar for
  residential and industrial customers across Telangana.
- **Address:** #8-4-527/2, Ganeshnagar, Karimnagar 505001, Telangana.
- **Email:** laxminarayanaenterprisess@gmail.com
- **Phones on website:** +91 94930 83284, +91 97037 72963
- **Hours:** Mon–Fri 8:00 AM – 6:00 PM, Sat 9:00 AM – 5:00 PM
- **Claims on site:** 500+ customers, $2M+ savings, 25-year warranty.
- **TGREDCO:** "M/s. Laxmi Narayana Enterprises TSRE250724" appears in the
  2025 register — the independent third-party confirmation.
- **Ads (both `?id=`-confirmed):**
  - `1180974161286784` (Nov 6, 2026) — Telugu. "కరీంనగర్ ప్రజలకు శుభవార్త!
    ₹78,000 వరకు సోలార్ సబ్సిడీ…" Destination `fb.me`.
  - `1815605862989998` (Nov 6, 2026) — English. "Switch to Solar Energy with
    Laxmi Narayana Enterprises! … 25–30 Years Warranty … Rice Mills"
    Destination `fb.me`.
- **Reportable defect:** the phone numbers in the ads (9493093728, 8712780023)
  do **not** match the website phones (+91 94930 83284, +91 97037 72963).

### 2. Solar Apex Pvt Ltd — Khammam

- Website `https://solarapex.in/` — live. Solar Apex Pvt Ltd.
- **Address:** 3rd floor, Kakatiya Marvel, near Lanco Hills Road, Sri Laxmi
  Nagar Colony, Manikonda, Hyderabad, Telangana 500089.
- **Email:** info@solarapex.in
- **Phone on website:** +91 9666005198
- **Hours:** Mon–Sat 10:00 AM – 7:00 PM
- **Ads:**
  - `1143855195267637` (Nov 4, 2026) — page-confirmed to Solar Apex Khammam
    (61596329420215). Copy: "Call Us: 8125640121, 8008576480 / Visit Us: Church
    Compound Center, Khammam / www.solarapex.in". **Destination unconfirmed**
    (WhatsApp per the search card).
  - `2362213721277291` (Nov 9, 2026) — "Hiring Sales Officer for Warangal,
    Karimnagar and Kamareddy". **DROP — hiring ad, not a solar service ad.**
- **CAUTION — HQ vs branch.** The registered address is Manikonda,
  **Hyderabad**, not Khammam. The Khammam ad is a **branch/franchise ad** for
  the Khammam outlet. This is a material difference from the other four leads
  and must be stated plainly in any audit and any email. The audit is of
  `solarapex.in`, which is the Hyderabad corporate site.
- **Reportable defect:** the ad phones (8125640121, 8008576480) do **not**
  match the website phone (+91 9666005198).

### 3. GLO LED Private Limited — Khammam

- Website `https://gloled.co/` — live. Manufacturer and supplier of LED
  lighting with a **solar street light** product line.
- **Khammam outlet:** 11-10-268/6/A/1, near New RTC Bus Stand, Raparthi Nagar,
  Khammam, Telangana 507001 — Cell +91 7075216439
- **Corporate:** 5-5-35/121, Prashanti Nagar, IDA Kukatpally, Hyderabad 500072
  (also listed as #1A & 1B, TSIIC, Prasanthi Nagar, IE Kukatpally, Hyderabad).
- **Emails:** info.gloled@gmail.com, orders@gloled.co
- **Phones:** +91 83408 92683, +91 9553550700
- **Ad (`?id=`-confirmed):** `2177815426280429` (Oct 29, 2026), page
  GloledKhammam (61574417949137). Copy: "☀️ Need Solar Street Lights in Bulk in
  Khammam? GLOLED Solar Street Lights are suitable for contractors, builders,
  layouts, industries, institutions and large project requirements. ✅ Bulk
  Orders Welcome ✅ Multiple Wattages Available … 📞 Call / WhatsApp: 70365
  33794". **Destination `https://gloled.co/` — confirmed.**
- **SEGMENT NOTE — read before pitching.** GLO LED sells **bulk solar street
  lights as a B2B product** (contractors, builders, layouts, industries,
  municipalities). It is **not a rooftop EPC**. It qualifies under the standing
  gate (live ad + live website + email) but it is a different business model
  from the other 49 leads. Pitch it accordingly.

### 4. UDK Electrical Industries Pvt Ltd — Sangareddy

- Website `https://udkindustries.com/` — live. "LED lights manufacturer
  specializing in street lights, **solar lighting**, flood lights, industrial
  lights and poles."
- **Address:** 9-170002, Vidya Nagar Colony Road 3, Sangareddy,
  Telangana 502001.
- **Emails:** contact@udkindustries.com, sales@udkindustries.com
  (also hr@udkindustries.com for careers)
- **Phones:** 08455-456614 (landline), 9704317436, 8309767244, 9505186524
- **Hours:** 9:00 AM – 6:00 PM (Mon–Fri)
- **Ad:** `877640172078183` (Nov 9, 2026, 17 hrs active), page resolved to
  udk_industries (1156566704214778). Copy: "💡 LED Street Light Manufacturer in
  Telangana | UDK Electrical Industries Pvt. Ltd. … BIS Approved LED Street
  Lights … 📍 Manufacturer: Sangareddy, Telangana 📞 Contact: 08455546614 🌐
  www.udkindustries.com". **Destination unconfirmed** (WhatsApp per the search
  card).
- **SEGMENT NOTE — read before pitching.** UDK is an **LED/solar street-light
  manufacturer** (BIS-approved, OEM/ODL, bulk orders), not a rooftop EPC.
  Qualifies under the standing gate; different business model.

### 5. MICROB Energies — Hyderabad, installing across Telangana

- Website `https://www.microbenergies.com/` — live. Solar water pumps, solar
  pump controllers / VFD drives. "Get high-quality solar pumps in Hyderabad,
  Telangana… perfect for agricultural, industrial, and residential use."
- **Email:** Info@microbenergies.com
- **Phone:** +91 9492027647
- **Ads (both `?id=`-confirmed):**
  - `2147291065897730` (Nov 5, 2026) — "300 FT DEEP. 5 HP POWER. BUILT FOR
    PERFORMANCE. Another successful installation at Siddipet, Telangana! …
    5HP Solar Water Pumping System … 300 feet". Destination
    `instagram.com/microb_energies`.
  - `1867351030942485` (Nov 6, 2026) — "No need to spend money on a new motor!
    You can run the motor you already have on your farm with solar … 5-Year
    Warranty … Complete Setup & Support: Full installation across Telangana".
    Destination `instagram.com/microb_energies`.
- **SEGMENT NOTE — read before pitching.** MICROB sells **solar water pumps and
  pump controllers to farmers** (agri segment), not rooftop solar. Qualifies
  under the standing gate; different business model. The ad destination is
  Instagram, not the website — the website was found by search, not by
  following the ad.

## Drops and do-not-retry

- **Sri Narayana Enterprise Solar Energies** (Adilabad, `1112101324532591`,
  Oct 21, 2026) — **same company as existing lead #9 Sri Balaji Solar
  Energies.** Its ads point at `www.sribalajisolarenergies.com`. It is the
  Adilabad branch/entity of a lead already in `leads.csv`. **Do not add as a
  separate lead**; instead re-audit Sri Balaji, which is already flagged stale.
- **Solar Apex hiring ad** `2362213721277291` — hiring, not a service ad.
- **Land sellers** that matched "solar + city" because their plot amenities
  mention solar street lights: Alsaa D Global Real Estate (Sangareddy),
  vjrinfradevelopers (Sangareddy), GRR Properties (Jangaon), RICH Earth
  promoter and Developer (Vikarabad).
- **Zero-ad tier-2 TGREDCO EPCs** — full list in "What was searched" above.
- **Zero-ad city queries** — Nizamabad, Mahbubnagar, Nalgonda, Miryalaguda,
  Bodhan, Ramagundam, Huzurabad, Sircilla, Kothagudem, Mancherial, Zaheerabad,
  Bhongir, Gadwal, Korutla, Metpally.

## Already-existing leads re-confirmed by this run (do NOT duplicate)

Arka Solar Power (TSRE240412, batch 13), Varahi Energies (TSRE240436), Sri
Balaji Solar Energies (TSRE180085, Hanumakonda), Aditi Solar (TSRE180005),
Four Solar (TSRE180027), Freyr Energy (TSRE180165), Kapil Power (TSRE180166),
Kypas (TSRE240334), Punarvi (TSRE240335), Solox (TSRE240461), 3S Solutions
(TSRE240328), Green Carbon Hub (TSRE240393), Ksquare Energy (TSRE230309,
Ahmedabad), Wisda (TSRE240457), AB Solar (TSRE220261), Junna (TSRE180043),
Truzon/Suntek (TSRE180096), Greentek (TSRE180039), Amplus (TSRE180177).

## Gates — status

| Gate | Result |
|---|---|
| Gate 1 — `verify_report.py` | **NOT YET RUN** — no new reports built this batch |
| Gate 2 — report-reviewer | **NOT YET RUN** — no new reports built this batch |
| Gate 3 — `verify_live.py` | **BLOCKED** — sandbox has no outbound TLS. Owner must run `verify_live.py` (no `--offline`) before any email goes out. |

## Honesty statement

Everything above was read live from the Meta Ad Library and from the TGREDCO
register on 2026-11-10. No scores, pixel counts, PageSpeed numbers or Google
Transparency figures are recorded here, because none have been measured yet —
those only appear once the site audit runs, and only as measured values or as
explicit `not available` / `pending`.

**Three of the five leads (GLO LED, UDK, MICROB) are not rooftop EPCs.** They
are a solar street-light supplier, an LED/solar street-light manufacturer and a
solar water-pump company. They pass the standing qualification gate but they are
a different segment from the previous 49 leads, and the owner should know that
before any of them is pitched.

## Audits built (2026-11-10) — 3 reports, all gates pass

Single source of truth: **`01-LEADS/build_batch14_ksquare.py`**. Re-run it, never
re-fetch.

| Company | City | Score | Issues | Wins | Controls | Pages |
|---|---|---|---|---|---|---|
| GLO LED Private Limited | Khammam | **15/100** | 8 | 2 | 2P/4F/9U | 5 |
| UDK Electrical Industries Private Limited | Sangareddy | **10/100** | 7 | 6 | 2P/5F/8U | 5 |
| Microb Energies | Hyderabad | **10/100** | 7 | 5 | 3P/4F/8U | 5 |

### Gate results

| Gate | Command | Result |
|---|---|---|
| Gate 1 | `verify_report.py --ads-only` | **PASS — 46/46** |
| Gate 2 | report-reviewer (run manually against the three new JSONs + PDFs) | **PASS — no defects** |
| Gate 3 | `verify_live.py --offline` | **MATCH 46/46, DRIFT 0** |

Gate 3 must still be re-run by the owner **without** `--offline` before any
email goes out — this sandbox has no outbound TLS.

### What was actually measured, per lead

**GLO LED Private Limited — gloled.co**
- `<head>` fully read (source lines 521-583). **Zero of the 8 tracking tools.**
  The only analytics script is a cookieless Cloudflare Web Analytics beacon
  (`static.cloudflareinsights.com/beacon.min.js`, token
  `7dccf4e368ce442cb6b0b89e5875a997`) — it counts pageviews but cannot retarget
  anyone or record a conversion.
- **No `<title>` element on the homepage at all** — the W3C checker reports
  "Element head is missing a required instance of child element title".
- 4 HTML errors, 5 warnings, 0 info: no doctype before the start tag; two CSS
  negative padding values (-4em, -2px); the missing title.
- WordPress + Elementor + Max Mega Menu + Popup Maker + MyStickyWelcomeBar +
  10Web Speed Optimizer + Font Awesome 5.
- Conversion strength: Zoho Forms contact form (Name, Sales Rep Name, Mobile,
  Email, My Requirements, CAPTCHA), click-to-call on every number, 5 CTAs,
  popup capture, Google Maps directions links for the corporate office, the
  factory, the SMT unit, the Singapore office and all 14 outlets.
- No prices published anywhere.

**UDK Electrical Industries Private Limited — udkindustries.com**
- `<head>` fully read (source lines 79-340). **Google tag GT-W6XX8MT via Site
  Kit by Google 1.191.0 is the only tracking present** — 7 of 8 tools missing.
- WordPress 7.1.4 on GoDaddy managed WordPress, Zakra theme 4.3.3, WooCommerce
  11.2.2, Elementor + Essential Addons 6.8.8, Yoast SEO, Everest Forms,
  Magical Products Display 2.1.3, Animated Floating Chat Button 1.0.3, WP
  Google Places Review Slider 18.11.
- **`/contact/` is still the Zakra theme's demo content** — address "Moon
  Street , 446 Jupiter, JP 44600", emails "zakra@demos.com" and
  "first.last@demos.com", phones "+(123) 456-7890" and "+977 123-456789",
  lorem-ipsum body copy. The real Sangareddy address and 08455-456614 are
  nowhere on it.
- A hard-coded Google Maps API key is exposed in the `/contact/` source
  (`AIzaSyCmL18misQw9KdwqGaw3zHkitj8vG6QF2Y`).
- A second JSON-LD Organization block has `"url": "https://yourwebsite.com"`.
- 7 HTML errors, 0 warnings, 72 info, including a second `<head>` start tag
  with a `<title>` inside it, a `meta` between head and body, and an illegal
  `|` in the Google Fonts query string.
- Google review slider: 4.8 from 63 reviews (place ID
  ChIJGYW_eKj5yzsRkCDf_ODm78s).
- The homepage's "South India's No.1 LED Lights Manufacturer" is unverifiable.

**Microb Energies — microbenergies.com**
- `<head>` fully read (source lines 124-154). **Google tag GT-PZX459FK via Site
  Kit by Google is the only tracking present** — 7 of 8 tools missing.
- WordPress with the 'homefort' theme 1.1.4, Elementor 4.3.6 + Pro, Royal
  Elementor Addons 1.7.1070, Slider Revolution 6.7.40, WooCommerce 10.6.2,
  Contact Form 7 6.1.5, LT Core / LT Ext, Hostinger Reach, The Events Calendar
  6.18.3, Trustindex, Tawk.to.
- **WARRANTY CONTRADICTION** — the live ad says "5-Year Warranty" and the
  homepage says "5 Years Product Warranty", but the FAQ on `/contacts/` says
  "We offer 12-24 months warranty depending on the model", and separately gives
  the controller's *lifespan* as "5 years or more".
- Three homepage links point at the wrong pages: `/services/heat-pump/`,
  `/services/projecting-4/`, `/services/diagnostic-and-repair/`.
- The rooftop-solar block reuses the agricultural copy verbatim.
- The contact form has no email field. The testimonials heading reads "Cilent
  Testimonials".
- 21 HTML errors, 81 warnings, 104 info, including five heading-level skips and
  more than one h1.

### Bugs found and fixed in `audit_pdf.py` while building these

1. **`verification_log()` told a false story.** It chose its "why the tracking
   tags are unknown" sentence from the *length* of the `html_errors` string.
   Any site whose error text ran past 90 characters got the Arka boilerplate —
   "the W3C checker returned an IO error and a direct fetch returned HTTP 500"
   — which is simply untrue for GLO LED and MICROB, both of which were read in
   full. Replaced with an explicit `head_unread` flag so the three genuinely
   different situations are told apart by fact, not by string length.
2. **`next_steps()` could print the same step twice.** The dedupe ran, then a
   trailing `while len(steps) < 4` re-appended the "Book a 10-minute call"
   filler without checking whether that title was already used, so GLO LED's
   action plan told the reader to book the same call twice. The top-up now
   tracks the titles it has already used.

### Defects found and fixed in the new build script

1. The UDK `destination` string (a 200-character explanation) was interpolated
   verbatim into `next_steps()` step 1, where it read as gibberish
   mid-sentence. Shortened on the ad card; the full explanation lives in the
   promise-gap table.
2. The PDF filename is derived from the company's *legal* name while the JSON
   filename is derived from the lead key, so
   `audit_UDK_Electrical_Industries_Private_Limited.pdf` and
   `audit_Microb_Energies.pdf` had no matching JSON stem. This silently dropped
   the score and audit date from `AUDIT_PDF_INDEX.md` for both. Fixed in
   `02-OUTREACH/build_audit_pdf_index.py` with a normalised company-name
   fallback, and verified across all 46 ads-only PDFs with zero mismatches.

### Files touched

- `01-LEADS/build_batch14_ksquare.py` — new, single source of truth
- `01-LEADS/ads_only_results/audit_GLO_LED_Private_Limited.json` — new
- `01-LEADS/ads_only_results/audit_UDK_Electrical_Industries.json` — new
- `01-LEADS/ads_only_results/audit_MICROB_Energies.json` — new
- `02-OUTREACH/ads_only_pdfs/audit_GLO_LED_Private_Limited.pdf` — new
- `02-OUTREACH/ads_only_pdfs/audit_UDK_Electrical_Industries_Private_Limited.pdf` — new
- `02-OUTREACH/ads_only_pdfs/audit_Microb_Energies.pdf` — new
- `01-LEADS/audit_pdf.py` — the two bug fixes above
- `01-LEADS/leads.csv` — 49 → 52 rows
- `02-OUTREACH/generated_emails/sequence_manifest.json` — 49 → 52 sequences,
  each with a step-0 email written, then marked `draft` once the Gmail drafts
  were created and confirmed
- `02-OUTREACH/AUDIT_PDF_INDEX.md` — regenerated: 55 PDFs / 52 companies /
  23 scored
- `02-OUTREACH/build_audit_pdf_index.py` — new index generator


### Outreach — 3 step-0 drafts created 2026-11-10 (owner sends all three)

Gmail connector tools were re-loaded with `list_connector_tools` in the same
turn before use. **Replies were checked first** — `from:gloled.co`,
`from:udkindustries.com` and `from:microbenergies.com` each returned zero
messages with `search_scope.complete: true`, and `list_drafts` confirmed no
draft already existed for any of the three. From address
`smartpursuit3@gmail.com` (primary, verified).

| Lead | To | Draft ID | Thread ID | Attachment |
|---|---|---|---|---|
| GLO LED Private Limited | care@gloled.co | `r170216386970583953` | `1a1c37a6f9f49ada` | audit_GLO_LED_Private_Limited.pdf (24,888 B) — **confirmed attached** |
| UDK Electrical Industries | contact@udkindustries.com | `r-1697390660388353256` | `1a1c37a6d29317b8` | audit_UDK_Electrical_Industries_Private_Limited.pdf (25,126 B) |
| MICROB Energies | Info@microbenergies.com | `r-5384001971505321700` | `1a1c37a6f32d43a1` | audit_Microb_Energies.pdf (25,288 B) |

`create_draft` returns out of order and echoes back neither subject nor
recipient, so **every draft was read back with `get_draft`** and matched to its
lead by To + Subject before `sequence.py mark-draft` was run. The GLO LED draft
was additionally read at `format: "full"` to confirm the PDF part — MIME part 1
is `application/pdf`, filename `audit_GLO_LED_Private_Limited.pdf`, 24,888
bytes, `Content-Disposition: attachment`.

`mark-draft` run for all three. `tests_sequence.py` 17/17. Manifest now
**52 sequences / 199 steps — 90 sent / 34 draft / 75 pending**. Follow-ups
(steps 1–3) are all `pending`, none pre-created.

**Nothing has been sent.** All three drafts are unsent and the owner sends or
schedules them.

One thing to be aware of when scheduling: `sequence.py due` still lists
**Valcan Solar step 1** (`r-4135467498809954457`). That draft is in the trash
and the owner has said to leave it alone, so it has not been touched.
