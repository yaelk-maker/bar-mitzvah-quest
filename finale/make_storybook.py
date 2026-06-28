# -*- coding: utf-8 -*-
"""Build a print-ready A4 'Hero Book' storybook (storybook.html) for Guy's journey."""
import os, io, base64, urllib.parse, qrcode
from qrcode.image.pil import PilImage

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # this script lives in <repo>/finale/
OUT  = os.path.join(PROJ, "storybook.html")
PAGES_BASE = "https://yaelk-maker.github.io/bar-mitzvah-quest"

def qr_datauri(url):
    qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=2)
    qr.add_data(url); qr.make(fit=True)
    img = qr.make_image(fill_color="#120D0E", back_color="white")
    buf = io.BytesIO(); img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

GREETINGS = [
    ("סווטה (סבתא)", "סרטון - סווטה.mp4"),
    ("מרינה ומישה (סבא וסבתא)", "סרטון - מרינה ומישה.mp4"),
    ("משפחת שפירא", "סרטון - משפחת שפירא.mp4"),
    ("אירה ותום", "סרטון - אירה ותום.mp4"),
    ("רעיה", "סרטון - רעיה.mp4"),
    ("אליה", "סרטון - אליה.mp4"),
    ("ציליה", "סרטון - ציליה.mp4"),
    ("יובל והמשפחה", "סרטון - יובל והמשפחה.mp4"),
    ("רפי", "סרטון - רפי.mp4"),
]
def gurl(fname):
    return f"{PAGES_BASE}/photos/" + urllib.parse.quote("Videos - step 9/" + fname)

MESSAGES = [  # step 8 — real family/friend messages
    ("אילנה", "אתה אלוף העולם עבורי, אין דבר העומד בפני הרצון שלך. גאה בך על הדרך שאתה עובר, יכולת ההתמדה שלך, והכל מקושט בהומור ציני וחיוך מהמם ❤️"),
    ("שלי", "כוח אמיתי לא נמדד במה שאתה כבר יודע לעשות, אלא ביכולת שלך להתגבר על דברים שפעם חשבת שהם בלתי אפשריים. גיא — הכל תלוי בך! יש בך כוח לנצח הכל! 🫶🏽"),
    ("גילת", "כוח העל שלך זה להרשות לעצמך לשחרר, לרוץ ולהנות; לזהות את הלך הרוח בקבוצה ולהצטרף אליו; לא לוותר, לגלות אומץ ולהיות שווה בין שווים — תמיד בגובה העיניים."),
    ("אמירה", "בחיים כמו בכדורגל — יש לך כוח על להניף את הרגל ולבעוט חזק ומדויק למטרה!"),
    ("אלמוג", "כוח העל שלך הוא שאתה לא מוותר! עברנו יחד דרך עם אתגרים, ובכל זאת המשכת להאמין בעצמך עד שהגעת למטרה. הכוח הזה נמצא בך ויעזור לך להגשים כל מטרה 🦸🏽‍♂️❤️"),
    ("חלי", "כמו שבוב ספוג אומר — הרבה יותר קל להתנצל מאשר לבקש רשות 😄"),
    ("מירב", "אני מאוד אוהבת את התכונה שלך ללמוד כל דבר — 'כל מעשה במחשבה תחילה'. מוכן לקחת שיעורי בית ולהשקיע, בדיוק כמו במקרה חוק ארכימדס. וכמובן — ההומור שלך!"),
    ("אודליה", "גיא ילד פלא אהוב, אני מתרגשת ולא מאמינה שאתה כל כך גדול. זכיתי להיות חלק מהמסע שלך וראיתי כמה כוחות־על יש בך: למצוא פתרון טכנולוגי לכל דבר 💡, זיכרון מדהים 🧠, היכולת להצחיק 😄, התמדה 💪, סקרנות 🔍 והיכולת להיות חבר אמיתי 🤝. שתמיד תראה את כוחות־העל שבך. אוהבת מאוד 🤍"),
]

def img(rel, cls=""):
    return f'<div class="ph {cls}"><img src="{rel}"></div>'

