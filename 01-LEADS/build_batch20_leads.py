"""Batch 20 - solar Hyderabad, 2026-11-15 (second discovery run of the day).

Durable, re-runnable record of what was written into the pipeline for batch 20.
Every write is guarded by a duplicate assertion, so running this twice changes
nothing the second time.

  python3 build_batch20_leads.py            # dry run, prints what it would do
  python3 build_batch20_leads.py --write    # apply

What it does, in order:
  1. appends the 2 new lead rows to leads.csv (CRLF preserved, duplicate names
     refused, column count checked)
  2. appends the 25 batch-20 vetoes to known_leads_extra.json
  3. appends the 3 batch-20 `known` entries (the two guard gaps found this run)
  4. re-runs the duplicate guard over feeds/solar_hyderabad_2026-11-15_batch20.json
     and asserts it reports 0 new advertisers

Gate values used: live-ads, published-email, segment.
"""

import csv
import io
import json
import subprocess
import sys

LEADS = 'leads.csv'
EXTRA = 'known_leads_extra.json'
FEED = 'feeds/solar_hyderabad_2026-11-15_batch20.json'

HEADER = ['name', 'city', 'website', 'email', 'phone', 'snippet',
          'audit_score', 'audit_issues_count', 'status', 'added_date']

# ---------------------------------------------------------------- 1. new rows
NEW_ROWS = [
    [
        'Meissa Reeve',
        'Mehdipatnam, Hyderabad',
        'https://meissareeve.com/',
        'info@meissareeve.com',
        '+91 7893088071',
        (
            'Live Meta advertiser: 1 active ad on the "Meissa Reeve" page (Library ID 1691922249204293, '
            'started running 14 Nov 2026) - "Tired of your electricity bill going up every summer? Put your '
            'rooftop to work. Meissa Reeve designs and installs rooftop solar for homes across Hyderabad - so '
            'you generate your own power and cut your monthly bill. Free site visit & savings estimate; Help '
            'with the PM Surya Ghar subsidy process; End-to-end installation & net metering." Click lands on a '
            'WhatsApp deep link, never on the website. Contacts read live off the company\'s own site on '
            '2026-11-15 (third-eye re-verification): meissareeve.com/contacts/ publishes +91-7893088071 and '
            'info@meissareeve.com at Saptagiri Nagar, Retibowli, Mehdipatnam, Hyderabad. The solar division '
            'runs on re.meissareeve.com and sells residential, commercial, industrial and agricultural rooftop '
            'plants (on-grid / off-grid / hybrid) plus solar street lights, with named installations (Anees 2kW '
            'Moula Ali, Dr. Kasi 3kW R K Puram, Om Prakash 4kW Balnagar, Uma Shankar 3kW Begumpet). Parent site '
            'also runs EV charging stations and retrofitting divisions. Google Ads Transparency ?domain=meissareeve.com '
            'under region=IN returns 0 ads on 2026-11-15, so the live-ad evidence is Meta-only and is stated as such. '
            'Second inbox published on the solar division: enquiry@meissareeve.com.'
        ),
        '',
        '',
        'new',
        '2026-11-15',
    ],
    [
        'Visiontek Solar Energy',
        'Begumpet, Hyderabad',
        'https://visiontek.solar/',
        'info@visiontek.com',
        '+91 9701601421',
        (
            'Live Meta advertiser: 4 active ads on the "Visionteknewenergy" page - Library ID 1133037052650969 '
            '(12 Nov 2026, 2 ads use this creative), 1138341982459373 (12 Nov 2026, 2 ads use this creative), '
            '1449750756945639 (12 Nov 2026, 2 ads use this creative) and 2319725685441877 (4 Sep 2026) - '
            '"Still paying high electricity bills? Switch to Visiontek Solar and turn sunlight into savings. Our '
            'smart system powers your home directly, stores extra energy for the night and helps lower your '
            'monthly bill." Ad destination is a generic instagram.com link, so the ads drive no site traffic - '
            'a concrete finding for outreach. Contacts read live off the company\'s own site on 2026-11-15 '
            '(third-eye re-verification): visiontek.solar/contact-us/ publishes +91 9701601421 and '
            'info@visiontek.com at Linkwell Telesystems Pvt. Ltd., 1-11-252/1B, Behind Shoppers\' Stop, Begumpet, '
            'Hyderabad 500016. Solar division launched 2025 by VISIONTEK Linkwell Telesystems Pvt Ltd (founded '
            '1993, 32+ years of telecom and power-electronics manufacturing); product line RISE+ on-grid '
            'inverter, FUTURE+ hybrid inverter, VAULT+ LFP battery storage, PULSE+ panel-level optimiser. '
            'Google Ads Transparency ?domain=visiontek.solar under region=IN returns 0 ads on 2026-11-15, so the '
            'live-ad evidence is Meta-only and is stated as such. This is a solar inverter/storage manufacturer '
            'with a new solar division, not a rooftop EPC installer.'
        ),
        '',
        '',
        'new',
        '2026-11-15',
    ],
]

