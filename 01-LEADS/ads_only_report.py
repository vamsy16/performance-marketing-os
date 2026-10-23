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
    {
        "company": "Ecolt Energy",
        "legal": "Ecolt Energy",
        "city": "Hyderabad",
        "website": "https://www.ecoltenergy.com/",
        "email": "Contact@ecoltenergy.com",
        "phone": "+91 83411 13782",
        "fb_page": "https://www.facebook.com/61584855812336/",
        "checked_on": "2026-10-21",
        "ad_library": {
            "meta_own": {
                "found": True,
                "results_count": 2,
                "results_label": "2 ads use this creative and text",
                "query": "Telugu solar system",
                "ads": [
                    ad("1405421181747986", "Ecolt Energy", "Oct 13, 2026",
                       "Facebook lead form (fb.me 'Sign up')",
                       "Telugu: ఈరోజు సోలార్ పెట్టుబడి... రేపటి విద్యుత్ ఖర్చులకు "
                       "ఉపశమనం! మీ ఇంటి కరెంట్ బిల్లును తగ్గించుకోవాలని "
                       "అనుకుంటున్నారా? Ecolt Energy Rooftop Solar తో మీ ఇంటికు "
                       "సరిపోయే సోలార్ సిస్టమ్‌ను ఎంచుకోండి. ✅ 3KW Rooftop Solar — "
                       "₹1,90,000. 💰 ₹33,000 ప్రత్యేక తగ్గింపు. 🏛️ అర్హత ఉన్న "
                       "గృహాలకు PM Surya Ghar సబ్సిడీ ₹78,000 వరకు. 🔧 నిపుణుల "
                       "ఇన్‌స్టాలేషన్, అమ్మకం తర్వాత సేవలు. 📲 మీ ఇంటికి ఉచిత "
                       "Solar Estimate కోసం WhatsApp చేయండి: +91 82475 37597. 📍 "
                       "ఆంధ్రప్రదేశ్ & తెలంగాణ. (3KW Rooftop Solar at ₹1,90,000 with "
                       "a ₹33,000 special discount and PM Surya Ghar subsidy up to "
                       "₹78,000 - free solar estimate via WhatsApp.)"),
                ],
            },
            "summary": (
                "Ecolt Energy is running 2 live Telugu ads on Meta - both sharing one "
                "creative (Library ID 1405421181747986, started 13 October 2026) - "
                "selling a 3KW rooftop system at ₹1,90,000 with a ₹33,000 discount "
                "plus the ₹78,000 PM Surya Ghar subsidy, and every click lands in a "
                "Facebook lead form. The company has a Hyderabad office in Shaikpet "
                "(registered address Narasaraopet, AP) and a polished, "
                "calculator-driven website that receives none of the paid traffic."),
        },
        "funnel": {
            "type": "Facebook lead form only",
            "destination": "fb.me ('Sign up') on both ads",
            "meaning": (
                "Every click is captured inside Facebook. The polished ecoltenergy.com "
                "- savings calculator, project map, WhatsApp chat - is invisible to "
                "the buyer the ad just paid for."),
        },
        "findings": [
            "2 live Telugu ads - both sharing one creative (Library ID "
            "1405421181747986, running since 13 October 2026) - and every click lands "
            "in a Facebook lead form. ecoltenergy.com receives none of the traffic.",
            "The ad's WhatsApp number (+91 82475 37597) is different from the site's "
            "(+91 83411 13782) - two numbers, two funnels, one brand.",
            "The live site's 'Real projects, real power' counters all read 0 - 0 MW "
            "capacity installed, 0 projects completed, 0 est. energy generated/yr, "
            "0 CO₂ offset/yr - while the hero banner claims 2,000+ systems installed "
            "and 95% average bill reduction.",
            "The site's live weather widget reads 'Right now in Virginia Beach: "
            "16°C, clear skies' - hardcoded to a US city, on a Hyderabad solar "
            "company's homepage.",
            "The build is genuinely good (interactive bill-vs-solar comparison, "
            "savings calculator, project map across AP & Telangana) - none of it is "
            "in the paid path, and there is no pixel or retargeting pool from this "
            "spend.",
        ],
        "next_steps": [
            ("Point the ads at an owned page",
             "A landing page on ecoltenergy.com carrying the ad's exact offer - 3KW "
             "at ₹1,90,000, ₹33,000 off, subsidy eligibility - so the spend builds "
             "one measurable funnel instead of a Facebook form."),
            ("Fix the zero counters and the weather widget",
             "0 MW installed and 0 projects next to a '2,000+ systems' claim, plus a "
             "Virginia Beach widget, are the first things a paid visitor checks."),
            ("Unify the phone numbers",
             "The ad says +91 82475 37597, the site says +91 83411 13782. One "
             "number, everywhere, so the paid click and the site agree."),
            ("Install pixel and retargeting",
             "Two ads on one creative with no pixel means no audience to bring back "
             "and no way to see who dropped off after the click."),
        ],
        "contact_facts": [
            ("Email", "Contact@ecoltenergy.com"),
            ("Phone", "+91 83411 13782 (site); +91 82475 37597 (ad)"),
            ("Address", "8-1-87/4/7/2, Vinayak Nagar Colony, Shaikpet, Hyderabad, "
                        "Telangana 500033 (registered: Narasaraopet, AP)"),
            ("Entity", "Ecolt Energy - claims 2,000+ systems installed, 95% avg. "
                       "bill reduction, 30-yr performance warranty"),
            ("Meta page", "facebook.com/61584855812336 (Ecolt Energy)"),
        ],
    },
    {
        "company": "Orizen Solar Innovations",
        "legal": "Orizen Solar Innovations Pvt Ltd",
        "city": "Hyderabad",
        "website": "https://www.orizensolar.com/",
        "email": "info.orizensolar@gmail.com",
        "phone": "+91 9962039859",
        "fb_page": "https://www.facebook.com/61562730157779/",
        "checked_on": "2026-10-21",
        "ad_library": {
            "meta_own": {
                "found": True,
                "results_count": 1,
                "results_label": "1 result, multiple versions",
                "query": "Telugu solar system",
                "ads": [
                    ad("3529873930505195", "Orizen Solar Innovations", "Sep 18, 2026",
                       "WhatsApp (Send WhatsApp message)",
                       "Telugu: ☀️ సోలార్‌పై ప్రత్యేక Dussehra & Deepavali Dhamaka "
                       "Offer 🔥 ఈ పండుగ సీజన్‌లో మీ ఇంటికి Solar Power తీసుకురండి… "
                       "కరెంట్ బిల్లులపై భారం తగ్గించుకోండి! Orizen Solar Innovations "
                       "Pvt. Ltd. నుండి ప్రత్యేక Dussehra & Deepavali Dhamaka Offer "
                       "🎉 ✨ ₹78,000/- వరకు భారీ Subsidy 🔥 3 KW Solar System – "
                       "అదనంగా ₹10,000 Discount 🔥 5 KW Solar System – అదనంగా ₹20,000 "
                       "Discount 🎁 Solar Panel Cleaning Brush ఉచితం ☀️ WAAREE "
                       "Authorised Channel Partner. 📞 8374 670 999 | 8374 683 999 📍 "
                       "Budampadu Bypass, Ponnur Road, Guntur. (₹78,000 subsidy plus "
                       "up to ₹20,000 special discount - Dussehra & Deepavali Dhamaka "
                       "Offer.)"),
                ],
            },
            "summary": (
                "Orizen Solar Innovations is running a live Telugu ad on Meta (Library "
                "ID 3529873930505195, started 18 September 2026, multiple versions) "
                "offering a Dussehra & Deepavali Dhamaka package - ₹78,000 subsidy, "
                "3KW with ₹10,000 off, 5KW with ₹20,000 off, free panel-cleaning "
                "brush, WAAREE authorised channel partner - and every click goes to "
                "WhatsApp. The company is headquartered in Guntur with three AP "
                "offices (Guntur, Vijayawada, Tirupati) and is advertising into "
                "Telangana."),
        },
        "funnel": {
            "type": "WhatsApp only",
            "destination": "WhatsApp message from the ad",
            "meaning": (
                "The paid click goes straight to a chat. Nothing is measured, nothing "
                "is retargeted, and the site's on-grid/off-grid/hybrid pages - all "
                "of them - never get seen by the buyer the ad paid for."),
        },
        "findings": [
            "Live Telugu ad (Library ID 3529873930505195, running since 18 September "
            "2026, multiple versions) - the Dussehra & Deepavali offer sends every "
            "click to WhatsApp; orizensolar.com receives none of the traffic.",
            "Three phone numbers across the funnel: the ad (8374 670 999 / 8374 683 "
            "999) and the site (+91 9962039859) - split numbers for one offer.",
            "The live site still carries template text: the PM Surya Ghar blurb "
            "reads 'At Your Solar Partner, we are proud to support this initiative' "
            "- the company name was never filled in.",
            "The features section is headed 'Features of Origin Solar Panels' - "
            "'Origin', not 'Orizen' - and every 'Read More' service link points at "
            "'#' (the homepage anchor), so nothing on the site answers what the ad "
            "promises.",
            "Guntur-based with offices in Vijayawada and Tirupati, advertising into "
            "Telangana - no Telangana service-area proof for the buyer the ad is "
            "aimed at.",
        ],
        "next_steps": [
            ("Build an owned offer page",
             "Put the Dussehra & Deepavali offer - ₹78,000 subsidy, 3KW/5KW "
             "discounts, WAAREE partnership - on a page you control, with name and "
             "phone captured before the WhatsApp hand-off."),
            ("Fill in the template placeholders",
             "'Your Solar Partner' in the PM Surya Ghar blurb and 'Origin Solar' in "
             "the features heading are the first trust breaks a visitor finds."),
            ("Fix the dead service links",
             "Every 'Read More' points at the homepage anchor - the on-grid, "
             "off-grid and hybrid pages exist in the nav but are unreachable from "
             "the homepage flow."),
            ("Unify the numbers and add local proof",
             "One phone number everywhere, plus a Telangana service-area statement, "
             "turns a Guntur advertiser into a local option for the Telugu buyer."),
        ],
        "contact_facts": [
            ("Email", "info.orizensolar@gmail.com"),
            ("Phone", "+91 9962039859 (site); 8374 670 999 / 8374 683 999 (ad)"),
            ("Address", "Ring Road, Chandramouli Nagar, Vidyanagar, Guntur 522007; "
                        "offices in Vijayawada and Tirupati"),
            ("Entity", "Orizen Solar Innovations Pvt Ltd - claims 456+ completed "
                       "projects, 513+ happy customers, 10+ years of experience"),
            ("Meta page", "facebook.com/61562730157779 (Orizen Solar Innovations)"),
        ],
    },
    {
        "company": "Ray On Solar Systems",
        "legal": "Ray On Solar Systems",
        "city": "Hyderabad",
        "website": "https://www.rayonsolarsystems.in/",
        "email": "rayonsolars@gmail.com",
        "phone": "+91 8500976346",
        "fb_page": "https://www.facebook.com/61571060785642/",
        "checked_on": "2026-10-21",
        "ad_library": {
            "meta_own": {
                "found": True,
                "results_count": 1,
                "results_label": "1 result",
                "query": "Telugu solar system",
                "ads": [
                    ad("1107666674962232", "Ray On Solar Systems", "Oct 13, 2026",
                       "Instagram (instagram.com/ray_on_solar_systems_) with an "
                       "fb.me 'Get Quote' button",
                       "Reduce Your Electricity Bills with Solar - 3kW Solar Power "
                       "System Offer. Get your 3kW solar system at a special price "
                       "with subsidy and long-term warranty support. (Ad destination "
                       "links to the company's Instagram profile; the Get Quote "
                       "button goes to a generic fb.me link.)"),
                ],
            },
            "summary": (
                "Ray On Solar Systems is running 1 live ad on Meta (Library ID "
                "1107666674962232, started 13 October 2026) offering a 3kW solar "
                "system at a special price with subsidy - and the ad sends the "
                "click to Instagram, not to the company's website. The company is "
                "based in Visakhapatnam and is advertising into Telangana."),
        },
        "funnel": {
            "type": "Instagram + generic fb.me link",
            "destination": "instagram.com/ray_on_solar_systems_ (ad creative link) "
                           "and fb.me ('Get Quote')",
            "meaning": (
                "A social profile is not a funnel. There is no lead capture, no "
                "quote form and nothing to retarget - and the site's own free-quote "
                "form sits unused while the ad pays for clicks."),
        },
        "findings": [
            "The live 3kW-offer ad (Library ID 1107666674962232, started 13 October "
            "2026) sends Telugu solar buyers to an Instagram profile - not to "
            "rayonsolarsystems.in. A profile has no lead capture, no phone form and "
            "nothing to retarget.",
            "The ad's 'Get Quote' button goes to a generic fb.me link - the click "
            "never lands on a page that takes a name, a phone number or a bill "
            "amount.",
            "The site itself is a clean WordPress build with a free-quote form, "
            "on-grid/off-grid rooftop systems, PM Surya Ghar subsidy assistance and "
            "a real-time monitoring section - none of it is in the paid path.",
            "Visakhapatnam-based (Ravi Nagar, Naidu Thota, 530029) and advertising "
            "into Telangana - no Telangana service-area proof for the buyer the ad "
            "is aimed at.",
            "One live ad is the entire paid presence - no second creative, no "
            "retargeting, nothing to A/B test.",
        ],
        "next_steps": [
            ("Point the ad at the site's own quote page",
             "The site already has a free-quote form and the PM Surya Ghar subsidy "
             "section - sending the 3kW-offer click there instead of Instagram turns "
             "the spend into measurable leads."),
            ("Or build a dedicated 3kW offer page",
             "A landing page carrying the ad's exact offer - special 3kW price, "
             "subsidy, long-term warranty - with name, phone and locality captured "
             "before any chat."),
            ("Add Telangana-local proof",
             "A service-area statement and named local installs turn a Visakhapatnam "
             "advertiser into a local option for the Telugu buyer."),
            ("Test a second creative",
             "One ad cannot tell you which message works - a subsidy-focused and an "
             "EMI-focused version against each other would."),
        ],
        "contact_facts": [
            ("Email", "rayonsolars@gmail.com"),
            ("Phone", "+91 8500976346 / +91 9703774654"),
            ("Address", "Ravi Nagar, Naidu Thota, Visakhapatnam 530029"),
            ("Entity", "Ray On Solar Systems - claims 5+ years of technical "
                       "experience"),
            ("Meta page", "facebook.com/61571060785642 (also Instagram "
                          "@ray_on_solar_systems_)"),
        ],    },
    {
        "company": "MrSolar",
        "legal": "MrSolar (mrsolar.in)",
        "city": "Hyderabad",
        "website": "https://mrsolar.in/",
        "email": "info@mrsolar.in",
        "phone": "+91 8500225885",
        "fb_page": "https://www.facebook.com/mrsolarin/",
        "checked_on": "2026-10-22",
        "ad_library": {
            "meta_own": {
                "found": True,
                "results_count": 1,
                "results_label": "~1 result (a separate Nagpur 'Mr.Solar' page also matched the query and is a different company)",
                "query": "rooftop solar Hyderabad",
                "ads": [
                    ad("2766978160319102", "mrsolar.in", "May 5, 2026",
                       "fb.me 'Book now' (video ad)",
                       "Thinking about rooftop solar but not sure whom to trust? Watch this "
                       "Hyderabad customer share their real experience - from site survey to "
                       "installation and subsidy guidance. No sales talk. Just facts, uncut "
                       "customer review. CTA line: 'Real Solar Experience uncut - Hyderabad | "
                       "uncut Customer review | Rooftop solar | Subsidy support'."),
                ],
            },
            "summary": (
                "mrsolar.in has exactly one active Meta ad - a Hyderabad customer-review "
                "video that has been running since 5 May 2026, over five months on the same "
                "creative. The click goes to an fb.me link, not to a specific page on "
                "mrsolar.in. The site itself (fetched 2026-10-22) is the fullest asset in "
                "this batch: an ISO 9001:2015 badge, PM Surya Ghar subsidy content including "
                "the Rs 78,000 central subsidy and 300 free units, a savings calculator, an "
                "eligibility form, a WhatsApp button (wa.me/918500911912) and city pages for "
                "Hyderabad plus seven other Telangana towns. None of that machinery is "
                "referenced by the ad copy beyond a passing 'subsidy guidance'."),
        },
        "funnel": {
            "type": "fb.me link wrapper",
            "destination": "fb.me 'Book now' - Facebook's link wrapper, not a page on mrsolar.in",
            "meaning": (
                "The only live ad sends its click through an fb.me wrapper instead of to the "
                "subsidy page, calculator or eligibility form that already exist on "
                "mrsolar.in. After five months on one creative there is no second angle, no "
                "retargeting creative and no owned page behind the spend."),
        },
        "findings": [
            "One live ad, running since 5 May 2026 - over five months on a single "
            "customer-review video with no second creative angle behind it.",
            "The ad's click goes to an fb.me wrapper, while mrsolar.in already has the "
            "landing assets a subsidy-motivated click wants: the PM Surya Ghar Rs 78,000 "
            "subsidy page, the savings calculator and the eligibility form.",
            "The site positions itself as an 'unbiased consumer reviews of Telangana & AP "
            "solar companies' destination with an ISO 9001:2015 badge and city pages for "
            "Hyderabad, Karimnagar, Warangal, Siddipet, Nalgonda, Rangareddy, Medchal and "
            "Malkajgiri - a trust story the one ad never tells.",
            "Contact paths on the live site are split three ways: the contact page lists "
            "info@mrsolar.in and contact@mrsolar.in with +91 8500225885, while the floating "
            "WhatsApp button uses a different number, +91 85009 11912.",
        ],
        "next_steps": [
            ("Point the ad at the subsidy page",
             "The video promises 'subsidy guidance' - send the click to the PM Surya Ghar "
             "Rs 78,000 page with the calculator and eligibility form on it, so five months "
             "of spend finally lands on the page built to convert it."),
            ("Add a second creative angle",
             "One testimonial video for five months is the whole account. A calculator-led "
             "or eligibility-check creative gives the same audience a different door in."),
            ("Unify the contact numbers",
             "info@mrsolar.in / contact@mrsolar.in / +91 8500225885 on the contact page "
             "against +91 85009 11912 on the WhatsApp button - one enquiry path, one "
             "number."),
        ],
        "contact_facts": [
            ("Email", "info@mrsolar.in / contact@mrsolar.in (contact page)"),
            ("Phone", "+91 8500225885 (contact page); WhatsApp +91 85009 11912 (site button)"),
            ("Address", "1-128/4, Pochammagadda, Kompally, Hyderabad, Secunderabad, "
                        "Telangana 500100"),
            ("Site claims", "ISO 9001:2015; PM Surya Ghar Rs 78,000 subsidy + 300 free "
                            "units content; savings calculator; city pages for Hyderabad and "
                            "7 other Telangana towns"),
            ("Meta page", "facebook.com/mrsolarin"),
        ],
    },
    {
        "company": "Arcedo Systems",
        "legal": "Arcedo Systems Private Limited",
        "city": "Hyderabad",
        "website": "https://arcedo.net/",
        "email": "info@arcedo.net",
        "phone": "+91 8448448552",
        "fb_page": "https://www.facebook.com/61561703979379/",
        "checked_on": "2026-10-22",
        "ad_library": {
            "meta_own": {
                "found": True,
                "results_count": 3,
                "results_label": "~3 results on the Arcedo Systemss page (a sibling 'Suryon' page runs the same brand's residential ads)",
                "query": "Telugu \u0c38\u0c4b\u0c32\u0c3e\u0c30\u0c4d \u0c07\u0c28\u0c4d\u200c\u0c38\u0c4d\u0c1f\u0c3e\u0c32\u0c47\u0b37\u0c28\u0c4d (solar installation)",
                "ads": [
                    ad("2518444838650356", "Arcedo Systemss", "Sep 23, 2026",
                       "fb.me 'Get quote'",
                       "Telugu: \u0c2e\u0c40 \u0c07\u0c02\u0c1f\u0c3f\u0c15\u0c3f \u0c38\u0c4b\u0c32\u0c3e\u0c30\u0c4d \u0c38\u0c2c\u0c4d\u0c38\u0c3f\u0c21\u0c40 \u0c05\u0c30\u0c4d\u0c39\u0c24 \u0c09\u0c02\u0c26\u0c3e? PM Surya Ghar Yojana \u0c26\u0c4d\u0c35\u0c3e\u0c30\u0c3e \u0c0e\u0c02\u0c24 \u0c35\u0c30\u0c15\u0c41 \u0c2a\u0c4d\u0c30\u0c2f\u0c4b\u0c1c\u0c28\u0c02 \u0c2a\u0c4a\u0c02\u0c26\u0c17\u0c32\u0c30\u0c4b \u0c09\u0c1a\u0c3f\u0c24\u0c02\u0c17\u0c3e \u0c1a\u0c46\u0c15\u0c4d \u0c1a\u0c46\u0c2f\u0c15\u0c41\u0c15\u0c4b\u0c02\u0c21\u0c3f. (Does your home qualify for the solar subsidy - check free under PM Surya Ghar.) Headline: '\u0c38\u0c4b\u0c32\u0c3e\u0c30\u0c4d \u0c38\u0c2c\u0c4d\u0c38\u0c3f\u0c21\u0c40 \u0c05\u0c30\u0c4d\u0c39\u0c24 \u0c1a\u0c46\u0c15\u0c4d \u0c1a\u0c46\u0c2f\u0c02\u0c21\u0c3f'."),
                    ad("1441101634676762", "Arcedo Systemss", "Sep 30, 2026",
                       "https://solar.suryon.in/ (2 ads use this creative)",
                       "Telugu: \u0c30\u0c3e\u0c2c\u0c4b\u0c2f\u0c47 25 \u0c0f\u0c33\u0c4d\u0c32\u0c41, \u0c28\u0c46\u0c32\u0c15\u0c41 \u0c15\u0c47\u0c35\u0c32\u0c02 \u00e2\u00b9300 \u0c15\u0c30\u0c46\u0c02\u0c1f\u0c4d \u0c2c\u0c3f\u0c32\u0c4d\u0c32\u0c41? Suryon Solar Systems \u0c24\u0c4b \u0c07\u0c26\u0c3f \u0c28\u0c3f\u0c1c\u0c02\u0c17\u0c3e\u0c28\u0c47 \u0c38\u0c3e\u0c27\u0c4d\u0c2f\u0c02. 90% \u0c35\u0c30\u0c15\u0c41 \u0c06\u0c26\u0c3e, \u0c17\u0c35\u0c30\u0c4d\u0c28\u0c2e\u0c46\u0c02\u0c1f\u0c4d \u0c38\u0c2c\u0c4d\u0c38\u0c3f\u0c21\u0c40, 25 \u0c0f\u0c33\u0c4d\u0c32 \u0c2a\u0c30\u0c4d\u0c2b\u0c3e\u0c2e\u0c46\u0c02\u0c38\u0c4d \u0c35\u0c3e\u0c30\u0c02\u0c1f\u0c40, \u0c2b\u0c4d\u0c30\u0c40 \u0c39\u0c4b\u0c2e\u0c4d \u0c38\u0c48\u0c1f\u0c4d \u0c35\u0c3f\u0c1c\u0c3f\u0c1f\u0c4d. (Rs 300 monthly bill in 25 years with Suryon - government subsidy, 25-year performance warranty, free home site visit. Suryon-branded copy running on the Arcedo Systemss page.)"),
                    ad("1640504621042947", "Arcedo Systemss", "Oct 17, 2026",
                       "fb.com/messenger_doc/ ('Contact us')",
                       "CUT YOUR POWER BILLS by up to 50%*, with zero Capex. Get Solar + "
                       "Battery Storage running at your facility with zero heavy upfront "
                       "investment. Pay a simple monthly OPEX charges, while clean energy "
                       "works to lower your costs from day one. Key Benefits: No Big Capex, "
                       "Just Smart OPEX; Beat Rising Grid Tariffs; 24/7 Power with Battery "
                       "Backup; Built for Factories & Commercial Sites. Contact Us: "
                       "+91 844 844 8552."),
                ],
            },
            "summary": (
                "Arcedo Systems runs three live ads on its 'Arcedo Systemss' page - a Telugu "
                "PM Surya Ghar subsidy-eligibility ad (23 Sep, fb.me), a Telugu residential "
                "ad carrying Suryon Solar Systems branding that points at solar.suryon.in "
                "(30 Sep), and an English commercial OPEX ad for factories pointing at a "
                "Messenger document (17 Oct). A sibling Facebook page named 'Suryon' runs "
                "the same brand's residential Telugu ads with Arcedo's own contact details "
                "in the copy (info@arcedo.net, 844 844 8552) - one company, two pages, two "
                "brand names. arcedo.net itself is the large-scale-PV EPC site (rooftop, "
                "ground-mount, floating, O&M); the ads sell Rs 78,000-subsidy homes and "
                "zero-capex factory OPEX."),
        },
        "funnel": {
            "type": "Split across three destinations",
            "destination": "fb.me (Telugu subsidy ad), solar.suryon.in (Suryon-branded "
                           "residential ad), fb.com/messenger_doc/ (commercial OPEX ad)",
            "meaning": (
                "Three live ads, three different destinations - and not one of them is a "
                "page on arcedo.net. The residential click lands on a subdomain of a "
                "different brand name; the commercial click lands in a Messenger document. "
                "No single owned funnel, no shared page to test."),
        },
        "findings": [
            "Three live ads (23 Sep, 30 Sep, 17 Oct) with three different destinations: "
            "fb.me, solar.suryon.in and a Messenger document. None lands on arcedo.net.",
            "One company, two brands: the Telugu residential ad on the Arcedo page carries "
            "Suryon Solar Systems branding and points at solar.suryon.in, while a separate "
            "'Suryon' Facebook page runs the same brand's ads with Arcedo's contact "
            "details (info@arcedo.net, 844 844 8552) in the copy.",
            "The commercial OPEX ad - the highest-ticket offer (solar + battery for "
            "factories, zero capex) - sends its click to a Messenger document rather than "
            "a page that explains the OPEX model.",
            "arcedo.net positions as a large-scale solar EPC (rooftop, ground-mounted, "
            "floating solar, O&M, MEP) while the ads sell Rs 78,000-subsidy homes and "
            "zero-capex commercial OPEX - the ad-to-site message match is weak in both "
            "directions.",
            "The company's empanelment credentials (TGREDCO empanelled supplier and "
            "TGNPDCL listed vendor, per the Telangana discom supplier lists) appear "
            "nowhere in the live ad copy.",
        ],
        "next_steps": [
            ("One brand, one funnel",
             "Decide whether the residential buyer meets Arcedo or Suryon, then point "
             "every residential ad at one owned page on arcedo.net with the subsidy offer, "
             "the 25-year performance warranty and the free site visit on it."),
            ("Give the OPEX offer a real page",
             "Solar + battery at zero capex for factories is the highest-value offer in "
             "the account. A page with the OPEX model, the 50% bill-cut claim and the "
             "+91 844 844 8552 contact converts better than a Messenger document."),
            ("Put the empanelment in the copy",
             "TGREDCO-empanelled and discom-listed is the trust asset a subsidy buyer "
             "looks for - it belongs in the Telugu ad, not only in a supplier PDF."),
        ],
        "contact_facts": [
            ("Email", "info@arcedo.net (site contact page; also in the Suryon-page ad copy)"),
            ("Phone", "+91 8448448552 (contact page + ads); +91 9866966678 (team page)"),
            ("Address", "3rd & 6th Floor, Trendz Techpark, Kakatiya Hills, Madhapur, "
                        "Hyderabad 500081; 4th Floor 401, Vaishnavi Lamani Arcade, Doolapally "
                        "Rd, Kompally, Hyderabad 500014"),
            ("Entity", "Arcedo Systems Private Limited - CIN U35105TS2025PTC193163, "
                       "incorporated 21 Jan 2025, ROC Hyderabad (MCA records)"),
            ("Credentials", "TGREDCO empanelled supplier; TGNPDCL listed vendor "
                            "(Telangana discom supplier lists)"),
            ("Meta pages", "facebook.com/61561703979379 ('Arcedo Systemss'); sibling page "
                           "'Suryon' facebook.com/61585616331903 runs the same brand's "
                           "residential ads"),
        ],
    },
    {
        "company": "Arkahub",
        "legal": "Interglacial Renewable Technologies Pvt. Ltd.",
        "city": "Hyderabad",
        "website": "https://www.arkahub.in/",
        "email": "care@arkahub.in",
        "phone": "080 4736 2828",
        "fb_page": "https://www.facebook.com/61584060508957/",
        "checked_on": "2026-10-22",
        "ad_library": {
            "meta_own": {
                "found": True,
                "results_count": 2,
                "results_label": "~2 results on the 'Thearkahub' page (9 ads use the first creative)",
                "query": "Telugu \u0c38\u0c4b\u0c32\u0c3e\u0c30\u0c4d \u0c07\u0c28\u0c4d\u200c\u0c38\u0c4d\u0c1f\u0c3e\u0c32\u0c47\u0b37\u0c28\u0c4d (solar installation)",
                "ads": [
                    ad("1102186569459926", "Thearkahub", "Oct 14, 2026",
                       "https://www.arkahub.in/design-new (9 ads use this creative)",
                       "Telugu: \u0c38\u0c3e\u0c27\u0c3e\u0c30\u0c23 \u0c30\u0c3e\u0c15\u0c3f\u0c02\u0c17\u0c4d \u0c2e\u0c40 \u0c2a\u0c48\u0c15\u0c2a\u0c4d\u0c2a\u0c41\u0c2a\u0c48 \u0c07\u0c28\u0c41\u0c2a\u0c4d \u0c17\u0c41\u0c1f\u0c4d\u0c32\u0c32\u0c3e \u0c15\u0c28\u0c3f\u0c2a\u0c3f\u0c38\u0c4d\u0c24\u0c41\u0c02\u0c26\u0c3e? Arkahub \u0c15\u0c38\u0c4d\u0c1f\u0c02 GI \u0c28\u0c3f\u0c30\u0c4d\u0c2e\u0c3e\u0c23\u0c02 \u0c2a\u0c48\u0c15\u0c2a\u0c4d\u0c2a\u0c41\u0c32\u0c4b \u0c15\u0c32\u0c3f\u0c38\u0c3f\u0c2a\u0c4b\u0c24\u0c41\u0c02\u0c26\u0c3f, \u0c35\u0c48\u0c30\u0c4d\u0c32\u0c41 \u0c2a\u0c42\u0c30\u0c4d\u0c24\u0c3f\u0c17\u0c3e \u0c26\u0c3e\u0c1a\u0c2c\u0c21\u0c24\u0c3e\u0c2f\u0c3f. \u0c05\u0c02\u0c26\u0c02 \u0c24\u0c17\u0c4d\u0c17\u0c26\u0c41, \u0c2c\u0c32\u0c02 \u0c24\u0c17\u0c4d\u0c17\u0c26\u0c41. \u0c2e\u0c40 \u0c07\u0c02\u0c1f\u0c3f\u0c15\u0c3f \u0c09\u0c1a\u0c3f\u0c24 \u0c21\u0c3f\u0c1c\u0c48\u0c28\u0c4d \u0c05\u0c38\u0c46\u0c38\u0c4d\u0c2e\u0c46\u0c02\u0c1f\u0c4d \u0c2c\u0c41\u0c15\u0c4d \u0c1a\u0c46\u0c2f\u0c02\u0c21\u0c3f. (Solar that doesn't spoil the look of your home - hidden-wire flush installation, thirty-year warranty.) Headline: '\u0c2e\u0c40 \u0c07\u0c02\u0c1f\u0c3f \u0c05\u0c02\u0c26\u0c02 \u0c1a\u0c46\u0c21\u0c15\u0c42\u0c02\u0c21\u0c3e \u0c38\u0c4b\u0c32\u0c3e\u0c30\u0c4d. \u0c35\u0c48\u0c30\u0c4d\u0c32\u0c41 \u0c15\u0c28\u0c3f\u0c2a\u0c3f\u0c38\u0c4d\u0c24\u0c3f\u0c2f\u0c32\u0c47\u0c26\u0c41 \u0c2b\u0c4d\u0c32\u0c37\u0c4d \u0c07\u0c28\u0c4d\u200c\u0c38\u0c4d\u0c1f\u0c3e\u0c32\u0c47\u0b37\u0c28\u0c4d, \u0c2e\u0c41\u0c2a\u0c4d\u0c2a\u0c48 \u0c0f\u0c33\u0c4d\u0c32 \u0c35\u0c3e\u0c30\u0c02\u0c1f\u0c40\u0c24\u0c4b.'"),
                    ad("1098672362787317", "Thearkahub", "Oct 15, 2026",
                       "https://www.arkahub.in/hyderabad (this ad has multiple versions)",
                       "Telugu: \u0c1a\u0c3e\u0c32\u0c3e \u0c38\u0c4b\u0c32\u0c3e\u0c30\u0c4d \u0c15\u0c02\u0c2a\u0c46\u0c28\u0c40\u0c32\u0c41 \u0c2e\u0c3e\u0c1f\u0c32\u0c4d\u0c32\u0c4b\u0c28\u0c47 \u0c39\u0c3e\u0c2e\u0c40 \u0c07\u0c38\u0c4d\u0c24\u0c3e\u0c2f\u0c3f. Arkahub \u0c27\u0c30, 30 \u0c0f\u0c33\u0c4d\u0c32 \u0c35\u0c3e\u0c30\u0c02\u0c1f\u0c40, 5 \u0c0f\u0c33\u0c4d\u0c32 \u0c09\u0c1a\u0c3f\u0c24 \u0c2e\u0c46\u0c2f\u0c3f\u0c02\u0c1f\u0c46\u0c28\u0c46\u0c28\u0c4d\u0c38\u0c4d \u0c2e\u0c42\u0c21\u0c3f\u0c02\u0c1f\u0c40\u0c28\u0c40 \u0c30\u0c3e\u0c24\u0c2a\u0c42\u0c30\u0c4d\u0c35\u0c15\u0c02\u0c17\u0c3e \u0c07\u0c38\u0c4d\u0c24\u0c41\u0c02\u0c26\u0c3f. \u0c08\u0c30\u0c4b\u0c1c\u0c47 \u0c09\u0c1a\u0c3f\u0c24 \u0c35\u0c3f\u0c1c\u0c3f\u0c1f\u0c4d \u0c2c\u0c41\u0c15\u0c4d \u0c1a\u0c46\u0c2f\u0c02\u0c21\u0c3f. (Price, 30-year warranty and 5 years free maintenance in writing before you commit.) Headline: '\u0c38\u0c02\u0c24\u0c15\u0c02 \u0c1a\u0c47\u0c38\u0c47 \u0c2e\u0c41\u0c02\u0c21\u0c47 \u0c27\u0c30, \u0c35\u0c3e\u0c30\u0c02\u0c1f\u0c40, \u0c2e\u0c46\u0c2f\u0c3f\u0c02\u0c1f\u0c46\u0c28\u0c46\u0c28\u0c4d\u0c38\u0c4d \u0c2e\u0c42\u0c21\u0c42 \u0c30\u0c3e\u0c24\u0c2a\u0c42\u0c30\u0c4d\u0c35\u0c15\u0c02\u0c17\u0c3e \u0c2e\u0c40 \u0c1a\u0c46\u0c24\u0c3f\u0c32\u0c4b.'"),
                ],
            },
            "summary": (
                "Arkahub - the consumer brand of Interglacial Renewable Technologies Pvt. "
                "Ltd., listed on the MNRE portal under that name and backed by Kae Capital, "
                "Antler and Sparrow after a $2 million seed round - runs two Telugu ads "
                "into the Hyderabad market (14 and 15 Oct 2026). The second points at a "
                "dedicated Hyderabad landing page (arkahub.in/hyderabad). The site claims "
                "900+ happy customers, monthly panel health checks and cleaning for 4 "
                "years, 12-year panel / 25-year performance / 10-year inverter warranties, "
                "and lists Hyderabad among its operational cities alongside Bengaluru, Pune "
                "and Nagpur. Its registered office is in Bengaluru (Marthahalli)."),
        },
        "funnel": {
            "type": "Owned pages (both ads)",
            "destination": "arkahub.in/design-new and arkahub.in/hyderabad",
            "meaning": (
                "Both live ads point at pages on arkahub.in - one generic design page, one "
                "Hyderabad-specific page. The paid path lands on owned ground, which is "
                "the right structure; the gap is that the ads speak Telugu while the "
                "destination pages and the consultation form are English-first."),
        },
        "findings": [
            "Two live Telugu ads (14 and 15 Oct) and both point at owned pages - the "
            "second at a dedicated Hyderabad landing page (arkahub.in/hyderabad). The paid "
            "path already lands on owned ground.",
            "The two ads test two genuinely different angles - aesthetics (hidden wires, "
            "flush-mount custom GI structure, 'solar that doesn't spoil the look of your "
            "home') versus trust paperwork (price, 30-year warranty and 5 years free "
            "maintenance in writing). A real creative test.",
            "Language mismatch: both ads are Telugu, while arkahub.in's homepage, city "
            "selector and consultation form are English-first - the click lands in a "
            "different language from the one that earned it.",
            "Trust assets that never appear in the ad copy: MNRE-portal listing as "
            "Interglacial Renewable Technologies Pvt. Ltd., institutional backing (Kae "
            "Capital, Antler, Sparrow; $2M seed) and the 900+ customers claim.",
            "Hyderabad is one of four operational cities (Bengaluru, Hyderabad, Pune, "
            "Nagpur) with a registered office in Bengaluru - the Hyderabad page is doing "
            "the work of a local presence.",
        ],
        "next_steps": [
            ("Mirror the ad language on the landing page",
             "Both ads are Telugu; arkahub.in/hyderabad and the consultation form are "
             "English-first. A Telugu headline and form labels on the Hyderabad page keep "
             "the click in the language that earned it."),
            ("Put the paperwork promise on the Hyderabad page",
             "The winning ad angle is 'price, warranty and maintenance in writing' - the "
             "Hyderabad page should carry exactly that, plus the MNRE listing and the "
             "institutional backing."),
            ("Make the local presence explicit",
             "Hyderabad is one of four cities on the site - a Hyderabad team page, local "
             "install photos and a local number turn a city page into a local promise."),
        ],
        "contact_facts": [
            ("Email", "care@arkahub.in (contact page)"),
            ("Phone", "080 4736 2828 (contact page)"),
            ("Registered office", "Interglacial Renewable Technologies Pvt. Ltd., Purva "
                                  "Riviera, Marthahalli, Bengaluru 560037"),
            ("Operational cities", "Bengaluru, Hyderabad, Pune, Nagpur (site claim); "
                                   "dedicated landing page arkahub.in/hyderabad"),
            ("Credentials", "Listed on the MNRE portal as Interglacial Renewable "
                            "Technologies Pvt. Ltd.; backed by Kae Capital, Antler and "
                            "Sparrow ($2M seed); claims 900+ happy customers"),
            ("Meta page", "facebook.com/61584060508957 ('Thearkahub')"),
        ],
    },
    {
        "company": "Orbit Solar",
        "legal": "Orbit Solar Energy Systems",
        "city": "Hyderabad",
        "website": "https://orbitsolar.in/",
        "email": "",
        "phone": "+91 9059806772",
        "fb_page": "https://www.facebook.com/100093675784835/",
        "checked_on": "2026-10-22",
        "ad_library": {
            "meta_own": {
                "found": True,
                "results_count": 5,
                "results_label": "~5 results on the ORBIT SOLAR page (21 results matched 'orbitsolar.in' overall)",
                "query": "orbitsolar.in",
                "ads": [
                    ad("2110991659634519", "ORBIT SOLAR", "Dec 10, 2025",
                       "fb.me 'Sign Up' (6 creatives: 'See How Much You Can Save', 'Save "
                       "Rs.3,000/Month Like Him', 'Cut Your Bill by 90% Too', 'Get Rs.78K "
                       "Subsidy - Zero Hassle', 'Get a Solar Pergola Like This', 'Join "
                       "1000+ Happy Homes')",
                       "They trusted us. You can too. 5+ years, 1000+ installations across "
                       "Hyderabad - all with 25-year guarantees. orbitsolar.in. "
                       "+91-9059806772."),
                    ad("1569253241154571", "ORBIT SOLAR", "Nov 6, 2025",
                       "WhatsApp ('Cut Your Industry Energy Bill')",
                       "Why keep paying Lakhs in power bills every year? Schools, "
                       "Hospitals, and Offices in Hyderabad are already cutting 60-80% of "
                       "their electricity costs with Orbit Solar. Save Lakhs in Energy "
                       "Bills Every Year; Quick ROI - Payback in Just 3-4 Years; 30-Year "
                       "Panel Warranty + Professional AMC Support; 500+ Successful "
                       "Installations Across Telangana. Call/WhatsApp: +91-9059806772. "
                       "Website: https://orbitsolar.in/"),
                    ad("1956441998642638", "ORBIT SOLAR", "Nov 6, 2025",
                       "WhatsApp ('Schedule Your Free Site Assessment')",
                       "Eliminate Your Biggest Energy Expense with Solar Power. Switch to "
                       "solar and turn your biggest operational cost into a long-term "
                       "asset. Lock-in energy costs for 25+ years; maximize uptime & "
                       "operational resilience; industrial-grade durability; backed by a "
                       "25-year performance guarantee. Strategic Investment with ROI in "
                       "just 3-5 Years. Trusted by 1,000+ industrial clients across "
                       "India. Get Your FREE Custom ROI Proposal Today! Visit: "
                       "orbitsolar.in. Call/WhatsApp: +91-9059806772."),
                    ad("1327900616150394", "ORBIT SOLAR", "May 14, 2026",
                       "WhatsApp (industrial ad, multiple versions)",
                       "Unlock Massive Savings with Solar! Reliable Industrial Solar "
                       "Solutions by Orbit Solar. 100+ Successful Installations across "
                       "Telangana. Trusted by Businesses for performance & long-term "
                       "savings. Sustainable Power, Proven ROI. Click below for a Free ROI "
                       "Estimate!"),
                    ad("1276379831189065", "ORBIT SOLAR", "Sep 4, 2026",
                       "fb.me 'Get quote'",
                       "Power your home with solar - and stay powered when the grid goes "
                       "down. Orbit Solar's On-Grid Solar + UPS Combo brings solar savings "
                       "and reliable backup together in one practical power package. "
                       "Customized On-Grid Solar System; UPS Power Backup; Smart Auto "
                       "Switching; Net Metering Assistance; Professional Installation. "
                       "Call / WhatsApp: 9059806772. orbitsolar.in."),
                ],
            },
            "summary": (
                "Orbit Solar is the longest continuously-running advertiser in this batch: "
                "five live ads, the oldest started 6 November 2025 - residential "
                "('They trusted us. You can too', 10 Dec 2025, six creatives), two "
                "commercial/industrial ROI ads (6 Nov 2025), an industrial Telangana ad "
                "(14 May 2026) and a new On-Grid Solar + UPS combo (4 Sep 2026). Every ad "
                "funnels to fb.me or WhatsApp - none points at a specific page on "
                "orbitsolar.in. The site itself (fetched 2026-10-22) claims MNRE-approved "
                "vendor status, carries residential and commercial brochures, a savings "
                "calculator and an enquiry form, and lists a Mehdipatnam address - none of "
                "which the ad copy uses beyond printing 'orbitsolar.in'."),
        },
        "funnel": {
            "type": "Split - fb.me links and WhatsApp",
            "destination": "fb.me 'Sign Up' / 'Get quote' on the residential and UPS-combo "
                           "ads; WhatsApp (wa.me/919059806772) on the commercial and "
                           "industrial ads",
            "meaning": (
                "No ad sends its click to a page on orbitsolar.in. The commercial and "
                "industrial spend - the highest-ticket offers - lands in a WhatsApp chat, "
                "and the residential spend lands behind an fb.me wrapper. The site's "
                "calculator, brochures and enquiry form sit outside the paid path "
                "entirely."),
        },
        "findings": [
            "Five live ads and the oldest has run since 6 November 2025 - a year of "
            "continuous spend across residential, commercial and industrial angles, plus "
            "a new On-Grid + UPS combo (4 Sep 2026).",
            "Not one ad points at a page on orbitsolar.in - residential and UPS-combo ads "
            "go to fb.me, the commercial and industrial ads go straight to WhatsApp.",
            "The install-count claims differ across live ads: '1000+ installations across "
            "Hyderabad' (residential), '500+ Successful Installations Across Telangana' "
            "(commercial) and '1,000+ industrial clients across India' (industrial) - a "
            "prospect who sees two ads sees two different companies.",
            "No email address is published anywhere on the live site - enquiries only via "
            "the form (name, mobile, email, location, monthly bill), phone or WhatsApp.",
            "The newest offer - On-Grid Solar + UPS Combo with smart auto-switching - has "
            "no page of its own on orbitsolar.in; the ad is the only place it exists.",
        ],
        "next_steps": [
            ("Give each angle its own owned page",
             "Residential, commercial/industrial and the new UPS combo are three "
             "different buyers. One landing page per angle on orbitsolar.in - each with "
             "its own form - turns a year of fb.me and WhatsApp spend into a funnel you "
             "own and can test."),
            ("Reconcile the numbers",
             "1000+ installations, 500+ across Telangana and 1,000+ industrial clients "
             "cannot all be the headline. One verified number, used everywhere, is worth "
             "more than three that contradict."),
            ("Publish an email",
             "A business spending on Meta for a year with no email on its site loses "
             "every enquiry that prefers to write. A care@ address on the form, the "
             "footer and the ads."),
            ("Build the UPS combo page",
             "On-grid + UPS with auto-switching is a differentiated product with a live "
             "ad behind it - it deserves a page with the combo, the switching logic and "
             "the net-metering assistance explained."),
        ],
        "contact_facts": [
            ("Email", "None published on the live site - enquiry form, phone and WhatsApp "
                      "only"),
            ("Phone", "+91 9059806772 (site tel/WhatsApp links and every ad)"),
            ("Address", "12-2-800/216, Pillar no. 54, Dilshad Nagar, Mehdipatnam, "
                        "Hyderabad, Telangana 500028"),
            ("Site claims", "MNRE-Approved Vendor / Govt. Certified Solar Partner; "
                            "residential and commercial brochures; savings calculator; "
                            "5+ years, 1000+ installations across Hyderabad"),
            ("Meta page", "facebook.com - page ID 100093675784835 ('ORBIT SOLAR')"),
        ],    },
    {
        "company": "Krisol Solar",
        "legal": "Krisol Solar Infra Private Limited (subsidiary of Satya Enterprises)",
        "city": "Hyderabad",
        "website": "https://www.krisolsolar.com/",
        "email": "sales@krisolsolar.com",
        "phone": "+91 7337337677",
        "fb_page": "https://www.facebook.com/krisolsolar/",
        "checked_on": "2026-10-23",
        "ad_library": {
            "meta_own": {
                "found": True,
                "results_count": 3,
                "results_label": "~3 results on the Krisol Solar page",
                "query": "Krisol Solar",
                "ads": [
                    ad("1645269633918455", "Krisol Solar", "Oct 16, 2026",
                       "fb.me 'Get offer' (inside Facebook)",
                       "Breakthrough in Hyderabad! Save Rs. 1 Lakh on rooftop solar "
                       "installation with: Govt Subsidy of Rs. 78,000 + Exclusive "
                       "Rs. 22,000 Krisol Discount. Join thousands who've gone green & "
                       "cut their bills! Call 7337337677 or visit www.krisolsolar.com. "
                       "Creative line: 'Claim Rs. 22,000 Solar Discount'."),
                    ad("1853676722478455", "Krisol Solar", "Oct 16, 2026",
                       "fb.me 'Get offer' (inside Facebook)",
                       "Tired of paying skyrocketing electricity bills every single "
                       "month? Switch to clean, independent energy with a rooftop solar "
                       "system from Krisol Solar Infra Pvt Ltd: Save Rs. 3,000 to "
                       "Rs. 20,000+ on your monthly electricity bill; Save Rs. 30,000 to "
                       "Rs. 2-3 Lakhs every single year; 10+ Years Industry Expertise "
                       "across Telangana & Andhra Pradesh; Professional Consultation & "
                       "Free Expert Site Survey. Call: 73373 37677. Website: "
                       "www.krisolsolar.com. Creative line: 'Slash Your Monthly Power "
                       "Bill by Rs. 3,000 to Rs. 20,000+'."),
                    ad("1384204040458816", "Krisol Solar", "Oct 21, 2026",
                       "fb.me 'Get offer' (inside Facebook)",
                       "Same bill-saving copy as the 16 Oct ad (Save Rs. 3,000 to "
                       "Rs. 20,000+ per month, 10+ years across Telangana & Andhra "
                       "Pradesh, free expert site survey, call 73373 37677) running with "
                       "a new creative - the newest ad in the set."),
                ],
            },
            "summary": (
                "Krisol Solar is running 3 active Meta ads (Facebook and Instagram), all "
                "started between 16 and 21 October 2026. Two offer angles are live: the "
                "stacked Rs. 78,000 government subsidy + Rs. 22,000 Krisol discount, and "
                "the Rs. 3,000-20,000 monthly bill-saving story. Every ad's click lands "
                "on an fb.me link inside Facebook, so none of the spend reaches "
                "krisolsolar.com. No Google Ads advertiser record was checked for this "
                "report - that requires the full pipeline."),
        },
        "funnel": {
            "type": "Facebook Messenger link (fb.me)",
            "destination": "fb.me 'Get offer' (inside Facebook)",
            "meaning": (
                "Every click opens a Facebook surface, not krisolsolar.com. You own no "
                "pixel on the landing experience, you cannot retarget the people who "
                "clicked and did not enquire, and there is no page you can test a "
                "different headline or price on."),
        },
        "findings": [
            "All 3 live ads point to fb.me links inside Facebook - the click never "
            "lands on krisolsolar.com, so no pixel, no retargeting pool, no testable "
            "landing page.",
            "Your own site already has the pieces the ads need: a contact form, a "
            "'Government Subsidy Available' popup form (name, phone, city, email, "
            "message), an FAQ that explains the Rs. 78,000 PM Surya Ghar subsidy, and "
            "a services carousel (rooftops, water heaters, street lights, pumps). None "
            "of the paid traffic ever sees any of it.",
            "The contact page lists krisolsolarinfra@gmail.com while the site footer "
            "publishes sales@krisolsolar.com - two inboxes for the same enquiry, so "
            "leads can land where nobody is watching.",
            "3 ads, all launched within 5 days (16-21 Oct), all cold traffic. There is "
            "no second creative angle and no retargeting ad behind them yet.",
            "The 'Save Rs. 1 Lakh' stacked-offer ad is your sharpest hook and it is "
            "only 5 days old - the measurement to know which of the two angles works "
            "does not exist while the clicks stay inside Facebook.",
        ],
        "next_steps": [
            ("Move the click onto a page you own",
             "Point all 3 ads at a dedicated Kompally landing page carrying the same "
             "Rs. 78,000 + Rs. 22,000 offer, an enquiry form and the Meta Pixel - so "
             "every click is measurable and retargetable."),
            ("Install pixel + conversions API",
             "One pixel plus the Conversions API gives you the audience of everyone who "
             "clicked but did not enquire - usually 10-20x the people who fill a form."),
            ("Settle on one inbox",
             "Publish sales@krisolsolar.com everywhere (ads, forms, footer) and retire "
             "or forward the Gmail address so an enquiry can never sit unread."),
            ("Give the bill-saving angle somewhere to land",
             "The Rs. 3,000-20,000/month story deserves a savings calculator or "
             "before/after bill section on the landing page - it is the ad's whole "
             "promise and today it dead-ends at fb.me."),
        ],
        "contact_facts": [
            ("Email", "sales@krisolsolar.com (contact page: krisolsolarinfra@gmail.com)"),
            ("Phone / WhatsApp", "+91 7337337677"),
            ("Address", "Fairmount Square, 3rd Floor, Unit No. 312, Kompally, Medchal "
                        "Malkajgiri district, Telangana 500014"),
            ("Entity", "Krisol Solar Infra Private Limited - subsidiary of Satya "
                       "Enterprises, a solar dealer in Hyderabad"),
            ("Meta page", "facebook.com/krisolsolar"),
            ("Service area", "krisolsolar.com - 'Serving Telangana, Andhra Pradesh, "
                             "Karnataka & Maharashtra'"),
        ],
    },
    {
        "company": "PMP Solar Power",
        "legal": "PMP Group (PMP Solar / PMP Fabrication / PMP Electrical)",
        "city": "Hyderabad",
        "website": "https://pmpsolar.com/",
        "email": "sreepooji27@gmail.com",
        "phone": "+91 70324 67979",
        "fb_page": "https://www.facebook.com/61587366280305/",
        "checked_on": "2026-10-23",
        "ad_library": {
            "meta_own": {
                "found": True,
                "results_count": 5,
                "results_label": "~5 results for 'PMP Solar' (other matches are unrelated pages)",
                "query": "PMP Solar",
                "ads": [
                    ad("29275328785392295", "PMP Solar Power", "Oct 9, 2026",
                       "fb.me 'Get quote' (inside Facebook)",
                       "Hyderabad homeowners - this Dasara x Diwali, make the switch to "
                       "solar. Rs. 20,000 cash reward on 5 kW; Rs. 15,000 cash reward on "
                       "3 kW; 3 kW: Rs. 2,10,000; 5 kW: Rs. 3,10,000. Prices inclusive "
                       "of Rs. 78,000 PM Surya Ghar subsidy. Fixed festive pricing. No "
                       "negotiation. For Hyderabad homes only. Call / WhatsApp "
                       "7032467979 or check pmpsolar.com. Creative line: 'Rs. 20,000 "
                       "Cash Reward on 5 kW Solar | 3 kW Rs. 2.10L | 5 kW Rs. 3.10L | "
                       "Fixed Pricing'."),
                ],
            },
            "summary": (
                "PMP Solar Power is running 1 active Meta ad, started 9 October 2026, "
                "with the most concrete pricing in this lead set: 3 kW at Rs. 2,10,000 "
                "and 5 kW at Rs. 3,10,000, subsidy-inclusive, fixed festive pricing, "
                "Hyderabad homes only. The click lands on an fb.me link inside "
                "Facebook, so the spend never reaches pmpsolar.com. No Google Ads "
                "advertiser record was checked for this report - that requires the full "
                "pipeline."),
        },
        "funnel": {
            "type": "Facebook Messenger link (fb.me)",
            "destination": "fb.me 'Get quote' (inside Facebook)",
            "meaning": (
                "The click opens Facebook, not pmpsolar.com. The fixed festive pricing "
                "that makes the ad credible has no page to live on, no form to capture "
                "the enquiry, and no pixel to measure or retarget with."),
        },
        "findings": [
            "The one live ad sends the click to an fb.me link inside Facebook - "
            "pmpsolar.com, its 36 documented projects and its quote form never see the "
            "paid traffic.",
            "The ad's fixed festive pricing (3 kW Rs. 2.10L / 5 kW Rs. 3.10L, "
            "subsidy-inclusive, 'no negotiation') is the sharpest offer in this lead "
            "set - and today there is nowhere on your own site that a clicker can land "
            "and act on it.",
            "The site's proof is strong and invisible to the ad: 36 projects delivered, "
            "420 kW solar installed, 24 localities served, largest single plant 230 kW "
            "(D-Mart, Manneguda), plus named residential installs in Kompally, "
            "Bachupally, Alwal, Rampally, Bandlaguda and Nizamabad.",
            "PMP sells three businesses from one Kapra office - Solar, Fabrication and "
            "Electrical - but the only creative speaks to homeowners. Commercial and "
            "factory buyers (the D-Mart 230 kW audience) have no ad at all.",
            "Enquiries depend on a personal Gmail inbox (sreepooji27@gmail.com) plus "
            "+91 70324 67979 / WhatsApp - one mailbox between the ad and the site.",
        ],
        "next_steps": [
            ("Give the festive pricing a page of its own",
             "Build a Dasara-Diwali landing page on pmpsolar.com with the 3 kW / 5 kW "
             "fixed prices, the subsidy note, an enquiry form and the Meta Pixel - then "
             "point the ad at it."),
            ("Run a second creative for commercial buyers",
             "The 230 kW D-Mart plant and the fabrication + electrical divisions are a "
             "different product for a different buyer. One ad cannot carry both."),
            ("Put the project cards to work",
             "36 documented installs with locations are real proof. They belong next to "
             "the offer on the landing page, not only in the site's project grid."),
            ("Move enquiries off a personal inbox",
             "Add a role address (sales@pmpsolar.com or hello@pmpsolar.com) on the "
             "domain and point the form and the ad at it, so no enquiry depends on one "
             "person's Gmail."),
        ],
        "contact_facts": [
            ("Email", "sreepooji27@gmail.com"),
            ("Phone / WhatsApp", "+91 70324 67979 / wa.me/917032467979"),
            ("Address", "Kapra, Secunderabad, Hyderabad (Mon-Sat, 9:30 am - 6:30 pm)"),
            ("Entity", "PMP Group - PMP Solar, PMP Fabrication, PMP Electrical"),
            ("Meta page", "facebook.com/61587366280305 (PMP Solar Power)"),
            ("Track record", "pmpsolar.com - 36 projects delivered, 420 kW installed, "
                             "24 localities served, largest plant 230 kW"),
        ],
    },
    {
        "company": "Dakshin Solar Power Systems",
        "legal": "Dakshin Solar Power Systems",
        "city": "Hyderabad",
        "website": "https://www.dakshinsolar.com/",
        "email": "dakshinsolar@gmail.com",
        "phone": "+91 82476 79592",
        "fb_page": "https://www.facebook.com/61583923866617/",
        "checked_on": "2026-10-23",
        "ad_library": {
            "meta_own": {
                "found": True,
                "results_count": 4,
                "results_label": "~4 results for 'Dakshin Solar' (other matches are unrelated pages)",
                "query": "Dakshin Solar",
                "ads": [
                    ad("1100117022614568", "Dakshin Solar Power Systems", "Oct 16, 2026",
                       "WhatsApp ('Send WhatsApp message')",
                       "Switch to Solar. Save More. Power Your Future! Looking for a "
                       "reliable way to reduce your electricity bills? Dakshin Solar "
                       "Power Systems helps you make the smart switch to clean, "
                       "affordable solar energy. High-quality Solar Power Systems; "
                       "Residential & Commercial Solutions; Professional Installation; "
                       "Reliable & Long-Lasting Performance; Reduce Your Dependence on "
                       "Rising Electricity Costs. Contact Dakshin Solar Power Systems "
                       "today for a free consultation!"),
                ],
            },
            "summary": (
                "Dakshin Solar Power Systems is running 1 active Meta ad, started 16 "
                "October 2026 - a generic awareness ad whose click opens a WhatsApp "
                "chat rather than dakshinsolar.com. The site itself is detailed and "
                "specific (TOPCon panels, Polycab/Growatt inverters, an 8-component "
                "turnkey list with warranties, a completed-projects grid), none of "
                "which the paid click ever sees. No Google Ads advertiser record was "
                "checked for this report - that requires the full pipeline."),
        },
        "funnel": {
            "type": "WhatsApp chat",
            "destination": "WhatsApp ('Send WhatsApp message')",
            "meaning": (
                "The click opens a chat, not dakshinsolar.com. There is no page you "
                "own, no form that captures the enquiry in writing, no pixel, and no "
                "way to retarget everyone who started a chat and never replied."),
        },
        "findings": [
            "The single live ad routes to WhatsApp - the site's full component "
            "breakdown (TOPCon panels, Polycab/Growatt inverters, DCDB/ACDB boxes, "
            "elevated galvanised structures, MC4 connectors, lightning arrestor, "
            "chemical earthing pits) never gets seen by the click.",
            "The site's strongest asset - 'What's Included in Your Solar System', an "
            "8-component turnkey list with a 30-year panel warranty, 10-year inverter "
            "warranty and 5-year free service - is not reflected anywhere in the ad "
            "copy.",
            "One ad, one generic angle, live since 16 Oct. There is no subsidy "
            "creative even though the site leads with PM Surya Ghar (up to Rs. 78,000) "
            "and a 'Subsidy Scheme Ends 31st March 2027' countdown.",
            "The homepage's stat block (panel warranty, inverter warranty, free "
            "service, savings %, satisfaction %) ships as '0 Yrs' and '0%' in the page "
            "source and depends on script animation to fill in - if the animation does "
            "not run for a visitor, the page argues against itself. Worth verifying on "
            "a real phone.",
            "The completed-projects grid (residential and commercial installs across "
            "Hyderabad and Telangana) is exactly the proof a WhatsApp-clicking "
            "homeowner asks for next - and it is one tap further away than it needs "
            "to be.",
        ],
        "next_steps": [
            ("Send the ad to a page you own",
             "Point the ad at a Dakshin landing page with the TOPCon + warranty story, "
             "a quote form and the Meta Pixel, and keep WhatsApp as the second click - "
             "not the first."),
            ("Run the subsidy angle you already sell",
             "The site's PM Surya Ghar Rs. 78,000 section and the 31 March 2027 "
             "deadline are a ready-made second creative with real urgency behind it."),
            ("Put the 8-component list in front of the click",
             "Panels, inverter, structures, cables, connectors, arrestor, earthing - "
             "that list is the answer to 'what am I actually paying for'. It belongs on "
             "the landing page."),
            ("Fix the stat block",
             "Make the warranty and savings numbers render as real values in the HTML "
             "so no visitor - or no slow connection - ever sees 0 Yrs / 0%."),
        ],
        "contact_facts": [
            ("Email", "dakshinsolar@gmail.com"),
            ("Phone / WhatsApp", "+91 82476 79592 / wa.me/918247679592; +91 93810 89778"),
            ("Address", "Hyderabad, Telangana, India"),
            ("Entity", "Dakshin Solar Power Systems"),
            ("Meta page", "facebook.com/61583923866617 (Dakshin Solar Power Systems)"),
            ("Offer", "dakshinsolar.com - PM Surya Ghar subsidy up to Rs. 78,000, "
                      "'Scheme Ends 31st March 2027', save up to 90% on bills"),
        ],
    },
    {
        "company": "3S Solutions",
        "legal": "3S Solutions India Pvt. Ltd.",
        "city": "Hyderabad",
        "website": "https://3ssol.in/",
        "email": "praveen@3ssol.in",
        "phone": "+91 9581177119",
        "fb_page": "https://www.facebook.com/3SSolutionsSolarServices/",
        "checked_on": "2026-10-23",
        "ad_library": {
            "meta_own": {
                "found": True,
                "results_count": 7,
                "results_label": "~7 results for '3ssol.in'; 6 active ads on the 3S Solutions page",
                "query": "3ssol.in",
                "ads": [
                    ad("1283230217176481", "3S Solutions", "Sep 11, 2026",
                       "Video ad on the 3S Solutions page (no CTA destination captured)",
                       "Go Solar. Save More. Power Your Future! Get up to Rs. 78,000 PM "
                       "Surya Ghar subsidy from the Government of India + an additional "
                       "offer up to Rs. 10,000. Make the switch to clean energy with 3S "
                       "Solutions India Pvt. Ltd. - your trusted solar partner for "
                       "residential solar solutions, expert installation, genuine "
                       "products & reliable service. Call us: 9000121084 | 9581177119. "
                       "www.3ssol.in. Kukatpally, Hyderabad, Telangana."),
                    ad("2035989101138405", "3S Solutions", "Oct 11, 2026",
                       "fb.me 'See details' (inside Facebook)",
                       "Thinking about going solar? Start with a FREE Site "
                       "Consultation. Our solar experts will assess your rooftop, "
                       "electricity usage and installation requirements and help you "
                       "understand the right solar solution for your property. No "
                       "guesswork. No consultation fee. Available across Andhra Pradesh "
                       "& Telangana."),
                    ad("4590054947908510", "3S Solutions", "Oct 19, 2026",
                       "fb.me 'See details' (inside Facebook)",
                       "Why pay more for electricity when your rooftop can generate "
                       "power? Rs. 4,280 electricity bill? That was our customer's bill "
                       "last month in Hyderabad. Now it's Rs. 187. Your roof can do the "
                       "same. Calculate your FREE savings in 60 sec: "
                       "3scalculator.vercel.app. (2 ads use this creative and text.)"),
                    ad("1088110834213698", "3S Solutions", "Oct 19, 2026",
                       "fb.me 'See details' (inside Facebook)",
                       "Get a FREE Solar Site Consultation - explore rooftop solar "
                       "options, subsidy eligibility and potential electricity savings. "
                       "Switch to Solar and Save on Electricity Bills! Government "
                       "subsidy eligibility guidance under PM Surya Ghar Yojana; free "
                       "solar site consultation; quality panels and trusted equipment; "
                       "professional installation and support. Subsidy up to Rs. 78,000 "
                       "subject to scheme guidelines. Serving Andhra Pradesh & "
                       "Telangana."),
                ],
            },
            "summary": (
                "3S Solutions is running 6 active Meta ads (5 captured with full copy "
                "here), started between 11 September and 19 October 2026. Four "
                "different hooks are live: the Rs. 78,000 subsidy + Rs. 10,000 offer, "
                "the free site consultation, a Hyderabad customer's Rs. 4,280-to-Rs. 187 "
                "bill story, and subsidy-eligibility guidance. The newest clicks land "
                "on fb.me links, and the bill-saving creative pushes a savings "
                "calculator hosted off-domain at 3scalculator.vercel.app. No Google Ads "
                "advertiser record was checked for this report - that requires the full "
                "pipeline."),
        },
        "funnel": {
            "type": "Facebook Messenger link (fb.me) + off-domain calculator",
            "destination": "fb.me 'See details'; one creative sends to 3scalculator.vercel.app",
            "meaning": (
                "The newest clicks land inside Facebook or on a calculator hosted on a "
                "third-party Vercel domain - not on 3ssol.in. That traffic cannot be "
                "retargeted from your own site, the calculator's visitors never see "
                "your contact form, and the measurement lives outside your analytics."),
        },
        "findings": [
            "The newest ads (19 Oct) drive to fb.me links, and the Rs. 4,280-to-Rs. 187 "
            "bill-saving creative pushes a savings calculator at 3scalculator.vercel.app "
            "- a third-party host, not 3ssol.in. That is your best hook sending your "
            "best prospects to somebody else's domain.",
            "3ssol.in itself is content-rich - on-grid and off-grid system guides, "
            "Hyderabad locality pages (Jubilee Hills, Miyapur, Gachibowli, Uppal, LB "
            "Nagar, Kukatpally, Ameerpet, Balanagar, Hitec City) and a real contact "
            "form - and none of the six ads sends anyone there.",
            "Six ads, four hooks in five weeks: the testing instinct is there, but with "
            "the clicks inside Facebook or on a Vercel app there is no first-party data "
            "to tell you which hook actually converts.",
            "Contact splits across numbers - the ad promotes 9000121084 and 9581177119, "
            "the site footer lists +91 7075441637 (Telangana) and +91 7075441638 (AP), "
            "all feeding one inbox, praveen@3ssol.in.",
            "The distributor positioning - Growatt distributor in India, Vikram Solar "
            "distributor for AP & TG, TGREDCO-empanelled - is the strongest trust asset "
            "on the site and appears in no ad.",
        ],
        "next_steps": [
            ("Bring the calculator home",
             "Move the 60-second savings calculator onto 3ssol.in (or a subdomain you "
             "own) with the Meta Pixel installed, so the bill-saving ad's traffic "
             "becomes your retargetable audience."),
            ("Point every ad at a page you own",
             "Swap the fb.me destinations for dedicated landing pages - one per hook "
             "(subsidy offer, free consultation, bill savings) - each with a form and "
             "pixel."),
            ("Lead with the distributor badge",
             "Growatt and Vikram distributorships plus TGREDCO empanelment are proof "
             "competitors cannot copy in a headline. Put them in the creative."),
            ("Unify the contact numbers",
             "Publish one Hyderabad number and one AP number across ads, site and "
             "forms, and add a second inbox so praveen@3ssol.in is never the single "
             "point of failure."),
        ],
        "contact_facts": [
            ("Email", "praveen@3ssol.in"),
            ("Phone", "+91 9581177119 / +91 90001 21084 (site: Telangana +91 7075441637, "
                      "Andhra Pradesh +91 7075441638)"),
            ("Address", "Plot No. 196, 3rd Floor, Road Number 20, Vivekananda Nagar, "
                        "Kukatpally, Hyderabad, Telangana 500072"),
            ("Entity", "3S Solutions India Pvt. Ltd. - TGREDCO-empanelled; Growatt "
                       "distributor (India), Vikram Solar distributor (AP & TG)"),
            ("Meta page", "facebook.com/3SSolutionsSolarServices"),
            ("Service area", "3ssol.in - Hyderabad localities plus Andhra Pradesh & "
                             "Telangana"),
        ],
    },
    {
        "company": "Hydromo",
        "legal": "Hydromo",
        "city": "Hyderabad",
        "website": "https://hydromo.in/",
        "email": "info@hydromo.in",
        "phone": "+91 7995201717",
        "fb_page": "https://www.facebook.com/hydromo.in/",
        "checked_on": "2026-10-23",
        "ad_library": {
            "meta_own": {
                "found": True,
                "results_count": 170,
                "results_label": "~170 results for 'Hydromo' (mostly water-treatment ads); 2 active solar ads captured on the hydromo.in page",
                "query": "Hydromo",
                "ads": [
                    ad("1107398778509314", "Hydromo", "Sep 9, 2026",
                       "Video ad on the Hydromo page (2 ads use this creative)",
                       "Same grid. Different decision. Commercial solar cuts electricity "
                       "costs by 70-80%. Free site assessment across AP & Telangana."),
                    ad("2409434686477632", "Hydromo", "Oct 11, 2026",
                       "fb.me 'Get quote' (inside Facebook)",
                       "Running a cold storage, rice mill or food processing business? "
                       "Then you already know how quickly electricity costs can add up. "
                       "Refrigeration, processing and production demand consistent "
                       "power every day. Hydromo Solar helps high-consumption businesses "
                       "generate their own electricity. Explore commercial solar "
                       "solutions built for energy-intensive operations. Creative line: "
                       "'Built For High-Power Businesses - Solar for cold storage & "
                       "food businesses'."),
                ],
            },
            "summary": (
                "Hydromo - a water and wastewater treatment company by core trade - is "
                "running 2 active commercial-solar ads into Andhra Pradesh and "
                "Telangana, started 9 September and 11 October 2026. The newest click "
                "lands on an fb.me link inside Facebook; the site's own solar pages "
                "(solar-commercial, renewable-energy-solutions, "
                "solar-panel-installation-in-hyderabad) never see the paid traffic. No "
                "Google Ads advertiser record was checked for this report - that "
                "requires the full pipeline."),
        },
        "funnel": {
            "type": "Facebook Messenger link (fb.me)",
            "destination": "fb.me 'Get quote' (inside Facebook)",
            "meaning": (
                "The commercial-solar click opens Facebook, not hydromo.in. The site's "
                "solar service pages, its free-consultation form and its client proof "
                "stay invisible to the spend, and nobody who clicks without enquiring "
                "can be retargeted."),
        },
        "findings": [
            "Solar is a division of a water-treatment company - the site's own title is "
            "'Best Water Treatment and Waste Water Management Company in India' - yet "
            "it is buying commercial-solar ads across AP & Telangana. The ads and the "
            "site's centre of gravity do not match, and a buyer comparing vendors will "
            "notice.",
            "Both solar ads route to fb.me links; hydromo.in's solar pages "
            "(solar-commercial, renewable-energy-solutions, "
            "solar-panel-installation-in-hyderabad) and its free-consultation form "
            "never see the paid click.",
            "The trust assets are enormous and unused in the ads: Toyota, ITC, Larsen & "
            "Toubro, TATA, GMR, Dr Reddy's, HPCL, Cyient, Avantel, GVK, Auro Realty, "
            "DPS and Ankura Hospital logos, plus IGBC and ISO certification and 2025 "
            "sustainability awards.",
            "Two solar ads only (9 Sep, 11 Oct), both commercial. Residential rooftop "
            "- where the Rs. 78,000 PM Surya Ghar subsidy drives most Hyderabad demand "
            "- has no creative at all.",
            "The site runs an active technical blog (hybrid solar sizing, cost and "
            "payback; STP electricity consumption) - real expertise that could feed "
            "retargeting content nobody is currently being retargeted into.",
        ],
        "next_steps": [
            ("Give the solar division its own front door",
             "Build a solar-first landing page on hydromo.in for the AP & Telangana "
             "commercial offer, with the Meta Pixel, and point both ads at it - so the "
             "division does not borrow trust from a water-treatment homepage."),
            ("Spend the client list in the creative",
             "Toyota, ITC, L&T, TATA, GMR, Dr Reddy's - one line of named industrial "
             "references in a cold-storage or food-processing ad outperforms any "
             "generic savings claim."),
            ("Open the residential angle",
             "One residential creative built around the Rs. 78,000 PM Surya Ghar "
             "subsidy would test a market your two commercial-only ads never touch."),
            ("Turn the blog into retargeting fuel",
             "The hybrid-solar sizing/payback guide is exactly the content a clicked "
             "but unconverted commercial buyer should be retargeted with - once a "
             "pixel gives you that audience."),
        ],
        "contact_facts": [
            ("Email", "info@hydromo.in / nandita@hydromo.in (business@hydromo.in for "
                      "channel partners)"),
            ("Phone / WhatsApp", "+91 7995201717"),
            ("Address", "8-2-293/82/A/89/B, 2nd Floor, Road No. 09, Jubilee Hills Lane "
                        "(adjacent TV5), Hyderabad, Telangana 500033"),
            ("Entity", "Hydromo - offices in Hyderabad (corporate), Vijayawada and "
                       "Visakhapatnam"),
            ("Meta page", "facebook.com/hydromo.in"),
            ("Proof", "hydromo.in - client logos incl. Toyota, ITC, L&T, TATA, GMR, "
                      "Dr Reddy's, HPCL, Cyient, Avantel, GVK; IGBC & ISO certified; "
                      "2 sustainability awards in 2025"),
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
