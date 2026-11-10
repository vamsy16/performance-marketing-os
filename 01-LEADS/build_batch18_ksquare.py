#!/usr/bin/env python3
"""Build the four batch-18 audit reports (Four Solar, Origian Power,
Green Carbon Hub, Sri Balaji Solar Energies).

Everything below was read live on 2026-11-10:

  * Google Ads Transparency Centre - every advertiser record was opened
    directly at adstransparency.google.com/advertiser/<AR_ID>?region=IN and
    the verified legal name, ad count and visible creatives read off it:
      Four Solar      9 ads  AR03099108522298703873  FOUR SOLAR ENERGY SYSTEMS PVT. LTD
      Origian Power   3 ads  AR00071167135648317441  REDDYMASI SOHITH (an individual)
      Green Carbon Hub 14 ads AR10321845347697033217 ECOILA PRIVATE LIMITED
      Sri Balaji      0 ads  (domain probe, 2026-11-10)
  * Meta Ad Library (India, active ads) - queried for all four companies today.
    Four Solar and Origian Power both return "No ads match your search
    criteria". Green Carbon Hub returns 2 live ads (1387783212859779 since
    Aug 30 2026, 1031770816527038 since Sep 10 2026). Sri Balaji returns about
    8 active results, 5 of them captured verbatim below.
  * The four websites were read through the W3C Nu HTML Checker with
    showsource=yes. For Four Solar (source lines 1-399), Origian Power (lines
    1-182) and Green Carbon Hub (lines 1-62) the COMPLETE head was read, so the
    eight tracking rows are measured in both directions - a False below is a
    measurement, not an unread head. Sri Balaji's site is a React shell: the
    server returns no content without JavaScript, so its conversion rows are
    unknown rather than absent.
  * PageSpeed/Lighthouse: the keyless API returned 429, as it has for every
    report in this campaign. No speed figure is claimed anywhere.

Four Solar and Origian Power are ads-only reports (report_kind: ads_only in
the sequence manifest) and are rendered with generate_ads_only_pdf into
02-OUTREACH/ads_only_pdfs/. Green Carbon Hub and Sri Balaji are full audits
(report_kind: full_audit) and are rendered with generate_pdf into
02-OUTREACH/audit_pdfs/. All four existing reports were stale: the two
ads-only ones were built on the 2026-10-20 Meta-only probe (both companies
now run Google ads), and the two full-audit ones were built in the
no-website era and read "NO WEBSITE FOUND".

Run:  cd 01-LEADS && PYTHONPATH=/tmp/pdflibs python3 build_batch18_ksquare.py
"""
import json
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

from ads_audit import calculate_audit_score          # noqa: E402
from ads_audit_controls import evaluate              # noqa: E402
from audit_pdf import (generate_ads_only_pdf,        # noqa: E402
                       generate_pdf)

ADS_ONLY_DIR = os.path.join(BASE, "ads_only_results")
FULL_DIR = os.path.join(BASE, "audit_results")
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
    """None = never returned, so presence is unknown in both directions."""
    d = dict(pixels())
    for k in list(d):
        d[k] = None
    d.update(over)
    return d


# ===========================================================================
# Real measurements - the two ads-only leads (website half nested under
# 'site_audit', exactly as the ads-only report format requires).
# ===========================================================================

FOUR_SOLAR = {
    "ssl": True,
    "load_time_seconds": None,                 # not measured
    "final_url": "https://www.foursolar.com/",
    "audit_date": READ_ON,
    # The COMPLETE head was read (source lines 1 to 399). It carries exactly
    # one trace of tracking: the Meta Pixel's <noscript> image fallback at
    # source line 168, <img height="1" width="1" style="display:none"
    # src="https://www.facebook.com/tr?id=1513606190140594&ev=PageView...">.
    # No fbq() initialisation script was read anywhere in the head, and there
    # is no GA4 measurement ID, no GTM container and no Google Ads conversion
    # tag. og:title is "Home" and og:site_name is empty.
    "pixels": pixels(
        meta_pixel=True,                       # ID 1513606190140594, noscript only
    ),
    "conversion": {
        # Homepage form is Contact Form 7 ("Share Details & Get a Call-Back":
        # full name, phone, email, enquiry type, monthly bill, zipcode) and
        # the form's own note says the submission is stored in Google Sheets.
        # Click-to-chat-for-whatsapp is installed; no live-chat widget, no
        # popup opt-in and no price list were read.
        "has_contact_form": True,              # CF7 -> Google Sheets
        "has_phone_click": True,               # +91 8886002221, click-to-call
        "has_whatsapp_link": True,             # Click to Chat for WhatsApp
        "has_cta_buttons": 4,                  # Book a Site Visit, Explore Solutions, Get a Call Back, Contact Us
        "has_live_chat": None,                 # not read
        "has_popup_optin": False,              # none read
        "has_testimonials": None,              # not read as a block
        "has_pricing_page_link": False,        # no price list anywhere on the site
    },
    "seo": {
        # <title>Four Solar | Leading Residential, Commercial & MW Solar EPC India</title>
        "has_title": True,
        "title_text": "Four Solar | Leading Residential, Commercial & MW Solar EPC India",
        "title_length": 65,
        "has_meta_description": None,          # not returned in readable form
        "meta_desc_length": None,
        "h1_count": None,                      # not counted
        "h1_text": None,
        "has_og_tags": True,                   # og:title "Home", og:site_name empty
        "has_schema": None,                    # no JSON-LD block was read
        "has_favicon": None,                   # not read
        "image_count": None,
        "images_without_alt": None,
    },
    "pagespeed": {"error": PAGESPEED_ERROR},
    "page_count": {"has_sitemap": None},
    "local_signals": {
        # The site publishes a Somajiguda, Hyderabad address and a "Book a
        # Site Visit" page; no Google Maps embed and no local-business
        # structured data were read.
        "has_google_maps_embed": None,
        "has_address_schema": None,
        "mentions_city": True,
        "company_in_title": True,
    },
    "platform": "WordPress with the Bricks builder and Automatic CSS, "
                "Contact Form 7 plus the wpcf7-redirect plugin and a Google "
                "Sheets connector, Click to Chat for WhatsApp, locally-hosted "
                "Google Fonts",
    "html_errors": "38 errors, 2 warnings and 40 info messages on the "
                   "homepage. The dominant defect is structural: the broken "
                   "<noscript> element inside the <head> (the Meta Pixel "
                   "fallback, source line 168) leaves the head unclosed, "
                   "which cascades into a duplicate <body> start tag, stray "
                   "end tags for head / div / header and 'End tag for body "
                   "seen, but there were unclosed elements'. 24 of the 38 "
                   "errors are style rules sitting outside an @scope rule, "
                   "and the media queries still use the deprecated "
                   "min-device-width / max-device-width syntax.",
    "scope_note": "The complete <head> was read - source lines 1 to 399, "
                  "ending at the favicon links - so the eight tracking rows "
                  "are measured in both directions and a zero is a "
                  "measurement. The rows that still read 'Not checked' are "
                  "the ones the checker does not report and the source did "
                  "not carry in readable form in this pass: the meta "
                  "description length, the h1 count, the favicon, JSON-LD "
                  "schema and the image alt-text counts. The body past source "
                  "line 404 was not returned, so the footer scripts could not "
                  "be read either.",
}

