# Testing BentoBook

`python3 tools/testfiles.py` writes test files to test/ (two one-page PDFs
with real text and a Word document). With DevTools on
(`./bb debug devtools on`), `./bb incoming FILE…` hands files to the app as if
shared, `./bb debug open /TOOL` opens a tool, and `./bb cdp eval` can press
its button (`document.getElementById('process-btn').click()`).

## Checked on the Googlebook (2026-09-26, WebView 153, version 0.1)

| Check | Result |
| --- | --- |
| Cross-origin isolation | `crossOriginIsolated` and SharedArrayBuffer true in the page, workers and nested workers |
| Merge PDF (pdf-lib, CoherentPDF) | merged.pdf with both pages |
| Word to PDF (LibreOffice with four thread workers) | one-page PDF 1.7 from "LibreOfficeDev 24.8.8", text intact |
| PDF to Word (PyMuPDF, Ghostscript RGB pass) | .docx saved, no errors |
| PDF to PDF/A (Ghostscript 10.06) | saved |
| Compress PDF | saved |
| OCR (Tesseract, English) | text recognised exactly; searchable PDF saved |
| Edit PDF Text (pdfium engine) | the shared PDF opens with editable text boxes |
| Shared file → next tool | Merge, Word to PDF, OCR and the editor took it; the bar shows on the tool list |
| Saved bar | "Saved … to Download" with Open and Show |
| File picker | DocumentsUI opens with the input's filter (application/pdf) |
| No INTERNET permission | the site loads; nothing needs the network |

## For a person (not automatable here)

- [ ] Pick files in the file picker; several at once in Merge.
- [ ] Open a PDF with BentoBook from Files; share a Word file to it.
- [ ] Drag a PDF from Files onto a tool's drop area.
- [ ] Open and Show on the saved bar.
- [ ] Print from the Markdown to PDF editor.
- [ ] Back gesture/key goes back a page; the window resizes cleanly.
- [ ] A large scanned PDF (50+ pages) through OCR and Compress: time and
      memory.
