#!/usr/bin/env python3
"""Internal review drafts for five Telangana candidates, NOT client deliverables.

Uses the Ksquare/claude-ads renderer but replaces unsafe template defaults for
this partial, date-uncertain source capture. Rebuilds JSON and PDFs together.
Independent report review and full live verification are still mandatory.
"""
from collections import Counter
from pathlib import Path
import json
import re

import audit_pdf as pdf
from ads_audit_controls import evaluate
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / '02-OUTREACH' / 'ads_only_pdfs'
RESULTS = ROOT / 'ads_only_results'
DATE = 'source date not verified'

DATA = [
 dict(company='SunSolar Power Systems', page='SunSolarhyd', site='https://www.sunsolar.info/', aid='2576227376137902', started='Oct 22, 2026', dest='fb.me displayed; final click destination not confirmed',
 text='☀️ HYDERABAD, SWITCH TO SOLAR FOR JUST ₹1,31,999! 🏡⚡\n\n🎉 This is your chance to make the switch to clean energy with SunSolar Power Systems!\n\n🔥 SPECIAL 3 KW SOLAR OFFER\n\n💰 Only ₹1,31,999/-\n\n✅ Government Subsidy Included – ₹78,000\n\n💳 ₹0 Down Payment\n\n📉 Easy EMI Available\n\n🛡️ 30 Years Warranty\n\n🏡 Free Site Visit\n\nWhy pay high electricity bills when your rooftop can generate your own power? Invest in solar today and enjoy long-term savings with trusted Adani Solar & Waaree Solar panels! 🌞\n\n📲 Book your FREE solar consultation now!\n\n📞 Call: +91 98666 02001\n\n📍 Suite 312, 3rd Floor, Kokapet Terminal Complex, Gandipet Main Road, Narsingi, Hyderabad.\n\n⚡ Limited-time offer — enquire today and take the first step towards lower electricity bills!\n\n#SunSolar #Hyderabad #SolarPanels #SolarEnergy #AdaniSolar #WaareeSolar #SolarSubsidy #RooftopSolar #SolarOffer #SaveElectricity #ZeroDownPayment #SolarInstallation #GoSolar',
 issues=['The ad card shows fb.me; the final form or destination was not confirmed.', 'The offer mentions subsidy, EMI and warranty; verify eligibility and terms before relying on them.', 'The site estimator is preliminary and subject to site conditions; it is not proof of the ad offer price.'],
 wins=['The site offers phone, email and WhatsApp contact links.', 'The estimate is explicitly labelled preliminary and subject to site review.'],
 conversion=[('Contact options','Phone, email and WhatsApp links were visible on the separately reviewed homepage.'),('Estimator','Homepage provides a preliminary estimator; calculations and submission were not tested.'),('Actual ad destination','The card showed fb.me; its final click path was not verified.')],
 gap=[('Ad promotes a 3 kW offer with subsidy and financing claims.', 'The separate homepage provides an illustrative preliminary estimator. The offer terms and actual ad destination were not verified.')],
 steps=[('Test the ad path','With permission, open the ad on a phone and confirm the final form or chat and enquiry receipt.'),('Verify offer terms','Check subsidy, EMI and warranty terms against the exact promoted package.'),('Test the estimator','Check calculations, mobile usability and the handoff to a final site quote.'),('Check measurement','Verify configured events and attribution in the accounts and browser.')]),
 dict(company='PNR Sunrise Energies', page='PNR Sunrise Energies Pvt Ltd', site='https://sunriseenergies.in/', aid='28807326382303186', started='Nov 12, 2026', dest='WhatsApp shown; final click destination not confirmed',
 text='🚀 Turn Your Business Dreams into a Growing Solar Business! ☀️\n\nJoin PNR Sunrise Energies Pvt. Ltd. as a Channel Partner and explore exciting business opportunities in the fast-growing Solar & Renewable Energy Sector.\n\n🤝 Dedicated Business & Operational Support\n\n🏠 Residential Rooftop Solar\n\n🏭 Commercial & Industrial Solar\n\n⚡ EV Charging Stations\n\n💧 Solar Water Pumps & Solar Fencing\n\nWhy Partner With Us?\n\n✅ Genuine Products & Reliable Solutions\n\n✅ Competitive Pricing\n\n✅ Expert Business Support\n\n✅ Timely Service & Delivery\n\n✅ Long-Term Partnership & Growth\n\n📍 Location: Hyderabad\n\n📞 Call Now: 6304587145\n\n🌐 Website: sunriseenergies.in\n\n👉 Partner with us today and grow together in the solar industry!\n\n#SolarBusiness #ChannelPartner #SolarDealership #RenewableEnergy #HyderabadBusiness',
 issues=['The captured ad seeks channel partners; its actual WhatsApp handoff has not been tested.', 'The separately viewed site describes customer solar services and a preliminary calculator; partner routing is unverified.', 'Measurement and partner lead qualification require account or workflow access.'],
 wins=['Ad text names the company, website and telephone number.', 'The site describes its calculator assumptions as estimates, not a final quotation.'],
 conversion=[('Site CTA','Homepage offers a free solar assessment; submission was not tested.'),('Calculator','The site labels its estimates illustrative; calculations were not tested.'),('Ad handoff','WhatsApp is shown on the card; final recipient and routing were not checked.')],
 gap=[('Ad invites channel partners.', 'The site describes solar EPC and an assessment. The destination and partner-specific path are unverified.'), ('Ad names solar and EV charging.', 'The homepage lists residential, commercial, industrial solar and EV charging services; capacity and delivery claims were not independently checked.')],
 steps=[('Test partner enquiry','With permission, confirm the WhatsApp recipient and partner enquiry handoff.'),('Check message alignment','Review whether the reached destination clearly explains channel-partner next steps.'),('Review qualification','Confirm how partner enquiries are differentiated from customer enquiries.'),('Verify measurement','Check account configuration and event delivery; no missing tag is asserted.')]),
 dict(company='DLIFE Home Interiors', page='DLIFE Home Interiors', site='https://dlifeinteriors.com/location/hyderabad/', aid='1024820157266461', started='Aug 19, 2026', dest='Send message shown; final destination not confirmed',
 text="A Beautiful Home at Om Sree Gallaxy, Hyderabad by D'LIFE Interiors\n\nFrom bringing their ideas to life to delivering the entire home in just 40 days, D’LIFE made the journey of creating this home seamless and stress-free. With thoughtful designs, meticulous craftsmanship and attention to every detail, the family found a home that was beautifully theirs. And even after handover, D’LIFE’s continued support gave them the assurance that their home was always taken care of.\n\n#BringHappinessInside\n\nIn search of a professional interior design company?\n\nCall: +91 949 508 7777\n\nEmail: enquiry@dlifeinteriors.com\n\nWeb: www.dlifeinteriors.com",
 issues=['The Hyderabad page and embedded map show different Banjara Hills postcodes; confirm the correct address.', 'The ad offers messaging; the final message destination and branch handoff were not verified.', 'The ad describes a project completion time; the underlying project evidence was not checked.'],
 wins=['The ad includes a website, email and phone number.', 'The Hyderabad page provides enquiry links and lists experience centres.'],
 conversion=[('Contact options','The Hyderabad page shows email and WhatsApp links; delivery was not tested.'),('Offer information','The Hyderabad page displays package offers; eligibility and terms were not checked.'),('Ad handoff','The card says Send message; final click destination was not verified.')],
 gap=[('Ad showcases a Hyderabad home project and a stated completion time.', 'The separately reviewed Hyderabad page describes services and packages. The project claim was not independently verified.')],
 steps=[('Confirm address','Reconcile the Banjara Hills postal code shown in page text and the embedded map.'),('Test messaging','With permission, verify the ad message recipient and branch routing.'),('Review claims','Ensure project timelines and package offers have accurate, clear supporting terms.'),('Check measurement','Verify conversion events and reporting in the appropriate accounts and browser.')]),
 dict(company='Dr Sridhar Dental', page='Dr. Sridhar Foundation', site='https://sridhardental.com/services', aid='1672235477851281', started='Oct 20, 2026', dest='https://sridhardental.com/services (shown on ad card)',
 text='Greetings from Dr Sridhar Dental\n\nVijayawada, Andhra Pradesh\n\nPlease contact for details : 9490948081 , 9705650999\n\nOpp JNTU, KPHB\n\n&Nallagandla, Hyderabad\n\nMr Ramkoti 9989377723\n\n#sridharreddy\n\n#bestdentalhospitals#kidsstories#moralstories#positivethinking',
 issues=['The ad names several locations and phone numbers; routing to the intended branch has not been tested.', 'The linked services page offers booking and branch WhatsApp links; successful handoff is unverified.', 'Healthcare claims, consent and measurement require specialist and account review.'],
 wins=['The captured ad card links to the services page.', 'The services page offers booking and branch-specific WhatsApp links.'],
 conversion=[('Service page','The ad card shows the services URL; the linked page lists treatments.'),('Booking','Booking and branch WhatsApp links are shown; no appointment or message was submitted.'),('Branches','The ad mentions KPHB and Nallagandla as well as Vijayawada.')],
 gap=[('Ad lists Vijayawada and Hyderabad contacts.', 'The services page lists treatments and branch WhatsApp links. Branch routing and appointment completion remain untested.')],
 steps=[('Test booking path','With clinic permission, verify the services-to-appointment journey on mobile.'),('Check branch routing','Confirm messages and calls reach the intended location and receive follow-up.'),('Review healthcare claims','Have the clinic check claims and privacy practices; compliance was not assessed here.'),('Validate measurement','Check consent and conversion events in the clinic accounts and browser.')]),
 dict(company='Galaxy Dental Care', page='Galaxy Dental Care', site='https://galaxydentalcare.in/contact-us/', aid='966436166129348', started='May 19, 2026', dest='WhatsApp shown; final click destination not confirmed',
 text='Hyderabad’s Best Dental Implant Offer is Live!\n\nSave big and restore your smile with premium implants from trusted specialists.\n\n✔️ ₹7,500 OFF on Single Implant\n\n✔️ Complimentary Implant Care Kit\n\n✔️ Teeth Cleaning Package (₹1,500 Value)\n\n✔️ Lifetime Warranty on Implants\n\nBook your Implant Consultation today',
 issues=['The Banjara Hills branch page gives two postcodes for the same address; the correct code is unconfirmed.', 'The card shows WhatsApp; the actual recipient and branch-routing path were not tested.', 'The ad makes implant offer and warranty claims; eligibility and underlying terms were not verified.'],
 wins=['The contact page offers branch selection, phone and WhatsApp links.', 'Branch areas in the card overlap with those listed on the contact page.'],
 conversion=[('Appointment form','Contact page shows a branch-selection form; submission was not tested.'),('Contact','Phone and WhatsApp links are displayed on the contact page.'),('Ad handoff','Card says Send WhatsApp message; the final click destination was not tested.')],
 gap=[('Ad promotes an implant offer and warranty.', 'The separately viewed contact page offers a branch-selection appointment form. Offer terms and ad click path were not verified.')],
 steps=[('Confirm postcode','Reconcile Banjara Hills postal codes on the branch page and in listings.'),('Test enquiry routing','With permission, verify WhatsApp and branch-selection form handoff.'),('Check offer terms','Confirm implant offer eligibility and warranty conditions with the clinic.'),('Verify measurement','Review consent and conversion events with appropriate account access.')]),
]

