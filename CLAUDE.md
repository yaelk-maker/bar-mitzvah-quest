# Bar Mitzvah Quest - Claude Development Guide

## Project Overview
Gamified Bar Mitzvah identity quest PWA for Guy (12.5, Bar Mitzvah July 19, 2026). RPG-style 10-step journey building toward "Hero Book" displayed at the event. Guy has cerebral palsy and autism; his twin sister is Mika.

## Tech Stack
- **Vanilla HTML/CSS/JS** — no frameworks, no build step
- **PWA** with manifest.json; state persisted to Firebase Realtime Database (source of truth) + localStorage cache; family passcode `1907`
- **Hosted**: https://yaelk-maker.github.io/bar-mitzvah-quest/ (GitHub Pages, `master` branch)
- **Repo**: https://github.com/yaelk-maker/bar-mitzvah-quest (public)
- **Fonts**: Heebo (Hebrew body) + Bungee / Frank Ruhl Libre / Baloo 2 (display) from Google Fonts
- **Cache busting**: JS files use timestamp query params (auto-generated in index.html). `style.css` uses a manual `?v=...` tag — **bump it on every deploy that changes CSS** (currently `?v=20260701review`)
- **Design**: bright "floating islands in the sky" theme (see Design System). UI iterated via claude.ai/design exports + manual integration; design work happens on a `design` branch then merges to `master`.

## File Structure
```
bar-mitzvah-quest/
├── index.html          # Main HTML: home map, quest, hero book (3 screens)
├── family.html         # READ-ONLY family progress view (+ family.js, family.css) — mobile-first,
│                       #   live Firebase subscription, same passcode; never writes state

├── app.js              # State, navigation, quest rendering, map, validation
├── quests.js           # Quest data (10 quests) + MAP_POSITIONS
├── firebase-sync.js    # Firebase cloud sync, family passcode, cross-device reset
├── style.css           # Bright "floating islands" theme (active). Built as a base
│                       #   layer + override layer; bump ?v= tag in index.html on CSS deploys
├── map-v3.jpg          # ACTIVE map background — floating islands (names/scenes baked in)
├── cloud.svg           # Decorative drifting sky clouds
├── map-bg.png          # LEGACY lava map background (no longer used)
├── manifest.json, icon-192.png, icon-512.png  # PWA files
├── photos/             # Family/stage photos + video
│   ├── family-tree-bg.png            # Illustrated family tree template
│   ├── placeholder_parents_young.jpg # Quest 3
│   ├── placeholder_neta_baby.jpg     # Quest 3
│   ├── placeholder_nicu_twins.jpg    # Quest 3
│   ├── placeholder_ultrasound.jpg    # Quest 3
│   ├── placeholder_twins_babies.jpeg # Quest 6
│   ├── placeholder_twins_kids.jpeg   # Quest 6
│   ├── placeholder_twins_teens.jpeg  # Quest 6
│   ├── guy_soccer_video.mp4          # Quest 7 (autoplay loop)
│   ├── Guy - final step.jpeg         # Quest 10 (Bar Mitzvah card photo)
│   ├── Videos - step 9/              # Quest 9 greeting videos (11, Hebrew filenames; app.js prefixes photos/)
│   ├── qr/                           # Pre-generated QR PNGs per greeting video (Hero Book quest-9 chapter)
│   └── [11 Hebrew-named family photos]
├── brainrot/           # SAB voxel character PNGs (7 figures, 120px each)
├── CLAUDE.md, README.md, STITCH_PROMPT.md
```

## Architecture

### State Management
- Key: `bar-mitzvah-quest` in localStorage (fast local cache)
- Shape: `{ completedQuests: number[], responses: { [questId]: { [key]: value } }, currentQuest: number | null, resetAt: number }`
- Functions: `loadState()` / `saveState()`
- Reset: prefer `resetAllProgress()` (see Cloud Sync below) so all devices wipe. Local-only fallback: `localStorage.removeItem('bar-mitzvah-quest')` in console.

