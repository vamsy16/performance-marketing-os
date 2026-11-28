#!/usr/bin/env python3
"""Delivery gate — the last check before an audit PDF may be sent.

`verify_report.py` proves the PDF agrees with its JSON. This gate proves the
JSON itself is a complete, freshly measured, pipeline-built report and that
the PDF carries no draft/hold markers. A report that fails here is an internal
draft, not a deliverable — regardless of what any other gate printed.

Usage:
  python delivery_gate.py "SunSolar Power Systems"
  python delivery_gate.py --latest
  python delivery_gate.py --json audit_results/audit_X.json

Exit 0 = deliverable, 1 = HOLD (do not send), 3 = nothing matched.
"""

import argparse
import glob
import json
import os
import re
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE_DIR)
AUDIT_DIRS = [
    os.path.join(BASE_DIR, "audit_results"),
    os.path.join(BASE_DIR, "ads_only_results"),
]
PDF_DIRS = [
    os.path.join(ROOT, "02-OUTREACH", "audit_pdfs"),
    os.path.join(ROOT, "02-OUTREACH", "ads_only_pdfs"),
]

# Markers that only ever appear on a held/internal draft, never on a
# client-ready Smart Pursuit report.
DRAFT_MARKERS = (
    "INTERNAL DRAFT",
    "DO NOT SEND",
    "NOT FOR CLIENT DELIVERY",
    "NOT FOR OUTREACH",
    "REVIEW PENDING",
    "REVIEW AND LIVE RECHECK PENDING",
    "SCORE NOT ASSIGNED",
    "NOT SCORED",
    "SOURCE DATE NOT VERIFIED",
    "CURRENT STATUS IS NOT VERIFIED",
)

GENERATORS = {"run_pipeline.py", "ads_only_report.py", "discover_leads.py"}


def slug(name):
    return re.sub(r"[^a-zA-Z0-9]+", "_", name or "")[:50]


def _parse(value):
    if not value:
        return None
    text = str(value).strip()
    try:
        return __import__("datetime").datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        pass
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d", "%d %b %Y"):
        try:
            return __import__("datetime").datetime.strptime(text, fmt)
        except ValueError:
            continue
    return None


def find_report(company="", json_path=""):
    if json_path:
        path = json_path if os.path.isabs(json_path) else os.path.join(BASE_DIR, json_path)
        if os.path.isfile(path):
            return path
        return None
    if not company:
        return None
    target = f"audit_{slug(company)}.json"
    for directory in AUDIT_DIRS:
        path = os.path.join(directory, target)
        if os.path.isfile(path):
            return path
    # Substring fallback for names whose slug differs slightly.
    for directory in AUDIT_DIRS:
        for path in sorted(glob.glob(os.path.join(directory, "audit_*.json"))):
            try:
                with open(path, encoding="utf-8") as fh:
                    audit = json.load(fh)
            except Exception:
                continue
            if company.lower() in (audit.get("company") or "").lower():
                return path
    return None


def pdf_path_for(json_path, audit):
    name = f"audit_{slug(audit.get('company') or os.path.basename(json_path)[6:-5])}.pdf"
    ads_only = bool(audit.get("ads_only"))
    directory = PDF_DIRS[1] if ads_only else PDF_DIRS[0]
    return os.path.join(directory, name)


