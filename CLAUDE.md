# Bar Mitzvah Quest - Claude Development Guide

## Project Overview
Gamified Bar Mitzvah identity quest PWA for Guy (12.5, Bar Mitzvah July 19, 2026). RPG-style 10-step journey building toward "Hero Book" displayed at the event. Guy has cerebral palsy and autism; his twin sister is Mika.

## Tech Stack
- **Vanilla HTML/CSS/JS** — no frameworks, no build step
- **PWA** with manifest.json, localStorage state persistence
- **Hosted**: https://yaelk-maker.github.io/bar-mitzvah-quest/ (GitHub Pages, `master` branch)
- **Repo**: https://github.com/yaelk-maker/bar-mitzvah-quest (public)
- **Fonts**: Heebo (Hebrew) + Bungee (titles) from Google Fonts
- **Cache busting**: JS files use timestamp query params (auto-generated in index.html)

## File Structure
```
bar-mitzvah-quest/
├── index.html          # Main HTML: home map, quest, hero book (3 screens)
├── app.js              # State, navigation, quest rendering, map, validation
├── quests.js           # Quest data (10 quests) + MAP_POSITIONS
├── style.css           # Lava/volcanic game theme
├── map-bg.png          # Lava map background (itch.io asset pack)
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
│   └── [11 Hebrew-named family photos]
├── brainrot/           # SAB voxel character PNGs (7 figures, 90px each)
├── CLAUDE.md, README.md, STITCH_PROMPT.md
```

## Architecture

### State Management
- Key: `bar-mitzvah-quest` in localStorage
- Shape: `{ completedQuests: number[], responses: { [questId]: { [key]: value } }, currentQuest: number | null }`
- Functions: `loadState()` / `saveState()`
- Reset: `localStorage.removeItem('bar-mitzvah-quest')` in browser console

### Screens (toggled via `.active` CSS class)
| Screen | Purpose |
|--------|---------|
| `screen-home` | Treasure map with winding path, quest nodes, brainrot chars |
| `screen-quest` | Individual quest (height: 100vh; overflow-y: auto) |
| `screen-book` | Hero Book: all completed quest responses |

### Quest Progression
- Sequential unlock: Quest N+1 unlocks after Quest N completes
- Each quest: 100 XP (1000 total for all 10)
- Completed: green checkmark on map
- Next available: yellow pulse
- Locked: grey circle + lock icon (no name)

### Quest Validation
`getQuestValidation(questId)` checks per-task-type requirements. Complete button starts disabled, enables only when all sections pass. On click, re-validates and shows Hebrew toast with missing items.

### Map System
- Background: `map-bg.png` (lava, dark theme)
- Banner: 60px centered gradient header with "מסע הגיבורים של גיא"
- Nodes: x/y percentages defined in `MAP_POSITIONS` (quests.js)
- SVG curves: lava-orange trail + bright green completed overlay
- Characters: 7 SAB voxel PNGs, 90px each, static positioned (BRAINROT_CHARS in app.js)
- XP bar: gold on dark background
- No scrolling: all 10 nodes + chars fit in 100vh

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
| `kahoot-guide` | Numbered step list | 2 |
| `checklist` | Checkboxes | 2 |
| `multiselect` | Multiple choice checkboxes | — |
| `investigation-quiz` | Multi-step quiz + images, progressive unlock | 3 |
| `hero-journey` | Accordion collapsibles with instructions | 4 |
| `power-stones` | Toggle stone icons (strengths) | 4 |
| `message-bubbles` | Single-select cards | 4 |
| `brain-meters` | Sliders + buttons + brain map reveal | 5 |
| `brain-cards` | Flip cards + "זה אני!" claim buttons | 5 |
| `drag-select` | Single-select sentence cards | 5 |
| `twin-sort` | Drag & drop into 3 bins (Guy/Both/Mika); wrong answers shake/bounce | 6 |
| `twin-madlibs` | Dropdowns in sentence template | 6 |
| `trophy-hero-image` | Hero video/image with golden border | 7 |
| `trophy-cabinet` | Wooden shelf + drag & drop medals + live counter | 7 |
| `medal-factory` | Factory UI with custom dropdowns, produce button, animated result | 7 |
| `trophy-select` | Click placed medal → golden trophy pulse | 7 |
| `secret-envelopes` | 3D flip cards, corkboard Flexbox layout, nth-child rotations | 8 |
| `superpower-survey` | Name + power dropdown (5 people) | 8 |
| `support-map` | Categorized name + message inputs | 9 |
| `story` | Styled text block | — |