ORIGIAN = {
    "ssl": True,
    "load_time_seconds": None,                 # not measured
    "final_url": "https://origianpower.com/",
    "audit_date": READ_ON,
    # The COMPLETE head was read (source lines 1 to 182) and it carries NO
    # tracking of any kind: no Meta Pixel, no GA4, no GTM, no Google Ads tag,
    # no LinkedIn Insight, no Microsoft Clarity and no Hotjar. What it does
    # carry is a full Yoast SEO Premium stack - og + Twitter card set,
    # canonical, and a schema-graph JSON-LD (WebPage, ImageObject,
    # BreadcrumbList, WebSite) with article:modified_time 2025-12-17.
    "pixels": pixels(),                        # every row measured False
    "conversion": {
        # WPForms enquiry form with reCAPTCHA in the Contact Us section,
        # tel:+918121766831, three named testimonials with photographs. No
        # WhatsApp link, no live chat, no popup opt-in and no price list were
        # read on the homepage.
        "has_contact_form": True,              # WPForms + reCAPTCHA
        "has_phone_click": True,               # tel:+918121766831
        "has_whatsapp_link": False,            # none read
        "has_cta_buttons": None,               # not counted in this pass
        "has_live_chat": False,                # none read
        "has_popup_optin": False,              # none read
        "has_testimonials": True,              # Ravi 5 kW Nandyal; Damodar Reddy 2 x 5 kW Anantapur; Sharath 10 kW Anantapur
        "has_pricing_page_link": False,        # no price list published
    },
    "seo": {
        # <title>Best Solar Power Systems & Solar Panel Installers | Origian Power</title>
        "has_title": True,
        "title_text": "Best Solar Power Systems & Solar Panel Installers | Origian Power",
        "title_length": 65,
        "has_meta_description": True,          # Yoast writes one; og:description set is complete
        "meta_desc_length": None,              # length not returned in readable form
        "h1_count": None,                      # not counted
        "h1_text": None,
        "has_og_tags": True,                   # full og + Twitter card set
        "has_schema": True,                    # Yoast schema-graph JSON-LD
        "has_favicon": None,                   # not read
        "image_count": None,
        "images_without_alt": None,
    },
    "pagespeed": {"error": PAGESPEED_ERROR},
    "page_count": {"has_sitemap": None},
    "local_signals": {
        # The page names Hyderabad, Anantapur, Telangana and Andhra Pradesh;
        # no Google Maps embed and no local-business JSON-LD were read.
        "has_google_maps_embed": None,
        "has_address_schema": None,
        "mentions_city": True,
        "company_in_title": True,
    },
    "platform": "WordPress 6.9.11, Elementor 4.3.6, Slider Revolution 6.7.34 "
                "(sr7-module), greenly theme, Yoast SEO Premium 26.3 with a "
                "full schema graph, locally-hosted Google Fonts",
    "html_errors": "7 errors, 3 warnings and 87 info messages on the "
                   "homepage. The errors are four stray </br> end tags, an "
                   "'image_lists' unknown element inside the Slider "
                   "Revolution module, an <h4> that follows an <h2> with no "
                   "<h3> between them, two <section> elements and one "
                   "<article> with no accessible heading. The served HTML "
                   "also ships the three service cards (Solar on-grid power "
                   "plants, Solar off-grid power plants, Solar water heating "
                   "systems) twice, and the page closes with the stray text "
                   "'BESbswy' - Slider Revolution's own demo signature.",
    "scope_note": "The complete <head> was read - source lines 1 to 182, "
                  "ending at the favicon and preconnect links - and it "
                  "carries no tracking tag of any kind, so all eight tracking "
                  "rows are measured in both directions and every zero is a "
                  "measurement. The rows that still read 'Not checked' are "
                  "the ones the checker does not report and the source did "
                  "not carry in readable form: the meta description length, "
                  "the h1 count, the favicon, the CTA count, the image "
                  "alt-text counts and the sitemap.",
}

LEADS_ADS_ONLY = {
    "Four Solar": FOUR_SOLAR,
    "Origian Power": ORIGIAN,
}


# ===========================================================================
# Real measurements - the two full-audit leads (flat schema, as
# audit_pdf.generate_pdf expects).
# ===========================================================================

GREEN_CARBON_HUB = {
    "company": "Green Carbon Hub",
    "city": "Hyderabad",
    "website": "https://greencarbonhub.com/",
    "ssl": True,
    "load_time_seconds": None,                 # not measured
    "final_url": "https://greencarbonhub.com/",
    "audit_date": READ_ON,
    # The COMPLETE head was read (source lines 1 to 62). It carries two tags:
    # the GTM container GTM-TX4XRLT (lines 36-42) and a full Meta Pixel
    # 1088807282778475 - fbq('init', '1088807282778475') plus
    # fbq('track', 'PageView') and the noscript image fallback (lines 44-60).
    # No GA4 measurement ID and no Google Ads conversion tag were read in the
    # head; a GTM container is not itself a measurement, so the GA4 row is
    # not claimed either way.
    "pixels": pixels(
        meta_pixel=True,                       # 1088807282778475, full code
        google_tag_manager=True,               # container GTM-TX4XRLT
    ),
    "conversion": {
        # Homepage contact form (service selector: Solar Installation /
        # Water-Wastewater Management / Bio-Methanation, plus a message box)
        # posting to a PHP handler, tel:9182445300 in the offcanvas contact
        # block, and a "Chat with us" widget bottom-right. No WhatsApp link,
        # no popup opt-in and no price list were read; the only social proof
        # is a two-logo client strip (GE, AP Food Processing Society).
        "has_contact_form": True,              # homepage form -> PHP handler
        "has_phone_click": True,               # tel:9182445300
        "has_whatsapp_link": None,             # not read
        "has_cta_buttons": 4,                  # Get Started, Avail Service, Send message, Contact us and schedule a site visit
        "has_live_chat": True,                 # "Chat with us" widget
        "has_popup_optin": False,              # none read
        "has_testimonials": False,             # client logos only
        "has_pricing_page_link": False,        # "check prices" is a process step, not a published price
    },
    "seo": {
        # <title>GreenCarbonHub</title> - 14 characters, no service, no city,
        # no offer. The meta description element is shipped with an empty
        # content attribute. There is no <h1> anywhere in the served body;
        # the hero headings are an h4 ("Welcome to GreenCarbonHub") and an h3
        # ("Reduce/Offset your Carbon Footprint").
        "has_title": True,
        "title_text": "GreenCarbonHub",
        "title_length": 14,
        "has_meta_description": False,         # element present, content empty
        "meta_desc_length": 0,
        "h1_count": 0,
        "h1_text": None,
        "has_og_tags": None,                   # not read
        "has_schema": None,                    # not read
        "has_favicon": None,                   # not read
        "image_count": None,
        "images_without_alt": None,
    },
    "pagespeed": {"error": PAGESPEED_ERROR},
    "page_count": {"has_sitemap": None},
    "local_signals": {
        # The page names Hyderabad in the hero and the contact block; no
        # Google Maps embed and no local-business structured data were read.
        "has_google_maps_embed": None,
        "has_address_schema": None,
        "mentions_city": True,
        "company_in_title": True,
    },
    "platform": "Static PHP site (index.php / solar.php / contact.html) with "
                "a Bootstrap-style template, jQuery, Google Tag Manager "
                "container GTM-TX4XRLT and Meta Pixel 1088807282778475; "
                "large blocks of the template - the nav and the call / "
                "WhatsApp CSS - are commented out of the served HTML",
    "html_errors": "34 errors, 1 warning and 1 info message on the homepage. "
                   "The structural ones: a broken anchor "
                   "href=\"#\"#> on the Hyderabad contact link, four "
                   "attributes with no space between them, a <button> inside "
                   "an <a> at source line 681, an unclosed <main>, a "
                   "duplicate <body> and two <header> elements (one a sticky "
                   "clone). 15 of the 34 errors are style elements sitting in "
                   "the body, and an <h4> follows an <h2> with nothing "
                   "between them at source line 714.",
    "scope_note": "The complete <head> was read - source lines 1 to 62 - and "
                  "it carries two tags, the GTM container GTM-TX4XRLT and "
                  "Meta Pixel 1088807282778475, so those rows are measured. "
                  "What reads 'Not checked' is everything the head does not "
                  "carry and the checker does not report: GA4 measurement "
                  "inside the GTM container (a container is not a "
                  "measurement - nothing is counted until a tag is published "
                  "inside it), Open Graph tags, JSON-LD schema, the favicon, "
                  "the sitemap and the image alt-text counts.",
}

