#!/usr/bin/env python3
"""
Ad Library Research Engine — Pulls live ads from Meta Ad Library and Google Ads
Transparency Center using a real headless browser, then merges the findings into
an existing website audit JSON so outreach PDFs can show actual ad activity.

Usage:
  python ad_library.py "Ksquare Energy" --city Hyderabad
  python ad_library.py "Ksquare Energy" --website https://ksquareenergy.com
  python ad_library.py --latest
  python ad_library.py "Ksquare Energy" --competitors 3 --no-images
"""

import argparse
import glob
import json
import os
import re
import sys
import time
from datetime import datetime
from urllib.parse import quote_plus, unquote, urlparse

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import requests

BASE_DIR = os.path.dirname(__file__)
AUDIT_DIR = os.path.join(BASE_DIR, "audit_results")
IMG_DIR = os.path.join(AUDIT_DIR, "ad_images")

META_BASE = "https://www.facebook.com/ads/library/"
GOOGLE_BASE = "https://adstransparency.google.com/"

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")


def slugify(text, limit=40):
    return re.sub(r"[^a-zA-Z0-9]+", "_", text or "ad")[:limit]


# ---------------------------------------------------------------------------
# Image download
# ---------------------------------------------------------------------------

def download_image(url, out_dir, referer=None, timeout=20):
    """Download an ad creative image. Returns local path or None."""
    try:
        headers = {"User-Agent": UA}
        if referer:
            headers["Referer"] = referer
        resp = requests.get(url, headers=headers, timeout=timeout, stream=True)
        if resp.status_code != 200:
            return None
        ctype = resp.headers.get("content-type", "")
        ext = ".jpg"
        if "png" in ctype:
            ext = ".png"
        elif "webp" in ctype:
            ext = ".webp"
        os.makedirs(out_dir, exist_ok=True)
        fname = f"{slugify(os.path.basename(urlparse(url).path), 30)}_{abs(hash(url)) % 10**8}{ext}"
        path = os.path.join(out_dir, fname)
        with open(path, "wb") as f:
            for chunk in resp.iter_content(8192):
                f.write(chunk)
        if os.path.getsize(path) < 2000:
            os.remove(path)
            return None
        return path
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Meta Ad Library
# ---------------------------------------------------------------------------

def _meta_extract_round(page):
    """Parse ad cards currently present in the DOM."""
    ads = []
    loc = page.locator("text=/Library ID:/")
    for i in range(loc.count()):
        el = loc.nth(i)
        try:
            info = el.evaluate("""el => {
                let n = el;
                let best = null;
                for (let k=0;k<14;k++){
                    if (!n.parentElement) break;
                    n = n.parentElement;
                    const t = n.innerText || '';
                    if (t.includes('Sponsored') && t.includes('Library ID') && t.length > 60 && t.length < 2500) {
                        best = n;
                        break;
                    }
                }
                if (!best) best = el.parentElement || el;
                const imgs = Array.from(best.querySelectorAll('img'))
                    .map(i => i.src)
                    .filter(s => s.includes('scontent') && !s.includes('s60x60') && !s.includes('s32x32') && !s.includes('s24x24'));
                return {text: best.innerText, imgs: imgs.slice(0, 4)};
            }""")
        except Exception:
            continue

        text = info.get("text", "")
        m_id = re.search(r"Library ID:\s*(\d+)", text)
        m_start = re.search(r"Started running on\s+(.+)", text)
        m_page = re.search(r"\n([^\n]+)\nSponsored\n", text)
        lib_id = m_id.group(1) if m_id else ""
        ads.append({
            "library_id": lib_id,
            "page_name": (m_page.group(1).strip() if m_page else ""),
            "started": (m_start.group(1).strip() if m_start else ""),
            "text": text.split("Sponsored\n", 1)[-1].strip()[:700],
            "image_urls": info.get("imgs", [])[:3],
            "images": [],
            "library_url": f"https://www.facebook.com/ads/library/?id={lib_id}" if lib_id else "",
        })
    return ads


