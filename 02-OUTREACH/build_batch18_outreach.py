#!/usr/bin/env python3
"""Build the three batch-18 first-contact sequences: KehanSri, Hysun, V1.

Run from the repo root:
    PYTHONPATH=/tmp/pdflibs python3 02-OUTREACH/build_batch18_outreach.py

Mega Solar India and PNR Sunrise Energies are deliberately absent: neither
publishes an email address (Mega's only mailto links are example.com theme
placeholders; PNR's contact routes are a form, WhatsApp and a phone number),
so there is nothing to send to and no address has been invented.

Every figure in these bodies was read live on 2026-11-14 - the advertiser
records from Google's Ads Transparency Centre, the Meta Ad Library card, and
the page text saved under 01-LEADS/fetched/. Nothing is estimated, and the
caveat about the tracking rows is carried through into the email rather than
quietly dropped.

`BODIES` is stored verbatim, exactly as the text sits in the Gmail drafts:
prose paragraphs are single unwrapped lines, while the bullet list, the
verification URLs and the signature keep their own lines. Re-running this
script therefore reproduces the manifest and the .txt copies byte-for-byte
rather than re-wrapping them - the earlier hard-wrapped copy of these bodies
did not match what was actually in the drafts.
"""
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "02-OUTREACH", "generated_emails",
                        "sequence_manifest.json")
OUTDIR = os.path.join(ROOT, "02-OUTREACH", "generated_emails")
READ_ON = "2026-11-14"
SIG = ("Best,\nVamsi\nSmart Pursuit\n+91 70950 24220\n")

VERIFY = {
    "KehanSri Technologies & Service Pvt Ltd":
        "  https://adstransparency.google.com/advertiser/"
        "AR07894673884648046593?region=IN",
    "Hysun Solar Pvt. Ltd.":
        "  https://adstransparency.google.com/advertiser/"
        "AR08880526109242818561?region=IN",
    "V1 Solar Solutions":
        "  https://adstransparency.google.com/advertiser/"
        "AR09270299175948386305?region=IN\n"
        "  https://www.facebook.com/ads/library/?id=1446165934284837",
}

PDFS = {
    "KehanSri Technologies & Service Pvt Ltd":
        "audit_KehanSri_Technologies_Service_Pvt_Ltd.pdf",
    "Hysun Solar Pvt. Ltd.": "audit_Hysun_Solar_Pvt_Ltd_.pdf",
    "V1 Solar Solutions": "audit_V1_Solar_Solutions.pdf",
}

CONTACT_NOTES = {
    "KehanSri Technologies & Service Pvt Ltd":
        "Email and phone read live off kehansrisolar.com on 2026-11-14: "
        "info@kehansri.com, +91 888 628 6000 / +91 9985408601. Registered "
        "office 472, Rohit Nagar Phase-1, Bavadiakala, Bhopal 462039; "
        "operating address 2-55, Opposite Ingenium School, Sri Shyam Nagar, "
        "Telecom Nagar, Gachibowli, Hyderabad 500032. Founded 2016. Facebook "
        "https://www.facebook.com/kehansrisolar/.",
    "Hysun Solar Pvt. Ltd.":
        "Email read live off hysunsolar.com on 2026-11-14: "
        "info@hysunsolar.com, +91 7573999966 (site) / +91 7573999960 (Meta "
        "ads) / toll-free 1800-270-0025. Support address on their own Android "
        "app (com.HYSUN.HysunSolar) is infohysunsolar@gmail.com. The indexed "
        "contact page publishes 10 Radhekrishna Ind Hub, B/H Hinglaj Mata "
        "Mandir, Ahmedabad. NOTE: the site returned HTTP 500 on every path "
        "tried on 2026-11-14, so these details come from a search-engine "
        "snapshot of the live pages, not a direct read.",
    "V1 Solar Solutions":
        "Email and phone read live off v1solarsolutions.com on 2026-11-14: "
        "info@v1solarsolutions.com, +91 9066631441. 7, Magadi Main Rd, "
        "Asthagrama Layout, Kamakshipalya, Bengaluru 560079, Karnataka. "
        "Proprietor Mr Vijaykumar. GST 29DPTPK0093G1ZF. A second, misspelled "
        "domain v1solarsolutuons.in carries their IndiaMART manufacturer "
        "listing. Meta ads are run by the agency 99Ad Solutions.",
}

