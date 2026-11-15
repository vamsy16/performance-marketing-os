# Batch 21 — Telangana State, second pass (2026-11-15)

## Result

**2 new leads rowed** against an ask for 5. Both clear every standing gate:
live Meta ads verified per-ID, a Telangana city, a published email address,
fresh data. `01-LEADS/leads.csv` 68 → **70 rows**.

| # | Company | City | Website | Email | Verified Library IDs | Started | In-segment ads |
|---|---|---|---|---|---|---|---|
| 1 | **Eagle Solar Systems** | Mallampet/Bachupally/Medchal, Hyderabad | *(none — no own site)* | eaglesolarhyd@gmail.com | 1677382683817329, 1835997698149286 | Nov 7 / Nov 12, 2026 | 2 |
| 2 | **Solar Apex Pvt Ltd** | Manikonda, Hyderabad (Khammam franchise page) | solarapex.in | info@solarapex.in | 1143855195267637, 1667563528489384 | Nov 4, 2026 | 1 of 2 |

Neither is a duplicate: neither name appears in `leads.csv` or
`known_leads_extra.json`. Solar Apex *was* qualified by batch 14 on
2026-11-10 but was one of two leads that batch left unrowed — the row says
so, so it is not discovered twice.

## What was searched — 31 Meta Ad Library sweeps this batch

All `active_status=active`, `country=IN`, every chunk read.

**Product / intent queries:** `solar net metering` (~550), `solar water pump
Telangana` (2), `rooftop solar Khammam` (2), `solar AMC Hyderabad` (3),
`solar company Hyderabad` (~36), `solar EPC Telangana` (**0**), `solar
installation Telangana` (~62), `solar dealer Telangana` (4), `solar Hyderabad
free site visit` (~53), `solar Hyderabad zero down payment` (6), `PM Surya
Ghar Hyderabad` (~24), `solar Hyderabad Telugu subsidy 78000` (**0**),
`solar panels Hyderabad` (re-read), `solar Telangana` (re-read, ~180).

**Telugu queries:** `సోలార్ సబ్సిడీ` (~200), `సోలార్ పానల్` (2),
`సోలార్ హైదరాబాద్ సంస్థాన` (**0**).

**City queries:** `solar panel Karimnagar` (**0**), `solar panel Warangal`
(**0**), plus the four untried cities from batch 20 re-confirmed dead
(Nalgonda, Siddipet, Miryalaguda, Adilabad).

**Firm-name queries:** `Solar Bull Energy` (16 — a Pokémon-card collector),
`Vihaan Solar` (5 — Odisha + a Tamil Nadu plot seller), `Suryodaya Solar`
(**0**), `Sungrace Energy` (**0**), `Sri Sai Solar Systems` (**0**),
`S Cube Energy Infra` (37 — Odisha + PEB structures), `Swadeshi Energy
Solutions solar` (**0**), `RS Solar Systems Hyderabad` (**0**),
`Raio solar` (**0**), `Solak Renewables` (**0**).

**Other channels:** TGREDCO 2026 register re-read (304 suppliers — as a
*new-lead* channel it is exhausted; almost every name is already rowed or
vetoed, and it publishes no email for either of the two strongest
candidates). IndiaMART Hyderabad solar-listing page read for new names.
16 more Google Ads Transparency `?domain=` probes at `region=IN`.

### New advertisers seen and rejected

| Advertiser | Why rejected |
|---|---|
| Rayzon Solar | Gujarat module manufacturer, not Telangana |
| Ray On Solar Systems | Visakhapatnam, Andhra Pradesh — already rowed, and its city field was wrong (see below) |
| Arcedo Systemss / Suryon | Already rowed as Arcedo Systems (same business, info@arcedo.net) |
| Kapil Power & Infra | Already rowed (row 21) |
| Eastman New Energy | Already rowed (row 18) |
| Anudev Agencies & Solar | Jalgaon, Maharashtra |
| TD SOLAR | Kolkata (CESC/WBSEDCL customers, Bengali copy) |
| Ascent Energy | Godhra/Vadodara, Gujarat |
| KWIK M Solar | Varanasi |
| Ziewnic | Lahore, Pakistan |
| Sunbliss Solar And Consultancy | Sells a 29-day solar training course, not installations |
| MYSUN | Uttar Pradesh campaign, national brand |
| SolarSquare Energy | Already rowed (row in leads.csv, national brand) |
| Sri Balaji Solar Energies | Already rowed |
| AB Solar Power Systems | Already rowed and audited (CI 7/100) |
| Sunova Green Energy | Already rowed |
| Lumisun solar | Already rowed |
| Truzon Solar / Suntek | Already rowed |
| Big G Industries | Earthing pit covers, out of segment |
| Servotech Renewable | Dealer/distributor recruitment, out of segment |
| Ice Cube Energy | Jajpur, Odisha |
| BSSM Infra | Pre-engineered buildings, out of segment |
| Vyaktigat Vikas | Hindi computer-books seller — see the third-eye section |
| MRK Associates | Unknown advertiser — see the third-eye section |
| Sahasra Enclave / vjrinfradevelopers | HMDA villa plots mentioning solar, out of segment |

