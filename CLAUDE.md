# Bar Mitzvah Quest - Claude Development Guide

## Project Overview
Gamified Bar Mitzvah identity quest PWA for Guy (12.5, Bar Mitzvah July 19, 2026). RPG-style 10-step journey building toward "Hero Book" displayed at the event. Guy has cerebral palsy and autism; his twin sister is Mika.

## Tech Stack
- **Vanilla HTML/CSS/JS** — no frameworks, no build step
- **PWA** with manifest.json; state persisted to Firebase Realtime Database (source of truth) + localStorage cache; family passcode `1907`
- **Hosted**: https://yaelk-maker.github.io/bar-mitzvah-quest/ (GitHub Pages, `master` branch)
- **Repo**: https://github.com/yaelk-maker/bar-mitzvah-quest (public)
- **Fonts**: Heebo (Hebrew body) + Bungee / Frank Ruhl Libre / Baloo 2 (display) from Google Fonts
- **Cache busting**: JS files use timestamp query params (auto-generated in index.html). `style.css` uses a manual `?v=...` tag — **bump it on every deploy that changes CSS** (currently `?v=20260628live`)
- **Design**: bright "floating islands in the sky" theme (see Design System). UI iterated via claude.ai/design exports + manual integration; design work happens on a `design` branch then merges to `master`.

## File Structure
```
bar-mitzvah-quest/
├── index.html          # Main HTML: home map, quest, hero book (3 screens)
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
│   └── [11 Hebrew-named family photos]
├── Videos - step 9/    # Quest 9 greeting videos (Hebrew filenames)
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
| `screen-book` | Hero Book: all completed quest responses |

### Quest Progression
- Sequential unlock: Quest N+1 unlocks after Quest N completes
- Each quest: 100 XP (1000 total for all 10)
- The whole island map is always visible (an overview). Steps are not hidden.
- **Completed / current / locked** = clickable / clickable / not-clickable. Clickable steps show a `pointer` (hand) cursor; locked steps and the rest of the map show a plain arrow.
- **Current step** is indicated by a fixed pink banner `#current-step-banner` ("השלב שלי: <name>") pinned bottom-center above the XP bar — NOT an on-island marker (the baked map's island positions don't align with node coordinates, so on-island overlays float off). Populated from the next quest in the map render.
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
- Nodes: transparent hotspots (`13vw × 15vh`) sized to each island, positioned by `MAP_POSITIONS` (quests.js). DOM `.map-node-label`s are hidden (the baked map shows the names). Locked-step cloud cover was removed.
- Trail: rope-bridge style drawn as SVG in `drawMapPath()` (replaced the old lava path).
- `cloud.svg`: decorative drifting sky clouds.
- Characters: 7 SAB voxel PNGs, 120px, static (BRAINROT_CHARS in app.js).
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
| 9 - האנשים שלי | Partial | 10 greeting-video cards + overlay player (some placeholder videos) + emotion board |
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
- **Hero Book data gaps**: `openHeroBook()` only renders string responses, so Quest 4 (power stones + chosen message) and Quest 10 (card-builder object) and the custom factory medal **don't appear** in the book. To fix with the finale work.
- **Finale / storybook** (paused, designed not built): "Hero Movie" highlight reel + print-ready storybook (A4, QR codes to greeting videos). See brainstorm in chat history.
- Quest 9 still has some placeholder greeting videos
- `map-v3.jpg` bakes in island names/scenes → can't hide/recolor per-step; "Super powers" label is English
- Hero Book PDF export is basic (browser print)
- Mobile responsive design not supported (PC-first)
- Firebase config + family passcode (`1907`) are committed in client JS (public repo) — acceptable for this private family use, but not secret
- Untracked working files in repo root (`Design/`, `map-v4.jpg`, `new.style.bundled.css`, `backups/`, `Song for the movie.mpeg`) are scratch/abandoned assets, not used by the app

## Session log (2026-06-27/28) — what shipped to `master`
- Integrated the bright floating-islands redesign (map-v3.jpg, cloud.svg, restyled style.css, rope-bridge trail, island MAP_POSITIONS)
- Ran a 14-agent UI/UX/QA review (43 findings); fixed 39: strict completion, gentle feedback, accessibility (tap hints, contrast, video Esc), Firebase merge-on-write, passcode-always-shown, junk `responses.undefined` key, RTL counters, etc.
- Family flow: require a word per member + consistent card layout
- Map polish: removed locked-step clouds, moved XP bar bottom-center, fixed current-step pink banner, arrow/pointer cursors, clickable completion popup button
- Renamed steps app-wide to match the map; made Quest 2 optional
