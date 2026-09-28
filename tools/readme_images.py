#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""The README's screenshots (docs/images/*.png), in two steps.

  python3 tools/readme_images.py capture   drive the app on the Googlebook and save
                                           raw window captures in ~/.cache/pdf-toolbox/shots
  python3 tools/readme_images.py           compose docs/images/*.png from them

Capture needs PDF Toolbox open and visible, with DevTools on (`./ptb debug
devtools on`), and the demo PDF from `python3 tools/testfiles.py`. It sets up
each screen over the DevTools protocol (the tool, its file, the sidebar's
Recent list and search), so no personal files or names show, and captures the
app's window with `./ptb shot`. Composing rounds the window's corners and adds
a soft shadow (Pillow).
"""
import base64
import json
import pathlib
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = pathlib.Path.home() / ".cache/pdf-toolbox/shots"
OUT = ROOT / "docs/images"
DEMO = "PDF Toolbox Demo.pdf"

# name: (tool path, Recent list, collapsed, file input selector, what to do after loading)
SHOTS = {
    "hero": ("/pdf-multi-tool", ["compress-pdf", "sign-pdf", "edit-pdf-text", "merge-pdf"], False,
             "#pdf-file-input", None),
    "edit-text": ("/edit-pdf-text", ["pdf-multi-tool", "compress-pdf", "sign-pdf", "merge-pdf"], False,
                  "#drop-zone input[type=file]", None),
    "search": ("/sign-pdf", ["edit-pdf-text", "pdf-multi-tool", "compress-pdf", "merge-pdf"], False,
               "#drop-zone input[type=file]", "search"),
    "rail": ("/", ["sign-pdf", "edit-pdf-text", "pdf-multi-tool", "compress-pdf", "merge-pdf"], True,
             None, "flyout"),
}


def capture(names):
    sys.path.insert(0, str(ROOT / "tools"))
    import smoke  # the smoke test's page driver: the sidebar page and the tool in its frame
    RAW.mkdir(parents=True, exist_ok=True)
    page = smoke.Page()
    demo = base64.b64encode((ROOT / "test" / DEMO).read_bytes()).decode()
    for name in names:
        path, recent, collapsed, selector, after = SHOTS[name]
        # Start the sidebar page afresh with this Recent list and layout.
        page.top("localStorage.setItem('toolbox.recent', %s); localStorage.setItem('toolbox.collapsed', %s);"
                 "localStorage.removeItem('toolbox.closed'); location.replace('/toolbox/#' + %s);"
                 "location.reload(); true" % (json.dumps(json.dumps(recent)), json.dumps(json.dumps(collapsed)),
                                              json.dumps(path)))
        time.sleep(2)
        page.wait_top("!!window.__pdftoolbox && document.getElementById('view').contentDocument"
                      " && document.getElementById('view').contentDocument.readyState === 'complete'"
                      " && document.getElementById('view').contentWindow.location.pathname.replace(/\\.html$/, '') === %s"
                      % json.dumps(path), f"{path} did not open")
        time.sleep(2)
        if selector:
            page.eval("""(() => {
              const input = document.querySelector(%s);
              const dt = new DataTransfer();
              dt.items.add(new File([Uint8Array.from(atob(%s), (c) => c.charCodeAt(0))], %s, { type: 'application/pdf' }));
              input.files = dt.files;
              input.dispatchEvent(new Event('change', { bubbles: true }));
              return true;
            })()""" % (json.dumps(selector), json.dumps(demo), json.dumps(DEMO)))
            time.sleep(8)
        if after == "search":
            # Show the permit page in Sign's viewer, and "sign" typed in the sidebar's search.
            page.eval("(() => { const f = document.querySelector('iframe');"
                      " if (f && f.contentWindow.PDFViewerApplication) f.contentWindow.PDFViewerApplication.page = 7;"
                      " return true; })()")
            time.sleep(1.5)
            page.top("(() => { const q = document.getElementById('q'); q.focus(); q.value = 'sign';"
                     " q.dispatchEvent(new Event('input')); return true; })()")
        elif after == "flyout":
            page.top("document.querySelector('.group[data-name=\"Secure PDF\"] .head').click(); true")
        # The list starts at the top (a tool's category scrolls into view on load).
        if after != "search":
            page.top("document.getElementById('list').scrollTop = 0; true")
        time.sleep(1.5)
        out = RAW / f"{name}.png"
        subprocess.run([str(ROOT / "ptb"), "shot", str(out)], check=True, stdout=subprocess.DEVNULL)
        print(out)
    page.top("(() => { const q = document.getElementById('q'); q.value = ''; q.dispatchEvent(new Event('input'));"
             " q.blur(); return true; })()")


def compose(names):
    from PIL import Image, ImageChops, ImageDraw, ImageFilter

    def rounded(im, r):
        im = im.convert("RGBA")
        mask = Image.new("L", im.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, im.width - 1, im.height - 1), r, fill=255)
        im.putalpha(ImageChops.multiply(im.getchannel("A"), mask))
        return im

    def shadowed(im, blur=18, offset=(0, 10), alpha=110, pad=44):
        canvas = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
        shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        a = im.getchannel("A").point(lambda v: v * alpha // 255)
        shadow.paste(Image.new("RGBA", im.size, (10, 12, 30, 255)), (pad + offset[0], pad + offset[1]), a)
        canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(blur)))
        canvas.alpha_composite(im, (pad, pad))
        return canvas

    OUT.mkdir(parents=True, exist_ok=True)
    for name in names:
        im = Image.open(RAW / f"{name}.png")
        # The window's own corners are rounded, so the capture's corners show
        # what is behind it; a slightly larger radius hides them.
        out = shadowed(rounded(im, 22))
        out.save(OUT / f"{name}.png", optimize=True)
        print(OUT / f"{name}.png", out.size)


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "capture":
        capture(args[1:] or list(SHOTS))
    else:
        compose(args or list(SHOTS))
