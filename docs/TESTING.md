# Testing PDF Toolbox

`./ptb smoke` (tools/smoke.py) runs the main engines end to end on the device:
it opens Merge, Compress, PDF to Word, PDF to PDF/A, OCR and Word to PDF in the
sidebar's frame, gives each the test files, presses its button, waits for the
result in Download/ and deletes it again. The same script runs in the x86_64 workflow, in Google's
x86_64 Android 16 emulator (`--slow`).

`python3 tools/testfiles.py` writes test files to test/ (two one-page PDFs
with real text and a Word document). With DevTools on
(`./ptb debug devtools on`), `./ptb incoming FILE…` hands files to the app as if
shared, `./ptb debug open /TOOL` opens a tool, and `./ptb cdp eval` can press
its button (`document.getElementById('process-btn').click()`).

`python3 tools/survey.py` drops a test PDF into each of the 79 PDF tool
pages, in the sidebar's frame, and reports the compact header, the page height against the window's
and whether the tool's button is in view, plus every request that failed,
from the page or its workers. The app has no INTERNET permission, so a URL
off the app's origin in that list is a missing offline file. Run it after
updating BentoPDF.

## Checked on the Acer Googlebook 14 (Intel, 2026-09-30)

On the Acer Googlebook 14 (Intel Core Ultra 5 325, x86_64, Android 17, WebView 155.0.8059.16), with the
0.6.1 release APK from GitHub, the same file the Arm Googlebooks get, and the tools in the
sidebar's frame (825x975 px in the 881x975 px window, so the sidebar was folded into the rail).

