"""Measured data for the five Telangana leads (batch 15), read 2026-11-28.

Every value here was read live on 2026-11-28 from one of:

  * the lead's own page (direct fetch, plus the W3C Nu HTML Checker's
    "show source" view of the same URL, which returns the exact bytes served);
  * Meta Ad Library, country = India, active ads only (advertiser name search
    and/or direct library-id fetch);
  * Google Ads Transparency Centre, region = IN, domain filter;
  * the site's own sitemap index.

Where a check could not be run from this environment the value is None and the
reason is carried in `scope_note` / `pagespeed.error`. Nothing here is a
guess, an average or a remembered figure from an earlier session.
"""

CHECKED_ON = "2026-11-28"

# Shared PageSpeed outcome: the keyless PageSpeed Insights API could not be
# reached from the crawler on 2026-11-28, so no speed number is claimed.
PS_BLOCKED = {
    "mobile_performance_score": None,
    "largest_contentful_paint": None,
    "error": ("not measured - the PageSpeed Insights API could not be reached "
              "from this crawler; no speed score is claimed"),
}

ADS_URL = "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=IN&media_type=all"
GADS = "https://adstransparency.google.com/?region=IN&domain="

SOLAR_QUERY = "solar Hyderabad"
DENTAL_QUERY = "dental clinic Hyderabad"
INTERIOR_QUERY = "interior designers Hyderabad"


def _ad(lid, page, started, dest, text, note=""):
    return {
        "library_id": lid,
        "page_name": page,
        "started": started,
        "destination": dest,
        "text": text,
        "library_url": f"https://www.facebook.com/ads/library/?id={lid}",
        "verified_on": CHECKED_ON,
        "note": note,
    }


# ---------------------------------------------------------------------------
# 1. SunSolar Power Systems - sunsolar.info
# ---------------------------------------------------------------------------

