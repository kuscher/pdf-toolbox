#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# Makes build/PDFToolbox.aab, the Android App Bundle Google Play takes instead
# of an APK, from what ./build.sh leaves in build/: the same compiled
# resources, assets and dex. The resources are linked again in aapt2's proto
# format (what bundletool reads), laid out as one base module, bundled, and
# signed with jarsigner: a bundle carries a JAR signature, not apksigner's.
# Play App Signing then signs the APKs it serves from the bundle.
#
#   ./build.sh && tools/aab.sh    build/PDFToolbox.aab
#
# The key is the one build.sh signs the APK with: the release key in
# ~/.config/pdf-toolbox (PDFTOOLBOX_KEYS), else the test key, which is fine
# for checking the bundle but not for uploading it. bundletool's jar is
# fetched once into ~/.cache/android (ANDROID_CACHE), like the Android bits
# ./build.sh fetch gets.
set -euo pipefail
cd "$(dirname "$(readlink -f "$0")")/.."

C=${ANDROID_CACHE:-$HOME/.cache/android}
B=${PDFTOOLBOX_CACHE:-$HOME/.cache/pdf-toolbox}
BUNDLETOOL=1.18.3
OUT=build
AAB=$OUT/PDFToolbox.aab

[[ -f $OUT/res.zip && -f $OUT/dex/classes.dex && -d $OUT/assets ]] || { echo "no build/: run ./build.sh first" >&2; exit 1; }
[[ -f $C/bundletool-$BUNDLETOOL.jar ]] || curl -fSLo "$C/bundletool-$BUNDLETOOL.jar" \
  "https://github.com/google/bundletool/releases/download/$BUNDLETOOL/bundletool-all-$BUNDLETOOL.jar"

# One module zip: the manifest and resources.pb as protobuf, res/ as aapt2
# links it, dex/ and assets/ as they are (assets aren't resources; putting
# them straight into the zip saves compressing 180 MB twice).
rm -rf $OUT/aab && mkdir -p $OUT/aab
aapt2 link --proto-format -o $OUT/aab/proto.apk -I "$C/android.jar" --manifest AndroidManifest.xml $OUT/res.zip
python3 - "$OUT" <<'PY'
import os, sys, zipfile
out = sys.argv[1]
proto = zipfile.ZipFile(f"{out}/aab/proto.apk")
with zipfile.ZipFile(f"{out}/aab/base.zip", "w", zipfile.ZIP_DEFLATED) as base:
    for n in proto.namelist():
        if n == "AndroidManifest.xml":
            base.writestr("manifest/AndroidManifest.xml", proto.read(n))
        elif n == "resources.pb" or n.startswith("res/"):
            base.writestr(n, proto.read(n))
    base.write(f"{out}/dex/classes.dex", "dex/classes.dex")
    for root, _, files in os.walk(f"{out}/assets"):
        for f in sorted(files):
            path = os.path.join(root, f)
            base.write(path, os.path.relpath(path, out))
PY
java -jar "$C/bundletool-$BUNDLETOOL.jar" build-bundle --modules=$OUT/aab/base.zip --output=$OUT/aab/unsigned.aab --overwrite
java -jar "$C/bundletool-$BUNDLETOOL.jar" validate --bundle=$OUT/aab/unsigned.aab >/dev/null

KEYS=${PDFTOOLBOX_KEYS:-$HOME/.config/pdf-toolbox}
if [[ -f $KEYS/keystore.jks ]]; then
  KS=$KEYS/keystore.jks; PASS=(-storepass:file "$KEYS/keystore.pass" -keypass:file "$KEYS/keystore.pass")
else
  KS=$B/test-key.jks; PASS=(-storepass test-key -keypass test-key)
  [[ -f $KS ]] || { echo "no key: run ./build.sh first" >&2; exit 1; }
  echo "no release key in $KEYS: signing with the test key $KS (Play won't take it)" >&2
fi
# jarsigner wants the key's alias, which apksigner found by itself.
ALIAS=$(keytool -list -keystore "$KS" "${PASS[@]:0:2}" 2>/dev/null | sed -n 's/^\([^,]*\),.*PrivateKeyEntry.*/\1/p' | head -1)
[[ -n $ALIAS ]] || { echo "no private key in $KS" >&2; exit 1; }
cp $OUT/aab/unsigned.aab "$AAB"
jarsigner -keystore "$KS" "${PASS[@]}" -digestalg SHA-256 -sigalg SHA256withRSA "$AAB" "$ALIAS" >/dev/null
rm -rf $OUT/aab
ls -la "$AAB"
