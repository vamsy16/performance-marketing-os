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
