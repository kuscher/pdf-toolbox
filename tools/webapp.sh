#!/usr/bin/env bash
# Builds BentoPDF's web app for BentoBook and caches it:
#   ~/.cache/bentobook/web-<version>/   the site root the app serves
#
# BentoPDF's own air-gap route (docs/self-hosting, "Air-Gapped / Offline
# Deployment"): Simple Mode, and every WASM engine and the OCR data served
# from the app's origin instead of jsDelivr. The URLs are baked in at build
# time, and workers load them with importScripts(), so they must be same-origin.
#
#   tools/webapp.sh            build (or reuse the cached build)
#   tools/webapp.sh --force    rebuild
#   OCR_LANGS=eng,deu tools/webapp.sh --force
#                              other OCR languages (Tesseract codes, see
#                              BentoPDF's src/js/config/tesseract-languages.ts)
#
# Needs Node with npm (build.sh fetch puts one in ~/.cache/bentobook/node).
set -euo pipefail
cd "$(dirname "$(readlink -f "$0")")/.."

VERSION=2.8.8
COMMIT=f96cd4e5166f3d51393dfe9f3c440b5bb77802f1 # tag v2.8.8
ORIGIN=https://appassets.androidplatform.net
OCR_LANGS=${OCR_LANGS:-eng}
CACHE=${BENTOBOOK_CACHE:-$HOME/.cache/bentobook}
SRC=$CACHE/bentopdf-$VERSION
AIRGAP=$CACHE/airgap-$VERSION-${OCR_LANGS//,/-}
WEB=$CACHE/web-$VERSION
export PATH=$CACHE/node/bin:$PATH HUSKY=0

[[ ${1:-} == --force ]] && rm -rf "$WEB"
if [[ -f $WEB/.complete ]]; then echo "$WEB"; exit 0; fi
command -v npm >/dev/null || { echo "no npm: run ./build.sh fetch" >&2; exit 1; }

if [[ ! -f $SRC/package.json ]]; then
  rm -rf "$SRC" && mkdir -p "$SRC"
  git -C "$SRC" init -q
  git -C "$SRC" fetch -q --depth 1 https://github.com/alam00000/bentopdf.git "$COMMIT"
  git -C "$SRC" checkout -q FETCH_HEAD
fi
cd "$SRC"
[[ -d node_modules ]] || npm ci --no-audit --no-fund

# The AGPL engines (PyMuPDF, Ghostscript, CoherentPDF) and Tesseract, at the
# versions this release expects, plus OCR language data and fonts.
if ! ls "$AIRGAP"/bentopdf-pymupdf-wasm-*.tgz >/dev/null 2>&1; then
  bash scripts/prepare-airgap.sh --skip-docker --simple-mode --wasm-base-url "$ORIGIN/wasm" \
    --ocr-languages "$OCR_LANGS" --output-dir "$AIRGAP" </dev/null
fi

rm -rf dist
SIMPLE_MODE=true COMPRESSION_MODE=o DISABLE_GITHUB_STARS=true SITE_URL=$ORIGIN \
VITE_WASM_PYMUPDF_URL=$ORIGIN/wasm/pymupdf/ \
VITE_WASM_GS_URL=$ORIGIN/wasm/gs/ \
VITE_WASM_CPDF_URL=$ORIGIN/wasm/cpdf/ \
VITE_TESSERACT_WORKER_URL=$ORIGIN/wasm/ocr/worker.min.js \
VITE_TESSERACT_CORE_URL=$ORIGIN/wasm/ocr/core \
VITE_TESSERACT_LANG_URL=$ORIGIN/wasm/ocr/lang-data \
VITE_TESSERACT_AVAILABLE_LANGUAGES=$OCR_LANGS \
VITE_OCR_FONT_BASE_URL=$ORIGIN/wasm/ocr/fonts \
NODE_OPTIONS=--max-old-space-size=4096 \
  npm run build

rm -rf "$WEB.tmp" && cp -a dist "$WEB.tmp"
W=$WEB.tmp/wasm
mkdir -p "$W/pymupdf" "$W/gs" "$W/cpdf" "$W/ocr/core" "$W/ocr/lang-data" "$W/ocr/fonts"
# Laid out as the air-gap bundle's setup.sh does: Ghostscript's assets/ and
# CoherentPDF's dist/ at the root of their folders.
tar xzf "$AIRGAP"/bentopdf-pymupdf-wasm-*.tgz -C "$W/pymupdf" --strip-components=1
tar xzf "$AIRGAP"/bentopdf-gs-wasm-*.tgz -C "$W/gs" --strip-components=2 package/assets
# PyMuPDF imports the package's own entry point (gs/dist/index.js), which
# loads gs/assets/gs.js; the app serves gs/assets/* from gs/ (Web.serve).
tar xzf "$AIRGAP"/bentopdf-gs-wasm-*.tgz -C "$W/gs" --strip-components=1 package/dist/index.js
tar xzf "$AIRGAP"/coherentpdf-*.tgz -C "$W/cpdf" --strip-components=2 package/dist
tar xzf "$AIRGAP"/tesseract.js-core-*.tgz -C "$W/ocr/core" --strip-components=1
tar xzf "$AIRGAP"/tesseract.js-[0-9]*.tgz -C "$W/ocr" --strip-components=2 package/dist/worker.min.js
cp "$AIRGAP"/tesseract-langdata/*.traineddata.gz "$W/ocr/lang-data/"
cp "$AIRGAP"/ocr-fonts/* "$W/ocr/fonts/"
cp LICENSE "$WEB.tmp/LICENSE-bentopdf.txt"
echo "$VERSION" > "$WEB.tmp/bentopdf-version.txt"
touch "$WEB.tmp/.complete"
rm -rf "$WEB" && mv "$WEB.tmp" "$WEB"
echo "$WEB"
