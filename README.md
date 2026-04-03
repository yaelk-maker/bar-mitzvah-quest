# מסע הגיבורים שלי — My Hero's Journey

A gamified Bar Mitzvah identity quest app for Guy, built as a Progressive Web App.

## What Is This?

An RPG-style quest app where Guy (age 12.5) completes 10 identity missions leading up to his Bar Mitzvah on **July 19, 2026**. Each quest explores a different aspect of his identity — family roots, birth story, strengths, relationships — and produces a chapter in his personal "Hero Book."

The app uses a treasure map interface with a winding lava path, brainrot meme characters, and game-style XP progression to keep it fun and engaging.

## The 10 Quests

| # | Quest | Topic | Interactive Mechanics |
|---|-------|-------|---------------------|
| 1 | שורשים (Roots) | Family history & tree | Sequential family cards + illustrated tree overlay |
| 2 | משחק המשפחה (Family Game) | Kahoot family quiz | Kahoot guide + checklist |
| 3 | תיק החקירה המשפחתי (Family Investigation) | Birth story | 4-step investigation quiz with photo reveals |
| 4 | הגיבור שנולד (The Hero Born) | Prematurity & NICU | Accordion story cards + power stones + message bubbles |
| 5 | המוח שלי עובד אחרת (My Brain Works Differently) | CP & autism | Trait sliders + brain bubble energy map + flip cards |
| 6 | תאום אבל אני (Twin But Me) | Twin identity with Mika | Card sorting (drag & drop) + mad-libs blessing |
| 7 | הדרך שעשיתי (The Road I've Traveled) | Personal achievements | Trophy cabinet (drag & drop) + medal factory + golden trophy |
| 8 | הסופרפאוורס שלי (My Superpowers) | Strengths survey | Superpower survey (5 people) |
| 9 | האנשים שלי (My People) | Support network | Support map |
| 10 | מי אני עכשיו (Who I Am Now) | Personal manifesto | Story + manifesto |

## How It Works

- **Sequential unlocking**: Each quest unlocks only after completing the previous one
- **XP system**: 100 XP per quest, 1000 XP total
- **Validation**: Complete button only enables after interacting with every section
- **Auto-save**: All responses saved to localStorage in real time
- **Drag & Drop**: Quests 6 and 7 use HTML5 drag & drop with click fallback for mobile
- **Accessibility**: Clear visual affordances, instruction text, progress counters designed for autistic user
- **Hero Book**: After completing all quests, view/export the full identity book
- **Family tree**: Quest 1 builds an illustrated family tree from family member photos

## Tech Stack

- Vanilla HTML, CSS, JavaScript (no frameworks, no build step)
- Progressive Web App (installable on mobile)
- Hosted on GitHub Pages
- localStorage for data persistence
- SVG for brain bubble maps and map paths
- HTML5 Drag and Drop API
- Google Fonts: Heebo + Bungee + Frank Ruhl Libre

## Live App

**https://yaelk-maker.github.io/bar-mitzvah-quest/**

## Design

The visual style is a dark lava/volcanic game aesthetic:
- Lava map background with winding orange trail connecting quest nodes
- Bright green neon glow on completed quests, yellow pulse on next quest
- SAB (Steal a Brainrot) voxel characters scattered across the map
- Chunky game-style buttons with 3D shadow effects
- White cards with thick borders and rounded corners
- Wooden trophy cabinet with medal system
- Purple gradient medal factory
- Brain silhouette with colored energy bubbles

## Project Structure

```
index.html      -> Main HTML (3 screens: map, quest, book)
app.js          -> Application logic, rendering, validation (~1600 lines)
quests.js       -> Quest data model & map positions (~530 lines)
style.css       -> All styles (~2200 lines)
manifest.json   -> PWA configuration
photos/         -> Family photos, stage photos, video
brainrot/       -> SAB voxel character images (7 PNGs)
```

## Timeline

- **Now - April 2026**: Content preparation + design refinement (Quests 1-7 complete)
- **April - May 2026**: Complete Quests 8-10 content
- **May 2026**: App ready, Guy starts Quest 1
- **May - July 12**: ~1 quest per week (10 weeks)
- **July 12-18**: Finalize Hero Book + Bar Mitzvah presentation
- **July 19, 2026**: Bar Mitzvah

## Reset Progress

Full reset:
```javascript
localStorage.removeItem('bar-mitzvah-quest');
location.reload();
```

Reset from a specific quest (keep quests 1-N):
```javascript
let s = JSON.parse(localStorage.getItem('bar-mitzvah-quest'));
s.completedQuests = s.completedQuests.filter(id => id <= 5); // keep 1-5
[6,7,8,9,10].forEach(id => delete s.responses[id]);
s.currentQuest = null;
localStorage.setItem('bar-mitzvah-quest', JSON.stringify(s));
location.reload();
```
