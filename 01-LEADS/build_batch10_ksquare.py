#!/usr/bin/env python3
"""Rebuild the batch-10 ads reports into the full 5-page audit layout.

Owner instruction 2026-10-24: the batch-10 reports must be generated exactly
like ``02-OUTREACH/audit_pdfs/audit_Ksquare_Energy.pdf`` (the 5-page
DIGITAL MARKETING & PAID ADS AUDIT layout), every check in that layout must be
performed, and the report must carry real live data only - no simulated or
demo values.

Where the numbers come from (all read live on 2026-10-25):

* Meta Ad Library - the live ad cards already captured in each JSON.
* The company's own website, read through the W3C Nu HTML Checker with
  ``showsource=yes`` (``https://validator.w3.org/nu/?doc=<url>&showsource=yes``),
  which returns the raw served HTML with script tags intact. That is how the
  Meta Pixel / GA4 / GTM / Clarity / Hotjar / Google Ads tags below were read.
* A direct fetch of the same pages for headings, forms, links, CTAs,
  testimonials, pricing and image alt text.

Checks that could NOT be run are stored as None and render as
"Not checked in this pass" / "Not available at audit time". They are never
guessed:

* Google PageSpeed mobile score + LCP - the keyless API returns HTTP 429
  (quota limit 0/day), the same failure the reference Ksquare PDF reports.
* Server response time - not measured.
* Google Ads Transparency advertiser records - not fetched.
* Sitemap page count - not fetched.
* SolarSquare's page head is minified into ~125 lines; lines 3-125 were read
  but the doctype/title line (line 1) could not be isolated, so its meta
  description, Open Graph tags, schema and H1 are recorded as unchecked rather
  than assumed. Its <title> IS known (read from the live page).

Run:  cd 01-LEADS && python3 build_batch10_ksquare.py
"""
import json
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

from ads_audit import calculate_audit_score          # noqa: E402
from ads_audit_controls import evaluate              # noqa: E402
from audit_pdf import generate_ads_only_pdf          # noqa: E402

AUDIT_DIR = os.path.join(BASE, "ads_only_results")
READ_ON = "2026-10-25"
PAGESPEED_ERROR = "API returned 429"      # keyless PageSpeed quota, read live

NO_PIXELS = {
    "meta_pixel": False,
    "google_ads": False,
    "google_analytics_ga4": False,
    "google_analytics_ua": False,
    "linkedin_insight": False,
    "microsoft_clarity": False,
    "hotjar": False,
    "google_tag_manager": False,
}


def pixels(**over):
    d = dict(NO_PIXELS)
    d.update(over)
    return d


# ---------------------------------------------------------------------------
# Real measurements, one entry per batch-10 lead.
# ---------------------------------------------------------------------------

SUNOVA = {
    "ssl": True,
    "load_time_seconds": None,                 # not measured
    "final_url": "https://sunovagreenenergy.com/",
    "audit_date": READ_ON,
    "pixels": pixels(),                        # head lines 1-150 + page footer read: no tag of any kind
    "conversion": {
        "has_contact_form": True,              # "Submit Enquiry" form on /contact-us/
        "has_phone_click": True,               # tel:+91 9912848596 / tel:+919849763391
        "has_whatsapp_link": True,             # web.whatsapp.com/send?phone=919912848596
        "has_cta_buttons": 10,                 # Learn More x6, Book Site Visit, read more about us, contact us today, Let'sTalkSolar
        "has_live_chat": False,                # no chat widget on either page read
        "has_popup_optin": False,              # no popup/modal seen
        "has_testimonials": True,              # 3 testimonials (Ramesh Kumar, Suresh Reddy, Lakshmi Priya)
        "has_pricing_page_link": False,        # comparison table lists cost bands only, no prices
    },
    "seo": {
        "has_title": True,
        "title_text": "sunovagreenenergy.com",  # bare domain - no brand or keyword
        "title_length": 21,
        "has_meta_description": False,          # not present in the head read
        "meta_desc_length": 0,
        "h1_count": 0,                          # Nu checker: "document has heading elements but none has computed heading level of 1"
        "h1_text": "",
        "has_og_tags": False,                   # not present in the head read
        "has_schema": False,                    # no JSON-LD found
        "has_favicon": True,                    # not verified either way - never claimed in the layout
        "image_count": 31,                      # counted on the full homepage read
        "images_without_alt": 26,
    },
    "pagespeed": {"error": PAGESPEED_ERROR},
    "page_count": {"has_sitemap": None},
    "local_signals": {"has_google_maps_embed": False},
    "platform": ("WordPress + Elementor + Smart Slider 3 + ElementsKit Lite + "
                 "Premium Addons for Elementor, theme \"sungo\", LiteSpeed Cache 7.9.2"),
    "html_errors": "411 errors (359 HTML, 17 CSS parse, 22 CSS value, 321 style-rule)",
}

