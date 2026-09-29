#!/usr/bin/env python3
"""
Build a single searchable page containing all stanzas of The Rape of Lucrece.

Every stanza is rendered as plain text in the DOM (no virtual scrolling, nothing
hidden) so the browser's own Ctrl+F / Cmd+F works across the whole poem. A
sticky header tracks which stanza is currently on screen, so after a Ctrl+F jump
the stanza number is always visible.

Output: docs/shakespeare/rape-of-lucrece/all-stanzas.html
"""

import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
STANZAS_JSON = HERE / "stanzas.json"
OUT = ROOT / "docs" / "shakespeare" / "rape-of-lucrece" / "all-stanzas.html"

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The Rape of Lucrece - All Stanzas (searchable)</title>
<style>
  :root {
    color-scheme: dark;
    --bg: #17140f;
    --panel: #1f1b15;
    --ink: #eae4da;
    --muted: #a89e90;
    --accent: #e0a066;
    --accent2: #d2691e;
    --rule: #3a322a;
    --badge-bg: #2a231b;
    --hit: #5c4a1a;
    --barh: 120px;
  }

  * { box-sizing: border-box; }
  body {
    margin: 0;
    background: var(--bg);
    color: var(--ink);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6;
  }

  /* ---- sticky tracker ---- */
  .bar {
    position: sticky;
    top: 0;
    z-index: 50;
    background: var(--panel);
    border-bottom: 2px solid var(--accent2);
    padding: 10px 16px;
    display: flex;
    flex-wrap: wrap;
    gap: 10px 14px;
    align-items: center;
  }
  .bar .now {
    font-weight: 700;
    color: var(--accent);
    font-size: 1.05rem;
    white-space: nowrap;
  }
  .bar .now .lines {
    font-weight: 400;
    color: var(--muted);
    font-size: .85rem;
    margin-left: 6px;
  }
  .bar .spacer { flex: 1 1 auto; }
  .bar a.jump {
    color: var(--accent);
    font-weight: 600;
    text-decoration: none;
    font-size: .85rem;
    white-space: nowrap;
  }
  .bar a.jump:hover { text-decoration: underline; }
  input[type="search"], input[type="number"] {
    font: inherit;
    font-size: .9rem;
    padding: 6px 9px;
    border: 1px solid var(--rule);
    border-radius: 6px;
    background: var(--bg);
    color: var(--ink);
  }
  input[type="number"] { width: 5.5rem; }
  input[type="search"] { width: min(260px, 45vw); }

  #findout:empty { display: none; }
  #findout {
    width: 100%;
    font-size: .85rem;
    color: var(--muted);
    max-height: 4.6em;      /* a long hit list must not swallow the viewport */
    overflow-y: auto;
    overscroll-behavior: contain;
  }
  #findout b { color: var(--accent); }
  #findout .chip {
    display: inline-block;
    margin: 3px 4px 0 0;
    padding: 1px 8px;
    background: var(--badge-bg);
    border: 1px solid var(--rule);
    border-radius: 999px;
    text-decoration: none;
    color: var(--accent);
    font-weight: 600;
    font-size: .8rem;
  }
  .chip:hover { background: var(--accent2); color: #fff; }

  /* ---- body ---- */
  main {
    max-width: 820px;
    margin: 0 auto;
    padding: 24px 16px 64px;
  }
  header.title { margin-bottom: 8px; }
  header.title h1 {
    color: var(--accent);
    border-bottom: 3px solid var(--accent2);
    padding-bottom: 10px;
    margin: 0 0 8px;
    font-size: 1.6rem;
  }
  header.title p { color: var(--muted); margin: 6px 0; font-size: .92rem; }

  .stanza {
    background: var(--panel);
    border: 1px solid var(--rule);
    border-left: 4px solid var(--accent2);
    border-radius: 8px;
    padding: 14px 16px;
    margin: 18px 0;
    scroll-margin-top: calc(var(--barh) + 14px);
  }
  .stanza.cur { border-left-color: var(--accent); }
  .shead {
    display: flex;
    align-items: baseline;
    gap: 10px;
    flex-wrap: wrap;
    margin-bottom: 8px;
    padding-bottom: 6px;
    border-bottom: 1px dashed var(--rule);
  }
  .snum {
    font-weight: 700;
    color: var(--accent);
    font-size: 1rem;
  }
  .shead a {
    margin-left: auto;
    font-size: .78rem;
    font-weight: 600;
    color: var(--accent2);
    text-decoration: none;
    white-space: nowrap;
  }
  .shead a:hover { text-decoration: underline; }
  @media print { .shead a { display: none; } }
  ol.lines {
    margin: 0;
    padding: 0;
    list-style: none;
    font-family: Georgia, 'Iowan Old Style', 'Times New Roman', serif;
    font-size: 1.02rem;
  }
  ol.lines li {
    display: flex;
    gap: 12px;
    padding: 1px 0;
  }
  ol.lines .ln {
    flex: 0 0 3.2rem;
    text-align: right;
    color: var(--muted);
    font-family: 'Monaco', 'Menlo', monospace;
    font-size: .72rem;
    padding-top: .35rem;
    user-select: none;
  }
  mark { background: var(--hit); color: inherit; border-radius: 2px; }

  /* lets the last stanzas scroll up under the bar, so the tracker can name them */
  .tail { height: 60vh; }

  @media (max-width: 520px) {
    ol.lines .ln { flex-basis: 2.4rem; }
    .bar { padding: 8px 12px; }
  }
  @media print {
    .bar { display: none; }
    .stanza { break-inside: avoid; box-shadow: none; }
    .tail { display: none; }
  }
</style>
</head>
<body>

<div class="bar">
  <span class="now" id="now">Stanza 1<span class="lines" id="nowlines">lines 1-7</span></span>
  <span class="spacer"></span>
  <input type="search" id="q" placeholder="Find text &rarr; get stanza no." autocomplete="off" spellcheck="false">
  <input type="number" id="go" min="1" max="__TOTAL__" placeholder="# 1-__TOTAL__">
  <a class="jump" href="index.html">Overview</a>
  <a class="jump" href="#top">Top</a>
  <div id="findout"></div>
</div>

<main id="top">
  <header class="title">
    <h1>The Rape of Lucrece &mdash; All Stanzas</h1>
    <p>William Shakespeare &middot; __TOTAL__ stanzas &middot; __LINES__ lines, complete on one page.</p>
    <p>Search any phrase to find which stanza it belongs to.</p>
  </header>

__STANZAS__
</main>

<div class="tail" aria-hidden="true"></div>

<script>
(function () {
  var blocks = Array.prototype.slice.call(document.querySelectorAll('.stanza'));
  var bar = document.querySelector('.bar');
  var barh = 120;
  function syncBar() {
    barh = Math.ceil(bar.getBoundingClientRect().height);
    document.documentElement.style.setProperty('--barh', barh + 'px');
  }
  var nowEl = document.getElementById('now');
  var nowLines = document.getElementById('nowlines');
  var cur = null;

  /* --- track which stanza is on screen (also catches Ctrl+F jumps) --- */
  var tops = [];
  function measure() {
    tops = blocks.map(function (b) { return b.getBoundingClientRect().top + window.scrollY; });
  }
  function update() {
    var probe = window.scrollY + barh + 18;
    var lo = 0, hi = tops.length - 1, idx = 0;
    while (lo <= hi) {
      var mid = (lo + hi) >> 1;
      if (tops[mid] <= probe) { idx = mid; lo = mid + 1; } else { hi = mid - 1; }
    }
    var b = blocks[idx];
    if (b === cur) return;
    if (cur) cur.classList.remove('cur');
    b.classList.add('cur');
    cur = b;
    nowEl.firstChild.nodeValue = 'Stanza ' + b.dataset.n + ' ';
    nowLines.textContent = 'lines ' + b.dataset.from + '-' + b.dataset.to;
  }
  var queued = false;
  function onScroll() {
    if (queued) return;
    queued = true;
    requestAnimationFrame(function () { queued = false; update(); });
  }
  syncBar(); measure(); update();
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', function () { syncBar(); measure(); update(); });

  /* --- jump straight to a stanza number --- */
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(function () { syncBar(); measure(); update(); });
  }

  document.getElementById('go').addEventListener('change', function () {
    var n = parseInt(this.value, 10);
    var t = document.getElementById('s' + n);
    if (t) t.scrollIntoView({ block: 'start' });
  });

  /* --- in-page search: reports which stanzas contain the phrase --- */
  var q = document.getElementById('q');
  var out = document.getElementById('findout');
  function setOut(h) {            // bar height changes with this row, so re-measure
    out.innerHTML = h;
    syncBar(); measure(); update();
  }
  var texts = blocks.map(function (b) {
    return b.querySelector('ol.lines').textContent.toLowerCase().replace(/\\s+/g, ' ');
  });

  function clearMarks() {
    blocks.forEach(function (b) {
      if (!b.dataset.marked) return;
      delete b.dataset.marked;
      b.querySelectorAll('mark').forEach(function (m) {
        m.replaceWith(document.createTextNode(m.textContent));
      });
      b.querySelector('ol.lines').normalize();
    });
  }

  function markIn(block, needle) {
    var walker = document.createTreeWalker(
      block.querySelector('ol.lines'), NodeFilter.SHOW_TEXT);
    var nodes = [], n;
    while ((n = walker.nextNode())) nodes.push(n);
    nodes.forEach(function (node) {
      if (node.parentNode.classList && node.parentNode.classList.contains('ln')) return;
      var low = node.nodeValue.toLowerCase(), at = low.indexOf(needle);
      if (at < 0) return;
      var span = document.createElement('mark');
      var mid = node.splitText(at);
      mid.splitText(needle.length);
      span.appendChild(mid.cloneNode(true));
      mid.replaceWith(span);
      block.dataset.marked = '1';
    });
  }

  var timer;
  q.addEventListener('input', function () {
    clearTimeout(timer);
    timer = setTimeout(function () {
      clearMarks();
      var needle = q.value.trim().toLowerCase().replace(/\\s+/g, ' ');
      if (needle.length < 2) { setOut(''); return; }
      var hits = [];
      texts.forEach(function (t, i) { if (t.indexOf(needle) >= 0) hits.push(i); });
      if (!hits.length) {
        setOut('No stanza contains <b>' + needle.replace(/[<&]/g, '') + '</b>.');
        return;
      }
      hits.forEach(function (i) { markIn(blocks[i], needle); });
      var label = hits.length === 1 ? 'Found in stanza (click to jump): ' : 'Found in ' + hits.length + ' stanzas (click to jump): ';
      setOut(label + hits.map(function (i) {
        var b = blocks[i];
        return '<a class="chip" href="#s' + b.dataset.n + '">' + b.dataset.n + '</a>';
      }).join(''));
    }, 140);
  });
})();
</script>
</body>
</html>
"""


def main():
    stanzas = json.loads(STANZAS_JSON.read_text(encoding="utf-8"))
    stanzas.sort(key=lambda s: s["stanza_number"])

    parts = []
    line_no = 0
    for s in stanzas:
        num = s["stanza_number"]
        lines = s["lines"]
        first = line_no + 1
        last = line_no + len(lines)

        items = []
        for offset, text in enumerate(lines):
            items.append(
                '        <li><span class="ln">%d</span><span>%s</span></li>'
                % (first + offset, html.escape(text))
            )
        line_no = last

        parts.append(
            '  <section class="stanza" id="s{n}" data-n="{n}" data-from="{f}" data-to="{t}">\n'
            '    <div class="shead">\n'
            '      <span class="snum">Stanza {n}</span>\n'
            '      <a href="{n}.html">explanation &rarr;</a>\n'
            "    </div>\n"
            '    <ol class="lines">\n{items}\n    </ol>\n'
            "  </section>".format(n=num, f=first, t=last, items="\n".join(items))
        )

    out = (
        TEMPLATE.replace("__STANZAS__", "\n".join(parts))
        .replace("__TOTAL__", str(len(stanzas)))
        .replace("__LINES__", str(line_no))
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(out, encoding="utf-8")
    print("Wrote %s (%d stanzas, %d lines, %.0f KB)"
          % (OUT, len(stanzas), line_no, OUT.stat().st_size / 1024))


if __name__ == "__main__":
    main()
