#!/usr/bin/env python3
"""Build an INTERNAL evidence workpaper, not an audit report or client deliverable.

This deliberately does not create audit JSON, scores, lead status updates or
outreach. Observations were taken from the linked public-page fetches; the
independent review and repository live gate have NOT passed.
"""
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak

OUT = Path(__file__).parent / 'telangana_five_internal_evidence_workpaper.pdf'

DATA = [
    {
        'name': 'SunSolar Power Systems / SunSolarhyd',
        'ad': 'https://www.facebook.com/ads/library/?id=2576227376137902',
        'site': 'https://www.sunsolar.info/',
        'facts': [
            'The direct ad card displayed Active and names SunSolar Power Systems, a Hyderabad address and phone number. The site displays the same address and number; this is identity evidence, not proof of ad performance.',
            'The ad advertises a 3 kW offer with subsidy and financing claims. The separately reviewed homepage contains a preliminary estimator and says a final quotation depends on a site inspection and other conditions.',
            'The ad card displays fb.me. The final click-through destination was not verified; the homepage must not be described as the ad landing page.'
        ],
        'actions': [
            'Verify the actual mobile click path and whether an enquiry is received; do not submit a lead without permission.',
            'Review offer eligibility, financing terms and the relationship between the advertised offer and the estimator. They are not necessarily comparable.',
            'Confirm live tracking and conversion events in the browser and accounts; page text alone cannot verify them.'
        ],
        'contact': 'sales@sunsolar.info | +91 9866602001 (site; delivery not tested)',
    },
    {
        'name': 'PNR Sunrise Energies Pvt Ltd',
        'ad': 'https://www.facebook.com/ads/library/?id=28807326382303186',
        'site': 'https://sunriseenergies.in/',
        'facts': [
            'The direct ad card displayed Active and names PNR Sunrise Energies, Hyderabad, the website domain and the same phone number shown on the website.',
            'The captured ad seeks channel partners; it should not be represented as a residential customer-acquisition campaign. The website separately describes solar EPC and EV charging services.',
            'The card shows WhatsApp; the final conversation path and follow-up are not verified. The site has an assessment CTA and a calculator described as illustrative.'
        ],
        'actions': [
            'With permission, test the partner enquiry path and ask how leads are qualified and followed up.',
            'Evaluate whether the partner offer and the destination reached after clicking are aligned; the destination is unconfirmed.',
            'Verify conversion measurement in the accounts and browser. No business email was confirmed from the fetched homepage.'
        ],
        'contact': '+91 6304587145 (ad and site; delivery not tested)',
    },
    {
        'name': "D'LIFE Home Interiors",
        'ad': 'https://www.facebook.com/ads/library/?id=1024820157266461',
        'site': 'https://dlifeinteriors.com/location/hyderabad/',
        'facts': [
            "The direct ad card displayed Active, describes a Hyderabad home project, and prints D'LIFE's domain, email and phone. The Hyderabad page shows the same email and Banjara Hills phone.",
            'The ad shows a Send message action; the final message destination and handoff were not tested. The separately reviewed Hyderabad page promotes interior packages and includes enquiry links.',
            'The Hyderabad page text lists the Banjara Hills postcode as 500034 while its embedded map text lists 500028. The correct postcode has not been independently determined.'
        ],
        'actions': [
            'Confirm the correct Banjara Hills address and align the website and map listing if needed.',
            'Test the message enquiry and callback workflow with permission, including any branch routing.',
            'Review the stated package and project claims for clear terms and evidence; this workpaper does not assess whether the claims are true.'
        ],
        'contact': 'enquiry@dlifeinteriors.com | +91 9495087777 (site; delivery not tested)',
    },
    {
        'name': 'Dr. Sridhar International Dental Hospital / Foundation',
        'ad': 'https://www.facebook.com/ads/library/?id=1672235477851281',
        'site': 'https://sridhardental.com/services',
        'facts': [
            'The direct ad card displayed Active under Dr. Sridhar Foundation; it mentions Hyderabad KPHB and Nallagandla and links to the dental services page. The site lists those locations as well as other branches.',
            'The services page describes multiple treatments and links to booking and branch WhatsApp contacts. No appointment, message, call or submission was tested.',
            'The ad also mentions Vijayawada and contains several contact numbers. Do not assume all enquiries are routed to a Hyderabad branch.'
        ],
        'actions': [
            'Check the ad-to-services-to-booking experience on mobile and confirm the intended branch receives enquiries.',
            'Check appointment form confirmation and branch-specific follow-up using an authorised test, not a real unsolicited patient lead.',
            'Confirm healthcare advertising claims, consent and measurement with the clinic; public page text does not establish compliance or conversion performance.'
        ],
        'contact': 'jntu@sridhardental.com | +91 8121222888 (KPHB site contact; delivery not tested)',
    },
    {
        'name': 'Galaxy Dental Care',
        'ad': 'https://www.facebook.com/ads/library/?id=966436166129348',
        'site': 'https://galaxydentalcare.in/contact-us/',
        'facts': [
            'The direct ad card displayed Active under Galaxy Dental Care and lists Hyderabad branches; the site lists the same branch areas. Its card shows Send WhatsApp message; the final destination was not tested.',
            'The contact page displays a branch-selection appointment form, telephone and WhatsApp links. A form submission, message delivery and branch routing were not tested.',
            'The Banjara Hills branch page gives postcode 500034 in its main text and 500028 in its branch list. The correct value has not been established.'
        ],
        'actions': [
            'Verify and align the Banjara Hills postcode across branch pages and listings.',
            'With permission, test WhatsApp and the appointment form, including branch selection, response time and lead handoff.',
            'Check the implant offer and its terms with the clinic; the ad text is a business claim, not proof of clinical outcomes or performance.'
        ],
        'contact': 'contact@galaxydentalcare.in | +91 8686676781 (site; delivery not tested)',
    },
]

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleW', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=17, leading=20, textColor=colors.HexColor('#10243d'), spaceAfter=7))
styles.add(ParagraphStyle(name='WarnW', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, leading=13, textColor=colors.HexColor('#9d291e'), spaceAfter=6))
styles.add(ParagraphStyle(name='SectionW', parent=styles['Heading2'], fontSize=10, leading=13, textColor=colors.HexColor('#135e75'), spaceBefore=8, spaceAfter=3))
styles.add(ParagraphStyle(name='BodyW', parent=styles['Normal'], fontSize=9, leading=13, spaceAfter=5))
styles.add(ParagraphStyle(name='SourceW', parent=styles['Normal'], fontSize=8, leading=11, textColor=colors.HexColor('#135e75'), spaceAfter=3, wordWrap='CJK'))


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor('#dce3e8'))
    canvas.line(17*mm, 18*mm, A4[0]-17*mm, 18*mm)
    canvas.setFont('Helvetica-Bold', 8)
    canvas.setFillColor(colors.HexColor('#9d291e'))
    canvas.drawString(17*mm, 13*mm, 'INTERNAL WORKPAPER - NOT CLIENT-READY')
    canvas.setFillColor(colors.HexColor('#536477'))
    canvas.drawRightString(A4[0]-17*mm, 13*mm, str(doc.page))
    canvas.restoreState()


