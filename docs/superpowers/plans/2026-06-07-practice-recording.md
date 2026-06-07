# Practice Page — Recording Feature Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a collapsing right sidebar with session recording to the practice page — captures mic audio + pitch data, persists in IndexedDB, replays audio in sync with the pitch canvas.

**Architecture:** All changes are in `docs/tools/carnatic/practice/index.html` (single self-contained file, no build system). `#app` becomes a flex row — `#main` holds the existing controls + canvas, `#sidebar` is the new collapsing panel. IndexedDB stores each recording as a blob + pitch data array. Playback mode swaps the canvas's time/data source without changing the rendering logic.

**Tech Stack:** Vanilla JS, Web Audio API (already used), MediaRecorder API, IndexedDB API, CSS flex transitions.

---

### Task 1: Restructure layout — wrap existing content in `#main`, add `#sidebar`

**Files:**
- Modify: `docs/tools/carnatic/practice/index.html`

The current `#app` is `flex-direction: column` with a full-bleed canvas trick (`width: 100vw`). We need `#app` as a flex row, with `#main` as the column child. Remove the full-bleed trick — the canvas fills its container naturally in the new layout.

- [ ] **Step 1: Replace `#app` CSS, add `#main` and `#sidebar` CSS**

Find the existing `#app` and `#canvas-wrap` rules and replace them, then add new rules. The complete CSS block to find and replace:

Find:
```css
    #app {
      display: flex;
      flex-direction: column;
      height: 100vh;
      max-width: 1600px;
      margin: 0 auto;
      padding: 16px 24px 0;
    }
```

Replace with:
```css
    #app {
      display: flex;
      flex-direction: row;
      height: 100vh;
      width: 100%;
    }

    #main {
      flex: 1;
      min-width: 0;
      display: flex;
      flex-direction: column;
      padding: 16px 24px 0;
      max-width: 1600px;
      margin: 0 auto;
      width: 100%;
    }

    #sidebar {
      width: 280px;
      flex-shrink: 0;
      background: #0e0e0e;
      border-left: 1px solid #1c1c1c;
      display: flex;
      flex-direction: row;
      transition: width 0.2s ease;
      overflow: hidden;
    }
    #sidebar.collapsed { width: 32px; }

    #sidebar-toggle {
      width: 32px;
      flex-shrink: 0;
      background: none;
      border: none;
      border-right: 1px solid #1c1c1c;
      color: #555;
      cursor: pointer;
      font-size: 1rem;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 0;
      align-self: stretch;
    }
    #sidebar-toggle:hover { color: #999; background: #111; }

    #sidebar-inner {
      flex: 1;
      min-width: 0;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }
    .sidebar-head {
      padding: 14px 12px 10px;
      font-size: 0.72rem;
      font-weight: 600;
      color: #666;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      border-bottom: 1px solid #1c1c1c;
      flex-shrink: 0;
    }
    #rec-list {
      flex: 1;
      overflow-y: auto;
      padding: 4px 0;
    }
    #rec-list::-webkit-scrollbar { width: 4px; }
    #rec-list::-webkit-scrollbar-thumb { background: #2a2a2a; border-radius: 2px; }

    .rec-item {
      padding: 10px 12px;
      border-bottom: 1px solid #141414;
      cursor: pointer;
    }
    .rec-item:hover { background: #141414; }
    .rec-item.active { background: #0d1a2e; }

    .rec-name {
      font-size: 0.78rem;
      color: #ccc;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      display: block;
      margin-bottom: 4px;
    }
    .rec-meta-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
    }
    .rec-duration { font-size: 0.72rem; color: #555; }
    .rec-delete {
      background: none; border: none; color: #444; cursor: pointer;
      font-size: 0.8rem; padding: 2px 4px; border-radius: 3px;
    }
    .rec-delete:hover { color: #f44336; background: rgba(244,67,54,0.08); }

    .rec-playbar {
      display: none;
      align-items: center;
      gap: 8px;
      margin-top: 6px;
    }
    .rec-item.active .rec-playbar { display: flex; }
    .rec-playbtn {
      background: none; border: 1px solid #333; color: #aaa;
      width: 26px; height: 26px; border-radius: 50%;
      cursor: pointer; font-size: 0.7rem; flex-shrink: 0;
      display: flex; align-items: center; justify-content: center;
    }
    .rec-playbtn:hover { border-color: #555; color: #fff; }
    .rec-timestr { font-size: 0.7rem; color: #555; }

    .rec-empty {
      padding: 24px 12px;
      color: #444;
      font-size: 0.78rem;
      text-align: center;
      line-height: 1.6;
    }
```

