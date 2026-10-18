#!/usr/bin/env python3
"""
Lead Data Hygiene — repairs and filters scraped lead data.

The original DuckDuckGo scraper glued phone digits and page fragments into
emails (38660sales@enersol.co.in), pulled directory/listicle/blog pages as
"leads", and wrote a structurally broken CSV. This module:

  1. Repairs leads.csv structure (missing newlines between records)
  2. Sanitizes emails (strip glued digits/words, cut garbage TLD tails)
  3. Normalizes phones (+91 formatting, URL-decoding)
  4. Drops non-pitchable URLs (directories, blogs, listicles, gov, ad links)
  5. Rewrites a clean, properly quoted CSV

Usage:
  python lead_data.py                  # clean leads.csv in place
  python lead_data.py --check          # dry run: report only, no write
"""

import argparse
import csv
import io
import os
import re
import sys
from urllib.parse import unquote, urlparse

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LEADS_CSV = os.path.join(BASE_DIR, "leads.csv")

CSV_FIELDS = ["name", "city", "website", "email", "phone", "snippet",
              "audit_score", "audit_issues_count", "status", "added_date"]

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

DOMAIN_TLD_RE = re.compile(
    r"^(?P<base>[a-z0-9.-]*?\.(?:co\.in|com|in|net|org|edu|gov|info|io|ai|me|uk|au|ca))"
    r"(?:[a-z0-9].*)?$")

GLUE_PREFIXES = ("address", "email", "guide", "contact", "whatsapp", "submit")
EMAIL_WORDS = ("info", "sales", "support", "hello", "contact", "enquiry",
               "inquiries", "inquiry", "mktg", "office", "team", "admin")

# Hosts that are directories, marketplaces, listicles, or platforms — not
# pitchable installer businesses.
JUNK_HOSTS = (
    "f6s.com", "aeroleads.com", "starofservice.in", "enfsolar.com",
    "builtindelhi.in", "professnow.com", "renewableaffairs.com",
    "blueblogsolar.com", "greentax.in", "gosolarindex.in", "mytribe.in",
    "solarcalculators.in", "connectsolar.in", "solarvipani.com",
    "urjaone.com", "energydirectory.in", "bing.com", "google.com",
)

# Content/directory paths — dropped only for non-blocklisted hosts too
# (a company blog page is still that company, but /blogs/ on Loom Solar is
# a listicle directory, so path rules run for everyone).
JUNK_PATH_RE = re.compile(
    r"^/(?:blogs?|articles?|profession|listicle|directory)(?:/|$)", re.I)


def host_of(url):
    try:
        host = (urlparse(url if "://" in url else "https://" + url).hostname or "").lower()
        host = host[4:] if host.startswith("www.") else host
        return host if re.match(r"^[a-z0-9.-]+\.[a-z]{2,}$", host) else ""
    except Exception:
        return ""


def is_junk_url(url):
    """True if this URL is a directory/listicle/blog/ad page, not an installer."""
    host = host_of(url)
    if not host:
        return True
    if host.endswith(".gov.in") or host.endswith(".gov"):
        return True
    for jh in JUNK_HOSTS:
        if host == jh or host.endswith("." + jh):
            return True
    path = urlparse(url if "://" in url else "https://" + url).path or "/"
    return bool(JUNK_PATH_RE.match(path))