## The two leads in detail

### 1. Eagle Solar Systems

- **Ads (2, both `?id=`-confirmed):** `1677382683817329` (Nov 7, 2026) and
  `1835997698149286` (Nov 12, 2026), page `61595903925834`. Telugu rooftop
  solar, ₹78,000 PM Surya Ghar subsidy, "90% varaku aada", phones
  9000666985 / 9000666984, "హైదరాబాద్ & తెలంగాణ అంతటా సేవలు". CTA is an
  fb.me lead form on both — no ad traffic can reach a website, and the firm
  has none.
- **Email:** `eaglesolarhyd@gmail.com`, published in the Telangana
  government's TGREDCO 2026 empanelled-supplier register, regn. TSRE240360,
  SY.No.142/A/1, Mallampet, Bachupally, Maheshwaram, Medchal, Hyderabad
  500072, mobile 9000666985 — the same number the ads publish.
- **Third-party corroboration:** Justdial lists the same Mallampet/Bachupally
  Eagle Solar Systems as a solar-fence and solar-power-system dealer (21
  years, 09980785458); IndiaMART lists a proprietorship est. 2013, RAMA
  KRISHNAIAH KUMBAM, solar water heaters / fencing / street lights **plus**
  interior designing, false ceiling and modular kitchen, up to 10 employees.
  A small proprietor firm with a wider trade than rooftop solar — recorded,
  not hidden.
- **City guard:** the full register address string resolves to Hyderabad and
  passes. (Bachupally / Mallampet / Medchal are not in `LOCALITIES` on their
  own, so the string only resolves because it also carries "Hyderabad" — the
  same gap noted in batch 20.)

### 2. Solar Apex Pvt Ltd

- **Ads (2, both `?id=`-confirmed):** brand ad `1143855195267637` (Nov 4,
  2026) — "Call Us: 8125640121, 8008576480 / Visit Us: Church Compound
  Center, Khammam / www.solarapex.in", CTA `api.whatsapp.com`. Franchise /
  dealership-recruitment ad `1667563528489384` (Nov 4, 2026), Telugu,
  claiming Khammam dealers earn ₹50,000–₹1 lakh+ a month.
- **Segment call:** the row stands on the brand ad. The recruitment ad is
  recorded and excluded from the audit's ad count, on the same reasoning that
  rejected Servotech and Go Rewatt. Batch 14's third ad
  (`2362213721277291`, a hiring ad on the corporate page
  `facebook.com/61575888183929`) is no longer in the Ad Library.
- **Contacts:** `info@solarapex.in` and +91 96660 05198 from the firm's own
  `/contact/` page, 3rd floor, Kakatiya Marvel, near Lanco Hills Road, Sri
  Laxmi Nagar Colony, Manikonda, Hyderabad 500089. The homepage mailto is
  broken and points at `info@domain.com` — only `/contact/` works.
- **HQ vs branch:** registered in Manikonda, Hyderabad; the advertising page
  is the Khammam outlet (LinkedIn corroborates Mohammed Mubashir as
  Franchise Owner, Khammam District). Both cities are inside Telangana.
- **Reportable defect, still true:** the ad phones (8125640121, 8008576480)
  do not match the website phone (+91 96660 05198).

## Third-eye pass — run after the audit, as required

Every ad ID recorded on a touched row was re-opened on its own with
`?id=<LibraryID>` **after** the gates ran. It caught two real errors.

**1. Two of the three IDs I had attributed to Ray On Solar Systems are
wrong.** The row carried `1107666674962232` as its only live ad; opening it
returns **"Ad isn't in the Ad Library"** and resolves the page to **MRK
Associates**. A second ID, `2401086164116585`, which surfaced next to the
Ray On card in the `సోలార్ పానల్` sweep, resolves to **Vyaktigat Vikas**, a
Hindi computer-books advertiser, and dumps ~230 unrelated ads. Both were
read off search-result lists — the same trap that produced the batch-20
Meissa/Visiontek and Eagle/Solox mix-ups. Only `3529873930505195`
(Sep 18, 2026, "multiple versions") opens as Ray On Solar Systems. The row
is corrected to one verified ID and the two misattributed IDs are written
into it so they are never reused.

