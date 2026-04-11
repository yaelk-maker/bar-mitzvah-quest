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
| 8 | הסופרפאוורס שלי (My Superpowers) | Secret messages | 8 scattered envelope cards with personal messages + power select |
| 9 | האנשים שלי (My People) | Video greetings | Title cards → overlay video player + emotion board |
| 10 | מי אני עכשיו (Who I Am Now) | Personal manifesto | Story + manifesto |

## How It Works

- **Sequential unlocking**: Each quest unlocks only after completing the previous one
- **XP system**: 100 XP per quest, 1000 XP total
- **Validation**: Complete button only enables after interacting with every section
- **Auto-save**: All responses saved to localStorage in real time
- **Drag & Drop**: Quests 6 and 7 use HTML5 drag & drop with click fallback
- **Envelope cards**: Quest 8 uses scattered expand/collapse cards with asymmetric sizes
- **Video overlay**: Quest 9 hides videos behind title cards; click opens fullscreen overlay player
- **Accessibility**: Clear visual affordances, instruction text, progress counters designed for autistic user
- **Hero Book**: After completing all quests, view/export the full identity book
- **Family tree**: Quest 1 builds an illustrated family tree from family member photos (displayed at 1000px+)

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

The visual style is a dark glassmorphism gaming aesthetic (RPG quest log feel):
- Lava map background with winding orange trail connecting 90px quest nodes
- Bright green neon glow on completed quests, yellow pulse on next quest
- SAB (Steal a Brainrot) voxel characters (120px) scattered across the map
- Dark glass cards (`rgba(15,15,35,0.75)`) with `backdrop-filter: blur` and cyan neon borders
- Light text on dark backgrounds with neon accent colors
- Full-width PC layout (1400px quest body, 900px task blocks centered)
- Chunky game-style buttons with neon glow on hover
- Wooden trophy cabinet with medal system
- Purple gradient medal factory
- Brain silhouette with colored energy bubbles
- Custom dark scrollbar with cyan thumb
- Scattered asymmetric card layouts for envelopes and video cards

## Project Structure

```
index.html              -> Main HTML (3 screens: map, quest, book)
app.js                  -> Application logic, rendering, validation (~1900 lines)
quests.js               -> Quest data model & map positions (~530 lines)
style.css               -> All styles (~3200 lines, dark glassmorphism theme)
manifest.json           -> PWA configuration
photos/                 -> Family photos, stage photos, video
photos/Videos - step 9/ -> Quest 9 greeting videos
brainrot/               -> SAB voxel character images (7 PNGs, 120px)
```

## Timeline

- **Now - April 2026**: Content preparation + design refinement (Quests 1-8 complete, Quest 9 partial)
- **April - May 2026**: Complete Quest 9 videos + Quest 10 content
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
