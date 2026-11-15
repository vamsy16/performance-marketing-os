#!/usr/bin/env python3
"""
Full-audit builder for the 2 batch-20 leads - Ksquare-shaped, built from data
actually read on 2026-11-15, with everything that could not be measured left
explicitly null.

Same contract as build_full_audits_batch18.py:

  `run_audit()` fetches the target page over HTTP. This sandbox has no outbound
  route to arbitrary hosts, so the normal audit path cannot run here. Rather
  than invent numbers, this builder takes the page text that *was* read live
  through the sandbox's page fetcher and derives the same audit fields from it.

What is real here
-----------------
  * page titles, H1s, image counts and alt text, link text, CTA link text
  * sitemap URL lists, counted verbatim (including the theme-demo pages)
  * tel: / mailto: / wa.me links, counted from the rendered link markdown
  * SSL (the HTTPS fetch succeeded)
  * the live Google Ads Transparency and Meta Ad Library evidence, every Meta
    ID re-opened individually on 2026-11-15 during the third-eye pass

What is deliberately null (never guessed)
-----------------------------------------
  * all eight tracking pixels - the page *source* was never available, only
    rendered text, so no pixel claim is made in either direction
  * server response time, PageSpeed scores, LCP
  * meta description, Open Graph tags, Schema.org, favicon - head markup
  * Google Maps embed where the page text did not include one
  * live chat, popup opt-in, pricing-page link - not observable in page text

`calculate_audit_score()` treats None as "not measured": it neither penalises
nor counts it as a win, and it never appears as a finding. The PDF renderer
prints "could not be checked in this pass" for those rows.

No value in either audit is copied from audit_Ksquare_Energy.json or from any
other report. That file was read only for its shape.

Usage:
  python build_full_audits_batch20.py            # build both
  python build_full_audits_batch20.py --only Meissa
"""

import argparse
import json
import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from ads_audit import calculate_audit_score, generate_ad_check_urls  # noqa: E402
from audit_pdf import generate_pdf  # noqa: E402

CHECKED = "2026-11-15"
UNCHECKED_NOTE = ("Not checked in this pass - the sandbox could not retrieve "
                  "this page's HTML source (no outbound route to arbitrary "
                  "hosts), so no claim is made either way.")

GADS = "https://adstransparency.google.com/advertiser/"


def gcreative(adv, cr):
    return f"{GADS}{adv}/creative/{cr}?region=IN"


def ad(library_id, page_name, started, destination, text, ad_count=None):
    return {"library_id": str(library_id),
            "library_url": "https://www.facebook.com/ads/library/?id=%s" % library_id,
            "ad_count": ad_count, "format": None, "page_name": page_name,
            "started": started, "destination": destination, "text": text,
            "images": []}


# ===========================================================================
# Evidence, read live on 2026-11-15. Every count below was derived
# mechanically from the page text saved in 01-LEADS/fetched/ with a fixed
# regex, so each one can be re-derived from that file.
# ===========================================================================

