# BentoBook design

BentoPDF is a static web app: every tool runs in the browser, with its
engines compiled to WebAssembly. BentoBook serves an offline build of it
from the APK into a WebView and adds what a browser tab would get from
Chrome: the file picker, downloads, "Open with", printing and a proper
window. Nothing runs in the Linux VM, and the app has no INTERNET
permission.

```
BentoBook.apk
├── assets/web/        BentoPDF v2.8.8, simple mode, air-gapped build
│   ├── wasm/          PyMuPDF (Pyodide), Ghostscript, CoherentPDF, Tesseract + English data
│   └── libreoffice-wasm/   LibreOffice 24.8 (Emscripten, threads)
├── assets/shell/page_shim.js   injected into every page at document start
└── classes.dex        MainActivity, Web (asset server), Downloads, Store
```

## Building it

- **tools/webapp.sh** follows BentoPDF's own air-gap recipe
  (docs/self-hosting, "Air-Gapped / Offline Deployment"). It checks out
  v2.8.8, runs `scripts/prepare-airgap.sh --skip-docker` to fetch the
  engine packages at the versions that release expects, and builds with
  `SIMPLE_MODE=true` and every `VITE_WASM_*`/`VITE_TESSERACT_*` URL pointing
  at the app's origin (the URLs are baked in; workers load them with
  `importScripts`, so they must be same-origin). The engines are laid out the
  way the bundle's `setup.sh` does it. The result is cached in
  `~/.cache/bentobook/web-<version>`.

  | Package | Version | Where |
  | --- | --- | --- |
  | @bentopdf/pymupdf-wasm | 0.11.16 | wasm/pymupdf |
  | @bentopdf/gs-wasm (Ghostscript 10.06) | 0.1.1 | wasm/gs (assets/ at the top, plus dist/index.js) |
  | coherentpdf | 2.5.5 | wasm/cpdf (dist/ at the top) |
  | tesseract.js / tesseract.js-core | 7.0.0 | wasm/ocr |
  | eng.traineddata (4.0.0_best_int), Noto Sans | | wasm/ocr/lang-data, fonts |
  | LibreOffice WASM (@matbee/libreoffice-converter) | in BentoPDF's public/ | libreoffice-wasm |
  | @embedpdf/fonts-latin, -arabic, -hebrew (Noto Sans/Naskh, Regular) | 1.0.0 | wasm/embedpdf |

  The air-gap script misses one download: the PDF Editor's (EmbedPDF's)
  fallback fonts, for text in fonts a PDF doesn't embed. BentoPDF fetches
  them from jsDelivr unless `VITE_EMBEDPDF_FONTS_URL` is set; offline, the
  editor's pages stayed blank. webapp.sh sets it and unpacks the files
  BentoPDF's `src/js/config/editor-fonts.ts` names: latin (also Greek,
  Cyrillic, Vietnamese), arabic and hebrew by default, 0.8 MB;
  `EDITOR_FONTS=latin,arabic,hebrew,jp,kr,sc,tc` adds CJK at several MB each.

- **build.sh** is Gradle-free like DrawBook's: aapt2, javac, D8,
  zipalign, apksigner. It drops the `.br` copies meant for nginx and prepends
  shell/nested-workers.js to LibreOffice's converter worker (below). The
  only library is androidx.webkit **1.18.0-alpha02**, for the
  cross-origin isolation allowlist.

## Serving the site (Web.serve)

A WebViewClient answers every request for `https://appassets.androidplatform.net/`
from `assets/web`, the way BentoPDF's nginx and serve.json would: clean
URLs (`/merge-pdf` → `merge-pdf.html`), directory indexes, correct MIME
types (`application/wasm` matters for streaming compilation). LibreOffice's
`soffice.wasm.gz` and `soffice.data.gz` are served as they are; the loader
checks for the gzip magic bytes and unpacks them itself. Three special cases:

- `/sw.js` is a 404 and the shim makes `serviceWorker.register` reject:
  everything is local already, and WebView would not route a service
  worker's fetches to the app.
