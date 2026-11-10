#!/usr/bin/env python3
"""Build the batch-13 (Hyderabad / Telangana) ads reports from real measurements.

Owner instruction 2026-10-24 (still standing): every audit PDF is generated
exactly like ``02-OUTREACH/audit_pdfs/audit_Ksquare_Energy.pdf`` - the 5-page
"DIGITAL MARKETING & PAID ADS AUDIT" layout - every check in that layout is
performed, the claude-ads control-review section is carried alongside it, and
only real live data is used. No simulated or demo values anywhere.

WHERE EVERY NUMBER BELOW CAME FROM (all read live on 2026-11-10):

* Meta Ad Library - each library ID was confirmed by opening the ad directly at
  ``https://www.facebook.com/ads/library/?id=<LibraryID>`` and reading the page
  name, start date, destination and full ad copy off the returned card. Ad IDs
  routinely appear next to another advertiser's card in a keyword search, so an
  ID is only recorded here when the metadata block and its own card were
  adjacent in the same response.
* The company's own website, read through the W3C Nu HTML Checker with
  ``showsource=yes`` (``https://validator.w3.org/nu/?doc=<url>&showsource=yes``),
  which returns the served HTML with script tags intact. That is how the Meta
  Pixel / GA4 / GTM / Google Ads tags, the JSON-LD blocks, the title, the meta
  description, the Open Graph tags and the plugin stack below were read.
* A direct fetch of the same pages for headings, forms, links, CTAs,
  testimonials, pricing and image alt text.
* The TGREDCO empanelled-supplier registers (``tgredco.telangana.gov.in``,
  2025 and 2026 editions) as the **independent third-party confirmation** the
  owner's third-eye rule requires.

CHECKS THAT COULD NOT BE RUN ARE STORED AS ``None`` AND RENDER AS
"Not checked in this pass" / "Not available at audit time". They are never
guessed:

* Google PageSpeed mobile score + LCP - the keyless API returns HTTP 429
  (quota limit 0/day), the same failure the reference Ksquare PDF reports.
* Google Ads Transparency advertiser records - not fetched.
* Sitemap page count - not fetched.
* **Arka Solar Power's whole site.** ``arkasolarpower.com`` could not be read
  on 2026-11-10: the W3C Nu HTML Checker returned an IO error
  (``java.io.EOFException``) for the homepage, the ``www`` host and an inner
  page, and a direct fetch returned HTTP 500 for the homepage and two inner
  pages. The site is live - its Meta ad has been running since 30 Oct 2026 and
  its pages are indexed - but its served HTML was not retrievable through any
  channel available here, so every pixel, SEO, conversion and error-count field
  for Arka is recorded as ``None``. The report says so rather than asserting
  anything. ``verify_live.py`` re-fetches it on the owner's machine, where the
  TLS path may succeed.

Run:  cd 01-LEADS && PYTHONPATH=/tmp/pdflibs python3 build_batch13_ksquare.py
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
ARKA_UNREADABLE = (
    "Not checked - the site could not be read on 2026-11-10. The W3C Nu HTML "
    "Checker returned an IO error (java.io.EOFException) for "
    "https://arkasolarpower.com/, the www host and an inner page, and a direct "
    "fetch returned HTTP 500. No figure is claimed for this check."
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


def unchecked(**over):
    """Every field None - used for a page that could not be retrieved at all."""
    d = {
        "has_contact_form": None,
        "has_phone_click": None,
        "has_whatsapp_link": None,
        "has_cta_buttons": None,
        "has_live_chat": None,
        "has_popup_optin": None,
        "has_testimonials": None,
        "has_pricing_page_link": None,
    }
    d.update(over)
    return d


def unchecked_seo(**over):
    d = {
        "has_title": None,
        "title_text": "",
        "title_length": None,
        "has_meta_description": None,
        "meta_desc_length": None,
        "h1_count": None,
        "h1_text": "",
        "has_og_tags": None,
        "has_schema": None,
        "has_favicon": None,
        "image_count": None,
        "images_without_alt": None,
    }
    d.update(over)
    return d


# ---------------------------------------------------------------------------
# Real measurements, one entry per batch-13 lead.
# ---------------------------------------------------------------------------

AADITHYA = {
    "ssl": True,
    "load_time_seconds": None,                 # not measured
    "final_url": "https://aadithyasolarenergies.com/",
    "audit_date": READ_ON,
    # The whole <head> was read (source lines 1-122, every line covered): RSS and
    # oEmbed links, WordPress 7.0.8 generator tag, canonical, shortlink,
    # favicons, Elementor / Contact Form 7 / Table Addons stylesheets, Google
    # Fonts. There is no Meta Pixel, no GA4, no GTM, no Google Ads conversion
    # tag, no Open Graph block and no JSON-LD structured data anywhere in it.
    "pixels": pixels(),
    "conversion": {
        # /contact/ carries a Contact Form 7 form (the plugin stylesheet
        # contact-form-7/includes/css/styles.css is enqueued in the head) with
        # the fields Full Name / Phone / Email / Message and a "Submit now"
        # button. "explore more" and "Discover More" are the only CTAs, and
        # "Discover More" points at http://themexriver.com/ - the theme
        # vendor's own site, not a page of the advertiser's.
        "has_contact_form": True,              # Contact Form 7, 4 fields + submit
        "has_phone_click": True,               # tel:+91-9491032828 in the footer
        "has_whatsapp_link": False,            # no wa.me link anywhere read
        "has_cta_buttons": 4,                  # explore more x2, Discover More, Submit now
        "has_live_chat": False,                # no chat widget in the source
        "has_popup_optin": False,              # no opt-in popup in the source
        "has_testimonials": False,             # no review or testimonial block read
        "has_pricing_page_link": False,        # system sizes only, no pricing page
    },
    "seo": {
        # The title is read off the live RSS feed link in the head:
        # <link rel="alternate" ... title="Aadithya Solar Energies &raquo; Feed">
        "has_title": True,
        "title_text": "Aadithya Solar Energies",
        "title_length": 24,
        # The meta description is the theme's own default placeholder, never
        # customised for the business.
        "has_meta_description": True,
        "meta_desc_length": 27,
        # The validator flagged 4 separate <h1> elements on the homepage, and
        # heading levels skip from h2 to h5 and from h1 to h5.
        "h1_count": 4,
        "h1_text": "",
        "has_og_tags": False,                  # no og:* block in the head
        "has_schema": False,                   # no JSON-LD in the head
        "has_favicon": True,                   # 32x32 and 192x192 site icons
        "image_count": None,                   # not counted on the full page
        "images_without_alt": None,
    },
    "pagespeed": {"error": PAGESPEED_ERROR},
    "page_count": {"has_sitemap": None},
    "local_signals": {"has_google_maps_embed": True},
    "platform": "WordPress 7.0.8, theme 'eergx' (themexriver.com/wp/eergx/), "
                "Elementor, Contact Form 7 6.1.6, Table Addons for Elementor, "
                "Bootstrap, Font Awesome, Google Fonts Inter / AR One Sans / "
                "Roboto / Roboto Slab",
    "html_errors": "55 errors, 10 warnings, 59 info on the homepage",
}

SUNX = {
    "ssl": True,
    "load_time_seconds": None,                 # not measured
    "final_url": "https://sunxsolarsolutions.in/",
    "audit_date": READ_ON,
    # The whole <head> was read on both / and /contact: canonical, Open Graph,
    # Twitter cards, favicons, webmanifest, a LocalBusiness JSON-LD block, one
    # stylesheet and one inline script. No Meta Pixel, no GA4, no GTM and no
    # Google Ads conversion tag anywhere in it.
    "pixels": pixels(),
    "conversion": {
        # /contact carries a "book a free site survey" flow, the hero has two
        # CTAs and the nav a third; /calculator is a savings calculator, not a
        # published price list. The contact page's meta description advertises
        # WhatsApp, but no wa.me link was read, so that field stays unverified.
        "has_contact_form": True,              # free site survey form on /contact
        "has_phone_click": True,               # tel:+919912127174 in the topbar
        "has_whatsapp_link": None,             # advertised, but no link read
        "has_cta_buttons": 4,                  # Get a quote (nav + hero), Contact us, All solutions
        "has_live_chat": None,                 # not read
        "has_popup_optin": None,               # not read
        "has_testimonials": None,              # not read
        "has_pricing_page_link": False,        # /calculator is a savings tool, no prices published
    },
    "seo": {
        "has_title": True,
        "title_text": "Solar & Wind Energy Company in Hyderabad | SunX Solar "
                      "and Renewable Solutions",
        "title_length": 74,
        "has_meta_description": True,          # unique per page, 160+ chars
        "meta_desc_length": None,              # not measured to the character
        "h1_count": 1,                         # "Clean power your building makes for itself"
        "h1_text": "Clean power your building makes for itself",
        "has_og_tags": True,                   # og:type/site_name/title/description/url/image/width/height/locale
        "has_schema": True,                    # JSON-LD LocalBusiness with telephone, address, hours
        "has_favicon": True,                   # 32x32, 512x512, apple-touch-icon
        "image_count": None,                   # not counted on the full page
        "images_without_alt": None,            # hero image only carries alt=""
    },
    "pagespeed": {"error": PAGESPEED_ERROR},
    "page_count": {"has_sitemap": None},
    "local_signals": {"has_google_maps_embed": True},
    "platform": "Hand-written static HTML site (assets/css/style.css, "
                "site.webmanifest, inline SVG icons), Plus Jakarta Sans + Inter "
                "from Google Fonts, LocalBusiness JSON-LD",
    "html_errors": "2 errors, 1 warning, 0 info on the homepage; the same 2 "
                   "errors and 1 warning on /contact",
}

ARKA = {
    "ssl": None,
    # No score may be claimed for a site that could not be read at all - a
    # "0/100" would read as "this site is flawless", which is the opposite of
    # the truth. The report renders "N/A - site not read" instead.
    "score_unavailable": True,
    "scope_note": (
        "arkasolarpower.com is live and its Meta ad has run since 30 Oct 2026, "
        "but the site could not be retrieved while this audit was prepared: "
        "the W3C checker returned an IO error for the homepage, the www host "
        "and an inner page, and a direct fetch returned HTTP 500, all on "
        "2026-11-10. Every website row below therefore reads 'not checked in "
        "this pass', and no audit score, pixel finding, page-speed figure or "
        "error count is claimed for this site anywhere in this report. "
        "Re-running the audit on a working connection is the first action on "
        "the last page."
    ),
    "load_time_seconds": None,                 # not measured
    "final_url": "https://arkasolarpower.com/",
    "audit_date": READ_ON,
    # The head was never returned, so presence is unknown in both directions.
    "pixels": unknown_pixels(),
    "conversion": unchecked(),
    "seo": unchecked_seo(),
    "pagespeed": {"error": PAGESPEED_ERROR},
    "page_count": {"has_sitemap": None},
    "local_signals": {"has_google_maps_embed": None},
    "platform": "Not read - " + ARKA_UNREADABLE,
    "html_errors": ARKA_UNREADABLE,
}

LEADS = {
    "Aadithya Solar Energies": AADITHYA,
    "SunX Solar and Renewable Solutions": SUNX,
    "The Arka Solar Power": ARKA,
}

# Extra real findings that belong at the top of "Top priorities" - each one is
# read from the live ad destination or the live page, not invented.
EXTRA_ISSUES = {
    "Aadithya Solar Energies": [
        "Your live ad's 'Book now' button goes to http://fb.me/ - a Facebook "
        "link shortener - not to aadithyasolarenergies.com, so the spend never "
        "reaches the site you are paying to advertise.",
        "With no Meta Pixel, no GA4 and no Google Ads tag anywhere in the "
        "site's <head>, nothing on aadithyasolarenergies.com can record who "
        "clicked, so even a visitor who does arrive cannot be counted or "
        "retargeted.",
        "The <head> still carries the theme's default meta description, "
        "'Solar Energy WordPress Theme' - the text Google shows under your "
        "listing has never been written for your business.",
        "The theme is unfinished: the header prints the placeholder phone "
        "(229) 555-0109, the email link is labelled 'example@email.com', the "
        "service and 'About' links point at the theme demo on themexriver.com, "
        "and the footer shows two different addresses.",
    ],
    "SunX Solar and Renewable Solutions": [
        "Your live ad's 'Send message' button goes to "
        "instagram.com/sunxsolarsolutions, not to sunxsolarsolutions.in, so "
        "the click lands in a social inbox instead of on the site that "
        "explains the offer.",
        "The ad tells people to call 8333075151, but the number published on "
        "the website is +91 99121 27174 - a caller who reaches one and not the "
        "other has no way to tell they reached the same company.",
        "sunxsolarsolutions.in has no Meta Pixel, no GA4 and no Google Ads "
        "conversion tag, so the Diwali offer cannot be measured from click to "
        "enquiry even once the destination is fixed.",
    ],
    "The Arka Solar Power": [
        "Your live ad's destination is an fb.me link, so the click does not "
        "reach arkasolarpower.com and the site's own claims - 'No.1 Solar "
        "Company in Telangana', '700+ happy homes' - are never shown to the "
        "person who paid attention to the ad.",
        "arkasolarpower.com could not be read on 2026-11-10 (the W3C checker "
        "returned an IO error and a direct fetch returned HTTP 500), so this "
        "audit records the site's tracking, SEO and conversion setup as not "
        "checked rather than guessing. Re-running the check on a working "
        "connection is the first thing to do before this report is sent.",
    ],
}

# The ad promise vs what the live landing page actually delivers.
PROMISE_GAP = {
    "Aadithya Solar Energies": [
        ("Ad: 'Rs.78,000 వరకు Solar Subsidy వివరాల కోసం మీ వివరాలు నమోదు "
         "చేయండి' - register your details for solar subsidy information up to "
         "Rs.78,000, under the PM Surya Ghar Muft Bijli Yojana, with rooftop "
         "installation, bill savings and bank-loan help listed as tick-box "
         "benefits.",
         "The subsidy figure and the service list are real and are on the site "
         "- EPC Services, Solar Rooftop Solutions, Residential Solar "
         "Installations and Solar Street Light and Fencing, with 5KW / 20KW / "
         "45KW system sizes. But the ad's 'Book now' button goes to fb.me, so "
         "the visitor is asked to register on a Facebook page instead of the "
         "page that lists those services."),
        ("Ad: 'Aadithya Solar Energies ను ఈరోజే సంప్రదించండి, Call: 94910 "
         "32828'.",
         "That number is on the site (tel:+91-9491032828 in the footer) - but "
         "the header of the same page still prints the theme's placeholder "
         "(229) 555-0109 above it, so a visitor sees two different phone "
         "numbers before they reach the real one."),
        ("Ad: 'మీ ఇంటి మీదే మీ సొంత Power Plant' - your own power plant on "
         "your own roof.",
         "The site does describe rooftop solar and a Google Maps embed of the "
         "Gandipet office is on /contact/. Nothing on the site answers the "
         "question the ad raises - there is no savings calculator, no "
         "subsidy table and no price, and the only CTA is a 'Discover More' "
         "link that leaves the site for the theme vendor's homepage."),
    ],
    "SunX Solar and Renewable Solutions": [
        ("Ad: 'Diwali special offer ... Silver coin, Fridge, Washing machine, "
         "Water purifier, Smart phone. For more details about sunx solar "
         "solutions please call 8333075151'.",
         "The offer itself is only on Facebook. sunxsolarsolutions.in "
         "publishes no Diwali promotion anywhere in its served HTML, and the "
         "number it publishes is +91 99121 27174 - so a visitor who lands on "
         "the site cannot find the offer they were shown, and the number in "
         "the ad does not match the one on the page."),
        ("Ad destination: instagram.com/sunxsolarsolutions, 'Send message'.",
         "The site is the better asset - it has a LocalBusiness JSON-LD block "
         "with both phone numbers, the Serilingampally address, Mon-Sat "
         "09:30-19:00 hours, a /calculator savings tool and a /sales quote "
         "form - but the ad never sends anyone to any of it."),
        ("Ad: 'solarenergy #diwalispecial #offer'.",
         "The site is built for exactly this traffic: rooftop grid-tied, "
         "hybrid + storage, ground-mount, C&I and O&M pages, a wind-energy "
         "page and a projects page. The only thing standing between the ad and "
         "those pages is the destination - and, once that is fixed, the "
         "absence of any pixel to measure it."),
    ],
    "The Arka Solar Power": [
        ("Ad: 'reduce your electricity bill by more than 90%', 'Subsidy "
         "Benefits Available', 'Easy EMI / Loan Options', '25+ Years "
         "Performance', 'Govt. Approved Installation', 'Free Site Inspection'.",
         "Six specific claims in one ad. The site backs the segment and the "
         "subsidy angle - 'No.1 Solar Company in Telangana', industrial, "
         "commercial and residential solar plus solar water heaters - but the "
         "ad's destination is an fb.me link, so none of the supporting detail "
         "is shown to the person reading the ad, and nothing on this pass "
         "verified which of the six the site substantiates."),
        ("Ad: 'Attention home owners of Hyderabad!'",
         "The TGREDCO empanelled-supplier register carries Arka Solar Power at "
         "HMT Nagar, Nacharam, Hyderabad 500076 (registration TSRE240412, "
         "phone 7989343107) and the company is registered as ARKA SOLAR POWER "
         "(INDIA) PRIVATE LIMITED, CIN U40102TG2015PTC101798, incorporated "
         "20 Nov 2015 - so the Hyderabad EPC claim is independently "
         "confirmed. The registration number alone is not enough: the same "
         "TSRE240412 is also listed against 'M/s. ARKA ENTERPRISES' of "
         "Yusufguda, so only the website and Facebook page identify the "
         "advertiser."),
    ],
}

COMPANY = {
    "Aadithya Solar Energies": {
        "legal": "Aadithya Solar Energies",
        "city": "Gandipet, Hyderabad 500086",
        "website": "https://aadithyasolarenergies.com/",
        "contact_facts": "Sy.No.186, Near Water Tank, Kismatpur, Gandipet "
                         "Mandal, Ranga Reddy District, Telangana 500086 (the "
                         "/contact/ page also prints Plot No. 42, Himayath "
                         "Sagar, Bandlaguda Jagir, Gandipet Mandal) | "
                         "info@aadithyasolarenergies.com | +91 94910 32828",
        "contact": {"phone": "+91 94910 32828",
                    "email": "info@aadithyasolarenergies.com",
                    "whatsapp": ""},
    },
    "SunX Solar and Renewable Solutions": {
        "legal": "SunX Solar and Renewable Solutions",
        "city": "Serilingampally, Hyderabad 500032",
        "website": "https://sunxsolarsolutions.in/",
        "contact_facts": "H.No. 1152, 1st Floor, BHEL Old MIG Colony, "
                         "Serilingampally, Ranga Reddy District, Hyderabad "
                         "500032 | nitish@sunxsolarsolutions.in | "
                         "+91 99121 27174 | Mon-Sat 09:30-19:00",
        "contact": {"phone": "+91 99121 27174",
                    "email": "nitish@sunxsolarsolutions.in",
                    "whatsapp": ""},
    },
    "The Arka Solar Power": {
        "legal": "The Arka Solar Power",
        "city": "Nacharam, Hyderabad 500076",
        "website": "https://arkasolarpower.com/",
        "contact_facts": "HMT Nagar, Nacharam, Hyderabad 500076 (TGREDCO "
                         "registration TSRE240412; registered office "
                         "8-1-293/A/71/1, Dwaraka Nagar Colony, Shaikpet, "
                         "Hyderabad 500081) | info@arkasolarpower.com | "
                         "+91 91330 41888 (Telangana)",
        "contact": {"phone": "+91 91330 41888",
                    "email": "info@arkasolarpower.com",
                    "whatsapp": ""},
    },
}


# ---------------------------------------------------------------------------
# The live Meta ads, read from the Ad Library on 2026-11-10. Every library ID
# was confirmed by opening the ad directly; ad IDs routinely appear next to
# another advertiser's card in a keyword search.
# ---------------------------------------------------------------------------

ADS = {
    "Aadithya Solar Energies": [
        {
            "library_id": "1596852225147259",
            "library_url": "https://www.facebook.com/ads/library/?id=1596852225147259",
            "page_name": "Aadithya Solar Energies",
            "started": "Sep 11, 2026",
            "destination": "fb.me (http://fb.me/), confirmed on the ad card",
            "text": "Video ad, copy in Telugu script, which this report's fonts cannot render - given below by meaning. Latin-script lines are verbatim from the card; open the live ad to read the original.\n"
                    "\n"
                    "Verbatim: \"Rs.78,000 Solar Subsidy\", \"Rs.78,000 Solar!\", \"Power Plant!\", \"Rooftop Solar Installation\", \"Solar Power\", \"Savings\", \"Aadithya Solar Energies\", \"Call: 94910 32828\".\n"
                    "\n"
                    "Translated: register your details for solar subsidy information up to Rs.78,000; your own power plant on your own roof; check on electricity bills that rise every month; under the PM Surya Ghar Muft Bijli Yojana eligible households can get up to Rs.78,000 subsidy, with help through the process.\n"
                    "\n"
                    "CTA on the card: 'Book now'",
        },
    ],
    "SunX Solar and Renewable Solutions": [
        {
            "library_id": "1113916408287479",
            "library_url": "https://www.facebook.com/ads/library/?id=1113916408287479",
            "page_name": "SunX Solutions",
            "started": "Nov 6, 2026",
            "destination": "Instagram (instagram.com/sunxsolarsolutions), confirmed on the ad card",
            "text": "Video ad. Telugu copy:\n"
                    "\n"
                    "Diwali special offer pomdheyandi \u2026\u2026\u2026. "
                    "E pamduganu marintha special cheskondi\u2764\ufe0f\n"
                    "\n"
                    "Silver coin\U0001fa99\n"
                    "\n"
                    "Fridge \U0001f60d\n"
                    "\n"
                    "Washing machine \U0001f495\n"
                    "\n"
                    "Water purifier\n"
                    "\n"
                    "Smart phone \U0001f4f1\n"
                    "\n"
                    "For more details about sunx solar solutions please call "
                    "8333075151\n"
                    "\n"
                    "#diwaligifting #solarenergy #diwalispecial #offer #fyp\n"
                    "\n"
                    "CTA on the card: 'Send message'",
        },
    ],
    "The Arka Solar Power": [
        {
            "library_id": "1557646593071478",
            "library_url": "https://www.facebook.com/ads/library/?id=1557646593071478",
            "page_name": "The ARKA SOLAR POWER",
            "started": "Oct 30, 2026",
            "destination": "an fb.me link, confirmed on the ad card",
            "text": "Mixed Telugu / English copy:\n"
                    "\n"
                    "Attention home owners of Hyderabad! \u2026 switch to "
                    "Rooftop Solar with 'ARKA Solar Power' and reduce your "
                    "electricity bill by more than 90%.\n"
                    "\n"
                    "\u2705 Subsidy Benefits Available\n"
                    "\u2705 Easy EMI / Loan Options\n"
                    "\u2705 25+ Years Performance\n"
                    "\u2705 Govt. Approved Installation\n"
                    "\u2705 Free Site Inspection",
        },
    ],
}


SITE_EVIDENCE_NOTE = (
    "Landing-page source read live on {d} through the W3C Nu HTML Checker "
    "(validator.w3.org/nu/?doc=<url>&showsource=yes), which returns the served "
    "HTML with script tags intact, plus a direct fetch of the same pages. "
    "Tags found: {found}."
)

ARKA_EVIDENCE_NOTE = (
    "The landing page's <head> could not be read on {d}: the W3C Nu HTML "
    "Checker returned an IO error (java.io.EOFException) for "
    "https://arkasolarpower.com/ and its inner pages, and a direct fetch "
    "returned HTTP 500, so the title, meta description, Open Graph tags, "
    "structured data and any pixel were never returned. Those checks are "
    "reported as not checked, not as failures. Tags found: {found}."
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
    note = (ARKA_EVIDENCE_NOTE.format(
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
                "query": "solar Hyderabad / Telangana keyword search",
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
            "note": "Ad destination as shown on the live ad card.",
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
        if site.pop("score_unavailable", False):
            # Nothing on the site was measurable, so the repo's own algorithm
            # returns 0 - which a reader would take as "no problems found".
            # Claim no score instead.
            result["score"] = None
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
        shown = ("n/a" if result["score"] is None
                 else f"{result['score']}/100")
        print(f"  {company:<36} score {shown:>10}  "
              f"issues {len(result['issues']):>2}  wins {len(result['wins']):>2}  "
              f"controls {counts.get('pass', 0)}P/{counts.get('fail', 0)}F/"
              f"{counts.get('unknown', 0)}U  -> {os.path.basename(out)}")
        changed.append(out)

    print(f"\nRebuilt {len(changed)} reports.")
    return changed


if __name__ == "__main__":
    main()
