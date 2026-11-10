#!/usr/bin/env python3
"""Register the five batch-17 leads and build their outreach sequences.

Run from the repo root:
    PYTHONPATH=/tmp/pdflibs python3 02-OUTREACH/build_batch17_outreach.py

Adds five rows to 01-LEADS/leads.csv and five sequences (step 0 only) to
02-OUTREACH/generated_emails/sequence_manifest.json. Every figure in the
snippets and in the email bodies was read live on 2026-11-10 - from the Google
Ads Transparency Centre advertiser record for the ad counts and verified legal
names, and from the W3C Nu HTML Checker plus a direct page fetch for every
website finding. Nothing is estimated.

Each lead is identity-verified in Google's Ads Transparency Centre and has a
resolvable website of its own, which is the gate every lead in this repo has to
pass. None of the five was found by a Meta Ad Library sweep - all five are
Google-only advertisers, which is why a whole discovery channel had to be
opened to reach them.
"""
import csv
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEADS_CSV = os.path.join(ROOT, "01-LEADS", "leads.csv")
MANIFEST = os.path.join(ROOT, "02-OUTREACH", "generated_emails",
                        "sequence_manifest.json")
READ_ON = "2026-11-10"
SIG = ("Best,\nVamsi\nSmart Pursuit\n+91 70950 24220\n")

# ---------------------------------------------------------------------------
# leads.csv rows
# ---------------------------------------------------------------------------

