# -*- coding: utf-8 -*-
"""Build the final Bar Mitzvah movie in TWO versions by appending the family
blessing videos to the Hero-Movie highlight reel:

  finale/Hero-Movie-Short.mp4  — Hero-Movie + only the "מזל טוב גיא" moment from each blessing
  finale/Hero-Movie-Long.mp4   — Hero-Movie + the FULL blessing from every family member

The "mazal tov" moments come from finale/blessing_segments.json. A null segment
falls back to the first `default_seconds` of the clip. Run with --transcribe on
a machine with internet access to auto-detect the moments with faster-whisper
(word-level timestamps, searching for "מזל טוב"), which rewrites the json.

Usage (from the repo root):
    pip install pillow imageio-ffmpeg python-bidi        # one-time
    python finale/make_blessings.py                      # build both versions
    python finale/make_blessings.py --transcribe         # auto-fill segments first (needs internet)
    python finale/make_blessings.py --skip-base          # blessings-only movies (no Hero-Movie intro)

New blessing videos: drop the file into "photos/Videos - step 9/" and add/uncomment
its entry in BLESSINGS below, then rerun. Missing files are skipped with a warning.
"""
import os, sys, json, re, subprocess, shutil

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont
from bidi.algorithm import get_display

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIDS = os.path.join(PROJ, "photos", "Videos - step 9")
FIN = os.path.join(PROJ, "finale")
BUILD = os.path.join(FIN, "_build_blessings")
SEGMENTS_JSON = os.path.join(FIN, "blessing_segments.json")
BASE_MOVIE = os.path.join(FIN, "Hero-Movie.mp4")

W, H, FPS = 1280, 720, 30
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
if not os.path.exists(FONT_BOLD):  # Windows fallback (Arial has Hebrew)
    FONT_BOLD = r"C:\Windows\Fonts\arialbd.ttf"

# Order = closest family first, then the rest. (name, filename)
BLESSINGS = [
    ("אבא ואמא",            "סרטון - אבא ואמא.mp4"),
    ("נטע ומיקה",           "סרטון - נטע ומיקה.mp4"),
    ("סווטה",               "סרטון - סווטה.mp4"),
    ("מרינה ומישה",         "סרטון - מרינה ומישה.mp4"),
    ("משפחת שפירא",         "סרטון - משפחת שפירא.mp4"),
    ("אירה ותום",           "סרטון - אירה ותום.mp4"),
    ("רעיה",                "סרטון - רעיה.mp4"),
    ("אליה",                "סרטון - אליה.mp4"),
    ("ציליה",               "סרטון - ציליה.mp4"),
    ("יובל והמשפחה",        "סרטון - יובל והמשפחה.mp4"),
    ("רפי",                 "סרטון - רפי.mp4"),
]

ENC = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "24", "-pix_fmt", "yuv420p",
       "-r", str(FPS), "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2"]


