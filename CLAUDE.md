# BentoBook

BentoPDF (static web app, engines in WASM) as an Android app for Googlebooks,
Intel (x86_64) and Arm alike: an offline build served from the APK into a
WebView, with the file picker, downloads, "Open with" and printing added. No
native code, no Linux VM, no INTERNET permission. Read docs/DESIGN.md; the user
guide is README.md. Development happens on an HP Googlebook 14 (Arm) over adb.

## Commands

```sh
./build.sh fetch | ./build.sh     # toolchain once; then web app (cached) + build/BentoBook.apk
tools/webapp.sh [--force]         # BentoPDF's air-gapped build, ~/.cache/bentobook/web-<v>
./bb app | install | start | stop | logs [N]
./bb debug dump | reload | open PATH | devtools on|off | crash
./bb incoming FILE...             # hand files to the app as if shared (they land in Download/)
./bb cdp targets | eval JS        # after ./bb debug devtools on
./bb shot FILE [full]             # screenshot; view it before sharing
./bb smoke [CHECK...]             # the engines end to end on the device (tools/smoke.py)
./bb share                        # executables/BentoBook-<v>.apk to the Googlebook's Download
./bb live-resize [on|off|status]  # Android's per-app switch: live window resizing, no veil
./bb release [--publish]          # release files; --publish tags and makes the GitHub release
python3 tools/licenses.py         # notices (build.sh runs it; fails on unlisted engines)
python3 tools/icon.py [--preview DIR]  # the icon's vector layers and docs/icon.svg
python3 tools/testfiles.py        # test PDFs and a .docx in test/
python3 tools/survey.py [PAGE...]  # every PDF tool: compact layout, failed requests (devtools on)
```

adb comes from VSCodeBook's setup; its server runs on a Unix socket. Never
start it on TCP 5037.

## Rules

- **Keep it offline.** No INTERNET permission, no CDN URLs: every engine is
  served from the app's origin (tools/webapp.sh).
- **No native code.** One APK serves x86_64 and Arm Googlebooks; build.sh
  refuses an APK with `lib/` or `.so` files.
- **Don't inject Android input.** Pickers, installs and permission dialogs
  belong to the user. JS in the app's own WebView over CDP is fine for tests.
- **Clean up test files**: `./bb incoming` and tool runs write to Download/
  (owner local.bentobook); delete them when done (smoke.py does).
- **Kill processes by PID**, not `pkill -f`.
- **The release key never goes in git.** It is `~/.config/bentobook/keystore.jks`
  with its password in `keystore.pass`; the maintainer has a backup. .gitignore
  blocks `*.jks` and `*.pass`.
- **Each release** bumps versionCode and versionName in AndroidManifest.xml,
  adds a CHANGELOG.md section, builds, runs `./bb smoke`, commits, then
  `./bb release --publish`.
- **Licenses:** BentoBook's code is MIT; the APK is AGPL-3.0 as a whole
  (BentoPDF and several engines). Every component is in
  licenses/components.json with its texts; a new engine or font file in the
  web build stops tools/licenses.py until it is listed. Releases carry the
  source archive.
- **Ask before outward-facing steps** (new remotes, visibility changes,
  sharing).

## Code style

Java 17, framework views, no Gradle; the only library is androidx.webkit.
Comments say why, not what. Every source file starts with an SPDX line.
