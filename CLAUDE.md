# Bar Mitzvah Quest - Claude Development Guide

## Project Overview
A gamified Bar Mitzvah identity quest PWA for Guy (12.5, Bar Mitzvah July 19, 2026). Guy has cerebral palsy and autism, is a twin with his sister Mika. The app is a 10-step RPG-style journey that builds toward a personal "Hero Book" shown at the Bar Mitzvah.

## Tech Stack
- **Vanilla HTML/CSS/JS** — no frameworks, no build step
- **PWA** with manifest.json, localStorage for state persistence
- **Hosted on GitHub Pages**: https://yaelk-maker.github.io/bar-mitzvah-quest/
- **Repo**: https://github.com/yaelk-maker/bar-mitzvah-quest (public, `master` branch)
- **Font**: Heebo (Hebrew) + Bungee (titles), loaded from Google Fonts
- **Cache busting**: JS files loaded with timestamp query params (auto-generated in index.html)

## File Structure
```
bar-mitzvah-quest/
├── index.html          # Main HTML - 3 screens: home map, quest, hero book
├── app.js              # All app logic: state, navigation, quest rendering, map, validation
├── quests.js           # Quest data model (10 quests) + MAP_POSITIONS
├── style.css           # All styles - lava/volcanic game theme
├── map-bg.png          # Lava/volcanic game map background (from itch.io asset pack)
├── manifest.json       # PWA manifest
├── icon-192.png        # PWA icon (192x192)
├── icon-512.png        # PWA icon (512x512)
├── photos/             # Family member photos + stage photos + video
│   ├── family-tree-bg.png            # Illustrated family tree template
│   ├── placeholder_parents_young.jpg # Quest 3 - parents story
│   ├── placeholder_neta_baby.jpg     # Quest 3 - Neta as baby
│   ├── placeholder_nicu_twins.jpg    # Quest 3 - twins in NICU
│   ├── placeholder_ultrasound.jpg    # Quest 3 - ultrasound
│   ├── placeholder_twins_babies.jpeg # Quest 6 - twins as babies
│   ├── placeholder_twins_kids.jpeg   # Quest 6 - twins as kids
│   ├── placeholder_twins_teens.jpeg  # Quest 6 - twins as teens
│   ├── guy_soccer_video.mp4          # Quest 7 - hero video (autoplay loop)
│   └── [11 family member photos with Hebrew filenames]
├── brainrot/           # SAB (Steal a Brainrot) voxel character PNGs (7 figures)
│   ├── sab-tralalero.png, sab-shark.png, sab-spaghetti.png
│   ├── sab-blue.png, sab-giftbox.png, sab-bat.png, sab-67.png
├── CLAUDE.md           # This file
├── README.md           # Project documentation
└── STITCH_PROMPT.md    # Google Stitch design prompts (reference only)
```

## Architecture

### State Management
- All state stored in `localStorage` under key `bar-mitzvah-quest`
- State shape: `{ completedQuests: number[], responses: { [questId]: { [key]: value } }, currentQuest: number | null }`
- `loadState()` / `saveState()` for persistence
- To reset: `localStorage.removeItem('bar-mitzvah-quest')` in browser console

### Screen System
Three screens toggled via CSS `.active` class:
1. **`screen-home`** — Treasure map with winding path, quest nodes, brainrot characters
2. **`screen-quest`** — Individual quest view with tasks. Uses `height: 100vh; overflow-y: auto` so sticky footer works.
3. **`screen-book`** — Hero Book view (all completed quest responses)

### Quest Progression
- Sequential unlock: Quest N+1 unlocks only after Quest N is completed
- Each quest awards 100 XP (total 1000 XP for all 10)
- Completed quests show green checkmark on map
- Next available quest pulses yellow
- Locked quests show grey circle with lock icon (no name visible)

### Quest Completion Validation
The `getQuestValidation(questId)` function checks per-task-type requirements before enabling the complete button. Each interactive task type has its own validation rule (e.g., at least 1 stone selected, all cards sorted, all dropdowns filled). The complete button starts **disabled** and enables only when all sections pass validation. On click, `completeQuest()` also runs validation and shows a Hebrew toast listing missing items.