SUNSOLAR = {
    "company": "SunSolar Power Systems",
    "vertical": "solar",
    "legal": "SunSolar Power Systems (Hyderabad)",
    "city": "Hyderabad, Telangana",
    "website": "https://www.sunsolar.info/",
    "checked_on": CHECKED_ON,
    "summary": (
        "SunSolar is running four active Meta ads, all opened on 21-23 November 2026, and every one of "
        "them sends the click to a bare http://fb.me/ redirect - a destination we cannot inspect and that "
        "carries no tracking parameters. The site itself does fire a Google Ads conversion tag "
        "(AW-18179174251) on the lead form, the WhatsApp links and both phone numbers, so the money spent "
        "on Google is measurable. Meta spend is not: there is no Meta Pixel anywhere in the served page, "
        "no GA4, and no GTM container, which means the four live Facebook ads produce leads SunSolar can "
        "count only by hand. The Google Ads Transparency Centre returns no advertiser record for "
        "sunsolar.info in India, so the Google Ads tag is currently collecting conversion data for an "
        "account that shows no live Google ads."),
    "meta_own": {
        "found": True,
        "page": "SunSolarhyd",
        "page_url": "https://www.facebook.com/sunsolarhyd/",
        "query": "SunSolarhyd (advertiser name search)",
        "search_url": ADS_URL + "&q=SunSolarhyd&search_type=keyword_unordered",
        "results_count": 4,
        "results_label": "4 active ad cards returned for the advertiser's own page",
        "ads": [
            _ad("1810233520093832", "SunSolarhyd", "23 Nov 2026", "http://fb.me/",
                "ANANTHAPUR, SWITCH TO SOLAR FOR JUST Rs. 2,18,999! This is your chance to make the "
                "switch to clean energy with SunSolar Power Systems! SPECIAL 5 KW SOLAR OFFER Only "
                "Rs. 2,18,999/- Government Subsidy Included - Rs. 78,000. Rs. 0 Down Payment. Easy EMI "
                "Available. 30 Years Warranty. Free Site Visit. Invest in solar today and enjoy long-term "
                "savings with trusted Adani Solar & Waaree Solar panels! Book your FREE solar consultation "
                "now! Call: +91 98666 02001. Suite 312, 3rd Floor, Kokapet Terminal Complex, Gandipet Main "
                "Road, Narsingi, Hyderabad."),
            _ad("2413566255849370", "SunSolarhyd", "21 Nov 2026", "http://fb.me/",
                "5 kW Solar at Rs. 2,18,999/-! Get offer. A 5 kW rooftop system priced at Rs. 2,18,999 "
                "with the Rs. 78,000 government subsidy already deducted, 30-year warranty and a free "
                "site visit, from SunSolar Power Systems, Narsingi, Hyderabad."),
            _ad("1866738597708833", "SunSolarhyd", "21 Nov 2026", "http://fb.me/",
                "Go Solar for Just Rs. 1,71,999! Make your home energy-efficient with a 4 kW Solar System "
                "from SunSolar Power Systems. Festive Season Offer Includes: Rs. 78,000 Government Subsidy "
                "Included, 0 Down Payment, Easy EMI Available, 30 Years Warranty, Free Site Visit. Your "
                "Solar Price Breakdown: Rs. 2,49,999 - Rs. 78,000 Subsidy = Rs. 1,71,999/-. Call "
                "+91 98666 02001."),
            _ad("2576227376137902", "SunSolarhyd", "22 Oct 2026", "http://fb.me/",
                "HYDERABAD - GO SOLAR AT Rs. 1,31,999 FOR A 3 KW SYSTEM. Government Subsidy Included. "
                "30 Years Warranty. Free Site Visit. Original Price: Rs. 2,96,999/- Government Subsidy: "
                "Rs. 78,000/- Your Final Price: Rs. 2,18,999/- Call Now: +91 98666 20001. Office: Suite 312, "
                "3rd Floor, Kokapet Terminal Complex, Gandipet Main Road, Narsingi, Hyderabad, Telangana - "
                "500075. Book your FREE solar consultation today!"),
        ],
    },
    "google_own": {
        "found": False,
        "query_url": GADS + "sunsolar.info",
        "detail": None,
        "note": ("Domain filter sunsolar.info, region India, advertiser-type all, live on 2026-11-28: "
                 "the Transparency Centre returns no advertiser record and no ads for this domain."),
    },
    "meta_competitors": {
        "query": SOLAR_QUERY,
        "search_url": ADS_URL + "&q=solar%20Hyderabad&search_type=keyword_unordered",
        "results_count": 430,
        "ads": [
            _ad("942037648839408", "Sri Balaji Solar Energies", "29 May 2026", "http://fb.me/",
                "[Ad copy in Telugu - open the live ad] Rs. 0 down payment rooftop solar, up to Rs. 78,000 "
                "central subsidy, EMI from Rs. 1,355/month, 10,000+ customers, free site visit across "
                "Warangal, Hanumakonda, Rajahmundry, Bhadrachalam, Hyderabad and nearby districts."),
            _ad("1472241928117694", "SolarSquare Energy", "13 Oct 2026",
                "https://www.solarsquare.in/rooftop-solar-in-hyderabad-1",
                "Solar Is for Every Home. Hyderabad, what if your solar savings came with a money-back "
                "guarantee? Guaranteed Savings. Trusted by 36,000+ Homes. India's No. 1 Home Solar Company. "
                "Switch to SolarSquare! Book Now."),
            _ad("29143729581958632", "Visionteknewenergy", "12 Nov 2026", "https://www.instagram.com/",
                "Still paying high electricity bills? Switch to Visiontek Solar and turn sunlight into "
                "savings. Our smart system powers your home directly, stores extra energy for the night and "
                "helps lower your monthly bill."),
        ],
    },
    "pixels": {
        "meta_pixel": False,
        "google_ads": True,
        "google_analytics_ga4": False,
        "google_analytics_ua": False,
        "linkedin_insight": False,
        "microsoft_clarity": False,
        "hotjar": False,
        "google_tag_manager": False,
    },
    "conversion": {
        "has_contact_form": True,
        "has_phone_click": True,
        "has_whatsapp_link": True,
        "has_cta_buttons": 12,
        "has_live_chat": False,
        "has_popup_optin": False,
        "has_testimonials": False,
        "has_pricing_page_link": True,
    },
    "seo": {
        "title": "SunSolar Power Systems | Rooftop Solar in Hyderabad & Telangana",
        "title_text": "SunSolar Power Systems | Rooftop Solar in Hyderabad & Telangana",
        "title_length": 64,
        "has_meta_description": True,
        "meta_description": ("SunSolar Power Systems designs, installs and maintains premium rooftop solar "
                             "for homes and businesses across Hyderabad and Telangana. Get a free quote."),
        "h1_count": 1,
        "h1_text": "Power Your Future with the Sun",
        "has_og_tags": True,
        "has_schema": False,
        "has_favicon": True,
        "image_count": 3,
        "images_without_alt": 0,
    },
    "pagespeed": PS_BLOCKED,
    "page_count": {
        "has_sitemap": False,
        "note": ("No sitemap at /sitemap.xml - the request returned no document on 2026-11-28, and no "
                 "sitemap is referenced from the homepage markup."),
    },
    "local_signals": {"has_google_maps_embed": False, "mentions_city": True},
    "html_errors": {
        "errors": 2,
        "warnings": None,
        "info": None,
        "note": ("validator halted after the first two errors, so this is a floor, not a total; the one "
                 "read in full is 'Bad value video for attribute as on element link' (line 18)"),
    },
    "ssl": True,
    "load_time_seconds": None,
    "final_url": "https://www.sunsolar.info/",
    "scope_note": (
        "The homepage was read directly and through the W3C checker's source view: head (lines 1-36) and "
        "the closing script block (lines 577-580, gsap, ScrollTrigger, script.js, tracking.js). tracking.js "
        "defines SUNSOLAR_CONVERSIONS and fires one Google Ads conversion action "
        "(AW-18179174251/3vm-CPqx27UcEOvewNxD) for the lead form, the WhatsApp link and both phone links - "
        "that is source-code evidence that the tag is installed and wired, not proof that a conversion has "
        "ever been recorded in the account. No Meta Pixel, GA4, GTM, LinkedIn, Clarity or Hotjar script is "
        "present in the served HTML. The four Meta ads are live; the fb.me redirect hides their landing page "
        "from inspection."),
    "recommended_steps": [
        ("Put a destination you control behind the four live ads",
         "All four SunSolar ads open on http://fb.me/, a redirect with no landing page, no UTM and no "
         "pixel - so Meta spend cannot be joined to the enquiries it produces. A page on sunsolar.info "
         "with the pixel installed fixes that in an afternoon."),
        ("Install the Meta Pixel and fire the same events tracking.js already fires",
         "The Google Ads conversion tag already listens for #leadForm, [data-whatsapp-link] and "
         "[data-phone-link]. Adding a Meta Pixel on those same three actions turns the 4 live ads into a "
         "measurable, retargetable channel instead of a bill."),
        ("Turn on GA4 alongside the Google Ads tag",
         "AW-18179174251 records conversions but nothing records sessions, sources or page paths. Without "
         "GA4 the only numbers available are the ones Google Ads chooses to report."),
        ("Fix the video preload before the next campaign",
         "The homepage preloads assets/video/sunsolar-cinematic-loop.mp4 and the validator flags "
         "'Bad value video for attribute as' on line 18; on mobile data that preload is the first thing "
         "between a paid click and the quote calculator."),
    ],
    "funnel": {
        "from": "4 live Meta ads (started 21-23 Nov 2026) + a wired Google Ads conversion tag",
        "to": "http://fb.me/ redirect (ad click) / homepage lead form on sunsolar.info",
        "destination": "http://fb.me/ (ads) - https://www.sunsolar.info/ (site form, WhatsApp, 2 phones)",
        "note": ("The ad destination could not be inspected: fb.me is a short-link redirect. The site form "
                 "posts to the WhatsApp link with the name, phone, property type, monthly bill and message."),
    },
    "contact_facts": [
        "Phone: +91 98666 02001 and +91 99599 96002",
        "Email: sales@sunsolar.info",
        "Address: Suite 312, Kokapet Terminal Complex, Narsingi, Hyderabad 500075",
        "Meta page: facebook.com/sunsolarhyd (4 active ads)",
    ],
    "site_evidence": {"pixel": False, "utm": False, "checked_on": CHECKED_ON,
                      "note": "Ad click lands on http://fb.me/ - no landing page reachable for a UTM check."},
}

# ---------------------------------------------------------------------------
# 2. PNR Sunrise Energies - sunriseenergies.in
# ---------------------------------------------------------------------------