# ------------------------------------------------------------- 2. new vetoes
NEW_VETOES = [
    ("Ohmhydrasolutions", "", "Kerala", "2026-11-15", "segment",
     "Live Meta advertiser (Library ID 1160240256472893, started Nov 12 2026) but the ad is Malayalam-language electrical and plumbing work with KSEB connection assistance - a Kerala local-services business, not a Hyderabad/Telangana solar EPC."),
    ("Mocaup", "", "India (multi-city)", "2026-11-15", "segment",
     "Live Meta advertiser (Library ID 1540056057821006, started Aug 5 2026) but it resells solar enquiries to EPCs ('connecting Solar Vendors and EPC providers with property owners') - a lead-generation agency, not a solar EPC, and therefore a competitor rather than a prospect."),
    ("Alsaa D Global Real Estate", "https://www.alsaadglobalrealestate.com/", "Sangareddy", "2026-11-15", "segment",
     "Live Meta advertiser (Library ID 2160085101235277, started Aug 13 2026) but it is a real-estate investment scheme selling panel-ownership leases on the Kapil Solar Energy site at Sangareddy - not a solar EPC."),
    ("Go Rewatt", "https://www.gorewatt.com/", "Karnataka / Tamil Nadu", "2026-11-15", "segment",
     "Live Meta advertiser (Library ID 1498216172114493, started Sep 30 2026) but the ad recruits distributors for South India with priority markets Karnataka and Tamil Nadu - not a Hyderabad solar EPC."),
    ("BoxBee - Buzzing Deal Every Day", "https://boxbee.in/", "India (e-commerce)", "2026-11-15", "segment",
     "Live Meta advertiser (Library ID 990388019982431, started Oct 16 2026) but it sells a Rs.1,999 solar-panel cleaning brush - an e-commerce product ad, not a solar EPC."),
    ("SunSolarhyd", "", "Narsingi, Hyderabad", "2026-11-15", "published-email",
     "Live Meta advertiser with 3 active ads on the 'SunSolarhyd' page (Library IDs 2576227376137902 and 2285688872164421, Oct 2026, plus a third Oct 23 2026 creative): 'HYDERABAD, SWITCH TO SOLAR FOR JUST Rs.1,31,999' with Suite 312, 3rd Floor, Kokapet Terminal Complex, Gandipet Main Road, Narsingi, Hyderabad and +91 98666 02001. No email address is published anywhere the ads or the company point to, and the domain could not be identified - sunsolarpowersystems.com is a different, Ramanathapuram-based business. Fails the published-email gate."),
    ("Sirius Solar Energy Systems", "https://siriussolarenergy.com/", "Hyderabad", "2026-11-15", "live-ads",
     "0 live Google ads (Ads Transparency Centre, region=IN, domain=siriussolarenergy.com) and 0 Meta ads (keyword sweep 'Sirius Solar Energy' returned 'No ads match your search criteria'). PM Surya Ghar vendor with marketing@siriussolarenergy.com, but no live advertising to pitch against."),
    ("Greentek India Pvt Ltd", "https://greentekindia.co.in/", "Hyderabad", "2026-11-15", "live-ads",
     "0 live Google ads (Ads Transparency Centre, region=IN, domain=greentekindia.co.in) and 0 Meta ads (keyword sweep 'Greentek India solar' returned 'No ads match your search criteria'). PM Surya Ghar vendor with projects@greentekindia.co.in, but no live advertising. Distinct from Greentek Solutions (greentecksolutions.com, Borabanda), which also has 0 live ads."),
    ("Gigawatt Solar Pvt Ltd", "https://gigawattsolar.in/", "Hyderabad", "2026-11-15", "live-ads",
     "0 live Google ads (Ads Transparency Centre, region=IN, domain=gigawattsolar.in). PM Surya Ghar vendor with info@gigawattsolar.in."),
    ("Solar Idea Pvt Ltd", "https://solaridea.com/", "Hyderabad", "2026-11-15", "live-ads",
     "0 live Google ads (Ads Transparency Centre, region=IN, domain=solaridea.com). PM Surya Ghar vendor with info@solaridea.com."),
    ("Zytech Solar India Pvt Ltd", "https://zytechsolar.co.in/", "Hyderabad", "2026-11-15", "live-ads",
     "0 live Google ads (Ads Transparency Centre, region=IN, domain=zytechsolar.co.in). PM Surya Ghar vendor with aadesh@zytechsolar.co.in."),
    ("Amplus KN One Power Pvt Ltd", "https://amplussolar.com/", "Hyderabad", "2026-11-15", "live-ads",
     "0 live Google ads (Ads Transparency Centre, region=IN, domain=amplussolar.com). PM Surya Ghar vendor with rohit.khanduja@amplussolar.com."),
    ("Solar Bull Enegy LLP", "https://solarbull.in/", "Hyderabad", "2026-11-15", "live-ads",
     "0 live Google ads (Ads Transparency Centre, region=IN, domain=solarbull.in). PM Surya Ghar vendor with srini@solarBull.in."),
    ("NATURAL ENERGIES", "https://naturalenergies.in/", "Hyderabad", "2026-11-15", "live-ads",
     "0 live Google ads on naturalenergies.in and 0 on naturalenergiess.com (Ads Transparency Centre, region=IN, both probed). PM Surya Ghar vendor with info@naturalenergies.in."),
    ("Nova Solar Solutions SecBad", "https://novasolar.in/", "Secunderabad", "2026-11-15", "live-ads",
     "0 live Google ads (Ads Transparency Centre, region=IN, domain=novasolar.in). PM Surya Ghar vendor with john@novasolar.in."),
    ("Renew Solar", "https://renewsolar.in/", "Hyderabad", "2026-11-15", "live-ads",
     "0 live Google ads (Ads Transparency Centre, region=IN, domain=renewsolar.in). PM Surya Ghar vendor with kalyan@renewsolar.in."),
    ("Accutech Infosystems Pvt Ltd", "https://accutech.co.in/", "Hyderabad", "2026-11-15", "live-ads",
     "0 live Google ads (Ads Transparency Centre, region=IN, domain=accutech.co.in). PM Surya Ghar vendor with vidyasagar@accutech.co.in."),
    ("Coolkaru Info Solutions Pvt Ltd", "https://coolkaru.com/", "Hyderabad", "2026-11-15", "live-ads",
     "0 live Google ads (Ads Transparency Centre, region=IN, domain=coolkaru.com). PM Surya Ghar vendor with prudhvi@coolkaru.com."),
    ("E Mug Energy Pvt Ltd", "https://emugenergy.com/", "Hyderabad", "2026-11-15", "live-ads",
     "0 live Google ads (Ads Transparency Centre, region=IN, domain=emugenergy.com). PM Surya Ghar vendor with ksr@emugenergy.com."),
    ("SUN ENERGY SYSTEMS", "https://sunenergysystems.com/", "Hyderabad", "2026-11-15", "live-ads",
     "0 live Google ads (Ads Transparency Centre, region=IN, domain=sunenergysystems.com). PM Surya Ghar vendor with bvrao@sunenergysystems.com."),
    ("CubeFore Solutions Pvt Ltd", "https://cubeforesolutions.in/", "Hyderabad", "2026-11-15", "live-ads",
     "0 live Google ads (Ads Transparency Centre, region=IN, domain=cubeforesolutions.in). PM Surya Ghar vendor with info@cubeforesolutions.in."),
    ("Suntek Energy Systems Pvt Ltd", "https://suntek.co.in/", "Hyderabad", "2026-11-15", "live-ads",
     "Re-probed 2026-11-15 under region=IN: still 0 live Google ads. Already vetoed 2026-11-14; kept so the probe is not repeated."),
    ("Sunup Solar Power", "https://sunupsolarpower.com/", "Domalguda, Hyderabad", "2026-11-15", "live-ads",
     "0 live Google ads (Ads Transparency Centre, region=IN, domain=sunupsolarpower.com). Publishes santosh@sunupsolarpower.com and +91 888 505 2521, but no live advertising."),
    ("Sunpower Solar Solutions", "https://sunpowersolarsolutions.com/", "Boduppal, Hyderabad", "2026-11-15", "live-ads",
     "0 live Google ads (Ads Transparency Centre, region=IN, domain=sunpowersolarsolutions.com). Publishes info@sunpowersolarsolutions.com and +91 8885551536 / 7674899302, but no live advertising."),
    ("Sunpower Solar Services", "https://sunpowersolarservices.co.in/", "Nagole, Hyderabad", "2026-11-15", "live-ads",
     "0 live Google ads (Ads Transparency Centre, region=IN, domain=sunpowersolarservices.co.in). Publishes sunpowersolarservice@gmail.com, but no live advertising."),
    ("Sun Solar Systems", "https://sunsolarsystems.in/", "Turkayamjal, Ranga Reddy", "2026-11-15", "live-ads",
     "0 live Google ads (Ads Transparency Centre, region=IN, domain=sunsolarsystems.in). Publishes info@sunsolarsystems.in and +91 9281259430, but no live advertising. Distinct from sunsolarps.com (Ramanathapuram) and from the Hyderabad SunSolarhyd Meta advertiser."),
]