| Check | Result |
| --- | --- |
| Install (release APK, certificate SHA-256 98:70:15:C8:…:DB:C3:D0) | installs over nothing with `adb install`; the installed APK carries the same certificate; no INTERNET permission |
| `./ptb smoke` | all six pass, with the HP's output sizes to the byte: Merge (1,319 bytes), Compress (759), PDF to Word (36,848), PDF/A (11,289), OCR (9,526), Word to PDF (10,110), 6 to 13 s each |
| Merge PDF (pdf-lib, CoherentPDF; timed out in the x86_64 emulator's WebView 133) | passes, 7 s |
| OCR (Tesseract, English; timed out in the x86_64 emulator's WebView 133) | passes, 9 s |
| Word to PDF (LibreOffice with threads; skipped in the emulator: no cross-origin isolation in WebView 133) | `crossOriginIsolated` and SharedArrayBuffer true in the frame; passes, 13 s |
| Layout survey (tools/survey.py) | 79 PDF tools: 76 fold into the compact header (Add Watermark, Edit Bookmarks and Edit PDF Text keep BentoPDF's layout, as on the HP), 74 end exactly at the frame's bottom, none is wider than the frame, no request failed. PDF to Text, Posterize and Scanner Effect scroll a little (1,023 to 1,183 px); on Scanner Effect that puts the button just below the frame (at 974 of 975 px), which the HP's list didn't have |
| Excel to PDF, PowerPoint to PDF (LibreOffice) | work, with Word to PDF: tables and charts come through |
| File picker, several files at once in Merge | works: both listed, one 2-page PDF saved, the saved bar shows |
| Open with PDF Toolbox from Files; share a Word file to it | works when PDF Toolbox isn't running: the bar shows on the tool list and the next tool takes the file. **Not when it's already open**: `onNewIntent` offers the file to the tool in the frame at once, so a PDF lands in whatever PDF tool is showing (reproduced: Merge open, Open with, the file goes into Merge's list with no bar), and switching to the tool you wanted finds nothing (`incoming=0`). Fixed on the `open-with-while-open` branch |
| Drag a PDF from Files onto a tool's drop area | works (Compress) |
| Open and Show on the saved bar | both work |
| Print from the Markdown to PDF editor | the dialog shows only the formatted document (the editor's button is **Export PDF**). **The sidebar doesn't come back when the dialog closes**: on the Acer the dialog hides the page and shows it again without a `focus` event, so the copy stays up until the next click (logged: `visibilitychange` hidden, then visible, no `focus`; `pointerdown` restores). Fixed on the `print-restore-sidebar` branch |
| Back, window resize, the rail below 960 px | work |
| Ctrl+K and Ctrl+B on the keyboard, with the focus in a tool too | work |
| Live resize (`./ptb live-resize on`), also on Sign and Crop | works: in a new window the page follows the drag with no veil, and the drag uses `ResizeTaskPositioner` (with it off: `MultiDisplayVeiledResizeTaskPositioner`) |
| OCR, a 60-page scanned PDF (200 dpi, 11.2 MB, no text layer) | 535 s through smoke.py's driver (about 9 s a page); peak PSS 136 MB for the app and 1,099 MB for its WebView renderer; MemAvailable never below 4,202 MB; 12,689,840 bytes out |
| Compress, the same 60-page PDF | 23 s; 5,039,836 bytes (from 11,215,035) |

## Checked for 0.6 (2026-09-27)

On the HP Googlebook 14 (Arm, Android 17, WebView 153.0.8010.39), with the
tools in the sidebar's frame (1100x788 px in the 1359x876 px window).

| Check | Result |
| --- | --- |
| `./ptb smoke` | all six pass: Merge (1,319 bytes), Compress (759), PDF to Word (36,848), PDF/A (11,289), OCR (9,526), Word to PDF (10,110), 7 to 12 s each; `crossOriginIsolated` and SharedArrayBuffer true in the frame |
| Layout survey (tools/survey.py) | 79 PDF tools: 76 fold into the compact header, 70 end exactly at the frame's bottom, none is wider than the frame, no request failed. Add Page Labels, Bates Numbering, Edit Metadata, Booklet, PDF to CBZ, PDF to Text and Posterize are long forms that scroll (836 to 1,188 px); Add Watermark and Edit Bookmarks are full pages that scroll |
| Full-height tools | the PDF Multi Tool fills the frame with two PDFs (toolbar at the top, its own header hidden); the Workflow Builder, Edit PDF Text, the PDF Editor, Sign and Crop fit it with their buttons in view |
| Sidebar | 7 categories and 118 tools from BentoPDF's tools.ts; Recent keeps the last five; the marked tool, the window title and the URL's hash follow the frame |
| Search | "sign" finds Sign PDF, Digital Signature and Validate Signature, "word" Word to PDF and PDF to Word only, "workflow" the Workflow Builder (listed only under Popular); Enter opens the first match and moves the focus into the tool |
| Rail, narrow window | Ctrl+B and the button fold the sidebar into the icon rail, with flyouts and names on hover; in an 820 px viewport (CDP emulation) the rail shows and the button opens the sidebar over the tool |
| Keys in a tool | Ctrl+K and Ctrl+B pressed with the focus in the tool's page reach the sidebar (CDP key events) |
| Back | back from Compress returns to Merge, then to the tool list, and the sidebar follows |
| About & licenses | open in the frame without their own way back; the sidebar keeps About marked on Licenses |
| Links out of the app | a link in the frame to another app is handed to Android, and the frame stays |
| Open with / Share | `./ptb incoming` shows the file's bar on the tool list; Merge PDF took the file when opened from the sidebar |
| Print (Markdown to PDF) | the tool's Print puts a copy of its page in the sidebar page and asks the app to print "Markdown to PDF – PDF Toolbox"; with print media, only the formatted document shows; the sidebar comes back afterwards. (The test caught the app message, so no print dialog opened) |
| Rename | installs as `local.pdftoolbox`, signed with the same key as BentoBook 0.5; BentoBook was uninstalled afterwards |
| x86_64 (GitHub Actions run 36350541540: Android 16 `android-36;default;x86_64` emulator, WebView 133.0.6943.137) | builds and installs; the sidebar page comes up and drives the tools in its frame; Compress (759 bytes) and PDF to Word (36,848 bytes) match the Googlebook's output, PDF/A gives 11,274 bytes. The emulator's own System UI was slow under software rendering (its "isn't responding" dialog was up at the end); the app kept working |

## Checked for 0.5 (2026-09-27)

| Check | Result |
| --- | --- |
| `./ptb smoke` on an HP Googlebook 14 (Arm, Android 17, WebView 153.0.8010.39) | all six pass: Merge (merged.pdf), Compress, PDF to Word (.docx), PDF/A, OCR (searchable PDF), Word to PDF (LibreOffice), 7 to 12 s each |
| Files dropped from the APK (the web root's CoherentPDF copy, cpdf's Node builds, Tesseract's non-single-file builds, unused badges) | Merge (CoherentPDF) and OCR (Tesseract) still pass; the APK is 188 MB (0.4: 196 MB) |
| No native code | no `lib/` or `.so` in the APK; `aapt2 dump badging` shows no native-code line, so every ABI installs it |
| Release key | APK Signature Scheme v3, certificate SHA-256 98:70:15:C8:…:DB:C3:D0; 0.4 (old key) had to be uninstalled first, as expected |
| About & licenses | the link sits at the right of BentoPDF's top bar; About shows the licenses, source, engines, required notices; Licenses lists 266 components with their texts; the filter works |
| Icon | the adaptive icon shows in the taskbar and the window's caption |
| Window size | Googlebook OS picks the launch size itself: 1359x876 px on the 1920x1200 screen, the same with a `<layout>` default of 80% x 85% or 50% x 50% |
| x86_64 build (GitHub Actions, ubuntu-24.04 x86_64) | `./build.sh fetch && ./build.sh` builds the APK in under 4 minutes, with Ubuntu's aapt, zipalign and apksigner |
| x86_64 device (Android 16 `android-36;default;x86_64` emulator, WebView 133.0.6943.137, run 36304733878) | installs and starts; the page shim runs; Compress (PyMuPDF) gives the same 759 bytes as on the Googlebook, PDF to Word (PyMuPDF, pdf2docx, Ghostscript) the same 36,848 bytes, PDF/A (Ghostscript) 11,294 bytes. Merge and OCR time out there: their pages' PDF.js previews never come up in WebView 133. Word to PDF is skipped: WebView 133 has no cross-origin isolation allowlist |
| x86_64 emulator, Android 17 images (standard and desktop) | not usable in CI: under the emulator's software rendering SurfaceFlinger aborts on every screen read-back (`!rcEnc->featureInfo()->hasReadColorBufferDma`), restarting Android before an install finishes |

## Checked on an HP Googlebook 14 (Arm; 2026-09-26, WebView 153, versions 0.1 to 0.3)

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
| Live resize (0.4) | `am compat enable ENABLE_FLUID_RESIZING` accepted on the release build and kept across an app update; SystemUI's log shows which positioner a drag used |
| Details, remove file (0.3) | Details brings back the title and drop zone and Hide details folds them; removing the file restores the page (Crop, Merge, Compress) |

## For a person (not automatable here)

- [ ] Pick files in the file picker; several at once in Merge.
- [ ] Open a PDF with PDF Toolbox from Files; share a Word file to it. Both
      again with PDF Toolbox already open on a PDF tool: the bar shows with
      **Use here**, the open tool keeps its files, and the next tool takes it.
- [ ] Drag a PDF from Files onto a tool's drop area.
- [ ] Open and Show on the saved bar.
- [ ] Export PDF in the Markdown to PDF editor (it prints): the print dialog
      shows only the formatted document, and the sidebar comes back when it
      closes, after Print and after Cancel, with no click.
- [ ] Back gesture/key goes back to the previous tool; the window resizes
      cleanly, and below 960 px the sidebar folds into the rail.
- [ ] Ctrl+K and Ctrl+B on the keyboard, with the focus in a tool too.
- [ ] With `./ptb live-resize` on: drag a window edge; the page follows
      live, no veil (`adb logcat | grep TaskPositioner` names
      `ResizeTaskPositioner`, not `MultiDisplayVeiledResizeTaskPositioner`).
      Try it on Sign and Crop too.
- [ ] A large scanned PDF (50+ pages) through OCR and Compress: time and
      memory.
