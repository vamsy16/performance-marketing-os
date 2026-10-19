#!/usr/bin/env python3
"""
Audit PDF Engine — Builds the client-ready audit report PDF.
Combines the website audit with live ad-library research (Meta + Google)
into a branded Smart Pursuit report, ready to send to leads.

Usage:
  python audit_pdf.py "Ksquare Energy"
  python audit_pdf.py --latest
  python audit_pdf.py path/to/audit.json
  python audit_pdf.py --all
"""

import argparse
import glob
import json
import os
import re
import sys
from datetime import datetime
from xml.sax.saxutils import escape

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

BASE_DIR = os.path.dirname(__file__)
AUDIT_DIR = os.path.join(BASE_DIR, "audit_results")
OUT_DIR = os.path.join(os.path.dirname(BASE_DIR), "02-OUTREACH", "audit_pdfs")
LOGO_PATH = os.path.join(os.path.dirname(BASE_DIR), "smart pursuit logo.png")

YOUR_NAME = os.environ.get("SP_NAME", "Vamsi")
YOUR_AGENCY = os.environ.get("SP_AGENCY", "Smart Pursuit")
YOUR_PHONE = os.environ.get("SP_PHONE", "+91 70950 24220")
TAGLINE = "SOLAR GROWTH PARTNER"

PAGE_W, PAGE_H = A4
MARGIN = 16 * mm
CONTENT_W = PAGE_W - 2 * MARGIN

NAVY = colors.HexColor("#0E2A47")
DEEP = colors.HexColor("#16406E")
AMBER = colors.HexColor("#F5A524")
GREEN = colors.HexColor("#137333")
RED = colors.HexColor("#C5221F")
GREY = colors.HexColor("#5F6380")
LIGHT = colors.HexColor("#F4F7FB")
CARD = colors.HexColor("#FAFBFD")
BORDER = colors.HexColor("#D9E2EE")
BLUE = colors.HexColor("#1B6EC2")

FONT = "Helvetica"
FONT_BOLD = "Helvetica-Bold"
BASE14 = True

_SAFE_MAP = {
    "\u20b9": "Rs. ", "\u2013": "-", "\u2014": "-", "\u2018": "'", "\u2019": "'",
    "\u201c": '"', "\u201d": '"', "\u2022": "-", "\u2192": "->", "\u2197": "↗",
    "\u2713": "OK", "\u2717": "X", "\u00a0": " ", "\u25cf": "-", "\u2026": "...",
}


def _register_fonts():
    global FONT, FONT_BOLD, BASE14
    windir = os.environ.get("WINDIR", r"C:\Windows")
    try:
        pdfmetrics.registerFont(TTFont("SP-Regular", os.path.join(windir, "Fonts", "arial.ttf")))
        pdfmetrics.registerFont(TTFont("SP-Bold", os.path.join(windir, "Fonts", "arialbd.ttf")))
        pdfmetrics.registerFontFamily("SP-Regular", normal="SP-Regular", bold="SP-Bold")
        FONT, FONT_BOLD, BASE14 = "SP-Regular", "SP-Bold", False
    except Exception:
        BASE14 = True


def T(text):
    if text is None:
        return ""
    text = str(text)
    if BASE14:
        text = "".join(_SAFE_MAP.get(ch, ch) for ch in text)
        text = text.encode("cp1252", errors="replace").decode("cp1252")
    return escape(text)