def _meta_destinations(page):
    """Map library_id -> {destination, whatsapp} from the raw SSR page HTML.

    Each ad card's CTA link sits inline as an l.facebook.com/l.php?u=<url>
    redirect (or a WhatsApp wa.me / api.whatsapp.com link). Splitting the HTML
    by 'Library ID:' attributes each destination to its card.
    """
    try:
        raw = page.content()
    except Exception:
        return {}
    raw = raw.replace("\\/", "/")
    raw = re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)), raw)
    out = {}
    for seg in re.split(r"Library ID:", raw)[1:]:
        m_id = re.match(r"\s*(\d+)", seg)
        if not m_id:
            continue
        dest, wa = "", ""
        for u in re.findall(r"https://l\.facebook\.com/l\.php\?u=([^\"&\s]+)", seg):
            try:
                d = unquote(u)
            except Exception:
                continue
            if d.startswith("http") and "facebook.com" not in d and "instagram.com" not in d:
                dest = d
                break
        wm = re.search(r"https://(?:api\.whatsapp\.com/send\?phone=|wa\.me/)([0-9]+)", seg)
        if wm:
            wa = wm.group(1)
        if dest or wa:
            out.setdefault(m_id.group(1), {"destination": dest, "whatsapp": wa})
    return out


def meta_search(page, query, country="IN", max_ads=6):
    """Search Meta Ad Library, scrolling and extracting incrementally."""
    url = (f"{META_BASE}?active_status=active&ad_type=all&country={country}"
           f"&q={quote_plus(query)}&search_type=keyword_unordered")
    try:
        page.goto(url, timeout=60000, wait_until="domcontentloaded")
        page.wait_for_timeout(9000)
    except Exception as e:
        return {"query": query, "results_label": "", "results_count": 0,
                "ads": [], "error": str(e), "url": url}

    body = page.inner_text("body")
    m = re.search(r"~?([\d,]+)\s+results?", body)
    results_count = int(m.group(1).replace(",", "")) if m else 0

    unique = {}
    for round_i in range(6):
        for ad in _meta_extract_round(page):
            key = ad["library_id"] or (ad["page_name"] + "|" + ad["text"][:60])
            if key not in unique:
                unique[key] = ad
        if len(unique) >= max_ads:
            break
        try:
            page.mouse.wheel(0, 2400)
            page.wait_for_timeout(1800)
        except Exception:
            break

    ads = list(unique.values())[:max_ads]
    dests = _meta_destinations(page)
    for ad in ads:
        d = dests.get(ad["library_id"], {})
        ad["destination"] = d.get("destination", "")
        ad["whatsapp"] = d.get("whatsapp", "")
    return {
        "query": query,
        "results_label": (m.group(0) if m else "0 results"),
        "results_count": results_count,
        "ads": ads,
        "url": url,
    }


def name_matches(company, page_name):
    """True if a Meta page name plausibly belongs to the audited company."""
    def norm(s):
        s = re.sub(r"[^a-z0-9 ]", " ", (s or "").lower())
        drop = {"pvt", "ltd", "private", "limited", "co", "company", "the", "solar",
                "energy", "power", "systems", "india", "indian"}
        return {w for w in s.split() if w and w not in drop and len(w) > 1}

    a, b = norm(company), norm(page_name)
    if not a or not b:
        return False
    return len(a & b) >= 1 or a <= b or b <= a


# ---------------------------------------------------------------------------
# Google Ads Transparency Center
# ---------------------------------------------------------------------------

