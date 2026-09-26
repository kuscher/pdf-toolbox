# BentoBook

[BentoPDF](https://github.com/alam00000/bentopdf), the private PDF toolkit,
as an Android app for the HP Googlebook 14: more than 100 PDF tools in a
desktop window, all running on the device. No server, no Linux VM, and the
app has no internet permission at all: your files can't leave the Googlebook.

## What it does

- **Organize:** merge, split, reorder, rotate, delete and extract pages;
  the PDF Multi Tool does all of it on one page grid.
- **Edit:** Edit PDF Text (click a paragraph and type), annotate, highlight,
  redact, sign, fill and create forms, watermarks, page numbers, bookmarks.
- **Convert:** Word, Excel, PowerPoint and OpenDocument to PDF (LibreOffice,
  offline), PDF to Word, Excel, text and images, images to PDF, PDF/A,
  EPUB, email and Markdown to PDF.
- **Clean up:** OCR (English), compress, remove blank pages, deskew,
  encrypt and decrypt, remove metadata.
- **Workflow Builder:** chain tools into your own pipeline.

## Install

Open `BentoBook-<version>.apk` from the Download folder in Files and allow
Files to install it if Android asks. BentoBook needs no permissions.

**Live window resizing** (optional, needs a computer with adb once):
Android normally hides a window behind a veil with its icon while you
resize it. With Wireless debugging paired, run
`adb shell am compat enable ENABLE_FLUID_RESIZING local.bentobook` (or
`./bb live-resize` from this repo) and reopen BentoBook: the page then
follows the window edge as you drag. `am compat reset` undoes it.

## Using it

- **Pick a tool, then a file:** click the drop area and choose files in
  Android's file picker.
- **From Files:** open a PDF with BentoBook, or share any supported file
  (PDF, images, Word, Excel, PowerPoint, OpenDocument, EPUB, email) to it.
  A bar says the file is waiting; open a tool and the file goes straight
  in.
- **Once your file is in,** the tool's page folds its title and drop
  area into a slim header: **← Tools**, the tool, your file, **Change
  file** (or **Add files**) and **Details**, which shows the folded part
  again. Editors (Sign, PDF Editor, Crop, Form Filler, Stamps and others)
  fill the window, with their own toolbar and buttons in view.
- **Results** are saved to your **Download** folder. A bar at the bottom
  shows the name, with **Open** (in your PDF viewer) and **Show** (in
  Files).
- **Back** (the back key or gesture) goes back to the previous page; the
  "Back to Tools" link does the same.

## Limits

- **OCR is English only.** Other languages need a rebuild
  (`OCR_LANGS=eng,deu tools/webapp.sh --force`, then `./build.sh`), a few MB
  each.
- **Nothing that needs the internet:** trusted timestamps and certificate
  checks for digital signatures don't work.
- **Office conversion** needs Android System WebView 152 or later (the
  Googlebook has it): it relies on a new WebView switch for
  SharedArrayBuffer. On older WebViews the other tools still work.
- **Very large files** can exhaust WebView's memory. The app then reloads
  the tool list and says so.
- **Long option forms** (Posterize, Edit Metadata) still scroll a little;
  the header stays at the top.
- **Size:** the APK is about 196 MB, mostly the engines: LibreOffice
  (78 MB), Python and PyMuPDF (41 MB), OCR (20 MB), Ghostscript (11 MB).

## Sharing it

The APK is signed with this repo's `keystore.jks` (password `bentobook`);
updates must be signed with the same key.

BentoPDF, PyMuPDF, Ghostscript and CoherentPDF are licensed under the
**AGPL-3.0**, so whoever you give the APK to is entitled to its complete
source: this repository, BentoPDF v2.8.8, and the engine packages named in
docs/DESIGN.md.

## Building

```sh
./build.sh fetch          # once: Android toolchain bits and Node with npm
./build.sh                # BentoPDF's web app (first time) and build/BentoBook.apk
./bb app                  # build, install on the Googlebook and launch
```

See [docs/DESIGN.md](docs/DESIGN.md) for how it works and
[docs/TESTING.md](docs/TESTING.md) for what was tested.

## Credits

BentoPDF © the BentoPDF authors (AGPL-3.0 or commercial). It bundles
LibreOffice (MPL-2.0), PyMuPDF and MuPDF (AGPL-3.0), Ghostscript
(AGPL-3.0), CoherentPDF (AGPL-3.0), Tesseract (Apache-2.0), pdf.js
(Apache-2.0), Pyodide (MPL-2.0) and more; see BentoPDF's licensing page.
