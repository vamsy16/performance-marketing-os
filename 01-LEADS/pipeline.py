#!/usr/bin/env python3
"""
Lead Pipeline — Find, deduplicate, audit, and rank solar company leads.
ONE command. Zero duplicates. Prioritized by audit opportunity.

Usage:
  python pipeline.py                    # Find + audit new leads for default cities
  python pipeline.py --cities "Mumbai,Pune"
  python pipeline.py --max 10           # Limit to 10 audits
  python pipeline.py --skip-audit       # Find + dedup only (fast)
  python pipeline.py --import FILE.csv  # Audit leads from existing CSV
"""

import argparse
import csv
import io
import json
import os
import re
import sys
import time
from datetime import datetime
from urllib.parse import urlparse, unquote

# Fix Windows console encoding for Unicode
if sys.platform == "win32":
    import codecs
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import requests
from bs4 import BeautifulSoup
from ddgs import DDGS

# Add parent so we can import the audit engine
sys.path.insert(0, os.path.dirname(__file__))
from ads_audit import run_audit, save_audit, check_tracking_pixels, check_conversion_elements, check_seo_basics

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

BASE_DIR = os.path.dirname(__file__)
LEADS_CSV = os.path.join(BASE_DIR, "leads.csv")
AUDIT_DIR = os.path.join(BASE_DIR, "audit_results")
PIPELINE_LOG = os.path.join(BASE_DIR, "pipeline_log.json")
CRM_DATA = os.path.join(os.path.dirname(BASE_DIR), "05-CRM", "crm_data.json")

# ---------------------------------------------------------------------------
# Defaults — EDIT THESE
# ---------------------------------------------------------------------------

DEFAULT_CITIES = [
    "Mumbai", "Pune", "Delhi", "Bangalore", "Hyderabad",
    "Chennai", "Ahmedabad", "Jaipur",
]

SEARCH_QUERIES = [
    "solar panel installer {city}",
    "solar energy company {city}",
    "rooftop solar installation {city}",
    "solar power solutions company {city}",
]

SKIP_DOMAINS = [
    "justdial", "sulekha", "yellowpages", "indiamart", "tradeindia",
    "google.com", "facebook.com", "youtube.com", "linkedin.com",
    "twitter.com", "instagram.com", "wikipedia.org", "amazon.",
    "flipkart", "quikr", "olx", "exportersindia", "dir.indiamart",
]


# ---------------------------------------------------------------------------
# Deduplication Engine
# ---------------------------------------------------------------------------

