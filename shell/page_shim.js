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

  // 6. Compact tool layout. BentoPDF's tool pages stack its sticky top bar, a
  //    title block and a 256 px drop zone above the file card and the tool
  //    itself, capped at 672 px wide, with viewers sized 75 to 85vh: fine on a
  //    big monitor, but in a laptop window the tool starts below the fold, and
  //    scrolled to, its toolbar hides under the sticky top bar. Once a file is
  //    in, fold all of that into one slim header (back, tool, file, Change
  //    file, Details). Viewer tools (Sign, PDF Editor, Crop, Form Filler,
  //    Stamps) also fold the file card, go full width and get their viewer
  //    sized so the whole tool ends at the window's bottom edge. Multi-file
  //    tools keep their file list (reordering happens there). Tools that are
  //    a full page already (Edit PDF Text, Bookmarks, Watermark) are left
  //    alone. Removing the file, or the tool dropping its workspace, restores
  //    the page.
  if (isTop) {
    let state = null;
    let queued = false;
    const css = (el, props) => {
      const old = {};
      for (const k of Object.keys(props)) { old[k] = el.style[k]; el.style[k] = props[k]; }
      return old;
    };
    const flowing = (el) => {
      if (!(el instanceof HTMLElement) || el.id === 'bentobook-toolbar') return false;
      if (/^(SCRIPT|STYLE|TEMPLATE|LINK|META)$/.test(el.tagName) || !el.offsetHeight) return false;
      const pos = getComputedStyle(el).position;
      return pos !== 'fixed' && pos !== 'absolute';
    };
    const pageTop = (el) => el.getBoundingClientRect().top + window.scrollY;
    // The tool's main block: an element at least half the window tall, below
    // the drop zone, outside the upload card's header.
    const workspaceFor = (drop) => {
      const below = drop.offsetHeight ? drop.getBoundingClientRect().bottom - 1 : -Infinity;
      return [...document.body.querySelectorAll('div, section')].find((e) =>
        e.offsetHeight >= innerHeight * 0.5 && !e.contains(drop) && e.id !== 'bentobook-toolbar'
        && e.getBoundingClientRect().top >= below);
    };
    // Its resizable part: the viewer box with a fixed height (h-[75vh],
    // style="height: 85vh"), else its tallest scroller. Pixel heights are left
    // out: those belong to a viewer's own layout (Cropper.js).
    const resizable = (ws) => {
      const big = [ws, ...ws.querySelectorAll('div, section, iframe')]
        .filter((e) => e.offsetHeight >= ws.offsetHeight * 0.35);
      const fixed = big.filter((e) => /(^|\s)(h-\[|min-h-\[|h-screen)/.test(String(e.className)) || /vh/.test(e.style.height));
      const scroller = big.filter((e) => /auto|scroll/.test(getComputedStyle(e).overflowY));
      const pick = (list) => list.sort((a, b) => b.offsetHeight - a.offsetHeight)[0];
      return pick(fixed) || pick(scroller) || null;
    };
    const visual = (ws) => [...ws.querySelectorAll('canvas, iframe, img, embed')]
      .some((e) => e.offsetHeight >= ws.offsetHeight * 0.3);
    // What follows the drop zone on the page: the file card on most tools,
    // Merge's own file list.
    const afterDrop = (drop) => {
      for (let n = drop; n && n !== document.body; n = n.parentElement) {
        for (let sib = n.nextElementSibling; sib; sib = sib.nextElementSibling) {
          if (flowing(sib)) return sib;
        }
      }
      return null;
    };
    // The page's file list: the standard file card, or Bates' own list.
    const fileList = () => document.getElementById('file-display-area') || document.getElementById('file-list');
    // The biggest picture in a viewer (Adjust Colors' preview): a fallback
    // to shrink when there is no viewer box.
    const picture = (ws) => [...ws.querySelectorAll('canvas, img')]
      .filter((e) => e.offsetHeight >= ws.offsetHeight * 0.3).sort((a, b) => b.offsetHeight - a.offsetHeight)[0] || null;
    const fileLabel = (input, area) => {
      if (input && input.files.length > 1) return `${input.files.length} files`;
      if (input && input.files.length === 1) return input.files[0].name;
      if (input && input.multiple && area && area.children.length > 1) return `${area.children.length} files`;
      const name = area && area.querySelector('.truncate, .font-medium');
      if (name && name.textContent.trim()) return name.textContent.trim();
      return input && input.files[0] ? input.files[0].name : '';
    };
    const button = (label, title, onclick) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.textContent = label;
      b.title = title;
      b.style.cssText = 'flex:none;background:#374151;color:#e5e7eb;border:1px solid #4b5563;border-radius:8px;'
        + 'padding:5px 12px;font-family:inherit;font-size:13px;font-weight:500;line-height:1.2;cursor:pointer;white-space:nowrap';
      b.onmouseenter = () => { b.style.background = '#4b5563'; };
      b.onmouseleave = () => { b.style.background = '#374151'; };
      b.onclick = onclick;
      return b;
    };
    // Cropper.js scales its page by a single ratio when the window resizes,
    // which leaves it taller than its box and off centre. These are the crops
    // (in the page's own pixels) to put back after laying it out afresh; the
    // instance sits on its image as .cropper.
    const crops = (box) => [...(box ? box.querySelectorAll('img') : [])]
      .map((img) => img.cropper).filter((c) => c && c.ready && typeof c.render === 'function')
      .map((c) => [c, c.getData()]);
    const fit = () => {
      if (!state || state.expanded || !(state.flex || state.picture)) return;
      const resized = !!state.crops;
      const saved = state.crops || crops(state.flex);
      state.crops = null;
      // The tool ends at its workspace or whatever follows it on the page
      // (Sign's Apply button sits after its viewer).
      let bottom = state.anchor.getBoundingClientRect().bottom;
      for (let n = state.anchor; n && n.parentElement !== document.body; n = n.parentElement) {
        for (let sib = n.nextElementSibling; sib; sib = sib.nextElementSibling) {
          if (flowing(sib)) bottom = Math.max(bottom, sib.getBoundingClientRect().bottom);
        }
      }
      // Plus the paddings and borders of the boxes around it.
      for (let n = state.anchor.parentElement; n && n !== document.body; n = n.parentElement) {
        const cs = getComputedStyle(n);
        bottom += (parseFloat(cs.paddingBottom) || 0) + (parseFloat(cs.borderBottomWidth) || 0);
        if (n === state.root) break;
      }
      const box = state.flex || state.picture;
      const height = Math.max(240, Math.round(box.offsetHeight - (bottom + 4 - innerHeight)));
      const changed = Math.abs(height - box.offsetHeight) > 1;
      if (changed) {
        if (state.flex) {
          css(state.flex, { height: height + 'px', maxHeight: 'none', minHeight: '0' });
        } else {
          // A picture keeps its proportions: cap its height, let the width follow.
          css(state.picture, { width: 'auto', height: 'auto', maxWidth: '100%', maxHeight: height + 'px' });
        }
        // Viewers lay out on window resize (the PDF editor), not when their
        // box changes.
        state.fitting = true;
        window.dispatchEvent(new Event('resize'));
        state.fitting = false;
      }
      if (changed || resized) {
        for (const [cropper, data] of saved) {
          cropper.render();
          cropper.setData(data);
        }
      }
    };
    const setExpanded = (on) => {
      state.expanded = on;
      for (const [el, display] of state.hidden) el.style.display = on && !state.chrome.has(el) ? display : 'none';
      state.details.textContent = on ? 'Hide details' : 'Details';
      if (on && state.flex) css(state.flex, state.flexStyle);
      if (on && state.picture) css(state.picture, state.pictureStyle);
      if (!on) {
        window.scrollTo(0, 0);
        fit();
      }
    };
    const enter = (drop, input, area, ws) => {
      const viewer = !!ws && !!(resizable(ws) || visual(ws));
      let anchor = viewer ? ws : afterDrop(drop);
      // Single-file tools: the header names the file, so the card folds too
      // and the view starts at the tool's options.
      if (anchor && !viewer && !input.multiple && anchor === area) {
        for (let sib = area.nextElementSibling; sib; sib = sib.nextElementSibling) {
          if (flowing(sib)) { anchor = sib; break; }
        }
      }
      if (!anchor) return;
      const root = document.getElementById('uploader') || anchor.parentElement;
      const title = (document.querySelector('#tool-uploader h1, #uploader h1') || document.querySelector('h1') || {}).textContent
        || document.title;
      // Hide everything laid out before the anchor, level by level up to
      // <body> (that includes the sticky top bar).
      const hidden = [];
      for (let n = anchor; n && n !== document.body; n = n.parentElement) {
        for (let sib = n.previousElementSibling; sib; sib = sib.previousElementSibling) {
          if (!flowing(sib)) continue;
          hidden.push([sib, sib.style.display]);
          sib.style.display = 'none';
        }
      }
      // And the footer after the page: the tool ends at the window's bottom.
      let top = anchor;
      while (top.parentElement && top.parentElement !== document.body) top = top.parentElement;
      const chrome = new Set(hidden.filter(([el]) => el.parentElement === document.body).map(([el]) => el));
      for (let sib = top.nextElementSibling; sib; sib = sib.nextElementSibling) {
        if (!flowing(sib)) continue;
        hidden.push([sib, sib.style.display]);
        chrome.add(sib);
        sib.style.display = 'none';
      }
      const styled = [];
      const tighten = (n) => {
        if (n === root) return { paddingTop: '12px', paddingBottom: '12px', minHeight: '0' };
        if (n.id === 'tool-uploader') return { paddingTop: '12px', paddingBottom: '12px', marginTop: '0' };
        return {};
      };
      for (let n = anchor; n && n !== document.body; n = n.parentElement) {
        const props = tighten(n);
        if (n === anchor) props.marginTop = '0';
        // Viewers go full width; forms keep BentoPDF's readable 672 px.
        if (viewer && getComputedStyle(n).maxWidth !== 'none') props.maxWidth = 'none';
        if (Object.keys(props).length) styled.push([n, css(n, props)]);
      }
      const bar = document.createElement('div');
      bar.id = 'bentobook-toolbar';
      bar.style.cssText = 'position:sticky;top:0;z-index:40;display:flex;align-items:center;gap:10px;'
        + 'height:48px;padding:0 12px;background:#1f2937;border-bottom:1px solid #374151;'
        + 'color:#e5e7eb;font-family:inherit;font-size:14px;line-height:1.2;box-sizing:border-box';
      const back = button('← Tools', 'Back to all tools', () => {
        const b = document.getElementById('back-to-tools');
        if (b) b.click(); else location.href = '/';
      });
      const name = document.createElement('div');
      name.style.cssText = 'flex:none;font-weight:600;color:#fff;white-space:nowrap';
      name.textContent = title.trim();
      const file = document.createElement('div');
      file.style.cssText = 'flex:1;min-width:0;color:#9ca3af;overflow:hidden;text-overflow:ellipsis;white-space:nowrap';
      const change = button(input.multiple ? 'Add files' : 'Change file',
        input.multiple ? 'Add more files' : 'Open another file', () => input.click());
      const details = button('Details', 'Show the tool description and the drop zone', () => setExpanded(!state.expanded));
      bar.append(back, name, file, change, details);
      document.body.prepend(bar);
      const flex = viewer ? resizable(ws) : null;
      const pic = viewer && !flex ? picture(ws) : null;
      state = {
        drop, input, area, ws, anchor, viewer, root, bar, file, details, hidden, chrome, styled, flex, expanded: false,
        picture: pic,
        pictureStyle: pic ? { width: pic.style.width, height: pic.style.height, maxWidth: pic.style.maxWidth, maxHeight: pic.style.maxHeight } : null,
        flexStyle: flex ? { height: flex.style.height, maxHeight: flex.style.maxHeight, minHeight: flex.style.minHeight } : null,
      };
      file.textContent = fileLabel(input, area);
      window.scrollTo(0, 0);
      fit();
      setTimeout(fit, 300);
      setTimeout(fit, 1200);
    };
    const leave = () => {
      for (const [el, display] of state.hidden) el.style.display = display;
      for (const [el, old] of state.styled) css(el, old);
      if (state.flex) css(state.flex, state.flexStyle);
      if (state.picture) css(state.picture, state.pictureStyle);
      state.bar.remove();
      state = null;
    };
    const check = () => {
      queued = false;
      const drop = document.getElementById('drop-zone');
      if (!drop) return;
      const input = drop.querySelector('input[type=file]');
      const area = fileList();
      // The page's own list, when it has one: the input keeps its files after
      // the list's remove button empties it.
      const loaded = area ? area.children.length > 0 : !!(input && input.files.length);
      if (state) {
        if (!loaded || !state.anchor.isConnected || (!state.anchor.offsetHeight && !state.expanded)) {
          leave();
        } else {
          state.file.textContent = fileLabel(input, area);
          // A viewer that shows up after the file card: switch to viewer mode.
          if (state.viewer || state.expanded) return;
          const ws = workspaceFor(drop);
          if (!ws || !(resizable(ws) || visual(ws))) return;
          leave();
        }
      }
      if (!loaded || !input) return;
      const ws = workspaceFor(drop);
      if (ws && pageTop(ws) < 150) return; // a full-page tool already
      enter(drop, input, area, ws);
    };
    const queue = () => {
      if (!queued) {
        queued = true;
        setTimeout(check, 150); // not requestAnimationFrame: it stalls while the window is hidden
      }
    };
    // Registered before any viewer's own listener, so it sees the crops
    // before Cropper.js rescales them.
    window.addEventListener('resize', () => {
      if (!state || state.fitting) return;
      state.crops = crops(state.flex);
      setTimeout(fit, 50);
    });
    const start = () => {
      if (!document.getElementById('drop-zone')) return;
      new MutationObserver((records) => {
        if (state && records.every((r) => state.bar.contains(r.target))) return;
        queue();
      }).observe(document.body, {
        subtree: true, childList: true, attributes: true, attributeFilter: ['class', 'hidden'],
      });
    };
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start, { once: true });
    else start();
  }

  // 7. Page colour for the window caption: the theme-color meta tag, else the
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
