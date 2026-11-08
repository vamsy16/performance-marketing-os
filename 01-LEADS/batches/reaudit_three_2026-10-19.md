# Re-audit these 3 first — their PDFs say "NO WEBSITE FOUND", but they have sites

Found while sourcing contacts for the CI-audited leads (2026-10-19).

The scheduled pipeline run (39230572146) discovered these three through their
**Meta ads**, and every one of those ads points at `fb.me` — a Facebook
short-link, not a website. The pipeline therefore concluded "no website to
audit" and produced a 5-page report whose headline is **NO WEBSITE FOUND**,
with no score and no tracking data.

All three **do** have live websites. Sending the current PDFs would tell a
prospect with a working site that they have none, so no Gmail drafts were
created for them. Re-run the audit with the correct URL and the reports become
real ones (score, pixels, PageSpeed) — and the pitch gets better, not worse:
*their paid clicks never reach the site they already own.*

| Company | Website (verified live) | Verified contact |
|---|---|---|
| Sri Balaji Solar Energies | https://www.sribalajisolarenergies.com/ | sbse4444@gmail.com · +91 9959491774 · +91 87024 44646 |
| Green Carbon Hub | https://greencarbonhub.com/ | info@greencarbonhub.com · +91 9182445300 · +91 9182445715 |
| Suryon (by ARCEDO Systems) | https://suryon.in/ | info@arcedo.net · +91 8448448552 |

Contacts are already in `01-LEADS/leads.csv` (status `needs_reaudit`), so
`audit_outreach.py --export` will fill the `to:` field automatically once the
audit JSON carries the right domain.

## Re-run (Actions or laptop)

Actions → **Ads Audit Pipeline → Run workflow**, `mode=audit`:

| website | company | city |
|---|---|---|
| `https://www.sribalajisolarenergies.com/` | `Sri Balaji Solar Energies` | `Hyderabad` |
| `https://greencarbonhub.com/` | `Green Carbon Hub` | `Hyderabad` |
| `https://suryon.in/` | `Suryon` | `Hyderabad` |

Or on a laptop:

```bash
cd 01-LEADS
python run_pipeline.py https://www.sribalajisolarenergies.com/ "Sri Balaji Solar Energies" --city Hyderabad
python run_pipeline.py https://greencarbonhub.com/ "Green Carbon Hub" --city Hyderabad
python run_pipeline.py https://suryon.in/ "Suryon" --city Hyderabad
python verify_report.py --all
cd ../02-OUTREACH && python audit_outreach.py --export
```

Then delete the three stale `audit_pdfs/audit_{Sri_Balaji_Solar_Energies,
Green_Carbon_Hub,Suryon}.pdf` files (or let the rebuild overwrite them) and
re-run the QA gate before any draft goes out.

## Extra findings worth using

- **Sri Balaji Solar Energies** — TSREDCO-empanelled (regn TSRE180085) and
  MNRE PM Surya Ghar authorised; won six awards at the Telangana Annual Solar
  Awards 2026; HO Hanumkonda, Warangal 506001. Strong proof base, zero of it
  visible to the people clicking their ads.
- **Green Carbon Hub** — B2B2C net-zero marketplace (solar install, water &
  wastewater, bio-methanation); clients include GE and the AP Food Processing
  Society.
- **Suryon** — claims 500 MW installed over 9+ years; its "Request Custom Quote
  via WhatsApp" button points at `wa.me/919999999999`, a placeholder number, so
  that CTA cannot be producing leads.