Also find and replace the `#canvas-wrap` rule:

Find:
```css
    #canvas-wrap {
      flex: 1;
      min-height: 0;
      width: 100vw;
      margin-left: calc(-50vw + 50%);
    }
```

Replace with:
```css
    #canvas-wrap {
      flex: 1;
      min-height: 0;
    }
```

- [ ] **Step 2: Update HTML structure**

Find the existing `<div id="app">` opening and the closing `</div>` before `<script>`. Wrap the existing content:

Find:
```html
  <div id="app">
    <div id="controls">
```

Replace with:
```html
  <div id="app">
    <div id="main">
    <div id="controls">
```

Find:
```html
    <div id="canvas-wrap">
      <canvas id="pitch-canvas"></canvas>
    </div>
  </div>
```

Replace with:
```html
    <div id="canvas-wrap">
      <canvas id="pitch-canvas"></canvas>
    </div>
    </div><!-- /#main -->

    <div id="sidebar" class="collapsed">
      <button id="sidebar-toggle" title="Recordings">›</button>
      <div id="sidebar-inner">
        <div class="sidebar-head">Recordings</div>
        <div id="rec-list">
          <p class="rec-empty">No recordings yet.<br>Hit Record to start.</p>
        </div>
      </div>
    </div>
  </div>
```

- [ ] **Step 3: Wire the toggle button in JS**

Add this at the end of the IIFE (before the closing `})();`):

```javascript
    // --- Sidebar toggle ---
    var sidebarEl = document.getElementById('sidebar');
    document.getElementById('sidebar-toggle').addEventListener('click', function () {
      var collapsed = sidebarEl.classList.toggle('collapsed');
      this.textContent = collapsed ? '›' : '‹';
    });
```

- [ ] **Step 4: Verify in browser**

Open `http://localhost:8765/tools/carnatic/practice/` (or just open the file). Confirm:
- Page renders with the canvas taking most of the width
- A thin strip is visible on the right with a `›` arrow
- Clicking `›` opens the sidebar to 280px with "Recordings" header
- Clicking `‹` collapses it back
- The canvas resizes smoothly during transition

- [ ] **Step 5: Commit**

```bash
git add docs/tools/carnatic/practice/index.html
git commit -m "Add collapsing recordings sidebar layout"
```

---

### Task 2: IndexedDB helpers

**Files:**
- Modify: `docs/tools/carnatic/practice/index.html`

Add four IndexedDB functions and initialize the DB on page load. All DB operations return Promises so they compose naturally with async/await.

- [ ] **Step 1: Add IndexedDB helpers to the JS**

Add this block inside the IIFE, after the `const SA_FREQUENCIES` declaration and before `const LIVE_WINDOW_SECS`:

```javascript
    // --- IndexedDB ---
    var db = null;

    function openDB() {
      return new Promise(function (resolve, reject) {
        var req = indexedDB.open('carnatic-practice', 1);
        req.onupgradeneeded = function (e) {
          var d = e.target.result;
          if (!d.objectStoreNames.contains('recordings')) {
            d.createObjectStore('recordings', { keyPath: 'id', autoIncrement: true });
          }
        };
        req.onsuccess = function (e) { resolve(e.target.result); };
        req.onerror   = function (e) { reject(e.target.error); };
      });
    }

    function dbSave(record) {
      // record: { name, createdAt, duration, raga, sa, audioBlob, pitchData }
      // Returns Promise<id>
      return new Promise(function (resolve, reject) {
        var tx   = db.transaction('recordings', 'readwrite');
        var store = tx.objectStore('recordings');
        var req  = store.add(record);
        req.onsuccess = function (e) { resolve(e.target.result); };
        req.onerror   = function (e) { reject(e.target.error); };
      });
    }

    function dbGetAll() {
      // Returns Promise<Array> — all records including blobs
      return new Promise(function (resolve, reject) {
        var tx   = db.transaction('recordings', 'readonly');
        var store = tx.objectStore('recordings');
        var req  = store.getAll();
        req.onsuccess = function (e) { resolve(e.target.result); };
        req.onerror   = function (e) { reject(e.target.error); };
      });
    }

    function dbDelete(id) {
      return new Promise(function (resolve, reject) {
        var tx   = db.transaction('recordings', 'readwrite');
        var store = tx.objectStore('recordings');
        var req  = store.delete(id);
        req.onsuccess = function () { resolve(); };
        req.onerror   = function (e) { reject(e.target.error); };
      });
    }
```