# ---------------- page builders ----------------
def cover():
    return f"""
<section class="page cover">
  <div class="cloud c1"></div><div class="cloud c2"></div><div class="cloud c3"></div>
  <div class="cover-inner">
    <div class="kicker">ספר הגיבור</div>
    <h1 class="booktitle">מסע הגיבורים<br>של גיא</h1>
    <div class="cover-map"><img src="map-v3.jpg"></div>
    <div class="cover-sub">עשרה שלבים · סיפור אחד גדול</div>
    <div class="cover-date">בר המצווה · 19 ביולי 2026</div>
  </div>
</section>"""

def intro():
    return f"""
<section class="page light intro">
  <h2 class="ititle">לגיא היקר 💙</h2>
  <p class="ibody">
    כל גיבור מתחיל את המסע שלו במקום אחד — ומגיע רחוק הרבה יותר ממה שחשב.<br><br>
    הספר הזה מספר את הסיפור שלך: מאיפה באת, את הקרב הראשון שניצחת כשהיית פג קטנטן,
    את הכוחות המיוחדים שגילית בדרך, ואת כל האנשים שאוהבים אותך ומלווים אותך.<br><br>
    עברת עשרה שלבים במסע — וכאן הם כולם, במקום אחד, כדי שתזכור תמיד:
    <b>אתה גיבור, בדיוק כמו שאתה.</b>
  </p>
  <div class="iheart">⭐</div>
</section>"""

def step(no, name, msg, accent, body):
    return f"""
<section class="page light step" style="--accent:{accent}">
  <header class="shead">
    <div class="sno">{no}</div>
    <div class="sname">{name}</div>
    <div class="smsg">״{msg}״</div>
  </header>
  <div class="sbody">{body}</div>
</section>"""

def grid(cells):
    g = "".join(f'<figure class="gc"><img src="{src}"><figcaption>{n}</figcaption></figure>' for src,n in cells)
    return f'<div class="pgrid">{g}</div>'

def _mcards(items):
    return "".join(
        f'<div class="mcard{" wide" if len(txt)>200 else ""}"><div class="mfrom">{frm}</div><div class="mtext">{txt}</div></div>'
        for frm,txt in items)

def messages_pages():
    return f"""
<section class="msgflow" style="--accent:#673AB7">
  <header class="shead">
    <div class="sno">8</div><div class="sname">כוחות העל שלי</div>
    <div class="smsg">״יש לי כוחות מיוחדים״</div>
  </header>
  <p class="lead">אנשים שאוהבים אותך כתבו לך מהו כוח־העל שלך:</p>
  <div class="mcol">{_mcards(MESSAGES)}</div>
</section>"""

def greetings_page():
    cells = ""
    for name, fname in GREETINGS:
        uri = qr_datauri(gurl(fname))
        cells += f'<figure class="qrc"><img src="{uri}"><figcaption>{name}</figcaption></figure>'
    return f"""
<section class="page light step" style="--accent:#00BCD4">
  <header class="shead">
    <div class="sno">9</div><div class="sname">האנשים שלי</div>
    <div class="smsg">״אני לא לבד במסע״</div>
  </header>
  <p class="lead">אנשים שאוהבים אותך הכינו לך סרטוני ברכה. סרקו את הקוד בטלפון כדי לצפות 🎬</p>
  <div class="qrgrid">{cells}</div>
</section>"""

def closing():
    return f"""
<section class="page closing">
  <div class="cloud c1"></div><div class="cloud c2"></div>
  <div class="cl-inner">
    <h1 class="booktitle">מזל טוב, גיא!</h1>
    <div class="cl-sub">הגיבור שמוכן לבר המצווה</div>
    <div class="cl-photo"><img src="photos/Guy - final step.jpeg"></div>
    <div class="cl-love">באהבה אינסופית — המשפחה שלך ❤️</div>
    <div class="cover-date">19 ביולי 2026</div>
  </div>
</section>"""

# ---------------- step bodies ----------------
b1 = grid([
    ("photos/סבא מישה (מצד אבא).jpg","סבא מישה"),
    ("photos/סבתא מרינה (מצד אבא).JPG","סבתא מרינה"),
    ("photos/סבא אלכס (מצד אמא).jpeg","סבא אלכס"),
    ("photos/סבתא סווטה (מצד אמא).jpeg","סבתא סווטה"),
    ("photos/אבא איליה.jpg","אבא איליה"),
    ("photos/אמא יעל.jpg","אמא יעל"),
    ("photos/דודה מצד אבא - אירה.jpg","דודה אירה"),
    ("photos/דודה מצד אימא - ג'ני.jpeg","דודה ג׳ני"),
]) + '<p class="lead">המשפחה שגידלה אותך באהבה — שלושה דורות שעומדים מאחוריך בכל צעד.</p>'

