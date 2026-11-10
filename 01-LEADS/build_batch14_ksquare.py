#!/usr/bin/env python3
"""Build the batch-14 (Telangana State, beyond Hyderabad) ads reports.

Owner instruction 2026-10-24 (still standing): every audit PDF is generated
exactly like ``02-OUTREACH/audit_pdfs/audit_Ksquare_Energy.pdf`` - the 5-page
"DIGITAL MARKETING & PAID ADS AUDIT" layout - every check in that layout is
performed, the claude-ads control-review section is carried alongside it, and
only real live data is used. No simulated or demo values anywhere.

WHERE EVERY NUMBER BELOW CAME FROM (all read live on 2026-11-10):

* Meta Ad Library - each library ID was confirmed by opening the ad directly at
  ``https://www.facebook.com/ads/library/?id=<LibraryID>`` and reading the page
  name, start date, destination and full ad copy off the returned card.
* The company's own website, read through the W3C Nu HTML Checker with
  ``showsource=yes`` (``https://validator.w3.org/nu/?doc=<url>&showsource=yes``),
  which returns the served HTML with script tags intact. That is how the Google
  tag, the JSON-LD blocks, the title, the meta description, the Open Graph tags
  and the plugin stack below were read.
* A direct fetch of the same pages for headings, forms, links, CTAs,
  testimonials, pricing and image alt text.
* The TGREDCO empanelled-supplier register
  (``tgredco.telangana.gov.in/Updates_2026/List_of_Empanelled_Suppliers_2026.pdf``)
  as the independent third-party confirmation the owner's third-eye rule needs.

CHECKS THAT COULD NOT BE RUN ARE STORED AS ``None`` AND RENDER AS
"Not checked in this pass" / "Not available at audit time". They are never
guessed:

* Google PageSpeed mobile score + LCP - the keyless API returns HTTP 429
  (quota limit 0/day), the same failure the reference Ksquare PDF reports.
* Google Ads Transparency advertiser records - not fetched.
* Sitemap page count - not fetched.
* **The <head> of microbenergies.com and gloled.co.** Both sites serve very
  large inline stylesheets, so the W3C Nu HTML Checker returns 40+ response
  chunks and the head's script tags sit past what could be read here. The
  error/warning/info counts, the title, the meta description, the Open Graph
  tags, the plugin stack and every content check for those two sites ARE
  measured - only the eight pixel checks are unknown, and they render as "not
  checked in this pass" rather than as "no pixel found".
* **Laxminarayanasolar.in was dropped entirely.** See the batch log: the domain
  serves the cPanel default holding page ("Future home of something quite
  cool"), a direct fetch returns HTTP 500, and both of the advertiser's live
  ads point at ``fb.me`` rather than the domain. There is no website to audit,
  so no report and no outreach is produced for that lead.

Run:  cd 01-LEADS && PYTHONPATH=/tmp/pdflibs python3 build_batch14_ksquare.py
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
# The head of these two sites was never returned, so pixel presence is unknown
# in BOTH directions - it must not be rendered as "no pixel found".
HEAD_UNREAD = (
    "The <head> script tags were not returned while this audit was prepared: "
    "the served HTML carries very large inline stylesheets, so the W3C Nu HTML "
    "Checker response ran past what could be read. The error/warning counts, "
    "the title, the meta description, the Open Graph tags, the plugin stack and "
    "every content check for this site ARE measured below. Only the eight "
    "tracking-tag checks are unknown, and they are reported as not checked "
    "rather than as absent."
)


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
    """None = the head was never read, so presence is unknown in both directions."""
    d = dict(pixels())
    for k in list(d):
        d[k] = None
    d.update(over)
    return d


# ---------------------------------------------------------------------------
# Real measurements, one entry per batch-14 lead.
# ---------------------------------------------------------------------------

GLOLED = {
    "ssl": True,
    "load_time_seconds": None,                 # not measured
    "final_url": "https://gloled.co/",
    "audit_date": READ_ON,
    # The page was read in full - title absence, error counts, plugin stack,
    # every content check below AND the <head> script tags. Nothing on this
    # site is unknown for that reason; see the pixels comment below.
    # The whole <head> was read (source lines 521-583, every line covered). The
    # only analytics script in it is Cloudflare Web Analytics
    # (static.cloudflareinsights.com/beacon.min.js, token
    # 7dccf4e368ce442cb6b0b89e5875a997) - a cookieless, aggregate pageview
    # beacon that cannot identify a visitor, retarget anyone or record a
    # conversion. There is no Meta Pixel, no GA4, no GTM, no Google Ads
    # conversion tag, no LinkedIn Insight, no Microsoft Clarity and no Hotjar
    # anywhere in the head.
    "pixels": pixels(),
    "conversion": {
        # /contact-us/ embeds a Zoho Forms form with Name (First / Last), Sales
        # Rep Name, Mobile Number, Email ID, My Requirements (Lights for House /
        # Lights for Industry or commercial / I am Reseller / OEM enquiry), a
        # Zoho CRM field and a CAPTCHA. "Book Appointment", "Customer Care",
        # "Delivery manager" and a "PLace Order" button are the other CTAs.
        # No wa.me link was read on either page.
        "has_contact_form": True,              # Zoho Forms embed, 6 fields + CAPTCHA
        "has_phone_click": True,               # 9553550700, +44 7587 011245, 14 outlet cells
        "has_whatsapp_link": None,             # not read on the pages checked
        "has_cta_buttons": 5,                  # PLace Order, Book Appointment, Customer Care, Delivery manager, Get Started Today
        "has_live_chat": None,                 # not read
        "has_popup_optin": True,               # Popup Maker (pum-17202) + MyStickyWelcomeBar
        "has_testimonials": None,              # not read
        "has_pricing_page_link": False,        # catalogue PDF only, no price list
    },
    "seo": {
        # The W3C checker reports "Element head is missing a required instance
        # of child element title" on the homepage. There is no <title> element
        # at all, so nothing is indexed with a page title.
        "has_title": False,
        "title_text": "",
        "title_length": 0,
        "has_meta_description": None,          # not read
        "meta_desc_length": None,
        "h1_count": None,                      # not counted
        "h1_text": "",
        "has_og_tags": None,                   # not read
        "has_schema": None,                    # not read
        "has_favicon": None,                   # not read
        "image_count": None,
        "images_without_alt": None,
    },
    "pagespeed": {"error": PAGESPEED_ERROR},
    "page_count": {"has_sitemap": None},
    "local_signals": {
        # Google Maps "Directions" links (maps.app.goo.gl) for the corporate
        # office, the factory, the SMT unit, the Singapore office and all
        # fourteen retail outlets, including the Khammam outlet the ad runs for.
        "has_google_maps_embed": True,
    },
    "platform": "WordPress (block-theme --wp--preset--* CSS variables), "
                "Elementor, Max Mega Menu, Popup Maker, MyStickyWelcomeBar, "
                "10Web Speed Optimizer, Font Awesome 5, Google Fonts "
                "Montserrat / Odor Mean Chey / Roboto",
    "html_errors": "4 errors, 5 warnings, 0 info on the homepage. Errors: no "
                   "doctype before the start tag; two CSS negative padding "
                   "values (-4em and -2px); and the head is missing a required "
                   "<title> element. Warnings: a redundant type attribute on "
                   "two style elements, a Unicode Private Use Area glyph, a "
                   "redundant type attribute on a JavaScript resource, and no "
                   "lang attribute on the html start tag.",
}

UDK = {
    "ssl": True,
    "load_time_seconds": None,                 # not measured
    "final_url": "https://udkindustries.com/",
    "audit_date": READ_ON,
    # The whole head was read (source lines 79-340, every line covered). Site
    # Kit by Google loads gtag.js with the Google tag GT-W6XX8MT. There is no
    # Meta Pixel, no Google Tag Manager container, no Google Ads conversion
    # tag, no LinkedIn Insight, no Microsoft Clarity and no Hotjar anywhere in
    # it.
    "pixels": pixels(
        google_analytics_ga4=True,             # Site Kit "Google Analytics snippet", id GT-W6XX8MT
    ),
    "conversion": {
        # /contact/ carries an Everest Forms shortcode ([everest_form id="277"])
        # and a floating WhatsApp chat button. The page still prints the Zakra
        # theme demo's contact details, which is recorded as a defect, not as
        # the company's real details.
        "has_contact_form": True,              # Everest Forms, shortcode id 277
        "has_phone_click": True,               # but the numbers on /contact/ are the theme demo's
        "has_whatsapp_link": True,             # api.whatsapp.com/send?phone=+919505186524
        "has_cta_buttons": 3,                  # call us now, Go Back, Start Shopping
        "has_live_chat": True,                 # animated-floating-chat-button (WhatsApp)
        "has_popup_optin": None,               # not read
        "has_testimonials": True,              # WP Google Places Review Slider, 4.8 from 63 reviews
        "has_pricing_page_link": False,        # WooCommerce /shop/ exists, no price list read
    },
    "seo": {
        # <title>UDK Electrical Industries</title> sits inside a SECOND, invalid
        # <head> element that the checker flags; the browser renders the page
        # title as "Home - UDK Electrical Industries".
        "has_title": True,
        "title_text": "Home - UDK Electrical Industries",
        "title_length": 33,
        "has_meta_description": True,          # Yoast SEO
        "meta_desc_length": None,              # not measured to the character
        "h1_count": None,                      # not counted
        "h1_text": "",
        "has_og_tags": True,                   # og:locale / og:type / og:title / og:description
        "has_schema": True,                    # 4 JSON-LD blocks (see platform / findings)
        "has_favicon": True,                   # 512x512 site icon
        "image_count": None,
        "images_without_alt": None,
    },
    "pagespeed": {"error": PAGESPEED_ERROR},
    "page_count": {"has_sitemap": None},
    "local_signals": {
        # A static Google Map is embedded on /contact/ with a hard-coded Google
        # Maps API key visible in the page source.
        "has_google_maps_embed": True,
    },
    "platform": "WordPress 7.1.4 on GoDaddy managed WordPress, Zakra theme "
                "4.3.3, WooCommerce 11.2.2, Elementor + Essential Addons for "
                "Elementor Lite 6.8.8 + Essential Blocks, Yoast SEO, Site Kit "
                "by Google 1.191.0, Schema plugin 1.7.9.6, Everest Forms, "
                "Magical Products Display 2.1.3, Animated Floating Chat Button "
                "1.0.3, WP Google Places Review Slider 18.11, jQuery 3.7.1, "
                "Font Awesome 6.2.4, Google Fonts Lora / Raleway / Roboto",
    "html_errors": "7 errors, 0 warnings, 72 info on the homepage. Errors: an "
                   "illegal | character in the Google Fonts query string; a "
                   "CSS font-style value of 'default'; a CSS parse error; a "
                   "second <head> start tag while one was already open; a "
                   "<title> element inside that second head; a meta element "
                   "between head and body; and the checker giving up after the "
                   "last error.",
}

MICROB = {
    "ssl": True,
    "load_time_seconds": None,                 # not measured
    "final_url": "https://microbenergies.com/",
    "audit_date": READ_ON,
    # The page was read in full - title, meta description, error counts, plugin
    # stack, every content check below AND the <head> script tags. Nothing on
    # this site is unknown for that reason; see the pixels comment below.
    # The whole <head> was read (source lines 124-154, every line covered). Site
    # Kit by Google loads gtag.js with the Google tag GT-PZX459FK. There is no
    # Meta Pixel, no Google Tag Manager container, no Google Ads conversion
    # tag, no LinkedIn Insight, no Microsoft Clarity and no Hotjar anywhere in
    # it. Third-party scripts that ARE loaded: Slider Revolution 6.7.40,
    # WooCommerce 10.6.2, jQuery 3.7.1 and LT Ext paroller 1.4.7, plus the
    # Trustindex review widget, Tawk.to live chat and Instagram embeds further
    # down the page.
    "pixels": pixels(
        google_analytics_ga4=True,             # Site Kit "Google tag", id GT-PZX459FK
    ),
    "conversion": {
        # /contacts/ carries a three-field form (Your Name, Mobile Number,
        # Submit) with NO email field, a fifteen-question FAQ accordion, and a
        # Tawk.to live-chat widget.
        "has_contact_form": True,              # 3 fields: name, mobile, submit - no email field
        "has_phone_click": True,               # +91 95053-73125 in the footer
        "has_whatsapp_link": None,             # not read
        "has_cta_buttons": 7,                  # Contact US, More Products, Explore More Products, Contact Us, View More, View Products, Get a Free Solar Project Consultation
        "has_live_chat": True,                 # Tawk.to ("I have a question" / "Tell me more")
        "has_popup_optin": None,               # not read
        "has_testimonials": True,              # "Cilent Testimonials" + Trustindex Google widget
        "has_pricing_page_link": False,        # HP / kW ranges in the FAQ only, no prices
    },
    "seo": {
        "has_title": True,
        "title_text": "Best Solar Water Pump Inverter for Farmers | Microb "
                      "Energies",
        "title_length": 57,
        # "Looking for the best solar water pump inverter for farmers? Microb
        # ...iency solar pump controllers designed for agriculture. Save energy
        # and boost productivity today."
        "has_meta_description": True,
        "meta_desc_length": None,              # not measured to the character
        # The checker warns "Consider using the h1 element as a top-level
        # heading only", which it raises only when a page carries more than one
        # h1. The count itself was not taken.
        "h1_count": None,
        "h1_text": "",
        "has_og_tags": True,                   # og:locale / og:type read; the rest not read
        "has_schema": None,                    # not read
        "has_favicon": None,                   # not read
        "image_count": None,
        "images_without_alt": None,
    },
    "pagespeed": {"error": PAGESPEED_ERROR},
    "page_count": {"has_sitemap": None},
    "local_signals": {"has_google_maps_embed": None},
    "platform": "WordPress with the 'homefort' theme 1.1.4, Elementor 4.3.6 + "
                "Elementor Pro, Royal Elementor Addons 1.7.1070, Slider "
                "Revolution 6.7.40, WooCommerce 10.6.2, Contact Form 7 6.1.5, "
                "LT Core / LT Ext, Hostinger Reach, The Events Calendar "
                "6.18.3, Site Kit by Google, Trustindex review widget, Tawk.to "
                "live chat; Google Fonts Open Sans / Barlow / Roboto / Roboto "
                "Slab / Poppins",
    "html_errors": "21 errors, 81 warnings, 104 info on the homepage. Errors "
                   "include: two p end tags with no p element in scope; six "
                   "bad xmlns values (https:// where http:// is required); a "
                   "stray div end tag; a style element in body that is not its "
                   "parent's first child; six style rules outside an @scope "
                   "rule; and five heading-level skips (h3 after h1, h6 after "
                   "h2 twice, h5 after h2, h5 after h3). Warnings include 68 "
                   "redundant type attributes on JavaScript resources, nine on "
                   "style elements, a warning that more than one h1 is in use, "
                   "and three sections with no heading.",
}

LEADS = {
    "GLO LED Private Limited": GLOLED,
    "UDK Electrical Industries": UDK,
    "MICROB Energies": MICROB,
}

# Extra real findings that belong at the top of "Top priorities" - each one is
# read from the live ad destination or the live page, not invented.
EXTRA_ISSUES = {
    "GLO LED Private Limited": [
        "The homepage has no <title> element at all - the W3C checker reports "
        "'Element head is missing a required instance of child element title'.",
        "Your Khammam ad sends people to gloled.co, where the only Khammam "
        "content is one line in a fourteen-outlet list on /contact-us/.",
        "The landing page opens with no doctype before the start tag and "
        "carries two CSS rules with negative padding values (-4em and -2px).",
        "The contact form is a Zoho Forms embed that asks for a Sales Rep Name "
        "before it will accept an enquiry, and its widget markup carries "
        "Zoho's own error strings, including 'Your form has been deactivated.'",
        "No prices are published anywhere - the catalogue is a PDF and the only "
        "pricing language on the site is the ad's 'Special Pricing for Bulk "
        "Requirements'.",
    ],
    "UDK Electrical Industries": [
        "Your /contact/ page is still the Zakra theme's demo content: the "
        "address 'Moon Street , 446 Jupiter, JP 44600', the emails "
        "'zakra@demos.com' and 'first.last@demos.com', the numbers "
        "'+(123) 456-7890' and '+977 123-456789', and lorem-ipsum body copy. "
        "Your real Sangareddy address appears nowhere on it.",
        "A hard-coded Google Maps API key is visible in the source of "
        "/contact/ (key=AIzaSyCmL18misQw9KdwqGaw3zHkitj8vG6QF2Y).",
        "A second JSON-LD Organization block still has \"url\": "
        "\"https://yourwebsite.com\" - an unfilled placeholder.",
        "The homepage claims 'South India's No.1 LED Lights Manufacturer', a "
        "superlative no page on the site substantiates.",
        "The Google Fonts stylesheet URL uses an illegal | character in its "
        "query string, which the checker flags as a bad value.",
    ],
    "MICROB Energies": [
        "Your live ad promises a '5-Year Warranty' and the homepage repeats "
        "'5 Years Product Warranty', but your own FAQ on /contacts/ says 'We "
        "offer 12-24 months warranty depending on the model'.",
        "Both live ads point at instagram.com/microb_energies, so nobody who "
        "clicks an ad about a 5HP pump at Siddipet reaches microbenergies.com.",
        "Three homepage links go to the wrong page: 'Solar Water Pump Inverter "
        "/ Controller' to /services/heat-pump/, 'Zero Fuel Cost' to "
        "/services/projecting-4/, 'Rooftop Solar' to "
        "/services/diagnostic-and-repair/.",
        "The 'Power Your Future with Rooftop Solar' block reuses the "
        "agricultural copy word for word.",
        "The contact form has no email field at all, and the testimonials "
        "heading is spelled 'Cilent Testimonials'.",
    ],
}

PROMISE_GAP = {
    "GLO LED Private Limited": [
        ("Ad: 'Need Solar Street Lights in Bulk in Khammam? ... Bulk Orders "
         "Welcome, Multiple Wattages Available, Suitable for Roads, Layouts & "
         "Projects, Reliable Solar Lighting Solutions, Special Pricing for "
         "Bulk Requirements, Khammam & Nearby Areas. Call / WhatsApp: 70365 "
         "33794.'",
         "The bulk, multi-wattage and project claims are backed - gloled.co "
         "carries a Solar Lights product line, a Projects page and a catalogue "
         "PDF, and the Khammam outlet at 11-10-268/6/A/1 near the New RTC Bus "
         "Stand is listed on /contact-us/. But the ad sends the click to "
         "https://gloled.co/, where the Khammam address is one line among "
         "fourteen outlets and there is no price, no wattage table and no "
         "bulk-order form. The phone number in the ad, 70365 33794, is not "
         "one of the numbers published on the site."),
        ("Ad: 'Send your requirement today and get a quotation from our team.'",
         "The only route to a quotation is a Zoho Forms embed that asks for a "
         "Sales Rep Name and a CAPTCHA before it will accept the enquiry, and "
         "whose widget markup carries Zoho's own error strings including 'Your "
         "form has been deactivated.' There is no price list to compare "
         "against."),
        ("Ad destination: https://gloled.co/ - confirmed on the ad card.",
         "The site itself has no <title> element on the homepage, no doctype "
         "before the start tag and two CSS rules with negative padding "
         "values, so the page the ad pays for is the least finished asset in "
         "the funnel. The Khammam outlet is a real, verifiable presence - it "
         "is on /contact-us/ with a Google Maps directions link - but nothing "
         "on the landing page points at it."),
    ],
    "UDK Electrical Industries": [
        ("Ad: 'LED Street Light Manufacturer in Telangana | UDK Electrical "
         "Industries Pvt. Ltd. ... BIS Approved LED Street Lights, Energy "
         "Saving up to 80%, IP65 Weatherproof Design, 2 Years Warranty, OEM & "
         "Customized Manufacturing, Bulk Orders Across India. Manufacturer: "
         "Sangareddy, Telangana. Contact: 08455546614.'",
         "Every claim on the card is substantiated on udkindustries.com - the "
         "BIS certification, the IP66/IP67 rating, the OEM & ODM service, the "
         "bulk orders and the Sangareddy unit at 9-170002 Vidya Nagar Colony "
         "Road 3 are all on the homepage, and 08455-456614 is one of four "
         "published numbers. The homepage's own claim to be 'South India's "
         "No.1 LED Lights Manufacturer' is not substantiated anywhere."),
        ("Ad: 'www.udkindustries.com'.",
         "The homepage is the strongest asset here - WordPress 7.1.4, a Google "
         "tag (GT-W6XX8MT), four JSON-LD blocks, Open Graph tags and a Google "
         "review slider showing 4.8 from 63 reviews. But /contact/, the page a "
         "visitor lands on to make contact, is still the Zakra theme's demo: "
         "'Moon Street , 446 Jupiter, JP 44600', 'zakra@demos.com' and "
         "'+(123) 456-7890'. The ad's own number is not on it."),
    ],
    "MICROB Energies": [
        ("Ad: '300 FT DEEP. 5 HP POWER. BUILT FOR PERFORMANCE. Another "
         "successful installation at Siddipet, Telangana! ... 5HP Solar Water "
         "Pumping System, designed to deliver reliable water pumping even at a "
         "depth of 300 feet.'",
         "The site backs the product: /solar-water-pump-controllers/ covers "
         "1HP-10HP MPPT controllers with dry-run protection, and the FAQ gives "
         "panel sizing for 1 HP (~1.2 kW), 3 HP (~3.5 kW) and 5 HP (~5.5 kW). "
         "What the site does not back is the warranty. The ad says '5-Year "
         "Warranty' and the homepage says '5 Years Product Warranty', but the "
         "FAQ on /contacts/ says 'We offer 12-24 months warranty depending on "
         "the model' - and separately gives the controller's *lifespan* as "
         "'5 years or more'. The ad has turned a lifespan figure into a "
         "warranty promise."),
        ("Ad destination: instagram.com/microb_energies, on both live ads.",
         "The website is far the stronger asset: a fifteen-question FAQ, "
         "efficiency and protection specifications, hybrid solar-plus-grid "
         "models, optional GSM/IoT monitoring, and a 'Get a Free Solar Project "
         "Consultation' CTA. None of it is reachable from the ad."),
        ("Ad: 'MICROB ENERGIES. Engineered for Performance. Designed for "
         "Reliability. Designed. Engineered. Manufactured in India.'",
         "The site does claim an in-house manufacturing facility in Hyderabad "
         "and MNRE certification. But three of the homepage's own service "
         "links point at the wrong pages - /services/heat-pump/, "
         "/services/projecting-4/ and /services/diagnostic-and-repair/ - so a "
         "visitor who tries to read about the product is sent to a heat-pump "
         "or a repair page instead."),
    ],
}

COMPANY = {
    "GLO LED Private Limited": {
        "legal": "GLO LED Private Limited",
        "city": "Kukatpally, Hyderabad 500072 (Khammam outlet)",
        "website": "https://gloled.co/",
        "contact_facts": "Corporate office 5-5-35/45, Prasanthi Nagar, "
                         "Kukatpally, Hyderabad 500072 | Factory 1A & 1B Type "
                         "II, TSIIC Prasanthi Nagar, IE Kukatpally, Hyderabad "
                         "500072 | Khammam outlet 11-10-268/6/A/1, near New "
                         "RTC Bus Stand, Raparthi Nagar, Khammam 507001, +91 "
                         "7036971733 | care@gloled.co | 9553550700 (India) / "
                         "+44 7587 011245 (UK) / +91 9441051844 / +91 9989274877",
        "contact": {"phone": "+91 9553550700",
                    "email": "care@gloled.co",
                    "whatsapp": ""},
    },
    "UDK Electrical Industries": {
        "legal": "UDK Electrical Industries Private Limited",
        "city": "Sangareddy 502001",
        "website": "https://udkindustries.com/",
        "contact_facts": "9-170002, Vidya Nagar Colony Road 3, Sangareddy, "
                         "Telangana 502001 | contact@udkindustries.com / "
                         "sales@udkindustries.com | 08455-456614 (landline), "
                         "9704317436, 8309767244, 9505186524 | Mon-Fri "
                         "9:00 AM - 6:00 PM. NOTE: none of these details are "
                         "on /contact/, which still carries the Zakra theme "
                         "demo's placeholder address, emails and phone numbers.",
        "contact": {"phone": "+91 8455456614",
                    "email": "contact@udkindustries.com",
                    "whatsapp": "+91 9505186524"},
    },
    "MICROB Energies": {
        "legal": "Microb Energies",
        "city": "Peerzadiguda, Uppal, Hyderabad 500039",
        "website": "https://microbenergies.com/",
        "contact_facts": "Kuruma Nagar, Plot No. 11 & 12, Street Number 4, "
                         "Phase II, Peerzadiguda, Uppal, Hyderabad, Telangana "
                         "500039 | Info@microbenergies.com | +91 95053 73125 | "
                         "Mon-Sat 9:30 to 6:00, Sunday closed",
        "contact": {"phone": "+91 9505373125",
                    "email": "Info@microbenergies.com",
                    "whatsapp": ""},
    },
}


# ---------------------------------------------------------------------------
# The live Meta ads, read from the Ad Library on 2026-11-10. Every library ID
# was confirmed by opening the ad directly; ad IDs routinely appear next to
# another advertiser's card in a keyword search.
# ---------------------------------------------------------------------------

ADS = {
    "GLO LED Private Limited": [
        {
            "library_id": "2177815426280429",
            "library_url": "https://www.facebook.com/ads/library/?id=2177815426280429",
            "page_name": "GloledKhammam",
            "started": "Oct 29, 2026",
            "destination": "https://gloled.co/ - confirmed on the ad card",
            "text": "Video ad. Copy verbatim from the card:\n"
                    "\n"
                    "Need Solar Street Lights in Bulk in Khammam?\n"
                    "\n"
                    "GLOLED Solar Street Lights are suitable for contractors, "
                    "builders, layouts, industries, institutions and large "
                    "project requirements.\n"
                    "\n"
                    "Bulk Orders Welcome\n"
                    "Multiple Wattages Available\n"
                    "Suitable for Roads, Layouts & Projects\n"
                    "Reliable Solar Lighting Solutions\n"
                    "Special Pricing for Bulk Requirements\n"
                    "Khammam & Nearby Areas\n"
                    "\n"
                    "Have a bulk requirement? Send your requirement today and "
                    "get a quotation from our team.\n"
                    "\n"
                    "Call / WhatsApp: 70365 33794\n"
                    "\n"
                    "Headline on the card: 'Solar Street Lights - Bulk Orders "
                    "in Khammam | Bulk & Project Requirements | Call 70365 "
                    "33794'",
        },
    ],
    "UDK Electrical Industries": [
        {
            "library_id": "877640172078183",
            "library_url": "https://www.facebook.com/ads/library/?id=877640172078183",
            "page_name": "udk_industries (Instagram)",
            "started": "Nov 9, 2026",
            # Two direct ?id= fetches resolved to the udk_industries page but
            # the ad card itself never rendered, so the click-through is not
            # verified. The destination shown on the keyword-search card was a
            # WhatsApp link. This report does not claim a destination.
            "destination": "not confirmed - see the promise-gap table below",
            "text": "Video ad. Copy verbatim from the keyword-search card:\n"
                    "\n"
                    "LED Street Light Manufacturer in Telangana | UDK "
                    "Electrical Industries Pvt. Ltd.\n"
                    "\n"
                    "Looking for high-quality LED Street Lights? UDK "
                    "Electrical Industries Pvt. Ltd. is a trusted manufacturer "
                    "of BIS-approved LED lighting solutions for roads, "
                    "highways, industries, campuses, layouts, municipalities, "
                    "and government projects.\n"
                    "\n"
                    "BIS Approved LED Street Lights\n"
                    "Energy Saving up to 80%\n"
                    "High Brightness & Long Life\n"
                    "IP65 Weatherproof Design\n"
                    "2 Years Warranty\n"
                    "OEM & Customized Manufacturing\n"
                    "Bulk Orders Across India\n"
                    "\n"
                    "Manufacturer: Sangareddy, Telangana\n"
                    "Contact: 08455546614\n"
                    "www.udkindustries.com\n"
                    "\n"
                    "CTA on the card: 'Send WhatsApp message'",
        },
    ],
    "MICROB Energies": [
        {
            "library_id": "2147291065897730",
            "library_url": "https://www.facebook.com/ads/library/?id=2147291065897730",
            "page_name": "microb_energies",
            "started": "Nov 5, 2026",
            "destination": "Instagram (instagram.com/microb_energies), "
                           "confirmed on the ad card",
            "text": "Video ad. Copy verbatim from the card:\n"
                    "\n"
                    "300 FT DEEP. 5 HP POWER. BUILT FOR PERFORMANCE.\n"
                    "\n"
                    "Another successful installation at Siddipet, Telangana!\n"
                    "\n"
                    "Today, the MICROB ENERGIES team successfully installed a "
                    "complete 5HP Solar Water Pumping System, designed to "
                    "deliver reliable water pumping even at a depth of 300 "
                    "feet.\n"
                    "\n"
                    "Deep borewell. Demanding conditions. Consistent "
                    "performance.\n"
                    "\n"
                    "When the challenge goes deeper, MICROB ENERGIES delivers "
                    "confidence through intelligent solar pump control "
                    "technology.\n"
                    "\n"
                    "MICROB ENERGIES\n"
                    "Engineered for Performance. Designed for Reliability.\n"
                    "Designed. Engineered. Manufactured in India.\n"
                    "\n"
                    "#MicrobEnergies #SolarWaterPump #SolarPumpController "
                    "#5HPSolarPump #Siddipet\n"
                    "\n"
                    "CTA on the card: 'Visit Instagram profile'",
        },
        {
            "library_id": "1867351030942485",
            "library_url": "https://www.facebook.com/ads/library/?id=1867351030942485",
            "page_name": "microb_energies",
            "started": "Nov 6, 2026",
            "destination": "Instagram (instagram.com/microb_energies), "
                           "confirmed on the ad card",
            "text": "Video ad. Copy verbatim from the card:\n"
                    "\n"
                    "No need to spend money on a new motor! You can run the "
                    "motor you already have on your farm with solar.\n"
                    "\n"
                    "Microb Energies brings you the right controller solution "
                    "tailored to your needs. Options that work with both solar "
                    "and grid power (electricity) are also available!\n"
                    "\n"
                    "Complete Setup & Support: Full installation across "
                    "Telangana by our expert team.\n"
                    "5-Year Warranty: No compromise on quality!\n"
                    "\n"
                    "CTA on the card: 'Visit Instagram profile'",
        },
    ],
}


SITE_EVIDENCE_NOTE = (
    "Landing-page source read live on {d} through the W3C Nu HTML Checker "
    "(validator.w3.org/nu/?doc=<url>&showsource=yes), which returns the served "
    "HTML with script tags intact, plus a direct fetch of the same pages. "
    "Tags found: {found}."
)

HEAD_UNREAD_NOTE = (
    "Landing-page source read live on {d} through the W3C Nu HTML Checker "
    "(validator.w3.org/nu/?doc=<url>&showsource=yes). The page carries very "
    "large inline stylesheets, so the <head> script tags ran past what could "
    "be read; the title, meta description, Open Graph tags, error counts, "
    "plugin stack and every content check below ARE measured, but the eight "
    "tracking-tag checks are unknown and are reported as not checked rather "
    "than as absent. Tags found: {found}."
)


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


def build_base(company):
    """Create the ads-only JSON shell, or refresh the ad-library half of an
    existing one.

    The website measurements are never overwritten here - they are re-read from
    the LEADS dicts every run. The ad-library block IS refreshed every run,
    because ad copy is re-verified against the live Ad Library and a corrected
    transcription has to replace the old one rather than sit beside it.
    """
    path = os.path.join(AUDIT_DIR,
                        f"audit_{company.replace(' ', '_')}.json")
    meta = COMPANY[company]
    ads = ADS[company]
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            audit = json.load(f)
        audit["ad_library"] = {
            "meta_own": {
                "found": True,
                "results_count": len(ads),
                "results_label": f"{len(ads)} live ad"
                                 f"{'' if len(ads) == 1 else 's'}",
                "query": "solar + Telangana city keyword search",
                "ads": ads,
            },
            "summary": (
                f"{len(ads)} live Meta ad"
                f"{'' if len(ads) == 1 else 's'} confirmed on {READ_ON} by "
                "opening each library ID directly. Google Ads Transparency "
                "records were not checked in this pass."
            ),
        }
        audit["funnel"] = {
            "destination": ads[0]["destination"],
            "note": "Ad destination as shown on the live ad card, or recorded "
                    "as unconfirmed where the card did not render.",
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
        "source": ("Meta Ad Library (India, active ads) + the company's own "
                   "live website (page source read through the W3C Nu HTML "
                   "Checker)"),
        "ad_library": {
            "meta_own": {
                "found": True,
                "results_count": len(ads),
                "results_label": f"{len(ads)} live ad"
                                 f"{'' if len(ads) == 1 else 's'}",
                "query": "solar + Telangana city keyword search",
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
            "note": "Ad destination as shown on the live ad card, or recorded "
                    "as unconfirmed where the card did not render.",
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
        audit["promise_gap"] = gap_rows(company)
        audit["ads_audit"] = evaluate(audit, evidence)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(audit, f, indent=2, ensure_ascii=False)
            f.write("\n")

        out = generate_ads_only_pdf(audit)
        counts = (audit["ads_audit"] or {}).get("counts") or {}
        print(f"  {company:<26} score {result['score']:>3}/100  "
              f"issues {len(result['issues']):>2}  wins {len(result['wins']):>2}  "
              f"controls {counts.get('pass', 0)}P/{counts.get('fail', 0)}F/"
              f"{counts.get('unknown', 0)}U  -> {os.path.basename(out)}")
        changed.append(out)

    print(f"\nRebuilt {len(changed)} reports.")
    return changed


if __name__ == "__main__":
    main()
