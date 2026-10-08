#!/usr/bin/env python3
"""
Render stanza explanation pages from pipeline/explanations/<N>.json.

The JSON is the source of truth; these pages are only presentation. Poem text
always comes from stanzas.json: if a JSON file's quoted lines differ from it,
the page is not written.

Usage:
  render_pages.py --out DIR [STANZA ...]   render the given stanzas (default: every JSON present)

Writes only <N>.html files into DIR. It never touches index.html or
all-stanzas.html, and it does nothing unless --out is given, so it cannot
overwrite the live pages by accident.
"""

import argparse
import html
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TOTAL = 265

CSS = """
  :root { color-scheme: dark; }
  * { box-sizing: border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6; color: #eae4da; background: #17140f;
    max-width: 900px; margin: 0 auto; padding: 20px;
  }
  .container { background: #1f1b15; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,.45); }
  h1 { color: #e0a066; border-bottom: 3px solid #d2691e; padding-bottom: 10px; margin: 0 0 30px; }
  h2 { color: #d9a06a; margin: 40px 0 20px; border-left: 4px solid #d2691e; padding-left: 15px; }
  .navigation {
    display: flex; justify-content: space-between; align-items: center; gap: 10px;
    margin: 0 0 30px; padding: 20px; background: #2a231b; border-radius: 8px; border: 2px solid #d2691e;
  }
  .navigation:last-child { margin: 30px 0 0; }
  .nav-btn { padding: 10px 20px; text-decoration: none; background: #8b4513; color: #f5ede2;
             border-radius: 5px; font-weight: bold; transition: background-color .3s; }
  .nav-btn:hover { background: #a0522d; }
  .nav-btn.overview { background: #d2691e; }
  .nav-btn.disabled { background: #3a322a; color: #8a8175; cursor: not-allowed; }
  pre.stanza {
    background: #2a231b; padding: 20px; border-radius: 5px; border-left: 4px solid #d2691e;
    font-family: 'Monaco', 'Menlo', monospace; font-size: 16px; line-height: 1.8;
    white-space: pre-wrap; margin: 0;
  }
  ol.lines { list-style: none; margin: 0; padding: 0; }
  ol.lines li { padding: 14px 0; border-bottom: 1px solid #3a322a; }
  ol.lines li:last-child { border-bottom: 0; }
  .q { font-family: Georgia, 'Iowan Old Style', 'Times New Roman', serif; font-size: 1.05rem; color: #e0a066; }
  .m { margin-top: 4px; color: #e3dccf; font-weight: 400; }
  .why { margin-top: 8px; color: #b3a99a; font-size: .95rem; }
  .ex { margin-top: 8px; padding: 8px 12px; background: #241f18; border-left: 3px solid #6f9bc4; color: #b3a99a; font-size: .95rem; }
  .ex span { color: #8fb4d9; font-weight: 700; margin-right: 6px; font-size: .85em; text-transform: uppercase; letter-spacing: .04em; }
  p.summary { margin: 0; }
  @media (max-width: 600px) {
    .container { padding: 20px; }
    .navigation { flex-wrap: wrap; justify-content: center; }
  }
"""


def nav(n):
    prev = ('<a href="%d.html" class="nav-btn prev">← Stanza %d</a>' % (n - 1, n - 1)
            if n > 1 else '<span class="nav-btn disabled">← Previous</span>')
    nxt = ('<a href="%d.html" class="nav-btn next">Stanza %d →</a>' % (n + 1, n + 1)
           if n < TOTAL else '<span class="nav-btn disabled">Next →</span>')
    return '<div class="navigation">%s<a href="index.html" class="nav-btn overview">\U0001F4DA Overview</a>%s</div>' % (prev, nxt)


def validate(data, poem_lines):
    """Return a list of problems; empty means the file is acceptable to render."""
    errs = []
    n = data.get("stanza")
    lines = data.get("lines")
    if not isinstance(lines, list) or len(lines) != 7:
        return ["stanza %s: needs exactly 7 lines, found %s" % (n, len(lines) if isinstance(lines, list) else lines)]
    for i, row in enumerate(lines):
        if row.get("n") != i + 1:
            errs.append("line %d: wrong number %r" % (i + 1, row.get("n")))
        if row.get("text") != poem_lines[i]:
            errs.append("line %d: quoted text differs from stanzas.json" % (i + 1))
        if not str(row.get("meaning", "")).strip():
            errs.append("line %d: empty meaning" % (i + 1))
        for opt in ("why", "example"):
            if opt in row and not str(row[opt]).strip():
                errs.append("line %d: %s is present but empty (leave it out instead)" % (i + 1, opt))
    if not str(data.get("summary", "")).strip():
        errs.append("empty summary")
    return errs


def render(n, data, poem_lines):
    def row(i):
        r = data["lines"][i]
        parts = ['<div class="q">%s</div>' % html.escape(poem_lines[i]),
                 '<div class="m">%s</div>' % html.escape(r["meaning"].strip())]
        if r.get("why"):
            parts.append('<div class="why">%s</div>' % html.escape(r["why"].strip()))
        if r.get("example"):
            parts.append('<div class="ex"><span>Example</span> %s</div>' % html.escape(r["example"].strip()))
        return "      <li>%s</li>" % "".join(parts)

    rows = "\n".join(row(i) for i in range(7))
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Stanza %(n)d - The Rape of Lucrece Analysis</title>
<style>%(css)s</style>
</head>
<body>
  <div class="container">
    %(nav)s
    <h1>Stanza %(n)d - Explanation</h1>
    <h2>Original Stanza</h2>
    <pre class="stanza">%(poem)s</pre>
    <h2>Line by Line</h2>
    <ol class="lines">
%(rows)s
    </ol>
    <h2>Overall Meaning</h2>
    <p class="summary">%(summary)s</p>
    %(nav)s
  </div>
</body>
</html>
""" % {"n": n, "css": CSS, "nav": nav(n), "poem": html.escape("\n".join(poem_lines)),
       "rows": rows, "summary": html.escape(data["summary"].strip())}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, help="directory to write <N>.html into")
    ap.add_argument("stanzas", nargs="*", type=int)
    args = ap.parse_args()

    poem = {s["stanza_number"]: s["lines"] for s in json.loads((ROOT / "stanzas.json").read_text(encoding="utf-8"))}
    src = HERE / "explanations"
    wanted = args.stanzas or sorted(int(p.stem) for p in src.glob("*.json"))
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    bad = 0
    for n in wanted:
        path = src / ("%d.json" % n)
        if not path.exists():
            print("stanza %d: no JSON file, skipped" % n)
            bad += 1
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        errs = validate(data, poem[n])
        if errs or data.get("stanza") != n:
            print("stanza %d NOT rendered:" % n, errs or ["stanza number inside file does not match"])
            bad += 1
            continue
        (out / ("%d.html" % n)).write_text(render(n, data, poem[n]), encoding="utf-8")
        print("stanza %d -> %s" % (n, out / ("%d.html" % n)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