b3 = ('<p class="lead">פתחת את תיק החקירה המשפחתי וגילית מאיפה באת:</p>'
   + grid([
        ("photos/placeholder_parents_young.jpg","איך הכל התחיל"),
        ("photos/placeholder_neta_baby.jpg","נטע, הבכורה"),
        ("photos/placeholder_ultrasound.jpg","שני לבבות"),
        ("photos/placeholder_nicu_twins.jpg","הצוות נולד"),
     ])
   + '<p class="note">בהתחלה היו שלושה עוברים — והטבע דאג שאתה ומיקה תקבלו את כל הכוח לגדול. '
     'בני יומיים קיבלתם שמות־כוח: <b>גיא בארי</b> (בריאות וחוזק) ו־<b>מיקה גבריאל</b> (המלאך השומר).</p>')

b4 = (img("photos/placeholder_nicu_twins.jpg","wide")
   + '<p class="lead">נולדת מוקדם, פג קטנטן ולוחם. בימים הראשונים היה דימום במוח שעיצב חלק מההתמודדויות שלך — '
     'שיתוק מוחין ואוטיזם. אבל גילינו בך כוח פנימי אדיר: <b>לא ויתרת.</b></p>'
   + '<div class="stones">💎 חוזק פנימי · 🔥 עקשנות · 🦁 אומץ · 🛡️ התמודדות · 🕰️ סבלנות · ⚡ נחישות · ⭐ אמונה בעצמי</div>')

b5 = ('<p class="lead big">כל מוח בעולם הוא ייחודי — כמו טביעת אצבע 🧠</p>'
   + '<div class="traits">'
     '<span>🎨 דמיון ויצירתיות</span><span>👁️ חושים רגישים</span><span>🔍 ריכוז עמוק</span>'
     '<span>💪 כוח וגוף</span><span>💙 רגשות חזקים</span><span>🧩 זיכרון</span></div>'
   + '<p class="note">המוח שלך עובד אחרת — וזה בדיוק הכוח שלך.</p>')

b6 = (grid([
        ("photos/placeholder_twins_babies.jpeg","תאומים מהיום הראשון"),
        ("photos/placeholder_twins_kids.jpeg","גדלים יחד"),
        ("photos/נטע אחות בכורה.jpg","נטע — המנטורית"),
     ])
   + '<div class="blessing"><div class="bfrom">הברכה של נטע ✨</div>'
     '<div class="btext">״אחי הקטן והאלוף חוגג בר מצווה! למרות שלפעמים אנחנו מציקים אחד לשני, אין בעולם על הצחוקים '
     'והשטויות שלנו יחד. אני מבטיחה תמיד להיות שם בשבילך 😉. אוהבת אותך הכי בעולם.״</div></div>')

b7 = (img("photos/Guy - final step.jpeg","tall")
   + '<p class="lead">ארון הגביעים שלך מלא יותר ממה שחשבת:</p>'
   + '<div class="medals">💻 מומחה למחשבים · ⚽ כדורגל · 😁 חיוך שמנצח הכל · 💪 לא מוותר · 🏊 שחייה · 📚 לומד כל יום</div>')

b10 = (img("photos/Guy - final step.jpeg","tall")
   + '<div class="card10">'
     '<div class="c10row"><span>הטייטל שלי:</span> גיא הלוחם</div>'
     '<div class="c10row"><span>הנשק הסודי שלי:</span> מוח שלא מוותר</div>'
     '<div class="c10row"><span>המטרה שלי לשנה הבאה:</span> להמשיך להיות גיבור</div>'
     '</div>'
   + '<p class="note big">זה אני, בן 13 — ואני לא מוותר לעצמי.</p>')