class Deduplicator:
    """
    Zero-duplicate guarantee.
    Checks company name (normalized), domain, and email against ALL existing data.
    """

    # Words to strip when normalizing company names
    NOISE_WORDS = {
        "pvt", "pvt ltd", "private", "limited", "ltd", "llp", "inc",
        "co", "company", "the", "and", "&", "-", "solutions", "services",
        "solar", "energy", "power", "systems", "tech", "technologies",
        "enterprises", "industries", "group", "india", "indian",
    }

    def __init__(self):
        self.seen_names = set()      # normalized names
        self.seen_domains = set()    # extracted domains
        self.seen_emails = set()     # email addresses
        self.seen_websites = set()   # full website URLs (normalized)
        self.records = []            # all known records for debugging

        # Load existing data from all sources
        self._load_existing()

    def _normalize_name(self, name):
        """
        Normalize a company name for dedup comparison.
        'SunTech Solar Pvt Ltd' → 'suntech'
        'Suntech Solar' → 'suntech'
        These should match.
        """
        if not name:
            return ""
        # Lowercase
        name = name.lower().strip()
        # Remove special chars
        name = re.sub(r"[^a-z0-9\s]", " ", name)
        # Split into words
        words = name.split()
        # Remove noise words
        meaningful = [w for w in words if w not in self.NOISE_WORDS and len(w) > 1]
        # Sort so word order doesn't matter
        return " ".join(sorted(meaningful))

    def _extract_domain(self, url):
        """Extract base domain from a URL. 'www.SunTech.com/about' → 'suntech.com'"""
        if not url:
            return ""
        try:
            if not url.startswith(("http://", "https://")):
                url = "https://" + url
            domain = urlparse(url).netloc.lower()
            domain = domain.replace("www.", "").replace("m.", "")
            # Remove subdomains except the main two parts
            parts = domain.split(".")
            if len(parts) > 2:
                domain = ".".join(parts[-2:])
            return domain
        except:
            return ""

    def _load_existing(self):
        """Load all previously seen leads from CSV, audit results, and CRM."""
        # From leads.csv
        if os.path.exists(LEADS_CSV):
            with open(LEADS_CSV, "r", encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    self._register(
                        name=row.get("name", ""),
                        website=row.get("website", ""),
                        email=row.get("email", ""),
                    )

        # From CRM
        if os.path.exists(CRM_DATA):
            try:
                with open(CRM_DATA, "r", encoding="utf-8") as f:
                    crm = json.load(f)
                for lead in crm.get("leads", []):
                    self._register(
                        name=lead.get("name", ""),
                        website=lead.get("website", ""),
                        email=lead.get("email", ""),
                    )
            except:
                pass

        # From previous pipeline runs
        if os.path.exists(PIPELINE_LOG):
            try:
                with open(PIPELINE_LOG, "r", encoding="utf-8") as f:
                    log = json.load(f)
                for entry in log.get("processed", []):
                    self._register(
                        name=entry.get("name", ""),
                        website=entry.get("website", ""),
                        email=entry.get("email", ""),
                    )
            except:
                pass

        total = len(self.seen_names) + len(self.seen_domains) + len(self.seen_emails)
        if total:
            print(f"  Loaded {len(self.seen_names)} names, "
                  f"{len(self.seen_domains)} domains, "
                  f"{len(self.seen_emails)} emails from existing data")

    def _register(self, name="", website="", email=""):
        """Add a record to the dedup index."""
        norm_name = self._normalize_name(name)
        domain = self._extract_domain(website)
        email_domain = email.split("@")[1] if "@" in email else ""

        if norm_name:
            self.seen_names.add(norm_name)
        if domain:
            self.seen_domains.add(domain)
        if email:
            self.seen_emails.add(email.lower())
        if email_domain and email_domain not in ("gmail.com", "yahoo.com", "hotmail.com", "outlook.com"):
            self.seen_domains.add(email_domain)

        self.records.append({
            "name": name, "norm_name": norm_name,
            "domain": domain, "email": email,
        })

    def is_duplicate(self, name="", website="", email=""):
        """
        Check if a lead already exists.
        Returns (is_dup, reason).
        """
        norm_name = self._normalize_name(name)
        domain = self._extract_domain(website)
        email_domain = email.split("@")[1] if "@" in email else ""

        # Check name match
        if norm_name and norm_name in self.seen_names:
            return True, f"Name match: '{norm_name}'"

        # Check domain match
        if domain and domain in self.seen_domains:
            return True, f"Domain match: '{domain}'"

        # Check email match
        if email and email.lower() in self.seen_emails:
            return True, f"Email match: '{email}'"

        # Check email domain (for business emails)
        if email_domain and email_domain not in ("gmail.com", "yahoo.com", "hotmail.com", "outlook.com"):
            if email_domain in self.seen_domains:
                return True, f"Email domain match: '{email_domain}'"

        return False, ""

    def register(self, name="", website="", email=""):
        """Mark a lead as seen (call after confirming it's new)."""
        self._register(name=name, website=website, email=email)

    def save_log(self, new_leads):
        """Save pipeline run log for future dedup."""
        log = {"processed": [], "last_run": datetime.now().isoformat()}
        if os.path.exists(PIPELINE_LOG):
            try:
                with open(PIPELINE_LOG, "r", encoding="utf-8") as f:
                    existing = json.load(f)
                log["processed"] = existing.get("processed", [])
            except:
                pass

        for lead in new_leads:
            log["processed"].append({
                "name": lead.get("name", ""),
                "website": lead.get("website", ""),
                "email": lead.get("email", ""),
                "date": datetime.now().strftime("%Y-%m-%d"),
            })

        with open(PIPELINE_LOG, "w", encoding="utf-8") as f:
            json.dump(log, f, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Lead Discovery
# ---------------------------------------------------------------------------

def search_duckduckgo(query):
    """Search DuckDuckGo using the ddgs library (free, reliable)."""
    results = []
    try:
        with DDGS() as ddgs:
            raw = list(ddgs.text(query, max_results=10))
        for r in raw:
            results.append({
                "title": r.get("title", ""),
                "url": r.get("href", r.get("link", "")),
                "snippet": r.get("body", r.get("snippet", "")),
            })
    except Exception as e:
        print(f"  Search error: {e}")
    return results


def extract_contact(url):
    """Extract email and phone from a website."""
    result = {"email": "", "phone": ""}
    try:
        if not url.startswith("http"):
            url = "https://" + url
        resp = requests.get(url, timeout=10, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        })
        soup = BeautifulSoup(resp.text, "html.parser")
        text = soup.get_text()
        html = resp.text.lower()

        # Email
        emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
        skip_patterns = ["example", "sentry", "wixpress", ".png", ".jpg", ".svg", "@2x", "noreply", "no-reply"]
        for e in emails:
            if not any(s in e.lower() for s in skip_patterns):
                result["email"] = e.lower()
                break

        # Phone (Indian formats)
        phones = re.findall(r"(?:\+91[\s-]?)?[6-9]\d{4}[\s-]?\d{5}", text)
        if phones:
            result["phone"] = phones[0].strip()

        # Also check tel: links
        if not result["phone"]:
            tel_links = soup.find_all("a", href=re.compile(r"^tel:"))
            if tel_links:
                phone = tel_links[0]["href"].replace("tel:", "").strip()
                result["phone"] = phone

    except:
        pass
    return result


def find_solar_companies(cities, queries, dedup, max_results=50):
    """Find solar companies with zero duplicates."""
    found = []
    seen_this_run = set()  # extra safety within single run

    for city in cities:
        print(f"\n>> Searching {city}...")
        for q_template in queries:
            query = q_template.format(city=city)
            print(f"  >> {query}")

            results = search_duckduckgo(query)
            time.sleep(2)

            for r in results:
                title = r["title"]
                title_lower = title.lower()
                url = r["url"]

                # Filter: must be solar-related
                if not any(kw in title_lower for kw in ["solar", "energy", "power", "renewable"]):
                    continue

                # Filter: skip directories
                if any(d in url.lower() for d in SKIP_DOMAINS):
                    continue

                # Filter: must have a real website
                domain = Deduplicator()._extract_domain(url)
                if not domain or "." not in domain:
                    continue

                # === ZERO DUPLICATE CHECKS ===

                # Check 1: Already seen in this run
                if domain in seen_this_run:
                    continue

                # Check 2: Duplicate against existing data
                is_dup, reason = dedup.is_duplicate(name=title, website=url)
                if is_dup:
                    print(f"    SKIP (dup): {title[:40]} -- {reason}")
                    continue

                # Check 3: Name-only fuzzy check against this run's finds
                norm_name = dedup._normalize_name(title)
                if norm_name in seen_this_run:
                    continue

                # === NEW LEAD — collect contact info ===
                    print(f"    NEW: {title[:50]}")
                contact = extract_contact(url)

                lead = {
                    "name": title[:100],
                    "city": city,
                    "website": url,
                    "email": contact["email"],
                    "phone": contact["phone"],
                    "snippet": r["snippet"][:200],
                    "domain": domain,
                }

                found.append(lead)
                seen_this_run.add(domain)
                seen_this_run.add(norm_name)
                dedup.register(name=title, website=url, email=contact["email"])

                if len(found) >= max_results:
                    return found

    return found


# ---------------------------------------------------------------------------
# CSV Handling
# ---------------------------------------------------------------------------

def load_leads_from_csv(filepath):
    """Load leads from an existing CSV file."""
    leads = []
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return leads

    with open(filepath, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            leads.append({
                "name": row.get("name", ""),
                "city": row.get("city", ""),
                "website": row.get("website", ""),
                "email": row.get("email", ""),
                "phone": row.get("phone", ""),
                "snippet": row.get("notes", ""),
                "domain": Deduplicator()._extract_domain(row.get("website", "")),
            })
    return leads


def save_leads_csv(leads):
    """Save new leads to leads.csv (append)."""
    file_exists = os.path.exists(LEADS_CSV)
    existing_count = 0

    if file_exists:
        with open(LEADS_CSV, "r", encoding="utf-8") as f:
            existing_count = sum(1 for _ in csv.DictReader(f))

    with open(LEADS_CSV, "a", newline="", encoding="utf-8") as f:
        fields = ["name", "city", "website", "email", "phone", "snippet",
                   "audit_score", "audit_issues_count", "status", "added_date"]
        writer = csv.DictWriter(f, fieldnames=fields)
        if not file_exists:
            writer.writeheader()

        for lead in leads:
            writer.writerow({
                "name": lead.get("name", ""),
                "city": lead.get("city", ""),
                "website": lead.get("website", ""),
                "email": lead.get("email", ""),
                "phone": lead.get("phone", ""),
                "snippet": lead.get("snippet", ""),
                "audit_score": lead.get("audit_score", ""),
                "audit_issues_count": lead.get("audit_issues_count", ""),
                "status": "new",
                "added_date": datetime.now().strftime("%Y-%m-%d"),
            })

    return existing_count, len(leads)


# ---------------------------------------------------------------------------
# Pipeline Runner
# ---------------------------------------------------------------------------

def run_pipeline(cities=None, max_audits=10, skip_audit=False, import_file=None):
    """Run the full pipeline: find → dedup → audit → rank."""
    print("=" * 60)
    print("SOLAR LEAD PIPELINE — Zero Duplicates Guaranteed")
    print("=" * 60)

    # Step 1: Initialize dedup engine (loads ALL existing data)
    print("\n[1/5] Loading existing data for deduplication...")
    dedup = Deduplicator()

    # Step 2: Find or load leads
    if import_file:
        print(f"\n[2/5] Loading leads from {import_file}...")
        all_leads = load_leads_from_csv(import_file)
        # Dedup even imported leads
        new_leads = []
        for lead in all_leads:
            is_dup, reason = dedup.is_duplicate(
                name=lead["name"], website=lead["website"], email=lead["email"]
            )
            if not is_dup:
                new_leads.append(lead)
                dedup.register(name=lead["name"], website=lead["website"], email=lead["email"])
        skipped = len(all_leads) - len(new_leads)
        print(f"  Loaded: {len(all_leads)}, After dedup: {len(new_leads)} (skipped {skipped})")
    else:
        print(f"\n[2/5] Searching for solar companies...")
        cities_to_use = cities or DEFAULT_CITIES
        new_leads = find_solar_companies(
            cities_to_use, SEARCH_QUERIES, dedup,
            max_results=max_audits * 2  # find more than we'll audit
        )
        print(f"\n  Found {len(new_leads)} NEW unique leads")

    if not new_leads:
        print("\nNo new leads found. Try expanding cities or wait a few days.")
        return

    # Step 3: Audit each lead
    audited_leads = []
    if not skip_audit:
        print(f"\n[3/5] Auditing {min(len(new_leads), max_audits)} leads...")
        for i, lead in enumerate(new_leads[:max_audits], 1):
            print(f"\n  [{i}/{min(len(new_leads), max_audits)}] {lead['name'][:40]}")
            if lead["website"]:
                audit = run_audit(lead["website"], lead["name"], lead["city"])
                lead["audit"] = audit
                lead["audit_score"] = audit.get("score", {}).get("score", "")
                lead["audit_issues_count"] = len(audit.get("score", {}).get("issues", []))
                lead["audit_issues"] = audit.get("score", {}).get("issues", [])
                lead["audit_wins"] = audit.get("score", {}).get("wins", [])
                save_audit(audit)
                time.sleep(2)  # be nice to PageSpeed API
            else:
                lead["audit_score"] = ""
                lead["audit_issues_count"] = 0
                lead["audit_issues"] = []
                lead["audit_wins"] = []
            audited_leads.append(lead)
    else:
        audited_leads = new_leads[:max_audits]

    # Step 4: Rank by opportunity (more issues = better pitch)
    print(f"\n[4/5] Ranking leads by opportunity...")
    audited_leads.sort(
        key=lambda x: (
            int(x.get("audit_score") or 0),
            x.get("audit_issues_count") or 0
        ),
        reverse=True
    )

    # Step 5: Save everything
    print(f"\n[5/5] Saving results...")
    count_before, count_added = save_leads_csv(audited_leads)
    dedup.save_log(audited_leads)

    # Save detailed audit rankings
    ranking_file = os.path.join(AUDIT_DIR, "rankings.json")
    os.makedirs(AUDIT_DIR, exist_ok=True)
    ranking_data = []
    for rank, lead in enumerate(audited_leads, 1):
        ranking_data.append({
            "rank": rank,
            "name": lead["name"],
            "city": lead["city"],
            "website": lead["website"],
            "email": lead["email"],
            "phone": lead["phone"],
            "audit_score": lead.get("audit_score", ""),
            "top_issues": lead.get("audit_issues", [])[:3],
        })
    with open(ranking_file, "w", encoding="utf-8") as f:
        json.dump(ranking_data, f, indent=2, ensure_ascii=False)

    # Print summary
    print(f"\n{'='*60}")
    print(f"PIPELINE COMPLETE")
    print(f"{'='*60}")
    print(f"New leads found:    {len(new_leads)}")
    print(f"Leads audited:      {len(audited_leads)}")
    print(f"Leads saved:        {count_added}")
    print(f"Total in CSV:       {count_before + count_added}")
    print(f"Rankings saved:     {ranking_file}")

    # Print top 5 opportunities
    print(f"\n{'='*60}")
    print("TOP 5 OPPORTUNITIES (contact these first):")
    print(f"{'='*60}")
    for lead in ranking_data[:5]:
        score = lead.get("audit_score", "?")
        issues = lead.get("top_issues", [])
        print(f"\n  #{lead['rank']} {lead['name'][:40]} ({lead['city']})")
        print(f"     Score: {score}/100 | Issues: {len(issues)}")
        print(f"     Email: {lead['email'] or 'N/A'} | Phone: {lead['phone'] or 'N/A'}")
        if issues:
            print(f"     Top issue: {issues[0][:60]}")

    print(f"\nNext step: python ../02-OUTREACH/audit_outreach.py --rankings {ranking_file}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Solar Lead Pipeline")
    parser.add_argument("--cities", type=str, help="Comma-separated city list")
    parser.add_argument("--max", type=int, default=10, help="Max audits to run")
    parser.add_argument("--skip-audit", action="store_true", help="Skip audit step (fast)")
    parser.add_argument("--import", type=str, dest="import_file", help="Import leads from CSV")

    args = parser.parse_args()

    cities = None
    if args.cities:
        cities = [c.strip() for c in args.cities.split(",")]

    run_pipeline(
        cities=cities,
        max_audits=args.max,
        skip_audit=args.skip_audit,
        import_file=args.import_file,
    )


if __name__ == "__main__":
    main()