# Render overrides apply only to this draft batch. The normal shared renderer is
# unchanged. Source date is uncertain and incomplete checks cannot be scored.
pdf.TAGLINE = 'PERFORMANCE MARKETING'
pdf.days_running = lambda started: None
# Scale per report to retain legibility despite different ad-copy lengths.
STYLE_NAMES = ('body', 'body_b', 'small', 'small_b', 'cell', 'cell_b', 'cell_grey', 'link')
BASE_STYLES = {k: (pdf.ST[k].fontSize, pdf.ST[k].leading) for k in STYLE_NAMES}

def safe_stat(audit):
    return pdf.facts_table([('Audit score', 'Not scored - source checks are incomplete.'),
                            ('Ad evidence', 'One captured card; not a count of all ads.'),
                            ('Tracking and performance', 'Not checked; no absence or results are asserted.')])

def safe_score(audit):
    return pdf.empty_box('No score is assigned. Unknown measurements are not evidence of good or bad performance.')

def safe_panel(audit):
    body = [Paragraph('<b>INTERNAL DRAFT - NOT FOR CLIENT DELIVERY</b>', pdf.ST['h3']),
            Spacer(1, 1*mm),
            Paragraph('<b>WHAT WAS READ LIVE FOR THIS REPORT:</b> A direct Meta ad card and public website text were fetched. The card displayed Active; current status is not verified. One card is a sample, not the full account.', pdf.ST['body']),
            Spacer(1, 1*mm),
            Paragraph('Source timing is uncertain: the session date and sandbox/source clock conflict. Recheck all sources on a trusted clock. Independent report review and the live-data gate have not passed. Tracking, PageSpeed, Google Ads, account metrics and lead delivery were not measured.', pdf.ST['small'])]
    box = Table([[body]], colWidths=[pdf.CONTENT_W]); box.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#FFF4E1')),('BOX',(0,0),(-1,-1),.8,pdf.AMBER),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)])); return box