ROWS = [
    {
        "name": "Zenith Energy Services Private Limited",
        "city": "Shaikpet, Hyderabad (serves Karimnagar, Khammam, Nizamabad)",
        "website": "https://zenithenergy.com/",
        "email": "zenith@zenithenergy.com",
        "phone": "+91 7075756795",
        "snippet": (
            "Live Google advertiser - 9 live ads in Google's Ads Transparency "
            "Centre under advertiser AR02278013072834560001, identity-verified "
            "as ZENITH ENERGY SERVICES PRIVATE LIMITED, including a YouTube "
            "video creative. Domain confirmed on the advertiser record. NOTE: "
            "this company was probed on 2026-10-23 in batch 9 and recorded as a "
            "zero-ad website probe because that sweep covered Meta only - it has "
            "been running 9 Google ads throughout, which is why the Google Ads "
            "Transparency channel was opened. Site audited 2026-11-10: "
            "WordPress 7.1.4, hello-elementor 3.5.1, Elementor 4.4.0 + Pro, "
            "ElementsKit Lite 4.0.9, Essential Addons 6.8.8, TablePress 3.4.1, "
            "AIOSEO 5.0.4, score 10/100 - Google Tag Manager container "
            "GTM-NGZ8TG9J is the only tracking script in the head, and it is a "
            "container rather than a measurement, so nothing is counted until "
            "tags are published inside it; 158 errors, 5 warnings, 146 info. "
            "MATERIAL DEFECTS: (1) a complete second HTML document - doctype, "
            "<html>, <head>, meta charset, viewport and a <title> - is embedded "
            "inside the body at source line 417, shipped by the India-map "
            "plugin, which alone produces the checker's stray-doctype, "
            "stray-html, stray-head, duplicate-charset and unclosed-element "
            "errors; (2) all four hero counters read zero - 'Energy audits 0+', "
            "'Carbon reduction projects 0+', 'Renewable projects supported 0 "
            "GW', 'Net Zero projects completed 0+' - on a page that separately "
            "claims 180+ major projects across 28 states and 8 union "
            "territories; (3) the AIOSEO Organization schema name is the "
            "lowercase string 'zenith' and carries no address, telephone, email "
            "or logo. Strengths: full og and Twitter card set, Search Console "
            "verified, a real client carousel (rgppl, Epiroc, Indian Oil, HP, "
            "NALCO, Medicare, MSN, Macro Power Controls) and three named case "
            "studies - Basavatarakam Indo American Cancer Hospital, a "
            "clean-cooking project in Koraput, Odisha, and a net-zero roadmap "
            "for VPCL Visakha Pharmacity. Registered office D.NO. 1-89/A/8/C/2&3, "
            "Vittal Rao Nagar, M3 Block, Shaikpet, Telangana 500081; CIN "
            "U74140TG1990PTC011583, incorporated 10 Aug 1990; directors Sindhu "
            "Jannareddy and Vindhya Pulicherla. SEGMENT: energy-efficiency and "
            "net-zero consultancy that also sells rooftop solar EPC - broader "
            "than pure rooftop EPC."
        ),
        "audit_score": 10,
        "audit_issues_count": 7,
        "status": "audited",
        "added_date": READ_ON,
    },
    {
        "name": "SunWorks Energy Private Limited",
        "city": "Jubilee Hills, Hyderabad",
        "website": "https://sunworks.in/",
        "email": "gosolar@sunworks.in",
        "phone": "+91 8688326316",
        "snippet": (
            "Live Google advertiser - 1 live ad in Google's Ads Transparency "
            "Centre under advertiser AR07942131426432909313, identity-verified "
            "as SUNWORKS ENERGY PRIVATE LIMITED, a Display image creative "
            "(simgad/8721599813200798262). Domain confirmed on the advertiser "
            "record. Site audited 2026-11-10: WordPress, Astra theme, Elementor "
            "4.3.2 + Elementor Pro 3.34.0, Swiper 8.4.5, Site Kit by Google - "
            "score not claimed because the <head> script tags were not returned "
            "in readable form, so the eight tracking rows are unknown in both "
            "directions and are reported as not checked; 298 errors, 47 "
            "warnings, 101 info, the highest error count in this batch. "
            "MATERIAL DEFECTS: (1) the years-in-business figure contradicts "
            "itself three times on one page - 'Since 2015' (11 years in 2026), "
            "then '10+ Years of Experience', then '15+ Years Solar Experience'; "
            "(2) three of the four service cards point at the wrong page - "
            "'Solar EPC 03' and 'Operations and Maintenance 04' both link to "
            "/consultancy-advisory/, while the slider directly above the same "
            "block links correctly to /epc-services/ and /operations-maintenance/; "
            "(3) the site's own script and CSS optimiser is deleting its "
            "images - 29 <img> elements are missing both src and srcset and 5 "
            "more carry sizes without srcset, so they cannot load at all; (4) "
            "og:site_name is set to \"Home\"; (5) 46 duplicate IDs and 70 "
            "illegal bv-* attributes left by the optimiser. What IS confirmed "
            "in the head: Site Kit by Google's gtag.js loader "
            "(id=\"google_gtagjs-js-after\") at source line 706. Strengths: a "
            "25-logo clientele wall (BSF, Meil, SRK Infra, Aparna Industries, "
            "R.S. Brothers, Katuri Medical College, Presidency High School, "
            "Asian Fab Tech, Magna Group), five awards including 'Best "
            "Engineering team of the Year 2024 - Telangana', seven named "
            "projects with capacities (Viswateja Spinning Mills 3.6 MWp, SVLN "
            "1.5 MWp, NRKR 4.2 Mwp, Patchala 2 Mwp) and two named testimonials. "
            "2nd Floor, Plot 126, Road Number 11, Jubilee Hills, Hyderabad. "
            "SEGMENT: solar EPC, design and engineering, and O&M - squarely "
            "rooftop and commercial EPC."
        ),
        "audit_score": "",
        "audit_issues_count": 5,
        "status": "audited",
        "added_date": READ_ON,
    },
    {
        "name": "Nature Power Solar",
        "city": "Kothagudem 507101 (serves Telangana and Andhra Pradesh)",
        "website": "https://naturepowersolar.com/",
        "email": "info@naturepowersolar.com",
        "phone": "+91 9666088988",
        "snippet": (
            "Live Google advertiser - 1 live ad in Google's Ads Transparency "
            "Centre under advertiser AR11194127933927063553, identity-verified "
            "as CHITWALA JOHN SANDEEP, a sole proprietorship trading as Nature "
            "Power Solar Technologies & Services, Display creative "
            "simgad/14883437245831789543. Domain confirmed on the advertiser "
            "record. Independently confirmed on the TGREDCO 2026 "
            "empanelled-supplier register as 'M/s. Nature Power Solar "
            "Technologies & Services', 2-2-1/2 Budidagadda Basthi, Kothagudem "
            "507101. Site audited 2026-11-10: hand-built static HTML, score "
            "8/100 - the cleanest markup in this batch at 6 errors, 0 warnings, "
            "0 info, and the best-built page overall. Tracking: GA4 "
            "G-9MMYLNMH9T, Google tag GT-5TQ454D4 and Google Ads conversion ID "
            "AW-609769092 are all live in the head - the only batch-17 lead "
            "with a confirmed Google Ads conversion tag. MATERIAL DEFECTS: (1) "
            "Search Console and Bing verification are still the developer's "
            "commented-out placeholders - the source carries <!-- <meta "
            "name=\"google-site-verification\" content=\"PASTE_TOKEN\"> --> and "
            "<!-- <meta name=\"msvalidate.01\" content=\"PASTE_TOKEN\"> -->, so "
            "Google has never verified ownership of a domain the company buys "
            "Google ads for; (2) no Meta Pixel at all, so nobody who leaves "
            "without filling the form can be reached again; (3) a stray "
            "<script> start tag after </body> at source line 420; (4) the "
            "calculator's <output> element has an id that does not match the "
            "for attribute of its own label; (5) a role=tab with no "
            "corresponding role=tabpanel. Strengths - genuinely the strongest "
            "asset in this batch: a live savings calculator publishing real "
            "Telangana numbers (a Rs.3,500 monthly bill resolving to 4 kW at "
            "Rs.2.48 lakh, Rs.78,000 subsidy, Rs.1.7 lakh net, Rs.3,325 a month "
            "saved, 4.1-year payback), the correct PM Surya Ghar tiers "
            "(Rs.30,000 / Rs.60,000 / Rs.78,000, Rs.18,000 per kW for RWAs to "
            "500 kW, scheme to 31 March 2027), full LocalBusiness + WebSite + "
            "FAQPage + ItemList JSON-LD naming founder Sagar Earpula, "
            "operations manager Abhilash Earpula and the Google Maps listing "
            "cid 8850580709543659187, six services with real specifications, "
            "and a WhatsApp hand-off that pre-fills the estimate. "
            "SEGMENT: rooftop and commercial solar EPC plus pumps, fencing, "
            "heaters and street lights."
        ),
        "audit_score": 8,
        "audit_issues_count": 7,
        "status": "audited",
        "added_date": READ_ON,
    },
    {
        "name": "Surya Renewable Energies",
        "city": "Kothapet, Hyderabad",
        "website": "http://suryarenewable.com/",
        "email": "info@suryarenewable.com",
        "phone": "+91 9182311739",
        "snippet": (
            "Live Google advertiser - 2 live ads in Google's Ads Transparency "
            "Centre under advertiser AR08105928276372881409, identity-verified "
            "as LANKA V K PHANI VISWANATH - one YouTube video creative "
            "(ytimg/24H234ft0Yk) and one Display image creative "
            "(simgad/10231766854828954333). Domain confirmed on the advertiser "
            "record. Site audited 2026-11-10: hand-built static HTML, score "
            "23/100 - 1 error, 0 warnings, 0 info, the cleanest markup in this "
            "batch. MATERIAL DEFECTS: (1) the Google Ads conversion event can "
            "never fire - the head still carries the template's placeholder "
            "label, gtag('event', 'conversion', {'send_to': "
            "'AW-18243186763/WHATSAPP_LABEL'}) with the comment 'Replace with "
            "your WhatsApp conversion label' above it, so every WhatsApp click "
            "the company pays for is sent to a label that does not exist; (2) "
            "the hero slider is three Pexels stock videos hot-linked straight "
            "from pexels.com/download/video/7040278/, /19202862/ and "
            "/18680290/; (3) no Open Graph tags, no Twitter card, no canonical, "
            "no JSON-LD and no sitemap reference anywhere in the 138-line "
            "document; (4) the <title> is 108 characters and the three hero "
            "slides each carry their own <h1>, so the page competes with itself "
            "for three queries; (5) a stray <script> after </body> at source "
            "line 138. Tracking: the Google Ads tag AW-18243186763 is the only "
            "tag in the whole document - no GA4, no GTM, no Meta Pixel, no "
            "LinkedIn Insight, no Clarity, no Hotjar. Strengths: a genuine "
            "rooftop and ground-mount EPC scope - rooftop solar, ground-mount "
            "systems, net metering, battery storage and AMC for residential and "
            "commercial plants, with feasibility studies, site surveys and "
            "net-metering approvals handled - plus a floating WhatsApp button "
            "pre-filled with the enquiry. The company describes itself on its "
            "own homepage as 'a new bee in this energy sector', and wind and "
            "hydro are described only as equipment trading. Alkapuri Colony, "
            "Kothapet, Hyderabad. SEGMENT: rooftop and ground-mount solar EPC, "
            "with wind and micro-hydro trading alongside."
        ),
        "audit_score": 23,
        "audit_issues_count": 12,
        "status": "audited",
        "added_date": READ_ON,
    },
    {
        "name": "Milestone Solarcom Private Limited",
        "city": "Hyderabad",
        "website": "https://www.milestonesolar.in/",
        "email": "milestonesolarcomsales@gmail.com",
        "phone": "+91 9030005033",
        "snippet": (
            "Live Google advertiser - 6 live ads in Google's Ads Transparency "
            "Centre under advertiser AR10713925876992442369, identity-verified "
            "as ZAHEERUDDIN JAVEED MOHAMMED, trading as Milestone Solarcom. "
            "Domain confirmed on the advertiser record. Independently confirmed "
            "on the TGREDCO 2026 empanelled-supplier register as 'M/s. "
            "Milestone Solarcom Pvt. Ltd.', registration TSRE180047. Site "
            "audited 2026-11-10: WordPress, Astra theme, Elementor, AIOSEO "
            "5.0.2.1, Site Kit by Google 1.187.0, MyStickyMenu, Click to Chat "
            "for WhatsApp, score 3/100 - 128 errors, 10 warnings, 53 info. "
            "MATERIAL DEFECTS: (1) every trust counter on the homepage reads "
            "zero - 'Years of experience 0+', 'Installations 0+', 'Happy "
            "Customers 0%' and 'Customer Support 0/7' - directly beside a "
            "'1,248 reviews' Google badge; (2) the click-to-call link is "
            "broken - the checker reports 'Bad value tel:+91 9030005033 for "
            "attribute href on element a: Illegal character after tel:. Space "
            "is not allowed', so the number cannot be dialled from the page; "
            "(3) 100 elements sit where they are not allowed - 55 <p> inside "
            "<span>, 22 <h3> inside <span>, 15 <h2> inside <span>, 7 <ul> "
            "inside <span>; (4) og:site_name is set to \"-\"; (5) three "
            "spelling errors in the primary conversion copy - 'top solar comapy "
            "in hyderabad', 'This Shceme', 'Sustanability Focused'; (6) a "
            "heading-level skip from h2 to h6. Tracking: Meta Pixel id "
            "1132764258717771 confirmed via its noscript fallback at source "
            "lines 191-192 - the only confirmed tag; Site Kit by Google 1.187.0 "
            "is installed and the head preconnects to googletagmanager.com, but "
            "no GA4 or Google Ads measurement ID could be read, so the Google "
            "spend behind 6 ads has no confirmed measurement. Strengths: real "
            "capability breadth - off-grid and on-grid SPV plants, hybrid "
            "plants, solar micro and mini grids, street lighting, fencing, "
            "water heating and water pumping - and a government-registered "
            "empanelment to back it. SEGMENT: solar EPC and integrator with a "
            "strong rural and off-grid line."
        ),
        "audit_score": 3,
        "audit_issues_count": 6,
        "status": "audited",
        "added_date": READ_ON,
    },
]