PNR = {
    "company": "PNR Sunrise Energies",
    "vertical": "solar",
    "legal": "PNR Sunrise Energies Pvt Ltd",
    "city": "Hyderabad, Telangana",
    "website": "https://sunriseenergies.in/",
    "checked_on": CHECKED_ON,
    "summary": (
        "PNR Sunrise Energies has one active Meta ad - opened 12 November 2026 - and it is a channel-partner "
        "recruitment ad, not a homeowner offer: the copy invites solar installers to 'partner with us' and "
        "the button opens a WhatsApp chat, while the website is only mentioned in the body text. The site "
        "sells solar EPC and EV charging and is technically clean for a hand-built page (6 markup errors, "
        "3 warnings), but it carries no analytics, no pixel and no tag manager of any kind, so neither the "
        "ad nor the site can attribute a single lead. The Google Ads Transparency Centre returns no "
        "advertiser record for sunriseenergies.in in India, and the site's canonical tag points at a "
        "placeholder domain (www.sunriseenergies.example), which tells Google the real page is elsewhere."),
    "meta_own": {
        "found": True,
        "page": "PNR Sunrise Energies",
        "page_url": "https://www.facebook.com/profile.php?id=61595350896439",
        "query": "PNR Sunrise Energies (advertiser name search)",
        "search_url": ADS_URL + "&q=PNR%20Sunrise%20Energies&search_type=keyword_unordered",
        "results_count": 1,
        "results_label": "1 active ad card returned for the advertiser (ad detail opened directly)",
        "ads": [
            _ad("28807326382303186", "PNR Sunrise Energies", "12 Nov 2026",
                "https://api.whatsapp.com/send (WhatsApp chat)",
                "Become a Solar Channel Partner with PNR Sunrise Energies Pvt Ltd. We are expanding across "
                "Telangana and Andhra Pradesh and looking for channel partners, dealers and installers. "
                "Partner with us for: rooftop solar projects, PM Surya Ghar subsidy support, EV charging "
                "installations, end-to-end EPC execution and marketing support. Attractive margins. "
                "Dedicated support. Growing market. Call or WhatsApp: +91 63045 87145. Website: "
                "sunriseenergies.in. Hyderabad, Telangana."),
        ],
    },
    "google_own": {
        "found": False,
        "query_url": GADS + "sunriseenergies.in",
        "detail": None,
        "note": ("Domain filter sunriseenergies.in, region India, advertiser-type all, live on 2026-11-28: "
                 "'No ads found' - no advertiser record and no ads for this domain."),
    },
    "meta_competitors": {
        "query": SOLAR_QUERY,
        "search_url": ADS_URL + "&q=solar%20Hyderabad&search_type=keyword_unordered",
        "results_count": 430,
        "ads": [
            _ad("1472241928117694", "SolarSquare Energy", "13 Oct 2026",
                "https://www.solarsquare.in/rooftop-solar-in-hyderabad-1",
                "Solar Is for Every Home. Hyderabad, what if your solar savings came with a money-back "
                "guarantee? Guaranteed Savings. Trusted by 36,000+ Homes. India's No. 1 Home Solar Company. "
                "Switch to SolarSquare! Book Now."),
            _ad("29143729581958632", "Visionteknewenergy", "12 Nov 2026", "https://www.instagram.com/",
                "Still paying high electricity bills? Switch to Visiontek Solar and turn sunlight into "
                "savings. Our smart system powers your home directly, stores extra energy for the night and "
                "helps lower your monthly bill."),
            _ad("942037648839408", "Sri Balaji Solar Energies", "29 May 2026", "http://fb.me/",
                "[Ad copy in Telugu - open the live ad] Rs. 0 down payment rooftop solar, up to Rs. 78,000 "
                "central subsidy, EMI from Rs. 1,355/month, 10,000+ customers, free site visit across "
                "Warangal, Hanumakonda, Rajahmundry, Bhadrachalam, Hyderabad and nearby districts."),
        ],
    },
    "pixels": {
        "meta_pixel": False,
        "google_ads": False,
        "google_analytics_ga4": False,
        "google_analytics_ua": False,
        "linkedin_insight": False,
        "microsoft_clarity": False,
        "hotjar": False,
        "google_tag_manager": False,
    },
    "conversion": {
        "has_contact_form": True,
        "has_phone_click": True,
        "has_whatsapp_link": True,
        "has_cta_buttons": 10,
        "has_live_chat": False,
        "has_popup_optin": False,
        "has_testimonials": True,
        "has_pricing_page_link": False,
    },
    "seo": {
        "title": "Sunrise Energies | Solar EPC Company in Hyderabad | Rooftop Solar, EV Charging & O&M",
        "title_text": "Sunrise Energies | Solar EPC Company in Hyderabad | Rooftop Solar, EV Charging & O&M",
        "title_length": 88,
        "has_meta_description": True,
        "meta_description": ("PNR Sunrise Energies builds rooftop solar, ground-mount and EV charging "
                             "projects across Telangana and Andhra Pradesh - EPC, subsidy paperwork and "
                             "O&M under one roof."),
        "h1_count": 1,
        "h1_text": "Power Your Future. Naturally.",
        "has_og_tags": True,
        "has_schema": False,
        "has_favicon": False,
        "image_count": None,
        "images_without_alt": None,
    },
    "pagespeed": PS_BLOCKED,
    "page_count": {
        "has_sitemap": None,
        "note": "Not checked in this pass - the sitemap was not fetched for this site.",
    },
    "local_signals": {"has_google_maps_embed": False, "mentions_city": True},
    "html_errors": {
        "errors": 6,
        "warnings": 3,
        "info": None,
        "note": ("includes an invalid 'r:' property inside @keyframes and aria-hidden=\"True\" on a "
                 "decorative element"),
    },
    "ssl": True,
    "load_time_seconds": None,
    "final_url": "https://sunriseenergies.in/",
    "scope_note": (
        "The single-page site was read in full through the W3C checker's source view (lines 1-683) and the "
        "closing inline script block. There is no script from Google, Meta, LinkedIn, Clarity, Hotjar or any "
        "tag manager in the served HTML - the only JavaScript is the site's own. That is a source-code "
        "finding: nothing on this page is measured today, but a tag could still be added server-side, which "
        "a page read cannot see. The homepage counters render as '0+', '0 MW' and '0%', and the canonical "
        "link points at https://www.sunriseenergies.example/ - a placeholder domain - so the page tells "
        "Google the authoritative copy lives somewhere that does not exist."),
    "recommended_steps": [
        ("Install one analytics layer before the next ad",
         "There is no GA4, no GTM and no Meta Pixel in the served HTML, so the one live ad produces leads "
         "into a WhatsApp inbox with no record of where they came from."),
        ("Fix the canonical URL",
         "The canonical tag points at https://www.sunriseenergies.example/, a placeholder. Every search "
         "engine reading it is told the real page is somewhere else - a one-line fix with a direct SEO "
         "payoff."),
        ("Make the homepage counters show real numbers",
         "The trust strip renders '0+', '0 MW' and '0%' because the counters animate from zero and the "
         "script never provides a value; on a slow phone they stay at zero."),
        ("Point the channel-partner ad at a partner landing page",
         "The ad is recruiting installers, but the button opens a WhatsApp chat. A page carrying margins, "
         "territories and an application form would qualify partners before a human spends time on them."),
    ],
    "funnel": {
        "from": "1 live Meta ad (12 Nov 2026) - channel-partner recruitment",
        "to": "WhatsApp chat (api.whatsapp.com)",
        "destination": ("https://api.whatsapp.com/send - the site sunriseenergies.in appears only as body "
                        "text in the ad, not as the click destination"),
        "note": ("No landing page is involved and no tracking parameter exists, so the ad cannot be joined "
                 "to any site visit."),
    },
    "contact_facts": [
        "Phone / WhatsApp: +91 63045 87145",
        "No email address and no street address are published on the homepage",
        "Meta page: PNR Sunrise Energies (1 active ad)",
    ],
    "site_evidence": {"pixel": False, "utm": False, "checked_on": CHECKED_ON,
                      "note": "Ad click lands in WhatsApp; the site is not the ad destination."},
}

# ---------------------------------------------------------------------------
# 3. D'LIFE Home Interiors - dlifeinteriors.com/location/hyderabad/
# ---------------------------------------------------------------------------

