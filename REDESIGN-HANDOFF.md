# Bar Mitzvah Quest — UI Restyle Handoff (for claude.ai/design)

> **Task:** Restyle an existing static PWA. **Output a new `style.css` only** (plus any image
> assets). Do **NOT** change HTML, do **NOT** rename/remove any class names or IDs, do **NOT**
> restructure the DOM, do **NOT** introduce a framework or rewrite any JavaScript. Reuse every
> existing selector so the styles still attach.

---

## 1. The vision

Replace the current dark **lava/volcanic** theme with a bright, airy **floating-islands-in-the-sky
fantasy** look (see reference image), for a Hebrew (RTL), PC-first kids' "hero quest" game.
The user is a 12-year-old who is autistic — keep the UI **calm, high-contrast, with clear
affordances and large tap targets**.

### Map screen (`#screen-home`)
- Each quest node becomes its own **floating island** in the sky, connected by glowing sky paths.
- The nodes already carry **state classes** — restyle them as:
  - `.map-node-done` → a fully-visible, lush **completed island**
  - `.map-node-next` → the **current island**, highlighted / gently pulsing
  - `.map-node-locked` → **hidden behind soft clouds** (cover with cloud puffs; no visible building/label)
- Restyle the existing SVG connector trail as a glowing path; completed segments in bright green.
- **All 10 nodes + the bottom "Hero Book" node must fit within `100vh` — no scrolling.**

### Quest screens (`#screen-quest`) and Hero Book (`#screen-book`)
- Same sky-fantasy palette. Turn the dark glass cards into bright **floating panels / soft cloud cards**.
- Keep the same layout, structure, and every class name.

### Color palette
| Role | Hex |
|------|-----|
| Sky gradient | `#AEDCF2` → `#D8EEF9` |
| Clouds | `#FFFFFF` w/ `#E6F2FB` shadow |
| Water / paths | `#46C8E6`, deep `#2A9FD0` |
| Islands | grass `#7CC674` / `#4F9E57`, cliffs `#8D7B6B` |
| Accents (categorical) | sakura pink `#F49FC0`, purple `#9C6FD0`, gold `#E8B84B`, teal `#3FB6A8`, red `#D6504A`, sky-blue `#5BA9E6` |
| Text | deep navy `#1C2B3A` on light panels (avoid pure black/white) |
| Path completed | bright green `#76E36B` |

---

## 2. Hard constraints (do not break)

- **`style.css` only** as code output (+ optional background/cloud/island image assets).
- **Preserve every class name, every `id`, and the DOM structure.** The JavaScript renders all
  content and queries these selectors — renaming any will break the app.
- Layout is **RTL** (Hebrew). Numeric XP values stay `direction: ltr; unicode-bidi: isolate`.
- **PC/desktop-first.** Map fits in `100vh`.
- Cap all images/videos at `max-height: 450px`.
- Do not touch interactive behavior (cards, drag-and-drop, quizzes, flip cards, video player,
  validation, progress) — appearance only.

---

## 3. Selector inventory (must be preserved)

### Screens & global shell
`screen-home` · `screen-quest` · `screen-book` · `task-block` · `task-info` · `task-label`
· `task-input` · `task-input-small` · `task-select` · `quest-intro` · `quest-message`
· `message-label` · `toast`

### Map (`#screen-home`)
`map-node` · `map-node-done` · `map-node-next` · `map-node-locked` · `map-node-start`
· `map-node-treasure` · `map-node-circle` · `map-node-next-circle` · `map-node-locked-circle`
· `map-node-treasure-circle` · `map-node-complete-circle` · `map-node-img` · `map-node-img-circle`
· `map-node-ftree-thumb` · `map-node-emoji` · `map-node-check` · `map-node-step`
· `map-node-label` · `map-node-subtitle` · `map-node-xp` · `node-color` · `brainrot`
· XP popup: `xp-overlay` · `xp-popup` · `xp-popup-icon` · `xp-gain` · `xp-message` · `xp-next`

### Hero Book (`#screen-book`)
`title-page` · `book-page` · `book-chapter-header` · `chapter-icon` · `book-message`
· `book-responses` · `book-response`

### Task types (group → classes)
- **family-flow (Q1):** `family-flow-block` · `family-grid` · `family-member` · `member-avatar`
  · `member-name` · `member-relation` · `flow-btn` · `flow-btn-prev` · `flow-nav` · `flow-photo`
  · `flow-name` · `flow-relation` · `flow-generation` · `flow-hero-message` · `flow-input-label`
  · `flow-word-input` · `flow-progress` · `flow-progress-bar` · `flow-progress-fill`
  · `flow-progress-text` · `ftree` · `ftree-map` · `ftree-mini` · `ftree-title`
  · `ftree-label-name` · `ftree-label-word`
- **checklist / multiselect (Q2):** `checklist` · `check-item` · `select-item` · `multiselect`
- **investigation-quiz (Q3):** `iq-container` · `iq-step` · `iq-step-header` · `iq-step-number`
  · `iq-step-title` · `iq-question` · `iq-options` · `iq-option-btn` · `iq-image` · `iq-image-wrap`
  · `iq-caption` · `iq-check` · `iq-reveal-story` · `iq-story` · `iq-completion`
