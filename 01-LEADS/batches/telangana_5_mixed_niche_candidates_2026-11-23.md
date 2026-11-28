# Telangana — five mixed-niche candidates (internal only)

**Status: shortlist, not audit-ready or outreach-approved.** The user broadened the last three beyond solar. Five candidates are listed below, including the two solar candidates previously found. The direct ad cards each displayed `Active` when fetched, and each business website was readable through the page-fetch tool. Ad status can change; do not treat this note as a permanent claim of live advertising.

**Date/source caution:** the session date is 2026-11-23, but the sandbox clock returned 2026-11-28 and some fetched search results contain ads starting after 23 November. Treat the active statuses as what the remote tool displayed, not proven as-of-23-November evidence; recheck the ads and website on a trusted current-date connection before acting.

**No client audits or third-eye checks have been completed.** The independent report-reviewer and live-data-auditor gates are still required, in addition to the automated report verifier. The sandbox cannot reach lead websites and Meta from the audit scripts. A nonzero or unreachable live verification is not a pass. Do not send or create client-facing outreach from this note. Phone numbers and emails are published contacts, not tested for deliverability; forms have not been submitted. The notes below do not claim or assess actual lead generation, conversion, ad spend, tracking, creative quality, or return on investment.

## 1. SunSolar Power Systems / SunSolarhyd — solar, Hyderabad

