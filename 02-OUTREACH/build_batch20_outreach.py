#!/usr/bin/env python3
"""Build the two batch-20 first-contact sequences: Meissa Reeve, Visiontek.

Run from the repo root:
    PYTHONPATH=/tmp/pdflibs python3 02-OUTREACH/build_batch20_outreach.py

Both leads now have a full audit, so these are full_audit sequences and the
attached report is the DIGITAL MARKETING & PAID ADS AUDIT - not the ads-only
report, which stays in 02-OUTREACH/ads_only_pdfs/ as the ad evidence.

Every figure in these bodies was read live on 2026-11-15 and is re-derivable
from 01-LEADS/fetched/. Two things are deliberately carried through rather than
dropped:

  - the eight tracking rows are "not checked in this pass", not "missing",
    because the page HTML source was never available - only rendered text;
  - the Visiontek ad-destination breakdown is five to a bare instagram.com
    root, five with no outbound link and one on fb.me. An earlier draft of the
    audit said six and four; that was wrong and is corrected in the report
    before this email was written, because quoting a wrong number to a
    prospect is worse than quoting nothing.

`BODIES` is stored verbatim, exactly as the text sits in the Gmail drafts:
prose paragraphs are single unwrapped lines, while the bullet list, the
verification URLs and the signature keep their own lines. Re-running this
script therefore reproduces the manifest and the .txt copies byte-for-byte.
"""

import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "02-OUTREACH"))

MANIFEST = os.path.join(ROOT, "02-OUTREACH", "generated_emails",
                        "sequence_manifest.json")
OUTDIR = os.path.join(ROOT, "02-OUTREACH", "generated_emails")
AUDIT_DIR = os.path.join(ROOT, "01-LEADS", "audit_results")
PDF_DIR = os.path.join(ROOT, "02-OUTREACH", "audit_pdfs")

READ_ON = "2026-11-15"

VERIFY = {
    "Meissa Reeve": [
        "  https://www.facebook.com/ads/library/?id=1641050694153685",
        "  https://adstransparency.google.com/?domain=meissareeve.com&region=IN",
    ],
    "Visiontek Solar Energy": [
        "  https://www.facebook.com/ads/library/?active_status=active&ad_type=all"
        "&country=IN&q=Visiontek%20Solar%20Energy",
        "  https://adstransparency.google.com/?domain=visiontek.solar&region=IN",
    ],
}

PDFS = {
    "Meissa Reeve": "audit_Meissa_Reeve.pdf",
    "Visiontek Solar Energy": "audit_Visiontek_Solar_Energy.pdf",
}

CONTACT_NOTES = {
    "Meissa Reeve":
        "Read live off meissareeve.com/contacts/ on 2026-11-15: "
        "info@meissareeve.com and +91-7893088071, both published as plain text "
        "rather than tel:/mailto: links, so neither is tappable on a phone. "
        "Meissa Reeve Pvt. Ltd., 12-2-727/1/57, Sapthagiri Nagar Colony, "
        "Rethibowli, Gudimalkapur, Hyderabad 500006; Mon-Fri 09:00-17:00. A "
        "second inbox, enquiry@meissareeve.com, is published on the solar "
        "division at re.meissareeve.com. The embedded Google rating is 4.8 "
        "from 24 reviews and carries Google's own \"Reviews aren't verified\" "
        "note. The map address and the written address differ.",
    "Visiontek Solar Energy":
        "Read live off visiontek.solar/contact-us/ on 2026-11-15: "
        "info@visiontek.com and +91 9701601421, both as real tappable links. "
        "VISIONTEK Linkwell Telesystems Pvt. Ltd., 1-11-252/1B, Behind "
        "Shoppers' Stop, Begumpet, Hyderabad 500016. Corporate site is "
        "visiontek.co.in (founded 1993); the solar division site visiontek.solar "
        "is the one the ads point at. Meta page is 'Visionteknewenergy'.",
}

SUBJECTS = {
    "Meissa Reeve":
        "Meissa Reeve: your sitemap still publishes 36 theme-demo pages, and "
        "your one live ad clicks into WhatsApp",
    "Visiontek Solar Energy":
        "Visiontek: 11 live Meta ads, and not one of them links to "
        "visiontek.solar",
}