def gate_company(company, json_path="", pdf_path=None, max_age_minutes=1440):
    """Return (ok, human-readable lines). Never raises on a bad report."""
    lines = []
    failures = []
    path = find_report(company, json_path)
    if not path:
        return False, [f"HOLD: no audit JSON found for '{company or json_path}'"]

    try:
        with open(path, encoding="utf-8") as fh:
            audit = json.load(fh)
    except Exception as exc:
        return False, [f"HOLD: cannot read {path} ({exc})"]

    company = audit.get("company") or company or os.path.basename(path)
    lines.append(f"report: {company}")
    lines.append(f"json:   {path}")

    # --- structural gate (the PDF must agree with its own JSON) -------------
    import verify_report
    if audit.get("ads_only"):
        _, built_pdf, errs = verify_report.verify_ads_only(path, audit)
    else:
        _, built_pdf, errs = verify_report.verify(path, audit)
    for err in errs:
        failures.append("structure: " + err)

    # --- mandatory website completeness (no "Not checked in this pass") -----
    import audit_completeness
    if audit_completeness.has_website_audit(audit):
        missing_checks = audit_completeness.unresolved(audit)
        if missing_checks:
            failures.append("hold: unresolved mandatory website checks — "
                            + ", ".join(missing_checks))
            failures.append("  A deliverable full audit must resolve every website check "
                            "from live page evidence; re-run the pipeline or hold the report.")

    pdf = pdf_path or built_pdf
    if not os.path.isfile(pdf):
        failures.append(f"PDF: not found at {pdf}")
    else:
        lines.append(f"pdf:    {pdf}")

    # --- completeness: nothing held, nothing unreachable, nothing empty ----
    if audit.get("review_pending"):
        failures.append("hold: review_pending is true — internal draft only")
    if audit.get("error"):
        failures.append(f"hold: website audit error stored in JSON ({audit['error']})")

    adlib = audit.get("ad_library") or {}
    for key in ("meta_own", "google_own", "meta_competitors", "google_competitors"):
        part = adlib.get(key) or {}
        if part.get("error") or part.get("status") == "unreachable":
            failures.append(f"hold: {key} source unreachable ({part.get('error')})")
    own_ads = (adlib.get("meta_own") or {}).get("ads") or []
    if not own_ads:
        failures.append("hold: zero live own ads — this lead must not get a PDF")
    for index, ad in enumerate(own_ads, 1):
        for key in ("library_id", "library_url", "text"):
            if not ad.get(key):
                failures.append(f"hold: own ad #{index} missing {key}")

    site = audit.get("site_audit") or audit
    score = (site.get("score") or {}).get("score")
    if not isinstance(score, (int, float)) or isinstance(score, bool):
        failures.append("hold: no numeric audit score (NOT SCORED is not deliverable)")

    for key in ("audit_date", "checked_on"):
        stamp = _parse(audit.get(key))
        if stamp is None:
            failures.append(f"hold: {key} is not a real date ('{audit.get(key)}')")
    prov = audit.get("provenance") or {}
    generator = prov.get("generator")
    if generator not in GENERATORS:
        failures.append(f"hold: provenance.generator is '{generator}' — "
                        "PDF was not built by the repo pipeline")
    run_at = _parse(prov.get("run_at"))
    if run_at is None:
        failures.append("hold: provenance.run_at missing or invalid")
    elif max_age_minutes >= 0:
        import datetime
        now = datetime.datetime.now()
        if run_at.tzinfo is not None:
            run_at = run_at.replace(tzinfo=None)
        age = abs((now - run_at).total_seconds()) / 60
        if age > max_age_minutes:
            failures.append(f"hold: report is {age:.0f} min old (max {max_age_minutes})")

    # --- PDF draft markers and score panel ---------------------------------
    if os.path.isfile(pdf):
        try:
            from pypdf import PdfReader
            flat = " ".join(" ".join((p.extract_text() or "").split())
                            for p in PdfReader(pdf).pages)
            upper = flat.upper()
            for marker in DRAFT_MARKERS:
                if marker in upper:
                    failures.append(f"hold: draft marker in PDF — '{marker}'")
            if audit_completeness.has_website_audit(audit):
                # A legitimate measured absence says "6 of 8 tools were not
                # found"; that is not an unresolved check. These two phrases
                # are held-draft markers and must never ship.
                for marker in ("NOT CHECKED IN THIS PASS", "NOT CHECKED - NOT MEASURED"):
                    if marker in upper:
                        failures.append(
                            f"hold: PDF contains '{marker.title()}' in a full audit "
                            "— every mandatory website check must be resolved "
                            "from live evidence, never left unchecked")
            if not re.search(r"\b\d{1,3}\s*/\s*100\b", flat):
                failures.append("hold: PDF has no numeric /100 score panel")
            for ad in own_ads[:5]:
                lib_id = ad.get("library_id")
                if lib_id and lib_id not in flat:
                    failures.append(f"hold: PDF missing live ad Library ID {lib_id}")
        except Exception as exc:
            failures.append(f"PDF: cannot inspect text ({exc})")

    if failures:
        lines.append("DELIVERY GATE: HOLD")
        for failure in failures:
            lines.append(f"  x {failure}")
        lines.append("  Fix by re-running the pipeline with fresh live data. "
                     "Never hand-edit a PDF or JSON.")
        return False, lines

    lines.append("DELIVERY GATE: PASS — complete, fresh, pipeline-built, no draft markers")
    lines.append("  Gate 2 (report-reviewer) and Gate 3 (verify_live.py) are still mandatory.")
    return True, lines


def main(argv=None):
    ap = argparse.ArgumentParser(description="Fail-closed delivery gate for audit PDFs")
    ap.add_argument("company", nargs="?", default="", help="company name")
    ap.add_argument("--json", default="", help="explicit audit JSON path")
    ap.add_argument("--latest", action="store_true", help="gate the most recent report")
    ap.add_argument("--max-age-minutes", type=int, default=1440,
                    help="maximum report age in minutes (default 1440)")
    args = ap.parse_args(argv)

    json_path = args.json
    company = args.company
    if args.latest and not json_path:
        candidates = []
        for directory in AUDIT_DIRS:
            candidates += glob.glob(os.path.join(directory, "audit_*.json"))
        if candidates:
            json_path = sorted(candidates, key=os.path.getmtime, reverse=True)[0]

    ok, lines = gate_company(company, json_path,
                             max_age_minutes=args.max_age_minutes)
    for line in lines:
        print(line)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
