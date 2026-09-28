#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Writes small test files to test/: two one-page PDFs with real text (for
merge, OCR and so on), a Word document (for LibreOffice's Word to PDF), and an
eight-page demo PDF with drawings, a table and charts for the README's
screenshots (a made-up hiking guide; tools/readme_images.py).

  python3 tools/testfiles.py
"""
import pathlib
import zipfile

OUT = pathlib.Path(__file__).resolve().parent.parent / "test"


def pdf(path, title, lines):
    stream = "BT /F1 28 Tf 72 700 Td (%s) Tj ET\n" % title
    y = 650
    for line in lines:
        stream += "BT /F1 16 Tf 72 %d Td (%s) Tj ET\n" % (y, line)
        y -= 28
    objs = [
        "<< /Type /Catalog /Pages 2 0 R >>",
        "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R "
        "/Resources << /Font << /F1 5 0 R >> >> >>",
        "<< /Length %d >>\nstream\n%sendstream" % (len(stream), stream),
        "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for i, body in enumerate(objs, 1):
        offsets.append(len(out))
        out += b"%d 0 obj\n%s\nendobj\n" % (i, body.encode("latin-1"))
    xref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)
    for off in offsets:
        out += b"%010d 00000 n \n" % off
    out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, xref)
    path.write_bytes(bytes(out))


def docx(path, paragraphs):
    body = "".join("<w:p><w:r><w:t>%s</w:t></w:r></w:p>" % p for p in paragraphs)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml",
                   '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                   '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                   '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                   '<Default Extension="xml" ContentType="application/xml"/>'
                   '<Override PartName="/word/document.xml" ContentType="application/'
                   'vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>')
        z.writestr("_rels/.rels",
                   '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                   '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
                   'relationships/officeDocument" Target="word/document.xml"/></Relationships>')
        z.writestr("word/document.xml",
                   '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                   '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
                   "<w:body>%s</w:body></w:document>" % body)


def write_pdf(path, pages, title):
    """A PDF of Letter pages from content streams, with the standard fonts
    F1 Helvetica, F2 Helvetica-Bold, F3 Times-Roman and F4 Helvetica-Oblique."""
    n = len(pages)
    fonts = ["Helvetica", "Helvetica-Bold", "Times-Roman", "Helvetica-Oblique"]
    font_base = 3 + 2 * n
    info = font_base + len(fonts)
    font_refs = " ".join("/F%d %d 0 R" % (i + 1, font_base + i) for i in range(len(fonts)))
    objs = ["<< /Type /Catalog /Pages 2 0 R >>",
            "<< /Type /Pages /Kids [%s] /Count %d >>" % (" ".join("%d 0 R" % (3 + 2 * i) for i in range(n)), n)]
    for i, stream in enumerate(pages):
        objs.append("<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents %d 0 R "
                    "/Resources << /Font << %s >> >> >>" % (4 + 2 * i, font_refs))
        objs.append("<< /Length %d >>\nstream\n%sendstream" % (len(stream.encode("latin-1")), stream))
    for f in fonts:
        objs.append("<< /Type /Font /Subtype /Type1 /BaseFont /%s /Encoding /WinAnsiEncoding >>" % f)
    objs.append("<< /Title (%s) >>" % title)
    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for i, body in enumerate(objs, 1):
        offsets.append(len(out))
        out += b"%d 0 obj\n%s\nendobj\n" % (i, body.encode("latin-1"))
    xref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)
    for off in offsets:
        out += b"%010d 00000 n \n" % off
    out += b"trailer\n<< /Size %d /Root 1 0 R /Info %d 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, info, xref)
    path.write_bytes(bytes(out))


class Page:
    """A page's drawing operations, in points from the bottom left."""

    def __init__(self):
        self.ops = []

    @staticmethod
    def rgb(hex_color):
        return " ".join("%.3f" % (int(hex_color[i:i + 2], 16) / 255) for i in (1, 3, 5))

    def rect(self, x, y, w, h, fill):
        self.ops.append("%s rg %.1f %.1f %.1f %.1f re f" % (self.rgb(fill), x, y, w, h))

    def frame(self, x, y, w, h, stroke, width=1):
        self.ops.append("%s RG %.1f w %.1f %.1f %.1f %.1f re S" % (self.rgb(stroke), width, x, y, w, h))

    def poly(self, points, fill):
        path = " ".join(("%.1f %.1f m" if i == 0 else "%.1f %.1f l") % p for i, p in enumerate(points))
        self.ops.append("%s rg %s h f" % (self.rgb(fill), path))

    def line(self, points, stroke, width=1):
        path = " ".join(("%.1f %.1f m" if i == 0 else "%.1f %.1f l") % p for i, p in enumerate(points))
        self.ops.append("%s RG %.1f w 1 J 1 j %s S" % (self.rgb(stroke), width, path))

    def circle(self, cx, cy, r, fill):
        k = 0.5523 * r
        self.ops.append(
            "%s rg %.1f %.1f m %.1f %.1f %.1f %.1f %.1f %.1f c %.1f %.1f %.1f %.1f %.1f %.1f c "
            "%.1f %.1f %.1f %.1f %.1f %.1f c %.1f %.1f %.1f %.1f %.1f %.1f c f" % (
                self.rgb(fill), cx + r, cy,
                cx + r, cy + k, cx + k, cy + r, cx, cy + r,
                cx - k, cy + r, cx - r, cy + k, cx - r, cy,
                cx - r, cy - k, cx - k, cy - r, cx, cy - r,
                cx + k, cy - r, cx + r, cy - k, cx + r, cy))

    def ellipse(self, cx, cy, rx, ry, fill):
        self.ops.append("q 1 0 0 %.3f 0 %.1f cm" % (ry / rx, cy - cy * ry / rx))
        self.circle(cx, cy, rx, fill)
        self.ops.append("Q")

    def outline(self, points, stroke, width=1):
        path = " ".join(("%.1f %.1f m" if i == 0 else "%.1f %.1f l") % p for i, p in enumerate(points))
        self.ops.append("%s RG %.1f w 1 j %s h S" % (self.rgb(stroke), width, path))

    def dashed(self, points, stroke, width=1, dash=(6, 4)):
        self.ops.append("[%d %d] 0 d" % dash)
        self.line(points, stroke, width)
        self.ops.append("[] 0 d")

    def text(self, x, y, s, size=12, font=1, color="#1f2937"):
        s = s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        self.ops.append("BT /F%d %.1f Tf %s rg %.1f %.1f Td (%s) Tj ET" % (font, size, self.rgb(color), x, y, s))

    def paragraph(self, x, y, s, width_chars, size=12, font=3, color="#374151", leading=1.45):
        words, line = s.split(), ""
        for w in words:
            if len(line) + len(w) + 1 > width_chars:
                self.text(x, y, line, size, font, color)
                y -= size * leading
                line = w
            else:
                line = (line + " " + w).strip()
        if line:
            self.text(x, y, line, size, font, color)
            y -= size * leading
        return y

    def header(self, title, number):
        self.rect(0, 732, 612, 60, "#4f46e5")
        self.text(54, 754, title, 22, 2, "#ffffff")
        self.text(520, 756, "Juniper Trail  %d" % number, 10, 1, "#c7d2fe")

    def stream(self):
        return "\n".join(self.ops) + "\n"


def mix(a, b, t):
    ca = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    cb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join("%02x" % round(x + (y - x) * t) for x, y in zip(ca, cb))


def demo(path):
    pages = []

    # 1. The cover: a mountain landscape, drawn.
    p = Page()
    for i in range(48):
        y0 = 250 + i * 11
        p.rect(0, y0, 612, 12, mix("#fde68a", "#93c5fd", i / 47))
    p.circle(430, 470, 78, "#fed7aa")
    p.circle(430, 470, 52, "#fdba74")
    p.poly([(0, 300), (0, 380), (90, 470), (170, 410), (262, 560), (360, 430), (450, 505),
            (540, 390), (612, 450), (612, 300)], "#a5b4fc")
    p.poly([(236, 518), (262, 560), (290, 515), (274, 524), (262, 510), (250, 524)], "#ffffff")
    p.poly([(428, 488), (450, 505), (470, 486), (458, 490), (450, 482), (441, 490)], "#ffffff")
    p.poly([(0, 250), (0, 330), (70, 400), (150, 335), (240, 445), (330, 345), (420, 415),
            (520, 320), (612, 375), (612, 250)], "#6366f1")
    p.poly([(0, 200), (0, 280), (110, 330), (210, 270), (300, 320), (400, 262), (500, 300),
            (612, 255), (612, 200)], "#3730a3")
    for i in range(24):
        p.rect(0, i * 10, 612, 11, mix("#059669", "#34d399", i / 23))
    p.poly([(90, 150), (140, 178), (330, 186), (500, 168), (540, 140), (430, 118), (200, 112)], "#60a5fa")
    for y, x0, x1 in ((160, 190, 300), (150, 260, 420), (135, 220, 330)):
        p.line([(x0, y), (x1, y)], "#bfdbfe", 2)
    for x, h in ((40, 70), (62, 52), (560, 80), (585, 58), (520, 46), (30, 40)):
        p.poly([(x - h * 0.28, 60), (x, 60 + h), (x + h * 0.28, 60)], "#065f46")
    p.text(54, 700, "JUNIPER TRAIL", 50, 2, "#1e1b4b")
    p.text(56, 668, "A field guide to the high meadows", 20, 1, "#312e81")
    p.text(56, 28, "Spring 2026 edition  -  Stages, maps, weather and a checklist", 11, 1, "#ecfdf5")
    pages.append(p.stream())

    # 2. The route, as a table.
    p = Page()
    p.header("Route overview", 2)
    y = p.paragraph(54, 690, "The Juniper Trail climbs from the lake at Aldmoor through larch "
                    "woods and open meadows to the pass below Mount Tessel, then drops to the "
                    "old mill at Brannock. Most walkers take four days; each stage ends at a hut "
                    "with beds and a warm meal.", 88)
    rows = [("Stage", "From - to", "Distance", "Climb", "Time"),
            ("1", "Aldmoor - Larch Hut", "11.2 km", "+620 m", "4 h"),
            ("2", "Larch Hut - Meadow Hut", "9.8 km", "+540 m", "3.5 h"),
            ("3", "Meadow Hut - Tessel Pass", "7.4 km", "+710 m", "4 h"),
            ("4", "Tessel Pass - Brannock", "13.1 km", "-1,240 m", "5 h")]
    cols = (54, 110, 310, 400, 480)
    y -= 18
    for i, row in enumerate(rows):
        p.rect(54, y - 8, 504, 28, "#e0e7ff" if i == 0 else ("#f5f7ff" if i % 2 else "#ffffff"))
        for x, cell in zip(cols, row):
            p.text(x + 8, y + 1, cell, 12, 2 if i == 0 else 1, "#1e1b4b" if i == 0 else "#374151")
        y -= 28
    p.line([(54, y + 20), (558, y + 20)], "#c7d2fe", 1)
    y -= 30
    p.rect(54, y - 62, 504, 78, "#ecfdf5")
    p.rect(54, y - 62, 5, 78, "#10b981")
    p.text(74, y - 2, "Tip", 13, 2, "#065f46")
    p.paragraph(74, y - 22, "Start stage 3 early: the pass is clear in the morning, and "
                "afternoon storms are common from July.", 80, 12, 1, "#065f46")
    y -= 110
    p.text(54, y, "Getting there", 16, 2, "#1e1b4b")
    p.paragraph(54, y - 24, "Buses run to Aldmoor twice a day from the valley station. From "
                "Brannock, the mill road leads down to the train in about an hour.", 88)
    pages.append(p.stream())

    # 3. The map: contours, a lake and river, the trail and its huts.
    p = Page()
    p.header("Trail map", 3)
    p.rect(54, 150, 504, 560, "#ecfccb")
    for pts in ([(54, 560), (120, 600), (180, 570), (200, 640), (140, 710), (54, 710)],
                [(420, 150), (470, 210), (558, 230), (558, 150)],
                [(60, 150), (70, 190), (130, 205), (210, 180), (240, 150)]):
        p.poly(pts, "#bbf7d0")
    import math
    for base in (38, 70, 102, 134, 166):
        ring = [(400 + base * (1 + 0.16 * math.sin(3 * t + 0.4) + 0.07 * math.cos(5 * t)) * math.cos(t),
                 520 + base * 0.8 * (1 + 0.16 * math.sin(3 * t + 0.4) + 0.07 * math.cos(5 * t)) * math.sin(t))
                for t in [i * math.pi / 30 for i in range(60)]]
        p.outline(ring, "#a8a29e", 0.8)
    p.ellipse(150, 232, 62, 28, "#93c5fd")
    p.line([(200, 245), (225, 290), (215, 340), (250, 390), (262, 440)], "#60a5fa", 3)
    trail = [(176, 250), (232, 362), (318, 452), (400, 522), (452, 430), (500, 332)]
    p.dashed(trail, "#dc2626", 2.5)
    p.poly([(390, 516), (400, 534), (410, 516)], "#57534e")
    for (x, y), label, dx in zip(trail, ("Aldmoor", "Larch Hut", "Meadow Hut", "Tessel Pass", "", "Brannock"),
                                 (12, 12, -78, 12, 0, 12)):
        if not label or label == "Tessel Pass":
            continue
        p.circle(x, y, 7, "#4f46e5")
        p.circle(x, y, 3, "#ffffff")
        p.text(x + dx, y - 4, label, 11, 2, "#1e1b4b")
    p.text(412, 530, "Tessel Pass", 11, 2, "#1e1b4b")
    p.text(412, 517, "2,410 m", 9, 1, "#57534e")
    p.text(120, 196, "Aldmoor Lake", 9, 4, "#1d4ed8")
    p.circle(512, 660, 22, "#ffffff")
    p.poly([(506, 656), (512, 678), (518, 656)], "#dc2626")
    p.poly([(506, 656), (512, 640), (518, 656)], "#9ca3af")
    p.text(508, 686, "N", 10, 2, "#1f2937")
    p.line([(80, 170), (180, 170)], "#1f2937", 2)
    for i, x in enumerate((80, 130, 180)):
        p.line([(x, 166), (x, 174)], "#1f2937", 1.5)
        p.text(x - 3, 178, str(i), 8, 1, "#1f2937")
    p.text(186, 167, "km", 8, 1, "#1f2937")
    p.rect(54, 70, 504, 56, "#f7fee7")
    p.dashed([(72, 98), (108, 98)], "#dc2626", 2.5)
    p.text(116, 94, "Trail", 11, 1, "#374151")
    p.circle(186, 98, 7, "#4f46e5")
    p.circle(186, 98, 3, "#ffffff")
    p.text(200, 94, "Hut", 11, 1, "#374151")
    p.poly([(262, 92), (272, 108), (282, 92)], "#57534e")
    p.text(290, 94, "Pass", 11, 1, "#374151")
    p.line([(352, 98), (372, 104), (392, 96)], "#60a5fa", 3)
    p.text(400, 94, "River", 11, 1, "#374151")
    p.outline([(462, 92), (492, 92), (492, 106), (462, 106)], "#a8a29e", 0.8)
    p.text(500, 94, "100 m", 11, 1, "#374151")
    pages.append(p.stream())

    # 3. Charts: the elevation profile and the rainfall.
    p = Page()
    p.header("Elevation and weather", 4)
    p.text(54, 690, "Elevation profile", 16, 2, "#1e1b4b")
    base, x0, x1 = 470, 72, 540
    heights = [620, 700, 820, 960, 1010, 1180, 1320, 1290, 1480, 1650, 1720, 1900, 2150, 2410,
               2200, 1850, 1600, 1380, 1100, 900, 760]
    pts = [(x0 + (x1 - x0) * i / (len(heights) - 1), base + (h - 500) * 0.09) for i, h in enumerate(heights)]
    p.poly([(x0, base)] + pts + [(x1, base)], "#c7d2fe")
    p.line(pts, "#4f46e5", 2.5)
    p.line([(x0, base), (x1, base)], "#6b7280", 1)
    p.circle(pts[13][0], pts[13][1], 4, "#4f46e5")
    p.text(pts[13][0] - 40, pts[13][1] + 10, "Tessel Pass 2,410 m", 10, 2, "#312e81")
    for i, label in enumerate(("0 km", "10 km", "20 km", "30 km", "41.5 km")):
        p.text(x0 - 8 + (x1 - x0) * i / 4, base - 16, label, 9, 1, "#6b7280")
    p.text(54, 410, "Average rainfall (mm)", 16, 2, "#1e1b4b")
    rain = [62, 58, 71, 88, 112, 140, 151, 138, 104, 86, 79, 70]
    months = "JFMAMJJASOND"
    for i, r in enumerate(rain):
        x = 78 + i * 39
        p.rect(x, 190, 24, r * 1.2, "#10b981" if 5 <= i <= 7 else "#6ee7b7")
        p.text(x + 7, 174, months[i], 10, 1, "#6b7280")
        p.text(x + 2, 196 + r * 1.2, str(r), 8, 1, "#374151")
    p.line([(70, 190), (548, 190)], "#6b7280", 1)
    p.paragraph(54, 140, "June to August are the wettest months, but also the warmest: "
                "the huts are open from mid-June to the end of September.", 88)
    pages.append(p.stream())

    # 5. The huts.
    p = Page()
    p.header("Huts on the way", 5)
    huts = [("Larch Hut", "1,240 m", "38 beds", "Mid-June to September"),
            ("Meadow Hut", "1,780 m", "24 beds", "July to mid-September"),
            ("Tessel Bivouac", "2,390 m", "8 beds, no staff", "All year, emergencies"),
            ("Brannock Mill", "690 m", "52 beds", "All year")]
    for i, (name, alt, beds, season) in enumerate(huts):
        x, y = 54 + (i % 2) * 258, 450 - (i // 2) * 250
        p.rect(x, y, 246, 230, "#f5f7ff")
        p.poly([(x + 24, y + 150), (x + 64, y + 190), (x + 104, y + 150)], "#4f46e5")
        p.rect(x + 32, y + 110, 64, 40, "#c7d2fe")
        p.rect(x + 56, y + 110, 16, 24, "#4f46e5")
        p.text(x + 24, y + 80, name, 16, 2, "#1e1b4b")
        for j, line in enumerate((alt, beds, season)):
            p.text(x + 24, y + 56 - j * 18, line, 11, 1, "#4b5563")
    p.paragraph(54, 120, "Book the staffed huts ahead in July and August. The bivouac below the "
                "pass has blankets and a stove, but no food.", 88)
    pages.append(p.stream())

    # 6. Flowers.
    p = Page()
    p.header("Flowers of the high meadows", 6)
    flowers = [("Alpine aster", "#a78bfa", "#fbbf24", "Dry, sunny slopes; July"),
               ("Mountain avens", "#fef3c7", "#facc15", "Rocks and screes; June"),
               ("Trumpet gentian", "#3b82f6", "#1e3a8a", "Short turf; May to July"),
               ("Bird's-eye primrose", "#f472b6", "#fde047", "Wet meadows; June"),
               ("Globeflower", "#fde047", "#f59e0b", "Damp meadows; June"),
               ("Alpine rose", "#e11d48", "#fda4af", "Open woods; July")]
    for i, (name, petal, centre, note) in enumerate(flowers):
        x, y = 54 + (i % 3) * 172, 470 - (i // 3) * 250
        p.rect(x, y, 160, 230, "#f0fdf4")
        cx, cy = x + 80, y + 150
        p.line([(cx, cy - 20), (cx - 6, y + 70)], "#16a34a", 3)
        for k in range(6):
            a = k * math.pi / 3
            p.circle(cx + 20 * math.cos(a), cy + 20 * math.sin(a), 14, petal)
        p.circle(cx, cy, 11, centre)
        p.text(x + 14, y + 44, name, 13, 2, "#14532d")
        p.text(x + 14, y + 24, note, 10, 1, "#4b5563")
    p.paragraph(54, 120, "Please leave the flowers where they grow: many of them are protected, "
                "and all of them are prettier on the mountain.", 88)
    pages.append(p.stream())

    # 7. A checklist and a permit to sign.
    p = Page()
    p.header("Checklist and permit", 7)
    items = [("Map and compass", True), ("Rain jacket", True), ("Warm layer", True),
             ("Water, 2 litres", False), ("Sun hat and cream", True), ("First-aid kit", False),
             ("Head torch", False), ("Hut booking", True), ("Snacks", True), ("Cash for the huts", False)]
    for i, (name, done) in enumerate(items):
        x = 54 if i < 5 else 320
        y = 680 - (i % 5) * 34
        p.frame(x, y - 3, 14, 14, "#4f46e5", 1.5)
        if done:
            p.line([(x + 3, y + 4), (x + 6, y), (x + 12, y + 10)], "#10b981", 2)
        p.text(x + 26, y, name, 13, 1, "#1f2937")
    p.frame(54, 190, 504, 280, "#c7d2fe", 1.5)
    p.rect(54, 430, 504, 40, "#eef2ff")
    p.text(72, 444, "Hiking permit - Tessel Pass", 15, 2, "#1e1b4b")
    for label, y in (("Name", 380), ("Date", 330), ("Emergency contact", 280), ("Signature", 220)):
        p.text(72, y, label, 11, 1, "#6b7280")
        p.line([(190, y - 2), (530, y - 2)], "#9ca3af", 1)
    p.paragraph(54, 150, "Show this page at Meadow Hut before stage 3. The warden keeps a copy "
                "until you sign out in Brannock.", 88, 11, 4, "#6b7280")
    pages.append(p.stream())

    # 8. On the trail.
    p = Page()
    p.header("On the trail", 8)
    rules = [("Stay on the path", "The meadows recover slowly; shortcuts become gullies in a season."),
             ("Take your rubbish home", "There are no bins above Larch Hut, and nothing rots at 2,000 m."),
             ("Leave the flowers", "Take photographs instead: the next walker would like to see them too."),
             ("Dogs on a lead", "Near the huts and the grazing cattle, from June to September."),
             ("Say hello", "Mountain paths are narrow. Walkers going up have right of way.")]
    y = 660
    for i, (title, text) in enumerate(rules, 1):
        p.circle(76, y + 4, 16, "#10b981")
        p.text(72 if i < 10 else 68, y - 1, str(i), 14, 2, "#ffffff")
        p.text(104, y + 6, title, 15, 2, "#1e1b4b")
        p.paragraph(104, y - 14, text, 78, 12, 3, "#4b5563")
        y -= 86
    p.rect(54, 120, 504, 80, "#eef2ff")
    p.text(78, 168, "Have a good walk.", 20, 2, "#312e81")
    p.text(78, 142, "Juniper Trail field guide, spring 2026 edition", 11, 4, "#4b5563")
    pages.append(p.stream())

    write_pdf(path, pages, "Juniper Trail field guide")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    pdf(OUT / "PDF Toolbox Test A.pdf", "PDF Toolbox test A",
        ["The quick brown fox jumps over the lazy dog.", "Page one of the merge test."])
    pdf(OUT / "PDF Toolbox Test B.pdf", "PDF Toolbox test B",
        ["Pack my box with five dozen liquor jugs.", "Page two of the merge test."])
    docx(OUT / "PDF Toolbox Test Letter.docx",
         ["PDF Toolbox test letter", "This Word document was converted to PDF by LibreOffice,",
          "running as WebAssembly inside PDF Toolbox, offline."])
    demo(OUT / "PDF Toolbox Demo.pdf")
    print(OUT)
