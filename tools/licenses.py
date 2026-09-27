#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""BentoBook's license notices: every part of the app, its license, its
copyright holders and where its source is.

    python3 tools/licenses.py [--web DIR] [--app DIR]

Reads
  licenses/components.json   everything that isn't an npm package in BentoPDF's
                             bundles: BentoPDF itself, the engines, their data
                             and fonts, the Android libraries
  licenses/texts/            the license texts components.json names
  licenses/npm/              texts for npm packages that ship none
  WEB/.vite/licenses.json    Vite's report on the npm packages in BentoPDF's
                             bundles (tools/webapp.sh turns it on); packages
                             only BentoPDF's workers use are added here
Writes
  THIRD_PARTY_NOTICES.md and licenses/javascript-packages.txt, in the repo
  with --app DIR: the app's /bentobook/ pages (about.html, licenses.html and
  the texts), which the APK serves at https://appassets.androidplatform.net/bentobook/

It fails when an engine, data or font file in the web build belongs to no
component, so a new engine in a BentoPDF update can't ship unlisted, and when
a package has no license text.
"""
import argparse
import datetime
import fnmatch
import html
import json
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LICENSES = os.path.join(ROOT, "licenses")
# Files that are an engine, its data or a font: each must belong to a component.
BINARY = re.compile(r"\.(wasm|data|gz|whl|zip|tar|traineddata|ttf|otf|woff2?|pfb|bcmap|icc|so)$", re.I)
LICENSE_FILE = re.compile(r"^(un)?licen[cs]e|^copying|^notice", re.I)
GROUPS = [
    ("app", "BentoPDF and BentoBook"),
    ("engine", "Engines"),
    ("data", "Data and fonts"),
    ("web", "Web components"),
    ("android", "Android libraries"),
]


def read(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def project():
    """Versions and URLs the notices mention, from the files that set them."""
    manifest = read(os.path.join(ROOT, "AndroidManifest.xml"))
    webapp = read(os.path.join(ROOT, "tools", "webapp.sh"))
    info = json.loads(read(os.path.join(LICENSES, "components.json")))["app"]
    info["version"] = re.search(r'android:versionName="([^"]+)"', manifest)[1]
    info["bentopdf_version"] = re.search(r"^VERSION=(\S+)", webapp, re.M)[1]
    info["bentopdf_commit"] = re.search(r"^COMMIT=([0-9a-f]+)", webapp, re.M)[1]
    return info


def components(info):
    data = json.loads(read(os.path.join(LICENSES, "components.json")))
    out = []
    for c in data["components"]:
        c = json.loads(json.dumps(c).replace("{bentopdf_version}", info["bentopdf_version"])
                       .replace("{bentopdf_commit}", info["bentopdf_commit"])
                       .replace("{version}", info["version"]))
        for t in c.get("texts", []):
            if not os.path.isfile(os.path.join(LICENSES, "texts", t)):
                sys.exit(f"licenses/components.json: {c['id']} names licenses/texts/{t}, which is missing")
        out.append(c)
    return out, data.get("npm_licenses", {}), data.get("attributions", [])


# ---- npm packages ----

def package_dir(src, name, start=None):
    """Node's lookup: node_modules next to the importer, then upwards."""
    d = start or src
    while True:
        p = os.path.join(d, "node_modules", name)
        if os.path.isfile(os.path.join(p, "package.json")):
            return p
        if os.path.samefile(d, src) or os.path.dirname(d) == d:
            return None
        d = os.path.dirname(d)