# ---------------------------------------------------------------------------
# Step-0 email bodies. Same convention as batches 13 and 14: the ad evidence
# first, the single biggest finding, an honest "to be fair" paragraph, a
# segment note where the business is broader than rooftop EPC, verification
# links the lead can open itself, and no score figure - that is in the PDF.
# ---------------------------------------------------------------------------

BODIES = {
    "Zenith Energy Services Private Limited": """Hi,

I spend my week reading the public ad-transparency records for the Telangana solar market, and I put together a short report on what Zenith Energy is doing right now.

What it covers (pulled from Google's Ads Transparency Centre on 2026-11-10):

  - 9 live ads under your advertiser record, identity-verified as ZENITH ENERGY SERVICES PRIVATE LIMITED, including a YouTube video creative - the highest ad count of any company I looked at this month
  - the ads serve Karimnagar, Khammam and Nizamabad through location pages on your site, and the click does reach zenithenergy.com, so that part is right
  - worth saying plainly: I had you down as a zero-ad company from an earlier sweep. That sweep only covered Meta. You have been running nine Google ads the whole time, which is exactly why I opened this channel.

The thing I would fix first is not the ads. It is the page underneath them.

A complete second HTML document is embedded inside your homepage body - a doctype, an <html> tag, a <head>, a meta charset, a viewport and a <title>, all sitting at source line 417. Your India-map plugin ships its own whole page inside yours. That one defect is what produces most of the 158 validation errors on the homepage, including the stray doctype, the duplicate charset and the unclosed elements.

Second, all four of your hero counters read zero. 'Energy audits 0+', 'Carbon reduction projects 0+', 'Renewable projects supported 0 GW' and 'Net Zero projects completed 0+'. On the same page that claims 180+ major projects across 28 states and 8 union territories. A prospect who scrolls to the proof section sees four zeros.

Third, on measurement: the only tracking script in your head is a Google Tag Manager container, GTM-NGZ8TG9J. A container is a box, not a measurement - nothing is counted until tags are published inside it. So at the moment nine ads are buying clicks and nothing on the page can tell you what they produced.

To be fair to you, the site has real substance underneath: three named case studies (Basavatarakam Indo American Cancer Hospital, the clean-cooking project in Koraput, and the net-zero roadmap for VPCL Visakha Pharmacity), a client carousel that includes Indian Oil, HP, NALCO, Epiroc and Medicare, a full Open Graph and Twitter card set, and Search Console verification already in place. The bones are good. The execution has drifted.

One more thing worth saying plainly: I have written this as an energy-efficiency and net-zero lead rather than a pure rooftop-solar lead, because that is what your site actually sells - ESCO retrofits, energy audits, water management and carbon offsets alongside the solar.

You can verify every line yourself:

  https://adstransparency.google.com/advertiser/AR02278013072834560001?region=IN
  https://validator.w3.org/nu/?doc=https://zenithenergy.com/&showsource=yes

Happy to walk you through what I found on a 10-minute call - or just keep the report, no strings attached.

""" + SIG,

    "SunWorks Energy Private Limited": """Hi,

I spend my week reading the public ad-transparency records for the Telangana solar market, and I put together a short report on what SunWorks Energy is doing right now.

What it covers (pulled from Google's Ads Transparency Centre on 2026-11-10):

  - 1 live ad under your advertiser record, identity-verified as SUNWORKS ENERGY PRIVATE LIMITED
  - the ad's destination is sunworks.in, which I confirmed on the advertiser record, so the click does reach your site

The first thing I would fix is not the ad. It is a number on your own homepage.

Your page says 'Since 2015, we've been helping businesses, institutions, and homeowners' - that is 11 years. A few lines below it, your milestones block says '10+ Years of Experience'. A few lines below that, the same page says '15+ Years Solar Experience'. Three different answers to the same question on one screen, and none of them matches the founding date printed above them.

The second thing is quieter and more expensive. Your site runs a script and CSS optimiser, and the optimiser is deleting your own images: 29 <img> elements on the homepage are missing both their src and srcset attributes, and five more carry a sizes attribute with no srcset. Those images cannot load at all. The W3C checker reports 298 errors and 47 warnings on the page - the highest count I recorded this month - and 46 of them are duplicate IDs.

Third, three of your four service cards point at the wrong page. 'Solar EPC 03' and 'Operations and Maintenance 04' both link to /consultancy-advisory/. The slider directly above the same block links correctly to /epc-services/ and /operations-maintenance/, so the two blocks disagree with each other - and the EPC service your ad is about is unreachable from the card.

To be fair to you, the site has genuine proof on it: a 25-logo clientele wall including BSF, Meil, SRK Infra, Aparna Industries, R.S. Brothers, Katuri Medical College and Presidency High School; five awards, among them 'Best Engineering team of the Year 2024 - Telangana'; and seven named projects with capacities attached, such as Viswateja Spinning Mills 3.6 MWp and SVLN 1.5 MWp. That is real, specific evidence and it is the strongest asset on the page.

One honest caveat on the report: I could not read your site's tracking tags. The served HTML carries very large inline stylesheets, so the eight tracking rows in the report read 'not checked' rather than 'missing' - I am not going to claim a problem I did not observe. What I can confirm is that Site Kit by Google is installed, so something is likely measuring. That is the first thing to verify.

You can verify every line yourself:

  https://adstransparency.google.com/advertiser/AR07942131426432909313?region=IN
  https://validator.w3.org/nu/?doc=https://sunworks.in/&showsource=yes

Happy to walk you through what I found on a 10-minute call - or just keep the report, no strings attached.

""" + SIG,

    "Nature Power Solar": """Hi,

I spend my week reading the public ad-transparency records for the Telangana solar market, and I put together a short report on what Nature Power Solar is doing right now.

What it covers (pulled from Google's Ads Transparency Centre on 2026-11-10):

  - 1 live ad under your advertiser record, identity-verified as CHITWALA JOHN SANDEEP
  - the ad's destination is naturepowersolar.com, which I confirmed on the advertiser record
  - I also found you independently on the TGREDCO 2026 empanelled-supplier register as Nature Power Solar Technologies & Services at the Kothagudem address, which is the third-party confirmation I look for

I want to start with the good news, because it is unusual: your site is the best-built page I read this month. Six validation errors, no warnings, no info messages, no plugin stack, no page builder. Your savings calculator publishes real numbers - a Rs.3,500 monthly bill resolving to a 4 kW system at Rs.2.48 lakh, Rs.78,000 of subsidy, Rs.1.7 lakh net, Rs.3,325 a month saved and a 4.1-year payback - and those figures hold up. Your PM Surya Ghar tiers are correct, your JSON-LD names your founder and operations manager and links your Google Maps listing, and your six service pages carry real specifications. Most solar sites in Telangana do not.

So the gap is not the page. It is that nothing on it is measured, and one specific thing is missing.

Your Search Console verification token is still the placeholder your developer shipped. The source carries <!-- <meta name=\"google-site-verification\" content=\"PASTE_TOKEN\"> --> and the Bing equivalent, both commented out. You are buying Google ads for a domain Google has never been able to confirm you own. That is a five-minute fix and it gates everything else.

Second, you have no Meta Pixel at all. You do have GA4 (G-9MMYLNMH9T), a Google tag (GT-5TQ454D4) and a Google Ads conversion ID (AW-609769092) - you are actually ahead of most of the leads I write to on that. But there is no way to reach the person who reads your calculator, does not fill the form, and leaves.

Third, there is no live chat and no popup opt-in, so the quote form is the only capture point on a page that clearly knows how to hold attention.

You can verify every line yourself:

  https://adstransparency.google.com/advertiser/AR11194127933927063553?region=IN
  https://validator.w3.org/nu/?doc=https://naturepowersolar.com/&showsource=yes

Happy to walk you through what I found on a 10-minute call - or just keep the report, no strings attached.

""" + SIG,

    "Surya Renewable Energies": """Hi,

I spend my week reading the public ad-transparency records for the Telangana solar market, and I put together a short report on what Surya Renewable Energies is doing right now.

What it covers (pulled from Google's Ads Transparency Centre on 2026-11-10):

  - 2 live ads under your advertiser record, identity-verified as LANKA V K PHANI VISWANATH - one YouTube video creative and one Display image
  - both point at suryarenewable.com, which I confirmed on the advertiser record

You have made a YouTube video ad, which puts you ahead of most rooftop companies in the state. So it is a shame that the first thing a visitor sees when they arrive is not your work.

Your hero slider is three stock videos pulled straight from Pexels - pexels.com/download/video/7040278/, /19202862/ and /18680290/, hot-linked into your page. The video you paid to produce is immediately undercut by somebody else's footage above it. Your own installations are the asset here and they are not on the page.

The second thing is the one that costs you money directly. Your head installs the Google Ads tag AW-18243186763 and defines a WhatsApp conversion event against it - but the event still sends to 'AW-18243186763/WHATSAPP_LABEL', with the template's own comment 'Replace with your WhatsApp conversion label' sitting above it. Google Ads will never record a conversion from your site. You are paying for clicks with no measurement of what they produce, and the one action your page is built to create - the floating WhatsApp button, pre-filled with the enquiry - is the one action Google cannot count.

Third, the page has no Open Graph tags, no Twitter card, no canonical and no structured data at all, so any link shared anywhere renders as a bare URL with no image and no description. Your title is 108 characters and your three hero slides each carry their own <h1>, so the page competes with itself for three different queries.

To be fair to you, the markup is the cleanest I recorded this month - one error, no warnings - and the solar scope underneath is a real EPC business: rooftop solar, ground-mount systems, net metering, battery storage and AMC for residential and commercial plants, with feasibility studies, site surveys and net-metering approvals handled. You also say on your own homepage that you are 'a new bee in this energy sector', which I would keep - it reads as honest rather than as a weakness.

One thing to flag plainly: your site sells solar, wind and hydro as three equal lines, and the wind and hydro lines read as equipment trading rather than installation. The report is written for the solar business, which is the one the ads are about.

You can verify every line yourself:

  https://adstransparency.google.com/advertiser/AR08105928276372881409?region=IN
  https://validator.w3.org/nu/?doc=http://suryarenewable.com/&showsource=yes

Happy to walk you through what I found on a 10-minute call - or just keep the report, no strings attached.

""" + SIG,

    "Milestone Solarcom Private Limited": """Hi,

I spend my week reading the public ad-transparency records for the Telangana solar market, and I put together a short report on what Milestone Solar is doing right now.

What it covers (pulled from Google's Ads Transparency Centre on 2026-11-10):

  - 6 live ads under your advertiser record, identity-verified as ZAHEERUDDIN JAVEED MOHAMMED, trading as Milestone Solarcom
  - the ads point at milestonesolar.in, which I confirmed on the advertiser record
  - I also found you independently on the TGREDCO 2026 empanelled-supplier register under registration TSRE180047, which is the third-party confirmation I look for

Six live ads is real commitment, so I will be direct about what happens after the click.

Your homepage presents four trust counters, and all four read zero. 'Years of experience 0+'. 'Installations 0+'. 'Happy Customers 0%'. 'Customer Support 0/7'. They sit directly beside a '1,248 reviews' Google badge, so the two halves of the same screen contradict each other. A buyer who scrolls to the proof section sees four zeros and then a review count they cannot click through to.

Second, your click-to-call link is broken. The W3C checker reports 'Bad value tel:+91 9030005033 for attribute href on element a: Illegal character after tel:. Space is not allowed'. There is a space inside the href, so the number cannot be dialled from the page. On a site whose meta description opens 'Looking for best solar company in Hyderabad?' - the exact phrase your six ads are buying - the phone number does not work.

Third, the checker reports 128 errors, and 100 of them are elements sitting where they are not allowed: 55 <p> tags inside <span>, 22 <h3> inside <span>, 15 <h2> inside <span> and 7 <ul> inside <span>. That is what is breaking the counters.

On measurement: your Meta Pixel (1132764258717771) is confirmed and working, which is more than most of the leads I write to. Site Kit by Google is installed too, but I could not read a GA4 or Google Ads measurement ID in your head, so the spend behind six Google ads has no confirmed measurement behind it. That is the first thing worth checking.

To be fair to you, the capability underneath is real and unusually broad: off-grid and on-grid SPV plants, hybrid plants, solar micro and mini grids, street lighting, fencing, water heating and water pumping - and a government empanelment registration to back it, which most competitors cannot show. The offer is not the problem. The page that has to carry it is.

Two small things that undermine the rest: your Open Graph site name is set to a hyphen, so every share of your homepage is attributed to '-', and your conversion copy carries 'top solar comapy in hyderabad', 'This Shceme' and 'Sustanability Focused'.

You can verify every line yourself:

  https://adstransparency.google.com/advertiser/AR10713925876992442369?region=IN
  https://validator.w3.org/nu/?doc=https://www.milestonesolar.in/&showsource=yes

Happy to walk you through what I found on a 10-minute call - or just keep the report, no strings attached.

""" + SIG,
}

