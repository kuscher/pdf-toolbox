# Testing BentoBook

`python3 tools/testfiles.py` writes test files to test/ (two one-page PDFs
with real text and a Word document). With DevTools on
(`./bb debug devtools on`), `./bb incoming FILE…` hands files to the app as if
shared, `./bb debug open /TOOL` opens a tool, and `./bb cdp eval` can press
its button (`document.getElementById('process-btn').click()`).

`python3 tools/survey.py` drops a test PDF into each of the 79 PDF tool
pages and reports the compact header, the page height against the window's
and whether the tool's button is in view, plus every request that failed,
from the page or its workers. The app has no INTERNET permission, so a URL
off the app's origin in that list is a missing offline file. Run it after
updating BentoPDF.

## Checked on the Googlebook (2026-09-26, WebView 153, versions 0.1 to 0.3)

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
| No INTERNET permission | the site loads; in 0.3's survey no request from any of the 79 PDF tools or their workers failed (0.2's PDF Editor asked jsDelivr for fonts) |
| Sign (0.3) | the page's text renders (pdf.js standard fonts from the app); header, pdf.js toolbar, page and Save in one window |
| PDF Editor (0.3) | pages render (EmbedPDF's fallback font from the app, not jsDelivr); tabs, toolbar and Download in one window |
| Crop (0.3) | page centred with an 80% crop box after the resize; Crop & Download in view |
| Compact header (0.3, tools/survey.py, window 1228x892) | 76 of the 79 PDF tools fold into the header, BentoPDF's top bar and the drop zone hidden; 72 end exactly at the window's bottom; Edit Metadata (27 px), PDF to Text (48 px, keeps its file list), Booklet (2 px) and Posterize (a long form) scroll a little; Edit PDF Text, Bookmarks and Watermark are full pages and keep BentoPDF's layout |
| Details, remove file (0.3) | Details brings back the title and drop zone and Hide details folds them; removing the file restores the page (Crop, Merge, Compress) |

## For a person (not automatable here)

- [ ] Pick files in the file picker; several at once in Merge.
- [ ] Open a PDF with BentoBook from Files; share a Word file to it.
- [ ] Drag a PDF from Files onto a tool's drop area.
- [ ] Open and Show on the saved bar.
- [ ] Print from the Markdown to PDF editor.
- [ ] Back gesture/key goes back a page; the window resizes cleanly.
- [ ] A large scanned PDF (50+ pages) through OCR and Compress: time and
      memory.
