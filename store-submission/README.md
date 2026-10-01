# Google Play submission kit

Everything the Play Console asks for when publishing PDF Toolbox, ready to copy or upload (made on 30 September 2026,
following StudioSnap's and HearOn Link's kits). The app is in the Play Console: io.github.kuscher.pdftoolbox,
app id 4972784690780747764, developer account Fika Labs (7424304467248438473). Play App Signing uses the release key (01:ED:3C:81…, uploaded with PEPK); 0.7 (8) went to closed testing (Google Group googlebook-studio-testers@googlegroups.com, 178 countries) and was sent for review on 30 September 2026.

## What's here

| Play Console field | File | Limit / spec |
|---|---|---|
| App name | [listing/en-US/title.txt](listing/en-US/title.txt) | 30 characters |
| Short description | [listing/en-US/short-description.txt](listing/en-US/short-description.txt) | 80 characters |
| Full description | [listing/en-US/full-description.txt](listing/en-US/full-description.txt) | 4,000 characters |
| Release notes ("What's new") | [listing/en-US/release-notes.txt](listing/en-US/release-notes.txt) | 500 characters |
| App icon | [graphics/icon-512.png](graphics/icon-512.png) | 512 × 512 PNG, full square (Play rounds the corners), drawn from the launcher icon's layers (`res/`, written by `tools/icon.py`) |
| Feature graphic | [graphics/feature-graphic.png](graphics/feature-graphic.png) | 1024 × 500, 24-bit PNG |
| Screenshots | [graphics/large-screen/](graphics/large-screen) (4) | 1920 × 1080 (16:9), 24-bit PNG. Used for phone, 7-inch, 10-inch and Chromebook |
| Store settings, contact, category | [forms/store-settings.md](forms/store-settings.md) | |
| Privacy policy | https://googlebook.studio/privacy/pdf-toolbox | public, outside googlebook.studio's invite gate |
| Data safety | [forms/data-safety.md](forms/data-safety.md) | "No data collected" |
| Content rating (IARC) | [forms/content-rating.md](forms/content-rating.md) | expected: Everyone / PEGI 3 |
| Other App content declarations | [forms/app-content.md](forms/app-content.md) | no permissions, so no declarations; what reviewers may raise |

The listing text avoids what Play's metadata policy rules out: rankings or superlatives, promotional words, testimonials,
emoji, calls to action and other companies' app names. Office formats are named by their extensions (.docx, .xlsx,
.pptx), and BentoPDF is named once, as the open-source project the app is. The screenshots are PDF Toolbox's own
README images (`docs/images/`) with a caption, made with `scripts/play/graphics.mjs` in kuscher/googlebook-tech; the
feature graphic's indigo is the icon's box colour, #4F46E5.

## Steps

1. **App signing (decide once, it can't be undone).** Recommended, as for the other apps: *Use existing app signing
   key*, uploaded with Google's PEPK tool from `~/.config/pdf-toolbox/keystore.jks` (alias `pdftoolbox`, SHA-256
   `01:ED:3C:81:45:A8:CB:8B:F8:99:59:79:4F:53:BD:74:01:E5:07:CF:6D:80:C0:C3:D2:D9:B6:EB:EF:AF:62:3E`), so the Play
   build and the APKs on GitHub have the same signature and people can move between them without uninstalling. The
   same key is the upload key.
2. **Build the bundle** (Play only takes .aab files): `./build.sh && tools/aab.sh` → `build/PDFToolbox.aab`, signed
   with that key. The 0.7 bundle is built (188 MB, its certificate checked against the fingerprint above). Each
   upload needs a higher version code than the last (`android:versionCode` in `AndroidManifest.xml`: 9 for 0.7.1).
   From the next version on, pushing the version's tag builds, signs and uploads the bundle
   ([docs/RELEASING.md](../docs/RELEASING.md)); nobody needs the key file for it.
3. **Closed test first** (personal developer account: 12 testers opted in for 14 days before production), with the
   Google Group googlebook-studio-testers@googlegroups.com.
4. **Store listing, store settings and App content:** fill them in from these files. The listing, graphics and contact
   details can also go up in one edit with `node scripts/play/listing.mjs io.github.kuscher.pdftoolbox
   ~/pdf-toolbox/store-submission https://github.com/kuscher/pdf-toolbox` in kuscher/googlebook-tech (without
   `--commit` it only validates).
5. **Release:** add the bundle to the closed testing track, paste `release-notes.txt`, send for review. There are no
   declarations or videos to file. A pushed tag does the first two: the bundle arrives on the closed testing track as
   a draft with `release-notes.txt` as its "What's new". Sending it for review stays a button in the Play Console.
6. **Once it's on Play:** the repo's README still says PDF Toolbox isn't in the Play Store (Install, and "Why isn't
   it in the Play Store?" under Questions); add the Play link there and on its googlebook.studio listing.
