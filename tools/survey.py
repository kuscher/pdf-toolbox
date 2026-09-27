#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Drop a test PDF into every PDF tool page, opened in the app's frame as the
sidebar opens it, and report the layout and any failed requests.

    ./ptb debug devtools on
    python3 tools/survey.py [/merge-pdf.html ...]

For each page (default: every page of the cached web build whose drop zone
takes PDFs) it prints whether the compact header came up, whether BentoPDF's
top bar and the drop zone are hidden, the document height against the
window's, and whether #process-btn is in view. Below that come the requests
that failed or got a 4xx/5xx, from the page and from every worker: CDP
auto-attaches to workers, since the engines fetch their data from there
(that is how the PDF Editor's jsDelivr fonts showed up). The app has no
INTERNET permission, so anything aimed off the app's origin fails.

Uses test/PDF Toolbox Test A.pdf (python3 tools/testfiles.py).
"""
import base64
import glob
import json
import os
import re
import socket
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cdp  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIGIN = "https://appassets.androidplatform.net"
PDF = os.path.join(ROOT, "test", "PDF Toolbox Test A.pdf")

MEASURE = """(async () => {
  const drop = document.getElementById('drop-zone');
  const input = drop.querySelector('input[type=file]');
  const bytes = Uint8Array.from(atob('%s'), (c) => c.charCodeAt(0));
  const dt = new DataTransfer();
  dt.items.add(new File([bytes], 'PDF Toolbox Test A.pdf', { type: 'application/pdf' }));
  input.files = dt.files;
  input.dispatchEvent(new Event('change', { bubbles: true }));
  await new Promise((r) => setTimeout(r, 6000));
  const bar = document.getElementById('pdftoolbox-toolbar');
  const btn = document.getElementById('process-btn');
  const r = btn && btn.offsetParent ? btn.getBoundingClientRect() : null;
  const nav = document.querySelector('body > nav');
  return JSON.stringify({
    bar: !!bar,
    nav: nav ? getComputedStyle(nav).display !== 'none' : false,
    drop: !!drop.offsetHeight,
    height: document.documentElement.scrollHeight,
    window: innerHeight,
    width: document.documentElement.scrollWidth,
    windowWidth: innerWidth,
    button: r ? (r.bottom <= innerHeight ? 'in view' : 'below, at ' + Math.round(r.top)) : '-',
  });
})()"""


def pdf_pages():
    version = re.search(r"^VERSION=(\S+)", open(os.path.join(ROOT, "tools", "webapp.sh")).read(), re.M)[1]
    web = os.path.expanduser(f"~/.cache/pdf-toolbox/web-{version}")
    pages = []
    for path in sorted(glob.glob(os.path.join(web, "*.html"))):
        html = open(path, encoding="utf-8").read()
        at = html.find('id="drop-zone"')
        if at < 0:
            continue
        tag = re.search(r"<input\b[^>]*>", html[at:])
        accept = re.search(r'accept="([^"]*)"', tag[0]) if tag else None
        if not accept or "pdf" in accept[1]:
            pages.append("/" + os.path.basename(path))
    return pages


def main():
    pages = sys.argv[1:] or pdf_pages()
    data = base64.b64encode(open(PDF, "rb").read()).decode()
    cdp.connect()
    target = [t for t in cdp.http_json("/json") if t.get("type") == "page"][0]
    ws = cdp.Socket("/" + target["webSocketDebuggerUrl"].split("/", 3)[3])
    next_id = [10000]
    urls, failures = {}, []

    def send(method, session=None, **params):
        next_id[0] += 1
        msg = {"id": next_id[0], "method": method, "params": params}
        if session:
            msg["sessionId"] = session
        ws.send(msg)
        return next_id[0]

    def handle(m):
        method, p, session = m.get("method"), m.get("params", {}), m.get("sessionId")
        if method == "Target.attachedToTarget":
            # Workers wait for the debugger, so their first requests are seen too.
            sid = p["sessionId"]
            send("Network.enable", sid)
            send("Target.setAutoAttach", sid, autoAttach=True, waitForDebuggerOnStart=True, flatten=True)
            send("Runtime.runIfWaitingForDebugger", sid)
        elif method == "Network.requestWillBeSent":
            urls[(session, p["requestId"])] = p["request"]["url"]
        elif method == "Network.responseReceived":
            res = p["response"]
            if res["status"] >= 400 and not res["url"].endswith("/sw.js"):  # sw.js: a 404 on purpose
                failures.append(f"{res['status']} {res['url']}")
        elif method == "Network.loadingFailed" and p.get("errorText") != "net::ERR_ABORTED":
            failures.append(f"{p.get('errorText')} {urls.get((session, p['requestId']), '?')}")

    def pump(until=None, seconds=0.0):
        # Events keep arriving while a call is out: handle them, or workers
        # would sit waiting for the debugger.
        end = time.time() + seconds
        while True:
            try:
                m = ws.recv(timeout=60 if until else max(0.05, end - time.time()))
            except (socket.timeout, TimeoutError):
                if until:
                    raise
                return None
            if until and m.get("id") == until:
                return m
            handle(m)
            if not until and time.time() >= end:
                return None

    ws.call("Network.enable")
    ws.call("Target.setAutoAttach", autoAttach=True, waitForDebuggerOnStart=True, flatten=True)
    ready = ws.call("Runtime.evaluate", expression="!!window.__pdftoolbox", returnByValue=True)
    if not ready["result"].get("value"):
        ws.call("Page.navigate", url=ORIGIN + "/toolbox/")
        time.sleep(4)
    try:
        for page in pages:
            urls.clear()
            failures.clear()
            # In the app's frame, as the sidebar opens it.
            pump(send("Runtime.evaluate", expression="window.__pdftoolbox.open(%s)" % json.dumps(page)))
            pump(seconds=3.5)
            try:
                in_frame = "document.getElementById('view').contentWindow.eval(%s)" % json.dumps(MEASURE % data)
                m = pump(send("Runtime.evaluate", expression=in_frame, awaitPromise=True, returnByValue=True))
                r = json.loads(m["result"]["result"]["value"])
                wide = f" WIDER {r['width']}/{r['windowWidth']}" if r["width"] > r["windowWidth"] + 1 else ""
                line = (f"header={'yes' if r['bar'] else 'no':3} topbar={'shown' if r['nav'] else 'hidden':6} "
                        f"dropzone={'shown' if r['drop'] else 'hidden':6} height={r['height']}/{r['window']} "
                        f"button={r['button']}{wide}")
            except Exception as e:  # a page without the usual drop zone, a timeout
                line = f"error: {str(e)[:100]}"
            pump(seconds=0.3)
            print(f"{page:32s} {line}", flush=True)
            for f in sorted(set(failures)):
                print(f"{'':32s} failed: {f[:160]}", flush=True)
    finally:
        cdp.unforward()


if __name__ == "__main__":
    main()