def latin_safe(text, placeholder="[Ad copy in regional language - open the ad via the link below]"):
    """Keep only Latin-script ad copy; Indic scripts cannot render in the PDF fonts."""
    if not text:
        return ""
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return ""
    latin = [c for c in letters if ord(c) < 0x250]
    if len(latin) / max(len(letters), 1) < 0.4:
        return placeholder
    text = re.sub(r"[^\x20-\x7E\u00A0-\u024F]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


_register_fonts()

# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------

ST = {
    "kicker": ParagraphStyle("kicker", fontName=FONT_BOLD, fontSize=8, leading=10,
                             textColor=AMBER),
    "h1": ParagraphStyle("h1", fontName=FONT_BOLD, fontSize=24, leading=28, textColor=NAVY),
    "h2": ParagraphStyle("h2", fontName=FONT_BOLD, fontSize=11, leading=14, textColor=colors.white),
    "h3": ParagraphStyle("h3", fontName=FONT_BOLD, fontSize=10.5, leading=13, textColor=NAVY),
    "body": ParagraphStyle("body", fontName=FONT, fontSize=9, leading=13.2,
                           textColor=colors.HexColor("#25303B")),
    "body_b": ParagraphStyle("body_b", fontName=FONT_BOLD, fontSize=9, leading=13.2,
                             textColor=colors.HexColor("#25303B")),
    "small": ParagraphStyle("small", fontName=FONT, fontSize=7.6, leading=10.2, textColor=GREY),
    "small_b": ParagraphStyle("small_b", fontName=FONT_BOLD, fontSize=7.6, leading=10.2, textColor=NAVY),
    "cell": ParagraphStyle("cell", fontName=FONT, fontSize=8.3, leading=11.2,
                           textColor=colors.HexColor("#25303B")),
    "cell_b": ParagraphStyle("cell_b", fontName=FONT_BOLD, fontSize=8.3, leading=11.2,
                             textColor=colors.HexColor("#25303B")),
    "cell_grey": ParagraphStyle("cell_grey", fontName=FONT, fontSize=7.8, leading=10.4, textColor=GREY),
    "link": ParagraphStyle("link", fontName=FONT_BOLD, fontSize=8, leading=11, textColor=BLUE),
    "tile_num": ParagraphStyle("tile_num", fontName=FONT_BOLD, fontSize=19, leading=21,
                               textColor=NAVY, alignment=TA_CENTER),
    "tile_lbl": ParagraphStyle("tile_lbl", fontName=FONT_BOLD, fontSize=6.6, leading=8.5,
                               textColor=GREY, alignment=TA_CENTER),
    "score_num": ParagraphStyle("score_num", fontName=FONT_BOLD, fontSize=34, leading=36,
                                textColor=NAVY, alignment=TA_CENTER),
    "white": ParagraphStyle("white", fontName=FONT, fontSize=8.6, leading=12, textColor=colors.white),
    "white_b": ParagraphStyle("white_b", fontName=FONT_BOLD, fontSize=11, leading=14,
                              textColor=colors.white),
}


# ---------------------------------------------------------------------------
# Audit data helpers
# ---------------------------------------------------------------------------

PIXEL_LABELS = {
    "meta_pixel": "Meta Pixel (Facebook / Instagram ads)",
    "google_ads": "Google Ads conversion tag",
    "google_analytics_ga4": "Google Analytics (GA4)",
    "google_analytics_ua": "Google Analytics (old version)",
    "linkedin_insight": "LinkedIn Insight Tag",
    "microsoft_clarity": "Microsoft Clarity (heatmaps)",
    "hotjar": "Hotjar (heatmaps)",
    "google_tag_manager": "Google Tag Manager",
}

CONVERSION_LABELS = {
    "has_contact_form": "Contact form on homepage",
    "has_phone_click": "Click-to-call phone number",
    "has_whatsapp_link": "WhatsApp chat link",
    "has_live_chat": "Live chat / chatbot",
    "has_popup_optin": "Popup or offer capture",
    "has_testimonials": "Testimonials / social proof",
    "has_pricing_page_link": "Pricing information visible",
}

FIXES = [
    ("No Meta Pixel", "Install the free Meta Pixel - without it you cannot retarget site visitors or measure which ads produce enquiries."),
    ("No Google Ads", "Add the Google Ads conversion tag (via Tag Manager) so every enquiry traces back to a campaign."),
    ("No Google Analytics", "Set up GA4 - right now nothing records how many people visit, where they come from, or which pages convert."),
    ("No contact form", "Put a short enquiry form (name, phone, rooftop size) above the fold on the homepage."),
    ("No WhatsApp", "Add a WhatsApp chat button - WhatsApp converts about 3x better than forms for Indian homeowners."),
    ("CTA button", "Add 2-3 more prominent call-to-action buttons (Get Free Quote) across the homepage."),
    ("No live chat", "Add a free chat widget (Tawk.to) so after-hours visitors still become leads."),
    ("testimonial", "Show recent customer reviews with names and photos next to the enquiry form."),
    ("meta description", "Write a 150-character meta description with your city + service keyword to lift Google click-through."),
    ("H1 tag", "Add exactly one H1 headline containing your main keyword."),
    ("structured data", "Add LocalBusiness schema so Google can show rich results with price and rating."),
    ("Open Graph", "Add Open Graph tags so shared links show a proper preview on WhatsApp and social."),
    ("alt text", "Add descriptive alt text to every image - free SEO that brings image-search traffic."),
    ("favicon", "Add a favicon so your site looks professional in browser tabs."),
    ("Mobile speed", "Compress images and enable caching - slow mobile pages lose more than half of visitors before they enquire."),
    ("live chat", "Add a free chat widget (Tawk.to) so after-hours visitors still become leads."),
]


def suggest_fix(issue):
    text = issue.lower()
    for keyword, fix in FIXES:
        if keyword.lower() in text:
            return fix
    return ""


def score_verdict(score):
    if score >= 50:
        return ("Significant gaps found", RED,
                "Several issues on this page are actively costing you enquiries. Every one of them is fixable within days.")
    if score >= 25:
        return ("Clear quick wins available", AMBER,
                "A handful of gaps are holding back your conversion rate. Fixing them is fast and low-cost.")
    return ("Solid foundation", GREEN,
            "Your homepage is in good shape. The remaining gaps are small but costly - close them before scaling ad spend.")


def next_steps(audit):
    steps = []
    pixels = audit.get("pixels", {})
    conv = audit.get("conversion", {})
    seo = audit.get("seo", {})
    adlib = audit.get("ad_library") or {}

    if adlib and not (adlib.get("google_own") or {}).get("found"):
        steps.append(("Open a Google Ads channel",
                      "No Google Ads presence was found, while competitors bid on the same 'solar + city' searches all day."))
    if adlib and not (adlib.get("meta_own") or {}).get("found"):
        steps.append(("Start Meta (Facebook / Instagram) ads",
                      "No active Meta ads were found. Local solar demand is being caught by competitors' feeds."))
    if not pixels.get("google_analytics_ga4") and not pixels.get("google_analytics_ua"):
        steps.append(("Turn on measurement (GA4)",
                      "Install Google Analytics 4 through Tag Manager - until this exists you cannot tell which marketing works."))
    if not pixels.get("google_ads"):
        steps.append(("Add the Google Ads conversion tag",
                      "Required before spending on Google Ads - otherwise every rupee is untracked."))
    if not pixels.get("meta_pixel"):
        steps.append(("Install the Meta Pixel",
                      "Unlocks retargeting ads to people who already visited your site - the cheapest leads you can buy."))
    if not conv.get("has_live_chat"):
        steps.append(("Capture after-hours enquiries",
                      "Add a chat widget or callback prompt - a share of solar research happens late at night."))
    if seo.get("images_without_alt", 0) > 0:
        steps.append((f"Fix {seo['images_without_alt']} images missing alt text",
                      "A one-hour fix that improves Google rankings and image-search traffic."))
    if not conv.get("has_contact_form"):
        steps.append(("Add an enquiry form above the fold",
                      "Make it effortless for mobile visitors to request a quote."))
    perf = audit.get("pagespeed", {}).get("mobile_performance_score")
    if perf is not None and perf < 50:
        steps.append((f"Speed up mobile (currently {perf}/100)",
                      "Every extra second of load time cuts conversions by roughly 7%."))

    if not steps:
        steps.append(("Scale with Google + Meta ads",
                      "Tracking and conversion basics are in place - paid ads can be launched and measured confidently."))
    return steps[:4]


def days_running(started):
    # Meta's Ad Library prints both "13 Oct 2026" (card DOM) and
    # "Oct 13, 2026" (page text) - accept either.
    for fmt in ("%d %b %Y", "%d %B %Y", "%b %d, %Y", "%B %d, %Y"):
        try:
            start = datetime.strptime(started.strip(), fmt)
            return (datetime.now() - start).days
        except Exception:
            continue
    return None


# ---------------------------------------------------------------------------
# Layout components
# ---------------------------------------------------------------------------

def section_bar(title, note=""):
    tick = Table([[""]], colWidths=[2.2 * mm], rowHeights=[8.5 * mm])
    tick.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), AMBER)]))
    right = Paragraph(T(note), ParagraphStyle(
        "secnote", fontName=FONT, fontSize=7.4, leading=9, textColor=colors.HexColor("#AFC3DA")))
    bar = Table([[tick, Paragraph(f"<b>{T(title)}</b>", ST["h2"]), right]],
                colWidths=[3.2 * mm, CONTENT_W * 0.55, CONTENT_W - 3.2 * mm - CONTENT_W * 0.55])
    bar.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (0, 0), 0),
        ("LEFTPADDING", (1, 0), (1, 0), 5),
        ("RIGHTPADDING", (-1, 0), (-1, 0), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return [Spacer(1, 5.5 * mm), bar, Spacer(1, 2.6 * mm)]


def status_text(ok, yes="OK", no="MISSING"):
    color = "#137333" if ok else "#C5221F"
    return Paragraph(f'<font color="{color}"><b>{T(yes if ok else no)}</b></font>', ST["cell"])


def two_col_status(items):
    rows = []
    for i in range(0, len(items), 2):
        chunk = items[i:i + 2]
        row = []
        for label, ok in chunk:
            row.extend([Paragraph(T(label), ST["cell"]), status_text(ok)])
        while len(row) < 4:
            row.extend([Paragraph("", ST["cell"]), Paragraph("", ST["cell"])])
        rows.append(row)
    table = Table(rows, colWidths=[CONTENT_W * 0.38, CONTENT_W * 0.12, CONTENT_W * 0.38, CONTENT_W * 0.12])
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 3.6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.6),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, LIGHT]),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, BORDER),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
    ]))
    return table