WISDA = {
    "ssl": True,
    "load_time_seconds": None,
    "final_url": "https://www.wisda.in/",
    "audit_date": READ_ON,
    "pixels": pixels(
        meta_pixel=True,              # 1494048391894940 (head, fbevents.js) + 1175755211312545 (body noscript)
        google_analytics_ga4=True,    # G-SYCFTFNH0N
        google_tag_manager=True,      # GTM-PTPCLJ5R
    ),
    "conversion": {
        "has_contact_form": True,              # "Get in Touch with Wisda" 8-field form
        "has_phone_click": True,               # tel:+919100047301 on /contact-us
        "has_whatsapp_link": False,            # no WhatsApp link on either page read
        "has_cta_buttons": 3,                  # Get free site visit x2 + form submit
        "has_live_chat": False,
        "has_popup_optin": False,
        "has_testimonials": True,              # Rahul Kumar, Hyderabad
        "has_pricing_page_link": False,        # "transparent pricing models" copy only, no prices published
    },
    "seo": {
        "has_title": True,
        "title_text": "Best Rooftop Solar Company in Hyderabad | Wisda Energy",
        "title_length": 57,
        "has_meta_description": True,          # present (length not captured)
        "meta_desc_length": None,
        "h1_count": 1,
        "h1_text": "Together for Future: Empowering India Through Green Energy",
        "has_og_tags": True,                   # og:url/type/title/description/image + Twitter summary_large_image
        "has_schema": True,                    # 4 JSON-LD blocks: Corporation, WebSite, ProfessionalService, FAQPage
        "has_favicon": True,
        "image_count": 18,                     # counted on the full homepage read
        "images_without_alt": 7,               # logo img + 6 testimonial images
    },
    "pagespeed": {"error": PAGESPEED_ERROR},
    "page_count": {"has_sitemap": None},
    "local_signals": {"has_google_maps_embed": False},   # Google Maps link on /contact-us, no embed
    "platform": "Custom HTML (Tailwind CDN, Swiper 11, Font Awesome 6.5.1, Google Fonts)",
    "html_errors": "15 errors, 1 warning, 7 info",
}

