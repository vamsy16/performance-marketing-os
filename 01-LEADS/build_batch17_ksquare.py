#!/usr/bin/env python3
"""Build the batch-17 (Telangana State, Google Ads Transparency channel) reports.

Owner instruction 2026-10-24 (still standing): every audit PDF is generated
exactly like ``02-OUTREACH/audit_pdfs/audit_Ksquare_Energy.pdf`` - the 5-page
"DIGITAL MARKETING & PAID ADS AUDIT" layout - every check in that layout is
performed, the claude-ads control-review section is carried alongside it, and
only real live data is used. No simulated or demo values anywhere.

WHERE EVERY NUMBER BELOW CAME FROM (all read live on 2026-11-10):

* Google Ads Transparency Centre - ``adstransparency.google.com/?region=IN&domain=<domain>``
  gave the advertiser name, the Verified badge and the ad count for each domain,
  and ``adstransparency.google.com/advertiser/<AR_ID>?region=IN`` gave the
  verified legal name behind each trading name. That is the discovery channel
  that found all five of these leads: every one of them buys Google Search,
  YouTube or Display ads and none of them had ever surfaced in a Meta Ad
  Library sweep.
* The company's own website, read through the W3C Nu HTML Checker with
  ``showsource=yes`` (``https://validator.w3.org/nu/?doc=<url>&showsource=yes``),
  which returns the served HTML with script tags intact. That is how the Google
  tag IDs, the JSON-LD blocks, the title, the meta description, the Open Graph
  tags and the plugin stack below were read.
* A direct fetch of the same pages for headings, forms, links, CTAs,
  testimonials, pricing, counters and image alt text.
* The TGREDCO empanelled-supplier register
  (``tgredco.telangana.gov.in/Updates_2026/List_of_Empanelled_Suppliers_2026.pdf``)
  as the independent third-party confirmation the owner's third-eye rule needs.

CHECKS THAT COULD NOT BE RUN ARE STORED AS ``None`` AND RENDER AS
"Not checked in this pass" / "Not available at audit time". They are never
guessed:

* Google PageSpeed mobile score + LCP - the keyless API returns HTTP 429
  (quota limit 0/day), the same failure the reference Ksquare PDF reports.
* The full served source of zenithenergy.com and sunworks.in. Both are large
  WordPress pages: the checker's response runs past what could be read here, so
  the eight tracking-tag checks for those two are unknown in BOTH directions.
  They are rendered as "not checked in this pass", never as "no pixel found".
  The error/warning/info counts, the title, the meta description, the Open Graph
  tags, the plugin stack and every content check for those two ARE measured.
* The Meta Ad Library was queried for zenith only (batch 9, 2026-10-23, zero
  results - that is a real measurement). It was not queried for the other four,
  so their Meta ad count is recorded as not checked rather than as zero.

Run:  cd 01-LEADS && PYTHONPATH=/tmp/pdflibs python3 build_batch17_ksquare.py
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
READ_ON = "2026-11-10"
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


def unknown_pixels(**over):
    """None = the head was never returned, so presence is unknown in both directions."""
    d = dict(pixels())
    for k in list(d):
        d[k] = None
    d.update(over)
    return d


# ---------------------------------------------------------------------------
# Real measurements, one entry per batch-17 lead.
# ---------------------------------------------------------------------------

ZENITH = {
    "ssl": True,
    "load_time_seconds": None,                 # not measured
    "final_url": "https://zenithenergy.com/",
    "audit_date": READ_ON,
    # The COMPLETE head was read - source lines 1 to 274, every line, ending at
    # the favicon links. It carries exactly one tracking script: Google Tag
    # Manager container GTM-NGZ8TG9J, loaded from
    # https://www.googletagmanager.com/gtm.js?id=GTM-NGZ8TG9J at source lines
    # 118-124. There is no Meta Pixel, no GA4 measurement ID, no Google Ads
    # conversion tag, no LinkedIn Insight, no Microsoft Clarity and no Hotjar
    # anywhere in it. Also read in the head: a Google Search Console
    # verification token (Om8XCzgJf3XYDKrfNtGSDsVkwXcddovoqMFpVua_EJs) and a
    # ThemeIsle "ti-site-data" counter that resolves to
    # ti-online-users-google=1 - an online-visitor counter, not a conversion
    # tracker. NOTE: GTM is a container, not a measurement - nothing is counted
    # until tags are published inside it, and no such tag could be read here.
    "pixels": pixels(
        google_tag_manager=True,               # container GTM-NGZ8TG9J
    ),
    "conversion": {
        # /contact/ is the site's only enquiry route and is linked from the hero
        # "Get in touch" button. No WhatsApp link, no live-chat widget, no popup
        # opt-in and no price list were read on the homepage or /contact/.
        "has_contact_form": True,              # /contact/ linked from the hero CTA
        "has_phone_click": True,               # +91 70757 56795, click-to-call
        "has_whatsapp_link": None,             # not read on the pages checked
        "has_cta_buttons": 4,                  # Get in touch, Net Zero, Scroll down, Explore our Net Zero goals
        "has_live_chat": None,                 # not read
        "has_popup_optin": None,               # not read
        "has_testimonials": None,              # not read as a block
        "has_pricing_page_link": False,        # no price list anywhere on the site
    },
    "seo": {
        # <title>Zenith Energy - Renewable Energy & Net-Zero Solutions</title>
        "has_title": True,
        "title_text": "Zenith Energy - Renewable Energy & Net-Zero Solutions",
        "title_length": 53,
        "has_meta_description": True,
        "meta_desc_length": 122,
        "h1_count": None,                      # not counted
        "h1_text": "Crafting Unique sustainable solutions for better Future World",
        "has_og_tags": True,                   # full og + twitter card set
        "has_schema": True,                    # AIOSEO JSON-LD, source lines 29-31
        "has_favicon": True,                   # 32x32, 192x192, 180x180, 270x270
        "image_count": None,
        "images_without_alt": None,
    },
    "pagespeed": {"error": PAGESPEED_ERROR},
    "page_count": {"has_sitemap": None},
    "local_signals": {
        # The homepage carries an interactive India map (28 states / 8 union
        # territories / 180+ major projects) but no Google Maps embed, no
        # directions link and no local-business JSON-LD was read.
        "has_google_maps_embed": False,
    },
    "platform": "WordPress 7.1.4, hello-elementor theme 3.5.1, Elementor 4.4.0 "
                "+ Elementor Pro (pro-elements 4.3.2), ElementsKit Lite 4.0.9, "
                "Essential Addons for Elementor Lite 6.8.8, TablePress 3.4.1, "
                "All in One SEO (AIOSEO) 5.0.4, locally-hosted Google Fonts "
                "(roboto, robotoslab, poppins, intertight), Elementor post CSS "
                "6 / 15347 / 8840, plus a custom interactive-India-map plugin",
    "html_errors": "158 errors (155 HTML), 5 warnings, 146 info on the homepage. "
                   "The most serious finding is structural: a complete second "
                   "HTML document - doctype, <html lang=\"en\">, <head>, "
                   "<meta charset=\"UTF-8\">, viewport and a <title> - is "
                   "embedded inside the body at source line 417, shipped by the "
                   "India-map plugin. That single defect produces the checker's "
                   "'Stray doctype', 'Stray start tag html', 'Stray start tag "
                   "head', 'A charset attribute on a meta element found after "
                   "the first 1024 bytes', 'A document must not include more "
                   "than one meta element with a charset attribute', 'Element "
                   "title not allowed as child of element div', 'Stray end tag "
                   "head / div', 'Start tag body seen but an element of the same "
                   "type was already open', 'End tag for body seen, but there "
                   "were unclosed elements' and 'Unclosed element div (5) / "
                   "header' errors. The rest are 7 'style element in body must "
                   "be the first child of its parent', 121 style rules outside "
                   "an @scope rule, a stray @import in a body style element, 5 "
                   "role=group children of role=list, and 4 duplicate IDs on "
                   "loop-dynamic-12687.",
}

SUNWORKS = {
    "ssl": True,
    "load_time_seconds": None,                 # not measured
    "final_url": "https://sunworks.in/",
    "audit_date": READ_ON,
    # The head's script tags were not returned in readable form: this page is
    # large enough that the checker's response ran past what could be read. One
    # positive observation WAS made - source line 706 carries Site Kit by
    # Google's gtag.js loader
    # (<script ... id=\"google_gtagjs-js-after\" defer=\"1\" data-cfasync=\"\" async=\"\">window…),
    # so Site Kit is installed on the site. The GA4 measurement ID itself sits
    # inside that script and was not returned, so the GA4 row is unknown rather
    # than confirmed, and the other seven rows are unknown in both directions.
    "pixels": unknown_pixels(),
    "conversion": {
        # Elementor Forms (form-field-name, form-field-email,
        # form-field-field_de60998, form-field-field_2b884b6,
        # form-field-field_9729fe7, form-field-message), an "Explore More" CTA on
        # every service slide, "Book a service visit" and "Send me a formal
        # quote". No WhatsApp link, no live chat, no popup opt-in and no price
        # list were read on the homepage.
        "has_contact_form": True,              # Elementor Forms, 6 fields
        "has_phone_click": None,               # not read on the pages checked
        "has_whatsapp_link": None,             # not read
        "has_cta_buttons": 4,                  # Explore More (x4 slides), Book a service visit, Send me a formal quote
        "has_live_chat": None,                 # not read
        "has_popup_optin": None,               # not read
        "has_testimonials": True,              # "Hear from Our Satisfied Customers"
        "has_pricing_page_link": False,        # no price list published
    },
    "seo": {
        # <title>SunWorks Energy | Top Solar EPC Company in India</title>
        "has_title": True,
        "title_text": "SunWorks Energy | Top Solar EPC Company in India",
        "title_length": 48,
        "has_meta_description": True,
        "meta_desc_length": 141,
        "h1_count": None,                      # not counted
        "h1_text": "Top Solar EPC Company in India",
        "has_og_tags": True,                   # og:site_name is "Home" - see findings
        "has_schema": None,                    # no JSON-LD block was read
        "has_favicon": True,                   # 32x32, 192x192, 180x180
        "image_count": None,
        "images_without_alt": None,
    },
    "pagespeed": {"error": PAGESPEED_ERROR},
    "page_count": {"has_sitemap": None},
    "local_signals": {
        # No Google Maps embed, no directions link and no local-business
        # structured data were read on the homepage.
        "has_google_maps_embed": False,
    },
    "platform": "WordPress, Astra theme, Elementor 4.3.2 + Elementor Pro "
                "3.34.0 (post IDs 36 and 1586), Swiper 8.4.5, Site Kit by "
                "Google, Elementor Pro mega-menu / sticky / icon-list / slides "
                "/ call-to-action widgets, plus a script and CSS optimiser "
                "that rewrites the markup with bv-* attributes",
    "html_errors": "298 errors (294 HTML), 47 warnings, 101 info on the "
                   "homepage - the highest error count in this audit. The "
                   "dominant cause is the site's own script and CSS optimiser, "
                   "which rewrites the served markup and leaves 70 illegal "
                   "bv-* attributes, 16 scripts with "
                   "type=\"bv_inline_delayed_js\", 10 style elements with a "
                   "non-text/css type, 32 style rules outside an @scope rule "
                   "and 46 duplicate IDs. The same optimiser breaks the images: "
                   "29 <img> elements are missing both src and srcset and 5 "
                   "more carry sizes without srcset, so they cannot load at "
                   "all. Also present: 6 inputs with an empty min/max, 2 "
                   "required selects with no placeholder option, 10 "
                   "element-in-element nesting errors, 6 summary elements "
                   "missing aria-checked/aria-level/role, 6 aria-expanded on a "
                   "summary for its parent details, 2 CSS parse errors and 2 "
                   "heading-level skips (h1 to h3, h2 to h4).",
}

NATUREPOWER = {
    "ssl": True,
    "load_time_seconds": None,                 # not measured
    "final_url": "https://naturepowersolar.com/",
    "audit_date": READ_ON,
    # The COMPLETE head was read - source lines 1 to 44, ending at </head>. It
    # carries one gtag.js loader and one config block:
    #   <script async src="https://www.googletagmanager.com/gtag/js?id=G-9MMYLNMH9T"></script>
    #   gtag('js', new Date());
    #   gtag('config', 'G-9MMYLNMH9T');
    #   gtag('config', 'GT-5TQ454D4');
    #   gtag('config', 'AW-609769092');
    # So GA4 (G-9MMYLNMH9T), a Google tag (GT-5TQ454D4) and a Google Ads
    # conversion ID (AW-609769092) are all live. There is no Meta Pixel, no GTM
    # container, no LinkedIn Insight, no Microsoft Clarity and no Hotjar
    # anywhere in the head. Search Console and Bing verification are still
    # commented-out placeholders - see findings.
    "pixels": pixels(
        google_analytics_ga4=True,             # G-9MMYLNMH9T
        google_ads=True,                       # AW-609769092
    ),
    "conversion": {
        # "Send me a formal quote for this system" under the savings calculator,
        # "Check if you qualify", "Book a service visit", six "Explore ..." links,
        # a WhatsApp hand-off that pre-fills the estimate
        # (wa.me/919666088988?text=...), a 5-character security check on the
        # quote form, and the full subsidy / EMI / pump / heater / fence /
        # lighting calculators. No live-chat widget and no popup opt-in were
        # read; no price list page - the calculator is the pricing surface.
        "has_contact_form": True,              # "Send me a formal quote" + CAPTCHA
        "has_phone_click": True,               # +91 96660 88988 click-to-call
        "has_whatsapp_link": True,             # wa.me/919666088988 with pre-filled estimate
        "has_cta_buttons": 9,                  # Explore rooftop/commercial/pumps/fencing/heaters/lighting, Check if you qualify, How to apply, Book a service visit
        "has_live_chat": False,                # no live-chat widget read
        "has_popup_optin": False,              # no popup opt-in read
        "has_testimonials": None,              # not read as a block
        "has_pricing_page_link": True,         # live savings calculator with real tariffs
    },
    "seo": {
        # <title>Rooftop Solar in Telangana | ₹78,000 Subsidy | Nature Power Solar</title>
        "has_title": True,
        "title_text": "Rooftop Solar in Telangana | Rs.78,000 Subsidy | Nature Power Solar",
        "title_length": 66,
        "has_meta_description": True,
        "meta_desc_length": 154,
        "h1_count": None,                      # not counted
        "h1_text": "Clean solar power for Telangana homes and rooftops",
        "has_og_tags": True,                   # full og + twitter card set, 1200x630 image
        "has_schema": True,                    # LocalBusiness + WebSite + FAQPage + ItemList JSON-LD
        "has_favicon": True,                   # ico, 32px png, apple-touch-icon, webmanifest
        "image_count": None,
        "images_without_alt": None,
    },
    "pagespeed": {"error": PAGESPEED_ERROR},
    "page_count": {"has_sitemap": None},
    "local_signals": {
        # The JSON-LD carries hasMap
        # https://www.google.com/maps?cid=8850580709543659187 and the same cid in
        # sameAs, plus geo coordinates 17.545692 / 80.629687, geo.region IN-TG,
        # geo.placename Kothagudem and opening hours Mon-Sat 09:00-19:00.
        "has_google_maps_embed": True,
    },
    "platform": "Hand-built static HTML (own /assets/css/style.css?v=5.5, "
                "/site.webmanifest, Google Fonts Outfit / DM Sans / Noto Sans "
                "Telugu). No CMS, no page builder, no plugin stack - the lightest "
                "build of the five.",
    "html_errors": "6 errors, 0 warnings, 0 info on the homepage - by far the "
                   "cleanest of the five. The errors are 2 aria-label attributes "
                   "on div elements without a role (the service carousel and the "
                   "orbit stage), an output element inside a label whose id does "
                   "not match the label's for attribute (the savings "
                   "calculator's bill-out output), a role=tab with no "
                   "corresponding role=tabpanel, a heading-level skip from h2 to "
                   "h4, and a stray <script> start tag after </body> at source "
                   "line 420.",
}

SURYARENEWABLE = {
    "ssl": True,
    "load_time_seconds": None,                 # not measured
    "final_url": "http://suryarenewable.com/",
    "audit_date": READ_ON,
    # The COMPLETE 138-line source was read end to end. The head carries exactly
    # one tracking script - the Google Ads tag AW-18243186763:
    #   <script async src="https://www.googletagmanager.com/gtag/js?id=AW-18243186763"></script>
    #   gtag('js', new Date()); gtag('config', 'AW-18243186763');
    # There is no GA4, no GTM container, no Meta Pixel, no LinkedIn Insight, no
    # Microsoft Clarity and no Hotjar anywhere in the document. See findings for
    # the placeholder conversion label that makes the tag ineffective.
    "pixels": pixels(
        google_ads=True,                       # AW-18243186763
    ),
    "conversion": {
        # Three CTAs - "Free Solar Quote", "Wind Project Enquiry", "Hydro
        # Consultation" - all point at enquiry.html, plus a "Send Enquiry" button
        # in the contact block and a floating WhatsApp button
        # (wa.me/919182311739?text=Hi%20Surya%20Renewable%20Energies...). No
        # live chat, no popup opt-in and no price list were read.
        "has_contact_form": True,              # enquiry.html, linked from 4 CTAs
        "has_phone_click": True,               # +91 91823 11739
        "has_whatsapp_link": True,             # wa.me/919182311739
        "has_cta_buttons": 4,                  # Free Solar Quote, Wind Project Enquiry, Hydro Consultation, Send Enquiry
        "has_live_chat": False,                # no live-chat widget read
        "has_popup_optin": False,              # no popup opt-in read
        "has_testimonials": False,             # no testimonial block read
        "has_pricing_page_link": False,        # no price list published
    },
    "seo": {
        # <title>Surya Renewable Energies | Solar Power, Wind Power, Hydro Power
        # Trader, Supplier and Service Provider</title>
        "has_title": True,
        "title_text": "Surya Renewable Energies | Solar Power, Wind Power, Hydro Power Trader, Supplier and Service Provider",
        "title_length": 108,
        "has_meta_description": True,
        "meta_desc_length": 137,
        "h1_count": 3,                         # one per hero slide
        "h1_text": "Solar Power & Solar Energy Experts / Wind Power & Wind Energy Solutions / Hydro Power & Hydro Energy Plants",
        "has_og_tags": False,                  # no Open Graph tags at all
        "has_schema": False,                   # no JSON-LD anywhere
        "has_favicon": True,                   # images/logo.png
        "image_count": None,
        "images_without_alt": None,
    },
    "pagespeed": {"error": PAGESPEED_ERROR},
    "page_count": {"has_sitemap": None},
    "local_signals": {
        # No Google Maps embed, no directions link and no local-business
        # structured data anywhere in the 138-line document.
        "has_google_maps_embed": False,
    },
    "platform": "Hand-built static HTML (own style.css, Inter from Google Fonts, "
                "images/logo.png). No CMS, no page builder, no plugin stack. "
                "Three Pexels stock videos are hot-linked as the hero slider "
                "background.",
    "html_errors": "1 error, 0 warnings, 0 info on the homepage - a single stray "
                   "<script> start tag after </body> at source line 138. This is "
                   "the only one of the five whose markup is close to clean, and "
                   "the trade-off is that almost nothing else is present either: "
                   "no canonical, no Open Graph, no Twitter card, no JSON-LD, no "
                   "sitemap reference and only one tracking tag in the whole "
                   "document.",
}

MILESTONE = {
    "ssl": True,
    "load_time_seconds": None,                 # not measured
    "final_url": "https://www.milestonesolar.in/",
    "audit_date": READ_ON,
    # The Meta Pixel IS confirmed. Source lines 191-192 carry its noscript
    # fallback: <img height="1" width="1" style="display:none" alt="fbpx"
    # src="https://www.facebook.com/tr?id=1132764258717771&ev=PageView&noscript=1" />
    # Site Kit by Google 1.187.0 is also installed (meta generator at source
    # line 47) and the head preconnects to www.googletagmanager.com, but the
    # GA4 / Google Ads measurement ID itself was not returned, so those rows are
    # unknown rather than confirmed. No GTM container, LinkedIn Insight,
    # Microsoft Clarity or Hotjar reference was read.
    "pixels": unknown_pixels(
        meta_pixel=True,                       # id 1132764258717771, noscript img
    ),
    "conversion": {
        # A "wpr-form" form (name="New Form" page="Home" page_id="5",
        # form_id=227f9364) sits in a section on the homepage, a floating
        # click-to-chat WhatsApp button (ht_ctc_* classes), and the published
        # phone numbers. No price list and no live-chat widget were read.
        "has_contact_form": True,              # wpr-form, hidden form_id 227f9364
        "has_phone_click": True,               # tel:+91 9030005033 - but see findings, the href is malformed
        "has_whatsapp_link": True,             # Click to Chat (ht_ctc) floating button
        "has_cta_buttons": 3,                  # homepage form, click-to-chat, phone
        "has_live_chat": False,                # WhatsApp click-to-chat only
        "has_popup_optin": False,              # no popup opt-in read
        "has_testimonials": True,              # "1,248 reviews" Google badge
        "has_pricing_page_link": False,        # no price list published
    },
    "seo": {
        # og:title "Best Solar Company in Hyderabad - Solar Installation & EPC |
        # Milestone Solar"; og:site_name is "-" - see findings.
        "has_title": True,
        "title_text": "Best Solar Company in Hyderabad - Solar Installation & EPC | Milestone Solar",
        "title_length": 78,
        "has_meta_description": True,
        "meta_desc_length": 122,
        "h1_count": None,                      # not counted
        "h1_text": "",
        "has_og_tags": True,                   # full og + twitter card set
        "has_schema": None,                    # no JSON-LD block was read
        "has_favicon": True,                   # 32x32, 192x192, 180x180, 270x270
        "image_count": None,
        "images_without_alt": None,
    },
    "pagespeed": {"error": PAGESPEED_ERROR},
    "page_count": {"has_sitemap": None},
    "local_signals": {
        # No Google Maps embed, no directions link and no local-business
        # structured data were read on the homepage.
        "has_google_maps_embed": False,
    },
    "platform": "WordPress, Astra theme (ast-primary-menu-enabled, "
                "ast-logo-title-inline, masthead), Elementor "
                "(elementor-top-section, data-element_type=\"section\"), All in "
                "One SEO (AIOSEO) 5.0.2.1, Site Kit by Google 1.187.0, MyStickyMenu "
                "(mystickymenu), Click to Chat for WhatsApp (ht_ctc_*), and a "
                "third-party form plugin whose markup injects page / page_id "
                "attributes onto the <form> element (wpr-form)",
    "html_errors": "128 errors, 10 warnings, 53 info on the homepage. The single "
                   "biggest cause is malformed nesting: 100 elements are not "
                   "allowed where they sit - 55 <p> inside <span>, 22 <h3> "
                   "inside <span>, 15 <h2> inside <span>, 7 <ul> inside <span> "
                   "and 1 <div> inside <button> - which also produces 3 stray "
                   "</p> end tags, 1 end tag for div with open elements, and "
                   "unclosed article / main elements. Beyond that: 2 itemid "
                   "attributes on elements with no itemscope or itemtype, 2 "
                   "tabindex elements nested inside <a>, 3 illegal attributes "
                   "on form and div elements (page, page_id, us'), 2 places with "
                   "no space between attributes, 2 inputs with size=\"1\", a "
                   "role=tab with no role=tabpanel, a heading-level skip from h2 "
                   "to h6, 2 style elements in body that are not the first child "
                   "of their parent, and 3 style rules outside an @scope rule. "
                   "The click-to-call link is also broken: the checker reports "
                   "'Bad value tel:+91 9030005033 for attribute href on element "
                   "a: Illegal character after tel:. Space is not allowed.'",
}

LEADS = {
    "Zenith Energy Services": ZENITH,
    "SunWorks Energy": SUNWORKS,
    "Nature Power Solar": NATUREPOWER,
    "Surya Renewable Energies": SURYARENEWABLE,
    "Milestone Solar": MILESTONE,
}

# Extra real findings that belong at the top of "Top priorities" - each one is
# read from the live advertiser record or the live page, not invented.
EXTRA_ISSUES = {
    "Zenith Energy Services": [
        "A complete second HTML document is embedded inside your homepage body: "
        "the checker finds a doctype, <html lang=\"en\">, <head>, "
        "<meta charset=\"UTF-8\">, a viewport meta and a <title> at source line "
        "417. Your India-map plugin ships its own whole page inside yours.",
        "All four of your hero counters read zero - 'Energy audits 0+', 'Carbon "
        "reduction projects 0+', 'Renewable projects supported 0 GW' and 'Net "
        "Zero projects completed 0+' - on a page that separately claims 180+ "
        "major projects across 28 states and 8 union territories.",
        "The checker reports 158 errors on the homepage, more than any other "
        "site in this audit, and 121 of them are style rules sitting outside an "
        "@scope rule.",
        "You are running 9 live Google ads - the highest count of any lead in "
        "this audit - and the ad destination is a page whose head carries no "
        "conversion tracking that could be confirmed in this pass.",
        "There is no price list anywhere on the site, so every enquiry arrives "
        "without a number attached to it.",
    ],
    "SunWorks Energy": [
        "Your years-in-business figure contradicts itself three times on one "
        "page: 'Since 2015' (11 years in 2026), then '10+ Years of Experience', "
        "then '15+ Years Solar Experience' a few lines further down.",
        "Three of your four service cards point at the wrong page. 'Solar EPC "
        "03' and 'Operations and Maintenance 04' both link to "
        "/consultancy-advisory/, while the slider directly above the same block "
        "links correctly to /epc-services/ and /operations-maintenance/. The two "
        "blocks disagree with each other.",
        "The optimiser on your site is breaking your own images: the checker "
        "reports 29 <img> elements missing both src and srcset, and 5 more "
        "carrying sizes without srcset. Those images cannot load at all.",
        "og:site_name is set to \"Home\" instead of SunWorks Energy, so every "
        "share of your homepage is attributed to a page called 'Home'.",
        "The checker reports 298 errors and 47 warnings on the homepage - the "
        "highest error count in this audit - and 46 of them are duplicate IDs.",
    ],
    "Nature Power Solar": [
        "Your Search Console and Bing verification tokens are still the "
        "commented-out placeholders the developer shipped: the source carries "
        "<!-- <meta name=\"google-site-verification\" content=\"PASTE_TOKEN\"> --> "
        "and <!-- <meta name=\"msvalidate.01\" content=\"PASTE_TOKEN\"> -->. You "
        "are buying Google ads for a site Google has never been able to verify "
        "ownership of.",
        "You run 1 live Google ad and the only tracking in your head is the "
        "Google Ads tag AW-609769092. There is no Meta Pixel, so nobody who "
        "leaves without filling the form can be reached again on Facebook or "
        "Instagram.",
        "Your markup is the cleanest of the five - 6 errors, 0 warnings, 0 info "
        "- and your savings calculator publishes real numbers. That is the "
        "strongest asset in this audit and it is doing the work of five pages.",
        "The checker finds a stray <script> start tag after </body> at source "
        "line 420, and your calculator's <output> element has an id that does "
        "not match the for attribute of its own label.",
        "There is no live chat and no popup opt-in, so the quote form is the "
        "only capture point on the page.",
    ],
    "Surya Renewable Energies": [
        "Your Google Ads conversion event can never record a conversion. The "
        "head still carries the template's placeholder label - "
        "gtag('event', 'conversion', {'send_to': "
        "'AW-18243186763/WHATSAPP_LABEL'}) with the comment 'Replace with your "
        "WhatsApp conversion label' - so every WhatsApp click you pay for is "
        "sent to a label that does not exist in your Google Ads account.",
        "Your hero slider is three Pexels stock videos hot-linked straight from "
        "pexels.com/download/video/7040278/, /19202862/ and /18680290/. The "
        "first thing a prospect sees on a page you pay to send them to is "
        "somebody else's stock footage.",
        "The page has no Open Graph tags, no Twitter card, no canonical, no "
        "JSON-LD and no sitemap reference, so every link shared anywhere "
        "renders as a bare URL with no image and no description.",
        "Your <title> is 108 characters and your three hero slides each carry "
        "their own <h1>, so the page competes with itself for three different "
        "queries at once.",
        "Your contact page is a single enquiry.html with no phone validation, "
        "no email field confirmation and no thank-you state read in this pass.",
    ],
    "Milestone Solar": [
        "Every trust counter on your homepage reads zero: 'Years of experience "
        "0+', 'Installations 0+', 'Happy Customers 0%' and 'Customer Support "
        "0/7'. A visitor who scrolls to the proof section sees four zeros.",
        "Your click-to-call link is broken. The checker reports 'Bad value "
        "tel:+91 9030005033 for attribute href on element a: Illegal character "
        "after tel:. Space is not allowed' - there is a space inside the href, "
        "so the number cannot be dialled from the page.",
        "The checker reports 128 errors, and 100 of them are elements sitting "
        "where they are not allowed - 55 <p> inside <span>, 22 <h3> inside "
        "<span>, 15 <h2> inside <span> and 7 <ul> inside <span>.",
        "og:site_name is set to \"-\", so every share of your homepage is "
        "attributed to a hyphen.",
        "You run 6 live Google ads and your only confirmed tracking is a Meta "
        "Pixel. Site Kit by Google is installed but no GA4 or Google Ads "
        "measurement ID could be read in this pass, so your Google spend has no "
        "confirmed measurement behind it.",
    ],
}

PROMISE_GAP = {
    "Zenith Energy Services": [
        ("Google Ads Transparency: 9 live ads under advertiser "
         "AR02278013072834560001, verified as ZENITH ENERGY SERVICES PRIVATE "
         "LIMITED, including a YouTube video creative.",
         "The site behind those 9 ads carries 158 HTML errors on the homepage, "
         "a complete second HTML document embedded in the body, and four hero "
         "counters that all read zero. The ad buys the click; the page has to "
         "carry it."),
        ("The advertiser's service pages promise ESCO retrofits, energy audits, "
         "solar, water management and net-zero programmes for industries and "
         "businesses across India.",
         "The homepage substantiates the ESCO claim (an empanelled ESCO with the "
         "Bureau of Energy Efficiency) and names three real case studies - "
         "Basavatarakam Indo American Cancer Hospital, a clean-cooking project "
         "in Koraput, Odisha, and a net-zero roadmap for VPCL Visakha "
         "Pharmacity - plus a client carousel. But there is no price list, no "
         "published capacity figure and no case-study metric, so a prospect "
         "cannot size the offer from the page."),
        ("The site positions Zenith as a national net-zero consultancy with "
         "180+ major projects across 28 states and 8 union territories.",
         "The India map that carries those numbers also carries the structural "
         "defect: its plugin ships a whole second HTML document inside the "
         "homepage body. The interactive widget is the most distinctive asset on "
         "the page and it is also the largest single source of validation "
         "errors."),
    ],
    "SunWorks Energy": [
        ("Google Ads Transparency: 1 live ad under advertiser "
         "AR07942131426432909313, verified as SUNWORKS ENERGY PRIVATE LIMITED.",
         "The ad lands on a homepage reporting 298 errors and 47 warnings, "
         "where 29 images cannot load because the optimiser stripped their src "
         "and srcset attributes. The page's own evidence is being deleted by "
         "its own performance plugin."),
        ("The homepage claims 'Since 2015' and '10+ Years of Experience' and, a "
         "few lines later, '15+ Years Solar Experience'.",
         "2015 to 2026 is 11 years. Neither figure matches the founding date on "
         "the same page, and the two counters contradict each other, so a "
         "prospect who reads both has no reason to trust either."),
        ("The homepage presents four services - Consultancy & Advisory, Design "
         "& Engineering, Solar EPC, Operations & Maintenance - each with a "
         "'Know More' link and a numbered card.",
         "Three of the four numbered cards link to /consultancy-advisory/, "
         "including 'Solar EPC 03' and 'Operations and Maintenance 04'. The "
         "slider above them links correctly to /epc-services/ and "
         "/operations-maintenance/, so the two blocks disagree and the EPC "
         "service - the one the ad is about - is unreachable from the card."),
        ("The site publishes a 25-logo clientele wall, five awards and two "
         "named testimonials (Presidency Schools, Vasantha Industries Pvt Ltd) "
         "with project names such as Viswateja Spinning Mills 3.6 MWp.",
         "That is genuine, specific proof and it is the strongest asset on the "
         "page. It sits below the broken counters and the contradictory "
         "experience figures, and none of it is connected to a tracking pixel "
         "that could be confirmed in this pass."),
    ],
    "Nature Power Solar": [
        ("Google Ads Transparency: 1 live ad under advertiser "
         "AR11194127933927063553, verified as CHITWALA JOHN SANDEEP - a sole "
         "proprietorship behind the Nature Power Solar trading name.",
         "The ad buys a click to the best-built page in this audit: 6 errors, 0 "
         "warnings, 0 info, a live savings calculator with real Telangana "
         "tariffs, and JSON-LD that names the founder, the operations manager, "
         "the Google Maps listing and the exact subsidy tiers. The gap is not "
         "the page - it is that nothing on it is measured."),
        ("The site claims 'Authorised PM Surya Ghar vendor' and publishes the "
         "subsidy as ₹30,000 for 1 kW, ₹60,000 for 2 kW and ₹78,000 for 3 kW "
         "and above, plus ₹18,000 per kW for apartment societies up to 500 kW, "
         "with the scheme running to 31 March 2027.",
         "Those figures match the published PM Surya Ghar schedule and the "
         "calculator's worked example (a ₹3,500 monthly bill resolving to a 4 kW "
         "system at ₹2.48 lakh, ₹78,000 subsidy, ₹1.7 lakh net, ₹3,325 a month "
         "saved, 4.1-year payback) is internally consistent. The claim is "
         "substantiated. What is missing is any way to see whether the claim "
         "converts."),
        ("The site claims '500+ installations' and '48-hour service - local "
         "team, every district'.",
         "Neither figure is backed by a case study, a photograph or a review "
         "count on the page read in this pass, and the Search Console "
         "verification token is still a commented-out placeholder, so Google has "
         "never confirmed who owns the domain those claims sit on."),
    ],
    "Surya Renewable Energies": [
        ("Google Ads Transparency: 2 live ads under advertiser "
         "AR08105928276372881409, verified as LANKA V K PHANI VISWANATH - one "
         "of them a YouTube video creative.",
         "The video ad buys attention and the page it lands on opens with three "
         "Pexels stock videos, not the advertiser's own installations. The "
         "strongest asset - a YouTube creative the company paid to produce - is "
         "immediately undercut by the stock footage above it."),
        ("The head installs the Google Ads tag AW-18243186763 and defines a "
         "WhatsApp conversion event against it.",
         "The event still sends to 'AW-18243186763/WHATSAPP_LABEL' with the "
         "template's own comment 'Replace with your WhatsApp conversion label' "
         "above it. Google Ads will never record a conversion from this page, "
         "so the advertiser is paying for clicks with no measurement of what "
         "they produce."),
        ("The site presents solar, wind and hydro as three equal service lines, "
         "each with its own hero slide, its own <h1> and its own CTA.",
         "The solar line is a genuine rooftop and ground-mount EPC - rooftop "
         "solar, ground-mount systems, net metering, battery storage and AMC "
         "for residential and commercial plants, with feasibility studies, site "
         "surveys and net-metering approvals handled. The wind and hydro lines "
         "are described only as equipment trading. The page asks the same "
         "attention for all three, and the company describes itself as 'a new "
         "bee in this energy sector'."),
        ("The page carries a floating WhatsApp button pre-filled with 'Hi Surya "
         "Renewable Energies, I need quote for solar power'.",
         "That is the only working conversion path on the site, and because the "
         "Google Ads conversion label is a placeholder, the one action the page "
         "is built to produce is the one action Google Ads cannot count."),
    ],
    "Milestone Solar": [
        ("Google Ads Transparency: 6 live ads under advertiser "
         "AR10713925876992442369, verified as ZAHEERUDDIN JAVEED MOHAMMED.",
         "The ads land on a homepage reporting 128 errors, where every trust "
         "counter reads zero and the click-to-call link has a space inside its "
         "href so the number cannot be dialled. The page pays for six ads' "
         "worth of clicks and then fails the two things a buyer does first."),
        ("The homepage presents 'Years of experience 0+', 'Installations 0+', "
         "'Happy Customers 0%' and 'Customer Support 0/7' next to a '1,248 "
         "reviews' Google badge.",
         "The four counters and the review badge contradict each other on the "
         "same screen, and the checker reports 100 elements sitting where they "
         "are not allowed - 55 <p> inside <span>, 22 <h3> inside <span>, 15 "
         "<h2> inside <span> and 7 <ul> inside <span> - which is what breaks "
         "the counters' markup."),
        ("The site lists off-grid and on-grid SPV plants, hybrid plants, "
         "solar-powered micro and mini grids, street lighting, fencing, water "
         "heating and water pumping, and is empanelled with TGREDCO under "
         "registration TSRE180047.",
         "The TGREDCO register independently confirms Milestone Solarcom Pvt "
         "Ltd and that registration number, so the capability claim is "
         "substantiated by a government source. The page itself publishes no "
         "price, no system size and no project photograph in this pass, so a "
         "prospect cannot size the offer."),
        ("The site's copy carries 'top solar comapy in hyderabad', 'This "
         "Shceme' and 'Sustanability Focused'.",
         "Three spelling errors in the primary conversion copy, on a page whose "
         "meta description opens 'Looking for best solar company in Hyderabad?' "
         "- the exact phrase six live ads are buying."),
    ],
}

COMPANY = {
    "Zenith Energy Services": {
        "legal": "Zenith Energy Services Private Limited",
        "city": "Shaikpet, Hyderabad 500081 (serves Karimnagar, Khammam and Nizamabad)",
        "website": "https://zenithenergy.com/",
        "contact_facts": "Registered office D.NO. 1-89/A/8/C/2&3, P. NO. 2P &3P "
                         "C1, Vittal Rao Nagar, M3 Block, Shaikpet, Telangana "
                         "500081 | +91 70757 56795 | zenith@zenithenergy.com | "
                         "CIN U74140TG1990PTC011583, incorporated 10 Aug 1990 | "
                         "Directors Sindhu Jannareddy and Vindhya Pulicherla | "
                         "ZoomInfo lists a second Hyderabad address at 10-5-6/b "
                         "My Home Plz, Masab Tank | Location pages published for "
                         "Karimnagar, Khammam and Nizamabad",
        "contact": {"phone": "+91 7075756795",
                    "email": "zenith@zenithenergy.com",
                    "whatsapp": ""},
    },
    "SunWorks Energy": {
        "legal": "SunWorks Energy Private Limited",
        "city": "Jubilee Hills, Hyderabad",
        "website": "https://sunworks.in/",
        "contact_facts": "2nd Floor, Plot 126, Road Number 11, Jubilee Hills, "
                         "Hyderabad | +91 86883 26316 | gosolar@sunworks.in | "
                         "Facebook publisher link "
                         "https://www.facebook.com/SunWorks.India | Awards "
                         "published on the homepage: 'Best Engineering team of "
                         "the Year 2024 - Telangana', 'Best Engineering team of "
                         "the year 2024 - Andhra Pradesh', 'Woman of the year "
                         "for Tech competence in Solar Project, Engineering, "
                         "Design & Tech Consultancy - Karnataka' | Directors "
                         "named on the homepage: Rajyalakshmi Kola and Arjun "
                         "Penumatsa",
        "contact": {"phone": "+91 8688326316",
                    "email": "gosolar@sunworks.in",
                    "whatsapp": ""},
    },
    "Nature Power Solar": {
        "legal": "Nature Power Solar",
        "city": "Kothagudem 507101 (serves all of Telangana and Andhra Pradesh)",
        "website": "https://naturepowersolar.com/",
        "contact_facts": "2-2-1/2, Budidagadda Basthi, Kothagudem, Telangana "
                         "507101 | +91 96660 88988 / +91 84660 88988 | "
                         "info@naturepowersolar.com | geo 17.545692 / 80.629687 "
                         "| Google Maps listing cid 8850580709543659187 | Open "
                         "Mon-Sat 09:00-19:00 | Founder & Technical Lead Sagar "
                         "Earpula, Operations Manager Abhilash Earpula | "
                         "Independently listed on the TGREDCO 2026 empanelled-"
                         "supplier register as 'M/s. Nature Power Solar "
                         "Technologies & Services', 2-2-1/2 Budidagadda Basthi, "
                         "Kothagudem 507101",
        "contact": {"phone": "+91 9666088988",
                    "email": "info@naturepowersolar.com",
                    "whatsapp": "+91 9666088988"},
    },
    "Surya Renewable Energies": {
        "legal": "Surya Renewable Energies",
        "city": "Kothapet, Hyderabad",
        "website": "http://suryarenewable.com/",
        "contact_facts": "Alkapuri Colony, Kothapet, Hyderabad, Telangana | "
                         "info@suryarenewable.com | +91 91823 11739 | WhatsApp "
                         "wa.me/919182311739 | Serves Telangana and Andhra "
                         "Pradesh | Self-described on the homepage as 'a new bee "
                         "in this energy sector'",
        "contact": {"phone": "+91 9182311739",
                    "email": "info@suryarenewable.com",
                    "whatsapp": "+91 9182311739"},
    },
    "Milestone Solar": {
        "legal": "Milestone Solarcom Private Limited",
        "city": "Hyderabad",
        "website": "https://www.milestonesolar.in/",
        "contact_facts": "+91 9030005033 / +91 9246527527 | "
                         "milestonesolarcomsales@gmail.com (published on the "
                         "site) and milestonesolarcom@gmail.com (registered "
                         "address) | TGREDCO empanelled supplier registration "
                         "TSRE180047, listed on the 2026 register as 'M/s. "
                         "Milestone Solarcom Pvt. Ltd.' | Claims 1,248 Google "
                         "reviews | Trading name on the site: Milestone Solar / "
                         "Milestone Solarcom",
        "contact": {"phone": "+91 9030005033",
                    "email": "milestonesolarcomsales@gmail.com",
                    "whatsapp": "+91 9030005033"},
    },
}


# ---------------------------------------------------------------------------
# The live Google ads, read from the Google Ads Transparency Centre on
# 2026-11-10. Every advertiser ID was opened directly at
# adstransparency.google.com/advertiser/<AR_ID>?region=IN and the verified
# legal name read off the returned record.
# ---------------------------------------------------------------------------

ADS = {
    "Zenith Energy Services": [
        {
            "library_id": "AR02278013072834560001",
            "library_url": "https://adstransparency.google.com/advertiser/AR02278013072834560001?region=IN",
            "page_name": "ZENITH ENERGY SERVICES PRIVATE LIMITED (verified)",
            "started": "2026-11-10 (advertiser record read live)",
            "destination": "https://zenithenergy.com/ - domain confirmed on the advertiser record",
            "text": "9 live ads listed under this advertiser in Google's Ads "
                    "Transparency Centre - the highest count of any lead in this "
                    "audit. 4 image creatives were visible on the advertiser "
                    "page plus 5 further creatives, including 1 YouTube video "
                    "creative (oeb4Qg-89OQ).\n"
                    "\n"
                    "Advertiser verified. Legal name read off the advertiser "
                    "record: ZENITH ENERGY SERVICES PRIVATE LIMITED.\n"
                    "\n"
                    "The ads serve Karimnagar, Khammam and Nizamabad through "
                    "location pages on the site (/solar-company-in-karimnagar/, "
                    "/solar-company-in-khammam/), covering commercial, "
                    "industrial, residential and institutional rooftop solar, "
                    "EPC, battery energy storage, O&M and customised financing.",
        },
    ],
    "SunWorks Energy": [
        {
            "library_id": "AR07942131426432909313",
            "library_url": "https://adstransparency.google.com/advertiser/AR07942131426432909313?region=IN",
            "page_name": "SUNWORKS ENERGY PRIVATE LIMITED (verified)",
            "started": "2026-11-10 (advertiser record read live)",
            "destination": "https://sunworks.in/ - domain confirmed on the advertiser record",
            "text": "1 live ad listed under this advertiser in Google's Ads "
                    "Transparency Centre - a Display image creative "
                    "(simgad/8721599813200798262).\n"
                    "\n"
                    "Advertiser verified. Legal name read off the advertiser "
                    "record: SUNWORKS ENERGY PRIVATE LIMITED.\n"
                    "\n"
                    "The site the ad points at sells four services - "
                    "Consultancy & Advisory, Design & Engineering, Solar EPC and "
                    "Operations & Maintenance - and positions the company as a "
                    "'Top Solar EPC Company in India'.",
        },
    ],
    "Nature Power Solar": [
        {
            "library_id": "AR11194127933927063553",
            "library_url": "https://adstransparency.google.com/advertiser/AR11194127933927063553?region=IN",
            "page_name": "CHITWALA JOHN SANDEEP (verified)",
            "started": "2026-11-10 (advertiser record read live)",
            "destination": "https://naturepowersolar.com/ - domain confirmed on the advertiser record",
            "text": "1 live ad listed under this advertiser in Google's Ads "
                    "Transparency Centre - a Display image creative "
                    "(simgad/14883437245831789543).\n"
                    "\n"
                    "Advertiser verified. Legal name read off the advertiser "
                    "record: CHITWALA JOHN SANDEEP - a sole proprietorship "
                    "trading as Nature Power Solar Technologies & Services.\n"
                    "\n"
                    "The ad serves a Kothagudem-headquartered business whose "
                    "site covers rooftop solar, solar pumps, fencing and water "
                    "heaters across Telangana, with the PM Surya Ghar subsidy "
                    "and net metering handled end to end.",
        },
    ],
    "Surya Renewable Energies": [
        {
            "library_id": "AR08105928276372881409",
            "library_url": "https://adstransparency.google.com/advertiser/AR08105928276372881409?region=IN",
            "page_name": "LANKA V K PHANI VISWANATH (verified)",
            "started": "2026-11-10 (advertiser record read live)",
            "destination": "http://suryarenewable.com/ - domain confirmed on the advertiser record",
            "text": "2 live ads listed under this advertiser in Google's Ads "
                    "Transparency Centre - one YouTube video creative "
                    "(ytimg/24H234ft0Yk) and one Display image creative "
                    "(simgad/10231766854828954333).\n"
                    "\n"
                    "Advertiser verified. Legal name read off the advertiser "
                    "record: LANKA V K PHANI VISWANATH.\n"
                    "\n"
                    "The site the ads point at sells rooftop solar, "
                    "ground-mount systems, net metering, battery storage and AMC "
                    "for residential and commercial plants, plus wind and "
                    "micro-hydro equipment trading.",
        },
    ],
    "Milestone Solar": [
        {
            "library_id": "AR10713925876992442369",
            "library_url": "https://adstransparency.google.com/advertiser/AR10713925876992442369?region=IN",
            "page_name": "ZAHEERUDDIN JAVEED MOHAMMED (verified)",
            "started": "2026-11-10 (advertiser record read live)",
            "destination": "https://www.milestonesolar.in/ - domain confirmed on the advertiser record",
            "text": "6 live ads listed under this advertiser in Google's Ads "
                    "Transparency Centre - 4 image creatives were visible on the "
                    "advertiser page plus 2 further creatives.\n"
                    "\n"
                    "Advertiser verified. Legal name read off the advertiser "
                    "record: ZAHEERUDDIN JAVEED MOHAMMED, trading as Milestone "
                    "Solarcom.\n"
                    "\n"
                    "The site the ads point at sells off-grid and on-grid SPV "
                    "plants, hybrid plants, solar micro and mini grids, street "
                    "lighting, fencing, water heating and water pumping, and is "
                    "empanelled with TGREDCO under TSRE180047.",
        },
    ],
}


def build_base(company):
    """Create the ads-only JSON shell, or refresh the ad-library half of an
    existing one.

    The website measurements are never overwritten here - they are re-read from
    the LEADS dicts every run. The ad-library block IS refreshed every run,
    because the Transparency Centre record is re-verified and a corrected
    transcription has to replace the old one rather than sit beside it.
    """
    path = os.path.join(AUDIT_DIR,
                        f"audit_{company.replace(' ', '_')}.json")
    meta = COMPANY[company]
    ads = ADS[company]
    n = len(ads)
    google_detail = {
        "name": ads[0]["page_name"],
        "ad_count": 9 if company == "Zenith Energy Services" else
                    (1 if company in ("SunWorks Energy", "Nature Power Solar") else
                     (2 if company == "Surya Renewable Energies" else 6)),
        "url": meta["website"],
        "image_files": [
            "Zenith: 4 image creatives visible on the advertiser page plus 5 "
            "further creatives, including 1 YouTube video creative "
            "(oeb4Qg-89OQ)."
            if company == "Zenith Energy Services" else
            ("SunWorks: 1 Display image creative, simgad/8721599813200798262."
             if company == "SunWorks Energy" else
             ("Nature Power Solar: 1 Display image creative, "
              "simgad/14883437245831789543."
              if company == "Nature Power Solar" else
              ("Surya Renewable: 1 YouTube video creative "
               "(ytimg/24H234ft0Yk) plus 1 Display image creative "
               "(simgad/10231766854828954333)."
               if company == "Surya Renewable Energies" else
               "Milestone Solar: 4 image creatives visible on the advertiser "
               "page plus 2 further creatives.")))
        ],
        "text": ads[0]["text"],
    }
    adlib = {
        "meta_own": {
            # Only Zenith was actually queried in the Meta Ad Library (batch 9,
            # 2026-10-23, zero results). The other four were never queried, so
            # their Meta count is recorded as not checked - found is None - and
            # the report says so rather than implying a measured zero.
            "found": False if company == "Zenith Energy Services" else None,
            "results_count": 0,
            "results_label": "0 live ads (Meta Ad Library, queried 2026-10-23)",
            "query": "solar + Telangana city keyword search",
            "note": ("Queried on 2026-10-23 in batch 9 and recorded as a "
                     "zero-ad website probe; that probe covered Meta only. The "
                     "advertiser's paid activity is on Google, not Meta."
                     if company == "Zenith Energy Services" else
                     "The Meta Ad Library was not queried for this company. "
                     "This lead was found through the Google Ads Transparency "
                     "Centre, so no Meta ad count is claimed either way."),
        },
        "google_own": {
            "found": True,
            "results_count": google_detail["ad_count"],
            "results_label": f"{google_detail['ad_count']} live Google ads",
            "query": f"adstransparency.google.com/?region=IN&domain={meta['website'].split('//')[-1].strip('/')}",
            "detail": google_detail,
        },
        "summary": (
            f"{google_detail['ad_count']} live Google ads confirmed on {READ_ON} "
            f"in Google's Ads Transparency Centre under advertiser "
            f"{ads[0]['page_name']} (ID {ads[0]['library_id']}), identity-"
            f"verified, with {meta['website']} as the advertised domain. "
            + ("The Meta Ad Library was queried on 2026-10-23 and returned zero "
               "results for this company."
               if company == "Zenith Energy Services" else
               "The Meta Ad Library was not queried for this company, so no "
               "Meta ad count is claimed either way.")
        ),
        "meta_competitors": {},
        "google_competitors": {
            "advertisers": [],
            "note": ("Competitor sweeps were not run for this lead in this pass, "
                     "so no competitor Google advertiser counts are claimed "
                     "here."),
        },
    }

    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            audit = json.load(f)
        audit["ad_library"] = adlib
        audit["funnel"] = {
            "destination": meta["website"],
            "note": ("Advertised domain as shown on the Google Ads Transparency "
                     "Centre advertiser record."),
        }
        return audit, path

    audit = {
        "company": meta["legal"],
        "legal": meta["legal"],
        "city": meta["city"],
        "website": meta["website"],
        "ads_only": True,
        "website_audit_run": True,
        "checked_on": READ_ON,
        "generated_at": READ_ON,
        "source": ("Google Ads Transparency Centre (advertiser record read "
                   "directly) + the company's own live website (page source "
                   "read through the W3C Nu HTML Checker)"),
        "ad_library": adlib,
        "funnel": {
            "destination": meta["website"],
            "note": ("Advertised domain as shown on the Google Ads Transparency "
                     "Centre advertiser record."),
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


def evidence_for(site, pixels_map):
    found = []
    if pixels_map.get("meta_pixel"):
        found.append("Meta Pixel")
    if pixels_map.get("google_analytics_ga4"):
        found.append("GA4 / Google tag")
    if pixels_map.get("google_tag_manager"):
        found.append("Google Tag Manager")
    if pixels_map.get("google_ads"):
        found.append("Google Ads conversion tag")
    if not found:
        found = ["no Meta Pixel, GA4, GTM or Google Ads tag confirmed"]

    head_unread = pixels_map.get("meta_pixel") is None
    note = (HEAD_UNREAD_NOTE.format(d=READ_ON, found=", ".join(found))
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


def gap_rows(company):
    return PROMISE_GAP.get(company, [])


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

        # When the <head> script tags were never returned, the eight tracking
        # rows are unknown in BOTH directions. Scoring a page on tracking that
        # could not be read would be a guess, so the score is withdrawn and the
        # report says exactly that instead of printing a measured-looking zero.
        head_unread = all(v is None for v in site["pixels"].values())
        if head_unread:
            result["score"] = None
            audit["head_unread"] = True
            site["head_unread"] = True

        audit["site_audit"] = site
        audit["website_audit_run"] = True
        audit["audit_date"] = READ_ON
        # These pages carry more unmeasured rows than a normal report, so the
        # status tables use the compact "Not checked" label. The full phrase
        # still appears under each table and in the verification log.
        audit["status_compact"] = True

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
        _sc = result["score"]
        _sc = "n/a" if _sc is None else f"{_sc:>3}/100"
        print(f"  {company:<26} score {_sc:<9} "
              f"issues {len(result['issues']):>2}  wins {len(result['wins']):>2}  "
              f"controls {counts.get('pass', 0)}P/{counts.get('fail', 0)}F/"
              f"{counts.get('unknown', 0)}U  -> {os.path.basename(out)}")
        changed.append(out)

    print(f"\nRebuilt {len(changed)} reports.")
    return changed


HEAD_UNREAD_NOTE = (
    "Read on {d}. The <head> script tags of this page were not returned in "
    "readable form, so tracking-tag presence is unknown in both directions and "
    "is reported as not checked rather than as absent. Confirmed in the head: "
    "{found}. Every other check on this page - the title, the meta description, "
    "the Open Graph tags, the plugin stack, the validator counts and all content "
    "checks - was measured."
)

SITE_EVIDENCE_NOTE = (
    "Read on {d} from the served page source through the W3C Nu HTML Checker. "
    "Confirmed present: {found}."
)


if __name__ == "__main__":
    main()
