#!/usr/bin/env python3
"""Refine the two new Telangana rows with facts the third-eye pass turned up.

Two things had to be corrected after the first draft of these rows:

1. Solar Apex was already qualified by batch 14 on 2026-11-10 but was never
   rowed - the log lists it as one of five qualifying leads, and only three of
   the five were added to leads.csv. The row now records that history so
   nobody mistakes it for a fresh discovery twice over.

2. Batch 14 recorded Solar Apex's ad destination as UNCONFIRMED and left a
   hiring ad on file. Both are now settled: the ?id= fetch shows the CTA is
   api.whatsapp.com, and the hiring ad 2362213721277291 (which ran on the
   corporate page facebook.com/61575888183929, not the Khammam franchise
   page) is no longer in the Ad Library.

Eagle's row gains the note that a page's ads cannot be enumerated through
?id=<page_id> - Meta answers "The ad you searched for doesn't exist" - so the
count of two comes from the per-ad view, which does list sibling ads.
"""
import csv
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LEADS = os.path.join(HERE, "leads.csv")

EAGLE_SNIPPET = (
    "Live Meta advertiser: 2 active ads on the \"Eagle Solar Systems\" page "
    "(FB page 61595903925834), each one re-verified individually on 2026-11-15 "
    "by opening its Library ID on its own - 1677382683817329 (started running "
    "7 Nov 2026) and 1835997698149286 (started running 12 Nov 2026). Telugu "
    "rooftop-solar creative: \"నెలనెలా వేల రూపాయలు కరెంట్ బిల్లులకే ఖర్చు "
    "చేస్తున్నారా?... ఇంటికి రూఫ్‌టాప్ సోలార్ ఇన్‌స్టాలేషన్, అర్హత "
    "ఉన్న వారికి ₹78,000 వరకు ప్రభుత్వ సబ్సిడీ, కరెంట్ బిల్లులో 90% వరకు "
    "ఆదా చేసే అవకాశం, PM సూర్య ఘర్ ముఫ్త్ బిజిలీ యోజన\", phones 9000666985 / "
    "9000666984, service area \"హైదరాబాద్ & తెలంగాణ అంతటా సేవలు\". Both "
    "CTAs are fb.me lead forms, so no ad traffic can reach a website - the "
    "firm has no website of its own. AD COUNT: two, and that is the whole "
    "page - a page's ads cannot be enumerated through ?id=<page_id> (Meta "
    "answers \"The ad you searched for doesn't exist\"), so the count comes "
    "from the per-ad view, which lists the page's other ads beneath the one "
    "requested. Published email eaglesolarhyd@gmail.com read from the "
    "Telangana government's TGREDCO 2026 empanelled-supplier register "
    "(https://tgredco.telangana.gov.in/Updates_2026/List_of_Empanelled_"
    "Suppliers_2026.pdf), regn. TSRE240360: SY.No.142/A/1, Mallampet, "
    "Bachupally, Maheshwaram, Medchal, Hyderabad 500072, mobile 9000666985 - "
    "the same number the ads publish. Third-eye corroboration: the same "
    "Mallampet/Bachupally Eagle Solar Systems is listed on Justdial as a "
    "solar-fence and solar-power-system dealer (21 years in business, "
    "09980785458) and on IndiaMART as a proprietorship established 2013 in "
    "the name of RAMA KRISHNAIAH KUMBAM, manufacturer and wholesale trader "
    "of solar water heaters, solar fencing and street lights, alongside "
    "interior designing, false ceiling and modular kitchen, up to 10 "
    "employees - a small proprietor firm with a wider trade than rooftop "
    "solar, recorded here rather than hidden. No own website and no domain "
    "to probe, so the audit can only measure the paid path."
)

APEX_SNIPPET = (
    "Live Meta advertiser: 2 active ads on the \"Solar Apex Khammam\" page "
    "(FB page 61596329420215), each re-verified individually on 2026-11-15. "
    "Brand ad 1143855195267637 (started running 4 Nov 2026): \"Call Us: "
    "8125640121, 8008576480 / Visit Us: Church Compound Center, Khammam / "
    "www.solarapex.in\", CTA api.whatsapp.com - in segment, a rooftop-solar "
    "installer, and this resolves the UNCONFIRMED destination batch 14 left "
    "on file. The second live ad 1667563528489384 (started running 4 Nov "
    "2026) is a Telugu dealership-recruitment ad claiming Khammam dealers "
    "earn Rs.50,000 to Rs.1 lakh plus a month; it is recorded because the "
    "same page runs it, and it is excluded from the ad count used for the "
    "audit, on the same reasoning that rejected Servotech and Go Rewatt. "
    "THIRD HISTORY - this firm is not a fresh discovery. Batch 14 "
    "(01-LEADS/batches/telangana_state_new_leads_batch14_2026-11-10.md) "
    "qualified it on 2026-11-10 as one of five leads, recorded the same "
    "brand ad and the same Manikonda address, and then rowed only three of "
    "the five - Solar Apex and Laxmi Narayana were left unrowed. It is rowed "
    "now, with that history stated rather than hidden. Batch 14 also carried "
    "a hiring ad 2362213721277291 (\"Hiring Sales Officer for Warangal, "
    "Karimnagar and Kamareddy\"); re-opened on 2026-11-15 it answers \"Ad "
    "isn't in the Ad Library\", and it ran on the corporate page "
    "facebook.com/61575888183929 rather than the Khammam franchise page. "
    "CAUTION - HQ vs branch: the registered address is Manikonda, Hyderabad "
    "500089; the advertising page is the Khammam outlet, and a LinkedIn post "
    "corroborates Mohammed Mubashir as Franchise Owner for Khammam District. "
    "Reportable defect carried over from batch 14 and still true: the ad "
    "phones 8125640121 / 8008576480 do not match the website phone +91 96660 "
    "05198. Contacts read live off the company's own site on 2026-11-15 "
    "(third-eye re-verification): solarapex.in publishes info@solarapex.in "
    "and +91 96660 05198 at 3rd floor, Kakatiya Marvel, near Lanco Hills "
    "Road, Sri Laxmi Nagar Colony, Manikonda, Hyderabad 500089, WhatsApp "
    "wa.me/919666005198. The homepage mailto href is broken and points at "
    "info@domain.com, so the /contact/ page is the only working email. "
    "Services listed: residential, commercial, industrial, apartments, "
    "street lights, water heaters and open-access; footer copyright 2026. "
    "Google Ads Transparency ?domain=solarapex.in under region=IN returns 0 "
    "ads on 2026-11-15, so the live-ad evidence is Meta-only and is stated "
    "as such."
)


def main():
    with io.open(LEADS, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames
        rows = list(reader)

    targets = {
        "Eagle Solar Systems": EAGLE_SNIPPET,
        "Solar Apex Pvt Ltd": APEX_SNIPPET,
    }
    seen = set()
    for r in rows:
        if r["name"] in targets:
            r["snippet"] = targets[r["name"]]
            seen.add(r["name"])
    missing = set(targets) - seen
    if missing:
        raise SystemExit("row not found: %s" % sorted(missing))

    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=fields, lineterminator="\r\n")
    writer.writeheader()
    for r in rows:
        writer.writerow(r)
    with io.open(LEADS, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())
    print("refined:", ", ".join(sorted(seen)))


if __name__ == "__main__":
    main()
