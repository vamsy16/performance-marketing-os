#!/usr/bin/env python3
"""Build batch-14 (Telangana) ads reports - the five final leads.

Five further Telangana solar leads confirmed 2026-11-21 through the Meta Ad
Library (India, active ads), each checked against its own live website and
cross-checked against the TGREDCO / TGNPDCL empanelled-supplier list:

  1. Griffin Energy (Hyderabad, Champapet) - 4 live Meta ads, website live.
  2. Nova Solar Solutions (Secunderabad, Tirumalagiri) - 3 ad IDs opened, all
     in one page listing, website live.
  3. Sri Narayana Enterprise Solar Energies (Adilabad) - 1 live ad running in
     ~9 creative variants, own website does not resolve -> ads-only report.
  4. Aadithya Solar Energies (Hyderabad, Kismatpur / Gandipet) - 1 live ad
     (2 ads on one creative) since 11 Sep 2026, website live but still on its
     purchased theme's demo content.
  5. Eagle Solar Systems (Hyderabad, Bachupally) - 3 live ads, NO website at
     all -> ads-only audit.

WHERE EVERY NUMBER BELOW CAME FROM (all read live 2026-11-21):

* Meta Ad Library (India, active ads). Every library ID below was confirmed by
  opening it directly at ``https://www.facebook.com/ads/library/?id=<ID>``
  with ``&country=IN``, and the page name / page ID beside the card in the same
  response is what is recorded here.
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

Sri Narayana Enterprise Solar Energies and Eagle Solar Systems carry no
``site_audit``: the first company's domain does not resolve and the second has
no website, so those two reports are live-ad-activity only and say so on
page 1.

Run:  cd 01-LEADS && PYTHONPATH=/tmp/pdflibs python3 build_batch14_5leads_telangana.py
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
# 1. GRIFFIN ENERGY (Hyderabad, Champapet)
# ---------------------------------------------------------------------------
# Website read live 2026-11-21: https://griffinenergy.in/ (single page, hash
# anchors #quote and #calculator). Title "Griffin Energy | Rooftop solar for
# Hyderabad homes". H1 "Quoted in 24 hours. Installed in one day."
# Phone +91 91605 55540 (tel: and wa.me), info@griffinenergy.in, registered
# office 17-1-386/SN/5/A, SN Reddy Nagar, Champapet, Vaishalinagar,
# Saroornagar, Hyderabad 500079. Free-site-survey form (name / mobile /
# locality / monthly-bill band), a size-and-subsidy calculator, a published
# PM Surya Ghar subsidy slab (1 kW 30,000 / 2 kW 60,000 / 3 kW+ 78,000) and an
# FAQ. The FAQ states: "Our registration on the national portal is in
# progress. We will show our vendor ID here once it is listed."
# Every live ad card is stamped "Griffin Energy is a private installer".

GRIFFIN_SITE = {
    "ssl": True,
    "load_time_seconds": None,
    "final_url": "https://griffinenergy.in/",
    "audit_date": READ_ON,
    "pixels": unknown_pixels(),
    "conversion": {
        "has_contact_form": True,          # #quote survey form (name/mobile/locality/bill)
        "has_phone_click": True,           # tel:+919160555540 in the contact block
        "has_whatsapp_link": True,         # wa.me/919160555540 (two links)
        "has_cta_buttons": 5,              # Book a free site survey / Check your system size /
                                           # Book a survey for 2.5 kW / Request my survey / WhatsApp us
        "has_live_chat": False,            # no chat widget in the rendered content
        "has_popup_optin": False,
        "has_testimonials": False,         # no named customer, review or project count anywhere
        "has_pricing_page_link": False,    # subsidy slab published, no system price
    },
    "seo": {
        "has_title": True,
        "title_text": "Griffin Energy | Rooftop solar for Hyderabad homes",
        "title_length": 51,
        "has_meta_description": None,      # head not captured
        "meta_desc_length": None,
        "h1_count": 1,
        "h1_text": "Quoted in 24 hours. Installed in one day.",
        "has_og_tags": None,               # head not captured (an og-image asset is referenced)
        "has_schema": None,
        "has_favicon": None,
        "image_count": None,
        "images_without_alt": None,
    },
    "pagespeed": {"error": PAGESPEED_ERROR},
    "page_count": {"has_sitemap": None},
    "local_signals": {"has_google_maps_embed": None},
    "platform": "Static single-page site, server-rendered HTML (hash anchors #quote / #calculator)",
    "html_errors": None,
    "scope_note": (
        "The website was read live on 2026-11-21 through a rendered-content "
        "fetch. Tracking-pixel and head checks (Meta Pixel, GA4, GTM, Google "
        "Ads, meta description, Open Graph, JSON-LD, favicon) need the raw "
        "served HTML and were not captured through this channel, so they are "
        "recorded as not checked rather than absent. PageSpeed and sitemap "
        "were not run."
    ),
}

GRIFFIN_ADS = [
    {
        "library_id": "2436699883532011",
        "library_url": "https://www.facebook.com/ads/library/?id=2436699883532011",
        "page_name": "Griffin Energy",
        "started": "Nov 15, 2026",
        "destination": "WhatsApp (WHATSAPP / wa.me) - Send WhatsApp message",
        "text": (
            "Charging your EV at a public charger costs about Rs.2.90 a km. "
            "From your own rooftop solar it is about 29 paise.\n\n"
            "That is roughly 90% less, and far below petrol at around Rs.7 a km. "
            "Over the life of the system, your roof becomes the cheapest fuel "
            "station in Hyderabad.\n\n"
            "Griffin installs Reliance HJT 715 Wp panels on Magnelis(R) steel, "
            "sized for your home and your EV, with subsidy and net meter "
            "handled for you.\n\n"
            "Message us for a free roof survey and a solar + EV plan.\n\n"
            "Headline: Charge your EV for up to 90% less\n"
            "Card footer: Griffin Energy is a private installer"
        ),
    },
    {
        "library_id": "1681876623343353",
        "library_url": "https://www.facebook.com/ads/library/?id=1681876623343353",
        "page_name": "Griffin Energy",
        "started": "Nov 15, 2026",
        "destination": "WhatsApp (WHATSAPP / wa.me) - Send WhatsApp message",
        "text": (
            "You bought the EV. Now stop paying to fuel it.\n\n"
            "Two extra solar panels on your roof generate enough to drive "
            "about 1,200 km every month. With net metering, that takes the "
            "energy cost of your driving to zero.\n\n"
            "Griffin sizes your rooftop system for your home and your car "
            "together: Reliance HJT 715 Wp panels on Magnelis(R) steel, with "
            "subsidy and net meter handled for you.\n\n"
            "Message us with your EV model for a free roof survey in "
            "Hyderabad.\n\n"
            "Headline: Run your EV on your own roof\n"
            "Card footer: Griffin Energy is a private installer"
        ),
    },
    {
        "library_id": "2928662904181620",
        "library_url": "https://www.facebook.com/ads/library/?id=2928662904181620",
        "page_name": "Griffin Energy",
        "started": "Nov 15, 2026",
        "destination": "WhatsApp (WHATSAPP / wa.me) - Send WhatsApp message",
        "text": (
            "The PM Surya Ghar subsidy of up to Rs.78,000 is scheduled to "
            "close on 31 March 2027.\n\n"
            "Approvals, installation and net metering take weeks, and the "
            "subsidy is paid only after the system is commissioned. The homes "
            "that start now are the ones that make it.\n\n"
            "Griffin installs Reliance HJT 715 Wp panels on Magnelis(R) steel, "
            "and one person handles your subsidy, net meter and loan.\n\n"
            "Message us for a free roof survey in Hyderabad.\n\n"
            "Headline: Rs.78,000 subsidy closes 31 March 2027\n"
            "Card footer: Griffin Energy is a private installer"
        ),
    },
    {
        "library_id": "1159969763254778",
        "library_url": "https://www.facebook.com/ads/library/?id=1159969763254778",
        "page_name": "Griffin Energy",
        "started": "Nov 4, 2026",
        "destination": "WhatsApp (WHATSAPP / wa.me) - Send WhatsApp Message",
        "text": (
            "Your solar panels come with a 30-year warranty. The frame "
            "holding them up usually doesn't.\n\n"
            "Cheap structures start rusting at the cut edges and bolt holes "
            "within a few monsoons. On a terrace, a rusting frame is a "
            "safety problem, not a cosmetic one.\n\n"
            "Every Griffin system stands on Magnelis(R) "
            "zinc-aluminium-magnesium coated steel from AM/NS India, carrying "
            "Reliance HJT panels.\n\n"
            "Free roof survey anywhere in Hyderabad. Written quote in 24 "
            "hours.\n\n"
            "Headline: The steel matters as much as panels\n"
            "Card footer: Griffin Energy is a private installer\n"
            "(Ad Library note: this ad has multiple versions)"
        ),
    },
]

GRIFFIN = {
    "company": "Griffin Energy",
    "legal": "Griffin Energy (private installer, Hyderabad)",
    "city": "Hyderabad, Telangana",
    "website": "https://griffinenergy.in/",
    "ads_only": True,
    "website_audit_run": True,
    "checked_on": READ_ON,
    "generated_at": READ_ON,
    "source": "Meta Ad Library (India, active) + live website fetch, 2026-11-21",
    "ad_count_note": (
        "Caveat: the page's own listing reported '~3 results' in the same "
        "session, so the live count is approximately 3-4; the 4 creatives above "
        "were each opened directly."
    ),
    "ad_library": {
        "meta_own": {
            "found": True,
            "results_count": 4,
            "results_label": "4 live ads (page listing showed ~3 results)",
            "query": "Griffin Energy advertiser page (page ID 1421460234380992), Meta Ad Library, India, active",
            "ads": GRIFFIN_ADS,
        },
        "summary": (
            "4 live Meta ads confirmed on 2026-11-21 on the Griffin Energy page "
            "(page ID 1421460234380992). Three started on 15 Nov 2026 and one "
            "on 4 Nov 2026. All four click to WhatsApp and all four carry the "
            "card footer 'Griffin Energy is a private installer'. The copy "
            "sells an EV-plus-rooftop angle (Rs.2.90 a km at a public charger "
            "vs 29 paise from the roof), the 31 March 2027 subsidy window, and "
            "Reliance HJT 715 Wp modules on Magnelis(R) steel. The website was "
            "read live the same day. Google Ads Transparency records were not "
            "checked in this pass."
        ),
    },
    "funnel": {
        "type": "WhatsApp chat",
        "destination": "WhatsApp (wa.me / 'Send WhatsApp message') on all 4 ads",
        "meaning": (
            "Every live ad sends the click to a WhatsApp chat rather than to "
            "griffinenergy.in. The site already has a free-survey form and a "
            "size-and-subsidy calculator, and none of this spend reaches "
            "either of them - so the click cannot be measured, retargeted or "
            "attributed."
        ),
    },
    "findings": [
        "All 4 live ads click to WhatsApp ('Send WhatsApp message'), never to "
        "griffinenergy.in - so the site's own survey form and its "
        "size-and-subsidy calculator cannot measure, retarget or attribute any "
        "of this spend.",
        "The ads promise 'subsidy and net meter handled for you', while the "
        "site's own FAQ still reads: 'Our registration on the national portal "
        "is in progress. We will show our vendor ID here once it is listed. "
        "Please ask us for the current status before you book.' The ad sells a "
        "service the site says is not yet in place.",
        "Every ad card is stamped 'Griffin Energy is a private installer', but "
        "no ad, and no page, explains what that means for a homeowner's "
        "Rs.78,000 - a disclaimered ad that still promises the subsidy leaves "
        "the buyer to guess.",
        "Three of the four live ads started on the same day (15 Nov 2026) and "
        "all four end at the same WhatsApp number, with no landing page and no "
        "UTM: the four creatives cannot be compared against each other or "
        "against anything downstream.",
        "The site publishes the PM Surya Ghar slab (1 kW Rs.30,000, 2 kW "
        "Rs.60,000, 3 kW and above Rs.78,000) but not one system price, so the "
        "ad's 'subsidy handled' promise cannot be priced in a single click.",
        "Nothing on the site - and nothing in any ad - names a customer, a "
        "review or a completed project count, on a purchase that runs to "
        "lakhs, while competing Hyderabad installers advertise install counts "
        "and reviews in the first line of the ad.",
    ],
    "next_steps": [
        ("Send at least one ad to griffinenergy.in, not only to WhatsApp",
         "The site already has the better funnel - a free-survey form and a "
         "subsidy calculator. Put a Meta Pixel and UTMs on it and point one "
         "creative there so the click becomes measurable and retargetable."),
        ("Publish the PM Surya Ghar vendor status, or stop implying it",
         "The FAQ says the portal registration is in progress. Until the "
         "vendor ID is listed, say in the ad exactly how the Rs.78,000 is "
         "claimed and by whom - the current copy reads as though Griffin "
         "claims it on the customer's behalf."),
        ("Put one worked price on the landing page",
         "The subsidy slab is published but no system price is. Show one "
         "worked example - 3 kWp, on-roof, net of subsidy, with the EMI - so "
         "the ad's promise can be priced without a phone call."),
        ("Add the proof the ads are missing",
         "One named Hyderabad install, one review, one kW figure. Griffin's "
         "technical story (Reliance HJT, Magnelis(R) steel) is stronger than "
         "most competitors'; the ad currently pairs it with no evidence that "
         "anyone has bought it."),
    ],
    "contact_facts": [
        ("Phone / WhatsApp", "+91 91605 55540"),
        ("Email", "info@griffinenergy.in"),
        ("Registered office",
         "17-1-386/SN/5/A, SN Reddy Nagar, Champapet, Vaishalinagar, "
         "Saroornagar, Hyderabad 500079, Telangana"),
        ("Facebook page", "https://www.facebook.com/Griffin.Energy/"),
        ("Page ID (Ad Library)", "1421460234380992"),
        ("Website", "https://griffinenergy.in/"),
        ("PM Surya Ghar status", "Site FAQ: registration on the national "
                                 "portal 'in progress' as of 2026-11-21"),
    ],
    "contact": {
        "phone": "+91 91605 55540",
        "email": "info@griffinenergy.in",
    },
    "site_audit": GRIFFIN_SITE,
    "audit_date": READ_ON,
    "site_evidence": {
        "pixel": None,
        "utm": False,
        "checked_on": READ_ON,
        "note": (
            "Head HTML not captured through the sandbox fetch channel; pixel "
            "presence is not checked, not asserted absent. No UTM parameters "
            "appear on any link in the rendered page content, and the ads "
            "themselves land on wa.me, which carries no campaign parameters."
        ),
    },
    "promise_gap": [
        {
            "promise": "'Subsidy and net meter handled for you' (3 of 4 ads)",
            "site": (
                "The site FAQ says the PM Surya Ghar registration is 'in "
                "progress' and asks the buyer to check the current status "
                "before booking. The ad makes the same service sound settled."
            ),
        },
        {
            "promise": "Rs.78,000 subsidy 'closes 31 March 2027'",
            "site": (
                "The site says the scheme 'is currently funded until 31 March "
                "2027'. The ad turns a funding window into a hard closing "
                "date - a claim a cautious buyer will check, and the page does "
                "not back it."
            ),
        },
        {
            "promise": "'Quoted in 24 hours. Installed in one day.'",
            "site": (
                "The site repeats both, but qualifies the one-day install as "
                "applying 'once your approval comes through' and puts the real "
                "timeline at 6-9 weeks. The ad drops the qualification."
            ),
        },
    ],
}


# ---------------------------------------------------------------------------
# 2. NOVA SOLAR SOLUTIONS (Secunderabad / Hyderabad)
# ---------------------------------------------------------------------------
# Website read live 2026-11-21: https://www.novasolar.in/ (two chunks).
# Title "Nova Solar Solutions". H1 "Powering a Sustainable Future with Smart
# Solar Energy". Claims: 'Govt Approved Installer', ISO 9001-2015, MNRE
# empanelled, NSIC registered, 10+ years. Phones +91 9866789995 /
# +91 8121172525 / 040-35697836, WhatsApp wa.me/919866789995,
# info@novasolar.in, Plot No.7, All Saints Road, near LIC Office,
# Tirumalagiri, Secunderabad 500015.
# The site publishes a full 1-10 kW price table (3 kW: gross Rs.2,05,000,
# subsidy Rs.78,000, net Rs.1,27,000), a panel-cleaning price list and an
# FAQ. Hero tile says "25yr Panel Warranty"; the PM Surya Ghar section says
# "Solar module performance warranty of 30 years". Hero and service images are
# hot-linked from images.unsplash.com, one captioned "Nova Solar team
# installing solar panels".

NOVA_SITE = {
    "ssl": True,
    "load_time_seconds": None,
    "final_url": "https://www.novasolar.in/",
    "audit_date": READ_ON,
    "pixels": unknown_pixels(),
    "conversion": {
        "has_contact_form": True,          # 'Request Free Consultation' form
        "has_phone_click": True,           # tel:+919866789995 etc.
        "has_whatsapp_link": True,         # wa.me/919866789995
        "has_cta_buttons": 11,             # 2 hero CTAs + Book a Cleaning Slot + 8 'Get Quote'
        "has_live_chat": False,
        "has_popup_optin": False,
        "has_testimonials": False,         # no customer quote/review section on the page
        "has_pricing_page_link": False,    # full price table, but no linked pricing page
    },
    "seo": {
        "has_title": True,
        "title_text": "Nova Solar Solutions",
        "title_length": 20,
        "has_meta_description": None,
        "meta_desc_length": None,
        "h1_count": 1,
        "h1_text": "Powering a Sustainable Future with Smart Solar Energy",
        "has_og_tags": None,
        "has_schema": None,
        "has_favicon": None,
        "image_count": None,
        "images_without_alt": None,
    },
    "pagespeed": {"error": PAGESPEED_ERROR},
    "page_count": {"has_sitemap": None},
    "local_signals": {"has_google_maps_embed": None},
    "platform": "Static single-page site (anchor sections #contact / #subsidy); stock Unsplash imagery hot-linked",
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

NOVA_ADS = [
    {
        "library_id": "2179943109395424",
        "library_url": "https://www.facebook.com/ads/library/?id=2179943109395424",
        "page_name": "Nova Solar",
        "started": "Nov 16, 2026",
        "destination": "Facebook lead form (FB.ME) - Sign up",
        "text": (
            "THIS FESTIVE SEASON, BRING HOME THE POWER OF THE SUN!\n\n"
            "Celebrate with Nova Solar and enjoy incredible festive benefits!\n\n"
            "Get a 3 kW Solar System at just Rs.1.22 Lakhs!\n\n"
            "And that's not all! Enjoy these EXCLUSIVE FREE BENEFITS:\n"
            "- Free Solar Panel Cleaning Sprinkler Installation\n"
            "- Free Quarterly Chemical Cleaning for 1 Year\n"
            "- Free Solar Panel Insurance for 1 Year\n"
            "- Free Quarterly Preventive Maintenance for 5 Years\n"
            "- Cash Discount up to Rs.10,000!\n\n"
            "Why keep paying high electricity bills when the sun can power "
            "your home?\n\n"
            "Call us today: 9866789995 / 9849639995\n"
            "www.novasolar.in\n\n"
            "Nova Solar - Know the Power of Sun! (T&C Apply)"
        ),
    },
    {
        "library_id": "1166448119664691",
        "library_url": "https://www.facebook.com/ads/library/?id=1166448119664691",
        "page_name": "Nova Solar",
        "started": "Nov 20, 2026",
        "destination": "Facebook lead form (FB.ME) - Sign up",
        "text": (
            "Same festive 3 kW offer as the 16 Nov ad (Rs.1.22 Lakhs, free "
            "sprinkler installation, 1-year chemical cleaning, 1-year panel "
            "insurance, 5-year quarterly preventive maintenance, cash discount "
            "up to Rs.10,000, 9866789995 / 9849639995, www.novasolar.in). "
            "Ad Library note: started 20 Nov 2026, total active time 7 hrs; "
            "creative is a video."
        ),
    },
    {
        "library_id": "2330186101154741",
        "library_url": "https://www.facebook.com/ads/library/?id=2330186101154741",
        "page_name": "Nova Solar",
        "started": "Nov 21, 2026",
        "destination": "Facebook lead form (FB.ME) - Sign up",
        "text": (
            "This festive season, say goodbye to high electricity bills!\n\n"
            "Get 3 kW Solar System at Just Rs.1.22 Lakhs!\n"
            "Get exciting FREE benefits and discounts up to Rs.10,000. "
            "For Hyderabad city only!\n\n"
            "Sign up\n\n"
            "Ad Library note: started 21 Nov 2026, total active time 6 hrs, "
            "Impressions <100 ('Low impression count')."
        ),
    },
]

NOVA = {
    "company": "Nova Solar Solutions",
    "legal": "Nova Solar Solutions (novasolarhyd)",
    "city": "Hyderabad, Telangana",
    "website": "https://www.novasolar.in/",
    "ads_only": True,
    "website_audit_run": True,
    "checked_on": READ_ON,
    "generated_at": READ_ON,
    "source": "Meta Ad Library (India, active) + live website fetch, 2026-11-21",
    "ad_count_note": (
        "Caveat: the page's own listing reported '~4 results' and '~5 results' "
        "on two reads the same day, so the live count is approximately 3-5; the "
        "3 creatives above were each opened directly."
    ),
    "ad_library": {
        "meta_own": {
            "found": True,
            "results_count": 3,
            "results_label": "3 live ads opened directly (page listing showed ~4-5 results)",
            "query": "Nova Solar advertiser page (page ID 707984349075711), Meta Ad Library, India, active",
            "ads": NOVA_ADS,
        },
        "summary": (
            "3 live Meta ads confirmed on 2026-11-21 on the Nova Solar page "
            "(page ID 707984349075711, facebook.com/novasolarhyd): 16 Nov, "
            "20 Nov and 21 Nov 2026. All three run the same festive 3 kW offer "
            "at Rs.1.22 Lakhs, and all three click to a Facebook lead form "
            "(FB.ME 'Sign up'). The page's own ad listing reported approximately "
            "4-5 active results across two reads the same day, so treat this as "
            "3-5 live ads rather than an exact count. The website was read live "
            "the same day. Google Ads Transparency records were not checked in "
            "this pass."
        ),
    },
    "funnel": {
        "type": "Facebook lead form",
        "destination": "Facebook lead form (FB.ME) - 'Sign up' on all 3 ads",
        "meaning": (
            "Every click ends inside a Facebook lead form. Nova Solar's own "
            "consultation form, its published 1-10 kW price table and its "
            "cleaning price list are never reached from paid spend, and no "
            "enquiry can be retargeted or attributed beyond Meta's own "
            "reporting."
        ),
    },
    "findings": [
        "The ad's headline price does not match the site's own price table: "
        "the ads say '3 kW Solar System at just Rs.1.22 Lakhs', while the site "
        "lists 3 kW at Rs.2,05,000 gross, Rs.78,000 subsidy and Rs.1,27,000 "
        "net - Rs.5,000 higher than the ad, before the Rs.10,000 cash "
        "discount the ad also promises.",
        "Two different module warranties are printed on the same page: the "
        "hero tiles say '25yr Panel Warranty', while the PM Surya Ghar "
        "section says 'Solar module performance warranty of 30 years'. The ad "
        "repeats neither, so the buyer could reasonably expect either.",
        "The 21 Nov ad says the offer is 'For Hyderabad city only', while the "
        "site sells 'across Telangana and beyond' from a Secunderabad "
        "(Tirumalagiri) office - the ad narrows the business's own market.",
        "All three ads land on an FB.ME lead form, so the site's consultation "
        "form, 1-10 kW price table and panel-cleaning price list are never "
        "reached from paid traffic and no visitor can be retargeted.",
        "The creative is a stock-photo page: the hero and service images are "
        "hot-linked from images.unsplash.com, including one captioned 'Nova "
        "Solar team installing solar panels' that is not a photograph of the "
        "Nova Solar team.",
        "The site claims 'Govt Approved Installer', MNRE empanelment, ISO "
        "9001-2015 and NSIC registration, but publishes no vendor code, "
        "certificate number or registration ID that a buyer could check - on "
        "a page that asks for a two-lakh decision.",
        "The two newest ads are 6-7 hours old with one under 100 impressions, "
        "so the account is spending too little for these creatives to learn "
        "anything - and the 16 Nov ad has already been superseded twice in "
        "five days.",
    ],
    "next_steps": [
        ("Reconcile Rs.1.22 Lakh with the site's Rs.1,27,000",
         "Either the ad price is pre-discount and the site table is not, or one "
         "of them is wrong. Show the arithmetic on the landing page - gross, "
         "subsidy, cash discount, net, EMI - so the two numbers add up in "
         "front of the buyer."),
        ("Pick one warranty number and use it everywhere",
         "25-year or 30-year, module or performance - not both on one page. "
         "Then put the same figure in the ad, where it is currently missing."),
        ("Put the festive offer on a page Nova owns",
         "Replace the FB.ME form with a landing page carrying the offer, the "
         "price table and the consultation form, with the Meta Pixel and UTMs "
         "- that is what makes the next ad campaign measurable and enables "
         "retargeting."),
        ("Publish the credentials, not the adjectives",
         "MNRE empanelment, ISO 9001-2015 and NSIC registration are checkable. "
         "Print the vendor code, the certificate number and the registration "
         "ID next to the claims."),
        ("Replace the stock photos with your own installs",
         "A stock image captioned as the Nova Solar team is the cheapest thing "
         "to fix and one of the most damaging if a buyer notices. Two or three "
         "real Hyderabad installs with the customer's permission will do more "
         "than any of the six service tiles."),
    ],
    "contact_facts": [
        ("Phone", "+91 9866789995 | +91 8121172525 | 040-35697836"),
        ("Ad creative phones", "9866789995 / 9849639995"),
        ("WhatsApp", "wa.me/919866789995"),
        ("Email", "info@novasolar.in"),
        ("Office", "Plot No.7, All Saints Road, near LIC Office, Tirumalagiri, "
                   "Secunderabad, Telangana 500015"),
        ("Facebook page", "https://www.facebook.com/novasolarhyd/"),
        ("Page ID (Ad Library)", "707984349075711"),
        ("Website", "https://www.novasolar.in/"),
    ],
    "contact": {
        "phone": "+91 9866789995",
        "email": "info@novasolar.in",
    },
    "site_audit": NOVA_SITE,
    "audit_date": READ_ON,
    "site_evidence": {
        "pixel": None,
        "utm": False,
        "checked_on": READ_ON,
        "note": (
            "Head HTML not captured through the sandbox fetch channel; pixel "
            "presence is not checked, not asserted absent. No UTM parameters "
            "appear on any link in the rendered page content, and all three "
            "ads land on fb.me, which cannot carry them."
        ),
    },
    "promise_gap": [
        {
            "promise": "'3 kW Solar System at just Rs.1.22 Lakhs' (all 3 ads)",
            "site": (
                "The site's own table prices 3 kW at Rs.2,05,000 gross, "
                "Rs.78,000 subsidy, Rs.1,27,000 net. The ad is Rs.5,000 below "
                "the site, and neither figure is explained."
            ),
        },
        {
            "promise": "'Free Quarterly Preventive Maintenance for 5 Years'",
            "site": (
                "The site does promise free quarterly preventive maintenance "
                "for 5 years in its FAQ, but the ad also stacks a free "
                "sprinkler install, 1-year chemical cleaning and 1-year "
                "insurance on top - none of which appear in the site's price "
                "table, so there is no way to see what the offer is worth."
            ),
        },
        {
            "promise": "'Cash Discount up to Rs.10,000'",
            "site": (
                "No cash-discount line exists anywhere on the site; the price "
                "table's net column is the subsidy only."
            ),
        },
    ],
}


# ---------------------------------------------------------------------------
# 3. SRI NARAYANA ENTERPRISE SOLAR ENERGIES (Adilabad)
# ---------------------------------------------------------------------------
# No usable website. The ad's own 'Website' line points at
# www.sribalajisolarenergies.com, which is the live site of Sri Balaji Solar
# Energies (Hanumakonda) - a separately branded business - while the company's
# own domain srinarayanasolarenergies.com did not load on 2026-11-21 (https,
# http and /about.html all failed in this pass). No site_audit is attached.

SRI_NARAYANA_ADS = [
    {
        "library_id": "1132334263122838",
        "library_url": "https://www.facebook.com/ads/library/?id=1132334263122838",
        "page_name": "Sri Narayana Enterprise Solar Energies",
        "started": "Nov 13, 2026",
        "destination": "WhatsApp (API.WHATSAPP.COM) - Send WhatsApp Message",
        "text": (
            "INTRODUCING THE PM SURYA GHAR INITIATIVE, EMPOWERING HOUSEHOLDS "
            "WITH CLEAN ENERGY THROUGH ROOFTOP SOLAR SYSTEMS. BENEFIT FROM A "
            "GENEROUS SUBSIDY OF Rs.78,000/-* TO HELP REDUCE RELIANCE ON "
            "CONVENTIONAL ELECTRICITY.\n\n"
            "TAKE ADVANTAGE OF ATTRACTIVE SUBSIDY BENEFITS OF UP TO "
            "Rs.78,000/-*! WITH EASY EMI PLANS STARTING AT JUST Rs.1,355/- FOR "
            "A 3KW SYSTEM.\n\n"
            "SWITCH TO SOLAR TODAY AND ENJOY THE BENEFITS OF A GREENER, "
            "SMARTER HOME.\n\n"
            "House No. 13-8/23, New Housing Board Colony, Adilabad, Telangana "
            "504001 | Call: +91-9490662135 | E-mail: Snepadilabad@gmail.com | "
            "Website: www.sribalajisolarenergies.com | Facebook: "
            "srinarayanaenterprisessolarenergies | Instagram: "
            "srinarayanaenterprises\n\n"
            "Ad Library note: the copy is set in bold Unicode pseudo-letters "
            "(U+1D400 block); reproduced here in plain capitals. The same ad "
            "runs about 9 near-identical creative variants."
        ),
    },
]

SRI_NARAYANA = {
    "company": "Sri Narayana Enterprise Solar Energies",
    "legal": "Sri Narayana Enterprises Solar Energies (Adilabad)",
    "city": "Adilabad, Telangana",
    "website": "",
    "ads_only": True,
    "website_audit_run": False,
    "checked_on": READ_ON,
    "generated_at": READ_ON,
    "source": "Meta Ad Library (India, active), 2026-11-21; own website unreachable",
    "ad_library": {
        "meta_own": {
            "found": True,
            "results_count": 1,
            "results_label": "1 live ad (about 9 near-identical creative variants)",
            "query": "Sri Narayana Enterprise Solar Energies page (page ID 936862456183233), Meta Ad Library, India, active",
            "ads": SRI_NARAYANA_ADS,
        },
        "summary": (
            "1 live Meta ad confirmed on 2026-11-21 on the Sri Narayana "
            "Enterprise Solar Energies page (page ID 936862456183233, started "
            "13 Nov 2026), running about 9 near-identical Telugu/English "
            "creative variants that all carry the same line - 'Subsidy Upto "
            "78,000/-(T&C Apply)' - and all click to WhatsApp. No website audit "
            "was run: the company's own domain srinarayanasolarenergies.com did "
            "not load on the day, and the website the ad itself names is "
            "another firm's site."
        ),
    },
    "funnel": {
        "type": "WhatsApp chat",
        "destination": "WhatsApp (API.WHATSAPP.COM) - 'Send WhatsApp Message' on every variant",
        "meaning": (
            "Every variant of the ad clicks to a WhatsApp chat, and the website "
            "named in the ad belongs to a different company. There is no page of "
            "Sri Narayana's own anywhere in the paid path, so nothing can be "
            "measured, retargeted or corrected once the buyer arrives."
        ),
    },
    "findings": [
        "The ad's own 'Website' line points at www.sribalajisolarenergies.com - "
        "the live site of Sri Balaji Solar Energies in Hanumakonda, a "
        "separately branded business - while the company's own domain "
        "srinarayanasolarenergies.com did not load on 2026-11-21 (https, http "
        "and /about.html all failed in this pass). Ad traffic is being sent to "
        "another firm's website.",
        "About 9 creative variants carry exactly the same offer line - "
        "'Subsidy Upto 78,000/-(T&C Apply)' - with different headlines ('No More "
        "Electricity Bills Tension', 'Cut Off On Your Electricity Bill', 'Power "
        "Up Your Home', 'Invest For Better Future'...). That is nine ads testing "
        "nothing: the same promise, the same creative shape, the same "
        "destination.",
        "The copy is set in bold Unicode pseudo-letters (the mathematical "
        "alphanumeric block, so 'Introducing' renders as pseudo-bold glyphs). "
        "Screen readers and some Android default fonts read those characters "
        "letter by letter or show boxes, and the body is one unbroken bold "
        "block with no line breaks between the offer and the address.",
        "The single live ad runs no price for a specific size, no warranty "
        "term, no panel or inverter brand and no service guarantee - only a "
        "Rs.1,355 EMI for 'a 3KW system' and 'T&C Apply', with no T&C anywhere a "
        "buyer can read.",
        "The contact email on the ad is a personal Gmail address "
        "(snepadilabad@gmail.com) rather than an address on the firm's own "
        "domain, which is the first thing a Rs.1 lakh+ buyer checks and the "
        "easiest thing to lose a lead over.",
        "The ad has been running since 13 Nov 2026 with no landing page and no "
        "site of its own to send the click to, so every enquiry sits in a "
        "WhatsApp thread with no record of which ad produced it.",
    ],
    "next_steps": [
        ("Fix the website line in the ad - today",
         "It currently sends buyers to another company's site. Either point it "
         "at your own domain, or remove the line until your domain resolves."),
        ("Get srinarayanasolarenergies.com back up, or replace it",
         "The domain did not load, so the ad has no owned destination. A "
         "one-page site with the subsidy table, your address and an enquiry "
         "form, plus the Meta Pixel, is enough to start measuring this spend."),
        ("Turn nine identical creatives into three real tests",
         "One price-led ('3 kW at Rs.X, EMI Rs.1,355'), one subsidy-led "
         "('what the Rs.78,000 covers'), one proof-led (installs, warranty, "
         "service area). Same destination, so the winner can actually be "
         "identified."),
        ("Rewrite the copy in normal Telugu text",
         "Bold Unicode pseudo-letters break screen readers and some Android "
         "fonts, and read as spam to the platforms. Plain Telugu with a "
         "headline, three bullets and one CTA will outperform it."),
        ("Move to a domain email address",
         "info@srinarayanasolarenergies.com (once the domain is live) is worth "
         "more than any creative change on a purchase this size."),
    ],
    "contact_facts": [
        ("Phone", "+91 9490 662 135 (as printed: +91-9490662135)"),
        ("Email", "snepadilabad@gmail.com (personal Gmail, per the ad)"),
        ("Address", "House No. 13-8/23, New Housing Board Colony, Adilabad, "
                    "Telangana 504001"),
        ("Facebook page",
         "https://www.facebook.com/srinarayanaenterprisessolarenergies/"),
        ("Page ID (Ad Library)", "936862456183233"),
        ("Instagram", "srinarayanaenterprises"),
        ("Website named in the ad",
         "www.sribalajisolarenergies.com - live, but it is Sri Balaji Solar "
         "Energies' site, not this company's"),
        ("Own domain", "srinarayanasolarenergies.com - did not load "
                       "2026-11-21 (http, https and /about.html all failed)"),
    ],
    "contact": {
        "phone": "+91 9490 662 135",
        "email": "snepadilabad@gmail.com",
    },
    "audit_date": READ_ON,
    "site_evidence": {
        "pixel": None,
        "utm": False,
        "checked_on": READ_ON,
        "note": (
            "No website of this company's own could be read: "
            "srinarayanasolarenergies.com did not load on 2026-11-21, so "
            "pixel and UTM checks were not run and are recorded as not "
            "checked, not as absent."
        ),
    },
    "promise_gap": [
        {
            "promise": "'Subsidy Upto 78,000/-(T&C Apply)' - the only offer line in all 9 variants",
            "site": (
                "There is no page of Sri Narayana's own to state the T&C, the "
                "eligibility rules or the sizes the Rs.78,000 applies to; the "
                "website named in the ad belongs to another company."
            ),
        },
        {
            "promise": "'Easy EMI plans starting at just Rs.1,355/- for a 3KW system'",
            "site": (
                "No lender, tenure, interest rate, down payment or processing "
                "fee is published anywhere the buyer can reach, so the EMI "
                "figure cannot be checked or compared."
            ),
        },
    ],
}


# ---------------------------------------------------------------------------
# 4. AADITHYA SOLAR ENERGIES (Hyderabad, Kismatpur / Gandipet)
# ---------------------------------------------------------------------------
# Website read live 2026-11-21: https://aadithyasolarenergies.com/ (3 chunks)
# and /contact/. WordPress on the commercial 'eergx' theme by ThemeXriver, with
# the theme's demo content still published:
#   * header shows the demo's US number 'Call Us: (229) 555-0109' while the
#     real number +91 9491032828 sits in the footer;
#   * 'explore more', 'Browse all services', 'Get A Fre Quote', several nav
#     items and the service links all point at themexriver.com/wp/eergx/...
#   * body copy: 'We are 100+ professional software engineers... Mobile app
#     easy management', counters 'Busines setup growth' / 'Business Problem
#     Solvingh', prices '$4/Kw on grid' and '17/Kw Hybrid', lorem text;
#   * testimonials are demo names, two of them identical ('Arjun Das,
#     Warangal'), and two 'Join Our Team' blocks repeat on one page;
#   * three addresses across the site; footer email text reads
#     example@email.com while the link is mailto:info@aadithyasolarenergies.com.

AADITHYA_SITE = {
    "ssl": True,
    "load_time_seconds": None,
    "final_url": "https://aadithyasolarenergies.com/",
    "audit_date": READ_ON,
    "pixels": unknown_pixels(),
    "conversion": {
        "has_contact_form": True,          # 'Quick Contact' + contact page form
        "has_phone_click": True,           # tel:+91-9491032828 in the footer
        "has_whatsapp_link": False,        # no wa.me / whatsapp link in the content
        "has_cta_buttons": 12,             # explore more x4, Browse all services,
                                           # Get Now x2, Get A Fre Quote x2, Submit now,
                                           # Request a Quote, Discover More
        "has_live_chat": False,
        "has_popup_optin": False,
        "has_testimonials": True,          # demo testimonials (stock names)
        "has_pricing_page_link": False,    # placeholder '$4/Kw' / '17/Kw', no real price
    },
    "seo": {
        "has_title": True,
        "title_text": "Aadithya Solar Energies",
        "title_length": 23,
        "has_meta_description": None,
        "meta_desc_length": None,
        "h1_count": 9,
        "h1_text": "B u i l d   a   B r i g h t   C a r e e r   i n   "
                   "R e n e w a b l e   E n e r g y",
        "has_og_tags": None,
        "has_schema": None,
        "has_favicon": None,
        "image_count": None,
        "images_without_alt": None,
    },
    "pagespeed": {"error": PAGESPEED_ERROR},
    "page_count": {"has_sitemap": None},
    "local_signals": {"has_google_maps_embed": None},
    "platform": "WordPress on the commercial 'eergx' theme (ThemeXriver), demo content still published",
    "html_errors": None,
    "scope_note": (
        "The website was read live on 2026-11-21 through a rendered-content "
        "fetch of the home page and /contact. Tracking-pixel and head checks "
        "(Meta Pixel, GA4, GTM, Google Ads, meta description, Open Graph, "
        "JSON-LD, favicon) need the raw served HTML and were not captured "
        "through this channel, so they are recorded as not checked rather than "
        "absent. PageSpeed and sitemap were not run."
    ),
}

AADITHYA_ADS = [
    {
        "library_id": "1596852225147259",
        "library_url": "https://www.facebook.com/ads/library/?id=1596852225147259",
        "page_name": "Aadithya Solar Energies",
        "started": "Sep 11, 2026",
        "destination": "Facebook lead form (FB.ME) - Sign up",
        "text": (
            "(Telugu - translated) 'Enter your details for solar subsidy "
            "details up to Rs.78,000.'\n\n"
            "FB.ME card (Telugu - translated): 'Solar with up to Rs.78,000 "
            "subsidy! Your own power plant on your own roof! Through PM Surya "
            "Ghar Muft Bijli Yojana, eligible household consumers can get a "
            "subsidy of up to Rs.78,000*. Rooftop Solar Installation / savings "
            "on electricity bills.'\n\n"
            "Ad Library note: '2 ads use this creative and text'; the page "
            "listing shows ~1 result. Creative is a video."
        ),
    },
]

AADITHYA = {
    "company": "Aadithya Solar Energies",
    "legal": "Aadithya Solar Energies (Hyderabad / Gandipet)",
    "city": "Hyderabad, Telangana",
    "website": "https://aadithyasolarenergies.com/",
    "ads_only": True,
    "website_audit_run": True,
    "checked_on": READ_ON,
    "generated_at": READ_ON,
    "source": "Meta Ad Library (India, active) + live website fetch, 2026-11-21",
    "ad_count_note": (
        "Caveat: one creative has been running since 11 Sep 2026 (71 days at "
        "this audit) with '2 ads use this creative and text' - a single creative "
        "is a single test, so there is nothing to compare it against."
    ),
    "ad_library": {
        "meta_own": {
            "found": True,
            "results_count": 1,
            "results_label": "1 live ad (2 ads use this creative and text)",
            "query": "Aadithya Solar Energies page (page ID 586497644535912), Meta Ad Library, India, active",
            "ads": AADITHYA_ADS,
        },
        "summary": (
            "1 live Meta ad confirmed on 2026-11-21 on the Aadithya Solar "
            "Energies page (page ID 586497644535912): library ID 1596852225147259, "
            "started 11 Sep 2026 - 71 days at the time of this report - with 2 "
            "ads using this creative and text. Telugu copy sells Rs.78,000 "
            "subsidy details and clicks to a Facebook lead form (FB.ME). The "
            "website was read live the same day; it is still running the demo "
            "content of the commercial theme it was built on. Google Ads "
            "Transparency records were not checked in this pass."
        ),
    },
    "funnel": {
        "type": "Facebook lead form",
        "destination": "Facebook lead form (FB.ME) - 'Sign up'",
        "meaning": (
            "The only live ad ends in a Facebook lead form, so the site is never "
            "reached from paid traffic - which is fortunate, because the site's "
            "own buttons send visitors to the theme vendor's demo pages. Nothing "
            "in this funnel can be measured end to end."
        ),
    },
    "findings": [
        "The site's header still shows the theme demo's US phone number - "
        "'Call Us: (229) 555-0109' - while the real number, +91 9491032828, "
        "appears only in the footer. A Hyderabad buyer sees an American "
        "placeholder at the top of the page.",
        "Every 'explore more', 'Browse all services', 'Get A Fre Quote' button "
        "and several navigation and service links point at "
        "themexriver.com/wp/eergx/... - the theme vendor's demo site. The site's "
        "own buttons walk visitors off the domain.",
        "The page is still running its software-agency template: 'We are 100+ "
        "professional software engineers with more than 10 years of experience... "
        "Mobile app easy management', counters labelled 'Busines setup growth', "
        "'Business Problem Solvingh' and 'Commitment to Clean 4%', prices written "
        "as '$4/Kw on grid' and '17/Kw Hybrid', and lorem text ('Every pleasure "
        "is to be welcomed and every pain avoided') under the offer blocks.",
        "The testimonials are demo names from the template and one of them "
        "appears twice ('Arjun Das, Warangal' on two different quotes), while "
        "the 'Join Our Team' recruitment block and the 'We Give Unparalleled "
        "Flexibility' block each appear twice on the same page.",
        "Three different addresses are published: Sy.No.186, near Water Tank, "
        "Kismatpur, Gandipet Mandal, Ranga Reddy 500086 (footer); Plot No.42, "
        "Himayath Sagar, Bandlaguda Jagir, Gandipet Mandal 500086 (contact "
        "page); and 1-284/5 Srikalahasti-Pichatur Road, Srikalahasti, Tirupati, "
        "Andhra Pradesh 517644 (footer).",
        "The only ad has been running since 11 Sep 2026 - 71 days - with 2 ads "
        "on a single creative, pointed at a lead form, while the site it should "
        "be sending people to still carries the header phone of its theme "
        "vendor. On top of that, the ad's form asks for 'solar subsidy "
        "details', but the site has no subsidy page beyond one FAQ line.",
        "The site's 'Quick Contact' form asks the visitor to pick a 'Service "
        "type' from rupee bands ('Less Than 1000 Rs', '1000-2500 Rs'... "
        "'More Than 7500 Rs') - a software-agency pricing dropdown that a solar "
        "buyer cannot answer.",
    ],
    "next_steps": [
        ("Fix the header phone number",
         "Remove '(229) 555-0109' from the header and put +91 9491032828 there. "
         "It is a five-minute change and it is the first thing on the page."),
        ("Repoint every theme link at a real page",
         "'Explore more', 'Browse all services', 'Get A Fre Quote' and the nav "
         "items currently send visitors to themexriver.com. That is free traffic "
         "being handed to the theme vendor."),
        ("Strip the demo content before spending another rupee",
         "Software-agency copy, '$4/Kw' prices, lorem text, duplicate "
         "testimonials and a repeated recruitment block. Replace them with two "
         "real projects, a real price and one form."),
        ("Build the subsidy page the ad promises",
         "The ad sells 'solar subsidy details'. Publish one page: the Rs.78,000 "
         "slab, eligibility, the documents needed and what you handle - then "
         "point the ad there with a Meta Pixel and UTMs."),
        ("Refresh the creative and settle on one address",
         "71 days on one creative with no variation is a wasted learning "
         "budget. And pick the address you actually operate from - the site "
         "currently publishes three."),
    ],
    "contact_facts": [
        ("Phone (real)", "+91 94910 32828 (footer; also tel:+91-9491032828)"),
        ("Phone (header, theme demo)", "(229) 555-0109 - not a Hyderabad number"),
        ("Email", "info@aadithyasolarenergies.com (footer text reads "
                  "example@email.com)"),
        ("Address (footer)", "Sy.No.186, near Water Tank, Kismatpur, Gandipet "
                             "Mandal, Ranga Reddy District, Telangana 500086"),
        ("Address (contact page)", "Plot No.42, Himayath Sagar, Bandlaguda "
                                   "Jagir, Gandipet Mandal, Ranga Reddy "
                                   "District, Telangana 500086"),
        ("Address (AP branch)", "1-284/5 Srikalahasti-Pichatur Road, revenue "
                                "ward 1, Srikalahasti, Tirupati, Andhra Pradesh "
                                "517644"),
        ("Facebook page", "https://www.facebook.com/aadithyasolarenergies/"),
        ("Page ID (Ad Library)", "586497644535912"),
        ("Website", "https://aadithyasolarenergies.com/"),
    ],
    "contact": {
        "phone": "+91 94910 32828",
        "email": "info@aadithyasolarenergies.com",
    },
    "site_audit": AADITHYA_SITE,
    "audit_date": READ_ON,
    "site_evidence": {
        "pixel": None,
        "utm": False,
        "checked_on": READ_ON,
        "note": (
            "Head HTML not captured through the sandbox fetch channel; pixel "
            "presence is not checked, not asserted absent. No UTM parameters "
            "appear on any link in the rendered page content, and the ad lands "
            "on fb.me, which cannot carry them."
        ),
    },
    "promise_gap": [
        {
            "promise": "'Enter your details for solar subsidy details up to Rs.78,000' (the ad's only line, in Telugu)",
            "site": (
                "There is no subsidy page. The Rs.78,000 figure appears once, "
                "inside an FAQ accordion, and nowhere on the enquiry path - so "
                "the ad's promise is answered by a form, not by information."
            ),
        },
        {
            "promise": "'Your own power plant on your own roof' (FB.ME card line, in Telugu)",
            "site": (
                "The site's offer blocks carry '$4/Kw on grid' and '17/Kw "
                "Hybrid' with lorem text underneath - no system size, no total "
                "price, no subsidy-adjusted price that a buyer could act on."
            ),
        },
        {
            "promise": "'Rooftop Solar Installation' (listed benefit in the ad)",
            "site": (
                "Installation is one of four service cards, and every card's "
                "link points at the theme vendor's demo site rather than a page "
                "about the work."
            ),
        },
    ],
}


# ---------------------------------------------------------------------------
# 5. EAGLE SOLAR SYSTEMS (Hyderabad, Bachupally) - NO WEBSITE
# ---------------------------------------------------------------------------
# No website exists for this business: none of the three live ads carries a
# site link, and every click goes to a Facebook lead form. Contact details come
# from the ads themselves and from the TGREDCO empanelled-supplier list
# (eaglesolarhyd@gmail.com, 9000666985; Sy.No-142/A/1, Mallampet, Bachupally,
# Maheshwaram, Medchal-Malkajgiri 502303). IndiaMART lists the firm as
# established 2013 (proprietor Rama Krishnaiah Kumbam). No site_audit.

EAGLE_ADS = [
    {
        "library_id": "2327283458060008",
        "library_url": "https://www.facebook.com/ads/library/?id=2327283458060008",
        "page_name": "Eagle Solar Systems",
        "started": "Nov 21, 2026",
        "destination": "Facebook lead form (FB.ME) - Book now",
        "text": (
            "Planning to Install Solar Panels on Your Rooftop?\n\n"
            "Here's an opportunity to make solar installation more affordable!\n\n"
            "Get up to Rs.78,000 Government Subsidy under PM Surya Ghar Muft "
            "Bijli Yojana, subject to applicable eligibility.\n\n"
            "Choose Eagle Solar System...\n\n"
            "FB.ME card: 'Install Solar & Claim Government Subsidy! - Book Your "
            "Rooftop Solar Installation Today.'\n\n"
            "Ad Library note: started 21 Nov 2026, total active time 7 hrs."
        ),
    },
    {
        "library_id": "1123693900270768",
        "library_url": "https://www.facebook.com/ads/library/?id=1123693900270768",
        "page_name": "Eagle Solar Systems",
        "started": "Nov 19, 2026",
        "destination": "Facebook lead form (FB.ME) - Book now",
        "text": (
            "(Telugu) 'Farmer! Install solar on your house and cut your "
            "electricity costs! Under PM Surya Ghar Muft Bijli Yojana, eligible "
            "households can get up to Rs.78,000 government subsidy. Quality "
            "solar panels. Expert installation. Reduce the burden of electricity "
            "bills. Full solar system support. Want solar on your house? Contact "
            "us today. 9000666985 | 9000666984. Serving Hyderabad and all of "
            "Telangana. *Subsidy eligibility and amount depend on government "
            "rules.*'\n\n"
            "FB.ME card: 'Get up to Rs.78,000 solar subsidy! - Install rooftop "
            "solar on your house with Eagle Solar Systems. Reduce your "
            "electricity bills...'\n\n"
            "Ad Library note: the original opens with the Telugu word "
            "'Raitanna' (addressing a farmer) on a residential rooftop offer."
        ),
    },
    {
        "library_id": "1677382683817329",
        "library_url": "https://www.facebook.com/ads/library/?id=1677382683817329",
        "page_name": "Eagle Solar Systems",
        "started": "Nov 7, 2026",
        "destination": "Facebook lead form (FB.ME) - Book now",
        "text": (
            "(Telugu) 'Spending thousands of rupees on electricity bills every "
            "month? Stop spending your hard-earned money on power bills! Install "
            "solar panels on your house now and get relief from electricity "
            "costs. Eagle Solar Systems special offer: rooftop solar installation "
            "for your home; up to Rs.78,000 government subsidy for eligible "
            "households; save up to 90% on your electricity bill*; PM Surya Ghar "
            "Muft Bijli Yojana benefits. Switch to solar today - take a step "
            "towards tomorrow's savings! Call for details: 9000666985 / "
            "9000666984. Serving Hyderabad and all of Telangana. Eagle Solar "
            "Systems - smart savings with smart energy.'\n\n"
            "FB.ME card: 'Say goodbye to electricity bills! Save with solar! - "
            "Chance to get up to Rs.78,000 government subsidy! Install solar for "
            "your home. Book now'"
        ),
    },
]

EAGLE = {
    "company": "Eagle Solar Systems",
    "legal": "Eagle Solar Systems (TGREDCO empanelled supplier)",
    "city": "Hyderabad, Telangana",
    "website": "",
    "ads_only": True,
    "website_audit_run": False,
    "checked_on": READ_ON,
    "generated_at": READ_ON,
    "source": "Meta Ad Library (India, active), 2026-11-21; no website exists",
    "ad_count_note": (
        "Caveat: the page's own listing reported '~2 results' in the same "
        "session, so the live count is approximately 2-3; the 3 creatives above "
        "were each opened directly."
    ),
    "ad_library": {
        "meta_own": {
            "found": True,
            "results_count": 3,
            "results_label": "3 live ads opened directly (page listing showed ~2 results)",
            "query": "Eagle Solar Systems page (page ID 1462508363606856), Meta Ad Library, India, active",
            "ads": EAGLE_ADS,
        },
        "summary": (
            "3 ad IDs were opened directly on 2026-11-21 and all three returned "
            "an active ad on the Eagle Solar Systems page (page ID "
            "1462508363606856, facebook.com/61595903925834): 2327283458060008 "
            "(21 Nov), 1123693900270768 (19 Nov) and 1677382683817329 (7 Nov). "
            "The page's own listing reported ~2 results in the same session, so "
            "treat the count as approximately 2-3 live ads with three creatives "
            "confirmed. Two are in Telugu and one in English, all sell the "
            "Rs.78,000 PM Surya Ghar subsidy, and all three click to a Facebook "
            "lead form. There is no website for this business, so no site audit "
            "was run."
        ),
    },
    "funnel": {
        "type": "Facebook lead form",
        "destination": "Facebook lead form (FB.ME) - 'Book now' on all 3 ads",
        "meaning": (
            "There is no website and no landing page anywhere in the funnel: "
            "every click ends in a Facebook lead form. Enquiries live in the "
            "Meta inbox, nothing can be retargeted, and there is no page a "
            "buyer can check the firm on before handing over a phone number."
        ),
    },
    "findings": [
        "There is no website at all. None of the three ads carries a site link "
        "and every click ends in a Facebook lead form ('Book now'), so all "
        "enquiry data sits inside Meta and nothing can be retargeted, scored or "
        "followed up outside the inbox.",
        "The 19 Nov Telugu ad opens with 'Raitanna' - the word for a farmer - on "
        "a residential rooftop offer for homeowners, so the first word of the ad "
        "excludes most of the audience it is paying to reach.",
        "All three ads make the same promise ('up to Rs.78,000', 'save up to "
        "90%' with an asterisk) and none of them states a system size, a price, "
        "an EMI or a warranty - a homeowner has nothing to compare and nothing "
        "to act on except calling.",
        "The 21 Nov English ad says 'Choose Eagle Solar System' (singular) "
        "against 'Eagle Solar Systems' everywhere else - the brand name is "
        "wrong in the headline of the newest ad.",
        "The company is on Telangana's TGREDCO empanelled-supplier list "
        "(Sy.No-142/A/1, Mallampet, Bachupally, Maheshwaram, "
        "Medchal-Malkajgiri 502303) - a government credential that appears "
        "nowhere in any ad, in a market where every competitor claims subsidy "
        "help.",
        "There is no page anywhere to verify the business: a buyer searching "
        "the name finds a Facebook page and third-party directory listings, on "
        "a purchase that runs to lakhs.",
    ],
    "next_steps": [
        ("Put up one landing page - before the next ad",
         "A single page with the Rs.78,000 slab, one worked price, the TGREDCO "
         "empanelment, your address, and an enquiry form with the Meta Pixel. "
         "That single page is what makes every future rupee measurable and "
         "retargetable."),
        ("Replace the farmer-opener with a homeowner version",
         "The farmer salutation 'Raitanna' opens a home rooftop ad. The Telugu copy should "
         "open with the homeowner's bill, the way the 7 Nov ad does."),
        ("Put one number in the creative",
         "A system size and a price or EMI (even '3 kW from Rs.X, EMI Rs.Y') "
         "will out-perform 'up to Rs.78,000' on its own, because every "
         "competitor is already saying 'up to Rs.78,000'."),
        ("Lead with the TGREDCO empanelment",
         "It is the strongest trust asset the business owns and it is currently "
         "used in none of the ads. Put it in the creative and on the landing "
         "page, with the supplier list reference."),
    ],
    "contact_facts": [
        ("Phone (ad)", "9000666985 | 9000666984"),
        ("Email (TGREDCO list)", "eaglesolarhyd@gmail.com"),
        ("Address (TGREDCO list)",
         "Sy.No-142/A/1, Mallampet, Bachupally, Maheshwaram, "
         "Medchal-Malkajgiri 502303, Telangana"),
        ("Facebook page", "https://www.facebook.com/61595903925834/"),
        ("Page ID (Ad Library)", "1462508363606856"),
        ("Website", "None - every ad clicks to a Facebook lead form"),
        ("Listed since", "Established 2013 (IndiaMART seller page)"),
        ("Empanelment", "TGREDCO empanelled-supplier list (Telangana)"),
    ],
    "contact": {
        "phone": "9000666985",
        "email": "eaglesolarhyd@gmail.com",
    },
    "audit_date": READ_ON,
    "site_evidence": {
        "pixel": None,
        "utm": False,
        "checked_on": READ_ON,
        "note": (
            "This business has no website, so no pixel or UTM check was "
            "possible. Recorded as not checked rather than absent."
        ),
    },
    "promise_gap": [
        {
            "promise": "'Save up to 90% on your electricity bill*' (7 Nov ad)",
            "site": (
                "The asterisk has no footnote in the ad, and there is no "
                "website where the qualifying conditions could be read."
            ),
        },
        {
            "promise": "'Quality solar panels / expert installation / full system support' (19 Nov ad)",
            "site": (
                "No panel brand, wattage, inverter, warranty term or service "
                "SLA is stated in any ad, and there is no page to check them "
                "against."
            ),
        },
    ],
}


LEADS = [GRIFFIN, NOVA, SRI_NARAYANA, AADITHYA, EAGLE]


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