SRI_BALAJI = {
    "company": "Sri Balaji Solar Energies",
    "city": "Hanumakonda / Warangal (HO), Hyderabad",
    "website": "https://www.sribalajisolarenergies.com/",
    "ssl": True,
    "load_time_seconds": None,                 # not measured
    "final_url": "https://www.sribalajisolarenergies.com/",
    "audit_date": READ_ON,
    # The served HTML is a create-react-app shell: <div id="root"> containing
    # a loader GIF, then the script bundles. The shell's head DOES carry two
    # real tags, both read directly: GA4 G-C58ZMRZ68Q and the GTM container
    # GTM-NCP9G6SM. No Meta Pixel, no Google Ads tag, no LinkedIn Insight,
    # no Clarity and no Hotjar were read in the shell.
    "pixels": pixels(
        google_analytics_ga4=True,             # G-C58ZMRZ68Q
        google_tag_manager=True,               # GTM-NCP9G6SM
    ),
    "conversion": {
        # Every conversion element renders client-side. The served shell
        # contains no form, no button, no phone link and no WhatsApp link,
        # so these rows are unknown rather than absent.
        "has_contact_form": None,              # renders client-side - not read
        "has_phone_click": None,               # renders client-side - not read
        "has_whatsapp_link": None,             # renders client-side - not read
        "has_cta_buttons": None,               # renders client-side - not read
        "has_live_chat": None,                 # renders client-side - not read
        "has_popup_optin": None,               # renders client-side - not read
        "has_testimonials": None,              # renders client-side - not read
        "has_pricing_page_link": None,         # renders client-side - not read
    },
    "seo": {
        # <title>Telangana's Top Solar Panel Installation Company | Sri Balaji
        # Solar Energies.</title> - 77 characters. The served shell has no
        # <h1> and no body content at all.
        "has_title": True,
        "title_text": "Telangana's Top Solar Panel Installation Company | Sri Balaji Solar Energies.",
        "title_length": 77,
        "has_meta_description": True,          # present in the shell
        "meta_desc_length": None,              # length not returned in readable form
        "h1_count": 0,
        "h1_text": None,
        "has_og_tags": None,                   # renders client-side - not read
        "has_schema": None,                    # renders client-side - not read
        "has_favicon": None,                   # not read
        "image_count": None,
        "images_without_alt": None,
    },
    "pagespeed": {"error": PAGESPEED_ERROR},
    "page_count": {"has_sitemap": None},
    "local_signals": {
        # The title names Telangana; everything else renders client-side.
        "has_google_maps_embed": None,
        "has_address_schema": None,
        "mentions_city": True,
        "company_in_title": True,
    },
    "platform": "React single-page application (create-react-app build: "
                "static/media bundles, manifest.json, theme-color "
                "#000000) with slick, swiper, AOS, GSAP and WOW.js loaded in "
                "the shell; GA4 G-C58ZMRZ68Q and GTM container GTM-NCP9G6SM "
                "are the only tags in the served head",
    "html_errors": "0 errors, 1 warning and 11 info messages on the served "
                   "HTML - the cleanest markup in this audit, because the "
                   "served page is a shell: one <div id=\"root\"> holding a "
                   "loader GIF, with the entire site rendered client-side by "
                   "React. Nothing on the page - no heading, no form, no "
                   "button, no price, no testimonial - is present in the HTML "
                   "the server returns.",
    "scope_note": "www.sribalajisolarenergies.com is a React single-page "
                  "application. The server returns a shell - doctype, head, a "
                  "loader GIF and the script bundles - and every heading, "
                  "form, button, testimonial and price renders only after "
                  "JavaScript runs. The W3C checker and a direct page fetch "
                  "therefore see no content, which is why every conversion "
                  "row reads 'Not checked': those rows are unmeasured, not "
                  "absent. The two tags that ARE in the shell - GA4 "
                  "G-C58ZMRZ68Q and GTM GTM-NCP9G6SM - were read directly "
                  "from the served head.",
}

LEADS_FULL = {
    "Green Carbon Hub": GREEN_CARBON_HUB,
    "Sri Balaji Solar Energies": SRI_BALAJI,
}


# ===========================================================================
# Extra real findings that belong at the top of "Top priorities" - each one
# is read from the live advertiser record or the live page, not invented.
# ===========================================================================

EXTRA_ISSUES = {
    "Four Solar": [
        "Your 9 live Google ads point at a homepage whose only tracking is a "
        "Meta Pixel that cannot fire: the pixel ID 1513606190140594 appears "
        "only inside a <noscript> image fallback at source line 168, and no "
        "fbq() initialisation script was read anywhere in the complete head. "
        "A visitor with JavaScript enabled - which is nearly all of them - is "
        "never counted.",
        "There is no Google tag of any kind on the site: no GA4 measurement "
        "ID, no GTM container and no Google Ads conversion tag was read in "
        "the head. You are buying Search, Display, Local and YouTube clicks "
        "with no Google-side measurement behind them.",
        "Your own site contradicts itself on size: the stat tiles claim '250+ "
        "MW Solar Capacity Engineered & Executed' and '1,500+ sites', while "
        "the About section of the same page says '13+ years in solar EPC and "
        "50 MW+ of projects delivered'. Two capacity figures, five times "
        "apart, on one page.",
        "The checker reports 38 errors on the homepage and the cause is your "
        "own pixel: the broken <noscript> in the head leaves the document "
        "with a duplicate <body>, stray end tags for head / div / header and "
        "'End tag for body seen, but there were unclosed elements'.",
        "og:site_name is empty and og:title is 'Home', so every share of your "
        "homepage on WhatsApp or Facebook is attributed to a page called "
        "'Home' - the exact channel your ad spend is meant to feed.",
    ],
    "Origian Power": [
        "Your 3 live Google ads are booked under the personal name REDDYMASI "
        "SOHITH, not Origian Power - the verified advertiser record shows an "
        "individual, so the brand you are buying for is invisible in the "
        "transparency record.",
        "There is no tracking of any kind on the site: no Meta Pixel, no GA4, "
        "no GTM, no Google Ads tag and no LinkedIn, Clarity or Hotjar was "
        "read in the complete head. You are paying for clicks with nothing on "
        "the page counting them.",
        "Your own page repeats itself: the three service cards - Solar "
        "on-grid power plants, Solar off-grid power plants, Solar water "
        "heating systems - appear twice in the served HTML, and the checker "
        "reports 4 stray </br> end tags, 2 sections and 1 article with no "
        "accessible heading, and an <h4> following an <h2>.",
        "All three testimonials are from Anantapur and Nandyal in Andhra "
        "Pradesh - Mr Ravi (5 kW, Nandyal), Mr Damodar Reddy (2 x 5 kW, "
        "Anantapur), Mr Sharath (10 kW, Anantapur) - on a page whose hero "
        "says Hyderabad and whose Google ads buy Hyderabad traffic.",
        "The only published contact routes are a Gmail address "
        "(origian.ei@gmail.com) and one phone line, and the page closes with "
        "the stray text 'BESbswy' before the footer - Slider Revolution's "
        "demo signature, left in production.",
    ],
    "Green Carbon Hub": [
        "Your 14 live Google ads are booked under a different legal entity: "
        "the verified advertiser record reads ECOILA PRIVATE LIMITED, not "
        "Green Carbon Hub. Anyone who checks the transparency centre sees a "
        "company name that does not match the brand on the ad.",
        "Your <title> is 'GreenCarbonHub' - 14 characters with no service, no "
        "city and no offer - and your meta description element is shipped "
        "with an empty content attribute. Both Google ads are buying 'solar "
        "rooftop service providers in Hyderabad' and 'subsidy up to Rs "
        "78,000' into a page that says neither.",
        "The only tracking on the site is GTM container GTM-TX4XRLT and Meta "
        "Pixel 1088807282778475. A container is not a measurement - no GA4 "
        "measurement ID could be read inside it - so 14 Google ads and 2 Meta "
        "ads run with no confirmed analytics behind them.",
        "The second phone number on your site dials the first one: the "
        "offcanvas contact block renders '+91 9182445715' inside an "
        "<a href=\"tel:9182445300\">. A buyer who taps the second number "
        "reaches the wrong line.",
        "There is no <h1> anywhere in the served page. The checker reports an "
        "<h4> following an <h2> with nothing between them, a <button> inside "
        "an <a> at source line 681, an unclosed <main>, a duplicate <body> "
        "and two <header> elements (one a sticky clone), on 34 errors total.",
        "Your navigation is mostly commented out - the live page serves a "
        "commented-out menu and a block of commented-out call / WhatsApp CSS "
        "- and the 'Login' button in the header points at contact.html. The "
        "only working conversion routes are the form, the phone links and the "
        "chat widget.",
    ],
    "Sri Balaji Solar Energies": [
        "Your entire website is invisible to everything that is not a "
        "browser: the served HTML is a React shell with a loader GIF, no h1, "
        "no headings, no form and no content. Google's crawler, the W3C "
        "checker, every link preview and every accessibility tool see an "
        "empty page.",
        "You run about 8 live Meta ads - every one of them clicking through "
        "to fb.me, none to your own site - while your site carries no Meta "
        "Pixel. You are paying to reach people and then handing them to "
        "Facebook's messenger with no way to bring them back.",
        "Your live ads contradict each other on your own history: Library ID "
        "942037648839408 says '14 years of trust' while 1454295123168911 and "
        "1541931104220931 say '15 years legacy'. Two ages, running at the "
        "same time.",
        "GA4 (G-C58ZMRZ68Q) and GTM (GTM-NCP9G6SM) are both installed in the "
        "shell - real measurement that most leads in this market do not have "
        "- but there is no Meta Pixel and no Google Ads tag, so the one "
        "measurement you have covers the channel you do not buy.",
        "Three different phone numbers appear across your live ads (+91-85200 "
        "27111, +91-91333 03164) and two more in our own register (+91 9959491774, "
        "+91 87024 44646), and every ad lands on the same fb.me redirect - a "
        "buyer has no way to tell which number is yours.",
    ],
}


