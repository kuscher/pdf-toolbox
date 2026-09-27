# Third-party notices

<!-- Written by tools/licenses.py from licenses/components.json and BentoPDF's
     build; run it again after changing either. -->

PDF Toolbox 0.6 is BentoPDF 2.8.8 in an Android app. PDF Toolbox's own code (this
repository) is under the MIT License ([LICENSE](LICENSE)). The app it builds contains BentoPDF
and several engines under the GNU Affero General Public License v3, so the app as a whole is
distributed under the AGPL v3 ([licenses/texts/AGPL-3.0.txt](licenses/texts/AGPL-3.0.txt)).
Every part keeps its own license, listed below with its copyright holders and its source.
The app shows the same list, with every license text, under **About & licenses**.

## BentoPDF, modified

PDF Toolbox contains a modified version of BentoPDF 2.8.8 (commit
[`f96cd4e`](https://github.com/alam00000/bentopdf/tree/f96cd4e5166f3d51393dfe9f3c440b5bb77802f1)), AGPL-3.0,
copyright © the BentoPDF authors. The changes, all in this repository:

- it is built in Simple Mode, with every engine, its data and the editor's fonts
  served from the app instead of CDNs, and with PDF Toolbox's name and logo in its
  header (tools/webapp.sh);
- PDF Toolbox's page script (shell/page_shim.js) runs in every page: opening and saving
  files through Android, printing, a compact tool layout and the About link;
- the app shows its pages in PDF Toolbox's sidebar window (shell/app.html), which hides
  BentoPDF's top bar and the PDF Multi Tool's header there;
- a prelude (shell/nested-workers.js) is prepended to the LibreOffice converter's worker,
  so its thread workers can start in Android's WebView.

PDFs made with PDF Toolbox keep BentoPDF's producer line, as BentoPDF asks.

## Source code

Whoever has the app is entitled to its complete source: this repository at the release's
tag (it builds the APK), BentoPDF at the commit above, and the sources listed for each
component below. Each GitHub release carries a source archive of the first two and the
engines' build scripts, and a second archive with the sources that
[licenses/mirror.txt](licenses/mirror.txt) lists: the GPL-2.0 fonts and the LGPL
libraries compiled into the engines, whose licenses ask for them next to the app
(`./ptb release`).

## BentoPDF and PDF Toolbox

| Component | Version | License | Copyright | Source |
| --- | --- | --- | --- | --- |
| PDF Toolbox | 0.6 | MIT ([MIT-PDFToolbox.txt](licenses/texts/MIT-PDFToolbox.txt)) | Copyright (c) 2026 the PDF Toolbox authors | https://github.com/kuscher/pdf-toolbox/tree/v0.6 |
| BentoPDF | 2.8.8 | AGPL-3.0-only ([AGPL-3.0.txt](licenses/texts/AGPL-3.0.txt)) | Copyright © 2026 BentoPDF, the BentoPDF authors | https://github.com/alam00000/bentopdf/tree/f96cd4e5166f3d51393dfe9f3c440b5bb77802f1 |

## Engines

| Component | Version | License | Copyright | Source |
| --- | --- | --- | --- | --- |
| LibreOffice | 24.8.8 | MPL-2.0 AND Apache-2.0 ([LibreOffice-24.8-LICENSE.txt](licenses/texts/LibreOffice-24.8-LICENSE.txt), [LibreOffice-24.8-license.xml.txt](licenses/texts/LibreOffice-24.8-license.xml.txt), [LibreOffice-COPYING.MPL.txt](licenses/texts/LibreOffice-COPYING.MPL.txt), [LibreOffice-NOTICE.txt](licenses/texts/LibreOffice-NOTICE.txt), [ICU-74.2-LICENSE.txt](licenses/texts/ICU-74.2-LICENSE.txt), [pdfium-6425-LICENSE.txt](licenses/texts/pdfium-6425-LICENSE.txt), [pdfium-6425-third_party-agg23-notice.txt](licenses/texts/pdfium-6425-third_party-agg23-notice.txt), [pdfium-6425-third_party-freetype-2.13.2-FTL.txt](licenses/texts/pdfium-6425-third_party-freetype-2.13.2-FTL.txt), [FreeType-FTL.txt](licenses/texts/FreeType-FTL.txt), [abseil-cpp-LICENSE-Apache-2.0.txt](licenses/texts/abseil-cpp-LICENSE-Apache-2.0.txt), [MuPDF-thirdparty-openjpeg-2.5.3-LICENSE.txt](licenses/texts/MuPDF-thirdparty-openjpeg-2.5.3-LICENSE.txt), [SPDX-Apache-2.0.txt](licenses/texts/SPDX-Apache-2.0.txt), [SPDX-MPL-1.1.txt](licenses/texts/SPDX-MPL-1.1.txt), [SPDX-BSL-1.0.txt](licenses/texts/SPDX-BSL-1.0.txt), [SPDX-CC0-1.0.txt](licenses/texts/SPDX-CC0-1.0.txt), [SPDX-Unicode-3.0.txt](licenses/texts/SPDX-Unicode-3.0.txt)) | Copyright © 2000–2025 LibreOffice contributors. All rights reserved.; This product is based on OpenOffice.org. Portions of this software are copyright © 2000-2011, Oracle and/or its affiliates.; Apache OpenOffice (http://www.openoffice.org) Copyright 2011, 2014 The Apache Software Foundation; Portions of this software (C) Copyright IBM Corporation 2003, 2012.  All Rights Reserved. | https://git.libreoffice.org/core/+/d1c9e0e4e1ddeb24fe8f93e56860b3765043f8b1 (mirror: https://github.com/LibreOffice/core/tree/d1c9e0e4e1ddeb24fe8f93e56860b3765043f8b1); bundled externals from https://dev-www.libreoffice.org/src/ as pinned in download.lst at that commit; build patch https://github.com/matbeedotcom/libreoffice-document-converter/blob/b94b8a6887d223be93b082543f5fd32bbd8dc646/build/patches/wasm-build-fixes.patch and build/autogen.input (identical to the versions in commit 749a21a4a16c that produced the binary) |
| ↳ ICU (icu4c + data icudt74l) | 74.2 | Unicode-3.0 | Copyright © 2016-2023 Unicode, Inc. | https://dev-www.libreoffice.org/src/icu4c-74_2-src.tgz, https://dev-www.libreoffice.org/src/icu4c-74_2-data.zip |
| ↳ HarfBuzz | 8.5.0 | MIT-Modern-Variant | see LibreOffice-24.8-LICENSE.txt, HarfBuzz section | https://dev-www.libreoffice.org/src/harfbuzz-8.5.0.tar.xz |
| ↳ Graphite2 | 1.3.14 | LGPL-2.1-or-later OR MPL-2.0 OR GPL-2.0-or-later | Copyright 2010, SIL International All rights reserved. | https://dev-www.libreoffice.org/src/graphite2-minimal-1.3.14.tgz |
| ↳ FreeType (LibreOffice external, used by vcl) | 2.13.3 | FTL OR GPL-2.0-or-later | Copyright (C) 1996-2024 by David Turner, Robert Wilhelm, Werner Lemberg (FreeType Project) | https://dev-www.libreoffice.org/src/freetype-2.13.3.tar.xz |
| ↳ Fontconfig (library + share/fontconfig/*.conf) | 2.15.0 | HPND-sell-variant | Copyright © 2002 Keith Packard | https://dev-www.libreoffice.org/src/fontconfig-2.15.0.tar.xz |
| ↳ cairo | 1.17.6 | LGPL-2.1-only OR MPL-1.1 | see LibreOffice-24.8-LICENSE.txt, Cairo section | https://dev-www.libreoffice.org/src/cairo-1.17.6.tar.xz |
| ↳ pixman | 0.42.2 | MIT | Copyright 1987, 1988, 1989, 1998 The Open Group; Copyright 2004, 2005, 2007, 2008, 2009, 2010 Red Hat, Inc.; and others listed in the LibreOffice notice | https://dev-www.libreoffice.org/src/pixman-0.42.2.tar.gz |
| ↳ libpng | 1.6.47 | libpng-2.0 | see LibreOffice-24.8-LICENSE.txt, libpng section | https://dev-www.libreoffice.org/src/libpng-1.6.47.tar.xz |
| ↳ libjpeg-turbo | 2.1.5.1 | IJG AND BSD-3-Clause AND Zlib | Copyright (C) 1991-2023 The libjpeg-turbo Project and many others | https://dev-www.libreoffice.org/src/libjpeg-turbo-2.1.5.1.tar.gz |
| ↳ libtiff | 4.7.0 | libtiff | Copyright (c) 1988-1997 Sam Leffler; Copyright (c) 1991-1997 Silicon Graphics, Inc. | https://dev-www.libreoffice.org/src/tiff-4.7.0.tar.xz |
| ↳ libwebp | 1.5.0 | BSD-3-Clause | Copyright (c) 2010, Google Inc. All rights reserved. | https://dev-www.libreoffice.org/src/libwebp-1.5.0.tar.gz |
| ↳ zlib | 1.3.1 | Zlib | (C) 1995-2024 Jean-loup Gailly and Mark Adler | https://dev-www.libreoffice.org/src/zlib-1.3.1.tar.xz |
| ↳ expat | 2.7.1 | MIT | see LibreOffice-24.8-LICENSE.txt, expat section | https://dev-www.libreoffice.org/src/expat-2.7.1.tar.xz |
| ↳ libxml2 | 2.13.8 | MIT | see LibreOffice-24.8-LICENSE.txt, libxml2 section | https://dev-www.libreoffice.org/src/libxml2-2.13.8.tar.xz |
| ↳ libxslt | 1.1.43 | MIT | see LibreOffice-24.8-LICENSE.txt, libxslt section | https://dev-www.libreoffice.org/src/libxslt-1.1.43.tar.xz |
| ↳ Little CMS (lcms2) | 2.16 | MIT | Copyright (c) 1998-2011 Marti Maria Saguer | https://dev-www.libreoffice.org/src/lcms2-2.16.tar.gz |
| ↳ OpenSSL (libcrypto) | 3.0.16 | Apache-2.0 | see LibreOffice-24.8-LICENSE.txt, OpenSSL section (Apache-2.0) | https://dev-www.libreoffice.org/src/openssl-3.0.16.tar.gz |
| ↳ Boost (mostly headers) | 1.85.0 | BSL-1.0 | see LibreOffice-24.8-LICENSE.txt, C++ Boost Library section | https://dev-www.libreoffice.org/src/boost_1_85_0.tar.xz |
| ↳ liborcus | 0.19.2 | MPL-2.0 |  | https://dev-www.libreoffice.org/src/liborcus-0.19.2.tar.xz |
| ↳ mdds | 2.1.1 | MIT | Copyright (c) 2010 Kohei Yoshida | https://dev-www.libreoffice.org/src/mdds-2.1.1.tar.xz |
| ↳ PDFium | 6425 (chromium/6425) | BSD-3-Clause AND Apache-2.0 | Copyright 2014 The PDFium Authors | https://dev-www.libreoffice.org/src/pdfium-6425.tar.bz2 |
| ↳ PDFium third_party/freetype (separate FreeType copy compiled because OS=EMSCRIPTEN is not LINUX/ANDROID) | 2.13.2 (VER-2-13-2-109, f42ce25563b73fed0123d18a2556b9ba01d2c76b) | FTL | Portions of this software are copyright © <year> The FreeType Project (www.freetype.org). All rights reserved. | https://dev-www.libreoffice.org/src/pdfium-6425.tar.bz2 (third_party/freetype) |
| ↳ PDFium third_party/agg23 (Anti-Grain Geometry) | 2.3 | LicenseRef-AGG-2.3-permissive | Copyright (C) 2002-2005 Maxim Shemanarev (http://www.antigrain.com) | https://dev-www.libreoffice.org/src/pdfium-6425.tar.bz2 (third_party/agg23) |
| ↳ PDFium third_party/libopenjpeg | 2.5.0 + pdfium patches | BSD-2-Clause | Copyright (c) 2002-2014, Universite catholique de Louvain (UCL), Belgium; Copyright (c) 2002-2014, Professor Benoit Macq; and others (see MuPDF-thirdparty-openjpeg-2.5.3-LICENSE.txt, same text) | https://dev-www.libreoffice.org/src/pdfium-6425.tar.bz2 (third_party/libopenjpeg) |
| ↳ PDFium third_party/abseil-cpp (bad_optional_access, bad_variant_access) | as vendored in pdfium 6425 | Apache-2.0 | Copyright 2017 The Abseil Authors. | https://dev-www.libreoffice.org/src/pdfium-6425.tar.bz2 (third_party/abseil-cpp) |
| ↳ Raptor RDF Parser Library | 2.0.15 | LGPL-2.1-or-later OR GPL-2.0-or-later OR Apache-2.0 | Copyright (C) 2000-2008 David Beckett; Copyright (C) 2000-2005 University of Bristol. All Rights Reserved. | https://dev-www.libreoffice.org/src/a39f6c07ddb20d7dd2ff1f95fa21e2cd-raptor2-2.0.15.tar.gz |
| ↳ Rasqal RDF Query Library | 0.9.33 | LGPL-2.1-or-later OR GPL-2.0-or-later OR Apache-2.0 | Copyright (C) 2000-2008 David Beckett; Copyright (C) 2000-2005 University of Bristol. All Rights Reserved. | https://dev-www.libreoffice.org/src/1f5def51ca0026cd192958ef07228b52-rasqal-0.9.33.tar.gz |
| ↳ Redland RDF Application Framework (librdf) | 1.0.17 | LGPL-2.1-or-later OR GPL-2.0-or-later OR Apache-2.0 | Copyright (C) 2000-2008 David Beckett; Copyright (C) 2000-2005 University of Bristol. All Rights Reserved. | https://dev-www.libreoffice.org/src/e5be03eda13ef68aabab6e42aa67715e-redland-1.0.17.tar.gz |
| ↳ Argon2 (phc-winner-argon2) | 20190702 | CC0-1.0 OR Apache-2.0 |  | https://dev-www.libreoffice.org/src/phc-winner-argon2-20190702.tar.gz |
| ↳ Box2D | 2.4.1 | MIT | see upstream box2d LICENSE (Copyright (c) 2019 Erin Catto) | https://dev-www.libreoffice.org/src/box2d-2.4.1.tar.gz |
| ↳ Hunspell | 1.7.2 | MPL-1.1 OR GPL-2.0-or-later OR LGPL-2.1-or-later |  | https://dev-www.libreoffice.org/src/hunspell-1.7.2.tar.gz |
| ↳ Hyphen | 2.8.8 | MPL-1.1 OR GPL-2.0-or-later OR LGPL-2.1-or-later |  | https://dev-www.libreoffice.org/src/5ade6ae2a99bc1e9e57031ca88d36dad-hyphen-2.8.8.tar.gz |
| ↳ MyThes | 1.2.5 | LicenseRef-MyThes-BSD-style | Copyright 2003 Kevin B. Hendricks, Stratford, Ontario, Canada And Contributors. All rights reserved. | https://dev-www.libreoffice.org/src/mythes-1.2.5.tar.xz |
| ↳ liblangtag (+ share/liblangtag data: Unicode CLDR bcp47/supplemental XML, IANA language-subtag-registry dated 2023-10-16) | 0.6.7 | LGPL-3.0-or-later OR MPL-2.0 |  | https://dev-www.libreoffice.org/src/liblangtag-0.6.7.tar.bz2 |
| ↳ libnumbertext | 1.0.11 | BSD-3-Clause OR LGPL-3.0-or-later | Copyright 2009–2019 László Németh et al. | https://dev-www.libreoffice.org/src/libnumbertext-1.0.11.tar.xz |
| ↳ librevenge | 0.0.5 | MPL-2.0 OR LGPL-2.1-or-later |  | https://dev-www.libreoffice.org/src/librevenge-0.0.5.tar.bz2 |
| ↳ libodfgen | 0.1.8 | MPL-2.0 OR LGPL-2.1-or-later |  | https://dev-www.libreoffice.org/src/libodfgen-0.1.8.tar.xz |
| ↳ libwps (MS Works/Multiplan/Lotus spreadsheet import via MSWorksCalcImportFilter) | 0.4.14 | MPL-2.0 OR LGPL-2.1-or-later |  | https://dev-www.libreoffice.org/src/libwps-0.4.14.tar.xz |
| ↳ libmwaw (MWAWCalcImportFilter) | 0.3.22 | MPL-2.0 OR LGPL-2.1-or-later |  | https://dev-www.libreoffice.org/src/libmwaw-0.3.22.tar.xz |
| ↳ libstaroffice (StarOffice Writer/Calc import) | 0.0.7 | MPL-2.0 OR LGPL-2.1-or-later |  | https://dev-www.libreoffice.org/src/libstaroffice-0.0.7.tar.xz |
| ↳ zxcvbn-c | 2.5 | MIT | Copyright (c) 2015-2017 Tony Evans | https://dev-www.libreoffice.org/src/zxcvbn-c-2.5.tar.gz |
| ↳ Dragonbox (header-only, sal) | 1.1.3 | Apache-2.0 WITH LLVM-exception OR BSL-1.0 |  | https://dev-www.libreoffice.org/src/dragonbox-1.1.3.tar.gz |
| ↳ dtoa (David M. Gay) | 20180411 | LicenseRef-dtoa-Gay (MIT-style) | Copyright (c) 1991, 2000, 2001 by Lucent Technologies. | https://dev-www.libreoffice.org/src/dtoa-20180411.tgz |
| ↳ frozen (header-only) | 1.1.1 | Apache-2.0 |  | https://dev-www.libreoffice.org/src/frozen-1.1.1.tar.gz |
| ↳ JessyInk code in the SVG presentation engine (filter/source/svg/presentation_engine.js, embedded) | as in LibreOffice 24.8 | MPL-2.0 OR GPL-3.0-or-later | Copyright 2008-2013 Hannes Hochreiner | https://git.libreoffice.org/core/+/d1c9e0e4e1ddeb24fe8f93e56860b3765043f8b1 (mirror: https://github.com/LibreOffice/core/tree/d1c9e0e4e1ddeb24fe8f93e56860b3765043f8b1) |
| ↳ Dojo Toolkit code in the SVG presentation engine | as in LibreOffice 24.8 | BSD-3-Clause | Copyright (c) 2005-2012, The Dojo Foundation | https://git.libreoffice.org/core/+/d1c9e0e4e1ddeb24fe8f93e56860b3765043f8b1 (mirror: https://github.com/LibreOffice/core/tree/d1c9e0e4e1ddeb24fe8f93e56860b3765043f8b1) |
| ↳ SVGPathSeg polyfill in the SVG presentation engine | as in LibreOffice 24.8 | BSD-3-Clause | Copyright 2015 The Chromium Authors. All rights reserved. | https://git.libreoffice.org/core/+/d1c9e0e4e1ddeb24fe8f93e56860b3765043f8b1 (mirror: https://github.com/LibreOffice/core/tree/d1c9e0e4e1ddeb24fe8f93e56860b3765043f8b1) |
| ↳ Colibre icon theme (share/config/images_colibre.zip) | as in LibreOffice 24.8 | CC0-1.0 | Original author: Andreas Kainz | https://git.libreoffice.org/core/+/d1c9e0e4e1ddeb24fe8f93e56860b3765043f8b1 (mirror: https://github.com/LibreOffice/core/tree/d1c9e0e4e1ddeb24fe8f93e56860b3765043f8b1) |
| ↳ Emscripten runtime (musl libc, libc++/libc++abi, compiler-rt, malloc) | 3.1.74 per build script | MIT AND (Apache-2.0 WITH LLVM-exception) AND (MIT OR NCSA) |  | see component emscripten-runtime |
| PyMuPDF | 1.26.3 | AGPL-3.0-or-later ([PyMuPDF-1.26.3-COPYING.txt](licenses/texts/PyMuPDF-1.26.3-COPYING.txt), [MuPDF-1.26.3-COPYING-AGPL-3.0.txt](licenses/texts/MuPDF-1.26.3-COPYING-AGPL-3.0.txt)) | Copyright (C) 2023 Artifex Software, Inc. (pymupdf/table.py); Copyright 2020-2022, Harald Lieder (pymupdf/utils.py, __main__.py) | https://files.pythonhosted.org/packages/source/p/pymupdf/pymupdf-1.26.3.tar.gz (sha256 b7d2c3ffa9870e1e4416d18862f5ccd356af5fe337b4511093bbbce2ca73b7e5); git https://github.com/pymupdf/PyMuPDF/tree/1.26.3 (48cdb0d2f0b7971fb5a7848e816dfd2bd6e193f4) |
| ↳ MuPDF | 1.26.3 | AGPL-3.0-or-later |  | see component mupdf |
| Ghostscript (@bentopdf/gs-wasm) | 10.06.0 | AGPL-3.0-only ([AGPL-3.0.txt](licenses/texts/AGPL-3.0.txt), [ghostscript-10.06.0--LICENSE.txt](licenses/texts/ghostscript-10.06.0--LICENSE.txt), [bentopdf-gs-wasm-0.1.1--README.md.txt](licenses/texts/bentopdf-gs-wasm-0.1.1--README.md.txt), [freetype-2.13.3--LICENSE.TXT.txt](licenses/texts/freetype-2.13.3--LICENSE.TXT.txt), [freetype-2.13.3--FTL.TXT.txt](licenses/texts/freetype-2.13.3--FTL.TXT.txt), [libjpeg-9f--README.txt](licenses/texts/libjpeg-9f--README.txt), [libpng-1.6.50--LICENSE.txt](licenses/texts/libpng-1.6.50--LICENSE.txt), [zlib-1.3.1--LICENSE.txt](licenses/texts/zlib-1.3.1--LICENSE.txt), [lcms2mt-2.12--COPYING.txt](licenses/texts/lcms2mt-2.12--COPYING.txt), [openjpeg-2.5.3--LICENSE.txt](licenses/texts/openjpeg-2.5.3--LICENSE.txt), [jbig2dec-0.20--LICENSE.txt](licenses/texts/jbig2dec-0.20--LICENSE.txt), [libtiff-4.7.0--LICENSE.md.txt](licenses/texts/libtiff-4.7.0--LICENSE.md.txt), [brotli-1.0.9--LICENSE.txt](licenses/texts/brotli-1.0.9--LICENSE.txt), [ghostscript-10.06.0--base-sha2.c-notice.txt](licenses/texts/ghostscript-10.06.0--base-sha2.c-notice.txt), [ghostscript-10.06.0--base-aes.c-notice.txt](licenses/texts/ghostscript-10.06.0--base-aes.c-notice.txt), [ghostscript-10.06.0--base-gsmd5.c-notice.txt](licenses/texts/ghostscript-10.06.0--base-gsmd5.c-notice.txt), [ghostscript-10.06.0--Resource-CMap-Adobe-notice.txt](licenses/texts/ghostscript-10.06.0--Resource-CMap-Adobe-notice.txt), [Apache-2.0.txt](licenses/texts/Apache-2.0.txt), [emscripten-4.0.22--LICENSE.txt](licenses/texts/emscripten-4.0.22--LICENSE.txt), [emscripten-4.0.22--system-lib-libc-musl-COPYRIGHT.txt](licenses/texts/emscripten-4.0.22--system-lib-libc-musl-COPYRIGHT.txt), [emscripten-4.0.22--system-lib-compiler-rt-LICENSE.TXT.txt](licenses/texts/emscripten-4.0.22--system-lib-compiler-rt-LICENSE.TXT.txt)) | Copyright (C) 2001-2025 Artifex Software, Inc. All Rights Reserved.; GPL Ghostscript 10.06.0 (2025-09-09) banner: Copyright (C) 2025 Artifex Software, Inc.  All rights reserved.; @bentopdf/gs-wasm packaging (loader dist/index.js, build scripts): BentoPDF (package author; no copyright line stated) | Ghostscript: https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs10060/ghostpdl-10.06.0.tar.xz (sha512 c1b2763908fb0c4d23a116c3d67717922a9f8d95631aa27de02c5b0ba255f406c4c329a4cbc68af43408ad674007022dcc92ce364dc7306a565e70c3bf8ea2ef; same as tag ghostpdl-10.06.0 = commit 2d6e764c1f4a73520ed6de6dd3fa78ad30cd6a63 of https://github.com/ArtifexSoftware/ghostpdl); packaging: https://github.com/alam00000/bentopdf-gs-wasm/tree/v0.1.1 (commit 9eb6ab47e19ee2ff01fd73c3ee5f8bbc9e50e36e) = https://registry.npmjs.org/@bentopdf/gs-wasm/-/gs-wasm-0.1.1.tgz |
| ↳ FreeType | 2.13.3 | FTL OR GPL-2.0-or-later | Copyright (C) 1996-2024 by David Turner, Robert Wilhelm, and Werner Lemberg.; Portions of this software are copyright (C) 2024 The FreeType Project (www.freetype.org). All rights reserved. | https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs10060/ghostpdl-10.06.0.tar.xz (freetype/; upstream https://gitlab.freedesktop.org/freetype/freetype/-/tree/VER-2-13-3) |
| ↳ libjpeg (Independent JPEG Group), with Artifex patches | 9f (14-Jan-2024) | IJG | Copyright (C) 1991-2024, Thomas G. Lane, Guido Vollbeding. | https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs10060/ghostpdl-10.06.0.tar.xz (jpeg/; upstream https://www.ijg.org/files/jpegsrc.v9f.tar.gz) |
| ↳ libpng | 1.6.50 | libpng-2.0 | Copyright (c) 1995-2025 The PNG Reference Library Authors.; Copyright (c) 2018-2025 Cosmin Truta.; Copyright (c) 2000-2002, 2004, 2006-2018 Glenn Randers-Pehrson.; Copyright (c) 1996-1997 Andreas Dilger.; Copyright (c) 1995-1996 Guy Eric Schalnat, Group 42, Inc. | https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs10060/ghostpdl-10.06.0.tar.xz (libpng/; upstream https://github.com/pnggroup/libpng/tree/v1.6.50) |
| ↳ zlib | 1.3.1 | Zlib | (C) 1995-2022 Jean-loup Gailly and Mark Adler (LICENSE file); Copyright (C) 1995-2024 Jean-loup Gailly and Mark Adler (zlib.h) | https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs10060/ghostpdl-10.06.0.tar.xz (zlib/; upstream https://github.com/madler/zlib/tree/v1.3.1) |
| ↳ lcms2mt (Artifex's thread-safe fork of Little CMS 2) | 2.12 | MIT | Copyright (c) 1998-2020 Marti Maria Saguer | https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs10060/ghostpdl-10.06.0.tar.xz (lcms2mt/) |
| ↳ OpenJPEG | 2.5.3 | BSD-2-Clause | Copyright (c) 2002-2014, Universite catholique de Louvain (UCL), Belgium; Copyright (c) 2002-2014, Professor Benoit Macq; Copyright (c) 2003-2014, Antonin Descampe; Copyright (c) 2003-2009, Francois-Olivier Devaux; Copyright (c) 2005, Herve Drolon, FreeImage Team; Copyright (c) 2002-2003, Yannick Verschueren; Copyright (c) 2001-2003, David Janssens; Copyright (c) 2011-2012, Centre National d'Etudes Spatiales (CNES), France; Copyright (c) 2012, CS Systemes d'Information, France | https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs10060/ghostpdl-10.06.0.tar.xz (openjpeg/; upstream https://github.com/uclouvain/openjpeg/tree/v2.5.3) |
| ↳ jbig2dec | 0.20 | AGPL-3.0-or-later | Copyright (C) 2001-2023 Artifex Software, Inc. | https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs10060/ghostpdl-10.06.0.tar.xz (jbig2dec/; upstream https://github.com/ArtifexSoftware/jbig2dec/tree/0.20) |
| ↳ LibTIFF | 4.7.0 | libtiff | Copyright (c) 1988-1997 Sam Leffler; Copyright (c) 1991-1997 Silicon Graphics, Inc. | https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs10060/ghostpdl-10.06.0.tar.xz (tiff/; upstream https://gitlab.com/libtiff/libtiff/-/tree/v4.7.0) |
| ↳ Brotli | 1.0.9 (per c/common/version.h in the ghostpdl tree) | MIT | Copyright (c) 2009, 2010, 2013-2016 by the Brotli Authors. | https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs10060/ghostpdl-10.06.0.tar.xz (brotli/; upstream https://github.com/google/brotli) |
| ↳ SHA-2 implementation (base/sha2.c) | ghostpdl 10.06.0 copy ($Id: sha2.c,v 1.1 2001/11/08) | BSD-3-Clause | Copyright (c) 2000-2001, Aaron D. Gifford | https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs10060/ghostpdl-10.06.0.tar.xz (base/sha2.c) |
| ↳ AES implementation from XySSL (base/aes.c) | ghostpdl 10.06.0 copy | BSD-3-Clause | Copyright (C) 2006-2007  Christophe Devine | https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs10060/ghostpdl-10.06.0.tar.xz (base/aes.c) |
| ↳ MD5 implementation (base/gsmd5.c, L. Peter Deutsch) | ghostpdl 10.06.0 copy | Zlib | Copyright (C) 1999-2021 Artifex Software, Inc. | https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs10060/ghostpdl-10.06.0.tar.xz (base/gsmd5.c) |
| ↳ URW++ base 35 Type 1 fonts (35 files in %rom%Resource/Font: Nimbus Sans/Roman/Mono PS, URW Bookman, URW Gothic, C059, P052, Z003, D050000L, Standard Symbols PS) | 1.00-2.00 (as in ghostpdl 10.06.0 Resource/Font) | AGPL-3.0-or-later WITH AdditionRef-Ghostscript-font-exception | (URW)++,Copyright 2014 by (URW)++ Design & Development; (URW)++,Copyright 2013 by (URW)++ Design & Development; URW Software, Copyright 2015 by URW | https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs10060/ghostpdl-10.06.0.tar.xz (Resource/Font/; also https://github.com/ArtifexSoftware/urw-base35-fonts) |
| ↳ Droid Sans Fallback (%rom%Resource/CIDFSubst/DroidSansFallback.ttf) | 2.52a | Apache-2.0 | Digitized data copyright Google Corporation (c) 2006 | https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs10060/ghostpdl-10.06.0.tar.xz (Resource/CIDFSubst/DroidSansFallback.ttf) |
| ↳ Adobe CMap resources (180 files in %rom%Resource/CMap; Identity-UTF16-H is Artifex's) | as in ghostpdl 10.06.0 Resource/CMap | BSD-3-Clause | Copyright 1990-2015 Adobe Systems Incorporated. All rights reserved. (162 files); Copyright 1990-2017 Adobe Systems Incorporated. All rights reserved. (18 files) | https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs10060/ghostpdl-10.06.0.tar.xz (Resource/CMap/; upstream https://github.com/adobe-type-tools/cmap-resources) |
| ↳ Artifex ICC profiles (14 in %rom%iccprofiles) and PostScript resources (Resource/Init, ColorSpace, Decoding, Encoding, IdiomSet, SubstCID, CIDFont/ArtifexBullet) | ghostpdl 10.06.0 | AGPL-3.0-or-later | Copyright Artifex Software 2009-2019 (ICC 'cprt' tags); Copyright (C) 2001-2023 Artifex Software, Inc. (ArtifexBullet) | https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs10060/ghostpdl-10.06.0.tar.xz (iccprofiles/, Resource/) |
| ↳ Emscripten runtime (gs.js glue; musl libc, compiler-rt, dlmalloc linked into gs.wasm) | unknown ('Emscripten SDK (latest)', built <= 2025-12-24; 4.0.22 inferred) | (MIT OR NCSA) AND MIT AND Apache-2.0 WITH LLVM-exception AND CC0-1.0 | Copyright (c) 2010-2014 Emscripten authors, see AUTHORS file.; Copyright (c) 2005-2020 Rich Felker, et al. (musl) | https://github.com/emscripten-core/emscripten (exact version not recorded) |
| ↳ @bentopdf/gs-wasm loader (dist/index.js, compiled from src/index.ts) | 0.1.1 | AGPL-3.0-only | BentoPDF (no copyright line stated) | https://github.com/alam00000/bentopdf-gs-wasm/blob/v0.1.1/src/index.ts |
| CoherentPDF (coherentpdf.js) | 2.5.5 | AGPL-3.0-or-later ([coherentpdf-2.5.5--LICENSE.md.txt](licenses/texts/coherentpdf-2.5.5--LICENSE.md.txt), [AGPL-3.0.txt](licenses/texts/AGPL-3.0.txt), [camlpdf-git8d00a3b--LICENSE.txt](licenses/texts/camlpdf-git8d00a3b--LICENSE.txt), [cpdf-source-git8ce990f--cpdfxmlm.ml-ISC-notice.txt](licenses/texts/cpdf-source-git8ce990f--cpdfxmlm.ml-ISC-notice.txt), [cpdf-source-gitbe63d2b--cpdfyojson.ml-BSD-notice.txt](licenses/texts/cpdf-source-gitbe63d2b--cpdfyojson.ml-BSD-notice.txt), [cpdf-source-git8ce990f--LICENSE-Unicode-section.txt](licenses/texts/cpdf-source-git8ce990f--LICENSE-Unicode-section.txt), [APAFML.txt](licenses/texts/APAFML.txt), [js_of_ocaml-4.0.0--LICENSE.txt](licenses/texts/js_of_ocaml-4.0.0--LICENSE.txt), [ocaml-4.14.0--LICENSE.txt](licenses/texts/ocaml-4.14.0--LICENSE.txt), [sjcl-1.0.8--LICENSE.txt.txt](licenses/texts/sjcl-1.0.8--LICENSE.txt.txt), [Zlib.txt](licenses/texts/Zlib.txt), [asn1.js-5.4.1--LICENSE.txt](licenses/texts/asn1.js-5.4.1--LICENSE.txt), [assert-1.5.0--LICENSE.txt](licenses/texts/assert-1.5.0--LICENSE.txt), [available-typed-arrays-1.0.5--LICENSE.txt](licenses/texts/available-typed-arrays-1.0.5--LICENSE.txt), [base64-js-1.5.1--LICENSE.txt](licenses/texts/base64-js-1.5.1--LICENSE.txt), [bn.js-4.12.0--LICENSE.txt](licenses/texts/bn.js-4.12.0--LICENSE.txt), [bn.js-5.2.1--LICENSE.txt](licenses/texts/bn.js-5.2.1--LICENSE.txt), [brorand-1.1.0--README-license-section.txt](licenses/texts/brorand-1.1.0--README-license-section.txt), [browser-pack-6.1.0--LICENSE.txt](licenses/texts/browser-pack-6.1.0--LICENSE.txt), [browserify-17.0.0--LICENSE.txt](licenses/texts/browserify-17.0.0--LICENSE.txt), [browserify-aes-1.2.0--LICENSE.txt](licenses/texts/browserify-aes-1.2.0--LICENSE.txt), [browserify-cipher-1.0.1--LICENSE.txt](licenses/texts/browserify-cipher-1.0.1--LICENSE.txt), [browserify-des-1.0.2--license.txt](licenses/texts/browserify-des-1.0.2--license.txt), [browserify-rsa-4.1.0--LICENSE.txt](licenses/texts/browserify-rsa-4.1.0--LICENSE.txt), [browserify-sign-4.2.1--LICENSE.txt](licenses/texts/browserify-sign-4.2.1--LICENSE.txt), [browserify-zlib-0.2.0--LICENSE.txt](licenses/texts/browserify-zlib-0.2.0--LICENSE.txt), [buffer-5.2.1--LICENSE.txt](licenses/texts/buffer-5.2.1--LICENSE.txt), [buffer-xor-1.0.3--LICENSE.txt](licenses/texts/buffer-xor-1.0.3--LICENSE.txt), [call-bind-1.0.2--LICENSE.txt](licenses/texts/call-bind-1.0.2--LICENSE.txt), [cipher-base-1.0.4--LICENSE.txt](licenses/texts/cipher-base-1.0.4--LICENSE.txt), [constants-browserify-1.0.0--README-license-section.txt](licenses/texts/constants-browserify-1.0.0--README-license-section.txt), [create-ecdh-4.0.4--LICENSE.txt](licenses/texts/create-ecdh-4.0.4--LICENSE.txt), [create-hash-1.2.0--LICENSE.txt](licenses/texts/create-hash-1.2.0--LICENSE.txt), [create-hmac-1.1.7--LICENSE.txt](licenses/texts/create-hmac-1.1.7--LICENSE.txt), [crypto-browserify-3.12.0--LICENSE.txt](licenses/texts/crypto-browserify-3.12.0--LICENSE.txt), [des.js-1.0.1--README-license-section.txt](licenses/texts/des.js-1.0.1--README-license-section.txt), [diffie-hellman-5.0.3--LICENSE.txt](licenses/texts/diffie-hellman-5.0.3--LICENSE.txt), [elliptic-6.5.4--README-license-section.txt](licenses/texts/elliptic-6.5.4--README-license-section.txt), [es-abstract-1.20.1--LICENSE.txt](licenses/texts/es-abstract-1.20.1--LICENSE.txt), [events-3.3.0--LICENSE.txt](licenses/texts/events-3.3.0--LICENSE.txt), [evp_bytestokey-1.0.3--LICENSE.txt](licenses/texts/evp_bytestokey-1.0.3--LICENSE.txt), [foreach-2.0.6--LICENSE.txt](licenses/texts/foreach-2.0.6--LICENSE.txt), [function-bind-1.1.1--LICENSE.txt](licenses/texts/function-bind-1.1.1--LICENSE.txt), [get-intrinsic-1.1.2--LICENSE.txt](licenses/texts/get-intrinsic-1.1.2--LICENSE.txt), [has-1.0.3--LICENSE-MIT.txt](licenses/texts/has-1.0.3--LICENSE-MIT.txt), [has-symbols-1.0.3--LICENSE.txt](licenses/texts/has-symbols-1.0.3--LICENSE.txt), [has-tostringtag-1.0.0--LICENSE.txt](licenses/texts/has-tostringtag-1.0.0--LICENSE.txt), [hash-base-3.1.0--LICENSE.txt](licenses/texts/hash-base-3.1.0--LICENSE.txt), [hash.js-1.1.7--README-license-section.txt](licenses/texts/hash.js-1.1.7--README-license-section.txt), [hmac-drbg-1.0.1--README-license-section.txt](licenses/texts/hmac-drbg-1.0.1--README-license-section.txt), [ieee754-1.2.1--LICENSE.txt](licenses/texts/ieee754-1.2.1--LICENSE.txt), [inherits-2.0.1--LICENSE.txt](licenses/texts/inherits-2.0.1--LICENSE.txt), [inherits-2.0.4--LICENSE.txt](licenses/texts/inherits-2.0.4--LICENSE.txt), [is-arguments-1.1.1--LICENSE.txt](licenses/texts/is-arguments-1.1.1--LICENSE.txt), [is-generator-function-1.0.10--LICENSE.txt](licenses/texts/is-generator-function-1.0.10--LICENSE.txt), [is-typed-array-1.1.9--LICENSE.txt](licenses/texts/is-typed-array-1.1.9--LICENSE.txt), [md5.js-1.3.5--LICENSE.txt](licenses/texts/md5.js-1.3.5--LICENSE.txt), [miller-rabin-4.0.1--README-license-section.txt](licenses/texts/miller-rabin-4.0.1--README-license-section.txt), [minimalistic-assert-1.0.1--LICENSE.txt](licenses/texts/minimalistic-assert-1.0.1--LICENSE.txt), [minimalistic-crypto-utils-1.0.1--README-license-section.txt](licenses/texts/minimalistic-crypto-utils-1.0.1--README-license-section.txt), [object-assign-4.1.1--license.txt](licenses/texts/object-assign-4.1.1--license.txt), [pako-1.0.11--LICENSE.txt](licenses/texts/pako-1.0.11--LICENSE.txt), [parse-asn1-5.1.6--LICENSE.txt](licenses/texts/parse-asn1-5.1.6--LICENSE.txt), [pbkdf2-3.1.2--LICENSE.txt](licenses/texts/pbkdf2-3.1.2--LICENSE.txt), [process-0.11.10--LICENSE.txt](licenses/texts/process-0.11.10--LICENSE.txt), [public-encrypt-4.0.3--LICENSE.txt](licenses/texts/public-encrypt-4.0.3--LICENSE.txt), [randombytes-2.1.0--LICENSE.txt](licenses/texts/randombytes-2.1.0--LICENSE.txt), [randomfill-1.0.4--LICENSE.txt](licenses/texts/randomfill-1.0.4--LICENSE.txt), [readable-stream-3.6.0--LICENSE.txt](licenses/texts/readable-stream-3.6.0--LICENSE.txt), [ripemd160-2.0.2--LICENSE.txt](licenses/texts/ripemd160-2.0.2--LICENSE.txt), [safe-buffer-5.2.1--LICENSE.txt](licenses/texts/safe-buffer-5.2.1--LICENSE.txt), [safer-buffer-2.1.2--LICENSE.txt](licenses/texts/safer-buffer-2.1.2--LICENSE.txt), [sha.js-2.4.11--LICENSE.txt](licenses/texts/sha.js-2.4.11--LICENSE.txt), [stream-browserify-3.0.0--LICENSE.txt](licenses/texts/stream-browserify-3.0.0--LICENSE.txt), [string_decoder-1.3.0--LICENSE.txt](licenses/texts/string_decoder-1.3.0--LICENSE.txt), [util-0.10.3--LICENSE.txt](licenses/texts/util-0.10.3--LICENSE.txt), [util-0.12.4--LICENSE.txt](licenses/texts/util-0.12.4--LICENSE.txt), [util-deprecate-1.0.2--LICENSE.txt](licenses/texts/util-deprecate-1.0.2--LICENSE.txt), [which-typed-array-1.1.8--LICENSE.txt](licenses/texts/which-typed-array-1.1.8--LICENSE.txt)) | Copyright Coherent Graphics Ltd 2007 - 2022 (CamlPDF/CPDF; package author 'Coherent Graphics Ltd') | https://github.com/coherentgraphics/coherentpdf.js/tree/v2.5.5 (commit 51dbad27345a31d7e5825638b5bdc2be4407fa16 = npm gitHead; https://registry.npmjs.org/coherentpdf/-/coherentpdf-2.5.5.tgz) plus the OCaml sources it compiles, whose exact revisions are not recorded: camlpdf 8d00a3b642e82e778c3b5631dd238ec46d78daf6, cpdf-source 8ce990f715ed20fabc9abac2ba469cf9265dea9e, cpdflib-source 3828968d0bc295709b86ee8b7c55b4600b037e97 (inferred: last commits before the 2022-08-18 npm publish) |
| ↳ CPDF (cpdf-source: Coherent PDF Command Line Tools as an OCaml library) | 2.5.x snapshot of Aug 2022 (git 8ce990f inferred) | AGPL-3.0-or-later (as distributed in coherentpdf.js dist/; the 2022 source repo carried the Coherent Graphics Non-Commercial licence, relicensed AGPL-3.0 in July 2024) | Copyright Coherent Graphics Ltd 2022. | https://github.com/johnwhitington/cpdf-source/tree/8ce990f715ed20fabc9abac2ba469cf9265dea9e (inferred: last commit before 2022-08-18) |
| ↳ cpdflib (cpdflib-source, compiled as module Cpdf; version string '2.5.5') | 2.5.5 (uncommitted working copy; nearest commit 3828968 of 2022-07-14 says '2.5.2') | AGPL-3.0-or-later (as distributed in coherentpdf.js dist/; repo then under the Coherent Graphics Non-Commercial licence, AGPL-3.0 since July 2024) | Copyright Coherent Graphics Ltd | https://github.com/johnwhitington/cpdflib-source/tree/3828968d0bc295709b86ee8b7c55b4600b037e97 (inferred) |
| ↳ CamlPDF | 2.5.x snapshot of Aug 2022 (git 8d00a3b inferred; tags v2.5.1 2022-01, v2.5.3 later) | LGPL-2.1-or-later WITH OCaml-LGPL-linking-exception | Copyright Coherent Graphics Ltd 2007 - 2022. | https://github.com/johnwhitington/camlpdf/tree/8d00a3b642e82e778c3b5631dd238ec46d78daf6 (inferred) |
| ↳ Xmlm (as cpdf-source/cpdfxmlm.ml) | unknown (%%VERSION%% placeholder) | ISC | Copyright (c) 2007 Daniel C. Bünzli | https://github.com/johnwhitington/cpdf-source/blob/8ce990f715ed20fabc9abac2ba469cf9265dea9e/cpdfxmlm.ml |
| ↳ Yojson (as cpdf-source/cpdfyojson.ml) | unknown (%%VERSION%% placeholder) | BSD-3-Clause | Copyright (c) 2010-2012, Martin Jambon All rights reserved. | https://github.com/johnwhitington/cpdf-source/blob/8ce990f715ed20fabc9abac2ba469cf9265dea9e/cpdfyojson.ml (licence header only added in commit be63d2b, 2024-08-02) |
| ↳ Unicode Character Database UnicodeData.txt (as cpdf-source/cpdfunicodedata.ml) | unknown | Unicode-DFS-2015 | Copyright (c) 1991-2015 Unicode, Inc. All rights reserved. | https://github.com/johnwhitington/cpdf-source/blob/8ce990f715ed20fabc9abac2ba469cf9265dea9e/LICENSE |
| ↳ Adobe Core 14 AFM font metrics (CamlPDF pdfafmdata) | AFM 4.1 files of 1997 | APAFML | Copyright (c) 1985, 1987, 1989, 1990, 1997 Adobe Systems Incorporated. All Rights Reserved. | https://github.com/johnwhitington/camlpdf/tree/8d00a3b642e82e778c3b5631dd238ec46d78daf6/compressor |
| ↳ Adobe Glyph List (CamlPDF pdfglyphlist) | 2.0 (September 20, 2002) | LicenseRef-Adobe-Glyph-List (no licence text in the 2002 file; Adobe later published the AGL under BSD-3-Clause) | Adobe Systems Incorporated | https://github.com/johnwhitington/camlpdf/blob/8d00a3b642e82e778c3b5631dd238ec46d78daf6/compressor/glyphlist.txt |
| ↳ OCaml standard library and unix library (compiled to JS) | unknown (js_of_ocaml 4.0.0 supports OCaml 4.04-4.14; 4.14.0 LICENSE used as reference) | LGPL-2.1-only WITH OCaml-LGPL-linking-exception | Copyright Institut National de Recherche en Informatique et en Automatique (INRIA) | https://github.com/ocaml/ocaml (version not recorded) |
| ↳ js_of_ocaml runtime and library | 4.0.0 | LGPL-2.1-or-later WITH OCaml-LGPL-linking-exception | Copyright (C) 2010 Jérôme Vouillon, Laboratoire PPS - CNRS Université Paris Diderot; Copyright CNRS Université Paris Diderot | https://github.com/ocsigen/js_of_ocaml/tree/4.0.0 |
| ↳ SJCL - Stanford JavaScript Crypto Library (custom minified build: AES, SHA-256/512, codecs; coherentpdf.js sjcl.js, browserified into the browser builds) | unknown (1.0.8 LICENSE used) | BSD-2-Clause | Copyright (c) 2009-2015, Emily Stark, Mike Hamburg and Dan Boneh at Stanford University. All rights reserved. | https://github.com/coherentgraphics/coherentpdf.js/tree/v2.5.5/sjcl.js; upstream https://github.com/bitwiseshiftleft/sjcl |
| ↳ coherentpdf.js bindings (exports.ml, cpdfzlib.js, cpdfcrypt.js, nodestubs.js) | 2.5.5 | AGPL-3.0-or-later | Coherent Graphics Ltd | https://github.com/coherentgraphics/coherentpdf.js/tree/v2.5.5 |
| ↳ asn1.js | 5.4.1 (inferred) | MIT | Copyright (c) 2017 Fedor Indutny | https://registry.npmjs.org/asn1.js/-/asn1.js-5.4.1.tgz |
| ↳ assert | 1.5.0 (inferred) | MIT | Copyright Joyent, Inc. and other Node contributors. All rights reserved. | https://registry.npmjs.org/assert/-/assert-1.5.0.tgz |
| ↳ available-typed-arrays | 1.0.5 (inferred) | MIT | Copyright (c) 2020 Inspect JS | https://registry.npmjs.org/available-typed-arrays/-/available-typed-arrays-1.0.5.tgz |
| ↳ base64-js | 1.5.1 (inferred) | MIT | Copyright (c) 2014 Jameson Little | https://registry.npmjs.org/base64-js/-/base64-js-1.5.1.tgz |
| ↳ bn.js | 4.12.0 (inferred) | MIT | Copyright Fedor Indutny, 2015. | https://registry.npmjs.org/bn.js/-/bn.js-4.12.0.tgz |
| ↳ bn.js | 5.2.1 (inferred) | MIT | Copyright Fedor Indutny, 2015. | https://registry.npmjs.org/bn.js/-/bn.js-5.2.1.tgz |
| ↳ brorand | 1.1.0 (inferred) | MIT | Copyright Fedor Indutny, 2014. | https://registry.npmjs.org/brorand/-/brorand-1.1.0.tgz |
| ↳ browserify-aes | 1.2.0 (inferred) | MIT | Copyright (c) 2014-2017 browserify-aes contributors | https://registry.npmjs.org/browserify-aes/-/browserify-aes-1.2.0.tgz |
| ↳ browserify-cipher | 1.0.1 (inferred) | MIT | Copyright (c) 2014-2017 Calvin Metcalf & contributors | https://registry.npmjs.org/browserify-cipher/-/browserify-cipher-1.0.1.tgz |
| ↳ browserify-des | 1.0.2 (inferred) | MIT | Copyright (c) 2014-2017 Calvin Metcalf, Fedor Indutny & contributors | https://registry.npmjs.org/browserify-des/-/browserify-des-1.0.2.tgz |
| ↳ browserify-rsa | 4.1.0 (inferred) | MIT | Copyright (c) 2014-2016 Calvin Metcalf & contributors | https://registry.npmjs.org/browserify-rsa/-/browserify-rsa-4.1.0.tgz |
| ↳ browserify-sign | 4.2.1 (inferred) | ISC | Copyright (c) 2014-2015 Calvin Metcalf and browserify-sign contributors | https://registry.npmjs.org/browserify-sign/-/browserify-sign-4.2.1.tgz |
| ↳ browserify-zlib | 0.2.0 (inferred) | MIT | Copyright (c) 2014-2015 Devon Govett <devongovett@gmail.com>; Copyright Node.js contributors. All rights reserved.; Copyright Joyent, Inc. and other Node contributors. All rights reserved. | https://registry.npmjs.org/browserify-zlib/-/browserify-zlib-0.2.0.tgz |
| ↳ buffer | 5.2.1 (inferred) | MIT | Copyright (c) Feross Aboukhadijeh, and other contributors. | https://registry.npmjs.org/buffer/-/buffer-5.2.1.tgz |
| ↳ buffer-xor | 1.0.3 (inferred) | MIT | Copyright (c) 2015 Daniel Cousens | https://registry.npmjs.org/buffer-xor/-/buffer-xor-1.0.3.tgz |
| ↳ call-bind | 1.0.2 (inferred) | MIT | Copyright (c) 2020 Jordan Harband | https://registry.npmjs.org/call-bind/-/call-bind-1.0.2.tgz |
| ↳ cipher-base | 1.0.4 (inferred) | MIT | Copyright (c) 2017 crypto-browserify contributors | https://registry.npmjs.org/cipher-base/-/cipher-base-1.0.4.tgz |
| ↳ constants-browserify | 1.0.0 (inferred) | MIT | Copyright (c) 2013 Julian Gruber <julian@juliangruber.com> | https://registry.npmjs.org/constants-browserify/-/constants-browserify-1.0.0.tgz |
| ↳ create-ecdh | 4.0.4 (inferred) | MIT | Copyright (c) 2014-2017 createECDH contributors | https://registry.npmjs.org/create-ecdh/-/create-ecdh-4.0.4.tgz |
| ↳ create-hash | 1.2.0 (inferred) | MIT | Copyright (c) 2017 crypto-browserify contributors | https://registry.npmjs.org/create-hash/-/create-hash-1.2.0.tgz |
| ↳ create-hmac | 1.1.7 (inferred) | MIT | Copyright (c) 2017 crypto-browserify contributors | https://registry.npmjs.org/create-hmac/-/create-hmac-1.1.7.tgz |
| ↳ crypto-browserify | 3.12.0 (inferred) | MIT | Copyright (c) 2013 Dominic Tarr | https://registry.npmjs.org/crypto-browserify/-/crypto-browserify-3.12.0.tgz |
| ↳ des.js | 1.0.1 (inferred) | MIT | Copyright Fedor Indutny, 2015. | https://registry.npmjs.org/des.js/-/des.js-1.0.1.tgz |
| ↳ diffie-hellman | 5.0.3 (inferred) | MIT | Copyright (c) 2017 Calvin Metcalf | https://registry.npmjs.org/diffie-hellman/-/diffie-hellman-5.0.3.tgz |
| ↳ elliptic | 6.5.4 | MIT | Copyright Fedor Indutny, 2014. | https://registry.npmjs.org/elliptic/-/elliptic-6.5.4.tgz |
| ↳ es-abstract | 1.20.1 (inferred) | MIT | Copyright (C) 2015 Jordan Harband | https://registry.npmjs.org/es-abstract/-/es-abstract-1.20.1.tgz |
| ↳ events | 3.3.0 (inferred) | MIT | Copyright Joyent, Inc. and other Node contributors. | https://registry.npmjs.org/events/-/events-3.3.0.tgz |
| ↳ evp_bytestokey | 1.0.3 (inferred) | MIT | Copyright (c) 2017 crypto-browserify contributors | https://registry.npmjs.org/evp_bytestokey/-/evp_bytestokey-1.0.3.tgz |
| ↳ function-bind | 1.1.1 (inferred) | MIT | Copyright (c) 2013 Raynos. | https://registry.npmjs.org/function-bind/-/function-bind-1.1.1.tgz |
| ↳ get-intrinsic | 1.1.2 (inferred) | MIT | Copyright (c) 2020 Jordan Harband | https://registry.npmjs.org/get-intrinsic/-/get-intrinsic-1.1.2.tgz |
| ↳ has | 1.0.3 (inferred) | MIT | Copyright (c) 2013 Thiago de Arruda | https://registry.npmjs.org/has/-/has-1.0.3.tgz |
| ↳ has-symbols | 1.0.3 (inferred) | MIT | Copyright (c) 2016 Jordan Harband | https://registry.npmjs.org/has-symbols/-/has-symbols-1.0.3.tgz |
| ↳ has-tostringtag | 1.0.0 (inferred) | MIT | Copyright (c) 2021 Inspect JS | https://registry.npmjs.org/has-tostringtag/-/has-tostringtag-1.0.0.tgz |
| ↳ hash-base | 3.1.0 (inferred) | MIT | Copyright (c) 2016 Kirill Fomichev | https://registry.npmjs.org/hash-base/-/hash-base-3.1.0.tgz |
| ↳ hash.js | 1.1.7 (inferred) | MIT | Copyright Fedor Indutny, 2014. | https://registry.npmjs.org/hash.js/-/hash.js-1.1.7.tgz |
| ↳ hmac-drbg | 1.0.1 (inferred) | MIT | Copyright Fedor Indutny, 2017. | https://registry.npmjs.org/hmac-drbg/-/hmac-drbg-1.0.1.tgz |
| ↳ ieee754 | 1.2.1 (inferred) | BSD-3-Clause | Copyright 2008 Fair Oaks Labs, Inc. | https://registry.npmjs.org/ieee754/-/ieee754-1.2.1.tgz |
| ↳ inherits | 2.0.1 (inferred) | ISC | Copyright (c) Isaac Z. Schlueter | https://registry.npmjs.org/inherits/-/inherits-2.0.1.tgz |
| ↳ inherits | 2.0.4 (inferred) | ISC | Copyright (c) Isaac Z. Schlueter | https://registry.npmjs.org/inherits/-/inherits-2.0.4.tgz |
| ↳ is-arguments | 1.1.1 (inferred) | MIT | Copyright (c) 2014 Jordan Harband | https://registry.npmjs.org/is-arguments/-/is-arguments-1.1.1.tgz |
| ↳ is-generator-function | 1.0.10 (inferred) | MIT | Copyright (c) 2014 Jordan Harband | https://registry.npmjs.org/is-generator-function/-/is-generator-function-1.0.10.tgz |
| ↳ is-typed-array | 1.1.9 (inferred) | MIT | Copyright (c) 2015 Jordan Harband | https://registry.npmjs.org/is-typed-array/-/is-typed-array-1.1.9.tgz |
| ↳ md5.js | 1.3.5 (inferred) | MIT | Copyright (c) 2016 Kirill Fomichev | https://registry.npmjs.org/md5.js/-/md5.js-1.3.5.tgz |
| ↳ miller-rabin | 4.0.1 (inferred) | MIT | Copyright Fedor Indutny, 2014. | https://registry.npmjs.org/miller-rabin/-/miller-rabin-4.0.1.tgz |
| ↳ minimalistic-assert | 1.0.1 (inferred) | ISC | Copyright 2015 Calvin Metcalf | https://registry.npmjs.org/minimalistic-assert/-/minimalistic-assert-1.0.1.tgz |
| ↳ minimalistic-crypto-utils | 1.0.1 (inferred) | MIT | Copyright Fedor Indutny, 2017. | https://registry.npmjs.org/minimalistic-crypto-utils/-/minimalistic-crypto-utils-1.0.1.tgz |
| ↳ object-assign | 4.1.1 (inferred) | MIT | Copyright (c) Sindre Sorhus <sindresorhus@gmail.com> (sindresorhus.com) | https://registry.npmjs.org/object-assign/-/object-assign-4.1.1.tgz |
| ↳ pako | 1.0.11 (inferred) | (MIT AND Zlib) | Copyright (C) 2014-2017 by Vitaly Puzrin and Andrei Tuputcyn | https://registry.npmjs.org/pako/-/pako-1.0.11.tgz |
| ↳ parse-asn1 | 5.1.6 (inferred) | ISC | Copyright (c) 2017, crypto-browserify contributors | https://registry.npmjs.org/parse-asn1/-/parse-asn1-5.1.6.tgz |
| ↳ pbkdf2 | 3.1.2 (inferred) | MIT | Copyright (c) 2014 Daniel Cousens | https://registry.npmjs.org/pbkdf2/-/pbkdf2-3.1.2.tgz |
| ↳ process | 0.11.10 (inferred) | MIT | Copyright (c) 2013 Roman Shtylman <shtylman@gmail.com> | https://registry.npmjs.org/process/-/process-0.11.10.tgz |
| ↳ public-encrypt | 4.0.3 (inferred) | MIT | Copyright (c) 2017 Calvin Metcalf | https://registry.npmjs.org/public-encrypt/-/public-encrypt-4.0.3.tgz |
| ↳ randombytes | 2.1.0 (inferred) | MIT | Copyright (c) 2017 crypto-browserify | https://registry.npmjs.org/randombytes/-/randombytes-2.1.0.tgz |
| ↳ randomfill | 1.0.4 (inferred) | MIT | Copyright (c) 2017 crypto-browserify | https://registry.npmjs.org/randomfill/-/randomfill-1.0.4.tgz |
| ↳ readable-stream | 3.6.0 (inferred) | MIT | Copyright Node.js contributors. All rights reserved.; Copyright Joyent, Inc. and other Node contributors. All rights reserved. | https://registry.npmjs.org/readable-stream/-/readable-stream-3.6.0.tgz |
| ↳ ripemd160 | 2.0.2 (inferred) | MIT | Copyright (c) 2016 crypto-browserify | https://registry.npmjs.org/ripemd160/-/ripemd160-2.0.2.tgz |
| ↳ safe-buffer | 5.2.1 (inferred) | MIT | Copyright (c) Feross Aboukhadijeh | https://registry.npmjs.org/safe-buffer/-/safe-buffer-5.2.1.tgz |
| ↳ safer-buffer | 2.1.2 (inferred) | MIT | Copyright (c) 2018 Nikita Skovoroda <chalkerx@gmail.com> | https://registry.npmjs.org/safer-buffer/-/safer-buffer-2.1.2.tgz |
| ↳ sha.js | 2.4.11 (inferred) | (MIT AND BSD-3-Clause) | Copyright (c) 2013-2018 sha.js contributors; Copyright (c) 1998 - 2009, Paul Johnston & Contributors | https://registry.npmjs.org/sha.js/-/sha.js-2.4.11.tgz |
| ↳ stream-browserify | 3.0.0 (inferred) | MIT | Copyright (c) James Halliday | https://registry.npmjs.org/stream-browserify/-/stream-browserify-3.0.0.tgz |
| ↳ string_decoder | 1.3.0 (inferred) | MIT | Copyright Node.js contributors. All rights reserved.; Copyright Joyent, Inc. and other Node contributors. All rights reserved. | https://registry.npmjs.org/string_decoder/-/string_decoder-1.3.0.tgz |
| ↳ util | 0.10.3 (inferred) | MIT | Copyright Joyent, Inc. and other Node contributors. All rights reserved. | https://registry.npmjs.org/util/-/util-0.10.3.tgz |
| ↳ util | 0.12.4 (inferred) | MIT | Copyright Joyent, Inc. and other Node contributors. All rights reserved. | https://registry.npmjs.org/util/-/util-0.12.4.tgz |
| ↳ util-deprecate | 1.0.2 (inferred) | MIT | Copyright (c) 2014 Nathan Rajlich <nathan@tootallnate.net> | https://registry.npmjs.org/util-deprecate/-/util-deprecate-1.0.2.tgz |
| ↳ which-typed-array | 1.1.8 (inferred) | MIT | Copyright (c) 2015 Jordan Harband | https://registry.npmjs.org/which-typed-array/-/which-typed-array-1.1.8.tgz |
| ↳ foreach | 2.0.6 (inferred) | MIT | Copyright (c) 2013 Manuel Stofer | https://registry.npmjs.org/foreach/-/foreach-2.0.6.tgz |
| ↳ browser-pack (browserify prelude / empty module stub) | 6.1.0 (inferred) | MIT | Copyright (c) James Halliday (package author; LICENSE file carries no copyright line) | https://registry.npmjs.org/browser-pack/-/browser-pack-6.1.0.tgz |
| ↳ browserify (browserify (builtin shims, _empty.js for fs)) | 17.0.0 (inferred) | MIT | Copyright (c) 2010 James Halliday | https://registry.npmjs.org/browserify/-/browserify-17.0.0.tgz |
| tesseract.js-core (Tesseract and Leptonica) | 7.0.0 | Apache-2.0 ([tesseract.js-core-7.0.0--LICENSE.txt](licenses/texts/tesseract.js-core-7.0.0--LICENSE.txt), [Apache-2.0.txt](licenses/texts/Apache-2.0.txt), [leptonica-1.83.0-git4af068b--leptonica-license.txt](licenses/texts/leptonica-1.83.0-git4af068b--leptonica-license.txt), [libjpeg-9a--README.txt](licenses/texts/libjpeg-9a--README.txt), [giflib-5.1.4--COPYING.txt](licenses/texts/giflib-5.1.4--COPYING.txt), [giflib-5.1.4--openbsd-reallocarray.c-header.txt](licenses/texts/giflib-5.1.4--openbsd-reallocarray.c-header.txt), [libpng-1.6.38.git-a37d483--LICENSE.txt](licenses/texts/libpng-1.6.38.git-a37d483--LICENSE.txt), [libtiff-4.3.0-gitb51bb15--COPYRIGHT.txt](licenses/texts/libtiff-4.3.0-gitb51bb15--COPYRIGHT.txt), [libtiff-4.3.0-gitb51bb15--tif_luv.c-header.txt](licenses/texts/libtiff-4.3.0-gitb51bb15--tif_luv.c-header.txt), [libwebp-1.2.2-git20ef03e--COPYING.txt](licenses/texts/libwebp-1.2.2-git20ef03e--COPYING.txt), [libwebp-1.2.2-git20ef03e--PATENTS.txt](licenses/texts/libwebp-1.2.2-git20ef03e--PATENTS.txt), [openlibm-0.8.0-gitae2d916--LICENSE.md.txt](licenses/texts/openlibm-0.8.0-gitae2d916--LICENSE.md.txt), [zlib-1.2.12--README.txt](licenses/texts/zlib-1.2.12--README.txt), [emscripten-4.0.15--LICENSE.txt](licenses/texts/emscripten-4.0.15--LICENSE.txt), [emscripten-4.0.15--musl-COPYRIGHT.txt](licenses/texts/emscripten-4.0.15--musl-COPYRIGHT.txt), [emscripten-4.0.15--libcxx-LICENSE.TXT.txt](licenses/texts/emscripten-4.0.15--libcxx-LICENSE.TXT.txt)) | No copyright line stated in the package (LICENSE is the unfilled Apache-2.0 text); author per package.json: antimatter15, contributor jeromewu | https://github.com/naptha/tesseract.js-core/tree/v7.0.0 (tag object 3128cf5bc831d61f0664903db766406f1eb3b81c -> commit acffef2b66eb44a31df297e11d905f4b39001068) with its git submodules third_party/* at the pinned commits listed under includes; npm tarball https://registry.npmjs.org/tesseract.js-core/-/tesseract.js-core-7.0.0.tgz |
| ↳ Tesseract OCR engine (tesseract.js fork github.com/Balearica/tesseract) | 5.3.0 per the VERSION file: upstream tesseract-ocr/tesseract main through fa4d4449c50a (2 commits short of 5.3.1) plus 31 tesseract.js commits, fork commit 2a9c1c49c360462733c386d2a44fcd22c4e21411; the binaries report '5.1.0-288-g2a9c1' (git describe in the fork) | Apache-2.0 | (C) Copyright 1987-1996, Hewlett-Packard Ltd. / Hewlett-Packard Company (per-file headers); (C) Copyright 2006-2020, Google Inc. (per-file headers); Includes tessdata/pdf.ttf (GlyphLessFont, part of Tesseract), embedded with --embed-file | https://github.com/Balearica/tesseract/tree/2a9c1c49c360462733c386d2a44fcd22c4e21411 |
| ↳ Leptonica | 1.83.0 development snapshot (commit 4af068b56a9674da915debea4ed7e1b9885b17e8, 2022-03-10; built without OpenJPEG, HAVE_LIBJP2K=0) | BSD-2-Clause | Copyright (C) 2001-2020 Leptonica.  All rights reserved. | https://github.com/DanBloomberg/leptonica/tree/4af068b56a9674da915debea4ed7e1b9885b17e8 |
| ↳ libjpeg (Independent JPEG Group), via the LuaDist mirror | 9a (19-Jan-2014), mirror commit 6c0fcb8ddee365e7abc4d332662b06900612e923 | IJG | Copyright (C) 1991-2014, Thomas G. Lane, Guido Vollbeding | https://github.com/LuaDist/libjpeg/tree/6c0fcb8ddee365e7abc4d332662b06900612e923 (IJG jpegsrc.v9a) |
| ↳ giflib | 5.1.4 (mirror commit fa37672085ce4b3d62c51627ab3c8cf2dda8009a) | MIT AND ISC | Copyright (c) 1997  Eric S. Raymond; Copyright (c) 2008 Otto Moerbeek <otto@drijf.net> (lib/openbsd-reallocarray.c, ISC) | https://github.com/mirrorer/giflib/tree/fa37672085ce4b3d62c51627ab3c8cf2dda8009a (giflib 5.1.4) |
| ↳ libpng | 1.6.38.git development snapshot (commit a37d4836519517bdce6cb9d956092321eca3e73b, 2021-03-13) | libpng-2.0 | Copyright (c) 1995-2020 The PNG Reference Library Authors.; Copyright (c) 2018-2020 Cosmin Truta.; Copyright (c) 2000-2002, 2004, 2006-2018 Glenn Randers-Pehrson.; Copyright (c) 1996-1997 Andreas Dilger.; Copyright (c) 1995-1996 Guy Eric Schalnat, Group 42, Inc. | https://github.com/glennrp/libpng/tree/a37d4836519517bdce6cb9d956092321eca3e73b |
| ↳ libtiff (libtiff and libtiffxx) | 4.3.0 plus development commits (commit b51bb157123264e26d34c09cc673d213aea61fc7, 2022-03-21) | libtiff | Copyright (c) 1988-1997 Sam Leffler; Copyright (c) 1991-1997 Silicon Graphics, Inc.; Copyright (c) 1997 Greg Ward Larson (tif_luv.c, SGILog codec, compiled in) | https://gitlab.com/libtiff/libtiff/-/tree/b51bb157123264e26d34c09cc673d213aea61fc7 |
| ↳ libwebp (libwebp, libwebpdecoder, libwebpdemux) | 1.2.2 plus development commits (commit 20ef03ee351d4ff03fc5ff3ec4804a879d1b9d5c, 2022-04-07) | BSD-3-Clause | Copyright (c) 2010, Google Inc. All rights reserved.; Additional IP Rights Grant (Patents) in PATENTS | https://github.com/webmproject/libwebp/tree/20ef03ee351d4ff03fc5ff3ec4804a879d1b9d5c |
| ↳ OpenLibm | 0.8.0 plus development commits (commit ae2d91698508701c83cab83714d42a1146dccf85, 2022-01-19) | MIT AND ISC AND BSD-2-Clause AND SunPro | Copyright (c) 2011-14 The Julia Project.; Copyright (c) 2008 Stephen L. Moshier <steve@moshier.net>; Copyright 1992-2011 The FreeBSD Project. All rights reserved.; Copyright (C) 1993 by Sun Microsystems, Inc. All rights reserved. | https://github.com/JuliaMath/openlibm/tree/ae2d91698508701c83cab83714d42a1146dccf85 |
| ↳ zlib | 1.2.12 (commit 21767c654d31d2dccdde4330529775c6c5fd5389) | Zlib | (C) 1995-2022 Jean-loup Gailly and Mark Adler | https://github.com/madler/zlib/tree/21767c654d31d2dccdde4330529775c6c5fd5389 (tag v1.2.12) |
| ↳ Emscripten runtime (generated JS glue, musl-based libc, malloc) | 4.0.15 (per build-with-docker.sh; not verifiable from the stripped binaries) | (MIT OR NCSA) AND MIT | Copyright (c) 2010-2014 Emscripten authors, see AUTHORS file.; Copyright © 2005-2020 Rich Felker, et al. (musl) | https://github.com/emscripten-core/emscripten/tree/4.0.15 |
| ↳ LLVM libc++ / libc++abi / compiler-rt (as shipped in Emscripten) | as in Emscripten 4.0.15 | Apache-2.0 WITH LLVM-exception | LLVM Project contributors (the LLVM exception waives attribution for portions embedded in object code) | https://github.com/emscripten-core/emscripten/tree/4.0.15/system/lib |
| PDF.js | 5.5.207 | Apache-2.0 ([pdfjs-dist-5.5.207--LICENSE.txt](licenses/texts/pdfjs-dist-5.5.207--LICENSE.txt), [MPL-2.0.txt](licenses/texts/MPL-2.0.txt)) | Copyright 2024 Mozilla Foundation (license header of build/pdf.mjs and build/pdf.worker.min.mjs; pdfjsBuild 527964698); Copyright 2014 Mozilla Foundation (web/pdf_viewer.css) | https://github.com/mozilla/pdf.js/tree/5279646985f4744386a9fe3cf61b28bf1ff88d6e (tag v5.5.207); npm tarball https://registry.npmjs.org/pdfjs-dist/-/pdfjs-dist-5.5.207.tgz |
| PDFium with EmbedPDF (bentopdf-pdfium) | 8ff5002c6cd5 | AGPL-3.0-only ([AGPL-3.0.txt](licenses/texts/AGPL-3.0.txt), [bentopdf-pdfium-viewer-8ff5002c6cd5--NOTICE.txt](licenses/texts/bentopdf-pdfium-viewer-8ff5002c6cd5--NOTICE.txt), [embedpdf-2.9.1--LICENSE.txt](licenses/texts/embedpdf-2.9.1--LICENSE.txt), [embedpdf-pdfium-2.9.1--LICENSE.txt](licenses/texts/embedpdf-pdfium-2.9.1--LICENSE.txt), [embedpdf-runtime-fce2b000cc7a--LICENSE.txt](licenses/texts/embedpdf-runtime-fce2b000cc7a--LICENSE.txt), [embedpdf-runtime-fce2b000cc7a--NOTICE.txt](licenses/texts/embedpdf-runtime-fce2b000cc7a--NOTICE.txt), [Apache-2.0.txt](licenses/texts/Apache-2.0.txt), [harfbuzz-11.0.0--COPYING.txt](licenses/texts/harfbuzz-11.0.0--COPYING.txt), [harfbuzz-11.0.0--src-ms-use-COPYING.txt](licenses/texts/harfbuzz-11.0.0--src-ms-use-COPYING.txt), [freetype-2.14.1-38-gb91f75bd--LICENSE.TXT.txt](licenses/texts/freetype-2.14.1-38-gb91f75bd--LICENSE.TXT.txt), [freetype-2.14.1-38-gb91f75bd--FTL.TXT.txt](licenses/texts/freetype-2.14.1-38-gb91f75bd--FTL.TXT.txt), [libjpeg-turbo-3.1.0--LICENSE.md.txt](licenses/texts/libjpeg-turbo-3.1.0--LICENSE.md.txt), [libjpeg-turbo-3.1.0--README.ijg.txt](licenses/texts/libjpeg-turbo-3.1.0--README.ijg.txt), [libpng-1.6.43--LICENSE.txt](licenses/texts/libpng-1.6.43--LICENSE.txt), [zlib-1.3.1--LICENSE.txt](licenses/texts/zlib-1.3.1--LICENSE.txt), [brotli-9801a2c5--LICENSE.txt](licenses/texts/brotli-9801a2c5--LICENSE.txt), [icu-77.1--LICENSE.txt](licenses/texts/icu-77.1--LICENSE.txt), [lcms2-2.15--LICENSE.txt](licenses/texts/lcms2-2.15--LICENSE.txt), [openjpeg-2.5.4--LICENSE.txt](licenses/texts/openjpeg-2.5.4--LICENSE.txt), [agg-2.3--copying.txt](licenses/texts/agg-2.3--copying.txt), [fast_float-7.0.0--LICENSE-MIT.txt](licenses/texts/fast_float-7.0.0--LICENSE-MIT.txt), [skia-c497e689--LICENSE.txt](licenses/texts/skia-c497e689--LICENSE.txt), [emscripten-3.1.70--LICENSE.txt](licenses/texts/emscripten-3.1.70--LICENSE.txt), [emscripten-3.1.70--musl-COPYRIGHT.txt](licenses/texts/emscripten-3.1.70--musl-COPYRIGHT.txt), [emscripten-3.1.70--libcxx-LICENSE.TXT.txt](licenses/texts/emscripten-3.1.70--libcxx-LICENSE.TXT.txt)) | Copyright 2026 BentoPDF; Copyright (c) 2025 CloudPDF; Copyright (c) 2024 CloudPDF, Ji Chang; Copyright 2025-2026 CloudPDF LTD; Copyright 2014 The PDFium Authors; Original code copyright 2014 Foxit Software Inc. http://www.foxitsoftware.com | https://github.com/alam00000/bentopdf-pdfium-viewer/tree/3ec97c1ea26601703353fbc3f390cc2a54f983bc/packages/pdfium (engine source the CI build used; the binary was committed by CI as packages/pdfium/src/vendor/pdfium.{js,wasm} in f48637921bf4 and is unchanged at 8ff5002c6cd5532f6fd2dffeeb43c56887dad5f8) + PDFium fork submodule https://github.com/embedpdf/runtime/tree/fce2b000cc7a9e2cabc92db41cd57ca03233f07d (packages/pdfium/pdfium-src, from https://github.com/embedpdf/pdfium.git, now embedpdf/runtime) with the third-party revisions pinned in its DEPS |
| ↳ BentoPDF EditCore (ec_* text-editing engine; packages/pdfium/build/code/editcore) | 0.2.0 (string 'EditCore 0.2.0' in the wasm) | AGPL-3.0-only | Copyright 2026 BentoPDF | https://github.com/alam00000/bentopdf-pdfium-viewer/tree/3ec97c1ea26601703353fbc3f390cc2a54f983bc/packages/pdfium/build/code/editcore |
| ↳ EmbedPDF @embedpdf/pdfium build glue and PDFiumExt_* C++ extension (packages/pdfium/build/code/cpp, generated JS glue/exports), modified by BentoPDF | 2.9.1 base (fork of embedpdf/embed-pdf-viewer v2.9.1, aa45d6ef07aa) | MIT | Copyright (c) 2024 CloudPDF, Ji Chang | https://github.com/alam00000/bentopdf-pdfium-viewer/tree/3ec97c1ea26601703353fbc3f390cc2a54f983bc/packages/pdfium/build/code/cpp |
| ↳ EmbedPDF Runtime additions to PDFium (EPDF_* APIs: fpdfsdk/epdf_*.cpp, public/epdf_*.h, png/jpeg shims, redaction) | embedpdf/runtime@fce2b000cc7a (2026-08-16) | Apache-2.0 | Copyright 2025-2026 CloudPDF LTD | https://github.com/embedpdf/runtime/tree/fce2b000cc7a9e2cabc92db41cd57ca03233f07d |
| ↳ PDFium (upstream base 7cfa57a91284ba907cb0facaf9cd8e4a570fe5c7, 2026-02-14; plus BentoPDF patches security-fixes, editcore-pdfium, brotli-decode); includes PDFium's built-in standard-font data (core/fxge/fontdata/chromefontdata, Foxit/Chrome Sans/Serif/Fixed/Symbol/Dingbats + MM fonts) | embedpdf/runtime@fce2b000cc7a | BSD-3-Clause AND Apache-2.0 | Copyright 2014 The PDFium Authors; Original code copyright 2014 Foxit Software Inc. http://www.foxitsoftware.com; Copyright (c) 1990-1994 Adobe Systems Incorporated (PostScript code inside the embedded multiple-master font data) | https://github.com/embedpdf/runtime/tree/fce2b000cc7a9e2cabc92db41cd57ca03233f07d (upstream https://pdfium.googlesource.com/pdfium/+/7cfa57a91284ba907cb0facaf9cd8e4a570fe5c7) |
| ↳ FreeType | 2.14.1-38 (VER-2-14-1-38, b91f75bd02db43b06d634591eb286d3eb0ce3b65) | FTL | Copyright 1996-2002, 2006 by David Turner, Robert Wilhelm, and Werner Lemberg (FTL.TXT); Portions of this software are copyright (C) The FreeType Project (https://freetype.org). All rights reserved. | https://chromium.googlesource.com/chromium/src/third_party/freetype2.git/+/b91f75bd02db43b06d634591eb286d3eb0ce3b65 (mirror of https://gitlab.freedesktop.org/freetype/freetype) |
| ↳ libjpeg-turbo (Chromium copy) | 3.1.0 (chromium/deps/libjpeg_turbo@6bb85251a8382b5e07f635a981ac685cc5ab5053; upstream 20ade4dea9589515a69793e447a6c6220b464535) | IJG AND BSD-3-Clause AND Zlib | Copyright (C)2009-2024 D. R. Commander. All Rights Reserved.; Copyright (C)2015 Viktor Szathmary. All Rights Reserved.; This software is copyright (C) 1991-2020, Thomas G. Lane, Guido Vollbeding.; This software is based in part on the work of the Independent JPEG Group. | https://chromium.googlesource.com/chromium/deps/libjpeg_turbo.git/+/6bb85251a8382b5e07f635a981ac685cc5ab5053 |
| ↳ libpng (Chromium copy) | 1.6.43 | libpng-2.0 | Copyright (c) 1995-2024 The PNG Reference Library Authors.; Copyright (c) 2018-2024 Cosmin Truta.; Copyright (c) 2000-2002, 2004, 2006-2018 Glenn Randers-Pehrson.; Copyright (c) 1996-1997 Andreas Dilger.; Copyright (c) 1995-1996 Guy Eric Schalnat, Group 42, Inc. | https://chromium.googlesource.com/chromium/src/third_party/libpng.git/+/172f83835c98264e6eefdbe8ae82dc08be337ad0 |
| ↳ zlib (Chromium fork, Cr_z_-prefixed, with Chromium/Intel/ARM SIMD additions) | 1.3.1 (chromium/src/third_party/zlib@980253c1cc835c893c57b5cfc10c5b942e10bc46) | Zlib | Copyright (C) 1995-2024 Jean-loup Gailly and Mark Adler | https://chromium.googlesource.com/chromium/src/third_party/zlib.git/+/980253c1cc835c893c57b5cfc10c5b942e10bc46 |
| ↳ Little CMS (PDFium copy, patched) | 2.15 (d0752309ff93f62be246ee9bf18338107f30d485 + PDFium patches) | MIT | Copyright (c) 2023 Marti Maria Saguer | https://github.com/embedpdf/runtime/tree/fce2b000cc7a9e2cabc92db41cd57ca03233f07d/third_party/lcms |
| ↳ OpenJPEG (PDFium copy, patched) | 2.5.4 (6c4a29b00211eb0430fa0e5e890f1ce5c80f409f + PDFium patches) | BSD-2-Clause | Copyright (c) 2002-2014, Universite catholique de Louvain (UCL), Belgium; Copyright (c) 2002-2014, Professor Benoit Macq; Copyright (c) 2003-2014, Antonin Descampe; Copyright (c) 2003-2009, Francois-Olivier Devaux; Copyright (c) 2005, Herve Drolon, FreeImage Team; Copyright (c) 2002-2003, Yannick Verschueren; Copyright (c) 2001-2003, David Janssens; Copyright (c) 2011-2012, Centre National d'Etudes Spatiales (CNES), France; Copyright (c) 2012, CS Systemes d'Information, France | https://github.com/embedpdf/runtime/tree/fce2b000cc7a9e2cabc92db41cd57ca03233f07d/third_party/libopenjpeg |
| ↳ Anti-Grain Geometry (PDFium copy) | 2.3 | LicenseRef-AGG-2.3 | Copyright (C) 2002-2005 Maxim Shemanarev (McSeem) | https://github.com/embedpdf/runtime/tree/fce2b000cc7a9e2cabc92db41cd57ca03233f07d/third_party/agg23 |
| ↳ Brotli decoder (added by BentoPDF's brotli-decode.patch for /BrotliDecode streams) | 9801a2c5d6c67c467ffad676ac301379bb877fc3 (chromium/src/third_party/brotli@ac16a36bc55c4c896135084e878f0d6a2f9b347e) | MIT | Copyright (c) 2009, 2010, 2013-2016 by the Brotli Authors. | https://chromium.googlesource.com/chromium/src/third_party/brotli.git/+/ac16a36bc55c4c896135084e878f0d6a2f9b347e |
| ↳ ICU common library (icuuc; compiled-in character-property tables, no icudt data file) | 77.1 (chromium/deps/icu@a86a32e67b8d1384b33f8fa48c83a6079b86f8cd) | Unicode-3.0 | Copyright © 2016-2025 Unicode, Inc.; Copyright (c) 1995-2016 International Business Machines Corporation and others; plus the third-party notices in the ICU LICENSE file | https://chromium.googlesource.com/chromium/deps/icu.git/+/a86a32e67b8d1384b33f8fa48c83a6079b86f8cd |
| ↳ Abseil C++ (parts used by PDFium fxcrt) | 0437a6d16a02455a07bb59da6f08ef01c6a20682 (chromium mirror 675d3d37ecbec78fd51378c6774c45715b1e4382) | Apache-2.0 | Copyright The Abseil Authors | https://chromium.googlesource.com/chromium/src/third_party/abseil-cpp.git/+/675d3d37ecbec78fd51378c6774c45715b1e4382 |
| ↳ fast_float | 7.0.0 (cb1d42aaa1e14b09e1452cfdef373d051b8c02a4) | MIT | Copyright (c) 2021 The fast_float authors | https://chromium.googlesource.com/external/github.com/fastfloat/fast_float.git/+/cb1d42aaa1e14b09e1452cfdef373d051b8c02a4 |
| ↳ Skia path-ops / geometry subset (EmbedPDF Runtime 'redaction_pathops' static library) | c497e689bf3db5c8efe853dae45dd61867d3363a | BSD-3-Clause | Copyright (c) 2011 Google Inc. All rights reserved. | https://skia.googlesource.com/skia.git/+/c497e689bf3db5c8efe853dae45dd61867d3363a |
| ↳ HarfBuzz (vendored in the fork at packages/pdfium/build/code/harfbuzz; shaping + hb-subset for EditCore), incl. src/ms-use tables | 11.0.0 | MIT-Modern-Variant AND MIT | Copyright © 2010-2022  Google, Inc.; Copyright © 2015-2020  Ebrahim Byagowi; Copyright © 2019,2020  Facebook, Inc.; Copyright © 2012,2015  Mozilla Foundation; Copyright © 2011  Codethink Limited; Copyright © 2008,2010  Nokia Corporation and/or its subsidiary(-ies); Copyright © 2009  Keith Stribley; Copyright © 2011  Martin Hosken and SIL International; Copyright © 2007  Chris Wilson; Copyright © 2005,2006,2020,2021,2022,2023  Behdad Esfahbod; Copyright © 2004,2007,2008,2009,2010,2013,2021,2022,2023  Red Hat, Inc.; Copyright © 1998-2005  David Turner and Werner Lemberg; Copyright © 2016  Igalia S.L.; Copyright © 2022  Matthias Clasen; Copyright © 2018,2021  Khaled Hosny; Copyright © 2018,2019,2020  Adobe, Inc; Copyright © 2013-2015  Alexei Podtelezhnikov; Copyright (c) Microsoft Corporation. (src/ms-use) | https://github.com/alam00000/bentopdf-pdfium-viewer/tree/3ec97c1ea26601703353fbc3f390cc2a54f983bc/packages/pdfium/build/code/harfbuzz (== https://github.com/harfbuzz/harfbuzz/tree/11.0.0 per hb-version.h) |
| ↳ Emscripten runtime and system libraries (JS glue editcore.js, musl-based libc, LLVM libc++/libc++abi, compiler-rt, dlmalloc) | 3.1.70 (emscripten/emsdk:3.1.70 image) | (MIT OR NCSA) AND MIT AND (Apache-2.0 WITH LLVM-exception) | Copyright (c) 2010-2014 Emscripten authors, see AUTHORS file.; Copyright © 2005-2020 Rich Felker, et al. (musl libc; further notices in its COPYRIGHT file); LLVM Project contributors (libc++, libc++abi, compiler-rt; Apache-2.0 WITH LLVM-exception) | https://github.com/emscripten-core/emscripten/tree/3.1.70 |
| qpdf (qpdf-wasm) | 12.2.0 (qpdf-wasm 0.3.0) | Apache-2.0 AND ISC ([qpdf-12.2.0--LICENSE.txt.txt](licenses/texts/qpdf-12.2.0--LICENSE.txt.txt), [qpdf-12.2.0--NOTICE.md.txt](licenses/texts/qpdf-12.2.0--NOTICE.md.txt), [qpdf-12.2.0--libqpdf-MD5_native.cc-notice.txt](licenses/texts/qpdf-12.2.0--libqpdf-MD5_native.cc-notice.txt), [Apache-2.0.txt](licenses/texts/Apache-2.0.txt), [template-ISC.txt](licenses/texts/template-ISC.txt), [zlib-1.2.12--README.txt](licenses/texts/zlib-1.2.12--README.txt), [libjpeg-turbo-2.1.1-git7aa2a89--LICENSE.md.txt](licenses/texts/libjpeg-turbo-2.1.1-git7aa2a89--LICENSE.md.txt), [libjpeg-turbo-2.1.1-git7aa2a89--README.ijg.txt](licenses/texts/libjpeg-turbo-2.1.1-git7aa2a89--README.ijg.txt), [emscripten-4.0.15--LICENSE.txt](licenses/texts/emscripten-4.0.15--LICENSE.txt), [emscripten-4.0.15--musl-COPYRIGHT.txt](licenses/texts/emscripten-4.0.15--musl-COPYRIGHT.txt), [emscripten-4.0.15--libcxx-LICENSE.TXT.txt](licenses/texts/emscripten-4.0.15--libcxx-LICENSE.TXT.txt)) | qpdf is copyright (c) 2005-2021 Jay Berkenbilt, 2022-2025 Jay Berkenbilt and Manfred Holger; @neslinesli93/qpdf-wasm (build scripts, pre/post JS): no copyright line upstream (package.json license ISC; GitHub user neslinesli93) | https://github.com/neslinesli93/qpdf-wasm/tree/0.3.0 (commit e661db2d17e391a9fbe6b350b4ea6dbd8c385891 = npm gitHead); npm https://registry.npmjs.org/@neslinesli93/qpdf-wasm/-/qpdf-wasm-0.3.0.tgz (sha1 fc32b0ef137f178d23e97f7ccca8285170165bd4). Compiled sources pinned by its Dockerfile: https://github.com/qpdf/qpdf/tree/856d32c610334855d30e96d25eb5f9636fb62f08 (tag v12.2.0), https://github.com/madler/zlib/tree/21767c654d31d2dccdde4330529775c6c5fd5389 (zlib 1.2.12), https://github.com/ImageMagick/jpeg-turbo/tree/7aa2a898c564041a24b09d0a6e780aaa632d08d3 (libjpeg-turbo 2.1.1) + patches/jpeg-turbo.patch |
| ↳ qpdf (libqpdf + qpdf CLI qpdf/qpdf.cc), native crypto provider only | 12.2.0 | Apache-2.0 | qpdf is copyright (c) 2005-2021 Jay Berkenbilt, 2022-2025 Jay Berkenbilt and Manfred Holger | https://github.com/qpdf/qpdf/tree/v12.2.0 (commit 856d32c610334855d30e96d25eb5f9636fb62f08) |
| ↳ sphlib sha2 code (in qpdf) | sphlib 3.0 | MIT | Copyright (c) 2007-2011  Projet RNRT SAPHIR | qpdf v12.2.0 libqpdf/sha2.c, sha2big.c (see NOTICE.md) |
| ↳ Rijndael (AES) implementation (in qpdf) | as in qpdf 12.2.0 | LicenseRef-Public-Domain | Philip J. Erdelsky's public domain implementation (libqpdf/rijndael.cc) | qpdf v12.2.0 libqpdf/rijndael.cc |
| ↳ MD5 (derived from the RSA Data Security, Inc. MD5 Message-Digest Algorithm, in qpdf) | as in qpdf 12.2.0 | RSA-MD | Copyright (C) 1991-2, RSA Data Security, Inc. Created 1991. All rights reserved. | qpdf v12.2.0 libqpdf/MD5_native.cc |
| ↳ zlib | 1.2.12 | Zlib | (C) 1995-2022 Jean-loup Gailly and Mark Adler | https://github.com/madler/zlib/tree/21767c654d31d2dccdde4330529775c6c5fd5389 (tag v1.2.12) |
| ↳ libjpeg-turbo (ImageMagick's jpeg-turbo fork), libjpeg API only, no SIMD | 2.1.1 (commit 7aa2a898c564041a24b09d0a6e780aaa632d08d3) | IJG AND BSD-3-Clause AND Zlib | Copyright (C) 1991-2021 The libjpeg-turbo Project and many others; Copyright (C)2009-2021 D. R. Commander. All Rights Reserved.; Copyright (C)2015 Viktor Szathmáry. All Rights Reserved.; This software is copyright (C) 1991-2020, Thomas G. Lane, Guido Vollbeding. | https://github.com/ImageMagick/jpeg-turbo/tree/7aa2a898c564041a24b09d0a6e780aaa632d08d3 + https://github.com/neslinesli93/qpdf-wasm/blob/0.3.0/patches/jpeg-turbo.patch |
| ↳ Emscripten runtime (JS glue) and system libraries: musl libc, LLVM libc++/libc++abi/compiler-rt, dlmalloc | Emscripten 3.1.74 | (MIT OR NCSA) AND MIT AND Apache-2.0 WITH LLVM-exception AND CC0-1.0 | Copyright (c) 2010-2014 Emscripten authors, see AUTHORS file.; Copyright © 2005-2020 Rich Felker, et al. (musl); LLVM: contributors listed in CREDITS.TXT; dlmalloc 2.8.6: written by Doug Lea and released to the public domain (CC0) | https://github.com/emscripten-core/emscripten/tree/3.1.74 |
| libvips (wasm-vips) | 8.18.1 (wasm-vips 0.0.17) | MIT AND LGPL-2.1-or-later ([wasm-vips-0.0.17--LICENSE.txt](licenses/texts/wasm-vips-0.0.17--LICENSE.txt), [wasm-vips-0.0.17--THIRD-PARTY-NOTICES.md.txt](licenses/texts/wasm-vips-0.0.17--THIRD-PARTY-NOTICES.md.txt), [libvips-8.18.1--LICENSE.txt](licenses/texts/libvips-8.18.1--LICENSE.txt), [libvips-8.18.1--libvips-foreign-libnsgif-COPYING.txt](licenses/texts/libvips-8.18.1--libvips-foreign-libnsgif-COPYING.txt), [libvips-8.18.1--libvips-foreign-radiance.c-notice.txt](licenses/texts/libvips-8.18.1--libvips-foreign-radiance.c-notice.txt), [libvips-8.18.1--libvips-foreign-vips2tiff.c-tiff2vips.c-notice.txt](licenses/texts/libvips-8.18.1--libvips-foreign-vips2tiff.c-tiff2vips.c-notice.txt), [glib-2.88.0--LICENSES-LGPL-2.1-or-later.txt](licenses/texts/glib-2.88.0--LICENSES-LGPL-2.1-or-later.txt), [libexif-0.6.25--COPYING.txt](licenses/texts/libexif-0.6.25--COPYING.txt), [LGPL-2.1.txt](licenses/texts/LGPL-2.1.txt), [LGPL-3.0.txt](licenses/texts/LGPL-3.0.txt), [GPL-3.0.txt](licenses/texts/GPL-3.0.txt), [libffi-3.5.2--LICENSE.txt](licenses/texts/libffi-3.5.2--LICENSE.txt), [zlib-ng-2.3.3--LICENSE.md.txt](licenses/texts/zlib-ng-2.3.3--LICENSE.md.txt), [expat-2.7.5--COPYING.txt](licenses/texts/expat-2.7.5--COPYING.txt), [lcms2-2.18--LICENSE.txt](licenses/texts/lcms2-2.18--LICENSE.txt), [highway-1.3.0--LICENSE.txt](licenses/texts/highway-1.3.0--LICENSE.txt), [highway-1.3.0--LICENSE-BSD3.txt](licenses/texts/highway-1.3.0--LICENSE-BSD3.txt), [mozjpeg-5.0.0-git0826579--LICENSE.md.txt](licenses/texts/mozjpeg-5.0.0-git0826579--LICENSE.md.txt), [mozjpeg-5.0.0-git0826579--README.ijg.txt](licenses/texts/mozjpeg-5.0.0-git0826579--README.ijg.txt), [libultrahdr-1.4.0--LICENSE.txt](licenses/texts/libultrahdr-1.4.0--LICENSE.txt), [libultrahdr-1.4.0--adobe-hdr-gain-map-license-NOTICE.txt](licenses/texts/libultrahdr-1.4.0--adobe-hdr-gain-map-license-NOTICE.txt), [libpng-1.6.55--LICENSE.txt](licenses/texts/libpng-1.6.55--LICENSE.txt), [libimagequant-2.4.1--COPYRIGHT.txt](licenses/texts/libimagequant-2.4.1--COPYRIGHT.txt), [cgif-0.5.2--LICENSE.txt](licenses/texts/cgif-0.5.2--LICENSE.txt), [libwebp-1.6.0--COPYING.txt](licenses/texts/libwebp-1.6.0--COPYING.txt), [libwebp-1.6.0--PATENTS.txt](licenses/texts/libwebp-1.6.0--PATENTS.txt), [libtiff-4.7.1--LICENSE.md.txt](licenses/texts/libtiff-4.7.1--LICENSE.md.txt), [libtiff-4.7.1--libtiff-tif_lzw.c-notice.txt](licenses/texts/libtiff-4.7.1--libtiff-tif_lzw.c-notice.txt), [mimalloc-3.2.8--LICENSE.txt](licenses/texts/mimalloc-3.2.8--LICENSE.txt), [emscripten-4.0.15--LICENSE.txt](licenses/texts/emscripten-4.0.15--LICENSE.txt), [emscripten-4.0.15--musl-COPYRIGHT.txt](licenses/texts/emscripten-4.0.15--musl-COPYRIGHT.txt), [emscripten-4.0.15--libcxx-LICENSE.TXT.txt](licenses/texts/emscripten-4.0.15--libcxx-LICENSE.TXT.txt)) | Copyright (c) 2020-present Kleis Auke Wolthuizen. (wasm-vips bindings and build); libvips, GLib, libexif and the other statically linked libraries: see includes | https://github.com/kleisauke/wasm-vips/tree/v0.0.17 (commit 02850a289018b638ed0013a31521d7c30247eec8 = npm gitHead); npm https://registry.npmjs.org/wasm-vips/-/wasm-vips-0.0.17.tgz (sha1 2348b17dc479803f935a67457fbd8e03aab3011b; binaries only). Library sources: the tarballs pinned in build.sh (see includes) plus the patches build.sh downloads: https://github.com/libvips/libvips/compare/v8.18.1...kleisauke:wasm-vips-8.18.1.patch, https://github.com/GNOME/glib/compare/2.88.0...kleisauke:wasm-vips-2.88.0.patch, https://github.com/emscripten-core/emscripten/compare/5.0.3...kleisauke:wasm-vips-5.0.3.patch, https://github.com/emscripten-core/emscripten/compare/be68a76...kleisauke:mimalloc-update-3.2.8.patch, https://github.com/kleisauke/libjpeg-turbo/commit/a60fb467fc7601b008741d42e98268c8a7bcb5b4.patch, https://github.com/google/libultrahdr/commit/5ed39d67cd31d254e84ebf76b03d4b7bcc12e2f7.patch |
| ↳ libvips | 8.18.1 | LGPL-2.1-or-later | No project-wide copyright line; per-file headers, e.g. 'Copyright (C) 1991-2005 The National Gallery', 'MODIFICATION FOR VIPS Copyright 1991, K.Martinez'; Authors (CITATION.cff): the libvips team: John Cupitt, Kirk Martinez, Lovell Fuller, Kleis Auke Wolthuizen | https://github.com/libvips/libvips/releases/download/v8.18.1/vips-8.18.1.tar.xz + https://github.com/libvips/libvips/compare/v8.18.1...kleisauke:wasm-vips-8.18.1.patch |
| ↳ libnsgif (copy bundled in libvips, libvips/foreign/libnsgif, synced 22 Jan 2023) | as bundled in libvips 8.18.1 | MIT | Copyright (C) 2004 Richard Wilson; Copyright (C) 2008 Sean Fox; Copyright (C) 2013-2021 Michael Drake | vips-8.18.1.tar.xz, libvips/foreign/libnsgif (upstream https://www.netsurf-browser.org/projects/libnsgif/) |
| ↳ Radiance HDR reader/writer code in libvips (libvips/foreign/radiance.c) | Radiance 5.4 code as bundled in libvips 8.18.1 | LicenseRef-Radiance-2.0 | Radiance v5.4 Copyright (c) 1990 to 2022, The Regents of the University of California, through Lawrence Berkeley National Laboratory (subject to receipt of any required approvals from the U.S. Dept. of Energy). All rights reserved. | vips-8.18.1.tar.xz, libvips/foreign/radiance.c |
| ↳ TIFF parts of libvips (libvips/foreign/vips2tiff.c, tiff2vips.c) | as in libvips 8.18.1 | LGPL-2.1-or-later AND LicenseRef-Leffler-1988-legend | Copyright (c) 1988, 1990 by Sam Leffler.; MODIFICATION FOR VIPS Copyright 1991, K.Martinez; Copyright 1994 Ahmed Abbood. | vips-8.18.1.tar.xz |
| ↳ GLib (glib, gobject, gmodule, parts of gio) | 2.88.0 | LGPL-2.1-or-later | Copyright (C) 1995-1997 Peter Mattis, Spencer Kimball and Josh MacDonald (glib/glib.h; other files per their headers) | https://download.gnome.org/sources/glib/2.88/glib-2.88.0.tar.xz + https://github.com/GNOME/glib/compare/2.88.0...kleisauke:wasm-vips-2.88.0.patch |
| ↳ libexif | 0.6.25 | LGPL-2.1-or-later | Copyright (c) 2001 Lutz Mueller <lutz@users.sourceforge.net> (and other authors per file headers) | https://github.com/libexif/libexif/releases/download/v0.6.25/libexif-0.6.25.tar.xz |
| ↳ libffi | 3.5.2 | MIT | libffi - Copyright (c) 1996-2025 Anthony Green, Red Hat, Inc and others. | https://github.com/libffi/libffi/releases/download/v3.5.2/libffi-3.5.2.tar.gz |
| ↳ zlib-ng (zlib-compat mode) | 2.3.3 | Zlib | (C) 1995-2024 Jean-loup Gailly and Mark Adler | https://github.com/zlib-ng/zlib-ng/archive/refs/tags/2.3.3.tar.gz |
| ↳ Expat | 2.7.5 | MIT | Copyright (c) 1998-2000 Thai Open Source Software Center Ltd and Clark Cooper; Copyright (c) 2001-2025 Expat maintainers | https://github.com/libexpat/libexpat/releases/download/R_2_7_5/expat-2.7.5.tar.xz |
| ↳ Little CMS (lcms2) | 2.18 | MIT | Copyright (c) 2023 Marti Maria Saguer (LICENSE file); Copyright (c) 1998-2026 Marti Maria Saguer (source headers) | https://github.com/mm2/Little-CMS/releases/download/lcms2.18/lcms2-2.18.tar.gz |
| ↳ Highway (SIMD library) | 1.3.0 | Apache-2.0 OR BSD-3-Clause | Copyright (c) The Highway Project Authors. All rights reserved. | https://github.com/google/highway/archive/refs/tags/1.3.0.tar.gz |
| ↳ mozjpeg (libjpeg-turbo derivative) | 5.0.0 per its CMakeLists and the binary; untagged snapshot, commit 08265790774cd0714832c9e675522acbe5581437 (latest mozjpeg tag is v4.1.5) | IJG AND BSD-3-Clause AND Zlib | Copyright (C) 1991-2024 The libjpeg-turbo Project and many others; Copyright (C)2009-2024 D. R. Commander. All Rights Reserved.; Copyright (C)2015 Viktor Szathmáry. All Rights Reserved.; This software is copyright (C) 1991-2020, Thomas G. Lane, Guido Vollbeding. | https://github.com/mozilla/mozjpeg/archive/0826579.tar.gz (commit 08265790774cd0714832c9e675522acbe5581437) + https://github.com/kleisauke/libjpeg-turbo/commit/a60fb467fc7601b008741d42e98268c8a7bcb5b4.patch (+ JCP_FASTEST sed in build.sh) |
| ↳ libultrahdr (incl. third_party/image_io) | 1.4.0 | Apache-2.0 | Copyright 2022 The Android Open Source Project; This product includes Gain Map technology under license by Adobe. | https://github.com/google/libultrahdr/archive/refs/tags/v1.4.0.tar.gz + https://github.com/google/libultrahdr/commit/5ed39d67cd31d254e84ebf76b03d4b7bcc12e2f7.patch |
| ↳ libpng | 1.6.55 | libpng-2.0 | Copyright (c) 1995-2026 The PNG Reference Library Authors.; Copyright (c) 2018-2026 Cosmin Truta.; Copyright (c) 2000-2002, 2004, 2006-2018 Glenn Randers-Pehrson.; Copyright (c) 1996-1997 Andreas Dilger.; Copyright (c) 1995-1996 Guy Eric Schalnat, Group 42, Inc. | https://github.com/pnggroup/libpng/archive/refs/tags/v1.6.55.tar.gz |
| ↳ libimagequant (lovell/libimagequant, BSD-licensed 2.4.x line) | 2.4.1 | BSD-2-Clause AND HPND-Pbmplus | © 1997-2002 by Greg Roelofs; based on an idea by Stefan Schneider.; © 2009-2014 by Kornel Lesiński.; © 1989, 1991 by Jef Poskanzer. | https://github.com/lovell/libimagequant/archive/refs/tags/v2.4.1.tar.gz |
| ↳ cgif | 0.5.2 | MIT | Copyright (c) 2021-2023, Daniel Löbl <dloebl.2000@gmail.com> | https://github.com/dloebl/cgif/archive/refs/tags/v0.5.2.tar.gz |
| ↳ libwebp (incl. sharpyuv, libwebpmux, libwebpdemux) | 1.6.0 | BSD-3-Clause | Copyright (c) 2010, Google Inc. All rights reserved. | https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-1.6.0.tar.gz |
| ↳ libtiff | 4.7.1 | libtiff AND LicenseRef-BSD-compress-1985 | Copyright © 1988-1997 Sam Leffler; Copyright © 1991-1997 Silicon Graphics, Inc.; Copyright (c) 1985, 1986 The Regents of the University of California. (LZW code, tif_lzw.c) | https://download.osgeo.org/libtiff/tiff-4.7.1.tar.gz |
| ↳ Emscripten runtime (JS glue, embind) and system libraries: musl libc, LLVM libc++/libc++abi/compiler-rt | Emscripten 5.0.3 (patched by kleisauke) | (MIT OR NCSA) AND MIT AND Apache-2.0 WITH LLVM-exception | Copyright (c) 2010-2014 Emscripten authors, see AUTHORS file.; Copyright © 2005-2020 Rich Felker, et al. (musl); LLVM: Copyright (c) 2009-2019 by the contributors listed in CREDITS.TXT (legacy notice; Apache-2.0 WITH LLVM-exception for current code) | https://github.com/emscripten-core/emscripten/tree/5.0.3 + https://github.com/emscripten-core/emscripten/compare/5.0.3...kleisauke:wasm-vips-5.0.3.patch |
| ↳ mimalloc (Emscripten's copy, updated by kleisauke's mimalloc-update-3.2.8 patch) | 3.2.8 | MIT | Copyright (c) 2018-2025 Microsoft Corporation, Daan Leijen | https://github.com/emscripten-core/emscripten/compare/be68a76...kleisauke:mimalloc-update-3.2.8.patch (upstream https://github.com/microsoft/mimalloc/tree/v3.2.8) |
| Pyodide | 0.28.0a3 | MPL-2.0 ([Pyodide-0.28.0a3-LICENSE-MPL-2.0.txt](licenses/texts/Pyodide-0.28.0a3-LICENSE-MPL-2.0.txt), [Pyodide-vendored-stackframe-error-stack-parser-LICENSE.txt](licenses/texts/Pyodide-vendored-stackframe-error-stack-parser-LICENSE.txt), [libffi-LICENSE.txt](licenses/texts/libffi-LICENSE.txt), [bzip2-1.0.6-LICENSE.txt](licenses/texts/bzip2-1.0.6-LICENSE.txt), [zlib-1.3.1-LICENSE.txt](licenses/texts/zlib-1.3.1-LICENSE.txt)) | LICENSE file has no copyright line; Pyodide contributors (project started at Mozilla by Michael Droettboom) | https://github.com/pyodide/pyodide/tree/ed567eb8d2b41fb0e325927c44466b866ef56a34; built files as published at https://cdn.jsdelivr.net/pyodide/v0.28.0a3/full/ (npm https://registry.npmjs.org/pyodide/-/pyodide-0.28.0-alpha.3.tgz) |
| ↳ stackframe / error-stack-parser (vendored, rewritten to ES6 in src/js/vendor/stackframe) | as vendored in 0.28.0a3 | MIT | Copyright (c) 2017 Eric Wendelin and other contributors | https://github.com/pyodide/pyodide/tree/ed567eb8d2b41fb0e325927c44466b866ef56a34/src/js/vendor/stackframe |
| ↳ libffi | 3.4.4 (git f08493d249d2067c8b3207ba46693dd858f95db3, 2023-02-18) | MIT | libffi - Copyright (c) 1996-2022  Anthony Green, Red Hat, Inc and others. | https://github.com/libffi/libffi/tree/f08493d249d2067c8b3207ba46693dd858f95db3 |
| ↳ zlib (Emscripten port, -sUSE_ZLIB) | 1.3.1 | Zlib | (C) 1995-2024 Jean-loup Gailly and Mark Adler | https://github.com/madler/zlib/archive/refs/tags/v1.3.1.tar.gz |
| ↳ bzip2 (Emscripten port, -sUSE_BZIP2) | 1.0.6 | bzip2-1.0.6 | copyright (C) 1996-2010 Julian R Seward | https://github.com/emscripten-ports/bzip2/archive/1.0.6.zip |
| ↳ CPython 3.13.2 | 3.13.2 | PSF-2.0 |  | see component cpython |
| ↳ Emscripten runtime | 4.0.9 | see component emscripten-runtime |  | see component emscripten-runtime |
| BentoPDF PDF Viewer (EmbedPDF) | 2.9.1 | AGPL-3.0-only AND MIT ([AGPL-3.0.txt](licenses/texts/AGPL-3.0.txt), [embedpdf-2.9.1--LICENSE.txt](licenses/texts/embedpdf-2.9.1--LICENSE.txt), [bentopdf-pdfium-viewer-8ff5002c6cd5--NOTICE.txt](licenses/texts/bentopdf-pdfium-viewer-8ff5002c6cd5--NOTICE.txt), [preact-10.28.3--LICENSE.txt](licenses/texts/preact-10.28.3--LICENSE.txt), [tailwind-merge-3.4.0--LICENSE.md.txt](licenses/texts/tailwind-merge-3.4.0--LICENSE.md.txt), [floating-ui-dom-1.7.5--LICENSE.txt](licenses/texts/floating-ui-dom-1.7.5--LICENSE.txt), [tailwindcss-4.1.18--LICENSE.txt](licenses/texts/tailwindcss-4.1.18--LICENSE.txt), [babel-helpers-7.28.6--LICENSE.txt](licenses/texts/babel-helpers-7.28.6--LICENSE.txt), [tabler-icons-2.47.0--LICENSE.txt](licenses/texts/tabler-icons-2.47.0--LICENSE.txt), [feather-4.29.2--LICENSE.txt](licenses/texts/feather-4.29.2--LICENSE.txt), [emscripten-3.1.70--LICENSE.txt](licenses/texts/emscripten-3.1.70--LICENSE.txt)) | Copyright 2026 BentoPDF; Copyright (c) 2025 CloudPDF | https://github.com/alam00000/bentopdf-pdfium-viewer/tree/8ff5002c6cd5532f6fd2dffeeb43c56887dad5f8/viewers/snippet (plus the workspace packages/* it bundles); upstream base https://github.com/embedpdf/embed-pdf-viewer/tree/v2.9.1 (aa45d6ef07aa2c6a77e15387d74661e835239408) |
| ↳ EmbedPDF packages @embedpdf/core, engines, models, pdfium (JS glue), utils, plugin-* (annotation, attachment, bookmark, capture, commands, document-manager, export, fullscreen, history, i18n, interaction-manager, pan, print, redaction, render, rotate, scroll, search, selection, spread, thumbnail, tiling, ui, viewport, zoom) and the snippet UI, as modified by BentoPDF | 2.9.1 (+ BentoPDF commits to 8ff5002c6cd5) | MIT AND AGPL-3.0-only | Copyright (c) 2025 CloudPDF; Copyright 2026 BentoPDF | https://github.com/alam00000/bentopdf-pdfium-viewer/tree/8ff5002c6cd5532f6fd2dffeeb43c56887dad5f8/packages |
| ↳ preact (incl. hooks, compat, jsx-runtime) | 10.28.3 | MIT | Copyright (c) 2015-present Jason Miller | https://github.com/preactjs/preact/tree/10.28.3 |
| ↳ tailwind-merge | 3.4.0 | MIT | Copyright (c) 2021 Dany Castillo | https://github.com/dcastil/tailwind-merge/tree/v3.4.0 |
| ↳ @floating-ui/dom, @floating-ui/core, @floating-ui/utils | 1.7.5 / 1.7.4 / 0.2.10 | MIT | Copyright (c) 2021-present Floating UI contributors | https://github.com/floating-ui/floating-ui (npm @floating-ui/dom@1.7.5) |
| ↳ Tailwind CSS generated stylesheet (preflight + utilities, embedded as a string) | 4.1.18 | MIT | Copyright (c) Tailwind Labs, Inc. | https://github.com/tailwindlabs/tailwindcss/tree/v4.1.18 |
| ↳ Babel helpers (regeneratorRuntime and other inlined helpers) | 7.28.6 (@babel/helpers, per lockfile) | MIT | Copyright (c) 2014-present Sebastian McKenzie and other contributors; Copyright (c) 2014-present, Facebook, Inc. (regenerator helper) | https://github.com/babel/babel/tree/v7.28.6/packages/babel-helpers |
| ↳ Tabler Icons SVG path data (snippet icon components, e.g. device-floppy) | 2.x (path data identical to v2.47.0; exact version unknown) | MIT | Copyright (c) 2020-2023 Paweł Kuna | https://github.com/tabler/tabler-icons/tree/v2.47.0 |
| ↳ Feather Icons SVG path data (e.g. alert-triangle) | 4.x (exact version unknown) | MIT | Copyright (c) 2013-2023 Cole Bemis | https://github.com/feathericons/feather/tree/v4.29.2 |
| ↳ Emscripten-generated PDFium JS glue (inside worker-engine/direct-engine chunks; same build as bentopdf-pdfium) | 3.1.70 | MIT OR NCSA | Copyright (c) 2010-2014 Emscripten authors, see AUTHORS file. | https://github.com/emscripten-core/emscripten/tree/3.1.70 |
| Emscripten runtime (in LibreOffice and Pyodide) | 3.1.74, 4.0.9 | (MIT OR NCSA) AND MIT AND (Apache-2.0 WITH LLVM-exception) ([Emscripten-LICENSE.txt](licenses/texts/Emscripten-LICENSE.txt), [Emscripten-musl-COPYRIGHT.txt](licenses/texts/Emscripten-musl-COPYRIGHT.txt), [Emscripten-libcxx-LICENSE.txt](licenses/texts/Emscripten-libcxx-LICENSE.txt), [Emscripten-libcxxabi-LICENSE.txt](licenses/texts/Emscripten-libcxxabi-LICENSE.txt), [Emscripten-compiler-rt-LICENSE.txt](licenses/texts/Emscripten-compiler-rt-LICENSE.txt), [SPDX-NCSA.txt](licenses/texts/SPDX-NCSA.txt)) | Copyright (c) 2010-2014 Emscripten authors, see AUTHORS file.; Copyright © 2005-2020 Rich Felker, et al. (musl); The LLVM Project is under the Apache License v2.0 with LLVM Exceptions | https://github.com/emscripten-core/emscripten/tree/4.0.9 and /tree/3.1.74 (system/lib/libc/musl, system/lib/libcxx, system/lib/libcxxabi, system/lib/compiler-rt) |
| fontTools | 4.56.0 | MIT ([fonttools-4.56.0-LICENSE.txt](licenses/texts/fonttools-4.56.0-LICENSE.txt), [fonttools-4.56.0-LICENSE.external.txt](licenses/texts/fonttools-4.56.0-LICENSE.external.txt)) | Copyright (c) 2017 Just van Rossum | https://files.pythonhosted.org/packages/bf/ff/44934a031ce5a39125415eb405b9efb76fe7f9586b75291d66ae5cbfc4e6/fonttools-4.56.0-py3-none-any.whl (as re-published by Pyodide 0.28.0a3); git tag 4.56.0 |
| ↳ Adobe Glyph List / AGLFN (fontTools/agl.py) | as in 4.56.0 | BSD-3-Clause | Adobe Systems Incorporated | https://github.com/fonttools/fonttools/blob/4.56.0/LICENSE.external |
| ↳ cu2qu | as in 4.56.0 | Apache-2.0 | Copyright 2016 Google Inc. All Rights Reserved. | https://github.com/fonttools/fonttools/blob/4.56.0/LICENSE.external |
| heic2any (with libheif and libde265) | 0.0.4 | MIT AND LGPL-3.0-or-later ([heic2any-0.0.4--LICENSE.md.txt](licenses/texts/heic2any-0.0.4--LICENSE.md.txt), [libheif-1.10.0--COPYING.txt](licenses/texts/libheif-1.10.0--COPYING.txt), [libde265-1.0.2--COPYING.txt](licenses/texts/libde265-1.0.2--COPYING.txt), [libde265-1.0.2--libde265-md5.cc-notice.txt](licenses/texts/libde265-1.0.2--libde265-md5.cc-notice.txt), [LGPL-3.0.txt](licenses/texts/LGPL-3.0.txt), [GPL-3.0.txt](licenses/texts/GPL-3.0.txt), [gifshot-0.4.5--LICENSE.txt.txt](licenses/texts/gifshot-0.4.5--LICENSE.txt.txt), [gifshot-0.4.5--src-modules-dependencies-NeuQuant.js-notice.txt](licenses/texts/gifshot-0.4.5--src-modules-dependencies-NeuQuant.js-notice.txt), [gifshot-0.4.5--src-modules-dependencies-gifWriter.js-notice.txt](licenses/texts/gifshot-0.4.5--src-modules-dependencies-gifWriter.js-notice.txt), [emscripten-4.0.15--LICENSE.txt](licenses/texts/emscripten-4.0.15--LICENSE.txt), [emscripten-4.0.15--musl-COPYRIGHT.txt](licenses/texts/emscripten-4.0.15--musl-COPYRIGHT.txt), [emscripten-4.0.15--libcxx-LICENSE.TXT.txt](licenses/texts/emscripten-4.0.15--libcxx-LICENSE.TXT.txt)) | Copyright (c) 2020 Alex Corvi (heic2any); Embedded libheif/libde265 (LGPL-3.0-or-later) and gifshot (MIT): see includes | https://github.com/alexcorvi/heic2any/tree/0.0.4 (tag -> 3428539e643e112323a5b8a2c77c6402cb1372f6; version commit 8595b0f3c79b986187c5bfa84e9755231ec988e8; src/libheif.js and src/gifshot.js are prebuilt inputs); npm https://registry.npmjs.org/heic2any/-/heic2any-0.0.4.tgz (sha1 eddb8e6fec53c8583a6e18b65069bb5e8d19028a). Embedded libraries: https://github.com/strukturag/libheif/releases/download/v1.10.0/libheif-1.10.0.tar.gz, https://github.com/strukturag/libde265/releases/download/v1.0.2/libde265-1.0.2.tar.gz, prebuilt libheif.js as published at https://github.com/strukturag/libheif/blob/d7d6f2bd6b5e793f1f4dd483cf18a0ad57ac7237/libheif.js, https://registry.npmjs.org/gifshot/-/gifshot-0.4.5.tgz |
| ↳ libheif (libheif.js Emscripten/asm.js build incl. pre.js/post.js JS API) | 1.10.0 | LGPL-3.0-or-later | Copyright (c) 2017 struktur AG, Dirk Farin <farin@struktur.de> (libheif/heif.cc; other files per headers); (c)2017 struktur AG, http://www.struktur.de, opensource@struktur.de (libheif.js pre.js header) | https://github.com/strukturag/libheif/releases/download/v1.10.0/libheif-1.10.0.tar.gz (tag v1.10.0 = commit 667eeabb553ce73094eb29faea3f31fb8610fec2); built file: https://github.com/strukturag/libheif/blob/d7d6f2bd6b5e793f1f4dd483cf18a0ad57ac7237/libheif.js |
| ↳ libde265 (HEVC decoder, linked into libheif.js) | 1.0.2 | LGPL-3.0-or-later | Copyright (c) 2013-2014 struktur AG, Dirk Farin <farin@struktur.de> (libde265/de265.cc; other files per headers) | https://github.com/strukturag/libde265/releases/download/v1.0.2/libde265-1.0.2.tar.gz |
| ↳ MD5 implementation in libde265 (libde265/md5.cc, Solar Designer) | as in libde265 1.0.2 | LicenseRef-Public-Domain | Written by Alexander Peslyak (Solar Designer) in 2001; no copyright claimed (fallback: Copyright (c) 2001 Alexander Peslyak) | https://github.com/strukturag/libde265/blob/v1.0.2/libde265/md5.cc |
| ↳ gifshot | 0.4.5 | MIT | Copyright 2017 Yahoo Inc. | https://registry.npmjs.org/gifshot/-/gifshot-0.4.5.tgz (github.com/yahoo/gifshot; the GitHub repo no longer resolves via the API) |
| ↳ NeuQuant neural-net colour quantizer (inside gifshot) | JS port 0.3 as in gifshot 0.4.5 | LicenseRef-NeuQuant | Copyright (c) 1994 Anthony Dekker; @author Kevin Weiner (original Java version), Thibault Imbert (AS3 version), antimatter15, sole | gifshot 0.4.5 src/modules/dependencies/NeuQuant.js |
| ↳ omggif GIF writer (inside gifshot) | as in gifshot 0.4.5 | MIT | (c) Dean McNamee <dean@gmail.com>, 2013. | gifshot 0.4.5 src/modules/dependencies/gifWriter.js (https://github.com/deanm/omggif) |
| ↳ Emscripten runtime and system libraries (libc++, musl) compiled into libheif.js | unknown (Emscripten build of December 2020) | (MIT OR NCSA) AND MIT AND Apache-2.0 WITH LLVM-exception | Copyright (c) 2010-2014 Emscripten authors, see AUTHORS file.; Copyright © 2005-2020 Rich Felker, et al. (musl); LLVM libc++: contributors listed in CREDITS.TXT | https://github.com/emscripten-core/emscripten (exact version not recorded by libheif's gh-pages build) |
| LibreOffice converter (@matbee/libreoffice-converter) | 2.3.1 and 2.6.0 | MPL-2.0 ([LibreOffice-COPYING.MPL.txt](licenses/texts/LibreOffice-COPYING.MPL.txt)) |  | https://github.com/matbeedotcom/libreoffice-document-converter/tree/v2.3.1 (commit b94b8a6887d223be93b082543f5fd32bbd8dc646); npm https://registry.npmjs.org/@matbee/libreoffice-converter/-/libreoffice-converter-2.3.1.tgz; wrapper: tag v2.6.0 (1bfae4a495b9fb17a0e6b20a13d0ad30ad58d343), https://registry.npmjs.org/@matbee/libreoffice-converter/-/libreoffice-converter-2.6.0.tgz |
| ↳ Emscripten JS runtime glue (soffice.js / soffice.worker.js) | 3.1.74 per build script (not verifiable from the minified output) | MIT OR NCSA | Copyright (c) 2010-2014 Emscripten authors, see AUTHORS file. | https://github.com/emscripten-core/emscripten/tree/3.1.74 |
| lxml | 5.4.0 | BSD-3-Clause ([lxml-5.4.0-LICENSE.txt](licenses/texts/lxml-5.4.0-LICENSE.txt), [lxml-5.4.0-LICENSES.txt](licenses/texts/lxml-5.4.0-LICENSES.txt), [lxml-5.4.0-doc-licenses-BSD.txt](licenses/texts/lxml-5.4.0-doc-licenses-BSD.txt), [lxml-5.4.0-doc-licenses-elementtree.txt](licenses/texts/lxml-5.4.0-doc-licenses-elementtree.txt), [libxml2-2.9.10-Copyright.txt](licenses/texts/libxml2-2.9.10-Copyright.txt), [libxslt-1.1.33-Copyright.txt](licenses/texts/libxslt-1.1.33-Copyright.txt)) | Copyright (c) 2004 Infrae. All rights reserved.; lxml.cssselect and lxml.html: copyright Ian Bicking (BSD); ElementTree-derived code: Copyright (c) 1999-2003 by Secret Labs AB | https://files.pythonhosted.org/packages/source/l/lxml/lxml-5.4.0.tar.gz (sha256 d12832e1dbea4be280b22fd0ea7c9b87f0d8fc51ba06e92dc62d52f804f78ebd) |
| ↳ libxml2 (static) | 2.9.10 | MIT | Copyright (C) 1998-2012 Daniel Veillard.  All Rights Reserved. | http://xmlsoft.org/sources/libxml2-2.9.10.tar.gz (sha256 aafee193ffb8fe0c82d4afef6ef91972cbaf5feea100edc2f262750611b4be1f) |
| ↳ libxslt + libexslt (static) | 1.1.33 | MIT | Copyright (C) 2001-2002 Daniel Veillard.  All Rights Reserved.; libexslt: Copyright (C) 2001-2002 Thomas Broyer, Charlie Bozeman and Daniel Veillard. | http://xmlsoft.org/sources/libxslt-1.1.33.tar.gz (sha256 8e36605144409df979cab43d835002f63988f3dc94d5d3537c12796db90e38c8) |
| ↳ zlib (Pyodide static lib, build dependency of libxml2) | 1.3.1 | Zlib | (C) 1995-2024 Jean-loup Gailly and Mark Adler | https://github.com/madler/zlib/releases/download/v1.3.1/zlib-1.3.1.tar.gz |
| ↳ ISO Schematron resources (src/lxml/isoschematron/resources) | as in 5.4.0 | MIT-style / ISO copyright notices inside the files | copyright International Organization for Standardization; Rick Jelliffe and Academia Sinica Computing Center, Taiwan | lxml 5.4.0 sdist |
| MuPDF | 1.26.3 | AGPL-3.0-or-later ([MuPDF-1.26.3-COPYING-AGPL-3.0.txt](licenses/texts/MuPDF-1.26.3-COPYING-AGPL-3.0.txt), [MuPDF-1.26.3-docs-license.md.txt](licenses/texts/MuPDF-1.26.3-docs-license.md.txt), [MuPDF-thirdparty-brotli-1.1.0-LICENSE.txt](licenses/texts/MuPDF-thirdparty-brotli-1.1.0-LICENSE.txt), [MuPDF-thirdparty-freetype-2.13.3-LICENSE.txt](licenses/texts/MuPDF-thirdparty-freetype-2.13.3-LICENSE.txt), [FreeType-FTL.txt](licenses/texts/FreeType-FTL.txt), [MuPDF-thirdparty-gumbo-parser-0.10.1-COPYING-Apache-2.0.txt](licenses/texts/MuPDF-thirdparty-gumbo-parser-0.10.1-COPYING-Apache-2.0.txt), [MuPDF-thirdparty-harfbuzz-6.0.0-COPYING.txt](licenses/texts/MuPDF-thirdparty-harfbuzz-6.0.0-COPYING.txt), [MuPDF-thirdparty-jbig2dec-0.20-LICENSE.txt](licenses/texts/MuPDF-thirdparty-jbig2dec-0.20-LICENSE.txt), [MuPDF-thirdparty-lcms2mt-2.16-LICENSE.txt](licenses/texts/MuPDF-thirdparty-lcms2mt-2.16-LICENSE.txt), [MuPDF-thirdparty-libjpeg-9f-README.txt](licenses/texts/MuPDF-thirdparty-libjpeg-9f-README.txt), [MuPDF-thirdparty-mujs-1.3.5-COPYING.txt](licenses/texts/MuPDF-thirdparty-mujs-1.3.5-COPYING.txt), [MuPDF-thirdparty-openjpeg-2.5.3-LICENSE.txt](licenses/texts/MuPDF-thirdparty-openjpeg-2.5.3-LICENSE.txt), [MuPDF-thirdparty-zint-2.13.0-LICENSE.txt](licenses/texts/MuPDF-thirdparty-zint-2.13.0-LICENSE.txt), [MuPDF-thirdparty-zint-2.13.0-backend-BSD-3-Clause-header.txt](licenses/texts/MuPDF-thirdparty-zint-2.13.0-backend-BSD-3-Clause-header.txt), [MuPDF-thirdparty-zlib-1.3.1-LICENSE.txt](licenses/texts/MuPDF-thirdparty-zlib-1.3.1-LICENSE.txt), [MuPDF-thirdparty-zxing-cpp-2.3.0-LICENSE-Apache-2.0.txt](licenses/texts/MuPDF-thirdparty-zxing-cpp-2.3.0-LICENSE-Apache-2.0.txt), [MuPDF-fonts-urw-OFL.txt](licenses/texts/MuPDF-fonts-urw-OFL.txt), [MuPDF-fonts-sil-CharisSIL-OFL.txt](licenses/texts/MuPDF-fonts-sil-CharisSIL-OFL.txt), [MuPDF-fonts-noto-COPYING-OFL-1.1.txt](licenses/texts/MuPDF-fonts-noto-COPYING-OFL-1.1.txt), [MuPDF-fonts-droid-NOTICE-Apache-2.0.txt](licenses/texts/MuPDF-fonts-droid-NOTICE-Apache-2.0.txt), [Adobe-cmap-resources-LICENSE.md.txt](licenses/texts/Adobe-cmap-resources-LICENSE.md.txt), [MuPDF-resources-README-cmaps.txt](licenses/texts/MuPDF-resources-README-cmaps.txt)) | Copyright (C) 2004-2025 Artifex Software, Inc. | https://mupdf.com/downloads/archive/mupdf-1.26.3-source.tar.gz (sha256 ab467fc2d888cd8424cdce4bc6dd7ec61f34820582ddf3769a336e6909d9a48e); git https://github.com/ArtifexSoftware/mupdf tag 1.26.3 |
| ↳ brotli | 1.1.0 | MIT | Copyright (c) 2009, 2010, 2013-2016 by the Brotli Authors. | https://mupdf.com/downloads/archive/mupdf-1.26.3-source.tar.gz thirdparty/brotli |
| ↳ extract (Artifex document extraction library) | as in MuPDF 1.26.3 | AGPL-3.0-only | Artifex Software, Inc. | https://mupdf.com/downloads/archive/mupdf-1.26.3-source.tar.gz thirdparty/extract |
| ↳ FreeType | 2.13.3 | FTL OR GPL-2.0-or-later | Copyright (C) 1996-2024 by David Turner, Robert Wilhelm, and Werner Lemberg. | https://mupdf.com/downloads/archive/mupdf-1.26.3-source.tar.gz thirdparty/freetype |
| ↳ gumbo-parser (Artifex fork) | 0.10.1 | Apache-2.0 | Copyright 2010 Google Inc. | https://mupdf.com/downloads/archive/mupdf-1.26.3-source.tar.gz thirdparty/gumbo-parser |
| ↳ HarfBuzz | 6.0.0 | MIT-Modern-Variant | Copyright © 2010-2020  Google, Inc.; Copyright © 2018,2019,2020  Ebrahim Byagowi; Copyright © 2019,2020  Facebook, Inc.; Copyright © 2012  Mozilla Foundation; Copyright © 2011  Codethink Limited; Copyright © 2008,2010  Nokia Corporation and/or its subsidiary(-ies); Copyright © 2009  Keith Stribley; Copyright © 2009  Martin Hosken and SIL International; Copyright © 2007  Chris Wilson; Copyright © 2005,2006,2020,2021  Behdad Esfahbod; Copyright © 2005  David Turner; Copyright © 2004,2007,2008,2009,2010  Red Hat, Inc.; Copyright © 1998-2004  David Turner and Werner Lemberg | https://mupdf.com/downloads/archive/mupdf-1.26.3-source.tar.gz thirdparty/harfbuzz |
| ↳ jbig2dec | 0.20 | AGPL-3.0-or-later | Artifex Software, Inc. | https://mupdf.com/downloads/archive/mupdf-1.26.3-source.tar.gz thirdparty/jbig2dec |
| ↳ lcms2mt (MuPDF thread-safe fork of Little CMS) | 2.16 | MIT | Copyright (c) 2023 Marti Maria Saguer | https://mupdf.com/downloads/archive/mupdf-1.26.3-source.tar.gz thirdparty/lcms2 |
| ↳ libjpeg (IJG) | 9f (14-Jan-2024) | IJG | Copyright (C) 1991-2024, Thomas G. Lane, Guido Vollbeding. | https://mupdf.com/downloads/archive/mupdf-1.26.3-source.tar.gz thirdparty/libjpeg |
| ↳ MuJS | 1.3.5 | ISC | Copyright (c) 2013-2020 Artifex Software, Inc. | https://mupdf.com/downloads/archive/mupdf-1.26.3-source.tar.gz thirdparty/mujs |
| ↳ OpenJPEG | 2.5.3 | BSD-2-Clause | Copyright (c) 2002-2014, Universite catholique de Louvain (UCL), Belgium; Copyright (c) 2002-2014, Professor Benoit Macq; and others in LICENSE | https://mupdf.com/downloads/archive/mupdf-1.26.3-source.tar.gz thirdparty/openjpeg |
| ↳ zlib | 1.3.1 | Zlib | (C) 1995-2024 Jean-loup Gailly and Mark Adler | https://mupdf.com/downloads/archive/mupdf-1.26.3-source.tar.gz thirdparty/zlib |
| ↳ zint (barcode generation, backend only) | 2.13.0 | BSD-3-Clause | Copyright (C) 2009-2024 Robin Stuart <rstuart114@gmail.com> | https://mupdf.com/downloads/archive/mupdf-1.26.3-source.tar.gz thirdparty/zint |
| ↳ zxing-cpp (barcode reading) | 2.3.0 | Apache-2.0 | ZXing authors / zxing-cpp contributors (per-file headers) | https://mupdf.com/downloads/archive/mupdf-1.26.3-source.tar.gz thirdparty/zxing-cpp |
| ↳ URW++ base-35 fonts subset (Nimbus Sans/Roman/Mono PS, Standard Symbols PS, Dingbats, Nimbus Boxes), CFF | as in MuPDF 1.26.3 | OFL-1.1 | Copyright 2016 by (URW)++ Design & Development. | https://mupdf.com/downloads/archive/mupdf-1.26.3-source.tar.gz resources/fonts/urw |
| ↳ Charis SIL (stripped "dumb" CFF version) | 5.000 | OFL-1.1 | Copyright (c) 1997-2014, SIL International (http://scripts.sil.org/) with Reserved Font Names "Charis" and "SIL". | https://mupdf.com/downloads/archive/mupdf-1.26.3-source.tar.gz resources/fonts/sil |
| ↳ Noto fonts (Noto Sans/Serif Regular, ~150 script fonts, Noto Sans Math, Noto Music, Noto Emoji, Noto Sans Symbols/Symbols2, Naskh Arabic, Nastaliq Urdu) | as in MuPDF 1.26.3 | OFL-1.1 | Copyright The Noto Project Authors / Google (per font) | https://mupdf.com/downloads/archive/mupdf-1.26.3-source.tar.gz resources/fonts/noto |
| ↳ Droid Sans Fallback (CJK fallback) | as in MuPDF 1.26.3 | Apache-2.0 | Copyright (c) 2005-2008, The Android Open Source Project | https://mupdf.com/downloads/archive/mupdf-1.26.3-source.tar.gz resources/fonts/droid |
| ↳ Adobe CMap resources (CJK CMaps compiled in, headers stripped) | as in MuPDF 1.26.3 | BSD-3-Clause | Copyright 1990-2023 Adobe. All rights reserved. | https://github.com/adobe-type-tools/cmap-resources (MuPDF resources/cmaps) |
| ↳ ICC profiles (resources/icc gray/rgb/cmyk/lab) | as in MuPDF 1.26.3 | AGPL-3.0-or-later | Copyright Artifex Software 2011/2018; Copyright 2009 Artifex Software Inc | https://mupdf.com/downloads/archive/mupdf-1.26.3-source.tar.gz resources/icc |
| NumPy | 2.2.5 | BSD-3-Clause AND MIT AND Zlib ([numpy-2.2.5-LICENSE.txt](licenses/texts/numpy-2.2.5-LICENSE.txt), [numpy-2.2.5-bundled-lapack_lite-LICENSE.txt](licenses/texts/numpy-2.2.5-bundled-lapack_lite-LICENSE.txt), [numpy-2.2.5-bundled-pocketfft-LICENSE.md.txt](licenses/texts/numpy-2.2.5-bundled-pocketfft-LICENSE.md.txt), [numpy-2.2.5-bundled-dragon4-MIT-header.txt](licenses/texts/numpy-2.2.5-bundled-dragon4-MIT-header.txt), [numpy-2.2.5-bundled-libdivide-LICENSE.txt](licenses/texts/numpy-2.2.5-bundled-libdivide-LICENSE.txt), [numpy-2.2.5-random-LICENSE.md.txt](licenses/texts/numpy-2.2.5-random-LICENSE.md.txt), [numpy-2.2.5-random-distributions-LICENSE.md.txt](licenses/texts/numpy-2.2.5-random-distributions-LICENSE.md.txt), [numpy-2.2.5-random-mt19937-LICENSE.md.txt](licenses/texts/numpy-2.2.5-random-mt19937-LICENSE.md.txt), [numpy-2.2.5-random-pcg64-LICENSE.md.txt](licenses/texts/numpy-2.2.5-random-pcg64-LICENSE.md.txt), [numpy-2.2.5-random-philox-LICENSE.md.txt](licenses/texts/numpy-2.2.5-random-philox-LICENSE.md.txt), [numpy-2.2.5-random-sfc64-LICENSE.md.txt](licenses/texts/numpy-2.2.5-random-sfc64-LICENSE.md.txt), [numpy-2.2.5-random-splitmix64-LICENSE.md.txt](licenses/texts/numpy-2.2.5-random-splitmix64-LICENSE.md.txt)) | Copyright (c) 2005-2024, NumPy Developers. All rights reserved. | https://files.pythonhosted.org/packages/source/n/numpy/numpy-2.2.5.tar.gz (sha256 a9c0d994680cd991b1cb772e8b297340085466a6fe964bc9d4e80f5e2f43c291) + Pyodide patch 0001-TST-Prevent-import-error-when-tests-are-not-included.patch |
| ↳ lapack-lite (f2c-translated LAPACK/BLAS subset) | as in 2.2.5 | BSD-3-Clause | see numpy/linalg/lapack_lite/LICENSE.txt | numpy v2.2.5 |
| ↳ pocketfft (C++ header-only) | submodule 33ae5dc94c9cdc7f1c78346504a85de87cadaa12 | BSD-3-Clause | Copyright (C) 2010-2018 Max-Planck-Society | https://github.com/mreineck/pocketfft/tree/33ae5dc94c9cdc7f1c78346504a85de87cadaa12 |
| ↳ dragon4 | as in 2.2.5 | MIT | Copyright (c) 2014 Ryan Juckett | numpy v2.2.5 numpy/_core/src/multiarray/dragon4.c |
| ↳ libdivide | as in 2.2.5 | Zlib | see numpy/_core/include/numpy/libdivide/LICENSE.txt | numpy v2.2.5 |
| ↳ numpy.random bit generators and distributions | as in 2.2.5 | NCSA OR BSD-3-Clause (module) plus component licenses (BSD-3-Clause, MIT, public domain) | Copyright (c) 2019 Kevin Sheppard; Copyright (C) 1997 - 2002, Makoto Matsumoto and Takuji Nishimura; Copyright 2014 Melissa O'Neill; Copyright 2010-2012, D. E. Shaw Research | numpy v2.2.5 numpy/random/src/* |
| OpenCV (opencv-python) | 4.11.0.86 | Apache-2.0 AND MIT AND LGPL-2.1-or-later AND BSD-3-Clause ([opencv-python-4.11.0.86-LICENSE.txt](licenses/texts/opencv-python-4.11.0.86-LICENSE.txt), [opencv-python-4.11.0.86-LICENSE-3RD-PARTY.txt](licenses/texts/opencv-python-4.11.0.86-LICENSE-3RD-PARTY.txt), [OpenCV-4.11.0-COPYRIGHT.txt](licenses/texts/OpenCV-4.11.0-COPYRIGHT.txt), [OpenCV-ADE-0.1.2e-LICENSE.txt](licenses/texts/OpenCV-ADE-0.1.2e-LICENSE.txt), [FFmpeg-4.4.1-LICENSE.md.txt](licenses/texts/FFmpeg-4.4.1-LICENSE.md.txt), [FFmpeg-4.4.1-COPYING.LGPLv2.1.txt](licenses/texts/FFmpeg-4.4.1-COPYING.LGPLv2.1.txt), [libwebp-1.2.2-COPYING.txt](licenses/texts/libwebp-1.2.2-COPYING.txt), [libwebp-1.2.2-PATENTS.txt](licenses/texts/libwebp-1.2.2-PATENTS.txt), [libtiff-4.4.0-COPYRIGHT.txt](licenses/texts/libtiff-4.4.0-COPYRIGHT.txt), [libpng-1.6.39-LICENSE.txt](licenses/texts/libpng-1.6.39-LICENSE.txt), [MuPDF-thirdparty-libjpeg-9f-README.txt](licenses/texts/MuPDF-thirdparty-libjpeg-9f-README.txt), [zlib-1.3.1-LICENSE.txt](licenses/texts/zlib-1.3.1-LICENSE.txt)) | Copyright (C) 2000-2022, Intel Corporation, all rights reserved.; Copyright (C) 2009-2011, Willow Garage Inc., all rights reserved.; Copyright (C) 2009-2016, NVIDIA Corporation, all rights reserved.; Copyright (C) 2010-2013, Advanced Micro Devices, Inc., all rights reserved.; Copyright (C) 2015-2023, OpenCV Foundation, all rights reserved.; Copyright (C) 2008-2016, Itseez Inc., all rights reserved.; Copyright (C) 2019-2023, Xperience AI, all rights reserved.; Copyright (C) 2019-2022, Shenzhen Institute of Artificial Intelligence and Robotics for Society, all rights reserved.; Copyright (C) 2022-2023, Southern University of Science And Technology, all rights reserved.; Copyright (c) Olli-Pekka Heinisuo (opencv-python packaging, MIT) | https://files.pythonhosted.org/packages/17/06/68c27a523103dad5837dc5b87e71285280c4f098c60e4fe8a8db6486ab09/opencv-python-4.11.0.86.tar.gz (sha256 03d60ccae62304860d232272e4a4fda93c39d595780cb40b161b310244b736a4) |
| ↳ FFmpeg (libavcodec/libavformat/libavutil/libswscale, static; configured without --enable-gpl) | 4.4.1 (Lavc58.134.100, Lavf58.76.100) | LGPL-2.1-or-later | FFmpeg developers (see per-file headers) | https://github.com/FFmpeg/FFmpeg/archive/refs/tags/n4.4.1.tar.gz (sha256 82b43cc67296bcd01a59ae6b327cdb50121d3a9e35f41a30de1edd71bb4a6666) |
| ↳ protobuf (OpenCV 3rdparty, dnn) | 3.19.1 | BSD-3-Clause | Copyright 2008 Google Inc.  All rights reserved. | opencv 4.11.0 3rdparty/protobuf |
| ↳ flatbuffers (OpenCV builtin, dnn TFLite importer) | 23.5.9 | Apache-2.0 |  | opencv 4.11.0 3rdparty/flatbuffers |
| ↳ ADE (G-API graph library) | 0.1.2e | Apache-2.0 | Copyright (C) 2018 Intel Corporation | https://github.com/opencv/ade/archive/refs/tags/v0.1.2e.zip |
| ↳ libwebp (+webpmux, webpdemux) | 1.2.2 | BSD-3-Clause | Copyright (c) 2010, Google Inc. All rights reserved. | https://github.com/webmproject/libwebp/archive/refs/tags/v1.2.2.tar.gz |
| ↳ libtiff | 4.4.0 | libtiff | Copyright (c) 1988-1997 Sam Leffler; Copyright (c) 1991-1997 Silicon Graphics, Inc. | https://download.osgeo.org/libtiff/tiff-4.4.0.tar.gz |
| ↳ libjpeg (IJG, Emscripten port -sUSE_LIBJPEG) | 9f | IJG | Copyright (C) 2024, Thomas G. Lane, Guido Vollbeding | https://storage.googleapis.com/webassembly/emscripten-ports/jpegsrc.v9f.tar.gz (mirror of http://www.ijg.org/files/jpegsrc.v9f.tar.gz) |
| ↳ libpng (Emscripten port -sUSE_LIBPNG) | 1.6.39 | libpng-2.0 | Copyright (c) 1995-2022 The PNG Reference Library Authors.; Copyright (c) 2018-2022 Cosmin Truta.; Copyright (c) 2000-2002, 2004, 2006-2018 Glenn Randers-Pehrson.; Copyright (c) 1996-1997 Andreas Dilger.; Copyright (c) 1995-1996 Guy Eric Schalnat, Group 42, Inc. | https://storage.googleapis.com/webassembly/emscripten-ports/libpng-1.6.39.tar.gz |
| ↳ zlib (Emscripten port -sUSE_ZLIB) | 1.3.1 | Zlib | (C) 1995-2024 Jean-loup Gailly and Mark Adler | https://github.com/madler/zlib/archive/refs/tags/v1.3.1.tar.gz |
| OpenJPEG (in PDF.js) | 2.5.4 | BSD-2-Clause ([openjpeg-2.5.4--LICENSE.txt](licenses/texts/openjpeg-2.5.4--LICENSE.txt), [pdf.js.openjpeg-b47d31b8355a--LICENSE_PDFJS_OPENJPEG.txt](licenses/texts/pdf.js.openjpeg-b47d31b8355a--LICENSE_PDFJS_OPENJPEG.txt), [emscripten-4.0.15--LICENSE.txt](licenses/texts/emscripten-4.0.15--LICENSE.txt), [emscripten-4.0.15--musl-COPYRIGHT.txt](licenses/texts/emscripten-4.0.15--musl-COPYRIGHT.txt)) | Copyright (c) 2002-2014, Universite catholique de Louvain (UCL), Belgium; Copyright (c) 2002-2014, Professor Benoit Macq; Copyright (c) 2003-2014, Antonin Descampe; Copyright (c) 2003-2009, Francois-Olivier Devaux; Copyright (c) 2005, Herve Drolon, FreeImage Team; Copyright (c) 2002-2003, Yannick Verschueren; Copyright (c) 2001-2003, David Janssens; Copyright (c) 2011-2012, Centre National d'Etudes Spatiales (CNES), France; Copyright (c) 2012, CS Systemes d'Information, France; Copyright (c) 2024, Mozilla Foundation (pdf.js.openjpeg wrapper, LICENSE_PDFJS_OPENJPEG) | https://github.com/uclouvain/openjpeg/tree/6c4a29b00211eb0430fa0e5e890f1ce5c80f409f (tag v2.5.4) plus 0001-Add-support-for-buffer-based-stream-see-https-github.patch and src/ from https://github.com/mozilla/pdf.js.openjpeg/tree/b47d31b8355a3863ab37282ceeb5183f7ac2761c |
| ↳ Emscripten runtime and system libraries (JS glue, musl libc, compiler-rt parts) | unknown (emscripten/emsdk:latest on 2025-09-21, probably 4.0.15) | (MIT OR NCSA) AND MIT | Copyright (c) 2010-2014 Emscripten authors; musl: Copyright (c) 2005-2020 Rich Felker, et al. | https://github.com/emscripten-core/emscripten |
| PDF.js annotation viewer (modified by BentoPDF) | 4.3.136 | Apache-2.0 AND MPL-2.0 AND MIT AND BSD-2-Clause ([pdfjs-dist-5.5.207--LICENSE.txt](licenses/texts/pdfjs-dist-5.5.207--LICENSE.txt), [MPL-2.0.txt](licenses/texts/MPL-2.0.txt), [quickjs-2024-01-13--LICENSE.txt](licenses/texts/quickjs-2024-01-13--LICENSE.txt), [openjpeg-2.5.2--LICENSE.txt](licenses/texts/openjpeg-2.5.2--LICENSE.txt), [emscripten-4.0.15--LICENSE.txt](licenses/texts/emscripten-4.0.15--LICENSE.txt)) | Copyright 2023 Mozilla Foundation (header of build/pdf.mjs, pdf.worker.mjs, pdf.sandbox.mjs, web/viewer.mjs; pdfjsBuild 0cec64437); Copyright 2012 Mozilla Foundation (web/viewer.html); QuickJS: Copyright (c) 2017-2021 Fabrice Bellard; Copyright (c) 2017-2021 Charlie Gordon (pdf.sandbox.mjs); OpenJPEG 2.5.2 copyright holders (see pdfjs-openjpeg-wasm) (wasm embedded in pdf.worker.mjs) | https://github.com/mozilla/pdf.js/tree/0cec644372c38756474eb45c4e2aa0058960464a (tag v4.3.136); release zip https://github.com/mozilla/pdf.js/releases/download/v4.3.136/pdfjs-4.3.136-dist.zip; example copy https://github.com/Laomai-codefee/pdfjs-annotation-extension/tree/f3f120a7639b578b3fdecd347856a2f9b402ad9a/examples/pdfjs-4.3.136-dist; BentoPDF copy https://github.com/alam00000/bentopdf/tree/f96cd4e5166f3d51393dfe9f3c440b5bb77802f1/public/pdfjs-annotation-viewer |
| ↳ OpenJPEG (JPX decoder, wasm embedded base64 in build/pdf.worker.mjs) | 2.5.2 | BSD-2-Clause | see openjpeg-2.5.2--LICENSE.txt (UCL, Benoit Macq, Antonin Descampe, ... CS Systemes d'Information) | https://github.com/uclouvain/openjpeg/tree/v2.5.2 (pdf.js commit 2e83cfbbc16b "Add a jpx decoder based on OpenJPEG 2.5.2") |
| ↳ pdf.js.openjpeg wrapper | 393eed5fbaea (2024-05-14) | Apache-2.0 | Mozilla Foundation | https://github.com/mozilla/pdf.js.openjpeg/tree/393eed5fbaea512ea6bdfe1be6305d4add3c354c (Apache-2.0 until relicensed to BSD-2-Clause on 2024-06-04) |
| ↳ QuickJS (pdf.js scripting sandbox) | 2024-01-13 (3f81070e573e3592728dbbbd04c84c498b20d6dc) | MIT | Copyright (c) 2017-2021 Fabrice Bellard; Copyright (c) 2017-2021 Charlie Gordon | https://github.com/bellard/quickjs/tree/3f81070e573e3592728dbbbd04c84c498b20d6dc |
| ↳ Firefox/Photon icons with MPL-2.0 headers (web/images/annotation-paperclip.svg, annotation-pushpin.svg, toolbarButton-editorStamp.svg) | as in pdf.js 4.3.136 | MPL-2.0 | Mozilla (MPL-2.0 file header) | https://github.com/mozilla/pdf.js/tree/0cec644372c38756474eb45c4e2aa0058960464a/web/images |
| ↳ Emscripten runtime (OpenJPEG build) | unknown (2024-05) | MIT OR NCSA | Copyright (c) 2010-2014 Emscripten authors | https://github.com/emscripten-core/emscripten |
| PDF.js viewer (modified by BentoPDF) | 5.4.296 | Apache-2.0 AND MPL-2.0 AND MIT ([pdfjs-dist-5.5.207--LICENSE.txt](licenses/texts/pdfjs-dist-5.5.207--LICENSE.txt), [MPL-2.0.txt](licenses/texts/MPL-2.0.txt), [quickjs-2024-01-13--LICENSE.txt](licenses/texts/quickjs-2024-01-13--LICENSE.txt)) | Copyright 2024 Mozilla Foundation (header of pdf.mjs, pdf.worker.mjs, pdf.sandbox.mjs, viewer.mjs, pdf_viewer.mjs; pdfjsBuild f56dc8601); Copyright 2012 Mozilla Foundation (viewer.html); Copyright 2014 Mozilla Foundation (viewer.css); QuickJS: Copyright (c) 2017-2021 Fabrice Bellard; Copyright (c) 2017-2021 Charlie Gordon (compiled into pdf.sandbox.mjs) | https://github.com/mozilla/pdf.js/tree/f56dc86014bb00c5a239680df53d2010e9aad0f8 (tag v5.4.296); release zip https://github.com/mozilla/pdf.js/releases/download/v5.4.296/pdfjs-5.4.296-dist.zip; pdf_viewer.* from https://registry.npmjs.org/pdfjs-dist/-/pdfjs-dist-5.4.296.tgz; BentoPDF-modified copies: https://github.com/alam00000/bentopdf/tree/f96cd4e5166f3d51393dfe9f3c440b5bb77802f1/public/pdfjs-viewer |
| ↳ QuickJS (pdf.js scripting sandbox, via mozilla/pdf.js.quickjs) | 2024-01-13 (bellard/quickjs 3f81070e573e3592728dbbbd04c84c498b20d6dc) | MIT | Copyright (c) 2017-2021 Fabrice Bellard; Copyright (c) 2017-2021 Charlie Gordon | https://github.com/bellard/quickjs/tree/3f81070e573e3592728dbbbd04c84c498b20d6dc (pdf.js commit 275b6748b690 "Update quickjs to 3f81070e...") |
| ↳ Firefox/Photon icons with MPL-2.0 headers (images/altText_spinner.svg, annotation-paperclip.svg, annotation-pushpin.svg, toolbarButton-editorStamp.svg) | as in pdf.js 5.4.296 | MPL-2.0 | Mozilla (MPL-2.0 file header, no copyright line) | https://github.com/mozilla/pdf.js/tree/f56dc86014bb00c5a239680df53d2010e9aad0f8/web/images |
| pdf2docx | 0.5.8 | GPL-3.0-only ([pdf2docx-0.5.8-LICENSE.txt](licenses/texts/pdf2docx-0.5.8-LICENSE.txt)) | No copyright line in the 0.5.8 distribution; METADATA author: Artifex <support@artifex.com> (project originally by dothinking) | https://files.pythonhosted.org/packages/b5/f9/6d567df395c0409baf2b4dd9cd30d1e977c70672fe7ec2a684af1e6aa41c/pdf2docx-0.5.8-py3-none-any.whl; git https://github.com/ArtifexSoftware/pdf2docx/tree/v0.5.8 (f30fb2bbbd90aa9aaed1d79b9aaad8979cbde47c) |
| pdfjs-annotation-extension | 2.2.0 | Apache-2.0 ([pdfjs-annotation-extension-2.2.0--LICENSE.txt](licenses/texts/pdfjs-annotation-extension-2.2.0--LICENSE.txt), [pdfjs-annotation-extension-2.2.0--bundled-third-party-notices.txt](licenses/texts/pdfjs-annotation-extension-2.2.0--bundled-third-party-notices.txt), [Zlib.txt](licenses/texts/Zlib.txt)) | No copyright line stated upstream (LICENSE is the plain Apache-2.0 text with the unfilled appendix); author: Laomai (GitHub Laomai-codefee) | https://github.com/Laomai-codefee/pdfjs-annotation-extension/tree/f3f120a7639b578b3fdecd347856a2f9b402ad9a (tag v2.2.0); release build https://github.com/Laomai-codefee/pdfjs-annotation-extension/releases/download/v2.2.0/pdfjs-annotation-extension-v2.2.0-dist.zip |
| ↳ react | 18.3.1 | MIT | Copyright (c) Facebook, Inc. and its affiliates. | https://registry.npmjs.org/react/-/react-18.3.1.tgz |
| ↳ react-dom (+ scheduler 0.23.2) | 18.3.1 | MIT | Copyright (c) Facebook, Inc. and its affiliates. | https://registry.npmjs.org/react-dom/-/react-dom-18.3.1.tgz |
| ↳ antd (+ ~55 rc-*/@ant-design/*/@rc-component/* packages, @babel/runtime, classnames, stylis, @emotion/hash, ...) | 5.26.2 (inferred) | MIT | Copyright (c) 2015-present Ant UED, https://xtech.antfin.com/ (and the sub-packages' own lines, see notices file) | https://registry.npmjs.org/antd/-/antd-5.26.2.tgz |
| ↳ konva | 9.3.20 | MIT | Original work Copyright (C) 2011 - 2013 by Eric Rowell (KineticJS); Modified work Copyright (C) 2014 - present by Anton Lavrenov (Konva) | https://registry.npmjs.org/konva/-/konva-9.3.20.tgz |
| ↳ i18next / react-i18next (+ html-parse-stringify, void-elements) | 23.16.8 / 15.5.3 (inferred) | MIT | Copyright (c) 2024 i18next (i18next 23.16.8); Copyright (c) 2025 i18next (react-i18next 15.5.3) | https://registry.npmjs.org/i18next/-/i18next-23.16.8.tgz ; https://registry.npmjs.org/react-i18next/-/react-i18next-15.5.3.tgz |
| ↳ exceljs (its prebuilt browser bundle dist/exceljs.min.js "ExcelJS 19-10-2023") | 4.4.0 | MIT | Copyright (c) 2014-2019 Guyon Roche | https://registry.npmjs.org/exceljs/-/exceljs-4.4.0.tgz |
| ↳ modules inside the ExcelJS browser bundle: jszip 3.10.1 (MIT OR GPL-3.0-or-later; with pako 1.0.x MIT AND Zlib, lie, immediate, setimmediate), core-js 3.33.0, regenerator-runtime, dayjs, saxes (ISC), xmlchars, uuid, @fast-csv/*, lodash.*, readable-stream, buffer, ieee754 (BSD-3-Clause), crypto-browserify with elliptic 6.5.4, bn.js, sha.js (MIT AND BSD-3-Clause), parse-asn1 (ISC), inherits (ISC), minimalistic-assert (ISC), browserify-sign (ISC) and other browserify shims | as built 2023-10-19 (versions inferred except those stated) | MIT AND ISC AND BSD-3-Clause AND Zlib AND (MIT OR GPL-3.0-or-later) | see pdfjs-annotation-extension-2.2.0--bundled-third-party-notices.txt part B | https://github.com/exceljs/exceljs/tree/v4.4.0 (Gruntfile/browserify build) |
| ↳ pdf-lib (+ pako 1.0.11 (MIT AND Zlib), tslib 1.14.1 (0BSD), @pdf-lib/standard-fonts, @pdf-lib/upng) | 1.17.1 | MIT AND Zlib AND 0BSD | Copyright (c) 2019 Andrew Dillon; pako: Copyright (C) 2014-2017 by Vitaly Puzrin and Andrei Tuputcyn; tslib: Copyright (c) Microsoft Corporation. | https://registry.npmjs.org/pdf-lib/-/pdf-lib-1.17.1.tgz |
| ↳ dayjs | 1.11.13 (inferred) | MIT | Copyright (c) 2018-present, iamkun | https://registry.npmjs.org/dayjs/-/dayjs-1.11.13.tgz |
| ↳ web-highlighter | 0.7.4 | MIT | Copyright (c) 2018 Alien ZHOU | https://registry.npmjs.org/web-highlighter/-/web-highlighter-0.7.4.tgz |
| ↳ @floating-ui/dom (+ core, utils) | 1.7.1 (inferred) | MIT | Copyright (c) 2021-present Floating UI contributors | https://registry.npmjs.org/@floating-ui/dom/-/dom-1.7.1.tgz |
| ↳ nanoid / file-saver | 5.1.5 (inferred) / 2.0.5 | MIT | Copyright 2017 Andrey Sitnik <andrey@sitnik.ru>; Copyright © 2016 Eli Grey | https://registry.npmjs.org/nanoid/-/nanoid-5.1.5.tgz ; https://registry.npmjs.org/file-saver/-/file-saver-2.0.5.tgz |
| ↳ webpack runtime, css-loader and style-loader runtime | webpack 5 (unknown) | MIT | Copyright JS Foundation and other contributors | https://github.com/webpack/webpack |
| ↳ 12 default stamp PNGs (Approved, Closed, Completed, Draft, OK, Paid, Received, Certified, Success, Urgent, Verified, Void; 640 px) embedded as data: URIs by BentoPDF | n/a | NOASSERTION | unknown | unknown (not in the upstream extension; look like stock clip-art, e.g. Pixabay/OpenClipart - unverified) |
| PyMuPDF for WebAssembly (@bentopdf/pymupdf-wasm) | 0.11.16 | AGPL-3.0-only ([bentopdf-pymupdf-wasm-0.11.16-LICENSE.txt](licenses/texts/bentopdf-pymupdf-wasm-0.11.16-LICENSE.txt)) | PyMuPDF is copyright © Artifex Software, Inc. (README attribution); package.json author: BentoPDF; contributors: Artifex Software, Inc. | npm https://registry.npmjs.org/@bentopdf/pymupdf-wasm/-/pymupdf-wasm-0.11.16.tgz (gitHead f82b32b8d183f07e277acf1a82704115c34841ba); https://github.com/alam00000/bentopdf-pymupdf-wasm (src/*.ts for dist/index.js) |
| PyMuPDF4LLM | 0.0.27 | AGPL-3.0-or-later ([pymupdf4llm-0.0.27-LICENSE.txt](licenses/texts/pymupdf4llm-0.0.27-LICENSE.txt)) | Copyright (C) 2024-2025 Artifex Software, Inc. | https://files.pythonhosted.org/packages/e9/c8/7eed2e902b61574b15b295017ddb5738c4970aa9ab76903fbaace28a522e/pymupdf4llm-0.0.27-py3-none-any.whl; git https://github.com/pymupdf/RAG/tree/v0.0.27 (b7e6e905480f1d346febc6db0f19160ee1d8e90f) |
| Python (CPython) | 3.13.2 | PSF-2.0 ([CPython-3.13.2-LICENSE.txt](licenses/texts/CPython-3.13.2-LICENSE.txt), [CPython-3.13.2-Doc-license.rst.txt](licenses/texts/CPython-3.13.2-Doc-license.rst.txt)) | Copyright (c) 2001-2024 Python Software Foundation; All Rights Reserved; Copyright (c) 1995-2001 Corporation for National Research Initiatives; All Rights Reserved.; Copyright (c) 1991 - 1995, Stichting Mathematisch Centrum Amsterdam, The Netherlands.  All rights reserved. | https://www.python.org/ftp/python/3.13.2/Python-3.13.2.tgz (tag v3.13.2) + Pyodide patches in pyodide cpython/patches at ed567eb8d2b41fb0e325927c44466b866ef56a34 |
| ↳ expat (bundled in CPython Modules/expat) | 2.6.4 | MIT | see CPython Doc/license.rst "expat" section | CPython v3.13.2 Modules/expat |
| ↳ libmpdec (mpdecimal, bundled) | 2.5.1 | BSD-2-Clause | see CPython Doc/license.rst "libmpdec" section | CPython v3.13.2 Modules/_decimal/libmpdec |
| ↳ HACL* (bundled hash implementations) | as vendored in 3.13.2 | MIT | see CPython Doc/license.rst "Hashing" / Modules/_hacl | CPython v3.13.2 Modules/_hacl |
| ↳ other incorporated software listed in Doc/license.rst (Mersenne Twister, dtoa/strtod, SipHash, BLAKE2 reference code, ...) | 3.13.2 | various permissive |  | CPython v3.13.2 Doc/license.rst |
| python-docx | 1.2.0 | MIT ([python-docx-1.2.0-LICENSE.txt](licenses/texts/python-docx-1.2.0-LICENSE.txt)) | Copyright (c) 2013 Steve Canny, https://github.com/scanny | https://files.pythonhosted.org/packages/d0/00/1e03a4989fa5795da308cd774f05b704ace555a70f9bf9d3be057b680bcf/python_docx-1.2.0-py3-none-any.whl; git tag v1.2.0 |
| qcms (in PDF.js) | 0.3.0 | MIT AND BSD-2-Clause ([qcms-0.3.0--LICENSE_QCMS.txt](licenses/texts/qcms-0.3.0--LICENSE_QCMS.txt), [pdf.js.qcms-fc23a407f1ed--LICENSE_PDFJS_QCMS.txt](licenses/texts/pdf.js.qcms-fc23a407f1ed--LICENSE_PDFJS_QCMS.txt), [rust-1.87.0--LICENSE-MIT.txt](licenses/texts/rust-1.87.0--LICENSE-MIT.txt), [rust-1.87.0--COPYRIGHT.txt](licenses/texts/rust-1.87.0--COPYRIGHT.txt), [once_cell-1.21.3--LICENSE-MIT.txt](licenses/texts/once_cell-1.21.3--LICENSE-MIT.txt), [wasm-bindgen-0.2.100--LICENSE-MIT.txt](licenses/texts/wasm-bindgen-0.2.100--LICENSE-MIT.txt), [Apache-2.0.txt](licenses/texts/Apache-2.0.txt)) | qcms: Copyright (C) 2009-2024 Mozilla Corporation; qcms: Copyright (C) 1998-2007 Marti Maria; pdf.js.qcms wrapper: Copyright (c) 2025, Mozilla Foundation (LICENSE_PDFJS_QCMS, BSD-2-Clause as shipped by pdf.js); Rust standard library: Copyright (c) The Rust Project Contributors; wasm-bindgen: Copyright (c) 2014 Alex Crichton | qcms crate 0.3.0 https://crates.io/api/v1/crates/qcms/0.3.0/download ; wrapper https://github.com/mozilla/pdf.js.qcms/tree/fc23a407f1ed9ccfea15875d27e0936dcc798a1f |
| ↳ qcms | 0.3.0 | MIT | Copyright (C) 2009-2024 Mozilla Corporation; Copyright (C) 1998-2007 Marti Maria | https://crates.io/crates/qcms/0.3.0 |
| ↳ once_cell | 1.21.3 | MIT OR Apache-2.0 | no copyright line in LICENSE-MIT (Aleksey Kladov and contributors) | https://github.com/matklad/once_cell/tree/v1.21.3 |
| ↳ wasm-bindgen (runtime part) | 0.2.100 | MIT OR Apache-2.0 | Copyright (c) 2014 Alex Crichton | https://github.com/rustwasm/wasm-bindgen/tree/0.2.100 |
| ↳ Rust core/alloc/std (incl. dlmalloc allocator) | rustc 1.87.0 (17067e9ac 2025-05-09) | MIT OR Apache-2.0 | Copyright (c) The Rust Project Contributors | https://github.com/rust-lang/rust/tree/1.87.0 |
| tesseract.js (worker) | 7.0.0 | Apache-2.0 ([tesseract.js-7.0.0--LICENSE.md.txt](licenses/texts/tesseract.js-7.0.0--LICENSE.md.txt), [Apache-2.0.txt](licenses/texts/Apache-2.0.txt), [tesseract.js-7.0.0--worker.min.js.LICENSE.txt](licenses/texts/tesseract.js-7.0.0--worker.min.js.LICENSE.txt), [regenerator-runtime-0.13.11--LICENSE.txt](licenses/texts/regenerator-runtime-0.13.11--LICENSE.txt), [zlibjs-0.3.1--LICENSE.txt](licenses/texts/zlibjs-0.3.1--LICENSE.txt), [wasm-feature-detect-1.8.0--LICENSE.txt](licenses/texts/wasm-feature-detect-1.8.0--LICENSE.txt), [bmp-js-0.1.0--LICENSE.txt](licenses/texts/bmp-js-0.1.0--LICENSE.txt), [is-url-1.2.4--LICENSE-MIT.txt](licenses/texts/is-url-1.2.4--LICENSE-MIT.txt), [buffer-6.0.3--LICENSE.txt](licenses/texts/buffer-6.0.3--LICENSE.txt), [base64-js-1.5.1--LICENSE.txt](licenses/texts/base64-js-1.5.1--LICENSE.txt), [ieee754-1.2.1--LICENSE.txt](licenses/texts/ieee754-1.2.1--LICENSE.txt), [idb-keyval-6.2.1--LICENCE.txt](licenses/texts/idb-keyval-6.2.1--LICENCE.txt), [webpack-5.98.0--LICENSE.txt](licenses/texts/webpack-5.98.0--LICENSE.txt)) | No copyright line stated upstream (LICENSE.md is the unfilled Apache-2.0 text); project naptha/tesseract.js, contributors per package.json: jeromewu | https://github.com/naptha/tesseract.js/tree/v7.0.0 (tag object b5cff0bca691a99ff69f1b162184e6c5a78629ef -> commit 42eae669e4b3a66429d8516f078912cc747a89df); npm tarball https://registry.npmjs.org/tesseract.js/-/tesseract.js-7.0.0.tgz (contains src/ and the webpack config) |
| ↳ regenerator-runtime | 0.13.11 | MIT | Copyright (c) 2014-present, Facebook, Inc. | https://registry.npmjs.org/regenerator-runtime/-/regenerator-runtime-0.13.11.tgz (github.com/facebook/regenerator, packages/runtime) |
| ↳ zlibjs (bin/node-zlib.js: gunzip) | 0.3.1 | MIT | Copyright (c) 2012 imaya | https://registry.npmjs.org/zlibjs/-/zlibjs-0.3.1.tgz (github.com/imaya/zlib.js) |
| ↳ wasm-feature-detect | 1.8.0 | Apache-2.0 | Copyright 2017 Google Inc. | https://registry.npmjs.org/wasm-feature-detect/-/wasm-feature-detect-1.8.0.tgz (github.com/GoogleChromeLabs/wasm-feature-detect) |
| ↳ bmp-js | 0.1.0 | MIT | Copyright (c) 2014 @丝刀口 | https://registry.npmjs.org/bmp-js/-/bmp-js-0.1.0.tgz (github.com/shaozilee/bmp-js) |
| ↳ is-url | 1.2.4 | MIT | No copyright line in the package's LICENSE-MIT (package by Segment, github.com/segmentio/is-url) | https://registry.npmjs.org/is-url/-/is-url-1.2.4.tgz (github.com/segmentio/is-url) |
| ↳ buffer | 6.0.3 | MIT | Copyright (c) Feross Aboukhadijeh, and other contributors. | https://registry.npmjs.org/buffer/-/buffer-6.0.3.tgz (github.com/feross/buffer) |
| ↳ base64-js | 1.5.1 | MIT | Copyright (c) 2014 Jameson Little | https://registry.npmjs.org/base64-js/-/base64-js-1.5.1.tgz (github.com/beatgammit/base64-js) |
| ↳ ieee754 | 1.2.1 | BSD-3-Clause | Copyright 2008 Fair Oaks Labs, Inc. | https://registry.npmjs.org/ieee754/-/ieee754-1.2.1.tgz (github.com/feross/ieee754) |
| ↳ idb-keyval | 6.2.1 | Apache-2.0 | Copyright 2016, Jake Archibald | https://registry.npmjs.org/idb-keyval/-/idb-keyval-6.2.1.tgz (github.com/jakearchibald/idb-keyval) |
| ↳ webpack runtime (module bootstrap code emitted by webpack) | 5.98.0 | MIT | Copyright JS Foundation and other contributors | https://registry.npmjs.org/webpack/-/webpack-5.98.0.tgz (github.com/webpack/webpack) |
| typing_extensions | 4.12.2 | PSF-2.0 ([typing_extensions-4.12.2-LICENSE.txt](licenses/texts/typing_extensions-4.12.2-LICENSE.txt)) | Copyright (c) 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023 Python Software Foundation; All Rights Reserved | https://files.pythonhosted.org/packages/26/9f/ad63fc0248c5379346306f8668cda6e2e2e9c95e01216d2b8ffd9ff037d0/typing_extensions-4.12.2-py3-none-any.whl (as re-published by Pyodide 0.28.0a3); git tag 4.12.2 |

## Data and fonts

| Component | Version | License | Copyright | Source |
| --- | --- | --- | --- | --- |
| Adobe CMaps (in PDF.js) | 2014-03-17 | BSD-3-Clause ([adobe-cmap-resources-pdf.js-bcmaps-2014--LICENSE.txt](licenses/texts/adobe-cmap-resources-pdf.js-bcmaps-2014--LICENSE.txt)) | Copyright 1990-2009 Adobe Systems Incorporated. All rights reserved. (cmaps/LICENSE); Copyright 1990-2015 Adobe Systems Incorporated. (as quoted in pdf.js viewer.html) | Converted files: https://github.com/mozilla/pdf.js/tree/f56dc86014bb00c5a239680df53d2010e9aad0f8/external/bcmaps (added in pdf.js commit 734d6f346e1f, 2014-03-17); upstream data: https://github.com/adobe-type-tools/cmap-resources (revision used in 2014 not recorded) |
| Alef (in LibreOffice) | 1.001 | OFL-1.1 ([SPDX-OFL-1.1.txt](licenses/texts/SPDX-OFL-1.1.txt), [LibreOffice-24.8-LICENSE.txt](licenses/texts/LibreOffice-24.8-LICENSE.txt)) | Copyright (c) 2012, HaGilda & Mushon Zer-Aviv (<http://hagilda.com\|info@hagilda.com>), with Reserved Font Name Alef Regular.; Copyright (c) 2012, HaGilda & Mushon Zer-Aviv (<http://hagilda.com\|info@hagilda.com>), with Reserved Font Name Alef Bold. | https://dev-www.libreoffice.org/src/alef-1.001.tar.gz |
| Alex Brush (signature font) | 1.111 | OFL-1.1 ([alex-brush-1.111--OFL.txt](licenses/texts/alex-brush-1.111--OFL.txt)) | Copyright 2011 The Alex Brush Project Authors (https://github.com/googlefonts/alex-brush) | https://github.com/google/fonts/tree/23e54b51ddffbc7713c583748e3bd86f62b1fa4a/ofl/alexbrush (same version as shipped; the shipped file is not byte-identical, see notes) |
| Allura (signature font) | 1.110 | OFL-1.1 ([allura-1.110--OFL.txt](licenses/texts/allura-1.110--OFL.txt)) | Copyright 2010 The Allura Project Authors (https://github.com/googlefonts/allura) | https://github.com/google/fonts/tree/23e54b51ddffbc7713c583748e3bd86f62b1fa4a/ofl/allura (same version as shipped; the shipped file is not byte-identical, see notes) |
| Amiri (in LibreOffice) | 1.001 | OFL-1.1 ([SPDX-OFL-1.1.txt](licenses/texts/SPDX-OFL-1.1.txt)) | Copyright 2010-2022 The Amiri Project Authors (https://github.com/aliftype/amiri). | https://dev-www.libreoffice.org/src/Amiri-1.001.zip |
| Caladea (in LibreOffice) | 1.002 | Apache-2.0 ([SPDX-Apache-2.0.txt](licenses/texts/SPDX-Apache-2.0.txt)) | Copyright (c) 2012 Huerta Tipografia | https://dev-www.libreoffice.org/src/368f114c078f94214a308a74c7e991bc-crosextrafonts-20130214.tar.gz |
| Carlito (in LibreOffice) | 1.103 | OFL-1.1 ([SPDX-OFL-1.1.txt](licenses/texts/SPDX-OFL-1.1.txt)) | Copyright (c) 2010-2013 by tyPoland Lukasz Dziedzic with Reserved Font Name "Carlito". | https://dev-www.libreoffice.org/src/c74b7223abe75949b4af367942d96c7a-crosextrafonts-carlito-20130920.tar.gz |
| Cedarville Cursive (font, Fontsource) | 1.001 | OFL-1.1 ([fontsource-cedarville-cursive-5.2.7--LICENSE.txt](licenses/texts/fontsource-cedarville-cursive-5.2.7--LICENSE.txt), [OFL-1.1.txt](licenses/texts/OFL-1.1.txt)) | Copyright (c) 2010, Kimberly Geswein (kimberlygeswein.com kimberlygeswein@gmail.com) | https://registry.npmjs.org/@fontsource/cedarville-cursive/-/cedarville-cursive-5.2.7.tgz (exact files); font sources: https://github.com/google/fonts/tree/main/ofl/cedarvillecursive |
| CGATS001Compat ICC profile (in PDF.js) | bdd8466 | CC0-1.0 ([CC0-1.0.txt](licenses/texts/CC0-1.0.txt)) | none (CC0 public-domain dedication; author Clinton Ingram / saucecontrol) | https://github.com/saucecontrol/Compact-ICC-Profiles/blob/bdd84663061bc4ae95ca70decff54f581e27f702/profiles/CGATS001Compat-v2-micro.icc |
| Culmus Hebrew fonts (in LibreOffice) | 0.133 | GPL-2.0-only ([Culmus-0.133-LICENSE.txt](licenses/texts/Culmus-0.133-LICENSE.txt), [Culmus-0.133-LICENSE-BITSTREAM.txt](licenses/texts/Culmus-0.133-LICENSE-BITSTREAM.txt), [Culmus-0.133-GNU-GPL-2.0.txt](licenses/texts/Culmus-0.133-GNU-GPL-2.0.txt)) | Copyright 2002-2018 by Maxim Iorsh (iorsh@users.sourceforge.net). Distributed under the terms of GNU General Public License version 2. Latin glyphs and part of punctuation copyright 1990 as an unpublished work by Bitstream Inc. All rights reserved. (David CLM); Copyright (c) 2002-2011 by Maxim Iorsh. Latin glyphs, digits and punctuation: portions of Century Schoolbook L ver. 1.06 Copyright (URW)++, Copyright 1999 by (URW)++ Design & Development. (Frank Ruehl CLM); Copyright 2004-2010 by Maxim Iorsh. All rights reserved. (Miriam CLM); Copyright 2002-2010 by Maxim Iorsh. Hebrew vowel marks positioning algorithms implementation by Yoram Gnat 2010. Latin glyphs, digits and punctuation Copyright (URW)++, Copyright 1999 by (URW)++ Design & Development. (Miriam Mono CLM); Copyright (c) 2002-2017 by Maxim Iorsh. Latin glyphs, digits and punctuation copyright 1999 by (URW)++ Design & Development. (Nachlieli CLM); (c) Copyright 1989-1992, Bitstream Inc., Cambridge, MA. (Bitstream Charter portions, see LICENSE-BITSTREAM) | https://dev-www.libreoffice.org/src/culmus-0.133.tar.gz (sha256 c0c6873742d07544f6bacf2ad52eb9cb392974d56427938dc1dfbc8399c64d05) |
| Dancing Script (font, Fontsource) | 2.001 | OFL-1.1 ([fontsource-dancing-script-5.2.8--LICENSE.txt](licenses/texts/fontsource-dancing-script-5.2.8--LICENSE.txt), [OFL-1.1.txt](licenses/texts/OFL-1.1.txt)) | Copyright 2016 The Dancing Script Project Authors (https://github.com/googlefonts/DancingScript), with Reserved Font Name 'Dancing Script'. | https://registry.npmjs.org/@fontsource/dancing-script/-/dancing-script-5.2.8.tgz (exact files); font sources: https://github.com/googlefonts/DancingScript |
| DejaVu fonts (in LibreOffice) | 2.37 | Bitstream-Vera AND LicenseRef-Arev AND LicenseRef-Public-Domain ([DejaVu-2.37-LICENSE.txt](licenses/texts/DejaVu-2.37-LICENSE.txt)) | Copyright (c) 2003 by Bitstream, Inc. All Rights Reserved. Bitstream Vera is a trademark of Bitstream, Inc.; Copyright (c) 2006 by Tavmjong Bah. All Rights Reserved.; DejaVu changes are in public domain; math extensions (TeX Gyre DJV Math by B. Jackowski, P. Strzelczyk, P. Pianowski) are in public domain; letters from Euler Fraktur (AMSfonts) are (c) American Mathematical Society | https://dev-www.libreoffice.org/src/33e1e61fab06a547851ed308b4ffef42-dejavu-fonts-ttf-2.37.zip |
| DM Sans (font, Fontsource) | 4.004 | OFL-1.1 ([fontsource-dm-sans-5.2.8--LICENSE.txt](licenses/texts/fontsource-dm-sans-5.2.8--LICENSE.txt), [OFL-1.1.txt](licenses/texts/OFL-1.1.txt)) | Copyright 2014 The DM Sans Project Authors (https://github.com/googlefonts/dm-fonts) | https://registry.npmjs.org/@fontsource/dm-sans/-/dm-sans-5.2.8.tgz (exact files); font sources: https://github.com/googlefonts/dm-fonts |
| Foxit standard fonts (in PDF.js) | pdf.js 5.4.296 | BSD-3-Clause ([pdf.js-5.4.296--LICENSE_FOXIT.txt](licenses/texts/pdf.js-5.4.296--LICENSE_FOXIT.txt)) | Copyright 2014 PDFium Authors. All rights reserved.; Original code copyright 2014 Foxit Software Inc. http://www.foxitsoftware.com (pdf.js external/standard_fonts/README.md) | https://github.com/mozilla/pdf.js/tree/f56dc86014bb00c5a239680df53d2010e9aad0f8/external/standard_fonts (extracted from PDFium) |
| Gentium Basic fonts (in LibreOffice) | 1.102 | OFL-1.1 ([SPDX-OFL-1.1.txt](licenses/texts/SPDX-OFL-1.1.txt)) | Copyright (c) 2003-2013, SIL International (http://www.sil.org/) with Reserved Font Names "Gentium" and "SIL". | https://dev-www.libreoffice.org/src/1725634df4bb3dcb1b2c91a6175f8789-GentiumBasic_1102.zip |
| Great Vibes (font, Fontsource) | 1.103 | OFL-1.1 ([fontsource-great-vibes-5.2.8--LICENSE.txt](licenses/texts/fontsource-great-vibes-5.2.8--LICENSE.txt), [OFL-1.1.txt](licenses/texts/OFL-1.1.txt)) | Copyright 2010 The Great Vibes Pro Project Authors (https://github.com/googlefonts/great-vibes) | https://registry.npmjs.org/@fontsource/great-vibes/-/great-vibes-5.2.8.tgz (exact files); font sources: https://github.com/googlefonts/great-vibes |
| Handlee (signature font) | 1.001 | OFL-1.1 ([handlee-1.001--OFL.txt](licenses/texts/handlee-1.001--OFL.txt)) | Copyright (c) 2011, Admix Designs (http://www.admixdesigns.com/) with Reserved Font Name Handlee. (font name table); Copyright (c) 2011, Joe Prince, Vissol Ltd. (http://www.vissol.co.uk/mavenpro/) with Reserved Font Name "Handlee". (OFL.txt in google/fonts) | https://github.com/google/fonts/tree/23e54b51ddffbc7713c583748e3bd86f62b1fa4a/ofl/handlee (same version as shipped; the shipped file is not byte-identical, see notes) |
| Kalam (font, Fontsource) | 2.001 | OFL-1.1 ([fontsource-kalam-5.2.8--LICENSE.txt](licenses/texts/fontsource-kalam-5.2.8--LICENSE.txt), [OFL-1.1.txt](licenses/texts/OFL-1.1.txt)) | Copyright (c) 2014 Indian Type Foundry (info@indiantypefoundry.com) | https://registry.npmjs.org/@fontsource/kalam/-/kalam-5.2.8.tgz (exact files); font sources: https://github.com/google/fonts/tree/main/ofl/kalam (Indian Type Foundry) |
| Kalam (signature font) | 2.001 | OFL-1.1 ([kalam-2.001--OFL.txt](licenses/texts/kalam-2.001--OFL.txt)) | Copyright (c) 2014 Indian Type Foundry (info@indiantypefoundry.com) | https://github.com/google/fonts/tree/23e54b51ddffbc7713c583748e3bd86f62b1fa4a/ofl/kalam (same version as shipped; the shipped file is not byte-identical, see notes) |
| Lato (font, Fontsource) | 1.104 | OFL-1.1 ([fontsource-lato-5.2.7--LICENSE.txt](licenses/texts/fontsource-lato-5.2.7--LICENSE.txt), [OFL-1.1.txt](licenses/texts/OFL-1.1.txt)) | Copyright (c) 2010-2011 by tyPoland Lukasz Dziedzic (team@latofonts.com) with Reserved Font Name "Lato". Licensed under the SIL Open Font License, Version 1.1. | https://registry.npmjs.org/@fontsource/lato/-/lato-5.2.7.tgz (exact files); font sources: https://github.com/google/fonts/tree/main/ofl/lato |
| Liberation fonts (in LibreOffice) | 2.1.5 | OFL-1.1 ([SPDX-OFL-1.1.txt](licenses/texts/SPDX-OFL-1.1.txt)) | Digitized data copyright (c) 2010 Google Corporation.; Copyright (c) 2012 Red Hat, Inc. | https://dev-www.libreoffice.org/src/liberation-fonts-ttf-2.1.5.tar.gz |
| Liberation Sans 1.07 (in PDF.js) | 1.07.4 | GPL-2.0-only WITH Font-exception-2.0 ([liberation-fonts-1.07.4--License.txt](licenses/texts/liberation-fonts-1.07.4--License.txt), [GPL-2.0.txt](licenses/texts/GPL-2.0.txt)) | Copyright (c) 2007 Red Hat, Inc. All rights reserved. LIBERATION is a trademark of Red Hat, Inc. (font name table); Copyright © 2007-2011 Red Hat, Inc. All rights reserved. LIBERATION is a trademark of Red Hat, Inc. (License.txt of the 1.07.4 release) | Font sources: https://releases.pagure.org/liberation-fonts/liberation-fonts-1.07.4.tar.gz (binaries: liberation-fonts-ttf-1.07.4.tar.gz); files as shipped: https://github.com/mozilla/pdf.js/tree/f56dc86014bb00c5a239680df53d2010e9aad0f8/external/standard_fonts |
| Liberation Sans Narrow (in LibreOffice) | 1.07.5 | GPL-2.0-only WITH Font-exception-2.0 ([LiberationSansNarrow-1.07.6-License.txt](licenses/texts/LiberationSansNarrow-1.07.6-License.txt), [LiberationSansNarrow-1.07.6-COPYING-GPL-2.0.txt](licenses/texts/LiberationSansNarrow-1.07.6-COPYING-GPL-2.0.txt)) | Copyright 2010 Oracle and/or its affiliates; Copyright © 2007-2011 Red Hat, Inc. All rights reserved. LIBERATION is a trademark of Red Hat, Inc. | https://dev-www.libreoffice.org/src/liberation-narrow-fonts-ttf-1.07.6.tar.gz (sha256 8879d89b5ff7b506c9fc28efc31a5c0b954bbe9333e66e5283d27d20a8519ea3) |
| Libre Hebrew fonts (in LibreOffice) | 1.0 | OFL-1.1 ([SPDX-OFL-1.1.txt](licenses/texts/SPDX-OFL-1.1.txt)) | Copyright (c) 2003–2016 The David Libre Project Authors.; Copyright 2015 The Frank Ruhl Hofshi Project Authors.; Copyright 2016 Michal Sahar. All rights reserved.; Copyright (c) 2015 by Hubert & Fischer. All rights reserved. Hebrew characters (c) 2016 by Meir Sadan. | https://dev-www.libreoffice.org/src/libre-hebrew-1.0.tar.gz |
| Linux Libertine G and Biolinum G (in LibreOffice) | 5.1.3 | GPL-2.0-only WITH Font-exception-2.0 OR OFL-1.0 ([SPDX-OFL-1.0.txt](licenses/texts/SPDX-OFL-1.0.txt), [SPDX-GPL-2.0-only.txt](licenses/texts/SPDX-GPL-2.0-only.txt), [SPDX-Font-exception-2.0.txt](licenses/texts/SPDX-Font-exception-2.0.txt)) | Copyright (c) 2003-2006, Philipp H. Poll (http://linuxlibertine.sf.net/). All Rights Reserved.; "Linux Libertine" is a Reserved Font Name for this Font Software.; Graphite extension of the original Linux Libertine font was made by Laszlo Nemeth under the same license. | https://dev-www.libreoffice.org/src/e7a384790b13c29113e22e596ade9687-LinLibertineG-20120116.zip |
| Merriweather (font, Fontsource) | 2.100 | OFL-1.1 ([fontsource-merriweather-5.2.11--LICENSE.txt](licenses/texts/fontsource-merriweather-5.2.11--LICENSE.txt), [OFL-1.1.txt](licenses/texts/OFL-1.1.txt)) | Copyright 2024 The Merriweather Project Authors (https://github.com/EbenSorkin/Merriweather4) with Reserved Font Name "Merriweather". | https://registry.npmjs.org/@fontsource/merriweather/-/merriweather-5.2.11.tgz (exact files); font sources: https://github.com/EbenSorkin/Merriweather4 |
| Noto fonts (in LibreOffice) | 2.015 and others | OFL-1.1 ([SPDX-OFL-1.1.txt](licenses/texts/SPDX-OFL-1.1.txt)) | Copyright 2022 The Noto Project Authors (https://github.com/notofonts/latin-greek-cyrillic); Copyright 2022 The Noto Project Authors (https://github.com/notofonts/arabic); Copyright 2019-2022 Google LLC. All Rights Reserved. (Noto Kufi Arabic); Copyright 2024 The Noto Project Authors (https://github.com/notofonts/hebrew); Copyright 2022 The Noto Project Authors (https://github.com/notofonts/hebrew); Copyright 2022 The Noto Project Authors (https://github.com/notofonts/armenian); Copyright 2022 The Noto Project Authors (https://github.com/notofonts/georgian); Copyright 2022 The Noto Project Authors (https://github.com/notofonts/lao); Copyright 2022 The Noto Project Authors (https://github.com/notofonts/lisu) | https://dev-www.libreoffice.org/src/{NotoSans-v2.015,NotoSerif-v2.015,NotoKufiArabic-v2.109,NotoNaskhArabic-v2.019,NotoSansArabic-v2.010,NotoSansHebrew-v3.001,NotoSerifHebrew-v2.004,NotoSansArmenian-v2.008,NotoSerifArmenian-v2.008,NotoSansGeorgian-v2.005,NotoSerifGeorgian-v2.003,NotoSansLao-v2.003,NotoSerifLao-v2.003,NotoSansLisu-v2.102}.zip |
| Noto Naskh Arabic (PDF Editor) | 1.00 | Apache-2.0 ([Apache-2.0.txt](licenses/texts/Apache-2.0.txt), [embedpdf-fonts-1.0.0--LICENSE.txt](licenses/texts/embedpdf-fonts-1.0.0--LICENSE.txt)) | Copyright 2014 Google Inc. All Rights Reserved.; Noto is a trademark of Google Inc. and may be registered in certain jurisdictions. | https://registry.npmjs.org/@embedpdf/fonts-arabic/-/fonts-arabic-1.0.0.tgz (file fonts/NotoNaskhArabic-Regular.ttf); font upstream: Noto Naskh Arabic (Google Noto project; today https://github.com/notofonts/arabic) |
| Noto Sans (OCR text layer) | 2.008 | OFL-1.1 ([noto-fonts-ffebf8c1--LICENSE.txt](licenses/texts/noto-fonts-ffebf8c1--LICENSE.txt), [OFL-1.1.txt](licenses/texts/OFL-1.1.txt)) | Copyright 2015-2021 Google LLC. All Rights Reserved. (font name table); Copyright 2018 The Noto Project Authors (github.com/googlei18n/noto-fonts) (repository LICENSE) | https://github.com/googlefonts/noto-fonts/blob/ffebf8c1ee449e544955a7e813c54f9b73848eac/hinted/ttf/NotoSans/NotoSans-Regular.ttf (last commit of the archived googlefonts/noto-fonts repo, 2023-01-25) |
| Noto Sans (PDF Editor) | 2.015 | OFL-1.1 ([notofonts-latin-greek-cyrillic-NotoSans-v2.015--OFL.txt](licenses/texts/notofonts-latin-greek-cyrillic-NotoSans-v2.015--OFL.txt), [embedpdf-fonts-1.0.0--LICENSE.txt](licenses/texts/embedpdf-fonts-1.0.0--LICENSE.txt)) | Copyright 2022 The Noto Project Authors (https://github.com/notofonts/latin-greek-cyrillic); Noto is a trademark of Google LLC. | https://registry.npmjs.org/@embedpdf/fonts-latin/-/fonts-latin-1.0.0.tgz (file fonts/NotoSans-Regular.ttf); font upstream: https://github.com/notofonts/latin-greek-cyrillic/releases/tag/NotoSans-v2.015 |
| Noto Sans Hebrew (PDF Editor) | 1.02 | Apache-2.0 ([Apache-2.0.txt](licenses/texts/Apache-2.0.txt), [embedpdf-fonts-1.0.0--LICENSE.txt](licenses/texts/embedpdf-fonts-1.0.0--LICENSE.txt)) | Copyright 2012 Google Inc. All Rights Reserved.; Noto is a trademark of Google Inc. and may be registered in certain jurisdictions. | https://registry.npmjs.org/@embedpdf/fonts-hebrew/-/fonts-hebrew-1.0.0.tgz (file fonts/NotoSansHebrew-Regular.ttf); font upstream: Noto Sans Hebrew (Google Noto project; today https://github.com/notofonts/hebrew) |
| OpenSymbol (in LibreOffice) | 102.12 | MPL-2.0 ([LibreOffice-COPYING.MPL.txt](licenses/texts/LibreOffice-COPYING.MPL.txt)) | (c) 2009 Sun Microsystems Inc.; THERE DOES NOT EXIST (c) 2011 Julien Nabet; PRECEDES <-> DOES NOT SUCCEED (c) 2011 Olivier Hallot; PRIME <-> TRIPLE PRIME (c) 2013 Mathias Hasselmann; phi <-> phi1 (c) 2015 Khaled Hosny; (c) 2016 Mike Kaganski; zero ... lozenge (c) 2010 Google Corporation; uni20D1 (c) 2019 Takeshi Abe; uniF030 <-> uniF039 (c) 2020 Ming Hua | https://git.libreoffice.org/core/+/d1c9e0e4e1ddeb24fe8f93e56860b3765043f8b1 (mirror: https://github.com/LibreOffice/core/tree/d1c9e0e4e1ddeb24fe8f93e56860b3765043f8b1) extras/source/truetype/symbol/OpenSymbol.sfd |
| PDF.js translations | pdf.js 5.4.296 | MPL-2.0 ([MPL-2.0.txt](licenses/texts/MPL-2.0.txt)) | Mozilla contributors (each viewer.ftl carries the MPL-2.0 header "This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0"; no copyright line) | https://github.com/mozilla/pdf.js/tree/f56dc86014bb00c5a239680df53d2010e9aad0f8/l10n and https://github.com/mozilla/pdf.js/tree/0cec644372c38756474eb45c4e2aa0058960464a/l10n; zh-TW modified copies: https://github.com/alam00000/bentopdf/tree/f96cd4e5166f3d51393dfe9f3c440b5bb77802f1/public/pdfjs-viewer/locale/zh-TW/viewer.ftl |
| Reem Kufi (in LibreOffice) | 1.7 | OFL-1.1 ([SPDX-OFL-1.1.txt](licenses/texts/SPDX-OFL-1.1.txt)) | Copyright 2015-2022 The Reem Kufi Project Authors (https://github.com/aliftype/reem-kufi). | https://dev-www.libreoffice.org/src/ReemKufi-1.7.zip |
| Sacramento (signature font) | 1.000 | OFL-1.1 ([sacramento-1.000--OFL.txt](licenses/texts/sacramento-1.000--OFL.txt)) | Copyright (c) 2012 by Brian J. Bonislawsky DBA Astigmatic (AOETI) (astigma@astigmatic.com), with ReservedFont Name "Sacramento" (font name table) | https://github.com/google/fonts/tree/23e54b51ddffbc7713c583748e3bd86f62b1fa4a/ofl/sacramento (same version as shipped; the shipped file is not byte-identical, see notes) |
| Scheherazade (in LibreOffice) | 2.100 | OFL-1.1 ([SPDX-OFL-1.1.txt](licenses/texts/SPDX-OFL-1.1.txt)) | Copyright (c) 1994-2015, SIL International (http://www.sil.org/), with Reserved Font Names "Scheherazade" and "SIL". | https://dev-www.libreoffice.org/src/Scheherazade-2.100.zip |
| sRGB ICC profile (ICC) | v2 (2009) | LicenseRef-ICC-sRGB-profile-terms ([icc-srgb-iec61966-2-1-no-black-scaling-2009--terms-of-use.txt](licenses/texts/icc-srgb-iec61966-2-1-no-black-scaling-2009--terms-of-use.txt)) | Copyright International Color Consortium, 2009 | https://www.color.org/sRGB_IEC61966-2-1_no_black_scaling.icc (ICC download; now only archived: http://web.archive.org/web/20231124171008/https://www.color.org/sRGB_IEC61966-2-1_no_black_scaling.icc, byte-identical, sha256 b3599c68b79236e5ce69d8dd22178157553631c5fe829130602cde98d8764790) |
| Tesseract English model (tessdata_best) | 4.0.0_best_int | Apache-2.0 ([Apache-2.0.txt](licenses/texts/Apache-2.0.txt)) | No copyright notice stated upstream; tessdata_best models were trained for Tesseract 4 at Google (imported to tesseract-ocr/tessdata_best by Jeff Breidenbach, Google, 2017-09-14, 'Initial import (on behalf of Ray)') | https://registry.npmjs.org/@tesseract.js-data/eng/-/eng-1.0.0.tgz (package/4.0.0_best_int/eng.traineddata.gz; package gitHead b86746569320a6103cea84cc2b8d9ee74f0f45d3 of github.com/naptha/tessdata), derived from https://github.com/tesseract-ocr/tessdata_best/blob/e9f15884bc503cf905c8a1dbbc9cb14458152628/eng.traineddata (unchanged since the 2017-09-14 initial import; same file at tags 4.0.0 and 4.1.0) |

## Web components

| Component | Version | License | Copyright | Source |
| --- | --- | --- | --- | --- |
| Lucide icons | 0.575.0 | ISC AND MIT ([lucide-0.575.0--LICENSE.txt](licenses/texts/lucide-0.575.0--LICENSE.txt)) | Copyright (c) for portions of Lucide are held by Cole Bemis 2013-2026 as part of Feather (MIT). All other copyright (c) for Lucide are held by Lucide Contributors 2026.; Copyright (c) 2013-2026 Cole Bemis (Feather, MIT) | https://registry.npmjs.org/lucide/-/lucide-0.575.0.tgz; git: https://github.com/lucide-icons/lucide tag 0.575.0 = commit 10f6d5f8c6d9a1dae5e0ddec3925456ea7eca7bd (packages/lucide) |
| Phosphor Icons | 2.1.2 | MIT ([phosphor-icons-web-2.1.2--LICENSE.txt](licenses/texts/phosphor-icons-web-2.1.2--LICENSE.txt)) | Copyright (c) 2020-2021 Phosphor Icons | https://registry.npmjs.org/@phosphor-icons/web/-/web-2.1.2.tgz; git: https://github.com/phosphor-icons/web tag v2.1.2 = commit 70854726d7bd82ae21f0dc81b5b5c35240a77066 |
| SheetJS Community Edition | 0.20.3 | Apache-2.0 ([xlsx-0.20.3--LICENSE.txt](licenses/texts/xlsx-0.20.3--LICENSE.txt)) | Copyright (C) 2012-present SheetJS LLC; xlsx.js (C) 2013-present SheetJS -- http://sheetjs.com | https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz (package-lock integrity sha512-oLDq3jw7AcLqKWH2AhCpVTZl8mf6X2YReP+Neh0SJUzV/BdZYjth94tG5toiMB1PPrYtxOCfaoUCkvtuH+3AJA==); git: https://git.sheetjs.com/sheetjs/sheetjs tag v0.20.3 = commit 8a7cfd47bde8258c0d91df6a737bf0136699cdf8 |
| Tailwind CSS (in the site's stylesheets) | 4.2.2 | MIT ([tailwindcss-4.2.2-LICENSE.txt](licenses/texts/tailwindcss-4.2.2-LICENSE.txt)) | Copyright (c) Tailwind Labs, Inc. | https://github.com/tailwindlabs/tailwindcss/tree/v4.2.2 |
| Vite (runtime helpers in the site's scripts) | 8.1.2 | MIT ([vite-8.1.2-LICENSE.txt](licenses/texts/vite-8.1.2-LICENSE.txt)) | Copyright (c) 2019-present, VoidZero Inc. and Vite contributors | https://github.com/vitejs/vite/tree/v8.1.2 |

## Android libraries

| Component | Version | License | Copyright | Source |
| --- | --- | --- | --- | --- |
| AndroidX Core (PackageInfoCompat and Pair only) | 1.1.0 | Apache-2.0 ([Apache-2.0.txt](licenses/texts/Apache-2.0.txt)) | Copyright (C) The Android Open Source Project | https://dl.google.com/android/maven2/androidx/core/core/1.1.0/core-1.1.0-sources.jar |
| AndroidX WebKit | 1.18.0-alpha02 | Apache-2.0 ([Apache-2.0.txt](licenses/texts/Apache-2.0.txt)) | Copyright (C) The Android Open Source Project | https://dl.google.com/android/maven2/androidx/webkit/webkit/1.18.0-alpha02/webkit-1.18.0-alpha02-sources.jar |

## JavaScript packages (188)

The npm packages in BentoPDF's scripts, from its build's own report. Their license
texts are in [licenses/javascript-packages.txt](licenses/javascript-packages.txt).

| Package | Version | License |
| --- | --- | --- |
| [@babel/runtime](https://babel.dev/docs/en/next/babel-runtime) | 7.29.2 | MIT |
| [@braintree/sanitize-url](https://github.com/braintree/sanitize-url#readme) | 7.1.2 | MIT |
| [@iconify/utils](https://iconify.design/docs/libraries/utils/) | 3.1.0 | MIT |
| [@kenjiuno/msgreader](https://github.com/HiraokaHyperTools/msgreader) | 1.28.0 | Apache-2.0 |
| [@lit/reactive-element](https://lit.dev/) | 2.1.2 | BSD-3-Clause |
| [@matbee/libreoffice-converter](https://github.com/matbeedotcom/libreoffice-document-converter#readme) | 2.6.0 | MPL-2.0 |
| [@mermaid-js/parser](https://github.com/mermaid-js/mermaid/tree/develop/packages/mermaid/parser/#readme) | 1.2.0 | MIT |
| [@neslinesli93/qpdf-wasm](https://github.com/neslinesli93/qpdf-wasm) | 0.3.0 | ISC AND Apache-2.0 |
| [@nodable/entities](https://github.com/nodable/val-parsers) | 2.1.0 | MIT |
| [@pdf-lib/fontkit](https://github.com/Hopding/fontkit) | 1.1.1 | MIT |
| [@pdf-lib/standard-fonts](https://github.com/Hopding/standard-fonts) | 1.0.0 | MIT |
| [@pdf-lib/upng](https://github.com/Hopding/upng) | 1.0.1 | MIT |
| [@phosphor-icons/web](https://phosphoricons.com) | 2.1.2 | MIT |
| [@retejs/lit-plugin](https://retejs.org) | 2.0.7 | MIT |
| [@upsetjs/venn.js](https://github.com/upsetjs/venn.js) | 2.0.0 | MIT |
| [assert](https://github.com/browserify/commonjs-assert) | 2.1.0 | MIT |
| [available-typed-arrays](https://github.com/inspect-js/available-typed-arrays#readme) | 1.0.7 | MIT |
| bentopdf-pdfium | 0.0.0-8ff5002c6cd5 | AGPL-3.0-only |
| bentopdf-viewer | 2.9.1 | AGPL-3.0-only AND MIT |
| [bwip-js](https://github.com/metafloor/bwip-js) | 4.8.0 | MIT |
| [call-bind](https://github.com/ljharb/call-bind#readme) | 1.0.8 | MIT |
| [call-bind-apply-helpers](https://github.com/ljharb/call-bind-apply-helpers#readme) | 1.0.2 | MIT |
| [call-bound](https://github.com/ljharb/call-bound#readme) | 1.0.4 | MIT |
| [canvg](https://github.com/canvg/canvg) | 3.0.11 | MIT |
| [core-js](https://core-js.io) | 3.49.0 | MIT |
| [cose-base](https://github.com/iVis-at-Bilkent/cose-base#readme) | 1.0.3 | MIT |
| [cose-base](https://github.com/iVis-at-Bilkent/cose-base#readme) | 2.2.0 | MIT |
| [cropperjs](https://fengyuanchen.github.io/cropperjs) | 1.6.2 | MIT |
| [cross-fetch](https://github.com/lquixada/cross-fetch) | 4.1.0 | MIT |
| [cytoscape](http://js.cytoscape.org) | 3.34.0 | MIT |
| [cytoscape-cose-bilkent](https://github.com/cytoscape/cytoscape.js-cose-bilkent) | 4.1.0 | MIT |
| [cytoscape-fcose](https://github.com/iVis-at-Bilkent/cytoscape.js-fcose) | 2.2.0 | MIT |
| [d3](https://d3js.org) | 7.9.0 | ISC |
| [d3-array](https://d3js.org/d3-array/) | 2.12.1 | BSD-3-Clause |
| [d3-array](https://d3js.org/d3-array/) | 3.2.4 | ISC |
| [d3-axis](https://d3js.org/d3-axis/) | 3.0.0 | ISC |
| [d3-brush](https://d3js.org/d3-brush/) | 3.0.0 | ISC |
| [d3-color](https://d3js.org/d3-color/) | 3.1.0 | ISC |
| [d3-dispatch](https://d3js.org/d3-dispatch/) | 3.0.1 | ISC |
| [d3-ease](https://d3js.org/d3-ease/) | 3.0.1 | BSD-3-Clause |
| [d3-format](https://d3js.org/d3-format/) | 3.1.2 | ISC |
| [d3-hierarchy](https://d3js.org/d3-hierarchy/) | 3.1.2 | ISC |
| [d3-interpolate](https://d3js.org/d3-interpolate/) | 3.0.1 | ISC |
| [d3-path](https://d3js.org/d3-path/) | 1.0.9 | BSD-3-Clause |
| [d3-path](https://d3js.org/d3-path/) | 3.1.0 | ISC |
| [d3-sankey](https://github.com/d3/d3-sankey) | 0.12.3 | BSD-3-Clause |
| [d3-scale](https://d3js.org/d3-scale/) | 4.0.2 | ISC |
| [d3-scale-chromatic](https://d3js.org/d3-scale-chromatic/) | 3.1.0 | ISC |
| [d3-selection](https://d3js.org/d3-selection/) | 3.0.0 | ISC |
| [d3-shape](https://d3js.org/d3-shape/) | 1.3.7 | BSD-3-Clause |
| [d3-shape](https://d3js.org/d3-shape/) | 3.2.0 | ISC |
| [d3-time](https://d3js.org/d3-time/) | 3.1.0 | ISC |
| [d3-time-format](https://d3js.org/d3-time-format/) | 4.1.0 | ISC |
| [d3-timer](https://d3js.org/d3-timer/) | 3.0.1 | ISC |
| [d3-transition](https://d3js.org/d3-transition/) | 3.0.1 | ISC |
| [d3-zoom](https://d3js.org/d3-zoom/) | 3.0.0 | ISC |
| [dagre-d3-es](https://github.com/tbo47/dagre-es) | 7.0.14 | MIT |
| [dayjs](https://day.js.org) | 1.11.20 | MIT |
| [debug](https://github.com/debug-js/debug) | 4.4.3 | MIT |
| [define-data-property](https://github.com/ljharb/define-data-property#readme) | 1.1.4 | MIT |
| [define-properties](https://github.com/ljharb/define-properties) | 1.2.1 | MIT |
| [diff](https://github.com/kpdecker/jsdiff) | 8.0.3 | BSD-3-Clause |
| [dompurify](https://github.com/cure53/DOMPurify) | 3.4.12 | (MPL-2.0 OR Apache-2.0) |
| [dunder-proto](https://github.com/es-shims/dunder-proto#readme) | 1.0.1 | MIT |
| [entities](https://github.com/fb55/entities) | 4.5.0 | BSD-2-Clause |
| [es-define-property](https://github.com/ljharb/es-define-property#readme) | 1.0.1 | MIT |
| [es-errors](https://github.com/ljharb/es-errors#readme) | 1.3.0 | MIT |
| [es-object-atoms](https://github.com/ljharb/es-object-atoms#readme) | 1.1.1 | MIT |
| [es-toolkit](https://es-toolkit.dev) | 1.46.1 | MIT |
| [events](https://github.com/Gozala/events) | 3.3.0 | MIT |
| [fast-png](https://github.com/image-js/fast-png#readme) | 6.4.0 | MIT |
| [fast-xml-parser](https://github.com/NaturalIntelligence/fast-xml-parser) | 5.7.1 | MIT |
| [fflate](https://101arrowz.github.io/fflate) | 0.8.2 | MIT |
| [follow-redirects](https://github.com/follow-redirects/follow-redirects) | 1.16.0 | MIT |
| [for-each](https://github.com/Raynos/for-each) | 0.3.5 | MIT |
| [function-bind](https://github.com/Raynos/function-bind) | 1.1.2 | MIT |
| [generator-function](https://github.com/TimothyGu/generator-function#readme) | 2.0.1 | MIT |
| [get-intrinsic](https://github.com/ljharb/get-intrinsic#readme) | 1.3.0 | MIT |
| [get-proto](https://github.com/ljharb/get-proto#readme) | 1.0.1 | MIT |
| [gopd](https://github.com/ljharb/gopd#readme) | 1.2.0 | MIT |
| [has-property-descriptors](https://github.com/inspect-js/has-property-descriptors#readme) | 1.0.2 | MIT |
| [has-symbols](https://github.com/ljharb/has-symbols#readme) | 1.1.0 | MIT |
| [has-tostringtag](https://github.com/inspect-js/has-tostringtag#readme) | 1.0.2 | MIT |
| [hasown](https://github.com/inspect-js/hasOwn#readme) | 2.0.2 | MIT |
| [heic2any](https://github.com/alexcorvi/heic2any#readme) | 0.0.4 | MIT AND LGPL-3.0-or-later |
| [highlight.js](https://highlightjs.org/) | 11.11.1 | BSD-3-Clause |
| [html2canvas](https://html2canvas.hertzen.com) | 1.4.1 | MIT |
| [i18next](https://www.i18next.com) | 25.10.2 | MIT |
| [i18next-http-backend](https://github.com/i18next/i18next-http-backend) | 3.0.6 | MIT |
| [iconv-lite](https://github.com/ashtuchkin/iconv-lite) | 0.6.3 | MIT |
| [inherits](https://github.com/isaacs/inherits) | 2.0.4 | ISC |
| [internmap](https://github.com/mbostock/internmap/) | 2.0.3 | ISC |
| [iobuffer](https://github.com/image-js/iobuffer#readme) | 5.4.0 | MIT |
| [iobuffer](https://github.com/image-js/iobuffer#readme) | 6.0.1 | MIT |
| [is-arguments](https://github.com/inspect-js/is-arguments) | 1.2.0 | MIT |
| [is-callable](https://github.com/inspect-js/is-callable) | 1.2.7 | MIT |
| [is-generator-function](https://github.com/inspect-js/is-generator-function) | 1.1.2 | MIT |
| [is-nan](https://github.com/es-shims/is-nan) | 1.3.2 | MIT |
| [is-regex](https://github.com/inspect-js/is-regex) | 1.2.1 | MIT |
| [is-typed-array](https://github.com/inspect-js/is-typed-array) | 1.1.15 | MIT |
| [jspdf](https://github.com/parallax/jsPDF) | 4.2.1 | MIT |
| [jspdf-autotable](https://simonbengtsson.github.io/jsPDF-AutoTable) | 5.0.7 | MIT |
| [jszip](https://github.com/Stuk/jszip) | 3.10.1 | (MIT OR GPL-3.0-or-later) |
| [katex](https://katex.org) | 0.16.47 | MIT |
| [khroma](https://github.com/fabiospampinato/khroma) | 2.1.0 | MIT |
| [layout-base](https://github.com/iVis-at-Bilkent/layout-base#readme) | 1.0.2 | MIT |
| [layout-base](https://github.com/iVis-at-Bilkent/layout-base#readme) | 2.0.1 | MIT |
| [linkify-it](https://github.com/markdown-it/linkify-it) | 5.0.2 | MIT |
| [lit](https://lit.dev/) | 3.3.2 | BSD-3-Clause |
| [lit-element](https://lit.dev/) | 4.2.2 | BSD-3-Clause |
| [lit-html](https://lit.dev/) | 3.3.2 | BSD-3-Clause |
| [lodash-es](https://lodash.com/custom-builds) | 4.18.1 | MIT |
| [lucide](https://lucide.dev) | 0.575.0 | ISC |
| [markdown-it](https://github.com/markdown-it/markdown-it) | 14.2.0 | MIT |
| [markdown-it-abbr](https://github.com/markdown-it/markdown-it-abbr) | 2.0.0 | MIT |
| [markdown-it-anchor](https://github.com/valeriangalliat/markdown-it-anchor) | 9.2.0 | Unlicense |
| [markdown-it-deflist](https://github.com/markdown-it/markdown-it-deflist) | 3.0.0 | MIT |
| [markdown-it-emoji](https://github.com/markdown-it/markdown-it-emoji) | 3.0.0 | MIT |
| [markdown-it-footnote](https://github.com/markdown-it/markdown-it-footnote) | 4.0.0 | MIT |
| [markdown-it-ins](https://github.com/markdown-it/markdown-it-ins) | 4.0.0 | MIT |
| [markdown-it-mark](https://github.com/markdown-it/markdown-it-mark) | 4.0.0 | MIT |
| [markdown-it-sub](https://github.com/markdown-it/markdown-it-sub) | 2.0.0 | MIT |
| [markdown-it-sup](https://github.com/markdown-it/markdown-it-sup) | 2.0.0 | MIT |
| [markdown-it-task-lists](https://github.com/revin/markdown-it-task-lists#readme) | 2.1.1 | ISC |
| [markdown-it-toc-done-right](https://github.com/nagaozen/markdown-it-toc-done-right#readme) | 4.2.0 | MIT |
| [marked](https://marked.js.org) | 16.4.2 | MIT |
| [math-intrinsics](https://github.com/es-shims/math-intrinsics#readme) | 1.1.0 | MIT |
| [mdurl](https://github.com/markdown-it/mdurl) | 2.0.0 | MIT |
| [mermaid](https://github.com/mermaid-js/mermaid) | 11.16.1 | MIT |
| [ms](https://github.com/vercel/ms) | 2.1.3 | MIT |
| [node-forge](https://github.com/digitalbazaar/forge) | 1.4.0 | (BSD-3-Clause OR GPL-2.0) |
| [object-inspect](https://github.com/inspect-js/object-inspect) | 1.13.4 | MIT |
| [object-is](https://github.com/es-shims/object-is) | 1.1.6 | MIT |
| [object-keys](https://github.com/ljharb/object-keys) | 1.1.1 | MIT |
| [object.assign](https://github.com/ljharb/object.assign) | 4.1.7 | MIT |
| [pako](https://github.com/nodeca/pako) | 1.0.11 | (MIT AND Zlib) |
| [pako](https://github.com/nodeca/pako) | 2.1.0 | (MIT AND Zlib) |
| [papaparse](https://www.papaparse.com/) | 5.5.3 | MIT |
| [path-expression-matcher](https://github.com/NaturalIntelligence/path-expression-matcher#readme) | 1.5.0 | MIT |
| [pdf-fontkit](https://github.com/znacloud/pdf-fontkit) | 1.8.9 | MIT |
| [pdf-lib](https://pdf-lib.js.org) | 1.17.1 | MIT |
| [pdfjs-dist](https://mozilla.github.io/pdf.js/) | 5.5.207 | Apache-2.0 |
| [performance-now](https://github.com/braveg1rl/performance-now) | 2.1.0 | MIT |
| [pixelmatch](https://github.com/mapbox/pixelmatch#readme) | 7.1.0 | ISC |
| [possible-typed-array-names](https://github.com/ljharb/possible-typed-array-names#readme) | 1.1.0 | MIT |
| [postal-mime](https://postal-mime.postalsys.com) | 2.7.4 | MIT-0 |
| [punycode](https://mths.be/punycode) | 1.4.1 | MIT |
| [punycode.js](https://mths.be/punycode) | 2.3.1 | MIT |
| [qs](https://github.com/ljharb/qs) | 6.15.0 | BSD-3-Clause |
| [raf](https://github.com/chrisdickinson/raf) | 3.4.1 | MIT |
| [readable-stream](https://github.com/nodejs/readable-stream) | 3.6.2 | MIT |
| [regenerator-runtime](https://github.com/facebook/regenerator/tree/main/packages/runtime) | 0.13.11 | MIT |
| [rete](https://retejs.org) | 2.0.6 | MIT |
| [rete-area-plugin](https://retejs.org) | 2.1.5 | MIT |
| [rete-connection-plugin](https://retejs.org) | 2.0.5 | MIT |
| [rete-engine](https://retejs.org) | 2.1.1 | MIT |
| [rete-render-utils](https://retejs.org) | 2.0.3 | MIT |
| [rgbcolor](https://github.com/yetzt/node-rgbcolor) | 1.0.1 | MIT OR SEE LICENSE IN FEEL-FREE.md |
| [roughjs](https://roughjs.com) | 4.6.6 | MIT |
| [safe-buffer](https://github.com/feross/safe-buffer) | 5.2.1 | MIT |
| [safe-regex-test](https://github.com/ljharb/safe-regex-test#readme) | 1.1.0 | MIT |
| [safer-buffer](https://github.com/ChALkeR/safer-buffer) | 2.1.2 | MIT |
| [set-function-length](https://github.com/ljharb/set-function-length#readme) | 1.2.2 | MIT |
| [side-channel](https://github.com/ljharb/side-channel#readme) | 1.1.0 | MIT |
| [side-channel-list](https://github.com/ljharb/side-channel-list#readme) | 1.0.0 | MIT |
| [side-channel-map](https://github.com/ljharb/side-channel-map#readme) | 1.0.1 | MIT |
| [side-channel-weakmap](https://github.com/ljharb/side-channel-weakmap#readme) | 1.0.2 | MIT |
| [sortablejs](https://github.com/SortableJS/Sortable) | 1.15.7 | MIT |
| [stackblur-canvas](http://www.quasimondo.com/StackBlurForCanvas/StackBlurDemo.html) | 2.7.0 | MIT |
| [stream-browserify](https://github.com/browserify/stream-browserify) | 3.0.0 | MIT |
| [string_decoder](https://github.com/nodejs/string_decoder) | 1.3.0 | MIT |
| [strnum](https://github.com/NaturalIntelligence/strnum) | 2.2.3 | MIT |
| [stylis](https://github.com/thysultan/stylis.js) | 4.3.6 | MIT |
| [svg-pathdata](https://github.com/nfroidure/svg-pathdata) | 6.0.3 | MIT |
| [tesseract.js](https://github.com/naptha/tesseract.js) | 7.0.0 | Apache-2.0 |
| [tiff](https://image-js.github.io/tiff/) | 7.1.3 | MIT |
| [ts-dedent](https://github.com/tamino-martinius/node-ts-dedent) | 2.2.0 | MIT |
| [tslib](https://www.typescriptlang.org/) | 1.14.1 | 0BSD |
| [uc.micro](https://github.com/markdown-it/uc.micro) | 2.1.0 | MIT |
| [url](https://github.com/defunctzombie/node-url) | 0.11.4 | MIT |
| [util](https://github.com/browserify/node-util) | 0.12.5 | MIT |
| [util-deprecate](https://github.com/TooTallNate/util-deprecate) | 1.0.2 | MIT |
| [uuid](https://github.com/uuidjs/uuid) | 14.0.1 | MIT |
| [vite-plugin-node-polyfills](https://github.com/davidmyersdev/vite-plugin-node-polyfills) | 0.26.0 | MIT |
| [wasm-vips](https://github.com/kleisauke/wasm-vips) | 0.0.17 | MIT AND LGPL-2.1-or-later |
| [which-typed-array](https://github.com/inspect-js/which-typed-array) | 1.1.20 | MIT |
| [xlsx](https://sheetjs.com/) | 0.20.3 | Apache-2.0 |
| [zgapdfsigner](https://github.com/zboris12/zgapdfsigner) | 2.7.5 | MIT |

## Notices some licenses require

- Portions of this software are copyright © 2024-2025 The FreeType Project (www.freetype.org). All rights reserved.
- This software is based in part on the work of the Independent JPEG Group.
- This product includes Gain Map technology under license by Adobe.

## Details

How each component gets into the app, where its build scripts are, and notes from the license
audit: obligations, and what couldn't be verified.

### PDF Toolbox 0.6

- **Used for:** The Android app around BentoPDF: its window and sidebar, files, downloads and printing, the page script, these pages, and the scripts that build it

### BentoPDF 2.8.8

- **Used for:** The PDF tools: every page, script, style and translation of the site, built by tools/webapp.sh
- Modified by PDF Toolbox: built in Simple Mode with every engine served from the app and PDF Toolbox's name and logo in its header (tools/webapp.sh); PDF Toolbox's page script runs in its pages (shell/page_shim.js); its pages are shown in PDF Toolbox's sidebar window, without BentoPDF's top bar (shell/app.html); a prelude is prepended to the LibreOffice converter's worker (shell/nested-workers.js).

### LibreOffice 24.8.8

- **In the app via:** @matbee/libreoffice-converter 2.3.x wasm/ files, vendored in BentoPDF public/libreoffice-wasm/ and gzip-compressed
- **Used for:** Office-to-PDF conversion: Word (doc/docx), Excel (xls/xlsx), PowerPoint (ppt/pptx), ODT/ODS/ODP/ODG, RTF, WPS/WPD/Pages/VSD/PUB pages and the matching workflow nodes (src/js/utils/libreoffice-loader.ts)
- **Build:** matbeedotcom/libreoffice-document-converter build/: Dockerfile.build (ubuntu:24.04, emsdk 3.1.74), build-wasm.sh (clones git.libreoffice.org/core branch libreoffice-24-8 with --depth 1, applies wasm-build-fixes.patch, copies autogen.input: --host=wasm32-local-emscripten --with-main-module=all --disable-gui --enable-wasm-strip --enable-pdfium --disable-poppler --disable-nss --without-java ... ), then post-processes soffice.js
- Exact corresponding source = LibreOffice core d1c9e0e4 + wasm-build-fixes.patch + autogen.input + the download.lst tarballs; the build scripts clone the moving branch (not a tag), so the commit was taken from versionrc/setuprc buildid inside soffice.data. The Emscripten version (3.1.74) is from the build scripts only; the binary carries no producers section. wasm-strip mode (kept by the patch) disables libcdr, libetonyek, libfreehand, libmspub, libpagemaker, libqxp, libvisio, libzmf, libepubgen, zxing, curl, NSS, skia, libcmis, lpsolve/CoinMP, python/java and the EPUB/extended writerperfect filters: no WordPerfect, AbiWord, eBook, MS Works (writer), Visio, Publisher or Keynote/Pages import filters are registered in the binary, and libwpd/libwpg/libabw/libe-book/libetonyek left no traces. BentoPDF's WPD/VSD/PUB/Pages tools therefore probably cannot work with this engine (functional observation, not tested). No LGPL-only or GPL-only code is compiled in: every multi-licensed external offers an MPL/Apache/BSD option. The generated LICENSE text is unfiltered (all externals LibreOffice can bundle), which is a superset of this build. LibreOffice's own renderer XSL drops <pre>/<dd>/<h4> content, so the text was rendered with a full XHTML-to-text converter; license.xml is also shipped verbatim. soffice.data carries LibreOfficeDev branding images (program/intro*.png, shell/about.svg, logo*.svg): TDF trademarks, not displayed by the headless engine. COPYING.LGPL (LGPL-3.0) is still present at the repo root for legacy reasons; the project notice states MPL-2.0 (with ALv2 portions requiring the NOTICE file).

### PyMuPDF 1.26.3

- **In the app via:** @bentopdf/pymupdf-wasm 0.11.16 assets/
- **Used for:** PyMuPDF-based tools: EPUB/MOBI/FB2/CBZ/XPS/email/image/TXT/PSD-to-PDF, compress, deskew, rasterize, redact, extract images/tables, PDF-to-text/SVG/CSV/Excel/Markdown/DOCX/PDF-A, PDF layers, prepare-for-AI, decrypt (src/js/utils/pymupdf-loader.ts); all nine wheels are loaded at PyMuPDF init
- **Build:** Pyodide recipe https://github.com/pyodide/pyodide-recipes/blob/595830b7abec1e74e5a5f7cb196f946263df7e85/packages/PyMuPDF/meta.yaml (PYMUPDF_SETUP_FLAVOUR=pb, PYMUPDF_SETUP_MUPDF_TESSERACT=0, HAVE_LIBCRYPTO=no, exports whole_archive); recipe unchanged until 2026-04-03, so it is the one used for Pyodide 0.29.0
- Upstream metadata: "Dual Licensed - GNU AFFERO GPL 3.0 or Artifex Commercial License"; we use it under AGPL. The wheel's dist-info COPYING is only that one line; the repo COPYING at tag 1.26.3 is the full AGPL-3.0 text (identical to MuPDF-1.26.3-COPYING-AGPL-3.0.txt). Inconsistency upstream: pymupdf/__init__.py says "SPDX-License-Identifier: GPL-3.0-only" while table.py says AGPL-3.0-or-later and utils.py says AGPL 3.0. Under AGPL s13, users interacting with it (even locally) must be able to get the Corresponding Source: point to the sdist, the MuPDF tarball and the Pyodide recipe.

### Ghostscript (@bentopdf/gs-wasm) 10.06.0

- **In the app via:** @bentopdf/gs-wasm 0.1.1 (bentopdf-gs-wasm-0.1.1.tgz from BentoPDF's scripts/prepare-airgap.sh); tools/webapp.sh extracts package/assets/* to wasm/gs/ and package/dist/index.js to wasm/gs/dist/
- **Used for:** PDF to PDF/A (pdfwrite -dPDFA, with the web root's sRGB ICC profile), Font to Outline (pdfwrite -dNoOutputFonts), their Workflow Builder nodes, and PDF to Word (the PyMuPDF wrapper converts the PDF to RGB with Ghostscript before pdf2docx)
- **Build:** build_scripts/build.sh and optimize.sh in @bentopdf/gs-wasm 0.1.1 (https://github.com/alam00000/bentopdf-gs-wasm/tree/v0.1.1/build_scripts): emconfigure ./configure --disable-contrib --disable-cups --disable-dbus --disable-fontconfig --disable-gtk --without-libpaper --without-libidn --without-pdftoraster --without-ijs --without-x --with-drivers=BMP,JPEG,PNG,PS,TIFF, CFLAGS -Os -flto, -sMODULARIZE -sEXPORT_ES6 -sFILESYSTEM, closure, binaryen wasm-opt version_124. Not shipped in the APK.
- Upstream GPL Ghostscript is AGPL-3.0-or-later (ghostpdl LICENSE); the npm package @bentopdf/gs-wasm declares AGPL-3.0-only for its packaging/build scripts. Either way the APK must offer the complete Corresponding Source (ghostpdl-10.06.0 + the gs-wasm build scripts).
- The package's LICENSE (AGPL-3.0 text), README (modification/attribution notice) and build_scripts/ are NOT shipped: tools/webapp.sh extracts only package/assets/* and package/dist/index.js. Ship the texts listed here and point to the source.
- Exact source not pinned: build_scripts/README.md says 'Clone the GhostPDL repository' (no tag/commit) and 'Emscripten SDK (latest)'; the README mentions .github/workflows that produced the binary, but the repo's workflows only publish to npm and gs.wasm was committed prebuilt in the initial commit (2025-12-24). The banner 'GPL Ghostscript 10.06.0 (2025-09-09)' equals the ghostpdl-10.06.0 release, so that release is the inferred source; reproducibility not verified.
- README says 'This package is a modified version of Ghostscript ... adapted for WebAssembly'; no source patches are published (only configure flags). If ghostpdl sources were modified, that modified source is missing (AGPL section 6). Unverified.
- Compiled in (verified by strings/tables in gs.wasm, versions from the ghostpdl-10.06.0 tree): FreeType, IJG libjpeg, libpng, zlib, lcms2mt, OpenJPEG, jbig2dec, LibTIFF, Brotli (static dictionary present), sha2.c (SHA-256/512 constants), aes.c (AES S-box), MD5. NOT compiled in: Tesseract/Leptonica (no OCR devices or strings), Expat and jpegxr (XPS only; jpegxr's ITU licence is not AGPL-compatible, absent here), Extract (no docxwrite device), CUPS, IJS, libpaper, fontconfig.
- The %rom% file system inside gs.wasm (269 files) holds the 35 URW base-35 fonts (AGPL + font exception from ghostpdl LICENSE: fonts may be embedded in output PDF/PS documents regardless of the document's licence), DroidSansFallback.ttf (Apache-2.0), 181 CMaps and 14 Artifex ICC profiles; fonts, ICC profiles and DroidSans are byte-identical to ghostpdl-10.06.0. The ROM build strips PostScript comments, so the Adobe BSD-3-Clause notice in each CMap header is gone from the shipped copies: it must be reproduced in the app's notices (text ghostscript-10.06.0--Resource-CMap-Adobe-notice.txt).
- IJG licence: the documentation must state 'This software is based in part on the work of the Independent JPEG Group'. FreeType FTL: the documentation must include 'Portions of this software are copyright (C) 2024 The FreeType Project (www.freetype.org). All rights reserved.'
- zlib's LICENSE file says (C) 1995-2022 while zlib.h of 1.3.1 says 1995-2024; both lines are listed.
- Emscripten version is inferred (latest release before the 2025-12-24 commit is 4.0.22); its LICENSE, musl COPYRIGHT and compiler-rt LICENSE were taken from 4.0.22 as reference copies.
- The URW font exception has no SPDX identifier; 'AdditionRef-Ghostscript-font-exception' is a local reference to the paragraph in ghostscript-10.06.0--LICENSE.txt.
- wasm/gs/dist/index.js loads gs.js from '<base>/assets/'; PDF Toolbox serves wasm/gs/assets/* from wasm/gs/ (docs in tools/webapp.sh).

### CoherentPDF (coherentpdf.js) 2.5.5

- **In the app via:** coherentpdf 2.5.5 (npm; coherentpdf-2.5.5.tgz from BentoPDF's scripts/prepare-airgap.sh; tools/webapp.sh extracts package/dist to wasm/cpdf/), and BentoPDF's public/coherentpdf.browser.min.js copied by Vite to the web root
- **Used for:** Merge PDF, Alternate Merge, Split PDF, Add/Edit/Extract Attachments, Add Page Labels, Table of Contents (and its Workflow node), PDF to JSON / JSON to PDF, decrypting password-protected inputs (utils/pdf-decrypt.ts); loaded from wasm/cpdf/coherentpdf.browser.min.js by a <script> tag or importScripts() in public/workers/*.js
- **Build:** Not WebAssembly: plain JavaScript. coherentpdf.js Makefile + ./build (copies camlpdf, cpdf-source, cpdflib-source; OCaml -> bytecode -> js_of_ocaml 4.0.0; browserify -s coherentpdf and uglifyjs for the browser builds): https://github.com/coherentgraphics/coherentpdf.js/tree/v2.5.5/Makefile
- Not a WASM engine: js_of_ocaml output (OCaml compiled to JavaScript). wasm/cpdf/coherentpdf.browser*.js additionally contain browserify's Node polyfills (crypto-browserify stack, browserify-zlib/pako, buffer, streams, util, events, process) listed in includes.
- The web-root coherentpdf.browser.min.js (1325062 bytes) is the npm 2.5.5 coherentpdf.browser.min.js with a 401-byte comment prepended ('a modified version of cpdf.js ... Copyright (c) 2025 BentoPDF ... AGPLv3'); the code after the header is byte-identical, so it is the same component. Nothing in BentoPDF 2.8.8 loads it: every loader uses WasmProvider.getUrl('cpdf') (= wasm/cpdf/ in this build). It ships only because Vite copies public/; it could be dropped.
- wasm/cpdf/coherentpdf.js and coherentpdf.min.js are the Node builds (they require('./sjcl.js'), which is not shipped); unused in the WebView, shipped only because dist/ is extracted whole.
- Corresponding-source gap: the coherentpdf.js repo holds only the bindings; its build script copies ../camlpdf, ../cpdf-source and ../cpdflib-source without recording revisions. The compiled Cpdf.version returns '2.5.5', a string found in no cpdflib-source commit (all 2022 commits say '2.5.2'), so the dist was built from an uncommitted working copy. The commit IDs given in source are the nearest (inferred) snapshots.
- In August 2022 cpdf-source and cpdflib-source were published under the 'Coherent Graphics Ltd Non-Commercial Use License'; they became AGPL-3.0 on 2024-07-23 (cpdf-source c2aae96, cpdflib-source 7692ffb). The compiled dist/ was released by the copyright holder as AGPL-3.0-or-later (package.json, README 'The files in dist/ are distributed under the AGPL'), so the grant for the shipped files is AGPL; but source offered for the 2022 snapshots should be accompanied by that AGPL grant (the 2022 repos' own LICENSE files say non-commercial). CoherentPDF is also sold under a commercial licence.
- Browserify polyfill versions are inferred (resolution of browserify 17.0.0's dependency ranges as of 2022-08-18); only elliptic 6.5.4 is verified (its package.json is embedded). The bundle also requires 'foreach' and es-abstract helpers, which point to an older lockfile, so exact versions differ for some packages; licence texts come from the inferred versions (same copyright holders, years may differ). Packages without a LICENSE file (indutny's bn.js family, constants-browserify) use the licence section of their README.
- sjcl: upstream dual licence (BSD-2-Clause OR GPL-2.0-or-later; npm metadata says GPL-2.0-only); coherentpdf's LICENSE.md redistributes it under BSD-2-Clause.
- pako is (MIT AND Zlib): its zlib port files carry the zlib licence (Zlib.txt).
- CamlPDF embeds Adobe's Core 14 AFM metrics; the APAFML terms ask that the AFM data not be distributed without Adobe's notice, which CamlPDF does not ship: APAFML.txt (SPDX text) added here.
- OCaml compiler version used is unknown; the OCaml 4.14.0 LICENSE is a reference copy (the licence is the same across 4.x).

### tesseract.js-core (Tesseract and Leptonica) 7.0.0

- **In the app via:** BentoPDF air-gap bundle (scripts/prepare-airgap.sh: npm pack tesseract.js-core@7.0.0); PDF Toolbox tools/webapp.sh extracts the whole package to wasm/ocr/core/
- **Used for:** OCR engine for the OCR PDF tool, the Workflow Builder's OCR node and Compare PDFs; the worker loads one *.wasm.js single-file build (relaxed-SIMD / SIMD / plain, each LSTM-only or with the legacy engine) according to browser support
- **Build:** In the tesseract.js-core repo at v7.0.0: build-with-docker.sh (Docker image emscripten/emsdk:4.0.15), build.sh, build-scripts/build-{zlib,libtiff,openlibm,giflib,libpng,libjpeg,libwebp,leptonica,tesseract}.sh and var.sh (-O3 --closure 1), javascript/ (WebIDL glue: tesseract.idl, glue.js, anterior.js, src/wrapper.cpp); link flags and linked libraries in the WASM_BUILD section of the Tesseract fork's CMakeLists.txt
- The package itself ships its LICENSE as wasm/ocr/core/LICENSE (unfilled Apache-2.0, no copyright line); there is no NOTICE file in tesseract.js-core, the Tesseract fork or tessdata_best (raw NOTICE URLs: 404).
- Tesseract here is a fork (github.com/Balearica/tesseract) with changes listed in the tesseract.js-core README (WASM CMake build, SSE/relaxed-SIMD paths in src/arch_sse, JSON renderer, page-angle detection, WriteImage/SaveParameters, logging changes). Its CMakeLists links libgif, libjpeg, libopenlibm, libpng, libtiff, libtiffxx, libwebp, libwebpdecoder, libwebpdemux and libz, and embeds tessdata/pdf.ttf.
- Leptonica 1.83.0, libpng 1.6.38.git, libtiff 4.3.0+, libwebp 1.2.2+ and OpenLibm 0.8.0+ are development snapshots at the pinned submodule commits, not release tarballs: the corresponding source is the commit (tree URLs above).
- Linked libraries verified by strings in the wasm: libpng ('1.6.38.git'), IJG libjpeg ('9a  19-Jan-2014', 'Copyright (C) 2014, Thomas G. Lane, Guido Vollbeding'), zlib ('1.2.12'), libtiff (SGILog/LogLuv codec functions), libwebp/Leptonica WebP I/O ('WEBPVP8L', pixReadMemWebP), Leptonica ('leptonica-%d.%d.%d', PNM/PDF writers). giflib and OpenLibm are linked per the CMakeLists (giflib: GIF87a/GIF89a strings only), not otherwise verifiable in the stripped binary.
- Emscripten 4.0.15 is inferred from build-with-docker.sh at the tag; the wasm files have no custom sections (no producers info).
- IJG obligation: binary-only redistribution requires the documentation to state "this software is based in part on the work of the Independent JPEG Group"; put that sentence in the app's notices.
- libtiff and giflib's reallocarray (ISC) require their copyright and permission notices in all copies: reproduce the COPYRIGHT file and the tif_luv.c and openbsd-reallocarray.c notices (texts listed).
- OpenLibm's LICENSE.md also mentions LGPL-2.1 test files (test-double.c, test-float.c); they are not part of the static library that is linked.
- Only the six *.wasm.js single-file builds are loaded in the browser (tesseract.js getCore.js with a core directory URL); the six *.js + *.wasm pairs (about 19.5 MB), index.js, README.md and package.json ship but are unused. Keep wasm/ocr/core/LICENSE if trimming.
- Security aside (not licensing): the image libraries are 2021-2022 snapshots (libwebp before the CVE-2023-4863 fix in 1.3.2, zlib 1.2.12, libtiff 4.3.0-dev, giflib 5.1.4). BentoPDF passes browser-rendered canvases to Tesseract (worker.recognize(canvas)), which limits exposure.

### PDF.js 5.5.207

- **In the app via:** pdfjs-dist 5.5.207 (BentoPDF dependency, bundled by Vite)
- **Used for:** PDF rendering, thumbnails, page rasterizing and text extraction in most tools (52 source files import pdfjs-dist; src/js/utils/helpers.ts getPDFDocument); pdf_viewer.css styles the Form Creator
- assets/main-CTXic8Nn.js (hashed name of this build; the other main-*.js chunk has no pdf.js code) and assets/form-creator-*.css are mixed Vite chunks: they also contain BentoPDF code and other npm packages (covered by Vite's license report, which lists pdfjs-dist 5.5.207 Apache-2.0). assets/pdf.worker-*.js is the Vite-rebundled build/pdf.worker.min.mjs; Vite's report leaves workers out.
- pdf_viewer.css images are inlined as data: URIs into assets/form-creator-*.css; one of them (altText_spinner.svg) carries an MPL-2.0 header (Mozilla/Firefox icon), hence MPL-2.0.txt. cursor-editorTextHighlight.svg is emitted as its own file (byte-identical to pdfjs-dist/web/images).
- BentoPDF passes wasmUrl = pdfjs-viewer/wasm/ (helpers.ts), so this library runs the OpenJPEG and qcms WebAssembly shipped with the 5.4.296 viewer (components pdfjs-openjpeg-wasm, pdfjs-qcms-wasm; the files are byte-identical to pdfjs-dist 5.5.207's own wasm/). pdfjs-dist 5.5.207 also has wasm/jbig2.wasm (PDFium-derived, BSD-3-Clause) which is NOT shipped: JBIG2 falls back to pdf.js's JS decoder. No cMapUrl/standardFontDataUrl/iccUrl is set, so the main app fetches no cmaps/standard fonts/ICC files.
- The worker contains the Emscripten/wasm-bindgen loader glue for those wasm modules (generated code, no separate notice in upstream).
- The Mozilla licence headers are stripped from the shipped Vite chunks (no "Copyright ... Mozilla Foundation" left in assets/pdf.worker-*.js, main-CTXic8Nn.js or form-creator-*.css), so PDF Toolbox's notices are the only place the attribution and Apache-2.0 text appear.

### PDFium with EmbedPDF (bentopdf-pdfium) 8ff5002c6cd5

- **In the app via:** bentopdf-pdfium (BentoPDF vendor/bentopdf-pdfium/bentopdf-pdfium-8ff5002c6cd5.tgz, file: dependency); imported by BentoPDF src/js/editcore/engine-loader.js
- **Used for:** PDF Editor (edit-pdf: EmbedPDF viewer engine for rendering, annotations, true redaction, forms; free-text flattening on save via src/js/utils/freetext-flatten.ts) and Edit PDF Text (edit-pdf-text: paragraph editing, shaping, font subsetting/re-encoding via the ec_* EditCore API)
- **Build:** https://github.com/alam00000/bentopdf-pdfium-viewer/tree/3ec97c1ea26601703353fbc3f390cc2a54f983bc: packages/pdfium/Dockerfile (FROM emscripten/emsdk:3.1.70), docker-compose.yml, scripts/build.sh (gclient sync of DEPS, GN args pdf_use_skia=false pdf_enable_xfa=false pdf_enable_v8=false pdf_is_complete_lib=true use_custom_libcxx=false target_os=wasm; applies build/patch/security-fixes.patch, editcore-pdfium.patch, brotli-decode.patch), build/compile.esm.sh (em++ -O3 -sUSE_ZLIB=1 ... -o pdfium.js), .github/workflows/build-pdfium.yml (CI build + publish). Vendored into BentoPDF by BentoPDF's .github/workflows/update-bentopdf-viewer.yml (copies pdfium.js/pdfium.wasm to editcore.js/editcore.wasm, writes package.json)
- Provenance (verified): editcore.wasm/editcore.js are byte-identical (git blob SHA1 0fe9a407... / 9cc85e42...) to packages/pdfium/src/vendor/pdfium.wasm / pdfium.js in alam00000/bentopdf-pdfium-viewer at 8ff5002c6cd5532f6fd2dffeeb43c56887dad5f8. '8ff5002c6cd5' is that fork's main HEAD (first 12 hex) when BentoPDF's update workflow ran (vendor/*/.upstream-version); it is NOT the Vite engineVersion hash (sha256(editcore.js+editcore.wasm)[:12] = 1c4976616d6a).
- The wasm binary was built by the fork's CI from commit 3ec97c1ea266 ('fix: include BrotliDecode') and committed by github-actions in f48637921bf4 ('chore: publish pdfium.wasm built from 3ec97c1ea266'); 8ff5002c6cd5 only changed TypeScript. So the Corresponding Source is the fork at 3ec97c1ea266 plus embedpdf/runtime@fce2b000cc7a and the DEPS-pinned third_party repos, built with emsdk 3.1.70. All of it is public (fork is a public GitHub repo with an AGPL-3.0 LICENSE, NOTICE and licenses/).
- Reproducibility caveats: the CI restores a cached ninja out/ dir (restore-keys pdfium-out-) and Docker layers; the Dockerfile's depot_tools and install-build-deps use moving 'main' heads. The fork README links a non-existent 'LICENSE-MIT' file (the MIT text is licenses/LICENSE.embedpdf-mit).
- License reading: package.json says the deprecated SPDX id 'AGPL-3.0' (no 'or later' grant anywhere) -> recorded as AGPL-3.0-only; BentoPDF says its own contributions are also available commercially. The binary combines AGPL (BentoPDF EditCore + modifications), MIT (EmbedPDF), Apache-2.0 (CloudPDF EPDF runtime additions; parts of PDFium), BSD-3-Clause (PDFium, Skia) and the libraries listed in includes; all permissive parts are AGPL-compatible. Apache-2.0 and BSD/MIT notices must be reproduced; no NOTICE file obligations beyond embedpdf/runtime's NOTICE (included).
- FTL advertising clause: product documentation must credit FreeType ('Portions of this software are copyright (C) <year> The FreeType Project (https://freetype.org). All rights reserved.'). IJG: documentation must state 'this software is based in part on the work of the Independent JPEG Group'.
- Included-library set inferred from GN deps at embedpdf/runtime@fce2b000 with the build's args (pdf_enable_xfa=false, pdf_enable_v8=false, pdf_use_skia=false): libtiff, bigint, dragonbox, V8, XFA, partition_alloc are NOT built; highway/fp16/cpu_features only serve full Skia (not built). Verified by strings: OpenJPEG, lcms ('cmsWhitePointFromTemp'), libpng '1.6.43', zlib messages, FreeType ('FREETYPE_PROPERTIES'), Brotli dictionary + 'BrotliDecode', Skia pathops source paths (../../third_party/skia/src/pathops/*), HarfBuzz paths (./code/harfbuzz/src/*), PDFium Chrome/Foxit font data. libjpeg-turbo (core/fxcodec and fpdfsdk deps; also used by EmbedPDF's epdf_jpeg_shim.cpp JPEG encoder), ICU (icuuc), Abseil and fast_float are linked per GN deps but not string-verifiable in the stripped wasm (no libjpeg message table: custom error handlers).
- Versions of FreeType, libjpeg-turbo, libpng, zlib, Brotli, ICU, Abseil, fast_float, lcms2, OpenJPEG, AGG come from README.chromium/README.pdfium at the DEPS-pinned revisions; libpng 1.6.43 is also confirmed by a string in the wasm. Chromium's libpng/zlib LICENSE copies carry older year ranges; the upstream LICENSE of the same version is reproduced instead.
- compile.esm.sh links with -sUSE_ZLIB=1 (Emscripten's zlib port, zlib 1.2.13 in emsdk 3.1.70), but no EditCore/ext source includes zlib.h and PDFium uses Chromium's Cr_z_-prefixed zlib, so the port is most likely not linked (unverified; same Zlib license either way).
- The spell-check feature (ec_spell_*) fetches 'dict/en.txt.gz', which BentoPDF does not ship (no dictionary in the APK), so no word-list license applies.
- Trademarks: the fork README notes 'EmbedPDF' and 'CloudPDF' are brand names of CloudPDF; PDFium is a Google project. Nothing of these marks is shown in PDF Toolbox's UI from this component.

### qpdf (qpdf-wasm) 12.2.0 (qpdf-wasm 0.3.0)

- **In the app via:** npm @neslinesli93/qpdf-wasm@0.3.0 (BentoPDF dependency): dist/qpdf.js glue bundled by Vite into the main chunk; the wasm ships as BentoPDF's public/qpdf.wasm, byte-identical to the package's dist/qpdf.wasm
- **Used for:** Encrypt PDF, Change Permissions, Remove Restrictions/decrypt, Linearize, Repair PDF, Overlay PDF, Split PDF, Workflow nodes (encrypt, linearize, overlay, repair), and the automatic decrypt/repair fallback when pdf-lib cannot load a file (utils/load-pdf-document.ts)
- **Build:** https://github.com/neslinesli93/qpdf-wasm/blob/0.3.0/Dockerfile and build.sh (emscripten/emsdk:3.1.74; -Oz -flto; --closure 1; js/pre.js, js/post.js)
- public/qpdf.wasm (shipped at the web root, loaded via locateFile '/qpdf.wasm') is byte-identical to the package's dist/qpdf.wasm (sha256 abd933f4ccace4f732999381b21aec8b7e3726f18a5b167fafd57f88dd440876). The Emscripten glue dist/qpdf.js is bundled into assets/main-*.js (only that part of the chunk belongs to this component).
- The wrapper declares ISC (package.json; Vite's report shows ISC without text) but neither the npm package nor the GitHub repo has a LICENSE file or copyright line; template-ISC.txt is referenced for lack of an upstream text. Its own contribution is tiny (build scripts, js/pre.js, js/post.js, d.ts).
- Apache-2.0 s.4(d): qpdf's NOTICE.md must be reproduced (it also carries the sphlib MIT notice and the Rijndael public-domain note). qpdf's NOTICE lets recipients alternatively treat qpdf under Artistic-2.0 (pre-v7 terms); we rely on Apache-2.0.
- RSA-MD: material mentioning qpdf's MD5 must identify it as 'derived from the RSA Data Security, Inc. MD5 Message-Digest Algorithm'.
- IJG: product documentation must say 'This software is based in part on the work of the Independent JPEG Group.' The TurboJPEG API is not linked (-ljpeg only), so the BSD-3-Clause part is included for completeness.
- Verified in the binary: qpdf '12.2.0', 'Copyright (c) 2005-2021 Jay Berkenbilt', 'Copyright (c) 2022-2025 Jay Berkenbilt and Manfred Holger', 'libjpeg-turbo version 2.1.1 (build 20250627)', QPDFCrypto_native only (no GnuTLS/OpenSSL). Inferred from the Dockerfile only: zlib 1.2.12 (no zlib version or copyright string survives -Oz -flto) and dlmalloc as Emscripten's default allocator.
- Emscripten 3.1.74's LICENSE, musl COPYRIGHT and libc++ LICENSE.TXT are byte-identical to the emscripten-4.0.15--* texts already in texts/ (md5 verified), so those are referenced.

### libvips (wasm-vips) 8.18.1 (wasm-vips 0.0.17)

- **In the app via:** npm wasm-vips@0.0.17 (BentoPDF dependency). Vite emits lib/vips.wasm (imported as 'wasm-vips/vips.wasm?url') and bundles lib/vips-es6.js twice: the module chunk and a copy used as the pthread worker script
- **Used for:** PDF to TIFF: pages rendered by pdf.js are encoded by libvips into single- or multi-page TIFF (LZW, Deflate, JPEG, PackBits or no compression)
- **Build:** https://github.com/kleisauke/wasm-vips/blob/v0.0.17/build.sh (defaults: SIMD, modules, UHDR/JXL/AVIF/SVG on) run in the Dockerfile at the same tag (docker.io/emscripten/emsdk:5.0.3 + the two Emscripten patches above; Rust nightly-2026-03-19 only for the resvg side module); JS/C++ bindings: src/ and meson.build at the tag
- Only the main module ships: assets/vips-C9VSaDuC.wasm is byte-identical to wasm-vips 0.0.17 lib/vips.wasm. The side modules lib/vips-heif.wasm (libheif + aom), vips-jxl.wasm (libjxl + brotli) and vips-resvg.wasm (resvg + Rust crates) are not in the APK, and BentoPDF passes dynamicLibraries: [] so they are never requested (the glue still names vips-jxl.wasm/vips-heif.wasm as defaults). wasm-vips's THIRD-PARTY-NOTICES.md (reproduced as shipped upstream) lists aom, brotli, libheif, libjxl and resvg too; those do not apply to PDF Toolbox's files.
- LGPL: vips.wasm statically links LGPL-2.1-or-later code (libvips, GLib, libexif; wasm-vips's notice says it uses them under LGPLv3 via the 'any later version' clause) together with MIT/BSD/Apache code. Obligations when shipping the APK: LGPL text and notices; the complete corresponding source of those libraries INCLUDING wasm-vips's patches; and, because everything is linked into one wasm, the means to relink with a modified library (LGPL-2.1 s.6(a) / LGPL-3.0 s.4(d)(0)): satisfied by offering the wasm-vips v0.0.17 source and build.sh together with all pinned dependency sources.
- Provenance risk for that source offer: build.sh applies patches fetched from GitHub compare URLs on kleisauke's branches, which can be force-pushed or deleted. As fetched on 2026-09-27: libvips patch sha256 a5d09c00b0be2e7e1d5b608b4638bfcf2c77d26ec8f2be04579eeccc01a1b1dd, glib patch c6fe50bf0d348d14691738f7b35acc7470c30b6f104360829c292b7b37d71b70, emscripten wasm-vips-5.0.3 patch 0dffd4e429472f850042e0938faa56dadc9061f74575549f539215391c703d7e, mimalloc-update-3.2.8 patch 16b08eef67d7d0e2e4dd7d2cd9cb4f4cd55b480574d28a0858e34eb3002f3b6b, libjpeg-turbo a60fb46 patch 707c465f0215a786843438a352039bf18ccc83e5bb374670270c1e4e753bbe8b, libultrahdr 5ed39d6 patch 8e1d51b65d057a1b9337172f4c3479ee6431d00dd585d3fd43f6a07c2c0b3244. Whether these equal what was applied for the March 2026 build is not verifiable; mirror them with the source offer.
- libultrahdr (UHDR load/save is compiled in): its NOTICE 'This product includes Gain Map technology under license by Adobe.' must be reproduced; Adobe's underlying license terms are not published in the repo.
- IJG (mozjpeg): product documentation must say 'This software is based in part on the work of the Independent JPEG Group.'
- libtiff's LZW codec (BentoPDF's default TIFF compression) carries the old Berkeley 'compress' notice: materials related to distribution must acknowledge that the software was developed by the University of California, Berkeley (excerpt in libtiff-4.7.1--libtiff-tif_lzw.c-notice.txt; no exact SPDX id, hence LicenseRef-BSD-compress-1985). LicenseRef-Radiance-2.0 = the Radiance Software License 2.0 text in the radiance.c excerpt; LicenseRef-Leffler-1988-legend = the legend in the vips2tiff.c/tiff2vips.c excerpt.
- libvips's Radiance code (RAD load/save is enabled in this build) requires the Radiance Software License 2.0 notice in binary distributions; vips2tiff.c/tiff2vips.c carry Sam Leffler's legend that must be included 'as a part of the software program'. Both are reproduced as excerpts.
- libimagequant 2.4.1 is Lovell Fuller's fork of the last BSD-licensed libimagequant (not GPL-3.0 v2.5+/v4); the Jef Poskanzer notice in its COPYRIGHT is the SPDX HPND-Pbmplus text (compared with SPDX license-list-data).
- Highway is dual-licensed; either Apache-2.0 or BSD-3-Clause may be chosen (no NOTICE file upstream). libwebp's PATENTS (Google's patent grant) is included.
- GLib: only LGPL-2.1-or-later code is linked as far as determinable (GLib also contains xdgmime under LGPL-2.1-or-later OR AFL-2.0, and c-utf8 code dual Apache-2.0 OR LGPL-2.1+ in gutf8.c; no xdgmime/PCRE2 strings are present in vips.wasm).
- Emscripten 5.0.3's LICENSE, musl COPYRIGHT and libc++ LICENSE.TXT are byte-identical to the emscripten-4.0.15--* texts already in texts/ (md5 verified), so those files are referenced; libc++abi and compiler-rt LICENSE.TXT carry the same Apache-2.0 WITH LLVM-exception terms (differ only in the library name).
- Versions not visible in the binary (GLib, libffi, expat, libexif, lcms2, highway, libimagequant, cgif, libwebp, libtiff) come from versions.json and build.sh pins, not from binary strings.
- Vite's own license report lists wasm-vips only as MIT; the LGPL and third-party parts above are not in it.

### Pyodide 0.28.0a3

- **In the app via:** @bentopdf/pymupdf-wasm 0.11.16 assets/
- **Used for:** Python runtime for PyMuPDF and the other wheels
- **Build:** pyodide repo Makefile/Makefile.envs at ed567eb8d2b41fb0e325927c44466b866ef56a34 (PYVERSION 3.13.2, PYODIDE_EMSCRIPTEN_VERSION 4.0.9) and cpython/Makefile
- Alpha pre-release. The npm package metadata (src/js/package.json) declares "Apache-2.0" while the repository LICENSE is MPL-2.0; follow the LICENSE file (MPL-2.0) and note the discrepancy. SQLite and OpenSSL are separate Pyodide packages and are not shipped. pyodide-lock.json lists 329 packages but only the nine wheels below are shipped.

### BentoPDF PDF Viewer (EmbedPDF) 2.9.1

- **In the app via:** bentopdf-viewer (BentoPDF vendor/bentopdf-viewer/bentopdf-viewer-8ff5002c6cd5.tgz, file: dependency); dynamically imported by src/js/logic/edit-pdf-page.ts
- **Used for:** PDF Editor (edit-pdf): the complete viewer/editor UI (rendering, thumbnails, search, annotations, true redaction, forms, attachments, bookmarks, export/print); runs on the shared bentopdf-pdfium engine (EmbedPDF.init({ wasmUrl: editcore.wasm }))
- **Build:** BentoPDF .github/workflows/update-bentopdf-viewer.yml: clone https://github.com/alam00000/bentopdf-pdfium-viewer main, 'pnpm install --no-frozen-lockfile', 'pnpm run build:snippet' (viewers/snippet/rollup.config.js, rollup + babel + terser, preact/compat aliased for react), 'npm pack ./viewers/snippet', delete dist/pdfium.wasm, rename to bentopdf-viewer and drop @embedpdf/* deps from package.json
- package.json of the vendored tarball says 'MIT' (inherited from @embedpdf/snippet), but the source repo alam00000/bentopdf-pdfium-viewer was relicensed to AGPL-3.0 in e3c3e619d525 ('Relicense to AGPL-3.0 and rebrand as BentoPDF PDF Viewer'); its NOTICE keeps EmbedPDF's MIT notice (Copyright 2025 CloudPDF). So BentoPDF's modifications are AGPL-3.0 (only; no or-later grant) and the EmbedPDF base stays MIT. Vite's license report lists it as MIT only.
- The vendored tarball has no LICENSE file (upstream npm @embedpdf/snippet@2.9.1 ships one; the fork's viewers/snippet has none), so the MIT text must come from our notices (embedpdf-2.9.1--LICENSE.txt, identical to upstream).
- Vite re-minified the chunks; the '/*! regenerator-runtime -- Copyright (c) 2014-present, Facebook, Inc. -- license (MIT) */' comment present in the tarball's dist was dropped from the shipped assets/embedpdf-*.js, so that notice must be reproduced separately (babel-helpers LICENSE). The tailwindcss '/*! tailwindcss v4.1.18 \| MIT License */' comment survives.
- Bundled third-party code versions come from the fork's pnpm-lock.yaml at 8ff5002c6cd5 (preact 10.28.3, tailwind-merge 3.4.0, @floating-ui/dom 1.7.5 + core 1.7.4 + utils 0.2.10, tailwindcss 4.1.18, @babel/helpers 7.28.6); BentoPDF's workflow ran 'pnpm install --no-frozen-lockfile', so exact versions are inferred, not string-verified (tailwindcss 4.1.18 and snippet 2.9.1 are verified by strings). @floating-ui is imported by viewers/snippet/src/components/ui/{dropdown,tooltip}.tsx (GitHub code search).
- Icon provenance is inferred from matching SVG path data for two samples (device-floppy = Tabler v2.47.0 exactly, alert-triangle = Feather exactly); other icons were not checked individually.
- The dist also contains demo.pdf, demo-annotations.pdf, ebook.pdf and index.html, which are not in the web root (not imported). The bundle contains jsDelivr fallback URLs for @embedpdf/pdfium@2.9.1 pdfium.wasm and @embedpdf/fonts-*; BentoPDF passes wasmUrl and VITE_EMBEDPDF_FONTS_URL so they are not fetched offline.
- 'EmbedPDF'/'CloudPDF' are CloudPDF brand names (fork README: no trademark rights granted); the EmbedPDF logo is referenced only in the README (remote URL), not shipped.

### Emscripten runtime (in LibreOffice and Pyodide) 3.1.74, 4.0.9

- **In the app via:** @matbee/libreoffice-converter (soffice.*), Pyodide (pyodide.asm.*), Pyodide-built wheels (side modules import libc from pyodide.asm.wasm)
- **Used for:** Runtime support for every WebAssembly engine in this part
- License files are byte-identical at 3.1.74 and 4.0.9. The same runtime also sits in the other agent's WASM modules (Ghostscript, CPDF, Tesseract, ...); declare it once.

### fontTools 4.56.0

- **In the app via:** @bentopdf/pymupdf-wasm 0.11.16 assets/ (from Pyodide 0.28.0a3 CDN)
- **Used for:** Font handling for pdf2docx
- **Build:** Pyodide recipe packages/fonttools/meta.yaml at ed567eb8d2b41fb0e325927c44466b866ef56a34 (repackages the PyPI wheel)
- LICENSE.external is not in the wheel dist-info; fetched from the 4.56.0 tag. Test fonts listed there (OFL) are not in the wheel.

### heic2any (with libheif and libde265) 0.0.4

- **In the app via:** npm heic2any@0.0.4 (BentoPDF dependency; dist/heic2any.js bundled by Vite into its own chunk)
- **Used for:** HEIC/HEIF decoding (converted to PNG first): HEIC to PDF, HEIC/HEIF files added to Image to PDF, the PDF Multi Tool and the Workflow Builder's image input
- **Build:** heic2any build/build.ts at tag 0.0.4 (tsc + buble + uglify; wraps src/libheif.js into a Blob worker string); libheif.js itself: libheif v1.10.0 build-emscripten.sh with pre.js/post.js (https://github.com/strukturag/libheif/blob/v1.10.0/build-emscripten.sh; pins libde265 1.0.2, asm.js output, --memory-init-file 0)
- heic2any declares only MIT (package.json, LICENSE.md, Vite's report), but dist/heic2any.js embeds, as a worker-source string, libheif.js: libheif 1.10.0 + libde265 1.0.2 compiled to asm.js with Emscripten, both LGPL-3.0-or-later. No LGPL notice survives in the shipped chunk: heic2any's uglify step and Vite's minifier strip comments (even gifshot's Yahoo MIT header is gone from assets/heic2any-*.js), so PDF Toolbox's notices must supply the LGPL-3.0 and GPL-3.0 texts and the copyright lines.
- LGPL-3.0 s.4 obligations for this Combined Work: prominent notice + license texts; Minimal Corresponding Source of the library (libheif 1.10.0 and libde265 1.0.2 sources and the build recipe: libheif v1.10.0 build-emscripten.sh, pre.js, post.js) and the Corresponding Application Code (heic2any 0.0.4 source) so a user can rebuild with a modified libheif. PDF Toolbox's AGPL source offer should include or point to these exact sources.
- Provenance (verified): heic2any 0.0.4 src/libheif.js equals libheif's gh-pages libheif.js at commit d7d6f2bd6b5e793f1f4dd483cf18a0ad57ac7237 (2020-12-17, message 'Update to libheif 1.10.1') after normalising CRLF line endings, plus a trailing '// .... end libheif' comment. Inferred: built from libheif v1.10.0 (commit 667eeabb553c): the embedded version string is '1.10.0', no v1.10.1 tag exists, and master had no further commits until at least 2020-12-18. The Emscripten version used is unknown.
- libde265 1.0.2 is read from the embedded string following 'libde265 HEVC decoder, version ' and matches the LIBDE265_VERSION=1.0.2 pin in libheif v1.10.0's build-emscripten.sh. libde265's md5.cc is linked (SEI 'decoded picture MD5 mismatch' strings present).
- npm's gitHead for heic2any 0.0.4 (3222e591, a 2020 commit) is stale; the published dist/heic2any.js is byte-identical to dist/heic2any.js at tag 0.0.4.
- gifshot 0.4.5's NeuQuant code requires 'that this copyright notice remain intact' (no SPDX id, hence LicenseRef-NeuQuant); libde265's md5.cc is public domain with a permissive fallback (LicenseRef-Public-Domain, no notice required); omggif's MIT notice is also reproduced (both as verbatim excerpts from the gifshot 0.4.5 npm sources). BentoPDF requests image/png, so the GIF path is unused, but the code ships.
- Emscripten texts: the current Emscripten LICENSE/musl/libc++ texts (emscripten-4.0.15--*) are referenced; that the 2020 build used identical terms is inferred (Emscripten has been MIT OR NCSA throughout).
- Aside (not licensing): libheif 1.10.0 and libde265 1.0.2 are old releases with published CVEs; they parse user-supplied HEIC files inside a Web Worker.

### LibreOffice converter (@matbee/libreoffice-converter) 2.3.1 and 2.6.0

- **In the app via:** BentoPDF 2.8.8 public/libreoffice-wasm/ (vendored copy in the BentoPDF repo, not taken from node_modules) + npm dependency @matbee/libreoffice-converter ^2.5.0 resolved to 2.6.0 (bundled by Vite)
- **Used for:** Office-to-PDF conversion: Word (doc/docx), Excel (xls/xlsx), PowerPoint (ppt/pptx), ODT/ODS/ODP/ODG, RTF, WPS/WPD/Pages/VSD/PUB pages and the matching workflow nodes (src/js/utils/libreoffice-loader.ts)
- **Build:** build/build-wasm.sh, build/autogen.input, build/Dockerfile.build, build/patches/wasm-build-fixes.patch in the same repo (unchanged between the binary commit 749a21a4 and v2.4.0)
- No LICENSE file exists in the GitHub repo (GitHub reports license: null) or in the npm package; MPL-2.0 is declared only in package.json ("license": "MPL-2.0") and the README ("MPL-2.0 (same as LibreOffice)"). No copyright holder is named (package.json author is empty; repo owner is GitHub user matbeedotcom). Ship the MPL-2.0 text ourselves and point to the repo for Source Code Form (MPL-2.0 s3.2). browser.worker.global.js sourcemap lists only the package's own src/*.ts (no bundled npm deps). soffice.js/soffice.worker.js are Emscripten-generated LibreOffice glue, post-processed by build-wasm.sh (PACKAGE_NAME path fix, browser copies). BentoPDF's package.json pulls 2.6.0, but the engine files BentoPDF ships are the older 2.3.x set; lessons.md in the BentoPDF repo says the vendored files must not be swapped independently.

### lxml 5.4.0

- **In the app via:** @bentopdf/pymupdf-wasm 0.11.16 assets/ (from Pyodide 0.28.0a3 CDN)
- **Used for:** XML backend for python-docx (PDF to DOCX)
- **Build:** Pyodide recipes at ed567eb8d2b41fb0e325927c44466b866ef56a34: packages/lxml, packages/libxml, packages/libxslt, packages/zlib, packages/libiconv meta.yaml
- GNU libiconv 1.16 (LGPL-2.1) is listed as a host requirement in the recipe, but it is NOT linked: etree.so imports iconv/iconv_open/iconv_close from the Pyodide main module (musl libc) and contains no libiconv_open symbol and none of libiconv's alias tables (KOI8-R, CP1252, ...). No LGPL obligation arises from lxml as shipped (inferred from the binary).

### MuPDF 1.26.3

- **In the app via:** PyMuPDF 1.26.3 wheel (PyMuPDF.libs/libmupdf.so)
- **Used for:** PyMuPDF-based tools: EPUB/MOBI/FB2/CBZ/XPS/email/image/TXT/PSD-to-PDF, compress, deskew, rasterize, redact, extract images/tables, PDF-to-text/SVG/CSV/Excel/Markdown/DOCX/PDF-A, PDF layers, prepare-for-AI, decrypt (src/js/utils/pymupdf-loader.ts); all nine wheels are loaded at PyMuPDF init
- **Build:** Built by PyMuPDF setup.py (flavour pb) inside the Pyodide recipe; Tesseract/Leptonica disabled (PYMUPDF_SETUP_MUPDF_TESSERACT=0), no libcrypto
- MuPDF is dual AGPL/commercial; used under AGPL. Tesseract, Leptonica, curl, freeglut and libarchive are in the source tree but not compiled in (no tesseract/leptonica strings; flavour pb). HarfBuzz is an old 6.0.0 snapshot as pinned by MuPDF. The embedded Noto set has 179 resource blobs; Source Han Serif is not embedded (only its name appears). Third-party versions come from headers in the source tarball; the exact submodule commits are those of MuPDF tag 1.26.3.

### NumPy 2.2.5

- **In the app via:** @bentopdf/pymupdf-wasm 0.11.16 assets/ (from Pyodide 0.28.0a3 CDN)
- **Used for:** Array support for OpenCV (deskew) and pdf2docx
- **Build:** Pyodide recipe packages/numpy/meta.yaml at ed567eb8d2b41fb0e325927c44466b866ef56a34 (-Dallow-noblas=true: no BLAS/LAPACK library, bundled lapack_lite used)
- The Pyodide wheel ships only the 30-line numpy LICENSE; bundled-code licenses fetched from the v2.2.5 tag. No OpenBLAS; no Highway/SVML/x86-simd-sort code found in the wasm build.

### OpenCV (opencv-python) 4.11.0.86

- **In the app via:** @bentopdf/pymupdf-wasm 0.11.16 assets/ (from Pyodide 0.28.0a3 CDN)
- **Used for:** Deskew (Canny/HoughLinesP) and image processing helpers in the PyMuPDF wrapper; imported at init
- **Build:** Pyodide recipe packages/opencv-python (meta.yaml, extras/build_args.sh, extras/*.cmake, patches) at ed567eb8d2b41fb0e325927c44466b866ef56a34; FFmpeg/libwebp/libtiff from Pyodide recipes packages/ffmpeg, libwebp, libtiff at the same commit
- LGPL: FFmpeg 4.4.1 is statically linked into cv2.so, so LGPL-2.1 s6 applies: provide the FFmpeg source plus the means to relink (the full opencv-python sdist + Pyodide recipe + FFmpeg tarball, i.e. the complete buildable source, satisfies s6(a) because the rest is open source). The wheel's LICENSE-3RD-PARTY.txt is the generic PyPI one (lists Qt, libvpx, OpenSSL, etc. that are NOT in this wasm build) but contains the correct texts for OpenCV (Apache-2.0), FFmpeg (LGPL-2.1), libwebp, libpng, zlib, bzip2, TIFF, protobuf and flatbuffers. JPEG is IJG libjpeg 9f (not libjpeg-turbo as that file says). BUILD_ZLIB=OFF, WITH_OPENJPEG/QUIRC/IPP/ITT/OPENEXR=OFF. bzip2 is imported from pyodide.asm.wasm.

### OpenJPEG (in PDF.js) 2.5.4

- **In the app via:** BentoPDF public/pdfjs-viewer/wasm (= pdf.js 5.4.296 web/wasm)
- **Used for:** JPEG 2000 (JPX) image decoding for the main app's pdfjs-dist (wasmUrl pdfjs-viewer/wasm/) and the pdf.js viewer
- **Build:** https://github.com/mozilla/pdf.js.openjpeg/tree/b47d31b8355a3863ab37282ceeb5183f7ac2761c (Dockerfile, compile_lib.sh, compile.sh, build.js; image emscripten/emsdk:latest)
- openjpeg_nowasm_fallback.js is the same decoder compiled to plain JS (used when WebAssembly is unavailable).
- The binary carries no version string or producers section; the OpenJPEG version comes from pdf.js commit e9394d0f6302 ("Update OpenJPEG to 2.5.4", 2025-09-21) and the pinned OPENJPEG_GIT_HASH in the build repo's Dockerfile, which is the v2.5.4 tag commit. Emscripten version inferred from the build date (texts referenced are version-independent: LICENSE identical in 3.1.70, 4.0.15 and 4.0.22).
- LICENSE_OPENJPEG is byte-identical to OpenJPEG v2.5.4 LICENSE. Files byte-identical to pdf.js 5.4.296 web/wasm and to pdfjs-dist 5.5.207 wasm/.

### PDF.js annotation viewer (modified by BentoPDF) 4.3.136

- **In the app via:** BentoPDF public/pdfjs-annotation-viewer (from Laomai-codefee/pdfjs-annotation-extension examples/pdfjs-4.3.136-dist)
- **Used for:** Add Stamps (src/js/logic/add-stamps.ts) loads pdfjs-annotation-viewer/web/viewer.html in an iframe
- **Build:** pdf.js gulpfile at the tag; OpenJPEG decoder from https://github.com/mozilla/pdf.js.openjpeg/tree/393eed5fbaea512ea6bdfe1be6305d4add3c354c (pdf.js commit 699e8aa3e41c); QuickJS via mozilla/pdf.js.quickjs
- build/* (pdf.mjs, pdf.worker.mjs, pdf.sandbox.mjs and their .map), web/viewer.css, web/viewer.mjs.map, images, cmaps, standard_fonts, LICENSE are byte-identical to the pdf.js 4.3.136 release zip. web/viewer.mjs: Laomai's example edits (annotationMode 0, default editor mode 0, file-origin check commented out) plus BentoPDF's (no default PDF); web/viewer.html: Laomai's script tag for the extension plus BentoPDF's HASH_PARAMS shim and prettier formatting. No change notices in the files (Apache-2.0 sec. 4(b)).
- pdf.js 4.3.136 (2024) is outdated; not a licence issue, but the example viewer disables pdf.js's check that a ?file= URL has the viewer's origin (security note, not licence).
- pdfjs-annotation-viewer/LICENSE is pdf.js's Apache-2.0 LICENSE (identical to pdfjs-dist-5.5.207--LICENSE.txt).
- Emscripten text referenced is version-independent (identical LICENSE in 3.1.70 and 4.0.x); the emscripten version of the 2024 OpenJPEG build is not recorded.

### PDF.js viewer (modified by BentoPDF) 5.4.296

- **In the app via:** BentoPDF public/pdfjs-viewer (copied into the web root by Vite)
- **Used for:** Sign PDF (src/js/logic/sign-pdf-page.ts) and Form Filler (form-filler-page.ts) load pdfjs-viewer/viewer.html in an iframe; the typed-signature font/colour picker is a BentoPDF addition
- **Build:** pdf.js gulpfile (gulp generic / dist) at the tag; QuickJS sandbox built with https://github.com/mozilla/pdf.js.quickjs (pdf.js external/quickjs/README.md)
- Byte-identical to upstream 5.4.296: pdf.worker.mjs, pdf.sandbox.mjs, viewer.mjs.map (release zip), pdf_viewer.mjs.map, pdf_viewer.d.mts (npm pdfjs-dist 5.4.296), all 73 images. Modified by BentoPDF (no change notice in the files; Apache-2.0 sec. 4(b) asks for one): pdf.mjs (signature colour), viewer.mjs (signature font/colour controls, default annotationEditorMode 1, no default PDF, paths to pdf.worker/pdf.sandbox), viewer.html (flattened paths, font/colour picker), viewer.css (prettier-reformatted plus @font-face rules for the extra signature fonts), pdf_viewer.mjs (worker paths), pdf_viewer.css (3 CSS-variable tweaks).
- BentoPDF's modifications carry no license statement of their own; as part of the BentoPDF repository they are presumably AGPL-3.0-only (BentoPDF's licence) - inferred, not stated.
- pdfjs-viewer/form-viewer.html and sign-viewer.html are BentoPDF-authored pages ("... - Bento PDF"), not pdf.js; they belong to BentoPDF's own AGPL-3.0-only component (and are not referenced from src/, apparently unused).
- No top-level LICENSE file ships in pdfjs-viewer/ (the licence is only in file headers); PDF Toolbox's notices must supply the Apache-2.0 text.
- The viewer's AppOptions keep upstream defaults cMapUrl ../web/cmaps/, standardFontDataUrl ../web/standard_fonts/, iccUrl ../web/iccs/, wasmUrl ../web/wasm/, which resolve outside pdfjs-viewer/ in BentoPDF's flattened layout; so this viewer probably never loads the cmaps/standard_fonts/iccs/wasm shipped next to it (inferred from the code, not tested). The extra signature fonts are loaded via viewer.css.
- Sub-components with their own licences are separate entries: pdfjs-openjpeg-wasm, pdfjs-qcms-wasm, pdfjs-standard-fonts-foxit, pdfjs-standard-fonts-liberation, pdfjs-cmaps, pdfjs-iccs, pdfjs-l10n, font-alex-brush, font-allura, font-handlee, font-kalam-ttf, font-sacramento.

### pdf2docx 0.5.8

- **In the app via:** @bentopdf/pymupdf-wasm 0.11.16 assets/
- **Used for:** PDF to DOCX
- Shipped as GPL-3.0 (METADATA "GPL v3", LICENSE = GPLv3 text; no "or later" grant found, hence -only). The @bentopdf README wrongly calls it AGPL-3.0. GPL-3.0 and AGPL-3.0 may be combined (s13 of both). Upstream relicensed to MIT on 2026-03-09 (commit ce5ba003), which does not apply to 0.5.8. METADATA also requires opencv-python-headless and fire, which are not shipped (opencv-python is used instead).

### pdfjs-annotation-extension 2.2.0

- **In the app via:** BentoPDF public/pdfjs-annotation-viewer/web/pdfjs-annotation-extension
- **Used for:** Add Stamps (src/js/logic/add-stamps.ts) loads pdfjs-annotation-viewer/web/viewer.html in an iframe (stamps, shapes, signatures, comments on top of the pdf.js 4.3.136 viewer)
- **Build:** webpack: configuration/webpack.prod.config.js in the repo at v2.2.0 (`npm run build`); BentoPDF's patch of the minified bundle is not published anywhere (its fork alam00000/pdfjs-annotation-extension has no own commits)
- Provenance VERIFIED: after replacing base64 images with a placeholder, the shipped bundle differs from the upstream v2.2.0 release asset in exactly 3 places: the two handwriting-font entries (label and URL changed to Kalam.ttf / Allura.ttf, replacing the upstream Chinese fonts "PingFangChangAnTi-2" and "qiantubifengshouxieti", which are not shipped) and DEFAULT_STAMP (6 upstream stamps replaced by 12 other PNGs). So the code is exactly upstream v2.2.0 (commit f3f120a7639b578b3fdecd347856a2f9b402ad9a) as built by the upstream author; the corresponding source is that tag.
- RED FLAG (attribution): the bundle begins "For license information please see pdfjs-annotation-extension.js.LICENSE.txt", but that file is shipped neither upstream nor by BentoPDF. pdfjs-annotation-extension-2.2.0--bundled-third-party-notices.txt is a RECONSTRUCTION: dependency closure of the extension's imports resolved with npm --before=2025-06-27 (upstream has no lockfile), plus the ExcelJS browser bundle's modules resolved as of 2023-10-19. Confirmed versions: react/react-dom 18.3.1, konva 9.3.20, jszip 3.10.1, elliptic 6.5.4, core-js 3.33.0; the rest inferred; tree-shaking may have dropped some.
- RED FLAG (unknown rights): the 12 stamp images added by BentoPDF have no stated source or licence.
- jszip is dual MIT OR GPL-3.0-or-later: choose MIT. pako is MIT AND Zlib (Zlib.txt).
- pdfjs-annotation-extension-testdata.json is the upstream example data (examples/pdfjs-4.3.136-dist, v2.2.0) with four null values changed to 0 by BentoPDF; shipped but unused by BentoPDF's code (it passes its own ae_* hash parameters).
- The extension's fonts (Kalam.ttf, Allura.ttf) are separate components (font-kalam-ttf, font-allura).

### PyMuPDF for WebAssembly (@bentopdf/pymupdf-wasm) 0.11.16

- **In the app via:** BentoPDF air-gap bundle bentopdf-pymupdf-wasm-0.11.16.tgz extracted with --strip-components=1 to wasm/pymupdf/
- **Used for:** PyMuPDF-based tools: EPUB/MOBI/FB2/CBZ/XPS/email/image/TXT/PSD-to-PDF, compress, deskew, rasterize, redact, extract images/tables, PDF-to-text/SVG/CSV/Excel/Markdown/DOCX/PDF-A, PDF layers, prepare-for-AI, decrypt (src/js/utils/pymupdf-loader.ts); all nine wheels are loaded at PyMuPDF init
- **Build:** build_scripts/ in the package (Dockerfile, scripts/download.js, buildDeps.js, build.js) - stale, see notes
- Its build_scripts claim to be the AGPL "Corresponding Source" but do not match what ships: buildDeps.js/download.js pin PyMuPDF commit 4a53405a (tag 1.26.1) and copy "pymupdf-1.26.1-...whl", download Pyodide v0.28.0a3 assets and PyPI wheels, and have no entry for pymupdf4llm; the shipped pymupdf-1.26.3 wheel is instead byte-identical to the official Pyodide 0.29.0/0.29.1 build. The Docker/Emscripten 4.0.9/pyodide-build 0.30.5 environment is plausible. README credits list pdf2docx as AGPL-3.0; the shipped pdf2docx 0.5.8 is GPL-3.0 (compatible, but the attribution is wrong). README also mentions Ghostscript (covered by the other agent). dist/index.js has no bundled third-party code.

### PyMuPDF4LLM 0.0.27

- **In the app via:** @bentopdf/pymupdf-wasm 0.11.16 assets/ (downloaded from PyPI; not listed in its download.js)
- **Used for:** PDF to Markdown, "prepare PDF for AI"
- Dual licensed (AGPL-3.0 or Artifex commercial). The wheel has no license file; LICENSE fetched from the RAG repo at tag v0.0.27 (AGPL-3.0 text). Source headers say AGPL-3.0-or-later.

### Python (CPython) 3.13.2

- **In the app via:** Pyodide 0.28.0a3
- **Used for:** Python runtime
- **Build:** pyodide cpython/Makefile
- Doc/license.rst ("Licenses and Acknowledgements for Incorporated Software") is shipped because the PSF LICENSE file alone does not cover the incorporated third-party code.

### python-docx 1.2.0

- **In the app via:** @bentopdf/pymupdf-wasm 0.11.16 assets/
- **Used for:** DOCX writing for pdf2docx
- Includes default .docx templates (part of the package, same license).

### qcms (in PDF.js) 0.3.0

- **In the app via:** BentoPDF public/pdfjs-viewer/wasm (= pdf.js 5.4.296 web/wasm)
- **Used for:** ICC-based colour conversion (ICC colour spaces, CMYK to RGB) for the main app's pdfjs-dist and the pdf.js viewer
- **Build:** https://github.com/mozilla/pdf.js.qcms/tree/fc23a407f1ed9ccfea15875d27e0936dcc798a1f (Dockerfile rust:latest + cargo update, compile.sh wasm-pack)
- Crate versions from the binary: cargo registry paths qcms-0.3.0 and once_cell-1.21.3, producers section "rustc 1.87.0 (17067e9ac 2025-05-09), walrus 0.23.3, wasm-bindgen 0.2.100". The build repo's Cargo.lock at fc23a407 says once_cell 1.20.3, but its Dockerfile runs `cargo update`, so the build is not exactly reproducible from the lockfile.
- Licence labelling inconsistency (both permissive): pdf.js ships LICENSE_PDFJS_QCMS as BSD-2-Clause (Mozilla Foundation 2025) while the pdf.js.qcms repository's LICENSE and src/lib.rs header say MIT.
- Build repo commit chosen as the one matching pdf.js 5.4.296's last qcms update (pdf.js 782e883a8728, 2025-05-19, "Remove all the useless subarrays" = pdf.js.qcms fc23a407, same day) - inferred from dates and messages.

### tesseract.js (worker) 7.0.0

- **In the app via:** BentoPDF air-gap bundle (scripts/prepare-airgap.sh: npm pack tesseract.js@7.0.0); PDF Toolbox tools/webapp.sh extracts only package/dist/worker.min.js
- **Used for:** OCR: runs Tesseract in a Web Worker for the OCR PDF tool (searchable PDF), the Workflow Builder's OCR node and Compare PDFs (OCR of image-only pages)
- **Build:** webpack: scripts/webpack.config.prod.js (npm run build) in the repo/package at v7.0.0; bundled dependency versions from the tag's package-lock.json
- worker.min.js begins with '/*! For license information please see worker.min.js.LICENSE.txt */', but the app ships only worker.min.js; the referenced file (webpack's extracted banners: buffer, ieee754, regenerator-runtime, zlib.js) is reproduced as texts/tesseract.js-7.0.0--worker.min.js.LICENSE.txt.
- The rest of tesseract.js (createWorker, scheduler) is bundled by Vite into assets/tesseract-runtime-*.js and is in Vite's report (.vite/licenses.json lists tesseract.js 7.0.0 and regenerator-runtime 0.13.11). The worker's own dependencies (zlibjs, wasm-feature-detect, bmp-js, is-url, buffer, base64-js, ieee754, idb-keyval) are not in Vite's report and are covered here.
- No NOTICE file upstream (raw NOTICE at v7.0.0: 404); LICENSE.md carries no copyright line.
- is-url 1.2.4's LICENSE-MIT has no copyright line; attribution by package name/repository only.
- webpack's runtime snippets are not a module in the source map; the version (5.98.0) is taken from the tag's package-lock.json (inferred, not verifiable from the minified output).

### typing_extensions 4.12.2

- **In the app via:** @bentopdf/pymupdf-wasm 0.11.16 assets/ (from Pyodide 0.28.0a3 CDN)
- **Used for:** Dependency of python-docx
- 

### Adobe CMaps (in PDF.js) 2014-03-17

- **In the app via:** BentoPDF public/pdfjs-viewer/cmaps and public/pdfjs-annotation-viewer/web/cmaps (= pdf.js release zips)
- **Used for:** text in PDFs that use predefined CJK CMaps, in the two viewers
- **Build:** pdf.js external/cmapscompress (conversion to .bcmap)
- 168 .bcmap + LICENSE in each viewer; identical in pdf.js 4.3.136 and 5.4.296.
- Exact cmap-resources revision is not recorded by pdf.js (inferred: state of early 2014).

### Alef (in LibreOffice) 1.001

- **In the app via:** LibreOffice 24.8 bundled fonts (with_fonts=yes) inside soffice.data
- **Used for:** Font fallback/substitution when rendering Office documents to PDF; subsets may be embedded in output PDFs
- Name table only says "Copyright (c) 2012 by Hagilda. All rights reserved." with no license string; OFL-1.1 per the LibreOffice notice and upstream tarball. fsType=4 (preview & print embedding).

### Alex Brush (signature font) 1.111

- **In the app via:** BentoPDF (added to pdf.js standard_fonts / the annotation extension's font folder; not part of upstream pdf.js)
- **Used for:** typed signatures in Sign PDF (pdfjs-viewer signature dialog font picker)
- Not in upstream pdf.js 5.4.296: added by BentoPDF for the typed-signature font picker.
- Byte-level differences from the google/fonts repository TTF of the same version (tables such as DSIG/kern dropped or rebuilt, name table edited) match files served by the Google Fonts API; source of BentoPDF's copy not documented (inferred).

### Allura (signature font) 1.110

- **In the app via:** BentoPDF (added to pdf.js standard_fonts / the annotation extension's font folder; not part of upstream pdf.js)
- **Used for:** typed signatures in Sign PDF; handwriting font in Add Stamps (annotation extension)
- Not in upstream pdf.js 5.4.296: added by BentoPDF for the typed-signature font picker.
- Byte-level differences from the google/fonts repository TTF of the same version (tables such as DSIG/kern dropped or rebuilt, name table edited) match files served by the Google Fonts API; source of BentoPDF's copy not documented (inferred).
- The two shipped copies are byte-identical.

### Amiri (in LibreOffice) 1.001

- **In the app via:** LibreOffice 24.8 bundled fonts (with_fonts=yes) inside soffice.data
- **Used for:** Font fallback/substitution when rendering Office documents to PDF; subsets may be embedded in output PDFs
- 

### Caladea (in LibreOffice) 1.002

- **In the app via:** LibreOffice 24.8 bundled fonts (with_fonts=yes) inside soffice.data
- **Used for:** Font fallback/substitution when rendering Office documents to PDF; subsets may be embedded in output PDFs
- Apache-2.0 per the name table license string and the LibreOffice notice.

### Carlito (in LibreOffice) 1.103

- **In the app via:** LibreOffice 24.8 bundled fonts (with_fonts=yes) inside soffice.data
- **Used for:** Font fallback/substitution when rendering Office documents to PDF; subsets may be embedded in output PDFs
- 

### Cedarville Cursive (font, Fontsource) 1.001

- **In the app via:** @fontsource/cedarville-cursive 5.2.7 (BentoPDF dependency, imported by src/css/styles.css)
- **Used for:** declared as a Tailwind theme font in src/css/styles.css (--font-cedarville); no page or script in BentoPDF 2.8.8 uses the class, so it is loaded only if something asks for it
- Fontsource repackaging of the Google Fonts release (metadata.json: source https://github.com/google/fonts, Google Fonts API version v18, lastModified 2025-09-16); upstream font project: https://github.com/google/fonts/tree/main/ofl/cedarvillecursive.
- Imported weights/styles: 400 (src/css/styles.css @import '@fontsource/cedarville-cursive/<weight>.css'); Vite emits every unicode-range subset of those weights as WOFF2 + WOFF; subsets under 4 KB are inlined as data: URIs in assets/style-*.css instead of separate files.
- Fonts are redistributed unmodified as published by Fontsource (already subset and converted to WOFF/WOFF2 upstream); OFL-1.1 is satisfied by shipping the copyright notice + license text (texts) with the fonts; fonts may not be sold by themselves.

### CGATS001Compat ICC profile (in PDF.js) bdd8466

- **In the app via:** BentoPDF public/pdfjs-viewer/iccs (= pdf.js 5.4.296 web/iccs)
- **Used for:** pdf.js CMYK to RGB conversion (with qcms) in the pdfjs-viewer, if it resolves its iccUrl (see pdfjs-viewer notes); the main app does not set iccUrl
- iccs/LICENSE is the CC0 1.0 legal code.

### Culmus Hebrew fonts (in LibreOffice) 0.133

- **In the app via:** LibreOffice 24.8 bundled fonts (with_fonts=yes) inside soffice.data
- **Used for:** Font fallback/substitution when rendering Office documents to PDF; subsets may be embedded in output PDFs
- GPL-2.0 font data (mere aggregation with the rest of the app). The Culmus LICENSE grants the font-embedding exception only for Yoram Gnat's families (Shofar, Keter YG, Hadasim, Simple, Stam); the Maxim Iorsh families shipped here carry no embedding exception, so PDFs that embed their glyphs are in the classic GPL-font grey zone. GPL obligations: ship GPL-2.0 text and provide/offer the corresponding source (the culmus-0.133 tarball, which contains the TTF/OTF/Type1 files). Sample files verified byte-identical to the culmus-0.133 tarball.

### Dancing Script (font, Fontsource) 2.001

- **In the app via:** @fontsource/dancing-script 5.2.8 (BentoPDF dependency, imported by src/css/styles.css)
- **Used for:** declared as a Tailwind theme font in src/css/styles.css (--font-dancing); no page or script in BentoPDF 2.8.8 uses the class, so it is loaded only if something asks for it
- Fontsource repackaging of the Google Fonts release (metadata.json: source https://github.com/google/fonts, Google Fonts API version v29, lastModified 2025-09-08); upstream font project: https://github.com/googlefonts/DancingScript.
- Imported weights/styles: 400 (src/css/styles.css @import '@fontsource/dancing-script/<weight>.css'); Vite emits every unicode-range subset of those weights as WOFF2 + WOFF; subsets under 4 KB are inlined as data: URIs in assets/style-*.css instead of separate files.
- Fonts are redistributed unmodified as published by Fontsource (already subset and converted to WOFF/WOFF2 upstream); OFL-1.1 is satisfied by shipping the copyright notice + license text (texts) with the fonts; fonts may not be sold by themselves.
- Reserved Font Name "Dancing Script": PDF Toolbox must not modify these files and keep calling the result "Dancing Script"; unmodified redistribution (as here) is fine. Whether Google/Fontsource subsetting already counts as a "Modified Version" under OFL is the usual gray area accepted industry-wide for Google Fonts; nothing PDF Toolbox adds.

### DejaVu fonts (in LibreOffice) 2.37

- **In the app via:** LibreOffice 24.8 bundled fonts (with_fonts=yes) inside soffice.data
- **Used for:** Font fallback/substitution when rendering Office documents to PDF; subsets may be embedded in output PDFs
- LibreOffice's notice omits the TeX Gyre DJV Math / AMS Euler section, so the upstream DejaVu 2.37 LICENSE is shipped separately. DejaVuMathTeXGyre has fsType=12 (bitmap-only embedding); irrelevant to redistribution.

### DM Sans (font, Fontsource) 4.004

- **In the app via:** @fontsource/dm-sans 5.2.8 (BentoPDF dependency, imported by src/css/styles.css)
- **Used for:** the app-wide UI font (body text, src/css/styles.css)
- Fontsource repackaging of the Google Fonts release (metadata.json: source https://github.com/google/fonts, Google Fonts API version v17, lastModified 2025-09-11); upstream font project: https://github.com/googlefonts/dm-fonts.
- Imported weights/styles: 400, 500, 600, 700 (src/css/styles.css @import '@fontsource/dm-sans/<weight>.css'); Vite emits every unicode-range subset of those weights as WOFF2 + WOFF; subsets under 4 KB are inlined as data: URIs in assets/style-*.css instead of separate files.
- Fonts are redistributed unmodified as published by Fontsource (already subset and converted to WOFF/WOFF2 upstream); OFL-1.1 is satisfied by shipping the copyright notice + license text (texts) with the fonts; fonts may not be sold by themselves.

### Foxit standard fonts (in PDF.js) pdf.js 5.4.296

- **In the app via:** BentoPDF public/pdfjs-viewer/standard_fonts and public/pdfjs-annotation-viewer/web/standard_fonts (= pdf.js release zips)
- **Used for:** pdf.js substitutes for non-embedded standard 14 fonts (Times, Courier, Symbol, Dingbats) in the two viewers
- 10 .pfb files in each viewer; byte-identical between pdf.js 4.3.136 and 5.4.296 and to the release zips.

### Gentium Basic fonts (in LibreOffice) 1.102

- **In the app via:** LibreOffice 24.8 bundled fonts (with_fonts=yes) inside soffice.data
- **Used for:** Font fallback/substitution when rendering Office documents to PDF; subsets may be embedded in output PDFs
- 

### Great Vibes (font, Fontsource) 1.103

- **In the app via:** @fontsource/great-vibes 5.2.8 (BentoPDF dependency, imported by src/css/styles.css)
- **Used for:** declared as a Tailwind theme font in src/css/styles.css (--font-vibes); no page or script in BentoPDF 2.8.8 uses the class, so it is loaded only if something asks for it
- Fontsource repackaging of the Google Fonts release (metadata.json: source https://github.com/google/fonts, Google Fonts API version v21, lastModified 2025-09-05); upstream font project: https://github.com/googlefonts/great-vibes.
- Imported weights/styles: 400 (src/css/styles.css @import '@fontsource/great-vibes/<weight>.css'); Vite emits every unicode-range subset of those weights as WOFF2 + WOFF; subsets under 4 KB are inlined as data: URIs in assets/style-*.css instead of separate files.
- Fonts are redistributed unmodified as published by Fontsource (already subset and converted to WOFF/WOFF2 upstream); OFL-1.1 is satisfied by shipping the copyright notice + license text (texts) with the fonts; fonts may not be sold by themselves.

### Handlee (signature font) 1.001

- **In the app via:** BentoPDF (added to pdf.js standard_fonts / the annotation extension's font folder; not part of upstream pdf.js)
- **Used for:** typed signatures in Sign PDF (pdfjs-viewer signature dialog font picker)
- Not in upstream pdf.js 5.4.296: added by BentoPDF for the typed-signature font picker.
- Byte-level differences from the google/fonts repository TTF of the same version (tables such as DSIG/kern dropped or rebuilt, name table edited) match files served by the Google Fonts API; source of BentoPDF's copy not documented (inferred).
- google/fonts' OFL.txt copyright line (Joe Prince, Vissol Ltd., a Maven Pro URL) disagrees with the font's own name table (Admix Designs); both are recorded.
- Reserved Font Name "Handlee": if these API-processed files count as Modified Versions, OFL condition 3 technically bars the name; low practical risk (Google distributes them under that name).

### Kalam (font, Fontsource) 2.001

- **In the app via:** @fontsource/kalam 5.2.8 (BentoPDF dependency, imported by src/css/styles.css)
- **Used for:** declared as a Tailwind theme font in src/css/styles.css (--font-kalam); no page or script in BentoPDF 2.8.8 uses the class, so it is loaded only if something asks for it
- Fontsource repackaging of the Google Fonts release (metadata.json: source https://github.com/google/fonts, Google Fonts API version v18, lastModified 2025-09-11); upstream font project: https://github.com/google/fonts/tree/main/ofl/kalam (Indian Type Foundry).
- Imported weights/styles: 300, 400, 700 (src/css/styles.css @import '@fontsource/kalam/<weight>.css'); Vite emits every unicode-range subset of those weights as WOFF2 + WOFF; subsets under 4 KB are inlined as data: URIs in assets/style-*.css instead of separate files.
- Fonts are redistributed unmodified as published by Fontsource (already subset and converted to WOFF/WOFF2 upstream); OFL-1.1 is satisfied by shipping the copyright notice + license text (texts) with the fonts; fonts may not be sold by themselves.

### Kalam (signature font) 2.001

- **In the app via:** BentoPDF (added to pdf.js standard_fonts / the annotation extension's font folder; not part of upstream pdf.js)
- **Used for:** typed signatures in Sign PDF; handwriting font in Add Stamps (annotation extension)
- Not in upstream pdf.js 5.4.296: added by BentoPDF for the typed-signature font picker.
- Byte-level differences from the google/fonts repository TTF of the same version (tables such as DSIG/kern dropped or rebuilt, name table edited) match files served by the Google Fonts API; source of BentoPDF's copy not documented (inferred).
- The two shipped copies are byte-identical. Kalam also ships as @fontsource/kalam WOFF/WOFF2 files (separate component).
- Trademark: "Kalam is a trademark of Indian Type Foundry" (name table).

### Lato (font, Fontsource) 1.104

- **In the app via:** @fontsource/lato 5.2.7 (BentoPDF dependency, imported by src/css/styles.css)
- **Used for:** declared as a Tailwind theme font in src/css/styles.css (--font-lato); no page or script in BentoPDF 2.8.8 uses the class, so it is loaded only if something asks for it
- Fontsource repackaging of the Google Fonts release (metadata.json: source https://github.com/google/fonts, Google Fonts API version v25, lastModified 2025-09-16); upstream font project: https://github.com/google/fonts/tree/main/ofl/lato.
- Imported weights/styles: 400, 700, 400-italic (src/css/styles.css @import '@fontsource/lato/<weight>.css'); Vite emits every unicode-range subset of those weights as WOFF2 + WOFF; subsets under 4 KB are inlined as data: URIs in assets/style-*.css instead of separate files.
- Fonts are redistributed unmodified as published by Fontsource (already subset and converted to WOFF/WOFF2 upstream); OFL-1.1 is satisfied by shipping the copyright notice + license text (texts) with the fonts; fonts may not be sold by themselves.
- Reserved Font Name "Lato": PDF Toolbox must not modify these files and keep calling the result "Lato"; unmodified redistribution (as here) is fine. Whether Google/Fontsource subsetting already counts as a "Modified Version" under OFL is the usual gray area accepted industry-wide for Google Fonts; nothing PDF Toolbox adds.

### Liberation fonts (in LibreOffice) 2.1.5

- **In the app via:** LibreOffice 24.8 bundled fonts (with_fonts=yes) inside soffice.data
- **Used for:** Font fallback/substitution when rendering Office documents to PDF; subsets may be embedded in output PDFs
- 

### Liberation Sans 1.07 (in PDF.js) 1.07.4

- **In the app via:** BentoPDF public/pdfjs-viewer/standard_fonts and public/pdfjs-annotation-viewer/web/standard_fonts (= pdf.js release zips)
- **Used for:** pdf.js fallback font for missing (non-embedded) sans-serif/XFA fonts in the two viewers
- RED FLAG: the LICENSE_LIBERATION shipped next to the fonts (from pdf.js 4.3.136/5.4.296) is the SIL OFL 1.1 of Liberation 2.x, but the files are Liberation Sans 1.07.4 (name table: "Version 1.07.4", "Licensed under the Liberation Fonts license"), i.e. GPLv2 with the font-embedding exception plus Red Hat EULA terms. pdf.js fixed this upstream in commit 4315a4be3168 (2026-08-10, issue #21746), after 5.4.296. PDF Toolbox's notices should carry the 1.07.4 License.txt and GPL-2.0, not the OFL.
- GPL-2.0 obligations: offer the corresponding source (the 1.07.4 source tarball above; the TTF is not the preferred form, the SFD sources are) and the licence text. License.txt adds exception (b): distribution in a "physical product" must allow access to/modification of the font source and reinstalling the modified version on that product; and sec. 2: modified redistributions must drop the LIBERATION trademark from file names.
- SPDX expression approximates the licence: the exception text (a) equals Font-exception-2.0, but exception (b) and the EULA terms (trademark, warranty, North Carolina law) have no SPDX id; Fedora calls it "Liberation".
- The files are not byte-identical to liberation-fonts-ttf-1.07.4.tar.gz: FontForge-regenerated in 2019 (FFTM), 681 vs 682 glyphs, modified date 2014-05-09 - probably a distro rebuild from the 1.07.4 sources; pdf.js describes them as the unmodified 1.07.4 release. Whether this counts as a modified version (trademark clause) is unresolved.

### Liberation Sans Narrow (in LibreOffice) 1.07.5

- **In the app via:** LibreOffice 24.8 bundled fonts (with_fonts=yes) inside soffice.data
- **Used for:** Font fallback/substitution when rendering Office documents to PDF; subsets may be embedded in output PDFs
- Red Hat "Liberation Font Software" EULA: GPL-2.0 plus exception (a) font embedding and exception (b) "any distribution of the object code of the Software in a physical product must provide you the right to access and modify the source code ... and to reinstall that modified version ... on the same physical product"; also Red Hat trademark terms. The SPDX expression approximates this; ship both files. Relevant if the APK is ever preinstalled on hardware. Regular weight verified byte-identical to the 1.07.6 tarball.

### Libre Hebrew fonts (in LibreOffice) 1.0

- **In the app via:** LibreOffice 24.8 bundled fonts (with_fonts=yes) inside soffice.data
- **Used for:** Font fallback/substitution when rendering Office documents to PDF; subsets may be embedded in output PDFs
- Frank Ruhl Hofshi name table has no license string; OFL-1.1 per the LibreOffice notice.

### Linux Libertine G and Biolinum G (in LibreOffice) 5.1.3

- **In the app via:** LibreOffice 24.8 bundled fonts (with_fonts=yes) inside soffice.data
- **Used for:** Font fallback/substitution when rendering Office documents to PDF; subsets may be embedded in output PDFs
- Dual licensed; elect OFL-1.0 (the LibreOffice notice quotes OFL 1.0 text; "or later" wording of the GPL option is not stated).

### Merriweather (font, Fontsource) 2.100

- **In the app via:** @fontsource/merriweather 5.2.11 (BentoPDF dependency, imported by src/css/styles.css)
- **Used for:** declared as a Tailwind theme font in src/css/styles.css (--font-merriweather); no page or script in BentoPDF 2.8.8 uses the class, so it is loaded only if something asks for it
- Fontsource repackaging of the Google Fonts release (metadata.json: source https://github.com/google/fonts, Google Fonts API version v33, lastModified 2025-09-02); upstream font project: https://github.com/EbenSorkin/Merriweather4.
- Imported weights/styles: 400, 700, 400-italic (src/css/styles.css @import '@fontsource/merriweather/<weight>.css'); Vite emits every unicode-range subset of those weights as WOFF2 + WOFF; subsets under 4 KB are inlined as data: URIs in assets/style-*.css instead of separate files.
- Fonts are redistributed unmodified as published by Fontsource (already subset and converted to WOFF/WOFF2 upstream); OFL-1.1 is satisfied by shipping the copyright notice + license text (texts) with the fonts; fonts may not be sold by themselves.
- Reserved Font Name "Merriweather": PDF Toolbox must not modify these files and keep calling the result "Merriweather"; unmodified redistribution (as here) is fine. Whether Google/Fontsource subsetting already counts as a "Modified Version" under OFL is the usual gray area accepted industry-wide for Google Fonts; nothing PDF Toolbox adds.

### Noto fonts (in LibreOffice) 2.015 and others

- **In the app via:** LibreOffice 24.8 bundled fonts (with_fonts=yes) inside soffice.data
- **Used for:** Font fallback/substitution when rendering Office documents to PDF; subsets may be embedded in output PDFs
- 

### Noto Naskh Arabic (PDF Editor) 1.00

- **In the app via:** @embedpdf/fonts-arabic@1.0.0 (npm pack by PDF Toolbox tools/webapp.sh, one file extracted; file named in BentoPDF src/js/config/editor-fonts.ts)
- **Used for:** PDF Editor (EmbedPDF) fallback font, fetched via VITE_EMBEDPDF_FONTS_URL to draw text whose font a PDF does not embed (Arabic)
- License mismatch: package.json and LICENSE say OFL-1.1, but the font's own name table (IDs 13/14) says 'Licensed under the Apache License, Version 2.0'. This is an old (v1.00, 2014) Noto build from Google's Apache-2.0 era; later Noto releases are OFL-1.1. The Apache-2.0 grant embedded in the file is the verifiable one, so it is recorded here; both texts are listed (package LICENSE as shipped by the package). Both are permissive; no practical conflict.
- Exact upstream file/commit (googlefonts/noto-fonts history) not identified.

### Noto Sans (OCR text layer) 2.008

- **In the app via:** BentoPDF air-gap bundle: prepare-airgap.sh downloads the URL from src/js/config/font-mappings.ts, https://rawcdn.githack.com/googlefonts/noto-fonts/ffebf8c1ee449e544955a7e813c54f9b73848eac/hinted/ttf/NotoSans/NotoSans-Regular.ttf
- **Used for:** Font of the invisible OCR text layer that the OCR PDF tool and the Workflow OCR node embed (subset by default) into searchable output PDFs (Noto Sans covers Latin/Greek/Cyrillic; English is the only bundled OCR language)
- Name table: 'Noto is a trademark of Google LLC.'; manufacturer Monotype Imaging Inc., designer Monotype Design Team; license description OFL 1.1. The repository LICENSE declares no Reserved Font Name.
- OFL permits bundling with software and embedding (subset) into documents; the license text must accompany the font (texts listed).
- The OCR font differs from the PDF editor's NotoSans-Regular.ttf in wasm/embedpdf/fonts-latin@1.0.0/fonts/ (629024 bytes, another version; covered by the EmbedPDF fonts entry).

### Noto Sans (PDF Editor) 2.015

- **In the app via:** @embedpdf/fonts-latin@1.0.0 (npm pack by PDF Toolbox tools/webapp.sh, one file extracted; file named in BentoPDF src/js/config/editor-fonts.ts)
- **Used for:** PDF Editor (EmbedPDF) fallback font, fetched via VITE_EMBEDPDF_FONTS_URL to draw text whose font a PDF does not embed (Latin, Greek, Cyrillic, Vietnamese)
- The package's LICENSE (identical in all three @embedpdf/fonts-* packages) has a generic header 'Copyright 2014-2021 Adobe ... Copyright 2014-2021 Google Inc ..., with Reserved Font Name 'Noto Sans'' that does not match this font's own copyright line; the upstream OFL.txt of Noto Sans v2.015 (correct header) is reproduced as well.
- Not byte-identical to any NotoSans-Regular.ttf in the notofonts NotoSans-v2.015 release zip (hinted 621572, unhinted 431364, full 825628 bytes vs 629024 here); probably a Google Fonts static instance. Version and copyright from the font's name table.
- OFL-1.1: may be redistributed with software; may not be sold by itself; 'Noto' is a trademark of Google LLC (no Reserved Font Name in the upstream OFL.txt header).

### Noto Sans Hebrew (PDF Editor) 1.02

- **In the app via:** @embedpdf/fonts-hebrew@1.0.0 (npm pack by PDF Toolbox tools/webapp.sh, one file extracted; file named in BentoPDF src/js/config/editor-fonts.ts)
- **Used for:** PDF Editor (EmbedPDF) fallback font, fetched via VITE_EMBEDPDF_FONTS_URL to draw text whose font a PDF does not embed (Hebrew)
- License mismatch: package.json and LICENSE say OFL-1.1, but the font's own name table (IDs 13/14) says 'Licensed under the Apache License, Version 2.0' (old v1.02 Noto build, Apache-2.0 era). Recorded as Apache-2.0; both texts listed. Both permissive.
- Exact upstream file/commit not identified.

### OpenSymbol (in LibreOffice) 102.12

- **In the app via:** LibreOffice 24.8 bundled fonts (with_fonts=yes) inside soffice.data
- **Used for:** Font fallback/substitution when rendering Office documents to PDF; subsets may be embedded in output PDFs
- License inferred: the SFD in LibreOffice core carries copyright lines but no license statement, so it falls under the LibreOffice project license (MPL-2.0). Some glyphs are credited to Google (2010), likely from Croscore/Liberation 2 (OFL/Apache) - unverified.

### PDF.js translations pdf.js 5.4.296

- **In the app via:** BentoPDF public/pdfjs-viewer/locale and public/pdfjs-annotation-viewer/web/locale
- **Used for:** UI strings of the two embedded viewers
- 112 + 111 viewer.ftl files, all with MPL-2.0 headers; locale.json is pdf.js's generated index (Apache-2.0).
- zh-TW/viewer.ftl differs from upstream in both viewers (BentoPDF edits/reformatting). MPL-2.0 is file-level copyleft: the modified files are themselves source and ship in the APK, which satisfies it; keep the headers.

### Reem Kufi (in LibreOffice) 1.7

- **In the app via:** LibreOffice 24.8 bundled fonts (with_fonts=yes) inside soffice.data
- **Used for:** Font fallback/substitution when rendering Office documents to PDF; subsets may be embedded in output PDFs
- 

### Sacramento (signature font) 1.000

- **In the app via:** BentoPDF (added to pdf.js standard_fonts / the annotation extension's font folder; not part of upstream pdf.js)
- **Used for:** typed signatures in Sign PDF (pdfjs-viewer signature dialog font picker)
- Not in upstream pdf.js 5.4.296: added by BentoPDF for the typed-signature font picker.
- Byte-level differences from the google/fonts repository TTF of the same version (tables such as DSIG/kern dropped or rebuilt, name table edited) match files served by the Google Fonts API; source of BentoPDF's copy not documented (inferred).
- Trademark: "Sacramento is a trademark of Astigmatic" (name table).
- Reserved Font Name "Sacramento": if these API-processed files count as Modified Versions, OFL condition 3 technically bars the name; low practical risk (Google distributes them under that name).

### Scheherazade (in LibreOffice) 2.100

- **In the app via:** LibreOffice 24.8 bundled fonts (with_fonts=yes) inside soffice.data
- **Used for:** Font fallback/substitution when rendering Office documents to PDF; subsets may be embedded in output PDFs
- 

### sRGB ICC profile (ICC) v2 (2009)

- **In the app via:** BentoPDF public/ (copied verbatim to the web root by Vite)
- **Used for:** PDF to PDF/A (Ghostscript): src/js/utils/ghostscript-loader.ts fetches it and embeds it unchanged as the OutputIntent ICC stream of every PDF/A file the app writes
- A data file, not code. Terms (ICC, 2013 page for this exact file): use/copy/distribute for any purpose without fee, provided the file is not changed (including its copyright tag) and ICC's name is not used in advertising. The file ships unmodified; ICC's current general profile terms (registry.color.org) are even broader.
- No SPDX identifier exists for these terms, hence LicenseRef-.
- The profile is also copied into user output (PDF/A OutputIntent), unchanged, which the terms allow.

### Tesseract English model (tessdata_best) 4.0.0_best_int

- **In the app via:** BentoPDF air-gap bundle: prepare-airgap.sh downloads https://cdn.jsdelivr.net/npm/@tesseract.js-data/eng/4.0.0_best_int/eng.traineddata.gz (TESSDATA_VERSION=4.0.0_best_int; the npm package version is not pinned, jsDelivr resolved it to the latest, 1.0.0)
- **Used for:** English recognition model for all OCR features (OCR PDF, Workflow OCR node, Compare PDFs); the only bundled OCR language
- **Build:** https://github.com/naptha/tessdata/blob/b86746569320a6103cea84cc2b8d9ee74f0f45d3/gzip-integerize-traineddata.sh (combine_tessdata -c, then gzip)
- The npm package @tesseract.js-data/eng declares "license": "MIT" in package.json and ships no LICENSE file; the model data comes from tesseract-ocr/tessdata_best, whose README says all data are licensed under Apache-2.0. Declared here as Apache-2.0 (the upstream data license); the MIT label can at most cover naptha's packaging.
- tessdata_best has no NOTICE file and no copyright line; its LICENSE is the plain Apache-2.0 text.
- prepare-airgap.sh's jsDelivr URL has no package version, so a future @tesseract.js-data/eng release would silently change this file on a rebuild; pin @tesseract.js-data/eng@1.0.0 for reproducibility (sha256 45b4cb346724ac1774f1c36f42f182b887bcdb28ebe63e6fff90ac41f3fcff91).
- The integerized LSTM component was produced by naptha with combine_tessdata -c; that conversion was not re-run here (the other components were compared, see evidence).

### Lucide icons 0.575.0

- **In the app via:** lucide (BentoPDF dependency: import { createIcons, icons } from 'lucide' in ~120 modules)
- **Used for:** nearly all UI icons (tool cards, buttons) on every page
- Icons are SVG path data compiled into JS; no separate asset files. Because pages import the whole `icons` object, the entire icon set ships.
- package.json says ISC; the LICENSE also carries Feather's MIT notice for derived icons, so the expression here is "ISC AND MIT". Vite's report lists it as ISC with the same LICENSE text.

### Phosphor Icons 2.1.2

- **In the app via:** @phosphor-icons/web (BentoPDF dependency: import '@phosphor-icons/web/regular')
- **Used for:** UI icons in the app shell (src/js/main.ts), the Workflow Builder and Edit PDF Text; the sidebar's icons
- The four font files are byte-identical to src/regular/Phosphor.{woff2,woff,ttf,svg} in the package (CRC32 compared). Font name table: copyright "Phosphor Icons", designers "Tobias Fried & Helena Zhang", license "MIT".
- Also in Vite's report as MIT, but that report covers only the JS/CSS import, not the emitted font files.

### SheetJS Community Edition 0.20.3

- **In the app via:** xlsx (BentoPDF dependency from the SheetJS CDN, not the npm registry)
- **Used for:** PDF to Excel (src/js/logic/pdf-to-excel-page.ts) and the Workflow Builder's PDF-to-XLSX node
- Bundled by Vite from xlsx.mjs into its own chunk (version string 0.20.3 present in the chunk); the minifier dropped the "/*! xlsx.js (C) 2013-present SheetJS */" banner, so the notice must come from the app's notices.
- xlsx.mjs embeds SheetJS's own ssf, cfb and crc32 modules (all "(C) 2013/2014-present SheetJS"); the optional codepage tables (cpexcel) are not imported.
- Also listed in Vite's report (.vite/licenses.json) as Apache-2.0; there is no NOTICE file. README adds: "All rights not explicitly granted by the Apache 2.0 License are reserved by the Original Author."
- git.sheetjs.com web pages need a login; the tag/commit was read through its public API (/api/v1/repos/sheetjs/sheetjs/tags).

### Tailwind CSS (in the site's stylesheets) 4.2.2

- **In the app via:** assets/*.css
- **Used for:** BentoPDF's styles are generated with it and include its base styles

### Vite (runtime helpers in the site's scripts) 8.1.2

- **In the app via:** assets/*.js
- **Used for:** Builds BentoPDF's scripts and adds its small module-loading helpers to them

### AndroidX Core (PackageInfoCompat and Pair only) 1.1.0

- **In the app via:** classes.dex
- **Used for:** Two classes AndroidX WebKit needs

### AndroidX WebKit 1.18.0-alpha02

- **In the app via:** classes.dex
- **Used for:** The WebView features the app uses: the page script channel, profiles and the cross-origin isolation that lets LibreOffice run threads


## Trademarks

PDF Toolbox is an independent project, not made, endorsed or supported by the BentoPDF
authors, Google or the makers of the components above. BentoPDF is the name of the
BentoPDF authors' project. Googlebook and Android are trademarks of Google LLC.
LibreOffice is a registered trademark of The Document Foundation. Ghostscript and
MuPDF are trademarks of Artifex Software, Inc. Other names are trademarks of their
owners, used only to say what PDF Toolbox contains.
