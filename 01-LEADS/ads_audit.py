#!/usr/bin/env python3
"""
Ads Audit Engine — Automated advertising audit for solar companies.
Checks website health, tracking pixels, ad presence signals, and conversion readiness.

Usage:
  python ads_audit.py https://example.com
  python ads_audit.py "Company Name" --city Mumbai
  python ads_audit.py --batch leads.csv
"""

import io
import json
import os
import re
import sys
import time
from datetime import datetime
from urllib.parse import urlparse

# Fix Windows console encoding for Unicode
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import requests
from bs4 import BeautifulSoup

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "audit_results")


# ---------------------------------------------------------------------------
# Website Analysis
# ---------------------------------------------------------------------------

def fetch_website(url, timeout=12):
    """Fetch a website homepage and return parsed soup + raw HTML."""
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    try:
        resp = requests.get(url, timeout=timeout, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }, allow_redirects=True)
        soup = BeautifulSoup(resp.text, "html.parser")
        return {
            "final_url": resp.url,
            "status_code": resp.status_code,
            "html": resp.text,
            "soup": soup,
            "load_time": resp.elapsed.total_seconds(),
        }
    except Exception as e:
        return {"error": str(e), "final_url": url}


def check_tracking_pixels(html):
    """Detect which tracking/advertising pixels are installed."""
    pixels = {
        "meta_pixel": False,
        "google_ads": False,
        "google_analytics_ga4": False,
        "google_analytics_ua": False,
        "linkedin_insight": False,
        "microsoft_clarity": False,
        "hotjar": False,
        "google_tag_manager": False,
    }

    html_lower = html.lower()

    checks = {
        "meta_pixel": ["fbq(", "facebook.com/tr", "connect.facebook.net"],
        "google_ads": ["googletagmanager.com/gtag/js", "aw-"],
        "google_analytics_ga4": ["gtag/js?id=g-", "googletagmanager.com/gtag/js"],
        "google_analytics_ua": ["google-analytics.com/analytics.js", "ua-"],
        "linkedin_insight": ["snap.licdn.com", "linkedin.com/px"],
        "microsoft_clarity": ["clarity.ms"],
        "hotjar": ["hotjar.com", "hj("],
        "google_tag_manager": ["googletagmanager.com/gtm.js", "gtm-"],
    }

    for pixel, keywords in checks.items():
        pixels[pixel] = any(kw in html_lower for kw in keywords)

    return pixels


def check_conversion_elements(soup, html):
    """Check for lead capture and conversion elements."""
    html_lower = html.lower()
    checks = {
        "has_contact_form": bool(soup.find("form")),
        "has_phone_click": bool(re.search(r"tel:", html_lower)),
        "has_whatsapp_link": "wa.me" in html_lower or "whatsapp" in html_lower,
        "has_cta_buttons": _count_cta_buttons(soup),
        "has_live_chat": any(x in html_lower for x in [
            "tawk.to", "zendesk", "intercom", "crisp", "tidio",
            "livechat", "chatwoot"
        ]),
        "has_popup_optin": bool(soup.find(class_=re.compile(r"popup|modal|optin", re.I))),
        "has_testimonials": bool(re.search(r"testimonial|review|client.?say", html_lower)),
        "has_pricing_page_link": bool(re.search(r"price|pricing|cost|plan", html_lower)),
    }
    return checks


def _count_cta_buttons(soup):
    """Count elements that look like call-to-action buttons."""
    cta_words = ["call", "contact", "get quote", "free", "book", "survey",
                 "install", "buy", "learn more", "request", "start",
                 "whatsapp", "enquire", "inquiry", "sign up", "download"]
    count = 0
    for el in soup.find_all(["a", "button"]):
        text = el.get_text(strip=True).lower()
        if any(word in text for word in cta_words) and len(text) < 40:
            count += 1
    return count


