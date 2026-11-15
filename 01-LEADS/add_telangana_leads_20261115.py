#!/usr/bin/env python3
"""Row the two new Telangana leads verified live on 2026-11-15.

Every value in this script comes from a real measurement taken this session:
Meta Ad Library page views opened per-ID, the firms' own sites, the Telangana
government's TGREDCO 2026 empanelled-supplier register PDF, and web search.
Nothing is copied from another report.

Rows added
----------
1. Eagle Solar Systems     2 live Meta ads, email from the state register
2. Solar Apex Pvt Ltd      2 live Meta ads, email from its own site

Rejects recorded in the registry so they are not re-hunted pointlessly:
Griffin Energy and Surya Shakti Solar Energy both run live Meta ads in
Hyderabad but publish no email address, so they fail the published-email
gate. They are vetted, not blocked - a vetted entry expires.

Also corrected
--------------
Ray On Solar Systems was rowed with city "Hyderabad" while its own site says
Visakhapatnam, Andhra Pradesh. The row's snippet already said so; the city
field contradicted it. Both are now consistent.
"""
import csv
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LEADS = os.path.join(HERE, "leads.csv")
EXTRA = os.path.join(HERE, "known_leads_extra.json")

EAGLE_SNIPPET = (
    "Live Meta advertiser: 2 active ads on the \"Eagle Solar Systems\" page "
    "(FB page 61595903925834), each one re-verified individually on 2026-11-15 "
    "by opening its Library ID on its own - 1677382683817329 (started running "
    "7 Nov 2026) and 1835997698149286 (started running 12 Nov 2026). Telugu "
    "rooftop-solar creative: PM Surya Ghar subsidy of up to Rs.78,000, \"90% "
    "varaku aada\", phones 9000666985 / 9000666984, service area \"Hyderabad & "
    "Telangana anthata sevalu\". Both CTAs are fb.me lead forms, so no ad "
    "traffic can reach a website - the firm has no website of its own. "
    "Published email eaglesolarhyd@gmail.com read from the Telangana "
    "government's TGREDCO 2026 empanelled-supplier register "
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
    "www.solarapex.in\", CTA WhatsApp - in segment, a rooftop-solar "
    "installer. The second live ad 1667563528489384 (started running 4 Nov "
    "2026) is a Telugu dealership-recruitment ad claiming Khammam dealers "
    "earn Rs.50,000 to Rs.1 lakh plus a month; it is recorded because the "
    "same page runs it, and it is excluded from the ad count used for the "
    "audit, on the same reasoning that rejected Servotech and Go Rewatt. "
    "Contacts read live off the company's own site on 2026-11-15 (third-eye "
    "re-verification): solarapex.in publishes info@solarapex.in and +91 96660 "
    "05198 at 3rd floor, Kakatiya Marvel, near Lanco Hills Road, Sri Laxmi "
    "Nagar Colony, Manikonda, Hyderabad 500089, WhatsApp wa.me/919666005198. "
    "The homepage mailto href is broken and points at info@domain.com, so the "
    "/contact/ page is the only working email. Services listed: residential, "
    "commercial, industrial, apartments, street lights, water heaters and "
    "open-access; footer copyright 2026. A LinkedIn post corroborates "
    "Mohammed Mubashir as Franchise Owner for Khammam District, so the "
    "advertising page is a franchisee of the Hyderabad-registered Solar Apex "
    "Pvt Ltd - both cities are inside Telangana. Google Ads Transparency "
    "?domain=solarapex.in under region=IN returns 0 ads on 2026-11-15, so the "
    "live-ad evidence is Meta-only and is stated as such."
)

NEW_ROWS = [
    {
        "name": "Eagle Solar Systems",
        "city": "Mallampet, Bachupally, Medchal, Hyderabad 500072",
        "website": "",
        "email": "eaglesolarhyd@gmail.com",
        "phone": "+91 9000666985 / +91 9000666984",
        "snippet": EAGLE_SNIPPET,
        "audit_score": "",
        "audit_issues_count": "",
        "status": "new",
        "added_date": "2026-11-15",
    },
    {
        "name": "Solar Apex Pvt Ltd",
        "city": "Manikonda, Hyderabad",
        "website": "https://www.solarapex.in/",
        "email": "info@solarapex.in",
        "phone": "+91 96660 05198 / 8125640121 / 8008576480",
        "snippet": APEX_SNIPPET,
        "audit_score": "",
        "audit_issues_count": "",
        "status": "new",
        "added_date": "2026-11-15",
    },
]