def safe_verification(audit):
    extra = {
      'SunSolar Power Systems': [('Identity cross-check', 'The ad text and homepage display the same Hyderabad address and main phone. This does not prove the ad click destination.'), ('Estimate limitations', 'The homepage says its estimate is preliminary and that final pricing depends on an inspection, system design, eligibility and other conditions.')],
      'PNR Sunrise Energies': [('Identity cross-check', 'The ad and homepage show the same company name, website domain and main number. Partner lead handling was not tested.'), ('Calculator limitations', 'The website describes calculator figures as illustrative and says a final quotation depends on a site assessment. The calculator was not exercised.')],
      'DLIFE Home Interiors': [('Branch source', 'Hyderabad page text and its embedded map show different postcodes. Confirm the correct one before publication.')],
      'Dr Sridhar Dental': [('Branch contact source', 'https://sridhardental.com/contact lists KPHB and Nallagandla. Branch contact information is self-reported and was not tested.'), ('Evidence boundaries', 'The ad card links to the services page; a successful visit, appointment completion and patient follow-up were not tested.'), ('Services page', 'The page offers a booking link and separately lists branch-specific WhatsApp options. The displayed contact details do not confirm lead delivery.')],
      'Galaxy Dental Care': [('Branch postcode source', 'https://galaxydentalcare.in/banjara-hills/ gives 500034 in the main address and 500028 in the branch list. Neither value has been confirmed.'), ('Evidence boundaries', 'The website form and WhatsApp link were observed separately from the ad. Neither submission nor the ad click-through was tested.'), ('Contact page', 'The contact page lists multiple Hyderabad branches and a branch selector for appointments. Actual selection and notification were not tested.')],
    }
    rows = [('Ad sample', 'Direct Meta Library ID, linked from the ad card. Source date and current status require recheck.'), ('Website', audit['website'] + ' - public page text, not a full browser or source audit.')]
    rows.extend(extra.get(audit['company'], []))
    rows.extend([('Tracking, speed, account results', 'Not checked; no scores or performance claims.'), ('Independent gates', 'Report reviewer and live-data auditor pending. Do not deliver to clients.')])
    return pdf.facts_table(rows)