def check_seo_basics(soup):
    """On-page SEO signals."""
    title = soup.find("title")
    meta_desc = soup.find("meta", attrs={"name": "description"})
    h1_tags = soup.find_all("h1")
    og_tags = soup.find_all("meta", attrs={"property": re.compile(r"^og:")})

    return {
        "has_title": bool(title and title.get_text(strip=True)),
        "title_text": title.get_text(strip=True) if title else "",
        "title_length": len(title.get_text(strip=True)) if title else 0,
        "has_meta_description": bool(meta_desc and meta_desc.get("content", "").strip()),
        "meta_desc_length": len(meta_desc.get("content", "")) if meta_desc else 0,
        "h1_count": len(h1_tags),
        "h1_text": h1_tags[0].get_text(strip=True) if h1_tags else "",
        "has_og_tags": len(og_tags) > 0,
        "has_schema": bool(soup.find("script", attrs={"type": "application/ld+json"})),
        "has_favicon": bool(soup.find("link", rel="icon") or soup.find("link", rel="shortcut icon")),
        "image_count": len(soup.find_all("img")),
        "images_without_alt": sum(1 for img in soup.find_all("img") if not img.get("alt")),
    }


def check_ssl(url):
    """Check if site uses HTTPS."""
    return url.startswith("https://")


def check_pagespeed(url):
    """Run Google PageSpeed Insights (free, no key needed for basic)."""
    if not url.startswith("http"):
        url = "https://" + url
    try:
        api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy=mobile&category=performance"
        resp = requests.get(api_url, timeout=30)
        if resp.status_code != 200:
            return {"error": f"API returned {resp.status_code}"}

        data = resp.json()
        result = {
            "mobile_performance_score": None,
            "largest_contentful_paint": None,
            "first_contentful_paint": None,
            "cumulative_layout_shift": None,
            "total_blocking_time": None,
        }

        # Lighthouse scores
        lighthouse = data.get("lighthouseResult", {})
        categories = lighthouse.get("categories", {})
        if "performance" in categories:
            result["mobile_performance_score"] = round(
                categories["performance"]["score"] * 100
            ) if categories["performance"]["score"] else None

        # Core Web Vitals
        audits = lighthouse.get("audits", {})
        if "largest-contentful-paint" in audits:
            result["largest_contentful_paint"] = audits["largest-contentful-paint"].get("displayValue", "")
        if "first-contentful-paint" in audits:
            result["first_contentful_paint"] = audits["first-contentful-paint"].get("displayValue", "")
        if "cumulative-layout-shift" in audits:
            result["cumulative_layout_shift"] = audits["cumulative-layout-shift"].get("displayValue", "")
        if "total-blocking-time" in audits:
            result["total_blocking_time"] = audits["total-blocking-time"].get("displayValue", "")

        return result
    except Exception as e:
        return {"error": str(e)}


def check_page_count(url, max_pages=15):
    """Estimate site size by counting sitemap pages or linked pages."""
    if not url.startswith("http"):
        url = "https://" + url
    parsed = urlparse(url)
    base = f"{parsed.scheme}://{parsed.netloc}"

    # Try sitemap.xml first
    try:
        resp = requests.get(f"{base}/sitemap.xml", timeout=8, headers={
            "User-Agent": "Mozilla/5.0"
        })
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "xml")
            urls = soup.find_all("loc")
            return {"sitemap_pages": len(urls), "has_sitemap": True}
    except:
        pass

    # Fallback: count internal links on homepage
    try:
        resp = requests.get(base, timeout=8, headers={
            "User-Agent": "Mozilla/5.0"
        })
        soup = BeautifulSoup(resp.text, "html.parser")
        internal_links = set()
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.startswith("/") or parsed.netloc in href:
                if not any(href.endswith(ext) for ext in [".pdf", ".jpg", ".png", ".zip"]):
                    internal_links.add(href)
        return {"linked_pages": len(internal_links), "has_sitemap": False}
    except:
        pass

    return {"sitemap_pages": 0, "has_sitemap": False}


