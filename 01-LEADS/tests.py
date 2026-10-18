#!/usr/bin/env python3
"""
Unit tests for the ads-audit pipeline's pure logic — data hygiene, lead
discovery helpers, PDF text safety, and report-verification patterns.

Run:  python tests.py          (stdlib unittest, no extra dependency)
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lead_data import (sanitize_email, clean_phone, clean_text, is_junk_url,
                       host_of)
from discover_leads import city_from_query, resolve_website, website_from_text
from audit_pdf import latin_safe
from verify_report import SOCIAL_WEBSITE_RE


class TestSanitizeEmail(unittest.TestCase):
    CASES = {
        "38660sales@enersol.co.in": "sales@enersol.co.in",
        "32735solarinstallers.in@gmail.comkottayam": "solarinstallers.in@gmail.com",
        "400078enquiryinfo@renovapulseenergy.comstay": "info@renovapulseenergy.com",
        "7276949339info@netsolarenergy.comhadapsar": "info@netsolarenergy.com",
        "411001info@agnisolar.com": "info@agnisolar.com",
        "skyberginfra@yahoo.comcompany": "skyberginfra@yahoo.com",
        "addressinfo@saweriurja.comcontact": "info@saweriurja.com",
        "27500sales@bridgewaypower.inbridgeway": "sales@bridgewaypower.in",
        "16282support@avghnisolar.com": "support@avghnisolar.com",
        "emailinfo@sriishaansolar.com": "info@sriishaansolar.com",
        "guidecontact+91-8047136984inquiry@y2solar.comwhatsapp": "inquiry@y2solar.com",
        "info@ksquareenergy.com": "info@ksquareenergy.com",
        "info.magwinsolar@gmail.com": "info.magwinsolar@gmail.com",
        "sales@prathamsolar.com": "sales@prathamsolar.com",
        "": "",
        "no email here": "",
        "contact at example dot com": "",
    }

    def test_all_garbled_forms(self):
        for raw, want in self.CASES.items():
            self.assertEqual(sanitize_email(raw), want, f"input: {raw!r}")


class TestCleanPhone(unittest.TestCase):
    def test_plain_mobile(self):
        self.assertEqual(clean_phone("+91 9619191172"), "+91 9619191172")
        self.assertEqual(clean_phone("8657444499"), "+91 8657444499")
        self.assertEqual(clean_phone("+917997116161"), "+91 7997116161")

    def test_missing_country_code(self):
        self.assertEqual(clean_phone("89568 40133"), "+91 8956840133")
        self.assertEqual(clean_phone("9196679667"), "+91 9196679667")

    def test_landline_with_zero(self):
        self.assertEqual(clean_phone("01143536666"), "+91 1143536666")
        self.assertEqual(clean_phone("020 66434111"), "+91 2066434111")

    def test_urlencoded(self):
        self.assertEqual(clean_phone("%20+91-%209000%20828%20333"), "+91 9000828333")

    def test_junk_and_tollfree(self):
        self.assertEqual(clean_phone("+91000000000"), "")
        self.assertEqual(clean_phone("18004198777"), "18004198777")
        self.assertEqual(clean_phone(""), "")


class TestJunkFilter(unittest.TestCase):
    JUNK = [
        "https://www.f6s.com/companies/solar/india/maharashtra/mumbai/co",
        "https://aeroleads.com/list/top-solar-companies-in-mumbai",
        "https://www.loomsolar.com/blogs/solar-installer/top-10-...",
        "https://solar.delhi.gov.in/",
        "https://www.bing.com/aclick?ld=e8etP9RwR-pwIW38Eb",
        "https://professnow.com/profession/top-10-best-solar-panel-installer-in-mumbai/",
        "https://builtindelhi.in/articles/solar-company-in-delhi",
        "https://www.starofservice.in/dir/karnataka/bangalore/...",
        "https://www.enfsolar.com/directory/installer/India?area1=Maharashtra",
        "https://greentax.in/solar-installers/mumbai",
        "https://gosolarindex.in/mumbai",
        "https://mytribe.in/home-services/solar-panel-installation-in-delhi",
        "https://www.urjaone.com/solar-panel-installation-in-delhi",
        "https://solarcalculators.in/solar-in-mumbai/",
        "https://connectsolar.in/solar-installers/maharashtra/mumbai",
        "https://www.solarvipani.com/in/solar/maharashtra/mumbai/mumbai",
        "https://energydirectory.in/karnataka/cities/bangalore/solar/...",
        "https://renewableaffairs.com/top-10-solar-companies-in-delhi-ncr/",
        "https://blueblogsolar.com/blogs/all/the-top-10-solar-panel-...",
        "",
    ]

    REAL = [
        "https://www.ksquareenergy.com/solar-company-in-hyderabad",
        "https://venushomeappliances.com/",
        "https://www.solnceenergy.com/solar-company-in-mumbai",
        "https://thermosun.in/top-10-solar-panel-companies-in-delhi-india/",
        "https://agnisolar.com/",
        "https://www.tatapowersolar.com/contact-us/find-a-dealer/delhi/",
    ]

    def test_junk(self):
        for url in self.JUNK:
            self.assertTrue(is_junk_url(url), f"should drop: {url}")

    def test_real_installers(self):
        for url in self.REAL:
            self.assertFalse(is_junk_url(url), f"should keep: {url}")

    def test_host_of(self):
        self.assertEqual(host_of("https://www.KsquareEnergy.com/path"), "ksquareenergy.com")
        self.assertEqual(host_of("bad url"), "")


class TestCleanText(unittest.TestCase):
    def test_replacement_char(self):
        self.assertEqual(clean_text("Solar Panel Installers in Mumbai \ufffd"), "Solar Panel Installers in Mumbai")
        self.assertEqual(clean_text("Best Solar Company \u2014 Pune \x00"), "Best Solar Company \u2014 Pune")


class TestDiscoveryHelpers(unittest.TestCase):
    def test_city_from_query(self):
        self.assertEqual(city_from_query("solar Hyderabad"), "Hyderabad")
        self.assertEqual(city_from_query("rooftop solar panels in Delhi"), "Delhi")
        self.assertEqual(city_from_query("solar companies near me"), "")

    def test_resolve_website_rejects_social(self):
        ad = {"destination": "https://fb.me/abc123", "text": "Call us — ksquareenergy.com for quotes"}
        self.assertIn("ksquareenergy.com", resolve_website(ad))

    def test_resolve_website_prefers_destination(self):
        ad = {"destination": "https://venushomeappliances.com/kitchen", "text": ""}
        self.assertEqual(resolve_website(ad), "https://venushomeappliances.com/kitchen")

    def test_resolve_website_none(self):
        self.assertEqual(resolve_website({"destination": "https://wa.me/91999999999", "text": "call"}), "")

    def test_website_from_text_skips_social(self):
        text = "Follow us on facebook.com/ourpage or visit samrajsolar.com today"
        self.assertIn("samrajsolar.com", website_from_text(text))


class TestLatinSafe(unittest.TestCase):
    def test_ascii_passthrough(self):
        self.assertEqual(latin_safe("Get a free quote today"), "Get a free quote today")

    def test_indic_placeholder(self):
        out = latin_safe("\u0a86\u0aa1\u0abe \u0a9b\u0ac7\u0a9f\u0abe \u0aa4\u0ac1\u0a02")
        self.assertIn("regional language", out)


class TestVerifyPatterns(unittest.TestCase):
    def test_social_website_re(self):
        for url in ("http://fb.me/x", "https://facebook.com/123", "https://instagram.com/p/x"):
            self.assertTrue(SOCIAL_WEBSITE_RE.search(url), url)
        self.assertFalse(SOCIAL_WEBSITE_RE.search("https://ksquareenergy.com"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