def worker_packages(src):
    """npm packages in the site's Vite-built workers, which Vite's report
    leaves out: the bare imports reachable from each worker entry."""
    js = os.path.join(src, "src")
    entries = []
    for dirpath, _, files in os.walk(js):
        for f in files:
            if not f.endswith((".ts", ".js", ".mjs")):
                continue
            path = os.path.join(dirpath, f)
            text = read(path)
            for m in re.finditer(r"new\s+(?:Shared)?Worker\(\s*new\s+URL\(\s*['\"]([^'\"]+)['\"]", text):
                entries.append(os.path.normpath(os.path.join(dirpath, m[1])))
            for m in re.finditer(r"from\s+['\"]([^'\"]+)\?worker", text):
                entries.append(os.path.normpath(os.path.join(dirpath, m[1])))
    seen, bare = set(), set()
    spec = re.compile(r"""(?:import|export)\s[^'";]*?from\s*['"]([^'"]+)['"]|import\s*\(?\s*['"]([^'"]+)['"]""")
    while entries:
        path = entries.pop()
        for candidate in (path, path + ".ts", path + ".js", os.path.join(path, "index.ts")):
            if os.path.isfile(candidate):
                path = candidate
                break
        else:
            continue
        if path in seen:
            continue
        seen.add(path)
        for m in spec.finditer(read(path)):
            s = (m[1] or m[2]).split("?")[0]
            if s.startswith("."):
                entries.append(os.path.normpath(os.path.join(os.path.dirname(path), s)))
            elif not s.startswith(("/", "virtual:", "node:")):
                parts = s.split("/")
                bare.add("/".join(parts[:2]) if s.startswith("@") else parts[0])
    return sorted(bare)


def npm_packages(report_path, src, overrides):
    report = json.loads(read(report_path))
    pkgs = {(e["name"], e["version"]): dict(e, via="bundle") for e in report}
    names = {e["name"] for e in report}
    # Worker-only packages, with the dependencies they bring.
    queue = [(n, None) for n in worker_packages(src) if n not in names]
    while queue:
        name, start = queue.pop()
        d = package_dir(src, name, start)
        if not d:
            continue
        pj = json.loads(read(os.path.join(d, "package.json")))
        key = (name, pj.get("version", "0.0.0"))
        if key in pkgs or name in names:
            continue
        lic = pj.get("license")
        pkgs[key] = {"name": name, "version": key[1], "via": "worker",
                     "identifier": lic if isinstance(lic, str) else None}
        queue += [(dep, d) for dep in pj.get("dependencies", {})]
    out, missing = [], []
    for (name, version), e in sorted(pkgs.items()):
        d = package_dir(src, name)
        text, where = e.get("text"), "package"
        if not text and d:
            for f in sorted(os.listdir(d)):
                if LICENSE_FILE.match(f) and os.path.isfile(os.path.join(d, f)):
                    text = read(os.path.join(d, f)).strip()
                    break
        override = os.path.join(LICENSES, "npm", name.replace("/", "__") + ".txt")
        if not text and os.path.isfile(override):
            text, where = read(override).strip(), "project"
        if not text:
            missing.append(f"{name}@{version}")
            continue
        homepage = None
        if d:
            pj = json.loads(read(os.path.join(d, "package.json")))
            repo = pj.get("repository")
            repo = repo.get("url") if isinstance(repo, dict) else repo
            homepage = pj.get("homepage") or repo
            if homepage:
                homepage = re.sub(r"^git\+|\.git$", "", homepage)
                homepage = re.sub(r"^git://", "https://", homepage)
                homepage = re.sub(r"^github:", "https://github.com/", homepage)
                if re.match(r"^[\w.-]+/[\w.-]+$", homepage):
                    homepage = "https://github.com/" + homepage
        out.append({
            "name": name, "version": version, "via": e["via"],
            "license": overrides.get(name) or e.get("identifier") or "see text",
            "text": text, "text_from": where, "homepage": homepage,
        })
    if missing:
        sys.exit("no license text for: " + ", ".join(missing)
                 + "\nadd licenses/npm/<name with / as __>.txt (see the others there)")
    return out


# ---- coverage ----

def coverage(web, comps):
    unlisted = []
    for dirpath, dirs, files in os.walk(web):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for f in files:
            rel = os.path.relpath(os.path.join(dirpath, f), web)
            if f.endswith(".br") or not BINARY.search(f):
                continue
            if not any(fnmatch.fnmatchcase(rel, g) for c in comps for g in c.get("files", [])):
                unlisted.append(rel)
    if unlisted:
        sys.exit("files in the web build that no component in licenses/components.json claims:\n  "
                 + "\n  ".join(sorted(unlisted)[:40]) + ("\n  ..." if len(unlisted) > 40 else ""))


# ---- output ----

def esc(s):
    return html.escape(str(s), quote=True)