DLIFE = {
    "company": "D'LIFE Home Interiors",
    "conservative_scope": True,  # cache layer hides the tag layer - measured findings only
    "vertical": "interiors",
    "legal": "D'LIFE Interiors Private Limited",
    "city": "Hyderabad, Telangana",
    "website": "https://dlifeinteriors.com/location/hyderabad/",
    "checked_on": CHECKED_ON,
    "summary": (
        "D'LIFE is the only lead in this batch that is advertising on both platforms at scale: five active "
        "Meta ads read today (the oldest running since 13 May 2026) and roughly 200 live Google ads under "
        "the verified advertiser 'D'LIFE Interiors Private Limited'. The spend is national while the page we "
        "audited is Hyderabad-specific, and the mismatch shows: the ads quote a Delhi phone number "
        "(+91 9567231111) on a page that publishes +91 949 508 7777, and every Meta ad opens a Messenger "
        "chat rather than the site. The Hyderabad page is served through NitroPack, which rewrites and "
        "defers third-party scripts, so no pixel could be confirmed from the HTML - that is recorded as "
        "unchecked, not as missing. What is measurable is the markup: 148 validator errors, including 64 "
        "telephone links with unencoded spaces that will not dial on some Android handsets."),
    "meta_own": {
        "found": True,
        "page": "D'LIFE Home Interiors (dlifehome)",
        "page_url": "https://www.facebook.com/dlifehome/",
        "query": "Dlife Interiors (advertiser name search - the apostrophe breaks Meta's search box)",
        "search_url": ADS_URL + "&q=Dlife%20Interiors&search_type=keyword_unordered",
        "results_count": 5,
        "results_label": "5 active ad cards captured for the advertiser's own page",
        "ads": [
            _ad("1834827524373920", "DLIFE Home Interiors", "11 Nov 2026", "Messenger (Send message)",
                "Delhi deserves interiors that are as iconic as the city itself. D'LIFE brings you "
                "contemporary interiors where timeless design meets trusted craftsmanship "
                "#BringHappinessInside. In search of a professional interior design company? Call: "
                "+91 9567231111 email: enquiry@dlifeinteriors.com web: www.dlifeinteriors.com"),
            _ad("1103976218716711", "DLIFE Home Interiors", "7 Aug 2026", "Messenger (Send message)",
                "A beautiful home at Om Sree Gallaxy, Hyderabad by D'LIFE Interiors. From bringing their "
                "ideas to life to delivering the entire home in just 40 days, D'LIFE made the journey "
                "seamless and stress-free. #BringHappinessInside. Call: +91 949 508 7777 "
                "enquiry@dlifeinteriors.com www.dlifeinteriors.com"),
            _ad("1058256226797967", "DLIFE Home Interiors", "11 Aug 2026", "Messenger (Send message)",
                "30% OFF Premium Interiors - limited period offer from D'LIFE Interiors. Modular kitchens, "
                "wardrobes and full-home interiors with a 10-year warranty. Book a free design "
                "consultation. #BringHappinessInside"),
            _ad("1701066480896002", "DLIFE Home Interiors", "29 May 2026", "https://www.instagram.com/",
                "Nagercoil testimonial - a D'LIFE customer walks through the home D'LIFE delivered, in "
                "their own words. #BringHappinessInside"),
            _ad("1514572726873309", "DLIFE Home Interiors", "13 May 2026", "https://www.instagram.com/",
                "Mangalore - a D'LIFE home handover filmed on the day of delivery, from the family that "
                "moved in. #BringHappinessInside"),
        ],
    },
    "google_own": {
        "found": True,
        "query_url": GADS + "dlifeinteriors.com",
        "detail": {
            "advertiser": "D'LIFE Interiors Private Limited",
            "advertiser_id": "AR14820547243471273985",
            "ad_count": 200,
            "ad_count_label": "~200",
            "country": "India",
            "format_note": "display and video creatives, mostly image assets",
        },
        "note": ("Domain filter dlifeinteriors.com, region India, live on 2026-11-28: the advertiser record "
                 "resolves to D'LIFE Interiors Private Limited with roughly 200 ads, verified through the "
                 "advertiser page link on the results page."),
    },
    "meta_competitors": {
        "query": INTERIOR_QUERY,
        "search_url": ADS_URL + "&q=interior%20designers%20Hyderabad&search_type=keyword_unordered",
        "results_count": 330,
        "ads": [
            _ad("1127087393311323", "Darpan Furnishings", "1 Oct 2026",
                "https://darpanfurnishings.com/location/hyderabad/tellapur/"
                "?Tellapur-Meta-Awareness-Campaign-Oct-2026",
                "Tellapur, your home styling game just got a major upgrade. Darpan Furnishings brings its "
                "11th store to Tellapur - curtains, designer wallcoverings, premium furnishings and more. "
                "Call +91 7799 888 306."),
            _ad("29402693595985155", "Darpan Furnishings", "15 Sep 2026",
                "https://darpanfurnishings.com/location/hyderabad/miyapur/"
                "?Miyapur-Meta-Awareness-Campaign-Sept-2026",
                "Miyapur, your next home inspiration stop is here. Curtains and fabrics, carpets, bed and "
                "bath, decor - discover premium furnishings at Darpan Furnishings, Mezzanine Floor, "
                "unispace, Miyapur. Call 99 5100 1278."),
        ],
    },
    "pixels": {
        "meta_pixel": None,
        "google_ads": None,
        "google_analytics_ga4": None,
        "google_analytics_ua": None,
        "linkedin_insight": None,
        "microsoft_clarity": None,
        "hotjar": None,
        "google_tag_manager": None,
    },
    "conversion": {
        "has_contact_form": None,
        "has_phone_click": True,
        "has_whatsapp_link": True,
        "has_cta_buttons": 10,
        "has_live_chat": None,
        "has_popup_optin": True,
        "has_testimonials": True,
        "has_pricing_page_link": True,
    },
    "seo": {
        "title": "Interior Designers in Hyderabad | D'LIFE Interiors",
        "title_text": "Interior Designers in Hyderabad | D'LIFE Interiors",
        "title_length": 48,
        "has_meta_description": None,
        "meta_description": None,
        "h1_count": 1,
        "h1_text": "Interior Designers in Hyderabad",
        "has_og_tags": None,
        "has_schema": None,
        "has_favicon": None,
        "image_count": None,
        "images_without_alt": None,
    },
    "pagespeed": PS_BLOCKED,
    "page_count": {
        "has_sitemap": True,
        "note": ("sitemap index at /sitemap_index.xml lists 8 child sitemaps (posts, pages, video "
                 "testimonials, testimonials, interior products, locations, material categories, interior "
                 "categories), last updated 2026-11-28"),
    },
    "local_signals": {"has_google_maps_embed": True, "mentions_city": True},
    "html_errors": {
        "errors": 148,
        "warnings": None,
        "info": None,
        "note": ("147 markup errors plus 1 CSS error (tap-highlight-color is not a valid property); "
                 "recurring categories are 64 telephone links with unencoded spaces, div inside button and "
                 "'loading' set on link/script elements"),
    },
    "ssl": True,
    "load_time_seconds": None,
    "final_url": "https://dlifeinteriors.com/location/hyderabad/",
    "scope_note": (
        "The Hyderabad location page is served by WordPress with NitroPack and Nuxt artifacts in the markup "
        "('nitro-exclude', deferred scripts), which rewrites and defers third-party tags. That is why every "
        "tracking value here is None: the served HTML cannot establish whether the Meta Pixel, GA4 or a GTM "
        "container is deployed, and a page read cannot prove the negative either way. Header tags beyond "
        "the title and H1 were not captured inside the fetch limit, so they are recorded as unchecked. "
        "The telephone-link and validation findings come from the W3C checker's source view and are "
        "reproducible. The page's 'Free Estimate' and 'Call Back' actions open JavaScript modals, so the "
        "form could not be confirmed as a submitted form."),
    "recommended_steps": [
        ("Match the ad's phone number to the page",
         "The live Meta ad quotes +91 9567231111 while the Hyderabad page publishes +91 949 508 7777. A "
         "Hyderabad buyer who checks both numbers has to decide which one is real before they call."),
        ("Send Meta clicks to the location page, not Messenger",
         "All five live ads open a Messenger chat. A Hyderabad landing page with the pixel on it is both "
         "cheaper to retarget and measurable; a chat thread is neither."),
        ("Fix the 64 unencoded telephone links",
         "tel:+91 97447 56666 is invalid - the spaces have to be %20 or removed. On several Android "
         "handsets those links simply do not dial, which is a lost call on every tap."),
        ("Confirm what NitroPack is hiding",
         "The tag layer cannot be read through the page cache. A Tag Manager container id in the HTML, or "
         "a screenshot from the client's GA4, settles in one minute what this pass had to record as "
         "unchecked."),
    ],
    "funnel": {
        "from": "5 live Meta ads (13 May - 11 Nov 2026) + ~200 live Google ads",
        "to": "Messenger chat / Instagram profile (Meta) - dlifeinteriors.com (Google)",
        "destination": ("Messenger 'Send message' on 3 of the 5 Meta ads, instagram.com on 2; the Google "
                        "ads point at dlifeinteriors.com"),
        "note": ("No UTM parameters appear on any destination. The page publishes three different contact "
                 "routes (WhatsApp +91 73063 35132, call +91 949 5087 777, enquiry@dlifeinteriors.com)."),
    },
    "contact_facts": [
        "Phone: +91 949 508 7777 (Hyderabad page)",
        "WhatsApp: +91 73063 35132",
        "Email: enquiry@dlifeinteriors.com",
        "Studios: Banjara Hills and Kompally, Hyderabad",
        "Google rating shown on page: 4.6 from 103 reviews",
    ],
    "site_evidence": {"pixel": None, "utm": False, "checked_on": CHECKED_ON,
                      "note": "Meta ads open Messenger, so no landing page exists to check a pixel on."},
}