def run(args):
    p = subprocess.run(args, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    if p.returncode != 0:
        raise RuntimeError("ffmpeg failed:\n" + p.stderr.decode("utf-8", "replace")[-2000:])


def duration_of(path):
    p = subprocess.run([FFMPEG, "-i", path], stderr=subprocess.PIPE)
    m = re.search(rb"Duration: (\d+):(\d+):(\d+\.\d+)", p.stderr)
    if not m:
        raise RuntimeError("no duration for " + path)
    h, mi, s = int(m.group(1)), int(m.group(2)), float(m.group(3))
    return h * 3600 + mi * 60 + s


def heb(text):
    return get_display(text)


# ---------------- PIL cards / overlays ----------------
def sky_gradient(draw):
    top, bottom = (142, 201, 240), (255, 175, 196)  # sky blue -> soft pink
    for y in range(H):
        t = y / H
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        draw.line([(0, y), (W, y)], fill=c)


def confetti(draw):
    import random
    random.seed(7)
    colors = [(255, 122, 182), (147, 51, 234), (251, 140, 0), (34, 197, 94), (56, 189, 248)]
    for _ in range(60):
        x, y = random.randint(0, W), random.randint(0, H)
        r = random.randint(3, 7)
        draw.ellipse([x, y, x + r, y + r], fill=random.choice(colors))


def make_card(title, sub, out_png):
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    sky_gradient(d)
    confetti(d)
    f1 = ImageFont.truetype(FONT_BOLD, 84)
    f2 = ImageFont.truetype(FONT_BOLD, 40)
    t1 = heb(title)
    w1 = d.textlength(t1, font=f1)
    # soft white panel behind the text
    pad = 46
    d.rounded_rectangle([(W - w1) / 2 - pad, H / 2 - 120, (W + w1) / 2 + pad, H / 2 + 40 + (70 if sub else 0)],
                        radius=34, fill=(255, 255, 255, 235), outline=(76, 29, 149), width=5)
    d.text(((W - w1) / 2, H / 2 - 96), t1, font=f1, fill=(76, 29, 149))
    if sub:
        t2 = heb(sub)
        w2 = d.textlength(t2, font=f2)
        d.text(((W - w2) / 2, H / 2 - 4), t2, font=f2, fill=(219, 39, 119))
    img.save(out_png)


def make_lower_third(name, out_png):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(FONT_BOLD, 42)
    t = heb("ברכה מ" + name)
    w = d.textlength(t, font=f)
    x1, y1 = W - w - 110, H - 118
    d.rounded_rectangle([x1, y1, W - 40, H - 48], radius=26, fill=(255, 122, 182, 225), outline=(255, 255, 255, 255), width=4)
    d.text((x1 + 34, y1 + 11), t, font=f, fill=(255, 255, 255))
    img.save(out_png)


# ---------------- ffmpeg helpers ----------------
def card_to_video(png, secs, out_mp4):
    run([FFMPEG, "-y", "-loop", "1", "-t", str(secs), "-i", png,
         "-f", "lavfi", "-t", str(secs), "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
         "-shortest", *ENC,
         "-vf", f"scale={W}:{H},fade=t=in:d=0.4,fade=t=out:st={secs-0.4:.2f}:d=0.4",
         out_mp4])


def encode_clip(src, out_mp4, start=None, end=None, lower_third=None):
    """Uniform 720p encode: blurred-pad to 16:9, optional trim + name overlay,
    gentle audio fades + loudness normalization."""
    dur = duration_of(src)
    if start is not None:
        start = max(0.0, min(start, max(0.0, dur - 1)))
        end = min(end if end is not None else dur, dur)
        clip_len = end - start
    else:
        start, clip_len = 0.0, dur
    inputs = [FFMPEG, "-y", "-ss", f"{start:.2f}", "-t", f"{clip_len:.2f}", "-i", src]
    vf = (f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},gblur=sigma=18[bg];"
          f"[0:v]scale={W}:{H}:force_original_aspect_ratio=decrease[fg];"
          f"[bg][fg]overlay=(W-w)/2:(H-h)/2")
    if lower_third:
        inputs += ["-i", lower_third]
        vf += f"[v0];[v0][1:v]overlay=0:0"
    vf += f",fade=t=in:d=0.25,fade=t=out:st={max(0.0, clip_len-0.3):.2f}:d=0.3,fps={FPS}[vout]"
    af = f"[0:a]loudnorm=I=-17:TP=-1.5,afade=t=in:d=0.25,afade=t=out:st={max(0.0, clip_len-0.3):.2f}:d=0.3[aout]"
    run(inputs + ["-filter_complex", vf + ";" + af, "-map", "[vout]", "-map", "[aout]", *ENC, out_mp4])


def reencode_base(out_mp4):
    run([FFMPEG, "-y", "-i", BASE_MOVIE,
         "-filter_complex",
         f"[0:v]scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,fps={FPS}[vout];"
         f"[0:a]aresample=48000[aout]",
         "-map", "[vout]", "-map", "[aout]", *ENC, out_mp4])


