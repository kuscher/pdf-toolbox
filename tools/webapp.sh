#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# Builds BentoPDF's web app for PDF Toolbox and caches it:
#   ~/.cache/pdf-toolbox/web-<version>/   the site root the app serves
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
#   EDITOR_FONTS=latin,arabic,hebrew,jp,kr,sc,tc tools/webapp.sh --force
#                              the PDF Editor's fallback fonts (below)
#
# Needs Node with npm (build.sh fetch puts one in ~/.cache/pdf-toolbox/node).
set -euo pipefail
cd "$(dirname "$(readlink -f "$0")")/.."

VERSION=2.8.8
COMMIT=f96cd4e5166f3d51393dfe9f3c440b5bb77802f1 # tag v2.8.8
ORIGIN=https://appassets.androidplatform.net
OCR_LANGS=${OCR_LANGS:-eng}
EDITOR_FONTS=${EDITOR_FONTS:-latin,arabic,hebrew}
CACHE=${PDFTOOLBOX_CACHE:-$HOME/.cache/pdf-toolbox}
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

# The PDF Editor (EmbedPDF) draws text in fonts a PDF doesn't embed with
# fallback fonts it fetches from jsDelivr unless VITE_EMBEDPDF_FONTS_URL
# says otherwise, and the air-gap script leaves them out; offline, its pages
# stay blank. The files are the ones BentoPDF's src/js/config/editor-fonts.ts
# names: latin (also Greek, Cyrillic, Vietnamese), arabic and hebrew by
# default, under 1 MB together; jp, kr, sc and tc add several MB each.
FONTS=$CACHE/embedpdf-fonts
mkdir -p "$FONTS"
EDITOR_FONT_FILES=()
for pack in ${EDITOR_FONTS//,/ }; do
  file=$(sed -nE "s/^ *$pack: '(fonts-$pack@[0-9.]+\/fonts\/[^']+)',?$/\1/p" src/js/config/editor-fonts.ts)
  [[ -n $file ]] || { echo "no editor font pack '$pack' in editor-fonts.ts" >&2; exit 1; }
  version=${file#*@}; tgz=$FONTS/embedpdf-fonts-$pack-${version%%/*}.tgz
  [[ -f $tgz ]] || (cd "$FONTS" && npm pack -q "@embedpdf/${file%%/*}" >/dev/null)
  EDITOR_FONT_FILES+=("$tgz:$file")
done

# Vite's license report: every npm package the site's bundles contain, with
# its license text (build.license). BentoPDF's build script runs a plain
# `vite build`, and Vite reads vite.config.mjs before vite.config.ts, so this
# file wraps BentoPDF's config and adds the report. tools/licenses.py turns it
# into the app's notices. (Vite leaves workers out; licenses.py adds theirs.)
cat > vite.config.mjs <<'EOF'
// Written by PDF Toolbox's tools/webapp.sh: BentoPDF's config plus Vite's license report.
import { mergeConfig } from 'vite';
import base from './vite.config.ts';
export default async (env) => mergeConfig(
  await (typeof base === 'function' ? base(env) : base),
  { build: { license: { fileName: '.vite/licenses.json' } } });
EOF

rm -rf dist
# PDF Toolbox's name and icon where BentoPDF shows its own (the home page's
# title, the PDF Multi Tool's header, the navbar): BentoPDF's own branding
# options. The icon is served from the app's toolbox/ folder (build.sh).
VITE_BRAND_NAME="PDF Toolbox" VITE_BRAND_LOGO=toolbox/icon.svg \
SIMPLE_MODE=true COMPRESSION_MODE=o DISABLE_GITHUB_STARS=true SITE_URL=$ORIGIN \
VITE_WASM_PYMUPDF_URL=$ORIGIN/wasm/pymupdf/ \
VITE_WASM_GS_URL=$ORIGIN/wasm/gs/ \
VITE_WASM_CPDF_URL=$ORIGIN/wasm/cpdf/ \
VITE_TESSERACT_WORKER_URL=$ORIGIN/wasm/ocr/worker.min.js \
VITE_TESSERACT_CORE_URL=$ORIGIN/wasm/ocr/core \
VITE_TESSERACT_LANG_URL=$ORIGIN/wasm/ocr/lang-data \
VITE_TESSERACT_AVAILABLE_LANGUAGES=$OCR_LANGS \
VITE_OCR_FONT_BASE_URL=$ORIGIN/wasm/ocr/fonts \
VITE_EMBEDPDF_FONTS_URL=$ORIGIN/wasm/embedpdf \
NODE_OPTIONS=--max-old-space-size=4096 \
  npm run build
[[ -s dist/.vite/licenses.json ]] || { echo "no license report in dist/.vite: did Vite read vite.config.mjs?" >&2; exit 1; }

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
for entry in "${EDITOR_FONT_FILES[@]}"; do
  file=${entry#*:}
  mkdir -p "$W/embedpdf/${file%/*}"
  tar xzf "${entry%%:*}" -O "package/fonts/${file##*/}" > "$W/embedpdf/$file"
done
cp LICENSE "$WEB.tmp/LICENSE-bentopdf.txt"
echo "$VERSION" > "$WEB.tmp/bentopdf-version.txt"
touch "$WEB.tmp/.complete"
rm -rf "$WEB" && mv "$WEB.tmp" "$WEB"
echo "$WEB"