- Website: https://www.sunsolar.info/ — rooftop solar systems for homes and businesses, Narsingi, Hyderabad.
- Contact on website: sales@sunsolar.info; +91 9866602001 and +91 9959996002.
- [Direct Meta ad 2576227376137902](https://www.facebook.com/ads/library/?id=2576227376137902): displayed Active, start Oct 22, 2026. Advertiser SunSolarhyd; text names SunSolar Power Systems and the same address and main number as the website. The visible card displays fb.me; final destination not verified.
- Prior discovery: earlier batch rejected a different domain, `sunsolarhyd.com`, as unreachable. The newly observed `sunsolar.info` site matches the ad by address and phone; do not claim the old domain works.
- Gmail `in:anywhere` query for the company name, handles, both domains, main email and both phone numbers returned zero; complete for the searched identifiers. No same-company audit JSON, PDF or manifest entry found in previous check. New aliases may still exist.

## 2. PNR Sunrise Energies Pvt Ltd — solar, Hyderabad

- Website: https://sunriseenergies.in/ — solar EPC and related services; website describes activity in Telangana and Andhra Pradesh.
- Contact displayed: +91 6304587145; no business email located on the fetched home page.
- [Direct Meta ad 28807326382303186](https://www.facebook.com/ads/library/?id=28807326382303186): displayed Active, start Nov 12, 2026; identifies the same company, domain and phone, and says Hyderabad. It is a **channel-partner recruitment** ad, not evidence of consumer lead campaigns; card displays WhatsApp and final destination has not been tested.
- Repo text/filename search for name, domain and phone found no prior audit; Gmail `in:anywhere` search for those identifiers returned zero, complete for that query. Matching Gmail drafts search returned zero. Unknown aliases remain possible.

## 3. D'LIFE Home Interiors — interior design, Hyderabad

- Website: https://dlifeinteriors.com/location/hyderabad/ — describes interior design and experience centres in Banjara Hills and Kompally.
- Contact from website: enquiry@dlifeinteriors.com; Banjara Hills +91 9495087777. Its Banjara Hills page displays conflicting postcodes in its text and embedded map; do not use a postcode without confirmation.
- [Direct Meta ad 1024820157266461](https://www.facebook.com/ads/library/?id=1024820157266461): displayed Active, start Aug 19, 2026. The ad names D'LIFE Interiors, describes a Hyderabad project, and prints `dlifeinteriors.com`, the same email and phone. Its CTA is Send message; final destination has not been tested.
- No matching company/domain in leads.csv, manifest or audit JSON company/legal/website fields; no matching audit PDF filename found. Gmail `in:anywhere` search of domain, company names and phone returned zero, complete for that query; matching draft search returned zero. Search does not prove no mail under other aliases.

## 4. Dr. Sridhar International Dental Hospital / Dr. Sridhar Foundation — dental, Hyderabad

- Website: https://sridhardental.com/contact — lists branches in KPHB, Ameerpet and Nallagandla, Hyderabad, and Vijayawada. KPHB contact: jntu@sridhardental.com, +91 8121222888. These are branch contacts, not verified decision-maker details.
- [Direct Meta ad 1672235477851281](https://www.facebook.com/ads/library/?id=1672235477851281): displayed Active, start Oct 20, 2026. Advertiser is Dr. Sridhar Foundation; copy names Dr Sridhar Dental and Hyderabad KPHB/Nallagandla, and its displayed CTA links directly to `https://sridhardental.com/services`. On the website the same branches are listed. The copy also mentions Vijayawada; do not describe the business as Telangana-only.
- No matching company/domain in leads.csv, manifest or audit JSON company/legal/website fields; no matching audit PDF filename found. Gmail `in:anywhere` searches of company, domain, phones, all three listed Hyderabad branch emails and the Vijayawada Gmail address returned zero, complete for those searches; matching draft search returned zero. Other aliases may exist.

## 5. Galaxy Dental Care — dental, Hyderabad

- Website: https://galaxydentalcare.in/contact-us/ — lists the Hyderabad branches named on the ad, including Kondapur, Banjara Hills, Kukatpally and Nallagandla.
- Contact on website: contact@galaxydentalcare.in; +91 8686676781 and +91 8686616148.
- [Direct Meta ad 966436166129348](https://www.facebook.com/ads/library/?id=966436166129348): displayed Active, start May 19, 2026, from page `Galaxydentalcare`. Ad name and nine named branches match the website. A search result for that specific Facebook page also identifies the same website and main phone, but direct Facebook page fetch returned 403; this extra page association is search-result evidence, not a directly verified Facebook profile. Ad card shows WhatsApp, not a verified website click destination.
- No matching company/domain in leads.csv, manifest or audit JSON company/legal/website fields; no matching audit PDF filename found. Gmail `in:anywhere` searches for name, domain, listed numbers, an alternate domain and a public Facebook-page email returned zero, complete for those queries; matching draft search returned zero. Unknown aliases remain possible.
- The Banjara Hills branch page gives conflicting postcodes for the same address (500034 in its main text and 500028 in its branch list); do not use either without confirming.

## Additional repository check

A case-insensitive search of text under `01-LEADS` and `02-OUTREACH` for candidate names, domains and known alternate Galaxy identifiers found only earlier SunSolar discovery/exclusion notes (and an unrelated Hysun substring match). The initial attempt to scan PDFs with `pdftotext` was invalid because that program was not installed. A subsequent `pypdf` extraction successfully read 55 existing PDFs in those directories and found no candidate-name/domain matches; none had wholly empty extracted text or extraction errors. Individual image-only pages and unsearched aliases could still hide prior work; this is not a guarantee of uniqueness.

An owner-only [preliminary evidence workpaper](telangana_five_internal_evidence_workpaper.pdf) has been prepared for review, with ad and website source links and per-lead checks. It is not a completed audit or client deliverable. An independent reviewer has not reviewed it; no mandatory audit gate has passed for these leads. Direct Python HTTPS probes for all five websites and one Meta ad produced TLS EOF in the sandbox; page-fetch availability does not establish a `verify_live.py` pass.

## Next steps for all five

1. Reconcile the date discrepancy and independently re-open every ad and site. Repeat Gmail/registry duplicate checks just before auditing, including discovered aliases. PNR needs a sourced business email before an email draft can be prepared.
2. Run the audit pipeline with actual current observations. Preserve unknowns; never infer ad destinations, pixel presence, performance or pricing from unavailable data. Tailor recommendations to the actual business and campaign objective.
3. Run the mandatory automated report verification, independent report-reviewer review, and live-data-auditor / `verify_live.py`. Do not deliver or draft outreach until all three pass; a restricted network, drift, or unreachable source requires a hold. An owner machine or GitHub runner with source access may be needed.