def score_bar(score):
    filled = max(2, min(CONTENT_W - 4, CONTENT_W * score / 100))
    color = GREEN if score < 25 else (AMBER if score < 50 else RED)
    bar = Table([[""]], colWidths=[filled, CONTENT_W - filled], rowHeights=[3.2 * mm])
    bar.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), color),
        ("BACKGROUND", (1, 0), (1, 0), colors.HexColor("#E8EDF4")),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return bar


def stat_tiles(audit):
    no_site = audit.get("no_website")
    score = audit.get("score", {}).get("score", 0)
    issues = len(audit.get("score", {}).get("issues", []))
    pixels = audit.get("pixels", {})
    gaps = sum(1 for v in pixels.values() if not v)
    if no_site:
        gaps = len(PIXEL_LABELS)
    adlib = audit.get("ad_library") or {}
    meta_n = (adlib.get("meta_own") or {}).get("results_count", 0)
    g_detail = (adlib.get("google_own") or {}).get("detail") or {}
    g_n = g_detail.get("ad_count", 0)
    ads_txt = f"{meta_n + g_n}" if (meta_n + g_n) else "0"
    ads_color = GREEN if (meta_n + g_n) else RED

    def tile(num, label, num_color=NAVY):
        return [
            Paragraph(f'<font color="{num_color.hexval()}">{T(num)}</font>', ST["tile_num"]),
            Spacer(1, 0.8 * mm),
            Paragraph(T(label), ST["tile_lbl"]),
        ]

    if no_site:
        score_cell = tile("N/A", "WEBSITE AUDIT", RED)
        issue_cell = tile("0", "ISSUES FOUND", RED)
    else:
        score_cell = tile(str(score) + "/100", "AUDIT SCORE (LOWER IS BETTER)",
                          GREEN if score < 25 else (AMBER if score < 50 else RED))
        issue_cell = tile(str(issues), "ISSUES FOUND")

    tiles = Table([[score_cell, issue_cell,
                    tile(str(gaps), "TRACKING GAPS"),
                    tile(ads_txt, "LIVE ADS RUNNING", ads_color)]],
                  colWidths=[CONTENT_W / 4] * 4)
    tiles.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BACKGROUND", (0, 0), (-1, -1), CARD),
        ("BOX", (0, 0), (-1, -1), 0.6, BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.6, BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return tiles


def score_panel(audit):
    if audit.get("no_website"):
        left = [
            Paragraph("N/A", ParagraphStyle("scn", parent=ST["score_num"], textColor=RED)),
            Paragraph("NO WEBSITE", ST["tile_lbl"]),
        ]
        right = [
            Paragraph('<font color="#C5221F"><b>NO WEBSITE FOUND</b></font>', ST["h3"]),
            Spacer(1, 1.2 * mm),
            Paragraph(
                "This business converts customers directly inside the ad platform "
                "(WhatsApp / Facebook) - there is no website to audit. Every lead lives in a chat "
                "inbox: nothing can be tracked, retargeted, or scaled, and enquiries are lost the "
                "moment the conversation goes cold. This is the strongest possible pitch for a "
                "landing page with real tracking.", ST["body"]),
        ]
        card = Table([[left, right]], colWidths=[CONTENT_W * 0.22, CONTENT_W * 0.78])
        card.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FDF4F3")),
            ("BOX", (0, 0), (-1, -1), 0.7, BORDER),
            ("LINEAFTER", (0, 0), (0, 0), 0.7, BORDER),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (1, 0), (1, 0), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ]))
        return card

    score = audit.get("score", {}).get("score", 0)
    headline, color, verdict = score_verdict(score)
    left = [
        Paragraph(f'{score}', ParagraphStyle("scn", parent=ST["score_num"], textColor=color)),
        Paragraph("ISSUES / 100", ST["tile_lbl"]),
    ]
    right = [
        Paragraph(f'<font color="{color.hexval()}"><b>{T(headline)}</b></font>', ST["h3"]),
        Spacer(1, 1.2 * mm),
        Paragraph(T(verdict), ST["body"]),
        Spacer(1, 2 * mm),
        score_bar(score),
    ]
    card = Table([[left, right]], colWidths=[CONTENT_W * 0.22, CONTENT_W * 0.78])
    card.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
        ("BOX", (0, 0), (-1, -1), 0.7, BORDER),
        ("LINEAFTER", (0, 0), (0, 0), 0.7, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (1, 0), (1, 0), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return card


def priorities_table(issues):
    rows = []
    for i, issue in enumerate(issues[:4], 1):
        fix = suggest_fix(issue)
        detail = f"<br/><b><font color='#137333'>Fix:</font></b> {T(fix)}" if fix else ""
        rows.append([
            Paragraph(f'<font color="#C5221F"><b>{i}</b></font>', ST["cell"]),
            Paragraph(f"<b>{T(issue)}</b>{detail}", ST["cell"]),
        ])
    table = Table(rows, colWidths=[8 * mm, CONTENT_W - 8 * mm])
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.HexColor("#FDF4F3")]),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, BORDER),
    ]))
    return table