## Quest Status (April 2026)

| Quest | Status | Content |
|-------|--------|---------|
| 1 - שורשים | Complete | Family flow + tree |
| 2 - משחק המשפחה | Complete | Kahoot + checklist |
| 3 - תיק החקירה | Complete | 4-step quiz + images |
| 4 - הגיבור שנולד | Complete | Accordion + stones + bubbles |
| 5 - המוח שלי עובד אחרת | Complete | Meters + map + flip cards |
| 6 - תאום אבל אני | Complete | 2x drag & drop + mad-libs |
| 7 - הדרך שעשיתי | Complete | Cabinet + factory + trophy |
| 8 - הסופרפאוורס שלי | Complete | 8 corkboard flip cards (real messages) + power select |
| 9 - האנשים שלי | Partial | 10 cinema videos (5 real + 5 placeholder) + emotion board |
| 10 - מי אני עכשיו | Needs content | Personal manifesto |

## Design System
| Element | Value |
|---------|-------|
| Theme | Dark lava/volcanic game + bright neon |
| Background | `map-bg.png` (map); `#1a1025` (body) |
| Banner | Dark gradient, gold/orange/pink text (Bungee) |
| Cards | White, 20px rounded, chunky borders, shadows |
| Buttons | Chunky game style, bottom shadow (3D) |
| Completed nodes | Green neon glow |
| Next node | Yellow neon pulse |
| Locked nodes | Dark volcanic stone |
| Path: default | `#ff8f00` (lava orange) |
| Path: completed | `#76ff03` (bright green) |
| Text direction | RTL (Hebrew); XP numbers use ltr + isolate |
| Characters | 7 SAB voxel PNGs, 90px, static |
| Accessibility | Clear instructions, visual affordances, progress counters (autistic user friendly) |

## Constraints
- **Hebrew RTL**: Numbers in XP need `direction: ltr; unicode-bidi: isolate`
- **No frameworks**: Vanilla only
- **Photo filenames**: Hebrew characters (e.g., `סבא מישה (מצד אבא).jpg`); twins use `.jpeg`
- **Photo centering**: Custom `object-position` via `photoPos` field in quests.js
- **Brainrot**: SAB voxel PNGs only, all 90px, static (no emoji, no animations)
- **Map scaling**: All 10 nodes + chars fit in 100vh, no scrolling
- **Family tree image**: ~800KB compressed (original 6MB)
- **Cache busting**: Auto via timestamps in index.html

## Common Tasks

**Add/edit quest**: Edit `quests.js` QUESTS array. Required: id, name, subtitle, icon, mapIcon, xp, message, color, intro, tasks[], artifact.

**Add task type**: (1) Add case in `showQuest()` switch (app.js), (2) Add validation in `getQuestValidation()`, (3) Call `updateCompleteButton()` in handlers, (4) Add CSS in style.css.

**Add validation**: Edit `getQuestValidation()` in app.js. Add case for task type; push to `missing[]` if incomplete.

**Change map positions**: Edit `MAP_POSITIONS` in quests.js (x: 0-100, y: 0-100; max y ~75%).

**Change family tree photos**: Edit `treePositions` in `renderFamilyTree()` (app.js). Each: `idx` (member index), `left`/`top` (%), `cls` (ftree-gp, ftree-parent, ftree-child, ftree-hero).

**Add brainrot chars**: Edit `BRAINROT_CHARS` (app.js). Each: `{ img, top, right/left, size }` (all 90px). Add PNGs to brainrot/ folder.

**Deploy**: `git add . && git commit -m "description" && git push`. Auto-deploys from master (1-2 min). Cache busting is automatic.

**Reset progress**:
```javascript
// Full reset
localStorage.removeItem('bar-mitzvah-quest');
location.reload();

// Partial (keep quests 1-5, reset 6+)
let s = JSON.parse(localStorage.getItem('bar-mitzvah-quest'));
s.completedQuests = s.completedQuests.filter(id => id <= 5);
[6,7,8,9,10].forEach(id => delete s.responses[id]);
s.currentQuest = null;
localStorage.setItem('bar-mitzvah-quest', JSON.stringify(s));
location.reload();
```

## Known Issues / TODO
- Quests 8-10 need parent content
- Hero Book PDF export is basic (browser print)
- Mobile responsive design incomplete
- Completed quest artifact preview on map (deferred)
- Presentation export not implemented
- Family tree photo positions may need fine-tuning per screen size