### Map System
- **Background**: Lava/volcanic game map (`map-bg.png`) with dark theme
- **Banner**: 60px centered header with gradient title "מסע הגיבורים של גיא"
- `MAP_POSITIONS` array in quests.js defines x/y percentage positions for each node
- SVG bezier curves connect nodes (lava-orange trail + bright green completed overlay)
- `BRAINROT_CHARS` array in app.js defines 7 SAB voxel character images (all 90px, static positioned)
- Map is fullscreen (100vh), no scrolling
- XP bar with gold colors on dark background

### Family Tree (Quest 1 - Illustrated Template)
- Uses `photos/family-tree-bg.png` as background — an illustrated tree with circular photo slots
- Family member photos are absolutely positioned over the template's circular slots
- 3 rows: grandparents (top 4), parents & aunts (middle 4 + heart), children (bottom 3)
- Each member shows: circular photo, name label, relation, and the word Guy wrote
- Guy's photo has special golden glow (hero style)
- Positions defined as percentage coordinates in `renderFamilyTree()` function in app.js

### Task Types
Quest tasks are rendered dynamically based on `type`:
- `info` — Read-only text block
- `textarea` / `reflection` — Text input areas
- `family-flow` — Sequential family member cards with per-person word input, culminating in illustrated family tree overlay
- `kahoot-guide` — Step-by-step guide with numbered list
- `checklist` — Checkbox items
- `multiselect` — Multiple choice checkboxes
- `investigation-quiz` — Multi-step quiz with story reveal, images, and progressive unlocking (Quest 3)
- `hero-journey` — Accordion collapsible cards with instruction text and clear affordances (Quest 4)
- `power-stones` — Toggle-able stone icons representing strengths (Quest 4)
- `message-bubbles` — Single-select message cards (Quest 4)
- `brain-meters` — Trait sliders with level buttons + brain bubble map reveal (Quest 5)
- `brain-cards` — Flip cards with "זה אני!" claim buttons (Quest 5)
- `drag-select` — Single-select sentence cards (Quest 5)
- `twin-sort` — Card sorting into 3 bins (Guy/Both/Mika) with drag & drop + click fallback. Wrong answers shake and bounce back. (Quest 6)
- `twin-madlibs` — Mad-libs sentence with dropdown selects (Quest 6)
- `trophy-hero-image` — Hero video/image at top with golden border. Uses `<video autoplay loop muted playsinline>` with image fallback. (Quest 7)
- `trophy-cabinet` — Wooden shelf cabinet with drag & drop medal placement + live counter (Quest 7)
- `medal-factory` — Game-like factory UI with custom dropdowns, produce button, and animated medal result (Quest 7)
- `trophy-select` — Click a placed medal to crown it as golden trophy with pulse animation (Quest 7)
- `twin-shared` / `twin-unique` — Numbered text inputs for twin comparison (legacy, replaced by twin-sort)
- `superpower-survey` — Name + power dropdown for 5 people
- `support-map` — Categorized name + message inputs
- `story` — Styled text block for parent-written stories
- `achievement-picker` — Placeholder for parent-provided achievements (legacy, replaced by trophy-cabinet)

## Quest Status (as of April 2026)

| Quest | Status | Interactive Elements |
|-------|--------|---------------------|
| 1 - שורשים | Complete | Family flow + illustrated tree |
| 2 - משחק המשפחה | Complete | Kahoot guide + checklist |
| 3 - תיק החקירה | Complete | 4-step investigation quiz with images |
| 4 - הגיבור שנולד | Complete | Accordion cards + power stones + message bubbles |
| 5 - המוח שלי עובד אחרת | Complete | Brain meters + brain bubble map + flip cards |
| 6 - תאום אבל אני | Complete | 2x card sorting (drag & drop) + mad-libs blessing |
| 7 - הדרך שעשיתי | Complete | Trophy cabinet (drag & drop) + medal factory + golden trophy |
| 8 - הסופרפאוורס שלי | Needs content | Superpower survey (5 people) |
| 9 - האנשים שלי | Needs content | Support map |
| 10 - מי אני עכשיו | Needs content | Personal manifesto |

