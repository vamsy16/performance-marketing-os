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