- **hero-journey (Q4):** `hj-container` · `hj-accordion` · `hj-card` · `hj-card-header`
  · `hj-card-title` · `hj-card-icon` · `hj-card-body` · `hj-card-hint` · `hj-instruction`
- **power-stones (Q4):** `ps-grid` · `ps-stone` · `ps-icon` · `ps-text`
- **message-bubbles (Q4):** `mb-container` · `mb-bubble`
- **brain-meters (Q5):** `brain-meters` · `meter-row` · `meter-header` · `meter-name` · `meter-icon`
  · `meter-bar-track` · `meter-bar-fill` · `meter-levels` · `meter-level-btn` · `brain-map-section`
  · `brain-map-box` · `brain-map-title` · `brain-map-desc` · `brain-map-svg` · `brain-map-charts`
  · `brain-map-result` · `brain-map-reveal-btn`
- **brain-cards (Q5):** `brain-cards-grid` · `brain-card` · `brain-card-inner` · `brain-card-front`
  · `brain-card-back` · `brain-card-icon` · `brain-card-title` · `brain-card-desc` · `brain-bubble`
  · info card: `ic-inner` · `ic-front` · `ic-back` · `ic-icon` · `ic-title` · `ic-example`
- **drag-select (Q5):** `drag-select-options` · `drag-select-option`
- **twin-sort (Q6):** `ts-container` · `ts-stage-header` · `ts-stage-icon` · `ts-stage-title`
  · `ts-intro` · `ts-image` · `ts-image-wrap` · `ts-pool` · `ts-card` · `ts-bins` · `ts-bin`
  · `ts-bin-label` · `ts-bin-cards`
- **neta-envelope (Q6):** `ne-container` · `ne-locked-card` · `ne-locked-icon` · `ne-locked-title`
  · `ne-locked-text` · `ne-open-btn` · `ne-modal-overlay` · `ne-modal` · `ne-modal-title`
  · `ne-modal-body` · `ne-modal-close` · `ne-modal-feedback` · `ne-question` · `ne-question-header`
  · `ne-question-emoji` · `ne-question-text` · `ne-question-feedback` · `ne-options` · `ne-option`
  · `ne-option-text` · `ne-qfb-correct` · `ne-qfb-wrong` · `ne-unlocked` · `ne-unlocked-row`
  · `ne-video` · `ne-photo-container` · `ne-photo-frame` · `ne-greeting` · `ne-greeting-text`
  · `ne-signature` · `ne-success-header` · `ne-feedback-success` · `ne-completion-message`
- **trophy-cabinet / medal-factory / trophy-select (Q7):** `trophy-hero` · `trophy-hero-video`
  · `trophy-hero-caption` · `tc-wrap` · `tc-cabinet` · `tc-shelf` · `tc-medal` · `tc-medal-icon`
  · `tc-medal-text` · `tc-medal-pool` · `tc-counter` · `tc-counter-text` · `mf-wrap` · `mf-header`
  · `mf-header-icon` · `mf-header-title` · `mf-row` · `mf-prefix` · `mf-select` · `mf-select-wrap`
  · `mf-produce-btn` · `mf-result` · `mf-produced-medal` · `mf-produced-icon` · `mf-produced-text`
  · `mf-produced-detail` · `ml-completion` · `tselect-wrap` · `tselect-trophy` · `tselect-text`
  · `tselect-hint` · `tselect-golden`
- **secret-envelopes / superpower-survey (Q8):** `env-wrap` · `env-card` · `env-card-inner`
  · `env-card-front` · `env-card-back` · `env-icon` · `env-from` · `env-name` · `env-quote`
  · `env-hint` · `env-progress` · `superpower-survey` · `survey-person`
- **cinema-videos / emotion-board / support-map (Q9):** `cin-wrap` · `cin-video-box`
  · `cin-video-title` · `cin-hint` · `cin-overlay` · `cin-overlay-inner` · `cin-overlay-title`
  · `cin-overlay-close` · `emo-wrap` · `emo-btn` · `emo-icon` · `emo-text` · `support-map`
  · `support-cat` · `support-person`
- **card-builder (Q10):** `cb-wrap` · `cb-form` · `cb-card-block` · `cb-select` · `cb-reveal-btn`
  · `cb-card` · `cb-card-inner`(if present) · `cb-card-img-wrap` · `cb-card-img` · `cb-card-body`
  · `cb-card-title` · `cb-card-prefix` · `cb-card-value` · `cb-card-summary` · `cb-result`
  · `cb-finale` · `cb-confetti`

### Dynamic state / modifier classes (toggled by JS — STYLE THESE, never rename)
`done` · `next` · `locked` · `solved` · `completed` · `open` · `opened` · `flipped` · `visible`
· `claimed` · `selected` · `placed` · `correct` · `highlight` · `faded` · `saved` · `ready`
· `inspiration-card` · `inspiration-grid` · `animate-fadeIn` · `shadow-neon` · `drop-shadow-neon`

---

## 4. What to deliver back
- A new **`style.css`** mapped onto the selectors above.
- Any **image assets** (sky background, island tiles, cloud puffs for `.map-node-locked`,
  panel textures).
- Keep the file a drop-in replacement — no HTML/JS edits required to use it.
