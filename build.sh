#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# Builds and signs BentoBook without Gradle: Debian's aapt2 for resources,
# javac for the code, Google's D8 for dex, then zipalign and apksigner from
# Debian or Ubuntu, on x86_64 or arm64 (sudo apt install aapt zipalign
# apksigner default-jdk-headless git python3 curl).
#
#   ./build.sh fetch   once per machine: the Android bits Debian doesn't
#                      package (~/.cache/android) and a Node toolchain with
#                      npm for this machine's CPU (~/.cache/bentobook/node)
#   ./build.sh         builds build/BentoBook.apk; the first run also builds
#                      BentoPDF's web app (tools/webapp.sh, cached)
#
# The release key is not in the repository: it lives in ~/.config/bentobook
# (keystore.jks and keystore.pass; BENTOBOOK_KEYS points elsewhere). Without
# it the APK is signed with a test key, which is fine for trying a build but
# can't update a BentoBook installed from a release.
set -euo pipefail
cd "$(dirname "$(readlink -f "$0")")"

C=${ANDROID_CACHE:-$HOME/.cache/android}
B=${BENTOBOOK_CACHE:-$HOME/.cache/bentobook}
WEBKIT=1.18.0-alpha02 # for Profile#setCrossOriginIsolatedAllowlist
NODE_MAJOR=22

fetch() {
  mkdir -p "$C/dl" "$B"
  local repo=https://dl.google.com/android
  unzip_one() { python3 -c "import zipfile,sys; open(sys.argv[3],'wb').write(zipfile.ZipFile(sys.argv[1]).read(sys.argv[2]))" "$@"; }
  [[ -f $C/android.jar ]] || { curl -fSLo "$C/dl/p30.zip" $repo/repository/platform-30_r03.zip &&
    unzip_one "$C/dl/p30.zip" android-11/android.jar "$C/android.jar"; }
  [[ -f $C/android-37.jar ]] || { curl -fSLo "$C/dl/p37.zip" $repo/repository/platform-37.2_r01.zip &&
    unzip_one "$C/dl/p37.zip" android-37.2/android.jar "$C/android-37.jar"; }
  [[ -f $C/r8.jar ]] || curl -fSLo "$C/r8.jar" https://maven.google.com/com/android/tools/r8/8.5.35/r8-8.5.35.jar
  [[ -f $C/webkit-$WEBKIT.jar ]] || { curl -fSLo "$C/dl/webkit.aar" $repo/maven2/androidx/webkit/webkit/$WEBKIT/webkit-$WEBKIT.aar &&
    unzip_one "$C/dl/webkit.aar" classes.jar "$C/webkit-$WEBKIT.jar"; }
  [[ -f $C/androidx-core-bits-1.1.0.jar ]] || { curl -fSLo "$C/dl/core.aar" $repo/maven2/androidx/core/core/1.1.0/core-1.1.0.aar &&
    python3 - "$C/dl/core.aar" "$C/androidx-core-bits-1.1.0.jar" <<'PY2'
import io, sys, zipfile
classes = zipfile.ZipFile(io.BytesIO(zipfile.ZipFile(sys.argv[1]).read("classes.jar")))
with zipfile.ZipFile(sys.argv[2], "w") as out:
    for n in classes.namelist():
        if n.startswith(("androidx/core/content/pm/PackageInfoCompat", "androidx/core/util/Pair")):
            out.writestr(n, classes.read(n))
PY2
  }
  rm -rf "$C/dl"
  if [[ ! -x $B/node/bin/npm ]]; then
    local v
    v=$(curl -fsSL https://nodejs.org/dist/index.json | python3 -c \
      "import json,sys; print(next(r['version'] for r in json.load(sys.stdin) if r['lts'] and r['version'].startswith('v$NODE_MAJOR.')))")
    curl -fsSL "https://nodejs.org/dist/$v/node-$v-linux-$(uname -m | sed 's/aarch64/arm64/;s/x86_64/x64/').tar.xz" | tar xJ -C "$B"
    ln -sfn "$B/node-$v-linux-"* "$B/node"
  fi
  echo "toolchain in $C, node $("$B/node/bin/node" --version) in $B"
}

if [[ ${1:-} == fetch ]]; then fetch; exit; fi
for f in android.jar android-37.jar r8.jar webkit-$WEBKIT.jar androidx-core-bits-1.1.0.jar; do
  [[ -f $C/$f ]] || { echo "missing $C/$f: run ./build.sh fetch" >&2; exit 1; }
done
WEB=$(tools/webapp.sh | tail -1)
LIBS="$C/webkit-$WEBKIT.jar:$C/androidx-core-bits-1.1.0.jar"
OUT=build
APK=$OUT/BentoBook.apk