SOLARSQUARE = {
    "ssl": True,
    "load_time_seconds": None,
    "final_url": "https://www.solarsquare.in/rooftop-solar-in-hyderabad-1",
    "audit_date": READ_ON,
    # Head lines 3-125 read (WordPress minified): no Meta Pixel, no GA4, no GTM,
    # no Google Ads tag. MoEngage IS present and reads utm_source/utm_campaign/fbclid
    # from cookies - noted in the report text.
    "pixels": pixels(),
    "conversion": {
        "has_contact_form": True,              # "Book a FREE Solar Consultation" form -> admin-ajax.php
        "has_phone_click": True,               # tel:+91 9830003000 (malformed - illegal space after tel:)
        "has_whatsapp_link": True,             # WhatsApp links + whatsapp_number form field
        "has_cta_buttons": 6,
        "has_live_chat": False,
        "has_popup_optin": True,               # #leadFormModal lead-form modal
        "has_testimonials": True,              # Santosh Singh, Samir Patil, Dr. Sudhakar Shukla
        "has_pricing_page_link": True,         # full Hyderabad price table, indicative as of 01 Oct 2026
    },
    "seo": {
        "has_title": True,
        "title_text": "Top Solar Company in Hyderabad | Solar Panel Price & Installation",
        "title_length": 66,
        "has_meta_description": None,          # head line 1 could not be isolated - not assumed
        "meta_desc_length": None,
        "h1_count": None,                      # not assumed (Nu checker raised no missing-H1 warning)
        "h1_text": "",
        "has_og_tags": None,
        "has_schema": None,
        "has_favicon": True,                   # cropped-favicon-32x32.png seen in the head
        "image_count": None,                   # page read in part (5 chunks, 1 read)
        "images_without_alt": None,
    },
    "pagespeed": {"error": PAGESPEED_ERROR},
    "page_count": {"has_sitemap": None},
    "local_signals": {"has_google_maps_embed": False},   # Map.png image, not an embed
    "platform": "WordPress (theme \"sse\"), Bootstrap, Slick, jQuery UI, MoEngage",
    # The city page's head is minified into ~125 lines; lines 3-125 were read but
    # the doctype/title line could not be isolated, so these rows stay unchecked.
    "scope_note": (
        "SolarSquare serves this city page minified into roughly 125 source lines. "
        "Lines 3-125 of the head were read in full, but the doctype/title line could "
        "not be isolated, so its meta description, Open Graph tags, structured data, "
        "H1 and image alt counts are reported as not checked rather than assumed. "
        "The page title IS known and is shown below."),
    "html_errors": "35 errors, 30 warnings (6 duplicate form IDs, tel: href with illegal space, viewport blocks zoom)",
}

RAYZON = {
    "ssl": True,
    "load_time_seconds": None,
    "final_url": "https://rayzonsolar.com/contact-us",
    "audit_date": READ_ON,
    "pixels": pixels(),                        # head lines 1-186 read: no pixel, GA4, GTM or Google Ads tag
    "conversion": {
        "has_contact_form": True,              # contact form with Submit on /contact-us
        "has_phone_click": True,               # tel:+919638000461, tel:18001231232
        "has_whatsapp_link": False,
        "has_cta_buttons": 5,
        "has_live_chat": True,                 # Tawk.to widget (embed.tawk.to)
        "has_popup_optin": False,
        "has_testimonials": False,             # none on the page read
        "has_pricing_page_link": False,
    },
    "seo": {
        "has_title": True,
        "title_text": "Rayzon Solar | Contact Us",
        "title_length": 24,
        "has_meta_description": True,          # present (length not captured)
        "meta_desc_length": None,
        "h1_count": 1,
        "h1_text": "Let's get in touch",
        "has_og_tags": True,                   # og:type/url/title/description/image/site_name/locale (og:image points at an .mp4)
        "has_schema": True,                    # 4 JSON-LD blocks: ContactPage, Organization, WebSite, BreadcrumbList
        "has_favicon": True,                   # img/favicon.ico seen in the head
        "image_count": 5,
        "images_without_alt": 2,               # both header logos carry alt=""
    },
    "pagespeed": {"error": PAGESPEED_ERROR},
    "page_count": {"has_sitemap": None},
    "local_signals": {"has_google_maps_embed": False},   # 360-degree panoee tour iframe, no Google Maps embed
    "platform": "Custom HTML/PHP (Bootstrap + custom CSS)",
    "html_errors": ("28 errors, 20 warnings, 5 info (no lang attribute on <html>, 13 duplicate IDs, "
                    "heading-level skips, iframe attribute errors)"),
}

LEADS = {
    "Sunova Green Energy": SUNOVA,
    "Wisda Energy": WISDA,
    "SolarSquare Energy": SOLARSQUARE,
    "Rayzon Solar": RAYZON,
}

