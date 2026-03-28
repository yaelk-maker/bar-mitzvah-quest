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
├── style.css           # All styles - bright "brainrot" game theme
├── manifest.json       # PWA manifest
├── icon-192.png        # PWA icon (192x192)
├── icon-512.png        # PWA icon (512x512)
├── photos/             # Family member photos (11 JPG/JPEG files, Hebrew names)
├── brainrot/           # Brainrot character PNGs (12 active + 5 backup)
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
- `MAP_POSITIONS` array in quests.js defines x/y percentage positions for each node
- SVG bezier curves connect nodes (brown dirt trail + green completed overlay)
- `BRAINROT_CHARS` array in app.js defines character images scattered on map
- Map is fullscreen (100vh), no scrolling

### Task Types
Quest tasks are rendered dynamically based on `type`:
- `info` — Read-only text block
- `textarea` / `reflection` — Text input areas
- `family-flow` — Sequential family member cards with per-person word input, culminating in illustrated family tree
- `family-tree` — Grid of family members with photo + word input
- `kahoot-guide` — Step-by-step guide with numbered list
- `checklist` — Checkbox items
- `multiselect` — Multiple choice checkboxes
- `twin-shared` / `twin-unique` — Numbered text inputs for twin comparison
- `superpower-survey` — Name + power dropdown for 5 people
- `support-map` — Categorized name + message inputs
- `story` — Styled text block for parent-written stories
- `achievement-picker` — Placeholder for parent-provided achievements

## Design System
- **Theme**: Bright, colorful "brainrot/Roblox" game style — NOT dark/pirate
- **Background**: Sky-to-grass gradient (light blue → green)
- **Cards**: White with chunky borders, rounded corners (20px), drop shadows
- **Buttons**: Chunky game buttons with bottom shadows (3D effect)
- **Colors**: See CSS `:root` variables
- **Direction**: RTL (Hebrew), with LTR isolation for XP numbers
- **Animations**: bounceIn screen transitions, pulse on active nodes, floating brainrot characters

## Important Constraints
- **Hebrew RTL**: All text is right-to-left. Numbers in XP display need `direction: ltr; unicode-bidi: isolate`
- **No frameworks**: Must stay vanilla HTML/CSS/JS
- **Photo filenames**: Hebrew characters in filenames (e.g., `סבא מישה (מצד אבא).jpg`)
- **Photo face centering**: Each photo has custom `object-position` via `photoPos` field
- **Mobile adaptation**: Deferred — currently desktop-first. Will be addressed after all content is complete
- **Brainrot characters**: Must be actual PNG images, not emoji. Must be prominent and animated
- **Map scaling**: All 10 nodes + characters must fit in one viewport (100vh) without scrolling

## Common Tasks

### Adding/editing a quest
Edit `quests.js` — add to the `QUESTS` array following the existing pattern. Each quest needs: id, name, subtitle, icon, mapIcon, xp, message, color, intro, tasks[], artifact.

### Changing map node positions
Edit `MAP_POSITIONS` in `quests.js`. Values are percentages (x: 0-100, y: 0-100). Ensure all nodes stay within viewport (y max ~75%, x range 10-85%).

### Adding brainrot characters
Add PNG to `brainrot/` folder, add entry to `BRAINROT_CHARS` array in `app.js` with position, size, and animation.

### Deploying
```bash
git add . && git commit -m "description" && git push
```
GitHub Pages auto-deploys from `master` branch.

## Known Issues / TODO
- Map visual design needs improvement (consider using illustrated game map background image from Freepik)
- Quests 3-10 need parent-provided content (stories, achievement lists, photos)
- Hero Book PDF export is basic (browser print)
- Mobile responsive design not yet implemented
- Completed quests should show artifact preview on map (deferred)
- Presentation export not implemented yet