def google_search_advertisers(page, query, wait_ms=4500):
    """Type into Ads Transparency search and read advertiser suggestions."""
    try:
        page.goto(f"{GOOGLE_BASE}?hl=en&region=anywhere", timeout=60000, wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        box = page.locator("input").first
        box.click()
        box.type(query, delay=50)
        page.wait_for_timeout(wait_ms)
    except Exception as e:
        return {"query": query, "advertisers": [], "error": str(e)}

    rows = page.evaluate("""() => {
        const list = document.querySelector('.advertisers-list');
        if (!list) return [];
        return Array.from(list.querySelectorAll('.advertiser-suggestion')).map(e => ({
            text: e.innerText.replace(/\\n/g, ' | '),
            cls: e.className,
        }));
    }""")

    advertisers = []
    for r in rows:
        parts = [p.strip() for p in r["text"].split("|") if p.strip()]
        if not parts:
            continue
        name = parts[0]
        country = ""
        ad_count = 0
        for p in parts[1:]:
            m = re.search(r"~?([\d,]+)\s*ads?", p, re.I)
            if m:
                ad_count = int(m.group(1).replace(",", ""))
            elif p.lower() in ("india", "in"):
                country = "IN"
            elif len(p) == 3 and p.isalpha() and p.upper() not in ("ADS",):
                country = p.upper()
            elif p.lower() in ("south africa", "united states", "united kingdom"):
                country = p
        if name and name.lower() != "advertisers":
            advertisers.append({"name": name, "country": country, "ad_count": ad_count})

    return {"query": query, "advertisers": advertisers}


def google_open_advertiser(page, advertiser):
    """Open an advertiser page, return ad count + creative image urls."""
    aid = advertiser.get("advertiser_id", "")
    name = advertiser.get("name", "")
    url = f"{GOOGLE_BASE}advertiser/{aid}?hl=en&region=anywhere" if aid else \
        f"{GOOGLE_BASE}?hl=en&region=anywhere&q={quote_plus(name)}"

    if not aid:
        found = google_search_advertisers(page, name)
        if not found["advertisers"]:
            return {"url": url, "ad_count": 0, "images": [], "found": False}
        advertiser = found["advertisers"][0]
        aid = ""
        # re-search and click through DOM
        page.goto(f"{GOOGLE_BASE}?hl=en&region=anywhere", timeout=60000, wait_until="domcontentloaded")
        page.wait_for_timeout(2500)
        box = page.locator("input").first
        box.click()
        box.type(name, delay=50)
        page.wait_for_timeout(4000)
        clicked = page.evaluate("""() => {
            const el = document.querySelector('.advertiser-suggestion');
            if (!el) return false;
            el.click();
            return true;
        }""")
        if not clicked:
            return {"url": url, "ad_count": 0, "images": [], "found": False}

    try:
        if aid:
            page.goto(url, timeout=60000, wait_until="domcontentloaded")
        page.wait_for_timeout(7000)
        for _ in range(4):
            page.mouse.wheel(0, 2000)
            page.wait_for_timeout(2000)
    except Exception as e:
        return {"url": url, "ad_count": 0, "images": [], "found": False, "error": str(e)}

    body = page.inner_text("body")
    m = re.search(r"~?([\d,]+)\s*ads?\b", body)
    ad_count = int(m.group(1).replace(",", "")) if m else 0

    imgs = page.evaluate("""() => {
        const urls = Array.from(document.querySelectorAll('img'))
            .map(i => i.src || i.getAttribute('data-src') || '')
            .concat(Array.from(document.querySelectorAll('source')).map(s => s.srcset || ''));
        const flat = [];
        for (const u of urls) for (const part of u.split(/\\s+/)) if (part.startsWith('http')) flat.push(part);
        return Array.from(new Set(flat.filter(s =>
            (s.includes('googleusercontent') || s.includes('storage.googleapis') || s.includes('gstatic') || s.includes('ggpht')) &&
            !s.includes('favicon') && !s.includes('=s24') && !s.includes('=s48') && !s.includes('=s64') &&
            !s.includes('avatar') && s.length > 60 && !s.endsWith('.ico')
        ))).slice(0, 8);
    }""")

    return {
        "name": advertiser.get("name", name),
        "advertiser_id": aid or advertiser.get("advertiser_id", ""),
        "country": advertiser.get("country", ""),
        "ad_count": ad_count or advertiser.get("ad_count", 0),
        "url": page.url,
        "images": imgs[:4],
        "found": True,
    }


# ---------------------------------------------------------------------------
# Research runner
# ---------------------------------------------------------------------------

def run_research(company, city="", website="", competitors=3, with_images=True):
    """Pull live Meta + Google ad data for a lead and their market."""
    from playwright.sync_api import sync_playwright

    domain = ""
    if website:
        domain = urlparse(website if website.startswith("http") else "https://" + website).netloc.replace("www.", "")

    result = {
        "checked_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "meta_own": {"found": False, "results_count": 0, "results_label": "", "ads": [], "query": company},
        "meta_competitors": {"found": False, "results_count": 0, "results_label": "", "ads": [], "query": ""},
        "google_own": {"found": False, "advertisers": [], "detail": None, "query": company},
        "google_competitors": {"found": False, "advertisers": [], "query": ""},
        "notes": [],
    }

    img_root = os.path.join(IMG_DIR, slugify(company or domain))

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, channel="chrome")
        ctx = browser.new_context(user_agent=UA, locale="en-US",
                                  viewport={"width": 1400, "height": 1000})
        page = ctx.new_page()

        print(f"  [meta] searching own ads: '{company}'")
        meta_own = meta_search(page, company, max_ads=5)
        own_ads = [a for a in meta_own["ads"] if name_matches(company, a.get("page_name", "")) or not a.get("page_name")]
        meta_own["ads"] = own_ads if own_ads else meta_own["ads"][:2]
        meta_own["found"] = bool(meta_own["results_count"]) and bool(own_ads)
        result["meta_own"] = meta_own
        print(f"    -> {meta_own['results_label'] or 'no results'}, {len(meta_own['ads'])} ad cards parsed")

        comp_query = f"solar {city}".strip() if city else "solar company"
        print(f"  [meta] searching competitor ads: '{comp_query}'")
        meta_comp = meta_search(page, comp_query, max_ads=competitors + 8)
        relevant = re.compile(r"solar|rooftop|panel|renewable|photovolta|inverter", re.I)
        excluded = re.compile(r"expo|exhibition|stall|trade.?show|magazine|news", re.I)
        comp_ads, seen_pages = [], set()
        for a in meta_comp["ads"]:
            page_name = a.get("page_name") or ""
            if not page_name or name_matches(company, page_name):
                continue
            if not relevant.search(page_name + " " + a.get("text", "")):
                continue
            if excluded.search(page_name):
                continue
            key = page_name.lower()
            if key in seen_pages:
                continue
            seen_pages.add(key)
            comp_ads.append(a)
            if len(comp_ads) >= competitors:
                break
        meta_comp["ads"] = comp_ads
        meta_comp["found"] = bool(comp_ads)
        result["meta_competitors"] = meta_comp
        print(f"    -> {meta_comp['results_label'] or 'no results'}, {len(comp_ads)} competitor ads kept")

        print(f"  [google] searching advertisers: '{company}'")
        g_own = google_search_advertisers(page, company)
        if domain:
            g_own_dom = google_search_advertisers(page, domain)
            seen = {a["name"].lower() for a in g_own["advertisers"]}
            g_own["advertisers"] += [a for a in g_own_dom["advertisers"] if a["name"].lower() not in seen]
        matched = [a for a in g_own["advertisers"] if name_matches(company, a["name"])]
        result["google_own"]["advertisers"] = matched or g_own["advertisers"][:3]
        result["google_own"]["found"] = bool(matched)

        if matched:
            print(f"  [google] opening advertiser page: {matched[0]['name']}")
            detail = google_open_advertiser(page, matched[0])
            result["google_own"]["detail"] = detail
            result["google_own"]["found"] = bool(detail.get("ad_count"))
            print(f"    -> {detail.get('ad_count', 0)} ads")
        else:
            print("    -> no advertiser match (likely not running Google ads)")
            result["notes"].append(
                f"No Google Ads advertiser record found for '{company}'"
                + (f" or '{domain}'" if domain else "") + ".")

        print("  [google] discovering Indian competitor advertisers")
        queries = []
        for a in result["meta_competitors"]["ads"]:
            full = (a.get("page_name") or "").strip()
            if full:
                queries.append(full)
                first = full.split()[0]
                if len(first) > 3:
                    queries.append(first)
        queries += ["Waaree", "Loom Solar", "Tata Power", "Vikram Solar", "Goldi Solar"]
        indian, seen_names = [], set()
        for q in queries:
            if len(indian) >= 3:
                break
            gq = google_search_advertisers(page, q)
            for adv in gq["advertisers"]:
                key = adv["name"].lower()
                if key in seen_names or name_matches(company, adv["name"]):
                    continue
                seen_names.add(key)
                if adv.get("country") == "IN" and adv.get("ad_count", 0) > 0:
                    indian.append(adv)
        indian.sort(key=lambda a: a.get("ad_count", 0), reverse=True)

        for adv in indian[:2]:
            adv["detail"] = google_open_advertiser(page, adv)

        result["google_competitors"]["advertisers"] = indian[:3]
        result["google_competitors"]["found"] = bool(indian)
        result["google_competitors"]["query"] = ", ".join(queries[:3])
        print(f"    -> {len(indian[:3])} Indian advertisers found")

        if with_images:
            all_ads = result["meta_own"]["ads"] + result["meta_competitors"]["ads"]
            for ad in all_ads:
                local = []
                for url in ad.get("image_urls", [])[:2]:
                    path = download_image(url, img_root, referer="https://www.facebook.com/")
                    if path:
                        local.append(path)
                ad["images"] = local

            g_details = []
            if result["google_own"].get("detail"):
                g_details.append(result["google_own"]["detail"])
            g_details += [a["detail"] for a in result["google_competitors"]["advertisers"]
                          if a.get("detail")]
            for det in g_details:
                local = []
                for url in det.get("images", [])[:2]:
                    path = download_image(url, img_root, referer="https://adstransparency.google.com/")
                    if path:
                        local.append(path)
                det["image_files"] = local

        browser.close()

    total_meta = result["meta_own"]["results_count"] + result["meta_competitors"]["results_count"]
    if not result["meta_own"]["found"]:
        result["notes"].append("No active Meta (Facebook/Instagram) ads found for this company.")
    if not result["google_own"]["found"]:
        result["notes"].append("No active Google ads found for this company.")
    result["summary"] = build_summary(result, company, city)
    return result