def check_google_business_signals(soup, company_name, city):
    """Detect if site links to Google Maps / has local SEO signals."""
    html = str(soup).lower()
    return {
        "has_google_maps_embed": "google.com/maps" in html or "maps.google" in html,
        "has_address_schema": bool(soup.find("script", attrs={"type": "application/ld+json"})),
        "mentions_city": city.lower() in html if city else None,
        "company_in_title": company_name.lower() in (soup.find("title").get_text().lower() if soup.find("title") else ""),
    }


# ---------------------------------------------------------------------------
# Ad Presence Check (generates manual check URLs)
# ---------------------------------------------------------------------------

def generate_ad_check_urls(website, company_name):
    """Generate URLs for manual ad library checks (no free API exists)."""
    domain = urlparse(website if website.startswith("http") else "https://" + website).netloc.replace("www.", "")

    return {
        "google_ads_transparency": f"https://adstransparency.google.com/?region=anywhere&q={domain}&country=IN",
        "meta_ad_library": f"https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=IN&q={company_name}&search_type=keyword_unordered",
        "note": "Open these URLs in your browser to check if they're running ads and what those ads look like."
    }


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def calculate_audit_score(checks, pixels, conversion, seo, pagespeed):
    """Score 0-100. Higher = more problems = better sales opportunity for you."""
    score = 0
    issues = []
    wins = []

    # Tracking (20 points available — missing = your opportunity)
    if not pixels["meta_pixel"]:
        score += 5
        issues.append("No Meta Pixel installed — can't run retargeting or track ad conversions")
    else:
        wins.append("Meta Pixel is installed")

    if not pixels["google_ads"] and not pixels["google_tag_manager"]:
        score += 5
        issues.append("No Google Ads / GTM tracking — can't measure ad performance")
    else:
        wins.append("Google tracking is present")

    if not pixels["google_analytics_ga4"] and not pixels["google_analytics_ua"]:
        score += 5
        issues.append("No Google Analytics — flying blind on website traffic")
    else:
        wins.append("Google Analytics is installed")

    # Conversion elements (25 points)
    if not conversion["has_contact_form"]:
        score += 8
        issues.append("No contact form on homepage — visitors can't easily enquire")
    else:
        wins.append("Contact form exists")

    if not conversion["has_whatsapp_link"]:
        score += 5
        issues.append("No WhatsApp link — losing mobile leads (WhatsApp converts 3x better for Indian home services)")
    else:
        wins.append("WhatsApp link present")

    if conversion["has_cta_buttons"] == 0:
        score += 7
        issues.append("No clear call-to-action buttons on homepage")
    elif conversion["has_cta_buttons"] < 3:
        score += 3
        issues.append("Only 1-2 CTA buttons — could be more aggressive")
    else:
        wins.append(f"Good CTA presence ({conversion['has_cta_buttons']} buttons)")

    if not conversion["has_live_chat"]:
        score += 3
        issues.append("No live chat — missing after-hours leads")
    else:
        wins.append("Live chat present")

    if not conversion["has_testimonials"]:
        score += 2
        issues.append("No visible testimonials/social proof on homepage")
    else:
        wins.append("Testimonials visible")

    # SEO (20 points)
    if not seo["has_meta_description"]:
        score += 4
        issues.append("No meta description — lower click-through from Google")
    if seo["h1_count"] == 0:
        score += 4
        issues.append("No H1 tag on homepage")
    elif seo["h1_count"] > 1:
        score += 1
        issues.append(f"Multiple H1 tags ({seo['h1_count']}) — confuses Google")
    if not seo["has_schema"]:
        score += 4
        issues.append("No structured data (Schema.org) — missing rich results in Google")
    if not seo["has_og_tags"]:
        score += 3
        issues.append("No Open Graph tags — links look bad when shared on social/WhatsApp")
    if seo["images_without_alt"] > 0:
        score += 2
        issues.append(f"{seo['images_without_alt']} images missing alt text — hurts SEO")
    if not seo["has_favicon"]:
        score += 1
        issues.append("No favicon — looks unprofessional in browser tabs")

    # Performance (15 points)
    perf = pagespeed.get("mobile_performance_score")
    if perf is not None:
        if perf < 50:
            score += 10
            issues.append(f"Mobile speed score: {perf}/100 — VERY slow, losing mobile visitors")
        elif perf < 90:
            score += 5
            issues.append(f"Mobile speed score: {perf}/100 — room for improvement")
        else:
            wins.append(f"Good mobile speed: {perf}/100")

    # HTTPS
    # (checked separately)

    return {
        "score": min(score, 100),
        "issues": issues,
        "wins": wins,
    }


