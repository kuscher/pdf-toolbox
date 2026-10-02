# PDF Toolbox

BentoPDF (static web app, engines in WASM) as an Android app for Googlebooks,
Intel (x86_64) and Arm alike: an offline build served from the APK into a
WebView, with the file picker, downloads, "Open with" and printing added, and
a sidebar of every tool (shell/app.*, served at /toolbox/) with the tool in a
full-height frame. No native code, no Linux VM, no INTERNET permission. Called
BentoBook up to 0.5. Read docs/DESIGN.md; the user guide is README.md.
Development happens on an HP Googlebook 14 (Arm) over adb.

## This repo is public
The Play listing links here. Keep out of every file, commit message and release note: device serial numbers and
adb names, build numbers and codenames, what else is installed or open on the owner's devices, the names of his
private projects and paths into their repos, and where signing keys are backed up (say "backed up privately").

## Commands

```sh
./build.sh fetch | ./build.sh     # toolchain once; then web app (cached) + build/PDFToolbox.apk
tools/webapp.sh [--force]         # BentoPDF's air-gapped build, ~/.cache/pdf-toolbox/web-<v>
./ptb app | install | start | stop | logs [N]
./ptb debug dump | reload | open PATH | devtools on|off | crash
./ptb incoming FILE...            # hand files to the app as if shared (they land in Download/)
./ptb cdp targets | eval JS       # after ./ptb debug devtools on
./ptb shot FILE [full]            # screenshot; view it before sharing
./ptb smoke [CHECK...]            # the engines end to end on the device (tools/smoke.py)
./ptb share                       # executables/PDFToolbox-<v>.apk to the Googlebook's Download
./ptb live-resize [on|off|status] # Android's per-app switch: live window resizing, no veil
git tag v<v> && git push origin v<v>  # the release: GitHub signs and publishes it (docs/RELEASING.md)
./ptb release [--publish]         # the same by hand, on a machine that has the release key
tools/aab.sh                      # build/PDFToolbox.aab for Google Play, after ./build.sh (release key to upload)
python3 tools/licenses.py         # notices (build.sh runs it; fails on unlisted engines)
python3 tools/icon.py [--preview DIR]  # the icon's vector layers and docs/icon.svg
python3 tools/testfiles.py        # test PDFs, a .docx and the demo PDF in test/
python3 tools/readme_images.py [capture]  # README screenshots: capture on the device, then compose
python3 tools/survey.py [PAGE...]  # every PDF tool: compact layout, failed requests (devtools on)
```

adb comes from VSCodeBook's setup; its server runs on a Unix socket. Never
start it on TCP 5037.

## Rules

- **Keep it offline.** No INTERNET permission, no CDN URLs: every engine is
  served from the app's origin (tools/webapp.sh).
- **No native code.** One APK serves x86_64 and Arm Googlebooks; build.sh
  refuses an APK with `lib/` or `.so` files.
- **The package name stays `io.github.kuscher.pdftoolbox`.** Google Play and every
  installed copy are keyed on it. Up to 0.6.1 it was the placeholder
  `local.pdftoolbox`; those installs are a different app to Android and don't
  update in place.
- **Don't inject Android input.** Pickers, installs and permission dialogs
  belong to the user. JS in the app's own WebView over CDP is fine for tests.
- **Clean up test files**: `./ptb incoming` and tool runs write to Download/
  (owner io.github.kuscher.pdftoolbox); delete them when done (smoke.py does).
- **Kill processes by PID**, not `pkill -f`.
- **The release key never goes in git.** GitHub signs the releases: the key
  (a new key since 2026-09-30, alias `pdftoolbox`) is a secret of the repo's
  `release` environment, and the maintainer has a private backup
  outside the repo. You never need the key file: without
  one in `~/.config/pdf-toolbox` (`keystore.jks`, `keystore.pass`) build.sh signs
  with a test key, which is fine for testing. .gitignore blocks `*.jks` and `*.pass`.
- **Each release** bumps versionCode and versionName in AndroidManifest.xml,
  adds a CHANGELOG.md section, writes Play's "What's new"
  (store-submission/listing/en-US/release-notes.txt, at most 500 characters),
  builds, runs `./ptb smoke`, commits and pushes, then
  `git tag v<version> && git push origin v<version>`. The tag makes the GitHub
  release and a draft on Google Play's closed-testing track; sending it for
  review stays a button in the Play Console. docs/RELEASING.md has the details.
- **Licenses:** PDF Toolbox's own code is MIT; the APK is AGPL-3.0 as a whole
  (BentoPDF and several engines). Every component is in
  licenses/components.json with its texts; a new engine or font file in the
  web build stops tools/licenses.py until it is listed. Releases carry the
  source archive.
- **Ask before outward-facing steps** (new remotes, visibility changes,
  sharing).

## Code style

Java 17, framework views, no Gradle; the only library is androidx.webkit.
Comments say why, not what. Every source file starts with an SPDX line.
