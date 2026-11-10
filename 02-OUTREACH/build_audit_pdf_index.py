#!/usr/bin/env python3
"""Regenerate 02-OUTREACH/AUDIT_PDF_INDEX.md from the PDFs and JSONs on disk.

Run from the repo root:
    python3 02-OUTREACH/build_audit_pdf_index.py
"""
import glob
import json
import os
import re

import pypdf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANCH = "arena/eb03c2c4-performance-marketing-os"
BASE = f"https://github.com/vamsy16/performance-marketing-os/blob/{BRANCH}"
FOLDERS = [
    ("Full audits", "02-OUTREACH/audit_pdfs", "audit_*.pdf",
     "audit_results", "The complete 5-page DIGITAL MARKETING & PAID ADS AUDIT: "
     "website tracking, conversion readiness, technical snapshot and audit score."),
    ("Ads reports", "02-OUTREACH/ads_only_pdfs", "audit_*.pdf",
     "ads_only_results", "Since 2026-10-25 these use the *same* 5-page Ksquare "
     "layout and carry live website data; before that date they were the shorter "
     "ad-activity sheet."),
]


def score_of(a):
    """Score for the index column, from either JSON shape.

    Batch-10+ ads reports keep it at site_audit.score.score; the older full
    audits keep it at score.score. Reading only one path silently under-counts.
    """
    sa = a.get("site_audit") or {}
    s = (sa.get("score") or {}).get("score")
    if s is None:
        s = (a.get("score") or {}).get("score")
    if s is None:
        return None
    return f"{s}/100"


def date_of(a):
    for k in ("audit_date", "checked_on", "checked_at", "generated_at"):
        v = a.get(k)
        if v:
            return str(v)[:16]
    return ""


def company_of(a, fallback):
    return a.get("company") or a.get("legal") or fallback


def _norm(x):
    return re.sub(r"[^a-z0-9]", "", str(x or "").lower())


_JSON_CACHE = {}


def load_json(json_dir, stem):
    """Load the JSON behind a PDF.

    The PDF filename is derived from the company's *legal* name while the JSON
    filename is derived from the lead key, so the two do not always share a
    stem - audit_UDK_Electrical_Industries_Private_Limited.pdf is backed by
    audit_UDK_Electrical_Industries.json. Matching only on the stem silently
    drops the score and the audit date for those rows, so fall back to a
    normalised company-name match across the whole folder.
    """
    key = (json_dir, stem)
    if key in _JSON_CACHE:
        return _JSON_CACHE[key]
    direct = os.path.join(ROOT, "01-LEADS", json_dir, stem + ".json")
    a = {}
    if os.path.exists(direct):
        with open(direct, encoding="utf-8") as f:
            a = json.load(f)
    else:
        # The PDF stem still carries the audit_ prefix; the JSON's
        # company field does not. Strip it before comparing.
        want = _norm(re.sub(r"^audit_", "", stem))
        for jf in glob.glob(os.path.join(ROOT, "01-LEADS", json_dir,
                                         "audit_*.json")):
            try:
                with open(jf, encoding="utf-8") as f:
                    cand = json.load(f)
            except Exception:
                continue
            names = [cand.get("company"), cand.get("legal"),
                     os.path.basename(jf)[:-5]]
            for n in names:
                if n and _norm(re.sub(r"^audit_", "", str(n))) == want:
                    a = cand
                    break
            if a:
                break
    _JSON_CACHE[key] = a
    return a


def rows(folder, json_dir):
    out = []
    for pdf in sorted(glob.glob(os.path.join(ROOT, folder, "audit_*.pdf"))):
        name = os.path.basename(pdf)
        stem = name[:-4]
        a = load_json(json_dir, stem)
        try:
            pages = len(pypdf.PdfReader(pdf).pages)
        except Exception:
            pages = "?"
        size = f"{os.path.getsize(pdf) / 1024:.0f} KB"
        out.append({
            "company": company_of(a, stem.replace("audit_", "").replace("_", " ")),
            "pages": pages,
            "size": size,
            "score": score_of(a) or "—",
            "date": date_of(a) or "—",
            "url": f"{BASE}/{folder}/{name}",
        })
    out.sort(key=lambda r: r["company"].lower())
    return out


def table(rs):
    lines = ["| Company | Pages | Size | Score | Audited | PDF |",
             "|---|---|---|---|---|---|"]
    for r in rs:
        lines.append(
            f"| {r['company']} | {r['pages']} | {r['size']} | {r['score']} | "
            f"{r['date']} | [open]({r['url']}) |")
    return "\n".join(lines)


def main():
    blocks = []
    total_pdfs = 0
    companies = set()
    scored = 0
    for label, folder, _pat, json_dir, blurb in FOLDERS:
        rs = rows(folder, json_dir)
        total_pdfs += len(rs)
        for r in rs:
            companies.add(r["company"])
            if r["score"] != "—":
                scored += 1
        blocks.append(
            f"## {label} — `{folder}/`\n\n"
            f"{blurb}\n\n"
            f"{table(rs)}\n")

    both = []
    names = {}
    for label, folder, _p, jd, _b in FOLDERS:
        for r in rows(folder, jd):
            names.setdefault(r["company"], []).append(label)
    both = sorted(c for c, v in names.items() if len(v) > 1)

    head = [
        "# Every audit PDF in this repo — index",
        "",
        f"**{total_pdfs} PDFs** covering **{len(companies)} companies** "
        f"({scored} of them scored), on branch `{BRANCH}`.",
        "",
        "They live in **two folders**, which is why looking at one folder makes "
        "the total look small:",
        "",
    ]
    for i, (label, folder, _p, _jd, blurb) in enumerate(FOLDERS, start=1):
        n = len(rows(folder, _jd))
        head.append(f"{i}. [`{folder}/`]({BASE}/{folder}) — **{n} {label.lower()}**. {blurb}")
    head.append("")
    if both:
        head.append("> " + ", ".join(both) + f" — {len(both)} "
                    f"compan{'y' if len(both) == 1 else 'ies'} — have **both** a "
                    "full audit and an ads report. That is why "
                    f"{total_pdfs} files cover {len(companies)} companies.")
        head.append("")

    out = "\n".join(head) + "\n" + "\n".join(blocks)
    path = os.path.join(ROOT, "02-OUTREACH/AUDIT_PDF_INDEX.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"wrote {path}")
    print(f"  {total_pdfs} PDFs / {len(companies)} companies / {scored} scored")


if __name__ == "__main__":
    main()