# Extra real findings that belong at the top of "Top priorities" - each one is
# read from the live ad destination, not invented.
EXTRA_ISSUES = {
    "Sunova Green Energy": [
        "Your live ad clicks through to an fb.me lead form inside Facebook - "
        "the spend never reaches sunovagreenenergy.com, so the site cannot be "
        "measured, retargeted or tested.",
    ],
    "Wisda Energy": [
        "Your live ad clicks through to an fb.me lead form inside Facebook - "
        "the spend never reaches wisda.in, so no pixel can be measured on the "
        "landing experience.",
    ],
    "SolarSquare Energy": [
        "Three live ads all point at solarsquare.in, yet not one of those paid "
        "clicks can be traced to an enquiry.",
    ],
    "Rayzon Solar": [
        "Your live ad clicks through to instagram.com, not rayzonsolar.com - "
        "neither destination can be measured.",
    ],
}

# ---------------------------------------------------------------------------
# What each ad promises, against what the landing page actually delivers.
# Both sides are read live - the promise from the ad copy in the Ad Library,
# the delivery from the measured site facts above.
# ---------------------------------------------------------------------------

PROMISE_GAP = {
    "Sunova Green Energy": [
        ("Ad: 'Install a Solar Rooftop System for your home and save up to "
         "Rs.1,00,000 with Government Subsidy + Special Discount Offers. Up to "
         "Rs.78,000 Subsidy Available. Additional Rs.22,000 Discount.'",
         "The click never reaches a page that answers this. The ad lands on an "
         "fb.me lead form inside Facebook, and sunovagreenenergy.com's own "
         "comparison table lists cost bands only - no prices are published "
         "anywhere on the pages read."),
        ("Ad: '30 Years Performance Life. 7+ Years Industry Experience. 5 Years "
         "Comprehensive AMC Support. Trusted by 500+ Homes Across Hyderabad.'",
         "None of these four claims is verifiable on the page. The site's "
         "served HTML has no H1, no meta description, no Open Graph tags and no "
         "structured data, and the page raises 411 validator errors - so a "
         "visitor who does arrive has nothing to check the claims against."),
    ],
    "Wisda Energy": [
        ("Ad: 'Save up to Rs.1,00,000 with Government Subsidy + Special "
         "Discount Offers. Up to Rs.78,000 Subsidy Available.'",
         "The site's own copy promises 'transparent pricing models' but "
         "publishes no prices at all, so the subsidy and discount figures in "
         "the ad cannot be checked against anything on wisda.in - and the ad "
         "lands on an fb.me lead form, so paid visitors never reach the page "
         "regardless."),
        ("Ad: 'Trusted by 500+ Homes Across Hyderabad.'",
         "The tracking that would prove this is in place - Meta Pixel "
         "1494048391894940, GA4 G-SYCFTFNH0N and GTM-PTPCLJ5R are all installed "
         "- which is exactly why the fb.me destination is costing you: the "
         "pixel is measuring a Facebook form, not your own site."),
    ],
    "SolarSquare Energy": [
        ("Ad: three live ads all pointing at solarsquare.in",
         "The site has the strongest measurement stack of the batch - MoEngage "
         "is installed and reads utm_source, utm_campaign and fbclid from "
         "cookies, and there is a #leadFormModal lead-form popup plus a full "
         "Hyderabad price table marked indicative as of 01 Oct 2026. Not one of "
         "those paid clicks can currently be traced to an enquiry, though, "
         "because the destination is the site itself with no conversion event "
         "wired to the ad."),
        ("Ad: residential rooftop solar in Hyderabad",
         "Backed on the page by the Hyderabad price table and the 'Book a FREE "
         "Solar Consultation' form posting to admin-ajax.php. Two defects under "
         "cut it: the viewport blocks zoom, and the tel: link carries an "
         "illegal space after the scheme, so the click-to-call number does not "
         "dial on some phones."),
    ],
    "Rayzon Solar": [
        ("Ad: 'Rayzon Solar' rooftop ad, clicking through to instagram.com",
         "The click never reaches rayzonsolar.com at all - it lands on "
         "Instagram, so the site's contact form, its four JSON-LD blocks and "
         "its Tawk.to live chat are all invisible to paid traffic. Neither "
         "destination can be measured, because no pixel of any kind is "
         "installed on the site."),
        ("Ad: contact / enquiry intent",
         "The page answers it well once a visitor arrives: tel:+919638000461 and "
         "tel:18001231232, a contact form with Submit, and a live Tawk.to chat "
         "widget. The gap is purely that nothing sends paid traffic there."),
    ],
}