def bullets_table(items, color, marker):
    rows = [[Paragraph(f'<font color="{color.hexval()}"><b>{T(marker)}</b></font>', ST["cell"]),
             Paragraph(T(item), ST["cell"])] for item in items]
    table = Table(rows, colWidths=[9 * mm, CONTENT_W - 9 * mm])
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 2.6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6),
    ]))
    return table


def ad_card(ad, platform="Meta"):
    """One live-ad sample: creative image + copy + metadata."""
    img_cell = []
    imgs = ad.get("images") or ad.get("image_files") or []
    for path in imgs[:1]:
        if path and os.path.exists(path):
            try:
                w, h = PILImage.open(path).size
                max_w, max_h = 40 * mm, 40 * mm
                scale = min(max_w / w, max_h / h, 1.0)
                img_cell = [Image(path, width=w * scale, height=h * scale)]
            except Exception:
                img_cell = []

    name = ad.get("page_name") or ad.get("name") or platform
    started = ad.get("started", "")
    days = days_running(started) if started else None
    meta_bits = []
    if started:
        meta_bits.append(f"Running since <b>{T(started)}</b>" + (f" ({days} days)" if days and days > 0 else ""))
    if ad.get("library_id"):
        meta_bits.append(f"Library ID {T(ad['library_id'])}")
    if ad.get("ad_count"):
        meta_bits.append(f"~{ad['ad_count']} live ads on Google")

    copy = latin_safe(ad.get("text", ""))
    copy_html = f'"{T(copy)}"' if copy and not copy.startswith("[") else T(copy)

    link = ad.get("library_url") or ad.get("url") or ""
    link_html = (f'<link href="{escape(link)}" color="#1B6EC2"><b>Open the live ad</b></link>'
                 if link else "")

    text_cell = [
        Paragraph(f'<b>{T(name)}</b>', ST["cell_b"]),
        Paragraph("  |  ".join(meta_bits) if meta_bits else platform, ST["small"]),
        Spacer(1, 1 * mm),
        Paragraph(copy_html[:400], ST["cell_grey"]),
    ]
    if link_html:
        text_cell += [Spacer(1, 1 * mm), Paragraph(link_html, ST["link"])]

    if img_cell:
        content = Table([[img_cell, text_cell]], colWidths=[43 * mm, CONTENT_W - 43 * mm - 8 * mm])
    else:
        content = Table([[text_cell]], colWidths=[CONTENT_W - 8 * mm])
    content.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0 if img_cell else 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))

    wrap = Table([[content]], colWidths=[CONTENT_W])
    wrap.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.white),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return KeepTogether([wrap, Spacer(1, 2.2 * mm)])


def empty_box(text):
    box = Table([[Paragraph(T(text), ST["cell"])]], colWidths=[CONTENT_W])
    box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return box


def facts_table(rows_data):
    rows = [[Paragraph(T(l), ST["cell_b"]), Paragraph(T(v), ST["cell"])] for l, v in rows_data]
    table = Table(rows, colWidths=[CONTENT_W * 0.36, CONTENT_W * 0.64])
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 3.2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, LIGHT]),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, BORDER),
    ]))
    return table


def steps_table(steps):
    rows = []
    for i, (title, detail) in enumerate(steps, 1):
        rows.append([
            Paragraph(f'<font color="#0E2A47"><b>{i}</b></font>', ST["cell"]),
            Paragraph(f"<b>{T(title)}</b><br/>{T(detail)}", ST["cell"]),
        ])
    table = Table(rows, colWidths=[8 * mm, CONTENT_W - 8 * mm])
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, BORDER),
    ]))
    return table


def logo_flowable(width=15 * mm):
    path = white_logo_path()
    if not path:
        return None
    try:
        w, h = PILImage.open(path).size
        return Image(path, width=width, height=width * h / w)
    except Exception:
        return None


def white_logo_path():
    """Recolour the dark logo to white so it can sit directly on the navy band."""
    if not os.path.exists(LOGO_PATH):
        return None
    out_dir = os.path.join(AUDIT_DIR, "_branding")
    out = os.path.join(out_dir, "logo_white.png")
    try:
        if os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(LOGO_PATH):
            return out
        os.makedirs(out_dir, exist_ok=True)
        im = PILImage.open(LOGO_PATH).convert("RGBA")
        alpha = im.split()[3]
        white = PILImage.merge(
            "RGBA",
            (PILImage.new("L", im.size, 255),
             PILImage.new("L", im.size, 255),
             PILImage.new("L", im.size, 255),
             alpha))
        white.save(out)
        return out
    except Exception:
        return LOGO_PATH