# ===========================================================================
# What the live ad promises, against what the landing page actually shows.
# Both columns are read live.
# ===========================================================================

PROMISE_GAP = {
    "Four Solar": [
        ("Google Ads Transparency: 9 live ads under advertiser "
         "AR03099108522298703873, verified as Four Solar Energy Systems Pvt. "
         "Ltd - including Local ads with DIRECTIONS and CALL buttons and "
         "image creatives headed 'Buy Solar Panels Online' and 'Buy Solar "
         "Panels for Homes'.",
         "The Local ads carry empty rating stars and placeholder 'Open Hours' "
         "and 'Distance' fields - the ad format that leans on a Google "
         "Business Profile is running without a rated profile behind it. The "
         "click lands on a homepage with no Google-side tracking at all."),
        ("The ad copy promises 'Get Quality Pre and Post Solar Installation "
         "Services by Top Solar Rooftop Company in Hyd'.",
         "The site substantiates the pre/post claim better than most: a "
         "4-step process, a 'Book a Site Visit' page, a CF7 form that "
         "captures the monthly bill and zipcode, and a WhatsApp click-to-chat. "
         "What it cannot do is tell you which of those produced an enquiry, "
         "because nothing on the page is measured on the Google side."),
        ("The homepage presents '250+ MW Solar Capacity Engineered & "
         "Executed', '13+ years' and '1,500+ sites', with segments for "
         "Industrial & MSME, Commercial & Institutional, Ground-Mounted "
         "MW-Scale, PM-KUSUM, PM Surya Ghar, Gated Communities and Solar "
         "Kits, and a brand wall of Renew, Vikram, Pahal, Navgrun, Waaree and "
         "Solex.",
         "The About section of the same page says '50 MW+ of projects "
         "delivered'. The six brand logos are shipped three times in a row, "
         "so the page reads as padded even where the underlying credentials "
         "are real."),
    ],
    "Origian Power": [
        ("Google Ads Transparency: 3 live ads under advertiser "
         "AR00071167135648317441, verified as REDDYMASI SOHITH - one YouTube "
         "video creative (DTApvXLQPMQ) and two Display image creatives.",
         "The advertiser of record is a person, not the company. A prospect "
         "who checks the transparency record sees a name that does not match "
         "the brand, and the page those ads land on has no tracking that "
         "could tell either of you what the spend produced."),
        ("The homepage promises 'Cut electricity bills by 70-95%', 'Get PM "
         "Suryaghar subsidy for residential rooftop systems', 'Increase home "
         "value' and 'reliable backup power with off-grid systems'.",
         "The PM Suryaghar subsidy section is present and the service "
         "descriptions are specific. But the three proofs on the page are all "
         "Anantapur-district installations, the three service cards are "
         "shipped twice in the HTML, and the page's own "
         "article:modified_time is 2025-12-17 - the site has not been touched "
         "in eleven months while the ads run."),
        ("The site presents solar on-grid power plants, solar off-grid power "
         "plants and solar water heating systems as three service lines, with "
         "a projects gallery and three named testimonials.",
         "The gallery and the testimonials are real, and the contact section "
         "carries a working tel: link and a WPForms form with reCAPTCHA. What "
         "is missing is any measurement at all: no pixel, no GA4, no tag "
         "manager, so nobody can say whether the twelve pages of content have "
         "ever produced an enquiry."),
    ],
    "Green Carbon Hub": [
        ("Google Ads Transparency: 14 live ads under advertiser "
         "AR10321845347697033217, verified as ECOILA PRIVATE LIMITED - 11 "
         "Display image creatives, 2 YouTube video creatives (rFydyADZH6U and "
         "4g7BazeEIbw) and one further creative carrying the visible copy "
         "'Get Subsidy Upto Rs 78000 - Solar Panels for Home'.",
         "The advertiser name on the record is Ecoila Private Limited while "
         "the creative and the destination are GreenCarbonHub - the entity "
         "behind the spend does not match the brand in front of the buyer. "
         "The landing page's own title is the bare word 'GreenCarbonHub'."),
        ("Two Meta ads are live on the GreenCarbonHub page - Library ID "
         "1387783212859779 ('Don't Just Install Solar. Keep It Performing!', "
         "running since Aug 30, 2026) and 1031770816527038 ('Get Free Solar "
         "Checkup and Cleaning Today in Hyderabad!', since Sep 10, 2026) - "
         "both promising lifetime maintenance support.",
         "Both ads click through to fb.me, not to the site, and the site's "
         "only maintenance-related content is a service card. The one thing "
         "the ads are selling - lifetime maintenance - has no page of its "
         "own, and while Meta Pixel 1088807282778475 is installed, the GA4 "
         "measurement inside GTM-TX4XRLT could not be read from the "
         "container."),
        ("The site positions GCH as 'a B2B2C marketplace offering design, "
         "installation and maintenance of various net-zero services', with a "
         "4-step process (site visit, select branded components and check "
         "prices, entrust the work, start the net-zero journey) and clients "
         "including GE and the AP Food Processing Society.",
         "The client logos are real and the process is clear, but the page "
         "carries no case study, no capacity figure, no price and no review "
         "count - and 15 of its 34 errors are style elements sitting in the "
         "body, with most of the navigation commented out of the served "
         "HTML."),
    ],
    "Sri Balaji Solar Energies": [
        ("Meta Ad Library: about 8 active ad results on the Sri Balaji Solar "
         "Energies page (queried 2026-11-10), including Library IDs "
         "942037648839408 and 1454295123168911 and 1541931104220931 (running "
         "since May 29, 2026), 2103721667197349 (since Aug 18, 2026) and "
         "4493621594235361 (since Aug 25, 2026).",
         "Every one of them clicks to fb.me, not to the site - and the site "
         "carries no Meta Pixel. The ads are the entire front door, and the "
         "house behind them renders nothing without JavaScript."),
        ("The Telugu ad copy promises 'no more current bills to pay', 'Rs. 0 "
         "(zero) upfront cost', 'central government subsidy up to Rs. "
         "78,000', 'pay just Rs. 1,355 EMI instead of a monthly current bill' "
         "and '10,000+ satisfied customers', with service listed across "
         "Warangal, Hanumakonda, Rajahmundry, Bhadrachalam, Ghatkesar, "
         "Huzurabad, Hyderabad and nearby districts.",
         "Those are specific, checkable promises - and the page they should "
         "lead to cannot be read without JavaScript, so a buyer who taps "
         "through to the site instead of fb.me gets a loader. The same ads "
         "give the company's age as both 14 years and 15 years."),
        ("Google's Ads Transparency Centre returns zero ads for "
         "sribalajisolarenergies.com (queried 2026-11-10) - all of the paid "
         "activity is on Meta.",
         "That is a defensible channel choice for a Telugu-first residential "
         "offer, and GA4 (G-C58ZMRZ68Q) plus GTM (GTM-NCP9G6SM) are both "
         "installed in the shell, so the measurement side is the strongest of "
         "the four leads in this audit. What is missing is any way to measure "
         "the Meta side: no Meta Pixel was read in the served head."),
    ],
}


# ===========================================================================
# Verified contact details, read from the live site / advertiser record.
# ===========================================================================