- `/wasm/gs/assets/*` is served from `/wasm/gs/*`. BentoPDF's own loaders
  want `gs.js` at the top of the Ghostscript folder; PyMuPDF's PDF-to-Word
  path imports the npm package's `dist/index.js`, which loads `assets/gs.js`.
  The alias saves shipping `gs.wasm` (15.5 MB) twice.
- `/web/standard_fonts/*`, `/web/cmaps/*` and `/web/iccs/*` are served from
  `/pdfjs-viewer/`. Sign's viewer (`pdfjs-viewer/sign-viewer.html`) looks
  for pdf.js's data at `../web/`, where the pdf.js distribution keeps it.
  In Chrome the 404s go unnoticed because pdf.js falls back to system
  fonts; WebView has none to give it, so text in PDFs that don't embed
  their fonts (Helvetica, Times) was invisible.

Without INTERNET permission, WebView blocks network loads, but intercepted
requests are not network loads, so the app works; links out of the app
(GitHub, docs) go to the browser.

## SharedArrayBuffer in WebView

LibreOffice's WASM is an Emscripten build with threads, so it needs
SharedArrayBuffer, which needs a cross-origin-isolated page. WebView never
gives that by default: it runs every page in one renderer process, and the
COOP/COEP headers bentopdf.com sends are applied but grant nothing.