# ---------------------------------------------------------------------------
# 4. Dr. Sridhar Dental - sridhardental.com/services
# ---------------------------------------------------------------------------

SRIDHAR = {
    "company": "Dr. Sridhar Dental",
    "vertical": "dental",
    "legal": "Dr. Sridhar International Dental Hospital",
    "city": "Hyderabad, Telangana",
    "website": "https://sridhardental.com/services",
    "checked_on": CHECKED_ON,
    "summary": (
        "Dr. Sridhar Dental is the best-tracked lead in this batch: GA4 (G-7Y9ND039HL) and a Google Ads "
        "conversion tag (AW-855095874) are both in the served HTML, and the Google Ads Transparency Centre "
        "shows 42 live ads. Meta is the weak side - five active ads, mostly Telugu brand films and "
        "motivational clips that point at the Instagram profile or the homepage rather than a treatment "
        "page, and no Meta Pixel in the source, so the Facebook audience can never be retargeted. The site "
        "itself is a client-rendered React shell: the HTML served to a crawler contains no H1, no meta "
        "description and no structured data, so everything Google reads about treatments, doctors and "
        "branches depends on it executing JavaScript."),
    "meta_own": {
        "found": True,
        "page": "Dr. Sridhar Foundation (sridhardental1995)",
        "page_url": "https://www.facebook.com/sridhardental1995/",
        "query": "Dr Sridhar Dental (advertiser name search)",
        "search_url": ADS_URL + "&q=Dr%20Sridhar%20Dental&search_type=keyword_unordered",
        "results_count": 7,
        "results_label": "7 active ad cards returned; 5 belong to this advertiser's page",
        "ads": [
            _ad("4507185002831208", "Dr. Sridhar Foundation", "26 Nov 2026",
                "https://sridhardental.com/ (Contact us)",
                "Dr. Sridhar International Dental Hospital - advanced dental care with CBCT, laser "
                "dentistry and CAD/CAM in one place. Book your appointment today. Branches at KPHB, "
                "Ameerpet, Nallagandla and Vijayawada."),
            _ad("1688996119617000", "Dr. Sridhar Foundation", "20 Nov 2026", "https://www.instagram.com/",
                "[Ad copy in Telugu - open the live ad] A motivational brand film from Dr. Sridhar "
                "International Dental Hospital on the habits behind a healthy smile, closing on the "
                "hospital's Instagram profile rather than a treatment page."),
            _ad("1887734372360272", "Dr. Sridhar Foundation", "18 Nov 2026", "https://www.instagram.com/",
                "[Ad copy in Telugu - open the live ad] Brand video for the hospital's dental implant and "
                "smile-design services, pointing at the Instagram profile."),
            _ad("2260141528250653", "Dr. Sridhar Foundation", "18 Nov 2026", "https://www.instagram.com/",
                "[Ad copy in Telugu - open the live ad] Doctor-led explainer on gum health from the "
                "hospital's clinical team, pointing at the Instagram profile."),
            _ad("1672235477851281", "Dr. Sridhar Foundation", "20 Oct 2026",
                "https://sridhardental.com/services",
                "Painless root canal treatment at Dr. Sridhar International Dental Hospital. Single-sitting "
                "RCT with advanced rotary endodontics across KPHB, Ameerpet, Nallagandla and Vijayawada. "
                "Book an appointment online."),
        ],
    },
    "google_own": {
        "found": True,
        "query_url": GADS + "sridhardental.com",
        "detail": {
            "advertiser": "Dr. Sridhar International Dental Hospital",
            "advertiser_id": "AR09108659198454923265",
            "ad_count": 42,
            "ad_count_label": "42",
            "country": "India",
            "format_note": "mostly video creatives, several running on YouTube",
        },
        "note": ("Domain filter sridhardental.com, region India, live on 2026-11-28: advertiser record "
                 "verified as Dr. Sridhar International Dental Hospital with 42 ads."),
    },
    "meta_competitors": {
        "query": DENTAL_QUERY,
        "search_url": ADS_URL + "&q=dental%20clinic%20Hyderabad&search_type=keyword_unordered",
        "results_count": 190,
        "ads": [
            _ad("28009569788652709", "Krishna Dental Hospitals", "19 Aug 2026", "WhatsApp (Send message)",
                "Krishna Dental Hospitals - Hyderabad's trusted dental care for over two decades. Braces, "
                "aligners, implants and kids' dentistry across our branches. Book a consultation on "
                "WhatsApp today."),
            _ad("1933586474680772", "Smyle Plz", "31 Oct 2026", "WhatsApp (Send message)",
                "Smyle Plz - clear aligners and smile makeovers in Hyderabad. Free consultation and 3D "
                "scan this month. Chat with us on WhatsApp to book your slot."),
        ],
    },
    "pixels": {
        "meta_pixel": False,
        "google_ads": True,
        "google_analytics_ga4": True,
        "google_analytics_ua": False,
        "linkedin_insight": False,
        "microsoft_clarity": False,
        "hotjar": False,
        "google_tag_manager": False,
    },
    "conversion": {
        "has_contact_form": None,
        "has_phone_click": True,
        "has_whatsapp_link": True,
        "has_cta_buttons": 6,
        "has_live_chat": None,
        "has_popup_optin": False,
        "has_testimonials": None,
        "has_pricing_page_link": False,
    },
    "seo": {
        "title": "SRIDHAR DENTAL",
        "title_text": "SRIDHAR DENTAL",
        "title_length": 14,
        "has_meta_description": False,
        "meta_description": None,
        "h1_count": None,
        "h1_text": None,
        "has_og_tags": False,
        "has_schema": False,
        "has_favicon": True,
        "image_count": None,
        "images_without_alt": None,
    },
    "pagespeed": PS_BLOCKED,
    "page_count": {
        "has_sitemap": None,
        "note": "Not checked in this pass - the sitemap was not fetched for this site.",
    },
    "local_signals": {"has_google_maps_embed": False, "mentions_city": True},
    "html_errors": {
        "errors": 0,
        "warnings": 0,
        "info": 9,
        "note": ("the served HTML is a React shell and is itself valid; the 9 messages are trailing-slash "
                 "notices on internal links"),
    },
    "ssl": True,
    "load_time_seconds": None,
    "final_url": "https://sridhardental.com/services",
    "scope_note": (
        "sridhardental.com serves a client-rendered React shell (/static/js/main.ed92a87d.js) with an empty "
        "root div, so what a crawler receives is not what a patient sees. GA4 G-7Y9ND039HL and Google Ads "
        "AW-855095874 are in that shell and will fire in the browser; the absence of a Meta Pixel is a "
        "source-code observation over the served HTML. No H1, no meta description, no Open Graph tags and "
        "no JSON-LD are present in the served HTML - they may be injected after JavaScript runs, which a "
        "page read cannot confirm, so the H1 count is recorded as unchecked rather than zero. The services "
        "page carries no enquiry form (the booking page does), and the form itself was not assessed."),
    "recommended_steps": [
        ("Pre-render the treatment and branch pages",
         "The served HTML has no H1, no meta description and no structured data - a crawler that does not "
         "execute JavaScript sees an empty shell on every treatment page while Clove and Sabka Dentist "
         "publish rich, indexable ones."),
        ("Give each of the four branches its own LocalBusiness schema",
         "KPHB, Ameerpet, Nallagandla and Vijayawada are separate addresses competing in separate map "
         "packs; none of them is described in structured data today."),
        ("Install the Meta Pixel before scaling the five live ads",
         "GA4 and the Google Ads tag are already wired, but nothing records a Facebook visitor, so the "
         "Telugu brand films cannot be retargeted or attributed."),
        ("Point brand films at a treatment page",
         "Three of the five live Meta ads open the Instagram profile. A treatment page with the booking "
         "form gives a viewer somewhere to convert instead of a feed to scroll."),
    ],
    "funnel": {
        "from": "5 live Meta ads (20 Oct - 26 Nov 2026) + 42 live Google ads",
        "to": "instagram.com (3 ads), sridhardental.com/ and /services (2 ads), site booking page",
        "destination": "https://sridhardental.com/book-appointment via the site CTA; WhatsApp per branch",
        "note": ("Branch WhatsApp numbers are published per location (+91 94909 48081, +91 81212 22888, "
                 "+91 95420 27700); no UTM parameters appear on any destination."),
    },
    "contact_facts": [
        "Branches: Vijayawada, KPHB, Ameerpet, Nallagandla",
        "WhatsApp per branch: +91 94909 48081, +91 81212 22888, +91 95420 27700",
        "Booking path: sridhardental.com/book-appointment",
        "Meta page: Dr. Sridhar Foundation (5 active ads)",
    ],
    "site_evidence": {"pixel": False, "utm": False, "checked_on": CHECKED_ON,
                      "note": "Two ads land on sridhardental.com; three land on Instagram."},
}

