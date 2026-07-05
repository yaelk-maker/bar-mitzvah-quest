# -*- coding: utf-8 -*-
"""Build Guy's Bar Mitzvah journey movie: HTML scenes -> Chrome PNG -> ffmpeg MP4."""
import os, subprocess, urllib.parse, pathlib, html, sys

# Repo-relative: this script lives in <repo>/finale/. Build artifacts go to <repo>/finale/_build.
PROJ   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRATCH= os.path.join(PROJ, "finale", "_build")
FRAMES = os.path.join(SCRATCH, "frames")
SCENES = os.path.join(SCRATCH, "scenes")
CHROME = r"C:/Program Files/Google/Chrome/Application/chrome.exe"
SONG   = os.path.join(PROJ, "Song for the movie.mpeg")
OUT    = os.path.join(PROJ, "finale", "Hero-Movie.mp4")
os.makedirs(FRAMES, exist_ok=True); os.makedirs(SCENES, exist_ok=True)

import imageio_ffmpeg
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

def furl(rel):
    """file:// URL for a photo in the project (rel may include 'photos/...' or root file)."""
    p = pathlib.Path(PROJ) / rel
    return "file:///" + urllib.parse.quote(str(p).replace("\\", "/"))

def P(name):   # photo in photos/
    return furl("photos/" + name)

FPS = 30
XF  = 1.0  # crossfade seconds