# ---------------------------------------------------------------------------
# Full Audit
# ---------------------------------------------------------------------------

def run_audit(website, company_name="", city=""):
    """Run a complete audit on a company website."""
    print(f"\n{'='*60}")
    print(f"AUDITING: {company_name or website}")
    print(f"{'='*60}")

    result = {
        "company": company_name,
        "city": city,
        "website": website,
        "audit_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "ssl": None,
        "load_time_seconds": None,
        "pixels": {},
        "conversion": {},
        "seo": {},
        "pagespeed": {},
        "page_count": {},
        "local_signals": {},
        "ad_check_urls": {},
        "score": {},
    }

    # Fetch site
    print("[1/7] Fetching website...")
    site = fetch_website(website)
    if "error" in site:
        result["error"] = site["error"]
        print(f"  ERROR: {site['error']}")
        return result

    result["final_url"] = site["final_url"]
    result["load_time_seconds"] = round(site["load_time"], 2)
    result["ssl"] = check_ssl(site["final_url"])

    # Tracking pixels
    print("[2/7] Checking tracking pixels...")
    result["pixels"] = check_tracking_pixels(site["html"])
    found = [k for k, v in result["pixels"].items() if v]
    print(f"  Found: {', '.join(found) if found else 'NONE'}")

    # Conversion elements
    print("[3/7] Checking conversion elements...")
    result["conversion"] = check_conversion_elements(site["soup"], site["html"])
    print(f"  Form: {result['conversion']['has_contact_form']}, "
          f"WhatsApp: {result['conversion']['has_whatsapp_link']}, "
          f"CTAs: {result['conversion']['has_cta_buttons']}")

    # SEO basics
    print("[4/7] Checking SEO basics...")
    result["seo"] = check_seo_basics(site["soup"])
    print(f"  Title: {result['seo']['title_text'][:50]}")
    print(f"  Meta desc: {'YES' if result['seo']['has_meta_description'] else 'MISSING'}")

    # PageSpeed
    print("[5/7] Running PageSpeed Insights (may take 15-30s)...")
    result["pagespeed"] = check_pagespeed(site["final_url"])
    perf = result["pagespeed"].get("mobile_performance_score")
    print(f"  Mobile performance: {perf}/100" if perf else "  PageSpeed: unavailable")

    # Page count
    print("[6/7] Checking site size...")
    result["page_count"] = check_page_count(site["final_url"])

    # Local signals
    print("[7/7] Checking local SEO signals...")
    result["local_signals"] = check_google_business_signals(
        site["soup"], company_name or "", city
    )

    # Ad check URLs
    result["ad_check_urls"] = generate_ad_check_urls(
        site["final_url"], company_name or website
    )

    # Score
    result["score"] = calculate_audit_score(
        result["conversion"], result["pixels"],
        result["conversion"], result["seo"], result["pagespeed"]
    )

    print(f"\n  AUDIT SCORE: {result['score']['score']}/100")
    print(f"  Issues found: {len(result['score']['issues'])}")
    print(f"  Things done right: {len(result['score']['wins'])}")

    return result