def p(text, style='BodyW'):
    return Paragraph(escape(text), styles[style])


def source(label, url):
    return Paragraph(f'{escape(label)}: <link href="{escape(url)}" color="#135e75">{escape(url)}</link>', styles['SourceW'])

story = []
for i, item in enumerate(DATA):
    if i: story.append(PageBreak())
    story += [p('INTERNAL EVIDENCE WORKPAPER', 'WarnW'), p(item['name'], 'TitleW'),
              p('HOLD: preliminary public-source observations only. Not a completed audit; no independent review or successful live-verification gate. Do not send to a lead.', 'WarnW'),
              p('Timing warning: the session date is 23 Nov 2026, but the sandbox clock reads 28 Nov and retrieved source data includes later-dated material. Active labels are what the fetched cards displayed, not verified as-of-date claims. Recheck using a trusted clock.', 'BodyW'),
              p('Observed evidence', 'SectionW')]
    for fact in item['facts']: story.append(p('• ' + fact))
    story.append(p('Checks to perform, not proven problems', 'SectionW'))
    for action in item['actions']: story.append(p('• ' + action))
    story += [p('Contact: ' + item['contact']), p('Source links', 'SectionW'), source('Captured ad card', item['ad']), source('Separately examined website', item['site'])]
    if item['name'].startswith('Galaxy'):
        story.append(source('Branch postcode comparison', 'https://galaxydentalcare.in/banjara-hills/'))
    story += [Spacer(1, 3*mm), p('Not checked: complete ad inventory, ad results, cost, tracking/event firing, Google Ads, speed metrics, form delivery or account setup. No scores are asserted. Independent report review and a passing live verifier are required before a client-ready audit.', 'BodyW')]

doc = SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=18*mm, leftMargin=18*mm, topMargin=15*mm, bottomMargin=23*mm, title='Telangana five - internal evidence workpaper')
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUT)
