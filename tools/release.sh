#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# Makes a BentoBook release from build/BentoBook.apk, for the version in
# AndroidManifest.xml:
#
#   tools/release.sh            the files, in executables/release-<version>/
#   tools/release.sh --publish  also tags v<version>, pushes the tag and makes
#                               the GitHub release with the files
#
# The files:
#   BentoBook.apk                  the app. The name stays the same in every
#                                  release, so .../releases/latest/download/
#                                  BentoBook.apk always gets the newest one.
#   BentoBook-<v>-source.tar.gz    the source the AGPL asks for next to the app:
#                                  this repository at the release commit,
#                                  BentoPDF at the commit tools/webapp.sh pins,
#                                  the engines' build scripts and the notices
#   SHA256SUMS                     checksums of both
#   notes.md                       the release notes (from CHANGELOG.md)
set -euo pipefail
cd "$(dirname "$(readlink -f "$0")")/.."

V=$(sed -n 's/.*android:versionName="\([^"]*\)".*/\1/p' AndroidManifest.xml)
TAG=v$V
OUT=executables/release-$V
APK=build/BentoBook.apk
CACHE=${BENTOBOOK_CACHE:-$HOME/.cache/bentobook}
KEYS=${BENTOBOOK_KEYS:-$HOME/.config/bentobook}
BV=$(sed -n 's/^VERSION=//p' tools/webapp.sh)
BC=$(sed -n 's/^COMMIT=\([0-9a-f]*\).*/\1/p' tools/webapp.sh)
REPO=$(python3 -c "import json; print(json.load(open('licenses/components.json'))['app']['repo'])")
die() { echo "release: $*" >&2; exit 1; }

# The APK must be this version, signed with the release key, and built from
# the commit the source archive is made of.
[[ -f $APK ]] || die "no $APK: run ./build.sh"
got=$(aapt2 dump badging "$APK" | sed -n "s/.*versionName='\([^']*\)'.*/\1/p")
[[ $got == "$V" ]] || die "$APK is version $got, AndroidManifest.xml says $V: run ./build.sh"
[[ -f $KEYS/keystore.jks ]] || die "no release key in $KEYS (see README, Signing)"
cert=$(apksigner verify --print-certs "$APK" | sed -n 's/.*certificate SHA-256 digest: //p' | head -1)
want=$(keytool -list -v -keystore "$KEYS/keystore.jks" -storepass:file "$KEYS/keystore.pass" |
  sed -n 's/^[[:space:]]*SHA256: //p' | head -1 | tr -d ':' | tr 'A-F' 'a-f')
[[ -n $cert && $cert == "$want" ]] || die "$APK isn't signed with the release key in $KEYS"
[[ -z $(git status --porcelain) ]] || die "commit first: the source archive is made from HEAD"
grep -q "^## $V" CHANGELOG.md || die "CHANGELOG.md has no section for $V"
[[ -d $CACHE/bentopdf-$BV ]] || die "no BentoPDF checkout in $CACHE: run ./build.sh"

rm -rf "$OUT" && mkdir -p "$OUT"
cp "$APK" "$OUT/BentoBook.apk"
cp "$APK" "executables/BentoBook-$V.apk"

NAME=BentoBook-$V-source
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/$NAME/engine-build-scripts"
git archive --prefix=bentobook/ HEAD | tar x -C "$TMP/$NAME"
git -C "$CACHE/bentopdf-$BV" archive --prefix="bentopdf-$BV/" "$BC" | tar x -C "$TMP/$NAME"
# From each engine package: its license, readme, package.json and build
# scripts (the compiled files are in the APK).
python3 - "$TMP/$NAME/engine-build-scripts" "$CACHE"/airgap-"$BV"-*/*.tgz <<'PY'
import os, re, sys, tarfile
out = sys.argv[1]
for tgz in sys.argv[2:]:
    dest = os.path.join(out, os.path.basename(tgz)[:-4])
    with tarfile.open(tgz) as t:
        keep = [m for m in t.getmembers() if m.isfile() and re.match(
            r"package/((licen[cs]e|copying|readme|notice)[^/]*|package\.json|build_scripts/.*)$", m.name, re.I)]
        for m in keep:
            m.name = m.name[len("package/"):]
        t.extractall(dest, members=keep, filter="data")
PY
cat > "$TMP/$NAME/README.md" <<EOF
# BentoBook $V: source

The complete source of BentoBook $V ($REPO/releases/tag/$TAG):

- \`bentobook/\`: BentoBook itself at the release commit ($(git rev-parse HEAD)).
  Its README says how to build the APK; THIRD_PARTY_NOTICES.md lists every
  component with its license and the source of its exact version.
- \`bentopdf-$BV/\`: BentoPDF $BV at commit $BC, the app's PDF tools
  (AGPL-3.0; https://github.com/alam00000/bentopdf).
- \`engine-build-scripts/\`: the npm packages of the engines BentoPDF's air-gap
  script fetches (Ghostscript, PyMuPDF, CoherentPDF, Tesseract), without their
  compiled files: their licenses, READMEs and the build scripts that make them
  (Ghostscript's and PyMuPDF's are in \`build_scripts/\`).
EOF
tar czf "$OUT/$NAME.tar.gz" -C "$TMP" "$NAME"

(cd "$OUT" && sha256sum BentoBook.apk "$NAME.tar.gz" > SHA256SUMS)
apk_sha=$(cut -d' ' -f1 < <(sha256sum "$OUT/BentoBook.apk"))
fingerprint=$(sed 's/../&:/g; s/:$//' <<< "${cert^^}")
size=$(( $(stat -c %s "$OUT/BentoBook.apk") / 1000000 ))
{
  awk -v v="$V" '$0 ~ "^## " v { on = 1; next } /^## / { on = 0 } on' CHANGELOG.md
  cat <<EOF

## Install

On your Googlebook, download **BentoBook.apk** below ($size MB) in Chrome and open it.
Android asks once to allow installs from Chrome (or Files): allow it, then
choose **Install**. The [README]($REPO#install) walks through it with the
messages you'll see. One APK for every Googlebook, Intel (x86_64) or Arm.

## Verify

- SHA-256 of BentoBook.apk: \`$apk_sha\`
- Signing certificate SHA-256: \`$fingerprint\`

## License and source

BentoBook's own code is MIT-licensed. The app contains BentoPDF and several
engines under the GNU AGPL v3, so the app as a whole is distributed under the
AGPL v3; every component is listed in [THIRD_PARTY_NOTICES.md]($REPO/blob/$TAG/THIRD_PARTY_NOTICES.md)
and in the app under About & licenses. The complete source is
**$NAME.tar.gz** below.
EOF
} > "$OUT/notes.md"
ls -la "$OUT"

if [[ ${1:-} == --publish ]]; then
  git rev-parse -q --verify "refs/tags/$TAG" >/dev/null || git tag -a "$TAG" -m "BentoBook $V"
  [[ $(git rev-parse "$TAG^{commit}") == "$(git rev-parse HEAD)" ]] || die "$TAG is not HEAD"
  git push origin "$TAG"
  gh release create "$TAG" --title "BentoBook $V" --notes-file "$OUT/notes.md" --latest \
    "$OUT/BentoBook.apk" "$OUT/$NAME.tar.gz" "$OUT/SHA256SUMS"
fi
