"""Add the two batch-20 leads to the ads-only builder, 2026-11-15.

Appended AFTER the third-eye re-verification, so every ad ID below was opened
by its own Library ID and confirmed live and correctly attributed on
2026-11-15. The two IDs that the original batch-20 record got wrong are NOT
here:

  1691922249204293  recorded as Meissa Reeve  -> actually AB Solar Power Systems
  2319725685441877  recorded as Visiontek     -> actually mr_koti_00 / Garuda
                                                      Solar, Guntur (Andhra)

  python3 add_batch20_ads_only.py            # dry run
  python3 add_batch20_ads_only.py --write
"""

import io
import sys

PATH = 'ads_only_report.py'

ENTRIES = '''
    {
        "company": "Meissa Reeve",
        "legal": "Meissa Reeve Pvt. Ltd.",
        "city": "Mehdipatnam, Hyderabad",
        "website": "https://meissareeve.com/",
        "email": "info@meissareeve.com",
        "phone": "+91 7893088071",
        "fb_page": "https://www.facebook.com/61596697943588/",
        "checked_on": "2026-11-15",
        "ad_library": {
            "meta_own": {
                "found": True,
                "results_count": 1,
                "results_label": "~1 result",
                "query": "Meissa Reeve",
                "ads": [
                    ad("1641050694153685", "Meissa Reeve", "Nov 14, 2026",
                       "WhatsApp deep link ('Send WhatsApp message')",
                       "Tired of your electricity bill going up every summer? "
                       "Put your rooftop to work. Meissa Reeve designs and installs "
                       "rooftop solar for homes across Hyderabad - so you generate "
                       "your own power and cut your monthly bill. Free site visit & "
                       "savings estimate; Help with the PM Surya Ghar subsidy "
                       "process; End-to-end installation & net metering. Tap 'Send "
                       "WhatsApp message' and tell us your monthly bill - we'll show "
                       "you how much you can save. #HarGharSolar", ad_count=1),
                ],
            },
            "summary": (
                "Meissa Reeve is running exactly one active Meta ad, on the 'Meissa "
                "Reeve' page (facebook.com/61596697943588), started 14 Nov 2026 and "
                "roughly 18 hours old when it was re-checked. The click lands on a "
                "WhatsApp deep link - never on meissareeve.com. Google Ads "
                "Transparency for meissareeve.com returns 0 ads under region=IN, so "
                "Meta is the entire paid channel and it rests on a single creative."),
        },
        "funnel": {
            "type": "WhatsApp deep link",
            "destination": "wa.me deep link behind the 'Send WhatsApp message' CTA",
            "meaning": (
                "Every click becomes a WhatsApp conversation with a salesperson. That "
                "is workable, but nothing is measurable: no pixel, no conversion "
                "event, no audience of people who clicked and went quiet, and no page "
                "where a different headline or price could be tested."),
        },
        "findings": [
            "One ad, one message, one channel. The whole paid programme is a single "
            "creative launched on 14 Nov 2026 - there is no second angle to compare "
            "against and nothing running behind it if this one fatigues.",
            "The ad sends the click to WhatsApp, not to the website. re.meissareeve.com "
            "carries the residential, commercial, industrial and agricultural rooftop "
            "work plus four named installations, and none of the paid traffic ever "
            "lands on it.",
            "The copy does the qualifying work WhatsApp cannot: it asks for the monthly "
            "bill and names the three things that actually decide a solar sale - free "
            "site visit, PM Surya Ghar subsidy handling, end-to-end installation with "
            "net metering.",
            "The parent company runs three divisions (solar re., enter e., EV ev.) and "
            "the ad is only about solar, which is the right call - but it means the "
            "solar division has to win on its own with one creative.",
            "Zero Google ads under region=IN. For a search term as intent-heavy as "
            "'solar panel installation Hyderabad' that is an open channel, and the "
            "WhatsApp funnel means there is no landing page to send that traffic to yet.",
        ],
        "next_steps": [
            ("Give the WhatsApp click somewhere to land",
             "A single page on re.meissareeve.com with the offer, the subsidy explainer "
             "and an enquiry form, so the click is measurable and retargetable even "
             "while WhatsApp stays the primary conversion."),
            ("Run a second angle against the first",
             "The current ad leads on bill savings. A second creative leading on the "
             "PM Surya Ghar subsidy - the number, the paperwork, the timeline - tests "
             "a different motive without touching the one that is working."),
            ("Put the four named installs to work",
             "Anees 2 kW Moula Ali, Dr. Kasi 3 kW R K Puram, Om Prakash 4 kW Balnagar "
             "and Uma Shankar 3 kW Begumpet are real, local and verifiable. They belong "
             "next to the offer, not only on a projects page."),
            ("Open the search channel",
             "No Google ads at all. The subsidy and the free site visit are exactly the "
             "queries Hyderabad homeowners type, and there is currently no paid "
             "presence on any of them."),
        ],
        "contact_facts": [
            ("Email", "info@meissareeve.com (enquiry@meissareeve.com also published "
                      "on the solar division)"),
            ("Phone / WhatsApp", "+91 7893088071 / wa.me/917893088071"),
            ("Address", "Saptagiri Nagar, Retibowli, Mehdipatnam, Hyderabad; Google "
                        "listing 12-2-727/1/57, Sapthagiri Nagar Colony, Rethibowli, "
                        "Gudimalkapur, Hyderabad, Telangana 500006"),
            ("Entity", "Meissa Reeve Pvt. Ltd. - solar division on re.meissareeve.com"),
            ("Hours", "Mon-Fri 09:00-17:00"),
            ("Meta page", "facebook.com/61596697943588 (Meissa Reeve)"),
        ],
        "site_evidence": {
            "pixel": None,
            "utm": None,
            "checked_on": "2026-11-15",
            "note": ("Contacts page read live 2026-11-15 through a text-only fetch, so "
                     "page source was not pulled and Meta Pixel presence is unverified "
                     "either way; graded unknown per the catalog's runtime contract. "
                     "The live ad does not link to the site at all - it links to "
                     "WhatsApp."),
        },
    },
    {
        "company": "Visiontek Solar Energy",
        "legal": "VISIONTEK Linkwell Telesystems Pvt Ltd",
        "city": "Begumpet, Hyderabad",
        "website": "https://visiontek.solar/",
        "email": "info@visiontek.com",
        "phone": "+91 9701601421",
        "fb_page": "https://www.facebook.com/Visionteknewenergy/",
        "checked_on": "2026-11-15",
        "ad_library": {
            "meta_own": {
                "found": True,
                "results_count": 11,
                "results_label": "11 distinct creatives verified",
                "query": "Visiontek",
                "ads": [
                    ad("1133037052650969", "Visionteknewenergy", "Nov 12, 2026",
                       "instagram.com root ('Chat with us' / Send Message)",
                       "Still paying high electricity bills? Switch to Visiontek Solar "
                       "and turn sunlight into savings. Our smart system powers your "
                       "home directly, stores extra energy for the night and helps "
                       "lower your monthly bill. Its time to power your home naturally. "
                       "#Visiontek #GoSolar #SolarPower #SolarEnergy #EnergyStorage",
                       ad_count=2),
                    ad("1449750756945639", "Visionteknewenergy", "Nov 12, 2026",
                       "instagram.com root ('Send Message')",
                       "Say goodbye to soaring electricity bills and take control of "
                       "your energy expenses. Switch to solar today and start "
                       "generating your own clean savings. #CutElectricityBills "
                       "#SolarSavings #GoGreen #EnergyIndependence #VisiontekSolar",
                       ad_count=2),
                    ad("2208275783425425", "Visionteknewenergy", "Nov 12, 2026",
                       "instagram.com root ('Send Message')",
                       "Control your electricity bill before it shocks you! Go solar "
                       "with Visiontek and take charge of your energy. #Visiontek "
                       "#GoSolar #SolarEnergy #SolarPower #SaveOnElectricity "
                       "#RenewableEnergy #CleanEnergy #SolarSolutions #GreenEnergy "
                       "#EnergySavings", ad_count=2),
                    ad("1138341982459373", "Visionteknewenergy", "Nov 12, 2026",
                       "instagram.com root ('Send Message')",
                       "Say goodbye to soaring electricity bills and take control of "
                       "your energy expenses. Switch to solar today and start "
                       "generating your own clean savings. #CutElectricityBills "
                       "#SolarSavings #GoGreen #EnergyIndependence #VisiontekSolar",
                       ad_count=2),
                    ad("910533972050441", "Visionteknewenergy", "Nov 12, 2026",
                       "instagram.com root ('Send Message')",
                       "Going solar is more than installing panels; it's about choosing "
                       "the right power solution! Understand your energy needs, select "
                       "the right inverter and plan your backup for reliable, efficient "
                       "power. Make a smarter energy choice with Visiontek! #Visiontek "
                       "#SolarEnergy #SolarPower #CleanEnergy #RenewableEnergy",
                       ad_count=2),
                    ad("1642086640990986", "Visionteknewenergy", "Nov 12, 2026",
                       "image creative, no outbound link shown",
                       "Control your electricity bill before it shocks you! Go solar "
                       "with Visiontek and take charge of your energy. #Visiontek "
                       "#GoSolar #SolarEnergy #SolarPower #SaveOnElectricity "
                       "#RenewableEnergy #CleanEnergy #SolarSolutions #GreenEnergy "
                       "#EnergySavingSolutions", ad_count=2),
                    ad("1949641059333335", "Visionteknewenergy", "Nov 12, 2026",
                       "image creative, no outbound link shown",
                       "Big on performance. Compact in design. With Visiontek Solar "
                       "Inverters, you get powerful solar performance without giving up "
                       "valuable space. Built for efficiency, designed for modern "
                       "spaces, and made to power more with less. Less space. More "
                       "power. Smarter solar. #Visiontek #SolarInverter #SolarPower "
                       "#RenewableEnergy #CleanEnergy #SolarSolutions", ad_count=2),
                    ad("1846039203313070", "Visionteknewenergy", "Nov 12, 2026",
                       "video creative, no outbound link shown",
                       "Stop choosing between comfort and savings. Switch to Visiontek "
                       "Solar and stay cool without the high bills. #VisiontekSolar "
                       "#SolarPower #SaveMore #SmartHome #CleanEnergy", ad_count=2),
                    ad("1443714387877981", "Visionteknewenergy", "Nov 12, 2026",
                       "carousel, no outbound link shown",
                       "Still paying high electricity bills? Switch to Visiontek Solar "
                       "and turn sunlight into savings. Our smart system powers your "
                       "home directly, stores extra energy for the night and helps "
                       "lower your monthly bill. Its time to power your home naturally. "
                       "#Visiontek #GoSolar #SolarPower #SolarEnergy #EnergyStorage",
                       ad_count=2),
                    ad("2172490176994377", "Visionteknewenergy", "Nov 6, 2026",
                       "fb.me short link",
                       "This Diwali, light up your life with the power of solar! "
                       "Celebrate the festival of lights by making a brighter, smarter "
                       "energy choice with Visiontek. Explore our range of On-Grid, "
                       "Off-Grid & Hybrid Solar Inverters and energy storage solutions "
                       "for your home and business.", ad_count=2),
                    ad("986852867827035", "Visionteknewenergy", "Nov 12, 2026",
                       "carousel, no outbound link shown",
                       "Going solar is more than installing panels; it's about choosing "
                       "the right power solution! Understand your energy needs, select "
                       "the right inverter and plan your backup for reliable, efficient "
                       "power. Make a smarter energy choice with Visiontek! #Visiontek "
                       "#SolarEnergy #SolarPower #CleanEnergy #RenewableEnergy",
                       ad_count=2),
                ],
            },
            "summary": (
                "Visionteknewenergy is running 11 distinct live Meta creatives, every "
                "one of them started on 12 Nov 2026 except a Diwali creative from 6 "
                "Nov 2026 - a single coordinated launch, which means this is a fresh, "
                "actively managed account rather than a stale one. Meta groups them, "
                "reporting '2 ads use this creative and text' on each, so the real "
                "number of ads is higher than the number of distinct IDs. Six of the "
                "eleven send the click to a bare instagram.com root and one to fb.me; "
                "the rest carry no outbound link at all. Google Ads Transparency for "
                "visiontek.solar returns 0 ads under region=IN, so Meta is the entire "
                "paid channel."),
        },
        "funnel": {
            "type": "Instagram root / fb.me / no link",
            "destination": "instagram.com root on 6 creatives, fb.me on 1, none on 4",
            "meaning": (
                "Almost none of this spend can reach a page the company controls. The "
                "instagram.com links land on the Instagram home feed, not a profile, a "
                "post or a message thread - a click there has nowhere to go and cannot "
                "be attributed. Four creatives carry no link at all."),
        },
        "findings": [
            "Eleven distinct creatives, all launched on the same day (12 Nov 2026) with "
            "one from 6 Nov. Volume is not the problem here - coordination and "
            "destination are.",
            "Six of the eleven point at a bare instagram.com root and one at fb.me. A "
            "click on instagram.com lands on the Instagram home feed, not on anything "
            "belonging to Visiontek, so that traffic is effectively unattributable.",
            "The copy is generic brand awareness - 'Switch to Visiontek Solar', 'Big on "
            "performance. Compact in design.' - with no price, no subsidy figure, no "
            "system size and no offer anywhere across eleven creatives.",
            "The ads sell inverters and storage (RISE+, FUTURE+, VAULT+, PULSE+) as "
            "much as they sell rooftop solar. That matches the business - this is a "
            "manufacturer's solar division launched in 2025, not a rooftop EPC - but it "
            "means the ad programme is building product awareness rather than "
            "generating installation enquiries.",
            "visiontek.solar has a working contact form, WhatsApp support, four "
            "documented product lines and a blog posted on 11 and 12 Nov 2026 - and "
            "almost none of the paid traffic is pointed at any of it.",
            "Zero Google ads under region=IN, so the entire paid presence is these "
            "eleven Meta creatives.",
        ],
        "next_steps": [
            ("Point the ads at something Visiontek owns",
             "Every instagram.com and fb.me destination should become a real page - a "
             "product page for the inverter creatives, an enquiry page for the "
             "bill-saving ones. As it stands the spend cannot be measured or "
             "retargeted."),
            ("Add a number to the copy",
             "Eleven creatives and not one price, subsidy figure or system size. Even a "
             "starting price or the PM Surya Ghar subsidy amount gives the ad something "
             "to be judged on."),
            ("Split the two audiences the copy is mixing",
             "Some creatives sell inverters to people who already know what an inverter "
             "is; others sell rooftop solar to homeowners. They are different buyers "
             "and are currently competing in the same account."),
            ("Use the blog and the WhatsApp button",
             "Two posts published on 11 and 12 Nov 2026 and a live WhatsApp button on "
             "every page - the ads could be driving to either of those instead of to "
             "Instagram's home feed."),
        ],
        "contact_facts": [
            ("Email", "info@visiontek.com"),
            ("Phone / WhatsApp", "+91 9701601421 / wa.me/+919701601421"),
            ("Address", "Linkwell Telesystems Pvt. Ltd., 1-11-252/1B, Behind Shoppers' "
                        "Stop, Begumpet, Hyderabad 500016, Telangana, India"),
            ("Entity", "VISIONTEK Linkwell Telesystems Pvt Ltd - 32+ years in telecom "
                       "and power electronics; solar division launched 2025"),
            ("Products", "RISE+ on-grid inverter, FUTURE+ hybrid inverter, VAULT+ LFP "
                         "battery storage, PULSE+ panel-level optimiser"),
            ("Meta page", "facebook.com/Visionteknewenergy"),
        ],
        "site_evidence": {
            "pixel": None,
            "utm": None,
            "checked_on": "2026-11-15",
            "note": ("Homepage and contact page read live 2026-11-15 through a "
                     "text-only fetch, so page source was not pulled and Meta Pixel "
                     "presence is unverified either way; graded unknown per the "
                     "catalog's runtime contract. Ten of the eleven live ads do not "
                     "link to the site at all."),
        },
    },
'''


def main():
    write = '--write' in sys.argv
    s = io.open(PATH, encoding='utf-8').read()
    if '"Meissa Reeve"' in s or '"Visiontek Solar Energy"' in s:
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
