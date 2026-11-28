#!/usr/bin/env python3
"""Regression checks for these provisional, not-client-ready audit drafts."""
import json
import unittest
from pathlib import Path
from pypdf import PdfReader
from reportlab.lib import colors
import audit_pdf

ROOT = Path(__file__).resolve().parents[1]
CASES = {
    'SunSolar_Power_Systems': ('AW-18179174251', 'www.sunsolar.info', '1472241928117694'),
    'PNR_Sunrise_Energies': ('sunriseenergies.example', 'sunriseenergies.in', '1472241928117694'),
    'DLIFE_Home_Interiors': ('215010909028561', 'dlifeinteriors.com', '2019161465707252'),
    'Dr_Sridhar_Dental': ('G-7Y9ND039HL', 'sridhardental.com', '966436166129348'),
    'Galaxy_Dental_Care': ('GTM-TRRMQGQ', 'galaxydentalcare.in', '1672235477851281'),
}


class TestProvisionalAuditDrafts(unittest.TestCase):
    def test_dark_table_headers_are_actually_white(self):
        audit = {'ad_library': {'meta_own': {'ads': [{'library_id': '123'}]}}}
        tables = [audit_pdf.ad_evidence_table(audit),
                  audit_pdf.promise_gap_table({'promise_gap': [('ad', 'website')]}),
                  audit_pdf.verification_log({})]
        for table in tables:
            for paragraph in table._cellvalues[0]:
                for fragment in paragraph.frags:
                    self.assertEqual(fragment.textColor, colors.white)

    def test_each_report_has_scoped_evidence_and_hold(self):
        for slug, (snippet, domain, competitor) in CASES.items():
            with self.subTest(company=slug):
                data = json.loads((ROOT / '01-LEADS' / 'ads_only_results' / f'audit_{slug}.json').read_text())
                reader = PdfReader(ROOT / '02-OUTREACH' / 'ads_only_pdfs' / f'audit_{slug}.pdf')
                text = '\n'.join(page.extract_text() for page in reader.pages)
                self.assertEqual(len(reader.pages), 5)
                self.assertTrue(all('DO NOT SEND TO CLIENTS' in page.extract_text() for page in reader.pages))
                self.assertIn(snippet, text)
                self.assertIn('Source snippets only', text)
                self.assertIn('Google Ads Transparency - domain search', text)
                self.assertIn(competitor, text)
                self.assertIsNone(data['site_audit']['score']['score'])
                self.assertTrue(all(value is None for value in data['site_audit']['pixels'].values()))
                self.assertIn(domain, data['ad_library']['google_public_evidence']['url'])
                self.assertIn(competitor, data['ad_library']['competitor_public_sample']['url'])
                links = []
                for page in reader.pages:
                    for ann in page.get('/Annots', []):
                        action = ann.get_object().get('/A') or {}
                        links.append(action.get('/URI', ''))
                self.assertIn(data['ad_library']['google_public_evidence']['url'], links)
                self.assertIn(data['ad_library']['competitor_public_sample']['url'], links)


if __name__ == '__main__':
    unittest.main()
