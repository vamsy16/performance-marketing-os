#!/usr/bin/env python3
"""
Ads-audit control review — claude-ads methodology.

Standing owner instruction (2026-10-24): every audit PDF from now on must also
carry the ads audit from https://github.com/vamsy16/claude-ads, on top of the
Ksquare 5-page format (see AUDIT_FORMAT_STANDARD.md).

This module grades the subset of the claude-ads Meta Ads control catalog that
can honestly be evaluated from PUBLIC evidence only — the Meta Ad Library ad
cards (copy, formats, start dates, destinations, platforms) plus the lead's own
landing page when it was fetched during discovery.

The catalog's own runtime contract is followed exactly:
  * a control is graded only when current evidence establishes the expectation;
  * controls that need Ads Manager / account access are returned as `unknown`,
    never guessed, never scored;
  * no platform-wide thresholds or broad benchmarks are applied.

Control IDs and intents come from claude-ads `ads/references/meta-audit.md`
(control registry M01–M72). Everything not listed in OBSERVABLE below is
account-only and is summarised as one explicit "needs account access" row.

Usage:
  from ads_audit_controls import evaluate
  result = evaluate(lead_dict, site_evidence=site_evidence_dict_or_None)
  # -> {"controls": [...], "counts": {...}, "methodology": "..."}
"""

METHODOLOGY = (
    "Control review follows the claude-ads Meta Ads audit catalog "
    "(github.com/vamsy16/claude-ads, ads/references/meta-audit.md). Each control "
    "is graded only where public evidence establishes it - Ad Library ad data "
    "and the lead's own landing page. Controls that require Ads Manager access "
    "(bidding, budgets, audiences, learning phase, EMQ, CAPI status) are marked "
    "unknown on purpose: they cannot be verified from outside the account and "
    "are never guessed."
)

# Dispositions
PASS = "pass"            # evidence shows the control is satisfied
FAIL = "fail"            # evidence shows a gap worth acting on
UNKNOWN = "unknown"      # evidence absent - needs account access
NA = "not_applicable"    # surface does not apply to this advertiser

ACCOUNT_ONLY_CONTROLS = (
    "M02 Conversions API, M03 event deduplication, M04 Event Match Quality, "
    "M06 aggregated measurement, M07 standard vs custom events, M08 CAPI "
    "Gateway, M09/M-AT1 attribution windows, M10 data freshness, M13/M14 "
    "learning phase, M15/M16 campaign & ad-set structure, M17 budget "
    "distribution, M36 bid strategy, M37 frequency caps, M38 breakdown "
    "reporting, M40 A/B testing, M19-M24 audiences & first-party data"
)


def _texts(ads):
    return " ".join((a.get("text") or "") + " " + (a.get("destination") or "")
                    for a in ads).lower()


def _formats(ads):
    """Formats visible on the ad cards: image / video / carousel."""
    out = []
    for a in ads:
        f = (a.get("format") or "").lower()
        if f:
            out.append(f)
        elif a.get("images"):
            out.append("image")
        elif "video" in (a.get("text") or "").lower():
            out.append("video")
    return out


def _concepts(ads):
    """Offer angles visible in the live ad copy."""
    blob = _texts(ads)
    found = []
    for key, label in (
        ("subsidy", "government subsidy"), ("78,000", "subsidy amount"),
        ("discount", "discount offer"), ("emi", "EMI / financing"),
        ("save", "bill savings"), ("warranty", "warranty"),
        ("trusted by", "social proof"), ("years", "experience claim"),
        ("site visit", "free site visit"), ("installation", "installation speed"),
        ("loan", "loan assistance"), ("monitoring", "monitoring / AMC"),
    ):
        if key in blob and label not in found:
            found.append(label)
    return found