PAGES = [
    cover(), intro(),
    step("1","עץ השורשים","אני חלק מסיפור גדול","#4CAF50", b1),
    step("3","חקירה משפחתית","פיצחתי את התעלומות המשפחתיות","#2196F3", b3),
    step("4","הגיבור שנולד","כבר בהתחלה הייתי גיבור","#F44336", b4),
    step("5","המוח המיוחד שלי","אני מבין את הגוף והמוח שלי","#FF9800", b5),
    step("6","השבט שלי","אני תאום — ואני גם אני","#E91E63", b6),
    step("7","הדרך שעשיתי","ראו כמה רחוק הגעתי","#FFC107", b7),
    messages_pages(),
    greetings_page(),
    step("10","מי אני עכשיו","זה אני, בן 13 — ולא מוותר לעצמי","#FF5722", b10),
    closing(),
]

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Heebo:wght@400;500;700;800;900&family=Bungee&family=Baloo+2:wght@600;700;800&display=swap');
*{margin:0;padding:0;box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact}
html{font-family:'Heebo','Segoe UI',Arial,sans-serif;color:#120D0E}
body{background:#FBFAF8}
@page{size:A4 portrait;margin:0}
.page{width:210mm;min-height:297mm;page-break-after:always;position:relative;overflow:hidden;
  padding:18mm 16mm}
.page:last-child{page-break-after:auto}
.light{background:#FBFAF8}
/* clouds */
.cloud{position:absolute;border-radius:50%;background:rgba(255,255,255,.85);filter:blur(1px)}
.c1{width:60mm;height:26mm;top:20mm;right:18mm}.c2{width:42mm;height:18mm;top:12mm;left:24mm}
.c3{width:50mm;height:22mm;bottom:40mm;left:20mm}
/* cover */
.cover{background:linear-gradient(180deg,#8fd0ec,#bfe6f4 45%,#e2f4ea);text-align:center;display:flex;align-items:center;justify-content:center}
.cover-inner{position:relative;z-index:2;width:100%}
.kicker{font-family:'Baloo 2';font-weight:800;font-size:30px;color:#fff;background:linear-gradient(90deg,#FF7AB6,#DB2777);display:inline-block;padding:6px 28px;border-radius:999px}
.booktitle{font-family:'Bungee';font-size:62px;line-height:1.06;color:#fff;margin:22px 0 14px;
  -webkit-text-stroke:3px #6D28D9;text-shadow:0 6px 0 rgba(109,40,217,.30)}
.cover-map{width:150mm;margin:8px auto;border-radius:20px;overflow:hidden;border:8px solid #fff;box-shadow:0 18px 40px rgba(0,0,0,.22)}
.cover-map img{width:100%;display:block}
.cover-sub{font-family:'Baloo 2';font-weight:800;font-size:30px;color:#120D0E;margin-top:14px}
.cover-date{font-weight:800;font-size:22px;color:#fff;background:rgba(109,40,217,.6);display:inline-block;padding:8px 26px;border-radius:999px;margin-top:14px}
/* intro */
.intro{text-align:center;display:flex;flex-direction:column;justify-content:center}
.ititle{font-family:'Bungee';font-size:40px;color:#DB2777;margin-bottom:18px}
.ibody{font-size:24px;line-height:1.85;max-width:150mm;margin:0 auto;font-weight:500}
.iheart{font-size:70px;margin-top:30px}
/* step header */
.step .shead{border-bottom:4px solid var(--accent);padding-bottom:12px;margin-bottom:18px;position:relative}
.sno{font-family:'Bungee';font-size:30px;color:#fff;background:var(--accent);width:56px;height:56px;
  border-radius:16px;display:flex;align-items:center;justify-content:center;position:absolute;top:0;left:0}
.sname{font-family:'Baloo 2';font-weight:800;font-size:42px;color:var(--accent);padding-right:4px}
.smsg{font-size:24px;font-weight:700;color:#5A524D;margin-top:4px}
.sbody{font-size:22px}
.lead{font-size:23px;line-height:1.7;font-weight:600;margin:14px 0}
.lead.big{font-size:30px;text-align:center;color:#120D0E}
.note{font-size:21px;line-height:1.7;background:#F6F3F0;border-radius:16px;padding:16px 20px;margin-top:14px}
.note.big{text-align:center;font-weight:800;font-size:26px;background:none}
/* photos */
.ph{border-radius:18px;overflow:hidden;border:7px solid #fff;box-shadow:0 14px 34px rgba(0,0,0,.18);margin:0 auto}
.ph img{width:100%;display:block;object-fit:cover}
.ph.wide{width:150mm;height:78mm}.ph.wide img{height:100%}
.ph.tall{float:left;width:62mm;height:84mm;margin:0 0 10px 14px}.ph.tall img{height:100%}
.pgrid{display:flex;flex-wrap:wrap;gap:8mm;justify-content:center;margin:6px 0}
.gc{width:38mm;text-align:center}
.gc img{width:38mm;height:44mm;object-fit:cover;border-radius:14px;border:6px solid #fff;box-shadow:0 10px 24px rgba(0,0,0,.16)}
.gc figcaption{font-weight:800;font-size:18px;margin-top:6px;color:#5A524D}
/* stones / traits / medals */
.stones,.medals{font-size:22px;font-weight:700;line-height:1.9;background:#FFF4F8;border-radius:16px;padding:16px 20px;margin-top:14px;text-align:center}
.traits{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin:16px 0}
.traits span{font-weight:800;font-size:22px;background:#EAE7FF;border-radius:999px;padding:10px 22px}
/* blessing */
.blessing{background:#FFF4F8;border-right:10px solid #E91E63;border-radius:16px;padding:18px 22px;margin-top:16px}
.bfrom{font-family:'Baloo 2';font-weight:800;font-size:26px;color:#E91E63;margin-bottom:6px}
.btext{font-size:22px;line-height:1.7;font-weight:500}
/* messages step */
/* messages: flowing single-column letters, paginate naturally, never mid-card */
.msgflow{background:#FBFAF8;padding:18mm 16mm;page-break-before:always;page-break-after:always}
.mcol{margin-top:14px}
.mcard{break-inside:avoid;background:#fff;border-top:7px solid var(--accent);border-radius:16px;
  box-shadow:0 10px 24px rgba(0,0,0,.10);padding:18px 26px;margin-bottom:6mm}
.mfrom{font-family:'Baloo 2';font-weight:800;font-size:26px;color:#673AB7;margin-bottom:6px}
.mtext{font-size:21px;line-height:1.6;font-weight:500}
/* qr greetings */
.qrgrid{display:flex;flex-wrap:wrap;gap:7mm;justify-content:center;margin-top:14px}
.qrc{width:48mm;text-align:center;background:#fff;border-radius:14px;box-shadow:0 10px 24px rgba(0,0,0,.10);padding:10px}
.qrc img{width:40mm;height:40mm}
.qrc figcaption{font-weight:800;font-size:18px;margin-top:6px;color:#5A524D}
/* card10 */
.card10{background:#FFF4F8;border-radius:16px;padding:18px 22px;margin-bottom:10px}
.c10row{font-size:24px;font-weight:700;margin:8px 0}.c10row span{color:#FF5722;font-weight:800}
/* closing */
.closing{background:linear-gradient(180deg,#ffd3e3,#bfe6f4);text-align:center;display:flex;align-items:center;justify-content:center}
.cl-inner{position:relative;z-index:2}
.cl-photo{width:95mm;margin:18px auto;border-radius:20px;overflow:hidden;border:8px solid #fff;box-shadow:0 18px 40px rgba(0,0,0,.22)}
.cl-photo img{width:100%;display:block}
.cl-sub{font-family:'Baloo 2';font-weight:800;font-size:30px;color:#120D0E;margin-top:6px}
.cl-love{font-size:24px;font-weight:700;color:#120D0E;margin:14px 0}
@media screen{body{padding:20px}.page{margin:0 auto 20px;box-shadow:0 10px 40px rgba(0,0,0,.25)}}
.printbar{position:fixed;top:14px;left:14px;z-index:99}
.printbar button{font-family:'Baloo 2';font-weight:800;font-size:18px;background:#DB2777;color:#fff;border:0;border-radius:999px;padding:12px 26px;cursor:pointer;box-shadow:0 8px 20px rgba(219,39,119,.4)}
@media print{.printbar{display:none}}
"""

doc = f"""<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8">
<title>ספר הגיבור של גיא</title><style>{CSS}</style></head><body>
<div class="printbar"><button onclick="window.print()">🖨️ הדפס / שמור כ-PDF</button></div>
{''.join(PAGES)}
</body></html>"""

with open(OUT, "w", encoding="utf-8") as f:
    f.write(doc)
print("wrote", OUT, len(doc), "bytes;", len(PAGES), "pages")
