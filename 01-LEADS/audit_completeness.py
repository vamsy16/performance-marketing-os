#!/usr/bin/env python3
"""Single source of truth for 'is this website audit actually complete?'

A deliverable full audit must resolve every website check that the public page
can answer. `None` is a held-draft state, not a client-facing finding. The only
legitimate unavailable measurements are outside this list (PageSpeed quota,
account-only ad controls, an ad destination the card does not state).

Used by run_pipeline.py (refuse before rendering) and delivery_gate.py (refuse
a hand-built or externally produced report).
"""

MANDATORY_TOP = ("ssl", "load_time_seconds", "final_url", "html_errors")
MANDATORY_PIXELS = (
    "meta_pixel", "google_ads", "google_analytics_ga4", "google_analytics_ua",
    "linkedin_insight", "microsoft_clarity", "hotjar", "google_tag_manager",
)
MANDATORY_CONVERSION = (
    "has_contact_form", "has_phone_click", "has_whatsapp_link", "has_cta_buttons",
    "has_live_chat", "has_popup_optin", "has_testimonials", "has_pricing_page_link",
)
MANDATORY_SEO = (
    "has_title", "has_meta_description", "h1_count", "has_schema", "has_og_tags",
    "has_favicon", "image_count", "images_without_alt",
)
MANDATORY_PAGE_COUNT = ("has_sitemap",)
MANDATORY_LOCAL = ("has_google_maps_embed",)

GROUPS = (
    ("top", MANDATORY_TOP),
    ("pixels", MANDATORY_PIXELS),
    ("conversion", MANDATORY_CONVERSION),
    ("seo", MANDATORY_SEO),
    ("page_count", MANDATORY_PAGE_COUNT),
    ("local_signals", MANDATORY_LOCAL),
)

ALLOWED_UNAVAILABLE = (
    "PageSpeed / Lighthouse (HTTP 429 or API unreachable) -> 'Not available at audit time (...)'",
    "Account-only Meta controls (CAPI, EMQ, budgets, audiences, learning phase, etc.) -> UNKNOWN",
    "Ad destination when the live ad card does not state one -> 'Not confirmed from the ad card in this pass'",
)

# A mandatory check stored as one of these string values is just as unresolved
# as `None`. Do not let a builder hide a gap by writing a polite sentence.
UNRESOLVED_SENTINELS = {
    "", "not found", "not checked", "not checked in this pass",
    "not measured", "not available", "unavailable", "unknown", "n/a", "na",
}


def has_website_audit(audit):
    """True for a full audit or an ads-only report promoted to the Ksquare layout."""
    return bool(audit.get("site_audit")) or not audit.get("ads_only")


def site_scope(audit):
    return audit.get("site_audit") or audit


def unresolved(audit):
    """Return dotted names of mandatory website checks that are missing/None."""
    if not has_website_audit(audit):
        return []
    scope = site_scope(audit)
    missing = []
    for group, keys in GROUPS:
        source = scope if group == "top" else (scope.get(group) or {})
        for key in keys:
            if key not in source or source[key] is None:
                missing.append(f"{group}.{key}" if group != "top" else key)
                continue
            value = source[key]
            if isinstance(value, dict):
                missing.append(f"{group}.{key}" if group != "top" else key)
                continue
            if isinstance(value, str) and value.strip().lower() in UNRESOLVED_SENTINELS:
                missing.append(f"{group}.{key}" if group != "top" else key)
    return missing