### Cloud Sync (firebase-sync.js)
- **Firebase Realtime Database** is the source of truth; localStorage is the local cache.
- DB ref: `quest-progress`. Config + `databaseURL` live in `firebase-sync.js`.
- **Family passcode**: `1907` — passcode overlay (`showPasscodeScreen()`) gates entry on load; once entered, `sessionStorage['quest-passcode-ok']` skips it for the session.
- **Merge**: `mergeStates(local, cloud)` unions `completedQuests`, deep-merges `responses` (local wins per-key), keeps the latest `resetAt`.
- **Cross-device reset**: `resetAt` is a timestamp. If cloud's `resetAt` is newer than the device's last-seen (`quest-last-reset` in localStorage), the device wipes and trusts cloud.
- Reset helpers (browser console): `resetAllProgress()` = full wipe everywhere; `resetAllProgress([10])` = reset only the given quest ids everywhere. Both bump `resetAt`.

### Screens (toggled via `.active` CSS class)
| Screen | Purpose |
|--------|---------|
| `screen-home` | Floating-islands map (`map-v3.jpg`), quest hotspots, rope-bridge trail, brainrot chars, bottom-center XP bar + current-step pink banner |
| `screen-quest` | Individual quest (height: 100vh; overflow-y: auto) |
| `screen-book` | Hero Book: per-quest keepsake chapters (`BOOK_RENDERERS` in app.js) for completed quests only; empty/progress pages mid-journey; finale-movie button (`#btn-movie` → `playHeroMovie()`) appears only when all 10 are done |

### Quest Progression
- Sequential unlock: Quest N+1 unlocks after Quest N completes
- Each quest: 100 XP (1000 total for all 10)
- The whole island map is always visible (an overview). Steps are not hidden.
- **Completed / current / locked** = clickable / clickable / not-clickable. Clickable steps show a `pointer` (hand) cursor; locked steps and the rest of the map show a plain arrow.
- **Current step** is indicated by the fixed pink banner `#current-step-banner` ("השלב שלי: <name>") bottom-center above the XP bar, PLUS a bouncing pink "כאן!" badge (`.map-node-status.st-here`) anchored to the step's hotspot. Completed steps show a green ✓ badge (`.map-node-status.st-done`). Badges reuse the MAP_POSITIONS hotspot centers, so they land on/near each painted island.
- Completion popup (`showXPGain`): stars + confetti + a **clickable** green "המשימה הבאה נפתחה!" button (`.xp-next`, role=button) → dismisses + returns to map; backdrop click also dismisses; 3s auto-close fallback.

### Quest Validation & completion
`getQuestValidation(questId)` checks per-task-type requirements and returns `{ valid, missing }`.
- **Strict completion** (per user decision): require ALL items — open all hero-journey files, rate all brain-meters, open all 8 secret-envelopes, produce the medal (medal-factory), watch all Q9 videos, solve all investigation-quiz steps, twin-sort placed in the **correct** bin, etc.
- **Quest 2 is exempt** — `getQuestValidation` early-returns `valid` for `questId === 2` (its Kahoot is live/in-person, must never block progress).
- The Complete button stays **clickable even when invalid** (NOT natively disabled — a disabled button gives an ASD user no feedback). It carries a `.not-ready` style; clicking when invalid runs `completeQuest()` which shows the Hebrew "what's missing" toast.
- **Gentle, forgiving wrong-answer feedback** (per user decision): no harsh red flash / snap-back / hard gates. twin-sort wrong drop = calm hint + soft drift-back; Q3 quiz + Neta quiz wrong = soft amber hint, retryable.