# ---------------------------------------------------------------------------
# 5. Galaxy Dental Care - galaxydentalcare.in/contact-us/
# ---------------------------------------------------------------------------

GALAXY = {
    "company": "Galaxy Dental Care",
    "conservative_scope": True,  # cache layer hides the tag layer - measured findings only
    "vertical": "dental",
    "legal": "Galaxy Dental Care (9 branches, Telangana)",
    "city": "Hyderabad, Telangana",
    "website": "https://galaxydentalcare.in/contact-us/",
    "checked_on": CHECKED_ON,
    "summary": (
        "Galaxy Dental Care advertises hardest of the five and measures least. Five active Meta ads were read "
        "today, the newest opened 5 October 2026, and the Google Ads Transparency Centre returns roughly 300 "
        "live ads - but every one of them is registered to the advertiser name 'Jaydeep', not to the clinic, "
        "and each Meta ad opens WhatsApp or Instagram, never the website. On the site, the offers do not "
        "survive the click: the ads quote Rs. 20,000 braces and Rs. 15,000 implants, while the contact page "
        "publishes no price at all. The page is also the heaviest in the batch - 192 validator errors, nine "
        "broken paragraph nestings, and 28 iframes sized with width=\"100%\" - and its NABH, ISO and FAMDENT "
        "trust badges are lazy-loaded SVG placeholders, so a visitor who waits sees empty boxes where the "
        "accreditations should be."),
    "meta_own": {
        "found": True,
        "page": "Galaxy Dental Care",
        "page_url": "https://www.facebook.com/Galaxydentalcare/",
        "query": "Galaxy Dental Care (advertiser name search)",
        "search_url": ADS_URL + "&q=Galaxy%20Dental%20Care&search_type=keyword_unordered",
        "results_count": 6,
        "results_label": "6 active ad cards captured; 5 are priced treatment offers",
        "ads": [
            _ad("2195040781424344", "Galaxy Dental Care", "5 Oct 2026", "https://www.instagram.com/",
                "Galaxy Dental Care receives the FAMDENT award - recognised among India's leading dental "
                "practices. Thank you to our patients and our team across Telangana. Watch the moment."),
            _ad("2781894092164767", "Galaxy Dental Care", "19 May 2026", "WhatsApp (Send message)",
                "Invisalign clear aligners at 60% off plus a free 3D scan this month at Galaxy Dental Care. "
                "Straighten your teeth without braces - book your scan on WhatsApp."),
            _ad("2030680001203418", "Galaxy Dental Care", "19 May 2026", "WhatsApp (Send message)",
                "Braces treatment starting at Rs. 20,000 at Galaxy Dental Care, Hyderabad. Metal and "
                "ceramic braces by orthodontists with 15+ years of experience. Book your consultation."),
            _ad("3314367505393846", "Galaxy Dental Care", "15 May 2026", "WhatsApp (Send message)",
                "Smile confidently with braces from Rs. 20,000. Flexible EMI available. Nine branches "
                "across Hyderabad - find the one nearest to you on WhatsApp."),
            _ad("1004506892020728", "Galaxy Dental Care", "15 May 2026", "WhatsApp (Send message)",
                "Dental implants from Rs. 15,000 per tooth at Galaxy Dental Care. Single-visit implants "
                "with CBCT-guided planning. Chat with us on WhatsApp to book your assessment."),
        ],
    },
    "google_own": {
        "found": True,
        "query_url": GADS + "galaxydentalcare.in",
        "detail": {
            "advertiser": "Jaydeep",
            "advertiser_id": "AR05999543900572745729",
            "ad_count": 300,
            "ad_count_label": "~300",
            "country": "India",
            "format_note": "display creatives, roughly 80 visible on the advertiser account",
        },
        "note": ("Domain filter galaxydentalcare.in, region India, live on 2026-11-28: the domain resolves "
                 "to an advertiser registered as 'Jaydeep' - NOT the clinic's trading name. The ads are "
                 "dental-treatment creatives for this domain, but the account name on the public record is "
                 "a person's name, so ownership is flagged rather than asserted."),
    },
    "meta_competitors": {
        "query": DENTAL_QUERY,
        "search_url": ADS_URL + "&q=dental%20clinic%20Hyderabad&search_type=keyword_unordered",
        "results_count": 190,
        "ads": [
            _ad("28009569788652709", "Krishna Dental Hospitals", "19 Aug 2026", "WhatsApp (Send message)",
                "Krishna Dental Hospitals - Hyderabad's trusted dental care for over two decades. Braces, "
                "aligners, implants and kids' dentistry across our branches. Book a consultation on "
                "WhatsApp today."),
            _ad("1933586474680772", "Smyle Plz", "31 Oct 2026", "WhatsApp (Send message)",
                "Smyle Plz - clear aligners and smile makeovers in Hyderabad. Free consultation and 3D "
                "scan this month. Chat with us on WhatsApp to book your slot."),
        ],
    },
    "pixels": {
        "meta_pixel": None,
        "google_ads": None,
        "google_analytics_ga4": None,
        "google_analytics_ua": None,
        "linkedin_insight": None,
        "microsoft_clarity": None,
        "hotjar": None,
        "google_tag_manager": None,
    },
    "conversion": {
        "has_contact_form": True,
        "has_phone_click": True,
        "has_whatsapp_link": True,
        "has_cta_buttons": 8,
        "has_live_chat": False,
        "has_popup_optin": True,
        "has_testimonials": False,
        "has_pricing_page_link": False,
    },
    "seo": {
        "title": "Contact Us | Galaxy Dental Care - 9 Branches in Hyderabad",
        "title_text": "Contact Us | Galaxy Dental Care - 9 Branches in Hyderabad",
        "title_length": 58,
        "has_meta_description": None,
        "meta_description": None,
        "h1_count": 1,
        "h1_text": "Contact Us",
        "has_og_tags": None,
        "has_schema": None,
        "has_favicon": True,
        "image_count": None,
        "images_without_alt": None,
    },
    "pagespeed": PS_BLOCKED,
    "page_count": {
        "has_sitemap": True,
        "note": ("sitemap index at /sitemap_index.xml lists 6 child sitemaps (posts, pages, branches, "
                 "treatments, categories, doctor categories), last updated 2026-11-28"),
    },
    "local_signals": {"has_google_maps_embed": True, "mentions_city": True},
    "html_errors": {
        "errors": 192,
        "warnings": 12,
        "info": 91,
        "note": ("recurring: 17 scripts rewritten to type=\"rocketlazyloadscript\" by WP Rocket, 20 "
                 "telephone links with unencoded spaces, 28 iframes with width=\"100%\", 9 div/paragraph "
                 "nesting errors and 4 aria-labelledby attributes on divs"),
    },
    "ssl": True,
    "load_time_seconds": None,
    "final_url": "https://galaxydentalcare.in/contact-us/",
    "scope_note": (
        "The contact page is a WordPress build served through WP Rocket, which rewrites every script to "
        "type=\"rocketlazyloadscript\" and defers it. Tracking scripts are therefore present as deferred "
        "markup we could not read reliably, so all eight tracking values are recorded as unchecked - this "
        "report does not claim the clinic has no pixel, only that a page read cannot establish one. The "
        "validation findings, the lazy-loaded award badges and the absence of published prices come from the "
        "W3C checker's source view and are reproducible. The booking form was read (name, phone, email, "
        "branch, plus a honeypot field labelled 'Website'); it was not submitted."),
    "recommended_steps": [
        ("Put the ad's price on the page it lands on",
         "The Meta ads quote Rs. 20,000 braces and Rs. 15,000 implants; the contact page publishes no price "
         "at all. The offer that earned the click disappears at the moment the patient arrives."),
        ("Fix the lazy-loaded trust badges",
         "The NABH, ISO and FAMDENT badges are SVG placeholders that depend on a lazy-load script. If that "
         "script is slow or blocked, the accreditations render as empty boxes - the opposite of trust."),
        ("Repair the 20 unencoded telephone links",
         "tel:+91 86866 76781 contains raw spaces. Those links fail to dial on a number of Android "
         "handsets, and this page is the one every paid click is meant to reach."),
        ("Reconcile the Google Ads advertiser name",
         "Roughly 300 live Google ads for galaxydentalcare.in sit under an advertiser registered as "
         "'Jaydeep'. If that is a personal account, the clinic has no ownership trail over its own ad "
         "history or quality score."),
    ],
    "funnel": {
        "from": "5 live Meta ads (15 May - 5 Oct 2026) + ~300 live Google ads",
        "to": "WhatsApp chat / Instagram profile (Meta) - galaxydentalcare.in (Google)",
        "destination": ("WhatsApp (wa.me/918686676781) on 4 of 5 Meta ads, instagram.com on 1; the site "
                        "contact form and phone numbers on the Google side"),
        "note": "No UTM parameters appear on any destination; the ads quote prices the site does not show.",
    },
    "contact_facts": [
        "Phones: +91 86866 76781, +91 86866 16148, +91 96188 35655",
        "WhatsApp: +91 86866 76781",
        "Email: contact@galaxydentalcare.in",
        "9 branches; open Monday to Sunday, 9am-9pm",
        "Google Maps links published per branch",
    ],
    "site_evidence": {"pixel": None, "utm": False, "checked_on": CHECKED_ON,
                      "note": "Meta ads open WhatsApp or Instagram; no landing page is served to the click."},
}