RAY_ON_SNIPPET_ADDITION = (
    " Third-eye re-verification 2026-11-15: two further live ads confirmed on "
    "the same page by opening each ID individually - 3529873930505195 "
    "(started 18 Sep 2026, multiple versions) and 2401086164116585 (started "
    "15 Oct 2026) - so the row's ad evidence was incomplete. The firm's own "
    "site states plainly that it is located in Visakhapatnam (Ravi Nagar, "
    "Naidu Thota, 530029) and serves homes and businesses there; the city "
    "field of this row said Hyderabad, which contradicted the snippet and "
    "the state audit. Corrected on 2026-11-15."
)


def main():
    with io.open(LEADS, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames
        rows = list(reader)

    have = {r["name"].strip().lower() for r in rows}
    added = []
    for row in NEW_ROWS:
        if row["name"].strip().lower() in have:
            raise SystemExit("refusing to duplicate an existing row: %s"
                             % row["name"])
        rows.append(row)
        added.append(row["name"])

    for r in rows:
        if r["name"] == "Ray On Solar Systems":
            r["city"] = "Visakhapatnam, Andhra Pradesh (advertising into Hyderabad)"
            if "third-eye re-verification 2026-11-15" not in r["snippet"]:
                r["snippet"] = r["snippet"].rstrip() + RAY_ON_SNIPPET_ADDITION

    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=fields, lineterminator="\r\n")
    writer.writeheader()
    for r in rows:
        writer.writerow(r)
    with io.open(LEADS, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())

    with io.open(EXTRA, encoding="utf-8") as f:
        extra = json.load(f)
    known_names = {e["name"].strip().lower() for e in extra["known"]}
    vetted_names = {e["name"].strip().lower() for e in extra["vetted"]}

    extra["known"].extend([
        {
            "name": "Eagle Solar Systems",
            "website": "",
            "city": "Hyderabad",
            "note": ("Rowed in leads.csv 2026-11-15. 2 live Meta ads "
                     "(1677382683817329, 1835997698149286); email "
                     "eaglesolarhyd@gmail.com published in the TGREDCO 2026 "
                     "empanelled-supplier register, TSRE240360. No own "
                     "website."),
        },
        {
            "name": "Solar Apex Pvt Ltd",
            "website": "https://www.solarapex.in/",
            "city": "Hyderabad",
            "note": ("Rowed in leads.csv 2026-11-15. 2 live Meta ads "
                     "(1143855195267637 in segment, 1667563528489384 "
                     "dealership recruitment); info@solarapex.in from its own "
                     "/contact/ page, Manikonda, Hyderabad 500089. The "
                     "advertising page 'Solar Apex Khammam' is its Khammam "
                     "franchisee."),
        },
    ])
    extra["vetted"].extend([
        {
            "name": "Griffin Energy",
            "website": "",
            "city": "Hyderabad",
            "checked": "2026-11-15",
            "gate": "published-email",
            "reason": ("4 live Meta ads verified twice on the 'Griffin "
                       "Energy' page (1159969763254778 Nov 4, plus "
                       "1681876623343353 / 2436699883532011 / 2928662904181620 "
                       "Nov 15 2026) advertising Magnelis steel structures and "
                       "Reliance HJT panels with free roof surveys in "
                       "Hyderabad, but no website and no published email "
                       "address: 4 web searches and 20 Google Ads Transparency "
                       "?domain= probes returned only namesakes (Yemen, UK, "
                       "Texas, Australia)."),
        },
        {
            "name": "Surya Shakti Solar Energy",
            "website": "",
            "city": "Hyderabad",
            "checked": "2026-11-15",
            "gate": "published-email",
            "reason": ("2 live Meta ads verified individually "
                       "(1692983389068776 and 1856029798723640, both Nov 14 "
                       "2026) for on-grid/off-grid/hybrid rooftop solar in "
                       "Hyderabad, but no website and no published email: "
                       "IndiaMART listing indiamart.com/company/273630670/ "
                       "publishes GST 36BKKPA8706N1ZS and CEO A Madhavi but "
                       "no email, the firm is absent from the TGREDCO 2026 "
                       "register, and web search returns only namesakes "
                       "(Faridabad, Kathua J&K, Rajasthan)."),
        },
    ])
    # keep the registries unique
    for key in ("known", "vetted"):
        seen, out = set(), []
        for e in extra[key]:
            k = e["name"].strip().lower()
            if k in seen:
                continue
            seen.add(k)
            out.append(e)
        extra[key] = out

    with io.open(EXTRA, "w", encoding="utf-8") as f:
        json.dump(extra, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print("rows now:", len(rows))
    print("added:", ", ".join(added))
    print("known:", len(extra["known"]), "vetted:", len(extra["vetted"]))


if __name__ == "__main__":
    main()