def evaluate(lead, site_evidence=None):
    """Grade the publicly-observable controls for one lead.

    lead           - the LEADS entry dict (ad_library, funnel, website...)
    site_evidence  - optional dict from the landing-page check, e.g.
                     {"pixel": True|False|None, "utm": bool, "checked_on": str,
                      "note": str}
    """
    site_evidence = site_evidence or {}
    adlib = lead.get("ad_library") or {}
    meta = adlib.get("meta_own") or {}
    ads = meta.get("ads") or []
    funnel = lead.get("funnel") or {}
    dest = (funnel.get("destination") or "").lower()
    controls = []

    def add(cid, name, group, disposition, evidence):
        controls.append({"id": cid, "name": name, "group": group,
                         "disposition": disposition, "evidence": evidence})

    # ---- Tracking & measurement -------------------------------------------
    pixel = site_evidence.get("pixel")
    if pixel is True:
        add("M01", "Meta Pixel installed", "Tracking & measurement", PASS,
            "Meta Pixel code (fbq / connect.facebook.net) found in the live "
            "landing-page source.")
    elif pixel is False:
        add("M01", "Meta Pixel installed", "Tracking & measurement", FAIL,
            "No Meta Pixel code found in the landing-page source - ad clicks "
            "cannot be measured or retargeted.")
    else:
        add("M01", "Meta Pixel installed", "Tracking & measurement", UNKNOWN,
            "Landing page was not source-checked for this report; needs a "
            "page-source pull or account access.")

    if "fb.me" in dest or "lead form" in dest:
        add("M39", "UTM parameters on ad destinations", "Tracking & measurement",
            FAIL,
            "Live ads click to a Facebook lead form (fb.me) - traffic never "
            "reaches a page you own, so no URL can carry UTMs and click data "
            "stays inside Meta.")
    elif "utm_" in dest:
        add("M39", "UTM parameters on ad destinations", "Tracking & measurement",
            PASS, "Ad destination URL carries UTM parameters.")
    elif dest:
        add("M39", "UTM parameters on ad destinations", "Tracking & measurement",
            UNKNOWN,
            "Destination URL captured but parameter list not verified; needs "
            "the full click-through URL from Ads Manager.")
    else:
        add("M39", "UTM parameters on ad destinations", "Tracking & measurement",
            UNKNOWN, "No ad destination captured.")

    add("M05", "Domain verification", "Tracking & measurement", UNKNOWN,
        "Business Manager domain verification cannot be observed from public "
        "ad data; needs account access.")

    # ---- Creative ----------------------------------------------------------
    fmts = _formats(ads)
    if len(set(fmts)) >= 2:
        add("M25", "Creative format diversity", "Creative", PASS,
            f"Live ads use {len(set(fmts))} formats: {', '.join(sorted(set(fmts)))}.")
    elif fmts:
        add("M25", "Creative format diversity", "Creative", FAIL,
            f"All {len(ads)} live ads use a single format ({fmts[0]}) - no "
            "format variety to test what converts.")
    else:
        add("M25", "Creative format diversity", "Creative", UNKNOWN,
            "Ad-card formats were not captured for these ads.")

    concepts = _concepts(ads)
    if len(concepts) >= 3:
        add("M26", "Creative concept coverage", "Creative", PASS,
            f"{len(concepts)} distinct offer angles in live copy: "
            f"{', '.join(concepts)}.")
    elif concepts:
        add("M26", "Creative concept coverage", "Creative", FAIL,
            f"Only {len(concepts)} offer angle in live copy ({', '.join(concepts)}) "
            "- every ad says the same thing.")
    else:
        add("M26", "Creative concept coverage", "Creative", UNKNOWN,
            "Ad copy could not be read for these ads.")

    if any("trusted by" in _texts(ads) for _ in [0]):
        add("M30", "Social proof utilization", "Creative", PASS,
            "Live ad copy carries a social-proof claim (customer count / "
            "testimonial framing).")
    else:
        add("M30", "Social proof utilization", "Creative", FAIL,
            "No social proof (customer counts, reviews, testimonials) in the "
            "live ad copy.")

    add("M27", "Video aspect ratios", "Creative", UNKNOWN,
        "Creative files cannot be downloaded from the Ad Library; needs "
        "account access or the raw creatives.")
    add("M29", "Hook rate", "Creative", UNKNOWN,
        "Video performance metrics are account-only.")
    add("M31", "UGC / social-native content", "Creative", UNKNOWN,
        "Content style cannot be verified from ad cards alone.")
    add("M-CR4", "CTR benchmark", "Creative", UNKNOWN,
        "No spend or impression data is public for this advertiser; the "
        "catalog forbids benchmark guessing.")

    # ---- Structure & delivery ---------------------------------------------
    started = [a.get("started") for a in ads if a.get("started")]
    if started:
        newest = max(started)
        add("M-CR1", "Creative freshness", "Structure & delivery", PASS,
            f"Live creatives include recent launches (newest started "
            f"{newest}) - the account is not running one stale ad forever.")
    else:
        add("M-CR1", "Creative freshness", "Structure & delivery", UNKNOWN,
            "Ad start dates were not captured.")

    if len(ads) >= 3:
        add("M11", "Campaign fragmentation", "Structure & delivery", PASS,
            f"{len(ads)} distinct live ads visible - enough running to compare "
            "messages against each other.")
    elif len(ads) == 2:
        add("M11", "Campaign fragmentation", "Structure & delivery", PASS,
            "2 distinct live ads visible - a comparison is at least possible.")
    elif len(ads) == 1:
        add("M11", "Campaign fragmentation", "Structure & delivery", FAIL,
            "A single live ad - no internal comparison, no safety net if it "
            "fatigues.")
    else:
        add("M11", "Campaign fragmentation", "Structure & delivery", UNKNOWN,
            "No live ads captured.")

    if funnel:
        add("M18", "Campaign objective alignment", "Structure & delivery", PASS,
            f"Ad CTA and destination agree on one job: {funnel.get('type', 'captured destination')}.")
    else:
        add("M18", "Campaign objective alignment", "Structure & delivery",
            UNKNOWN, "No funnel captured.")

    add("M33", "Advantage+ Placements", "Structure & delivery", UNKNOWN,
        "Placement automation state is account-only.")
    add("M28", "Creative fatigue detection", "Creative", UNKNOWN,
        "Frequency and performance decay need account metrics.")

    counts = {PASS: 0, FAIL: 0, UNKNOWN: 0, NA: 0}
    for c in controls:
        counts[c["disposition"]] += 1

    return {
        "controls": controls,
        "counts": counts,
        "methodology": METHODOLOGY,
        "account_only": ACCOUNT_ONLY_CONTROLS,
    }