SUBJECTS = {
    "KehanSri Technologies & Service Pvt Ltd":
        "KehanSri: 24 live Google ads landing on a page with injected casino spam",
    "Hysun Solar Pvt. Ltd.":
        "Hysun Solar: your website returns HTTP 500, and your contact page is in Ahmedabad",
    "V1 Solar Solutions":
        "V1 Solar: no sitemap at all, and the same business on two spellings",
}

BODIES = {
    'KehanSri Technologies & Service Pvt Ltd': """Hi,

I spend my week reading the public ad-transparency records for the Hyderabad solar market, and I put together a full audit of your website against what your paid traffic is actually doing.

What it covers (read live on 2026-11-14):

  - 24 live ads under your advertiser record, identity-verified as KehanSri Technologies & Service Pvt Ltd - the largest live Google ad count I found in this sweep, spanning Display image creatives and a YouTube video
  - every click lands on kehansrisolar.com, a domain you own, which already puts you ahead of most of the installers I write to

So the spend is not the problem. The page it lands on is.

Your homepage carries injected casino spam. There are long blocks of Polish and German online-casino copy sitting between your services section and your projects carousel, with six outbound links, all of them to quora.com "unanswered" pages - pl.quora.com, de.quora.com and quora.com. The headings read "Najlepsze oferty na start dla nowych graczy", "Faszination der digitalen Glucksspiele" and "Wie Sie seriose und sichere Plattformen im Internet erkennen", and the link text includes "kasyna z bonusem bez depozytu za rejestracje" and "neue online casino vodds". That is a WordPress SEO-spam injection, and it is on the page 24 paid ads are pointing at.

The timing tells you how it got in. Every post in your sitemap is dated between 9 and 13 November 2026 - 156 of them, all created inside that five-day window. That is not editorial output; that is the injection mechanism.

The second thing is stranger. Your contact page embeds a live Google Map with a 4.9 rating across 131 reviews - and the embed URL carries gcid:preschool, with the listing named "Ingenium Foundation School Gachibowli". The star rating shown beside your solar enquiry form belongs to a school.

Third, five of your "Read More" buttons - Roof Top, Ground Mounted, Operation & Maintenance, Project Management and EPC & Development - point at www.wpstage.a2hosted.com/1411/kehanSri/, a different machine from the live site. And the header "Get a Quote" and "Contact Us" both go to kehansrisolar.com/kehanSri/contact-us/, a staging subdirectory on the live domain. A visitor who wants a quote is being sent to a staging path.

On the page itself: there is no H1 anywhere on the homepage (ten H2 headings and no H1 at all), no enquiry form on either page I read, and 24 of the 26 images on the homepage carry no alt text - four of them with a literal alt="null". The four testimonials in your sitemap are still named tiffany-brown-seven-media-group, max-freewind-seven-commerce, miriam-blackwood-seven-beauty-studio and richard-berrington-seven-education, which is the theme's placeholder content. /sample-page/ and /the7-web-master-home/ are both live and indexed, and your sizing table still prices 300 Wp and 320 Wp modules.

To be fair to you, the substance underneath is real: eight named projects from 10 kW to 5 MW - 10/35/45/50 KW and 5 MW in Hyderabad, 1.5 MW in Kolar, 100 KW in Mumbai, 1 MW in Ujjain - a published email, a click-to-call number, a live embedded map, a Gachibowli address with a Bhopal registered office, and a founding date of 2016. That is more proof than most of the Hyderabad installers I look at can show.

One honest caveat on the audit: I could not read your tracking tags. The page HTML source was not retrievable from where I work, so all eight tracking rows read "not checked" rather than "missing" - I am not going to claim a pixel is absent when I did not see the source. That is the first thing worth verifying once the injection is cleaned out.

You can verify every line yourself:

  https://adstransparency.google.com/advertiser/AR07894673884648046593?region=IN

Happy to walk you through what I found on a 10-minute call - or just keep the report, no strings attached.

Best,
Vamsi
Smart Pursuit
+91 70950 24220""",
    'Hysun Solar Pvt. Ltd.': """Hi,

I spend my week reading the public ad-transparency records for the Hyderabad solar market, and I put together an audit of your paid presence against your website.

What it covers (read live on 2026-11-14):

  - 1 live ad under your advertiser record, identity-verified as Hysun Solar pvt ltd, pointing at hysunsolar.com
  - live Meta ads selling the Rs.78,000 PM Surya Ghar subsidy to Hyderabad homeowners, on-grid / off-grid / hybrid systems and EMI

You are on both paid channels, which most of the installers I write to are not. So I will be direct about the split, because it is the whole story.

Every Meta click is captured inside a WhatsApp chat or a Facebook lead form. Not one of them reaches hysunsolar.com. The Google click does reach your site - so the same brand is being sold through two completely different funnels, and only one of them leaves you anything you own.

The second thing is the one that costs you money. Your website could not be read at all: every path I tried - the homepage, /contact-us/ and /index.html - returned HTTP 500. Whatever is serving that domain is erroring for non-browser clients. It is not a dead domain, because Google's crawler clearly reaches it and your ads are live, but anything built on top of it cannot be checked, and I would want to know about it before the next ad runs.

Third, the pages that are indexed publish an Ahmedabad address - 10 Radhekrishna Ind Hub, B/H Hinglaj Mata Mandir - under ads that target Suncity, Bandlaguda Jagir, Hyderabad 500091. And there are three contact routes with two different phone numbers: info@hysunsolar.com on the site, +91 7573999966 on the site, and +91 7573999960 on the Meta ads. Your own Android app lists infohysunsolar@gmail.com as its support address, which is a fourth route.

To be fair to you, there is real infrastructure here that no ad mentions: a toll-free number (1800-270-0025) published alongside the direct line, and a live Android app with one-tap service requests and panel-cleaning booking. That is an after-sales operation most rooftop installers never build.

Because the site could not be retrieved, the audit claims no score for it - the report says so on page 1, and every website row reads "not checked in this pass" rather than being filled with a guess. I would rather hand you a report that says what it does not know than one that invents a number.

You can verify every line yourself:

  https://adstransparency.google.com/advertiser/AR08880526109242818561?region=IN

Happy to walk you through what I found on a 10-minute call - or just keep the report, no strings attached.

Best,
Vamsi
Smart Pursuit
+91 70950 24220""",
    'V1 Solar Solutions': """Hi,

I spend my week reading the public ad-transparency records for the solar market, and I put together a full audit of your website against what your paid traffic is doing.

What it covers (read live on 2026-11-14):

  - 4 live ads under your advertiser record, identity-verified as VIJAYA KUMAR, all pointing at v1solarsolutions.com
  - 1 live Meta ad, Library ID 1446165934284837, running since 12 October 2026 and run by the agency 99Ad Solutions, selling solar water-heater repair, servicing and installation across Bengaluru and Hyderabad

You are the only lead in this sweep advertising on both channels with a published email address, so the plumbing is there. Two things are quietly costing you the Hyderabad traffic you are already paying for.

The Meta ad ends in a WhatsApp chat - api.whatsapp.com, not your site. No form, no email capture, nothing to follow up on if the conversation goes cold. And that ad is the only thing putting you in front of Hyderabad at all; the four Google ads all point at a site whose address is in Bengaluru.

Second, you have no sitemap. v1solarsolutions.com/sitemap.xml returns the homepage HTML - the path is rewritten, so search engines have nothing to crawl. That is the single cheapest fix on this list.

Third, the same business exists on two spellings. v1solarsolutuons.in carries your IndiaMART manufacturer listing while v1solarsolutions.com is the real site. Two domains, two presentations, one phone number - and your links, search authority and tracking are split across both.

On the page itself: there are two H1 tags, and the second one reads "COMMECIAL RO PLANT" - the product is misspelled in your main heading. The water-heater paragraph opens "choos V1 Solar". Seven of the eight images on the homepage carry no alt text. Your Google rating is 1.0 from 2 reviews, against an ad that leans on "expert technicians" and "prompt doorstep service". And the three testimonials - "Great Benefits!", "Reduced Bills" and "Money Saver" - each carry a quote but no name, city or system size, so there is nothing a prospect can check.

To be fair to you, the site works: a quote form on the contact page that captures product type before the callback, a click-to-call number on every page, a Google Maps link, and info@v1solarsolutions.com published where people can find it. That is a better foundation than most of what I look at.

One honest caveat: I could not read your tracking tags. The page HTML source was not retrievable from where I work, so all eight tracking rows read "not checked" rather than "missing". With four Google ads running, that is the first thing I would verify.

You can verify every line yourself:

  https://adstransparency.google.com/advertiser/AR09270299175948386305?region=IN
  https://www.facebook.com/ads/library/?id=1446165934284837

Happy to walk you through what I found on a 10-minute call - or just keep the report, no strings attached.

Best,
Vamsi
Smart Pursuit
+91 70950 24220""",
}