def md(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


def link(url, label=None):
    return f'<a href="{esc(url)}">{esc(label or re.sub(r"^https?://", "", url))}</a>'


def component_html(c):
    meta = [f"{esc(c['license'])}"]
    if c.get("used_for"):
        meta.append(esc(c["used_for"]))
    parts = [f'<div class="component" id="{esc(c["id"])}">',
             f'<h3>{esc(c["name"])} {esc(c.get("version", ""))}</h3>',
             f'<div class="meta">{" · ".join(meta)}</div>']
    for line in c.get("copyright", []):
        parts.append(f'<div class="meta">{esc(line)}</div>')
    links = []
    if c.get("homepage"):
        links.append(link(c["homepage"], "Website"))
    if c.get("source"):
        links.append(link(c["source"], "Source"))
    if c.get("build"):
        links.append(link(c["build"], "Build scripts"))
    for t in c.get("texts", []):
        links.append(f'<a href="licenses/{esc(t)}">{esc(t[:-4] if t.endswith(".txt") else t)}</a>')
    if links:
        parts.append(f'<p class="links">{"".join(links)}</p>')
    if c.get("includes"):
        rows = "".join(
            f"<tr><td>{esc(i['name'])} {esc(i.get('version', ''))}</td><td>{esc(i.get('license', ''))}</td>"
            f"<td>{esc('; '.join(i['copyright']) if isinstance(i.get('copyright'), list) else i.get('copyright', ''))}</td></tr>"
            for i in c["includes"])
        parts.append(f"<details><summary>Includes {len(c['includes'])} libraries</summary>"
                     f"<table><thead><tr><th>Library</th><th>License</th><th>Copyright</th></tr></thead>"
                     f"<tbody>{rows}</tbody></table></details>")
    if c.get("notes_public"):
        parts.append(f'<p class="muted">{esc(c["notes_public"])}</p>')
    parts.append("</div>")
    return "\n".join(parts)


def package_html(p):
    links = link(p["homepage"], "Source") if p.get("homepage") else ""
    return (f'<div class="component"><h3>{esc(p["name"])} {esc(p["version"])}</h3>'
            f'<div class="meta">{esc(p["license"])}{" · " + links if links else ""}</div>'
            f'<details><summary>License text</summary><pre>{esc(p["text"])}</pre></details></div>')


def app_pages(out, info, comps, pkgs, attributions):
    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(os.path.join(out, "licenses"))
    shutil.copy(os.path.join(ROOT, "shell", "bentobook.css"), out)
    shutil.copy(os.path.join(ROOT, "docs", "icon.svg"), out)
    for t in sorted({t for c in comps for t in c.get("texts", [])} | {"AGPL-3.0.txt", "MIT-BentoBook.txt"}):
        shutil.copy(os.path.join(LICENSES, "texts", t), os.path.join(out, "licenses", t))
    tag = f"v{info['version']}"
    source = f"{info['repo']}/tree/{tag}"
    rows = "\n".join(
        f"        <tr><td>{esc(c.get('about_name', c['name']))}</td><td>{esc(c.get('about', c.get('used_for', '')))}</td>"
        f"<td>{esc(c['license'])}</td></tr>"
        for c in comps if c.get("summary"))
    credits = "\n".join(f"      <li>{esc(a)}</li>" for a in attributions)
    values = {
        "version": info["version"], "year": str(datetime.date.today().year),
        "bentopdf_version": info["bentopdf_version"],
        "bentopdf_commit_short": info["bentopdf_commit"][:7],
        "bentopdf_url": f"https://github.com/alam00000/bentopdf/tree/{info['bentopdf_commit']}",
        "source_url": source, "source_label": re.sub(r"^https://", "", source),
        "releases_url": info["repo"] + "/releases", "releases_label": re.sub(r"^https://", "", info["repo"]) + "/releases",
        "component_count": str(len(comps) + len(pkgs)),
    }
    about = read(os.path.join(ROOT, "shell", "about.html"))
    raw = {"engine_rows": rows, "attributions": credits}
    about = re.sub(r"\{\{(\w+)\}\}", lambda m: raw[m[1]] if m[1] in raw else esc(values[m[1]]), about)
    write(os.path.join(out, "about.html"), about)

    body = []
    for group, title in GROUPS:
        members = [c for c in comps if c.get("group") == group]
        if members:
            body.append(f"<section><h2>{esc(title)}</h2>" + "\n".join(component_html(c) for c in members) + "</section>")
    body.append(f"<section><h2>JavaScript packages ({len(pkgs)})</h2>"
                "<p class=\"muted\">The npm packages in BentoPDF's scripts, as bundled by its build.</p>"
                + "\n".join(package_html(p) for p in pkgs) + "</section>")
    page = f"""<!doctype html>
<!-- Written by tools/licenses.py -->
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>BentoBook licenses</title>
<link rel="stylesheet" href="bentobook.css">
</head>
<body>
<nav class="top"><a href="about.html">← About</a><a href="/">Tools</a>
<input type="search" id="filter" placeholder="Filter by name or license" aria-label="Filter"></nav>
<main>
<header class="intro"><div><h1>Licenses</h1>
<p>BentoBook {esc(info['version'])} contains {len(comps) + len(pkgs)} components. Each is listed with its license,
its copyright holders and where its source code is.</p></div></header>
{chr(10).join(body)}
</main>
<script>
const filter = document.getElementById('filter');
filter.addEventListener('input', () => {{
  const q = filter.value.trim().toLowerCase();
  for (const c of document.querySelectorAll('.component')) {{
    const head = c.querySelector('h3').textContent + ' ' + c.querySelector('.meta').textContent;
    c.hidden = !!q && !head.toLowerCase().includes(q);
  }}
}});
</script>
</body>
</html>
"""
    write(os.path.join(out, "licenses.html"), page)


def repo_notices(info, comps, pkgs, attributions):
    lines = [
        "# Third-party notices",
        "",
        "<!-- Written by tools/licenses.py from licenses/components.json and BentoPDF's",
        "     build; run it again after changing either. -->",
        "",
        f"BentoBook {info['version']} is BentoPDF {info['bentopdf_version']} in an Android app. BentoBook's own code (this",
        "repository) is under the MIT License ([LICENSE](LICENSE)). The app it builds contains BentoPDF",
        "and several engines under the GNU Affero General Public License v3, so the app as a whole is",
        "distributed under the AGPL v3 ([licenses/texts/AGPL-3.0.txt](licenses/texts/AGPL-3.0.txt)).",
        "Every part keeps its own license, listed below with its copyright holders and its source.",
        "The app shows the same list, with every license text, under **About & licenses**.",
        "",
        "## BentoPDF, modified",
        "",
        f"BentoBook contains a modified version of BentoPDF {info['bentopdf_version']} (commit",
        f"[`{info['bentopdf_commit'][:7]}`](https://github.com/alam00000/bentopdf/tree/{info['bentopdf_commit']})), AGPL-3.0,",
        "copyright © the BentoPDF authors. The changes, all in this repository:",
        "",
        "- it is built in Simple Mode, with every engine, its data and the editor's fonts",
        "  served from the app instead of CDNs (tools/webapp.sh);",
        "- BentoBook's page script (shell/page_shim.js) runs in every page: opening and saving",
        "  files through Android, printing, a compact tool layout and the About link;",
        "- a prelude (shell/nested-workers.js) is prepended to the LibreOffice converter's worker,",
        "  so its thread workers can start in Android's WebView.",
        "",
        "PDFs made with BentoBook keep BentoPDF's producer line, as BentoPDF asks.",
        "",
        "## Source code",
        "",
        "Whoever has the app is entitled to its complete source: this repository at the release's",
        "tag (it builds the APK), BentoPDF at the commit above, and the sources listed for each",
        "component below. Each GitHub release carries a source archive of the first two and the",
        "engines' build scripts, and a second archive with the sources that",
        "[licenses/mirror.txt](licenses/mirror.txt) lists: the GPL-2.0 fonts and the LGPL",
        "libraries compiled into the engines, whose licenses ask for them next to the app",
        "(`./bb release`).",
        "",
    ]
    for group, title in GROUPS:
        members = [c for c in comps if c.get("group") == group]
        if not members:
            continue
        lines += [f"## {title}", "", "| Component | Version | License | Copyright | Source |", "| --- | --- | --- | --- | --- |"]
        for c in members:
            src = c.get("source") or c.get("homepage") or ""
            texts = ", ".join(f"[{t}](licenses/texts/{t})" for t in c.get("texts", []))
            lines.append(f"| {md(c['name'])} | {md(c.get('version', ''))} | {md(c['license'])}"
                         f"{' (' + texts + ')' if texts else ''} | {md('; '.join(c.get('copyright', [])))} | {src} |")
            for i in c.get("includes", []):
                cr = i.get("copyright", "")
                cr = "; ".join(cr) if isinstance(cr, list) else cr
                lines.append(f"| ↳ {md(i['name'])} | {md(i.get('version', ''))} | {md(i.get('license', ''))} | {md(cr)} | {i.get('source', '')} |")
        lines.append("")
    lines += [f"## JavaScript packages ({len(pkgs)})", "",
              "The npm packages in BentoPDF's scripts, from its build's own report. Their license",
              "texts are in [licenses/javascript-packages.txt](licenses/javascript-packages.txt).", "",
              "| Package | Version | License |", "| --- | --- | --- |"]
    for p in pkgs:
        name = f"[{md(p['name'])}]({p['homepage']})" if p.get("homepage") else md(p["name"])
        lines.append(f"| {name} | {md(p['version'])} | {md(p['license'])} |")
    lines += ["", "## Notices some licenses require", ""] + [f"- {a}" for a in attributions]
    lines += ["", "## Details", "",
              "How each component gets into the app, where its build scripts are, and notes from the license",
              "audit: obligations, and what couldn't be verified.", ""]
    for c in comps:
        bits = [f"### {c['name']} {c.get('version', '')}".rstrip(), ""]
        if c.get("via"):
            bits.append(f"- **In the app via:** {md(c['via'])}")
        if c.get("used_for"):
            bits.append(f"- **Used for:** {md(c['used_for'])}")
        if c.get("build"):
            bits.append(f"- **Build:** {md(c['build'])}")
        for n in c.get("notes", []):
            bits.append(f"- {md(n)}")
        if len(bits) > 2:
            lines += bits + [""]
    lines += ["", "## Trademarks", "",
              "BentoBook is an independent project, not made, endorsed or supported by the BentoPDF",
              "authors, Google or the makers of the components above. BentoPDF is the name of the",
              "BentoPDF authors' project. Googlebook and Android are trademarks of Google LLC.",
              "LibreOffice is a registered trademark of The Document Foundation. Ghostscript and",
              "MuPDF are trademarks of Artifex Software, Inc. Other names are trademarks of their",
              "owners, used only to say what BentoBook contains.", ""]
    write(os.path.join(ROOT, "THIRD_PARTY_NOTICES.md"), "\n".join(lines))
    texts = [f"License texts of the {len(pkgs)} npm packages in BentoBook {info['version']}'s scripts",
             "(written by tools/licenses.py)", ""]
    for p in pkgs:
        where = "" if p["text_from"] == "package" else " (text from licenses/npm/: the package ships none)"
        texts += ["=" * 78, f"{p['name']} {p['version']} ({p['license']}){where}", "=" * 78, "", p["text"], ""]
    write(os.path.join(LICENSES, "javascript-packages.txt"), "\n".join(texts))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    version = re.search(r"^VERSION=(\S+)", read(os.path.join(ROOT, "tools", "webapp.sh")), re.M)[1]
    cache = os.environ.get("BENTOBOOK_CACHE", os.path.expanduser("~/.cache/bentobook"))
    ap.add_argument("--web", default=os.path.join(cache, f"web-{version}"),
                    help="the web root the app serves (default: BentoPDF's cached build)")
    ap.add_argument("--report", help="Vite's license report (default: WEB/.vite/licenses.json)")
    ap.add_argument("--src", default=os.path.join(cache, f"bentopdf-{version}"), help="BentoPDF's checkout")
    ap.add_argument("--app", help="write the app's /bentobook/ pages here")
    args = ap.parse_args()
    info = project()
    comps, overrides, attributions = components(info)
    coverage(args.web, comps)
    pkgs = npm_packages(args.report or os.path.join(args.web, ".vite", "licenses.json"), args.src, overrides)
    repo_notices(info, comps, pkgs, attributions)
    if args.app:
        app_pages(args.app, info, comps, pkgs, attributions)
    print(f"{len(comps)} components, {len(pkgs)} npm packages"
          f" ({sum(p['via'] == 'worker' for p in pkgs)} only in workers)")


if __name__ == "__main__":
    main()