def cta_card(audit):
    company = audit.get("company") or audit.get("website", "your company")
    logo = logo_flowable(17 * mm)
    logo_cell = [logo] if logo else []
    body = [
        Paragraph("Ready to fix this - and start capturing those leads?", ST["white_b"]),
        Spacer(1, 1.8 * mm),
        Paragraph(
            f"{T(YOUR_AGENCY)} builds lead engines for solar companies using Google Ads, Meta Ads and local SEO. "
            f"Reply to this report or call {T(YOUR_PHONE)} for a free 10-minute walkthrough - we will show you "
            f"what to fix first, what it costs, and what it should return in extra enquiries. No pitch, no obligation.",
            ST["white"]),
        Spacer(1, 2.6 * mm),
        Paragraph(f"<b>{T(YOUR_NAME)}</b>  |  {T(YOUR_AGENCY)}  |  {T(YOUR_PHONE)}  |  Solar marketing specialist",
                  ParagraphStyle("ctac", fontName=FONT_BOLD, fontSize=8.6, leading=11, textColor=AMBER)),
    ]
    cols = ([logo_cell, body] if logo else [body])
    widths = ([22 * mm, CONTENT_W - 22 * mm] if logo else [CONTENT_W])
    card = Table([cols], colWidths=widths)
    card.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("VALIGN", (0, 0), (0, 0), "MIDDLE") if logo else ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (0, 0), 10),
        ("LEFTPADDING", (1, 0), (1, 0), 4) if logo else ("LEFTPADDING", (0, 0), (0, 0), 12),
        ("RIGHTPADDING", (-1, 0), (-1, 0), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 11),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 11),
        ("LINEBEFORE", (0, 0), (0, 0), 3, AMBER),
    ]))
    return card


# ---------------------------------------------------------------------------
# Ads-only story (live ad activity, website audit NOT run)
# ---------------------------------------------------------------------------

ADS_ONLY_LABEL = "LIVE AD ACTIVITY"


def honesty_banner(audit):
    """The panel that keeps an ads-only report from looking like a full audit.

    An ads-only report is built ONLY from public Meta Ad Library data. The
    website half of the audit (pixels, tracking, PageSpeed, conversion
    elements, score) is not run, so it must be stated - never implied.
    """
    checked = audit.get("checked_on") or audit.get("generated_at") or ""
    website = audit.get("website") or ""
    company = audit.get("company") or "this company"
    body = [
        Paragraph('<font color="#B26A00"><b>WEBSITE AUDIT NOT RUN</b></font>', ST["h3"]),
        Spacer(1, 1.2 * mm),
        Paragraph(
            f"This report covers <b>live ad activity only</b>, read from the public Meta Ad "
            f"Library on {T(checked)}. No website was fetched, so it contains "
            f"<b>no audit score, no tracking/pixel findings, no page-speed data and no "
            f"conversion checklist</b> - those numbers are only real once the full pipeline "
            f"runs. The complete report for {T(company)} is produced with:<br/>"
            f"<font color='#1B6EC2'>python run_pipeline.py {T(website)} \"{T(company)}\" "
            f"--city {T(audit.get('city') or 'Hyderabad')}</font>", ST["body"]),
    ]
    banner = Table([[body]], colWidths=[CONTENT_W])
    banner.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFF7E6")),
        ("BOX", (0, 0), (-1, -1), 0.8, AMBER),
        ("LINEBEFORE", (0, 0), (0, 0), 3, AMBER),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return banner