def build_summary(data, company, city):
    """One-paragraph executive summary of ad activity."""
    meta_n = data["meta_own"].get("results_count", 0)
    g_detail = data["google_own"].get("detail") or {}
    g_n = g_detail.get("ad_count", 0)
    comp_meta = data["meta_competitors"].get("results_count", 0)
    comp_google = len(data["google_competitors"].get("advertisers", []))

    parts = []
    if meta_n:
        parts.append(f"{company} is running active ads on Meta (Facebook/Instagram) — about {meta_n} live results in the Ad Library.")
    else:
        parts.append(f"{company} has no active Meta ads running right now.")
    if g_n:
        parts.append(f"On Google's network, the transparency centre shows roughly {g_n} live ads.")
    else:
        parts.append("No Google Ads advertiser record was found, so search/YouTube demand is going to competitors.")
    if comp_meta or comp_google:
        bits = []
        if comp_meta:
            bits.append(f"~{comp_meta} live Meta ads from competitors in {city or 'the market'}")
        if comp_google:
            bits.append(f"{comp_google} Indian advertisers on Google Ads in the solar category")
        parts.append("Meanwhile " + " and ".join(bits) + " are capturing the same customers.")
    return " ".join(parts)


# ---------------------------------------------------------------------------
# Audit merge + CLI
# ---------------------------------------------------------------------------

