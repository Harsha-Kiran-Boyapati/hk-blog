#!/usr/bin/env python3
"""
Split lit-charts.txt into one reference file per stanza.

The source interleaves the poem (with line numbers every fifth line) and a
plain-English translation paragraph after each stanza. Every chunk is aligned
to stanzas.json by comparing the poem text, so a bad split is reported rather
than silently written.

Output: pipeline/reference/litcharts/<N>.txt  (gitignored; copyrighted text,
used only as a reference for checking our own wording).
"""

import difflib
import json
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SRC = ROOT / "lit-charts.txt"
STANZAS = ROOT / "stanzas.json"
OUT = HERE / "reference" / "litcharts"

# A poem block scores ~0.8-1.0 against its stanza (the two sources differ in
# punctuation and a few spellings); a translation paragraph scores far lower.
MATCH = 0.6


def norm(s):
    """Compare poem text ignoring quote style, case, accents and spacing."""
    s = unicodedata.normalize("NFKD", s)
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = re.sub(r"[^a-z0-9]+", " ", s.lower())
    return s.strip()


def word_diff(ours_lines, theirs_lines):
    """Word-level differences, each with a little context, as (ours, theirs) strings."""
    a = " ".join(ours_lines).split()
    b = " ".join(theirs_lines).split()
    na = [norm(w) for w in a]
    nb = [norm(w) for w in b]
    out = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, na, nb, autojunk=False).get_opcodes():
        if tag == "equal":
            continue
        if tag == "replace" and (i2 - i1) == (j2 - j1) and all(
                difflib.SequenceMatcher(None, x, y).ratio() >= 0.7 for x, y in zip(na[i1:i2], nb[j1:j2])):
            continue  # same words spelled differently (call'd / called)
        lo, hi = max(i1 - 3, 0), min(i2 + 3, len(a))
        blo, bhi = max(j1 - 3, 0), min(j2 + 3, len(b))
        out.append((" ".join(a[lo:hi]), " ".join(b[blo:bhi])))
    return out


def similarity(a_lines, b_lines):
    # autojunk=False: the default heuristic discards common characters in long
    # strings and badly under-scores stanza-sized text
    return difflib.SequenceMatcher(None, " ".join(norm(l) for l in a_lines),
                                   " ".join(norm(l) for l in b_lines), autojunk=False).ratio()


def main():
    stanzas = {s["stanza_number"]: s["lines"] for s in json.loads(STANZAS.read_text(encoding="utf-8"))}
    raw = SRC.read_text(encoding="utf-8").split("\n")

    # drop pure line-number lines and the stray prompt left at the end of the file
    lines = [l for l in raw if not re.fullmatch(r"\s*\d+\s*", l)]
    blocks, cur = [], []
    for l in lines:
        if l.strip():
            cur.append(l.strip())
        elif cur:
            blocks.append(cur)
            cur = []
    if cur:
        blocks.append(cur)
    if blocks and blocks[-1] == ["Convert this to a well formatted pdf"]:
        blocks.pop()

    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.txt"):
        old.unlink()
    diffs, problems, bi = [], [], 0
    for n in range(1, 266):
        # the poem block is the first upcoming block that closely matches stanza n
        # (similarity, not equality: the two sources differ in a few words)
        found, best = None, MATCH
        for j in range(bi, min(bi + 4, len(blocks))):
            sc = similarity(blocks[j], stanzas[n])
            if sc >= best:
                found, best = j, sc
        if found is None:
            problems.append((n, "no matching poem block near block %d" % bi))
            break
        if found != bi:
            problems.append((n, "skipped %d unexpected block(s) before the poem" % (found - bi)))
        ratio = similarity(blocks[found], stanzas[n])
        wd = word_diff(stanzas[n], blocks[found])
        if wd:  # only real word differences, not punctuation or spelling variants
            diffs.append((n, ratio, wd))
        bi = found + 1
        # translation: blocks up to the next stanza's poem block
        trans = []
        while bi < len(blocks):
            if n < 265 and similarity(blocks[bi], stanzas[n + 1]) >= MATCH:
                break
            trans.append(" ".join(blocks[bi]))
            bi += 1
        if not trans:
            problems.append((n, "no translation found"))
        (OUT / ("%d.txt" % n)).write_text("\n\n".join(trans) + "\n", encoding="utf-8")

    print("stanzas written:", len(list(OUT.glob("*.txt"))))
    print("problems:", problems or "none")
    print("stanzas whose poem text differs between the two sources:", len(diffs))
    report = ["Differences between stanzas.json (ours) and the poem text inside lit-charts.txt", ""]
    for n, ratio, pairs in diffs:
        report.append("stanza %d (similarity %.3f)" % (n, ratio))
        for ours, theirs in pairs:
            report.append("  ours  : " + ours)
            report.append("  theirs: " + theirs)
        report.append("")
    (HERE / "reference" / "poem_text_differences.txt").write_text("\n".join(report), encoding="utf-8")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
