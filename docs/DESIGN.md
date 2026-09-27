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
│   └── bentobook/     About & licenses (tools/licenses.py)
├── assets/shell/page_shim.js   injected into every page at document start
└── classes.dex        MainActivity, Web (asset server), Downloads, Store
```

There is no native code: the engines are WebAssembly and the app is Java, so
one APK installs and runs on every Googlebook, x86_64 (Intel) or arm64
(Snapdragon, MediaTek). build.sh fails if a `lib/` directory or a `.so` ever
gets into the APK. The Arm side is tested on an HP Googlebook 14, the x86_64
side in CI (below).

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
isolate-and-credentialless`. **Verified on an HP Googlebook 14 (WebView
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

- A resizable desktop window, at least 600x480 dp. Googlebook OS picks the
  size it opens at: on the HP Googlebook 14 it is about 71% x 76% of the
  screen, and a `<layout>` default size of 1280x860 dp, 80% x 85% or 50% x 50%
  made no difference. The manifest asks for 80% x 85% for desktop modes that
  do use it, rather than a fixed size that can't fit a small screen. The
  caption bar is
  transparent over the root view's colour, which follows the page's top
  edge. The WebView is padded below the caption (caption, system bar and
  cutout insets), so a tool's controls never sit under the window buttons.
- **Live resizing.** In desktop windowing, SystemUI resizes a window under
  a veil (the app's icon on a plain colour) and lets the app lay out once,
  at the end of the drag. Checked in the HP Googlebook 14's SystemUI
  (`DesktopModeWindowDecorViewModel.createWindowDecoration`): a window
  gets the veiled positioner only when veiled resizing is on and compat
  change `ENABLE_FLUID_RESIZING` (460405642) is off for its package;
  otherwise `ResizeTaskPositioner` resizes it live. The change is disabled
  by default and `@Overridable`; Google turns it on for Chrome, Gmail, Docs
  and a few more through the `app_compat_overrides` device config. There is
  no manifest property for it. `./bb live-resize` sets the override for
  BentoBook over adb (`am compat enable`, allowed on a release build for an
  overridable change); it survives app updates. SystemUI chooses when it
  decorates a window, so it applies to windows opened afterwards, and its
  log names the positioner (`adb logcat | grep TaskPositioner`). During a
  live drag the page gets a stream of resize events; the shim refits at
  most every 50 ms, and the window background matches the page's, so an
  edge the WebView hasn't drawn yet doesn't flash.
- Back uses `OnBackInvokedCallback` (predictive back at targetSdk 37),
  registered only while the WebView can go back.
- If the renderer dies (a huge PDF), the app replaces the WebView and reloads
  the tool list instead of crashing.
- The file picker is `FileChooserParams.createIntent()`: at targetSdk 37 it
  opens DocumentsUI with the input's MIME filter, and `showSaveFilePicker`
  (the editor's "edit image externally") becomes CREATE_DOCUMENT.

## Licenses (tools/licenses.py)

Every part of the app is declared with its license, copyright holders and
source, and the texts ship in the APK:

- `licenses/components.json` lists everything that isn't an npm package in
  BentoPDF's scripts: BentoPDF itself, each engine (with the libraries compiled
  into it), fonts, data and the Android libraries. The texts it names are in
  `licenses/texts/`.
- The npm packages come from Vite's own report (`build.license`, which
  tools/webapp.sh turns on by putting a `vite.config.mjs` next to BentoPDF's
  config) plus the packages only BentoPDF's workers import, which that report
  leaves out. Packages that ship no license file get one from `licenses/npm/`.
- build.sh runs it: it writes the app's `/bentobook/about.html` and
  `licenses.html` with every text, and THIRD_PARTY_NOTICES.md and
  licenses/javascript-packages.txt in the repository. It stops the build when a
  file in the site that is an engine, data or a font belongs to no component,
  so an engine a BentoPDF update adds can't ship unlisted.
- The page shim puts **About & licenses** in BentoPDF's top bar on every page:
  Simple Mode hides BentoPDF's footer, and the AGPL wants the notices in reach.

BentoBook's own code is MIT. The app contains AGPL-3.0 parts (BentoPDF,
PyMuPDF/MuPDF, Ghostscript, CoherentPDF, the PDFium editor engine), so the APK
as a whole goes out under the AGPL-3.0 with its source: each release carries a
source archive (tools/release.sh) with this repository, BentoPDF at the pinned
commit and the engines' build scripts; THIRD_PARTY_NOTICES.md points to the
exact upstream source of everything else.

## Signing and releases

The release key is in `~/.config/bentobook` (`keystore.jks`, `keystore.pass`),
never in the repository; without it build.sh signs with a test key. 0.1 to 0.4
were signed with a key that was in the repository; it was taken out of the
history and retired, so 0.5 can't update those installs.

`tools/release.sh` (`./bb release [--publish]`) checks that build/BentoBook.apk
has the manifest's version and the release key's certificate, then writes
`BentoBook.apk` (the same name in every release, so
`releases/latest/download/BentoBook.apk` is a stable link), the source archive,
`SHA256SUMS` and the release notes (from CHANGELOG.md) to
`executables/release-<version>/`, and with `--publish` tags the commit and
makes the GitHub release.

## The icon (tools/icon.py)

A bento box of PDF tools in Material 3 Expressive style: a page, a "cookie"
shape and a pill in three compartments. `tools/icon.py` draws it once and
writes the adaptive icon's background, foreground and monochrome (themed icon)
layers as vector drawables, and `docs/icon.svg` for the README and the About
page; `--preview DIR` renders PNGs under the launcher masks.

## Testing on x86_64

`tools/smoke.py` runs the main engines end to end (Merge, Compress, PDF to
Word, PDF/A, OCR, Word to PDF) on whatever device adb reaches. The x86_64
workflow (.github/workflows/x86_64.yml) builds the APK on an x86_64 runner and
runs it in Google's `android-37.0;android-desktop;x86_64` emulator image.

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
