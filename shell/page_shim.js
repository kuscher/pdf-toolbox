// BentoBook page shim. The app injects it at document start into every
// page of its own origin. `bentobook` is the app's message channel
// (WebViewCompat.addWebMessageListener).
(() => {
  'use strict';
  if (window.__bentobook) return;
  window.__bentobook = true;
  const isTop = window.top === window;
  const host = () => window.bentobook;
  const send = (msg) => host() && host().postMessage(JSON.stringify(msg));

  // 1. No service worker: the files are local already, and WebView would not
  //    route the worker's fetches to the app.
  if (navigator.serviceWorker) {
    try {
      Object.defineProperty(navigator.serviceWorker, 'register', {
        value: () => Promise.reject(new DOMException('Not needed in BentoBook', 'NotSupportedError')),
        configurable: true,
      });
    } catch { /* leave it */ }
  }

  // 2. Installed-app mode, so the page skips "install this app" prompts.
  const realMatchMedia = window.matchMedia.bind(window);
  const mode = /\(\s*display-mode\s*:\s*(standalone|browser)\s*\)/;
  window.matchMedia = function (query) {
    const list = realMatchMedia(query);
    const m = mode.exec(String(query));
    if (!m) return list;
    const matches = m[1] === 'standalone';
    return new Proxy(list, {
      get(target, prop) {
        if (prop === 'matches') return matches;
        const value = Reflect.get(target, prop, target);
        return typeof value === 'function' ? value.bind(target) : value;
      },
    });
  };

  // 3. Downloads. BentoPDF saves with <a download href="blob:…"> and revokes
  //    the URL right away, which native code can't fetch. Keep each blob as it
  //    is created and stream its bytes to the app, which writes them to
  //    Download/. Chunks keep big PDFs out of single huge messages.
  const CHUNK = 4 << 20;
  let nextId = 0;
  const blobs = new Map();
  const createURL = URL.createObjectURL;
  const revokeURL = URL.revokeObjectURL;
  URL.createObjectURL = function (obj) {
    const url = createURL.call(URL, obj);
    if (obj instanceof Blob) blobs.set(url, obj);
    return url;
  };
  URL.revokeObjectURL = function (url) {
    setTimeout(() => blobs.delete(url), 60000);
    return revokeURL.call(URL, url);
  };
  const save = async (blob, name) => {
    const id = ++nextId;
    send({ type: 'download', id, name, mime: blob.type, size: blob.size });
    for (let at = 0; at < blob.size; at += CHUNK) {
      host().postMessage(await blob.slice(at, at + CHUNK).arrayBuffer());
    }
    send({ type: 'download.end', id });
  };
  const saveLink = (a) => {
    if (!host() || !a.hasAttribute('download')) return false;
    const blob = blobs.get(a.href);
    if (!blob) return false;
    const name = a.getAttribute('download') || 'download';
    save(blob, name).catch((e) => send({ type: 'download.failed', name, error: String(e) }));
    return true;
  };
  const click = HTMLAnchorElement.prototype.click;
  HTMLAnchorElement.prototype.click = function () {
    if (!saveLink(this)) return click.call(this);
  };
  document.addEventListener('click', (event) => {
    const a = event.target instanceof Element && event.target.closest('a[download]');
    if (a && saveLink(a)) event.preventDefault();
  }, true);

  // 4. window.print() (the Markdown editor's Print) goes to Android printing.
  if (isTop) {
    window.print = () => send({ type: 'print', title: document.title });
  }

  // 5. Files opened with or shared to BentoBook. Every tool is its own page,
  //    so the app keeps them and hands them to each page as it loads, until a
  //    tool's file input takes them, exactly as if they had been picked.
  if (isTop) {
    let incoming = [];
    let current = null;
    const accepts = (input, files) => {
      const accept = (input.getAttribute('accept') || '').split(',').map((s) => s.trim().toLowerCase()).filter(Boolean);
      if (!accept.length) return true;
      return files.every((f) => accept.some((a) => a.startsWith('.')
        ? f.name.toLowerCase().endsWith(a)
        : a.endsWith('/*') ? f.type.startsWith(a.slice(0, -1)) : f.type === a));
    };
    const offer = () => {
      if (!incoming.length) return;
      const input = [...document.querySelectorAll('input[type=file]')]
        .find((i) => !i.disabled && accepts(i, incoming));
      if (!input) return;
      const dt = new DataTransfer();
      for (const f of input.multiple ? incoming : incoming.slice(0, 1)) dt.items.add(f);
      input.files = dt.files;
      input.dispatchEvent(new Event('input', { bubbles: true }));
      input.dispatchEvent(new Event('change', { bubbles: true }));
      send({ type: 'incoming.used', count: dt.files.length });
      incoming = [];
      banner();
    };
    const banner = () => {
      let bar = document.getElementById('bentobook-incoming');
      if (!incoming.length) { if (bar) bar.remove(); return; }
      if (!bar) {
        bar = document.createElement('div');
        bar.id = 'bentobook-incoming';
        bar.style.cssText = 'position:fixed;left:50%;bottom:16px;transform:translateX(-50%);z-index:2147483647;'
          + 'background:#1f2937;color:#f9fafb;border:1px solid #6366f1;border-radius:10px;padding:10px 14px;'
          + 'font:14px system-ui,sans-serif;box-shadow:0 8px 24px rgba(0,0,0,.4);display:flex;gap:12px;align-items:center';
        document.body.appendChild(bar);
      }
      const n = incoming.length;
      const text = document.createElement('span');
      text.textContent = `${n === 1 ? incoming[0].name : n + ' files'}: open a tool and ${n === 1 ? 'it goes' : 'they go'} straight in.`;
      const dismiss = document.createElement('button');
      dismiss.textContent = 'Dismiss';
      dismiss.style.cssText = 'background:none;border:1px solid #6b7280;color:inherit;border-radius:6px;padding:2px 8px;cursor:pointer';
      dismiss.onclick = () => { incoming = []; banner(); send({ type: 'incoming.used', count: 0 }); };
      bar.replaceChildren(text, dismiss);
    };
    const finish = () => {
      if (current) incoming.push(new File(current.chunks, current.name, { type: current.mime }));
      current = null;
    };
    host() && host().addEventListener('message', (event) => {
      if (typeof event.data !== 'string') {
        if (current) current.chunks.push(event.data);
        return;
      }
      let m;
      try { m = JSON.parse(event.data); } catch { return; }
      if (m.type === 'incoming.begin') {
        incoming = [];
        current = null;
      } else if (m.type === 'incoming.file') {
        finish();
        current = { name: m.name, mime: m.mime, chunks: [] };
      } else if (m.type === 'incoming.end') {
        finish();
        banner();
        offer();
      }
    });
    const watch = () => {
      new MutationObserver(offer).observe(document.documentElement, { subtree: true, childList: true });
      send({ type: 'ready', isolated: self.crossOriginIsolated === true, sab: typeof SharedArrayBuffer === 'function' });
    };
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', watch, { once: true });
    else watch();
  }

  // 7. Tool pages stack a 256 px drop zone and the file card above the tool's
  //    workspace (Sign's editor, the PDF Editor's viewer, sized 75vh), which
  //    suits a big monitor but leaves the workspace below the fold in a laptop
  //    window: the tool looks as if it still wants a file. Once a file is in
  //    and a workspace shows up, fold the drop zone away (single-file tools;
  //    multi-file ones keep it for adding more) and bring the workspace to the
  //    top. Removing the file brings the drop zone back.
  if (isTop) {
    let fitted = null;
    let queued = false;
    const fit = () => {
      queued = false;
      const drop = document.getElementById('drop-zone');
      if (!drop) return;
      const input = drop.querySelector('input[type=file]');
      const area = document.getElementById('file-display-area');
      const loaded = area ? area.children.length > 0 : !!(input && input.files.length);
      if (!loaded) {
        if (fitted) {
          drop.style.display = '';
          fitted = null;
        }
        return;
      }
      if (fitted && fitted.isConnected && fitted.offsetHeight) return;
      const below = drop.getBoundingClientRect().bottom - 1;
      // Anywhere below the drop zone: Sign's editor sits outside the upload card.
      const workspace = [...document.body.querySelectorAll('div, section, canvas, iframe')].find((e) =>
        e.offsetHeight >= innerHeight * 0.5 && !e.contains(drop) && e.getBoundingClientRect().top >= below);
      if (!workspace) return;
      fitted = workspace;
      if (input && !input.multiple) drop.style.display = 'none';
      workspace.scrollIntoView({ block: 'start' });
    };
    const queue = () => {
      if (!queued) {
        queued = true;
        setTimeout(fit, 100);
      }
    };
    const start = () => {
      if (!document.getElementById('drop-zone')) return;
      new MutationObserver(queue).observe(document.body, {
        subtree: true, childList: true, attributes: true, attributeFilter: ['class', 'hidden', 'style'],
      });
    };
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start, { once: true });
    else start();
  }

  // 6. Page colour for the window caption: the theme-color meta tag, else the
  //    background of the page's top edge.
  if (isTop) {
    let last = '';
    const hex = (css) => {
      const m = /^rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?/.exec(css || '');
      if (!m || m[4] === '0') return '';
      return '#' + m.slice(1, 4).map((n) => (+n).toString(16).padStart(2, '0')).join('');
    };
    const topColor = () => {
      let el = document.elementFromPoint(window.innerWidth / 2, 2);
      while (el) {
        const c = hex(getComputedStyle(el).backgroundColor);
        if (c) return c;
        el = el.parentElement;
      }
      return hex(getComputedStyle(document.documentElement).backgroundColor) || '#ffffff';
    };
    const report = () => {
      const color = topColor();
      if (color === last) return;
      last = color;
      send({ type: 'theme', color });
    };
    const start = () => { report(); setInterval(report, 1500); };
    if (document.readyState === 'complete') start();
    else window.addEventListener('load', start, { once: true });
  }
})();