def draft_header(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(pdf.NAVY); canvas.rect(0, pdf.PAGE_H-21*mm, pdf.PAGE_W, 21*mm, stroke=0, fill=1)
    canvas.setFillColor(pdf.AMBER); canvas.rect(0, pdf.PAGE_H-22*mm, pdf.PAGE_W, 1*mm, stroke=0, fill=1)
    logo = ROOT / 'audit_results' / '_branding' / 'logo_white.png'
    text_x = pdf.MARGIN
    if logo.exists():
        canvas.drawImage(str(logo), pdf.MARGIN, pdf.PAGE_H-18*mm, 15*mm, 15*mm, mask='auto', preserveAspectRatio=True, anchor='c')
        text_x += 18*mm
    canvas.setFont('Helvetica-Bold', 14); canvas.setFillColor(colors.white)
    canvas.drawString(text_x, pdf.PAGE_H-10*mm, 'SMART PURSUIT')
    canvas.setFont('Helvetica', 8); canvas.drawString(text_x, pdf.PAGE_H-16*mm, 'PERFORMANCE MARKETING')
    canvas.setFont('Helvetica-Bold', 9); canvas.drawRightString(pdf.PAGE_W-pdf.MARGIN, pdf.PAGE_H-10*mm, 'ADS AUDIT REPORT')
    canvas.setFont('Helvetica-Bold', 8); canvas.drawRightString(pdf.PAGE_W-pdf.MARGIN, pdf.PAGE_H-16*mm, 'INTERNAL DRAFT - DO NOT SEND TO CLIENTS')
    canvas.setFont('Helvetica', 7.3); canvas.setFillColor(pdf.GREY)
    canvas.drawString(pdf.MARGIN, 8*mm, f'Prepared by {pdf.YOUR_NAME} | {pdf.YOUR_AGENCY} | {pdf.YOUR_PHONE}')
    canvas.drawRightString(pdf.PAGE_W-pdf.MARGIN, 8*mm, f'Page {doc.page}')
    canvas.restoreState()

def safe_cta(audit):
    return pdf.empty_box('Owner review only. Confirm the observations, complete independent review and pass the live verifier before sharing this report externally.')

old_story = pdf.build_story
def safe_story(audit):
    flowables = old_story(audit)
    for i, flow in enumerate(flowables):
        if isinstance(flow, Paragraph):
            text = flow.getPlainText()
            if text.startswith('Source observations were read from public pages on the date shown'):
                flowables[i] = Paragraph('This draft is based on a limited sample. Source timing is uncertain and no score is assigned; recheck before use.', pdf.ST['body'])
            elif text.startswith('Report generated automatically on '):
                flowables[i] = Paragraph('Internal draft only. Independent review and current live re-verification remain outstanding.', pdf.ST['small'])
    return flowables

pdf.stat_tiles = safe_stat
pdf.score_panel = safe_score
pdf.ads_only_honesty_panel = safe_panel
pdf.verification_log = safe_verification
pdf.header_footer = draft_header
pdf.cta_card = safe_cta
pdf.build_story = safe_story

TRACKING = ('meta_pixel','google_ads','google_analytics_ga4','google_analytics_ua','linkedin_insight','microsoft_clarity','hotjar','google_tag_manager')
CONV = ('has_contact_form','has_phone_click','has_whatsapp_link','has_cta_buttons','has_live_chat','has_popup_optin','has_testimonials','has_pricing_page_link')
SEO = ('has_title','title_text','has_meta_description','h1_count','has_og_tags','has_schema','has_favicon','image_count','images_without_alt')

def build(d):
    scale = {'SunSolar Power Systems':1.12, 'PNR Sunrise Energies':1.14,
             'DLIFE Home Interiors':1.16, 'Dr Sridhar Dental':1.18,
             'Galaxy Dental Care':1.18}[d['company']]
    for key, (size, leading) in BASE_STYLES.items():
        pdf.ST[key].fontSize, pdf.ST[key].leading = size * scale, leading * scale
    px = dict.fromkeys(TRACKING)
    site = {'ssl':True, 'load_time_seconds':None, 'final_url':d['site'], 'audit_date':DATE,
            'pixels':px, 'conversion':dict.fromkeys(CONV), 'seo':dict.fromkeys(SEO),
            'pagespeed':{'error':'not measured for this site'}, 'page_count':{'has_sitemap':None},
            'local_signals':{'has_google_maps_embed':None},
            'conversion_evidence':{'checked_on':DATE, 'method':'Public page text; no interaction.', 'sources':[d['site']], 'rows':d['conversion']},
            'score':{'score':None, 'issues':d['issues'], 'wins':d['wins']}}
    ad = {'library_id':d['aid'], 'library_url':'https://www.facebook.com/ads/library/?id='+d['aid'],
          'page_name':d['page'], 'started':d['started'], 'destination':d['dest'], 'text':d['text']}
    audit = {'company':d['company'], 'city':'Hyderabad', 'website':d['site'],
             'checked_on':DATE, 'audit_date':DATE, 'ads_only':True, 'website_audit_run':True,
             'conservative_scope':True, 'review_pending':True,
             'ad_library':{'meta_own':{'found':True, 'ads':[ad]}, 'summary':'One direct Meta ad card was captured; current status and source date require rechecking. Website observations are separate and limited.'},
             'funnel':{'type':'Destination not confirmed', 'destination':d['dest']},
             'site_audit':site, 'site_evidence':{'pixel':None,'ga4':None,'gtm':None,'google_ads_tag':None},
             'promise_gap':d['gap'], 'recommended_steps':d['steps']}
    controls = evaluate(audit, audit['site_evidence'])
    for c in controls['controls']:
        c['disposition']='unknown'
        c['evidence']='Sample and timing are incomplete; recheck this control with current evidence.'
    controls['counts'] = dict(Counter(c['disposition'] for c in controls['controls']))
    audit['ads_audit'] = controls
    slug = re.sub(r'[^a-zA-Z0-9]+', '_', d['company'])[:50]
    path = RESULTS / ('audit_' + slug + '.json')
    target = OUT / ('audit_' + slug + '.pdf')
    if path.exists():
        old = json.loads(path.read_text(encoding='utf-8'))
        if not old.get('review_pending') or old.get('company') != d['company'] or old.get('checked_on') != DATE:
            raise RuntimeError('Refusing to overwrite an existing audit: ' + slug)
    elif target.exists():
        raise RuntimeError('Refusing to overwrite an unmatched PDF: ' + slug)
    path.write_text(json.dumps(audit, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(pdf.generate_ads_only_pdf(audit, str(target)))

if __name__ == '__main__':
    for d in DATA: build(d)