def ads_only_tiles(audit):
    adlib = audit.get("ad_library") or {}
    meta_own = adlib.get("meta_own") or {}
    ads = meta_own.get("ads") or []
    n_ads = len(ads)
    started = [a.get("started", "") for a in ads if a.get("started")]
    oldest = None
    days = []
    for s in started:
        d = days_running(s)
        if d is not None:
            days.append(d)
    if days:
        oldest = max(days)
    funnel = audit.get("funnel") or {}
    funnel_txt = funnel.get("type") or "Not determined"

    def tile(num, label, num_color=NAVY):
        return [
            Paragraph(f'<font color="{num_color.hexval()}">{T(num)}</font>', ST["tile_num"]),
            Spacer(1, 0.8 * mm),
            Paragraph(T(label), ST["tile_lbl"]),
        ]

    ads_color = GREEN if n_ads else RED
    tiles = Table([[
        tile(n_ads, "LIVE ADS RUNNING", ads_color),
        tile(f"{oldest} days" if oldest is not None else "-", "LONGEST-RUNNING AD"),
        tile(funnel_txt, "WHERE CLICKS LAND", AMBER if "form" in funnel_txt.lower() else NAVY),
        tile("Meta", "SOURCE"),
    ]], colWidths=[CONTENT_W / 4] * 4)
    tiles.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BACKGROUND", (0, 0), (-1, -1), CARD),
        ("BOX", (0, 0), (-1, -1), 0.6, BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.6, BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return tiles


def build_ads_only_story(audit):
    story = []
    company = audit.get("company") or audit.get("website", "")
    city = audit.get("city", "")
    adlib = audit.get("ad_library") or {}
    meta_own = adlib.get("meta_own") or {}
    ads = meta_own.get("ads") or []
    funnel = audit.get("funnel") or {}

    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph(ADS_ONLY_LABEL, ST["kicker"]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(Paragraph(T(company), ST["h1"]))
    story.append(Spacer(1, 1.5 * mm))
    meta_line = " &nbsp;·&nbsp; ".join(
        T(x) for x in [city, audit.get("website", ""),
                       f"Ad data pulled {audit.get('checked_on', '')}"] if x)
    story.append(Paragraph(meta_line, ParagraphStyle(
        "metaline", parent=ST["small"], fontSize=8.4, leading=11)))
    story.append(Spacer(1, 2 * mm))
    story.append(HRFlowable(width="100%", thickness=1.4, color=AMBER, spaceBefore=1, spaceAfter=3))

    story.append(honesty_banner(audit))
    story.append(Spacer(1, 3.5 * mm))

    if adlib.get("summary"):
        story.append(Paragraph(f"<b>Executive summary.</b> {T(adlib['summary'])}", ST["body"]))
    story.append(Spacer(1, 3.5 * mm))
    story.append(ads_only_tiles(audit))
    story.append(Spacer(1, 3.5 * mm))

    story.extend(section_bar("Your live ads - Meta (Facebook / Instagram)",
                             "source: Meta Ad Library"))
    if ads:
        story.append(Paragraph(
            f"<b>{len(ads)} live ad{'s' if len(ads) != 1 else ''} verified.</b> "
            f"These are publicly visible in the Ad Library right now - click any ad to open it.",
            ST["body"]))
        story.append(Spacer(1, 2.5 * mm))
        for ad in ads[:4]:
            story.append(ad_card(ad, "Meta"))
    else:
        story.append(empty_box(
            "No active Meta ads were found for this company. Competitors in your city are buying "
            "this attention instead - which is itself the finding worth acting on."))

    story.extend(section_bar("Where your ad clicks land", "the funnel behind the spend"))
    if funnel:
        story.append(facts_table([
            ("Destination type", funnel.get("type", "Not determined")),
            ("Destination", funnel.get("destination", "Not determined")),
            ("What that means", funnel.get("meaning", "")),
        ]))
    else:
        story.append(empty_box("No ad destination was captured for this lead."))

    findings = audit.get("findings") or []
    if findings:
        story.extend(section_bar("What I found", "read live, not guessed"))
        story.append(bullets_table(findings, RED, "!"))

    steps = audit.get("next_steps") or []
    if steps:
        story.extend(section_bar("Recommended next steps", "what I would do first"))
        story.append(steps_table(steps))

    facts = audit.get("contact_facts") or []
    if facts:
        story.extend(section_bar("Verified contact details", "read from the live site / ad"))
        story.append(facts_table(facts))

    story.append(Spacer(1, 6 * mm))
    story.append(cta_card(audit))
    story.append(Spacer(1, 2.5 * mm))
    story.append(Paragraph(
        f"Ad-library data is live public data from the Meta Ad Library, read on "
        f"{audit.get('checked_on', '')}. No website audit, tracking check or page-speed test was "
        f"performed for this report - run the full pipeline for the complete audit. Generated by "
        f"the {YOUR_AGENCY} audit engine.", ST["small"]))
    return story


def generate_ads_only_pdf(audit, out_path=None):
    """Render an ads-only (live ad activity) report. Returns the output path."""
    company = audit.get("company") or audit.get("website", "audit")
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", company)[:50]
    ads_only_dir = os.path.join(os.path.dirname(BASE_DIR), "02-OUTREACH", "ads_only_pdfs")
    if out_path is None:
        os.makedirs(ads_only_dir, exist_ok=True)
        out_path = os.path.join(ads_only_dir, f"audit_{slug}.pdf")

    doc = SimpleDocTemplate(
        out_path, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN, topMargin=32 * mm, bottomMargin=15 * mm,
        title=f"Ads Audit (live ad activity) - {company}",
        author=f"{YOUR_NAME} - {YOUR_AGENCY}",
        subject="Live Meta ad activity report - website audit not included",
    )
    doc.build(build_ads_only_story(audit), onFirstPage=header_footer, onLaterPages=header_footer)
    return out_path


# ---------------------------------------------------------------------------
# Story
# ---------------------------------------------------------------------------

def build_story(audit):
    story = []
    company = audit.get("company") or audit.get("website", "")
    city = audit.get("city", "")
    seo = audit.get("seo", {})
    conv = audit.get("conversion", {})
    perf = audit.get("pagespeed", {})
    page_count = audit.get("page_count", {})
    local = audit.get("local_signals", {})
    issues = audit.get("score", {}).get("issues", [])
    wins = audit.get("score", {}).get("wins", [])
    adlib = audit.get("ad_library")

    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph("DIGITAL MARKETING & PAID ADS AUDIT", ST["kicker"]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(Paragraph(T(company), ST["h1"]))
    story.append(Spacer(1, 1.5 * mm))
    meta_line = " &nbsp;·&nbsp; ".join(
        T(x) for x in [city, audit.get("final_url") or audit.get("website", ""),
                       f"Audited {audit.get('audit_date', '')}"] if x)
    story.append(Paragraph(meta_line, ParagraphStyle(
        "metaline", parent=ST["small"], fontSize=8.4, leading=11)))
    story.append(Spacer(1, 2 * mm))
    story.append(HRFlowable(width="100%", thickness=1.4, color=AMBER, spaceBefore=1, spaceAfter=3))

    if adlib and adlib.get("summary"):
        story.append(Paragraph(f"<b>Executive summary.</b> {T(adlib['summary'])}", ST["body"]))
    else:
        story.append(Paragraph(
            "This report checks the things that decide whether website visitors become enquiries: "
            "tracking, ad readiness, conversion elements and page health - measured live on your website.",
            ST["body"]))
    story.append(Spacer(1, 3.5 * mm))
    story.append(stat_tiles(audit))
    story.append(Spacer(1, 3.5 * mm))
    story.append(score_panel(audit))

    story.extend(section_bar("Top priorities", "what to fix first"))
    if audit.get("no_website"):
        story.append(priorities_table([
            "No website exists - all leads stay inside WhatsApp / Facebook chat and cannot be tracked or retargeted",
            "No tracking of any kind can be installed without a web property (pixels, GA4, conversions)",
            "Build a landing page with enquiry form + Meta Pixel + GA4 to start converting this ad traffic you already pay for",
        ]))
    else:
        story.append(priorities_table(issues if issues else
                                      ["No critical issues detected - focus on scaling ads with clean tracking in place."]))

    story.append(PageBreak())

    # ---- Ad intelligence ----
    meta_own = (adlib or {}).get("meta_own") or {}
    google_own = (adlib or {}).get("google_own") or {}
    meta_comp = (adlib or {}).get("meta_competitors") or {}
    google_comp = (adlib or {}).get("google_competitors") or {}

    story.extend(section_bar("Your live ads - Meta (Facebook / Instagram)",
                             "source: Meta Ad Library"))
    if adlib is None:
        story.append(empty_box("Ad-library research not run yet. Execute:  python ad_library.py --latest"))
    else:
        if meta_own.get("ads"):
            n = meta_own.get("results_count", len(meta_own["ads"]))
            story.append(Paragraph(
                f"<b>{n} active ad results found.</b> Your Meta presence is live - the creatives below are "
                f"publicly visible in the Ad Library right now.", ST["body"]))
            story.append(Spacer(1, 2.5 * mm))
            for ad in meta_own["ads"][:3]:
                story.append(ad_card(ad, "Meta"))
        else:
            story.append(empty_box(
                "No active Meta ads were found for this company. Competitors in your city are buying this "
                "attention instead - see the competitor section below."))

    story.extend(section_bar("Your live ads - Google (Search / YouTube / Display)",
                             "source: Google Ads Transparency Center"))
    if adlib is None:
        story.append(empty_box("Ad-library research not run yet. Execute:  python ad_library.py --latest"))
    else:
        g_detail = google_own.get("detail") or {}
        if google_own.get("found") and g_detail.get("ad_count"):
            story.append(Paragraph(
                f"<b>Roughly {g_detail['ad_count']} live ads</b> are listed under this advertiser in Google's "
                f"transparency centre.", ST["body"]))
            story.append(Spacer(1, 2 * mm))
            story.append(ad_card({"name": g_detail.get("name", company),
                                  "ad_count": g_detail.get("ad_count"),
                                  "url": g_detail.get("url", ""),
                                  "images": g_detail.get("image_files", []),
                                  "text": ""}, "Google"))
        else:
            story.append(empty_box(
                "No Google Ads advertiser record was found for this company or domain. That means nobody is "
                "bidding on searches like 'solar panel price in " + (city or "your city") +
                "' in your name - a high-intent demand your competitors can take for free."))

    story.extend(section_bar("Competitor ad activity", "who is buying attention in your market"))

    if meta_comp.get("ads"):
        story.append(Paragraph(
            f"<b>Meta:</b> about {meta_comp.get('results_count', 0)} live competitor ads matched "
            f"'{T(meta_comp.get('query', ''))}'. Sample creatives below.", ST["body"]))
        story.append(Spacer(1, 2.5 * mm))
        for ad in meta_comp["ads"][:3]:
            story.append(ad_card(ad, "Meta"))
    elif adlib is not None:
        story.append(empty_box("No clearly relevant competitor Meta ads were captured for this market."))

    g_comps = google_comp.get("advertisers") or []
    if g_comps:
        story.append(Paragraph(
            "<b>Google Ads:</b> Indian solar advertisers currently active in the transparency centre:",
            ST["body"]))
        story.append(Spacer(1, 2 * mm))
        rows = []
        for adv in g_comps:
            det = adv.get("detail") or {}
            url = det.get("url") or adv.get("url") or ""
            link = (f'<link href="{escape(url)}" color="#1B6EC2"><b>View ads</b></link>' if url else "")
            rows.append([
                Paragraph(T(adv.get("name", "")), ST["cell_b"]),
                Paragraph(f"~{adv.get('ad_count', 0)} live ads", ST["cell"]),
                Paragraph(T(adv.get("country", "IN")), ST["cell"]),
                Paragraph(link, ST["cell"]),
            ])
        table = Table(rows, colWidths=[CONTENT_W * 0.42, CONTENT_W * 0.2, CONTENT_W * 0.14, CONTENT_W * 0.24])
        table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 3.4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3.4),
            ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, LIGHT]),
            ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
            ("LINEBELOW", (0, 0), (-1, -1), 0.4, BORDER),
        ]))
        story.append(table)
        story.append(Spacer(1, 2 * mm))
        story.append(Paragraph(
            "These advertisers prove the channel works in your category. The gap is yours to take.",
            ST["small"]))

    story.append(PageBreak())

    # ---- Website health ----
    story.extend(section_bar("Website tracking & pixels", "can you measure anything at all?"))
    pixel_items = [(label, bool(audit.get("pixels", {}).get(key)))
                   for key, label in PIXEL_LABELS.items()]
    story.append(two_col_status(pixel_items))
    story.append(Spacer(1, 2.2 * mm))
    missing = [label for label, ok in pixel_items if not ok]
    if missing:
        story.append(Paragraph(
            f"<b>{len(missing)} of {len(pixel_items)} tracking tools are missing.</b> Without them you cannot "
            "retarget past visitors, and you cannot tell which campaign produced a lead - which is exactly "
            "what stops paid ads from scaling profitably.", ST["body"]))
    else:
        story.append(Paragraph("Full tracking stack detected - paid campaigns can be measured accurately.", ST["body"]))

    story.extend(section_bar("Conversion readiness", "how easily a visitor becomes an enquiry"))
    conv_items = [(label, bool(conv.get(key))) for key, label in CONVERSION_LABELS.items()]
    conv_items.insert(3, (f"Call-to-action buttons: {conv.get('has_cta_buttons', 0)} on homepage",
                          conv.get("has_cta_buttons", 0) >= 3))
    story.append(two_col_status(conv_items))

    story.extend(section_bar("What is already working"))
    story.append(bullets_table(wins if wins else ["No major strengths detected on the homepage."], GREEN, "OK"))

    story.extend(section_bar("Technical snapshot"))
    seo_rows = [
        ("SSL / HTTPS", "Yes" if audit.get("ssl") else "NO - security and ranking issue"),
        ("Server response time", f"{audit.get('load_time_seconds', 'N/A')} seconds"),
        ("Mobile page speed",
         f"{perf['mobile_performance_score']}/100" if perf.get("mobile_performance_score") is not None
         else f"Not available at audit time ({perf.get('error', 'no data')})"),
        ("Largest contentful paint", perf.get("largest_contentful_paint") or "Not available"),
        ("Page title", seo.get("title_text") or "MISSING"),
        ("Meta description", f"Present ({seo.get('meta_desc_length', 0)} characters)"
         if seo.get("has_meta_description") else "MISSING - lower Google click-through"),
        ("H1 headline", seo.get("h1_text") or "MISSING"),
        ("Structured data (Schema)", "Present" if seo.get("has_schema") else "MISSING"),
        ("Open Graph tags", "Present" if seo.get("has_og_tags") else "MISSING"),
        ("Images on homepage", f"{seo.get('image_count', 0)} total, "
         f"{seo.get('images_without_alt', 0)} missing alt text"),
        ("Indexed pages (sitemap)", str(page_count.get("sitemap_pages", "unknown"))
         if page_count.get("has_sitemap") else "No sitemap found"),
        ("Google Maps / local SEO", "Maps embedded on homepage" if local.get("has_google_maps_embed")
         else "No Google Maps embed on homepage"),
    ]
    story.append(facts_table(seo_rows))

    story.extend(section_bar("Recommended next steps", "your 30-day action plan"))
    story.append(steps_table(next_steps(audit)))

    story.append(Spacer(1, 6 * mm))
    story.append(cta_card(audit))
    story.append(Spacer(1, 2.5 * mm))
    story.append(Paragraph(
        f"Report generated automatically on {datetime.now().strftime('%d %b %Y, %H:%M')} by the {YOUR_AGENCY} "
        "audit engine. Website findings reflect the homepage at the time of the audit; ad-library data is live "
        "public data from Meta and Google. Provided free of charge for evaluation purposes.",
        ST["small"]))
    return story