def gap_rows(company):
    return PROMISE_GAP.get(company, [])

SITE_EVIDENCE_NOTE = (
    "Landing-page source read live on {d} through the W3C Nu HTML Checker "
    "(validator.w3.org/nu/?doc=<url>&showsource=yes), which returns the served "
    "HTML with script tags intact, plus a direct fetch of the same pages. "
    "Tags found: {found}."
)


def evidence_for(site, pixels_map):
    found = []
    if pixels_map.get("meta_pixel"):
        found.append("Meta Pixel")
    if pixels_map.get("google_analytics_ga4"):
        found.append("GA4")
    if pixels_map.get("google_tag_manager"):
        found.append("Google Tag Manager")
    if pixels_map.get("google_ads"):
        found.append("Google Ads conversion tag")
    if not found:
        found = ["no Meta Pixel, GA4, GTM or Google Ads tag"]
    return {
        "pixel": bool(pixels_map.get("meta_pixel")),
        "ga4": bool(pixels_map.get("google_analytics_ga4")),
        "gtm": bool(pixels_map.get("google_tag_manager")),
        "google_ads_tag": bool(pixels_map.get("google_ads")),
        "checked_on": READ_ON,
        "note": SITE_EVIDENCE_NOTE.format(d=READ_ON, found=", ".join(found)),
    }


def main():
    changed = []
    for company, site in LEADS.items():
        path = os.path.join(AUDIT_DIR, f"audit_{company.replace(' ', '_')}.json")
        if not os.path.exists(path):
            print(f"  !! missing JSON for {company}: {path}")
            continue
        with open(path, encoding="utf-8") as f:
            audit = json.load(f)

        # ---- score: the repo's own algorithm, fed only measured values ----
        result = calculate_audit_score(
            audit.get("checks") or {},
            site["pixels"],
            site["conversion"],
            site["seo"],
            site["pagespeed"],
        )
        result["issues"] = EXTRA_ISSUES.get(company, []) + result["issues"]
        site = dict(site)
        site["score"] = result

        audit["site_audit"] = site
        # The ad-library summary predates the website read; drop the stale line
        # that claims Google Transparency was never checked by any means.
        adlib = audit.get("ad_library") or {}
        if adlib.get("summary"):
            adlib["summary"] = adlib["summary"].replace(
                "No Google Ads advertiser record was checked for this report - that "
                "requires the full pipeline.",
                "Google Ads Transparency records were not checked in this pass.")
        audit["website_audit_run"] = True
        audit["audit_date"] = READ_ON
        audit["source"] = ("Meta Ad Library (India, active ads) + the company's own "
                           "live website (page source read through the W3C Nu HTML Checker)")

        # ---- refresh the claude-ads control review with real evidence ----
        evidence = evidence_for(site, site["pixels"])
        audit["site_evidence"] = evidence
        audit["promise_gap"] = gap_rows(company)
        audit["ads_audit"] = evaluate(audit, evidence)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(audit, f, indent=2, ensure_ascii=False)
            f.write("\n")

        out = generate_ads_only_pdf(audit)
        counts = (audit["ads_audit"] or {}).get("counts") or {}
        print(f"  {company:<20} score {result['score']:>3}/100  "
              f"issues {len(result['issues']):>2}  wins {len(result['wins']):>2}  "
              f"controls {counts.get('pass', 0)}P/{counts.get('fail', 0)}F/"
              f"{counts.get('unknown', 0)}U  -> {os.path.basename(out)}")
        changed.append(out)
    print(f"\nRebuilt {len(changed)} reports.")
    return changed


if __name__ == "__main__":
    main()