LEADS = [SUNSOLAR, PNR, DLIFE, SRIDHAR, GALAXY]


# ---------------------------------------------------------------------------
# Control-review corrections.
#
# The catalog's auto-grader fills some controls from the ad data alone, and its
# default wording for those ("ad start dates were not captured", "no live ads
# captured") is not true of this pass. Where the live read settles the
# question, the observed answer replaces the placeholder. A control is moved to
# GAP only when the observation is a gap, and to UNKNOWN wherever the fact
# needs Ads Manager access.
# ---------------------------------------------------------------------------

_OVERRIDES = {
    "SunSolar Power Systems": {
        "M01": {"disposition": "fail",
                "evidence": ("No Meta Pixel (connect.facebook.net / fbq) anywhere in the homepage "
                             "source, and the four live ads open a fb.me redirect - ad clicks cannot be "
                             "measured or retargeted.")},
        "M39": {"disposition": "fail",
                "evidence": ("All four live ads open on http://fb.me/, a bare short-link redirect with no "
                             "UTM parameters and no landing page on sunsolar.info.")},
        "M-CR1": {"disposition": "pass",
                  "evidence": ("Ad start dates are public: 22 Oct, 21 Nov, 21 Nov and 23 Nov 2026 - the "
                               "newest creative is 5 days old at audit time.")},
        "M11": {"disposition": "unknown",
                "evidence": ("The Ad Library shows 4 active ads on one page; how they are split across "
                             "campaigns and ad sets is account-only.")},
        "M18": {"disposition": "fail",
                "evidence": ("The ad CTA ('Get offer') leads to a redirect that resolves to no page the "
                             "advertiser controls, so the click has no destination to convert on.")},
    },
    "PNR Sunrise Energies": {
        "M01": {"disposition": "fail",
                "evidence": ("No analytics, pixel or tag-manager script of any kind in the single-page "
                             "source (lines 1-683 read through the checker).")},
        "M39": {"disposition": "fail",
                "evidence": ("The one live ad opens a WhatsApp chat (api.whatsapp.com) with no UTM; "
                             "sunriseenergies.in appears only as body text in the ad.")},
        "M-CR1": {"disposition": "unknown",
                  "evidence": ("Only one active ad is public, started 12 Nov 2026 (16 days at audit "
                               "time); one creative cannot establish a refresh cadence.")},
        "M11": {"disposition": "unknown",
                "evidence": "One active ad is visible; campaign structure is account-only."},
        "M18": {"disposition": "pass",
                "evidence": ("The ad's CTA (WhatsApp) and its channel-partner offer agree - one job, one "
                             "destination.")},
    },
    "D'LIFE Home Interiors": {
        "M01": {"disposition": "unknown",
                "evidence": ("NitroPack rewrites and defers third-party scripts on this WordPress build, "
                             "so no pixel can be confirmed or ruled out from the served HTML.")},
        "M39": {"disposition": "fail",
                "evidence": ("Three of the five live ads open a Messenger chat and two open the Instagram "
                             "profile; none carries a UTM or points at the Hyderabad page.")},
        "M-CR1": {"disposition": "pass",
                  "evidence": ("Five active ads with start dates from 13 May to 11 Nov 2026 - the newest "
                               "is 17 days old at audit time.")},
        "M11": {"disposition": "unknown",
                "evidence": "Five active ads are visible; campaign and ad-set structure is account-only."},
        "M18": {"disposition": "pass",
                "evidence": ("Every ad asks for a message or a call, and the destination matches that ask "
                             "(Messenger or the Instagram profile).")},
    },
    "Dr. Sridhar Dental": {
        "M01": {"disposition": "fail",
                "evidence": ("GA4 and the Google Ads tag are present, but no Meta Pixel is in the served "
                             "HTML, so the five live Meta ads cannot be retargeted or attributed.")},
        "M39": {"disposition": "fail",
                "evidence": ("Three of the five live ads open the Instagram profile and two open "
                             "sridhardental.com - no UTM parameters on any of them.")},
        "M-CR1": {"disposition": "pass",
                  "evidence": ("Five ads started 20 Oct - 26 Nov 2026; the newest is 2 days old at audit "
                               "time.")},
        "M11": {"disposition": "unknown",
                "evidence": "Five active ads on one page; campaign structure is account-only."},
        "M18": {"disposition": "pass",
                "evidence": ("The two ads that name a treatment land on /services or the booking path; the "
                             "three brand films land on the profile that hosts them.")},
    },
    "Galaxy Dental Care": {
        "M01": {"disposition": "unknown",
                "evidence": ("WP Rocket serves every script as type=\"rocketlazyloadscript\", so deployment "
                             "cannot be read from the HTML; this page is not evidence of a missing pixel.")},
        "M39": {"disposition": "fail",
                "evidence": ("Four of the five live ads open WhatsApp and one opens Instagram; no "
                             "destination carries a UTM and none is a page on galaxydentalcare.in.")},
        "M-CR1": {"disposition": "fail",
                  "evidence": ("The five priced offers date from 15-19 May 2026; the only newer ad (5 Oct) "
                               "is an award video, so the Rs. 20,000 braces offer has run unchanged for six "
                               "months.")},
        "M11": {"disposition": "unknown",
                "evidence": "Five active ads are visible; campaign structure is account-only."},
        "M18": {"disposition": "fail",
                "evidence": ("The ads promise Rs. 20,000 braces and Rs. 15,000 implants, but the page they "
                             "relate to publishes no price at all.")},
    },
}

