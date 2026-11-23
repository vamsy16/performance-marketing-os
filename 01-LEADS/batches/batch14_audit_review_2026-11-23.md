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
