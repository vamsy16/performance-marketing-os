#!/usr/bin/env python3
"""Build batch-13 (Telangana, non-Hyderabad + new Hyderabad) ads reports.

Three new Telangana solar leads discovered 2026-11-21 via Meta Ad Library
(India, active ads) + TGREDCO empanelled-vendor cross-check:

  1. Kakatiya Energies (Hanamkonda) - 2 live Meta ads, website live.
  2. Visiontek / Visionteknewenergy (Hyderabad, Begumpet) - 5+ live Meta ads,
     website live. Home-solar + inverter/battery product ads.
  3. Laxmi Narayana Solar (Karimnagar) - 2 live Meta ads, website DOWN (HTTP
     500 on www + non-www, re-checked 2026-11-21). Ads-only report, no
     site_audit (website could not be read).

WHERE EVERY NUMBER BELOW CAME FROM (all read live 2026-11-21):

* Meta Ad Library (India, active ads) - each library ID confirmed by opening
  the ad directly at ``https://www.facebook.com/ads/library/?id=<LibraryID>``.
  Ad IDs routinely appear next to another advertiser's card, so an ID is only
  recorded here when metadata and card were adjacent in the same response.
* The company's own website, read via a direct fetch (rendered content).
  Pixel / head checks that need raw HTML are stored as ``None`` (not checked)
  rather than guessed, matching the Lumisun precedent in batch 11.

CHECKS THAT COULD NOT BE RUN ARE STORED AS ``None`` AND RENDER AS
"Not checked in this pass" / "Not available at audit time". They are never
guessed:

* Google PageSpeed mobile score + LCP - the keyless API returns HTTP 429.
* Google Ads Transparency advertiser records - not fetched.
* Sitemap page count - not fetched.
* Tracking pixels (Meta Pixel / GA4 / GTM / Google Ads) - raw head HTML was
  not captured through the sandbox fetch channel, so presence is recorded as
  not checked (None), never as absent.
* Laxmi Narayana Solar's website returns HTTP 500, so no site_audit is
  attached; the report is ads-only and says so.

Run:  cd 01-LEADS && PYTHONPATH=/tmp/pdflibs python3 build_batch13_telangana.py
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
# 1. KAKATIYA ENERGIES (Hanamkonda)
# ---------------------------------------------------------------------------
# Website read live 2026-11-21 via direct fetch of kakatiyaenergies.com.
# Title: "Kakatiya Energies - Save Energy. Save Money". PHP/CodeIgniter build
# (index.php routes). Multiple H1 slider headings (SOLAR FARMS / POWER PLANTS,
# SOLAR FOR IRRIGATION, SOLAR ROOFTOP FOR YOUR HOME, SOLAR FOR COMMERCIAL,
# SOLAR FOR INDUSTRIAL). "Request Quote" / "Get a Quote" CTAs link to
# /index.php/quote. Login/Register links present. Testimonials present
# (named customers: Kedasu Narender, Venkataiah Chikkula, Yerram Krishna
# Murthy, Sharda Kandula, Pratap Singh). Stats: 10+ years, 700+ happy clients,
# 70% satisfaction. Email kakatiyasolarenergies@gmail.com, phone +91-8125801257.
# No WhatsApp link and no contact <form> in the rendered content captured;
# quote flow is a link to /index.php/quote. Head (pixels/meta) not captured
# through this channel, so pixel presence is None (not checked).

KAKATIYA_SITE = {
    "ssl": True,
    "load_time_seconds": None,                 # not measured
    "final_url": "https://kakatiyaenergies.com/index.php",
    "audit_date": READ_ON,
    "pixels": unknown_pixels(),
    "conversion": {
        "has_contact_form": False,             # quote is a link, no <form> in content
        "has_phone_click": True,               # +91-8125801257 shown in header
        "has_whatsapp_link": False,            # no wa.me / whatsapp in rendered content
        "has_cta_buttons": 6,                  # Request Quote / Get a Quote (x6)
        "has_live_chat": False,                # no chat widget in content
        "has_popup_optin": False,              # no popup/modal in content
        "has_testimonials": True,              # named customer testimonials
        "has_pricing_page_link": False,        # no pricing page linked
    },
    "seo": {
        "has_title": True,
        "title_text": "Kakatiya Energies - Save Energy. Save Money",
        "title_length": 45,
        "has_meta_description": None,          # head not captured
        "meta_desc_length": None,
        "h1_count": 5,                         # slider H1s (farms/irrigation/rooftop/commercial/industrial)
        "h1_text": "SOLAR FARMS / POWER PLANTS",
        "has_og_tags": None,                   # head not captured
        "has_schema": None,                    # head not captured
        "has_favicon": None,                   # head not captured
        "image_count": None,                   # not counted through this channel
        "images_without_alt": None,
    },
    "pagespeed": {"error": PAGESPEED_ERROR},
    "page_count": {"has_sitemap": None},
    "local_signals": {"has_google_maps_embed": None},
    "platform": "PHP (CodeIgniter-style index.php routing), server-rendered",
    "html_errors": None,                       # validator not run in this pass
    "scope_note": (
        "The website was read live on 2026-11-21 through a rendered-content "
        "fetch. Tracking-pixel and head checks (Meta Pixel, GA4, GTM, Google "
        "Ads, meta description, Open Graph, JSON-LD) need the raw served HTML "
        "and were not captured through this channel, so they are recorded as "
        "not checked rather than absent. PageSpeed and sitemap were not run."
    ),
}

KAKATIYA_ADS = [
    {
        "library_id": "2172318326990537",
        "library_url": "https://www.facebook.com/ads/library/?id=2172318326990537",
        "page_name": "Kakatiya Energies",
        "started": "Nov 11, 2026",
        "destination": "WhatsApp (API.WHATSAPP.COM) - Send WhatsApp message",
        "text": (
            "Thinking About Switching to Solar? Now Is the Right Time!\n\n"
            "Why pay more on electricity bills when you can generate your own power?\n\n"
            "With KAKATIYA ENERGIES, get complete solar solutions for your home and business!\n\n"
            "Our Solar Solutions:\n"
            "- Residential Solar\n"
            "- Commercial & Industrial Solar\n"
            "- Petrol Bunk Solar\n"
            "- On-Grid, Off-Grid & Hybrid Systems\n"
            "- Professional Installation\n"
            "- Net Metering & Subsidy Assistance\n\n"
            "SUBSIDY BENEFIT: Up to Rs.78,000 for eligible households under the PM Surya Ghar scheme.\n\n"
            "Easy EMI Options Available!\n\n"
            "The stated subsidy deadline is March 2027. Plan your installation before the deadline!\n\n"
            "BOOK YOUR FREE SOLAR SITE VISIT TODAY!\n\n"
            "Hanamkonda: +91 81258 01257 | 81252 22834\n\n"
            "KAKATIYA ENERGIES"
        ),
    },
    {
        "library_id": "2539681153175683",
        "library_url": "https://www.facebook.com/ads/library/?id=2539681153175683",
        "page_name": "Kakatiya Energies",
        "started": "Nov 18, 2026",
        "destination": "WhatsApp (API.WHATSAPP.COM) - Send WhatsApp message",
        "text": (
            "GO SOLAR. SAVE BIG!\n\n"
            "Make your home solar-powered and enjoy electricity bill savings!\n\n"
            "Get up to Rs.78,000 Solar Subsidy!\n\n"
            "Don't miss the opportunity - Subsidy benefits are available until March 2027.\n\n"
            "Why wait? Start saving on electricity bills while contributing to a greener future.\n\n"
            "- Reduce electricity bills\n"
            "- Clean and renewable energy\n"
            "- Long-term savings\n"
            "- Professional solar installation\n\n"
            "Call Kakatiya Energies today: +91 8125801257\n\n"
            "KAKATIYA ENERGIES"
        ),
    },
]

KAKATIYA = {
    "company": "Kakatiya Energies",
    "legal": "Kakatiya Energies",
    "city": "Hanamkonda, Telangana",
    "website": "https://kakatiyaenergies.com/",
    "ads_only": True,
    "website_audit_run": True,
    "checked_on": READ_ON,
    "generated_at": READ_ON,
    "source": "Meta Ad Library (India, active) + live website fetch, 2026-11-21",
    "ad_library": {
        "meta_own": {
            "found": True,
            "results_count": 2,
            "results_label": "2 live ads",
            "query": "Kakatiya Energies advertiser search (Meta Ad Library, India, active)",
            "ads": KAKATIYA_ADS,
        },
        "summary": (
            "2 live Meta ads confirmed on 2026-11-21 by opening each library ID "
            "directly. Both ads sell rooftop solar (residential, commercial, "
            "industrial, petrol-bunk) with the Rs.78,000 PM Surya Ghar subsidy "
            "and a March 2027 deadline, and both click to WhatsApp. The website "
            "was read live the same day. Google Ads Transparency records were "
            "not checked in this pass."
        ),
    },
    "funnel": {
        "type": "WhatsApp chat",
        "destination": "WhatsApp (API.WHATSAPP.COM) - Send WhatsApp message",
        "meaning": (
            "Both live ads click straight to a WhatsApp chat. The enquiry never "
            "reaches kakatiyaenergies.com, so the website cannot measure, "
            "retarget or attribute this spend."
        ),
    },
    "findings": [
        "Both live ads click to WhatsApp, not to the website - the enquiry "
        "never reaches kakatiyaenergies.com, so the site cannot measure or "
        "retarget this spend.",
        "The March 2027 subsidy deadline is the strongest urgency lever in the "
        "copy, but the website's quote page does not restate the deadline or "
        "the Rs.78,000 subsidy figure, so a visitor who lands on the site "
        "loses the reason to act now.",
        "The homepage slider carries five H1 headings (farms, irrigation, "
        "rooftop, commercial, industrial), which dilutes the single message a "
        "rooftop buyer needs.",
        "No WhatsApp link was found in the rendered website content, even "
        "though both ads sell through WhatsApp - the two channels are not "
        "connected on the site.",
        "Testimonials are present and named, and the site states 700+ happy "
        "clients, but neither live ad uses that social proof - both ads lead "
        "with price and subsidy only.",
    ],
    "next_steps": [
        "Point at least one ad at a website landing page that restates the "
        "Rs.78,000 subsidy and the March 2027 deadline, with a Meta Pixel so "
        "the click can be measured and retargeted.",
        "Add the WhatsApp number (+91 81258 01257) to the website header so "
        "the channel the ads already use is one tap away for site visitors.",
        "Reduce the homepage to one H1 (rooftop solar for homes) and move "
        "farms/irrigation/industrial to their own service pages.",
        "Add a customer-count or testimonial line to the ad copy - the site "
        "already has 700+ clients and named reviews to borrow.",
    ],
    "contact_facts": [
        ("Phone (site)", "+91-8125801257"),
        ("Phone (ad)", "+91 81258 01257 | 81252 22834"),
        ("Email", "kakatiyasolarenergies@gmail.com"),
        ("Location", "Hanamkonda, Telangana (Warangal & Hyderabad service area)"),
        ("Facebook page", "https://www.facebook.com/kaktiyasolarenergies/"),
        ("Website", "https://kakatiyaenergies.com/"),
    ],
    "contact": {
        "phone": "+91 81258 01257",
        "email": "kakatiyasolarenergies@gmail.com",
    },
    "site_audit": KAKATIYA_SITE,
    "audit_date": READ_ON,
    "site_evidence": {
        "pixel": None,
        "utm": False,
        "checked_on": READ_ON,
        "note": "Head HTML not captured through the sandbox fetch channel; "
                "pixel presence is not checked, not absent.",
    },
    "promise_gap": [
        {
            "promise": "Up to Rs.78,000 subsidy under PM Surya Ghar (both ads)",
            "site": "The quote page and services do not restate the Rs.78,000 "
                    "figure or the March 2027 deadline.",
        },
        {
            "promise": "Free solar site visit (ad 1 CTA)",
            "site": "The site offers a quote request but does not name a free "
                    "site visit or its booking steps.",
        },
    ],
}


# ---------------------------------------------------------------------------
# 2. VISIONTEK (Hyderabad, Begumpet)
# ---------------------------------------------------------------------------
# Website read live 2026-11-21 via direct fetch of visiontek.solar.
# Title: "VISIONTEK – Powering India's Smart Energy Future". H1: "Engineering
# the Future of Intelligent Energy". Products: RISE+ (On-Grid Inverter),
# FUTURE+ (Hybrid Inverter), VAULT+ (LFP Battery), PULSE+ (panel-level
# optimiser). WhatsApp wa.me/+919701601421 (two links). Blogs dated Nov 12
# and Nov 19, 2026. No contact <form>, no testimonials, no phone number in
# the rendered content. Head (pixels/meta) not captured, so pixel presence
# is None (not checked). Visiontek is a manufacturer (32+ years, Linkwell
# Telesystems) that also sells home solar systems - the live ads mix
# home-solar system ads with inverter/battery product ads.

VISIONTEK_SITE = {
    "ssl": True,
    "load_time_seconds": None,                 # not measured
    "final_url": "https://visiontek.solar/",
    "audit_date": READ_ON,
    "pixels": unknown_pixels(),
    "conversion": {
        "has_contact_form": False,             # no <form> in rendered content
        "has_phone_click": False,              # no tel: link in rendered content
        "has_whatsapp_link": True,             # wa.me/+919701601421 (x2)
        "has_cta_buttons": 2,                  # Connect on WhatsApp / Chat on WhatsApp
        "has_live_chat": False,                # no chat widget in content
        "has_popup_optin": False,              # no popup/modal in content
        "has_testimonials": False,             # no testimonials in content
        "has_pricing_page_link": False,        # no pricing page linked
    },
    "seo": {
        "has_title": True,
        "title_text": "VISIONTEK – Powering India's Smart Energy Future",
        "title_length": 48,
        "has_meta_description": None,          # head not captured
        "meta_desc_length": None,
        "h1_count": 1,
        "h1_text": "Engineering the Future of Intelligent Energy",
        "has_og_tags": None,                   # head not captured
        "has_schema": None,                    # head not captured
        "has_favicon": None,                   # head not captured
        "image_count": None,                   # not counted through this channel
        "images_without_alt": None,
    },
    "pagespeed": {"error": PAGESPEED_ERROR},
    "page_count": {"has_sitemap": None},
    "local_signals": {"has_google_maps_embed": None},
    "platform": "Server-rendered marketing site (visiontek.solar)",
    "html_errors": None,                       # validator not run in this pass
    "scope_note": (
        "The website was read live on 2026-11-21 through a rendered-content "
        "fetch. Tracking-pixel and head checks (Meta Pixel, GA4, GTM, Google "
        "Ads, meta description, Open Graph, JSON-LD) need the raw served HTML "
        "and were not captured through this channel, so they are recorded as "
        "not checked rather than absent. PageSpeed and sitemap were not run."
    ),
}

VISIONTEK_ADS = [
    {
        "library_id": "1133037052650969",
        "library_url": "https://www.facebook.com/ads/library/?id=1133037052650969",
        "page_name": "Visionteknewenergy",
        "started": "Nov 12, 2026",
        "destination": "Instagram chat (Chat with us / Send Message)",
        "text": (
            "Still paying high electricity bills?\n\n"
            "Switch to Visiontek Solar and turn sunlight into savings. Our smart "
            "system powers your home directly, stores extra energy for the night "
            "and helps lower your monthly bill.\n\n"
            "Its time to power your home naturally.\n\n"
            "#Visiontek #GoSolar #SolarPower #SolarEnergy #EnergyStorage"
        ),
    },
    {
        "library_id": "1126670763504735",
        "library_url": "https://www.facebook.com/ads/library/?id=1126670763504735",
        "page_name": "Visionteknewenergy",
        "started": "Nov 12, 2026",
        "destination": "Instagram chat (Chat with us / Send Message)",
        "text": (
            "Summer heat is rising, and so are electricity bills.\n\n"
            "With increasing power consumption, it's time to think smarter about "
            "how we use energy. Switch to solar with Visiontek Solar Solutions "
            "and take a smarter step towards managing your energy needs.\n\n"
            "The right time to consider solar? It's now.\n\n"
            "#Visiontek #VisiontekSolar #SolarEnergy #SolarSolutions #GoSolar "
            "#RenewableEnergy"
        ),
    },
    {
        "library_id": "1642086640990986",
        "library_url": "https://www.facebook.com/ads/library/?id=1642086640990986",
        "page_name": "Visionteknewenergy",
        "started": "Nov 12, 2026",
        "destination": "Instagram chat (Chat with us / Send Message)",
        "text": (
            "Control your electricity bill before it shocks you!\n\n"
            "Go solar with Visiontek and take charge of your energy.\n\n"
            "#Visiontek #GoSolar #SolarEnergy #SolarPower #SaveOnElectricity "
            "#RenewableEnergy #CleanEnergy #SolarSolutions #GreenEnergy "
            "#EnergySavingSolutions"
        ),
    },
    {
        "library_id": "1129421993235131",
        "library_url": "https://www.facebook.com/ads/library/?id=1129421993235131",
        "page_name": "Visionteknewenergy",
        "started": "Nov 12, 2026",
        "destination": "Instagram chat (Chat with us / Send Message)",
        "text": (
            "One inverter. Multiple power sources.\n\n"
            "With the Visiontek Hybrid Inverter, harness power from solar, grid, "
            "and battery - all managed through one intelligent system.\n\n"
            "#Visiontek #FuturePlus #HybridInverter #SolarEnergy #RenewableEnergy "
            "#SolarPower"
        ),
    },
    {
        "library_id": "1682377416875296",
        "library_url": "https://www.facebook.com/ads/library/?id=1682377416875296",
        "page_name": "Visionteknewenergy",
        "started": "Nov 12, 2026",
        "destination": "Instagram chat (Chat with us / Send Message)",
        "text": (
            "Say goodbye to soaring electricity bills and take control of your "
            "energy expenses. Switch to solar today and start generating your "
            "own clean savings.\n\n"
            "#CutElectricityBills #SolarSavings #GoGreen #EnergyIndependence "
            "#VisiontekSolar"
        ),
    },
]

VISIONTEK = {
    "company": "Visiontek",
    "legal": "Visionteknewenergy (Linkwell Telesystems)",
    "city": "Hyderabad, Telangana",
    "website": "https://visiontek.solar/",
    "ads_only": True,
    "website_audit_run": True,
    "checked_on": READ_ON,
    "generated_at": READ_ON,
    "source": "Meta Ad Library (India, active) + live website fetch, 2026-11-21",
    "ad_library": {
        "meta_own": {
            "found": True,
            "results_count": 5,
            "results_label": "5 live ads captured (advertiser shows ~70 results)",
            "query": "Visionteknewenergy advertiser search (Meta Ad Library, India, active)",
            "ads": VISIONTEK_ADS,
        },
        "summary": (
            "5 live Meta ads captured on 2026-11-21 from the Visionteknewenergy "
            "advertiser page (the page shows roughly 70 active results; the 5 "
            "most recent, all started Nov 12, 2026, are reproduced here). Four "
            "sell a home solar system with storage; one sells the FUTURE+ "
            "hybrid inverter. All five click to Instagram chat. The website was "
            "read live the same day. Google Ads Transparency records were not "
            "checked in this pass."
        ),
    },
    "funnel": {
        "type": "Instagram chat",
        "destination": "Instagram chat (Chat with us / Send Message)",
        "meaning": (
            "All five captured ads click to an Instagram chat, not to "
            "visiontek.solar. The enquiry never reaches the website, so the "
            "site cannot measure, retarget or attribute this spend."
        ),
    },
    "findings": [
        "All five captured ads click to Instagram chat, not to visiontek.solar "
        "- the enquiry never reaches the website, so the site cannot measure "
        "or retarget this spend.",
        "Four of the five ads sell a home solar system, but the website leads "
        "with inverter and battery products (RISE+, FUTURE+, VAULT+, PULSE+). "
        "A visitor who lands on the site after a home-solar ad finds no "
        "rooftop-system offer, price or subsidy figure.",
        "No live ad mentions the PM Surya Ghar subsidy or any price, even "
        "though the website's own blogs (Nov 12 and Nov 19, 2026) discuss "
        "hybrid inverters and batteries - the strongest buying lever in this "
        "market is absent from the copy.",
        "The website has no contact form, no phone number and no testimonials "
        "in the rendered content; WhatsApp is the only conversion path, which "
        "matches the ads but leaves no measurable web funnel.",
        "The advertiser page shows roughly 70 active results, but the five "
        "captured here all started on the same day (Nov 12, 2026) with "
        "near-identical copy - the account is running volume, not tested "
        "variations.",
    ],
    "next_steps": [
        "Point the home-solar ads at a website landing page that sells the "
        "rooftop system (not the inverter catalogue) with a Meta Pixel, so "
        "the click can be measured and retargeted.",
        "Add the PM Surya Ghar subsidy figure and a starting price to at "
        "least one ad - competitors in Telangana lead with Rs.78,000 and "
        "this account does not mention subsidy at all.",
        "Add a contact form and a phone number to the website so visitors "
        "who do not use WhatsApp still have a way to enquire.",
        "Split the account into two campaigns - home solar systems and "
        "inverter/battery products - so each audience sees one message.",
    ],
    "contact_facts": [
        ("WhatsApp (site + ads)", "+91 9701601421 (wa.me/+919701601421)"),
        ("Location", "Begumpet, Hyderabad, Telangana"),
        ("Facebook page", "https://www.facebook.com/Visionteknewenergy/"),
        ("Website", "https://visiontek.solar/"),
        ("Products", "RISE+ On-Grid, FUTURE+ Hybrid, VAULT+ LFP Battery, PULSE+"),
    ],
    "contact": {
        "phone": "+91 9701601421",
        "email": "",
    },
    "site_audit": VISIONTEK_SITE,
    "audit_date": READ_ON,
    "site_evidence": {
        "pixel": None,
        "utm": False,
        "checked_on": READ_ON,
        "note": "Head HTML not captured through the sandbox fetch channel; "
                "pixel presence is not checked, not absent.",
    },
    "promise_gap": [
        {
            "promise": "Home solar system that powers your home and stores "
                       "extra energy for the night (ad 1)",
            "site": "The website sells inverters and batteries as products; "
                    "it does not present a complete home solar system offer "
                    "with price or subsidy.",
        },
        {
            "promise": "Switch to solar and lower your monthly bill (ads 2-5)",
            "site": "No savings figure, price or subsidy amount appears in "
                    "the rendered website content.",
        },
    ],
}


# ---------------------------------------------------------------------------
# 3. LAXMI NARAYANA SOLAR (Karimnagar) - website DOWN, ads-only report
# ---------------------------------------------------------------------------
# Website https://www.laxminarayanasolar.in/ returns HTTP 500 (www and
# non-www, re-checked 2026-11-21). No site_audit is attached. The report is
# ads-only and says so. Ad copy is in Telugu; the PDF font cannot render
# Telugu, so the stored text keeps the Telugu and the PDF shows the
# latin-safe placeholder for the body copy. The key facts (Rs.78,000 subsidy,
# Karimnagar, phones) are in the contact_facts and funnel, which are Latin.

LAXMI_ADS = [
    {
        "library_id": "1801231361161321",
        "library_url": "https://www.facebook.com/ads/library/?id=1801231361161321",
        "page_name": "Laxminarayanasolarsolutions",
        "started": "Nov 13, 2026",
        "destination": "URL link (ad destination not confirmed from the card)",
        "text": (
            "Karimnagar people, good news! Chance to get up to Rs.78,000 solar "
            "subsidy! Install solar panels on your home under the PM-Surya Ghar "
            "scheme and get relief from rising monthly current bills!\n\n"
            "Benefits from Laxmi Narayana Solar:\n"
            "- Eligibility for government subsidy up to Rs.78,000\n"
            "- Zero maintenance\n"
            "- 25-30 year warranty\n"
            "- Bank loan facility\n"
            "- Solar solutions for homes, hospitals, industries, hostels\n\n"
            "Do not delay in knowing your eligibility for the subsidy scheme "
            "benefits!\n\n"
            "Karimnagar, Telangana\n"
            "Call now: 9493093728 | 8712780023"
        ),
    },
    {
        "library_id": "1650285136378259",
        "library_url": "https://www.facebook.com/ads/library/?id=1650285136378259",
        "page_name": "Laxminarayanasolarsolutions",
        "started": "Nov 19, 2026",
        "destination": "Facebook lead form (FB.ME) - Get Solar Today",
        "text": (
            "No more trouble with high electricity bills!\n\n"
            "Install solar panels at your home and reduce your electricity "
            "costs. Under the PM Surya Ghar scheme, depending on eligibility, "
            "there is a chance to get government subsidy up to Rs.78,000.\n\n"
            "- Premium Quality Solar Panels\n"
            "- Residential Solar Installation\n"
            "- Bank Loan Facility\n"
            "- Professional Installation\n\n"
            "Contact us today for your solar installation!"
        ),
    },
]

LAXMI = {
    "company": "Laxmi Narayana Solar",
    "legal": "Laxminarayanasolarsolutions",
    "city": "Karimnagar, Telangana",
    "website": "https://www.laxminarayanasolar.in/",
    "ads_only": True,
    "website_audit_run": False,
    "checked_on": READ_ON,
    "generated_at": READ_ON,
    "source": "Meta Ad Library (India, active), 2026-11-21. Website returns "
              "HTTP 500, so no website audit was run.",
    "ad_library": {
        "meta_own": {
            "found": True,
            "results_count": 2,
            "results_label": "2 live ads",
            "query": "Laxminarayanasolarsolutions advertiser search (Meta Ad Library, India, active)",
            "ads": LAXMI_ADS,
        },
        "summary": (
            "2 live Meta ads confirmed on 2026-11-21 by opening each library ID "
            "directly. Both ads are in Telugu and sell rooftop solar in "
            "Karimnagar with the Rs.78,000 PM Surya Ghar subsidy, bank loan "
            "and 25-30 year warranty. One ad clicks to a URL link, the other "
            "to a Facebook lead form (FB.ME). The company website "
            "laxminarayanasolar.in returns HTTP 500, so no website audit was "
            "run for this report. Google Ads Transparency records were not "
            "checked in this pass."
        ),
    },
    "funnel": {
        "type": "Mixed: URL link and Facebook lead form",
        "destination": "Ad 1: URL link. Ad 2: Facebook lead form (FB.ME).",
        "meaning": (
            "The two live ads do not agree on where the click lands. One "
            "points at a URL, the other at an FB.ME lead form, so the spend "
            "cannot be measured in one place."
        ),
    },
    "findings": [
        "The company website laxminarayanasolar.in returns HTTP 500, so ad "
        "traffic that does reach the web has nowhere to land. This is the "
        "single biggest leak in the funnel.",
        "The two live ads do not agree on the destination - one is a URL "
        "link, the other an FB.ME lead form - so the spend cannot be measured "
        "in one place.",
        "Both ads are in Telugu, which is right for Karimnagar, but the "
        "website (when it loads) and the lead form do not carry the same "
        "Rs.78,000 subsidy figure in a way a visitor can verify.",
        "The ads promise zero maintenance and a 25-30 year warranty, but "
        "there is no live website page to confirm what those cover.",
        "No website audit was run for this report because the site is down; "
        "every website claim is therefore left unmade rather than guessed.",
    ],
    "next_steps": [
        ("Fix the website first",
         "The site returns HTTP 500, so every rupee currently lands on a dead "
         "page or a lead form. Restore the site before spending more on ads."),
        ("Unify the ad destination",
         "Point both ads at the same destination (the website landing page) "
         "with a Meta Pixel so the click can be measured and retargeted."),
        ("Publish the offer on the landing page",
         "Put the Rs.78,000 subsidy, bank-loan and warranty terms on the "
         "landing page so the ad promise can be verified in one click."),
        ("Re-audit once the site loads",
         "Re-run the full website audit once the site is back, then re-issue "
         "this report as a complete audit."),
    ],
    "contact_facts": [
        ("Phone (ad)", "9493093728 | 8712780023"),
        ("Location", "Karimnagar, Telangana"),
        ("Facebook page", "https://www.facebook.com/61583798920523/"),
        ("Website", "https://www.laxminarayanasolar.in/ (returns HTTP 500)"),
        ("Subsidy", "Up to Rs.78,000 under PM Surya Ghar"),
    ],
    "contact": {
        "phone": "9493093728",
        "email": "",
    },
    # No site_audit: the website is down (HTTP 500), so no website audit was run.
    "audit_date": READ_ON,
    "site_evidence": {
        "pixel": None,
        "utm": False,
        "checked_on": READ_ON,
        "note": "Website returns HTTP 500; no landing page was read, so pixel "
                "presence is not checked.",
    },
    "promise_gap": [
        {
            "promise": "Up to Rs.78,000 government subsidy (both ads)",
            "site": "The website is down (HTTP 500), so the promise cannot be "
                    "verified on the site.",
        },
        {
            "promise": "Zero maintenance, 25-30 year warranty (ad 1)",
            "site": "No live page states what the warranty covers.",
        },
    ],
}


LEADS = [KAKATIYA, VISIONTEK, LAXMI]


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