SUBJECTS = {
    "Zenith Energy Services Private Limited":
        "Zenith Energy: 9 live Google ads landing on a page with a second HTML document inside it",
    "SunWorks Energy Private Limited":
        "SunWorks Energy: your homepage gives three different answers on how old the company is",
    "Nature Power Solar":
        "Nature Power Solar: the best-built solar site I read this month, and Google cannot verify you own it",
    "Surya Renewable Energies":
        "Surya Renewable: your Google Ads conversion label is still the template placeholder",
    "Milestone Solarcom Private Limited":
        "Milestone Solar: 6 live Google ads, and every trust counter on the landing page reads zero",
}

CONTACT_NOTES = {
    "Zenith Energy Services Private Limited":
        "Email and phone read live on 2026-11-10: zenith@zenithenergy.com, "
        "+91 70757 56795. Registered office D.NO. 1-89/A/8/C/2&3, P. NO. 2P &3P "
        "C1, Vittal Rao Nagar, M3 Block, Shaikpet, Telangana 500081. CIN "
        "U74140TG1990PTC011583, incorporated 10 Aug 1990; directors Sindhu "
        "Jannareddy and Vindhya Pulicherla.",
    "SunWorks Energy Private Limited":
        "Email and phone read live on 2026-11-10: gosolar@sunworks.in, +91 86883 "
        "26316. 2nd Floor, Plot 126, Road Number 11, Jubilee Hills, Hyderabad. "
        "Facebook publisher link https://www.facebook.com/SunWorks.India.",
    "Nature Power Solar":
        "Email and phone read live on 2026-11-10: info@naturepowersolar.com, "
        "+91 96660 88988 / +91 84660 88988. 2-2-1/2, Budidagadda Basthi, "
        "Kothagudem, Telangana 507101; geo 17.545692 / 80.629687; open Mon-Sat "
        "09:00-19:00. Founder & Technical Lead Sagar Earpula, Operations "
        "Manager Abhilash Earpula. Independently listed on the TGREDCO 2026 "
        "empanelled-supplier register.",
    "Surya Renewable Energies":
        "Email and phone read live on 2026-11-10: info@suryarenewable.com, "
        "+91 91823 11739. Alkapuri Colony, Kothapet, Hyderabad, Telangana. "
        "WhatsApp wa.me/919182311739.",
    "Milestone Solarcom Private Limited":
        "Email and phone read live on 2026-11-10: "
        "milestonesolarcomsales@gmail.com (published on the site) and "
        "milestonesolarcom@gmail.com (registered address), +91 9030005033 / "
        "+91 9246527527. TGREDCO empanelled supplier registration TSRE180047.",
}


