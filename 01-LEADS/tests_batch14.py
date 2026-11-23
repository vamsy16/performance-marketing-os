"""Regression tests for draft scope, score consistency and live-verifier selection."""
import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from pypdf import PdfReader
from ads_audit import calculate_audit_score
import verify_live

HERE = Path(__file__).resolve().parent
NAMES = ('SundayGrids', 'Arrow Solar', 'Atria Power', 'RAGA Renewable Energy', 'Zenith Solars')

class Batch14Tests(unittest.TestCase):
    def test_drafts_are_labeled_five_pages_and_scores_match(self):
        for name in NAMES:
            with self.subTest(company=name):
                slug = name.replace(' ', '_')
                audit = json.loads((HERE / 'ads_only_results' / ('audit_' + slug + '.json')).read_text())
                site = audit['site_audit']
                score = calculate_audit_score({}, site['pixels'], site['conversion'], site['seo'], site['pagespeed'])
                self.assertEqual(site['score']['score'], score['score'])
                self.assertTrue(audit['review_pending'])
                self.assertNotIn('results_count', audit['ad_library']['meta_own'])
                self.assertEqual(1, len(audit['ad_library']['meta_own']['ads']))
                self.assertIsNone(site['pixels']['meta_pixel'])
                pdf = PdfReader(str(HERE.parent / '02-OUTREACH' / 'ads_only_pdfs' / ('audit_' + slug + '.pdf')))
                self.assertEqual(5, len(pdf.pages))
                text = ' '.join(page.extract_text() for page in pdf.pages)
                self.assertIn('INTERNAL DRAFT - NOT FOR OUTREACH', text)
                self.assertIn('Unknown checks do not add points', text)
                self.assertNotIn('??', text)

    def test_source_context_is_preserved(self):
        def load(name):
            return json.loads((HERE / 'ads_only_results' / ('audit_' + name.replace(' ', '_') + '.json')).read_text())
        raga = load('RAGA Renewable Energy')['site_audit']
        self.assertIsNone(raga['conversion']['has_testimonials'])
        self.assertTrue(any('hidden block' in i.lower() for i in raga['score']['issues']))
        self.assertTrue(any('tablet' in i.lower() for i in raga['score']['issues']))
        atria = load('Atria Power')['site_audit']
        self.assertTrue(atria['seo']['has_favicon'])
        self.assertIsNone(atria['page_count']['has_sitemap'])
        zenith = load('Zenith Solars')['site_audit']
        self.assertTrue(any('585106' in i and '585105' in i for i in zenith['score']['issues']))
        for name in NAMES:
            pdf = PdfReader(str(HERE.parent / '02-OUTREACH' / 'ads_only_pdfs' / ('audit_' + name.replace(' ', '_') + '.pdf')))
            text = ' '.join(page.extract_text() for page in pdf.pages)
            self.assertIn('not a verified total', text)
            self.assertNotIn('active ad results found', text)

    def test_conversion_observations_render_without_invented_cta_counts(self):
        snippets = {
            'SundayGrids': 'Parker 110: Reserve Solar Now',
            'Arrow Solar': 'Check Subsidy Eligibility and Book Now',
            'Atria Power': 'Corporate homepage Contact us',
            'RAGA Renewable Energy': 'Book a Free Site Visit links',
            'Zenith Solars': 'Homepage Get A Quote',
        }
        for name, evidence in snippets.items():
            with self.subTest(company=name):
                slug = name.replace(' ', '_')
                audit = json.loads((HERE / 'ads_only_results' / ('audit_' + slug + '.json')).read_text())
                site = audit['site_audit']
                self.assertIsNone(site['conversion']['has_cta_buttons'])
                self.assertEqual(5, len(site['conversion_evidence']['rows']))
                self.assertTrue(site['conversion_evidence']['sources'])
                pdf = PdfReader(str(HERE.parent / '02-OUTREACH' / 'ads_only_pdfs' / ('audit_' + slug + '.pdf')))
                text = ' '.join(page.extract_text() for page in pdf.pages)
                section = text.split('Conversion readiness', 1)[1].split('Observed positives', 1)[0]
                self.assertIn(evidence, section)
                self.assertNotIn('not checked in this pass', section.lower())
                self.assertIn('not tested', section.lower())
        arrow = json.loads((HERE / 'ads_only_results' / 'audit_Arrow_Solar.json').read_text())
        self.assertIsNone(arrow['site_audit']['conversion']['has_contact_form'])
        self.assertEqual(0, arrow['site_audit']['score']['score'])

    def test_latest_uses_modification_time_not_alphabetical_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            older = Path(tmp) / 'audit_Z.json'
            newer = Path(tmp) / 'audit_A.json'
            older.write_text('{}'); newer.write_text('{}')
            os.utime(older, (100, 100)); os.utime(newer, (200, 200))
            with patch.object(verify_live, 'ADS_ONLY_DIR', tmp):
                self.assertEqual([str(newer)], verify_live.load_reports(latest=1))

    def test_offline_does_not_claim_live_match(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'audit_test.json'
            path.write_text(json.dumps({'company':'Test', 'ad_library':{'meta_own':{'ads':[]}}}))
            out = io.StringIO()
            with patch.object(verify_live, 'ADS_ONLY_DIR', tmp), contextlib.redirect_stdout(out):
                self.assertEqual(0, verify_live.main(['--offline']))
            self.assertIn('live recheck still required', out.getvalue())
            self.assertNotIn('ALL LIVE CHECKS MATCH', out.getvalue())

if __name__ == '__main__':
    unittest.main()
