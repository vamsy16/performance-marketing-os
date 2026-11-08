#!/usr/bin/env python3
"""Build the three batch-6 FULL audit JSONs (Ecolt, Orizen, Ray On).

Every value below was verified live on 2026-10-21:
  - pixels/seo/conversion/page_count: read line-by-line from each site's raw
    source via the W3C Nu Html Checker source view (validator.w3.org/nu/
    ?doc=<url>&showsource=yes) - complete head + body + wp_head + footer read
    for all three sites.
  - own Meta ads: verified live in the Meta Ad Library (same Library IDs as the
    batch-6 ads-only reports).
  - own Google ads: verified in Google's Ads Transparency Center today
    (Orizen 1 ad / Ecolt 0 ads / Ray On 0 ads).
  - competitor Meta ads: verified live today in the Ad Library
    (Telugu query 'solar subsidy', ~180 results).
  - competitor Google ads: WAAREE verified live today; Venus + Orbit verified
    2026-10-18 (date noted in the notes).
  - pagespeed: PageSpeed/Lighthouse API not reachable from this sandbox -
    rendered honestly as unavailable (Ksquare precedent).
"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE, "audit_results")
DATE = "2026-10-21"

META_LIB_URL = ("https://www.facebook.com/ads/library/?active_status=active&ad_type=all"
                "&country=IN&q={}&search_type=keyword_unordered")

# ---- competitor ads verified LIVE today (Telugu 'solar subsidy' query) -------
COMPETITORS = [
    {
        "library_id": "28876616218695042",
        "page_name": "Eastman New Energy Private Limited",
        "started": "Sep 29, 2026",
        "text": ("Telugu: Under the PM Surya Ghar Muft Bijli Yojana, switch to Eastman hybrid solar "
                 "solutions and get a Rs.78,000* subsidy plus an additional state subsidy. Eastman hybrid "
                 "inverters with lithium batteries for 24x7 power. Call today: 80016 80016."),
        "image_urls": [
            "https://scontent-lax7-1.xx.fbcdn.net/v/t39.35426-6/787743815_1093982023611103_119215054499862290_n.jpg?stp=dst-jpg_s600x600_tt6&_nc_cat=101&ccb=1-7&_nc_sid=c53f8f&_nc_ohc=0bmg7Do2z1gQ7kNvwEb_z_l&_nc_oc=AdolFdyb6_FPR7afVdiq50D3zxRGNXxp4TMcH7Eet-Bu0EjHwZ3YZ1FyVVg1YB14Jvw&_nc_zt=14&_nc_ht=scontent-lax7-1.xx&_nc_gid=ExwgK2RLbzZfzDAuGfYJpQ&_nc_ss=7b289&oh=00_AQNx0IBDiX8FWT6coAqreS6gVaXIHDqrgYZa6jXwCk3hiA&oe=6ADDE721"
        ],
        "images": [],
        "library_url": "https://www.facebook.com/ads/library/?id=28876616218695042",
    },
    {
        "library_id": "1454295123168911",
        "page_name": "Sri Balaji Solar Energies",
        "started": "May 29, 2026",
        "text": ("Telugu: Say goodbye to big current bills! Get the best solar plan and subsidy details "
                 "for your home. Sri Balaji Solar Energies (15 years legacy). Leave your details - our "
                 "experts will call you."),
        "image_urls": [
            "https://scontent-lax7-1.xx.fbcdn.net/v/t39.35426-6/657034938_1472739317629903_7932454137442148511_n.jpg?stp=dst-jpg_s600x600_tt6&_nc_cat=109&ccb=1-7&_nc_sid=c53f8f&_nc_ohc=UHpdMPmZNj8Q7kNvwErTghS&_nc_oc=Ado3n02xjI_pFJlMRVaj22mk83i22E0TTriEwQgxZ7hUU8HQs5qkRaNC69bQ5LAOZcM&_nc_zt=14&_nc_ht=scontent-lax7-1.xx&_nc_gid=ExwgK2RLbzZfzDAuGfYJpQ&_nc_ss=7b289&oh=00_AQNlWfzyIg5WN3T-HXW2MGYIAmQuy0pc3EP625ypG_oA_g&oe=6ADDEDF2"
        ],
        "images": [],
        "library_url": "https://www.facebook.com/ads/library/?id=1454295123168911",
    },
    {
        "library_id": "2046407626037554",
        "page_name": "FreyrEnergy",
        "started": "Oct 13, 2026",
        "text": ("Telugu: Still paying high electricity bills? Switch to Freyr Energy smart solar "
                 "solutions and save up to Rs.1 lakh total with the Rs.78,000 government subsidy plus a "
                 "special Rs.22,000 Freyr Energy discount. 24x7 support, automated self-cleaning "
                 "sprinklers, track performance in the Freyr Energy App. 4.7 star Google rating."),
        "image_urls": [
            "https://scontent-lax7-1.xx.fbcdn.net/v/t39.35426-6/770719966_1825935338388582_5013599579577659041_n.jpg?stp=dst-jpg_s600x600_tt6&_nc_cat=110&ccb=1-7&_nc_sid=c53f8f&_nc_ohc=uShWOgb_4D4Q7kNvwGwksly&_nc_oc=Adqxr68sTTQBB68RRWXoxpe0P_gHJQqKOQwP-X8VQB5NfQqmNV9-vj1l8DF_a_1QJ3c&_nc_zt=14&_nc_ht=scontent-lax7-1.xx&_nc_gid=ExwgK2RLbzZfzDAuGfYJpQ&_nc_ss=7b289&oh=00_AQ7DNQxlzmImdI1fGTxa8Z2ml_u0ZbW6sH6zwHOhRz5Eg&oe=6ADDF534"
        ],
        "images": [],
        "library_url": "https://www.facebook.com/ads/library/?id=2046407626037554",
    },
]

META_COMP = {
    "query": "solar subsidy (Telugu)",
    "results_label": "~180 results",
    "results_count": 180,
    "ads": COMPETITORS,
    "url": ("https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=IN"
            "&q=%E0%B8%B8%E0%B0%B8%E0%B0%BE%E0%B0%B2%E0%B0%BE%E0%B0%B0%E0%B1%8D%20%E0%B0%B8%E0%B0%AC%E0%B0%B8%E0%B0%BF%E0%B0%A1%E0%B1%80&search_type=keyword_unordered"),
    "found": True,
}

# ---- Google competitors ------------------------------------------------------
# WAAREE verified LIVE in the transparency centre today (2026-10-21); Venus and
# Orbit verified 2026-10-18 (same centre) - verification dates stated in notes.
GOOGLE_COMP = {
    "found": True,
    "advertisers": [
        {
            "name": "WAAREE ENERGIES LIMITED",
            "country": "IN",
            "ad_count": 200,
            "detail": {
                "name": "WAAREE ENERGIES LIMITED",
                "advertiser_id": "AR01069449622662938625",
                "country": "IN",
                "ad_count": 200,
                "url": "https://adstransparency.google.com/advertiser/AR01069449622662938625?hl=en&region=anywhere",
                "images": [],
                "found": True,
                "image_files": [],
            },
        },
        {
            "name": "Venus Home Appliances Pvt Ltd",
            "country": "IN",
            "ad_count": 203,
            "detail": {
                "name": "Venus Home Appliances Pvt Ltd",
                "advertiser_id": "",
                "country": "IN",
                "ad_count": 203,
                "url": "https://adstransparency.google.com/?hl=en&region=anywhere",
                "images": [],
                "found": True,
                "image_files": [],
            },
        },
        {
            "name": "Orbit Solar Energy System",
            "country": "IN",
            "ad_count": 8,
        },
    ],
    "query": "solar advertisers in India",
}

PAGESPEED = {"error": "PageSpeed API unavailable during this audit"}

BUILD_NOTE = ("PDF built in an offline audit environment: ad-creative images cannot be downloaded "
              "here (ad-library CDN blocked), so the report carries the live ad copy, Library IDs and "
              "links but no creative thumbnails. Re-running audit_pdf.py locally embeds the creatives "
              "(owner-built full reports run 300-590KB). Every other figure was verified live.")


def load_own_ads(company_slug):
    with open(os.path.join(BASE, "ads_only_results", f"audit_{company_slug}.json"),
              encoding="utf-8") as f:
        d = json.load(f)
    mo = dict(d["ad_library"]["meta_own"])
    mo["images"] = []
    return mo


def google_own_none(query):
    return {"found": False, "advertisers": [], "detail": None, "query": query}


ORIZEN_TITLE = "ORIZEN SOLAR INNOVATIONS PVT. LTD "
ORIZEN_DESC = ("Orizen Solar, based in Guntur, Andhra Pradesh, specializes in providing high-quality "
               "solar energy solutions. From solar panel installations to solar inverters, we offer "
               "sustainable and efficient energy options for residential and commercial needs. Embrace "
               "clean energy and reduce your carbon footprint with Orizen Solar.")
RAYON_TITLE = "Roof top Solar System with PM Suryodhya ghar Subsidy"
RAYON_DESC = ("Install high-quality roof top solar system for your home or business with Ray On Solar "
              "Systems and also save more on cost with the Subsidy.")


def audit(**kw):
    kw.setdefault("audit_date", DATE)
    kw.setdefault("pagespeed", PAGESPEED)
    kw.setdefault("final_url", kw["website"])
    kw["ad_library"]["checked_at"] = DATE
    kw["ad_library"]["notes"] = [BUILD_NOTE] + list(kw["ad_library"].get("notes") or [])
    name = kw["company"]
    slug = kw.pop("_slug")
    out = os.path.join(OUT_DIR, f"audit_{slug}.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(kw, f, indent=2, ensure_ascii=False)
    print(f"wrote {out}")
    return kw


# ============================= ECOLT ENERGY ===================================
audit(
    _slug="Ecolt_Energy",
    company="Ecolt Energy",
    city="Hyderabad",
    website="https://www.ecoltenergy.com/",
    ssl=True,
    pixels={
        "meta_pixel": False, "google_ads": False, "google_analytics_ga4": False,
        "google_analytics_ua": False, "linkedin_insight": False,
        "microsoft_clarity": False, "hotjar": False, "google_tag_manager": False,
    },
    conversion={
        "has_contact_form": True,
        "has_phone_click": True,
        "has_whatsapp_link": True,
        "has_cta_buttons": 6,
        "has_live_chat": True,
        "has_popup_optin": True,
        "has_testimonials": True,
        "has_pricing_page_link": False,
    },
    seo={
        "has_title": True,
        "title_text": "Ecolt Energy | Rooftop Solar Installation & Financing",
        "title_length": 53,
        "has_meta_description": True,
        "meta_desc_length": 166,
        "h1_count": 1,
        "h1_text": "Power your future with confidence.",
        "has_og_tags": True,
        "has_schema": True,
        "has_favicon": True,
        "image_count": 3,
        "images_without_alt": 0,
    },
    page_count={"sitemap_pages": 18, "has_sitemap": True},
    local_signals={
        "has_google_maps_embed": False,
        "has_address_schema": True,
        "mentions_city": True,
        "company_in_title": True,
    },
    ad_check_urls={
        "google_ads_transparency": "https://adstransparency.google.com/?region=anywhere&country=IN&domain=ecoltenergy.com",
        "meta_ad_library": META_LIB_URL.format("Ecolt+Energy"),
        "note": "Open these URLs in your browser to check if they're running ads and what those ads look like.",
    },
    score={
        "score": 15,
        "issues": [
            "No Meta Pixel installed — can't run retargeting or track ad conversions",
            "No Google Ads / GTM tracking — can't measure ad performance",
            "No Google Analytics — flying blind on website traffic",
            "Your homepage's project map is explicitly labelled 'placeholder EXAMPLES only' in your own source code",
        ],
        "wins": [
            "Contact form exists",
            "WhatsApp link present",
            "Good CTA presence (6 buttons)",
            "Live chat present",
            "Testimonials visible",
        ],
    },
    ad_library={
        "meta_own": load_own_ads("Ecolt_Energy"),
        "google_own": google_own_none("Ecolt Energy"),
        "meta_competitors": META_COMP,
        "google_competitors": GOOGLE_COMP,
        "notes": [
            "No Google Ads advertiser record found for 'Ecolt Energy' or 'ecoltenergy.com' "
            "(checked in Google's Ads Transparency Center on 2026-10-21: 0 ads).",
            "Homepage project-map pins are placeholder examples per the site's own source comment "
            "('The pins below are placeholder EXAMPLES only - swap in your real project data').",
            "Homepage stat counters render as 0 without JavaScript (static HTML fallback).",
            "A quote popup re-opens automatically every 30 seconds while the page is open.",
            "Google competitor ads: WAAREE Energies verified live 2026-10-21; Venus and Orbit Solar "
            "verified in the same centre on 2026-10-18.",
        ],
        "summary": ("Ecolt Energy is running 2 live Telugu ads on Meta - both sharing one creative "
                    "(Library ID 1405421181747986, started 13 October 2026) selling a 3KW rooftop "
                    "system at Rs.1,90,000 with a Rs.33,000 discount plus the Rs.78,000 PM Surya Ghar "
                    "subsidy - and every click lands in a Facebook lead form, never on the polished "
                    "ecoltenergy.com the ad budget pays for. The site itself is strong on the basics: "
                    "SSL, contact form, WhatsApp, an 'Ask Ecolt' chat panel, full meta tags, Open Graph, "
                    "LocalBusiness schema and an 18-page sitemap with a Telugu version - but it carries "
                    "zero tracking. No Meta Pixel, no Google Ads tag, no GA4, no GTM: nothing a visitor "
                    "does on the site can be measured, attributed or retargeted, and the claim of "
                    "'2,000+ systems installed' sits above counters that read 0 and a project map your "
                    "own source code labels 'placeholder EXAMPLES only'. No Google Ads record exists for "
                    "the company, so search demand goes to competitors instead."),
    },
)

# ========================= ORIZEN SOLAR INNOVATIONS ===========================
audit(
    _slug="Orizen_Solar_Innovations",
    company="Orizen Solar Innovations",
    city="Hyderabad",
    website="https://www.orizensolar.com/",
    ssl=True,
    pixels={
        "meta_pixel": True, "google_ads": False, "google_analytics_ga4": False,
        "google_analytics_ua": False, "linkedin_insight": False,
        "microsoft_clarity": False, "hotjar": False, "google_tag_manager": False,
    },
    conversion={
        "has_contact_form": True,
        "has_phone_click": True,
        "has_whatsapp_link": True,
        "has_cta_buttons": 19,
        "has_live_chat": False,
        "has_popup_optin": False,
        "has_testimonials": True,
        "has_pricing_page_link": False,
    },
    seo={
        "has_title": True,
        "title_text": ORIZEN_TITLE,
        "title_length": len(ORIZEN_TITLE),
        "has_meta_description": True,
        "meta_desc_length": len(ORIZEN_DESC),
        "h1_count": 2,
        "h1_text": "Solar Panel Calculator",
        "has_og_tags": False,
        "has_schema": False,
        "has_favicon": True,
        "image_count": 69,
        "images_without_alt": 1,
    },
    page_count={"sitemap_pages": 0, "has_sitemap": False},
    local_signals={
        "has_google_maps_embed": False,
        "has_address_schema": False,
        "mentions_city": True,
        "company_in_title": True,
    },
    ad_check_urls={
        "google_ads_transparency": "https://adstransparency.google.com/?region=anywhere&country=IN&domain=orizensolar.com",
        "meta_ad_library": META_LIB_URL.format("Orizen+Solar+Innovations"),
        "note": "Open these URLs in your browser to check if they're running ads and what those ads look like.",
    },
    score={
        "score": 23,
        "issues": [
            "No Google Ads / GTM tracking — can't measure ad performance",
            "No Google Analytics — flying blind on website traffic",
            "No live chat — missing after-hours leads",
            "Multiple H1 tags (2) — confuses Google",
            "No structured data (Schema.org) — missing rich results in Google",
            "No Open Graph tags — links look bad when shared on social/WhatsApp",
            "1 images missing alt text — hurts SEO",
            "Your PM Surya Ghar section still reads 'At Your Solar Partner' — template placeholder text left live",
        ],
        "wins": [
            "Meta Pixel is installed",
            "Contact form exists",
            "WhatsApp link present",
            "Good CTA presence (19 buttons)",
            "Testimonials visible",
        ],
    },
    ad_library={
        "meta_own": load_own_ads("Orizen_Solar_Innovations"),
        "google_own": {
            "found": True,
            "detail": {
                "name": "Palisetty Ranadheer Kumar",
                "advertiser_id": "AR04254417204088406017",
                "country": "IN",
                "ad_count": 1,
                "url": "https://adstransparency.google.com/advertiser/AR04254417204088406017/creative/CR06536629552347611137?region=anywhere&country=IN",
                "images": [],
                "found": True,
                "image_files": [],
            },
            "advertisers": [
                {
                    "name": "Palisetty Ranadheer Kumar",
                    "country": "IN",
                    "ad_count": 1,
                    "detail": {
                        "name": "Palisetty Ranadheer Kumar",
                        "advertiser_id": "AR04254417204088406017",
                        "country": "IN",
                        "ad_count": 1,
                        "url": "https://adstransparency.google.com/advertiser/AR04254417204088406017/creative/CR06536629552347611137?region=anywhere&country=IN",
                        "images": [],
                        "found": True,
                        "image_files": [],
                    },
                }
            ],
            "query": "Orizen Solar Innovations",
        },
        "meta_competitors": META_COMP,
        "google_competitors": GOOGLE_COMP,
        "notes": [
            "Google Ads Transparency Center (2026-10-21): 1 Google ad points to orizensolar.com, run by "
            "verified advertiser 'Palisetty Ranadheer Kumar'.",
            "Meta Pixel (ID 1655381782019850) is installed but fires PageView only - the contact form "
            "submit never fires a Lead event, so form leads are not tracked back to ads.",
            "The hero carousel containing the page's headline H1s is commented out in the source code.",
            "The floating email icon links to mailto:example@example.com - a template placeholder.",
            "The site has no sitemap.xml (/sitemap.xml returns 404).",
            "Google competitor ads: WAAREE Energies verified live 2026-10-21; Venus and Orbit Solar "
            "verified in the same centre on 2026-10-18.",
        ],
        "summary": ("Orizen Solar Innovations is running a live Telugu Meta ad (Library ID 3529873930505195, "
                    "started 18 September 2026, multiple versions) with a Dussehra & Deepavali offer - "
                    "Rs.78,000 subsidy, 3KW with Rs.10,000 off, 5KW with Rs.20,000 off - and every click "
                    "goes to WhatsApp, so the website never sees the paid traffic. The site is the only "
                    "one of the three audited sites with the Meta Pixel installed (ID 1655381782019850) "
                    "and it is the only one with a Google Ads presence (1 ad via the Transparency Center) "
                    "- but the pixel fires PageView only, never a Lead event, and there is no GA4 or GTM "
                    "behind it. SEO is weak where it is easiest to fix: no Open Graph tags, no structured "
                    "data, no sitemap, two competing H1 tags, and a hero carousel whose H1s are commented "
                    "out of the code. Template leftovers are still live on the page - 'At Your Solar "
                    "Partner' in the PM Surya Ghar blurb, a mailto:example@example.com email icon and a "
                    "'Features of Origin Solar Panels' heading for a company called Orizen."),
    },
)

# ========================== RAY ON SOLAR SYSTEMS ==============================
audit(
    _slug="Ray_On_Solar_Systems",
    company="Ray On Solar Systems",
    city="Hyderabad",
    website="https://www.rayonsolarsystems.in/",
    ssl=True,
    pixels={
        "meta_pixel": False, "google_ads": False, "google_analytics_ga4": False,
        "google_analytics_ua": False, "linkedin_insight": False,
        "microsoft_clarity": False, "hotjar": False, "google_tag_manager": False,
    },
    conversion={
        "has_contact_form": False,
        "has_phone_click": False,
        "has_whatsapp_link": True,
        "has_cta_buttons": 4,
        "has_live_chat": False,
        "has_popup_optin": False,
        "has_testimonials": True,
        "has_pricing_page_link": False,
    },
    seo={
        "has_title": True,
        "title_text": RAYON_TITLE,
        "title_length": len(RAYON_TITLE),
        "has_meta_description": True,
        "meta_desc_length": len(RAYON_DESC),
        "h1_count": 1,
        "h1_text": "Install Roof Top Solar System and Start saving on your electricity bills while contributing to a sustainable future",
        "has_og_tags": True,
        "has_schema": False,
        "has_favicon": False,
        "image_count": 7,
        "images_without_alt": 0,
    },
    page_count={"sitemap_pages": 7, "has_sitemap": True},
    local_signals={
        "has_google_maps_embed": False,
        "has_address_schema": False,
        "mentions_city": True,
        "company_in_title": False,
    },
    ad_check_urls={
        "google_ads_transparency": "https://adstransparency.google.com/?region=anywhere&country=IN&domain=rayonsolarsystems.in",
        "meta_ad_library": META_LIB_URL.format("Ray+On+Solar+Systems"),
        "note": "Open these URLs in your browser to check if they're running ads and what those ads look like.",
    },
    score={
        "score": 31,
        "issues": [
            "No Meta Pixel installed — can't run retargeting or track ad conversions",
            "No Google Ads / GTM tracking — can't measure ad performance",
            "No Google Analytics — flying blind on website traffic",
            "No contact form on homepage — visitors can't easily enquire",
            "No live chat — missing after-hours leads",
            "No structured data (Schema.org) — missing rich results in Google",
            "No favicon — looks unprofessional in browser tabs",
            "Phone numbers on the homepage are plain text — no tap-to-call on mobile",
            "'Get Started' buttons link to /contact/, which returns a 404",
        ],
        "wins": [
            "WhatsApp link present",
            "Good CTA presence (4 buttons)",
            "Testimonials visible",
        ],
    },
    ad_library={
        "meta_own": load_own_ads("Ray_On_Solar_Systems"),
        "google_own": google_own_none("Ray On Solar Systems"),
        "meta_competitors": META_COMP,
        "google_competitors": GOOGLE_COMP,
        "notes": [
            "No Google Ads advertiser record found for 'Ray On Solar Systems' or 'rayonsolarsystems.in' "
            "(checked in Google's Ads Transparency Center on 2026-10-21: 0 ads).",
            "The only live Meta ad sends its click to Instagram, never to the website.",
            "Schema microdata on the page uses invalid https://schema.org URLs (12 validation errors) - "
            "Google ignores it.",
            "Page title still reads 'Suryodhya ghar' and does not contain the company name.",
            "The WordPress plugin that carries header snippets (HFCM) is used only for a Search Console "
            "verification tag - no pixel or analytics snippet exists anywhere in the page source.",
            "Google competitor ads: WAAREE Energies verified live 2026-10-21; Venus and Orbit Solar "
            "verified in the same centre on 2026-10-18.",
        ],
        "summary": ("Ray On Solar Systems is running 1 live Meta ad (Library ID 1107666674962232, started "
                    "13 October 2026) offering a 3kW solar system with subsidy - and its click goes to "
                    "Instagram, not to the website. The site has no tracking at all: no Meta Pixel, no "
                    "GA4, no GTM, and no Google Ads record. The homepage has no enquiry form and no "
                    "tap-to-call phone links, while every 'Get Started' button points to a /contact/ "
                    "address that returns a 404 - the site's own free-quote form sits unused while the ad "
                    "pays for clicks. Rank Math gives the site decent meta tags, but the title still "
                    "reads 'Suryodhya ghar', never mentions the brand, and the schema markup uses "
                    "invalid https://schema.org URLs that Google ignores. Meanwhile ~180 live "
                    "competitor Meta ads and WAAREE's ~200 Google ads are buying the same customers."),
    },
)

print("done")