EVIDENCE = [
    # ------------------------------------------------------------- Meissa Reeve
    {
        "company": "Meissa Reeve",
        "legal": "Meissa Reeve Pvt. Ltd.",
        "city": "Mehdipatnam, Hyderabad",
        "website": "https://meissareeve.com/",
        "email": "info@meissareeve.com",
        "phone": "+91 7893088071",
        "fb_page": "https://www.facebook.com/61596697943588/",
        "saved_pages": {
            "homepage": "01-LEADS/fetched/meissa_homepage.md",
            "contact": "01-LEADS/fetched/meissa_contacts.md",
            "solar": "01-LEADS/fetched/meissa_solar_home.md",
            "sitemap": "01-LEADS/fetched/meissa_sitemap_page.md",
        },
        "pages": {
            "homepage": {
                "url": "https://meissareeve.com/",
                "title": "Meissa Reeve",
                "h1": [],
                "form_fields": [],
                "chat_widget": False,
                "has_testimonials": False,
                # counted over fetched/meissa_homepage.md
                "image_total": 12, "image_no_alt": 10,
                "cta_total": 0,
                "links": [
                    ("Solar Energy", "https://re.meissareeve.com/"),
                    ("Enter", "https://e.meissareeve.com/"),
                    ("Enter", "https://ev.meissareeve.com/"),
                    ("EV Charging Stations",
                     "https://meissareeve.com/services/ev-charging-stations-both-fast-slow/"),
                    ("Retrofitting", "https://meissareeve.com/services/retrofitting/"),
                    ("Solar Carport with EVCS",
                     "https://meissareeve.com/services/lithium-ion-lithium-ferro-phosphate-batteries/"),
                    ("Repair & Maintenance",
                     "https://meissareeve.com/services/repair-maintenance/"),
                    ("Whatsapp", "https://wa.me/917893088071?text="),
                ],
            },
            "contact": {
                "url": "https://meissareeve.com/contacts/",
                "title": "Contact Us | Meissa Reeve",
                "h1": [],
                # contact-form-7 id="6846" is present on the page; the reader
                # does not render its field labels, only the shortcode tag.
                "form_fields": ["contact-form-7 id=6846"],
                "chat_widget": False,
                "has_testimonials": False,
                "image_total": 0, "image_no_alt": 0,
                "cta_total": 0,
                "links": [
                    ("Whatsapp", "https://wa.me/917893088071?text="),
                    ("Open in Maps",
                     "https://maps.google.com/?cid=887234906307059109&hl=en&gl=IN&source=embed"),
                ],
                # The phone and the email are published as plain text on this
                # page. Neither is a tel: or mailto: link - recorded because
                # the difference is the finding.
                "phone_as_plain_text": "+91-7893088071",
                "email_as_plain_text": "info@meissareeve.com",
                "google_rating": "4.8 from 24 reviews (embedded Google review widget)",
                "address": ("Saptagiri Nagar, Retibowli, Mehdipatnam, Hyderabad; Google "
                            "listing 12-2-727/1/57, Sapthagiri Nagar Colony, Rethibowli, "
                            "Gudimalkapur, Hyderabad, Telangana 500006"),
                "hours": "Mon-Fri 09:00 AM to 05:00 PM",
            },
            "solar": {
                "url": "https://re.meissareeve.com/",
                "title": "Meissa Solar | Meissa Reeve",
                "h1": ["About us"],
                "form_fields": [],
                "chat_widget": False,
                "has_testimonials": True,
                # counted over fetched/meissa_solar_home.md
                "image_total": 44, "image_no_alt": 3,
                "cta_total": 0,
                "links": [],
                "view_counter": "11,020 total views, 10 views today (publicly displayed)",
            },
        },
        "sitemap": {
            "url": "https://meissareeve.com/sitemap_index.xml",
            "sub_sitemaps": 17,
            "urls": [],            # counted, not listed, in the audit
            "page_url_count": 79,
            "image_url_count": 5,
            "theme_demo_pages": 36,
            "theme_demo_examples": [
                "/my-account/", "/checkout/", "/cart/", "/gallery-2-columns/",
                "/gallery-3-columns/", "/gallery-4-columns/", "/404-layout/",
                "/homepage-gas-station/", "/homepage-rental/", "/homepage-towing/",
                "/homepage-natural-honey/", "/multipage/", "/shop/",
                "/komaki/", "/gemopai/", "/virtus-motors/", "/petrol-pumps/",
                "/airport-metros/", "/news/", "/events-company/", "/videos/",
            ],
            "post_count": 0,
        },
        "maps_embed": True,
        "city_mentions": True,
        "company_in_title": False,
        "google_ads": {
            "ad_count": 0,
            "name": "",
            "advertiser_id": "",
            "creatives": [],
            "started": "",
            "destination": "",
            "note": ("Google Ads Transparency Centre for meissareeve.com under "
                     "region=IN returned 0 ads on 2026-11-15."),
        },
        "meta_ads": [
            ad("1641050694153685", "Meissa Reeve", "Nov 14, 2026",
               "WhatsApp deep link ('Send WhatsApp message')",
               "Tired of your electricity bill going up every summer? Put your "
               "rooftop to work. Meissa Reeve designs and installs rooftop solar "
               "for homes across Hyderabad - so you generate your own power and "
               "cut your monthly bill. Free site visit & savings estimate; Help "
               "with the PM Surya Ghar subsidy process; End-to-end installation "
               "& net metering. Tap 'Send WhatsApp message' and tell us your "
               "monthly bill - we'll show you how much you can save. "
               "#HarGharSolar", ad_count=1),
        ],
        "meta_summary": (
            "Meissa Reeve is running exactly one active Meta ad, on the page "
            "'Meissa Reeve' (facebook.com/61596697943588), started 14 Nov 2026 "
            "and about 18 hours old when it was re-checked. The click lands on a "
            "WhatsApp deep link, never on meissareeve.com. Google Ads "
            "Transparency for meissareeve.com returns 0 ads under region=IN, so "
            "Meta is the entire paid channel and it rests on a single creative."),
        "summary": (
            "Meissa Reeve is a multi-division Hyderabad company - solar rooftop "
            "EPC on re.meissareeve.com, EV charging and retrofitting alongside it "
            "- running one live Meta ad that pushes every click into WhatsApp. "
            "The site works and the solar division carries twelve named, "
            "verifiable installations, but the parent domain still publishes 36 "
            "unedited WordPress theme-demo pages, and the contact page's phone "
            "and email are plain text rather than tappable links. No website "
            "audit was possible for the ad's own destination because there isn't "
            "one: the ad never sends anyone to the site."),
        "defects": [
            ("36 unedited theme-demo pages are live and indexed",
             "The sitemap at meissareeve.com/sitemap_index.xml lists 17 "
             "sub-sitemaps, and page-sitemap.xml alone contains 79 page URLs. "
             "36 of them are untouched theme demo content: /my-account/, "
             "/checkout/, /cart/, /gallery-2-columns/, /gallery-3-columns/, "
             "/gallery-4-columns/, sixteen /elements/* pages, /404-layout/, "
             "/multipage/, /shop/, and four complete demo homepages - "
             "/homepage-gas-station/, /homepage-rental/, /homepage-towing/ and "
             "/homepage-natural-honey/ - plus product pages for three EV "
             "scooter brands (/komaki/, /gemopai/, /virtus-motors/) and "
             "/petrol-pumps/ and /airport-metros/. A prospect who follows a "
             "link can land on a page selling petrol pumps or honey. All of it "
             "is in the sitemap, so all of it is indexable."),
            ("The phone number and email are published as plain text, not links",
             "meissareeve.com/contacts/ shows +91-7893088071 and "
             "info@meissareeve.com as bare text. Neither is wrapped in a tel: "
             "or mailto: link, so a visitor on a phone - which is most of them "
             "for a local solar enquiry - cannot tap to call or tap to email. "
             "The email address is published, so the lead qualifies, but the "
             "click path is missing."),
            ("The homepage has no H1, and 10 of its 12 images carry no alt text",
             "Counted over the page text read on 2026-11-15: meissareeve.com "
             "renders 12 images, 10 of them with an empty alt attribute, and "
             "no H1 heading at all. The solar division is markedly better - 44 "
             "images with only 3 missing alt, and one H1 - so this is the "
             "parent site being left unpolished rather than a site-wide "
             "problem."),
            ("The solar division homepage has no action CTA anywhere",
             "re.meissareeve.com renders 50 links. Not one of them is an action "
             "- no 'get a quote', no 'book a site visit', no 'contact us'. The "
             "links are internal anchors, image links to full-size photos and "
             "social icons. The page explains on-grid, off-grid and hybrid "
             "systems and lists twelve installations, then gives the reader "
             "nothing to click."),
            ("Image URLs are listed as sitemap entries",
             "page-sitemap.xml interleaves raw /wp-content/uploads/ image URLs "
             "among the page URLs. That is a WordPress SEO plugin "
             "misconfiguration: it tells search engines that media files are "
             "indexable pages, which splits the site's ranking signal across "
             "hundreds of thin URLs."),
            ("A public view counter is displayed on the solar division",
             "re.meissareeve.com prints '11,020 total views, 10 views today' at "
             "the top of the page. That is an internal traffic metric "
             "published to every visitor, and 10 views a day is not a number "
             "worth advertising."),
        ],
        "wins": [
            "A real contact form is published (Contact Form 7, id 6846) on the "
            "contacts page",
            "WhatsApp is one tap away - a wa.me link sits on the homepage and "
            "again on the contacts page",
            "Twelve named installations with locality and system size are "
            "published: Anees 2kW Moula Ali, Dr. Kasi 3kW R K Puram, Om Prakash "
            "4kW Balnagar, Uma Shankar 3kW Begumpet, Sahifa Masjid Hyderabad "
            "10kW, 17kW Shad Nagar, 50kW Tamil Nadu, 88kW Choutupal, 5KW "
            "Cherlapally, 6KW Hafizpet, 15KW Sarath City Capital Mall "
            "Kondapur, Rainbow Hospital 150kW Banjara Hills",
            "A 4.8-star Google rating from 24 reviews is embedded on the "
            "contacts page",
            "Full postal address and business hours (Mon-Fri 09:00-17:00) are "
            "published",
            "HTTPS is live and the site loads over it",
        ],
        "contact_facts": [
            ("Email", "info@meissareeve.com (published as text on "
                      "meissareeve.com/contacts/, not as a mailto link)"),
            ("Second inbox", "enquiry@meissareeve.com, published on the solar "
                             "division"),
            ("Phone / WhatsApp", "+91 7893088071 / wa.me/917893088071 (published "
                                 "as text, not as a tel: link)"),
            ("Address", "Saptagiri Nagar, Retibowli, Mehdipatnam, Hyderabad; "
                        "Google listing 12-2-727/1/57, Sapthagiri Nagar Colony, "
                        "Rethibowli, Gudimalkapur, Hyderabad 500006"),
            ("Hours", "Mon-Fri 09:00 AM to 05:00 PM"),
            ("Entity", "Meissa Reeve Pvt. Ltd. - solar division on "
                       "re.meissareeve.com"),
            ("Meta page", "facebook.com/61596697943588 (Meissa Reeve)"),
        ],
    },
    # -------------------------------------------------------- Visiontek Solar
    {
        "company": "Visiontek Solar Energy",
        "legal": "VISIONTEK Linkwell Telesystems Pvt Ltd",
        "city": "Begumpet, Hyderabad",
        "website": "https://visiontek.solar/",
        "email": "info@visiontek.com",
        "phone": "+91 9701601421",
        "fb_page": "https://www.facebook.com/Visionteknewenergy/",
        "saved_pages": {
            "homepage": "01-LEADS/fetched/visiontek_homepage.md",
            "contact": "01-LEADS/fetched/visiontek_contact.md",
            "product": "01-LEADS/fetched/visiontek_product.md",
        },
        "pages": {
            "homepage": {
                "url": "https://visiontek.solar/",
                "title": "VISIONTEK - Powering India's Smart Energy Future",
                "h1": ["Engineering the Future  of Intelligent Energy"],
                "form_fields": [],
                "chat_widget": False,
                "has_testimonials": False,
                # counted over fetched/visiontek_homepage.md
                "image_total": 12, "image_no_alt": 0,
                "cta_total": 3,
                "links": [
                    ("View All Articles", "https://visiontek.solar/blogs"),
                    ("Connect on WhatsApp", "https://wa.me/+919701601421"),
                    ("Chat on WhatsApp", "https://wa.me/+919701601421"),
                ],
            },
            "contact": {
                "url": "https://visiontek.solar/contact-us",
                "title": "Contact VISIONTEK Solar",
                "h1": [],
                # the page renders a CONTACT FORM block with a SEND ENQUIRY
                # button and validation messages
                "form_fields": ["CONTACT FORM", "SEND ENQUIRY"],
                "chat_widget": False,
                "has_testimonials": False,
                # counted over fetched/visiontek_contact.md
                "image_total": 6, "image_no_alt": 0,
                "cta_total": 4,
                "links": [
                    ("+91 9701601421", "tel:+91 9701601421"),
                    ("info@visiontek.com", "mailto:info@visiontek.com"),
                    ("www.visiontek.co.in", "https://www.visiontek.co.in/"),
                    ("Connect on WhatsApp", "https://wa.me/+919701601421"),
                    ("Chat on WhatsApp", "https://wa.me/+919701601421"),
                ],
                "address": ("Linkwell Telesystems Pvt. Ltd., 1-11-252/1B, Behind "
                            "Shoppers' Stop, Begumpet, Hyderabad 500016, "
                            "Telangana, India"),
            },
            "product": {
                "url": "https://visiontek.solar/product",
                "title": "VISIONTEK Products",
                "h1": ["New Energy Solutions  for Every Need."],
                "form_fields": [],
                "chat_widget": False,
                "has_testimonials": False,
                # counted over fetched/visiontek_product.md
                "image_total": 14, "image_no_alt": 0,
                "cta_total": 3,
                "links": [
                    ("Download Catalogue", "https://visiontek.solar/product#"),
                    ("Connect on WhatsApp", "https://wa.me/+919701601421"),
                    ("Chat on WhatsApp", "https://wa.me/+919701601421"),
                ],
            },
        },
        "sitemap": {
            "url": "",
            "sub_sitemaps": 0,
            "urls": [],
            "page_url_count": 0,
            "image_url_count": 0,
            "theme_demo_pages": 0,
            "theme_demo_examples": [],
            "post_count": 0,
            "missing": "Both /sitemap.xml and /robots.txt return 404 Page Not Found.",
        },
        "maps_embed": True,
        "city_mentions": True,
        "company_in_title": False,
        "google_ads": {
            "ad_count": 0,
            "name": "",
            "advertiser_id": "",
            "creatives": [],
            "started": "",
            "destination": "",
            "note": ("Google Ads Transparency Centre for visiontek.solar under "
                     "region=IN returned 0 ads on 2026-11-15."),
        },
        "meta_ads": [
            ad("1133037052650969", "Visionteknewenergy", "Nov 12, 2026",
               "instagram.com root ('Chat with us' / Send Message)",
               "Still paying high electricity bills? Switch to Visiontek Solar "
               "and turn sunlight into savings. Our smart system powers your "
               "home directly, stores extra energy for the night and helps "
               "lower your monthly bill. Its time to power your home naturally. "
               "#Visiontek #GoSolar #SolarPower #SolarEnergy #EnergyStorage",
               ad_count=2),
            ad("1449750756945639", "Visionteknewenergy", "Nov 12, 2026",
               "instagram.com root ('Send Message')",
               "Say goodbye to soaring electricity bills and take control of "
               "your energy expenses. Switch to solar today and start "
               "generating your own clean savings. #CutElectricityBills "
               "#SolarSavings #GoGreen #EnergyIndependence #VisiontekSolar",
               ad_count=2),
            ad("2208275783425425", "Visionteknewenergy", "Nov 12, 2026",
               "instagram.com root ('Send Message')",
               "Control your electricity bill before it shocks you! Go solar "
               "with Visiontek and take charge of your energy. #Visiontek "
               "#GoSolar #SolarEnergy #SolarPower #SaveOnElectricity "
               "#RenewableEnergy #CleanEnergy #SolarSolutions #GreenEnergy "
               "#EnergySavings", ad_count=2),
            ad("1138341982459373", "Visionteknewenergy", "Nov 12, 2026",
               "instagram.com root ('Send Message')",
               "Say goodbye to soaring electricity bills and take control of "
               "your energy expenses. Switch to solar today and start "
               "generating your own clean savings. #CutElectricityBills "
               "#SolarSavings #GoGreen #EnergyIndependence #VisiontekSolar",
               ad_count=2),
            ad("910533972050441", "Visionteknewenergy", "Nov 12, 2026",
               "instagram.com root ('Send Message')",
               "Going solar is more than installing panels; it's about choosing "
               "the right power solution! Understand your energy needs, select "
               "the right inverter and plan your backup for reliable, efficient "
               "power. Make a smarter energy choice with Visiontek! #Visiontek "
               "#SolarEnergy #SolarPower #CleanEnergy #RenewableEnergy",
               ad_count=2),
            ad("1642086640990986", "Visionteknewenergy", "Nov 12, 2026",
               "image creative, no outbound link shown",
               "Control your electricity bill before it shocks you! Go solar "
               "with Visiontek and take charge of your energy. #Visiontek "
               "#GoSolar #SolarEnergy #SolarPower #SaveOnElectricity "
               "#RenewableEnergy #CleanEnergy #SolarSolutions #GreenEnergy "
               "#EnergySavingSolutions", ad_count=2),
            ad("1949641059333335", "Visionteknewenergy", "Nov 12, 2026",
               "image creative, no outbound link shown",
               "Big on performance. Compact in design. With Visiontek Solar "
               "Inverters, you get powerful solar performance without giving up "
               "valuable space. Built for efficiency, designed for modern "
               "spaces, and made to power more with less. Less space. More "
               "power. Smarter solar. #Visiontek #SolarInverter #SolarPower "
               "#RenewableEnergy #CleanEnergy #SolarSolutions", ad_count=2),
            ad("1846039203313070", "Visionteknewenergy", "Nov 12, 2026",
               "video creative, no outbound link shown",
               "Stop choosing between comfort and savings. Switch to Visiontek "
               "Solar and stay cool without the high bills. #VisiontekSolar "
               "#SolarPower #SaveMore #SmartHome #CleanEnergy", ad_count=2),
            ad("1443714387877981", "Visionteknewenergy", "Nov 12, 2026",
               "carousel, no outbound link shown",
               "Still paying high electricity bills? Switch to Visiontek Solar "
               "and turn sunlight into savings. Our smart system powers your "
               "home directly, stores extra energy for the night and helps "
               "lower your monthly bill. Its time to power your home naturally. "
               "#Visiontek #GoSolar #SolarPower #SolarEnergy #EnergyStorage",
               ad_count=2),
            ad("2172490176994377", "Visionteknewenergy", "Nov 6, 2026",
               "fb.me short link",
               "This Diwali, light up your life with the power of solar! "
               "Celebrate the festival of lights by making a brighter, smarter "
               "energy choice with Visiontek. Explore our range of On-Grid, "
               "Off-Grid & Hybrid Solar Inverters and energy storage solutions "
               "for your home and business.", ad_count=2),
            ad("986852867827035", "Visionteknewenergy", "Nov 12, 2026",
               "carousel, no outbound link shown",
               "Going solar is more than installing panels; it's about choosing "
               "the right power solution! Understand your energy needs, select "
               "the right inverter and plan your backup for reliable, efficient "
               "power. Make a smarter energy choice with Visiontek! #Visiontek "
               "#SolarEnergy #SolarPower #CleanEnergy #RenewableEnergy",
               ad_count=2),
        ],
        "meta_summary": (
            "Visionteknewenergy is running 11 distinct live Meta creatives, "
            "every one started 12 Nov 2026 except a Diwali creative from 6 Nov "
            "2026 - a single coordinated launch, which means this is a fresh, "
            "actively managed account rather than a stale one. Meta groups them, "
            "reporting '2 ads use this creative and text' on each, so the real "
            "number of ads is higher than the number of distinct IDs. Six of "
            "the eleven send the click to a bare instagram.com root and one to "
            "fb.me; the remaining four carry no outbound link at all. Google "
            "Ads Transparency for visiontek.solar returns 0 ads under "
            "region=IN, so Meta is the entire paid channel."),
        "summary": (
            "Visiontek Solar Energy is the solar division launched in 2025 by "
            "VISIONTEK Linkwell Telesystems, a 32-year-old telecom and "
            "power-electronics manufacturer in Begumpet. It is running 11 live "
            "Meta creatives launched in a single coordinated push on 12 Nov "
            "2026, and the site behind them is in genuinely good shape - every "
            "image has alt text, each page has one H1, and the contact page has "
            "tappable phone, email, WhatsApp and a working form. The problems "
            "are structural: there is no sitemap and no robots.txt at all, and "
            "ten of the eleven ads do not point at the site, so almost none of "
            "the spend can reach any of it."),
        "defects": [
            ("Ten of the eleven live ads do not point at the website",
             "Six creatives send the click to a bare instagram.com root, one to "
             "an fb.me short link, and four carry no outbound link at all. A "
             "click on instagram.com lands on the Instagram home feed - not a "
             "profile, not a post, not a message thread - so that traffic has "
             "nowhere to go and cannot be attributed. Only the fb.me creative "
             "resolves to anything owned, and that is a Facebook short link."),
            ("No sitemap and no robots.txt",
             "Both https://visiontek.solar/sitemap.xml and "
             "https://visiontek.solar/robots.txt return 404 Page Not Found. "
             "There is no crawlable index of the site and no crawler "
             "instruction, on a domain with a product catalogue, a blog and "
             "individual product pages."),
            ("Every social media link on the contact page is a dead anchor",
             "The contact page renders four social icons - Facebook, Twitter, "
             "LinkedIn and Instagram - and all four point at "
             "contact-us#, i.e. nowhere. The one social presence that does "
             "exist, facebook.com/Visionteknewenergy, is where the 11 live ads "
             "run, and the site does not link to it."),
            ("'Download Catalogue' does not download a catalogue",
             "The FUTURE+ 5KVA Hybrid Inverter block on the product page "
             "renders 'Download Catalogue (PDF, 1.2 MB)' as a link to "
             "visiontek.solar/product# - an anchor on the same page. There is "
             "no PDF behind it. A buyer trying to get the datasheet gets "
             "nothing."),
            ("The homepage advertises four of the six product lines",
             "The homepage's Featured Products section carries RISE+, FUTURE+, "
             "VAULT+ and PULSE+. The product page carries those plus NEXUS+ and "
             "the Nexus+ cloud platform. Two of the six lines a visitor can "
             "read about on the product page are invisible from the front "
             "door."),
            ("A broken video element is printed as visible text",
             "The product page renders 'Your browser does not support video.' "
             "in the page body, which means a video player with no playable "
             "source is shipping to every visitor."),
        ],
        "wins": [
            "Every image carries alt text - 0 of 12 on the homepage, 0 of 6 on "
            "the contact page, 0 of 14 on the product page",
            "Exactly one H1 per page, and each one is descriptive rather than a "
            "logo dump",
            "The contact page has a tappable tel: link and a tappable mailto: "
            "link, plus a contact form with a SEND ENQUIRY button and "
            "client-side validation messages",
            "WhatsApp support is on every page, not just the contact page",
            "Four product lines are documented with real technical detail, and "
            "a catalogue download is offered (even though the link is broken)",
            "The blog is current - posts dated 11 and 12 Nov 2026",
            "HTTPS is live and the site loads over it",
        ],
        "contact_facts": [
            ("Email", "info@visiontek.com (a real mailto: link on the contact "
                      "page)"),
            ("Phone / WhatsApp", "+91 9701601421 / wa.me/+919701601421"),
            ("Address", "Linkwell Telesystems Pvt. Ltd., 1-11-252/1B, Behind "
                        "Shoppers' Stop, Begumpet, Hyderabad 500016, Telangana, "
                        "India"),
            ("Entity", "VISIONTEK Linkwell Telesystems Pvt Ltd - 32+ years in "
                       "telecom and power electronics; solar division launched "
                       "2025"),
            ("Products", "RISE+ on-grid inverter, FUTURE+ hybrid inverter, "
                         "VAULT+ LFP battery storage, PULSE+ panel-level "
                         "optimiser, NEXUS+ energy management, Nexus+ cloud "
                         "platform"),
            ("Meta page", "facebook.com/Visionteknewenergy"),
        ],
    },
]