**2. Ray On Solar Systems was rowed with city "Hyderabad" while its own site
says Visakhapatnam, Andhra Pradesh.** The row's own snippet already said
"Based in Visakhapatnam … advertising into Telangana", so the city field
contradicted the row. Corrected to
"Visakhapatnam, Andhra Pradesh (advertising into Hyderabad)".

`--audit-state Telangana` therefore moves from 67 inside / 1 outside to
**68 inside / 2 outside / 0 unresolved**. `tests.py`'s
`StateCityGuardTests` was updated to match (42/42 still pass).

## Gates

| Gate | Result |
|---|---|
| `tests.py` | **42 / 42 OK** |
| `tests_sequence.py` | **25 / 25 OK** |
| `verify_report.py --all` | **ALL REPORTS PASS** |
| `verify_report.py --ads-only` | **ALL ADS-ONLY REPORTS PASS** |
| `discover_leads.py --audit-state Telangana` | 68 inside / 2 outside / 0 unresolved |
| `--state Telangana` sweep refusal | still refuses pre-network (unchanged) |

## Why only 2 of the 5 asked for

The published-email gate stopped the other three strongest candidates. Both
run more live ads than either rowed lead:

- **Griffin Energy** — 4 live Meta ads, verified twice (`1159969763254778`
  Nov 4; `1681876623343353`, `2436699883532011`, `2928662904181620` Nov 15,
  2026), page `facebook.com/Griffin.Energy`, page_id 1421460234380992.
  Genuinely strong creative: Magnelis® zinc-aluminium-magnesium steel from
  AM/NS India, Reliance HJT panels, EV-charging economics (₹2.90/km public vs
  ~29 paise rooftop), the PM Surya Ghar ₹78,000 deadline of 31 Mar 2027, free
  roof survey anywhere in Hyderabad, written quote in 24 hours. **No website
  and no email** — 4 web searches, 20 Google Ads Transparency `?domain=`
  probes and 4 city Meta sweeps returned only namesakes (Yemen, UK, Texas,
  Australia).
- **Surya Shakti Solar Energy** — 2 live Meta ads (`1692983389068776`,
  `1856029798723640`, both Nov 14, 2026), page `61592455701220`,
  on-grid/off-grid/hybrid, water pumps and heaters, "Hyderabad, Telangana".
  **No website and no email** — the IndiaMART listing
  `indiamart.com/company/273630670/` publishes GST 36BKKPA8706N1ZS and CEO
  A Madhavi but no email, the firm is absent from the TGREDCO register, and
  web search returns only namesakes (Faridabad, Kathua J&K, Rajasthan).
- **Valcan Solar** — 2 live ads, but already a batch-18 row. Duplicate.

Both rejects are recorded in `known_leads_extra.json` under `vetted` with
gate `published-email`, so they expire rather than blocking forever — if
either publishes an email it becomes eligible again without being re-hunted
by hand.

The owner should decide whether the published-email gate is absolute. If it
is, Telangana is close to exhausted: 31 sweeps, the full TGREDCO register,
20+ Google Transparency probes and the IndiaMART listings have all been read,
and the two firms left that clear the live-ads bar publish no email.

## Files touched

- `01-LEADS/leads.csv` — 68 → 70 rows; Ray On city + snippet corrected
- `01-LEADS/known_leads_extra.json` — Eagle + Solar Apex to `known`;
  Griffin Energy + Surya Shakti to `vetted` (gate `published-email`)
- `01-LEADS/tests.py` — `StateCityGuardTests` now expects 2 outside Telangana
- `01-LEADS/add_telangana_leads_20261115.py` — new, rows + registry
- `01-LEADS/fix_rayon_after_third_eye.py` — new, Ray On correction
- `01-LEADS/refine_new_telangana_rows.py` — new, batch-14 history + confirmed
  WhatsApp destination
- `01-LEADS/batches/telangana_state_2_leads_batch21_2026-11-15.md` — this log

## Honesty statement

Every ad ID, phone number, email address, address and date above was read
live from the Meta Ad Library, the firms' own sites, the TGREDCO register PDF
or web search on 2026-11-15. No score, pixel count, PageSpeed number or
Google Transparency figure is recorded for the two new leads, because no
site audit has been run on either — Eagle has no website to audit, and Solar
Apex has not been audited yet. Those values will appear only as measured
values, or as an explicit "not checked in this pass".

Nothing has been sent to anyone.
