# Discovery: Solar Hyderabad — 5 NEW Leads from the Live Meta Ad Library

Source: Meta Ad Library, India, active ads, query "solar Hyderabad"
(~330 results), checked 2026-10-18. Venus home appliances and Sri Balaji
Solar Energies also appeared but are EXCLUDED (already audited + reported).

| # | Advertiser (lead) | Ad Library evidence | Running since | Conversion destination | Contact found |
|---|---|---|---|---|---|
| 1 | ORBIT SOLAR | Library ID 2110991659634519 (+ more) | Dec 10, 2025 | orbitsolar.in ("Schedule a Free Site Audit") + FB sign-up forms | Phone/WhatsApp +91 9059806772 · Mehdipatnam, Hyderabad · no email on site |
| 2 | AB Solar Power Systems | Library ID 1970895137170804 | Oct 11, 2026 | absolar.in + FB "Get offer" forms | sales@absolar.in · +91 80990 40600 |
| 3 | Suryon | Library ID 1553074916624250 | Oct 1, 2026 | FB sign-up form ("Check your solar eligibility") | No website/email found yet |
| 4 | mrsolar.in (MrSolar) | Library ID 1080017474624010 | Sep 26, 2026 | mrsolar.in Hyderabad landing page + FB "Book now" | Phone +91 85009 11912 · no email found |
| 5 | The ARKA SOLAR POWER | Library ID 2121066642144700 (2 ads share creative) | Jul 13, 2026 | FB "Apply now" (free site inspection, Hyderabad homeowners) | No website/email found yet |

Ad angles observed (useful for outreach + competitor sections):
- Orbit: "1000+ installations across Hyderabad", apartments/common-area solar pitch
- AB Solar: Dussehra offer ₹22,000 off + ₹78,000 subsidy, ₹0 down payment EMI
- Suryon: "Your Roof Can Save You Money", eligibility/subsidy check
- MrSolar: uncut Hyderabad customer testimonial video, subsidy guidance
- ARKA: "reduce bill by more than 90%", free site inspection, EMI options

## Next step: audit their ADS (owner machine, Chrome required)

For each advertiser, run the direct pipeline with the ad destination so the
report covers Meta own ads + Google transparency + competitors + the
conversion page those ads send traffic to:

```bash
cd 01-LEADS
python run_pipeline.py https://orbitsolar.in "ORBIT SOLAR" --city Hyderabad
python run_pipeline.py https://absolar.in "AB Solar Power Systems" --city Hyderabad
python run_pipeline.py https://mrsolar.in "mrsolar.in" --city Hyderabad
python verify_report.py --all
cd ../02-OUTREACH && python audit_outreach.py --export
```

Suryon and ARKA have no public website in their ads (FB lead forms only) —
audit them via discovery mode, which handles no-website/lead-form funnels:
they are already inside the next `discover_leads.py "solar Hyderabad" --limit 8`
pool; the report will honestly show their funnel type instead of a fake
website score.

After pushing audit results, Arena verifies the reports, generates emails,
creates ONE initial Gmail draft per lead with an email (AB Solar first —
sales@absolar.in), and tracks thread_id / mails_sent / next_followup_date.
Orbit, MrSolar, Suryon and ARKA need an email found before drafting.