BODIES = {
    'Meissa Reeve': """Hi,

I spend my week reading the public ad-transparency records for the Hyderabad solar market, and I put together a full audit of your website against what your paid traffic is actually doing.

What it covers (read live on 2026-11-15):

  - 1 live ad on the page 'Meissa Reeve' (facebook.com/61596697943588), Library ID 1641050694153685, started 14 Nov 2026
  - 0 ads under meissareeve.com in Google Ads Transparency under region=IN, so Meta is your entire paid channel

So the spend is not the problem. There is one creative doing one job. The page behind it is where the work is.

The first thing I found is on the parent domain, and it is the one I would fix today. Your sitemap at meissareeve.com/sitemap_index.xml lists 17 sub-sitemaps, and page-sitemap.xml alone contains 80 page URLs. 36 of them are untouched theme demo content: /my-account/, /checkout/, /cart/, three gallery layouts, fifteen /elements/* pages, /404-layout/, /multipage/, /shop/, four complete demo homepages - /homepage-gas-station/, /homepage-rental/, /homepage-towing/ and /homepage-natural-honey/ - product pages for three EV scooter brands (/komaki/, /gemopai/, /virtus-motors/), /petrol-pumps/, /airport-metros/, /news/, /events-company/ and /videos/. A prospect who follows a link can land on a page selling petrol pumps. All of it is in the sitemap, so all of it is indexable. Five raw image URLs are listed in the sitemap as entries too, which is the same misconfiguration.

The second is that your ad's click goes to a WhatsApp deep link, never to meissareeve.com. That is a deliberate choice and it works, but it means the website is doing no work at all for the one campaign you are running - there is nothing on the other end of the click except a chat.

Third, on the contact page: your phone number and email are published as plain text, not as links. +91-7893088071 and info@meissareeve.com are both there to read, but a mobile visitor cannot tap either one.

To be fair to you, the solar division is the competent half. re.meissareeve.com carries 44 images with only 3 missing alt text, twelve named installations with locality and system size - Anees 2kW Moula Ali, Dr. Kasi 3 kW R K Puram, Om Prakash 4 kW Balnagar, Uma Shankar 3 kW Begumpet, Sahifa Masjid 10 kW, 17 kW Shad Nagar, 50 kW Tamil Nadu, 88 kW Choutupal - a 4.8-star Google rating from 24 reviews, and a real Contact Form 7 form with a full postal address and business hours. That is more proof than most Hyderabad installers can show.

The gap between the two halves is the whole story: the division that sells has no way for a visitor to act - its homepage has 50 links and not one of them is a button - and the domain that hosts it is publishing 36 pages of demo content. The parent homepage has no H1 at all and 10 of its 12 images carry no alt text.

One honest caveat: I could not read your tracking tags. The page HTML source was not retrievable from where I work, so all eight tracking rows in the report read "not checked in this pass" rather than "missing". I am not going to claim a pixel is absent when I did not see the source.

You can verify every line yourself:

  https://www.facebook.com/ads/library/?id=1641050694153685
  https://adstransparency.google.com/?domain=meissareeve.com&region=IN

Happy to walk you through what I found on a 10-minute call - or just keep the report, no strings attached.

Best,
Vamsi
Smart Pursuit
+91 70950 24220""",
    'Visiontek Solar Energy': """Hi,

I spend my week reading the public ad-transparency records for the Hyderabad solar market, and I put together a full audit of your website against what your paid traffic is actually doing.

What it covers (read live on 2026-11-15):

  - 11 distinct live creatives on the page 'Visionteknewenergy', every one started 12 Nov 2026 except a Diwali creative from 6 Nov 2026
  - 0 ads under visiontek.solar in Google Ads Transparency under region=IN, so Meta is your entire paid channel

Eleven creatives launched in a single coordinated push is a fresh, actively managed account - and it makes the next finding sharper, because none of that spend is reaching your site.

Not one of the eleven carries a visiontek.solar link. Five send the click to a bare instagram.com root, five carry no outbound link at all, and one goes to an fb.me short link. A click on instagram.com lands on the Instagram home feed - not a profile, not a post, not a message thread - so that traffic has nowhere to go and cannot be attributed to anything. Only the fb.me creative resolves to something you own, and that is a Facebook short link.

The second thing is that there is no sitemap and no robots.txt. Both visiontek.solar/sitemap.xml and visiontek.solar/robots.txt return 404 Page Not Found, on a domain with a product catalogue, a blog and individual product pages.

Third, every social link on your contact page is a dead anchor. All four icons - Facebook, Twitter, LinkedIn and Instagram - point at contact-us#, the page they are already on. That includes the Facebook page where the eleven ads actually run.

And the catalogue download does not download a catalogue: "Download Catalogue (PDF, 1.2 MB)" links to product#, which is the current page. There is no PDF behind it.

To be fair to you, the site itself is in genuinely good shape - better than most of what I look at. Every image carries alt text across the three pages I read (12 on the homepage, 6 on contact, 14 on product), each page has exactly one H1, the contact page has a tappable tel: link and a tappable mailto: link plus a working form with a SEND ENQUIRY button, WhatsApp is on every page, and your blog has posts dated 11 and 12 November 2026. The homepage advertises four of your six product lines. A broken video element is printing "Your browser does not support video." into the page body, and the PULSE+ category block is headed "Nexus+" - a copy-paste slip worth a two-minute fix.

So the substance is there. What is missing is the plumbing between eleven live ads and the site they are supposed to feed.

One honest caveat: I could not read your tracking tags. The page HTML source was not retrievable from where I work, so all eight tracking rows in the report read "not checked in this pass" rather than "missing". I am not going to claim a pixel is absent when I did not see the source.

You can verify every line yourself:

  https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=IN&q=Visiontek%20Solar%20Energy
  https://adstransparency.google.com/?domain=visiontek.solar&region=IN

Every one of the 11 Library IDs is printed in the attached report, next to the link that opens it.

Happy to walk you through what I found on a 10-minute call - or just keep the report, no strings attached.

Best,
Vamsi
Smart Pursuit
+91 70950 24220""",
}

