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
checks for the gzip magic bytes and unpacks them itself. Two special cases:

- `/sw.js` is a 404 and the shim makes `serviceWorker.register` reject:
  everything is local already, and WebView would not route a service
  worker's fetches to the app.
- `/wasm/gs/assets/*` is served from `/wasm/gs/*`. BentoPDF's own loaders
  want `gs.js` at the top of the Ghostscript folder; PyMuPDF's PDF-to-Word
  path imports the npm package's `dist/index.js`, which loads `assets/gs.js`.
  The alias saves shipping `gs.wasm` (15.5 MB) twice.

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
- **Tool workspaces.** 106 of the 110 tool pages stack a header, a 256 px
  drop zone and the file card above the tool's workspace (Sign's editor, the
  PDF Editor's viewer at 75vh, Crop, Form Filler), which leaves the workspace
  below the fold in a laptop window; the tool looks as if it still wants a
  file. That is BentoPDF's layout, not a WebView problem. Once
  `#file-display-area` has a file and an element at least half the window
  tall appears below the drop zone, the shim hides the drop zone
  (single-file inputs only; multi-file tools keep it for adding more) and
  scrolls that element to the top. Emptying the file card brings the drop
  zone back. It uses a timeout, not requestAnimationFrame, which doesn't
  run while the window is hidden.
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
   PDF to Word (PyMuPDF with Ghostscript).
