# App content declarations (Play Console › Policy › App content)

| Declaration | Answer |
|---|---|
| Privacy policy | https://googlebook.studio/privacy/pdf-toolbox |
| Ads | No, the app contains no ads |
| App access | All functionality is available without special access (no login) |
| Content rating | See `content-rating.md` |
| Target audience | 13 and over (13–15, 16–17, 18+). Not designed for children, so the Families policy doesn't apply |
| Data safety | See `data-safety.md` |
| News app | No |
| Government app | No |
| Financial features | My app doesn't provide any financial features |
| Health apps | No health features |
| Advertising ID | Not used (no ad or analytics SDKs; `AD_ID` isn't declared) |
| Permissions | **None.** The 0.7 (8) bundle's manifest has no `<uses-permission>` at all, no services (so no accessibility service and no foreground service), no receivers or providers, and no `<queries>`. Files come in through Android's file picker, Open with (PDF) and Share (PDF, images, text, office documents, EPUB, email): each hands over a content URI for that one file. Results go to Download through MediaStore, and printing uses Android's print dialog; neither needs a permission. |

## Declarations that need more than a tick

None. With no permissions and no services, the Console has nothing to ask about: no Accessibility API, foreground
service, photo and video, all-files access, package visibility or exact alarm declaration, and no declaration video.
If a later version adds a permission, check the bundle again with
`java -jar ~/.cache/android/bundletool-1.18.3.jar dump manifest --bundle=build/PDFToolbox.aab`.

## Things a reviewer or the pre-launch report may raise

- **Size.** `build/PDFToolbox.aab` is 188 MB; bundletool's `get-size total` puts the download at 186.4 MB on every
  device (the engines are assets, which Play doesn't split by device). Play's limit for the compressed download of
  the base module is 200 MB, so about 14 MB is left: more OCR languages or the CJK editor fonts would need
  Play Asset Delivery.
- **Code the app runs.** BentoPDF's tools are JavaScript and WebAssembly (LibreOffice, Ghostscript, Tesseract, Python
  with PyMuPDF) running in the app's WebView. All of it ships inside the APK and is served from the app's own asset
  origin; the app can't download anything, so the Device and Network Abuse rule against code from outside Google Play
  isn't touched. There is no native code (no `lib/`), which also makes the 16 KB page size requirement moot.
- **BentoPDF's name and license.** The app is BentoPDF (AGPL-3.0) with PDF Toolbox's own name and icon; About &
  licenses credits it, and PDFs it makes keep BentoPDF's producer line. The listing names BentoPDF once, as the
  open-source project it is, and says the app isn't made or endorsed by its authors. Each GitHub release carries the
  complete source, as the AGPL asks.
- **Tools that need the internet.** Timestamp PDF and certificate checks in Validate Signature can't work offline;
  screenshot 04 shows Timestamp PDF in the Secure PDF menu. The description's Limits paragraph says so.
- **Pre-launch devices.** minSdk is 34, so only Android 14 and later. On a phone-sized screen the sidebar folds into
  its icon row (below 960 px). Office to PDF needs a WebView with the cross-origin isolation allowlist (tested with
  WebView 153); on an older test device that one tool fails and the others still work.
