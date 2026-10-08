# Stanza explanation style guide

Every stanza gets **7 line entries and 1 summary**. Each line entry has a short
`meaning`, and, whenever the line is not obvious, a `why` and sometimes an `example`.
The aim is that a reader with no background can finish a line's entry and say what
the line means *and why the words mean that*. A bare paraphrase is not enough.

## Output (one JSON file per stanza: `explanations/<N>.json`)

```json
{
  "stanza": 137,
  "lines": [
    { "n": 1,
      "text": "<line copied exactly from stanzas.json>",
      "meaning": "<one short sentence, always present>",
      "why": "<optional: how the words give that meaning>",
      "example": "<optional: a concrete case that makes the idea click>" }
  ],
  "summary": "<2-4 sentences>"
}
```

`lines` has 7 entries, numbered 1-7, in order. `text` is copied character for
character from `stanzas.json`. `why` and `example` are left out when not needed;
they are never filled in just to fill the space. Pages are rendered from this
file; nothing is written to HTML or markdown by hand.

## What you are given

- the stanza, and the 3 stanzas before and after it, each with its LitCharts translation
- the full text of the poem, to check who is speaking and who is being addressed

LitCharts is a **reference for checking**, not a source to copy. It gives one
paragraph per stanza and does not say why a line means what it does; that is
exactly what this work adds. Agree with it unless the text gives a specific
reason not to, and never reuse its wording.

## Rules

1. **Plain modern English**, as to a friend reading Shakespeare for the first time.
2. **`meaning` says what the line means**, as the quick plain answer: usually one
   sentence. Not what it "shows" or "highlights". Do not open with "This line...".
   The depth belongs in `why`, not here.
3. **A `why` must earn its place.** Add one only when it gives the reader
   something they could not get from the line plus the `meaning`: how odd word
   order parses; an old or unusual sense of a word; what a figure of speech
   stands for; a reference to myth, history or custom; a play on words; who
   "thou" is. As long as it takes for a reader to follow, and no longer. **Cut it**
   if it restates the `meaning`, repeats a gloss the `meaning` already gives, or
   only adds a general moral ("nothing escapes Time"). **Cut it too** if it only
   describes structure the reader can already see: who is being addressed, which
   night it is, that a list continues. If a `why` would exist only to define one
   word or phrase, put the gloss in the `meaning` in brackets, after its modern
   equivalent, and drop the `why`. A `why` on a line that does not need one makes
   the page worse.
   **Explain loaded words.** An adjective or epithet that carries the line's point
   (like "false" in "false slave to false delight") needs its sense in this line
   stated, not just carried along in a paraphrase. A bracketed gloss is enough
   when the modern word is a true synonym. Keep a `why` when the original word
   brings an image the synonym loses (date: the length of a prison sentence or a
   lease, which is what makes "enchained" fit).
4. **An `example` must earn its place too.** Add one only when the idea is abstract
   or unfamiliar and a concrete case makes it click in a way the `why` does not:
   a modern everyday case, or a scene from the poem, usually a sentence or two.
   **Cut it** if it restates the `why`, is as abstract as the line itself, or
   illustrates something already obvious. An `example` is a concrete instance of
   the idea and it must really fit the line. If what you wrote explains why the
   line is so, it is a `why`, not an `example`.
5. **Plain lines stay plain.** A line that is already clear gets only a `meaning`.
   Most lines in a stanza should not need both a `why` and an `example`, and many
   will need neither.
6. **Gloss every archaic or unusual word**, with the meaning that fits here, not a
   dictionary list. Short glosses can sit in brackets inside the `meaning`.
7. **Figurative language: say what it stands for.** Do not name devices (no
   "metaphor", "alliteration", "personification").
8. **Give the single best interpretation, stated plainly.** Use the stanza, its
   neighbours and the poem's plot. No symbolism the passage does not need. Never
   hedge: no "probably", "perhaps", "may mean", "could be", "the likeliest
   reading", "either way". Where a line is disputed, pick the reading that best
   fits the text and say it as fact. It need not be certain, but it must be the
   best reading available. Do not state facts about history or word origins that
   you are not sure of.
9. **No filler.** No preamble, no sign-off, no "Here, Shakespeare...".
10. **Summary: the stanza's point, in as few words as it takes, often one
    sentence.** It must say something the seven entries do not already say by
    listing them: what the stanza is doing as a whole (a list of X, an accusation,
    a plea, a turn in the story). Never retell the lines in order or re-list their
    contents; the reader has just read them. Run longer only when the point comes
    from the whole and cannot be said briefly (an argument, a change of mood).
    No mention of the previous or next stanza, and no "sets up", "leads into" or
    "goes on". Nothing the seven entries do not support.
11. **Punctuation:** use only . , - ? ! in your own sentences. No semicolons,
    colons or long dashes. Quotation marks around quoted words and brackets for
    glosses are allowed. Where a poem line ends in ; or :, end the `meaning` in a
    comma or full stop.
12. **Names:** Lucrece, Tarquin, Collatine, Collatium, Ardea, Brutus. Keep the
    poem's own names for Time, Night, Opportunity.

## Length

There are no word limits. Length follows need: a plain line gets a short entry, a
dense line gets a longer one. The guard against padding is not a count but the
question "does this sentence tell the reader something new?". The checker flags an
entry that is unusually long (several times the length of its neighbours) for a
human look, but that is a flag, not a failure.

## The test

After reading only a line and its entry, could a reader who has never met the
line say what it means and why? If they would still be puzzled by how the words
produce the meaning, the entry needs a `why` (or a better one). Then ask the
opposite question of every `why` and `example` that is there: if it were deleted,
would the reader lose anything? If not, delete it.

## Example (stanza 137, line 5)

> **To mock the subtle in themselves beguiled,**
> *Meaning:* Time makes fools of clever people by letting them be tricked by their own scheming.
> *Why:* "Subtle" is used here as a noun for crafty, scheming people. "Beguiled" means deceived, and "in themselves" means by their own doing, so these are people who have fooled themselves. "Mock" is what Time does to them: it exposes them as dupes of their own cunning.
> *Example:* A con man so taken with his own lies that they end up ruining him.
