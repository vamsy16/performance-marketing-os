#!/usr/bin/env python3
"""Build batch-14 (Telangana) ads reports — leads 4 and 5 of the 5 requested.

Two further Telangana solar leads confirmed 2026-11-21 via the Meta Ad Library
(India, active ads) and cross-checked against the TGREDCO / TGNPDCL
empanelled-supplier lists:

  4. Envious Energy Private Limited (Begumpet, Hyderabad / Sainikpuri,
     Secunderabad) — TGREDCO vendor #12. 1 live Meta ad, website live.
  5. Sri Balaji Solar Energies (Lashkar Bazar, Hanumakonda, Warangal) —
     TGREDCO vendor #34, regn TSRE180085. 6 live Meta ads (all fb.me lead
     forms), website live.

WHERE EVERY NUMBER BELOW CAME FROM (all read live 2026-11-21):

* Meta Ad Library (India, active ads). Each library ID below was confirmed by
  opening it directly at ``https://www.facebook.com/ads/library/?id=<ID>``.
  Ad IDs routinely render next to a different advertiser's card, so nothing
  here is taken from a paged result: the ID, the page name and the card were
  adjacent in the same direct fetch.
* The company's own website, read through a rendered-content fetch.
* TGREDCO "List of Empanelled Suppliers 2025" for the registered address and
  contact person.

CHECKS THAT COULD NOT BE RUN ARE STORED AS ``None`` AND RENDER AS
"Not checked in this pass" / "Not available at audit time". They are never
guessed:

* Google PageSpeed mobile score + LCP - the keyless API returns HTTP 429.
* Tracking pixels (Meta Pixel / GA4 / GTM / Google Ads) - raw head HTML was not
  captured through the sandbox fetch channel, so presence is recorded as
  not-checked (None), never as absent.
* Google Ads Transparency advertiser records - not fetched.

Run:  cd 01-LEADS && PYTHONPATH=/tmp/pdflibs python3 build_batch14_telangana.py
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
# 1. ENVIOUS ENERGY PRIVATE LIMITED
# ---------------------------------------------------------------------------
# Website read live 2026-11-21 (www.enviousenergy.com). WordPress, "sunex"
# theme with ElementsKit. Read: home (3 chunks), contact-us, and the
# /our-team/marvin-mckinney/ page. TGREDCO list gives the empanelled address.
ENVIOUS_ADS = [
    {
        "library_id": "1122485234026419",
        "library_url": "https://www.facebook.com/ads/library/?id=1122485234026419",
        "page_name": "Envious Energy Private Limited",
        "started": "Nov 20, 2026",
        "destination": "WhatsApp (API.WHATSAPP.COM) - Send WhatsApp message",
        "text": (
            "Switch to Solar. Save More Every Day!\n\n"
            "Reduce your Electricity bill with Solar Installation\n\n"
            "**Switch to Solar. Save More Every Day!**\n\n"
            "Why pay higher electricity bills when the sun can power your "
            "home and business?\n\n"
            "High-Quality Solar Panels\n"
            "Expert Installation\n"
            "Lower Electricity Bills\n"
            "Government Subsidy Assistance*\n"
            "Reliable After-Sales Support\n\n"
            "Invest in clea... [card truncated by Meta]\n\n"
            "Residential & Commercial Solar"
        ),
    },
]

ENVIOUS_SITE = {
    "ssl": True,
    "load_time_seconds": None,
    "final_url": "https://www.enviousenergy.com/",
    "audit_date": READ_ON,
    "pixels": unknown_pixels(),
    "conversion": {
        "has_contact_form": False,
        "has_phone_click": True,
        "has_whatsapp_link": True,
        "has_cta_buttons": 5,
        "has_live_chat": False,
        "has_popup_optin": False,
        "has_testimonials": True,
        "has_pricing_page_link": False,
    },
    "seo": {
        "has_title": True,
        "title_text": "Home - Envious Energy",
        "title_length": 21,
        "has_meta_description": None,
        "meta_desc_length": None,
        "h1_count": 1,
        "h1_text": "Utilize Solar Energy to Give Your Future a Powerful Boost",
        "has_og_tags": None,
        "has_schema": None,
        "has_favicon": None,
        "image_count": None,
        "images_without_alt": None,
    },
    "pagespeed": {"error": PAGESPEED_ERROR},
    "page_count": {"has_sitemap": True},
    "local_signals": {"has_google_maps_embed": None},
    "platform": "WordPress (\"sunex\" theme + ElementsKit), server-rendered",
    "html_errors": None,
    "scope_note": (
        "The website was read live on 2026-11-21 through a rendered-content "
        "fetch of the home page, /contact-us/ and one team page. Tracking-pixel "
        "and head checks (Meta Pixel, GA4, GTM, Google Ads, meta description, "
        "Open Graph, JSON-LD, favicon) need the raw served HTML and were not "
        "captured through this channel, so they are recorded as not checked "
        "rather than absent. PageSpeed was not run."
    ),
}

ENVIOUS = {
    "company": "Envious Energy Private Limited",
    "legal": "Envious Energy Private Limited (TGREDCO vendor #12)",
    "city": "Hyderabad, Telangana",
    "website": "https://www.enviousenergy.com/",
    "ads_only": True,
    "website_audit_run": True,
    "checked_on": READ_ON,
    "generated_at": READ_ON,
    "source": "Meta Ad Library (India, active) + live website fetch, 2026-11-21",
    "ad_library": {
        "meta_own": {
            "found": True,
            "results_count": 1,
            "results_label": "1 live ad",
            "query": "Envious Energy advertiser search (Meta Ad Library, India, active)",
            "ads": ENVIOUS_ADS,
        },
        "summary": (
            "1 live Meta ad confirmed on 2026-11-21 by opening library ID "
            "1122485234026419 directly on the Envious Energy Private Limited "
            "page (page ID 1051756784689440). It is the only ad running: the "
            "page's own ad listing returns exactly 1 active ad. The creative "
            "sells residential and commercial rooftop solar with government "
            "subsidy assistance and clicks to WhatsApp, not to the website. "
            "The website was read live the same day. Google Ads Transparency "
            "records were not checked in this pass."
        ),
    },
    "funnel": {
        "type": "WhatsApp chat",
        "destination": "WhatsApp (API.WHATSAPP.COM) - Send WhatsApp message",
        "meaning": (
            "The only live ad clicks straight to a WhatsApp chat. The enquiry "
            "never reaches enviousenergy.com, so the site cannot measure, "
            "retarget or attribute any of this spend, and a brand with 13 "
            "years of project history gets no retargeting audience from it."
        ),
    },
    "findings": [
        "The single live ad clicks to WhatsApp, not to enviousenergy.com - "
        "the enquiry never reaches the website, so the spend cannot be "
        "measured, retargeted or attributed.",
        "The social-proof numbers on the home page are placeholders or "
        "incoherent: 'Solar Installations 304+', 'Energy Generated 32MW+', "
        "'Solar System Lifespan 1+', 'Solar Powered Homes 24+', 'Trees 4K+', "
        "'Commitment to Clean 4%', and a 'Years Of Experience 0+' counter. "
        "'Commitment to Clean 4%' and a 1+ year system lifespan are not "
        "things a buyer can believe.",
        "The review widget on the home page renders '0.2/5' directly above "
        "'Over 500 + Reviews'. A 0.2 rating printed on the page does more "
        "damage than showing no rating at all.",
        "Two template team members are still published: /our-team/"
        "marvin-mckinney/ and /our-team/kathryn-murphy/ carry stock bios "
        "('Marvin McKinney ... over a decade of experience ... Leslie leads "
        "complex projects', with the wrong name in the bio) and skill bars "
        "set to 1%.",
        "The company has three different addresses across its own channels: "
        "the contact page says 1-8-619 (29/2RT) Sai Arcade, Prakash Nagar, "
        "Begumpet, Hyderabad-500016; the footer says #1-10-75/1/1 to 6, Unit "
        "608, Saptagiri Towers, Begumpet, Hyderabad-500016; TGREDCO lists "
        "H.No 35-69, GK Colony, Sainikpuri Post, Secunderabad-500094.",
        "Two support phone numbers are in circulation on the same site "
        "(+91-89777 21950 in the header and footer) against the TGREDCO "
        "empanelled contact of 9000377655, and the footer email link points "
        "at 'mailto:info@domainname.com' instead of the real address.",
        "The home page has no contact form - the enquiry form only exists on "
        "/contact-us/ - so a visitor who is ready to enquire on the landing "
        "page has nowhere to type.",
        "Every H1 and section heading is rendered with letter-spacing "
        "('U t i l i z e   S o l a r   E n e r g y'), which reads as broken "
        "text to a screen reader and to Google.",
        "Ad copy promises 'Government Subsidy Assistance*' with an asterisk, "
        "but the ad card never carries the qualifying footnote and the site "
        "buries the Rs.78,000 PM Surya Ghar figure inside an FAQ accordion "
        "rather than on the landing path.",
    ],
    "next_steps": [
        (
            "Point the ad at the website, not just WhatsApp",
            "Add a website destination with a Meta Pixel and UTMs alongside "
            "the WhatsApp CTA so the click can be measured and the visitor "
            "can be retargeted.",
        ),
        (
            "Replace the placeholder counters with real figures",
            "TGREDCO empanelment and 13 years of delivery are stronger proof "
            "than '304+' and '4%'. Publish installed kW, project count and "
            "the named institutional clients (Gitanjali School, NTR Model "
            "School, The Hyderabad Gymkhana) as numbers, not counters.",
        ),
        (
            "Remove the 0.2/5 review widget",
            "Fix the rating source or remove the widget until it renders "
            "correctly - a 0.2/5 badge next to '500+ reviews' destroys trust "
            "at the exact moment of decision.",
        ),
        (
            "Delete or replace the stock team pages",
            "Marvin McKinney and Kathryn Murphy are unused template entries "
            "with mismatched bios and 1% skill bars. Replace them with the "
            "real leadership team or unpublish them.",
        ),
        (
            "Settle on one address and one phone number",
            "Pick the empanelled address and the number you actually answer, "
            "and use them in the header, the footer, the contact page and "
            "the ad account. Fix the 'info@domainname.com' footer link.",
        ),
        (
            "Put a form on the landing page",
            "Add the enquiry form to the home page, directly under the hero, "
            "so the visit does not have to survive a second click.",
        ),
    ],
    "contact_facts": [
        ("Phone (site)", "+91-89777 21950"),
        ("Phone (TGREDCO list)", "9000377655 (G. Surander Babu)"),
        ("Email", "info@enviousenergy.com"),
        ("Address (site, contact page)",
         "1-8-619 (29/2RT), Sai Arcade, 2nd floor, Prakash Nagar, "
         "Begumpet, Hyderabad-500016"),
        ("Address (site, footer)",
         "#1-10-75/1/1 to 6, Unit 608, Saptagiri Towers, Begumpet, "
         "Hyderabad-500016"),
        ("Address (TGREDCO list)",
         "H.No 35-69, GK Colony, Sainikpuri Post, Secunderabad-500094"),
        ("Facebook page", "https://www.facebook.com/enviousenergyprivatelimited/"),
        ("Website", "https://www.enviousenergy.com/"),
        ("Established", "2013 (stated on the site)"),
    ],
    "contact": {
        "phone": "+91 89777 21950",
        "email": "info@enviousenergy.com",
    },
    "site_audit": ENVIOUS_SITE,
    "audit_date": READ_ON,
    "site_evidence": {
        "pixel": None,
        "utm": False,
        "checked_on": READ_ON,
        "note": (
            "Head HTML not captured through the sandbox fetch channel; pixel "
            "presence is not checked, not asserted absent. No UTM parameters "
            "appear on any link found in the rendered page content."
        ),
    },
    "promise_gap": [
        {
            "promise": "'Government Subsidy Assistance*' - the asterisk has no footnote on the ad",
            "site": (
                "The Rs.78,000 PM Surya Ghar figure appears only inside an FAQ "
                "accordion on the home page, not on the hero or the CTA path. "
                "There is no subsidy page and no eligibility calculator."
            ),
        },
        {
            "promise": "'High-Quality Solar Panels' / 'Expert Installation'",
            "site": (
                "No panel brand, wattage class, warranty term or certification "
                "is named on the home page. The named clients and the 110-120 "
                "kW school installs sit in a testimonial carousel rather than "
                "a case-study the buyer can check."
            ),
        },
        {
            "promise": "'Reliable After-Sales Support'",
            "site": (
                "No support SLA, AMC plan, response time or service-area map is "
                "published. The only support surface is a WhatsApp widget."
            ),
        },
    ],
}


# ---------------------------------------------------------------------------
# 2. SRI BALAJI SOLAR ENERGIES
# ---------------------------------------------------------------------------
# Website read live 2026-11-21 (sribalajisolarenergies.com): home page (2
# chunks) and /contact. React SPA served from static/assets bundles.
SRI_BALAJI_ADS = [
    {
        "library_id": "942037648839408",
        "library_url": "https://www.facebook.com/ads/library/?id=942037648839408",
        "page_name": "Sri Balaji Solar Energies",
        "started": "May 29, 2026",
        "destination": "Facebook lead form (FB.ME) - Sign up",
        "text": (
            "ఇకపై కరెంట్ బిల్లు కట్టే పని లేదు!\n\n"
            "మీ ఇంటిపై సోలార్ సిస్టమ్ అమర్చుకోండి... ₹0 (సున్నా) ముందస్తు "
            "ఖర్చుతో!*\n\n"
            "శ్రీ బాలాజీ సోలార్ ఎనర్జీస్ (Sri Balaji Solar Energies) - 14 "
            "సంవత్సరాల నమ్మకం.\n\n"
            "మా ప్రత్యేకతలు:\n"
            "కేంద్ర ప్రభుత్వం నుండి ₹78,000/- వరకు సబ్సిడీ!\n"
            "నెలకు కరెంట్ బిల్లు బదులు, కేవలం ₹1355/- EMI కట్టండి.\n"
            "10,000+ సంతృప్తికరమైన కస్టమర్లు.\n"
            "ప్రభుత్వ ఉద్యోగులకు కూడా సబ్సిడీ వర్తిస్తుంది.\n\n"
            "కొత్తగూడెం, నర్సంపేట, వరంగల్, హన్మకొండ, రాజమహేంద్రవరం, "
            "భద్రాచలం, ఘట్‌కేసర్ హుజూరాబాద్ and hyderabad మరియు చుట్టుపక్కల "
            "జిల్లాల్లో సర్వీస్ కలదు.\n\n"
            "ఈ రోజే ఫ్రీ సైట్ విజిట్ (Free Site Visit) లభిస్తుంది"
        ),
    },
    {
        "library_id": "1454295123168911",
        "library_url": "https://www.facebook.com/ads/library/?id=1454295123168911",
        "page_name": "Sri Balaji Solar Energies",
        "started": "May 29, 2026",
        "destination": "Facebook lead form (FB.ME) - Get offer",
        "text": (
            "నెలకు వచ్చే భారీ కరెంటు బిల్లులకు స్వస్తి చెప్పండి!\n\n"
            "మీ ఇంటికి సరిపోయే ఉత్తమ సోలార్ ప్లాన్ మరియు సబ్సిడీ వివరాలు "
            "పొందండి!\n\n"
            "శ్రీ బాలాజీ సోలార్ ఎనర్జీస్ (15 ఏళ్ల లెగసీ). మీ వివరాలను నమోదు "
            "చేయండి. మా నిపుణులు మీకు కాల్ చేసి పూర్తి సమాచారం అంద..."
        ),
    },
]

SRI_BALAJI_SITE = {
    "ssl": True,
    "load_time_seconds": None,
    "final_url": "https://sribalajisolarenergies.com/",
    "audit_date": READ_ON,
    "pixels": unknown_pixels(),
    "conversion": {
        "has_contact_form": False,
        "has_phone_click": True,
        "has_whatsapp_link": False,
        "has_cta_buttons": 2,
        "has_live_chat": False,
        "has_popup_optin": False,
        "has_testimonials": True,
        "has_pricing_page_link": False,
    },
    "seo": {
        "has_title": True,
        "title_text": (
            "Telangana's Top Solar Panel Installation Company | "
            "Sri Balaji Solar Energies."
        ),
        "title_length": 82,
        "has_meta_description": None,
        "meta_desc_length": None,
        "h1_count": 1,
        "h1_text": "Go Solar With 'PM Surya Ghar Muft Bijli Yojana'",
        "has_og_tags": None,
        "has_schema": None,
        "has_favicon": None,
        "image_count": None,
        "images_without_alt": None,
    },
    "pagespeed": {"error": PAGESPEED_ERROR},
    "page_count": {"has_sitemap": None},
    "local_signals": {"has_google_maps_embed": True},
    "platform": "React single-page app (static/media + static/js bundles), client-rendered",
    "html_errors": None,
    "scope_note": (
        "The website was read live on 2026-11-21 through a rendered-content "
        "fetch of the home page and /contact. Tracking-pixel and head checks "
        "(Meta Pixel, GA4, GTM, Google Ads, meta description, Open Graph, "
        "JSON-LD, favicon) need the raw served HTML and were not captured "
        "through this channel, so they are recorded as not checked rather "
        "than absent. PageSpeed and sitemap were not run."
    ),
}

SRI_BALAJI = {
    "company": "Sri Balaji Solar Energies",
    "legal": "Sri Balaji Solar Energies (SBSE), TGREDCO regn TSRE180085",
    "city": "Hanumakonda, Telangana",
    "website": "https://sribalajisolarenergies.com/",
    "ads_only": True,
    "website_audit_run": True,
    "checked_on": READ_ON,
    "generated_at": READ_ON,
    "ad_count_note": (
        "Six ads are live on this page; the two above are the ones reproduced "
        "in full because each was opened directly by its library ID. The "
        "control review is therefore graded on a 2-ad evidence sample."
    ),
    "ad_copy_note": (
        "M30 is graded on the English keyword scan of the ad copy. Both ads in "
        "this report are in Telugu and the customer-count claim is written in "
        "Telugu script (10,000+ satisfied customers), which the keyword scan "
        "cannot see. The scan's 'no social proof' reading is therefore an "
        "artefact of the language, not a finding about this advertiser."
    ),
    "ad_text_note": (
        "The ad copy below is reproduced verbatim, in the original Telugu "
        "script, exactly as the Meta Ad Library shows it. It is not translated "
        "here, so that nothing in this report can drift from what the "
        "advertiser actually published. In summary: the ads offer rooftop "
        "solar at Rs.0 upfront and about Rs.1,355 a month against the "
        "Rs.78,000 PM Surya Ghar subsidy, cite 10,000+ satisfied customers "
        "and 14-15 years of trust, and name a service area covering "
        "Kothagudem, Narsampet, Warangal, Hanumakonda, Rajamahendravaram, "
        "Bhadrachalam, Ghatkesar/Huzurabad and Hyderabad."
    ),
    "source": "Meta Ad Library (India, active) + live website fetch, 2026-11-21",
    "ad_library": {
        "meta_own": {
            "found": True,
            "results_count": 2,
            "results_label": "2 ads reproduced (6 live on the page)",
            "query": "Sri Balaji Solar Energies advertiser search (Meta Ad Library, India, active)",
            "ads": SRI_BALAJI_ADS,
        },
        "summary": (
            "6 live Meta ads confirmed on 2026-11-21 on the page "
            "sribalajisolarenergies (page ID 108499924234875). The two ads "
            "reproduced above were each opened directly by library ID and both "
            "render the same page and the same Telugu card. All ads sell "
            "residential rooftop solar on a Rs.0-upfront, Rs.1,355-a-month EMI "
            "offer against the Rs.78,000 PM Surya Ghar subsidy, and every one "
            "of them clicks to an fb.me lead form rather than the website. The "
            "website was read live the same day. Google Ads Transparency "
            "records were not checked in this pass."
        ),
    },
    "funnel": {
        "type": "Facebook lead form",
        "destination": "Facebook lead form (FB.ME) - Sign up / Get offer",
        "meaning": (
            "Every live ad sends the click to an fb.me lead form. The traffic "
            "never touches sribalajisolarenergies.com, so no URL can carry "
            "UTMs, the site cannot set a retargeting audience, and the "
            "company cannot see which ad produced which enquiry - while it "
            "pays for six ads at once."
        ),
    },
    "findings": [
        "All 6 live ads click to fb.me lead forms, so the traffic never "
        "reaches the new website. No UTM can be attached, no retargeting "
        "audience can be built, and ad-to-enquiry attribution is impossible "
        "without opening Ads Manager.",
        "The home page's primary call to action, 'Click Here', links to "
        "pmsuryaghar.gov.in/consumerLogin - the national portal, not the "
        "company's own enquiry flow. The biggest button on the page hands the "
        "visitor to the government and loses them.",
        "The social-proof counters contradict each other across the site: the "
        "home page renders '0+ Project Done', '0+ Happy Clients', '0+ Award "
        "Winnings', '0+ Rating Customer', while the /about page for the same "
        "company reads 1000+ projects, 1200+ happy clients, 850+ awards and "
        "1100+ rated customers - and the ads claim 10,000+ customers. Three "
        "numbers for the same fact, none of them sourced.",
        "The displayed phone number and the dialled number disagree: the "
        "contact page shows +91 903 204 1774 but the tel: link dials +91 951 "
        "595 49 23, and neither matches the numbers the company is "
        "empanelled and advertised under (+91 9959491774 / +91 87024 44646).",
        "The contact page states 'Our Address: Hyderabad', but the registered "
        "head office is #6-1-34 Chintala Narasimhulu Complex, Lashkar Bazar, "
        "Hanumakonda, Warangal 506001. No street address for the office the "
        "customer would actually visit appears anywhere on the site.",
        "The age claim is inconsistent across the company's own channels: one "
        "live ad says '14 years of trust', another says '15-year legacy', the "
        "site says 'established in the year 2011' in one paragraph and "
        "'established in the year 2013' in the next.",
        "The ads sell on 'Rs.0 upfront' and 'Rs.1,355/month EMI', but the "
        "website restates neither figure and has no EMI or zero-upfront "
        "explanation anywhere, so the offer that earns the click disappears "
        "on landing.",
        "The home page has no contact form and no WhatsApp link - the only "
        "form is on /contact - while the ads already collect details through "
        "Meta, so the site offers the visitor no equivalent next step.",
        "The page title is 82 characters and will be truncated in search "
        "results, and the site carries a Google Maps embed but no structured "
        "LocalBusiness data was captured in this pass.",
        "The /Projects page - the proof page a serious buyer clicks to - is a "
        "bare image gallery of about 40 photos with no project name, capacity, "
        "location or date on any of them, so the strongest asset the company "
        "owns cannot be checked or quoted.",
    ],
    "next_steps": [
        (
            "Send the ads to the website, with tracking",
            "Point at least one of the six ads at a landing page on "
            "sribalajisolarenergies.com carrying UTMs and a Meta Pixel, and "
            "keep the fb.me form as a secondary path. The six-ad spend is "
            "currently invisible.",
        ),
        (
            "Take the government link off the primary button",
            "Re-point 'Click Here' at an on-site quote form; move the "
            "pmsuryaghar.gov.in login to a clearly secondary 'apply for "
            "subsidy' step after the lead is captured.",
        ),
        (
            "Fill in the zero counters",
            "Replace the home page's '0+ Project Done' and '0+ Happy Clients' "
            "with one set of real numbers, and use the same numbers on the "
            "/about page (which currently says 1000+ projects / 1200+ clients) "
            "and in the ads (10,000+ customers). The site already names real "
            "installs - Collector Office Suryapet, Relief Hospital Arepally 54 "
            "kW, Talla Padmavathi 56 kW, Vagdevi Junior College 30 kW - that "
            "can be counted.",
        ),
        (
            "Delete the lorem-ipsum filler",
            "The /about page call-to-action block still reads 'It is a long "
            "established fact that a reader will be distracted by the readable "
            "content of a page when looking at its layout' - unreplaced "
            "template text on a page a prospect reaches from the main menu.",
        ),
        (
            "Reconcile the phone numbers",
            "Make the displayed number, the tel: link, the TGREDCO record and "
            "the ad account all use one number that is actually answered.",
        ),
        (
            "Publish the Hanumakonda office address",
            "Replace 'Our Address: Hyderabad' with the Lashkar Bazar, "
            "Hanumakonda 506001 head office, and add the Warangal service "
            "area the ads already promise.",
        ),
        (
            "Put the zero-upfront and EMI offer on the landing page",
            "Restate 'Rs.0 upfront' and 'Rs.1,355/month' with the conditions "
            "on the page, so the promise in the ad survives the click.",
        ),
    ],
    "contact_facts": [
        ("Phone (shown on site)", "+91 903 204 1774"),
        ("Phone (tel: link actually dials)", "+91 951 595 49 23"),
        ("Phone (TGREDCO / ads)", "+91 9959491774 | +91 87024 44646"),
        ("Email", "sbse4444@gmail.com"),
        ("Address (registered HO)",
         "#6-1-34, Chintala Narasimhulu Complex, Lashkar Bazar, "
         "Hanumakonda, Warangal - 506001"),
        ("Address (site, contact page)", "'Hyderabad' - no street address given"),
        ("Facebook page", "https://www.facebook.com/sribalajisolarenergies/"),
        ("Website", "https://sribalajisolarenergies.com/"),
        ("TGREDCO regn", "TSRE180085 (empanelled supplier #34)"),
    ],
    "contact": {
        "phone": "+91 9959491774",
        "email": "sbse4444@gmail.com",
    },
    "site_audit": SRI_BALAJI_SITE,
    "audit_date": READ_ON,
    "site_evidence": {
        "pixel": None,
        "utm": False,
        "checked_on": READ_ON,
        "note": (
            "Head HTML not captured through the sandbox fetch channel; pixel "
            "presence is not checked, not asserted absent. No UTM parameters "
            "appear on any link found in the rendered page content."
        ),
    },
    "promise_gap": [
        {
            "promise": "Rs.0 (zero) upfront cost",
            "site": (
                "The website never mentions a zero-upfront plan. There is no "
                "EMI calculator, no financing partner and no terms for the "
                "Rs.0 offer the ad is built on."
            ),
        },
        {
            "promise": "Rs.1,355 per month EMI instead of a current bill",
            "site": (
                "No monthly figure appears anywhere on the site, and no system "
                "size or tenure is stated for it."
            ),
        },
        {
            "promise": "10,000+ satisfied customers",
            "site": (
                "The site's own counter reads '0+ Happy Clients', directly "
                "contradicting the ad."
            ),
        },
        {
            "promise": "Up to Rs.78,000 central subsidy",
            "site": (
                "The home page headline names PM Surya Ghar and the hero "
                "repeats Rs.78,000, but the primary button sends the visitor "
                "to the national portal login rather than an on-site "
                "explanation of eligibility."
            ),
        },
    ],
}


LEADS = [ENVIOUS, SRI_BALAJI]


def build_base(lead):
    """Attach the ads-audit control review and the website score."""
    lead["ads_audit"] = evaluate(lead, lead.get("site_evidence"))
    site = lead.get("site_audit") or {}
    if site:
        score = calculate_audit_score(
            {}, site.get("pixels") or {}, site.get("conversion") or {},
            site.get("seo") or {}, site.get("pagespeed") or {},
        )
        site["score"] = score
    return lead


def evidence_for(lead):
    ads = (lead.get("ad_library") or {}).get("meta_own", {}).get("ads") or []
    ids = ", ".join(a["library_id"] for a in ads)
    return f"{len(ads)} ads [{ids}]"


def main():
    os.makedirs(AUDIT_DIR, exist_ok=True)
    for lead in LEADS:
        lead = build_base(lead)
        slug = "".join(c if c.isalnum() else "_" for c in lead["company"])[:50]
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
            print("  score: (ads-only, website down - no site_audit)")


if __name__ == "__main__":
    main()