rm -rf $OUT
mkdir -p $OUT/gen $OUT/classes $OUT/dex $OUT/assets/shell $OUT/assets/web
# The site, minus what only a web server wants: precompressed copies for
# nginx, sitemaps, the build marker and Vite's license report (read below).
# (LibreOffice's .gz files and the OCR data stay: the page fetches those
# names and unpacks them itself.)
cp -a "$WEB"/. $OUT/assets/web/
find $OUT/assets/web \( -name '*.br' -o -name 'sitemap*.xml' -o -name .complete \) -delete
rm -rf $OUT/assets/web/.vite
# Files nothing in Simple Mode loads. The web root's CoherentPDF is a copy of
# wasm/cpdf's (which the workers load) under a header that calls it BentoPDF's
# own; the other cpdf builds are for Node or unminified. The badges are
# bentopdf.com's landing-page artwork, one of them DigitalOcean's logo.
rm -f $OUT/assets/web/coherentpdf.browser.min.js \
  $OUT/assets/web/wasm/cpdf/{coherentpdf.js,coherentpdf.min.js,coherentpdf.browser.js} \
  $OUT/assets/web/images/{badge,gdpr,ccpa,hipaa}.svg $OUT/assets/web/images/{bentopdf-tools,favicon}.png
# tesseract.js's worker loads Tesseract's single-file builds (*.wasm.js); the
# separate .js + .wasm pairs of the same six builds (19.5 MB) are never fetched.
find $OUT/assets/web/wasm/ocr/core \( -name 'tesseract-core*.wasm' -o \
  \( -name 'tesseract-core*.js' ! -name '*.wasm.js' \) \) -delete
cp shell/page_shim.js $OUT/assets/shell/
# Worker scripts that start workers of their own (see shell/nested-workers.js).
for w in libreoffice-wasm/browser.worker.global.js; do
  cat shell/nested-workers.js "$OUT/assets/web/$w" > "$OUT/w.tmp" && mv "$OUT/w.tmp" "$OUT/assets/web/$w"
done
# About & licenses (/bentobook/), and THIRD_PARTY_NOTICES.md in the repo. It
# stops the build if a file in the site belongs to no listed component.
python3 tools/licenses.py --web $OUT/assets/web --report "$WEB/.vite/licenses.json" --app $OUT/assets/web/bentobook

aapt2 compile --dir res -o $OUT/res.zip
aapt2 link -o $OUT/app.apk -I "$C/android.jar" --manifest AndroidManifest.xml \
  -A $OUT/assets --java $OUT/gen $OUT/res.zip
javac --release 17 -Xlint:all,-options,-serial,-classfile -Xmaxwarns 50 -encoding UTF-8 \
  -cp "$C/android-37.jar:$LIBS" -d $OUT/classes $(find src $OUT/gen -name '*.java')
java -cp "$C/r8.jar" com.android.tools.r8.D8 --release --min-api 34 --lib "$C/android-37.jar" \
  --output $OUT/dex $(find $OUT/classes -name '*.class') ${LIBS//:/ }

python3 - "$OUT" <<'PY'
import sys, zipfile
out = sys.argv[1]
with zipfile.ZipFile(f"{out}/app.apk", "a", zipfile.ZIP_DEFLATED) as apk:
    apk.write(f"{out}/dex/classes.dex", "classes.dex")
PY
# No native code, so one APK runs on every Googlebook, Arm or x86: the
# engines are WebAssembly. Keep it that way.
python3 - "$OUT/app.apk" <<'PY'
import sys, zipfile
native = [n for n in zipfile.ZipFile(sys.argv[1]).namelist() if n.startswith("lib/") or n.endswith(".so")]
if native:
    sys.exit(f"native code in the APK ties it to one CPU architecture: {native[:5]}")
PY
zipalign -f 4 $OUT/app.apk $OUT/aligned.apk
KEYS=${BENTOBOOK_KEYS:-$HOME/.config/bentobook}
if [[ -f $KEYS/keystore.jks ]]; then
  KS=$KEYS/keystore.jks PASS=file:$KEYS/keystore.pass
else
  KS=$B/test-key.jks PASS=pass:test-key
  [[ -f $KS ]] || keytool -genkeypair -keystore "$KS" -storetype PKCS12 -storepass test-key -alias bentobook \
    -keyalg RSA -keysize 2048 -validity 36500 -dname "CN=BentoBook test build" 2>/dev/null
  echo "no release key in $KEYS: signing with the test key $KS" >&2
fi
apksigner sign --ks "$KS" --ks-pass "$PASS" --out $APK $OUT/aligned.apk
rm -f $APK.idsig
ls -la $APK
