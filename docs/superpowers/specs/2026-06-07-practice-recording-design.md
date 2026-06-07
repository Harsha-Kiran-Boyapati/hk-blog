# Practice Page — Recording Feature Design

**Date:** 2026-06-07  
**File:** `docs/tools/carnatic/practice/index.html`

---

## Overview

Add session recording to the practice page. A collapsing right sidebar lists saved recordings. Each recording captures microphone audio (WebM blob) and pitch data (timestamped note detections). Recordings persist across sessions via IndexedDB. Playback replays the audio and re-drives the existing pitch canvas in sync.

---

## Layout

`#app` becomes a flex row:

- **`#main`** — existing flex column (controls bar + canvas), `flex: 1`, `min-width: 0`
- **`#sidebar`** — new right panel, `width: 280px` expanded / `width: 32px` collapsed, `transition: width 0.2s ease`

The canvas already fills available width via `flex: 1`, so it reflows automatically as the sidebar opens and closes. No layout logic needed beyond the CSS width transition.

Sidebar structure (top to bottom):
1. Header strip: "Recordings" label (hidden when collapsed) + toggle arrow button (`‹` / `›`)
2. Scrollable recording list

---

## Recording

**Controls bar addition:** A `Record` button in the right cluster, next to Visualizer.

**Start recording:**
- If the visualizer is not already running, start it automatically
- Call `MediaRecorder(micStream, { mimeType: 'audio/webm' })` on the existing mic stream (already open for YIN)
- Begin accumulating pitch points into a separate `recordingPoints[]` array — the live canvas `pitchPoints` 10-second window is unaffected
- Show a red ● dot and an elapsed timer (mm:ss) in the controls bar
- Record button label changes to "Stop"

**Stop recording:**
- `mediaRecorder.stop()` — collects all chunks into a single `Blob`
- Save to IndexedDB: audio blob + pitch data + metadata (see Storage)
- New entry appears at top of sidebar list
- Red dot and timer disappear; Record button resets

**Edge cases:**
- Stopping the Visualizer while recording also stops recording
- If mic permission is not yet granted, starting recording triggers `getUserMedia` (same as Visualizer start)
- If `audio/webm` is unsupported, fall back to `audio/ogg;codecs=opus`, then `audio/mp4`

---

## Playback

Clicking a recording in the sidebar:
1. Switches canvas to **playback mode** — live YIN detection pauses, mic stream keeps running in background
2. Creates a blob URL from the stored audio blob, sets it on a hidden `<audio>` element, calls `.play()`
3. Canvas rendering switches `elapsed` source from `Date.now() - startTime` to `audio.currentTime`
4. Pitch points come from the loaded recording's `pitchData` array instead of the live `pitchPoints` buffer
5. A playback bar at the bottom of the sidebar shows: recording name, `elapsed / total` time, play/pause button

**Stopping playback:**
- Clicking the sidebar's stop/close control, or audio reaching end → returns canvas to live mode
- Blob URL is revoked on cleanup

**No scrubbing in v1** — play/pause only.

---

## Sidebar Recording List

Each entry displays:
- **Name:** `"Mayamalavagowla · C3 · Jun 7 14:32"` (auto-generated, not editable in v1)
- **Duration:** e.g. `2:14`
- **Delete button:** visible on hover, removes entry from IndexedDB and list

Entries are sorted newest-first. List is populated on page load from IndexedDB (audio blobs loaded lazily on playback, not at startup).

---

## Storage

**IndexedDB** — database `carnatic-practice`, object store `recordings`, keyPath `id` (auto-increment).

Record schema:
```
{
  id:        number          — auto-increment primary key
  name:      string          — "Mayamalavagowla · C3 · Jun 7 14:32"
  createdAt: number          — Date.now() timestamp
  duration:  number          — seconds (float)
  raga:      string          — raga key e.g. "mayamalavagowla"
  sa:        string          — sa key e.g. "C3"
  audioBlob: Blob            — WebM audio
  pitchData: Array<{time: number, frequency: number, confidence: number}>
}
```

**On page load:** open IndexedDB, read all records (metadata only — blobs loaded lazily), render sidebar list.  
**On delete:** `indexedDB.delete(id)`, remove DOM entry, revoke any active blob URL for that id.

---

## Canvas Changes

The existing `renderCanvas()` reads from `state.pitchPoints`, `state.startTime`, and `Date.now()`. To support playback, two additions:

- `state.playbackMode: boolean` — when true, canvas reads from `state.playbackPoints` and `state.playbackAudio.currentTime` instead
- `state.playbackPoints: Array` — loaded from recording's `pitchData` on playback start
- `state.playbackAudio: HTMLAudioElement` — hidden element, blob URL set on playback

No other changes to the existing canvas rendering logic.

---

## What's Not In Scope (v1)

- Renaming recordings
- Exporting/downloading recordings
- Scrubbing (timeline seek)
- Recording the tanpura or beats audio (only mic is captured)