- [ ] **Step 2: Open the DB on init**

At the very bottom of the IIFE (after the sidebar toggle block, before `})();`):

```javascript
    // --- Init: open IndexedDB ---
    openDB().then(function (d) {
      db = d;
      return dbGetAll();
    }).then(function (recs) {
      renderRecList(recs);
    }).catch(function (err) {
      console.warn('IndexedDB unavailable:', err);
    });
```

- [ ] **Step 3: Add stub for `renderRecList` so init doesn't throw**

Add this stub right after the DB helpers (you'll flesh it out in Task 4):

```javascript
    function renderRecList(recs) {
      // stubbed — implemented in Task 4
      console.log('recordings loaded:', recs.length);
    }
```

- [ ] **Step 4: Verify in browser**

Open DevTools → Application → IndexedDB. Reload the page. Confirm `carnatic-practice` database exists with a `recordings` object store. Console should log `recordings loaded: 0`.

- [ ] **Step 5: Commit**

```bash
git add docs/tools/carnatic/practice/index.html
git commit -m "Add IndexedDB helpers for recordings persistence"
```

---

### Task 3: Record button + MediaRecorder

**Files:**
- Modify: `docs/tools/carnatic/practice/index.html`

Add a Record button to the controls bar. Clicking it starts `MediaRecorder` on the existing mic stream (starting the visualizer first if needed), accumulates pitch points into a separate array, and saves to IndexedDB on stop.

- [ ] **Step 1: Add Record button and rec-dot HTML to the controls bar**

Find the right cluster in the controls HTML:

```html
        <div class="field">
          <span class="lbl">Visualizer</span>
          <button id="toggle-btn" class="btn accent">Start</button>
        </div>
        <div class="vdiv"></div>
```

Replace with:

```html
        <div class="field">
          <span class="lbl">Visualizer</span>
          <button id="toggle-btn" class="btn accent">Start</button>
        </div>
        <div class="vdiv"></div>
        <div class="field">
          <span class="lbl">Record</span>
          <div class="field-row">
            <span id="rec-dot" style="display:none;color:#f44336;font-size:1.1rem;line-height:1;">●</span>
            <span id="rec-timer" style="display:none;font-size:0.82rem;color:#aaa;min-width:32px;"></span>
            <button id="rec-btn" class="btn">Start</button>
          </div>
        </div>
        <div class="vdiv"></div>
```

- [ ] **Step 2: Add recording state and helper**

Add after the `const LIVE_WINDOW_SECS` line:

```javascript
    var recState = {
      isRecording:   false,
      mediaRecorder: null,
      chunks:        [],
      startTime:     0,
      points:        [],        // pitch points timestamped from recording start
      timerInterval: null,
    };
```

Add this helper after `formatDuration`:

```javascript
    function formatRecName() {
      var raga = RAGAS[ragaSelect.value].name;
      var sa   = saSelect.value;
      var d    = new Date();
      var mon  = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][d.getMonth()];
      var hh   = String(d.getHours()).padStart(2, '0');
      var mm   = String(d.getMinutes()).padStart(2, '0');
      return raga + ' · ' + sa + ' · ' + mon + ' ' + d.getDate() + ' ' + hh + ':' + mm;
    }
```

- [ ] **Step 3: Add `startRecording`, `stopRecording`, `doStartRecording` functions**

Add after `stopLive`:

```javascript
    var recDotEl   = document.getElementById('rec-dot');
    var recTimerEl = document.getElementById('rec-timer');
    var recBtn     = document.getElementById('rec-btn');

    async function startRecording() {
      if (!state.isLive) await startLive();
      if (!state.stream) return;          // mic denied
      recState.chunks  = [];
      recState.points  = [];
      recState.startTime = Date.now();

      var mimeType = ['audio/webm', 'audio/ogg;codecs=opus', 'audio/mp4']
        .find(function (t) { return MediaRecorder.isTypeSupported(t); }) || '';
      recState.mediaRecorder = new MediaRecorder(
        state.stream,
        mimeType ? { mimeType: mimeType } : {}
      );
      recState.mediaRecorder.ondataavailable = function (e) {
        if (e.data.size > 0) recState.chunks.push(e.data);
      };
      recState.mediaRecorder.onstop = function () {
        var blob = new Blob(recState.chunks, { type: recState.mediaRecorder.mimeType });
        var dur  = (Date.now() - recState.startTime) / 1000;
        var rec  = {
          name:      formatRecName(),
          createdAt: Date.now(),
          duration:  dur,
          raga:      ragaSelect.value,
          sa:        saSelect.value,
          audioBlob: blob,
          pitchData: recState.points.slice(),
        };
        dbSave(rec).then(function (id) {
          rec.id = id;
          prependRecItem(rec);
        }).catch(function (err) {
          console.warn('Failed to save recording:', err);
        });
      };
      recState.mediaRecorder.start();
      recState.isRecording = true;

      recDotEl.style.display   = 'inline';
      recTimerEl.style.display = 'inline';
      recBtn.textContent       = 'Stop';
      recBtn.classList.add('on');

      recState.timerInterval = setInterval(function () {
        recTimerEl.textContent = formatDuration((Date.now() - recState.startTime) / 1000);
      }, 500);
    }

    function stopRecording() {
      if (!recState.isRecording) return;
      recState.isRecording = false;
      clearInterval(recState.timerInterval);
      recState.mediaRecorder.stop();

      recDotEl.style.display   = 'none';
      recTimerEl.style.display = 'none';
      recTimerEl.textContent   = '';
      recBtn.textContent       = 'Start';
      recBtn.classList.remove('on');
    }

    recBtn.addEventListener('click', function () {
      if (recState.isRecording) stopRecording(); else startRecording();
    });
```

- [ ] **Step 4: Intercept pitch points during recording**

In `onaudioprocess`, find:

```javascript
        if (result.frequency > 0 && result.confidence > 0.6) {
          state.pitchPoints.push({ time: elapsed, frequency: result.frequency, confidence: result.confidence });
          state.currentSwara = semitoneToSwaraIndex(freqToSemitone(result.frequency, state.saFreq));
```

Replace with:

```javascript
        if (result.frequency > 0 && result.confidence > 0.6) {
          state.pitchPoints.push({ time: elapsed, frequency: result.frequency, confidence: result.confidence });
          if (recState.isRecording) {
            recState.points.push({
              time:       (Date.now() - recState.startTime) / 1000,
              frequency:  result.frequency,
              confidence: result.confidence,
            });
          }
          state.currentSwara = semitoneToSwaraIndex(freqToSemitone(result.frequency, state.saFreq));
```

- [ ] **Step 5: Stop recording when visualizer is stopped**

In `stopLive`, add at the very top:

```javascript
    function stopLive() {
      if (recState.isRecording) stopRecording();
```

- [ ] **Step 6: Add stub for `prependRecItem` so save doesn't throw**

Add after `renderRecList`:

```javascript
    function prependRecItem(rec) {
      // stubbed — implemented in Task 4
      console.log('saved recording:', rec.id, rec.name, rec.duration.toFixed(1) + 's');
    }
```

- [ ] **Step 7: Verify in browser**

1. Open the page, click "Record" → Visualizer should start automatically, red dot and timer appear, Record button shows "Stop"
2. Hum for 5 seconds, click Stop
3. Open DevTools → Application → IndexedDB → carnatic-practice → recordings
4. Confirm one record exists with name, duration, audioBlob, pitchData array
5. Console should log `saved recording: 1 <name> 5.0s`

- [ ] **Step 8: Commit**

```bash
git add docs/tools/carnatic/practice/index.html
git commit -m "Add Record button and MediaRecorder audio capture"
```

---

### Task 4: Sidebar recording list + delete

**Files:**
- Modify: `docs/tools/carnatic/practice/index.html`

Replace the stubs from Tasks 2 and 3 with real implementations. Each sidebar entry shows name, duration, a playback bar (empty for now — wired in Task 5), and a delete button.

- [ ] **Step 1: Replace `renderRecList` stub with full implementation**

Find:
```javascript
    function renderRecList(recs) {
      // stubbed — implemented in Task 4
      console.log('recordings loaded:', recs.length);
    }
```

Replace with:

```javascript
    function renderRecList(recs) {
      var listEl = document.getElementById('rec-list');
      if (!recs || recs.length === 0) {
        listEl.innerHTML = '<p class="rec-empty">No recordings yet.<br>Hit Record to start.</p>';
        return;
      }
      // Sort newest-first
      var sorted = recs.slice().sort(function (a, b) { return b.createdAt - a.createdAt; });
      listEl.innerHTML = '';
      sorted.forEach(function (rec) { listEl.appendChild(makeRecEl(rec)); });
    }

    function makeRecEl(rec) {
      var el = document.createElement('div');
      el.className = 'rec-item';
      el.dataset.id = rec.id;
      el.innerHTML =
        '<span class="rec-name">' + rec.name + '</span>' +
        '<div class="rec-meta-row">' +
          '<span class="rec-duration">' + formatDuration(rec.duration) + '</span>' +
          '<button class="rec-delete" title="Delete">⌫</button>' +
        '</div>' +
        '<div class="rec-playbar">' +
          '<button class="rec-playbtn" data-state="stopped">▶</button>' +
          '<span class="rec-timestr">0:00 / ' + formatDuration(rec.duration) + '</span>' +
        '</div>';

      el.querySelector('.rec-delete').addEventListener('click', function (e) {
        e.stopPropagation();
        deleteRec(rec.id, el);
      });
      el.querySelector('.rec-playbtn').addEventListener('click', function (e) {
        e.stopPropagation();
        togglePlayback(rec, el);
      });
      el.addEventListener('click', function () {
        togglePlayback(rec, el);
      });
      return el;
    }

    function deleteRec(id, el) {
      dbDelete(id).then(function () {
        el.remove();
        var listEl = document.getElementById('rec-list');
        if (!listEl.querySelector('.rec-item')) {
          listEl.innerHTML = '<p class="rec-empty">No recordings yet.<br>Hit Record to start.</p>';
        }
      }).catch(function (err) {
        console.warn('Delete failed:', err);
      });
    }
```

- [ ] **Step 2: Replace `prependRecItem` stub**

Find:
```javascript
    function prependRecItem(rec) {
      // stubbed — implemented in Task 4
      console.log('saved recording:', rec.id, rec.name, rec.duration.toFixed(1) + 's');
    }
```

Replace with:

```javascript
    function prependRecItem(rec) {
      var listEl = document.getElementById('rec-list');
      var empty  = listEl.querySelector('.rec-empty');
      if (empty) empty.remove();
      listEl.insertBefore(makeRecEl(rec), listEl.firstChild);
    }
```

- [ ] **Step 3: Add stub for `togglePlayback` so clicks don't throw**

Add after `prependRecItem`:

```javascript
    function togglePlayback(rec, el) {
      // stubbed — implemented in Task 5
      console.log('play/stop', rec.id);
    }
```

- [ ] **Step 4: Verify in browser**

1. Reload the page. Previously saved recording should appear in the sidebar.
2. Record a short session and stop — new entry should appear at top of list.
3. Hover over an entry — delete button (⌫) appears.
4. Click delete — entry is removed. Reload to confirm it's gone from IndexedDB too.

- [ ] **Step 5: Commit**

```bash
git add docs/tools/carnatic/practice/index.html
git commit -m "Render recording list in sidebar with delete"
```

---

### Task 5: Playback mode — replay audio + pitch canvas

**Files:**
- Modify: `docs/tools/carnatic/practice/index.html`

Wire up playback. Clicking a recording item plays the audio and replays the pitch canvas using stored pitch points synced to `audio.currentTime`. Extend `state` with playback fields and refactor `renderCanvas` to read from either live or playback source.

- [ ] **Step 1: Add playback fields to `state`**

Find the `const state = {` block. Add four new fields at the end (before the closing `};`):

```javascript
      playbackMode:   false,
      playbackPoints: [],
      playbackRaga:   null,
      playbackSa:     null,
      playbackAudio:  null,
      playbackEl:     null,   // the currently-active sidebar item element
```

- [ ] **Step 2: Refactor `renderCanvas` to support playback source**

Inside `renderCanvas`, find the two lines that read the live time and points:

```javascript
      var elapsed        = (Date.now() - state.startTime) / 1000;
      var windowEnd      = elapsed;
```

And find the loop over pitch points:

```javascript
      for (var p = 0; p < state.pitchPoints.length; p++) {
        var point    = state.pitchPoints[p];
```

Replace the elapsed/windowEnd lines with:

```javascript
      var elapsed = state.playbackMode
        ? (state.playbackAudio ? state.playbackAudio.currentTime : 0)
        : (Date.now() - state.startTime) / 1000;
      var windowEnd      = elapsed;
```

Replace the pitch-points loop start with:

```javascript
      var pts = state.playbackMode ? state.playbackPoints : state.pitchPoints;
      for (var p = 0; p < pts.length; p++) {
        var point    = pts[p];
```

Also update `renderCanvas` to use the playback raga/sa when in playback mode. Find:

```javascript
      var raga   = state.raga;
      var saFreq = state.saFreq;
      if (!raga || !saFreq) return;
```

Replace with:

```javascript
      var raga   = state.playbackMode ? RAGAS[state.playbackRaga]   : state.raga;
      var saFreq = state.playbackMode ? SA_FREQUENCIES[state.playbackSa] : state.saFreq;
      if (!raga || !saFreq) return;
```

Also update the info text at the bottom of `renderCanvas` that reads `saSelect.value`:

Find:
```javascript
      ctx.fillText(raga.name + '  |  Sa = ' + saSelect.value, pL + 8, pT + 6);
```

Replace with:
```javascript
      var saLabel = state.playbackMode ? state.playbackSa : saSelect.value;
      ctx.fillText(raga.name + '  |  Sa = ' + saLabel, pL + 8, pT + 6);
```

- [ ] **Step 3: Add `startPlayback` and `stopPlayback` functions**

Add after `stopLive`:

```javascript
    function startPlayback(rec, el) {
      // Stop live detection while playing back
      if (state.isLive) {
        state.isLive = false;
        if (state.animFrame) { cancelAnimationFrame(state.animFrame); state.animFrame = null; }
        // Keep mic stream open — don't disconnect source/processor
      }
      // Stop any existing playback
      if (state.playbackMode) stopPlayback();

      // Set up audio
      var audio = new Audio();
      audio.src = URL.createObjectURL(rec.audioBlob);
      audio.play().catch(function (e) { console.warn('Audio play failed:', e); });

      state.playbackMode   = true;
      state.playbackPoints = rec.pitchData;
      state.playbackRaga   = rec.raga;
      state.playbackSa     = rec.sa;
      state.playbackAudio  = audio;
      state.playbackEl     = el;

      el.classList.add('active');
      var playBtn = el.querySelector('.rec-playbtn');
      playBtn.dataset.state = 'playing';
      playBtn.textContent   = '⏸';

      // Update time display while playing
      var timeStr = el.querySelector('.rec-timestr');
      var totalStr = formatDuration(rec.duration);
      var tickId = setInterval(function () {
        if (!state.playbackMode) { clearInterval(tickId); return; }
        timeStr.textContent = formatDuration(audio.currentTime) + ' / ' + totalStr;
      }, 250);

      audio.addEventListener('ended', function () {
        clearInterval(tickId);
        stopPlayback();
      });

      // Start canvas animation loop
      function pbAnimate() {
        if (!state.playbackMode) return;
        renderCanvas();
        state.animFrame = requestAnimationFrame(pbAnimate);
      }
      state.animFrame = requestAnimationFrame(pbAnimate);
    }

    function stopPlayback() {
      if (!state.playbackMode) return;
      if (state.animFrame) { cancelAnimationFrame(state.animFrame); state.animFrame = null; }

      if (state.playbackAudio) {
        URL.revokeObjectURL(state.playbackAudio.src);
        state.playbackAudio.pause();
        state.playbackAudio = null;
      }
      if (state.playbackEl) {
        state.playbackEl.classList.remove('active');
        var pb = state.playbackEl.querySelector('.rec-playbtn');
        if (pb) { pb.dataset.state = 'stopped'; pb.textContent = '▶'; }
        state.playbackEl = null;
      }

      state.playbackMode   = false;
      state.playbackPoints = [];
      state.playbackRaga   = null;
      state.playbackSa     = null;

      // Clear canvas
      var ctx = canvas.getContext('2d');
      var dpr = window.devicePixelRatio || 1;
      var rect = canvas.parentElement.getBoundingClientRect();
      canvas.width  = rect.width  * dpr;
      canvas.height = rect.height * dpr;
      ctx.fillStyle = '#0c0c0c';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
    }
```

- [ ] **Step 4: Replace `togglePlayback` stub**

Find:
```javascript
    function togglePlayback(rec, el) {
      // stubbed — implemented in Task 5
      console.log('play/stop', rec.id);
    }
```

Replace with:

```javascript
    function togglePlayback(rec, el) {
      if (state.playbackEl === el && state.playbackMode) {
        // Pause/resume
        var audio = state.playbackAudio;
        var btn   = el.querySelector('.rec-playbtn');
        if (audio.paused) {
          audio.play();
          btn.textContent = '⏸';
          btn.dataset.state = 'playing';
        } else {
          audio.pause();
          btn.textContent = '▶';
          btn.dataset.state = 'paused';
        }
      } else {
        startPlayback(rec, el);
      }
    }
```

- [ ] **Step 5: Stop playback when visualizer is started**

In `startLive`, find the line that sets `state.isLive = true;` and add before it:

```javascript
      if (state.playbackMode) stopPlayback();
```

- [ ] **Step 6: Verify in browser**

1. Record a ~10-second session singing a few svaras
2. Click the recording in the sidebar — it should expand, show the playbar, and start playing
3. The pitch canvas should replay the pitch dots scrolling in sync with the audio
4. Click ⏸ to pause — audio stops, canvas freezes at that point
5. Click ▶ to resume
6. Audio ends → canvas clears, sidebar item returns to normal state
7. Click another recording while one is playing — old one stops, new one starts

- [ ] **Step 7: Commit and push**

```bash
git add docs/tools/carnatic/practice/index.html
git commit -m "Add playback mode: audio + pitch canvas replay from recordings"
git push
```

---

## Self-Review

**Spec coverage:**
- ✅ Collapsing right sidebar with CSS width transition
- ✅ Record button in controls bar
- ✅ MediaRecorder on existing mic stream; auto-starts visualizer if not running
- ✅ Separate `recState.points` array — live canvas window unaffected
- ✅ Mime type fallback: webm → ogg → mp4
- ✅ IndexedDB: openDB, save, getAll, delete
- ✅ Schema: id, name, createdAt, duration, raga, sa, audioBlob, pitchData
- ✅ Sidebar list sorted newest-first, populated on load
- ✅ Delete with empty-state message
- ✅ Playback: blob URL → Audio element; canvas reads `audio.currentTime`
- ✅ Playback uses recording's raga/sa for canvas rendering
- ✅ Blob URL revoked on stop
- ✅ Stopping visualizer stops recording
- ✅ Starting visualizer stops playback
- ✅ Play/pause (no scrub, per spec)

**Placeholder scan:** No TBDs or vague steps — all code is shown in full.

**Type consistency:** `rec` object shape defined in Task 3 Step 3 and used consistently in Tasks 4 and 5. `state.playbackEl` set in `startPlayback`, cleared in `stopPlayback`, checked in `togglePlayback` — consistent. `formatDuration` used throughout — defined in the existing file.
