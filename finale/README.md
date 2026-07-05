# Finale — Hero Movie & Hero Storybook

Two keepsake deliverables that summarize Guy's 10-step journey, for the Bar Mitzvah (19 July 2026).

## Files
- **`Hero-Movie.mp4`** — ~3:05 highlight reel: title → the 10 steps (family, origin story, the fighter
  born premature, the special brain, the twins + Neta's blessing, achievements, the family's "super-power"
  messages, the people, who-I-am-now) → "מזל טוב גיא!" Set to `Song for the movie.mpeg` (Suno track),
  1080p, Hebrew RTL captions, Ken-Burns zoom + crossfades. Audio fades out at the end.
- **`Hero-Storybook.pdf`** — print-ready A4 (15 pages) version of the same journey, with real family photos,
  the family blessing messages, and **QR-code greeting cards** that open each greeting video (hosted on GitHub Pages).
- **`../storybook.html`** — the editable source of the storybook (lives in the repo root so `photos/...`
  paths resolve). Open it in a browser and use the "🖨️ הדפס / שמור כ-PDF" button to re-export the PDF.

## How to rebuild (Windows, no admin needed)
```bash
pip install imageio-ffmpeg "qrcode[pil]" pymupdf   # one-time
python finale/make_storybook.py                     # regenerates ../storybook.html
python finale/make_movie.py                         # regenerates finale/Hero-Movie.mp4
```
- `make_movie.py` renders each scene as HTML → screenshots it with headless Chrome → assembles the MP4 with
  a bundled ffmpeg (`imageio-ffmpeg`). Intermediate frames go to `finale/_build/` (safe to delete).
- Both scripts are **repo-relative** — run them from the repo root. They require Google Chrome installed at
  the default path and an internet connection (for the Google Fonts used on the slides/pages).

## To swap a photo or edit text
- Photos: replace the file in `../photos/` (keep the same name) and rerun.
- Movie narrative / durations: edit the `S.append(...)` scene list in `make_movie.py`.
- Storybook text / messages: edit `MESSAGES`, `GREETINGS`, and the `b1..b10` bodies in `make_storybook.py`.
