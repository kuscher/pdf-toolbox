# BentoBook

BentoPDF (static web app, engines in WASM) as an Android app for the HP
Googlebook 14: an offline build served from the APK into a WebView, with the
file picker, downloads, "Open with" and printing added. No Linux VM, no
INTERNET permission. Read docs/DESIGN.md; the user guide is README.md.

## Commands

```sh
./build.sh fetch | ./build.sh     # toolchain once; then web app (cached) + build/BentoBook.apk
tools/webapp.sh [--force]         # BentoPDF's air-gapped build, ~/.cache/bentobook/web-<v>
./bb app | install | start | stop | logs [N]
./bb debug dump | reload | open PATH | devtools on|off | crash
./bb incoming FILE...             # hand files to the app as if shared (they land in Download/)
./bb cdp targets | eval JS        # after ./bb debug devtools on
./bb shot FILE [full]             # screenshot; view it before sharing
./bb share                        # executables/BentoBook-<v>.apk to the Googlebook's Download
./bb live-resize [on|off|status]  # Android's per-app switch: live window resizing, no veil
python3 tools/testfiles.py        # test PDFs and a .docx in test/
python3 tools/survey.py [PAGE...]  # every PDF tool: compact layout, failed requests (devtools on)
```

adb comes from VSCodeBook's setup; its server runs on a Unix socket. Never
start it on TCP 5037.

## Rules

- **Keep it offline.** No INTERNET permission, no CDN URLs: every engine is
  served from the app's origin (tools/webapp.sh).
- **Don't inject Android input.** Pickers, installs and permission dialogs
  belong to the user. JS in the app's own WebView over CDP is fine for tests.
- **Clean up test files**: `./bb incoming` and tool runs write to Download/
  (owner local.bentobook); delete them when done.
- **Kill processes by PID**, not `pkill -f`.
- **Each release bumps** versionCode and versionName in AndroidManifest.xml and
  copies build/BentoBook.apk to `executables/BentoBook-<version>.apk` (not in
  git). Keep keystore.jks (password `bentobook`).
- **AGPL:** BentoPDF, PyMuPDF, Ghostscript and CoherentPDF are AGPL-3.0;
  shared builds must come with their source.
- **Ask before outward-facing steps** (new remotes, releases, sharing).

## Code style

Java 17, framework views, no Gradle; the only library is androidx.webkit.
Comments say why, not what.
