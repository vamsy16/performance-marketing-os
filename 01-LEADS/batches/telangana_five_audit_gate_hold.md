# Telangana five — audit continuation and gate hold

**Status: HOLD — no client-ready audit has been produced, no outreach is approved.** Five separate draft audit PDFs and companion JSONs have now been built for owner review using `build_telangana_mixed_internal_audits.py`; all pages are labelled internal and do-not-send. The separate evidence workpaper is only supporting research. The five PDFs are not approved for client delivery. No report-reviewer or live-data-auditor subagent has independently reviewed the five leads in this environment.

## Draft audit gate results

- `PYTHONPATH=/tmp/pdflibs python3 01-LEADS/verify_report.py --ads-only` returned exit 0, including the five draft JSON/PDF pairs. This is a structural check, not proof the facts are current.
- `PYTHONPATH=/tmp/pdflibs python3 01-LEADS/verify_live.py --company 'SunSolar Power Systems' --company 'PNR Sunrise Energies' --company 'DLIFE Home Interiors' --company 'Dr Sridhar Dental' --company 'Galaxy Dental Care' --timeout 3 --retries 0` returned exit 2, all five UNREACHABLE: both Meta and each site failed with TLS EOF. This is not a live pass.
- Independent report-reviewer and live-data-auditor verdicts: **NOT RUN**. A self-inspection cannot stand in for an independent reviewer.
- The revised PDFs have five pages and carry the draft warning on each page. They use Ksquare's underlying story, with internal-draft overrides, not the complete client-ready Ksquare audit: evidence, controls, creatives and section/page matching remain incomplete. `measure_gaps.py` reports worst unused tails of 10.2% SunSolar, 31.1% PNR, 37.7% D'LIFE, 7.3% Sridhar and 37.8% Galaxy. The latter three exceed the 12% layout target; page-one ads and split sections also differ from the reference. These are layout measurements, not independent QA. The reports do not assign scores or assert absence of tracking; they use one captured card per lead and mark full account/technical checks unknown.
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

A direct Python `requests.get` test of all five website URLs and each of the five direct Meta ad URLs returned TLS EOF in the sandbox. This is a connectivity test, not a `verify_live.py` run or passing verification. Page-fetch responses are not a substitute for the repository's required live verifier.

## Safe route to completion

1. Use a machine/runner that can access the five sites, direct Meta Ad Library pages and relevant verification services with a trustworthy clock. Recheck site/ad identity, ad activity and duplicate status before creating audits.
2. Capture fresh evidence, run the appropriate repository audit builders, and validate each PDF using `verify_report.py`. Avoid invented scores or inferred tracking/landing destinations.
3. Have a separate reviewer inspect the actual JSON and PDF in accordance with `.opencode/agent/report-reviewer.md`; record `REPORT REVIEW: PASS` only when supported.
4. Run the full live verification on each generated report via `verify_live.py` and follow the independent spot checks in `.opencode/agent/live-data-auditor.md`. Exit 0 and a genuine independent PASS are required. Resolve drift and regenerate as needed; unreachable is a hold.
5. Share only after all gates pass. No email or outreach is requested or authorised by this task.

The existing `.github/workflows/ads-audit-pipeline.yml` is pinned to a different branch and also generates outreach. Do not dispatch it as-is: it would violate this session's branch restriction and exceed this task. A suitable safe runner configuration must target only the current branch and avoid outreach generation, without writing to another branch.