# --------------------------------------------------- 3. new `known` entries
NEW_KNOWN = [
    ("Visionteknewenergy", "https://visiontek.solar/", "Begumpet, Hyderabad",
     "Meta Ad Library page name for Visiontek Solar Energy (visiontek.solar, info@visiontek.com, +91 9701601421). Rowed in leads.csv 2026-11-15. Added because 'Visionteknewenergy' is a single concatenated token, so the guard's token matcher cannot link it to 'Visiontek Solar Energy' - exactly the class of miss fixed for 'Telangana Solar' on 2026-11-15."),
    ("FreyrEnergy", "https://www.freyrenergy.com/", "Hyderabad",
     "Meta Ad Library page name for Freyr Energy (lead 34 in leads.csv, service@freyrenergy.com). Added because 'FreyrEnergy' is one concatenated token and 'Energy' is non-identifying, so the matcher sees zero identifying shared tokens."),
    ("Visiontek Solar", "https://visiontek.solar/", "Begumpet, Hyderabad",
     "Short form used inside the ad copy ('Switch to Visiontek Solar') for Visiontek Solar Energy. Rowed in leads.csv 2026-11-15."),
]


def do_leads(write):
    raw = open(LEADS, 'rb').read()
    assert raw.endswith(b'\r\n'), 'leads.csv must end with CRLF'
    rows = list(csv.reader(io.StringIO(raw.decode('utf-8'))))
    header, body = rows[0], rows[1:]
    assert header == HEADER, f'unexpected header: {header}'
    names = [r[0] for r in body]
    before = len(body)
    for r in NEW_ROWS:
        if r[0] in names:
            print(f'  SKIP row (already present): {r[0]}')
            continue
        assert len(r) == len(HEADER), f'bad column count for {r[0]!r}'
        if write:
            body.append(r)
            names.append(r[0])
    if write and len(body) != before:
        buf = io.StringIO()
        w = csv.writer(buf, lineterminator='\r\n')
        w.writerow(header)
        w.writerows(body)
        open(LEADS, 'w', encoding='utf-8', newline='').write(buf.getvalue())
        assert open(LEADS, 'rb').read().endswith(b'\r\n')
    print(f'  leads.csv: {before} rows -> {len(body)} rows'
          + ('' if write else '  (dry run)'))


