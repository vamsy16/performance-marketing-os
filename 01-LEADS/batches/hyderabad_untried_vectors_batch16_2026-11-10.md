# Batch 16 — Hyderabad, untried vectors (2026-11-10)

## Result

**0 qualifying new leads.** One new live advertiser was found and it fails the
qualification gate. The ask was for 5; the honest answer is 0, with the reason
recorded below.

## Context

Batch 15 closed out tier-2 Telangana. The owner then chose to return to Hyderabad
proper with vectors that had not been tried. This pass used suburb-level and
segment-level keyword angles rather than the city-level and company-name angles
already exhausted in batches 12 and 13.

## Queries run (14, all with `country=IN`, active ads only)

| Query | Results | Outcome |
|---|---|---|
| `solar Kukatpally` | ~3 | Big G Industries only — already a batch-11 no-website drop |
| `solar LB Nagar` | ~6 | SV Projects (HMDA plot seller), Nisha Solar (existing lead) |
| `solar Secunderabad` | ~6 | Valcan Solar (existing lead) |
| `solar inverter Hyderabad` | ~9 | PURE EV (dealership recruitment), Arkahub (existing), Krisol (existing) |
| `solar net metering Hyderabad` | ~13 | Shiven Energy & EV (Meerut, UP), Krisol, Hydromo — all read across 4 chunks |
| `solar panel price Hyderabad` | ~3 | Shiven Energy & EV (Meerut, UP) |
| `సోలార్ హైదరాబాద్` | 0 | Telugu city query, no results |
| `rooftop solar installation Hyderabad` | 0 | No results |
| `solar company Hyderabad` | ~39 | SolarSquare, Krisol, Four Solar, Sri Varahi Real Assets (land) — all 5 chunks read |
| `solar telangana` | ~150 | Eastman, Sri Balaji, Suryon, Orbit, MICROB, SunSolarhyd, Go Rewatt, Hindusthan, Servotech, BoxBee, Alsaa — all 5 chunks read |
| `3kW solar Hyderabad` | ~21 | Orbit, Suryon, Lumisun, SunSolarhyd, Nisha, Krisol, Venus, Manasa — all 4 chunks read |
| `solar for home Hyderabad` | 0 | No results |
| `solar battery Hyderabad` | ~5 | Shiven Energy & EV (Meerut, UP) |
| `solar for business Hyderabad` | 0 | No results |

Two `?id=` confirmations were attempted and **both returned a different
advertiser's card** — `2103721667197349` resolved to Sri Balaji Solar Energies
and `28816825727945655` resolved to Estate Dekho. Both were re-resolved by direct
name search. This is the known Ad Library rendering behaviour, recorded here
because it produced a near-miss on a genuinely new advertiser.

## The one new advertiser, and why it fails

**Manasa Enterprises** — page `ManasaEnterprises` (`61593163442429`).

**Ad Library ID: `826884287112902`, started 22 August 2026.** Resolved by a direct
`Manasa Enterprises Solar` search, which returns exactly one result with the
metadata block and the ad card adjacent in the same chunk. (The ID
`28816825727945655` appeared next to this card in the `3kW solar Hyderabad`
result set, but a direct `?id=` fetch of that ID renders Estate Dekho's villa ad,
so it is not attributed to Manasa.)

**Ad copy, verbatim:**

> ☀️ MANASAA ENTERPRISES — SOLAR MASTER DISTRIBUTOR — Domestic & Commercial Solar
> Systems — 💰 GOVT. SUBSIDY UP TO ₹78,000* — ⚡ Save on Electricity Bills —
> 🌱 Clean & Renewable Energy — SOLAR SYSTEMS: 3 kW – ₹2,05,000*; 5 kW –
> ₹3,10,000*; 10 kW – ₹5,92,000* — Also Available: Solar Pump Sets • Solar Street
> Lights • AC/DC Systems — ✅ Expert Installation ✅ Quality Products ✅
> After-Sales Support — 📞 CALL / WHATSAPP 7901253949 | 8074507650 — 📍 Kakinada |
> Hyderabad — 📧 manasaaenterprises2024@gmail.com

**Why it does not qualify:**

- **No website of its own.** The ad's only destination is
  `api.whatsapp.com/send` — a bare WhatsApp URL with no number appended. A web
  search finds the business only on third-party directories (Justdial, magicpin,
  IndiaMART) under "Manasa Enterprises, Pillar No 67, Mehadipatnam, Hyderabad"
  and as an IndiaMART-listed HJT solar-panel supplier. There is no domain to
  audit, so there is nothing to measure, no pages to review and no audit PDF to
  build.
- **It is a distributor/dealer, not an EPC.** The ad's own headline is "SOLAR
  MASTER DISTRIBUTOR" and the product line is resold panel sets and pump sets.
- **It was already probed and dropped in an earlier batch** as a no-website lead.
  Confirmed rather than re-litigated.

The standing gate is "live Meta ads **plus a resolvable website** plus a
reachable email". This advertiser meets the first and third conditions only. No
audit PDF and no outreach is produced.

## Non-qualifying advertisers seen in these pools

- **Shiven Energy & EV Pvt. Ltd.** (`61584116631098`) — Meerut, Uttar Pradesh.
  Appears in `solar net metering Hyderabad`, `solar panel price Hyderabad` and
  `solar battery Hyderabad` because its service-area list contains "Hyderabad"
  and "Warangal". Its own site footer is Meerut, E/513 Delhi Rd, Madhav Puram,
  Meerut 250002. **Wrong city.**
- **Go Rewatt** (`gorewatt`) — distributor recruitment for a renewable-energy
  manufacturer. Priority markets listed are "Karnataka | Tamil Nadu". Not a
  Telangana EPC.
- **Servotech Renewable Power System Limited** (`servotechofficial`) — national
  manufacturer appointing dealers/distributors in Telangana. Not a local EPC.
- **PURE EV** (`pureenergyindia`) — PuREPower dealership recruitment.
- **SV Projects / Sri Varahi Real Assets / Estate Dekho / 99acres Hyderabad
  Homes** — HMDA plot sellers and villa projects. Not solar businesses; they
  match only because "solar street lighting" or "5 kW solar power" appears in an
  amenity list.
- **BoxBee** (`boxbee.in`) — sells a ₹1,999 solar-panel cleaning brush. Consumer
  product, not an EPC.
- **SunSolarhyd** — batch-11 no-website drop; ad destination is `fb.me`.
- **Big G Industries** — batch-11 no-website drop; ad destination is
  `api.whatsapp.com/send`.
- **Sri Balaji Solar Energies** — existing lead #9, already flagged as needing a
  re-audit rather than a new audit.

## Conclusion

Hyderabad's paid-advertising solar market is fully covered. Across this pass,
14 keyword queries spanning ~250 ad results, the only advertisers running live
Meta ads in this market are already in `leads.csv` or are manufacturers,
recruitment ads, land sellers or consumer products.

The pool of live-ad solar advertisers in Hyderabad and Telangana combined is
small — roughly 15-18 active advertisers — and the repo now holds 52 leads.
Reaching further requires either a different ad platform or a change in the
offer, both of which are the owner's call.

## Gates

No reports were built this pass, so gates 1-3 were not run. Nothing was added to
`leads.csv`, `sequence_manifest.json` or `AUDIT_PDF_INDEX.md`.