def header_footer(canvas, doc):
    canvas.saveState()
    page = doc.page

    if page == 1:
        band_h = 26 * mm
        canvas.setFillColor(NAVY)
        canvas.rect(0, PAGE_H - band_h, PAGE_W, band_h, stroke=0, fill=1)
        canvas.setFillColor(AMBER)
        canvas.rect(0, PAGE_H - band_h - 1.6 * mm, PAGE_W, 1.6 * mm, stroke=0, fill=1)

        logo = white_logo_path()
        if logo:
            panel = 18 * mm
            x, y = MARGIN, PAGE_H - band_h + (band_h - panel) / 2
            canvas.drawImage(logo, x, y, panel, panel,
                             mask="auto", preserveAspectRatio=True, anchor="c")
            tx = x + panel + 5 * mm
        else:
            tx = MARGIN

        canvas.setFillColor(colors.white)
        canvas.setFont(FONT_BOLD, 15)
        canvas.drawString(tx, PAGE_H - 12.5 * mm, "SMART PURSUIT")
        canvas.setFont(FONT, 7.6)
        canvas.setFillColor(colors.HexColor("#AFC3DA"))
        canvas.drawString(tx, PAGE_H - 17 * mm, TAGLINE)
        canvas.setFont(FONT_BOLD, 8.5)
        canvas.setFillColor(colors.white)
        canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 11.5 * mm, "ADS AUDIT REPORT")
        canvas.setFont(FONT, 7.6)
        canvas.setFillColor(colors.HexColor("#AFC3DA"))
        canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 16 * mm,
                               datetime.now().strftime("%d %B %Y"))
    else:
        canvas.setFillColor(NAVY)
        canvas.rect(0, PAGE_H - 13 * mm, PAGE_W, 13 * mm, stroke=0, fill=1)
        canvas.setFillColor(AMBER)
        canvas.rect(0, PAGE_H - 14 * mm, PAGE_W, 1 * mm, stroke=0, fill=1)
        canvas.setFillColor(colors.white)
        canvas.setFont(FONT_BOLD, 9)
        canvas.drawString(MARGIN, PAGE_H - 8.6 * mm, "SMART PURSUIT")
        canvas.setFont(FONT, 7.3)
        canvas.setFillColor(colors.HexColor("#AFC3DA"))
        canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 8.6 * mm, "ADS AUDIT REPORT")

    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.6)
    canvas.line(MARGIN, 11.5 * mm, PAGE_W - MARGIN, 11.5 * mm)
    canvas.setFont(FONT, 7.3)
    canvas.setFillColor(GREY)
    canvas.drawString(MARGIN, 8 * mm, f"Prepared by {YOUR_NAME}  |  {YOUR_AGENCY}  |  {YOUR_PHONE}")
    canvas.drawRightString(PAGE_W - MARGIN, 8 * mm, f"Page {page}")
    canvas.restoreState()


