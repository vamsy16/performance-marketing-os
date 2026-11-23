#!/usr/bin/env python3
"""Batch 14 public-evidence drafts. Not approved for outreach.

Sources read 2026-11-23: each linked Meta Ad Library ID; the company website;
W3C Nu HTML checker with showsource=yes. Source review was partial; unobserved
tracking is unknown, not absent. Follow AGENTS.md review and live gates before
client delivery. Rebuild with PYTHONPATH=/tmp/pdflibs python3 build_batch14_karnataka.py.
"""
import json
from collections import Counter
from pathlib import Path
from ads_audit import calculate_audit_score
from ads_audit_controls import evaluate
from audit_pdf import generate_ads_only_pdf

ROOT = Path(__file__).resolve().parent
DATE = '2026-11-23'
TRACKING = ('meta_pixel','google_ads','google_analytics_ga4','google_analytics_ua',
            'linkedin_insight','microsoft_clarity','hotjar','google_tag_manager')
CONV = ('has_contact_form','has_phone_click','has_whatsapp_link','has_cta_buttons',
        'has_live_chat','has_popup_optin','has_testimonials','has_pricing_page_link')

DATA = {
'SundayGrids': dict(city='Bengaluru', url='https://www.sundaygrids.com/', id='1677559457265808', start='Nov 8, 2026', dest='https://www.sundaygrids.com/projects/278RAO1IVG', kind='Project page',
 text="What if your electricity bill could now be powered by solar you don't own on your roof?\n\nLiving in an apartment doesn’t stop you from using solar anymore.\n\nInstead of installing panels, you can now:\n\n* Reserve solar capacity\n\n* Let it generate power\n\n* Get bill credits every month\n\nNo roof. No hassle.\n\n25+ projects are already running across India, and ₹2Cr+ in bills have already been offset.\n\nCheck if this works for your home.",
 tags={'google_analytics_ua':True, 'google_tag_manager':True}, conv={}, seo={'h1_count':7},
 note='The actual ad link points to Parker 110, not the homepage. Its project page describes credits, validity and a reservation fee; form submission and event firing were not tested. GTM-PZ8PCNX, UA-170164983-1, PostHog and Calendly were seen on the homepage. Other tracking remains unverified.',
 issues=['The ad links to Parker 110; check project-specific terms and utility eligibility before scaling.', 'A legacy Universal Analytics ID and GTM container were observed on the homepage; verify current analytics and event delivery.', 'The homepage validator reported 25 errors and 21 warnings, including repeated IDs.'],
 gap=[('Ad: reserve solar capacity and get monthly bill credits.', 'The actual Parker 110 project page describes bill credits and a reservation fee, with utility eligibility and exit terms. The savings figures are company claims, not independently verified.'), ('Ad: 25+ projects and over ₹2 crore in bills offset.', 'These are ad claims; underlying project and billing records were not available for independent verification.')],
 steps=[('Validate landing experience','Test the Parker 110 signup and eligible utilities on mobile.'),('Check measurement','Verify GA4 and conversion events in the accounts and browser.'),('Review project terms','Check reservation fees, credit use and exit conditions are clear.'),('Repair markup','Review duplicate IDs reported by the HTML validator.')]),
'Arrow Solar': dict(city='Karnataka',url='https://arrowenergy.in/',id='4616054888675895',start='Oct 21, 2026',dest='fb.me (card link; exact form or final destination not verified)',kind='fb.me link',
 text='Paying high electricity bills? ☀️\n\nSwitch to solar with Arrow Power Controls, bringing 25 years of experience in solar installations.\n\n🏠 Residential rooftop solar\n\n🏢 Commercial solar solutions\n\n⚡ Systems tailored to your electricity requirements\n\n🔧 Professional installation and support\n\nLooking for a solar installation in Bengaluru?\n\nFill out our quick form with your contact details and approximate kW requirement. Our team will get in touch to understand your needs and help you take the next step.\n\nGet started today!',
 tags={'google_analytics_ga4':True},conv={'has_contact_form':False,'has_phone_click':True,'has_whatsapp_link':True},seo={'has_schema':True},
 note='The card displays arrowenergy.in but its public card link is fb.me; the final click-through and form were not verified. GA4 G-LY596XLF42 was observed in homepage source; runtime events were not tested.',
 issues=['The ad mentions a quick form; the public card link shown is fb.me, so verify the actual post-click form and lead capture.', 'The homepage has a phone and WhatsApp link but no homepage form was observed.', 'The ad says 25 years of experience while the homepage says 22+ years; reconcile the claims.'],
 gap=[('Ad: quick form and a call back for a solar installation.', 'The card shows a fb.me link; the final form was not tested. The homepage offers phone, WhatsApp and a contact link, rather than a homepage form.'), ('Ad: 25 years of experience.', 'The homepage says 22+ years. Verify the basis and update inconsistent wording.')],
 steps=[('Test the ad click','Open the live ad on mobile and confirm the form and lead handoff.'),('Align experience claims','Reconcile the ad and homepage experience figures.'),('Verify analytics','Check GA4 event firing and consent in a real browser.'),('Improve enquiry path','Review whether an on-page form would help visitors who avoid phone or chat.')]),
'Atria Power': dict(city='Bengaluru',url='https://www.atriapower.com/',id='1103298019283935',start='Nov 4, 2026',dest='fb.me (card link; form not verified)',kind='fb.me link',
 text='Why wait for a subsidy when you can start saving from day one?\n\nWith the Atria Subsidy, Bengaluru homeowners get benefits worth ₹75,000 on a 3 kW rooftop system, paid upfront. You pay only the balance.\n\n✔ 3 kW systems from ₹1.42 lakh after the Atria Subsidy\n\n✔ For independent houses with a monthly bill above ₹1,200\n\n✔ Financing options available\n\n✔ 4.9 on Google from 100+ reviews\n\n✔ 66+ year legacy, from the founders of ACT\n\nTap Get Offer to book a free site survey, or call +91 99011 00428.',
 tags={},conv={},seo={},
 note='The ad card shows fb.me and Get offer; the final form was not tested. The reviewed site is the corporate homepage, not the confirmed ad destination. The homepage validator hit its message cap; source and tracking review was partial.',
 issues=['The card shows fb.me and Get offer; verify the actual destination and survey booking flow.', 'The corporate homepage features solar, wind and hydro; its rooftop link points to a separate domain.', 'The homepage checker hit its message cap; do not treat the total as a count of actionable HTML defects.'],
 gap=[('Ad: 3 kW from ₹1.42 lakh after Atria Subsidy.', 'The reviewed corporate homepage is not the confirmed ad destination and does not establish this offer. Verify terms in the live form and the rooftop site.'), ('Ad: book a free survey via Get Offer.', 'The card shows fb.me; the booking flow and survey delivery were not tested.')],
 steps=[('Test Get Offer','Check the mobile post-click flow and lead handoff.'),('Clarify the offer','Confirm price, subsidy terms and eligibility wherever the offer is shown.'),('Verify tracking','Inspect runtime events and account configuration with consent.'),('Review validator output','Separate actionable markup findings from Wix CSS diagnostics.')]),
'RAGA Renewable Energy': dict(city='Mysuru',url='https://ragarenewableenergy.com/',id='3057224721288021',start='Nov 3, 2026',dest='http://instagram.com/ragarenewableenergy',kind='Instagram profile',
 text="☀️ Give Your Family the Power of a Brighter Tomorrow!\n\nA solar-powered home means more than just generating electricity. It's about smarter energy choices, reduced electricity expenses, and a cleaner environment for the next generation.\n\nWith Rooftop Solar, You Can:\n\n✔ Reduce dependence on conventional electricity.\n\n✔ Enjoy long-term electricity bill savings.\n\n✔ Explore government subsidy benefits.\n\n✔ Make your home more energy-efficient.\n\n✔ Contribute towards a greener environment.\n\nLet your rooftop become a source of power and savings.\n\n📍 Mysuru & Nearby Cities.\n\nChoose Solar. Choose a Sustainable Future. Choose Raga Renewable Energy.",
 tags={},conv={'has_contact_form':True},seo={'has_schema':True},
 note='The ad links to the Instagram profile, not the website. The homepage was reviewed separately. Unobserved source tags remain unknown and no form submission or event firing was tested.',
 issues=['The captured ad links to the Instagram profile; test how enquiries are received and followed up there.', 'A homepage testimonial attributed to John Doe refers to SunBright Energy; verify or remove this apparent placeholder.', 'Homepage counter text included 0+ years and 4% satisfaction in the fetched page; verify display and data in a browser.'],
 gap=[('Ad: rooftop solar and government subsidy benefits.', 'The captured ad links to Instagram. The separately reviewed website describes rooftop solutions and up to ₹78,000 in savings; eligibility was not verified.'), ('Ad: Mysuru and nearby cities.', 'The site lists a Mysuru address and a Bengaluru address; actual service coverage should be confirmed.')],
 steps=[('Test the Instagram path','Check profile, message handling and follow-up time.'),('Review testimonial','Verify or remove the John Doe / SunBright Energy quote.'),('Check counters','Test the homepage counters in a real browser and correct any stale values.'),('Validate enquiry form','Test a controlled submission and measurement with permission.')]),
'Zenith Solars': dict(city='Kalaburagi',url='https://zenithsolars.com/index.html',id='972063355961941',start='Oct 22, 2026',dest='Call now (number destination not exposed on card)',kind='Call now',
 text="⚡ Looking for Solar Installation in Kalaburagi?\n\nZenith Solars brings solar solutions for residential, educational, healthcare, and industrial properties.\n\n🏠 Homes | 🏫 Schools | 🏥 Hospitals | 🏭 Industries | 🏢 Commercial Buildings\n\nChoose solar energy for a more sustainable future. Contact our team to discuss your property's solar requirements.\n\n📞 Call +91-8197503333 or +91-9901349462.",
 tags={},conv={'has_contact_form':True},seo={},
 note='The ad CTA says Call now, not website. The index.html page was separately reviewed because the root URL was inaccessible to the checker. The call destination and form submission were not tested.',
 issues=['The ad uses Call now; verify which number the button calls and how calls are followed up.', 'The homepage has an enquiry form; its submission and success state were not tested.', 'The homepage validator reported 29 errors and one warning; review the actual markup rather than assuming visitor impact.'],
 gap=[('Ad: solar for homes, schools, hospitals, industries and commercial buildings.', 'The separately reviewed website lists multiple service and solution segments; the actual ad action is Call now.'), ('Ad: call either of two numbers.', 'Both numbers appear on the website; the number behind the CTA was not verified.')],
 steps=[('Test call CTA','Verify the dialled number and missed-call follow-up.'),('Test enquiry form','Run a controlled submission and confirm a success message.'),('Review markup','Prioritise actionable issues from the Nu HTML checker.'),('Verify measurement','Check tag deployment and lead events in account tools.')])
}