def clean_text(text):
    """Fix mojibake/replacement characters in scraped names and snippets."""
    text = (text or "").replace("\ufffd", " ")
    text = re.sub(r"[\x00-\x08\x0b-\x1f]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip(" ,")


def sanitize_email(cell):
    """Extract one real email from a garbled scrape cell."""
    m = EMAIL_RE.search(cell or "")
    if not m:
        return ""
    local, _, domain = m.group(0).lower().partition("@")
    local = re.sub(r"^\d+", "", local)               # 38660sales -> sales
    changed = True
    while changed and len(local) > 1:                 # addressinfo / guidecontact+91...
        changed = False
        for pref in GLUE_PREFIXES:
            if local.startswith(pref) and len(local) > len(pref):
                local = local[len(pref):]
                changed = True
                break
    local = re.sub(r"^[+0-9()\-\s]+", "", local)      # leftover +91-8047136984inquiry
    rest, found = local, []
    while rest:                                        # enquiryinfo -> ['enquiry','info']
        for w in sorted(EMAIL_WORDS, key=len, reverse=True):
            if rest.startswith(w):
                found.append(w)
                rest = rest[len(w):]
                break
        else:
            break
    if len(found) >= 2 and not rest:                   # glued words -> take the last
        local = found[-1]
    tld = DOMAIN_TLD_RE.match(domain)
    if not tld or not local or not re.match(r"^[a-z0-9._%+-]+$", local):
        return ""
    return f"{local}@{tld.group('base')}"


def clean_phone(cell):
    """Normalize an Indian phone from scrape garbage."""
    s = unquote(cell or "").strip()
    if not s:
        return ""
    s = re.sub(r"[()\-.]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    digits = re.sub(r"\D", "", s)
    core = digits[2:] if digits.startswith("91") and len(digits) > 10 else digits
    if core and set(core) == {"0"}:                   # placeholder numbers
        return ""
    if re.fullmatch(r"1[89]00\d*", digits):           # toll-free
        return digits
    if s.startswith("+") and digits.startswith("91") and len(digits) >= 12:
        local = digits[2:]
    elif len(digits) == 12 and digits.startswith("91"):
        local = digits[2:]
    elif len(digits) == 11 and digits.startswith("0"):
        local = digits[1:]
    elif len(digits) == 10:
        local = digits
    elif s.startswith("+") and digits:
        return "+" + digits
    else:
        return s if digits else ""
    if not local or set(local) == {"0"}:
        return ""
    return f"+91 {local}"


def repair_csv_text(raw):
    """The old scraper dropped newlines between records — put them back."""
    raw = raw.replace("\r\n", "\n").replace("\r", "\n")
    raw = re.sub(r"(?<=added_date)\s*(?=\")", "\n", raw, count=1)
    raw = re.sub(r"(?<=,\d{4}-\d{2}-\d{2})[ \t]*(?=[^\n,])", "\n", raw)
    return raw


def clean_leads(csv_path=LEADS_CSV, write=True):
    with open(csv_path, "r", encoding="utf-8", errors="replace") as f:
        repaired = repair_csv_text(f.read())

    reader = csv.DictReader(io.StringIO(repaired))
    rows_in = list(reader)

    seen_sites, out, dropped_junk, dropped_dupe, fixed = [], [], 0, 0, 0
    for row in rows_in:
        name = clean_text(row.get("name"))
        website = (row.get("website") or "").strip()
        if not name or not website:
            continue
        if is_junk_url(website):
            dropped_junk += 1
            continue
        host = host_of(website)
        if host in seen_sites:
            dropped_dupe += 1
            continue
        seen_sites.append(host)

        email = sanitize_email(row.get("email"))
        phone = clean_phone(row.get("phone"))
        raw_email, raw_phone = (row.get("email") or "").strip(), (row.get("phone") or "").strip()
        if (email != raw_email and raw_email) or (phone != raw_phone and raw_phone):
            fixed += 1
        out.append({
            "name": name,
            "city": clean_text(row.get("city")),
            "website": website,
            "email": email,
            "phone": phone,
            "snippet": clean_text(row.get("snippet"))[:300],
            "audit_score": (row.get("audit_score") or "").strip(),
            "audit_issues_count": (row.get("audit_issues_count") or "").strip(),
            "status": (row.get("status") or "new").strip() or "new",
            "added_date": (row.get("added_date") or "").strip(),
        })

    stats = {"rows_in": len(rows_in), "kept": len(out),
             "dropped_junk": dropped_junk, "dropped_duplicate_host": dropped_dupe,
             "contacts_fixed": fixed}

    if write and out:
        tmp = csv_path + ".tmp"
        with open(tmp, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=CSV_FIELDS, quoting=csv.QUOTE_MINIMAL)
            w.writeheader()
            w.writerows(out)
        os.replace(tmp, csv_path)
    return stats, out


def main():
    ap = argparse.ArgumentParser(description="Clean and repair leads.csv")
    ap.add_argument("--check", action="store_true", help="dry run, report only")
    args = ap.parse_args()

    stats, rows = clean_leads(write=not args.check)
    mode = "DRY RUN" if args.check else "CLEANED"
    print(f"[{mode}] {os.path.basename(LEADS_CSV)}")
    print(f"  rows parsed:      {stats['rows_in']}")
    print(f"  kept:             {stats['kept']}")
    print(f"  dropped (junk):   {stats['dropped_junk']} (directories/blogs/listicles/ads)")
    print(f"  dropped (dupe):   {stats['dropped_duplicate_host']} (same domain)")
    print(f"  contacts fixed:   {stats['contacts_fixed']} (emails/phones sanitized)")
    if stats["kept"] == 0:
        print("  WARNING: nothing kept — check the source file")
        sys.exit(1)


if __name__ == "__main__":
    main()