def generate_pdf(audit, out_path=None):
    """Render one audit dict to a branded PDF. Returns the output path."""
    company = audit.get("company") or audit.get("website", "audit")
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", company)[:50]
    if out_path is None:
        os.makedirs(OUT_DIR, exist_ok=True)
        out_path = os.path.join(OUT_DIR, f"audit_{slug}.pdf")

    doc = SimpleDocTemplate(
        out_path, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN, topMargin=32 * mm, bottomMargin=15 * mm,
        title=f"Ads Audit - {company}",
        author=f"{YOUR_NAME} - {YOUR_AGENCY}",
        subject="Free ads, tracking and conversion readiness audit",
    )
    doc.build(build_story(audit), onFirstPage=header_footer, onLaterPages=header_footer)
    return out_path


# ---------------------------------------------------------------------------
# CLI
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


def main():
    parser = argparse.ArgumentParser(description="Generate the branded audit PDF for a lead")
    parser.add_argument("target", nargs="?", help="Company name, website, or path to an audit JSON")
    parser.add_argument("--latest", action="store_true", help="Use the most recent audit")
    parser.add_argument("--all", action="store_true", dest="all_audits", help="Generate for every audit")
    parser.add_argument("--out", type=str, help="Explicit output PDF path")
    args = parser.parse_args()

    if not all_audits():
        print("No audits found. Run first:")
        print("  python ads_audit.py https://example.com")
        return

    jobs = []
    if args.all_audits:
        jobs = all_audits()
    elif args.latest:
        jobs = all_audits()[:1]
    elif args.target:
        path, audit = find_audit(args.target)
        if not audit:
            print(f"No audit found matching '{args.target}'")
            for p, a in all_audits():
                print(f"  - {a.get('company') or a.get('website')}")
            return
        jobs = [(path, audit)]
    else:
        parser.print_help()
        print("\nTip: python audit_pdf.py --latest")
        return

    print("=" * 60)
    print(f"GENERATING {len(jobs)} AUDIT PDF(S)")
    print("=" * 60)

    for path, audit in jobs:
        name = audit.get("company") or audit.get("website", "")
        if "error" in audit:
            print(f"  SKIP {name}: audit has errors")
            continue
        out = generate_pdf(audit, args.out if len(jobs) == 1 else None)
        score = audit.get("score", {}).get("score", "?")
        has_ads = bool(audit.get("ad_library"))
        print(f"\n  Lead:    {name}")
        print(f"  Score:   {score}/100 | ad-library data: {'YES' if has_ads else 'MISSING - run ad_library.py'}")
        print(f"  PDF:     {out}")

    print(f"\nNext: attach the PDF to your outreach email (02-OUTREACH/templates/)")


if __name__ == "__main__":
    main()