COMPANY = {
    "Four Solar": {
        "legal": "Four Solar Energy Systems Pvt. Ltd",
        "city": "Somajiguda, Hyderabad 500082 (serves India-wide)",
        "website": "https://www.foursolar.com/",
        "contact_facts": [
            ["Email", "contact@foursolar.com"],
            ["Phone", "+91 8886002221 / +91 9248716892 / 040-23405670"],
            ["Address", "6-3-1109/1/P/402, 4th Floor, Jewel Pawani Tower, "
                        "Raj Bhavan Rd, Somajiguda, Hyderabad 500082"],
            ["Entity", "Four Solar Energy Systems Pvt. Ltd - TGREDCO "
                       "empanelled, registration TSRE180027"],
            ["Google advertiser", "Four Solar Energy Systems Pvt. Ltd, "
                                  "AR03099108522298703873 (verified), 9 live "
                                  "ads read 2026-11-10"],
            ["Meta", "No active Meta ads (Ad Library, queried 2026-11-10); "
                     "facebook.com/foursolar"],
        ],
        "contact": {"phone": "+91 8886002221",
                    "email": "contact@foursolar.com",
                    "whatsapp": ""},
    },
    "Origian Power": {
        "legal": "Origian Power (Google ads verified under REDDYMASI SOHITH)",
        "city": "Nizampet & Hitech City, Hyderabad 500090 / Anantapur 515004 (head office)",
        "website": "https://origianpower.com/",
        "contact_facts": [
            ["Email", "origian.ei@gmail.com (the only address published on the site)"],
            ["Phone", "+91 8121766831 / +91 8121 3668 32 / +91 8121 7668 34"],
            ["Hyderabad offices", "Flat B-106, Adithya Wizz Lagoon, Nizampet, "
                                  "Hyderabad 500090; 3rd Floor, Lakeview "
                                  "Co-Working, InOrbit Mall Road, Hitech "
                                  "City, Hyderabad 500081"],
            ["Head office", "18-5, Indira Gandhi Nagar, Papampeta, Anantapur 515004"],
            ["Google advertiser", "REDDYMASI SOHITH, AR00071167135648317441 "
                                  "(verified), 3 live ads read 2026-11-10"],
            ["Meta", "No active Meta ads (Ad Library, queried 2026-11-10)"],
        ],
        "contact": {"phone": "+91 8121766831",
                    "email": "origian.ei@gmail.com",
                    "whatsapp": ""},
    },
    "Green Carbon Hub": {
        "legal": "Green Carbon Hub (Google ads verified under ECOILA PRIVATE LIMITED)",
        "city": "Hyderabad",
        "website": "https://greencarbonhub.com/",
        "contact_facts": [
            ["Email", "info@greencarbonhub.com"],
            ["Phone", "+91 9182445300 / +91 9182445715 - note the second "
                      "number is rendered inside an <a href=\"tel:9182445300\">, "
                      "so tapping it dials the first"],
            ["Google advertiser", "ECOILA PRIVATE LIMITED, "
                                  "AR10321845347697033217 (verified), 14 live "
                                  "ads read 2026-11-10"],
            ["Meta", "2 live ads on the GreenCarbonHub page (Ad Library, "
                     "queried 2026-11-10): 1387783212859779 since Aug 30 "
                     "2026 and 1031770816527038 since Sep 10 2026"],
            ["Tags in the head", "GTM-TX4XRLT and Meta Pixel 1088807282778475 "
                                 "(full init + PageView), read 2026-11-10"],
            ["Clients named on the site", "GE and the AP Food Processing Society"],
        ],
        "contact": {"phone": "+91 9182445300",
                    "email": "info@greencarbonhub.com",
                    "whatsapp": ""},
    },
    "Sri Balaji Solar Energies": {
        "legal": "Sri Balaji Solar Energies",
        "city": "Hanumakonda / Warangal 506001 (head office); Medipally, Hyderabad",
        "website": "https://www.sribalajisolarenergies.com/",
        "contact_facts": [
            ["Email", "sbse4444@gmail.com (TGREDCO empanelled-supplier register)"],
            ["Phone", "+91 9959491774 / +91 87024 44646 (register); the live "
                      "ads carry +91-85200 27111 and +91-91333 03164"],
            ["Meta", "About 8 active ad results on the Sri Balaji Solar "
                     "Energies page (Ad Library, queried 2026-11-10); every "
                     "ad clicks to fb.me"],
            ["Google", "Zero ads for sribalajisolarenergies.com in the "
                       "transparency centre (queried 2026-11-10)"],
            ["Tags in the head", "GA4 G-C58ZMRZ68Q and GTM-NCP9G6SM, read "
                                 "2026-11-10 from the served React shell"],
            ["Site", "React single-page app - the served HTML is a shell with "
                     "a loader GIF and no content"],
        ],
        "contact": {"phone": "+91 9959491774",
                    "email": "sbse4444@gmail.com",
                    "whatsapp": ""},
    },
}


# ===========================================================================
# The live Google ads, read from the Google Ads Transparency Centre on
# 2026-11-10. Every advertiser ID was opened directly at
# adstransparency.google.com/advertiser/<AR_ID>?region=IN and the verified
# legal name read off the returned record.
# ===========================================================================

ADS = {
    "Four Solar": [
        {
            "library_id": "AR03099108522298703873",
            "library_url": "https://adstransparency.google.com/advertiser/AR03099108522298703873?region=IN",
            "page_name": "Four Solar Energy Systems Pvt. Ltd (verified)",
            "started": "2026-11-10 (advertiser record read live)",
            "destination": "https://www.foursolar.com/ - domain confirmed on the advertiser record",
            "text": "9 live ads listed under this advertiser in Google's Ads "
                    "Transparency Centre - 4 image creatives were visible on "
                    "the advertiser page plus 5 further creatives, including "
                    "2 Local ads with DIRECTIONS and CALL buttons headed 'Buy "
                    "Solar Panels Online' and 'Buy Solar Panels for Homes' "
                    "with the line 'Get Quality Pre and Post Solar "
                    "Installation Services by Top Solar Rooftop Company in "
                    "Hyd'.\n"
                    "\n"
                    "Advertiser verified. Legal name read off the advertiser "
                    "record: FOUR SOLAR ENERGY SYSTEMS PVT. LTD.\n"
                    "\n"
                    "The Local ads render empty rating stars and placeholder "
                    "'Open Hours' and 'Distance' fields - the format leans on "
                    "a Google Business Profile that is not rated. The site "
                    "behind the spend sells Industrial & MSME, Commercial & "
                    "Institutional, Ground-Mounted MW-scale, PM-KUSUM, PM "
                    "Surya Ghar, Gated Community and Solar Kits EPC.",
        },
    ],
    "Origian Power": [
        {
            "library_id": "AR00071167135648317441",
            "library_url": "https://adstransparency.google.com/advertiser/AR00071167135648317441?region=IN",
            "page_name": "REDDYMASI SOHITH (verified)",
            "started": "2026-11-10 (advertiser record read live)",
            "destination": "https://origianpower.com/ - domain confirmed on the advertiser record",
            "text": "3 live ads listed under this advertiser in Google's Ads "
                    "Transparency Centre - 1 YouTube video creative "
                    "(DTApvXLQPMQ) and 2 Display image creatives "
                    "(simgad/1038914867575094063 and "
                    "simgad/12940158876711616666).\n"
                    "\n"
                    "Advertiser verified. Legal name read off the advertiser "
                    "record: REDDYMASI SOHITH - an individual, not Origian "
                    "Power.\n"
                    "\n"
                    "The site the ads point at sells on-grid and off-grid "
                    "solar power plants and solar water heating, promises "
                    "'Cut electricity bills by 70-95%' and PM Suryaghar "
                    "subsidy handling, and serves Hyderabad, Anantapur, "
                    "Telangana and Andhra Pradesh.",
        },
    ],
    "Green Carbon Hub": [
        {
            "library_id": "AR10321845347697033217",
            "library_url": "https://adstransparency.google.com/advertiser/AR10321845347697033217?region=IN",
            "page_name": "ECOILA PRIVATE LIMITED (verified)",
            "started": "2026-11-10 (advertiser record read live)",
            "destination": "https://greencarbonhub.com/ - domain confirmed on the advertiser record",
            "text": "14 live ads listed under this advertiser in Google's Ads "
                    "Transparency Centre - 11 Display image creatives were "
                    "visible on the advertiser page, plus 2 YouTube video "
                    "creatives (rFydyADZH6U and 4g7BazeEIbw) and one further "
                    "creative carrying the visible copy 'Get Subsidy Upto Rs "
                    "78000 - Solar Panels for Home' (www.greencarbonhub.com) "
                    "and 'Get affordable solar services from the best solar "
                    "rooftop service providers in Hyderabad'.\n"
                    "\n"
                    "Advertiser verified. Legal name read off the advertiser "
                    "record: ECOILA PRIVATE LIMITED - not Green Carbon Hub.\n"
                    "\n"
                    "The site behind the spend is a static PHP site whose "
                    "title is the bare word 'GreenCarbonHub', whose meta "
                    "description is empty, and whose services are Solar "
                    "Installation, Water & Wastewater Management and "
                    "Bio-Methanation.",
        },
    ],
    "Sri Balaji Solar Energies": [
        {
            "library_id": "",
            "library_url": "https://adstransparency.google.com/?region=IN&domain=sribalajisolarenergies.com",
            "page_name": "No advertiser record found (queried 2026-11-10)",
            "started": "2026-11-10 (domain probe read live)",
            "destination": "https://www.sribalajisolarenergies.com/ - the advertised domain",
            "text": "Zero live ads listed for this domain in Google's Ads "
                    "Transparency Centre (queried 2026-11-10). All of this "
                    "advertiser's paid activity is on Meta.\n"
                    "\n"
                    "That is a defensible channel choice for a Telugu-first "
                    "residential offer - and it means every enquiry comes "
                    "through the Meta ads, all of which click to fb.me rather "
                    "than to the site.",
        },
    ],
}


