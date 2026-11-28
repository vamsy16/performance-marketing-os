"""Regression tests for draft scope, score consistency and live-verifier selection."""
import contextlib
import io
import json
import os
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch

from pypdf import PdfReader
import ads_audit
from ads_audit import calculate_audit_score
import audit_pdf
import delivery_gate
import verify_live
import verify_report

HERE = Path(__file__).resolve().parent
NAMES = ('SundayGrids', 'Arrow Solar', 'Atria Power', 'RAGA Renewable Energy', 'Zenith Solars')

class Batch14Tests(unittest.TestCase):
    def test_drafts_are_labeled_five_pages_and_scores_match(self):
        for name in NAMES:
            with self.subTest(company=name):
                slug = name.replace(' ', '_')
                audit = json.loads((HERE / 'ads_only_results' / ('audit_' + slug + '.json')).read_text(encoding='utf-8'))
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
            return json.loads((HERE / 'ads_only_results' / ('audit_' + name.replace(' ', '_') + '.json')).read_text(encoding='utf-8'))
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
                audit = json.loads((HERE / 'ads_only_results' / ('audit_' + slug + '.json')).read_text(encoding='utf-8'))
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
        arrow = json.loads((HERE / 'ads_only_results' / 'audit_Arrow_Solar.json').read_text(encoding='utf-8'))
        self.assertIsNone(arrow['site_audit']['conversion']['has_contact_form'])
        self.assertEqual(0, arrow['site_audit']['score']['score'])

    def test_latest_uses_modification_time_not_alphabetical_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            older = Path(tmp) / 'audit_Z.json'
            newer = Path(tmp) / 'audit_A.json'
            older.write_text('{}'); newer.write_text('{}')
            os.utime(older, (100, 100)); os.utime(newer, (200, 200))
            empty = Path(tmp) / 'empty'
            empty.mkdir()
            with patch.object(verify_live, 'ADS_ONLY_DIR', tmp), \
                 patch.object(verify_live, 'FULL_DIR', str(empty)):
                self.assertEqual([str(newer)], verify_live.load_reports(latest=1))

    def test_held_draft_fails_both_gates(self):
        path = HERE / 'ads_only_results' / 'audit_Arrow_Solar.json'
        audit = json.loads(path.read_text(encoding='utf-8'))
        _, _, errs = verify_report.verify_ads_only(str(path), audit)
        self.assertTrue(any('review_pending' in e for e in errs), errs)
        ok, lines = delivery_gate.gate_company('Arrow Solar', json_path=str(path),
                                               max_age_minutes=-1)
        self.assertFalse(ok)
        joined = ' '.join(lines)
        self.assertIn('review_pending', joined)
        self.assertIn('DELIVERY GATE: HOLD', joined)

    def test_offline_does_not_claim_live_match(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'audit_test.json'
            path.write_text(json.dumps({'company':'Test', 'ad_library':{'meta_own':{'ads':[]}}}))
            empty = Path(tmp) / 'empty'
            empty.mkdir()
            out = io.StringIO()
            with patch.object(verify_live, 'ADS_ONLY_DIR', tmp), \
                 patch.object(verify_live, 'FULL_DIR', str(empty)), \
                 contextlib.redirect_stdout(out):
                self.assertEqual(4, verify_live.main(['--offline']))
            self.assertIn('live recheck still required', out.getvalue())
            self.assertNotIn('ALL LIVE CHECKS MATCH', out.getvalue())

class PipelineIntegrityTests(unittest.TestCase):
    def test_live_pixel_signatures_match_the_audit_signatures(self):
        html = ('<script src="https://www.googletagmanager.com/gtag/js?id=G-ABCDEF1234">'
                '</script><script src="https://www.googletagmanager.com/gtm.js?id=GTM-ABCDE12">'
                '</script>')
        audited = ads_audit.check_tracking_pixels(html)
        live = {key: bool(re.search(pattern, html, re.I))
                for key, pattern in verify_live.PIXEL_SIGNATURES}
        for key, expected in audited.items():
            with self.subTest(pixel=key):
                self.assertEqual(expected, live[key])

    def test_featured_ads_are_sorted_newest_first(self):
        ads = [
            {'started': '22 Oct 2026', 'library_id': 'old'},
            {'started': '23 Nov 2026', 'library_id': 'new'},
            {'started': '21 Nov 2026', 'library_id': 'mid'},
            {'started': '', 'library_id': 'undated'},
        ]
        ordered = sorted(ads, key=audit_pdf.ad_start_key, reverse=True)
        self.assertEqual(['new', 'mid', 'old', 'undated'],
                         [ad['library_id'] for ad in ordered])

    def test_verification_log_reports_what_was_actually_measured(self):
        audit = {
            'company': 'Test', 'audit_date': '2026-11-28 18:26',
            'load_time_seconds': 0.71,
            'pagespeed': {'error': 'API returned 429'},
            'page_count': {'has_sitemap': False},
            'ad_library': {
                'checked_at': '2026-11-28 18:26',
                'google_own': {'found': False, 'advertisers': [], 'detail': None},
                'meta_competitors': {'ads': [{'library_id': '1'}]},
                'google_competitors': {'advertisers': [{'name': 'A'}]},
            },
        }
        table = audit_pdf.verification_log(audit)
        joined = ' '.join(cell.text for row in table._cellvalues for cell in row)
        self.assertIn('Not available at audit time (API returned 429)', joined)
        self.assertIn('advertiser and ad-count lookup; no advertiser record found', joined)
        self.assertIn('Ad Library sweeps: 1 Meta ads and 1 Google advertisers captured', joined)
        self.assertIn('no sitemap found', joined)
        self.assertIn('0.71 seconds measured', joined)
        self.assertNotIn('NOT CHECKED - the centre was not queried', joined)

    def test_full_pdf_refuses_a_missing_score(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'draft.pdf'
            with self.assertRaisesRegex(ValueError, 'numeric score'):
                audit_pdf.generate_pdf({'company': 'No Score'}, out_path=str(out))
            self.assertFalse(out.exists())


if __name__ == '__main__':
    unittest.main()
