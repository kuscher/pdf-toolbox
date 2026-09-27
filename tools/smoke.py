#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Runs BentoBook's engines end to end on a device or an emulator: opens a
tool, gives it test files, presses its button and waits for the result in
Download/. The same run on an Arm Googlebook and on an x86_64 emulator shows
the one APK working on both.

  ./bb smoke [CHECK...]                             on the Googlebook, over adb
  ADB_SERIAL=emulator-5554 python3 tools/smoke.py   anywhere else (CI)

Checks: merge (pdf-lib and CoherentPDF), compress, pdf-to-docx (PyMuPDF,
pdf2docx, Ghostscript), pdfa (Ghostscript), ocr (Tesseract) and word (Word to
PDF: LibreOffice with threads, which needs cross-origin isolation and so a
recent Android System WebView, as 153 is; on an older one it is skipped).

Needs the app installed and running in a visible window, and the test files
(python3 tools/testfiles.py). It turns WebView debugging on and off again,
and deletes the files it made from Download/.
"""
import argparse
import base64
import json
import os
import re
import socket
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cdp  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST = os.path.join(ROOT, "test")
ORIGIN = "https://appassets.androidplatform.net"
PKG = "local.bentobook"
A, B, DOCX = "BentoBook Test A.pdf", "BentoBook Test B.pdf", "BentoBook Test Letter.docx"
CHECKS = {
    # name: (page, input files, engines, output name suffix, button to press
    # after processing, script to run before pressing the tool's button)
    "merge": ("/merge-pdf", [A, B], "pdf-lib, CoherentPDF", ".pdf", None, None),
    "compress": ("/compress-pdf", [A], "PyMuPDF", ".pdf", None, None),
    "pdf-to-docx": ("/pdf-to-docx", [A], "PyMuPDF, pdf2docx, Ghostscript", ".docx", None, None),
    "pdfa": ("/pdf-to-pdfa", [A], "Ghostscript", ".pdf", None, None),
    # OCR starts once a language is ticked; English is the one the app ships.
    "ocr": ("/ocr-pdf", [A], "Tesseract", ".pdf", "download-searchable-pdf",
            "const c = document.querySelector('.lang-checkbox[value=eng]');"
            " c.checked = true; c.dispatchEvent(new Event('change', { bubbles: true })); true"),
    "word": ("/word-to-pdf", [DOCX], "LibreOffice", ".pdf", None, None),
}
DOWNLOADS = "content://media/external/downloads"


def adb(*args, check=True):
    r = subprocess.run(["adb", *(["-s", cdp.SERIAL] if cdp.SERIAL else []), *args], capture_output=True, text=True)
    if check and r.returncode:
        raise RuntimeError(f"adb {' '.join(args)}: {r.stderr.strip()}")
    return r.stdout.replace("\r", "")


def shell(cmd):
    return adb("shell", cmd)


class Page:
    def __init__(self):
        cdp.connect()
        pages = [t for t in cdp.http_json("/json/list") if t.get("type") == "page"]
        if not pages:
            sys.exit("no WebView page to drive: is BentoBook open?")
        self.ws = cdp.Socket(re.search(r"(/devtools/.*)$", cdp.pick(pages, None)["webSocketDebuggerUrl"])[1])

    def eval(self, js, timeout=60):
        r = self.ws.call("Runtime.evaluate", timeout=timeout, expression=js, awaitPromise=True,
                         returnByValue=True, userGesture=True)
        if "exceptionDetails" in r:
            raise RuntimeError(json.dumps(r["exceptionDetails"].get("exception", r["exceptionDetails"]))[:300])
        return r["result"].get("value")

    def wait(self, js, timeout, what):
        end = time.time() + timeout
        while time.time() < end:
            try:
                value = self.eval(js)
                if value:
                    return value
            except (RuntimeError, socket.timeout, TimeoutError):
                pass  # the page is navigating
            time.sleep(1)
        raise TimeoutError(what)

    def open(self, path):
        self.ws.call("Page.navigate", url=ORIGIN + path)
        time.sleep(1)
        self.wait("document.readyState === 'complete' && !!document.querySelector('#drop-zone input[type=file]')",
                  60, f"{path} did not load")

    def give(self, names):
        files = [{"name": n, "b64": base64.b64encode(open(os.path.join(TEST, n), "rb").read()).decode(),
                  "type": "application/pdf" if n.endswith(".pdf") else
                  "application/vnd.openxmlformats-officedocument.wordprocessingml.document"} for n in names]
        self.eval("""(() => {
          const input = document.querySelector('#drop-zone input[type=file]');
          const dt = new DataTransfer();
          for (const f of %s) {
            const bytes = Uint8Array.from(atob(f.b64), (c) => c.charCodeAt(0));
            dt.items.add(new File([bytes], f.name, { type: f.type }));
          }
          input.files = dt.files;
          input.dispatchEvent(new Event('change', { bubbles: true }));
          return input.files.length;
        })()""" % json.dumps(files))

    def settle(self, count):
        """Waits for the page to list the files it was given: a tool's button
        is live before the page has read them, and pressing it then does
        nothing."""
        try:
            self.wait("(() => { const l = document.getElementById('file-list')"
                      " || document.getElementById('file-display-area');"
                      " return !l || l.children.length >= %d; })()" % count, 30, "")
        except TimeoutError:
            pass
        time.sleep(1.5)

    def press(self, button_id, timeout, what):
        self.wait("(() => { const b = document.getElementById(%r);"
                  " return !!b && !b.disabled && !!b.offsetParent; })()" % button_id, timeout, what)
        self.eval("document.getElementById(%r).click(); true" % button_id)

    def alert(self):
        return self.eval("(() => { const m = document.getElementById('alert-modal');"
                         " return m && !m.classList.contains('hidden') ? m.innerText.trim().replace(/\\s+/g, ' ') : ''; })()")


def user():
    return shell("am get-current-user").strip()


def saved_since(since):
    """Files BentoBook finished saving to Download/ since a device time."""
    out = shell(f"content query --user {user()} --uri {DOWNLOADS} --projection _id:_display_name:_size "
                f"--where \"owner_package_name='{PKG}' AND is_pending=0 AND date_added>={since}\"")
    return [dict(re.findall(r"(\w+)=([^,]*?)(?=, \w+=|$)", line.split(" ", 2)[-1]))
            for line in out.splitlines() if line.startswith("Row:")]


def delete(rows):
    for r in rows:
        shell(f"content delete --user {user()} --uri {DOWNLOADS}/{r['_id']}")


def run(page, name, isolated, timeout):
    path, files, engines, suffix, then, setup = CHECKS[name]
    if name == "word" and not isolated:
        return "skipped", "no cross-origin isolation in this WebView (it needs a newer one)"
    since = int(shell("date +%s").strip()) - 1
    start = time.time()
    page.open(path)
    page.give(files)
    page.settle(len(files))
    if setup:
        page.eval(setup)
    page.press("process-btn", 60, "the tool's button never came up")
    if then:
        page.press(then, timeout, f"#{then} never came up")
    end = start + timeout
    while time.time() < end:
        rows = [r for r in saved_since(since) if r.get("_display_name", "").endswith(suffix)]
        if rows:
            delete(saved_since(since))
            r = rows[0]
            return "ok", f"{r['_display_name']} ({int(r['_size']):,} bytes) in {time.time() - start:.0f} s [{engines}]"
        time.sleep(2)
    alert = page.alert()
    delete(saved_since(since))
    return "FAILED", f"nothing saved in {timeout} s" + (f"; the page says: {alert[:200]}" if alert else "")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("checks", nargs="*", choices=[[]] + list(CHECKS), metavar="CHECK", help=", ".join(CHECKS))
    ap.add_argument("--timeout", type=int, default=240, help="seconds per check (default 240)")
    args = ap.parse_args()
    for n in (A, B, DOCX):
        if not os.path.isfile(os.path.join(TEST, n)):
            subprocess.run([sys.executable, os.path.join(ROOT, "tools", "testfiles.py")], check=True,
                           stdout=subprocess.DEVNULL)
            break
    abis = shell("getprop ro.product.cpu.abilist").strip()
    release = shell("getprop ro.build.version.release").strip()
    webview = re.search(r"Current WebView package \(name, version\): \((\S+), ([^)]+)\)",
                        shell("dumpsys webviewupdate"))
    app = re.search(r"versionName=(\S+)", shell(f"dumpsys package {PKG}"))
    print(f"device: Android {release}, {abis}; WebView {webview[2] if webview else '?'}; "
          f"BentoBook {app[1] if app else 'not installed'}")
    if not app:
        sys.exit(1)
    adb("logcat", "-c")
    shell(f"am start --user current -n {PKG}/.MainActivity")
    time.sleep(3)
    # A fresh page load, so its "page ready" line lands in the cleared log
    # even when the app was open already.
    shell(f"am broadcast -a {PKG}.DEBUG -p {PKG} --es cmd devtools --ez on true")
    shell(f"am broadcast -a {PKG}.DEBUG -p {PKG} --es cmd reload")
    ready = None
    for _ in range(120):
        m = re.findall(r"page ready: crossOriginIsolated=(\w+) SharedArrayBuffer=(\w+)",
                       adb("logcat", "-d", "-s", "BentoBook:I"))
        if m:
            ready = m[-1]
            break
        time.sleep(1.5)
    if not ready:
        sys.exit("the app's page never reported ready (adb logcat -s BentoBook)")
    isolated = ready == ("true", "true")
    print(f"page ready: crossOriginIsolated={ready[0]} SharedArrayBuffer={ready[1]}")
    failed = 0
    try:
        page = Page()
        for name in args.checks or CHECKS:
            try:
                status, detail = run(page, name, isolated, args.timeout)
            except Exception as e:  # a page that never loads, a lost socket
                status, detail = "FAILED", f"{type(e).__name__}: {e}"
            failed += status == "FAILED"
            print(f"{name:12s} {status:8s} {detail}", flush=True)
    finally:
        cdp.unforward()
        shell(f"am broadcast -a {PKG}.DEBUG -p {PKG} --es cmd devtools --ez on false")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