ROWS = [
    {"name": "KehanSri Technologies & Service Pvt Ltd",
     "city": "Gachibowli, Hyderabad", "website": "https://kehansrisolar.com/",
     "email": "info@kehansri.com"},
    {"name": "Hysun Solar Pvt. Ltd.",
     "city": "Suncity, Bandlaguda Jagir, Hyderabad",
     "website": "https://www.hysunsolar.com",
     "email": "info@hysunsolar.com"},
    {"name": "V1 Solar Solutions",
     "city": "Kamakshipalya, Bengaluru (advertising into Hyderabad)",
     "website": "https://www.v1solarsolutions.com/",
     "email": "info@v1solarsolutions.com"},
]


def write_txt_files():
    """One reviewable .txt per lead, matching the ads_only_email_*.txt format."""
    written = []
    for row in ROWS:
        name = row["name"]
        slug = "".join(c if c.isalnum() else "_" for c in name)[:48].strip("_")
        path = os.path.join(OUTDIR, "batch18_email_%s.txt" % slug)
        with io.open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write("=== EMAIL FOR: %s ===\n" % name)
            f.write("City: %s\n" % row["city"])
            f.write("To: %s\n" % row["email"])
            f.write("Phone: %s\n" % {
                "KehanSri Technologies & Service Pvt Ltd":
                    "+91 888 628 6000 / +91 9985408601",
                "Hysun Solar Pvt. Ltd.": "+91 7573999966 / 1800-270-0025",
                "V1 Solar Solutions": "+91 9066631441",
            }[name])
            f.write("Website: %s\n" % row["website"])
            f.write("Report kind: FULL AUDIT (5-page DIGITAL MARKETING & PAID "
                    "ADS AUDIT, attached)\n")
            f.write("ATTACH THIS: %s\n"
                    % os.path.join(ROOT, "02-OUTREACH", "audit_pdfs",
                                   PDFS[name]))
            f.write("Template: full_audit_first_contact\n")
            f.write("Read on: %s\n" % READ_ON)
            f.write("\n--- SUBJECT ---\n%s\n" % SUBJECTS[name])
            f.write("\n--- BODY ---\n%s\n" % BODIES[name])
            f.write("\n--- END ---\n")
        written.append(path)
        print("  wrote %s" % os.path.basename(path))
    return written