### Map System
- Background: `map-v3.jpg` — floating islands in a bright sky. **Island names + scene icons are baked into this image** (so they can't be hidden/recolored via CSS, and node coordinates only approximately align with the painted islands).
- Title banner: top-center "מסע הגיבורים של גיא" (Bungee/display, white with purple stroke).
- Nodes: transparent hotspots (`13vw × 15vh`) sized to each island, positioned by `MAP_POSITIONS` (quests.js). DOM `.map-node-label`s are hidden (the baked map shows the names). Locked-step cloud cover was removed. Progress badges (`.map-node-status`) are the only visible node UI.
- **Hero Book node** (`.map-node-treasure`): ALWAYS on the map at (78%, 76%) with an enlarged hotspot (16vw × 28vh) covering the painted book + its painted "פתח" button; opens the book at any stage of the journey.
- Trail + brainrot chars: `drawMapPath()` / `renderBrainrotChars()` still run, but the final CSS layer hides `#map-path-svg`, `#trail-stones` and `#brainrot-container` — the bridges/characters seen on screen are baked into `map-v3.jpg`.
- `cloud.svg`: decorative drifting sky clouds (also hidden by the final layer).
- **XP bar**: compact, pinned **bottom-center** (`.map-xp`, fixed). Current-step pink banner sits just above it.
- Cursor: arrow across the map; clickable steps (`.map-node-done/-next/-treasure`) show `pointer`.
- No scrolling: everything fits in 100vh.

### Family Tree (Quest 1)
- Background: `photos/family-tree-bg.png` (illustrated tree with circular slots)
- Layout: 3 rows (grandparents top, parents/aunts middle, children bottom)
- Photos: absolutely positioned over template slots; Guy has golden glow
- Data: `renderFamilyTree()` in app.js positions members as % coordinates; `treePositions` array maps idx/left/top/cls

### Task Types
| Type | Purpose | Quest |
|------|---------|-------|
| `info` | Read-only text | — |
| `textarea` / `reflection` | Text input | — |
| `family-flow` | Sequential cards → family tree | 1 |
| `kahoot-guide` | Numbered step list | (legacy) |
| `inspiration-cards` | Flip cards (persist actual flip state) | 2 |
| `checklist` | Checkboxes | 2 |
| `multiselect` | Multiple choice checkboxes | — |
| `investigation-quiz` | Multi-step quiz + images, progressive unlock | 3 |
| `hero-journey` | Accordion collapsibles with instructions | 4 |
| `power-stones` | Toggle stone icons (strengths) | 4 |
| `message-bubbles` | Single-select cards | 4 |
| `brain-meters` | Sliders + buttons + brain map reveal | 5 |
| `brain-cards` | Flip cards + "זה אני!" claim buttons | 5 |
| `drag-select` | Single-select sentence cards | 5 |
| `twin-sort` | Drag & drop (or tap-to-place) into bins; only CORRECT placements persist; wrong = gentle hint + soft drift-back (no red shake); live "מויינו X/N" counter | 6 |
| `neta-envelope` | Locked gold envelope → trivia modal (3 Q's on Neta) → unlock video + greeting | 6 |
| `trophy-hero-image` | Hero video/image with golden border | 7 |
| `trophy-cabinet` | Wooden shelf + drag & drop medals + live counter | 7 |
| `medal-factory` | Factory UI with custom dropdowns, produce button, animated result | 7 |
| `trophy-select` | Click placed medal → golden trophy pulse | 7 |
| `secret-envelopes` | Scattered expand/collapse cards, asymmetric sizes, click-to-toggle | 8 |
| `superpower-survey` | Name + power dropdown (5 people) | 8 |
| `cinema-videos` | Scattered title cards → fullscreen overlay video player | 9 |
| `emotion-board` | Emotion selection grid | 9 |
| `support-map` | Categorized name + message inputs | 9 |
| `card-builder` | Build a Bar Mitzvah "winning card": dropdown fields (prefix + options) → reveal trading card with hero photo | 10 |
| `story` | Styled text block | — |

## Quest Status (June 2026)

Step names match the island map (`quest.name` is the single source of truth — used by map, banner, and quest-screen headers).

| Quest | Status | Content |
|-------|--------|---------|
| 1 - עץ השורשים | Complete | Family flow + tree |
| 2 - משחק הכרות | Complete (**optional** — never blocks) | Inspiration cards + checklist + textarea (live Kahoot game) |
| 3 - חקירה משפחתית | Complete | 4-step investigation quiz + images |
| 4 - הגיבור שנולד | Complete | Accordion + power stones + message bubbles |
| 5 - המוח המיוחד שלי | Complete | Meters + brain map + flip cards |
| 6 - השבט שלי | Complete | 2x drag & drop (twins) + Neta trivia envelope |
| 7 - הדרך שעשיתי | Complete | Cabinet + factory + trophy |
| 8 - Super powers | Complete | 8 scattered envelope cards (real messages) + power select |
| 9 - האנשים שלי | Complete | 11 greeting-video cards (incl. אבא ואמא + נטע ומיקה, added 2026-07-05) + overlay player + emotion board |
| 10 - מי אני עכשיו | Complete | `card-builder` — Bar Mitzvah trading card (title / secret weapon / next-year goal) + hero photo |

> Note: step 8's label is **English ("Super powers")** because that's what's painted on `map-v3.jpg`; switch to Hebrew only if the map art is updated too.

## Design System (bright "floating islands" theme)
The old dark lava/neon theme was replaced. `style.css` is layered: a base layer + a
bright "candy/islands" override layer that wins the cascade. Newer fixes are appended
at the end of `style.css` (highest priority).

| Element | Value |
|---------|-------|
| Theme | Bright, friendly floating-islands-in-the-sky (kid RPG) |
| Background | sky gradient + `map-v3.jpg` islands; light page (`#FBFAF8`-ish) |
| Title | Bungee/display, white with purple stroke (`#6D28D9`) |
| Cards / panels | Light/white panels, soft shadows, rounded |
| Accents | sakura pink `#FF7AB6`/`#DB2777`, purple `#9333EA`, gold/orange `#FB8C00`, teal/green, sky-blue |
| Current-step banner | Pink pill (`#FF7AB6→#DB2777`), white bold text, bottom-center |
| Completed nodes | clickable (pointer) | 
| Current node | shown via the pink banner (no on-island ring) |
| Locked nodes | visible island, not clickable (arrow cursor) |
| Text | dark ink on light panels (avoid pure black/white); RTL |
| RTL numbers | XP / "N/M" counters use `direction: ltr; unicode-bidi: isolate` |
| Characters | 7 SAB voxel PNGs, 120px, static |
| Accessibility | clear instructions, large affordances, progress counters, gentle/forgiving feedback (ASD-friendly) |

## Constraints
- **Hebrew RTL**: Numbers in XP need `direction: ltr; unicode-bidi: isolate`
- **No frameworks**: Vanilla only
- **PC-first design**: Optimized for desktop; mobile not currently supported
- **Bright islands theme**: New components use light panels + the bright accent palette (pinks/purple/gold/teal), dark ink text on light. Append new style overrides at the END of `style.css` so they win the layered cascade. (The old "dark glass / never use #fff" rule is obsolete.)
- **Photo filenames**: Hebrew characters (e.g., `סבא מישה (מצד אבא).jpg`); twins use `.jpeg`
- **Photo centering**: Custom `object-position` via `photoPos` field in quests.js
- **Brainrot**: SAB voxel PNGs only, all 120px, static (no emoji, no animations)
- **Map scaling**: All 10 nodes + chars fit in 100vh, no scrolling
- **Family tree**: Displayed at 1200px max-width with transparent task block container
- **Media max-height**: Images/videos capped at 450px
- **Cache busting**: Auto via timestamps in index.html

## Common Tasks

**Add/edit quest**: Edit `quests.js` QUESTS array. Required: id, name, subtitle, icon, mapIcon, xp, message, color, intro, tasks[], artifact.

**Add task type**: (1) Add case in `showQuest()` switch (app.js), (2) Add validation in `getQuestValidation()`, (3) Call `updateCompleteButton()` in handlers, (4) Add CSS in style.css.

**Add validation**: Edit `getQuestValidation()` in app.js. Add case for task type; push to `missing[]` if incomplete.

**Change map positions**: Edit `MAP_POSITIONS` in quests.js (x/y %, quest-id order: Q1=tree island … Q10=top-right). These are tuned to the islands painted in `map-v3.jpg` and only approximately align — re-tuning all 10 is the proper fix if precise node/island alignment is ever needed.

**Change family tree photos**: Edit `treePositions` in `renderFamilyTree()` (app.js). Each: `idx` (member index), `left`/`top` (%), `cls` (ftree-gp, ftree-parent, ftree-child, ftree-hero).

**Add brainrot chars**: Edit `BRAINROT_CHARS` (app.js). Each: `{ img, top, right/left, size }` (all 120px). Add PNGs to brainrot/ folder.

**Deploy**: Do UI work on a `design` branch, then fast-forward/merge into `master` and push. Auto-deploys from `master` (1-2 min). **Bump `style.css?v=` in index.html** when CSS changed (JS is timestamp-busted automatically).

**Reset progress** (cross-device, via Firebase — preferred):
```javascript
// Full reset — wipes this device AND every other device on next load
resetAllProgress();
location.reload();

// Partial reset — reset only specific quest ids everywhere (keep the rest)
resetAllProgress([6, 7, 8, 9, 10]);
location.reload();
```
Local-only fallback (does NOT propagate to other devices):
```javascript
localStorage.removeItem('bar-mitzvah-quest');
location.reload();
```

## Known Issues / TODO
- **Hero Book data gaps** — ✅ FIXED (2026-07-01). `openHeroBook()` now renders per-quest keepsake chapters via `BOOK_RENDERERS` (family grid with photos+words, power stones, brain-meter bars, twin-sort bins, Neta's greeting, medals + custom medal + trophy, all 8 blessing quotes, watched videos + emotion, and the final Bar Mitzvah card with photo).
- **Finale / storybook** — ✅ BUILT (2026-06-28). See `finale/` + `storybook.html`:
  - `finale/Hero-Movie.mp4` — ~3:05 highlight reel of the 10 steps set to `Song for the movie.mpeg`, 1080p, Hebrew RTL captions, Ken-Burns zoom + crossfades, audio fade-out.
  - `storybook.html` (+ exported `finale/Hero-Storybook.pdf`) — print-ready A4 (15 pages) "Hero Book": real photos, the family blessing messages, and QR-code greeting cards (photo + QR, 2×2 per page; most greeter photos still placeholders) for all 12 greetings incl. אבא ואמא + נטע ומיקה.
  - Reproducible builders: `finale/make_storybook.py`, `finale/make_movie.py` (repo-relative; render HTML scenes via headless Chrome, assemble MP4 with bundled ffmpeg via `imageio-ffmpeg`). See `finale/README.md`.
  - Built from authored journey content + real family photos (NOT Guy's saved responses — test data). Movie trimmed to ~3:05 with the song faded out; ask for a full-song (~3:57) cut if a longer version is wanted.
- **Quest 9 video path** — NOT a bug (verified 2026-07-01): `quests.js` stores `Videos - step 9/…mp4` and the `cinema-videos` renderer prefixes `photos/`, matching the on-disk `photos/Videos - step 9/` location (HTTP 200 verified).
- **Quest 9 complete** (2026-07-05): the real אבא ואמא + נטע ומיקה video files arrived and replaced the pre-wired guessed filenames (`סרטון - אמא ואבא.mp4` / `סרטון - האחיות.mp4`) — 11 in-app videos, all real. Their `photos/qr/` PNGs were regenerated for the real URLs (the stale guessed-name PNGs removed). Storybook greeting cards redesigned as photo+QR 2×2 pages (12 cards incl. the נטע TikTok card); `storybook.html` + `Hero-Storybook.pdf` rebuilt (15 pages).
- **Blessing movies rebuilt** (2026-07-05, twice): `Hero-Movie-Long.mp4` (9:12) + `Hero-Movie-Short.mp4` (4:42). 12 blessings — the 11 greeting videos + Neta's TikTok (`photos/neta_and_guy_video.mp4`, referenced as `../neta_and_guy_video.mp4` in BLESSINGS/segments) closing the set. `blessing_segments.json` is fully curated AND user-reviewed — 6 segments auto-found by faster-whisper (`medium` model; `small` misses most Hebrew), the rest hand-picked from word-level transcripts / adjusted by the user. DON'T re-run `--transcribe` blindly; it only fills `null` entries, so curated values are safe, but resetting them to null loses the curation. Audio: the "ברכות מהמשפחה" card carries a quiet song bed (continues from the reel), and the 12s outro card plays the song's real finale (`card_to_video(song=...)`).
- **Hero-Movie.mp4 updated** (2026-07-05/06): step-7 scene is now the real soccer clip (`videoscene()` in make_movie.py — slow-motion loop, blurred-pad centered, transparent HTML caption overlay) instead of a still; the step-3 ultrasound caption + Quest 3 quiz step + storybook note were reworded to remove the triplet-pregnancy reference ("הפתעה כפולה" framing) — per the parents, that detail must not appear anywhere. Per video QA: the zoompan Ken-Burns effect was REMOVED (it made stills tremble — keep scenes static), the decorative cloud overlays were removed from the map cover/finale scenes, and grid-cell name labels sit BELOW the photo (never overlaid on faces).
- **Karaoke subtitles** (2026-07-06): the reel burns the full song lyrics as bottom-edge strips — `LYRICS` table in make_movie.py, (start, end, line) timed via faster-whisper word timestamps of `Song for the movie.mpeg` + manual review (the sung "עוצר" transcribes as "רוצה"; timings are reliable). Strips are Chrome-rendered transparent PNGs overlaid with `enable=between(t,..)`. If the song ever changes, re-time the table.
- **Hero Book hidden from the map** (2026-07-06): `HERO_BOOK_ON_MAP = false` flag at the top of app.js — the parents will reveal the book + finale movies to Guy on a separate occasion. Flip to `true` to restore the map button (the painted "פתח" on map-v3.jpg stays visible but inert while hidden).
- **QR codes → YouTube** (2026-07-07): all 12 `yt` links in `GREETERS` (make_storybook.py) are filled and the 11 `photos/qr/*.png` (in-app Hero Book grid) were regenerated to the YouTube links (verified by decoding every QR). The `gh` GitHub-Pages fallbacks remain in the code but are unused. Remaining storybook gap: most greeter photos are still placeholders ("תמונה תתווסף").
- `map-v3.jpg` bakes in island names/scenes → can't hide/recolor per-step; "Super powers" label is English
- Hero Book PDF export is basic (browser print)
- Mobile responsive design not supported (PC-first)
- Firebase config + family passcode (`1907`) are committed in client JS (public repo) — acceptable for this private family use, but not secret
- `Song for the movie.mpeg` (repo root) is the Suno soundtrack — now **tracked** as the source music for `finale/Hero-Movie.mp4` (used by `finale/make_movie.py`)
- Untracked working files in repo root (`Design/`, `map-v4.jpg`, `new.style.bundled.css`, `backups/`) are scratch/abandoned assets, not used by the app

## Session log (2026-07-02) — family progress view (branch `claude/quest-accessibility-review-9ffbjj`, restarted from master)
- **family.html** — read-only, mobile-first "מעקב משפחתי" page at `/family.html`: live progress (X/10, XP bar, current step), a ✓/כאן/🔒 step list, and the completed Hero Book chapters (reuses `BOOK_RENDERERS` + `buildFamilyTreeHTML` + `buildCartoonBrainSVG` from app.js). Subscribes with `dbRef.on('value')` so it updates in real time; NEVER writes to Firebase/localStorage — safe to share with the wider family without risking Guy's saved answers.
- Same passcode gate (`showPasscodeScreen()` from firebase-sync.js; one unlock per session covers both pages).
- app.js boot now no-ops on pages without `#screen-home` so family.html can load it just for the shared renderers.
- Share link: https://yaelk-maker.github.io/bar-mitzvah-quest/family.html

## Session log (2026-07-01b) — brain image, tree-in-book, new videos, 2-version movie (same branch)
- **Cartoon brain**: `buildCartoonBrainSVG()` (app.js) draws a colorful cartoon brain whose puffy lobes are colored/sized by Guy's brain-meter answers (grey variant = "typical brain"). Used in the Quest 5 reveal AND Hero Book chapter 5. Replaced the old bubble SVG.
- **Family tree**: tree markup extracted to `buildFamilyTreeHTML()` and reused — the Hero Book chapter 1 now shows the real illustrated tree (photos + words), not a grid.
- **New greeting videos**: Quest 9 now lists `סרטון - אמא ואבא.mp4` (parents) and `סרטון - האחיות.mp4` (Neta+Mika) FIRST — **files not yet uploaded**; drop them into `photos/Videos - step 9/` with those exact names and they play (until then the friendly placeholder shows). Two more slots are reserved as comments in quests.js / make_storybook.py / make_blessings.py.
- **QR codes**: `photos/qr/*.png` (pre-generated, one per greeting video incl. the two pending ones — their URLs go live when the files are uploaded). Shown in Hero Book chapter 9; storybook.html regenerated with the new entries too.
- **Final movie ×2** (`finale/make_blessings.py`): `Hero-Movie-Short.mp4` (~4 min) = Hero-Movie + only the "מזל טוב גיא" moment of each blessing; `Hero-Movie-Long.mp4` (~7.5 min) = Hero-Movie + every FULL blessing. Uniform 720p, blurred-pad framing, per-person lower-third name tags (PIL+bidi Hebrew), section/outro cards. Both playable from the Hero Book footer once all 10 steps are done.
- **"מזל טוב" moments**: come from `finale/blessing_segments.json` (currently `null` = first 6s fallback, because this sandbox's network blocks whisper model downloads). Run `python finale/make_blessings.py --transcribe` on a normal machine to auto-detect the exact moments (faster-whisper word timestamps), then rerun the build; or hand-edit `[start, end]` seconds per video in the json.

## Session log (2026-07-01) — full UI/UX review + fixes (branch `claude/quest-accessibility-review-9ffbjj`)
- **Hero Book rewritten as a keepsake**: `BOOK_RENDERERS` renders every quest's real content (photos, chips, meter bars, sorting bins, Neta's greeting, the 8 blessing envelopes, the final card with hero photo). Book shows completed chapters only, plus friendly empty/progress pages.
- **Hero Book always reachable**: the painted "פתח" button on the map now works from day one (treasure hotspot moved to 78%/76% and enlarged to cover the painted book + button).
- **Map progress at a glance**: green ✓ badge on each completed island, bouncing pink "כאן!" badge on the current one (`.map-node-status`).
- **Finale movie wired in**: dead "צפייה במצגת" stub replaced by `playHeroMovie()` playing `finale/Hero-Movie.mp4` in the cinema overlay; button appears only when all 10 steps are done.
- Fixes: removed leftover completion check that could block Quest 2 (must never block); twin-sort drop can no longer grab a same-index card from the other sorting stage; factory-made personal medal + chosen "proudest" highlight now survive reload; PWA theme/background colors updated from the old dark theme to the bright sky palette.
- Verified end-to-end with headless-browser screenshots (map states, all 10 quests, book, popups); no JS errors. Bumped `style.css?v=20260701review`.

## Session log (2026-06-27/28) — what shipped to `master`
- Integrated the bright floating-islands redesign (map-v3.jpg, cloud.svg, restyled style.css, rope-bridge trail, island MAP_POSITIONS)
- Ran a 14-agent UI/UX/QA review (43 findings); fixed 39: strict completion, gentle feedback, accessibility (tap hints, contrast, video Esc), Firebase merge-on-write, passcode-always-shown, junk `responses.undefined` key, RTL counters, etc.
- Family flow: require a word per member + consistent card layout
- Map polish: removed locked-step clouds, moved XP bar bottom-center, fixed current-step pink banner, arrow/pointer cursors, clickable completion popup button
- Renamed steps app-wide to match the map; made Quest 2 optional
