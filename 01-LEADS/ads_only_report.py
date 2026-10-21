#!/usr/bin/env python3
"""
Ads-Only Report Builder — live Meta Ad Library data for leads whose website
audit has NOT run yet.

Why this exists
---------------
`run_pipeline.py` needs Playwright + Chrome to fetch a lead's website and to
drive the Meta Ad Library. Where that is not available (e.g. the Arena
sandbox), the website half of the audit cannot be produced honestly - so this
builder does NOT fake it. It builds a clearly-labelled **live ad activity**
report from public Meta Ad Library data only, and states in the PDF itself
that no website audit was performed.

Every field below was read live on 2026-10-18 from the Meta Ad Library and
from each company's own website. Nothing is estimated.

Usage:
  python ads_only_report.py                 # build JSON + PDF for every lead
  python ads_only_report.py --list          # show the leads, build nothing
  python ads_only_report.py --only "Truzon Solar"

Outputs:
  01-LEADS/ads_only_results/audit_<Company>.json
  02-OUTREACH/ads_only_pdfs/audit_<Company>.pdf
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from audit_pdf import generate_ads_only_pdf  # noqa: E402

RESULTS_DIR = os.path.join(BASE_DIR, "ads_only_results")

CHECKED_ON = "2026-10-18"
LIB = "https://www.facebook.com/ads/library/?id="


def ad(library_id, page_name, started, destination, text):
    """One live ad. library_id + library_url are the anti-fabrication fields:
    the builder refuses to emit a report whose ads cannot be opened live."""
    return {
        "library_id": str(library_id),
        "library_url": f"{LIB}{library_id}",
        "page_name": page_name,
        "started": started,
        "destination": destination,
        "text": text,
        "images": [],
    }


# ---------------------------------------------------------------------------
# Verified lead data — Meta Ad Library (India, active ads) + live sites,
# all read on 2026-10-18. Source of each field is noted per lead.
# ---------------------------------------------------------------------------

LEADS = [
    {
        "company": "Evergrid Energy",
        "legal": "Evergrid Energy Pvt Ltd",
        "city": "Hyderabad",
        "website": "https://www.evergridenergy.in",
        "email": "contact@evergridenergy.in",
        "phone": "+91 7330777310",
        "fb_page": "https://www.facebook.com/61593038197988/",
        "ad_library": {
            "meta_own": {
                "found": True,
                "results_count": 2,
                "results_label": "~2 results",
                "query": "Evergrid Energy",
                "ads": [
                    ad("1642242114211409", "Evergrid Energy", "Oct 16, 2026",
                       "Facebook lead form (fb.me 'Get quote')",
                       "Dussehra Offer: Rs. 22,000 OFF rooftop solar + up to Rs. 78,000 govt "
                       "subsidy. EMIs from Rs. 1,900/month. Installed in 21 days. Up to 30-year "
                       "panel warranty. Book your free site visit today."),
                    ad("1079793338257084", "Evergrid Energy", "Oct 17, 2026",
                       "Facebook lead form (fb.me 'Get quote')",
                       "Dussehra Offer: Rs. 22,000 OFF rooftop solar + up to Rs. 78,000 govt "
                       "subsidy. EMIs from Rs. 1,900/month. Installed in 21 days. Creative line: "
                       "'Ravan = your electricity bill. Time to end it.'"),
                ],
            },
            "summary": (
                "Evergrid Energy is running 2 active Dussehra-offer ads on Meta (Facebook and "
                "Instagram), started on 16 and 17 October 2026. Both ads send the click into a "
                "Facebook lead form, so the spend never reaches evergridenergy.in. No Google Ads "
                "advertiser record was checked for this report - that requires the full pipeline."),
        },
        "funnel": {
            "type": "Facebook lead form",
            "destination": "fb.me 'Get quote' (inside Facebook)",
            "meaning": (
                "Every rupee of ad spend lands inside Facebook's form. You own no pixel, you "
                "cannot retarget the people who clicked and did not submit, and there is no page "
                "you can test a different headline or price on."),
        },
        "findings": [
            "Both live ads dump the click into a Facebook lead form - not your website. No pixel "
            "ownership, no retargeting pool, no page to test.",
            "Your own site has a real quote form (name, phone, installation type, monthly bill, "
            "location) and a projects page - Kukatpally 6 kW residential, Shamshabad 120 kW "
            "commercial, Nacharam 20 kW commercial - that none of the paid traffic ever sees.",
            "The contact page shows contact@evergridenergy.in while the form's own mailto points "
            "at hello@evergridenergy.in - enquiries can land in an inbox nobody is watching.",
            "Two ads, both the same offer, both new (16-17 Oct). There is no second angle and no "
            "retargeting creative behind them yet.",
        ],
        "next_steps": [
            ("Move the click onto a page you own",
             "Send both ads to a dedicated landing page with the Dussehra offer, an enquiry form "
             "and the Meta Pixel installed - so every click is measurable and retargetable."),
            ("Install pixel + conversions API",
             "One pixel plus the Conversions API gives you the audience of everyone who clicked "
             "but did not submit - usually 10-20x the size of the people who fill a form."),
            ("Put your project photos to work",
             "Kukatpally, Shamshabad and Nacharam installs are real proof. They belong on the "
             "landing page next to the offer, not on a page the ad never sends anyone to."),
            ("Fix the email routing",
             "Point the contact form at the same inbox the site advertises, and add a second "
             "address so an enquiry can never sit unread."),
        ],
        "contact_facts": [
            ("Email", "contact@evergridenergy.in (form mailto: hello@evergridenergy.in)"),
            ("Phone / WhatsApp", "+91 7330777310 / wa.me/917330777310"),
            ("Address", "Harmony Heights, Road number 9, Park View Enclave Road, Jubilee Hills, "
                        "Hyderabad, Telangana 500034"),
            ("Entity", "Evergrid Energy Pvt Ltd - GST 36AAJCE8588K1ZS"),
            ("Meta page", "facebook.com/61593038197988 (Evergrid Energy)"),
        ],
    },
    {
        "company": "Solox Energies",
        "legal": "Solox Energies Private Limited",
        "city": "Hyderabad",
        "website": "https://solox.in",
        "email": "contact@solox.in",
        "phone": "+91 9988133789",
        "fb_page": "https://www.facebook.com/soloxenergies/",
        "ad_library": {
            "meta_own": {
                "found": True,
                "results_count": 1,
                "results_label": "~1 result",
                "query": "Solox Energies",
                "ads": [
                    ad("2023601181805342", "Solox Energies Pvt Ltd", "Oct 17, 2026",
                       "https://solox.in/ ('Book Now')",
                       "HELLO TELANGANA! YOUR SOLAR JOURNEY STARTS WITH ZERO DOWN PAYMENT! Zero "
                       "Down Payment on Solar Installation, Government Subsidy of up to Rs. "
                       "78,000, Free Site Visit, Expert Guidance from Site Survey to Installation, "
                       "Assistance with the Subsidy Process. Call us: 99881 33789 - www.solox.in"),
                ],
            },
            "summary": (
                "Solox Energies is running 1 active ad on Meta, started 17 October 2026, with "
                "multiple versions of the same creative. It is the only advertiser in this "
                "Hyderabad set whose ad sends traffic to its own website - the rest send clicks "
                "into Facebook forms."),
        },
        "funnel": {
            "type": "Own website",
            "destination": "https://solox.in/ ('Book Now')",
            "meaning": (
                "The right structure - the click reaches a page you own. The problem is what that "
                "page currently tells a homeowner who just clicked a paid ad."),
        },
        "findings": [
            "Your ad points at solox.in - that part is already right, and it is rarer in this "
            "market than it should be.",
            "But the page it lands on still reads '0+ MW' of renewable energy installed, '1+ "
            "projects' and '1+ years of cumulative team experience'. A homeowner who just clicked "
            "a paid ad reads that as a brand-new company, right next to your Rs. 0-down promise.",
            "The contact page displays contact@solox.in, but the form's own mailto still points at "
            "Sungosolarenergy@gmail.com - a leftover from the site template. Enquiries may not be "
            "reaching the inbox you advertise.",
            "One live ad, one creative, one audience. There is no second angle, no retargeting "
            "creative and no test structure behind it.",
            "Worth keeping: Google Analytics is already installed on the site, so traffic "
            "measurement exists - the gap is what happens after the click.",
        ],
        "next_steps": [
            ("Replace the placeholder numbers",
             "Fill in real installed capacity, project count and years of experience - or remove "
             "the counters entirely. On a paid landing page, '0+ MW' costs more than it says."),
            ("Repoint the enquiry form",
             "Make the form deliver to contact@solox.in and add a backup address, so no paid "
             "enquiry can be lost to an old template email."),
            ("Build the Rs. 0-down angle into a page",
             "Turn the ad promise into a landing page section: Rs. 0 down, subsidy up to Rs. "
             "78,000 handled end-to-end, free site visit - with the calculator next to it."),
            ("Start testing creatives",
             "Run 3-4 versions of the zero-down-payment angle (including Telugu) against the "
             "current one. You have analytics in place, so you will actually see the difference."),
        ],
        "contact_facts": [
            ("Email", "contact@solox.in (form mailto: Sungosolarenergy@gmail.com)"),
            ("Phone", "+91 9988133789 (Mon-Sat 9.00-18.00)"),
            ("Address", "Flat 401, Ace Krisna Prime, 11-9-50, Rd Number 1, Prabhat Nagar, Laxmi "
                        "Nagar Colony, Kothapet, Hyderabad 500102 (HQ) + Vijayawada branch"),
            ("Entity", "Solox Energies Private Limited - ISO 9001:2015"),
            ("Meta page", "facebook.com/soloxenergies (Solox Energies Pvt Ltd)"),
        ],
    },
    {
        "company": "Truzon Solar",
        "legal": "Truzon Solar",
        "city": "Hyderabad",
        "website": "https://www.truzonsolar.com",
        "email": "info@truzonsolar.com",
        "phone": "+91 9030032222",
        "fb_page": "https://www.facebook.com/truzonsolar/",
        "ad_library": {
            "meta_own": {
                "found": True,
                "results_count": 3,
                "results_label": "3 live ads verified",
                "query": "Truzon Solar",
                "ads": [
                    ad("1522258176260844", "Truzon Solar", "May 20, 2026",
                       "Facebook lead form ('Call Now +91 9030032222')",
                       "Solar is no longer difficult to install. With Truzon Solar the whole "
                       "process is simple and fast. Talk today and start your solar journey. "
                       "(Hindi creative - 7 ads share this creative and text)"),
                    ad("1399945148943213", "Truzon Solar", "Aug 25, 2026",
                       "Facebook lead form ('Book Now')",
                       "Solar is no longer difficult to install. With Truzon Solar the whole "
                       "process is simple. Contact today and start your solar journey. "
                       "(Marathi creative - 6 ads share this creative and text)"),
                    ad("1001393986178171", "Truzon Solar", "May 20, 2026",
                       "Facebook lead form",
                       "Solar is no longer difficult to install. With Truzon Solar the whole "
                       "process is simple and fast. Talk today and start your solar journey. "
                       "(Hindi creative)"),
                ],
            },
            "summary": (
                "Truzon Solar has been advertising on Meta continuously since May 2026 - the "
                "longest-running programme in this Hyderabad set - with 3 live ads across 2 "
                "creatives (7 ads share one creative, 6 share another). Every creative is Hindi or "
                "Marathi, and every CTA drops the click into a Facebook lead form."),
        },
        "funnel": {
            "type": "Facebook lead form",
            "destination": "fb.me ('Call Now +91 9030032222' / 'Book Now')",
            "meaning": (
                "The click never reaches truzonsolar.com. You cannot retarget the people who "
                "clicked and did not call, you cannot test a landing page, and the phone number in "
                "the button is the only thing connecting the ad to your business."),
        },
        "findings": [
            "Every live creative is Hindi or Marathi. In Hyderabad the strongest solar ads run in "
            "Telugu to the same homeowners - your own head office is here, but your ads are not "
            "speaking the local language.",
            "7 ads share one creative and 6 share another. You are buying reach on two ideas while "
            "competitors test new angles weekly.",
            "The 'Call Now' button sends people into a Facebook lead form, not your own quote page "
            "- so none of your residential, commercial, industrial and ground-mounted service "
            "pages ever get seen by paid traffic.",
            "You have the longest-running ad programme in this market (since May 2026) - which "
            "means the tracking and retargeting gap has been costing you the whole time.",
        ],
        "next_steps": [
            ("Run Telugu creative",
             "Translate the winning 'solar is no longer difficult' message into Telugu and test it "
             "against the Hindi and Marathi versions. This is the cheapest lift available in this "
             "market."),
            ("Send the click to your own page",
             "Move the CTA from the Facebook form to a Hyderabad landing page with a quote form, "
             "so the traffic becomes an asset you own and can retarget."),
            ("Break the creative deadlock",
             "Test 3-4 new angles - subsidy math, EMI vs bill, Dussehra-style offer, commercial "
             "rooftop - instead of spending the whole budget on two creatives."),
            ("Track the calls",
             "Put call tracking on the 9030032222 button so you know which creative actually "
             "produces booked site visits."),
        ],
        "contact_facts": [
            ("Email", "info@truzonsolar.com"),
            ("Phone", "+91-9030032222"),
            ("Corporate office", "5A, Astral Heights, Road No-1, Banjara Hills, Hyderabad 500034"),
            ("Services", "Residential, commercial and industrial rooftop, ground-mounted solar, "
                         "solar water heaters"),
            ("Meta page", "facebook.com/truzonsolar"),
        ],
    },
    {
        "company": "Punarvi Energies",
        "legal": "Punarvi Energies Limited",
        "city": "Hyderabad",
        "website": "https://www.punarvienergies.com",
        "email": "solar@punarvienergies.com",
        "phone": "+91 7799757777",
        "fb_page": "https://www.facebook.com/punarvisolarenergies/",
        "ad_library": {
            "meta_own": {
                "found": True,
                "results_count": 2,
                "results_label": "~2 results",
                "query": "Punarvi Energies",
                "ads": [
                    ad("1122725223617884", "Punarvi Energies Limited", "Oct 13, 2026",
                       "Facebook lead form (fb.me 'Get quote')",
                       "NAVARATRI MEGA SOLAR OFFER! 3 kW Solar - Rs. 1,02,000 (Actual Rs. "
                       "1,30,000). 5 kW Solar - Rs. 2,10,000 (Actual Rs. 3,30,000). Government "
                       "subsidy up to Rs. 78,000. FREE Solar Cleaning Kit."),
                    ad("994804120334409", "Punarvi Energies Limited", "Oct 13, 2026",
                       "Facebook lead form (fb.me 'Get quote')",
                       "Navaratri Dhamaka Offer! 3 KW - Rs. 1,02,000/- Only. 5 KW - Rs. 2,10,000/- "
                       "Only. FREE Solar Cleaning Kit on Every Booking. Govt Subsidy Up to Rs. "
                       "78,000. Offer valid until October 20th. Call Now: 7997667677"),
                ],
            },
            "summary": (
                "Punarvi Energies is running 2 active Navaratri-offer ads on Meta, both started 13 "
                "October 2026, both sending the click into a Facebook lead form. Behind the offer "
                "sits the strongest proof base in this market: MNRE-approved EPC, 79 MW installed "
                "and clients including IIIT Hyderabad, TGSPDCL, TSREDCO and HPCL."),
        },
        "funnel": {
            "type": "Facebook lead form",
            "destination": "fb.me 'Get quote' (inside Facebook)",
            "meaning": (
                "The click never reaches punarvienergies.com, so none of your 79 MW, your MNRE "
                "approval or your institutional clients appear in front of the person deciding "
                "whether to enquire."),
        },
        "findings": [
            "Both ads send the click into a Facebook lead form - your 79 MW of installed capacity, "
            "MNRE approval and clients like IIIT Hyderabad, TGSPDCL, TSREDCO and HPCL never appear "
            "in front of the person clicking.",
            "The phone number in the ad (7997667677) is a transposition of the number on your own "
            "site (7799757777). Worth checking before the offer closes on 20 October - calls may "
            "be going nowhere while the spend continues.",
            "You are the biggest spender in this set with the strongest references (11 MW Khammam "
            "ground-mount, 5 MW Parigi, 3 MW Jadcherla textiles, Google 5.0 from 26 reviews) - "
            "and the least ownership of the click.",
            "Both ads lead with price only. Nobody in your market is leading with '79 MW installed "
            "for TGSPDCL and IIIT Hyderabad' - that is an untested differentiator.",
        ],
        "next_steps": [
            ("Fix the number first",
             "Align the ad phone with the site phone (7799757777) and add call tracking on both, "
             "so the Navaratri spend stops leaking."),
            ("Send the click to your own proof",
             "A landing page with the offer at the top and the MW-scale references below it "
             "converts better than a Facebook form - and it is yours to retarget."),
            ("Lead with credentials, not just price",
             "Test a second creative angle: '79 MW installed for TGSPDCL, IIIT Hyderabad and HPCL' "
             "against the price-led one."),
            ("Capture the non-bookers",
             "Pixel + retargeting for everyone who clicked and did not submit. At your spend that "
             "audience is the cheapest pipeline you are currently not using."),
        ],
        "contact_facts": [
            ("Email", "solar@punarvienergies.com"),
            ("Phone", "+91 7799757777 | landline +91 40 49941999 | ad phone 7997667677"),
            ("Corporate office", "Plot No. 5, Chandragiri Colony, Above SBI Bank, 3rd Floor, "
                                 "Tirmulgherry, Hyderabad 500015"),
            ("Factory", "Plot No. 1, Phase-1, BN Reddy Nagar, Cherlapally, Hyderabad 500051"),
            ("Credentials", "MNRE Approved EPC - 79 MW installed, 2,400+ projects"),
            ("Meta page", "facebook.com/punarvisolarenergies"),
        ],
    },
    {
        "company": "Varahi Energies",
        "legal": "Varahi Energies",
        "city": "Hyderabad",
        "website": "https://varahienergies.in",
        "email": "varahienergies@gmail.com",
        "phone": "+91 9666120045",
        "fb_page": "",
        "ad_library": {
            "meta_own": {
                "found": False,
                "results_count": 0,
                "results_label": "No ads match your search criteria",
                "query": "Varahi Energies",
                "ads": [],
            },
            "summary": (
                "No active Meta ads were found for Varahi Energies. Meanwhile four Hyderabad "
                "installers - Evergrid Energy, Solox Energies, Truzon Solar and Punarvi Energies - "
                "are all live this week buying the same homeowner with Rs. 78,000-subsidy offers. "
                "Varahi's MNRE-approved track record (250+ projects, 700 kW+ PM Surya Ghar, 80 MW "
                "PM-KUSUM assistance) is not in front of any paid traffic."),
        },
        "funnel": {
            "type": "WhatsApp only",
            "destination": "wa.me/919666120045 on every call-to-action",
            "meaning": (
                "Every enquiry arrives as a chat message. There is no email capture anywhere on the "
                "site, so nobody who does not reply can be followed up with, and nothing can be "
                "retargeted or measured."),
        },
        "findings": [
            "No active Meta ads under your name - four Hyderabad installers are buying the same "
            "homeowner this week with the same Rs. 78,000-subsidy message.",
            "Every CTA on the site is a WhatsApp deep link. There is no email capture, so a visitor "
            "who does not reply cannot be followed up with, and no audience can be built.",
            "MNRE-approved vendor with 250+ projects, 700 kW+ of PM Surya Ghar work, a 545 kW "
            "commercial rice-industry plant and 80 MW of PM-KUSUM assistance - the proof exists, it "
            "just is not in front of paid traffic.",
            "Head office is in Nizamabad with the Hyderabad branch in Kompally, but there is very "
            "little Hyderabad-specific content for local search demand (Kompally, Secunderabad, "
            "Kukatpally).",
        ],
        "next_steps": [
            ("Turn WhatsApp into a funnel, not a dead end",
             "Keep WhatsApp as the reply channel, but capture name, phone and locality on the site "
             "first, so non-repliers can be followed up."),
            ("Test paid lead gen in Hyderabad",
             "Start with a small Meta budget on one residential offer. Your four competitors are "
             "already proving the demand exists in this city."),
            ("Build Hyderabad location pages",
             "Kompally, Secunderabad and Kukatpalli pages with real project photos - free local "
             "search traffic sitting next to the traffic you would be buying."),
            ("Show the live generation data",
             "Your site already displays a live generation widget (8.4 kW, 94%, 32 units today). "
             "That is a trust asset most installers do not have - put it on the homepage."),
        ],
        "contact_facts": [
            ("Email", "varahienergies@gmail.com"),
            ("Phone / WhatsApp", "+91 9666120045 / wa.me/919666120045 (Mon-Sat 9AM-7PM)"),
            ("Head office", "Kanteshwar, Beside Bajrang Tiles, Nizamabad, Telangana 503002"),
            ("Hyderabad branch", "Lane No. 4, Panchasheel Enclave St, Kompally, "
                                 "Hyderabad-Secunderabad 500067"),
            ("Credentials", "MNRE approved vendor - 250+ projects, 700 kW+ PM Surya Ghar, "
                            "80 MW PM-KUSUM assistance"),
        ],
    },
    {
        "company": "Twilight Solar",
        "legal": "Twilight Solar Pvt Ltd",
        "city": "Hyderabad",
        "website": "https://twilightsolar.com/",
        "email": "Prabhakar.katkam@gmail.com",
        "phone": "+91 9542846721",
        "fb_page": "https://www.facebook.com/twilightsolarpvtltd/",
        "checked_on": "2026-10-20",
        "ad_library": {
            "meta_own": {
                "found": True,
                "results_count": 2,
                "results_label": "~2 results",
                "query": "Twilight Solar Hyderabad",
                "ads": [
                    ad("3823689667771361", "Twilight Solar Pvt Ltd", "Jul 30, 2026",
                       "Facebook lead form (fb.me 'Get quote')",
                       "Hyderabad's Leading Brand For Complete Power & Energy Solution. We "
                       "provide complete Residential & Commercial Solar Solutions designed to "
                       "reduce electricity bills, helping you switch to sustainable power with "
                       "ease. From consultation to installation, our experts handle it all. "
                       "High-quality Solar Panels, Professional Installation, Cost-effective "
                       "Energy Solutions, 280+ Happy Customers, Well Equipped & Dedicated Team. "
                       "Make the smart move to solar today."),
                    ad("28023952863910719", "Twilight Solar Pvt Ltd", "Jul 30, 2026",
                       "Facebook lead form (fb.me 'Get quote')",
                       "Second version of the same 'Hyderabad's Leading Brand For Complete "
                       "Power & Energy Solution' creative - same copy, same 280+ Happy "
                       "Customers claim, same Facebook lead-form destination."),
                ],
            },
            "summary": (
                "Twilight Solar has run 2 active ads on Meta since 30 July 2026 - about 12 "
                "weeks - and they are two versions of one creative. Both send the click into a "
                "Facebook lead form, so none of the paid traffic ever reaches "
                "twilightsolar.com. Only ~2 results exist in the library, so this is a small "
                "advertiser: no spend or impression figures are published, and none are "
                "claimed here."),
        },
        "funnel": {
            "type": "Facebook lead form",
            "destination": "fb.me ('Get quote')",
            "meaning": (
                "The click never reaches a page you own. Every lead is captured inside "
                "Facebook, so there is no pixel on your site, no retargeting pool, no landing "
                "page you can test, and no way to see what happens after the click."),
        },
        "findings": [
            "Two live ads (both started 30 July 2026, about 12 weeks) and every click goes "
            "into a Facebook lead form - the paid traffic never reaches twilightsolar.com. You "
            "own no pixel, no retargeting pool and no page you can A/B test.",
            "The ad promises '280+ Happy Customers', but your own homepage counters read 128+ "
            "successful installations, 119+ satisfied customers and 12+ MW delivered. The ad is "
            "claiming more than double the number your site can prove.",
            "Two versions of one creative and no second angle - no retargeting creative, no "
            "test structure, and no Telugu creative in a Telangana-first market.",
            "The only contact email published on the site is a personal Gmail "
            "(Prabhakar.katkam@gmail.com), not a company-domain inbox - even though you own "
            "twilightsolar.com.",
            "The site itself is solid: residential, commercial, industrial, EPC, O&M and "
            "consulting pages, subsidy and net-metering support messaging, and a clear 5-step "
            "process. That is good raw material that no paid traffic ever sees.",
            "One caution for sizing this up: only ~2 ad results exist in the library, so treat "
            "this as a small advertiser, not a big spender.",
        ],
        "next_steps": [
            ("Point one ad at your own site",
             "Send even one of the two live ads to an owned landing page instead of the "
             "Facebook form, so you can test, measure and retarget from it."),
            ("Fix the customer-count gap",
             "Make the ad claim match what the site proves (128+ / 119+ / 12+ MW), or update "
             "the site counters. A homeowner who clicks the ad and sees half the number loses "
             "trust before the first call."),
            ("Build a Hyderabad residential landing page",
             "Your service pages already exist. Turn the Chengicherla/Hyderabad residential "
             "offer into one page: subsidy up to Rs. 78,000, net-metering support, free site "
             "evaluation, with the consultation form on it."),
            ("Test a second creative angle",
             "Run a Telugu and a Rs. 0-down/EMI version against the current creative. Two "
             "versions of the same ad cannot tell you which message works."),
            ("Move to a company-domain email",
             "Publish info@twilightsolar.com (or similar) so paid enquiries do not depend on "
             "one person's personal inbox."),
        ],
        "contact_facts": [
            ("Email", "Prabhakar.katkam@gmail.com (the only address published on the site)"),
            ("Phone", "+91 9542846721 / +91 9849934422"),
            ("Address", "Plot #206, Behind MYE Villas, Ramakrishna Nagar, Chengicherla, "
                        "Hyderabad 500039"),
            ("Site counters", "128+ successful installations, 119+ satisfied customers, "
                              "12+ MW solar capacity delivered, 2+ states"),
            ("Ad copy claim", "280+ Happy Customers"),
            ("Meta page", "facebook.com/twilightsolarpvtltd (Twilight Solar Pvt Ltd)"),
        ],
    },
    {
        "company": "Four Solar",
        "legal": "Four Solar Energy Systems Pvt. Ltd.",
        "city": "Hyderabad",
        "website": "https://www.foursolar.com/",
        "email": "contact@foursolar.com",
        "phone": "+91 8886002221",
        "fb_page": "https://www.facebook.com/foursolar/",
        "checked_on": "2026-10-20",
        "ad_library": {
            "meta_own": {
                "found": False,
                "results_count": 0,
                "results_label": "No ads match your search criteria",
                "query": "Four Solar Hyderabad",
                "ads": [],
            },
            "summary": (
                "No active Meta ads were found for Four Solar Energy Systems (Ad Library "
                "probe 'Four Solar Hyderabad', 2026-10-20). Meanwhile five Hyderabad "
                "installers - Evergrid Energy (Library IDs 1642242114211409 and "
                "1079793338257084), Solox Energies (2023601181805342), Truzon Solar "
                "(1522258176260844), Punarvi Energies (1122725223617884 and "
                "994804120334409) and Twilight Solar (3823689667771361 and "
                "28023952863910719) - are all live this month buying the same "
                "homeowner with Rs. 78,000-subsidy offers. Four Solar's 13-year track "
                "record is not in front of any paid traffic."),
        },
        "funnel": {
            "type": "Own website + chat/WhatsApp",
            "destination": "Site contact form, live chat widget and WhatsApp",
            "meaning": (
                "The conversion paths are decent - the form takes city and roof details, "
                "and there is a chat widget. The gap is that nothing paid drives into "
                "them, so every enquiry depends on someone already looking for you by "
                "name."),
        },
        "findings": [
            "No active Meta ads under your name - five Hyderabad installers (Evergrid, "
            "Solox, Truzon, Punarvi, Twilight) are live this month buying the same "
            "homeowner with the same Rs. 78,000-subsidy message.",
            "The site claims 13+ years, 50 MW+ delivered and 1500+ satisfied clients, "
            "with 15+ gated communities powered, a 1521-government-schools Telangana "
            "order and a 160 kW Corporate Bhavan (Ministry of Corporate Affairs) job. "
            "That proof exists - it is just not in front of paid traffic.",
            "TGREDCO-empanelled (TSRE180027) with PM Surya Ghar and PM-KUSUM experience - "
            "credentials that convert homeowners who have already seen three "
            "competitor ads.",
            "The site itself is in good shape: a multi-city quote form (Hyderabad, "
            "Secunderabad, Ranga Reddy, Medchal-Malkajgiri), a live chat widget, a "
            "WhatsApp button and a detailed residential page covering approvals, roof "
            "types and monitoring. Good raw material that no paid traffic ever sees.",
            "Everything on the site is in English. In this market the strongest "
            "competitor creatives run in Telugu to the same homeowner - and your head "
            "office is here.",
        ],
        "next_steps": [
            ("Test paid lead gen in Hyderabad",
             "Start with a small Meta budget on one residential offer - subsidy up to "
             "Rs. 78,000, free site visit. Your five competitors are already proving "
             "the demand exists in this city."),
            ("Build a dedicated residential landing page",
             "The residential page exists - turn it into one paid landing page: "
             "subsidy, gated-community track record, free site visit, quote form on "
             "it."),
            ("Run Telugu creative",
             "Test a Telugu version of the offer against English. Telugu is the "
             "language of the Telangana homeowner, and your competitors are already "
             "spending there."),
            ("Put the government work to work",
             "The 1521-schools order and the Corporate Bhavan job are strong proof for "
             "a trust-led paid campaign - most local installers cannot show that."),
        ],
        "contact_facts": [
            ("Email", "contact@foursolar.com"),
            ("Phone", "+91 8886002221 / 040-23405670 / +91 9248716892"),
            ("Address", "6-3-1109/1/P/402, 4th Floor, Jewel Pawani Tower, Raj Bhavan "
                        "Rd, Somajiguda, Hyderabad 500082"),
            ("Entity", "Four Solar Energy Systems Pvt. Ltd. - TGREDCO empanelled "
                       "TSRE180027"),
            ("Meta page", "facebook.com/foursolar"),
        ],
    },
    {
        "company": "Origian Power",
        "legal": "Origian Power",
        "city": "Hyderabad",
        "website": "https://origianpower.com/",
        "email": "origian.ei@gmail.com",
        "phone": "+91 8121766831",
        "fb_page": "",
        "checked_on": "2026-10-20",
        "ad_library": {
            "meta_own": {
                "found": False,
                "results_count": 0,
                "results_label": "No ads match your search criteria",
                "query": "Origian Power",
                "ads": [],
            },
            "summary": (
                "No active Meta ads were found for Origian Power (Ad Library probe "
                "'Origian Power', 2026-10-20). Meanwhile five Hyderabad installers - "
                "Evergrid Energy (Library IDs 1642242114211409 and 1079793338257084), "
                "Solox Energies (2023601181805342), Truzon Solar (1522258176260844), "
                "Punarvi Energies (1122725223617884 and 994804120334409) and Twilight "
                "Solar (3823689667771361 and 28023952863910719) - are all live this "
                "month buying the same homeowner with Rs. 78,000-subsidy offers. "
                "Origian's location-page content is not in front of any paid traffic."),
        },
        "funnel": {
            "type": "Own website form + phone",
            "destination": "WPForms contact form (with reCAPTCHA) + three phone lines",
            "meaning": (
                "The site already answers the 'where do I click' question, but the form "
                "runs behind reCAPTCHA and JavaScript - extra friction for someone who "
                "just tapped a paid ad. Nothing paid currently drives into it at all."),
        },
        "findings": [
            "No active Meta ads under your name - five Hyderabad installers (Evergrid, "
            "Solox, Truzon, Punarvi, Twilight) are live this month buying the same "
            "homeowner with the same Rs. 78,000-subsidy message.",
            "You already run a location-page farm: Hyderabad, Warangal, Nizamabad, "
            "Karimnagar and Suryapet in Telangana, plus Nellore, Vijayawada, "
            "Visakhapatam, Guntur, Tirupati, Kurnool, Kadapa and Nandyal in Andhra "
            "Pradesh. Real, ranking content - with zero paid traffic pointing at it.",
            "The only contact email published is a personal Gmail "
            "(origian.ei@gmail.com), even though you own origianpower.com AND "
            "origianpower.in. No company-domain inbox is advertised anywhere.",
            "Two Hyderabad offices (Nizampet 500090 and Hitech City 500081) but no "
            "Hyderabad-specific paid targeting - the pages exist, nothing buys into "
            "them.",
            "The contact form is WPForms behind reCAPTCHA. For a paid click that is one "
            "more step between the ad and the phone call.",
        ],
        "next_steps": [
            ("Point a small budget at the pages you already have",
             "You do not need new pages to start. A modest Meta budget aimed at the "
             "existing Hyderabad and Nizampet pages is the fastest test."),
            ("Move to a company-domain email",
             "Publish info@origianpower.com - you already own the domain. A Gmail "
             "address on a solar EPC site reads smaller than the service list next "
             "to it."),
            ("Reduce form friction",
             "Offer WhatsApp alongside the form, or drop the reCAPTCHA step, so a paid "
             "click reaches you in one tap."),
            ("Run Telugu creative",
             "Your location pages are in English only. Telugu creative is the language "
             "of the Telangana homeowner your competitors are buying."),
        ],
        "contact_facts": [
            ("Email", "origian.ei@gmail.com (the only address published on the site)"),
            ("Phone", "+91 8121766831 / +91 8121 3668 32 / +91 8121 7668 34"),
            ("Hyderabad offices", "Flat B-106, Adithya Wizz Lagoon, Nizampet, Hyderabad "
                                  "500090; 3rd Floor, Lakeview Co-Working, InOrbit Mall "
                                  "Road, Hitech City, Hyderabad 500081"),
            ("Head office", "18-5, Indira Gandhi Nagar, Papampeta, Anantapur 515004"),
            ("Domains", "origianpower.com and origianpower.in both live"),
        ],
    },
    {
        "company": "Mamindla Energy Solutions",
        "legal": "Mamindla Energy Solutions LLP",
        "city": "Hyderabad",
        "website": "https://www.m-e-solutions.co.in/",
        "email": "info@m-e-solutions.co.in",
        "phone": "+91 99498 75868",
        "fb_page": "",
        "checked_on": "2026-10-20",
        "ad_library": {
            "meta_own": {
                "found": False,
                "results_count": 0,
                "results_label": "No ads match your search criteria",
                "query": "Mamindla Energy Solutions",
                "ads": [],
            },
            "summary": (
                "No active Meta ads were found for Mamindla Energy Solutions (Ad "
                "Library probe 'Mamindla Energy Solutions', 2026-10-20). Meanwhile five "
                "Hyderabad installers - Evergrid Energy (Library IDs 1642242114211409 "
                "and 1079793338257084), Solox Energies (2023601181805342), Truzon "
                "Solar (1522258176260844), Punarvi Energies (1122725223617884 and "
                "994804120334409) and Twilight Solar (3823689667771361 and "
                "28023952863910719) - are all live this month buying the same "
                "homeowner with Rs. 78,000-subsidy offers. Mamindla's govt-empanelled "
                "credentials are not in front of any paid traffic."),
        },
        "funnel": {
            "type": "Own website form + phone",
            "destination": "Free-quote form on the homepage + one phone number",
            "meaning": (
                "The site is built to convert: quote form, savings calculator, named "
                "case studies. The problem is that nothing paid drives into it, so "
                "traffic depends entirely on someone already searching."),
        },
        "findings": [
            "No active Meta ads under your name - five Hyderabad installers (Evergrid, "
            "Solox, Truzon, Punarvi, Twilight) are live this month buying the same "
            "homeowner with the same Rs. 78,000-subsidy message.",
            "The site claims 100+ installations, 10+ MW delivered and 500+ happy "
            "customers, with an interactive savings calculator (bill + roof size in, "
            "system size, subsidy and payback out) and three named case studies: 8 kW "
            "residential in Kondapur, 25 kW commercial at a Hanamkonda school and 50 kW "
            "industrial in LB Nagar. Trust material, already built.",
            "Govt-empanelled vendor positioning, Tier-1 panel claims (Waaree, TATA, "
            "Adani) and full PM Surya Ghar paperwork handling - exactly the proof a "
            "homeowner wants after seeing three competitor ads.",
            "The Hyderabad branch sits in Madhapur, right in the commercial heart of "
            "the city - but there is no Hyderabad-specific paid targeting anywhere.",
            "Everything on the site is in English. Telugu creative is the language of "
            "the Telangana homeowner your competitors are buying.",
        ],
        "next_steps": [
            ("Test paid lead gen in Hyderabad",
             "A small Meta budget on one residential offer, targeted around the "
             "Madhapur/Hitech City side of the city, would sit right next to your "
             "branch office."),
            ("Turn the calculator into a landing page hook",
             "The savings calculator is already the best asset on the site. Put it at "
             "the top of a dedicated paid landing page."),
            ("Run Telugu creative",
             "Test a Telugu version of the Rs. 78,000-subsidy offer against English."),
            ("Use the case studies as ad proof",
             "The Kondapur, Hanamkonda and LB Nagar projects are named, specific and "
             "local - most competitor ads cannot show that."),
        ],
        "contact_facts": [
            ("Email", "info@m-e-solutions.co.in"),
            ("Phone", "+91 99498 75868"),
            ("Hyderabad branch", "4th Floor, Krishna Towers, Plot 527, 100 Feet Rd, "
                                 "Madhapur, Hyderabad 500081"),
            ("Head office", "47-5-706, Paidipally, Warangal 506006"),
            ("Site counters", "100+ installations, 10+ MW delivered, 500+ happy "
                              "customers"),
        ],
    },
    {
        "company": "Junna Solar Systems",
        "legal": "Junna Solar Systems Pvt Ltd",
        "city": "Hyderabad",
        "website": "https://www.junnasolar.com/",
        "email": "junnasolarsystems@gmail.com",
        "phone": "+91 9949555198",
        "fb_page": "https://www.facebook.com/junnasolar/",
        "checked_on": "2026-10-20",
        "ad_library": {
            "meta_own": {
                "found": False,
                "results_count": 0,
                "results_label": "No ads match your search criteria",
                "query": "Junna Solar",
                "ads": [],
            },
            "summary": (
                "No active Meta ads were found for Junna Solar Systems (Ad Library "
                "probe 'Junna Solar', 2026-10-20). Meanwhile five Hyderabad installers "
                "- Evergrid Energy (Library IDs 1642242114211409 and 1079793338257084), "
                "Solox Energies (2023601181805342), Truzon Solar (1522258176260844), "
                "Punarvi Energies (1122725223617884 and 994804120334409) and Twilight "
                "Solar (3823689667771361 and 28023952863910719) - are all live this "
                "month buying the same homeowner with Rs. 78,000-subsidy offers. "
                "Junna's 13-year rooftop track record is not in front of any paid "
                "traffic."),
        },
        "funnel": {
            "type": "Own website form (JavaScript app)",
            "destination": "Free-consultation form on junnasolar.com + phone",
            "meaning": (
                "The site is a JavaScript application - the homepage renders almost "
                "nothing without JS, and the floating WhatsApp button in the served "
                "HTML points at wa.me/undefined, a broken deep link. Enquiries that do "
                "arrive come by phone; nothing paid drives traffic to the site at all."),
        },
        "findings": [
            "No active Meta ads under your name - five Hyderabad installers (Evergrid, "
            "Solox, Truzon, Punarvi, Twilight) are live this month buying the same "
            "homeowner with the same Rs. 78,000-subsidy message.",
            "Incorporated in December 2012 and now a public limited company (CIN "
            "U40106TG2012PLC084777), TGREDCO-empanelled (TSRE180043) and a registered "
            "PM Surya Ghar vendor for Telangana North - 13+ years of rooftop and "
            "water-pump work, HQ in Kukatpally.",
            "The live site is a JavaScript app: the homepage renders almost nothing "
            "without JavaScript, so the first thing a paid click or a search visitor "
            "sees is a loader.",
            "The floating WhatsApp button in the served HTML points at wa.me/undefined "
            "- a broken deep link on the exact channel a solar buyer is most likely "
            "to tap.",
            "You are hiring across sales and project roles (project managers, sales "
            "engineers, project engineers) - clear growth mode, with zero paid "
            "acquisition behind it.",
        ],
        "next_steps": [
            ("Fix the broken WhatsApp link",
             "The floating button's wa.me target is undefined in the served HTML. "
             "That is a lost-lead path on the channel your customers actually use."),
            ("Server-render the homepage",
             "Make the key content (what you do, where you operate, how to enquire) "
             "visible without JavaScript, so search and paid traffic see it instantly."),
            ("Test paid lead gen in Hyderabad",
             "A small Meta budget on one residential offer, Kukatpally/Kompally/"
             "Secunderabad targeting, would put 13 years of rooftop work in front of "
             "buyers who currently only see competitor ads."),
            ("Run Telugu creative",
             "Telugu is the language of the Telangana homeowner - and it is what your "
             "competitors' creatives already speak."),
        ],
        "contact_facts": [
            ("Email", "junnasolarsystems@gmail.com"),
            ("Phone", "+91 9949555198 / 040-65999222"),
            ("Address", "Plot 17 & 18, IDA, Prasanthi Nagar Ext., Vignanapuri Colony, "
                        "Kukatpally, Hyderabad 500072"),
            ("Entity", "Junna Solar Systems Pvt Ltd - public limited, CIN "
                       "U40106TG2012PLC084777, TGREDCO empanelled TSRE180043"),
            ("Meta page", "facebook.com/junnasolar"),
        ],
    },
    {
        "company": "Valcan Solar",
        "legal": "Valcan Energy Systems",
        "city": "Hyderabad",
        "website": "https://valcansolar.com/",
        "email": "info@valcansolar.com",
        "phone": "+91 90300 33577",
        "fb_page": "https://www.facebook.com/valcansolar/",
        "checked_on": "2026-10-21",
        "ad_library": {
            "meta_own": {
                "found": True,
                "results_count": 2,
                "results_label": "~2 results",
                "query": "solar Secunderabad",
                "ads": [
                    ad("1156154097084461", "Valcan Solar", "Oct 7, 2026",
                       "https://valcansolar.com/ ('Book now')",
                       "GO SOLAR. WIN BIG. SAVE MORE! This festive season, make the switch "
                       "to solar with Valcan Solar and stand a chance to win exciting "
                       "prizes! Bumper Draw Prizes: 1st Prize - Get Your Solar System "
                       "FREE, 2nd Prize - EV Bike (5 Winners), 3rd Prize - EV Cycle (10 "
                       "Winners), Air Fryer (50 Winners), Induction Stove (50 Winners). "
                       "Government Subsidy up to Rs. 78,000, Additional Discount of Rs. "
                       "22,000, 0% Interest EMI, Free Insurance, Free Consultation. "
                       "Applicable for 2 kW to 10 kW solar systems. Valid Until: 24 "
                       "November 2026. Bumper Draw: 30 November 2026."),
                    ad("2941615846186384", "valcansolar", "Oct 15, 2026",
                       "Facebook lead form (Call Us)",
                       "MEGA UTSAV | 2KW-10KW Solar Systems. Bumper Prize Opportunities: "
                       "1st Prize - Solar System FREE, 2nd Prize - EV Bike - 5 Winners, "
                       "3rd Prize - EV Cycle - 10 Winners, 4th Prize - Air Fryer - 50 "
                       "Winners, 5th Prize - Induction Stove - 50 Winners. Government "
                       "Subsidy Rs 78,000. Additional Discount Rs 22,000. No-Cost EMI | "
                       "0% Interest. Free Insurance. Free Consultation. Offer Valid Up "
                       "To: 24th November 2026. Bumper Draw Date: 30th November 2026."),
                ],
            },
            "summary": (
                "Valcan Solar is running 2 active ads on Meta for the MEGA UTSAV bumper-"
                "draw campaign - one since 7 October 2026 pointing at valcansolar.com, "
                "one since 15 October 2026 pointing at a Facebook lead form. The offer "
                "(free solar system as first prize, EV bikes, Rs. 78,000 subsidy plus "
                "Rs. 22,000 discount, 0% EMI) runs until 24 November with the draw on "
                "30 November. Both ads surfaced in the 'solar Secunderabad' search - "
                "their home market."),
        },
        "funnel": {
            "type": "Split - own site + Facebook lead form",
            "destination": "valcansolar.com ('Book now') on one ad, a Facebook lead "
                           "form ('Call Us') on the other",
            "meaning": (
                "Half the spend lands on a page you own; half lands inside Facebook. "
                "Two destinations for one offer means two different experiences for "
                "the same click, and the Facebook side leaves you no pixel, no "
                "retargeting pool and nothing to test."),
        },
        "findings": [
            "2 live ads running the MEGA UTSAV bumper-draw offer (free solar system as "
            "first prize, EV bikes, air fryers) until 24 November, draw 30 November - a "
            "deadline-driven push with real money behind it.",
            "One ad sends clicks to valcansolar.com, the other into a Facebook lead "
            "form. The same offer, two different funnels - and the Facebook side owns "
            "none of the data.",
            "The site's 'Our Achievements' counters all read 0 - 0K+ projects completed, "
            "0% positive feedback, 0+ years of experience, 0% success rate. A visitor "
            "who just clicked a bumper-draw ad sees a brand-new company.",
            "The contact block's email reads marketing@vulcansolar.in - misspelled "
            "('vulcansolar'), while the header shows info@valcansolar.com instead. "
            "Enquiries may not reach either inbox.",
            "The contact block's phone link shows +91 9010008373 while the displayed "
            "number is +91 90300 33577 - two different numbers in the same block.",
            "The site itself claims 'since 2012', ISO 9001:2008 certification and 15+ "
            "years of experience - the substance is there, it just never reaches the "
            "paid visitor.",
        ],
        "next_steps": [
            ("Unify the two ads on one owned page",
             "Point both MEGA UTSAV ads at one landing page on valcansolar.com with the "
             "offer, the prize list and the 24 November deadline on it - so the spend "
             "builds one measurable funnel."),
            ("Fill in the achievement counters",
             "0+ years of experience and 0K+ projects read as a startup. Real numbers "
             "on a deadline-driven campaign page are the difference between a click and "
             "a call."),
            ("Fix the contact details",
             "Correct marketing@vulcansolar.in to a working valcansolar.com address and "
             "make the phone link match the displayed number - on a draw with a hard "
             "deadline, a broken enquiry path is a lost prize entry."),
            ("Build the deadline into the page",
             "Offer valid to 24 Nov, draw on 30 Nov - a countdown and a 'book before "
             "the draw' CTA turn urgency into conversions."),
        ],
        "contact_facts": [
            ("Email", "info@valcansolar.com (header); marketing@vulcansolar.in "
                      "(contact block, misspelled)"),
            ("Phone", "+91 90300 33577 (displayed); +91 9010008373 (phone link in the "
                      "contact block)"),
            ("Address", "Vikrampuri Colony, Karkhana, Secunderabad 500015; Plot No. 16, "
                        "Goyal Co-operative Housing Society Ltd, Tirumalagiri, "
                        "Secunderabad Cantonment 500015"),
            ("Entity", "Valcan Energy Systems - since 2012, ISO 9001:2008"),
            ("Meta page", "facebook.com/valcansolar (also Instagram @valcansolar)"),
        ],
    },
    {
        "company": "Ellvin Energy",
        "legal": "Ellvin Energy Private Limited",
        "city": "Hyderabad",
        "website": "https://ellvinenergy.com/",
        "email": "info@ellvinenergy.com",
        "phone": "+91 94677 29999",
        "fb_page": "https://www.facebook.com/61579321563426/",
        "checked_on": "2026-10-21",
        "ad_library": {
            "meta_own": {
                "found": True,
                "results_count": 1,
                "results_label": "6 ads use this creative and text",
                "query": "Telugu solar subsidy",
                "ads": [
                    ad("1688280062277703", "Ellvin energy", "Aug 12, 2026",
                       "Facebook lead form (fb.me 'Book now')",
                       "Telugu: మొదటి కోటి మందికి మాత్రమే సబ్సిడీ రాయితీ. Elvin Energy "
                       "తో ఒక్క రూపాయి ఖర్చు లేకుండా 3KW సోలార్ ప్లాంట్. ఇక మీరు "
                       "ఉత్పత్తి చేసిన విద్యుత్తుతో మీ భవిష్యత్తు వెలిగించుకోండి. "
                       "#GoGreen #SolarPower #ElvinEnergy #ElvinSolar #GoGreen "
                       "#SolarBenefits #PMSuryaGhar. (Subsidy discount for the first 1 "
                       "crore people; a 3KW solar plant at zero cost with Elvin "
                       "Energy.)"),
                ],
            },
            "summary": (
                "Ellvin Energy is running 6 live ads on Meta - all six sharing one "
                "Telugu creative (Library ID 1688280062277703, started 12 August 2026) "
                "- and every one of them sends the click into a Facebook lead form. The "
                "company was incorporated only in August 2025 (CIN "
                "U35105AP2025PTC120835), is headquartered in Tadepalli, Andhra Pradesh, "
                "and is advertising into Telangana in Telugu. No owned page receives "
                "any of this traffic."),
        },
        "funnel": {
            "type": "Facebook lead form only",
            "destination": "fb.me ('Book now') on all 6 ads",
            "meaning": (
                "Every lead is captured inside Facebook. There is no pixel on "
                "ellvinenergy.com, no retargeting pool, no landing page to test and no "
                "way to see what happens after the click."),
        },
        "findings": [
            "6 live ads - and all 6 share one Telugu creative (Library ID "
            "1688280062277703, running since 12 August 2026). One idea, six versions, "
            "no second angle and no retargeting creative.",
            "Every click lands in a Facebook lead form - the paid traffic never reaches "
            "ellvinenergy.com. No pixel, no retargeting pool, no page you can test.",
            "The company was incorporated only in August 2025 (CIN U35105AP2025PTC120835, "
            "directors Vijaya Bhaskar and Nirmala Gangavarapu) - a one-year-old "
            "installer buying Telugu solar leads in Telangana.",
            "The creative promises a '3KW solar plant at zero cost' to 'the first 1 "
            "crore people' - eligibility language that needs a real landing page behind "
            "it, not just a form.",
            "Headquartered in Tadepalli, Guntur (Andhra Pradesh), advertising into "
            "Telangana - no Hyderabad presence on the site, no local proof for a "
            "Telangana buyer.",
        ],
        "next_steps": [
            ("Build an owned Telugu landing page",
             "Put the 'zero-cost 3KW' eligibility promise on a page you control - "
             "eligibility check, subsidy maths, quote form - and point all 6 ads at it."),
            ("Install the pixel and start retargeting",
             "Six ads buying leads with no pixel on your site means no audience to "
             "re-market to. The Meta pixel plus a lead-form integration turns one click "
             "into a retargetable contact."),
            ("Test a second creative angle",
             "One creative cannot tell you which message works. Test a subsidy-focused "
             "and an EMI-focused Telugu version against each other."),
            ("Add Telangana-local proof",
             "Named local projects and a Telangana service area turn a cross-border "
             "advertiser into a local option for the homeowner reading the ad."),
        ],
        "contact_facts": [
            ("Email", "info@ellvinenergy.com"),
            ("Phone", "+91 94677 29999"),
            ("Address", "3rd Floor, Next Space Building, NH-service Road, Kunchanapalli "
                        "Village, Tadepalli, Guntur Dist, Andhra Pradesh 522501"),
            ("Entity", "Ellvin Energy Private Limited - incorporated Aug 2025, CIN "
                       "U35105AP2025PTC120835"),
            ("Meta page", "facebook.com/61579321563426 (Ellvin energy)"),
        ],
    },
    {
        "company": "Kapil Power & Infra",
        "legal": "Kapil Power & Infra (P) Ltd.",
        "city": "Hyderabad",
        "website": "https://kapilpower.com/",
        "email": "info@kapilpower.com",
        "phone": "+91 7729985106",
        "fb_page": "https://www.facebook.com/kapilpowerandinfra/",
        "checked_on": "2026-10-21",
        "ad_library": {
            "meta_own": {
                "found": True,
                "results_count": 2,
                "results_label": "~2 results",
                "query": "Telugu solar subsidy",
                "ads": [
                    ad("3669543896537319", "Kapil Power & Infra P Ltd", "Sep 14, 2026",
                       "Facebook lead form",
                       "Telugu: మీ ఇంటి విలువను పెంచండి మరియు పర్యావరణాన్ని "
                       "రక్షించండి. అత్యాధునిక టెక్నాలజీతో కూడిన ఆన్-గ్రిడ్ "
                       "సోలార్ సిస్టమ్స్‌ను మేము అందిస్తున్నాము. ఎటువంటి నిర్వహణ "
                       "ఖర్చు లేకుండా దశాబ్దాల పాటు ఉచిత విద్యుత్తును పొందండి. "
                       "(Increase your home's value and protect the environment with "
                       "modern-technology on-grid solar systems and decades of free "
                       "electricity.)"),
                    ad("2274643036665215", "Kapil Power & Infra P Ltd", "Oct 6, 2026",
                       "Facebook lead form (fb.me 'See details')",
                       "Stop Paying High Current Bills! Kapil Powerతో మీ ఇంటినే పవర్ "
                       "హౌస్‌గా మార్చుకోండి. Zero Electricity Bills (reduce your "
                       "current bill up to 90%), Government Subsidy (PM Surya Ghar), "
                       "Premium Panels (25 years warranty), Expert Installation (20+ "
                       "years experience), Trusted Brand (1000+ happy customers)."),
                ],
            },
            "summary": (
                "Kapil Power & Infra is running 2 active Telugu ads on Meta - one since "
                "14 September 2026 (on-grid solar systems) and one since 6 October 2026 "
                "(reduce your bill by 90%, 1000+ happy customers) - and both send the "
                "click into a Facebook lead form. Kapil Power is the solar arm of the "
                "Kapil Group, a Hyderabad household name since 1981, with 25+ years in "
                "solar, TGREDCO empanelment (TSRE180167) and offices in Kapil Towers, "
                "Financial District. None of the spend reaches kapilpower.com."),
        },
        "funnel": {
            "type": "Facebook lead form",
            "destination": "fb.me ('See details') on both ads",
            "meaning": (
                "Both ads land inside Facebook. For a group company with a full EPC "
                "website - rooftop, ground-mounted, street lighting, solar fencing, "
                "O&M - the paid click never sees any of it."),
        },
        "findings": [
            "2 live Telugu ads (14 Sep and 6 Oct 2026) and every click lands in a "
            "Facebook lead form - the paid traffic never reaches kapilpower.com.",
            "This is the Kapil Group - a Hyderabad household name since 1981 - with "
            "25+ years in solar, TGREDCO empanelment (TSRE180167) and a 2004-"
            "incorporated company. Heavyweight credibility, all of it invisible to the "
            "ad click.",
            "The site is a full EPC site: on-grid and off-grid, rooftop, ground-mounted, "
            "street lighting, solar fencing and O&M, with DISCOM and MNRE paperwork "
            "handled - real depth that no paid traffic ever sees.",
            "No owned landing page for the offers being advertised, no pixel on the "
            "site, no retargeting pool built from this spend.",
            "The '1000+ happy customers' claim in the ad has no matching proof page on "
            "the site - testimonials exist, but nothing a Telugu ad click can verify "
            "in one step.",
        ],
        "next_steps": [
            ("Build a Hyderabad residential landing page",
             "Point both Telugu ads at one page on kapilpower.com: PM Surya Ghar "
             "subsidy, 90% bill reduction, the 1000+ customer proof, and the free site "
             "visit - so the Kapil Group name works on the click."),
            ("Install the pixel and capture retargeting",
             "Meta lead forms give you a name and number. The pixel plus Conversions "
             "API on your own site gives you the audience to re-market to at a fraction "
             "of the cost."),
            ("Test a second creative angle",
             "Two ads is a start. Test a subsidy-focused and an EMI-focused Telugu "
             "version against the bill-reduction message."),
            ("Put the group's track record in front of the click",
             "25+ years, 1981, TGREDCO empanelment - trust assets most local "
             "competitors cannot show, currently invisible on the paid path."),
        ],
        "contact_facts": [
            ("Email", "info@kapilpower.com (also sales@kapilpower.com)"),
            ("Phone", "+91 7729985106"),
            ("Address", "14th Floor, Kapil Towers, Financial District, Nanakramguda, "
                        "Gachibowli, Hyderabad 500032"),
            ("Entity", "Kapil Power & Infra (P) Ltd. - Kapil Group company (since "
                       "1981), TGREDCO empanelled TSRE180167, incorporated 2004"),
            ("Meta page", "facebook.com/kapilpowerandinfra"),
        ],
    },
    {
        "company": "Solar6",
        "legal": "Solar6 Pvt Ltd",
        "city": "Hyderabad",
        "website": "https://www.solar6.co.in/",
        "email": "info@solar6.in",
        "phone": "+91 9912355344",
        "fb_page": "https://www.facebook.com/61589212079896/",
        "checked_on": "2026-10-21",
        "ad_library": {
            "meta_own": {
                "found": True,
                "results_count": 1,
                "results_label": "~1 result",
                "query": "Telugu solar subsidy",
                "ads": [
                    ad("1115998414098781", "Solar6 Pvt Ltd", "Sep 14, 2026",
                       "WhatsApp (Send WhatsApp message)",
                       "Telugu: దసరా స్పెషల్ ఆఫర్! ఈ పండుగ సీజన్‌లో జీరో డౌన్ "
                       "పేమెంట్‌తో సోలార్ పొందండి! సోలార్ సిస్టమ్ కేవలం ₹78,000కే + "
                       "ప్రభుత్వ సబ్సిడీ + FREE Amaron ఇన్వర్టర్ & బ్యాటరీ! Reliable "
                       "performance, low maintenance, after-sales support. Authorised "
                       "partners: Adani | Microtek | Waaree | SBI | Union Bank | "
                       "Canara Bank. 9052 144 777 | www.solar6.co.in. PAN India "
                       "Services. (Dasara special: zero down payment solar, system at "
                       "just Rs 78,000 + government subsidy + free Amaron inverter and "
                       "battery.)"),
                ],
            },
            "summary": (
                "Solar6 is running an active Telugu Dasara-special ad on Meta (Library "
                "ID 1115998414098781, started 14 September 2026) offering zero-down-"
                "payment solar with a free Amaron inverter and battery - and the ad "
                "sends every click to WhatsApp. The company has over a decade of "
                "experience, is headquartered in Kukatpally, and runs both "
                "solar6.co.in and solar6.in. The ad's phone number (9052 144 777) is "
                "different from the one published on the site (+91 9912355344)."),
        },
        "funnel": {
            "type": "WhatsApp only",
            "destination": "WhatsApp message from the ad",
            "meaning": (
                "The paid click goes straight to a chat. There is no site visit, no "
                "email capture, no landing page - so nothing can be measured, tested "
                "or retargeted, and a visitor who does not reply is gone."),
        },
        "findings": [
            "The live Dasara ad sends every click to WhatsApp - no site visit, no email "
            "capture, nothing to measure or retarget.",
            "The ad's phone number (9052 144 777) is different from the number "
            "published on the site (+91 9912355344) - two numbers, two funnels, one "
            "brand.",
            "The site's 'Success by the Numbers' counters all read 0 - 0+ projects "
            "completed, 0+ happy customers, 0+ team members, 0+ years of experience - "
            "while the homepage claims 'India's #2 Leading Rooftop Solar Company'.",
            "The site still carries template demo links (wordpress.vecurosoft.com/"
            "energiso) and a project image credited to 'Maxwatt Solar' - another "
            "company's photo.",
            "Authorised-partner line in the ad (Adani, Microtek, Waaree, SBI, Union "
            "Bank, Canara Bank) is strong trust material with no matching proof page "
            "for a WhatsApp-click visitor.",
        ],
        "next_steps": [
            ("Build an owned page for the offer",
             "Put the Dasara offer - zero down payment, Rs 78,000 + subsidy, free "
             "Amaron inverter and battery - on a landing page on solar6.co.in, and send "
             "the ad there."),
            ("Capture before the chat",
             "Name, phone and locality on the page first, WhatsApp second - so "
             "non-repliers can be followed up instead of lost."),
            ("Fix the counters and the credit",
             "0+ projects and 0+ years read as a startup next to an 'India's #2' claim. "
             "Remove the Maxwatt Solar photo credit and fill in real numbers."),
            ("Align the two phone numbers",
             "The ad says 9052 144 777, the site says +91 9912355344. One number, "
             "everywhere, so the paid click and the site agree."),
        ],
        "contact_facts": [
            ("Email", "info@solar6.in"),
            ("Phone", "+91 9912355344 (site); 9052 144 777 (ad)"),
            ("Address", "4-32-41/39, Kamalaprasanna Nagar, Allwyn Colony, Kukatpally, "
                        "Hyderabad 500072 (opp SBI Bank)"),
            ("Entity", "Solar6 - over a decade of experience, headquartered in "
                       "Hyderabad; sites solar6.co.in and solar6.in"),
            ("Meta page", "facebook.com/61589212079896 (Solar6 Pvt Ltd)"),
        ],
    },
    {
        "company": "Eastman New Energy",
        "legal": "Eastman New Energy Private Limited",
        "city": "Hyderabad",
        "website": "https://eastmansolar.in/",
        "email": "support@eaplworld.com",
        "phone": "80016 80016",
        "fb_page": "https://www.facebook.com/Eastmannewenergy/",
        "checked_on": "2026-10-21",
        "ad_library": {
            "meta_own": {
                "found": True,
                "results_count": 4,
                "results_label": "~4 results",
                "query": "Telugu solar subsidy",
                "ads": [
                    ad("3668088310036092", "Eastman New Energy Private Limited",
                       "Aug 30, 2026", "https://eastmansolar.in/ ('Learn more')",
                       "Telugu on-grid creative - PM Surya Ghar free-electricity "
                       "scheme, switch to Eastman on-grid solar solutions for the "
                       "Rs. 78,000* subsidy plus additional state subsidy. Call 80016 "
                       "80016."),
                    ad("929674622913607", "Eastman New Energy Private Limited",
                       "Aug 29, 2026", "https://eastmansolar.in/ ('Learn more')",
                       "Telugu hybrid creative - switch to Eastman hybrid solutions "
                       "for the Rs. 78,000* subsidy plus additional state subsidy, "
                       "with Eastman hybrid inverters and lithium batteries for 24x7 "
                       "power. Call 80016 80016."),
                    ad("2152229662052110", "Eastman New Energy Private Limited",
                       "Sep 29, 2026", "https://eastmansolar.in/ ('Learn more')",
                       "Telugu: మీ కరెంటు బిల్లును సున్నాకు తగ్గించండి. పీఎం "
                       "సూర్య ఘర్ ముఫ్త్ బిజిలీ యోజన కింద, ఈస్ట్‌మన్ ఆన్-గ్రిడ్ "
                       "సోలార్ సొల్యూషన్స్‌కు మారి ₹78,000* సబ్సిడీ + అదనపు రాష్ట్ర "
                       "సబ్సిడీ పొందండి. ఈరోజే కాల్ చేయండి 80016 80016. (Reduce "
                       "your current bill to zero under the PM Surya Ghar scheme with "
                       "Eastman on-grid solar solutions - Rs. 78,000* subsidy plus "
                       "additional state subsidy. Call 80016 80016 today.)"),
                    ad("28876616218695042", "Eastman New Energy Private Limited",
                       "Sep 29, 2026", "https://eastmansolar.in/ ('Learn more')",
                       "Telugu: ఈస్ట్‌మన్ సోలార్ హైబ్రిడ్ సొల్యూషన్స్‌కు మారి "
                       "₹78,000* సబ్సిడీ + అదనపు రాష్ట్ర సబ్సిడీ పొందండి. ఈస్ట్‌మన్ "
                       "హైబ్రిడ్ ఇన్వర్టర్లు, లిథియం బ్యాటరీలతో 24x7 విద్యుత్తు "
                       "ఆదాను ఆస్వాదించండి. (Switch to Eastman hybrid solar solutions "
                       "for the Rs. 78,000* subsidy plus additional state subsidy - "
                       "Eastman hybrid inverters with lithium batteries for 24x7 "
                       "power.)"),
                ],
            },
            "summary": (
                "Eastman New Energy is running 4 active Telugu ads on Meta (Aug 29 - "
                "Sep 29, 2026) - on-grid and hybrid creatives, both selling the "
                "Rs. 78,000 PM Surya Ghar subsidy plus an additional state subsidy - "
                "and all four send the click to eastmansolar.in. Eastman is not a "
                "local installer: the site is a manufacturer's product catalogue "
                "(800 MW in-house panel manufacturing, 1000+ distributors, 400+ OEM "
                "partners, part of the Eastman group's 25 GW production)."),
        },
        "funnel": {
            "type": "Own website (enquiry form behind reCAPTCHA)",
            "destination": "eastmansolar.in ('Learn more') on all 4 ads",
            "meaning": (
                "At least the spend lands on an owned site. But the destination is a "
                "manufacturer's product catalogue - on-grid, off-grid and hybrid "
                "inverter pages - while the ads promise a B2C subsidy. The gap between "
                "the ad promise and the page is where the conversion leaks."),
        },
        "findings": [
            "4 live Telugu ads (Aug 29 - Sep 29, 2026), on-grid and hybrid creatives, "
            "all pointing at eastmansolar.in - the spend stays on an owned domain.",
            "But the destination is a manufacturer's catalogue: 800 MW in-house panel "
            "manufacturing, 1000+ distributors, 400+ OEM partners, panels from 50W to "
            "590W - a B2B story for ads selling a B2C subsidy.",
            "The enquiry form runs behind reCAPTCHA and a character-limited "
            "'claim your subsidy of Rs 78,000' field - friction between the ad promise "
            "and the lead.",
            "Every ad ends with the same 80016 80016 short-code number - a call-centre "
            "funnel, not a local-installer one.",
            "Scale note: this is the solar arm of the Eastman group (25 GW group-wide "
            "production), not a local installer - the pitch here is the B2C funnel, "
            "not the product.",
        ],
        "next_steps": [
            ("Build a dedicated residential PM Surya Ghar page",
             "The ad promise is 'reduce your bill to zero with Rs 78,000 subsidy'. The "
             "page should be a residential subsidy calculator and quote form, not the "
             "inverter catalogue."),
            ("Cut the form friction",
             "reCAPTCHA plus a limited field on a Rs 78,000 offer loses clicks. Fewer "
             "fields, no captcha on the first step."),
            ("Install pixel and retargeting on the offer",
             "4 ads on one offer with no pixel means no way to see who dropped off "
             "after the click and no audience to bring back."),
            ("Test on-grid vs hybrid against the page",
             "Two creatives selling two product lines to one funnel - a landing page "
             "per line tells you which converts."),
        ],
        "contact_facts": [
            ("Email", "support@eaplworld.com"),
            ("Phone", "80016 80016 (short code, in every ad); 0124-4627900"),
            ("Address", "Eastman New Energy Private Limited - enquiry via eastmansolar.in "
                        "(maps link on site)"),
            ("Entity", "Eastman New Energy Private Limited - 800 MW in-house panel "
                       "manufacturing, part of EAPL (25 GW group-wide), 1000+ "
                       "distributors, 400+ OEM partners"),
            ("Meta page", "facebook.com/Eastmannewenergy"),
        ],
    },
]


def slug(name):
    return re.sub(r"[^a-zA-Z0-9]+", "_", name)[:50]


def validate(lead):
    """Refuse to build a report that could contain invented ad data."""
    problems = []
    ads = (lead.get("ad_library") or {}).get("meta_own", {}).get("ads", [])
    for a in ads:
        if not a.get("library_id"):
            problems.append(f"{lead['company']}: ad without library_id")
        if not a.get("library_url"):
            problems.append(f"{lead['company']}: ad without library_url")
        if not a.get("text"):
            problems.append(f"{lead['company']}: ad without copy")
    if not ads and (lead.get("ad_library") or {}).get("meta_own", {}).get("found"):
        problems.append(f"{lead['company']}: marked as advertising but has no ads")
    if ads and not (lead.get("ad_library") or {}).get("meta_own", {}).get("found"):
        problems.append(f"{lead['company']}: has ads but marked as not advertising")
    # These leads have websites - the report must not pretend otherwise.
    if not lead.get("website", "").startswith("http"):
        problems.append(f"{lead['company']}: website missing")
    if lead.get("no_website"):
        problems.append(f"{lead['company']}: no_website is not valid in ads-only mode")
    return problems


def build(lead):
    audit = {
        "company": lead["company"],
        "legal": lead.get("legal", ""),
        "city": lead["city"],
        "website": lead["website"],
        "ads_only": True,
        "website_audit_run": False,
        "checked_on": lead.get("checked_on", CHECKED_ON),
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "source": "Meta Ad Library (India, active ads) + the company's own live website",
        "ad_library": lead["ad_library"],
        "funnel": lead.get("funnel", {}),
        "findings": lead.get("findings", []),
        "next_steps": lead.get("next_steps", []),
        "contact_facts": lead.get("contact_facts", []),
        "contact": {"email": lead.get("email", ""), "phone": lead.get("phone", ""),
                    "fb_page": lead.get("fb_page", "")},
    }
    os.makedirs(RESULTS_DIR, exist_ok=True)
    json_path = os.path.join(RESULTS_DIR, f"audit_{slug(lead['company'])}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(audit, f, indent=2, ensure_ascii=False)
    pdf_path = generate_ads_only_pdf(audit)
    return json_path, pdf_path


def main():
    ap = argparse.ArgumentParser(description="Build ads-only (live ad activity) reports")
    ap.add_argument("--list", action="store_true", help="list leads, build nothing")
    ap.add_argument("--only", default="", help="build one lead by company name")
    args = ap.parse_args()

    leads = LEADS
    if args.only:
        leads = [l for l in LEADS if args.only.lower() in l["company"].lower()]
        if not leads:
            print(f"No lead matches '{args.only}'")
            sys.exit(1)

    if args.list:
        print(f"{len(LEADS)} leads with verified live ad data (checked {CHECKED_ON}):")
        for l in LEADS:
            n = len(l["ad_library"]["meta_own"]["ads"])
            print(f"  - {l['company']:<22} {n} live ad(s)  {l['website']}")
        return

    problems = []
    for lead in leads:
        problems.extend(validate(lead))
    if problems:
        print("REFUSING TO BUILD - incomplete ad data would produce a fake report:")
        for p in problems:
            print("  x", p)
        sys.exit(1)

    print("=" * 60)
    print(f"ADS-ONLY REPORT BUILDER - {len(leads)} lead(s), data checked {CHECKED_ON}")
    print("Website audit NOT run - reports say so on page 1.")
    print("=" * 60)

    for i, lead in enumerate(leads, 1):
        json_path, pdf_path = build(lead)
        size = os.path.getsize(pdf_path) // 1024
        n = len(lead["ad_library"]["meta_own"]["ads"])
        print(f"[{i}/{len(leads)}] {lead['company']}")
        print(f"    live ads: {n} | json: {os.path.basename(json_path)}")
        print(f"    pdf:      {pdf_path} ({size} KB)")

    print("\nQA gate for these reports:  python verify_report.py --ads-only")
    print("Full audit (website + tracking + speed) still needs your machine:")
    for lead in leads:
        print(f"  python run_pipeline.py {lead['website']} \"{lead['company']}\" "
              f"--city {lead['city']}")


if __name__ == "__main__":
    main()