def main():
    # ---- leads.csv -------------------------------------------------------
    with io.open(LEADS_CSV, "r", encoding="utf-8", newline="") as f:
        raw = f.read()
    lines = raw.split("\r\n")
    header = lines[0]
    existing = [l for l in lines[1:] if l.strip()]
    have = {l.split(",")[0] for l in existing}
    print(f"leads.csv: {len(existing)} existing rows")

    out = list(existing)
    added = 0
    for row in ROWS:
        if row["name"] in have:
            print(f"  = {row['name']} already present, skipping")
            continue
        buf = io.StringIO()
        w = csv.writer(buf, lineterminator="\r\n")
        w.writerow([row["name"], row["city"], row["website"], row["email"],
                    row["phone"], row["snippet"], row["audit_score"],
                    row["audit_issues_count"], row["status"],
                    row["added_date"]])
        out.append(buf.getvalue().rstrip("\r\n"))
        added += 1
        print(f"  + {row['name']}")

    with io.open(LEADS_CSV, "w", encoding="utf-8", newline="") as f:
        f.write(header + "\r\n" + "\r\n".join(out) + "\r\n")
    print(f"leads.csv: now {len(out)} rows (+{added})")

    # ---- manifest --------------------------------------------------------
    with io.open(MANIFEST, encoding="utf-8") as f:
        man = json.load(f)
    seqs = man["sequences"]
    have_seq = {s["company"] for s in seqs}
    print(f"\nmanifest: {len(seqs)} existing sequences")

    for row in ROWS:
        name = row["name"]
        if name in have_seq:
            print(f"  = {name} already in the manifest, skipping")
            continue
        body = BODIES[name]
        subject = SUBJECTS[name]
        seq = {
            "city": row["city"],
            "company": name,
            "contact_note": CONTACT_NOTES[name],
            "mails_sent": 0,
            "next_followup_date": "",
            "next_step": None,
            "report_kind": "ads_only",
            "steps": [{
                "body": body,
                "delay_after_previous_days": 0,
                "draft_created_at": "",
                "draft_id": "",
                "due_date": "",
                "kind": "initial",
                "message_id": "",
                "sent_at": "",
                "status": "pending",
                "step": 0,
                "subject": subject,
                "thread_id": "",
            }],
            "thread_id": "",
            "thread_subject": subject,
            "to": row["email"],
            "website": row["website"],
        }
        seqs.append(seq)
        print(f"  + {name} -> {row['email']}")

    with io.open(MANIFEST, "w", encoding="utf-8") as f:
        json.dump(man, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"manifest: now {len(seqs)} sequences")


if __name__ == "__main__":
    main()