def do_extra(write):
    d = json.load(open(EXTRA, encoding='utf-8'))
    seen = {(v.get('name', '').lower(), v.get('website', '').lower()) for v in d['vetted']}
    seen |= {(k.get('name', '').lower(), k.get('website', '').lower()) for k in d['known']}
    added_v = added_k = 0
    for name, site, city, checked, gate, reason in NEW_VETOES:
        key = (name.lower(), site.lower())
        if key in seen:
            print(f'  SKIP veto (already present): {name}')
            continue
        if write:
            d['vetted'].append({'name': name, 'website': site, 'city': city,
                                'checked': checked, 'gate': gate, 'reason': reason})
            seen.add(key)
        added_v += 1
    for name, site, city, note in NEW_KNOWN:
        key = (name.lower(), site.lower())
        if key in seen:
            print(f'  SKIP known (already present): {name}')
            continue
        if write:
            d['known'].append({'name': name, 'website': site, 'city': city, 'note': note})
            seen.add(key)
        added_k += 1
    if write:
        # indent=2 is the file's established convention - keep it, or every
        # re-run rewrites the whole file and buries the real change
        json.dump(d, open(EXTRA, 'w', encoding='utf-8'), indent=2,
                  ensure_ascii=False)
        open(EXTRA, 'a', encoding='utf-8').write('\n')
    print(f'  known_leads_extra.json: +{added_v} vetoes, +{added_k} known'
          f' -> known {len(d["known"])} / vetted {len(d["vetted"])}'
          + ('' if write else '  (dry run)'))


def do_guard():
    out = subprocess.run(
        [sys.executable, 'discover_leads.py', 'solar Hyderabad batch20 replay',
         '--feed', FEED],
        capture_output=True, text=True, env={'PYTHONPATH': '/tmp/pdflibs', 'PATH': '/usr/bin:/bin'},
    )
    tail = (out.stdout + out.stderr).strip().splitlines()
    skipped = [l for l in tail if 'skipped' in l]
    new = [l for l in tail if 'NEW advertisers' in l]
    print('  guard replay:', skipped[-1].strip() if skipped else '(no skip line)')
    print('  guard replay:', new[-1].strip() if new else '(no NEW line)')
    assert new and '0 NEW advertisers' in new[-1], 'feed is NOT fully absorbed'


def main():
    write = '--write' in sys.argv
    print('BATCH 20 - solar Hyderabad, 2026-11-15' + ('' if write else '   [DRY RUN]'))
    do_leads(write)
    do_extra(write)
    if write:
        print('re-running the duplicate guard over the saved feed...')
        do_guard()
    print('done.')


if __name__ == '__main__':
    main()