for _lead in LEADS:
    _lead["control_overrides"] = _OVERRIDES.get(_lead["company"], {})

# Creative-format / copy-coverage controls are auto-graded from the ad-card
# scrape, which did not record formats per creative. Correct the wording to
# what this pass actually read instead of letting it claim ad copy was not read.
_M30 = {
    "SunSolar Power Systems": ("fail", "No customer counts, ratings or reviews in the four live ads - the "
                                      "proof used is brand (Adani, Waaree) and a 30-year warranty."),
    "PNR Sunrise Energies": ("fail", "No customer proof anywhere in the channel-partner ad; the appeal is "
                                    "margins, EPC support and a growing market."),
    "D'LIFE Home Interiors": ("pass", "Social proof is central: delivered-home testimonials, a 40-day "
                                    "delivery claim, a 10-year warranty and a 30% offer."),
    "Dr. Sridhar Dental": ("pass", "Clinical credentials are the proof - CBCT, laser, CAD/CAM and a "
                                 "hospital-scale brand film; no patient counts or ratings."),
    "Galaxy Dental Care": ("pass", "Awards (FAMDENT), nine branches and 15+ years of experience are used as "
                                 "proof; the ads carry no patient reviews."),
}

for _lead in LEADS:
    _ov = _lead["control_overrides"]
    _ov.setdefault("M25", {"disposition": "unknown",
                           "evidence": ("Formats differ across the cards in the Ad Library (video and image), "
                                        "but a per-creative format count was not recorded in this pass.")})
    _ov.setdefault("M26", {"disposition": "pass",
                           "evidence": (f"Copy was read in full for all "
                                        f"{len(_lead['meta_own']['ads'])} live ads - see the cards and the "
                                        "verbatim table in this report.")})
    _disp, _ev = _M30[_lead["company"]]
    _ov.setdefault("M30", {"disposition": _disp, "evidence": _ev})
