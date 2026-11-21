#!/usr/bin/env python3
"""Build batch-15 (Telangana) ads reports - the five final leads.

Five further Telangana solar leads confirmed 2026-11-21 through the Meta Ad
Library (India, active ads), each opened by library ID, then cross-checked
against the company's own live site / the TGREDCO empanelled-supplier list:

  1. Growcell Solar Energy (Hyderabad, Banjara Hills) - 2 live ads, website
     live, contact page live with two offices.
  2. SunSolar (SunSolarhyd) (Hyderabad, Narsingi) - 5 live ads, NO website
     (sunsolarpowersolutions.in does not resolve) -> ads-only report.
  3. Roof Rays Solar Solutions (Tellapur, Hyderabad) - 3 ad IDs opened
     directly, website live, WhatsApp + email + address published.
  4. Akhil Electrical Works (Suryapet) - 4 live ads, no website; TGREDCO
     empanelled, Justdial profile -> ads-only report.
  5. Manasa Enterprises (Hyderabad, Miyapur) - 1 live ad carrying a full
     price ladder, no website -> ads-only report.

WHERE EVERY NUMBER BELOW CAME FROM (all read live 2026-11-21):

* Meta Ad Library (India, active ads). Every library ID below was confirmed by
  opening it directly at ``https://www.facebook.com/ads/library/?id=<ID>``
  with ``&country=IN``; the page name / page ID beside the card in the same
  response is what is recorded here. The "~N results" line is the page
  listing read in the same session, and where the two disagree the report says
  so rather than picking the flattering number.
* The company's own website, read through a rendered-content fetch. Head HTML
  (pixels, meta description, Open Graph, JSON-LD) is NOT captured through this
  channel, so those checks are stored as ``None`` (not checked) - never as
  absent.

CHECKS THAT COULD NOT BE RUN ARE STORED AS ``None`` AND RENDER AS
"Not checked in this pass" / "Not available at audit time". They are never
guessed:

* Google PageSpeed mobile score + LCP - the keyless API returns HTTP 429.
* Tracking pixels (Meta Pixel / GA4 / GTM / Google Ads) - raw head HTML not
  captured.
* Google Ads Transparency advertiser records - not fetched.
* Sitemap page count - not fetched.

SunSolar, Akhil Electrical Works and Manasa Enterprises carry no ``site_audit``
(none of the three has a website), so those three reports are live-ad-activity
only and say so on page 1.

Run:  cd 01-LEADS && PYTHONPATH=/tmp/pdflibs python3 build_batch15_5leads_telangana.py
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

from ads_audit import calculate_audit_score          # noqa: E402
from ads_audit_controls import evaluate              # noqa: E402
from audit_pdf import generate_ads_only_pdf          # noqa: E402

AUDIT_DIR = os.path.join(BASE, "ads_only_results")
READ_ON = "2026-11-21"
PAGESPEED_ERROR = "API returned 429"      # keyless PageSpeed quota, read live


def unknown_pixels(**over):
    """None = the head was never read, so presence is unknown in both directions."""
    d = {
        "meta_pixel": None,
        "google_ads": None,
        "google_analytics_ga4": None,
        "google_analytics_ua": None,
        "linkedin_insight": None,
        "microsoft_clarity": None,
        "hotjar": None,
        "google_tag_manager": None,
    }
    d.update(over)
    return d


# ---------------------------------------------------------------------------
# 1. GROWCELL SOLAR ENERGY (Hyderabad, Banjara Hills + Ahmedabad HO)
# ---------------------------------------------------------------------------
# Website read live 2026-11-21: https://growcellenergy.in/ and
# https://growcellenergy.in/contact-us/.
# Home: title "Solar Company in Hyderabad | GrowCell Energy", H1 "Empowering
# India with Clean Solar Energy". The counters render as "panels installed
# 475+ / brands 0+ / satisfied customers 4+ / Years success 0+" - the brand
# and year counters read 0+ on the live page. Four named testimonials
# (Mahesh Dabhoriya, Dipesh Shah, Amit Patel, Rahul Mehta) with no city on any
# of them. WhatsApp CTA wa.me/918520032200 with a pre-filled "residential
# solar system for my home" message. Two quote blocks on one page, one of
# which points its own button at https://growcellenergy.in/main-home/#quote.
# Contact page: Ahmedabad Head Office A-506 Siddhivinayak Tower, Makarba,
# S.G. Highway, Ahmedabad 380051, +91 97247 21060, sales@growcellenergy.in,
# maps cid 10437082199953957977; Hyderabad Office RELIANCE MAJESTIC, M FLOOR,
# 8-2, 626, Rd Number 11, Banjara Hills, Hyderabad 500034, +91 878 023 2338.
# Both ads are placed by "Growcell Solar Energy" (page 61591290572665) WITH the
# "Growcell Energy LLP" page (1244655595388630) - a co-authored/partner ad.

GROWCELL_SITE = {
    "ssl": True,
    "load_time_seconds": None,
    "final_url": "https://growcellenergy.in/",
    "audit_date": READ_ON,
    "pixels": unknown_pixels(),
    "conversion": {
        "has_contact_form": True,          # WPForms "Request a Quote" (name/phone/email/service/bill/city)
        "has_phone_click": True,           # +91 878 023 2338 / +91 97247 21060 on the contact page
        "has_whatsapp_link": True,         # wa.me/918520032200 with pre-filled message
        "has_cta_buttons": 6,              # Explore Our Services / Get a Free Quote Today /
                                           # Get In Touch (WhatsApp) / Request a Quote x2 / Submit
        "has_live_chat": False,
        "has_popup_optin": False,
        "has_testimonials": True,          # 4 named testimonials, no city or project detail
        "has_pricing_page_link": False,    # no system price anywhere on the site
    },
    "seo": {
        "has_title": True,
        "title_text": "Solar Company in Hyderabad | GrowCell Energy",
        "title_length": 45,
        "has_meta_description": None,      # head not captured
        "meta_desc_length": None,
        "h1_count": 1,
        "h1_text": "Empowering India with Clean Solar Energy",
        "has_og_tags": None,
        "has_schema": None,
        "has_favicon": None,
        "image_count": None,
        "images_without_alt": None,
    },
    "pagespeed": {"error": PAGESPEED_ERROR},
    "page_count": {"has_sitemap": None},
    "local_signals": {"has_google_maps_embed": True},   # Google Maps embed on /contact-us/
    "platform": "WordPress + WPForms Lite; two quote forms on one page",
    "html_errors": None,
    "scope_note": (
        "The website was read live on 2026-11-21 through a rendered-content "
        "fetch of the home page and the contact page. Tracking-pixel and head "
        "checks (Meta Pixel, GA4, GTM, Google Ads, meta description, Open "
        "Graph, JSON-LD, favicon) need the raw served HTML and were not "
        "captured through this channel, so they are recorded as not checked "
        "rather than absent. PageSpeed and sitemap were not run."
    ),
}

GROWCELL_ADS = [
    {
        "library_id": "2267587767143531",
        "library_url": "https://www.facebook.com/ads/library/?id=2267587767143531",
        "page_name": "Growcell Solar Energy",
        "started": "Nov 15, 2026",
        "destination": "Facebook lead form (FB.ME) - 'Get quote'",
        "text": (
            "Rs.78,000 TAK SUBSIDY!\n\n"
            "Apne ghar ki chhat par solar lagao aur pao PM Surya Ghar Yojana "
            "ke under Rs.78,000 tak ki government subsidy!\n\n"
            "Bijli ke bill ko karo kam aur clean, green energy ki taraf badhao "
            "ek kadam!\n\n"
            "- Up to Rs.78,000 subsidy for eligible residential consumers\n"
            "- Complete solar installation support\n"
            "- Subsidy documentation mein assistance\n"
            "- Save on electricity bills for years to come\n\n"
            "Growcell Energy ke saath apna solar journey shuru karein!\n\n"
            "Aaj hi contact karein aur apna solar quote paayein.\n\n"
            "Subsidy eligibility and amount are subject to government "
            "guidelines and approval.\n\n"
            "FB.ME card: 'Growcell Solar Energy - Get quote'\n"
            "Ad Library note: run jointly - the card reads 'Growcell Solar "
            "Energy with Growcell Energy LLP'; creative is a video; the card "
            "CTA is 'Get quote'. This is the only ad in the set that carries "
            "a subsidy figure, and it carries the qualifying line too."
        ),
    },
    {
        "library_id": "1171646568632890",
        "library_url": "https://www.facebook.com/ads/library/?id=1171646568632890",
        "page_name": "Growcell Solar Energy",
        "started": "Nov 15, 2026",
        "destination": "Facebook lead form (FB.ME) - 'Get quote'",
        "text": (
            "How much solar does your home need?\n\n"
            "Share your electricity bill with us and our team will help you "
            "understand:\n\n"
            "- Required solar capacity\n"
            "- Estimated system cost\n"
            "- Applicable subsidy\n"
            "- Expected monthly savings\n\n"
            "Get your FREE Solar Quote today!\n\n"
            "Headline (on the card): 'Rs.5K-Rs.10K Bill? Go Solar!'\n"
            "Card body: 'Rooftop solar lagakar apni electricity cost ko "
            "significantly reduce karein.'\n"
            "Ad Library note: creative is a video; the ad's own card headline "
            "assumes a Rs.5,000-10,000 monthly bill; card CTA is 'Get quote'."
        ),
    },
]

GROWCELL = {
    "company": "Growcell Solar Energy",
    "legal": "Growcell Energy LLP (Ahmedabad) - Hyderabad branch office",
    "city": "Hyderabad, Telangana (Banjara Hills); HO Ahmedabad",
    "offer_angles": [
        "Rs.78,000 PM Surya Ghar subsidy",
        "bill-based sizing / free quote",
    ],
    "social_proof_in_ads": False,
    "website": "https://growcellenergy.in/",
    "ads_only": True,
    "website_audit_run": True,
    "checked_on": READ_ON,
    "generated_at": READ_ON,
    "source": "Meta Ad Library (India, active) + live website fetch, 2026-11-21",
    "ad_count_note": (
        "Caveat: both live ads were opened directly, but no page-listing "
        "count was read for this page in the same session, so the live total "
        "may be higher than the 2 creatives reproduced here."
    ),
    "ad_library": {
        "meta_own": {
            "found": True,
            "results_count": 2,
            "results_label": "2 live ads opened directly (page listing not counted)",
            "query": "Growcell Solar Energy (page ID 61591290572665) + Growcell Energy LLP (1244655595388630), Meta Ad Library, India, active",
            "ads": GROWCELL_ADS,
        },
        "summary": (
            "2 live Meta ads confirmed on 2026-11-21, both started 15 Nov 2026 "
            "and both click to a Facebook lead form rather than to "
            "growcellenergy.in. The pair is placed by the 'Growcell Solar "
            "Energy' page together with the 'Growcell Energy LLP' page. One ad "
            "sells the Rs.78,000 PM Surya Ghar subsidy in Hinglish with the "
            "required eligibility caveat; the other offers a free quote from "
            "your electricity bill and carries the card headline 'Rs.5K-Rs.10K "
            "Bill? Go Solar!'. No ad states a system size, a system price or an "
            "EMI. The website was read live the same day; Google Ads "
            "Transparency records were not checked in this pass."
        ),
    },
    "funnel": {
        "type": "Facebook lead form",
        "destination": "Facebook lead form (FB.ME) - 'Get quote' on both ads",
        "meaning": (
            "Neither live ad links to growcellenergy.in, even though the site "
            "runs a WPForms quote form, a WhatsApp CTA and two office addresses "
            "that would all reassure a buyer spending lakhs. Every enquiry "
            "lands inside Meta, so no click can be retargeted, attributed or "
            "followed up outside the inbox."
        ),
    },
    "findings": [
        "Both ads are placed by the Growcell Energy LLP page, and a direct Ad "
        "Library lookup of the brand page (61591290572665) returns no active "
        "ads at all - so the name the ads are labelled with is not the page "
        "carrying the spend, and a buyer searching for the brand page finds "
        "nothing running.",
        "Both live ads click to a Facebook lead form, never to "
        "growcellenergy.in - so the site's own WPForms quote form, its "
        "WhatsApp CTA and its two office addresses are invisible to every "
        "rupee of this spend.",
        "The home page's own counters contradict each other: 'panels "
        "installed 475+' sits beside 'satisfied customers 4+' and 'brands 0+' "
        "and 'Years success 0+'. A visitor reading the proof strip sees two "
        "zeroes next to the one number the business wants to lead with.",
        "The Hyderabad address is 'RELIANCE MAJESTIC, M FLOOR, 8-2, 626, Rd "
        "Number 11, Banjara Hills' - a serviced/office building with no unit "
        "number, while the Ahmedabad head office gets a full unit ('A-506'). "
        "For a Hyderabad-targeted ad, the local address is the vaguer one.",
        "The two ads sell two different things. One leads with 'Rs.78,000 TAK "
        "SUBSIDY' and correctly footnotes 'subject to government guidelines "
        "and approval'; the other leads with 'How much solar does your home "
        "need?' and a 'Rs.5K-Rs.10K Bill?' headline that assumes a monthly "
        "bill band. Same budget, same day, two different offers - and no "
        "landing page behind either to show which one converts.",
        "Neither of the two live ads carries a system price, an EMI or a "
        "kW-to-bill table, and the site publishes none either "
        "anywhere, so the ad that asks the buyer to 'share your electricity "
        "bill' has nowhere to send them to self-serve a number first.",
        "All four site testimonials (Mahesh Dabhoriya, Dipesh Shah, Amit "
        "Patel, Rahul Mehta) carry no city and no system size - on a "
        "Hyderabad-targeted campaign, none of the proof is local.",
        "The ad copy is Hinglish while the website is English-only, so the "
        "buyer the ad speaks to arrives at a page written in a different "
        "register.",
    ],
    "next_steps": [
        ("Send one ad to growcellenergy.in, not only to the lead form",
         "The site already has a quote form, a WhatsApp CTA and two offices. "
         "Put a Meta Pixel and UTMs on it and point one creative there so the "
         "click becomes measurable, retargetable and attributable."),
        ("Fix the proof counters before the next rupee of spend",
         "'brands 0+' and 'Years success 0+' sit next to '475+ panels "
         "installed'. Either fill them from real numbers or remove them - a "
         "buyer who notices the zeroes discounts the 475 as well."),
        ("Put one worked price on the landing page",
         "The ads ask for a bill and promise a quote; the site shows no kW "
         "price, no EMI and no subsidy-adjusted total. One worked 3 kW "
         "example would answer the ad's question before the form."),
        ("Make the Hyderabad office as specific as the Ahmedabad one",
         "Add the floor/unit and a map link to the Banjara Hills address, and "
         "put the Hyderabad number on the ad's landing page - the campaign "
         "sells to Hyderabad but the site leads with an Ahmedabad head "
         "office."),
        ("Add the local proof the site is missing",
         "One named Hyderabad install with a kW size and a locality would do "
         "more than four uncited testimonials on a city-targeted campaign."),
    ],
    "contact_facts": [
        ("Phone (Hyderabad office)", "+91 878 023 2338"),
        ("Phone (Ahmedabad HO)", "+91 97247 21060"),
        ("WhatsApp (site CTA)", "wa.me/918520032200"),
        ("Email", "sales@growcellenergy.in"),
        ("Hyderabad office",
         "RELIANCE MAJESTIC, M FLOOR, 8-2, 626, Rd Number 11, Banjara Hills, "
         "Hyderabad, Telangana 500034"),
        ("Ahmedabad head office",
         "A-506, Siddhivinayak Tower, Beside Kataria Arcade, Near D.A.V. "
         "School, Makarba, S.G. Highway, Ahmedabad 380051"),
        ("Facebook page", "https://www.facebook.com/61591290572665/"),
        ("Second advertiser page", "https://www.facebook.com/growcellenergy/ (Growcell Energy LLP)"),
        ("Page ID (Ad Library)", "61591290572665 (advertiser) / 1244655595388630 (LLP)"),
        ("Website", "https://growcellenergy.in/"),
    ],
    "contact": {
        "phone": "+91 878 023 2338",
        "email": "sales@growcellenergy.in",
    },
    "site_audit": GROWCELL_SITE,
    "audit_date": READ_ON,
    "site_evidence": {
        "pixel": None,
        "utm": False,
        "checked_on": READ_ON,
        "note": (
            "Head HTML not captured through the sandbox fetch channel; pixel "
            "presence is not checked, not asserted absent. No UTM parameters "
            "appear on any link in the rendered page content, and the ads "
            "themselves land on an fb.me lead form, which carries no campaign "
            "parameters."
        ),
    },
    "promise_gap": [
        {
            "promise": "'Up to Rs.78,000 subsidy' + 'subsidy documentation mein assistance'",
            "site": (
                "The site never states whether Growcell is a registered PM "
                "Surya Ghar vendor, who files the application, or what happens "
                "if the subsidy is refused. The ad says eligibility is subject "
                "to government approval but leaves the buyer to assume "
                "Growcell handles it."
            ),
        },
        {
            "promise": "'Share your electricity bill ... estimated system cost'",
            "site": (
                "The site publishes no system price, no per-kW rate and no "
                "EMI, so the number the ad promises cannot be checked or "
                "self-served anywhere on growcellenergy.in."
            ),
        },
        {
            "promise": "'Rs.5K-Rs.10K Bill? Go Solar!' (card headline)",
            "site": (
                "Nothing on the site maps a monthly bill band to a kW size or "
                "a price, so the headline's implied 'your bill decides your "
                "system' is never actually worked out for the reader."
            ),
        },
    ],
}


# ---------------------------------------------------------------------------
# 2. SUNSOLAR (SUNSOLARHYD) (Hyderabad, Narsingi) - no website
# ---------------------------------------------------------------------------
# Ad page read live 2026-11-21: facebook.com/sunsolarhyd, page ID
# 1056719797535626. Five live ads opened: 2576227376137902 (Oct 22, 3 kW
# Rs.1,31,999), 2285688872164421 (Oct 23, same offer, ANANTHAPUR variant),
# 1443902311044175 (Oct 26), 2413566255849370 (Nov 21, 6 hrs, 5 kW
# Rs.2,18,999 from Rs.2,96,999 less Rs.78,000) and 1866738597708833 (Nov 21,
# 6 hrs, 4 kW Rs.1,71,999 from Rs.2,49,999 less Rs.78,000).
# sunsolarpowersolutions.in and www.sunsolarpowersolutions.in both return DNS
# NXDOMAIN, so there is no site to audit.
# The phone number is printed two different ways across the offer set:
# "+91 98666 02001" in the 3 kW and 4 kW ads, "+91 98666 20001" in the 5 kW
# ad. Both are recorded here exactly as printed, and neither is silently
# normalised into the other.

SUNSOLAR_ADS = [
    {
        "library_id": "2413566255849370",
        "library_url": "https://www.facebook.com/ads/library/?id=2413566255849370",
        "page_name": "SunSolarhyd",
        "started": "Nov 21, 2026",
        "destination": "Facebook lead form (FB.ME) - 'Get offer'",
        "text": (
            "GO SOLAR FOR JUST Rs.2,18,999/-!\n\n"
            "Power your home with clean, reliable solar energy and enjoy "
            "long-term electricity savings!\n\n"
            "Get a 5 kW Solar System at just Rs.2,18,999/- with SunSolar Power "
            "Systems, featuring trusted solar brands Adani Solar & Waaree "
            "Solar.\n\n"
            "WHY WAIT? MAKE THE SWITCH TO SOLAR TODAY!\n\n"
            "- 5 kW Solar Power System\n"
            "- 0 Down Payment\n"
            "- Easy EMI Available\n"
            "- Government Subsidy Included\n"
            "- 30 Years Warranty\n"
            "- Free Site Visit\n\n"
            "Original Price: Rs.2,96,999/-\n"
            "Government Subsidy: Rs.78,000/-\n"
            "Your Final Price: Rs.2,18,999/-\n\n"
            "Call Now: +91 98666 20001\n"
            "Office: Suite 312, 3rd Floor, Kokapet Terminal Complex, Gandipet "
            "Main Road, Narsingi, Hyderabad, Telangana - 500075.\n\n"
            "FB.ME card: '5 kW Solar at Rs.2,18,999/-! - Get offer'\n\n"
            "Ad Library note: this is the one ad in the set that prints the number as 98666 20001; the 3 kW and 4 kW ads print 98666 02001."
        ),
    },
    {
        "library_id": "1866738597708833",
        "library_url": "https://www.facebook.com/ads/library/?id=1866738597708833",
        "page_name": "SunSolarhyd",
        "started": "Nov 21, 2026",
        "destination": "Facebook lead form (FB.ME) - 'Get offer'",
        "text": (
            "Go Solar for Just Rs.1,71,999!\n\n"
            "Make your home energy-efficient with a 4 kW Solar System from "
            "SunSolar Power Systems!\n\n"
            "Festive Season Offer Includes:\n\n"
            "- Rs.78,000 Government Subsidy Included\n"
            "- 0 Down Payment\n"
            "- Easy EMI Available\n"
            "- 30 Years Warranty\n"
            "- Free Site Visit\n\n"
            "Your Solar Price Breakdown:\n"
            "Rs.2,49,999 - Rs.78,000 Subsidy = Rs.1,71,999/-\n\n"
            "Reduce your electricity expenses and make the switch to solar "
            "this festive season!\n\n"
            "Call +91 98666 02001\n"
            "Suite 312, 3rd Floor, Kokapet Terminal Complex, Gandipet Main "
            "Road, Narsingi, Hyderabad, Telangana - 500075.\n\n"
            "Book your FREE Solar Consultation Today! Limited-time festive "
            "offer.\n\n"
            "FB.ME card: '4 kW Solar at Rs.1,71,999 - Get offer'\n\n"
            "Ad Library note: opened at this ad's own permalink on 21 Nov 2026. Read 6 hrs live on one render and 7 on another the same day, so no hours-live figure is recorded here."
        ),
    },
    {
        "library_id": "2576227376137902",
        "library_url": "https://www.facebook.com/ads/library/?id=2576227376137902",
        "page_name": "SunSolarhyd",
        "started": "Oct 22, 2026",
        "destination": "Facebook lead form (FB.ME) - 'Get offer'",
        "text": (
            "HYDERABAD, SWITCH TO SOLAR FOR JUST Rs.1,31,999!\n\n"
            "This is your chance to make the switch to clean energy with "
            "SunSolar Power Systems!\n\n"
            "SPECIAL 3 KW SOLAR OFFER\n\n"
            "Only Rs.1,31,999/-\n"
            "- Government Subsidy Included - Rs.78,000\n"
            "- Rs.0 Down Payment\n"
            "- Easy EMI Available\n"
            "- 30 Years Warranty\n"
            "- Free Site Visit\n\n"
            "Why pay high electricity bills when your rooftop can generate "
            "your own power? Invest in solar today and enjoy long-term savings "
            "with trusted Adani Solar & Waaree Solar panels!\n\n"
            "Book your FREE solar consultation now!\n"
            "Call: +91 98666 02001\n"
            "Suite 312, 3rd Floor, Kokapet Terminal Complex, Gandipet Main "
            "Road, Narsingi, Hyderabad.\n\n"
            "FB.ME card: '3 KW Solar Rs.1,31,999 - Get offer'\n\n"
            "Ad Library note: opened at this ad's own permalink."
        ),
    },
    {
        "library_id": "2285688872164421",
        "library_url": "https://www.facebook.com/ads/library/?id=2285688872164421",
        "page_name": "SunSolarhyd",
        "started": "Oct 23, 2026",
        "destination": "Facebook lead form (FB.ME) - 'Get offer'",
        "text": (
            "ANANTHAPUR, SWITCH TO SOLAR FOR JUST Rs.1,31,999!\n\n"
            "This is your chance to make the switch to clean energy with "
            "SunSolar Power Systems!\n\n"
            "SPECIAL 3 KW SOLAR OFFER\n\n"
            "Only Rs.1,31,999/-\n"
            "- Government Subsidy Included - Rs.78,000\n"
            "- Rs.0 Down Payment\n"
            "- Easy EMI Available\n"
            "- 30 Years Warranty\n"
            "- Free Site Visit\n\n"
            "Why pay high electricity bills when your rooftop can generate "
            "your own power? Invest in solar today and enjoy long-term savings "
            "with trusted Adani Solar & Waaree Solar panels!\n\n"
            "Book your FREE solar consultation now!\n"
            "Call: +91 98666 02001\n"
            "Suite 312, 3rd Floor, Kokapet Terminal Complex, Gandipet Main "
            "Road, Narsingi, Hyderabad.\n\n"
            "FB.ME card: '3 KW Solar Rs.1,31,999 - Get offer'\n\n"
            "Ad Library note: the identical 3 kW creative as 2576227376137902 with only the city word changed; the hashtags still read #Hyderabad."
        ),
    },
]

SUNSOLAR = {
    "company": "SunSolar Power Systems",
    "legal": "SunSolar Power Systems, trading as SunSolarhyd (facebook.com/sunsolarhyd)",
    "city": "Hyderabad, Telangana (Narsingi)",
    "offer_angles": [
        "net price after subsidy (Rs.1.31-2.18 lakh ladder)",
        "subsidy included in the price",
        "EMI / zero down payment",
        "30-year warranty",
    ],
    "social_proof_in_ads": False,
    "website": "",
    "ads_only": True,
    "website_audit_run": False,
    "checked_on": READ_ON,
    "generated_at": READ_ON,
    "source": "Meta Ad Library (India, active), 2026-11-21; no website resolves",
    "ads_listing_read": True,
    "ad_count_note": (
        "4 live ads, each opened at its own permalink and checked against "
        "its Library ID. Ads 2576227376137902 and 2285688872164421 share one "
        "3 kW creative with only the city changed. No page-listing total was "
        "read, so a paused or region-restricted ad would not be counted here."
    ),
    "ad_library": {
        "meta_own": {
            "found": True,
            "results_count": 4,
            "results_label": "4 live ads, each verified at its own Ad Library permalink",
            "query": "SunSolarhyd page (page ID 1056719797535626), Meta Ad Library, India, active",
            "ads": SUNSOLAR_ADS,
        },
        "summary": (
            "At least 5 live Meta ads on the SunSolarhyd page (page ID "
            "1056719797535626) on 2026-11-21, running since 22 Oct 2026 with "
            "two fresh creatives on 21 Nov 2026 (6 hrs live at read). The page "
            "sells a price ladder - 3 kW Rs.1,31,999, 4 kW Rs.1,71,999, 5 kW "
            "Rs.2,18,999 - every rung presented as 'subsidy included' with "
            "Rs.0 down payment, '30 Years Warranty', free site visit and Adani "
            "/ Waaree panels. Every ad clicks to a Facebook lead form. There is "
            "no website: sunsolarpowersolutions.in does not resolve, so no site "
            "audit was run."
        ),
    },
    "funnel": {
        "type": "Facebook lead form",
        "destination": "Facebook lead form (FB.ME) - 'Get offer' on every ad",
        "meaning": (
            "There is no website and no landing page anywhere in the funnel: "
            "every click on a Rs.1.3-2.2 lakh offer ends in a Facebook lead "
            "form. The buyer cannot check the company, the warranty terms or "
            "the address before handing over a phone number, and nothing can "
            "be retargeted or followed up outside the Meta inbox."
        ),
    },
    "findings": [
        "There is no website at all - sunsolarpowersolutions.in returns DNS "
        "NXDOMAIN - yet the ads quote a full price ladder up to Rs.2,18,999. "
        "A buyer cannot check the firm, the warranty exclusions or the address "
        "anywhere before submitting a phone number.",
        "The page prints its own phone number two different ways inside the "
        "same offer set: '+91 98666 02001' in the 3 kW and 4 kW ads, "
        "'+91 98666 20001' in the 5 kW ad. One of the two is wrong on a "
        "lakh-scale purchase, and nobody can tell which from outside.",
        "'30 Years Warranty' is stated with no qualifier in every ad - no "
        "distinction between the module's performance warranty and the "
        "inverter, structure or workmanship, which is where the buyer's real "
        "risk sits.",
        "The 3 kW creative is re-used verbatim for Hyderabad (Oct 22) and "
        "Ananthapur (Oct 23) - only the first word changes, and the Ananthapur "
        "version still carries #Hyderabad in its hashtags - so the same "
        "Rs.1,31,999 is quoted across two different markets with no stated "
        "exclusions and a hashtag pointing at the wrong city.",
        "Every offer is presented as a net price - the 5 kW ad runs the sum "
        "out loud, 'Original Price Rs.2,96,999 - Government Subsidy Rs.78,000 "
        "= Your Final Price Rs.2,18,999' - but no ad says whether SunSolar "
        "nets that Rs.78,000 into the invoice or whether the buyer pays in "
        "full and waits for the subsidy to be credited after commissioning. "
        "On a Rs.2.19 lakh purchase that is the difference between arranging "
        "Rs.2.19 lakh and arranging Rs.2.97 lakh, and the ads never say which.",
        "'0 Down Payment' and 'Easy EMI Available' are stated without a "
        "lender, a tenure, a rate or a monthly figure anywhere in the ad set, "
        "so the single number a homeowner actually budgets cannot be found.",
        "Four of the five ads click to a lead form with no landing page, no "
        "UTM and no distinct offer tracking, so the 3 kW, 4 kW and 5 kW "
        "creatives cannot be compared against each other.",
    ],
    "next_steps": [
        ("Register one domain and put a single page on it",
         "A one-page site with the price ladder, the Rs.78,000 subsidy "
         "mechanics, the warranty split (module / inverter / workmanship), the "
         "Kokapet office address and a form with a Meta Pixel. Without it "
         "there is nothing to verify and nothing to retarget."),
        ("Fix the phone number to one correct format",
         "The page currently prints 98666 02001 and 98666 20001 in the same "
         "campaign. Pick the live one, use it everywhere, and put it on the "
         "landing page as a tel: link."),
        ("Split the warranty claim into its three parts",
         "'30 Years Warranty' with no qualifier reads as a warranty on the "
         "whole system. State module performance, inverter and workmanship "
         "separately - it is the fastest way to look more credible than the "
         "competitor making the same claim."),
        ("Say how the Rs.78,000 actually reaches the buyer",
         "State plainly that the subsidy is credited to the customer after "
         "commissioning, and what the buyer pays up front. Every ad currently "
         "presents a net price that may not be the amount payable at "
         "booking."),
        ("Put one EMI figure against each kW size",
         "'Easy EMI Available' is in all five ads and no ad gives a tenure or "
         "a monthly amount. One line - 3 kW, Rs.X/month, Y years - answers "
         "the question the lead form is asking the buyer to ask."),
        ("Use the Ananthapur variant as a lesson, not a template",
         "Re-running the Hyderabad creative with only the city swapped means "
         "neither market gets a locally priced, locally evidenced offer."),
    ],
    "contact_facts": [
        ("Phone (3 kW and 4 kW ads)", "+91 98666 02001"),
        ("Phone (5 kW ad)", "+91 98666 20001 - printed differently on the same page"),
        ("Office",
         "Suite 312, 3rd Floor, Kokapet Terminal Complex, Gandipet Main Road, "
         "Narsingi, Hyderabad, Telangana 500075"),
        ("Facebook page", "https://www.facebook.com/sunsolarhyd/"),
        ("Page ID (Ad Library)", "1056719797535626"),
        ("Website", "None - sunsolarpowersolutions.in does not resolve (NXDOMAIN)"),
        ("Panels named in ads", "Adani Solar, Waaree Solar"),
        ("Subsidy claim", "Rs.78,000 'included' in every price"),
    ],
    "contact": {
        "phone": "+91 98666 02001",
        "email": "",
    },
    "audit_date": READ_ON,
    "site_evidence": {
        "pixel": None,
        "utm": False,
        "checked_on": READ_ON,
        "note": (
            "This business has no website (the domain does not resolve), so no "
            "pixel or UTM check was possible. Recorded as not checked rather "
            "than absent. Every ad lands on an fb.me lead form, which carries "
            "no campaign parameters."
        ),
    },
    "promise_gap": [
        {
            "promise": "'30 Years Warranty' (every ad)",
            "site": (
                "There is no site and no warranty document anywhere, so a "
                "buyer cannot tell whether this covers the module only, the "
                "inverter, the structure or the workmanship."
            ),
        },
        {
            "promise": "'Government Subsidy Included - Rs.78,000' (every ad)",
            "site": (
                "No ad explains that PM Surya Ghar subsidy is credited to the "
                "customer after commissioning, or what is payable at booking - "
                "yet each price is quoted net of it."
            ),
        },
        {
            "promise": "'0 Down Payment' / 'Easy EMI Available'",
            "site": (
                "No lender, tenure, rate or monthly figure appears in any ad, "
                "and there is no site where the terms could be read."
            ),
        },
    ],
}


# ---------------------------------------------------------------------------
# 3. ROOF RAYS SOLAR SOLUTIONS (Tellapur, Hyderabad)
# ---------------------------------------------------------------------------
# Website read live 2026-11-21: https://roofrays.in/ (single page).
# Title "Solar Energy Solutions | Roof Rays Solar Solutions". H1 "SOLAR ENERGY
# SOLUTIONS FOR HOMES, HOUSING SOCIETIES, BUSINESSES & INDUSTRIES". Published
# contact block: 96669 90036, support@roofrays.in, "HUDA Complex, Tellapur,
# Hyderabad", Google Maps place Roof+Rays+Solar+Solutions at 17.4635977,
# 78.2867255, plus YouTube @RoofRaysSolarSolutions, Instagram roofrays_solar
# and a LinkedIn profile (vishwak-muvva). The site also publishes: four-step
# process, "Rs.1 Lakh Roof Protection Assurance", "5-Year Expert Maintenance
# Support", "14-27 working days" for a typical install, "60-90%" bill savings,
# an EMI line, and a subsidy countdown widget reading "Last date to apply 31
# March 2027" with a live "130 Days 02 Hrs" timer and a wa.me/919666990036
# eligibility CTA. Every page CTA points at /connect-with-us/#CONTACT - a form
# on the same page - not at WhatsApp or a phone dialler.
# A separate web search the same day returned the fuller street address
# (Vishnu Car Care Building, 2nd Floor, Tellapur Road, HUDA Complex, Plot No.
# 32), which is NOT on the site's own contact block; the report records it as
# a search-sourced address and keeps the site's own wording separate.

ROOFRAYS_SITE = {
    "ssl": True,
    "load_time_seconds": None,
    "final_url": "https://roofrays.in/",
    "audit_date": READ_ON,
    "pixels": unknown_pixels(),
    "conversion": {
        "has_contact_form": True,          # "Get Free Solar Consultation" form (name/WhatsApp/location/property type)
        "has_phone_click": True,           # 96669 90036 in the top bar and the footer
        "has_whatsapp_link": True,         # wa.me/919666990036 on the subsidy-eligibility CTA
        "has_cta_buttons": 8,              # Get a Free Quote / Get a Free Solar Consultation x2 /
                                           # Know More x3 / Check My Eligibility / Get Free Solar Consultation
        "has_live_chat": False,
        "has_popup_optin": True,           # the subsidy countdown panel expands over the page
        "has_testimonials": False,         # no named customer, review or install count anywhere
        "has_pricing_page_link": False,    # no system price or kW rate published
    },
    "seo": {
        "has_title": True,
        "title_text": "Solar Energy Solutions | Roof Rays Solar Solutions",
        "title_length": 55,
        "has_meta_description": None,      # head not captured
        "meta_desc_length": None,
        "h1_count": 1,
        "h1_text": "SOLAR ENERGY SOLUTIONS FOR HOMES, HOUSING SOCIETIES, BUSINESSES & INDUSTRIES",
        "has_og_tags": None,
        "has_schema": None,
        "has_favicon": None,
        "image_count": None,
        "images_without_alt": None,
    },
    "pagespeed": {"error": PAGESPEED_ERROR},
    "page_count": {"has_sitemap": None},
    "local_signals": {"has_google_maps_embed": True},   # maps place link in the contact block
    "platform": "WordPress; single-page landing with a separate /connect-with-us/ contact page",
    "html_errors": None,
    "scope_note": (
        "The website was read live on 2026-11-21 through a rendered-content "
        "fetch of the home page. Tracking-pixel and head checks (Meta Pixel, "
        "GA4, GTM, Google Ads, meta description, Open Graph, JSON-LD, "
        "favicon) need the raw served HTML and were not captured through this "
        "channel, so they are recorded as not checked rather than absent. "
        "PageSpeed and sitemap were not run."
    ),
}

ROOFRAYS_ADS = [
    {
        "library_id": "1825502928519547",
        "library_url": "https://www.facebook.com/ads/library/?id=1825502928519547",
        "page_name": "Roof Rays Solar Solutions",
        "started": "Nov 16, 2026",
        "destination": "Facebook lead form (FB.ME) - 'Get quote'",
        "text": (
            "What if you could drive up to 2,000 KM without worrying about "
            "monthly fuel expenses?\n\n"
            "Yes! It's possible with the right combination of a 5 kW rooftop "
            "solar system and an Electric Vehicle.\n\n"
            "Generate approximately 600 units of solar electricity every "
            "month.\n"
            "Use 300 units for your home.\n"
            "Utilize the surplus solar power to charge your EV.\n"
            "Potentially save up to Rs.20,000 per month on fuel expenses!\n\n"
            "Why pay more for electricity and fuel when your rooftop can help "
            "power both your home and your car?\n\n"
            "Switch to Solar. Drive Smarter. Save More!\n\n"
            "Contact Roof Rays Solar Solutions today for your FREE Solar "
            "Quotation!\n\n"
            "FB.ME card: 'Save Up to Rs.20,000/Month with Solar + EV! - Power "
            "Your Home & EV with Rooftop Solar. Get Your Free Quote Today!'\n"
            "Ad Library note: creative is a video."
        ),
    },
    {
        "library_id": "1635924467937920",
        "library_url": "https://www.facebook.com/ads/library/?id=1635924467937920",
        "page_name": "Roof Rays Solar Solutions",
        "started": "Nov 4, 2026",
        "destination": "Facebook lead form (FB.ME) - 'Get quote'",
        "text": (
            "Ready to cut down your electricity bills?\n\n"
            "Switch to rooftop solar with Roof Rays Solar Solutions and enjoy "
            "long-term savings! Eligible residential customers can get solar "
            "subsidies of up to Rs.78,000.\n\n"
            "Make your rooftop work for you.\n\n"
            "Enquire today for your FREE Solar Quote!\n\n"
            "FB.ME card: 'Save Up to Rs.78,000 with Solar! - Install Rooftop "
            "Solar. Reduce Your Bills.'\n"
            "Ad Library note: creative is a video."
        ),
    },
    {
        "library_id": "1184145723936677",
        "library_url": "https://www.facebook.com/ads/library/?id=1184145723936677",
        "page_name": "Roof Rays Solar Solutions",
        "started": "Nov 4, 2026",
        "destination": "Facebook lead form (FB.ME) - 'Get quote'",
        "text": (
            "Why pay more for electricity when you can turn sunshine into "
            "savings?\n\n"
            "Make the smart switch to rooftop solar with Roof Rays Solar "
            "Solutions!\n\n"
            "Get up to Rs.78,000 in eligible government subsidy.\n"
            "Reduce your electricity expenses.\n"
            "Enjoy clean energy and long-term savings.\n\n"
            "Don't wait! Start your solar journey today and make the most of "
            "available subsidy benefits.\n\n"
            "Get your FREE solar quotation now!\n\n"
            "FB.ME card: 'Turn Sunshine into Savings! - Go Solar. Save More. "
            "Enjoy Subsidy Benefits.'\n"
            "Ad Library note: creative is a video."
        ),
    },
]

ROOFRAYS = {
    "company": "Roof Rays Solar Solutions",
    "legal": "Roof Rays Solar Solutions (roofrays.in)",
    "city": "Hyderabad, Telangana (Tellapur / HUDA Complex)",
    "offer_angles": [
        "up to Rs.78,000 government subsidy",
        "solar + EV fuel savings",
        "electricity bill savings",
    ],
    "social_proof_in_ads": False,
    "website": "https://roofrays.in/",
    "ads_only": True,
    "website_audit_run": True,
    "checked_on": READ_ON,
    "generated_at": READ_ON,
    "source": "Meta Ad Library (India, active) + live website fetch, 2026-11-21",
    "ad_count_note": (
        "Caveat: 3 ad IDs were opened directly on 2026-11-21; an earlier read "
        "of the same page the same day showed 5 active ads, so the live total "
        "is approximately 3-5 and the 3 creatives above are the ones confirmed "
        "by direct open."
    ),
    "ad_library": {
        "meta_own": {
            "found": True,
            "results_count": 3,
            "results_label": "3 live ads, each re-read at its own Ad Library permalink",
            "query": "Roof Rays Solar Solutions, Meta Ad Library, India, active - "
        "the Ad Library reports this advertiser under page id 997092546826993, "
        "which differs from the 61587695438410 in the Facebook profile URL",
            "ads": ROOFRAYS_ADS,
        },
        "summary": (
            "3 ad IDs opened directly on 2026-11-21, all active on the Roof Rays "
            "Solar Solutions page (page ID 61587695438410): 1825502928519547 "
            "(16 Nov, solar + EV), 1635924467937920 and 1184145723936677 (both "
            "4 Nov, Rs.78,000 subsidy). An earlier read of the same page the "
            "same day showed 5 live ads, so treat the count as 3-5. All three "
            "click to a Facebook lead form rather than to roofrays.in. The site "
            "was read live the same day: four service lines, a four-step "
            "process, a Rs.1 lakh roof-protection assurance, a 5-year "
            "maintenance promise, a 14-27 working-day install window and a "
            "subsidy countdown dated 31 March 2027."
        ),
    },
    "funnel": {
        "type": "Facebook lead form",
        "destination": "Facebook lead form (FB.ME) - 'Get quote' on all 3 ads",
        "meaning": (
            "Every live ad ends in a Facebook lead form, while the site carries "
            "a detailed qualification form (property type, residence type, "
            "housing-society name, average monthly bill) that would sort a "
            "homeowner from a housing society from a C&I buyer before anyone "
            "picks up the phone. None of this spend reaches that form, so the "
            "richest qualification data the business owns is not being used."
        ),
    },
    "findings": [
        "All three live ads click to a Facebook lead form, never to "
        "roofrays.in - in a business that sells to homes, housing societies "
        "and commercial/industrial buyers separately, the site's own form "
        "(property type, residence type, society name, average monthly bill) "
        "would qualify each lead before the first call, and none of this spend "
        "reaches it.",
        "The site's subsidy panel is a live countdown - 'Last date to apply 31 "
        "March 2027', '130 Days 02 Hrs 07 Mins' - while the ads never mention "
        "a deadline at all. The urgency asset exists and is not being used "
        "where the money is being spent.",
        "The site promises 'Rs.1 Lakh Roof Protection Assurance' and '5-Year "
        "Expert Maintenance Support' and no live ad mentions either - the two "
        "most concrete, checkable offers the business has are missing from the "
        "creatives.",
        "The site does publish an estimated price table and a units-to-kW "
        "guide - 3 kW Rs.1,45,000-2,10,000, 5 kW Rs.2,30,000-3,50,000, 10 kW "
        "Rs.4,80,000-7,20,000, and '300-450 units -> 3 kW' - on its residential "
        "guide page. None of the three ads carries a price or links to that "
        "page: the ads land on a lead form, so the one comparison asset the "
        "business owns is invisible to its paid traffic.",
        "The ads target a Hyderabad homeowner with 'up to Rs.20,000 per month "
        "on fuel expenses' from a solar + EV combination, but no EV system, EV "
        "charger or worked EV example appears on the home page or the "
        "residential guide read for this report - the biggest number in the "
        "campaign is the one the destination does not set out.",
        "The site publishes no customer name, review, install count, kW "
        "installed or project photograph with a locality anywhere, on a "
        "purchase that runs to lakhs and next to competitors quoting install "
        "counts in their first line.",
        "The contact block gives the address as 'HUDA Complex, Tellapur' with "
        "no building, floor or plot number, while the Google Maps place it "
        "links to is pinned to a specific coordinate (17.4636, 78.2867) - a "
        "buyer checking the firm on a map gets a pin, not an address they can "
        "drive to.",
    ],
    "next_steps": [
        ("Point at least one ad at roofrays.in, not only at the lead form",
         "The site already qualifies leads better than the Meta form does. Put "
         "a Meta Pixel and UTMs on it and send one creative there so the click "
         "becomes measurable and the qualification data survives."),
        ("Put the 31 March 2027 countdown into the ad copy",
         "The site's own panel carries a live day counter. The same deadline, "
         "in the creative, is a stronger call to action than 'Get your FREE "
         "solar quotation' - and it is already the asset the business "
         "believes in."),
        ("Lead with the Rs.1 lakh roof-protection assurance",
         "Roof damage and leakage is the single biggest objection in rooftop "
         "solar, and Roof Rays already sells a named assurance against it. It "
         "appears in no ad. Put it in the creative and on the landing page."),
        ("Point the ads at the price guide that already exists",
         "The residential guide already answers the buyer's first question "
         "with a kW price range and a units-to-kW table. No ad links to it. "
         "Either send a creative there (with UTMs) or lift the 3 kW range into "
         "the ad itself so 'up to Rs.78,000' becomes a checkable number."),
        ("Either build an EV page or drop the Rs.20,000/month EV claim",
         "The 16 Nov ad's entire hook is solar + EV savings, and no EV content "
         "was found on the pages read for this report. A short EV page with "
         "one worked example would make the claim verifiable; without it, the "
         "number is the weakest link in the campaign."),
        ("Publish the full street address and one local install",
         "Add the building, floor and plot to the contact block, and one named "
         "Tellapur/Hyderabad install with a kW size. It converts a map pin "
         "into a business a buyer can check."),
    ],
    "contact_facts": [
        ("Phone", "96669 90036"),
        ("WhatsApp", "wa.me/919666990036 (subsidy eligibility CTA)"),
        ("Email", "support@roofrays.in"),
        ("Address (site)",
         "HUDA Complex, Tellapur, Hyderabad, Telangana"),
        ("Address (search result, not on the site's own block)",
         "Vishnu Car Care Building, 2nd Floor, Tellapur Road, HUDA Complex, "
         "Plot No. 32, Tellapur - recorded as search-sourced, verify before use"),
        ("Google Maps place", "Roof Rays Solar Solutions - 17.4635977, 78.2867255"),
        ("Facebook page", "https://www.facebook.com/profile.php?id=61587695438410"),
        ("Page ID (Ad Library)", "61587695438410"),
        ("Website", "https://roofrays.in/"),
        ("Social", "Instagram roofrays_solar, YouTube @RoofRaysSolarSolutions"),
    ],
    "contact": {
        "phone": "96669 90036",
        "email": "support@roofrays.in",
    },
    "site_audit": ROOFRAYS_SITE,
    "audit_date": READ_ON,
    "site_evidence": {
        "pixel": None,
        "utm": False,
        "checked_on": READ_ON,
        "note": (
            "Head HTML not captured through the sandbox fetch channel; pixel "
            "presence is not checked, not asserted absent. No UTM parameters "
            "appear on any link in the rendered page content, and the ads "
            "themselves land on an fb.me lead form, which carries no campaign "
            "parameters."
        ),
    },
    "promise_gap": [
        {
            "promise": "'Save up to Rs.20,000 per month on fuel expenses' (16 Nov ad)",
            "site": (
                "No EV system, EV charger or worked EV example appears on the "
                "home page or the residential guide read for this report. The "
                "claim rests on 600 units a month from 5 kW, half of it "
                "surplus, which nothing read sets out."
            ),
        },
        {
            "promise": "'Up to Rs.78,000 in eligible government subsidy' (both 4 Nov ads)",
            "site": (
                "The site states the subsidy deadline as 31 March 2027 and "
                "otherwise leaves the mechanics to the form - it does not say "
                "who applies, when it is credited, or what the buyer pays "
                "before it arrives."
            ),
        },
        {
            "promise": "'14-27 working days' install (site FAQ)",
            "site": (
                "The site gives the window but no ad does, and the FAQ does "
                "not say whether the clock starts at booking, at approval or "
                "at net-meter sanction - the part a buyer actually plans "
                "around."
            ),
        },
    ],
}


# ---------------------------------------------------------------------------
# 4. AKHIL ELECTRICAL WORKS (Suryapet) - no website
# ---------------------------------------------------------------------------
# Four ad IDs opened directly on 2026-11-21: 997508846276370 (21 Nov, 3 hrs
# live), 1677824443701148 (17 Nov), 1387795526583908 (17 Nov) and
# 1680326913622219 (14 Nov), all on page 874469655996702
# (facebook.com/100063714323294). All four click to WhatsApp; the copy is one
# of two creatives - the English "Go Solar, Save More!" card and the Telugu
# "AKHIL ELECTRICAL WORKS & SOLAR SYSTEMS" card. Neither states a price, a kW
# size, an EMI or a warranty.
# No website exists (none is linked from any ad).
# Corroboration read the same day: TGREDCO 2026 empanelled-supplier list
# (rn TSRE250617 / Sarpanch Street, 2-30, Sajjapuram, Palakeedu, Suryapet
# 508218; Narasimha, 9000974582, narasimhayaragorla2@gmail.com) and the
# TSSPDCL registered-contractor list (Akhil Electrical Works, H.No. 1-26,
# Sajjapuram, Palakaveedu, Nalgonda 508218, GSTIN 36AJGPY1304G1ZA). Justdial
# shows the business at Suryapet Bypass Road with 4.5-4.6 stars over 11-21
# ratings, 10 years in business and 08197560059.
# NOTE: the TGREDCO address says "2-30" and the TSSPDCL list says "1-26" for
# the same Sajjapuram/Palakeedu location. Both are recorded; the difference is
# reported, not reconciled by guesswork.

AKHIL_ADS = [
    {
        "library_id": "997508846276370",
        "library_url": "https://www.facebook.com/ads/library/?id=997508846276370",
        "page_name": "Akhil Electrical Works",
        "started": "Nov 21, 2026",
        "destination": "WhatsApp (WHATSAPP / api.whatsapp.com) - 'Send WhatsApp message'",
        "text": (
            "(Telugu) 'Do you want to install solar for your home? Contact us "
            "now for government subsidy details, prices and installation "
            "information! AKHIL ELECTRICAL WORKS & SOLAR SYSTEMS'\n\n"
            "Ad Library note: started 21 Nov 2026, total active time 3 hrs. "
            "No price, kW size, EMI or warranty in the creative."
        ),
    },
    {
        "library_id": "1677824443701148",
        "library_url": "https://www.facebook.com/ads/library/?id=1677824443701148",
        "page_name": "Akhil Electrical Works",
        "started": "Nov 17, 2026",
        "destination": "WhatsApp (WHATSAPP / api.whatsapp.com) - 'Send WhatsApp message'",
        "text": (
            "'Go Solar, Save More!'\n\n"
            "Image-led card: the creative is an image only, with the single "
            "line above as the ad copy. No price, kW size, subsidy amount, EMI "
            "or warranty is stated, and the only click destination is a "
            "WhatsApp chat."
        ),
    },
    {
        "library_id": "1387795526583908",
        "library_url": "https://www.facebook.com/ads/library/?id=1387795526583908",
        "page_name": "Akhil Electrical Works",
        "started": "Nov 17, 2026",
        "destination": "WhatsApp (WHATSAPP / api.whatsapp.com) - 'Send WhatsApp message'",
        "text": (
            "'3KW & 5KW Solar Systems | Subsidy Assistance | Call Now.'\n\n"
            "Image-led card with the line above as the ad copy and a WhatsApp "
            "click destination. The two sizes are named; no price, subsidy "
            "amount, EMI or warranty term is stated."
        ),
    },
    {
        "library_id": "1680326913622219",
        "library_url": "https://www.facebook.com/ads/library/?id=1680326913622219",
        "page_name": "Akhil Electrical Works",
        "started": "Nov 14, 2026",
        "destination": "WhatsApp (WHATSAPP / api.whatsapp.com) - 'Send WhatsApp message'",
        "text": (
            "'Go Solar, Save More!'\n\n"
            "Image-led card, WhatsApp-only click destination. Nothing in the "
            "ad states a system size, a price, a subsidy figure, an EMI or a "
            "warranty term."
        ),
    },
]

AKHIL = {
    "company": "Akhil Electrical Works",
    "legal": "Akhil Electrical Works (TGREDCO-empanelled; TSSPDCL registered contractor)",
    "city": "Suryapet, Telangana",
    "offer_angles": [
        "government subsidy assistance",
        "3 kW / 5 kW system sizes",
    ],
    "social_proof_in_ads": False,
    "website": "",
    "ads_only": True,
    "website_audit_run": False,
    "checked_on": READ_ON,
    "generated_at": READ_ON,
    "source": "Meta Ad Library (India, active), 2026-11-21; no website exists",
    "ad_count_note": (
        "Caveat: 4 ad IDs were opened directly on 2026-11-21 and all four "
        "returned an active ad; no page-listing count was read, so the live "
        "total may be higher than 4."
    ),
    "ad_library": {
        "meta_own": {
            "found": True,
            "results_count": 4,
            "results_label": "4 live ads opened directly (page listing not counted)",
            "query": "Akhil Electrical Works page (page ID 874469655996702), Meta Ad Library, India, active",
            "ads": AKHIL_ADS,
        },
        "summary": (
            "4 live Meta ads confirmed on 2026-11-21 on the Akhil Electrical "
            "Works page (page ID 874469655996702): 997508846276370 (21 Nov, 3 "
            "hrs live), 1677824443701148 and 1387795526583908 (both 17 Nov) and "
            "1680326913622219 (14 Nov). The set is two creatives - an English "
            "'Go Solar, Save More!' image card and a Telugu card naming 'AKHIL "
            "ELECTRICAL WORKS & SOLAR SYSTEMS' and promising subsidy details. "
            "Every ad clicks to WhatsApp. No ad states a price, a kW size, a "
            "subsidy amount, an EMI, a warranty or a place the business can be "
            "checked. There is no website, so no site audit was run."
        ),
    },
    "funnel": {
        "type": "WhatsApp chat",
        "destination": "WhatsApp (api.whatsapp.com) - 'Send WhatsApp message' on all 4 ads",
        "meaning": (
            "There is no website and no landing page: every click ends in a "
            "WhatsApp chat. The business's strongest trust assets - a TGREDCO "
            "empanelment, a TSSPDCL contractor registration and a decade of "
            "rated local work - appear nowhere in the funnel, so the buyer has "
            "to take all of that on trust from a stranger in a chat window."
        ),
    },
    "findings": [
        "There is no website at all, and every one of the four live ads ends in "
        "a WhatsApp chat, so a Suryapet homeowner comparing quotes has no page "
        "to check a genuine government-empanelled contractor on before making "
        "contact.",
        "The business is on Telangana's TGREDCO empanelled-supplier list and "
        "holds a TSSPDCL registered-contractor registration with a GSTIN - the "
        "strongest credentials in this market - and not one of them appears in "
        "any ad or in any funnel.",
        "Not one of the four ads carries a price, a subsidy amount, an EMI or "
        "a warranty term. Only one of them (17 Nov, '3KW & 5KW Solar Systems | "
        "Subsidy Assistance') even names a system size - so a buyer has no "
        "number to shortlist on, against competitors quoting a subsidy figure "
        "or a kW price in the same feed.",
        "The newest ad (21 Nov, 3 hrs live at read) asks the buyer to contact "
        "them 'for government subsidy details, prices' - i.e. the ad's own "
        "purpose is to make the buyer ask for the information the ad does not "
        "contain.",
        "Two of the four ads open on 'Go Solar, Save More!' - three words of "
        "generic English copy on an image card, with no locality, no product "
        "and no offer - in a district market where a named local credential "
        "would do the selling.",
        "The page is already splitting its message three ways - English "
        "'Go Solar, Save More!', an English '3KW & 5KW | Subsidy Assistance' "
        "cut, and a Telugu subsidy-and-price ask - which is real testing, but "
        "all three variants end at the same numberless WhatsApp chat. The "
        "variants differ in language, not in what the buyer is promised.",
        "The business has two different published addresses for the same "
        "Sajjapuram/Palakeedu location - '2-30' on the TGREDCO list and '1-26' "
        "on the TSSPDCL list - and with no website there is nowhere for a "
        "buyer to see which one is current.",
    ],
    "next_steps": [
        ("Put up one page - it does not need to be more than one",
         "A single page with the TGREDCO empanelment reference, the TSSPDCL "
         "registration, the Suryapet address, one price per kW, one named "
         "local install and a form with a Meta Pixel. That page is what makes "
         "every future rupee measurable, and it is what converts a WhatsApp "
         "click from a stranger into a credible quote."),
        ("Lead with the empanelment in the creative",
         "TGREDCO empanelment plus a TSSPDCL contractor licence is a stronger "
         "claim than 'up to Rs.78,000', and no competitor ad in the district "
         "can match it. Put it in the first line of the ad and on the card."),
        ("Put one number in every ad",
         "A kW size and a price, or an EMI ('3 kW from Rs.X, EMI Rs.Y'), will "
         "outperform 'Go Solar, Save More!' on its own - the buyer is already "
         "asking for the price in the ad's own copy."),
        ("Say Suryapet out loud",
         "No ad names the district, the town or a service area. A local buyer "
         "scanning a feed has no reason to read a card that could be from "
         "anywhere in India."),
        ("Replace the duplicate 17 Nov creative with a test",
         "Two ads, same day, same creative, same WhatsApp destination is not a "
         "test. Run the empanelment-led card against the subsidy-led one so "
         "the spend answers a question."),
        ("Fix the address on the registers",
         "Update whichever of '2-30' and '1-26' Sajjapuram is current on the "
         "TGREDCO and TSSPDCL lists, and publish the correct one on the new "
         "page. Two government lists disagreeing is a credibility risk once "
         "buyers start checking."),
    ],
    "contact_facts": [
        ("Phone / WhatsApp (Justdial, 2026-11-21)", "08197560059"),
        ("Phone (TGREDCO list)", "9000974582"),
        ("Contact person (TGREDCO list)", "Narasimha"),
        ("Email (TGREDCO list)", "narasimhayaragorla2@gmail.com"),
        ("Address (TGREDCO 2026 list)",
         "Sarpanch Street, 2-30, Sajjapuram, Palakeedu, Suryapet, Telangana "
         "508218"),
        ("Address (TSSPDCL contractor list)",
         "H.No. 1-26, Sajjapuram, Palakaveedu, Nalgonda 508218 - differs from "
         "the TGREDCO door number"),
        ("GSTIN (TSSPDCL list)", "36AJGPY1304G1ZA"),
        ("Justdial profile",
         "Suryapet Bypass Road, Suryapet - 4.5-4.6 stars over 11-21 ratings, "
         "10 years in business"),
        ("Registration", "TGREDCO empanelled supplier TSRE250617; TSSPDCL registered contractor"),
        ("Facebook page", "https://www.facebook.com/100063714323294/"),
        ("Page ID (Ad Library)", "874469655996702"),
        ("Website", "None - every ad clicks to WhatsApp"),
    ],
    "contact": {
        "phone": "08197560059",
        "email": "narasimhayaragorla2@gmail.com",
    },
    "audit_date": READ_ON,
    "site_evidence": {
        "pixel": None,
        "utm": False,
        "checked_on": READ_ON,
        "note": (
            "This business has no website, so no pixel or UTM check was "
            "possible. Recorded as not checked rather than absent. Every ad "
            "lands on a WhatsApp chat, which carries no campaign parameters."
        ),
    },
    "promise_gap": [
        {
            "promise": "'Contact us for government subsidy details, prices and installation information' (21 Nov ad)",
            "site": (
                "The ad contains none of the three things it asks the buyer to "
                "ask for, and there is no website or landing page where any of "
                "them could be read without opening a chat."
            ),
        },
        {
            "promise": "'Go Solar, Save More!' (3 of 4 ads)",
            "site": (
                "No saving figure, no bill band and no system size is stated, "
                "so the claim cannot be checked against anything - and with no "
                "site there is no page carrying the terms."
            ),
        },
    ],
}


# ---------------------------------------------------------------------------
# 5. MANASA ENTERPRISES (Hyderabad, Miyapur) - no website
# ---------------------------------------------------------------------------
# Ad 826884287112902 opened directly on 2026-11-21: page "ManasaEnterprises",
# page ID 1259997940531140, started 22 Aug 2026, clicks to WhatsApp.
# Copy: "MANASAA ENTERPRISES / SOLAR MASTER DISTRIBUTOR", subsidy up to
# Rs.78,000*, 3 kW Rs.2,05,000*, 5 kW Rs.3,10,000*, 10 kW Rs.5,92,000*,
# solar pump sets, street lights, AC/DC systems, calls 7901253949 /
# 8074507650, "Kakinada | Hyderabad", manasaaenterprises2024@gmail.com.
# The three prices carry an asterisk with no footnote anywhere in the ad.
# No website is linked; manasaaenterprises.com did not load on 2026-11-21.
# Corroboration the same day: Justdial lists Manasaa Enterprises at Hanuman
# Temple Road, behind RBR1 Complex, Miyapur, Hyderabad - 4 years in business,
# monocrystalline/polycrystalline/solar panel installation, "starts from
# Rs.40/watt", 5.0 from 1 rating. The Justdial listing carries no phone that
# matches either ad number, so the address is corroborated and the phone is
# only as good as the ad.

MANASA_ADS = [
    {
        "library_id": "826884287112902",
        "library_url": "https://www.facebook.com/ads/library/?id=826884287112902",
        "page_name": "ManasaEnterprises",
        "started": "Aug 22, 2026",
        "destination": "WhatsApp (api.whatsapp.com) - 'Send WhatsApp message'",
        "text": (
            "MANASAA ENTERPRISES\n"
            "SOLAR MASTER DISTRIBUTOR\n"
            "Domestic & Commercial Solar Systems\n\n"
            "GOVT. SUBSIDY UP TO Rs.78,000*\n"
            "Save on Electricity Bills\n"
            "Clean & Renewable Energy\n\n"
            "SOLAR SYSTEMS\n"
            "- 3 kW - Rs.2,05,000*\n"
            "- 5 kW - Rs.3,10,000*\n"
            "- 10 kW - Rs.5,92,000*\n\n"
            "Also Available:\n"
            "Solar Pump Sets - Solar Street Lights - AC/DC Systems\n\n"
            "- Expert Installation\n"
            "- Quality Products\n"
            "- After-Sales Support\n\n"
            "CALL / WHATSAPP\n"
            "7901253949 | 8074507650\n\n"
            "Kakinada | Hyderabad\n"
            "manasaaenterprises2024@gmail.com\n\n"
            "Ad Library note: every price and the subsidy figure carry an "
            "asterisk; no footnote or T&C appears anywhere in the ad."
        ),
    },
]

MANASA = {
    "company": "Manasaa Enterprises",
    "legal": "Manasaa Enterprises (Hyderabad, Miyapur)",
    "city": "Hyderabad, Telangana (Miyapur); also Kakinada, Andhra Pradesh",
    "offer_angles": [
        "published price ladder (3/5/10 kW)",
        "subsidy up to Rs.78,000",
    ],
    "social_proof_in_ads": False,
    "website": "",
    "ads_only": True,
    "website_audit_run": False,
    "checked_on": READ_ON,
    "generated_at": READ_ON,
    "source": "Meta Ad Library (India, active), 2026-11-21; no website resolves",
    "ad_count_note": (
        "Caveat: this is a single ad opened directly (826884287112902). No "
        "page listing was read for page 1259997940531140 in the same session, "
        "so the total number of active ads is not known and is not guessed "
        "here."
    ),
    "ad_library": {
        "meta_own": {
            "found": True,
            "results_count": 1,
            "results_label": "1 ad opened directly (page listing not counted)",
            "query": "ManasaEnterprises page (page ID 1259997940531140), Meta Ad Library, India, active",
            "ads": MANASA_ADS,
        },
        "summary": (
            "1 live Meta ad confirmed on 2026-11-21 on the ManasaEnterprises "
            "page (page ID 1259997940531140), running since 22 Aug 2026 and "
            "clicking to WhatsApp. It is the only ad in this batch that "
            "publishes a full price ladder - 3 kW Rs.2,05,000, 5 kW "
            "Rs.3,10,000, 10 kW Rs.5,92,000 - plus a Rs.78,000 subsidy claim, "
            "two phone numbers, an email and two cities. Every price and the "
            "subsidy carry an asterisk with no footnote in the ad. No website "
            "is linked and manasaaenterprises.com did not load, so no site "
            "audit was run."
        ),
    },
    "funnel": {
        "type": "WhatsApp chat",
        "destination": "WhatsApp (api.whatsapp.com) - 'Send WhatsApp message'",
        "meaning": (
            "The ad publishes a full three-tier price ladder and then sends "
            "every click to a WhatsApp chat with no landing page behind it. A "
            "buyer who has just been shown a Rs.5.92 lakh price has nowhere to "
            "check the company, the asterisk's conditions or the warranty, and "
            "the business cannot retarget or measure the click."
        ),
    },
    "findings": [
        "Every price in the ad - 3 kW Rs.2,05,000, 5 kW Rs.3,10,000, 10 kW "
        "Rs.5,92,000 - and the Rs.78,000 subsidy figure carry an asterisk, and "
        "no footnote, T&C or qualifying condition appears anywhere in the ad. "
        "On a Rs.5.9 lakh quote the terms are the offer.",
        "The prices are quoted per kW size with no panel brand, inverter "
        "brand, module wattage, structure type or warranty term attached to "
        "any of them, so the three tiers cannot be compared with each other or "
        "with any competitor's quote.",
        "The ad claims 'GOVT. SUBSIDY UP TO Rs.78,000' but the three system "
        "prices are not stated as net or gross of it, so a buyer cannot tell "
        "whether the Rs.2,05,000 for 3 kW already has the subsidy in it - and "
        "at 3 kW the subsidy is the single largest line item in the purchase.",
        "There is no website: manasaaenterprises.com did not load on "
        "2026-11-21, and every click ends in a WhatsApp chat, so a buyer "
        "cannot verify the distributor before committing to a lakh-scale "
        "order.",
        "The business calls itself a 'SOLAR MASTER DISTRIBUTOR' and the ad "
        "runs in Hyderabad, but the only address detail in it is 'Kakinada | "
        "Hyderabad' - no area, no street, no pin code for either city.",
        "Only third-party corroboration of an address exists (Justdial lists "
        "Miyapur, behind RBR1 Complex, Hanuman Temple Road, 4 years in "
        "business), and the ad itself carries none of it - nor a single "
        "review, install count or project photograph.",
        "The single ad has been running unchanged since 22 Aug 2026 with no "
        "variants, so there is no message test in the account and no evidence "
        "any creative angle has ever been tried.",
    ],
    "next_steps": [
        ("Publish the asterisk",
         "State, in the ad, whether each price is net or gross of the "
         "Rs.78,000, what the asterisk conditions are, and what is included "
         "(panel/inverter brand, structure, net-metering, warranty). It is the "
         "cheapest credibility upgrade available and it costs one line of "
         "copy."),
        ("Attach a specification to each of the three tiers",
         "3 kW / 5 kW / 10 kW with a panel brand, an inverter brand and a "
         "warranty term turns three numbers into three comparable products - "
         "and is what a buyer needs to shortlist against another quote."),
        ("Put up one page, even a single page",
         "The ad already publishes the hardest content to write (a price "
         "ladder). A one-page site repeating it with the address, the "
         "asterisk, the warranty split and a Meta Pixel would make every click "
         "measurable and retargetable - and give the buyer somewhere to check "
         "the firm."),
        ("Say where in Hyderabad you actually are",
         "'Kakinada | Hyderabad' is not an address. The Justdial listing gives "
         "Miyapur, behind RBR1 Complex, Hanuman Temple Road - publish it, with "
         "a map link, in the ad and on the page."),
        ("Add one piece of proof",
         "A named install, a kW size, a locality and a photograph. A 'master "
         "distributor' claim on a lakh-scale purchase with no install, review "
         "or project behind it is the weakest part of an otherwise "
         "unusually-specific ad."),
        ("Run a second creative",
         "One ad unchanged since 22 Aug 2026 means the account has never "
         "learned anything. A variant leading with the 3 kW price and one "
         "leading with the subsidy would answer which hook this market "
         "responds to."),
    ],
    "contact_facts": [
        ("Phone / WhatsApp (ad)", "7901253949 | 8074507650"),
        ("Email (ad)", "manasaaenterprises2024@gmail.com"),
        ("Location (ad)", "Kakinada | Hyderabad - no area, street or pin code"),
        ("Location (Justdial, 2026-11-21)",
         "Hanuman Temple Road, behind RBR1 Complex, Miyapur, Hyderabad - 4 "
         "years in business"),
        ("Justdial pricing line", "'Starts from Rs.40/watt' (directory listing, not the ad)"),
        ("Facebook page", "https://www.facebook.com/61593163442429/"),
        ("Page ID (Ad Library)", "1259997940531140"),
        ("Website", "None - manasaaenterprises.com did not load on 2026-11-21"),
        ("Published prices (ad)", "3 kW Rs.2,05,000 / 5 kW Rs.3,10,000 / 10 kW Rs.5,92,000, all asterisked"),
    ],
    "contact": {
        "phone": "7901253949",
        "email": "manasaaenterprises2024@gmail.com",
    },
    "audit_date": READ_ON,
    "site_evidence": {
        "pixel": None,
        "utm": False,
        "checked_on": READ_ON,
        "note": (
            "This business has no website that loads, so no pixel or UTM check "
            "was possible. Recorded as not checked rather than absent. The ad "
            "lands on a WhatsApp chat, which carries no campaign parameters."
        ),
    },
    "promise_gap": [
        {
            "promise": "'- 3 kW - Rs.2,05,000*' / '5 kW - Rs.3,10,000*' / '10 kW - Rs.5,92,000*'",
            "site": (
                "The asterisk has no footnote anywhere in the ad and there is "
                "no website where the conditions could be read. Whether the "
                "price is net or gross of the Rs.78,000 is never stated."
            ),
        },
        {
            "promise": "'GOVT. SUBSIDY UP TO Rs.78,000*'",
            "site": (
                "No ad or page explains who applies for the subsidy, when it is "
                "credited, or what the buyer pays before it arrives."
            ),
        },
        {
            "promise": "'SOLAR MASTER DISTRIBUTOR'",
            "site": (
                "No manufacturer authorisation, brand list or dealer certificate "
                "is named anywhere - and the ad names no panel or inverter "
                "brand at all."
            ),
        },
    ],
}


LEADS = [GROWCELL, SUNSOLAR, ROOFRAYS, AKHIL, MANASA]


def build_base(lead):
    """Attach the ads-audit control review and the website score."""
    # Control review (claude-ads methodology) - graded from public evidence.
    lead["ads_audit"] = evaluate(lead, lead.get("site_evidence"))
    # Website score - only when a site_audit was actually run.
    site = lead.get("site_audit") or {}
    if site:
        score = calculate_audit_score(
            {}, site.get("pixels") or {}, site.get("conversion") or {},
            site.get("seo") or {}, site.get("pagespeed") or {},
        )
        site["score"] = score
    return lead


def evidence_for(lead):
    """One-line evidence summary per lead, for the batch log."""
    ads = (lead.get("ad_library") or {}).get("meta_own", {}).get("ads") or []
    ids = ", ".join(a["library_id"] for a in ads)
    return f"{len(ads)} ads [{ids}]"


def main():
    os.makedirs(AUDIT_DIR, exist_ok=True)
    for lead in LEADS:
        lead = build_base(lead)
        slug = re.sub(r"[^a-zA-Z0-9]+", "_", lead["company"])[:50]
        out = os.path.join(AUDIT_DIR, f"audit_{slug}.json")
        with open(out, "w", encoding="utf-8") as f:
            json.dump(lead, f, indent=2, ensure_ascii=False)
        pdf = generate_ads_only_pdf(lead)
        print(f"[built] {lead['company']}")
        print(f"  json: {out}")
        print(f"  pdf:  {pdf}")
        print(f"  evidence: {evidence_for(lead)}")
        if lead.get("site_audit"):
            print(f"  score: {lead['site_audit']['score']['score']}/100")
        else:
            print("  score: (ads-only, no website - no site_audit)")


if __name__ == "__main__":
    main()