## Design System
- **Theme**: Dark lava/volcanic game style with bright neon accents
- **Map Background**: `map-bg.png` — lava game map from itch.io asset pack
- **Body Background**: `#1a1025` (dark purple)
- **Banner**: Dark gradient with gold/orange/pink gradient text (Bungee font)
- **Cards**: White with chunky borders, rounded corners (20px), drop shadows
- **Buttons**: Chunky game buttons with bottom shadows (3D effect)
- **Node styles**: Green neon glow (completed), yellow neon pulse (next), dark volcanic stone (locked)
- **Path colors**: Lava orange (`#ff8f00`) default, bright green (`#76ff03`) completed
- **Colors**: See CSS `:root` variables
- **Direction**: RTL (Hebrew), with LTR isolation for XP numbers
- **Brainrot characters**: 7 SAB voxel PNGs, static positioned (no animations), uniform 90px size
- **Accessibility**: Accordion cards use `aria-expanded`, buttons use semantic HTML, clear visual affordances for autistic user

## Important Constraints
- **Hebrew RTL**: All text is right-to-left. Numbers in XP display need `direction: ltr; unicode-bidi: isolate`
- **No frameworks**: Must stay vanilla HTML/CSS/JS
- **Photo filenames**: Hebrew characters in filenames (e.g., `סבא מישה (מצד אבא).jpg`), twin photos use `.jpeg` extension
- **Photo face centering**: Each photo has custom `object-position` via `photoPos` field in quests.js
- **Accessibility for autistic user**: Clear instructions, visual affordances (e.g., "לחץ לפתיחה 🔽"), counters showing progress, no ambiguous interactions
- **Brainrot characters**: Only SAB (Steal a Brainrot) voxel PNGs from the Figures folder. No emoji, no other meme images. All 90px, static.
- **Map scaling**: All 10 nodes + characters must fit in one viewport (100vh) without scrolling
- **Family tree image**: `photos/family-tree-bg.png` compressed to ~800KB for web performance (original was 6MB)
- **Cache busting**: JS files use timestamp-based cache busting (`document.write` in index.html) to prevent stale code on GitHub Pages

## Common Tasks

### Adding/editing a quest
Edit `quests.js` — add to the `QUESTS` array following the existing pattern. Each quest needs: id, name, subtitle, icon, mapIcon, xp, message, color, intro, tasks[], artifact.

### Adding a new task type
1. Add the `case` in the task rendering `switch` in `showQuest()` in app.js
2. Add validation in `getQuestValidation()` if the task requires user interaction
3. Call `updateCompleteButton()` in each click/change handler
4. Add CSS styles in style.css

### Adding quest validation
Edit `getQuestValidation()` in app.js. Add a `case` for your task type that checks `responses` and pushes to `missing[]` if incomplete. The complete button auto-disables when validation fails.

### Changing map node positions
Edit `MAP_POSITIONS` in `quests.js`. Values are percentages (x: 0-100, y: 0-100). Ensure all nodes stay within viewport (y max ~75%, x range 10-85%).

### Changing family tree photo positions
Edit the `treePositions` array inside `renderFamilyTree()` in `app.js`. Each entry has `idx` (member index in flowMembers), `left`/`top` percentages relative to the tree template image, and `cls` (ftree-gp, ftree-parent, ftree-child, or ftree-hero).

### Adding/changing brainrot characters
Edit `BRAINROT_CHARS` array in `app.js`. Each entry: `{ img, top, right/left, size }`. All should be 90px. Add PNGs with transparent backgrounds to `brainrot/` folder.

### Deploying
```bash
git add . && git commit -m "description" && git push
```
GitHub Pages auto-deploys from `master` branch. Allow 1-2 minutes for deployment. JS/CSS cache busting is automatic via timestamps.

### Resetting quest progress
Full reset:
```javascript
localStorage.removeItem('bar-mitzvah-quest');
location.reload();
```

Reset from a specific quest (e.g., keep quests 1-5, reset 6+):
```javascript
let s = JSON.parse(localStorage.getItem('bar-mitzvah-quest'));
s.completedQuests = s.completedQuests.filter(id => id <= 5);
[6,7,8,9,10].forEach(id => delete s.responses[id]);
s.currentQuest = null;
localStorage.setItem('bar-mitzvah-quest', JSON.stringify(s));
location.reload();
```

## Known Issues / TODO
- Quests 8-10 need parent-provided content
- Hero Book PDF export is basic (browser print)
- Mobile responsive design not yet fully implemented
- Completed quests should show artifact preview on map (deferred)
- Presentation export not implemented yet
- Family tree photo positions may need fine-tuning on different screen sizes
