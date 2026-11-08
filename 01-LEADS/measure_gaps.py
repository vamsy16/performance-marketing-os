#!/usr/bin/env python3
"""Measure how much of each page of an audit PDF is actually filled.

Renders every page with pypdfium2 and reports the vertical extent of the
ink (anything that is not near-white) plus the header/footer bands, which are
drawn on every page and must not be counted as body fill.

Usage:  PYTHONPATH=/tmp/pdflibs python3 measure_gaps.py <pdf> [<pdf> ...]
"""
import sys

import pypdfium2 as pdfium
from PIL import Image

HEADER_PX = 95          # branded header band + gold rule (top of every page)
FOOTER_PX = 55          # "Prepared by Vamsi" rule + footer (bottom of every page)
WHITE = 245             # anything this light counts as background


def ink_extent(img):
    """Return (first_ink_row, last_ink_row) of the body area, in pixels."""
    g = img.convert("L")
    w, h = g.size
    px = g.load()
    first = last = None
    for y in range(HEADER_PX, h - FOOTER_PX):
        row_has_ink = False
        for x in range(0, w, 3):          # every 3rd pixel is plenty
            if px[x, y] < WHITE:
                row_has_ink = True
                break
        if row_has_ink:
            if first is None:
                first = y
            last = y
    return first, last


def main(paths):
    for path in paths:
        pdf = pdfium.PdfDocument(path)
        n = len(pdf)
        print("=" * 74)
        print(f"{path}   ({n} pages)")
        worst = 0.0
        for i in range(n):
            img = pdf[i].render(scale=1.4).to_pil()
            first, last = ink_extent(img)
            h = img.size[1]
            body_top, body_bot = HEADER_PX, h - FOOTER_PX
            body_h = body_bot - body_top
            if last is None:
                fill = 0.0
                tail = body_h
            else:
                fill = (last - body_top) / body_h
                tail = body_bot - last
            worst = max(worst, tail / body_h)
            flag = "  <-- GAP" if tail / body_h > 0.12 else ""
            print(f"  page {i+1}: ink rows {first}-{last} of {body_top}-{body_bot}"
                  f"   fill {fill*100:5.1f}%   unused tail {tail/body_h*100:5.1f}%{flag}")
        print(f"  worst unused tail: {worst*100:.1f}%")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
