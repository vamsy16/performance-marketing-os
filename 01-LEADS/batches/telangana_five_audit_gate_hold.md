# Telangana five — audit continuation and gate hold

**Status: HOLD — no client-ready audit has been produced, no outreach is approved.** Five separate draft audit PDFs and companion JSONs have now been built for owner review using `build_telangana_mixed_internal_audits.py`; all pages are labelled internal and do-not-send. The separate evidence workpaper is only supporting research. The five PDFs are not approved for client delivery. No report-reviewer or live-data-auditor subagent has independently reviewed the five leads in this environment.

## Draft audit gate results

- `PYTHONPATH=/tmp/pdflibs python3 01-LEADS/verify_report.py --ads-only` returned exit 0, including the five draft JSON/PDF pairs. This is a structural check, not proof the facts are current.
- `PYTHONPATH=/tmp/pdflibs python3 01-LEADS/verify_live.py --company 'SunSolar Power Systems' --company 'PNR Sunrise Energies' --company 'DLIFE Home Interiors' --company 'Dr Sridhar Dental' --company 'Galaxy Dental Care' --timeout 3 --retries 0` returned exit 2, all five UNREACHABLE: both Meta and each site failed with TLS EOF. This is not a live pass.
- Independent report-reviewer and live-data-auditor verdicts: **NOT RUN**. A self-inspection cannot stand in for an independent reviewer.
- The revised PDFs have five pages and carry the draft warning on each page. They use Ksquare's underlying story, with internal-draft overrides, not the complete client-ready Ksquare audit: evidence, controls, creatives and section/page matching remain incomplete. `measure_gaps.py` reports worst unused tails of 4.1% SunSolar, 5.9% PNR, 6.3% D'LIFE, 12.0% Sridhar and 11.2% Galaxy (rounded); page-one ads and split sections still differ from the reference. These are layout measurements, not independent QA. The reports do not assign scores or assert absence of tracking; they use one captured card per lead and mark full account/technical checks unknown.
- Repeated Gmail `in:anywhere` searches for names, domains and known contacts for each of the five found no messages and reported complete scope for those queries. This is not proof that no unknown alias exists. No outreach was created or sent.


## Source and runtime checks

The page-fetch service returned a Nu HTML validator response for each of the five sites, but its response identifies validator version `26.11.28`, later than the session date `2026-11-23`; the sandbox clock also reports `2026-11-28`. These results cannot be certified as current on the session date and must be rechecked on a trusted clock. They are leads for technical investigation, not established client findings:

- [SunSolar home](https://validator.w3.org/nu/?doc=https%3A%2F%2Fwww.sunsolar.info%2F&out=json): the displayed response flags a `link rel=preload` with `as=video`. Browser behavior and business impact were not tested. Response spans chunks; no total is asserted.
- [PNR Sunrise home](https://validator.w3.org/nu/?doc=https%3A%2F%2Fsunriseenergies.in%2F&out=json): the displayed response flags `aria-hidden="True"` and several ARIA label errors. Recheck source and actual assistive technology behavior before describing impact.
- [D'LIFE Hyderabad](https://validator.w3.org/nu/?doc=https%3A%2F%2Fdlifeinteriors.com%2Flocation%2Fhyderabad%2F&out=json): the displayed response flags telephone links containing spaces, including a Hyderabad number. This is validator evidence, not proof that calling fails on a real device. Response spans multiple chunks; no total is asserted.
- [Dr. Sridhar services](https://validator.w3.org/nu/?doc=https%3A%2F%2Fsridhardental.com%2Fservices&out=json): fetched output ended prematurely in a JSON string; treat the validator result as incomplete, not a pass or count.
- [Galaxy Dental contact](https://validator.w3.org/nu/?doc=https%3A%2F%2Fgalaxydentalcare.in%2Fcontact-us%2F&out=json): response spans multiple chunks and includes markup diagnostics. No total or clinical/lead-generation impact is asserted.

Additional source leads from `showsource=yes` responses (not runtime or current-date verification):

- [SunSolar homepage](https://validator.w3.org/nu/?doc=https%3A%2F%2Fwww.sunsolar.info%2F&showsource=yes): Google Ads base tag `AW-18179174251`.
- [PNR homepage](https://validator.w3.org/nu/?doc=https%3A%2F%2Fsunriseenergies.in%2F&showsource=yes): canonical points to the reserved `https://www.sunriseenergies.example/`; investigate and recheck the production canonical before claiming an impact.
- [D'LIFE Hyderabad](https://validator.w3.org/nu/?doc=https%3A%2F%2Fdlifeinteriors.com%2Flocation%2Fhyderabad%2F&showsource=yes): Meta Pixel code and Google Ads base tag `AW-830229729`.
- [Sridhar services](https://validator.w3.org/nu/?doc=https%3A%2F%2Fsridhardental.com%2Fservices&showsource=yes): GA4 `G-7Y9ND039HL` and Google Ads base tag `AW-855095874` in the HTML shell.
- [Galaxy contact](https://validator.w3.org/nu/?doc=https%3A%2F%2Fgalaxydentalcare.in%2Fcontact-us%2F&showsource=yes): deferred GTM code `GTM-TRRMQGQ`.

These observations do not establish that tags executed, conversions fired, or the listed identifiers are configured correctly. All require a fresh trusted-date check; unobserved tools remain unknown, not missing.

## Additional public ad searches

Google Ads Transparency Center domain searches were fetched with **India / Any time / All platforms / All formats**. Results were 0 for [SunSolar](https://adstransparency.google.com/?region=IN&domain=www.sunsolar.info), 0 for [PNR](https://adstransparency.google.com/?region=IN&domain=sunriseenergies.in), approximately 200 for [D'LIFE](https://adstransparency.google.com/?region=IN&domain=dlifeinteriors.com), 42 for [Sridhar](https://adstransparency.google.com/?region=IN&domain=sridhardental.com), and approximately 300 for [Galaxy](https://adstransparency.google.com/?region=IN&domain=galaxydentalcare.in). These are domain-filtered archive results, **not active-ad counts**; 0 is not proof of no advertising elsewhere. The Galaxy samples were attributed by Google to the verified advertiser Jaydeep, who has ads for other businesses too; do not treat that advertiser's full count as Galaxy's. Sample D'LIFE and Sridhar creative detail pages report last shown on 28 and 27 Nov 2026 respectively, after the session date. This reinforces the timing hold; none of these values can be certified as current as of the session date.

Direct competitor ad samples were separately fetched: [SolarSquare 1472241928117694](https://www.facebook.com/ads/library/?id=1472241928117694) for the two solar businesses (PNR's sample is partner recruitment, SolarSquare's is consumer-directed); [Houseboat Interiors 2019161465707252](https://www.facebook.com/ads/library/?id=2019161465707252) for D'LIFE; and the two dental leads' directly attributed Meta cards for one another. Their ad overlays displayed Active, but source timing/current status still needs recheck; none establishes market share, audience overlap, or ad performance.

A direct Python `requests.get` test of all five website URLs and each of the five direct Meta ad URLs returned TLS EOF in the sandbox. This is a connectivity test, not a `verify_live.py` run or passing verification. Page-fetch responses are not a substitute for the repository's required live verifier.

## First-batch comparison and extra checks

The Ksquare reference and `build_batch10_ksquare.py` use the shared five-page story, public ad cards, direct page views and Nu source to populate website, conversion and technical checks. Batch 10 also left PageSpeed, server timing and other unmeasured fields unchecked. The five present drafts remain more limited: they use one ad card per business, conservative rendering overrides and ungraded controls, and do not yet satisfy the full standard or independent review.

A fresh page-fetch pass supplied the visible H1 heading for each reviewed page, now distinguished from an HTML H1 count; Sridhar's heading is rendered in the page view whereas Nu shows an HTML shell. SunSolar's robots file contains no sitemap directive and its sitemap fetch failed; PNR's robots and sitemap fetch attempts failed. D'LIFE and Galaxy robots files point to sitemap indexes; Sridhar's sitemap lists service and booking URLs. A sitemap is not evidence that pages are indexed. The D'LIFE and Galaxy indexes include future last-modified dates relative to the session date, so all source timing remains on hold. New PDF fields explicitly state these limits.

The full live verifier was rerun after this update: exit 2, MATCH 0 / DRIFT 0 / UNREACHABLE 5. No independent review was performed; the automated report verifier and regression tests passed. These results do not establish that the drafts match the first batch's completeness or are safe to send.

## Safe route to completion

1. Use a machine/runner that can access the five sites, direct Meta Ad Library pages and relevant verification services with a trustworthy clock. Recheck site/ad identity, ad activity and duplicate status before creating audits.
2. Capture fresh evidence, run the appropriate repository audit builders, and validate each PDF using `verify_report.py`. Avoid invented scores or inferred tracking/landing destinations.
3. Have a separate reviewer inspect the actual JSON and PDF in accordance with `.opencode/agent/report-reviewer.md`; record `REPORT REVIEW: PASS` only when supported.
4. Run the full live verification on each generated report via `verify_live.py` and follow the independent spot checks in `.opencode/agent/live-data-auditor.md`. Exit 0 and a genuine independent PASS are required. Resolve drift and regenerate as needed; unreachable is a hold.
5. Share only after all gates pass. No email or outreach is requested or authorised by this task.

The existing `.github/workflows/ads-audit-pipeline.yml` is pinned to a different branch and also generates outreach. Do not dispatch it as-is: it would violate this session's branch restriction and exceed this task. A suitable safe runner configuration must target only the current branch and avoid outreach generation, without writing to another branch. A read-only `gh api` request to the repository Actions permissions endpoint returned HTTP 403 (resource not accessible by integration), so this session could not confirm access to a suitable Actions runner. PageSpeed API fetches for the five URLs also failed without a usable HTTP response; no 429, scores or LCP values are asserted.