def save_audit(result):
    """Save audit result to file."""
    os.makedirs(RESULTS_DIR, exist_ok=True)
    name = re.sub(r"[^a-zA-Z0-9]+", "_", result.get("company") or result["website"])[:50]
    filepath = os.path.join(RESULTS_DIR, f"audit_{name}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    return filepath


def print_audit_report(result):
    """Pretty-print the audit findings."""
    print(f"\n{'='*60}")
    print(f"AUDIT REPORT: {result.get('company', result['website'])}")
    print(f"Date: {result['audit_date']}")
    print(f"{'='*60}")

    if "error" in result:
        print(f"ERROR: {result['error']}")
        return

    print(f"\nWebsite: {result['final_url']}")
    print(f"SSL: {'Yes' if result['ssl'] else 'NO (security issue)'}")
    print(f"Load time: {result.get('load_time_seconds', 'N/A')}s")

    score = result["score"]["score"]
    print(f"\n{'-'*40}")
    print(f"AUDIT SCORE: {score}/100")
    if score >= 50:
        print("  -> Strong audit opportunity. Many issues to fix.")
    elif score >= 25:
        print("  -> Moderate opportunity. Some clear wins available.")
    else:
        print("  -> Well-optimized site. Focus on ads/service angle instead.")
    print(f"{'-'*40}")

    print("\n[ISSUES FOUND - your pitch material]:")
    for issue in result["score"]["issues"]:
        print(f"  * {issue}")

    print("\n[WHAT'S WORKING]:")
    for win in result["score"]["wins"]:
        print(f"  * {win}")

    print("\n[TRACKING STATUS]:")
    for pixel, installed in result["pixels"].items():
        status = "YES" if installed else "NO "
        print(f"  [{status}] {pixel.replace('_', ' ').title()}")

    print("\n[MANUAL AD CHECK - open in browser]:")
    print(f"  Google Ads: {result['ad_check_urls']['google_ads_transparency']}")
    print(f"  Meta Ads:   {result['ad_check_urls']['meta_ad_library']}")

    if result["pagespeed"].get("mobile_performance_score") is not None:
        print(f"\n[PAGE SPEED]:")
        print(f"  Performance: {result['pagespeed']['mobile_performance_score']}/100")
        print(f"  LCP: {result['pagespeed'].get('largest_contentful_paint', 'N/A')}")
        print(f"  FCP: {result['pagespeed'].get('first_contentful_paint', 'N/A')}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nExamples:")
        print('  python ads_audit.py https://tanisolars.com')
        print('  python ads_audit.py "SunTech Solar" --city Mumbai')
        return

    company = ""
    city = ""
    website = ""
    args = sys.argv[1:]

    if "--city" in args:
        idx = args.index("--city")
        city = args[idx + 1] if idx + 1 < len(args) else ""
        args = args[:idx] + args[idx + 2:]

    if args[0].startswith("http") or "." in args[0]:
        website = args[0]
        if len(args) > 1:
            company = " ".join(args[1:])
    else:
        company = " ".join(args)
        print(f"\nNote: No URL provided for '{company}'.")
        print("Searching for website...")
        # Try common domain patterns
        slug = company.lower().replace(" ", "").replace("solar", "")
        guesses = [
            f"https://{company.lower().replace(' ', '')}.com",
            f"https://{slug}solar.com",
            f"https://www.{slug}solar.in",
        ]
        for g in guesses:
            try:
                r = requests.head(g, timeout=5, allow_redirects=True)
                if r.status_code < 400:
                    website = g
                    print(f"  Found: {g}")
                    break
            except:
                continue
        if not website:
            print("  Could not find website. Please provide URL manually.")
            print(f'  Usage: python ads_audit.py "https://example.com" --city {city}')
            return

    result = run_audit(website, company, city)
    save_audit(result)
    print_audit_report(result)

    filepath = os.path.join(RESULTS_DIR, f"audit_{re.sub(r'[^a-zA-Z0-9]+', '_', company or website)[:50]}.json")
    print(f"\nSaved to: {filepath}")


if __name__ == "__main__":
    main()
