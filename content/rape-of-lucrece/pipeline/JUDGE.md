# Judge checklist

How a stanza's explanation is checked. Two parts. Part A is a script, instant and
free. Part B is done by an independent agent that did not write the draft.

**Inputs for part B:** the stanza's JSON, its text and the 3 stanzas either side,
their LitCharts references, the full poem, and `STYLE.md`.

## A. Mechanical (script, no model)

Any failure here sends the draft straight back to the writer.

1. Seven lines, numbered 1 to 7. Each `text` is identical to `stanzas.json`. Every
   `meaning` is non-empty. A `why` or `example` is either absent or non-empty.
2. Punctuation in `meaning`, `why`, `example` and the overall meaning is only
   . , - ? ! plus quotation marks and brackets. No ; : or long dashes.
3. No hedging: probably, perhaps, likely, may mean, might, could be, could mean,
   either way, seems, appears, possibly.
4. No device labels: metaphor, simile, alliteration, personification, antithesis,
   anaphora, oxymoron, hyperbole, irony.
5. No "This line", "Here,", "Okay" openings. No "next stanza" or "previous stanza".
   No "lists", "asks" or similar labels at the start of the overall meaning, and no
   brackets in it.
6. **Flags for a human look, not failures:** an entry several times longer than
   its neighbours. Words in the overall meaning that appear nowhere in the line
   entries (a quick test for the overall adding something).

## B. Judged

Each defect is reported with the stanza, the line (or "overall"), the field, the
exact words quoted, which check it breaks, and a suggested fix. There is no score.
Only real defects are listed. Do not pad the list, and do not invent a defect to
look thorough.

1. **Faithful.** Before looking at the draft, write your own gloss of each line
   from the text and the references. Then compare. Report a meaning that differs
   from yours or from LitCharts. LitCharts is a reference and can be loose or
   wrong, so a disagreement is a defect only if the writer cannot point to
   something in the text that justifies it.
2. **Stays inside the stanza.** Every claim in a `meaning`, `why`, `example` or
   the overall meaning must be in the stanza, in its neighbours, or in the poem's
   plot as needed to say who or what a line is about. Report any added reason,
   effect, moral or idea. Examples that must be caught: "and it is Time that lets
   one generation follow another" (added to 137 line 1), "it promises happiness
   and leaves regret" (added to 133 line 3), "the tiger is Tarquin" (not in the
   text).
3. **A `why` earns its place.** Report a `why` that restates the `meaning`, repeats
   a gloss already given in the `meaning`, only describes structure the reader can
   already see (who is addressed, which night, that a list continues), or only
   adds a general moral. Report a `why` that exists only to define one word, which
   belongs in the `meaning` in brackets. But do not report a `why` for a word whose
   original brings an image its synonym loses ("date" as a prison sentence).
4. **An `example` earns its place.** Report an example that restates the `why`, is
   as abstract as the line, illustrates something already obvious, or does not
   really fit the line. If it explains why a line is so, it is a `why`, not an
   example.
5. **Nothing missing.** Report a line that a reader meeting it cold could not follow
   and that has no `why`: compressed or inverted word order, an old or unusual
   word sense, figurative language not made plain, a reference to myth or custom, a
   play on words, a pronoun or address left unresolved. Report a loaded word whose
   sense in this line is never stated, such as "false" in "false slave to false
   delight".
6. **Cold-reader test.** Give a fresh agent only one line and its entry. It must say
   what the line means and why. If it cannot, report the entry. Run this on every
   line that has a `why`, and on a sample of the plain ones.
7. **Meaning.** Plain modern English, usually one sentence. Archaic words glossed
   in brackets. References resolved. Figurative language stated as what it stands
   for. The single best reading, with no hedging.
8. **Overall meaning.** Connected modern prose for the whole stanza, in order, in the
   speaker's voice ("you", "I" or third person to match). Sentences that the poem
   splits across lines are joined. "To..." lists open with the main clause they
   need. Every clause comes from the line entries. No commentary labels.

**Verdict:** `pass` when there are no defects, otherwise `fail` with the list.

## Output format

```json
{ "verdict": "fail",
  "defects": [
    { "line": 1, "field": "why", "quote": "and it is Time that lets one generation follow another",
      "check": "stays-inside-the-stanza", "fix": "Delete the clause." } ] }
```

## Calibration, done before the judge is trusted

Run the judge on cases whose answer is known. If it misses a bad one or fails a
good one, fix the judge first.

- **Must fail:** the old 137 explanation (the tiger as Tarquin and the stanza read
  as about the rape), the old 137 line 1 ("beldam" read as a hag), the old 137
  summary ("all-powerful"), a draft with "and it is Time that lets one generation
  follow another", the old 133 line 3 `why` with "hurries a person's pleasures
  along", the old 138 line 2 `why` that only restates the meaning, and an entry
  for "To mock the subtle in themselves beguiled" with no `why`.
- **Must pass:** the stanzas of the pilot (131 to 140) once they have been
  approved.
