"""Add the two batch-21 leads to the ads-only builder, 2026-11-15.

Both were rowed in leads.csv earlier the same day and both had every ad ID
opened individually before anything was written down:

  Eagle Solar Systems  1677382683817329 (Nov 7 2026), 1835997698149286 (Nov 12 2026)
  Solar Apex Pvt Ltd   1143855195267637 (Nov 4 2026, brand - in segment),
                       1667563528489384 (Nov 4 2026, dealership recruitment)

Eagle has no website of its own, so it uses the no_website path added to
validate() and audit_pdf.py in this same change. Without that path the builder
refused to build a report for a firm with no site, which would have hidden the
single strongest finding we have about Eagle.

Solar Apex carries its brand ad in `ads` and records the recruitment ad in the
findings and in the note below, on the same reasoning that rejected Servotech
and Go Rewatt: the row stands on the in-segment creative, and the out-of-segment
one is disclosed rather than counted.

  python3 add_batch21_ads_only.py            # dry run
  python3 add_batch21_ads_only.py --write
"""

import io
import sys

PATH = 'ads_only_report.py'

ENTRIES = '''
    {
        "company": "Eagle Solar Systems",
        "legal": "Eagle Solar Systems (proprietorship)",
        "city": "Mallampet, Bachupally, Medchal, Hyderabad",
        "website": "",
        "no_website": True,
        "no_website_note": (
            "Eagle Solar Systems publishes no website of its own - no domain, no "
            "landing page, nothing. Both of its live Meta ads end in a Facebook "
            "lead form, so every rupee of spend lands inside Facebook and there "
            "is no page anywhere that a searcher, a referral or a shared link "
            "could land on. The email address eaglesolarhyd@gmail.com and the "
            "phone numbers are published in the Telangana government's TGREDCO "
            "2026 empanelled-supplier register, not on a site of the firm's own."),
        "email": "eaglesolarhyd@gmail.com",
        "phone": "+91 9000666985 / +91 9000666984",
        "fb_page": "https://www.facebook.com/61595903925834/",
        "checked_on": "2026-11-15",
        "ad_library": {
            "meta_own": {
                "found": True,
                "results_count": 2,
                "results_label": "2 ads on the page",
                "query": "Eagle Solar Systems",
                "ads": [
                    ad("1677382683817329", "Eagle Solar Systems", "Nov 7, 2026",
                       "Facebook lead form (fb.me 'Book now')",
                       "నెలనెలా వేల రూపాయలు కరెంట్ బిల్లులకే ఖర్చు చేస్తున్నారా? "
                       "మీ కష్టార్జిత డబ్బును కరెంట్ బిల్లుల కోసం ఖర్చు చేయడం ఆపండి! "
                       "ఇప్పుడు మీ ఇంటిపై సోలార్ ప్యానెల్స్ ఏర్పాటు చేసుకొని విద్యుత్ "
                       "ఖర్చుల నుంచి ఉపశమనం పొందండి. ఇంటికి రూఫ్‌టాప్ సోలార్ "
                       "ఇన్‌స్టాలేషన్; అర్హత ఉన్న వారికి ₹78,000 వరకు ప్రభుత్వ సబ్సిడీ; "
                       "కరెంట్ బిల్లులో 90% వరకు ఆదా చేసే అవకాశం; PM సూర్య ఘర్ ముఫ్త్ "
                       "బిజిలీ యోజన ప్రయోజనాలు. కాల్ చేయండి 9000666985 / 9000666984. "
                       "హైదరాబాద్ & తెలంగాణ అంతటా సేవలు.", ad_count=2),
                    ad("1835997698149286", "Eagle Solar Systems", "Nov 12, 2026",
                       "Facebook lead form (fb.me 'Book now')",
                       "మీ ఇంటి కరెంట్ బిల్లులు తగ్గించుకోవాలనుకుంటున్నారా? ఇప్పుడే మీ "
                       "ఇంటిపై సోలార్ ప్యానెల్స్ ఏర్పాటు చేసుకోండి. ప్రభుత్వ సబ్సిడీ "
                       "₹78,000 వరకు పొందే అవకాశం ఉంది! నెలవారీ విద్యుత్ ఖర్చులను "
                       "తగ్గించుకోండి. నాణ్యమైన సోలార్ ప్యానెల్స్, ప్రొఫెషనల్ "
                       "ఇన్‌స్టాలేషన్, ప్రభుత్వ సబ్సిడీ సహాయం.", ad_count=2),
                ],
            },
            "summary": (
                "Eagle Solar Systems is running 2 active Meta ads on its own page "
                "(facebook.com/61595903925834), started 7 and 12 November 2026 - five "
                "days apart, so this is an account being actively added to rather than "
                "one creative left running. Both ads are in Telugu and both lead on the "
                "same three things: the PM Surya Ghar subsidy of up to Rs.78,000, up to "
                "90% off the electricity bill, and a service area covering Hyderabad and "
                "all of Telangana. Both CTAs are Facebook lead forms, so no click ever "
                "leaves Facebook - and there is no website for a click to reach. Google "
                "Ads Transparency cannot be probed for this firm because it owns no "
                "domain, so Meta is the entire paid channel by necessity rather than by "
                "choice."),
        },
        "funnel": {
            "type": "Facebook lead form",
            "destination": "fb.me 'Book now' - inside Facebook",
            "meaning": (
                "Every click becomes a form submission inside Facebook. That is workable "
                "for collecting a phone number, but it is the only option available here: "
                "with no website there is no page to install a pixel on, no audience to "
                "retarget, nothing to A/B test a headline on, and nowhere for a referral "
                "or a WhatsApp share to land."),
        },
        "findings": [
            "There is no website at all. Both ads end in a Facebook lead form, so the "
            "firm has no page a customer can visit, share or return to - the entire "
            "digital presence is two ads and a lead form.",
            "Two ads, five days apart (7 and 12 Nov 2026), carrying the same three "
            "claims. The account is live and being added to, which is the right "
            "instinct - but both creatives point at the same dead end.",
            "The copy is specific where it counts: the Rs.78,000 PM Surya Ghar subsidy "
            "figure, the 90% bill-saving claim and an explicit Hyderabad-and-Telangana "
            "service area. The offer is clear; the place to act on it is not.",
            "The contact details are published only in the state's TGREDCO 2026 "
            "empanelled-supplier register (regn. TSRE240360) - eaglesolarhyd@gmail.com "
            "and mobile 9000666985, which is the same number the ads print. Nothing "
            "about the firm is published anywhere it controls.",
            "A Justdial listing and an IndiaMART page exist for the same Mallampet / "
            "Bachupally business, and both are directories rather than a home. The "
            "IndiaMART page describes a proprietorship est. 2013 trading in solar water "
            "heaters, solar fencing and street lights alongside interior designing, "
            "false ceiling and modular kitchen - a small firm with a wider trade than "
            "rooftop solar.",
        ],
        "next_steps": [
            ("Get one page that answers the ad",
             "A single page with the offer, the subsidy explainer, the service area and "
             "an enquiry form. Right now the ad asks for a phone number and gives the "
             "customer nothing to check beforehand."),
            ("Own the audience the lead form creates",
             "A Meta Pixel on that page plus the Conversions API turns the people who "
             "clicked and did not submit into a retargetable audience - the cheapest "
             "inventory a solar installer has."),
            ("Publish the proof the register already holds",
             "TGREDCO empanelment TSRE240360, the Mallampet address and a real phone "
             "number belong on a page the firm controls. Right now a customer who wants "
             "to check the company has to find a government PDF."),
            ("Give the subsidy its own page",
             "Rs.78,000 under PM Surya Ghar is the strongest line in both ads. A page "
             "explaining eligibility, paperwork and timeline is the single highest-value "
             "thing this firm could put online."),
        ],
        "contact_facts": [
            ("Email", "eaglesolarhyd@gmail.com - published in the TGREDCO 2026 "
                      "empanelled-supplier register, regn. TSRE240360"),
            ("Phone", "9000666985 / 9000666984 (both printed in the live ads; the "
                      "register lists 9000666985)"),
            ("Address", "SY.No.142/A/1, Mallampet, Bachupally, Maheshwaram, Medchal, "
                        "Hyderabad 500072 (per the TGREDCO register)"),
            ("Website", "None published. No domain, no landing page."),
            ("Entity", "Eagle Solar Systems - proprietorship, per the IndiaMART listing "
                       "established 2013 in the name of RAMA KRISHNAIAH KUMBAM"),
            ("Meta page", "facebook.com/61595903925834 (Eagle Solar Systems)"),
        ],
        "site_evidence": {
            "pixel": None,
            "utm": None,
            "checked_on": "2026-11-15",
            "note": ("There is no website to source-check, so Meta Pixel presence is "
                     "not merely unverified - there is nowhere for a pixel to live. "
                     "Both ads terminate in Facebook lead forms, so no ad click can "
                     "reach any page the firm owns."),
        },
    },
    {
        "company": "Solar Apex Pvt Ltd",
        "legal": "Solar Apex Pvt Ltd",
        "city": "Manikonda, Hyderabad",
        "website": "https://www.solarapex.in/",
        "email": "info@solarapex.in",
        "phone": "+91 96660 05198",
        "fb_page": "https://www.facebook.com/61596329420215/",
        "checked_on": "2026-11-15",
        "ad_library": {
            "meta_own": {
                "found": True,
                "results_count": 2,
                "results_label": "2 ads on the page",
                "query": "Solar Apex",
                "ads": [
                    ad("1143855195267637", "Solar Apex Khammam", "Nov 4, 2026",
                       "WhatsApp (api.whatsapp.com 'Send WhatsApp message')",
                       "Call Us: 8125640121, 8008576480. Visit Us: Church Compound "
                       "Center, Khammam. www.solarapex.in. "
                       "#solar #khammam #telangana #savemoney #government", ad_count=2),
                    ad("1667563528489384", "Solar Apex Khammam", "Nov 4, 2026",
                       "WhatsApp (api.whatsapp.com)",
                       "ఖమ్మం lo Solar Dealership teesukoni mee own business start "
                       "cheyyalanukuntunnara? ... Solar Apex tho mee business journey "
                       "ni start cheyyandi! ఖమ్మం lo maa solar dealerships teesukunna "
                       "vallu nelaku ₹50,000 nunchi ₹1 lakh plus varaku sampadinche "
                       "avakasalatho munduku velthunnaru. ... Meeru kothaga business "
                       "start cheyyalanukuntunnara? Leka already meeku oka business "
                       "undha? Mee existing business lo solar services ni kuda include "
                       "cheskovachu!", ad_count=2),
                ],
            },
            "summary": (
                "Solar Apex is running 2 active Meta ads on its Khammam franchise page "
                "(facebook.com/61596329420215), both started 4 November 2026. One is a "
                "brand ad - phone numbers, the Khammam address and www.solarapex.in - "
                "which is in segment for a rooftop-solar installer. The other recruits "
                "dealerships, promising Khammam dealers Rs.50,000 to Rs.1 lakh plus a "
                "month; that is a different audience and is excluded from the ad count "
                "used for this report. Both CTAs go to WhatsApp. A third ad the batch-14 "
                "run recorded, a hiring ad on the corporate page "
                "facebook.com/61575888183929, is no longer in the Ad Library. Google Ads "
                "Transparency for solarapex.in returns 0 ads under region=IN, so Meta is "
                "the entire paid channel."),
        },
        "funnel": {
            "type": "WhatsApp",
            "destination": "api.whatsapp.com behind 'Send WhatsApp message'",
            "meaning": (
                "Both ads open a WhatsApp conversation, and the brand ad prints "
                "www.solarapex.in as text without linking to it - so the site exists "
                "but is not part of the paid path. Nothing is measurable: no pixel "
                "firing, no conversion event, no retargeting pool, and no page where a "
                "different headline or price could be tested."),
        },
        "findings": [
            "The brand ad prints www.solarapex.in as plain text and then sends the "
            "click to WhatsApp. The site is never in the paid path, so none of the "
            "spend can be measured against it.",
            "The second live ad recruits dealerships, not customers - it promises "
            "Khammam dealers Rs.50,000 to Rs.1 lakh plus a month. Two different "
            "audiences are competing inside one ad account, and the recruitment ad is "
            "excluded from the count in this report.",
            "The homepage's mailto link is broken and points at info@domain.com. Only "
            "the /contact/ page publishes a working address, info@solarapex.in - so an "
            "enquiry sent from the homepage silently goes nowhere.",
            "The ad phone numbers (8125640121, 8008576480) do not match the website "
            "phone (+91 96660 05198). Two numbers in market, one on the site, and no "
            "way for a customer to tell which is current.",
            "The registered address is Manikonda, Hyderabad 500089, while the "
            "advertising page is the Khammam outlet (Church Compound Center). Both are "
            "inside Telangana, but the corporate site and the local page are run as "
            "separate things.",
            "Zero Google ads under region=IN for solarapex.in, so the whole paid "
            "presence is these two Meta ads on one franchise page.",
        ],
        "next_steps": [
            ("Put the site in the paid path",
             "Send the brand ad to a real page on solarapex.in - offer, subsidy "
             "explainer, enquiry form - so the click is measurable and retargetable "
             "instead of ending in a chat."),
            ("Split the two audiences",
             "Customer acquisition and dealership recruitment are different buyers with "
             "different economics. Separate campaigns, or at minimum separate ads with "
             "separate objectives, so neither dilutes the other."),
            ("Fix the broken mailto",
             "The homepage email link points at info@domain.com. One line of HTML, and "
             "it is currently losing every enquiry that trusts the link over the phone "
             "number."),
            ("Reconcile the phone numbers",
             "Publish one number that answers, and route the ad numbers to it. Two "
             "unmatched numbers in market reads as a company that is hard to reach."),
        ],
        "contact_facts": [
            ("Email", "info@solarapex.in - published on solarapex.in/contact/ (the "
                      "homepage mailto is broken and points at info@domain.com)"),
            ("Phone / WhatsApp", "+91 96660 05198 / wa.me/919666005198 on the site; "
                                 "8125640121 and 8008576480 in the ads"),
            ("Address", "3rd floor, Kakatiya Marvel, near Lanco Hills Road, Sri Laxmi "
                        "Nagar Colony, Manikonda, Hyderabad, Telangana 500089"),
            ("Franchise address", "Church Compound Center, Khammam - the address the "
                                  "live ads print"),
            ("Services", "Residential, commercial, industrial, apartments, street "
                         "lights, water heaters and open-access solar"),
            ("Meta pages", "facebook.com/61596329420215 (Solar Apex Khammam, the "
                           "advertiser) and facebook.com/61575888183929 (Solar Apex "
                           "Pvt Ltd, corporate)"),
        ],
        "site_evidence": {
            "pixel": None,
            "utm": None,
            "checked_on": "2026-11-15",
            "note": ("Homepage and /contact/ page read live on 2026-11-15 through a "
                     "text-only fetch, so page source was not pulled and Meta Pixel "
                     "presence is unverified either way; graded unknown per the "
                     "catalog's runtime contract. Neither live ad links to the site."),
        },
    },
'''


def main():
    write = '--write' in sys.argv
    s = io.open(PATH, encoding='utf-8').read()
    if '"Eagle Solar Systems"' in s or '"Solar Apex Pvt Ltd"' in s:
        print('one of these leads is already in the builder - nothing to do')
        return
    anchor = '        "company": "PNR Sunrise Energies Pvt Ltd",'
    i = s.index(anchor)
    j = s.index('\n]\n', i)
    assert s[j:j + 3] == '\n]\n', repr(s[j:j + 10])
    out = s[:j] + '\n' + ENTRIES.rstrip('\n') + s[j:]
    if write:
        io.open(PATH, 'w', encoding='utf-8').write(out)
        print('appended 2 entries; file now %d bytes (was %d)' % (len(out), len(s)))
    else:
        print('dry run: would append 2 entries (%d bytes)' % len(ENTRIES))


if __name__ == '__main__':
    main()