def concat(parts, out_mp4):
    lst = os.path.join(BUILD, "concat.txt")
    with open(lst, "w", encoding="utf-8") as f:
        for p in parts:
            f.write("file '" + p.replace("'", "'\\''") + "'\n")
    run([FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", out_mp4])


# ---------------- segments ----------------
def load_segments():
    if os.path.exists(SEGMENTS_JSON):
        with open(SEGMENTS_JSON, encoding="utf-8") as f:
            return json.load(f)
    return {"default_seconds": 6, "segments": {fname: None for _, fname in BLESSINGS}}


def save_segments(data):
    with open(SEGMENTS_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def transcribe_segments(data):
    """Find the 'מזל טוב' moment in each clip with faster-whisper (needs internet
    the first time, to download the model)."""
    from faster_whisper import WhisperModel
    model = WhisperModel("small", device="cpu", compute_type="int8")
    for name, fname in BLESSINGS:
        src = os.path.join(VIDS, fname)
        if not os.path.exists(src) or data["segments"].get(fname):
            continue
        print("  transcribing:", fname)
        segs, _ = model.transcribe(src, language="he", word_timestamps=True)
        found = None
        words = [w for s in segs for w in (s.words or [])]
        for i, wo in enumerate(words):
            if "מזל" in wo.word:
                nxt = words[i + 1].word if i + 1 < len(words) else ""
                if "טוב" in nxt or "טוב" in wo.word:
                    # capture a warm window around the moment
                    end_i = min(i + 4, len(words) - 1)
                    found = [max(0.0, wo.start - 0.8), words[end_i].end + 0.6]
                    break
        if found:
            data["segments"][fname] = [round(found[0], 2), round(found[1], 2)]
            print(f"    מזל טוב at {found[0]:.1f}s–{found[1]:.1f}s")
        else:
            print("    not found — keeping fallback")
    save_segments(data)


# ---------------- main ----------------
def main():
    transcribe = "--transcribe" in sys.argv
    skip_base = "--skip-base" in sys.argv
    os.makedirs(BUILD, exist_ok=True)

    data = load_segments()
    # make sure every configured blessing has a key
    for _, fname in BLESSINGS:
        data["segments"].setdefault(fname, None)
    save_segments(data)

    if transcribe:
        try:
            transcribe_segments(data)
        except Exception as e:
            print("transcription unavailable (%s) — using segments file / fallback" % e)

    present = [(n, f) for n, f in BLESSINGS if os.path.exists(os.path.join(VIDS, f))]
    missing = [f for _, f in BLESSINGS if not os.path.exists(os.path.join(VIDS, f))]
    for f in missing:
        print("! missing (skipped for now):", f)

    # shared cards
    sec_card_png = os.path.join(BUILD, "card-blessings.png")
    make_card("ברכות מהמשפחה", "האנשים שאוהבים אותך מברכים אותך", sec_card_png)
    sec_card = os.path.join(BUILD, "card-blessings.mp4")
    card_to_video(sec_card_png, 3.0, sec_card)

    outro_png = os.path.join(BUILD, "card-outro.png")
    make_card("!מזל טוב גיא", "אוהבים אותך עד השמיים", outro_png)
    outro = os.path.join(BUILD, "card-outro.mp4")
    card_to_video(outro_png, 4.0, outro)

    base = None
    if not skip_base:
        base = os.path.join(BUILD, "base-720.mp4")
        if not os.path.exists(base):
            print("re-encoding Hero-Movie base...")
            reencode_base(base)

    long_parts, short_parts = [], []
    if base:
        long_parts.append(base)
        short_parts.append(base)
    long_parts.append(sec_card)
    short_parts.append(sec_card)

    default_s = float(data.get("default_seconds", 6))
    for name, fname in present:
        src = os.path.join(VIDS, fname)
        safe = re.sub(r"[^\w]+", "_", fname)
        lt = os.path.join(BUILD, f"lt_{safe}.png")
        make_lower_third(name, lt)

        full = os.path.join(BUILD, f"full_{safe}.mp4")
        if not os.path.exists(full):
            print("encoding full:", fname)
            encode_clip(src, full, lower_third=lt)
        long_parts.append(full)

        seg = data["segments"].get(fname)
        if seg:
            start, end = float(seg[0]), float(seg[1])
        else:
            start, end = 0.0, default_s
        snip = os.path.join(BUILD, f"snip_{safe}.mp4")
        print(f"encoding snippet: {fname} [{start:.1f}s–{end:.1f}s]")
        encode_clip(src, snip, start=start, end=end, lower_third=lt)
        short_parts.append(snip)

    long_parts.append(outro)
    short_parts.append(outro)

    out_long = os.path.join(FIN, "Hero-Movie-Long.mp4")
    out_short = os.path.join(FIN, "Hero-Movie-Short.mp4")
    print("concatenating long version...")
    concat(long_parts, out_long)
    print("concatenating short version...")
    concat(short_parts, out_short)
    for p in (out_long, out_short):
        print("wrote %s (%.1f MB, %.0f sec)" % (os.path.basename(p), os.path.getsize(p) / 1e6, duration_of(p)))


if __name__ == "__main__":
    main()