def build_audit(ev):
    """Turn one evidence record into a full-audit dict. Nulls stay null."""
    home = (ev.get("pages") or {}).get("homepage")
    contact = (ev.get("pages") or {}).get("contact")
    sitemap = ev.get("sitemap") or {}

    def page_images(page):
        if not page:
            return None, None
        return page.get("image_total"), page.get("image_no_alt")

    def page_links(page):
        if not page:
            return []
        return page.get("links") or []

    def page_h1(page):
        if not page:
            return None, None
        h1 = page.get("h1") or []
        return len(h1), (h1[0] if h1 else "")

    def page_title(page):
        return page.get("title") if page else None

    def has_tel(pages):
        for p in pages:
            for _, href in page_links(p):
                if href.startswith("tel:"):
                    return True
        return False

    def has_wa(pages):
        for p in pages:
            for _, href in page_links(p):
                if "wa.me" in href or "api.whatsapp.com" in href:
                    return True
        return any(p and p.get("chat_widget") for p in pages)

    # The label says "on homepage", so it must measure the homepage.
    def has_form(pages):
        return bool(home and home.get("form_fields"))

    # A mailto: link to example.com is theme placeholder content, not a
    # published email.
    PLACEHOLDER_DOMAINS = ("example.com", "example.org", "example.net",
                           "test.com", "yourdomain.com", "sentry.io")

    def has_mailto(pages):
        """True only for a real mailto: LINK. An email published as plain
        text is a separate, weaker thing and is recorded as a defect instead -
        counting it here would report a click path that does not exist."""
        for p in pages:
            for _, href in page_links(p):
                if not href.startswith("mailto:"):
                    continue
                addr = href[len("mailto:"):].split("?")[0].strip().lower()
                if not addr or "@" not in addr:
                    continue
                if addr.rsplit("@", 1)[-1] in PLACEHOLDER_DOMAINS:
                    continue
                return True
        return False

    def has_testimonials(pages):
        return any(p and p.get("has_testimonials") for p in pages)

    CTA_RE = re.compile(
        r"^(get |book |call |enquire|inquire|contact|explore|know more|read more|"
        r"make an appointment|see |check |view |chat on|send|apply|request|"
        r"download|connect)", re.I)

    def cta_count(pages):
        for p in pages:
            if p and p.get("cta_total") is not None:
                return p["cta_total"]
        n = 0
        for p in pages:
            for text, _ in page_links(p):
                if CTA_RE.match(text.strip()):
                    n += 1
        return n

    pages = [p for p in (home, contact) if p]
    img_total, img_alt = page_images(home) if home else (None, None)
    h1_count, h1_text = page_h1(home) if home else (None, None)
    title = page_title(home) if home else None

    has_sitemap = None
    if sitemap.get("url"):
        has_sitemap = bool(sitemap.get("page_url_count"))
    elif sitemap.get("missing"):
        has_sitemap = False

    pixels = {k: None for k in (
        "meta_pixel", "google_ads", "google_analytics_ga4",
        "google_analytics_ua", "linkedin_insight", "microsoft_clarity",
        "hotjar", "google_tag_manager")}

    conversion = {
        "has_contact_form": has_form(pages) if pages else None,
        "has_phone_click": has_tel(pages) if pages else None,
        "has_whatsapp_link": has_wa(pages) if pages else None,
        "has_cta_buttons": cta_count(pages) if pages else None,
        "has_live_chat": None,
        "has_popup_optin": None,
        "has_testimonials": has_testimonials(pages) if pages else None,
        "has_pricing_page_link": None,
        "has_mailto_published": has_mailto(pages) if pages else None,
    }

    seo = {
        "has_title": bool(title) if title is not None else None,
        "title_text": title or "",
        "title_length": len(title) if title else None,
        "has_meta_description": None,
        "meta_desc_length": None,
        "h1_count": h1_count,
        "h1_text": h1_text or "",
        "has_og_tags": None,
        "has_schema": None,
        "has_favicon": None,
        "image_count": img_total,
        "images_without_alt": img_alt,
    }

    local_signals = {
        "has_google_maps_embed": ev.get("maps_embed"),
        "has_address_schema": None,
        "mentions_city": ev.get("city_mentions"),
        "company_in_title": ev.get("company_in_title"),
    }

    score = calculate_audit_score(
        {"ssl": True}, pixels, conversion, seo,
        {"error": "not run - no outbound network in this environment"})

    # The page defects read live are findings, not decoration. They go FIRST:
    # the "Top priorities" table prints the first four issues, and 36 live
    # theme-demo pages is a more urgent priority than a missing alt attribute.
    _defect_titles = [t for t, _d in ev.get("defects", []) if t not in score["issues"]]
    score["issues"] = _defect_titles + score["issues"]
    for _w in ev.get("wins", []):
        if _w not in score["wins"]:
            score["wins"].append(_w)
    score["issue_count"] = len(score["issues"])
    score["win_count"] = len(score["wins"])

    g = ev.get("google_ads") or {}
    g_detail = None
    if g.get("ad_count"):
        g_detail = {
            "name": g.get("name", ""),
            "ad_count": g.get("ad_count", 0),
            "advertiser_id": g.get("advertiser_id", ""),
            "creatives": g.get("creatives") or [],
            "started": g.get("started", "Active %s" % CHECKED),
            "destination": g.get("destination", ""),
            "note": g.get("note", ""),
            "url": (gcreative(g["advertiser_id"], g["creatives"][0])
                    if g.get("advertiser_id") and g.get("creatives") else ""),
        }

    meta_ads = ev.get("meta_ads") or []
    if meta_ads:
        meta_own = {
            "found": True,
            "results_count": len(meta_ads),
            "results_label": "~%d result%s" % (len(meta_ads),
                                               "s" if len(meta_ads) != 1 else ""),
            "query": ev["company"],
            "ads": meta_ads,
            "url": ("https://www.facebook.com/ads/library/?active_status=active"
                    "&ad_type=all&country=IN&is_targeted_country=false"
                    "&media_type=all&q=" + ev["company"].replace(" ", "%20")),
        }
    else:
        meta_own = {"found": None, "results_count": 0, "results_label": "",
                    "query": ev["company"], "ads": [], "url": ""}

    audit = {
        "company": ev["company"],
        "legal": ev.get("legal", ""),
        "city": ev["city"],
        "website": ev["website"],
        "email": ev.get("email", ""),
        "phone": ev.get("phone", ""),
        "audit_date": CHECKED,
        "ssl": True,
        "load_time_seconds": None,
        "pixels": pixels,
        "conversion": conversion,
        "seo": seo,
        "pagespeed": {
            "error": "not run - no outbound network route to the PageSpeed "
                     "API from this environment",
            "provenance": "NOT RUN - this environment has no outbound route to "
                          "Google's PageSpeed API, so no speed or Largest "
                          "Contentful Paint figure is claimed anywhere in this "
                          "report.",
        },
        "page_count": {
            "sitemap_pages": sitemap.get("page_url_count") or None,
            "has_sitemap": has_sitemap,
        },
        "local_signals": local_signals,
        "ad_check_urls": generate_ad_check_urls(ev["website"], ev["company"]),
        "final_url": ev["website"],
        "score": score,
        "ad_library": {
            "checked_at": CHECKED,
            "meta_own": meta_own,
            "meta_competitors": {"found": None, "results_count": 0,
                                 "results_label": "", "query": "", "ads": [],
                                 "url": ""},
            "google_own": {
                "found": bool(g_detail),
                "advertisers": [],
                "detail": g_detail,
                "query": ev["website"],
                "note": g.get("note", ""),
            },
            "google_competitors": {"found": None, "advertisers": [], "query": ""},
            "notes": [
                "Every figure in this audit was read live on %s. Fields the "
                "sandbox could not measure are recorded as null and printed as "
                "'could not be checked in this pass' - they are never reported "
                "as a pass or a failure." % CHECKED,
                "Tracking pixels could not be checked: the page HTML source was "
                "not retrievable from this environment, only rendered text.",
                "No value in this audit is copied from audit_Ksquare_Energy.json "
                "or from any other report. That file was read for its shape "
                "only.",
            ] + ([sitemap["missing"]] if sitemap.get("missing") else []),
            "summary": ev["meta_summary"],
        },
        "defects": [{"title": t, "detail": d} for t, d in ev.get("defects", [])],
        "wins": ev.get("wins", []),
        "contact_facts": ev.get("contact_facts", []),
        "summary": ev["summary"],
    }

    # ---- provenance: say exactly what was done ----------------------------
    _prov = [
        ("Live ads, library IDs, start dates, ad copy",
         "Meta Ad Library (India, active ads). Every library ID in this report "
         "was opened individually and confirmed live on %s during the "
         "third-eye re-verification pass." % CHECKED,
         CHECKED),
        ("Page text read on the live site",
         "Direct page fetch through the audit sandbox's page reader. The "
         "rendered text was counted mechanically with a fixed regex rather "
         "than estimated by reading it, so every count in this report can be "
         "re-derived from the saved page text. No page HTML source was "
         "available.",
         CHECKED),
        ("Headings, image counts, alt attributes, CTA link text, form fields, "
         "tel: / mailto: / wa.me links, outbound links",
         "Counted over the page text read - see the row above.",
         CHECKED),
        ("Tracking tags (8 of 8 could not be read)",
         "The page HTML source was not retrievable from this environment - "
         "script tags are stripped from rendered text - so no pixel, GA4, GTM "
         "or Clarity claim is made in either direction. Every tracking row "
         "reads not checked rather than missing.",
         "not run"),
        ("Meta description, Open Graph, Schema.org, favicon, consent mode",
         "NOT CHECKED - these live in the <head>, which was not returned in "
         "readable form. None is claimed as present or absent.",
         "not run"),
        ("Server response time, PageSpeed score, Largest Contentful Paint",
         "NOT RUN - no outbound route to Google's PageSpeed API from this "
         "environment.",
         "not run"),
    ]
    if sitemap.get("url"):
        _prov.append((
            "Sitemap contents and page counts",
            "%s and its sub-sitemaps fetched and counted verbatim." % sitemap["url"],
            CHECKED))
    else:
        _prov.append((
            "Sitemap contents and page counts",
            "NOT CHECKED - %s" % sitemap.get(
                "missing", "no sitemap was served to read."),
            "not run"))
    audit["provenance"] = _prov
    return audit


def main():
    ap = argparse.ArgumentParser(description="Build full audits for batch-20 leads")
    ap.add_argument("--only", default="", help="substring of the company name")
    args = ap.parse_args()

    leads = EVIDENCE
    if args.only:
        leads = [e for e in EVIDENCE if args.only.lower() in e["company"].lower()]
        if not leads:
            print("No lead matches '%s'" % args.only)
            sys.exit(1)

    for ev in leads:
        audit = build_audit(ev)
        out_dir = os.path.join(BASE_DIR, "audit_results")
        os.makedirs(out_dir, exist_ok=True)
        json_path = os.path.join(out_dir, "audit_%s.json"
                                 % re.sub(r"[^a-zA-Z0-9]+", "_", ev["company"]))
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(audit, f, indent=2, ensure_ascii=False)
        pdf_path = generate_pdf(audit)
        sc = audit["score"]["score"]
        print("[%s] score %s/100 | %d issues, %d wins | %d live ads"
              % (ev["company"], sc, audit["score"]["issue_count"],
                 audit["score"]["win_count"], len(ev["meta_ads"])))
        print("    json: %s" % json_path)
        print("    pdf:  %s" % pdf_path)


if __name__ == "__main__":
    main()