# ---- shared CSS ----
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Heebo:wght@400;700;800;900&family=Bungee&family=Baloo+2:wght@600;700;800&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1920px;height:1080px;overflow:hidden;font-family:'Heebo','Segoe UI',Arial,sans-serif}
.stage{width:1920px;height:1080px;position:relative;display:flex;flex-direction:column;
  align-items:center;justify-content:center;
  background:linear-gradient(180deg,#8fd0ec 0%,#b9e4f3 40%,#dff3e8 100%);overflow:hidden}
.cloud{position:absolute;border-radius:50%;background:rgba(255,255,255,.75);filter:blur(2px)}
.chip{position:absolute;top:64px;right:64px;font-family:'Baloo 2';font-weight:800;
  font-size:40px;color:#fff;background:linear-gradient(90deg,#FF7AB6,#DB2777);
  padding:14px 44px;border-radius:999px;box-shadow:0 12px 28px rgba(219,39,119,.35)}
.step-no{position:absolute;top:60px;left:64px;font-family:'Bungee';font-size:42px;color:#fff;
  -webkit-text-stroke:2px #6D28D9;opacity:.9}
.title{font-family:'Bungee';font-size:118px;line-height:1.05;color:#fff;text-align:center;
  -webkit-text-stroke:4px #6D28D9;text-shadow:0 8px 0 rgba(109,40,217,.30),0 18px 40px rgba(0,0,0,.25)}
.subtitle{margin-top:34px;font-size:54px;font-weight:800;color:#fff;background:rgba(109,40,217,.55);
  padding:16px 50px;border-radius:999px;backdrop-filter:blur(3px)}
.bigstmt{font-family:'Baloo 2';font-weight:800;font-size:92px;line-height:1.25;color:#120D0E;
  text-align:center;max-width:1500px;text-shadow:0 2px 0 rgba(255,255,255,.6)}
.bigstmt .hl{color:#DB2777}
.cap{font-family:'Baloo 2';font-weight:800;font-size:58px;color:#120D0E;text-align:center;
  background:rgba(255,255,255,.9);padding:22px 56px;border-radius:28px;max-width:1500px;
  box-shadow:0 16px 40px rgba(0,0,0,.16)}
.frame{border-radius:30px;overflow:hidden;border:14px solid #fff;background:#e9e9e9;
  box-shadow:0 28px 70px rgba(0,0,0,.28)}
.frame img{width:100%;height:100%;object-fit:cover;display:block}
.row{display:flex;gap:50px;align-items:center;justify-content:center}
.col{display:flex;flex-direction:column;gap:40px;align-items:center}
.portrait{width:560px;height:720px}
.land{width:880px;height:620px}
.sq{width:430px;height:430px}
.grid{display:flex;flex-wrap:wrap;gap:30px;justify-content:center;align-items:center;max-width:1640px}
.gcell{width:300px;height:330px;border-radius:24px;overflow:hidden;border:10px solid #fff;
  box-shadow:0 18px 40px rgba(0,0,0,.22);background:#ddd;position:relative}
.gcell img{width:100%;height:100%;object-fit:cover;object-position:center 30%}
.gname{position:absolute;bottom:0;left:0;right:0;background:rgba(109,40,217,.78);color:#fff;
  font-weight:800;font-size:30px;text-align:center;padding:8px 4px}
.quote{max-width:1400px;background:#fff;border-radius:36px;padding:70px 80px;
  box-shadow:0 30px 80px rgba(0,0,0,.22);position:relative;border-top:18px solid #FF7AB6}
.qmark{font-family:'Bungee';font-size:150px;color:#FFAFC4;line-height:.2;height:60px}
.qtext{font-size:60px;font-weight:700;color:#120D0E;line-height:1.5}
.qfrom{margin-top:34px;font-family:'Baloo 2';font-weight:800;font-size:46px;color:#DB2777;text-align:left}
.heart{font-size:90px;margin-top:10px}
.hero-panel{background:rgba(12,8,22,.46);backdrop-filter:blur(6px);border:3px solid rgba(255,255,255,.25);
  border-radius:48px;padding:64px 96px;display:flex;flex-direction:column;align-items:center;
  box-shadow:0 30px 90px rgba(0,0,0,.45)}
.title.strong{text-shadow:0 6px 0 rgba(109,40,217,.55),0 14px 36px rgba(0,0,0,.6)}
"""

CLOUDS = """
<div class="cloud" style="width:280px;height:120px;top:120px;left:120px"></div>
<div class="cloud" style="width:200px;height:90px;top:80px;right:240px"></div>
<div class="cloud" style="width:240px;height:100px;bottom:120px;left:260px"></div>
<div class="cloud" style="width:180px;height:80px;bottom:90px;right:160px"></div>
"""

def page(body, bg_style=""):
    return f"""<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8">
<style>{CSS}{bg_style}</style></head><body><div class="stage">{CLOUDS}{body}</div></body></html>"""

def chip(t):     return f'<div class="chip">{html.escape(t)}</div>' if t else ""
def stepno(t):   return f'<div class="step-no">{html.escape(t)}</div>' if t else ""

# ---------- scene builders ----------
def cover(title, subtitle, bg):
    bgs = f".stage{{background:linear-gradient(rgba(8,6,16,.55),rgba(109,40,217,.55)),url('{bg}') center/cover}}"
    body = f'<div class="hero-panel"><div class="title strong">{title}</div><div class="subtitle">{html.escape(subtitle)}</div></div>'
    return page(body, bgs)

def textscene(stmt, step_chip="", step="", accent="#DB2777"):
    body = chip(step_chip)+stepno(step)+f'<div class="bigstmt">{stmt}</div>'
    return page(body)

def single(photo, cap, klass="portrait", step_chip="", step=""):
    body = chip(step_chip)+stepno(step)+f"""<div class="col">
      <div class="frame {klass}"><img src="{photo}"></div>
      <div class="cap">{cap}</div></div>"""
    return page(body)

def duo(p1, p2, cap, klass="portrait", step_chip="", step=""):
    body = chip(step_chip)+stepno(step)+f"""<div class="col"><div class="row">
      <div class="frame {klass}"><img src="{p1}"></div>
      <div class="frame {klass}"><img src="{p2}"></div></div>
      <div class="cap">{cap}</div></div>"""
    return page(body)

def grid(cells, title, step_chip="", step=""):
    g = "".join(f'<div class="gcell"><img src="{src}"><div class="gname">{html.escape(n)}</div></div>' for src,n in cells)
    body = chip(step_chip)+stepno(step)+f'<div class="col"><div class="cap">{title}</div><div class="grid">{g}</div></div>'
    return page(body)

def quote(text, frm, step_chip="", step=""):
    body = chip(step_chip)+stepno(step)+f"""<div class="quote">
      <div class="qmark">&#8221;</div><div class="qtext">{text}</div>
      <div class="qfrom">{html.escape(frm)}</div></div>"""
    return page(body)

def videoscene(rel, cap, step_chip="", step=""):
    """A real video clip scene (muted; the soundtrack keeps playing). Returns a
    ('VIDEO', abs_path, overlay_html) marker; the overlay (chip + caption) is
    rendered to a transparent PNG and composited over the clip at assembly."""
    ov_css = (".stage{background:transparent !important}"
              ".cloud{display:none}"
              f".vcap{{position:absolute;bottom:70px;left:50%;transform:translateX(-50%);}}")
    body = chip(step_chip) + stepno(step) + f'<div class="vcap"><div class="cap">{cap}</div></div>'
    return ("VIDEO", os.path.join(PROJ, rel), page(body, ov_css))

def finale(title, sub, bg):
    bgs = f".stage{{background:linear-gradient(rgba(8,6,16,.50),rgba(219,39,119,.50)),url('{bg}') center/cover}}"
    body = f'<div class="hero-panel"><div class="title strong">{title}</div><div class="subtitle">{html.escape(sub)}</div><div class="heart">🎉❤️🎉</div></div>'
    return page(body, bgs)

# ---------- the narrative ----------
MAP = furl("map-v3.jpg")
S = []  # (html, duration_seconds)

S.append((cover('מסע הגיבורים<br>של גיא', 'הסיפור שלי — לקראת בר המצווה · 19.7.2026', MAP), 7.5))
S.append((textscene('לכל גיבור יש <span class="hl">סיפור התחלה</span>…<br>זה שלי.', step="✦"), 6))

# Step 1 - roots
S.append((grid([
    (P("סבא מישה (מצד אבא).jpg"),"סבא מישה"),
    (P("סבתא מרינה (מצד אבא).JPG"),"סבתא מרינה"),
    (P("סבא אלכס (מצד אמא).jpeg"),"סבא אלכס"),
    (P("סבתא סווטה (מצד אמא).jpeg"),"סבתא סווטה"),
], 'עץ השורשים — אני חלק מסיפור גדול', step_chip="שלב 1 · השורשים", step="1"), 11))
S.append((grid([
    (P("אבא איליה.jpg"),"אבא איליה"),
    (P("אמא יעל.jpg"),"אמא יעל"),
    (P("דודה מצד אבא - אירה.jpg"),"דודה אירה"),
    (P("דודה מצד אימא - ג'ני.jpeg"),"דודה ג׳ני"),
], 'המשפחה שגידלה אותי באהבה', step_chip="שלב 1 · השורשים", step="1"), 10))

# Step 3 - investigation / origin
S.append((single(P("placeholder_parents_young.jpg"),
    'איך הכל התחיל — אמא ואבא,<br>ונסיעה אחת לאילת ששינתה הכל', klass="land",
    step_chip="שלב 3 · חקירה משפחתית", step="3"), 10))
S.append((single(P("placeholder_neta_baby.jpg"),
    'קודם הגיעה נטע — האחות הבכורה.<br>היינו שלושה, וחלמנו לגדול', klass="land",
    step_chip="שלב 3 · חקירה משפחתית", step="3"), 9.5))
S.append((single(P("placeholder_ultrasound.jpg"),
    'הפתעה כפולה: <span style="color:#DB2777">שני לבבות פועמים</span> 💕<br>אני ומיקה — צוות מנצח כבר מהבטן', klass="land",
    step_chip="שלב 3 · חקירה משפחתית", step="3"), 10.5))

# Step 4 - hero born
S.append((single(P("placeholder_nicu_twins.jpg"),
    'נולדתי מוקדם, פג קטנטן ולוחם.<br>כבר אז — הייתי גיבור', klass="land",
    step_chip="שלב 4 · הגיבור שנולד", step="4"), 11))
S.append((textscene(
    'מהקרב הראשון יצאתי עם כוחות:<br><span class="hl">חוזק · אומץ · עקשנות · נחישות · אמונה</span>',
    step_chip="שלב 4 · הגיבור שנולד", step="4"), 8))

# Step 5 - brain
S.append((textscene(
    'המוח שלי עובד <span class="hl">אחרת</span> —<br>וזה בדיוק הכוח שלי 🧠',
    step_chip="שלב 5 · המוח המיוחד שלי", step="5"), 8))

# Step 6 - tribe / twins
S.append((duo(P("placeholder_twins_babies.jpeg"), P("placeholder_twins_kids.jpeg"),
    'אני תאום — ואני גם אני.<br>מיקה לצידי בכל צעד', klass="sq",
    step_chip="שלב 6 · השבט שלי", step="6"), 11))
S.append((single(P("נטע אחות בכורה.jpg"),
    'נטע, האחות הבכורה — המנטורית שלי 💛', klass="portrait",
    step_chip="שלב 6 · השבט שלי", step="6"), 8.5))
S.append((quote(
    'אחי הקטן והאלוף חוגג בר מצווה! אין בעולם על הצחוקים והשטויות שלנו יחד. אני מבטיחה תמיד להיות שם בשבילך 😉',
    'אוהבת אותך הכי בעולם, נטע ✨', step_chip="שלב 6 · הברכה של נטע", step="6"), 11))

# Step 7 - the road / achievements (real soccer clip, slow-motion loop)
S.append((videoscene("photos/guy_soccer_video.mp4",
    'ראו כמה רחוק הגעתי 🏆<br>גיא הלוחם — לא מוותר אף פעם',
    step_chip="שלב 7 · הדרך שעשיתי", step="7"), 10.5))

# Step 8 - super powers (real family messages)
S.append((textscene(
    'אנשים שאוהבים אותי כתבו לי<br><span class="hl">מה כוח־העל שלי</span> ⚡',
    step_chip="שלב 8 · Super Powers", step="8"), 7))
S.append((quote(
    'אתה אלוף העולם עבורי. אין דבר העומד בפני הרצון שלך — גאה בך על ההתמדה, ההומור והחיוך המהמם ❤️',
    '— אילנה', step_chip="שלב 8 · Super Powers", step="8"), 10))
S.append((quote(
    'כוח אמיתי נמדד ביכולת להתגבר על דברים שפעם חשבת שאי אפשר. גיא — יש בך כוח לנצח הכל! 🫶',
    '— שלי', step_chip="שלב 8 · Super Powers", step="8"), 10))
S.append((quote(
    'כוח־העל שלך הוא למצוא פתרון טכנולוגי לכל דבר, וזיכרון מדהים. אתה חושב כמו ממציא אמיתי 💡',
    '— אודליה', step_chip="שלב 8 · Super Powers", step="8"), 10))

# Step 9 - my people
S.append((single(P("Guy with Girls.jpg"),
    'אני לא לבד במסע —<br>מוקף באנשים שאוהבים אותי', klass="land",
    step_chip="שלב 9 · האנשים שלי", step="9"), 10))

# Step 10 - who I am now
S.append((single(P("Guy - final step.jpeg"),
    'מי אני עכשיו? גיא הלוחם.<br>הנשק הסודי שלי: <span style="color:#DB2777">מוח שלא מוותר</span>', klass="portrait",
    step_chip="שלב 10 · מי אני עכשיו", step="10"), 11))

# Finale
S.append((finale('מזל טוב גיא!', 'הגיבור שמוכן לבר המצווה · 19.7.2026', MAP), 9))
S.append((textscene('באהבה אינסופית,<br><span class="hl">המשפחה שלך</span> ❤️', step="✦"), 7))

print(f"{len(S)} scenes, raw sum = {sum(d for _,d in S):.1f}s")

# ---------- render scenes to PNG ----------
def render(i, htmltext, transparent=False):
    hp = os.path.join(SCENES, f"scene_{i:02d}.html")
    with open(hp, "w", encoding="utf-8") as f: f.write(htmltext)
    op = os.path.join(FRAMES, f"scene_{i:02d}.png")
    if os.path.exists(op): os.remove(op)
    extra = ["--default-background-color=00000000"] if transparent else []
    subprocess.run([CHROME,"--headless=new","--disable-gpu","--hide-scrollbars","--no-sandbox",
        "--no-first-run","--user-data-dir="+os.path.join(SCRATCH,"cdp_movie"),
        "--force-device-scale-factor=1","--window-size=1920,1080","--virtual-time-budget=6000",
        *extra, f"--screenshot={op}", "file:///"+hp.replace("\\","/")],
        capture_output=True)
    return op

def is_video(h): return isinstance(h, tuple) and h[0] == "VIDEO"

if "--assemble-only" not in sys.argv:
    for i,(h,_) in enumerate(S):
        if is_video(h):
            render(i, h[2], transparent=True)   # scene PNG = the transparent overlay
        else:
            render(i, h)
        print("rendered", i)
    # verify all frames exist and are right size
    from PIL import Image
    for i in range(len(S)):
        op = os.path.join(FRAMES, f"scene_{i:02d}.png")
        assert os.path.exists(op), f"missing frame {i}"
        assert Image.open(op).size == (1920,1080), f"bad size {i}"
    print("all frames OK")

# ---------- assemble with ffmpeg (zoom + xfade + audio) ----------
durs = [d for _,d in S]
n = len(S)
inputs = []
for i,(h,d) in enumerate(S):
    if is_video(h):
        # loop the clip enough times to survive the 0.5x slow-mo, trim at filter stage
        inputs += ["-stream_loop","6","-i",h[1]]
    else:
        inputs += ["-loop","1","-t",f"{d:.3f}","-i",os.path.join(FRAMES,f"scene_{i:02d}.png")]
inputs += ["-i", SONG]

# transparent caption overlays for video scenes come after the song input
ov_idx = {}
for i,(h,_) in enumerate(S):
    if is_video(h):
        ov_idx[i] = n + 1 + len(ov_idx)
        inputs += ["-i", os.path.join(FRAMES, f"scene_{i:02d}.png")]

fc = []
for i,(h,_) in enumerate(S):
    frames = max(2,int(round(durs[i]*FPS)))
    if is_video(h):
        # real clip: 0.5x slow-motion, muted, centered WITHOUT cropping —
        # the frame is filled with a blurred copy and the clip sits whole on top
        fc.append(
          f"[{i}:v]setpts=2.0*PTS,fps={FPS},trim=duration={durs[i]:.3f},setpts=PTS-STARTPTS,"
          f"split[vb{i}][vf{i}];"
          f"[vb{i}]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,gblur=sigma=20[bg{i}];"
          f"[vf{i}]scale=1920:1080:force_original_aspect_ratio=decrease[fg{i}];"
          f"[bg{i}][fg{i}]overlay=(W-w)/2:(H-h)/2,setsar=1[vv{i}];"
          f"[vv{i}][{ov_idx[i]}:v]overlay=0:0:eof_action=repeat,fps={FPS},format=yuv420p[v{i}]"
        )
        continue
    # gentle center zoom 1.0 -> 1.06 (Ken Burns), output 1920x1080
    fc.append(
      f"[{i}:v]scale=2112:1188:force_original_aspect_ratio=increase,crop=2112:1188,"
      f"zoompan=z='min(zoom+0.00035,1.06)':d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
      f"s=1920x1080:fps={FPS},setsar=1,format=yuv420p[v{i}]"
    )
# xfade chain
prev = "v0"; acc = durs[0]
for i in range(1,n):
    off = acc - XF
    out = f"x{i}"
    fc.append(f"[{prev}][v{i}]xfade=transition=fade:duration={XF}:offset={off:.3f}[{out}]")
    acc = acc + durs[i] - XF
    prev = out
total = acc
# audio: trim to video length + 2.5s fade out
fc.append(f"[{n}:a]atrim=0:{total:.3f},afade=t=out:st={max(0,total-3):.3f}:d=3[aud]")
filtergraph = ";".join(fc)

cmd = [FFMPEG,"-y",*inputs,"-filter_complex",filtergraph,
       "-map",f"[{prev}]","-map","[aud]",
       "-c:v","libx264","-pix_fmt","yuv420p","-r",str(FPS),"-preset","medium","-crf","20",
       "-c:a","aac","-b:a","192k","-shortest",OUT]
print("total video length: %.2fs"%total)
with open(os.path.join(SCRATCH,"ffmpeg_cmd.txt"),"w",encoding="utf-8") as f:
    f.write(" ".join(cmd))
r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode!=0:
    print("FFMPEG ERROR:\n", r.stderr[-3000:])
    sys.exit(1)
print("DONE ->", OUT, os.path.getsize(OUT), "bytes")
