# מסע הגיבורים שלי — My Hero's Journey

A gamified Bar Mitzvah identity quest app for Guy, built as a Progressive Web App.

## What Is This?

An RPG-style quest app where Guy (age 12.5) completes 10 identity missions leading up to his Bar Mitzvah on **July 19, 2026**. Each quest explores a different aspect of his identity — family roots, birth story, strengths, relationships — and produces a chapter in his personal "Hero Book."

The app uses a treasure map interface with a winding path, brainrot meme characters, and game-style XP progression to keep it fun and engaging.

## The 10 Quests

| # | Quest | Topic | Identity Message |
|---|-------|-------|-----------------|
| 1 | שורשים (Roots) | Family history & tree | "אני חלק מסיפור גדול" |
| 2 | משחק המשפחה (Family Game) | Kahoot family quiz | "אני מכיר את המשפחה שלי" |
| 3 | הסיפור שלפניי (The Story Before Me) | Birth story interview | "נולדתי עם ייעוד" |
| 4 | הלוחם הקטן (The Little Warrior) | Prematurity & NICU | "כבר בהתחלה הייתי גיבור" |
| 5 | המוח שלי עובד אחרת (My Brain Works Differently) | CP & autism | "אני מבין את הגוף והמוח שלי" |
| 6 | תאום אבל אני (Twin But Me) | Twin identity with Mika | "אני תאום ואני גם אני" |
| 7 | הדרך שעשיתי (The Road I've Traveled) | Personal achievements | "ראו כמה רחוק הגעתי" |
| 8 | הסופרפאוורס שלי (My Superpowers) | Strengths survey | "יש לי כוחות מיוחדים" |
| 9 | האנשים שלי (My People) | Support network | "אני לא לבד במסע" |
| 10 | מי אני עכשיו (Who I Am Now) | Personal manifesto | "זה אני, בן 13, ואני גאה" |

## How It Works

- **Sequential unlocking**: Each quest unlocks only after completing the previous one
- **XP system**: 100 XP per quest, 1000 XP total
- **Auto-save**: All responses saved to localStorage in real time
- **Hero Book**: After completing all quests, view/export the full identity book
- **Family tree**: Quest 1 builds an illustrated family tree from family member photos

## Tech Stack

- Vanilla HTML, CSS, JavaScript (no frameworks)
- Progressive Web App (installable on mobile)
- Hosted on GitHub Pages
- localStorage for data persistence
- Google Fonts: Heebo + Bungee

## Live App

**https://yaelk-maker.github.io/bar-mitzvah-quest/**

## Design

The visual style is a bright, colorful "brainrot/game" aesthetic:
- Sky-to-grass gradient background
- Treasure map home screen with winding dirt trail
- Animated brainrot meme characters (Skibidi, Doge, Among Us, etc.)
- Chunky game-style buttons with 3D shadow effects
- White cards with thick borders and rounded corners

## Project Structure

```
index.html      → Main HTML (3 screens: map, quest, book)
app.js          → Application logic & rendering
quests.js       → Quest data model & map positions
style.css       → All styles
manifest.json   → PWA configuration
photos/         → Family member photos
brainrot/       → Brainrot character images
```

## Timeline

- **Now – April 2026**: Content preparation + design refinement
- **May 2026**: App ready, Guy starts Quest 1
- **May – July 12**: ~1 quest per week (10 weeks)
- **July 12-18**: Finalize Hero Book + Bar Mitzvah presentation
- **July 19, 2026**: Bar Mitzvah

## Reset Progress

Open browser console and run:
```javascript
localStorage.removeItem('bar-mitzvah-quest');
location.reload();
```
