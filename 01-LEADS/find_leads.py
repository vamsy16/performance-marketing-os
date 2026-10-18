#!/usr/bin/env python3
"""
Solar Company Lead Finder — Free lead generation for your agency.
Finds solar businesses using free sources, saves to leads.csv.

Usage: python find_leads.py
Needs: pip install requests beautifulsoup4
"""

import csv
import io
import os
import re
import sys
import time
from datetime import datetime

# Fix Windows console encoding for Unicode
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

LEADS_FILE = os.path.join(os.path.dirname(__file__), "leads.csv")

# Your target cities — EDIT THIS
CITIES = [
    "Mumbai", "Pune", "Delhi", "Bangalore", "Hyderabad",
    "Chennai", "Ahmedabad", "Jaipur", "Lucknow", "Surat",
    "Indore", "Nagpur", "Kochi", "Coimbatore", "Bhopal",
]

# Search queries that find solar companies
SEARCH_QUERIES = [
    "solar panel installer {city}",
    "solar energy company {city}",
    "rooftop solar {city}",
    "solar panel installation services {city}",
    "solar power solutions {city}",
]


def load_existing_leads():
    """Load existing leads to avoid duplicates."""
    existing = set()
    if os.path.exists(LEADS_FILE):
        with open(LEADS_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing.add(row.get("name", "").strip().lower())
    return existing


def save_leads(leads):
    """Append leads to CSV."""
    file_exists = os.path.exists(LEADS_FILE)
    with open(LEADS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "name", "city", "phone", "email", "website",
            "source", "status", "notes", "added_date"
        ])
        if not file_exists:
            writer.writeheader()
        writer.writerows(leads)


def search_duckduckgo(query):
    """
    Search DuckDuckGo using the ddgs library (free, no API key needed).
    Returns list of {title, url, snippet}
    """
    results = []
    try:
        from ddgs import DDGS
        with DDGS() as ddgs:
            raw = list(ddgs.text(query, max_results=8))
        for r in raw:
            results.append({
                "title": r.get("title", ""),
                "url": r.get("href", r.get("link", "")),
                "snippet": r.get("body", r.get("snippet", "")),
            })
    except Exception as e:
        print(f"  Search error: {e}")
    return results


def extract_email_from_website(url):
    """Try to find contact email on a website."""
    import requests
    from bs4 import BeautifulSoup

    try:
        if not url.startswith("http"):
            url = "https://" + url
        resp = requests.get(url, timeout=8, headers={
            "User-Agent": "Mozilla/5.0"
        })
        soup = BeautifulSoup(resp.text, "html.parser")
        text = soup.get_text()

        # Find emails
        emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
        # Filter out common non-business emails
        skip = ["example.com", "sentry", "wixpress", "@2x", ".png", ".jpg"]
        for email in emails:
            if not any(s in email.lower() for s in skip):
                return email.lower()
    except:
        pass
    return ""


def extract_phone_from_website(url):
    """Try to find phone number on a website."""
    import requests
    from bs4 import BeautifulSoup

    try:
        if not url.startswith("http"):
            url = "https://" + url
        resp = requests.get(url, timeout=8, headers={
            "User-Agent": "Mozilla/5.0"
        })
        soup = BeautifulSoup(resp.text, "html.parser")
        text = soup.get_text()

        # Indian phone patterns
        phones = re.findall(
            r"(?:\+91[\s-]?)?[6-9]\d{4}[\s-]?\d{5}",
            text
        )
        if phones:
            return phones[0].strip()
    except:
        pass
    return ""


def main():
    print("=" * 60)
    print("SOLAR LEAD FINDER — Free Lead Generation")
    print("=" * 60)

    existing = load_existing_leads()
    print(f"Existing leads in database: {len(existing)}")

    all_new_leads = []

    for city in CITIES:
        print(f"\n--- Searching {city} ---")
        for query_template in SEARCH_QUERIES:
            query = query_template.format(city=city)
            print(f"  Query: {query}")

            results = search_duckduckgo(query)

            for r in results:
                title_lower = r["title"].lower()
                # Filter: must look like a solar business
                if not any(kw in title_lower for kw in [
                    "solar", "energy", "power", "renewable", "photovoltaic"
                ]):
                    continue

                # Skip directories and aggregators
                skip_domains = [
                    "justdial", "sulekha", "yellowpages", "indiamart",
                    "google.com", "facebook.com", "youtube.com",
                    "linkedin.com", "wikipedia.org", "amazon.",
                ]
                if any(d in r["url"].lower() for d in skip_domains):
                    continue

                # Deduplicate by name
                name_key = title_lower[:50]
                if name_key in existing:
                    continue

                existing.add(name_key)

                print(f"    Found: {r['title']}")
                print(f"    URL: {r['url']}")

                all_new_leads.append({
                    "name": r["title"][:100],
                    "city": city,
                    "phone": "",
                    "email": "",
                    "website": r["url"][:200],
                    "source": "duckduckgo",
                    "status": "new",
                    "notes": r["snippet"][:200],
                    "added_date": datetime.now().strftime("%Y-%m-%d"),
                })

            time.sleep(2)  # Be polite to the server

    # Enrich: try to get email/phone from websites
    print(f"\n--- Enriching {len(all_new_leads)} leads (getting contact info) ---")
    for lead in all_new_leads[:30]:  # Limit enrichment to avoid rate limits
        if lead["website"]:
            print(f"  Enriching: {lead['name'][:40]}")
            lead["email"] = extract_email_from_website(lead["website"])
            lead["phone"] = extract_phone_from_website(lead["website"])
            time.sleep(1)

    # Save
    if all_new_leads:
        save_leads(all_new_leads)
        print(f"\n{'=' * 60}")
        print(f"SAVED: {len(all_new_leads)} new leads to {LEADS_FILE}")
        print(f"{'=' * 60}")

        # Summary
        with_email = sum(1 for l in all_new_leads if l["email"])
        with_phone = sum(1 for l in all_new_leads if l["phone"])
        print(f"With email: {with_email}")
        print(f"With phone: {with_phone}")
        print(f"\nNext steps:")
        print(f"1. Open leads.csv and review")
        print(f"2. Run: python 05-CRM/crm.py add --file leads.csv")
        print(f"3. Start outreach using 02-OUTREACH/templates/")
    else:
        print("\nNo new leads found. Try expanding CITIES list.")


if __name__ == "__main__":
    main()