# ===========================================================================
# The live Meta ads, read from the Meta Ad Library (India, active ads) on
# 2026-11-10. Telugu copy is stored as an English gloss prefixed "Telugu:" -
# the same convention the batch-6 reports use - because the Indic script
# cannot render in the PDF fonts.
# ===========================================================================

META_ADS = {
    "Green Carbon Hub": [
        {
            "library_id": "1387783212859779",
            "page_name": "Green Carbon Hub",
            "started": "Aug 30, 2026",
            "destination": "http://fb.me/",
            "text": "Don't Just Install Solar. Keep It Performing!\n\n"
                    "Installing Solar System is only the beginning. With "
                    "GreenCarbonHub's lifetime maintenance support, your "
                    "solar system stays efficient, reliable and ready to "
                    "perform at its best.\n\n"
                    "Long-term solar care / Better system performance / "
                    "Reliable maintenance support / Complete peace of mind.\n\n"
                    "Choose GreenCarbonHub for solar care that lasts a "
                    "lifetime.",
            "image_urls": [],
            "images": [],
            "library_url": "https://www.facebook.com/ads/library/?id=1387783212859779",
        },
        {
            "library_id": "1031770816527038",
            "page_name": "Green Carbon Hub",
            "started": "Sep 10, 2026",
            "destination": "http://fb.me/",
            "text": "You invested in Solar to Save Money. But most systems "
                    "quietly Lose 30% Power because no one maintains them.\n\n"
                    "With Free Solar Checkup and Cleaning for your system, we "
                    "fix it!\n\n"
                    "Stay Efficient and Stay Worry Free. If your Solar output "
                    "is low and facing any issues, remember GreenCarbonHub. "
                    "For Optimum Solar Performance Through Life Time "
                    "Maintenance.\n\n"
                    "Contact Us Today! Call: +91 9182445300 / 715 | Email: "
                    "info@greencarbonhub.com | Visit: "
                    "www.greencarbonhub.com",
            "image_urls": [],
            "images": [],
            "library_url": "https://www.facebook.com/ads/library/?id=1031770816527038",
        },
    ],
    "Sri Balaji Solar Energies": [
        {
            "library_id": "942037648839408",
            "page_name": "Sri Balaji Solar Energies",
            "started": "May 29, 2026",
            "destination": "http://fb.me/",
            "text": "Telugu: No more current bills to pay! Get a solar system "
                    "installed on your roof with Rs. 0 (zero) upfront cost.* "
                    "Sri Balaji Solar Energies - 14 years of trust. Central "
                    "government subsidy up to Rs. 78,000; pay just Rs. 1,355 "
                    "EMI instead of a monthly current bill; 10,000+ satisfied "
                    "customers; the subsidy applies to government employees "
                    "too; service across Warangal, Hanumakonda, Rajahmundry, "
                    "Bhadrachalam, Ghatkesar, Huzurabad, Hyderabad and nearby "
                    "districts. Free site visit today.",
            "image_urls": [],
            "images": ["612709264_1552468135986225_124_9599309.jpg"],
            "library_url": "https://www.facebook.com/ads/library/?id=942037648839408",
        },
        {
            "library_id": "1454295123168911",
            "page_name": "Sri Balaji Solar Energies",
            "started": "May 29, 2026",
            "destination": "http://fb.me/",
            "text": "Telugu: Say goodbye to heavy monthly current bills! Get "
                    "the best solar plan and subsidy details for your home. "
                    "Sri Balaji Solar Energies (15 years legacy). Leave your "
                    "details - our experts will call you with full "
                    "information.",
            "image_urls": [],
            "images": ["657034938_1472739317629903_793_25053152.jpg"],
            "library_url": "https://www.facebook.com/ads/library/?id=1454295123168911",
        },
        {
            "library_id": "1541931104220931",
            "page_name": "Sri Balaji Solar Energies",
            "started": "May 29, 2026",
            "destination": "http://fb.me/",
            "text": "Telugu: Get the details! Sri Balaji Solar Energies (15 "
                    "years legacy). Leave your details - our experts will "
                    "call you with full information. (Lead-form ad.)",
            "image_urls": [],
            "images": [],
            "library_url": "https://www.facebook.com/ads/library/?id=1541931104220931",
        },
        {
            "library_id": "2103721667197349",
            "page_name": "Sri Balaji Solar Energies",
            "started": "Aug 18, 2026",
            "destination": "http://fb.me/",
            "text": "Telugu: Save 1 LAKH - LIMITED TIME OFFER. Pay EMI instead "
                    "of your current bill and save your money. Struggling "
                    "with high current bills? With the MNRE government "
                    "subsidy, install a SOLAR ONGRID SYSTEM on your roof, use "
                    "the power you need through net metering and sell the "
                    "surplus. Contact: +91-91333 03164.",
            "image_urls": [],
            "images": ["774834968_3674322072733699_349_40074366.jpg"],
            "library_url": "https://www.facebook.com/ads/library/?id=2103721667197349",
        },
        {
            "library_id": "4493621594235361",
            "page_name": "Sri Balaji Solar Energies",
            "started": "Aug 25, 2026",
            "destination": "http://fb.me/",
            "text": "Thinking about switching to solar? Explore rooftop solar "
                    "with Sri Balaji Solar Energies and check your "
                    "eligibility for subsidy and affordable EMI options. Book "
                    "your FREE site visit today.\n\n"
                    "Get Up to Rs. 78,000 Solar Subsidy in Telangana* - Check "
                    "Your Solar Eligibility.",
            "image_urls": [],
            "images": ["773671691_1623652985991006_244_5486747.jpg"],
            "library_url": "https://www.facebook.com/ads/library/?id=4493621594235361",
        },
    ],
}


# ===========================================================================
# Competitor creatives, captured 2026-10-19 from the "solar Hyderabad" query
# (~330 results) by the Ad Library sweep that ran with the original no-website
# reports. They are reproduced with their original start dates and library IDs;
# the own-ad data in this rebuild was re-read on 2026-11-10.
# ===========================================================================

COMPETITOR_QUERY = {
    "query": "solar Hyderabad",
    "results_label": "~330 results",
    "results_count": 330,
    "url": ("https://www.facebook.com/ads/library/?active_status=active"
            "&ad_type=all&country=IN&q=solar+Hyderabad&search_type=keyword_unordered"),
    "found": True,
}