def update_manifest():
    with io.open(MANIFEST, encoding="utf-8") as f:
        man = json.load(f)
    seqs = man["sequences"]
    have = {s["company"] for s in seqs}
    print("manifest: %d existing sequences" % len(seqs))
    added = 0
    for row in ROWS:
        name = row["name"]
        if name in have:
            print("  = %s already present, skipping" % name)
            continue
        subject = SUBJECTS[name]
        seqs.append({
            "city": row["city"],
            "company": name,
            "contact_note": CONTACT_NOTES[name],
            "mails_sent": 0,
            "next_followup_date": "",
            "next_step": None,
            "report_kind": "full_audit",
            "steps": [{
                "body": BODIES[name],
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
        })
        added += 1
        print("  + %s -> %s" % (name, row["email"]))
    with io.open(MANIFEST, "w", encoding="utf-8") as f:
        json.dump(man, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("manifest: now %d sequences (+%d)" % (len(seqs), added))
    return added


def main():
    print("=" * 66)
    print("BATCH-18 FIRST-CONTACT SEQUENCES - bodies read live %s" % READ_ON)
    print("Mega Solar India and PNR Sunrise Energies publish no email address,")
    print("so no sequence is created for either. Nothing is invented.")
    print("=" * 66)
    write_txt_files()
    print()
    update_manifest()
    print("\nDraft IDs are filled in after the Gmail drafts are created.")


if __name__ == "__main__":
    sys.exit(main())