# Expanded evidence from the 2026-11-23 homepage, validator source and sitemap
# reads. Source tags signal code presence only, not successful firing. Keep
# unverified negative claims unknown; do not turn a partial read into absence.
DATA['SundayGrids']['seo'].update(has_title=True, title_text='SundayGrids | Get monthly credits to save up on electricity.', has_meta_description=True)
DATA['SundayGrids']['conv'].update(has_testimonials=True, has_pricing_page_link=True)
DATA['SundayGrids']['sitemap'] = 'Sitemap fetched: homepage and project URLs listed; not a count of indexed pages.'
DATA['SundayGrids']['html_errors'] = '25 errors, 21 warnings, 51 info'
DATA['SundayGrids']['issues'] = [
    'The Parker 110 project page describes reservation fees and bill credits; check that eligible utilities and exit terms are clear before signup.',
    'Homepage source includes GTM-PZ8PCNX and legacy UA-170164983-1; verify GA4 and conversion events at runtime.',
    'The Nu checker flagged seven H1 elements, 12 duplicate SVG IDs and four skipped heading levels; review accessibility impact.',
]
DATA['Arrow Solar']['seo'].update(has_title=True, title_text='Arrow Power Controls | Solar EPC & Installation Company | Karnataka', has_meta_description=True, has_og_tags=True, has_favicon=True)
DATA['Arrow Solar']['conv'].update(has_pricing_page_link=True)
DATA['Arrow Solar']['sitemap'] = 'Sitemap fetched and lists solar services and project URLs; indexing not verified.'
DATA['Arrow Solar']['html_errors'] = '1 error, 2 warnings, 43 info'
DATA['Arrow Solar']['issues'] = [
    'The ad calls for a quick form, but the card link shows fb.me; verify the final destination and lead handoff.',
    'The ad says 25 years of experience while the homepage says 22+ years; reconcile these statements.',
    'Homepage pricing shows a 3 kW package at Rs. 1,44,000 after subsidy, while the hero says zero upfront cost; clarify financing and eligibility.',
    'No form was observed on the homepage; a quote form is available at /contact, but its submission was not tested.',
]
DATA['Atria Power']['seo'].update(has_title=True, title_text='Home | Atria Power', has_favicon=True)
DATA['Atria Power']['sitemap'] = 'robots.txt declares /sitemap.xml; sitemap fetch failed, so contents and indexing are unverified.'
DATA['Atria Power']['sitemap_confirmed'] = None
DATA['Atria Power']['note'] = 'The card says Get offer and links to fb.me; its final form was not tested. The separately reviewed corporate contact page has a form. Wix source review is partial; event firing remains unverified.'
DATA['Atria Power']['html_errors'] = '979 errors, 0 warnings, 22 info (checker hit message cap; includes 7 HTML errors)'
DATA['RAGA Renewable Energy']['seo'].update(has_title=True, title_text='Raga Renewable Energy Home -', has_meta_description=True, has_og_tags=True)
DATA['RAGA Renewable Energy']['conv'].update(has_phone_click=True)
DATA['RAGA Renewable Energy']['sitemap'] = 'Sitemap index and page sitemap fetched; indexing not verified.'
DATA['RAGA Renewable Energy']['html_errors'] = '27 errors, 12 warnings, 68 info'
DATA['RAGA Renewable Energy']['issues'] = [
    'The ad links to Instagram; verify profile enquiry handling and follow-up.',
    'The homepage enquiry form source is marked hidden on tablets; test visibility and submission.',
    'A hidden block contains a John Doe / SunBright quote; review it before reuse.',
    'The homepage counters are animated; check final display and substantiate their claims.',
]
DATA['RAGA Renewable Energy']['steps'] = [
    ('Test Instagram enquiries','Verify how messages are received and followed up after the captured ad.'),
    ('Test the enquiry form','Check tablet visibility and run a controlled submission with permission.'),
    ('Review hidden content','Remove or correct the unused John Doe / SunBright template block before reuse.'),
    ('Check counters','Test the final animated values in a browser and substantiate the claims.'),
]
DATA['Zenith Solars']['seo'].update(has_title=True, title_text='Solar System Installation Services in Kalaburagi - Zenith Solars', has_meta_description=True, has_og_tags=True, has_favicon=True, h1_count=6)
DATA['Zenith Solars']['conv'].update(has_phone_click=True)
DATA['Zenith Solars']['sitemap'] = 'Robots.txt points to /demo/sitemap.xml; that sitemap lists JCB equipment URLs, not solar pages.'
DATA['Zenith Solars']['html_errors'] = '29 errors, 1 warnings, 18 info (parser stopped after fatal error)'
DATA['Zenith Solars']['issues'] = [
    'robots.txt points to /demo/sitemap.xml, which lists Sri Sai JCB equipment pages rather than Zenith solar pages; investigate the sitemap and deployment.',
    'The ad says Call now; verify the dialled number and the missed-call follow-up.',
    'The index.html page has an enquiry form; its submission and success state were not tested.',
    'The header lists postal code 585106 while the contact page body lists 585105; confirm and align the address.',
]
DATA['SundayGrids']['score_basis'] = '1 point: seven H1 elements. Unknown checks are excluded.'
DATA['Arrow Solar']['score_basis'] = '8 points: no homepage form observed; contact page has a form. Unknown checks are excluded.'
DATA['Atria Power']['score_basis'] = '0 points from measured formula checks. Unknown checks are excluded; zero is not a clean bill of health.'
DATA['RAGA Renewable Energy']['score_basis'] = '0 points from measured formula checks. Unknown checks are excluded; zero is not a clean bill of health.'
DATA['Zenith Solars']['score_basis'] = '1 point: six H1 elements. Unknown checks are excluded.'
DATA['Zenith Solars']['steps'] = [
    ('Investigate sitemap','Confirm intended ownership of /demo and publish a sitemap for actual solar pages.'),
    ('Test call CTA','Verify the dialled number and missed-call follow-up.'),
    ('Test enquiry form','Run a controlled submission and confirm the success message.'),
    ('Align contact details','Confirm whether 585105 or 585106 is correct and use one consistent postal code.'),
]


