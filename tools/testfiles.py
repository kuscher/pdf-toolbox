#!/usr/bin/env python3
"""Writes small test files to test/: two one-page PDFs with real text (for
merge, OCR and so on) and a Word document (for LibreOffice's Word to PDF).

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


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    pdf(OUT / "BentoBook Test A.pdf", "BentoBook test A",
        ["The quick brown fox jumps over the lazy dog.", "Page one of the merge test."])
    pdf(OUT / "BentoBook Test B.pdf", "BentoBook test B",
        ["Pack my box with five dozen liquor jugs.", "Page two of the merge test."])
    docx(OUT / "BentoBook Test Letter.docx",
         ["BentoBook test letter", "This Word document was converted to PDF by LibreOffice,",
          "running as WebAssembly inside BentoBook, offline."])
    print(OUT)
