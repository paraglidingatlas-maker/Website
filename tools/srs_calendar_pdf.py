#!/usr/bin/env python3
"""The SRS 2027 race calendar as one PDF, from the pages that are live (chat 29, 24 Nov 2026).

Reads prototypes/v4/img/calendar/srs-2027/NN-name-2400.webp (01-cover to 13-december, all thirteen must be there)
and writes SRS-2027-Race-Calendar.pdf beside them: A4 landscape, one page each, and share.jpg (the cover at
1200px, the page's link preview). Run it whenever a page's image changes, then tools/v4_srs_calendar.py.
The first PDF (24 Nov) was the design chat's; this makes the same thing so a changed page needs no round trip.

    python3 tools/srs_calendar_pdf.py
"""
import glob
import os

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "prototypes", "v4", "img", "calendar", "srs-2027")

if __name__ == "__main__":
    files = sorted(glob.glob(os.path.join(D, "[0-9][0-9]-*-2400.webp")))
    assert len(files) == 13, "thirteen pages (the cover and twelve months), found %d" % len(files)
    pages = [Image.open(f).convert("RGB") for f in files]
    assert all(p.size == (2400, 1696) for p in pages), "a page is not 2400 x 1696"
    dpi = 2400 / (297 / 25.4)          # 2400px across A4's 297mm
    out = os.path.join(D, "SRS-2027-Race-Calendar.pdf")
    pages[0].save(out, "PDF", save_all=True, append_images=pages[1:], resolution=dpi, quality=92,
                  title="SRS 2027 Race Calendar", author="Aninder Singh / Paragliding Atlas")
    pages[0].resize((1200, 848), Image.LANCZOS).save(os.path.join(D, "share.jpg"), quality=86, optimize=True, progressive=True)
    print("wrote %s (%d pages, %.1f MB) and share.jpg" % (os.path.relpath(out, ROOT), len(pages), os.path.getsize(out) / 1e6))