def all_audits():
    files = sorted(glob.glob(os.path.join(AUDIT_DIR, "audit_*.json")), key=os.path.getmtime, reverse=True)
    out = []
    for path in files:
        try:
            with open(path, "r", encoding="utf-8") as f:
                out.append((path, json.load(f)))
        except Exception:
            continue
    return out


def find_audit(target):
    if os.path.isfile(target):
        with open(target, "r", encoding="utf-8") as f:
            return target, json.load(f)
    tl = target.lower()
    for path, audit in all_audits():
        if tl in (audit.get("company") or "").lower() or tl in (audit.get("website") or "").lower():
            return path, audit
    return None, None


def save_audit(audit, path=None):
    if path is None:
        name = re.sub(r"[^a-zA-Z0-9]+", "_", audit.get("company") or audit.get("website", ""))[:50]
        path = os.path.join(AUDIT_DIR, f"audit_{name}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(audit, f, indent=2, ensure_ascii=False)
    return path


def main():
    parser = argparse.ArgumentParser(description="Pull live ads from Meta + Google ad libraries")
    parser.add_argument("target", nargs="?", help="Company name or audit JSON path")
    parser.add_argument("--city", type=str, default="", help="City for competitor search")
    parser.add_argument("--website", type=str, default="", help="Website (for domain search)")
    parser.add_argument("--latest", action="store_true", help="Use most recent audit")
    parser.add_argument("--competitors", type=int, default=3, help="Competitor ads to keep")
    parser.add_argument("--no-images", action="store_true", help="Skip downloading ad creatives")
    args = parser.parse_args()

    audit_path, audit = None, None
    if args.latest:
        audits = all_audits()
        if audits:
            audit_path, audit = audits[0]
    elif args.target:
        audit_path, audit = find_audit(args.target)

    company = args.target if not audit else (audit.get("company") or args.target)
    if audit_path and args.target and os.path.isfile(args.target):
        company = audit.get("company") or company
    city = args.city or (audit.get("city", "") if audit else "")
    website = args.website or (audit.get("website", "") if audit else "")

    if audit and not company.lower().startswith("http"):
        pass
    elif company.lower().startswith("http") and audit:
        company = audit.get("company") or company

    print("=" * 60)
    print(f"AD LIBRARY RESEARCH: {company}")
    print("=" * 60)

    data = run_research(company, city=city, website=website,
                        competitors=args.competitors, with_images=not args.no_images)

    if audit:
        audit["ad_library"] = data
        path = save_audit(audit, audit_path)
        print(f"\nMerged into: {path}")
    else:
        path = save_audit({"company": company, "city": city, "website": website,
                           "ad_library": data})
        print(f"\nSaved standalone ad research: {path}")

    print(f"\nSUMMARY: {data['summary']}")
    print(f"Meta own ads:     {data['meta_own']['results_label'] or 'none'}")
    print(f"Google own ads:   {data['google_own']['detail']['ad_count'] if data['google_own'].get('detail') else 'none found'}")
    print(f"Competitor ads:   meta={len(data['meta_competitors']['ads'])}, "
          f"google advertisers={len(data['google_competitors']['advertisers'])}")
    print(f"\nNext: python audit_pdf.py --latest")


if __name__ == "__main__":
    main()
