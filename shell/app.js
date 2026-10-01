// SPDX-License-Identifier: MIT
// PDF Toolbox's window: the sidebar, built from BentoPDF's tool list
// (tools.js), and the frame on the right that shows the tool. The sidebar
// follows the frame (active tool, recent tools, the window title) and the
// frame follows the URL's hash, so a restored or reopened window comes back
// to the same tool.
(() => {
  'use strict';
  const categories = window.TOOLBOX_CATEGORIES || [];
  const $ = (id) => document.getElementById(id);
  const body = document.body;
  const nav = $('nav');
  const view = $('view');
  const list = $('list');
  const q = $('q');
  const flyout = $('flyout');
  const tip = $('tip');
  const store = {
    get(key, fallback) {
      try {
        const v = localStorage.getItem('toolbox.' + key);
        return v === null ? fallback : JSON.parse(v);
      } catch {
        return fallback;
      }
    },
    set(key, value) {
      try { localStorage.setItem('toolbox.' + key, JSON.stringify(value)); } catch { /* private storage off */ }
    },
  };
  const send = (msg) => window.pdftoolbox && window.pdftoolbox.postMessage(JSON.stringify(msg));

  // A tool can be in two categories (Popular and its own); its own is the
  // last one it appears in.
  const tools = new Map();
  for (const c of categories) for (const t of c.tools) tools.set(t.id, { ...t, category: c.name });

  // ---- The list ----

  const el = (tag, props, ...kids) => {
    const e = Object.assign(document.createElement(tag), props);
    e.append(...kids);
    return e;
  };
  const words = (text) => String(text).toLowerCase().split(/[^\p{L}\p{N}]+/u).filter(Boolean);
  const icon = (name, extra) => el('i', { className: `ph ${name}${extra ? ' ' + extra : ''}` });
  const item = (t, href) => {
    const a = el('a', { className: 'item', href: href || '/' + t.id, target: 'view' },
      icon(t.icon), el('span', { className: 'label', textContent: t.name }));
    a.dataset.id = t.id;
    a.dataset.name = t.name;
    if (t.subtitle) a.title = t.subtitle;
    a.dataset.words = words(t.name).join(' ');
    a.dataset.more = words(`${t.subtitle || ''} ${t.category || ''}`).join(' ');
    return a;
  };
  const closedGroups = new Set(store.get('closed', []));
  const group = (name, iconName, items, extra) => {
    const head = el('button', { className: 'head', type: 'button' },
      icon(iconName, 'cat-icon'), el('span', { className: 'label', textContent: name }), icon('ph-caret-down', 'caret'));
    head.dataset.name = name;
    const g = el('section', { className: 'group' + (extra ? ' ' + extra : '') }, head, el('div', { className: 'items' }, ...items));
    g.dataset.name = name;
    g.classList.toggle('closed', closedGroups.has(name));
    head.setAttribute('aria-expanded', String(!g.classList.contains('closed')));
    return g;
  };
  const home = item({ id: 'home', name: 'All tools', icon: 'ph-squares-four', subtitle: 'Every tool on one page' }, '/');
  home.classList.add('home');
  const recentGroup = group('Recent', 'ph-clock-counter-clockwise', [], 'recent');
  const groups = categories.map((c) => group(c.name, c.icon,
    c.tools.map((t) => item({ ...t, category: c.name })), c.name === 'Popular Tools' ? 'popular' : ''));
  const empty = el('div', { className: 'empty', textContent: 'No tool matches.' });
  list.append(home, recentGroup, ...groups, empty);
  // Search skips Popular, whose tools are in their own categories too; a tool
  // that is only in Popular (the Workflow Builder) is searched there.
  const elsewhere = new Set(categories.filter((c) => c.name !== 'Popular Tools').flatMap((c) => c.tools.map((t) => t.id)));
  for (const a of list.querySelectorAll('.group.popular .item')) a.classList.toggle('solo', !elsewhere.has(a.dataset.id));

  // ---- Which tool is open ----

  let current = null;
  const markActive = () => {
    const id = current === 'licenses' ? 'about' : current;
    for (const a of document.querySelectorAll('#nav .item, #flyout .item')) a.classList.toggle('active', a.dataset.id === id);
    const category = tools.get(current)?.category;
    for (const g of groups) g.querySelector('.head').classList.toggle('current', g.dataset.name === category);
  };
  let recent = store.get('recent', []).filter((id) => tools.has(id));
  const renderRecent = () => {
    recentGroup.querySelector('.items').replaceChildren(...recent.map((id) => item(tools.get(id))));
    recentGroup.hidden = recent.length === 0;
    markActive();
  };
  const remember = (id) => {
    recent = [id, ...recent.filter((r) => r !== id)].slice(0, 5);
    store.set('recent', recent);
    renderRecent();
  };
  renderRecent();

  // '/merge-pdf', '/merge-pdf.html' and '/de/merge-pdf' are all Merge PDF.
  const idOf = (path) => {
    if (path.startsWith('/toolbox/')) return path.slice(9).replace(/\.html$/, '') || 'home';
    const m = /^\/(?:[a-z]{2}(?:-[A-Za-z]{2})?\/)?([^/]*?)(?:\.html)?$/.exec(path);
    return !m || !m[1] || m[1] === 'index' ? 'home' : m[1];
  };
  const safe = (path) => (typeof path === 'string' && path.startsWith('/') && !path.startsWith('//') ? path : null);
  const framePath = () => {
    try {
      const l = view.contentWindow.location;
      return l.href === 'about:blank' ? null : l.pathname + l.search;
    } catch {
      return null;
    }
  };

  view.addEventListener('load', () => {
    const path = framePath();
    if (!path) return;
    current = idOf(path.replace(/\?.*$/, ''));
    markActive();
    const tool = tools.get(current);
    const page = ((view.contentDocument && view.contentDocument.title) || '')
      .replace(/\s*[-–|]\s*(BentoPDF|PDF Toolbox)\s*$/, '');
    document.title = tool ? `${tool.name} – PDF Toolbox`
      : current === 'home' || !page ? 'PDF Toolbox'
        : page.includes('PDF Toolbox') ? page : `${page} – PDF Toolbox`;
    if (tool) remember(current);
    if (location.hash !== '#' + path) history.replaceState(null, '', '#' + path);
    const shown = list.querySelector('.group:not(.recent):not(.popular):not(.closed) .item.active');
    if (shown) shown.scrollIntoView({ block: 'nearest' });
    send({ type: 'nav' });
  });
  const open = (path) => {
    const p = safe(path);
    if (p) view.src = p;
  };
  window.addEventListener('hashchange', () => {
    const p = safe(decodeURIComponent(location.hash.slice(1)));
    if (p && p !== framePath()) view.src = p;
  });
  view.src = safe(decodeURIComponent(location.hash.slice(1))) || '/';

  // ---- Expanded, collapsed (an icon rail) and floating ----
  // Below 960 px the sidebar is a rail, and opens over the tool; above, it
  // stays as the user left it. Searching from the rail opens it over the tool.

  const narrow = matchMedia('(max-width: 959px)');
  let railPreferred = store.get('collapsed', false);
  let floating = false;
  const layout = () => {
    const rail = narrow.matches || railPreferred;
    body.classList.toggle('collapsed', rail && !floating);
    body.classList.toggle('overlay', rail && floating);
    $('toggle').setAttribute('aria-label', rail && !floating ? 'Expand the sidebar' : 'Collapse the sidebar');
    closeFlyout();
    hideTip();
  };
  const toggleNav = () => {
    if (floating) floating = false;
    else if (narrow.matches) floating = true;
    else {
      railPreferred = !railPreferred;
      store.set('collapsed', railPreferred);
    }
    layout();
  };
  const unfloat = () => {
    if (floating) {
      floating = false;
      layout();
    }
  };
  narrow.addEventListener('change', () => {
    floating = false;
    layout();
  });
  $('toggle').addEventListener('click', toggleNav);

  // ---- Category flyouts on the rail ----

  let flyoutGroup = null;
  function closeFlyout() {
    flyout.hidden = true;
    flyout.replaceChildren();
    flyoutGroup = null;
    for (const h of document.querySelectorAll('.head.open')) h.classList.remove('open');
  }
  const openFlyout = (g) => {
    if (flyoutGroup === g) return closeFlyout();
    closeFlyout();
    flyout.append(el('h2', { textContent: g.dataset.name }), ...[...g.querySelectorAll('.item')].map((a) => a.cloneNode(true)));
    flyout.hidden = false;
    const head = g.querySelector('.head');
    const r = head.getBoundingClientRect();
    flyout.style.top = Math.max(8, Math.min(r.top - 8, innerHeight - flyout.offsetHeight - 8)) + 'px';
    head.classList.add('open');
    flyoutGroup = g;
    markActive();
    hideTip();
  };
  flyout.addEventListener('click', (e) => {
    if (e.target.closest('.item')) closeFlyout();
  });
  document.addEventListener('pointerdown', (e) => {
    if (!flyout.hidden && !flyout.contains(e.target) && !e.target.closest('.head')) closeFlyout();
    if (floating && !nav.contains(e.target)) unfloat();
  });
  // A click in the tool moves the focus into its frame.
  window.addEventListener('blur', () => setTimeout(() => {
    if (document.activeElement === view) {
      closeFlyout();
      unfloat();
    }
  }, 0));

  list.addEventListener('click', (e) => {
    const head = e.target.closest('.head');
    if (head) {
      const g = head.parentElement;
      if (body.classList.contains('collapsed')) return openFlyout(g);
      g.classList.toggle('closed');
      head.setAttribute('aria-expanded', String(!g.classList.contains('closed')));
      if (g.classList.contains('closed')) closedGroups.add(g.dataset.name);
      else closedGroups.delete(g.dataset.name);
      store.set('closed', [...closedGroups]);
      return;
    }
    if (e.target.closest('.item')) {
      if (q.value) clearSearch();
      unfloat();
    }
  });
  nav.querySelector('.foot').addEventListener('click', unfloat);
  nav.querySelector('.logo').addEventListener('click', unfloat);

  // Names on the rail, where the labels are hidden.
  const hideTip = () => { tip.hidden = true; };
  nav.addEventListener('mouseover', (e) => {
    const t = e.target.closest('.item, .head, .icon-btn, .logo');
    if (!t || !body.classList.contains('collapsed') || !flyout.hidden || !t.dataset.name) return hideTip();
    tip.textContent = t.dataset.name;
    tip.hidden = false;
    const r = t.getBoundingClientRect();
    tip.style.left = Math.round(r.right + 8) + 'px';
    tip.style.top = Math.round(r.top + r.height / 2 - tip.offsetHeight / 2) + 'px';
  });
  nav.addEventListener('mouseleave', hideTip);

  // ---- Search ----

  let selected = -1;
  const searchable = (g) => [...g.querySelectorAll(g.classList.contains('popular') ? '.item.solo' : '.item')];
  const matches = () => [...list.querySelectorAll('.group:not(.recent) .item:not(.miss)')];
  const select = (i) => {
    const items = matches();
    items[selected]?.classList.remove('selected');
    selected = items.length ? (i + items.length) % items.length : -1;
    if (selected >= 0) {
      items[selected].classList.add('selected');
      items[selected].scrollIntoView({ block: 'nearest' });
    }
  };
  // Each word typed starts a word of the tool's name ("sign" finds Sign PDF
  // and Digital Signature, "word" doesn't find Remove Password); when no name
  // matches, its description and category count too ("secure", "convert").
  function filter() {
    const typed = words(q.value);
    const searching = typed.length > 0;
    body.classList.toggle('searching', searching);
    const hits = (a, more) => {
      const own = (more ? `${a.dataset.words} ${a.dataset.more}` : a.dataset.words).split(' ');
      return typed.every((w) => own.some((o) => o.startsWith(w)));
    };
    const byName = groups.some((g) => searchable(g).some((a) => hits(a, false)));
    let any = false;
    for (const g of groups) {
      const own = searchable(g);
      let hit = false;
      for (const a of g.querySelectorAll('.item')) {
        const ok = own.includes(a) && hits(a, !byName);
        a.classList.toggle('miss', searching && !ok);
        a.classList.remove('selected');
        hit = hit || ok;
      }
      g.classList.toggle('miss', searching && !hit);
      any = any || hit;
    }
    body.classList.toggle('no-match', searching && !any);
    selected = -1;
    if (searching) select(0);
    else list.scrollTop = 0;
  }
  function clearSearch() {
    q.value = '';
    filter();
  }
  q.addEventListener('input', filter);
  q.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
      e.preventDefault();
      select(selected + (e.key === 'ArrowDown' ? 1 : -1));
    } else if (e.key === 'Enter') {
      const a = matches()[Math.max(selected, 0)];
      if (a && q.value.trim()) {
        e.preventDefault();
        a.click();
        view.focus();
      }
    } else if (e.key === 'Escape') {
      e.preventDefault();
      if (q.value) clearSearch();
      else {
        q.blur();
        unfloat();
      }
    }
  });
  const focusSearch = () => {
    if (body.classList.contains('collapsed')) {
      floating = true;
      layout();
    }
    q.focus();
    q.select();
  };
  $('search-btn').addEventListener('click', focusSearch);

  // ---- Keys, here and in the tool (the page script forwards them) ----

  const key = (e) => {
    const mod = (e.ctrlKey || e.metaKey) && !e.altKey && !e.shiftKey;
    const k = String(e.key || '').toLowerCase();
    if (mod && k === 'k') { focusSearch(); return true; }
    if (mod && k === 'b') { toggleNav(); return true; }
    if (k === 'escape' && (!flyout.hidden || floating)) {
      closeFlyout();
      unfloat();
      return true;
    }
    return false;
  };
  document.addEventListener('keydown', (e) => {
    if (e.target === q && e.key === 'Escape') return;
    if (key(e)) {
      e.preventDefault();
      e.stopPropagation();
    }
  }, true);

  // ---- Printing a tool's page ----
  // Android prints the window's top page, not a frame, so a copy of the
  // tool's page (its styles, with its own print rules, and its body) stands
  // in for the sidebar and the frame until the print dialog closes.

  // The print in progress: its id comes back from the app with printed(), so
  // a late onFinish from an earlier print can't take down a newer one's copy.
  let printing = null;
  const printTool = () => {
    const doc = view.contentDocument;
    if (!doc || !doc.body) return;
    const root = $('print-root');
    const copy = el('div', { className: doc.body.className });
    for (const n of doc.body.childNodes) copy.append(n.cloneNode(true));
    const styles = [...doc.querySelectorAll('link[rel="stylesheet"], style')].map((n) => n.cloneNode(true));
    root.replaceChildren(...styles, copy);
    document.documentElement.classList.add('printing');
    const loaded = [...root.querySelectorAll('link[rel="stylesheet"]')].map((l) => new Promise((resolve) => {
      l.addEventListener('load', resolve, { once: true });
      l.addEventListener('error', resolve, { once: true });
      setTimeout(resolve, 3000);
    }));
    Promise.all(loaded).then(() => {
      // The app calls printed(id) when Android is done with the document;
      // focus and a click are fallbacks.
      const id = crypto.randomUUID();
      const restore = () => {
        document.documentElement.classList.remove('printing');
        root.replaceChildren();
        removeEventListener('focus', restore);
        removeEventListener('pointerdown', restore, true);
        if (printing && printing.id === id) printing = null;
      };
      printing = { id, restore };
      send({ type: 'print', title: document.title, id });
      addEventListener('focus', restore, { once: true });
      addEventListener('pointerdown', restore, { once: true, capture: true });
    });
  };

  // Tells the tool in the frame that files are waiting ("Open with", "Share"
  // while the app is open): the app asks, and the tool's page answers with its
  // own channel. It holds them for the next tool rather than taking them.
  const poke = () => {
    try { view.contentWindow.pdftoolbox.postMessage(JSON.stringify({ type: 'ready', hold: true })); } catch { /* no tool page yet */ }
  };

  window.__pdftoolbox = { key, print: printTool, printed: (id) => printing && printing.id === id && printing.restore(), poke, open };
  layout();
})();