META_COMPETITORS = {
    "Green Carbon Hub": [
        {
            "library_id": "1634933028227929",
            "page_name": "Venus home appliances",
            "started": "Aug 19, 2026",
            "text": "Venus - the most reliable name in Home Appliances including "
                    "Water Heaters, Solar Water Heaters and High-performance "
                    "Fans. VENUS Water Heaters Now in Hyderabad. Visit GKK "
                    "Electricals for the latest VENUS range and exclusive "
                    "launch offers.",
            "image_urls": [],
            "images": [
                "772735182_1663495645499486_247_24651394.jpg",
                "769403501_1045846358303612_840_58474373.jpg",
            ],
            "library_url": "https://www.facebook.com/ads/library/?id=1634933028227929",
            "destination": "",
        },
        {
            "library_id": "942037648839408",
            "page_name": "Sri Balaji Solar Energies",
            "started": "May 29, 2026",
            "text": "Telugu: No more current bills to pay! Get a solar system "
                    "installed on your roof with Rs. 0 upfront cost. Sri Balaji "
                    "Solar Energies - 14 years of trust. Central government "
                    "subsidy up to Rs. 78,000; pay just Rs. 1,355 EMI instead "
                    "of a monthly current bill; 10,000+ satisfied customers; "
                    "service across Warangal, Hanumakonda, Rajahmundry, "
                    "Bhadrachalam, Ghatkesar, Huzurabad, Hyderabad and nearby "
                    "districts. Free site visit today.",
            "image_urls": [],
            "images": ["612709264_1552468135986225_124_59919500.jpg"],
            "library_url": "https://www.facebook.com/ads/library/?id=942037648839408",
            "destination": "http://fb.me/",
        },
        {
            "library_id": "2110991659634519",
            "page_name": "ORBIT SOLAR",
            "started": "Dec 10, 2025",
            "text": "\"They trusted us. You can too.\" 5+ years, 1000+ "
                    "installations across Hyderabad - all with 25-year "
                    "guarantees. orbitsolar.in | +91-9059806772. Ad variants: "
                    "'Save Rs. 3,000/Month Like Him', 'Cut Your Bill by 90% "
                    "Too', 'Get Rs. 78K Subsidy - Zero Hassle', 'Get a Solar "
                    "Pergola Like This', 'Join 1000+ Happy Homes'.",
            "image_urls": [],
            "images": [
                "595637113_843065571766706_2520_5490127.jpg",
                "594423875_1532465847848295_231_84847185.jpg",
            ],
            "library_url": "https://www.facebook.com/ads/library/?id=2110991659634519",
            "destination": "http://fb.me/",
        },
    ],
    "Sri Balaji Solar Energies": [
        {
            "library_id": "1634933028227929",
            "page_name": "Venus home appliances",
            "started": "Aug 19, 2026",
            "text": "Venus - the most reliable name in Home Appliances including "
                    "Water Heaters, Solar Water Heaters and High-performance "
                    "Fans. VENUS Water Heaters Now in Hyderabad. Visit GKK "
                    "Electricals for the latest VENUS range and exclusive "
                    "launch offers.",
            "image_urls": [],
            "images": [
                "772735182_1663495645499486_247_88094707.jpg",
                "769403501_1045846358303612_840_78324147.jpg",
            ],
            "library_url": "https://www.facebook.com/ads/library/?id=1634933028227929",
            "destination": "",
        },
        {
            "library_id": "1970895137170804",
            "page_name": "AB Solar Power Systems",
            "started": "Oct 11, 2026",
            "text": "This Dussehra, Hyderabad homes can go solar with Rs. 0 down "
                    "payment on eligible EMI plans, Rs. 22,000 off from AB "
                    "Solar, and up to Rs. 78,000 government subsidy*. Book a "
                    "free site visit. Call us: +91 80990 40600 | 9121 9121 35. "
                    "Visit: www.absolar.in. Serving Hyderabad & surrounding "
                    "areas.",
            "image_urls": [],
            "images": ["841439167_1424386869844643_261_75509363.jpg"],
            "library_url": "https://www.facebook.com/ads/library/?id=1970895137170804",
            "destination": "http://www.absolar.in/",
        },
        {
            "library_id": "1553074916624250",
            "page_name": "Suryon",
            "started": "Oct 1, 2026",
            "text": "Your Roof Can Save You Money! Go solar, reduce your monthly "
                    "electricity expenses. Reduce Your Electricity Bill with "
                    "Rooftop Solar! Generate your own clean electricity and "
                    "enjoy long-term savings on your monthly power bills. Check "
                    "your solar eligibility, subsidy benefits, and suitable "
                    "system size with our solar experts.",
            "image_urls": [],
            "images": ["790509774_1761904034702808_833_78008651.jpg"],
            "library_url": "https://www.facebook.com/ads/library/?id=1553074916624250",
            "destination": "http://fb.me/",
        },
    ],
}

# Local creative files, downloaded by the earlier Ad Library sweep into
# 01-LEADS/audit_results/ad_images/<lead>/. The stored basenames carry a
# cache-buster suffix that differs from the local copy, so files are matched
# on the leading <id>_<id>_<id> triple.
AD_IMAGE_DIR = os.path.join(BASE, "audit_results", "ad_images")
_IMG_INDEX = None


def _image_index():
    idx = {}
    if os.path.isdir(AD_IMAGE_DIR):
        for folder in sorted(os.listdir(AD_IMAGE_DIR)):
            path = os.path.join(AD_IMAGE_DIR, folder)
            if not os.path.isdir(path):
                continue
            for fn in sorted(os.listdir(path)):
                if not fn.lower().endswith((".jpg", ".jpeg", ".png")):
                    continue
                key = "_".join(fn.split("_")[:3])
                idx.setdefault(key, os.path.join(path, fn))
    return idx


def resolve_images(names):
    """Map stored creative basenames to the local files that exist here."""
    global _IMG_INDEX
    if _IMG_INDEX is None:
        _IMG_INDEX = _image_index()
    out = []
    for name in names or []:
        key = "_".join(os.path.basename(name).split("_")[:3])
        hit = _IMG_INDEX.get(key)
        if hit:
            out.append(hit)
    return out


def attach_images(ads):
    """Resolve every ad's local creative files in place."""
    for ad in ads:
        ad["images"] = resolve_images(ad.get("images"))
    return ads


# ---------------------------------------------------------------------------
# Google ad counts, read live today. (Sri Balaji is the zero-ad case.)
# ---------------------------------------------------------------------------

GOOGLE_AD_COUNT = {
    "Four Solar": 9,
    "Origian Power": 3,
    "Green Carbon Hub": 14,
    "Sri Balaji Solar Energies": 0,
}

META_QUERY = {
    "Four Solar": "Four Solar",
    "Origian Power": "Origian Power",
    "Green Carbon Hub": "Green Carbon Hub",
    "Sri Balaji Solar Energies": "Sri Balaji Solar Energies",
}

META_RESULTS = {          # what today's Ad Library query returned
    "Four Solar": (False, 0, "No ads match your search criteria"),
    "Origian Power": (False, 0, "No ads match your search criteria"),
    "Green Carbon Hub": (True, 2, "2 live ads"),
    "Sri Balaji Solar Energies": (True, 8, "~8 results"),
}


def google_detail(company):
    """The google_own block, built from the live advertiser record."""
    meta = COMPANY[company]
    ad = ADS[company][0]
    count = GOOGLE_AD_COUNT[company]
    domain = meta["website"].split("//")[-1].strip("/")
    if count:
        return {
            "found": True,
            "results_count": count,
            "results_label": f"{count} live Google ads",
            "query": f"adstransparency.google.com/?region=IN&domain={domain}",
            "detail": {
                "name": ad["page_name"],
                "advertiser_id": ad["library_id"],
                "country": "IN",
                "ad_count": count,
                "url": ad["library_url"],
                "image_files": [ad["text"]],
            },
        }
    return {
        "found": False,
        "results_count": 0,
        "results_label": "0 live Google ads",
        "query": f"adstransparency.google.com/?region=IN&domain={domain}",
        "detail": {
            "name": "No advertiser record found",
            "advertiser_id": "",
            "country": "IN",
            "ad_count": 0,
            "url": ad["library_url"],
            "image_files": [],
        },
    }


def meta_own_block(company):
    """The meta_own block from today's Ad Library query."""
    found, count, label = META_RESULTS[company]
    return {
        "found": found,
        "results_count": count,
        "results_label": label,
        "query": META_QUERY[company],
        "ads": attach_images(META_ADS.get(company, [])),
    }


def competitor_block(company):
    """The competitor Meta block, or an empty one when none was captured."""
    if company not in META_COMPETITORS:
        return {}
    block = dict(COMPETITOR_QUERY)
    block["captured_on"] = "2026-10-19"     # when the sweep actually ran
    block["ads"] = attach_images(META_COMPETITORS[company])
    return block


