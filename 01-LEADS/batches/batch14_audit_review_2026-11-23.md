# Batch 14: audit draft verification and handoff — 2026-11-23

**HOLD — not approved for outreach or client delivery.** Five internal PDFs
and matching JSONs were generated from observed public data. `review_pending`
is set on all five lead records. Each PDF is marked internal draft. The
independent report-reviewer and full live-data-auditor gates remain outstanding.
No claim of an independent third-eye pass is made.

## Evidence and corrections made during this pass

Each of these active cards was re-opened through `fetch_page` on 2026-11-23:

| Company | Card | What the card actually exposes | Separate page examined |
|---|---|---|---|
| SundayGrids | [1677559457265808](https://www.facebook.com/ads/library/?id=1677559457265808) | Project link `/projects/278RAO1IVG`; copy differs from earlier discovery excerpt | [Homepage](https://www.sundaygrids.com/) and [Parker 110](https://www.sundaygrids.com/projects/278RAO1IVG) |
| Arrow Solar | [4616054888675895](https://www.facebook.com/ads/library/?id=4616054888675895) | Card displays arrowenergy.in but href is fb.me; final form is not verified | [Homepage](https://arrowenergy.in/) |
| Atria Power | [1103298019283935](https://www.facebook.com/ads/library/?id=1103298019283935) | fb.me / Get offer; final form is not verified | [Corporate homepage](https://www.atriapower.com/), contact page; homepage text also read through allorigins raw |
| RAGA | [3057224721288021](https://www.facebook.com/ads/library/?id=3057224721288021) | Instagram profile | [Homepage](https://ragarenewableenergy.com/) |
| Zenith | [972063355961941](https://www.facebook.com/ads/library/?id=972063355961941) | Call now; dialled number not exposed | [index.html](https://zenithsolars.com/index.html) (root blocked checker) |

Only one card is captured per PDF; this is not a count of all active ads.
Public served HTML was examined using W3C Nu `showsource=yes` and page fetches;
absence of tracking is **unknown** where source review or runtime was incomplete.
No test submission, call, event firing, conversion metrics, PageSpeed or Google
Ads Transparency lookup was done. Atria's checker hit its message cap, largely
Wix CSS diagnostics; those are not represented as actionable HTML defects.
The scores use the repository's lower-is-better function with unknown values
excluded; they are **provisional**, not a complete-site health comparison.

The PDFs intentionally omit unsupported ad-copy symbols for font compatibility;
the JSON retains the originally captured Unicode. Assertions about the live
ad click destination were narrowed to what the actual card exposed. SundayGrids'
earlier discovery excerpt describes a different creative; the draft uses the
actual copy shown under the captured ID. Website comparisons for off-site ad
clicks are explicitly labelled as separate, not the destination.

## Gate results

1. `verify_report.py --ads-only`: all 46 report JSON/PDF pairs passed on
   2026-11-23. This is a structural check, not proof of live facts.
2. Independent report-reviewer agent: **NOT RUN** in this environment. An
   author re-read found and corrected the ad-copy and destination issues above,
   but it does not substitute for independent review.
3. `verify_live.py` on the five companies with `--offline`: 5 consistency
   matches; **not a live pass**. Full live run: exit **2**, five UNREACHABLE,
   TLS connections closed for Meta and each site. Do not send on this result.

The live verifier's `--latest` previously selected alphabetically, not by
modification time, and its offline success message incorrectly claimed live
verification. Both are corrected in this branch. Use explicit company names
for the final check, not `--latest`, and run on a machine with network access:

```sh
cd 01-LEADS
PYTHONPATH=/tmp/pdflibs python3 verify_live.py \
  --company 'SundayGrids' --company 'Arrow Solar' --company 'Atria Power' \
  --company 'RAGA Renewable Energy' --company 'Zenith Solars'
```

Require exit 0 and resolve any drift, then obtain a separate report-reviewer
PASS. After both gates pass, update the builder to clear `review_pending`, rebuild the
reports, and update lead statuses. SundayGrids has no published outreach email; do not draft
outreach without one. Do not treat `verify_report.py` PASS alone as approval.

## Expanded source pass — 2026-11-23

This pass re-read the companies' homepage text and Nu checker message summaries,
and re-opened representative ad cards or their public destination panels. It
adds title and metadata checks that were actually visible, selected conversion
signals, and the following specific observations. These are author's source
checks, **not** the independent reviewer or `verify_live.py` third gate:

- SundayGrids: [home source](https://validator.w3.org/nu/?doc=https%3A%2F%2Fwww.sundaygrids.com%2F&showsource=yes)
  reports 25 errors and 21 warnings, including 12 duplicate SVG IDs, four
  skipped heading levels, and seven H1s. [Sitemap](https://www.sundaygrids.com/sitemap.xml)
  lists project pages. Source shows legacy UA and GTM; deployment/runtime of
  the other tags remains unverified.
- Arrow: [home](https://arrowenergy.in/) has 3 kW indicative price of
  ₹1,44,000 after subsidy, while hero says zero upfront cost. It also says
  prices depend on site conditions and subsidy on approval. [Contact page](https://arrowenergy.in/contact)
  has an enquiry form, which was not submitted. [Source](https://validator.w3.org/nu/?doc=https%3A%2F%2Farrowenergy.in%2F&showsource=yes)
  has GA4 G-LY596XLF42, metadata and LocalBusiness schema. [Sitemap](https://arrowenergy.in/sitemap.xml)
  was fetched. No claim made about actual event firing.
- Atria: [homepage](https://www.atriapower.com/) presents solar, wind and hydro
  and links rooftop solutions to another domain. Its [validator](https://validator.w3.org/nu/?doc=https%3A%2F%2Fwww.atriapower.com%2F&showsource=yes)
  hit its cap: 979 errors including 7 HTML errors at the cutoff, dominated by
  CSS diagnostics, not an actionable-error total. Final ad form is untested.
- RAGA: [homepage source](https://validator.w3.org/nu/?doc=https%3A%2F%2Fragarenewableenergy.com%2F&showsource=yes)
  contains a `#` "Book a Free Site Visit" link in a block marked hidden on
  desktop, tablet and mobile; a second CTA links to `/contact-us/`. Likewise,
  the John Doe/SunBright quote is in a hidden block; do not claim it is visible.
  A separate homepage form container is marked hidden on tablets. Counters start
  at zero in source with data-to values including 12 years and 100% satisfaction;
  rendered values require browser verification. Other customer quotes also occur
  in source; actual visibility and authenticity are not established. [Sitemap
  index](https://ragarenewableenergy.com/sitemap_index.xml) and [page sitemap](https://ragarenewableenergy.com/page-sitemap1.xml) fetched.
- Zenith: [robots.txt](https://zenithsolars.com/robots.txt) points to
  `/demo/sitemap.xml`, whose [contents](https://zenithsolars.com/demo/sitemap.xml)
  include JCB equipment URLs. One such [3DX page](https://zenithsolars.com/demo/products/3dx)
  displays Sri Sai JCB content. This is an observation, not a conclusion about
  ownership or compromise. The [validator](https://validator.w3.org/nu/?doc=https%3A%2F%2Fzenithsolars.com%2Findex.html&showsource=yes)
  reports four duplicate class attributes around the form and a fatal nesting
  error after which it stopped; rendering and lead delivery were not tested.

Scores were recalculated using only measured values, with the score basis stated
in each PDF. Zenith's provisional score changed from 0 to 1 because six H1s
were observed; this does not score the sitemap finding. Source checks cannot
prove account configuration or client-side event firing, so missing runtime,
PageSpeed and account-only checks still require access. Independent report
review and a successful live verifier remain mandatory before client delivery.

## Follow-up source checks and remaining inputs — 2026-11-23

- [Atria contact](https://www.atriapower.com/contact-us) displays name, email,
  phone and message fields; no submission was made. [robots.txt](https://www.atriapower.com/robots.txt)
  declares a sitemap but the sitemap fetch failed; its contents and indexing
  remain unknown. W3C source includes a favicon.
- [RAGA source](https://validator.w3.org/nu/?doc=https%3A%2F%2Fragarenewableenergy.com%2F&showsource=yes)
  clarifies the hidden CTA and placeholder noted above. The form's tablet-hidden
  class is source evidence, not a tested browser defect.
- [Zenith contact](https://zenithsolars.com/contact.html) gives 585106 in the
  header and 585105 in the body; confirm the correct postal code before fixing.
- PageSpeed API fetches for all five returned a generic fetch error. The cause
  is unknown; no score or LCP can be inferred. These checks are author checks,
  not an independent third-eye review. Five drafts and scores remain provisional.

To finish: obtain five mobile PageSpeed report URLs or exports with test dates;
run real-browser mobile and desktop CTA tests with screenshots and permission
for controlled submissions/calls; supply consented Tag Assistant / Pixel Helper
or network-event captures; provide read-only Meta/Google Ads access or sanitized
exports for account-only controls. A separate reviewer must examine the PDF,
JSON and sources and issue the independent PASS. Run the live-verifier command
above from a network-enabled environment and resolve every mismatch. Do not
send before all gates pass.

## Conversion-readiness correction — 2026-11-23

Re-read the five public homepage texts plus [Arrow contact](https://arrowenergy.in/contact),
[Atria contact](https://www.atriapower.com/contact-us), the SundayGrids project,
and selected W3C source for SundayGrids, RAGA and Zenith. The JSON now records
source URLs and a dated five-row conversion evidence summary, rendered in each
PDF instead of generic unchecked CTA status. The rows distinguish a link, a
form in source or on a separate page, and what still requires interactive testing.
Examples: Arrow's `Check Subsidy Eligibility` and `Book Now` link to `/contact`;
Atria's corporate `Contact us` links to its contact page; RAGA's source has
an enquiry form in a tablet-hidden container. CTA counts remain unknown: these
examples do not establish a complete count or functioning buttons.

Arrow's homepage-form flag was changed from false to unknown: the fetched text
showed no form but does not prove no dynamically loaded form exists. Consequently
its provisional formula score changes **8 to 0** and `leads.csv` and the PDF
index are updated. Zero reflects excluded unknowns, not a clean bill of health.
No controlled submissions, browser interaction, runtime tracking checks,
PageSpeed measurement or independent third-eye review were performed. The
reports continue to be drafts, and the live and independent gates still apply.
