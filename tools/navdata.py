#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Writes the sidebar's tool list (toolbox/tools.js) from BentoPDF's own
(src/js/config/tools.ts): its categories, and each tool's page, name, icon
and one-line description.

    python3 tools/navdata.py --src BENTOPDF_CHECKOUT --web WEB_ROOT --out FILE

Tools whose page isn't in the web root are left out, and it fails if the
list comes out empty or a category has no tools: a BentoPDF update that
changes the file's layout shouldn't ship an empty menu.
"""
import argparse
import json
import os
import re
import sys

# Icons for the categories on the collapsed sidebar (Phosphor, like BentoPDF's).
CATEGORY_ICONS = {
    "Popular Tools": "ph-star",
    "Edit & Annotate": "ph-pencil-simple-line",
    "Convert to PDF": "ph-arrow-square-in",
    "Convert from PDF": "ph-arrow-square-out",
    "Organize & Manage": "ph-files",
    "Optimize & Repair": "ph-wrench",
    "Secure PDF": "ph-shield-check",
}
STRING = r"'((?:[^'\\]|\\.)*)'"


def unquote(s):
    return re.sub(r"\\(.)", r"\1", s)


def parse(text):
    categories = []
    heads = list(re.finditer(r"\{\s*name:\s*" + STRING + r",\s*tools:\s*\[", text))
    for i, head in enumerate(heads):
        body = text[head.end():heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        tools = []
        for m in re.finditer(r"\{\s*href:\s*import\.meta\.env\.BASE_URL\s*\+\s*" + STRING + r",\s*name:\s*" + STRING
                             + r",\s*icon:\s*" + STRING + r",\s*subtitle:\s*" + STRING, body):
            href, name, icon, subtitle = (unquote(g) for g in m.groups())
            tools.append({"id": re.sub(r"\.html$", "", href), "name": name, "icon": icon, "subtitle": subtitle})
        categories.append({"name": unquote(head.group(1)), "tools": tools})
    return categories


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--src", required=True)
    ap.add_argument("--web", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    text = open(os.path.join(args.src, "src", "js", "config", "tools.ts"), encoding="utf-8").read()
    categories = parse(text)
    missing = []
    for c in categories:
        kept = []
        for t in c["tools"]:
            if os.path.isfile(os.path.join(args.web, t["id"] + ".html")):
                kept.append(t)
            else:
                missing.append(t["id"])
        c["tools"] = kept
        c["icon"] = CATEGORY_ICONS.get(c["name"], "ph-folder")
    if not categories or any(not c["tools"] for c in categories):
        sys.exit(f"navdata: couldn't read the tool list from tools.ts ({[c['name'] for c in categories]})")
    if missing:
        print(f"navdata: left out tools without a page: {', '.join(missing)}", file=sys.stderr)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write("// Written by tools/navdata.py from BentoPDF's src/js/config/tools.ts.\n")
        f.write("window.TOOLBOX_CATEGORIES = " + json.dumps(categories, ensure_ascii=False, indent=1) + ";\n")
    unique = {t["id"] for c in categories for t in c["tools"]}
    print(f"{len(categories)} categories, {len(unique)} tools")


if __name__ == "__main__":
    main()
