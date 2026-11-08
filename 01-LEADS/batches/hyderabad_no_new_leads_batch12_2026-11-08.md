# Batch 12 — Hyderabad lead discovery, 2026-11-08

**Request:** "Find leads: solar Hyderabad, 5 leads"

**Outcome: 0 new qualifying leads.** This log records what was searched so the
next run does not repeat it, and so the reason for the zero is on file.

---

## Why the pipeline could not be used

`discover_leads.py` needs Playwright + headless Chrome + live outbound TLS.
This sandbox allows TCP connects to external hosts but the TLS handshake is
reset by the egress proxy (`SSLZeroReturnError`), so `requests` cannot reach
facebook.com, validator.w3.org, or any lead site. Playwright is not installed
and could not reach the Ad Library anyway. Discovery was therefore done with
`fetch_page` / `web_search`, which run outside the sandbox.

`/tmp/pdflibs` had also been wiped again; reinstalled with
`pip install --break-system-packages --target /tmp/pdflibs --upgrade pypdf pypdfium2 pillow reportlab requests beautifulsoup4 lxml`
(`pip` fails transiently with `SSL: DECRYPTION_FAILED_OR_BAD_RECORD_MAC` —
retry).

---

## What was searched — Meta Ad Library, `active_status=active&ad_type=all&country=IN`

| Query | Results | Outcome |
|---|---|---|
| `solar hyderabad` | 0 ads | empty |
| `solar energy hyderabad` | 0 ads | empty (known) |
| `solar panel hyderabad` | 0 ads | empty |
| `solar panel secunderabad` | 0 ads | empty (known) |
| `solar for home hyderabad` | 0 ads | empty |
| `solar epc hyderabad` | ~4 | all existing leads |
| `solar installation hyderabad` | ~78 | paged through; all existing leads or wrong business |
| `rooftop solar telangana` | ~53 | paged through; all existing leads or wrong city |
| `solar subsidy telangana` | ~67 | paged through; all existing leads |
| `net metering telangana` | ~11 | existing leads + Meerut |
| `solar warangal` | ~27 | land/plot sellers, not solar EPCs |
| `solar karimnagar` | ~16 | existing leads only |
| `solar nizamabad` | 0 ads | empty |
| `solar water heater hyderabad` | ~2 | Bengaluru company |

Per-advertiser name searches in the Ad Library, all returning **no ads**:
Zyronpro, Unisolar, Harsha Solar, NextGen Solar Power, Satyajan Energy,
Avghni Renewable, SolarCircuit, Creative Energy Solutions, Maa Solar Energy
Solutions, Vihaan Solar.

---

## New live advertisers found — and why each was dropped

Every advertiser in the Hyderabad result sets that was not already a lead was
checked against the two qualification gates (live ads **and** a resolvable
website in the right market).

| Advertiser | Library ID | Started | Why dropped |
|---|---|---|---|
| **99Ad Solutions** running ads for **V1 Solar Solutions** | 1446165934284837, 1571427961334945 | Oct 12 / Nov 4, 2026 | Business is **Bengaluru** — `v1solarsolutions.in`, 7 Srirama Nagar, Magadi Main Rd, Kamakshipalya, Bengaluru 560079, GST 29DPTPK0093G1ZF. The ad says "serving Bengaluru and Hyderabad" but the company, its products (FPC/ETC water heaters, RO, heat pump) and its proprietor Mr. Vijay are Bangalore. Wrong city, and a water-heater service business rather than a rooftop-solar EPC. |
| **Shakti On Roof** (Shakti Energy Solutions Pvt. Ltd.) | 1758170175294711 | Oct 27, 2026 | Subsidiary of **Shakti Pumps (India) Ltd**, headquartered **Greater Noida / Indore** (VMPL). A national module-and-inverter manufacturer, not a Hyderabad EPC. Wrong city. |
| **EcoSoch Pvt Ltd** | 1140479932004790 | Nov 4, 2026 | Ad references **BESCOM** — Bengaluru. Wrong city. |
| **Golden Infra Projects / GRR Properties / Landownershare / SR Infra projects / SR Properties** | various | Nov 2026 | Real-estate plot sellers on Warangal Highway, surfaced by the word "solar" in their amenity lists. Not solar companies. |
| **Shiven Energy and EV Pvt. Ltd.** | 2635628063554886 | Nov 3, 2026 | **Meerut**, Uttar Pradesh. Wrong city. |
| **mr_koti_00** (Instagram) running Garuda Solar Energy Solutions | 2319725685441877 | Sep 4, 2026 | **Guntur**, Andhra Pradesh. Wrong city. |

---

## Conclusion

The Hyderabad / Telangana rooftop-solar Meta advertising market is a **closed
set of roughly 20 advertisers**, and the 46 leads already in `leads.csv`
cover essentially all of them. Batch 11 (2026-11-08) took the last five
advertisers that had both live ads and a resolvable local website: Varna,
Hindusthan, Lumisun, Kypas and Lotus Industries.

Under the standing rule — *a zero-live-ad lead gets no audit PDF and no
outreach, because there is nothing to audit* — none of the 25 companies on the
gosolarindex.in Hyderabad register qualify. Ten of them were checked directly
against the Ad Library and run no Meta ads at all.

**Recommendation:** stop mining Hyderabad. The market is exhausted. Either
(a) move to a new city — the same `discover_leads.py "<vertical> <city>"` flow
works unchanged, and cities with active local solar advertisers but weaker
competition would give better conversion; or (b) re-audit the existing 46,
since ad creative, destinations and site tracking all drift over time and
`verify_live.py` exists precisely to catch that.