ROWS = [
    {"name": "Meissa Reeve", "city": "Mehdipatnam, Hyderabad",
     "website": "https://meissareeve.com/", "email": "info@meissareeve.com",
     "phone": "+91 7893088071", "legal": "Meissa Reeve Pvt. Ltd."},
    {"name": "Visiontek Solar Energy", "city": "Begumpet, Hyderabad",
     "website": "https://visiontek.solar/", "email": "info@visiontek.com",
     "phone": "+91 9701601421",
     "legal": "VISIONTEK Linkwell Telesystems Pvt Ltd"},
]


def slug(name):
    return "".join(c if c.isalnum() else "_" for c in name)[:48].strip("_")


def write_txt_files():
    written = []
    for row in ROWS:
        name = row["name"]
        path = os.path.join(OUTDIR, "batch20_email_%s.txt" % slug(name))
        with io.open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write("=== EMAIL FOR: %s ===\n" % name)
            f.write("City: %s\n" % row["city"])
            f.write("To: %s\n" % row["email"])
            f.write("Phone: %s\n" % row["phone"])
            f.write("Website: %s\n" % row["website"])
            f.write("Legal entity: %s\n" % row["legal"])
            f.write("Report kind: FULL AUDIT (DIGITAL MARKETING & PAID ADS "
                    "AUDIT, attached)\n")
            f.write("ATTACH THIS: %s\n"
                    % os.path.join(PDF_DIR, PDFS[name]))
            f.write("Template: full_audit_first_contact\n")
            f.write("Read on: %s\n" % READ_ON)
            f.write("\n--- SUBJECT ---\n%s\n" % SUBJECTS[name])
            f.write("\n--- BODY ---\n%s\n" % BODIES[name])
            f.write("\n--- VERIFY URLS ---\n%s\n"
                    % "\n".join(VERIFY[name]))
            f.write("\n--- CONTACT NOTE ---\n%s\n" % CONTACT_NOTES[name])
            f.write("\n--- END ---\n")
        written.append(path)
        print("  wrote %s" % os.path.basename(path))
    return written


def update_manifest():
    from sequence import upsert_sequence

    with io.open(MANIFEST, encoding="utf-8") as f:
        man = json.load(f)
    print("manifest: %d existing sequences" % len(man["sequences"]))

    added = 0
    for row in ROWS:
        name = row["name"]
        audit_file = os.path.join(AUDIT_DIR, "audit_%s.json" % slug(name))
        if not os.path.exists(audit_file):
            # slug() collapses non-alphanumerics, the audit filenames do too,
            # but be explicit rather than silently skipping a lead.
            cands = [p for p in os.listdir(AUDIT_DIR)
                     if p.startswith("audit_") and p.endswith(".json")
                     and name.split()[0].lower() in p.lower()]
            if len(cands) != 1:
                print("  ! cannot resolve the audit JSON for %r (%s)"
                      % (name, cands))
                continue
            audit_file = os.path.join(AUDIT_DIR, cands[0])
        with io.open(audit_file, encoding="utf-8") as f:
            audit = json.load(f)

        existing = any(s["company"].lower() == name.lower()
                       for s in man["sequences"])
        seq = upsert_sequence(man, row, audit,
                              SUBJECTS[name], BODIES[name], ads_only=False)
        seq["contact_note"] = CONTACT_NOTES[name]
        if not existing:
            added += 1
            print("  + %s -> %s (score %s/100, %d issues)"
                  % (name, row["email"], audit["score"]["score"],
                     len(audit["score"]["issues"])))
        else:
            print("  = %s already present, refreshed in place" % name)

    with io.open(MANIFEST, "w", encoding="utf-8") as f:
        json.dump(man, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("manifest: now %d sequences (+%d)" % (len(man["sequences"]), added))
    return added


def main():
    print("=" * 66)
    print("BATCH-20 FIRST-CONTACT SEQUENCES - bodies read live %s" % READ_ON)
    print("Both leads have a full audit, so these are full_audit sequences")
    print("and the attached report is the 6/7-page DIGITAL MARKETING audit.")
    print("=" * 66)
    write_txt_files()
    print()
    update_manifest()
    print("\nDraft IDs are filled in after the Gmail drafts are created.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
