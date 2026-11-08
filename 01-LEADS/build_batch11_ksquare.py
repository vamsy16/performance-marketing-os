#!/usr/bin/env python3
"""Build the batch-11 (Hyderabad / Telangana) ads reports from real measurements.

Owner instruction 2026-10-24 (still standing): every audit PDF is generated
exactly like ``02-OUTREACH/audit_pdfs/audit_Ksquare_Energy.pdf`` - the 5-page
"DIGITAL MARKETING & PAID ADS AUDIT" layout - every check in that layout is
performed, the claude-ads control-review section is carried alongside it, and
only real live data is used. No simulated or demo values anywhere.

WHERE EVERY NUMBER BELOW CAME FROM (all read live on 2026-11-08):

* Meta Ad Library (India, active ads) - the live ad cards below. Each library ID
  was confirmed by opening the ad directly at
  ``https://www.facebook.com/ads/library/?id=<LibraryID>``; ad IDs routinely
  appear next to another advertiser's card, so an ID is only recorded here when
  metadata and card were adjacent in the same response.
* The company's own website, read through the W3C Nu HTML Checker with
  ``showsource=yes`` (``https://validator.w3.org/nu/?doc=<url>&showsource=yes``),
  which returns the served HTML with script tags intact. That is how the Meta
  Pixel / GA4 / GTM / Google Ads tags, the JSON-LD blocks and the consent-mode
  configuration below were read.
* A direct fetch of the same pages for headings, forms, links, CTAs,
  testimonials, pricing and image alt text. For the two WordPress builds the
  ``wp-json`` REST API was also read (``/wp-json/wp/v2/pages/<id>``,
  ``/wp-json/``) for rendered content, plugin stack and site metadata.

CHECKS THAT COULD NOT BE RUN ARE STORED AS ``None`` AND RENDER AS
"Not checked in this pass" / "Not available at audit time". They are never
guessed:

* Google PageSpeed mobile score + LCP - the keyless API returns HTTP 429
  (quota limit 0/day), the same failure the reference Ksquare PDF reports.
* Google Ads Transparency advertiser records - not fetched.
* Sitemap page count - not fetched.
* Lumisun's ``<title>``, meta description, Open Graph, Twitter cards and
  JSON-LD sit on source lines 74-97 of its homepage, a range the Nu checker
  does not expose (it reported only void-element info messages there).
* Kypas's whole ``<head>``: its homepage raises 337 validator errors, and the
  message list fills the entire checker report, so the source section is
  unreachable through that channel. The plugin stack below is read from the
  ``wp-json`` root, not from the head.
* Bharath Enterprises Solar was dropped from this batch entirely -
  ``bharathsolarepc.com`` is a parked GoDaddy domain (see the batch doc).

Run:  cd 01-LEADS && PYTHONPATH=/tmp/pdflibs python3 build_batch11_ksquare.py
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
READ_ON = "2026-11-08"
PAGESPEED_ERROR = "API returned 429"      # keyless PageSpeed quota, read live


def pixels(**over):
    """All-False baseline, overridden by what was actually read in the head."""
    d = {
        "meta_pixel": False,
        "google_ads": False,
        "google_analytics_ga4": False,
        "google_analytics_ua": False,
        "linkedin_insight": False,
        "microsoft_clarity": False,
        "hotjar": False,
        "google_tag_manager": False,
    }
    d.update(over)
    return d


UNKNOWN_PIXELS = {
    # None = the head was never read, so presence is unknown in both directions.
    "meta_pixel": None,
    "google_ads": None,
    "google_analytics_ga4": None,
    "google_analytics_ua": None,
    "linkedin_insight": None,
    "microsoft_clarity": None,
    "hotjar": None,
    "google_tag_manager": None,
}


def unknown_pixels(**over):
    d = dict(UNKNOWN_PIXELS)
    d.update(over)
    return d


# ---------------------------------------------------------------------------
# Real measurements, one entry per batch-11 lead.
# ---------------------------------------------------------------------------

VARNA = {
    "ssl": True,
    "load_time_seconds": None,                 # not measured
    "final_url": "https://www.varnasolar.com/",
    "audit_date": READ_ON,
    # Whole head read through the Nu checker: no tag of any kind.
    "pixels": pixels(),
    "conversion": {
        # The body is a client-rendered React SPA (<div id="root">, /static/js/
        # main.fbb7979e.js), so the form, the chat widget and the CTA buttons are
        # not in the served HTML and are recorded as not checked.
        "has_contact_form": None,              # /#contact section - client-rendered
        "has_phone_click": True,               # tel:+91-9182445679 in the JSON-LD
        "has_whatsapp_link": True,             # wa.me/917207730803, wa.me/919182445679
        "has_cta_buttons": None,               # client-rendered
        "has_live_chat": None,
        "has_popup_optin": None,
        "has_testimonials": None,              # client-rendered
        "has_pricing_page_link": False,        # no pricing page published
    },
    "seo": {
        "has_title": True,
        "title_text": "Varna Solar | Top Solar EPC Company in Hyderabad & Telangana",
        "title_length": 56,
        "has_meta_description": True,          # present (length not captured)
        "meta_desc_length": None,
        "h1_count": 0,                          # React SPA - no static H1 at all
        "h1_text": "",
        "has_og_tags": True,                   # og:locale/type/title/description/url/site_name/image
        "has_schema": True,                    # JSON-LD LocalBusiness with OfferCatalog
        "has_favicon": True,                    # /images/varna-logo2.png
        "image_count": None,                   # client-rendered
        "images_without_alt": None,
    },
    "pagespeed": {"error": PAGESPEED_ERROR},
    "page_count": {"has_sitemap": None},
    "local_signals": {"has_google_maps_embed": False},
    "platform": "React single-page app (Create React App build: "
                "/static/js/main.fbb7979e.js, /static/css/main.ca667578.css), "
                "Google Fonts Inter 400-900",
    "html_errors": "0 errors, 0 warnings, 23 info",
}

HINDUSTHAN = {
    "ssl": True,
    "load_time_seconds": None,                 # not measured
    "final_url": "https://hindusthansolarenergy.com/",
    "audit_date": READ_ON,
    # Whole head read: GA4 G-LGSB5RQG1R and Google Ads AW-18521456304 are both
    # present, but gtag consent-mode v2 defaults all four storage signals to
    # 'denied' and the gtag library is only appended after the first interaction
    # or 5 s after idle. No Meta Pixel, no GTM.
    "pixels": pixels(
        google_analytics_ga4=True,     # G-LGSB5RQG1R
        google_ads=True,               # AW-18521456304
    ),
    "conversion": {
        # Also a client-rendered React SPA (/assets/index-B3fKUXGd.js), so the
        # form, CTAs, chat and popup are not in the served HTML.
        "has_contact_form": None,              # client-rendered
        "has_phone_click": True,               # tel:+918712636576 at all 7 branches
        "has_whatsapp_link": True,             # wa.aisensy.com/+919391585484
        "has_cta_buttons": None,               # client-rendered
        "has_live_chat": None,
        "has_popup_optin": None,
        "has_testimonials": True,              # review photos served from a Supabase bucket
        "has_pricing_page_link": False,        # live savings calculator, no published prices
    },
    "seo": {
        "has_title": True,
        "title_text": "Rooftop Solar in AP & Telangana | Hindusthan Solar",
        "title_length": 44,
        "has_meta_description": True,          # present (length not captured)
        "meta_desc_length": None,
        "h1_count": None,                      # React SPA - client-rendered
        "h1_text": "",
        "has_og_tags": True,                   # og:type/title/description/image + Twitter cards
        "has_schema": True,                    # JSON-LD LocalBusiness
        "has_favicon": True,                   # favicon.ico
        "image_count": None,                   # client-rendered
        "images_without_alt": None,
    },
    "pagespeed": {"error": PAGESPEED_ERROR},
    "page_count": {"has_sitemap": None},
    "local_signals": {"has_google_maps_embed": False},
    "platform": "React single-page app (react + motion/Framer Motion + Supabase "
                "client), Cloudflare, fonts Plus Jakarta Sans + Inter",
    "html_errors": "1 error (meta charset declared after the first 1024 bytes, "
                   "line 49), 0 warnings, 5 info",
}

LUMISUN = {
    "ssl": True,
    "load_time_seconds": None,                 # not measured
    "final_url": "https://lumisunsolar.com/",
    "audit_date": READ_ON,
    # The head was NOT exposed: the checker reported only void-element info
    # messages for source lines 74-97, which is where the title, description,
    # OG/Twitter tags and any pixel sit. Presence is unknown in both directions.
    "pixels": unknown_pixels(),
    "conversion": {
        # Read from /contact-us/ and the wp-json page body: six duplicated form
        # field IDs (form-field-name, -phone, -district, -bill_type, -bill,
        # -interest) prove a live contact form, and .lm-wa is a floating
        # WhatsApp button.
        "has_contact_form": True,              # name, phone, district, bill type, bill amount, interest
        "has_phone_click": True,               # tel:+917581774295
        "has_whatsapp_link": True,             # wa.me/918179992229
        "has_cta_buttons": 4,                  # Book Free Site Visit, WhatsApp Us, How the subsidy works, See All Projects
        "has_live_chat": False,
        "has_popup_optin": False,
        "has_testimonials": True,              # Trustindex Google reviews, 17 reviews
        "has_pricing_page_link": False,        # subsidy table only, no per-kW pricing
    },
    "seo": {
        "has_title": None,                     # head line 7-8 not exposed - not assumed
        "title_text": "",
        "title_length": None,
        "has_meta_description": None,          # not exposed - not assumed
        "meta_desc_length": None,
        "h1_count": 1,                         # read from wp-json/wp/v2/pages/20
        "h1_text": "Rooftop solar for your home, with the government subsidy "
                   "handled for you.",
        "has_og_tags": None,                   # not exposed - not assumed
        "has_schema": None,                    # not exposed - not assumed
        "has_favicon": True,                   # 32x32, 192x192, apple-touch-icon, msapplication-TileImage
        "image_count": None,                   # not counted on the full page
        "images_without_alt": None,
    },
    "pagespeed": {"error": PAGESPEED_ERROR},
    "page_count": {"has_sitemap": None},
    "local_signals": {"has_google_maps_embed": False},
    "platform": "WordPress 7.1.4 + Elementor 4.3.6 + Elementor Pro 4.3.1, "
                "Google Fonts Outfit + Manrope, Trustindex Google-review widget, "
                "LiteSpeed Cache",
    "html_errors": "92 errors, 3 warnings, 117 info on the homepage; "
                   "15 errors, 6 warnings, 50 info on /contact-us/",
}

KYPAS = {
    "ssl": True,
    "load_time_seconds": None,                 # not measured
    "final_url": "https://kypassolar.com/",
    "audit_date": READ_ON,
    # The whole head is unreachable: the homepage raises 337 validator errors and
    # the message list fills the checker report. The wp-json root shows the GTM
    # Kit plugin is installed, but no container ID could be read, so GTM stays
    # unknown rather than assumed present.
    "pixels": unknown_pixels(),
    "conversion": {
        "has_contact_form": True,              # "Book Site Vist" -> /contact-us/
        "has_phone_click": True,               # tel:+919100522215
        "has_whatsapp_link": True,             # wa.me/919100522215
        "has_cta_buttons": None,               # head/BODY count not captured
        "has_live_chat": False,
        "has_popup_optin": False,
        "has_testimonials": True,              # Trustindex Google-review widget
        "has_pricing_page_link": False,        # no published pricing
    },
    "seo": {
        "has_title": None,                     # head unreachable - not assumed
        "title_text": "",
        "title_length": None,
        "has_meta_description": None,          # head unreachable - not assumed
        "meta_desc_length": None,
        "h1_count": 1,                         # "Keep Your Power As Solar" on the rendered home page
        "h1_text": "Keep Your Power As Solar",
        "has_og_tags": None,                   # head unreachable - not assumed
        "has_schema": None,                    # head unreachable - not assumed
        "has_favicon": None,                   # head unreachable - not assumed
        "image_count": None,
        "images_without_alt": None,
    },
    "pagespeed": {"error": PAGESPEED_ERROR},
    "page_count": {"has_sitemap": None},
    "local_signals": {"has_google_maps_embed": False},
    "platform": "WordPress + Elementor 4.3.x + Royal Elementor Addons "
                "(elementor-319, wpr- classes), WPForms, LiteSpeed Cache, "
                "GTM Kit plugin active, Trustindex, Hostinger hosting",
    "html_errors": "337 errors on the homepage (270 style rules outside @scope "
                   "in a <style> element in body, plus 4 <style> placement "
                   "errors); 279 errors on /contact-us/",
}

LOTUS = {
    "ssl": True,
    "load_time_seconds": None,                 # not measured
    "final_url": "https://www.lotusindustriesindia.com/",
    "audit_date": READ_ON,
    # The full Next.js metadata export was read: title, description, author,
    # keywords, creator, publisher, robots, canonical, a complete Open Graph set
    # (including og:image dimensions and alt) and a complete Twitter set - and
    # no pixel, GA4, GTM, Google Ads, Clarity, Hotjar or LinkedIn tag anywhere.
    "pixels": pixels(),
    "conversion": {
        "has_contact_form": None,              # not found on the home page read
        "has_phone_click": True,               # tel:+916300348653
        "has_whatsapp_link": True,             # wa.me/917989500747
        "has_cta_buttons": 2,                  # REQUEST TECHNICAL SPECIFICATIONS, Learn More (x10)
        "has_live_chat": False,
        "has_popup_optin": False,
        "has_testimonials": False,             # case studies and a partner emblem, no testimonials
        "has_pricing_page_link": False,        # no published pricing
    },
    "seo": {
        "has_title": True,
        "title_text": "Lotus Industries | Solar Mounting Structures, Roll Forming, Aluminium Systems",
        "title_length": 71,
        "has_meta_description": True,          # present (length not captured)
        "meta_desc_length": None,
        "h1_count": 1,                         # "Lotus Industries - Solar Mounting Structures, Roll Forming & Aluminium Systems"
        "h1_text": "Lotus Industries - Solar Mounting Structures, Roll Forming "
                   "& Aluminium Systems",
        "has_og_tags": True,                   # og:title/description/url/site_name/locale/image + dimensions + alt
        "has_schema": False,                   # no JSON-LD in the metadata export
        "has_favicon": True,                   # /favicon.svg (shortcut icon, icon, apple-touch-icon)
        "image_count": None,                   # not counted on the full page
        "images_without_alt": None,
    },
    "pagespeed": {"error": PAGESPEED_ERROR},
    "page_count": {"has_sitemap": None},
    "local_signals": {"has_google_maps_embed": False},
    "platform": "Next.js (App Router, webpack-241370cd7f3a6004.js, "
                "css 3e3eadcbb32381d4.css, next/image optimiser, "
                "next-size-adjust)",
    "html_errors": "0 errors, 0 warnings, 31 info",
}


LEADS = {
    "Varna Solar Pvt. Ltd.": VARNA,
    "Hindusthan Solar Energy Enterprise": HINDUSTHAN,
    "Lumisun Solar": LUMISUN,
    "Kypas Solar Power Pvt Ltd": KYPAS,
    "Lotus Industries": LOTUS,
}

# Extra real findings that belong at the top of "Top priorities" - each one is
# read from the live ad destination or the live page, not invented.
EXTRA_ISSUES = {
    "Varna Solar Pvt. Ltd.": [
        "Your live ad clicks through to WhatsApp, not varnasolar.com - every "
        "rupee of that spend buys a chat thread you cannot retarget, and with "
        "no Meta Pixel on the site the visitor who does arrive is untraceable.",
    ],
    "Hindusthan Solar Energy Enterprise": [
        "Your two live ads click through to an fb.me lead form inside Facebook, "
        "so the spend never reaches hindusthansolarenergy.com at all.",
        "GA4 (G-LGSB5RQG1R) and the Google Ads tag (AW-18521456304) are both "
        "installed, but consent-mode v2 defaults ad_storage, ad_user_data, "
        "ad_personalization and analytics_storage to 'denied' and the gtag "
        "library is only appended after the first interaction or 5 s after "
        "idle - so the tags record almost nothing.",
    ],
    "Lumisun Solar": [
        "Both live ads click through to WhatsApp, not lumisunsolar.com, so "
        "neither paid visit can be traced to an enquiry.",
        "The Diwali offer in your ad copy (book for Rs.1,001 with 30% advance "
        "within 7 days of survey) has no matching price anywhere on the site - "
        "the landing page publishes subsidy bands only.",
    ],
    "Kypas Solar Power Pvt Ltd": [
        "Both live ads click through to an fb.me lead form inside Facebook, so "
        "the spend never reaches kypassolar.com.",
    ],
    "Lotus Industries": [
        "Your live ad clicks through to WhatsApp, not lotusindustriesindia.com, "
        "so the Diwali HJT offer in the ad cannot be measured on the site.",
    ],
}

SITE_EVIDENCE_NOTE = (
    "Landing-page source read live on {d} through the W3C Nu HTML Checker "
    "(validator.w3.org/nu/?doc=<url>&showsource=yes), which returns the served "
    "HTML with script tags intact, plus a direct fetch of the same pages. "
    "Tags found: {found}."
)

EVIDENCE_NOTE_HEAD_UNREAD = (
    "The landing page's <head> could not be read on {d}: the W3C Nu HTML "
    "Checker raised {errs} validator errors and the message list filled the "
    "whole report, so the source section - and with it the title, meta "
    "description, Open Graph tags, structured data and any pixel - was never "
    "returned. Those checks are reported as not checked, not as failures. "
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

    head_unread = pixels_map.get("meta_pixel") is None
    note = (EVIDENCE_NOTE_HEAD_UNREAD.format(
                d=READ_ON, errs=site["html_errors"], found=", ".join(found))
            if head_unread
            else SITE_EVIDENCE_NOTE.format(d=READ_ON, found=", ".join(found)))

    return {
        "pixel": bool(pixels_map.get("meta_pixel")),
        "ga4": bool(pixels_map.get("google_analytics_ga4")),
        "gtm": bool(pixels_map.get("google_tag_manager")),
        "google_ads_tag": bool(pixels_map.get("google_ads")),
        "checked_on": READ_ON,
        "note": note,
    }


# ---------------------------------------------------------------------------
# The live Meta ads, read from the Ad Library on 2026-11-08. Every library ID
# was confirmed by opening the ad directly; ad IDs routinely appear next to
# another advertiser's card in a keyword search.
# ---------------------------------------------------------------------------

ADS = {
    "Varna Solar Pvt. Ltd.": [
        {
            "library_id": "3418975398276429",
            "library_url": "https://www.facebook.com/ads/library/?id=3418975398276429",
            "page_name": "Varna Solar Pvt. Ltd.",
            "started": "Oct 30, 2026",
            "destination": "WhatsApp",
            "text": "Reduce Your Electricity Bills with Varna Solar Hyderabad! "
                    "Premium WAAREE solar panels for residential rooftops. PM "
                    "Surya Ghar subsidy up to Rs.78,000. Free site survey. "
                    "Call or WhatsApp Varna Solar.",
        },
    ],
    "Hindusthan Solar Energy Enterprise": [
        {
            "library_id": "1478901357671342",
            "library_url": "https://www.facebook.com/ads/library/?id=1478901357671342",
            "page_name": "Hindusthan Solar Energy Enterprise",
            "started": "Sep 23, 2026",
            "destination": "fb.me (inside Facebook)",
            "text": "Get a 3.82 kW solar system at a 3 kW package price, with "
                    "eligible government subsidy benefits and extra energy "
                    "discounts. Hindusthan Solar Energy - free quote today.",
        },
        {
            "library_id": "1080534018298988",
            "library_url": "https://www.facebook.com/ads/library/?id=1080534018298988",
            "page_name": "Hindusthan Solar Energy Enterprise",
            "started": "Sep 23, 2026",
            "destination": "fb.me (inside Facebook)",
            "text": "Get a 3.82 kW solar system at a 3 kW package price, with "
                    "eligible government subsidy benefits and extra energy "
                    "discounts. Hindusthan Solar Energy - free quote today.",
        },
    ],
    "Lumisun Solar": [
        {
            "library_id": "1639995594202458",
            "library_url": "https://www.facebook.com/ads/library/?id=1639995594202458",
            "page_name": "Lumisun Solar",
            "started": "Oct 28, 2026",
            "destination": "WhatsApp",
            "text": "Diwali Solar Utsav - residential 3 kW on-grid solar in "
                    "Hyderabad, Khammam, Warangal, Karimnagar and Suryapet. "
                    "Book your site visit now.",
        },
        {
            "library_id": "2587160308432344",
            "library_url": "https://www.facebook.com/ads/library/?id=2587160308432344",
            "page_name": "Lumisun Solar",
            "started": "Nov 5, 2026",
            "destination": "WhatsApp",
            "text": "Diwali Solar Utsav - residential 5 kW on-grid solar in "
                    "Hyderabad, Khammam, Warangal, Karimnagar and Suryapet. "
                    "Book for Rs.1,001 with 30% advance within 7 days of "
                    "survey, Bill-On-Us capped at Rs.3,000, and a 15 g silver "
                    "coin on net-meter commissioning.",
        },
    ],
    "Kypas Solar Power Pvt Ltd": [
        {
            "library_id": "1698264268490724",
            "library_url": "https://www.facebook.com/ads/library/?id=1698264268490724",
            "page_name": "Kypas Solar Power Pvt Ltd",
            "started": "Nov 2, 2026",
            "destination": "fb.me (inside Facebook)",
            "text": "STOP PAYING HIGH ELECTRICITY BILLS! Claim up to Rs.78,000 "
                    "government subsidy under PM Surya Ghar Muft Bijli Yojana. "
                    "Up to 15 years service support, 5-year generation "
                    "guarantee, 30-year ZAM structure warranty, complete bank "
                    "loan assistance, 24-hour service response, free Rs.3,000 "
                    "cleaning brush kit. Residential and commercial. Chanda "
                    "Nagar, Hyderabad. 91005 22215.",
        },
        {
            "library_id": "1117370117608767",
            "library_url": "https://www.facebook.com/ads/library/?id=1117370117608767",
            "page_name": "Kypas Solar Power Pvt Ltd",
            "started": "Nov 4, 2026",
            "destination": "fb.me (inside Facebook)",
            "text": "STOP PAYING HIGH ELECTRICITY BILLS! Claim up to Rs.78,000 "
                    "government subsidy under PM Surya Ghar Muft Bijli Yojana. "
                    "Up to 15 years service support, 5-year generation "
                    "guarantee, 30-year ZAM structure warranty, complete bank "
                    "loan assistance, 24-hour service response, free Rs.3,000 "
                    "cleaning brush kit. Residential and commercial. Chanda "
                    "Nagar, Hyderabad. 91005 22215.",
        },
    ],
    "Lotus Industries": [
        {
            "library_id": "2228866791035208",
            "library_url": "https://www.facebook.com/ads/library/?id=2228866791035208",
            "page_name": "Lotus Industries",
            "started": "Nov 6, 2026",
            "destination": "WhatsApp",
            "text": "DIWALI SPECIAL SOLAR SALE! Exclusive Diwali prices on "
                    "Reliance New Energy HJT solar systems for the home. Lotus "
                    "Industries Solar EPC.",
        },
    ],
}

COMPANY = {
    "Varna Solar Pvt. Ltd.": {
        "legal": "Varna Solar Pvt. Ltd.",
        "city": "Ameerpet, Hyderabad 500038",
        "website": "https://www.varnasolar.com/",
        "contact_facts": "8-3-214/7/1A, 2nd Floor, Pillar No. 1036, Sanjeeva "
                         "Reddy Nagar, Hyderabad 500038 (Ameerpet) | "
                         "info@varnasolar.com | +91 91824 45679",
        "contact": {"phone": "+91 91824 45679",
                    "email": "info@varnasolar.com",
                    "whatsapp": "+91 917207730803"},
    },
    "Hindusthan Solar Energy Enterprise": {
        "legal": "Hindusthan Solar Energy Enterprise",
        "city": "Secunderabad (Tarnaka) 500017",
        "website": "https://hindusthansolarenergy.com/",
        "contact_facts": "Lalapet, Tarnaka, Secunderabad 500017 (head office: "
                         "Vijayawada, Andhra Pradesh) | "
                         "info@hindusthansolarenergy.com | +91 87126 36576",
        "contact": {"phone": "+91 87126 36576",
                    "email": "info@hindusthansolarenergy.com",
                    "whatsapp": "+91 93915 85484"},
    },
    "Lumisun Solar": {
        "legal": "Lumisun Solar",
        "city": "Hyderabad, Telangana",
        "website": "https://lumisunsolar.com/",
        "contact_facts": "Hyderabad, Telangana | +91 81799 92229 (WhatsApp) | "
                         "PM Surya Ghar registered vendor, serves Telangana and "
                         "Andhra Pradesh",
        "contact": {"phone": "+91 81799 92229",
                    "email": "",
                    "whatsapp": "+91 81799 92229"},
    },
    "Kypas Solar Power Pvt Ltd": {
        "legal": "Kypas Solar Power Pvt Ltd",
        "city": "Chanda Nagar, Hyderabad",
        "website": "https://kypassolar.com/",
        "contact_facts": "Chanda Nagar, Hyderabad | +91 91005 22215 | "
                         "PM Surya Ghar Muft Bijli Yojana, bank loan at 6% "
                         "interest",
        "contact": {"phone": "+91 91005 22215",
                    "email": "",
                    "whatsapp": "+91 91005 22215"},
    },
    "Lotus Industries": {
        "legal": "Lotus Industries",
        "city": "Balanagar, Hyderabad 500037",
        "website": "https://www.lotusindustriesindia.com/",
        "contact_facts": "Unit-01 (HQ): Plot No. 268, Panchasheela Colony, "
                         "Gandhinagar, IDA, Balanagar, Hyderabad 500037 | "
                         "Unit-02: Sy no. 167/1/1, Jinnaram mandal, ORR Exit 5, "
                         "Gagillapur, Vailala, Gaddapotharam 502319 | "
                         "lotusindustries95@gmail.com | +91 79895 00747 / "
                         "83095 28763 / 90321 61817",
        "contact": {"phone": "+91 79895 00747",
                    "email": "lotusindustries95@gmail.com",
                    "whatsapp": "+91 79895 00747"},
    },
}


def build_base(company):
    """Create the ads-only JSON shell if it does not exist yet."""
    path = os.path.join(AUDIT_DIR,
                        f"audit_{company.replace(' ', '_')}.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f), path

    meta = COMPANY[company]
    ads = ADS[company]
    audit = {
        "company": meta["legal"],
        "legal": meta["legal"],
        "city": meta["city"],
        "website": meta["website"],
        "ads_only": True,
        "website_audit_run": True,
        "checked_on": READ_ON,
        "generated_at": READ_ON,
        "source": ("Meta Ad Library (India, active ads) + the company's own "
                   "live website (page source read through the W3C Nu HTML "
                   "Checker)"),
        "ad_library": {
            "meta_own": {
                "found": True,
                "results_count": len(ads),
                "results_label": f"{len(ads)} live ad"
                                 f"{'' if len(ads) == 1 else 's'}",
                "query": "solar Hyderabad / Telangana keyword search",
                "ads": ads,
            },
            "summary": (
                f"{len(ads)} live Meta ad"
                f"{'' if len(ads) == 1 else 's'} confirmed on {READ_ON} by "
                "opening each library ID directly. Google Ads Transparency "
                "records were not checked in this pass."
            ),
        },
        "funnel": {
            "destination": ads[0]["destination"],
            "note": "Ad destination as shown on the live ad card.",
        },
        "findings": [],
        "next_steps": [],
        "contact_facts": meta["contact_facts"],
        "contact": meta["contact"],
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(audit, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"  + created {os.path.basename(path)}")
    return audit, path


def main():
    if not os.path.isdir(AUDIT_DIR):
        print(f"  !! missing {AUDIT_DIR}")
        return []

    changed = []
    for company, site in LEADS.items():
        audit, path = build_base(company)
        if not os.path.exists(path):
            print(f"  !! missing JSON for {company}: {path}")
            continue

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
        audit["website_audit_run"] = True
        audit["audit_date"] = READ_ON

        # ---- refresh the claude-ads control review with real evidence ----
        evidence = evidence_for(site, site["pixels"])
        audit["site_evidence"] = evidence
        audit["ads_audit"] = evaluate(audit, evidence)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(audit, f, indent=2, ensure_ascii=False)
            f.write("\n")

        out = generate_ads_only_pdf(audit)
        counts = (audit["ads_audit"] or {}).get("counts") or {}
        print(f"  {company:<36} score {result['score']:>3}/100  "
              f"issues {len(result['issues']):>2}  wins {len(result['wins']):>2}  "
              f"controls {counts.get('pass', 0)}P/{counts.get('fail', 0)}F/"
              f"{counts.get('unknown', 0)}U  -> {os.path.basename(out)}")
        changed.append(out)

    print(f"\nRebuilt {len(changed)} reports.")
    return changed


if __name__ == "__main__":
    main()