def build(name, d):
    px={k:None for k in TRACKING}; px.update(d['tags'])
    conv={k:None for k in CONV}; conv.update(d['conv'])
    seo={'has_title':None,'title_text':None,'has_meta_description':None,'h1_count':None,'has_og_tags':None,'has_schema':None,'has_favicon':None,'image_count':None,'images_without_alt':None}; seo.update(d['seo'])
    result=calculate_audit_score({}, px, conv, seo, {})
    # Keep scores algorithmic, but show contextual public-evidence priorities,
    # not unsupported template assertions about lost sales or attribution.
    result['issues']=d['issues']
    site={'ssl':True,'load_time_seconds':None,'final_url':d['url'],'audit_date':DATE,'pixels':px,'conversion':conv,'seo':seo,'pagespeed':{'error':'not measured for this site'},'page_count':{'has_sitemap': d.get('sitemap_confirmed', True) if d.get('sitemap') else None, 'note':d.get('sitemap')},'local_signals':{'has_google_maps_embed':None},'scope_note':d['note'],'html_errors':d.get('html_errors'),'score':result}
    ad={'library_id':d['id'],'library_url':'https://www.facebook.com/ads/library/?id='+d['id'],'page_name':name,'started':d['start'],'destination':d['dest'],'text':d['text']}
    evidence={'pixel':None,'ga4':px['google_analytics_ga4'],'gtm':px['google_tag_manager'],'google_ads_tag':None,'checked_on':DATE,'note':'Selected served source reviewed; absence and runtime behavior are unverified.'}
    audit={'company':name,'city':d['city'],'website':d['url'],'checked_on':DATE,'audit_date':DATE,'generated_at':DATE,'ads_only':True,'website_audit_run':True,'conservative_scope':True,'review_pending':True,
       'ad_library':{'meta_own':{'found':True,'ads':[ad]},'summary':'One active Meta ad card captured on 2026-11-23; this is a sample, not necessarily the total. Google Ads activity was not checked.'},
       'score_basis':d['score_basis'],'funnel':{'type':d['kind'],'destination':d['dest']},'site_audit':site,'site_evidence':evidence,'promise_gap':d['gap'],'recommended_steps':d['steps']}
    controls=evaluate(audit,evidence)
    for c in controls['controls']:
        if c['id'] in ('M39','M25','M26','M30','M-CR1','M11','M18'):
            c['disposition']='unknown'
            c['evidence']='One card only; verify full account and click path.'
        if c['id']=='M01': c['evidence']='Partial source review; verify deployment and runtime.'
    controls['counts']=dict(Counter(c['disposition'] for c in controls['controls']))
    audit['ads_audit']=controls
    out=ROOT/'ads_only_results'/('audit_'+name.replace(' ','_')+'.json')
    out.write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    pdf=generate_ads_only_pdf(audit)
    print(name, result['score'], pdf)

if __name__=='__main__':
    for name,data in DATA.items(): build(name,data)