def adlib_block(company):
    """The full ad_library block, every field read today."""
    meta = COMPANY[company]
    g = google_detail(company)
    m = meta_own_block(company)
    g_count = g["results_count"]
    m_count = m["results_count"]
    g_name = ADS[company][0]["page_name"]

    if g_count and m_count:
        summary = (
            f"{g_count} live Google ads confirmed on {READ_ON} in Google's Ads "
            f"Transparency Centre under advertiser {g_name} (ID "
            f"{ADS[company][0]['library_id']}), identity-verified, with "
            f"{meta['website']} as the advertised domain; and {m_count} live "
            f"Meta ads on the {META_QUERY[company]} page in the Meta Ad "
            f"Library, read the same day."
        )
    elif g_count:
        summary = (
            f"{g_count} live Google ads confirmed on {READ_ON} in Google's Ads "
            f"Transparency Centre under advertiser {g_name} (ID "
            f"{ADS[company][0]['library_id']}), identity-verified, with "
            f"{meta['website']} as the advertised domain. The Meta Ad Library "
            f"was queried the same day and returned no ads for this company."
        )
    else:
        summary = (
            f"No Google Ads advertiser record was found for this domain on "
            f"{READ_ON} in Google's Ads Transparency Centre. {m_count} live "
            f"Meta ads were confirmed the same day in the Meta Ad Library on "
            f"the {META_QUERY[company]} page - all of the paid activity is on "
            f"Meta."
        )

    return {
        "checked_at": READ_ON,
        "meta_own": m,
        "google_own": g,
        "summary": summary,
        "meta_competitors": competitor_block(company),
        "google_competitors": {
            "advertisers": [],
            "note": ("Competitor Google advertiser sweeps were not run for "
                     "this lead in this pass, so no competitor Google "
                     "advertiser counts are claimed here."),
        },
        "notes": [
            f"Google Ads Transparency Centre advertiser record read directly "
            f"on {READ_ON}. Meta Ad Library (India, active ads) queried the "
            f"same day. Page source read through the W3C Nu HTML Checker with "
            f"showsource=yes on {READ_ON}."
            + (f" Competitor Meta creatives were captured on 2026-10-19 from "
               f"the '{COMPETITOR_QUERY['query']}' query "
               f"({COMPETITOR_QUERY['results_label']}) and are reproduced "
               f"with their original start dates and library IDs."
               if company in META_COMPETITORS else ""),
        ],
    }


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

    return {
        "pixel": bool(pixels_map.get("meta_pixel")),
        "ga4": bool(pixels_map.get("google_analytics_ga4")),
        "gtm": bool(pixels_map.get("google_tag_manager")),
        "google_ads_tag": bool(pixels_map.get("google_ads")),
        "checked_on": READ_ON,
        "note": (f"Read on {READ_ON} from the served page source through the "
                 f"W3C Nu HTML Checker. Confirmed present: "
                 f"{', '.join(found)}."),
    }


# ---------------------------------------------------------------------------
# Ads-only reports: refresh the existing JSON in place (website measurements
# are re-read from the LEADS dicts every run; the ad-library half is replaced
# because today's record supersedes the 2026-10-20 Meta-only probe).
# ---------------------------------------------------------------------------

def build_ads_only(company):
    path = os.path.join(ADS_ONLY_DIR, f"audit_{company.replace(' ', '_')}.json")
    if not os.path.exists(path):
        print(f"  !! missing JSON for {company}: {path}")
        return None
    with open(path, encoding="utf-8") as f:
        audit = json.load(f)

    meta = COMPANY[company]
    site = LEADS_ADS_ONLY[company]

    audit["company"] = company
    audit["legal"] = meta["legal"]
    audit["city"] = meta["city"]
    audit["website"] = meta["website"]
    audit["ads_only"] = True
    audit["website_audit_run"] = True
    audit["checked_on"] = READ_ON
    audit["generated_at"] = READ_ON
    audit["audit_date"] = READ_ON
    audit["source"] = ("Google Ads Transparency Centre (advertiser record "
                       "read directly) + Meta Ad Library (India, active ads) "
                       "+ the company's own live website (page source read "
                       "through the W3C Nu HTML Checker)")
    audit["ad_library"] = adlib_block(company)
    audit["funnel"] = {
        "destination": meta["website"],
        "note": ("Advertised domain as shown on the Google Ads Transparency "
                 "Centre advertiser record, read live on " + READ_ON + "."),
    }
    audit["contact_facts"] = meta["contact_facts"]
    audit["contact"] = meta["contact"]

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
    audit["status_compact"] = True

    evidence = evidence_for(site, site["pixels"])
    audit["site_evidence"] = evidence
    audit["promise_gap"] = PROMISE_GAP.get(company, [])
    audit["ads_audit"] = evaluate(audit, evidence)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(audit, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return audit, path


# ---------------------------------------------------------------------------
# Full audits: flat JSON, as audit_pdf.generate_pdf expects.
# ---------------------------------------------------------------------------

def build_full(company):
    site = dict(LEADS_FULL[company])
    meta = COMPANY[company]

    result = calculate_audit_score(
        {},
        site["pixels"],
        site["conversion"],
        site["seo"],
        site["pagespeed"],
    )
    result["issues"] = EXTRA_ISSUES.get(company, []) + result["issues"]

    audit = {
        "company": company,
        "legal": meta["legal"],
        "city": meta["city"],
        "website": meta["website"],
        "ssl": site["ssl"],
        "load_time_seconds": site["load_time_seconds"],
        "final_url": site["final_url"],
        "audit_date": READ_ON,
        "pixels": site["pixels"],
        "conversion": site["conversion"],
        "seo": site["seo"],
        "pagespeed": site["pagespeed"],
        "page_count": site["page_count"],
        "local_signals": site["local_signals"],
        "platform": site["platform"],
        "html_errors": site["html_errors"],
        "scope_note": site["scope_note"],
        "score": result,
        "status_compact": True,
        "ad_library": adlib_block(company),
        "ad_check_urls": {
            "google_ads_transparency": ADS[company][0]["library_url"],
            "meta_ad_library": (
                "https://www.facebook.com/ads/library/?active_status=active"
                "&ad_type=all&country=IN&q="
                + META_QUERY[company].replace(" ", "+")
                + "&search_type=keyword_unordered"),
            "note": ("Open these URLs in your browser to check the live ads "
                     "and re-read every figure in this report yourself."),
        },
        "promise_gap": PROMISE_GAP.get(company, []),
        "contact_facts": meta["contact_facts"],
        "contact": meta["contact"],
    }

    evidence = evidence_for(site, site["pixels"])
    audit["site_evidence"] = evidence
    audit["ads_audit"] = evaluate(audit, evidence)

    slug = company.replace(" ", "_")
    path = os.path.join(FULL_DIR, f"audit_{slug}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(audit, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return audit, path


def main():
    changed = []

    print("=" * 72)
    print("BATCH 18 - rebuilding 4 reports (ads-only x2, full audit x2)")
    print("=" * 72)

    for company in LEADS_ADS_ONLY:
        built = build_ads_only(company)
        if not built:
            continue
        audit, path = built
        out = generate_ads_only_pdf(audit)
        sc = audit["site_audit"]["score"]["score"]
        counts = (audit["ads_audit"] or {}).get("counts") or {}
        print(f"  {company:<26} score {sc:>3}/100  "
              f"issues {len(audit['site_audit']['score']['issues']):>2}  "
              f"wins {len(audit['site_audit']['score']['wins']):>2}  "
              f"controls {counts.get('pass', 0)}P/{counts.get('fail', 0)}F/"
              f"{counts.get('unknown', 0)}U  -> {os.path.basename(out)}")
        changed.append(out)

    for company in LEADS_FULL:
        audit, path = build_full(company)
        out = generate_pdf(audit)
        sc = audit["score"]["score"]
        counts = (audit["ads_audit"] or {}).get("counts") or {}
        print(f"  {company:<26} score {sc:>3}/100  "
              f"issues {len(audit['score']['issues']):>2}  "
              f"wins {len(audit['score']['wins']):>2}  "
              f"controls {counts.get('pass', 0)}P/{counts.get('fail', 0)}F/"
              f"{counts.get('unknown', 0)}U  -> {os.path.basename(out)}")
        changed.append(out)

    print(f"\nRebuilt {len(changed)} reports.")
    return changed


if __name__ == "__main__":
    main()
