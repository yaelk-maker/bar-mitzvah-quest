# Bar Mitzvah Quest - Claude Development Guide

## Project Overview
A gamified Bar Mitzvah identity quest PWA for Guy (12.5, Bar Mitzvah July 19, 2026). Guy has cerebral palsy and autism, is a twin with his sister Mika. The app is a 10-step RPG-style journey that builds toward a personal "Hero Book" shown at the Bar Mitzvah.

## Tech Stack
- **Vanilla HTML/CSS/JS** — no frameworks, no build step
- **PWA** with manifest.json, localStorage for state persistence
- **Hosted on GitHub Pages**: https://yaelk-maker.github.io/bar-mitzvah-quest/
- **Repo**: https://github.com/yaelk-maker/bar-mitzvah-quest (public, `master` branch)
- **Font**: Heebo (Hebrew) + Bungee (titles), loaded from Google Fonts

## File Structure
```
bar-mitzvah-quest/
├── index.html          # Main HTML - 3 screens: home map, quest, hero book
├── app.js              # All app logic: state, navigation, quest rendering, map
├── quests.js           # Quest data model (10 quests) + MAP_POSITIONS
├── style.css           # All styles - lava/volcanic game theme
├── map-bg.png          # Lava/volcanic game map background (from itch.io asset pack)
├── manifest.json       # PWA manifest
├── icon-192.png        # PWA icon (192x192)
├── icon-512.png        # PWA icon (512x512)
├── photos/             # Family member photos (11 JPG/JPEG files, Hebrew names)
│   └── family-tree-bg.png  # Illustrated family tree template with circular photo slots
├── brainrot/           # SAB (Steal a Brainrot) voxel character PNGs (7 figures)
│   ├── sab-tralalero.png   # Red elephant
│   ├── sab-shark.png       # Dark orca
│   ├── sab-spaghetti.png   # Pasta character
│   ├── sab-blue.png        # Blue voxel creature
│   ├── sab-giftbox.png     # Winged mystery box
│   ├── sab-bat.png         # Wooden bat character
│   └── sab-67.png          # Blue number character
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
2. **`screen-quest`** — Individual quest view with tasks (text inputs, checklists, etc.)
3. **`screen-book`** — Hero Book view (all completed quest responses)

### Quest Progression
- Sequential unlock: Quest N+1 unlocks only after Quest N is completed
- Each quest awards 100 XP (total 1000 XP for all 10)
- Completed quests show green checkmark on map
- Next available quest pulses yellow
- Locked quests show grey circle with lock icon (no name visible)

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
- `family-tree` — Grid of family members with photo + word input (legacy, replaced by family-flow)
- `kahoot-guide` — Step-by-step guide with numbered list
- `checklist` — Checkbox items
- `multiselect` — Multiple choice checkboxes
- `twin-shared` / `twin-unique` — Numbered text inputs for twin comparison
- `superpower-survey` — Name + power dropdown for 5 people
- `support-map` — Categorized name + message inputs
- `story` — Styled text block for parent-written stories
- `achievement-picker` — Placeholder for parent-provided achievements

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

## Important Constraints
- **Hebrew RTL**: All text is right-to-left. Numbers in XP display need `direction: ltr; unicode-bidi: isolate`
- **No frameworks**: Must stay vanilla HTML/CSS/JS
- **Photo filenames**: Hebrew characters in filenames (e.g., `סבא מישה (מצד אבא).jpg`)
- **Photo face centering**: Each photo has custom `object-position` via `photoPos` field in quests.js
- **Mobile adaptation**: Deferred — currently desktop-first. Will be addressed after all content is complete
- **Brainrot characters**: Only SAB (Steal a Brainrot) voxel PNGs from the Figures folder. No emoji, no other meme images. All 90px, static.
- **Map scaling**: All 10 nodes + characters must fit in one viewport (100vh) without scrolling
- **Family tree image**: `photos/family-tree-bg.png` compressed to ~800KB for web performance (original was 6MB)

## Common Tasks

### Adding/editing a quest
Edit `quests.js` — add to the `QUESTS` array following the existing pattern. Each quest needs: id, name, subtitle, icon, mapIcon, xp, message, color, intro, tasks[], artifact.

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
GitHub Pages auto-deploys from `master` branch. Allow 1-2 minutes for deployment. Users may need Ctrl+Shift+R to bypass cache.

## Known Issues / TODO
- Quests 3-10 need parent-provided content (stories, achievement lists, photos)
- Hero Book PDF export is basic (browser print)
- Mobile responsive design not yet implemented
- Completed quests should show artifact preview on map (deferred)
- Presentation export not implemented yet
- Family tree photo positions may need fine-tuning on different screen sizes