androidx.webkit 1.18.0-alpha01 (2026-09) added
`Profile#setCrossOriginIsolatedAllowlist`. MainActivity puts the app's own
origin on it (`Web.isolate()`, feature `CROSS_ORIGIN_ISOLATED_ALLOWLIST`),
and every response carries `Document-Isolation-Policy:
isolate-and-credentialless`. **Verified on the Googlebook (WebView
153.0.8010.36):** `crossOriginIsolated` is true in the page, in workers and in
nested workers, and SharedArrayBuffer and shared `WebAssembly.Memory` can
be posted to them. The page shim logs it on every load ("page ready:
crossOriginIsolated=true SharedArrayBuffer=true").

## Nested workers (shell/nested-workers.js)

With isolation working, LibreOffice still hung at 55% ("still waiting on run
dependencies: loading-workers"). Its converter runs in a worker, and
Emscripten starts four thread workers from inside it with
`new Worker('soffice.js', {name: 'em-pthread-N'})`. DevTools showed those
four script requests never getting a response or an error: **WebView does not
route the script request of a worker started by another worker to
`shouldInterceptRequest`**, so it waits forever. The converter's own
`importScripts` of the same file is answered, and a nested worker started
from a Blob works.

So build.sh prepends a small prelude to the converter worker's script. It
replaces `self.Worker` inside that worker: same-origin script URLs are
fetched with a synchronous XMLHttpRequest (which does reach the app) and the
worker starts from a Blob of the script, with the same options. After that,
Word to PDF works: LibreOffice loads, and `lok_documentSaveAs` writes the PDF.
Other tools start their workers from the page, which works as is.

## The page shim (shell/page_shim.js)

Injected at document start into every page of the app's origin, with a
`bentobook` message channel (`addWebMessageListener`):

- **Downloads.** BentoPDF saves with `<a download href="blob:…">` and
  revokes the URL at once, which native code can't fetch. The shim keeps
  each Blob as it is created (`URL.createObjectURL`), intercepts the click and
  streams the bytes to the app in 4 MB ArrayBuffer messages between a
  header and an end marker. MainActivity queues all three, in arrival
  order, on one IO thread, which writes a pending MediaStore Downloads item
  and publishes it at the end; then a bar offers Open and Show.
- **Incoming files.** VIEW (PDF) and SEND/SEND_MULTIPLE intents leave
  content URIs with MainActivity. Every tool is its own page, so each page
  sends `ready` when it loads and the app streams it the waiting files; the
  shim holds them as `File`s, shows a bar, and fills the first enabled file
  input whose `accept` matches (DataTransfer, then `input`/`change`
  events). The page answers `incoming.used` and the app forgets them.
- **Compact tool layout.** 106 of the 110 tool pages stack BentoPDF's
  sticky top bar (65 px), a title block and a 256 px drop zone above the
  file card and the tool, capped at 672 px wide, with viewers sized 75 to
  85vh. In a laptop window the tool starts below the fold, and scrolled to,
  its toolbar hides under the sticky top bar (Sign's did). That is
  BentoPDF's layout, not a WebView problem. Once a file is in, the shim
  hides everything laid out before the tool, level by level up to
  `<body>` (the top bar too), and the footer after it, and puts one 48 px
  header in their place: ← Tools, the tool's name, the file, Change file
  (Add files on multi-file tools, which keep their file list: Merge
  reorders there) and Details, which brings the title and drop zone back.
  - *Viewer tools* (a workspace at least half the window tall with a box
    of fixed height, a scroller or a big canvas: Sign, PDF Editor, Crop,
    Form Filler, Stamps, Adjust Colors…) go full width, and their viewer
    box is sized so the tool, including whatever follows it (Sign's Save
    button), ends at the window's bottom edge; again on every window
    resize. Then the page gets a `resize` event, since viewers lay out on
    that, not on their box changing. Cropper.js answers a resize by
    scaling its picture by one ratio, which left it off centre and taller
    than its box, so the shim lays Crop out afresh (`render()` on the
    instance the image carries) and puts the crop back; the crop is read
    in the shim's own resize listener, which runs before Cropper's.
  - *Form tools* (Compress, OCR, Split…) start at their options; a
    single-file tool folds its file card too, as the header names the file.
  - *Full-page tools* (Edit PDF Text, Bookmarks, Watermark: their
    workspace starts in the top 150 px) are left alone.
  - A MutationObserver (debounced with a timeout: requestAnimationFrame
    stalls while the window is hidden) re-checks the page. Removing the
    file, or the tool dropping its workspace, restores it; a viewer that
    appears after the file card switches to viewer mode.
- **`window.print()`** (Markdown editor) goes to Android printing via
  `WebView.createPrintDocumentAdapter`.
- **Standalone display mode** for `matchMedia('(display-mode: …)')`.
- **Caption colour:** the colour at the top edge of the page, reported
  every 1.5 s when it changes.

## The window

- A resizable desktop window, 1280x860 dp by default. The caption bar is
  transparent over the root view's colour, which follows the page's top
  edge. The WebView is padded below the caption (caption, system bar and
  cutout insets), so a tool's controls never sit under the window buttons.
- Back uses `OnBackInvokedCallback` (predictive back at targetSdk 37),
  registered only while the WebView can go back.
- If the renderer dies (a huge PDF), the app replaces the WebView and reloads
  the tool list instead of crashing.
- The file picker is `FileChooserParams.createIntent()`: at targetSdk 37 it
  opens DocumentsUI with the input's MIME filter, and `showSaveFilePicker`
  (the editor's "edit image externally") becomes CREATE_DOCUMENT.

## Debugging

`./bb debug devtools on` turns on WebView debugging (off by default),
after which `./bb cdp eval JS` runs JavaScript in the page. The debug
receiver needs `android.permission.DUMP`, so only the shell can use it:
`dump`, `reload`, `open PATH`, `devtools on|off`, `crash`, and `incoming`
(`./bb incoming FILE…`), which saves files to Download and offers them as if
shared: the shell can't grant the app another user's files.

## Updating BentoPDF

1. Set `VERSION` and `COMMIT` in tools/webapp.sh to a newer release tag.
2. `tools/webapp.sh --force`, `./build.sh`, then check `tools/webapp.sh`'s
   layout against the new `scripts/prepare-airgap.sh` and the generated
   `setup.sh` (the engine versions come from BentoPDF's
   `src/js/const/cdn-version.ts` and package-lock.json).
3. Run the checks in docs/TESTING.md, above all Word to PDF (threads) and
   PDF to Word (PyMuPDF with Ghostscript), and `tools/survey.py`: a new
   CDN URL shows up there as a failed request, a changed page layout as a
   missing header or an overflow.
