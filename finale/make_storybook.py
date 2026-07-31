# -*- coding: utf-8 -*-
"""Build a print-ready A4 'Hero Book' storybook (storybook.html) for Guy's journey.

v2 (2026-07-11): rebuilt around Guy's REAL answers (source: backups/quest-progress-
GUY-REAL-2026-07-11.json). Every step page now mirrors what Guy actually chose in
the app. Run:  python finale/make_storybook.py [--pdf]
  --pdf also exports finale/Hero-Storybook.pdf via headless Chrome.
"""
import os, io, sys, base64, subprocess, urllib.parse, qrcode

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # this script lives in <repo>/finale/
OUT  = os.path.join(PROJ, "storybook.html")
PDF  = os.path.join(PROJ, "finale", "Hero-Storybook.pdf")
PAGES_BASE = "https://yaelk-maker.github.io/bar-mitzvah-quest"
CHROME = r"C:/Program Files/Google/Chrome/Application/chrome.exe"

def qr_datauri(url):
    qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=2)
    qr.add_data(url); qr.make(fit=True)
    img = qr.make_image(fill_color="#120D0E", back_color="white")
    buf = io.BytesIO(); img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

# ---------------------------------------------------------------- links / QRs
MOVIE_REEL = "https://youtu.be/495-TIULjoE"              # 🎬 סרט המסע → Hero-Movie-Short (YouTube)
MOVIE_LONG = "https://youtu.be/_-aJujjaz5g"              # 💌 סרט הברכות המלא → Hero-Movie-Long (YouTube)
KAHOOT_URL = "https://guy-quiz-2026.web.app/host.html"
SONG_URL   = f"{PAGES_BASE}/" + urllib.parse.quote("Song for the movie.mpeg")
NETA_TIKTOK = "https://youtube.com/shorts/Ji0JC1f6ZF0"    # הטיקטוק של נטע וגיא
ALIYAH_URL  = "https://youtube.com/shorts/Va3sQpAf9r8"    # 🕍 העלייה לתורה של גיא (YouTube)

# Quest-9 greeting cards (11 — the Neta TikTok moved to the step-6 page).
#   photo : repo-relative photo of the greeter (None -> styled "photo coming" placeholder)
#           Frames are landscape and use object-fit:contain, so NOTHING gets cropped;
#           landscape ~4:3 photos fill the frame best.
GREETERS = [
    {"name":"אבא ואמא",              "photo":"photos/greeter_mom_dad.jpeg",      "yt":"https://youtu.be/4jHyyvb70Ks"},
    {"name":"נטע ומיקה",             "photo":"photos/greeter_netta_mika.png",    "yt":"https://youtu.be/Qa4KVhCRpjc"},
    {"name":"סבתא סווטה",            "photo":"photos/greeter_sveta.jpeg",        "yt":"https://youtu.be/Cf5mnhRm-As"},
    {"name":"סבא מישה וסבתא מרינה",  "photo":"photos/greeter_marina_misha.jpeg", "pos":"center 42%", "yt":"https://youtu.be/MUYZBT6HUPI"},
    {"name":"משפחת שפירא",           "photo":"photos/greeter_shapira.png",       "yt":"https://youtu.be/XwWagA9NWfU"},
    {"name":"אירה ותום",            "photo":"photos/greeter_ira_tom.png",       "yt":"https://youtu.be/AOkEkL9tOhI"},
    {"name":"רעיה",                 "photo":"photos/greeter_raya.png",          "yt":"https://youtu.be/EMq3iPnrWFM"},
    {"name":"אליה",                 "photo":"photos/greeter_alya.jpg",          "yt":"https://youtube.com/shorts/R8SSJwrQb04"},
    {"name":"ציליה",                "photo":"photos/greeter_zilya.png",         "yt":"https://youtube.com/shorts/ow_YiF40f_I"},
    {"name":"יובל והמשפחה",         "photo":"photos/greeter_yuval_family.png",  "yt":"https://youtu.be/YULbuPcMgOQ"},
    {"name":"רפי",                  "photo":"photos/greeter_rafi.png",          "yt":"https://youtu.be/WDOedGcOzdM"},
]

# ------------------------------------------------------- Guy's REAL answers
# Source of truth: backups/quest-progress-GUY-REAL-2026-07-11.json (Firebase export)
FAMILY = [  # quests.js order; word = what Guy wrote for each one (quest 1)
    {"name":"סבא מישה",   "rel":"סבא מצד אבא",  "photo":"photos/סבא מישה (מצד אבא).jpg",   "pos":"center 30%", "word":"מצחיק"},
    {"name":"סבתא מרינה", "rel":"סבתא מצד אבא", "photo":"photos/סבתא מרינה (מצד אבא).JPG", "pos":"center 30%", "word":"משחקת איתי"},
    {"name":"סבא אלכס",   "rel":"סבא מצד אמא",  "photo":"photos/סבא אלכס (מצד אמא).jpeg",  "pos":"45% 30%",    "word":"גר באוקראינה"},
    {"name":"סבתא סווטה", "rel":"סבתא מצד אמא", "photo":"photos/סבתא סווטה (מצד אמא).jpeg","pos":"center 35%", "word":"אוהבת אותי"},
    {"name":"אבא איליה",  "rel":"אבא",          "photo":"photos/אבא איליה.jpg",            "pos":"center 35%", "word":"מצווה עליי לתת לו נשיקות"},
    {"name":"אמא יעל",    "rel":"אמא",          "photo":"photos/אמא יעל.jpg",              "pos":"center 30%", "word":"יפה"},
    {"name":"דודה אירה",  "rel":"דודה מצד אבא", "photo":"photos/דודה מצד אבא - אירה.jpg",  "pos":"45% 35%",    "word":"אמא של בן החמודי"},
    {"name":"דודה ג׳ני",  "rel":"דודה מצד אמא", "photo":"photos/דודה מצד אימא - ג'ני.jpeg","pos":"center 30%", "word":"מחבקת אותי"},
    {"name":"נטע",        "rel":"אחות בכורה",   "photo":"photos/נטע אחות בכורה.jpg",       "pos":"center 35%", "word":"משחקת איתי רובלוקס"},
    {"name":"מיקה",       "rel":"אחות תאומה",   "photo":"photos/אחות תאומה מיקה.jpg",      "pos":"center 40%", "word":"המפקדת שלי"},
    {"name":"גיא",        "rel":"זה אתה!",      "photo":"photos/גיא ילד יום הולדת.jpg",    "pos":"center 30%", "word":"אוהב מחשבים"},
]
# tree layout (same % anchors as buildFamilyTreeHTML in app.js; bg is 2094x2048)
TREE_POS = [
    (0, 19,   23.5, "gp"), (1, 38.5, 23.5, "gp"), (2, 61,   23.5, "gp"), (3, 80, 23.5, "gp"),
    (6, 10,   42.6, "parent"), (4, 28.2, 42.6, "parent"), (5, 69.5, 42.6, "parent"), (7, 88.5, 42.6, "parent"),
    (8, 32.5, 62, "child"), (10, 49, 62, "hero"), (9, 64.2, 62, "child"),
]

INVESTIGATION = [  # quest 3 — image + the FULL in-quest caption per discovery
    ("photos/placeholder_parents_young.jpg", "איך הכל התחיל?",
     "אמא ואבא גדלו יחד בבני עייש, אבל רק כעבור שנים, בטיול בראש פינה עם חברים, הם התחילו לדבר באמת — וכעבור חצי שנה, בנסיעה לאילת, ב-1 באפריל, הפכו לזוג רשמי."),
    ("photos/placeholder_neta_baby.jpg", "מצטרפת שחקנית ראשונה – נטע!",
     "הנה נטע! היא הייתה בת חצי שנה בלבד — ממש תינוקת פצפונת — כשגילינו שאמא שוב בהיריון, והפעם... עם תאומים! היא כבר חיכתה לכם בקוצר רוח."),
    ("photos/placeholder_ultrasound.jpg", "הפתעה כפולה בבטן!",
     "תראה אותך ואת מיקה! שני לבבות פועמים ביחד — צוות מנצח. גדלתם יחד, זה לצד זה, ונתתם אחד לשני כוח עוד לפני שנולדתם. <b>כוח הצוות שבחרת: כוח של תאומים.</b>"),
    ("photos/placeholder_nicu_twins.jpg", "שמות הכוח שלנו",
     "נולדתם בשבוע 28, מוקדם מאוד, והתחזקתם בפגייה. בני יומיים קיבלתם 'שמות כוח': לך קראנו <b>גיא בארי</b> — כוח הבריאות והחוזק. למיקה קראנו <b>מיקה גבריאל</b> — המלאך השומר שלך, שתמיד תשמרו אחד על השנייה."),
]

HERO_STATIONS = [  # quest 4 hero-journey (full station texts)
    ("💗", "היציאה למסע", "#7EC8E3", "גיא, הסיפור של החיים שלך נפתח באתגר יוצא דופן. יצאת לעולם מוקדם מהצפוי, כפג. היית צריך לשהות באינקובטור כדי לגדול ולהתחזק."),
    ("⚡", "האתגר המפתיע", "#B39DDB", "בימים הראשונים האלה, בגלל שהגוף שלך היה עדין, נוצר אצלך דימום במוח. הדימום הזה הוא מה שעיצב חלק מההתמודדויות שלך היום: את שיתוק המוחין ואת האוטיזם."),
    ("🏆", "כוח הלוחם", "#81C784", "אבל הדבר הכי חשוב הוא מה שגילינו עליך: יש בך כוח פנימי אדיר. לא ויתרת! עכשיו, כשאתה מתקרב לבר המצווה, אנחנו רואים נער שניצח את הקרב הראשון שלו, וממשיך לנצח כל יום מחדש."),
]
GUY_STONES = ["💎 חוזק פנימי", "🔥 עקשנות (במובן הטוב!)", "🦁 אומץ", "🛡️ יכולת להתמודד עם קשיים", "⚡ נחישות", "⭐ אמונה בעצמי"]  # the 6 Guy chose
GUY_BUBBLE = "אני מבטיח להמשיך להתאמץ ולא לוותר, בדיוק כמו שאתה עשית"  # his message to baby Guy

BRAIN_TRAITS = [  # quest 5 — (name, icon, color, Guy's level 1-4)  levels: קצת/בינוני/הרבה/סופר!
    ("דמיון ויצירתיות", "🎨", "#FF6B6B", 4),
    ("חושים רגישים",    "👁️", "#45B7D1", 4),
    ("ריכוז עמוק",      "🔍", "#9B59B6", 1),
    ("כוח וגוף",        "💪", "#FF8C42", 3),
    ("רגשות חזקים",     "💙", "#4D96FF", 4),
    ("זיכרון",          "🧩", "#6BCB77", 4),
]
BRAIN_LEVELS = ["קצת", "בינוני", "הרבה", "סופר!"]
GUY_BRAIN_CARDS = [  # the cards Guy flipped and claimed "זה אני!"
    ("🎯", "מומחה עמוק", "כשמשהו מעניין אותך, אתה יכול ללמוד עליו לעומק שאחרים לא מגיעים אליו"),
    ("💪", "הגוף עובד אחרת", "השרירים שלך צריכים להתאמץ יותר, אבל זה מה שבנה בך כוח ונחישות יוצאי דופן"),
    ("🔄", "אוהב שגרה", "שינויים פתאומיים יכולים להיות קשים — אתה מעדיף לדעת מה הולך לקרות"),
    ("❤️", "רגשות עמוקים", "אתה מרגיש דברים חזק — שמחה, עצב, התרגשות. הרגשות שלך עוצמתיים"),
    ("⚡", "מוח מהיר", "לפעמים המוח רץ מהר מאוד — רעיונות, מחשבות ותגובות קופצים בלי הפסקה"),
]
GUY_SENTENCE = "המוח שלי עובד אחרת, וזה הכוח שלי"

TWIN_STAGES = [  # quest 6 — Guy sorted every card correctly; bins in RTL order
    ("👶", "גיל ינקות — המיון הראשון", "photos/placeholder_twins_babies.jpeg", [
        ("רק גיא",       ["אהבה מיוחדת ללזניה", "להתעורר קבוע ב-5 בבוקר"]),
        ("שנינו ביחד!",  ["לעשות לאמא ואבא הרבה רעש", "אמבטיות משותפות עם הרבה צחוקים"]),
        ("רק מיקה",      ["צעדים ראשונים כבר בגיל 9 חודשים", "קושי להירדם בלי אמא או אבא קרובים"]),
    ]),
    ("🎒", "גיל הילדות ובית הספר — כוחות חדשים", "photos/placeholder_twins_kids.jpeg", [
        ("רק גיא",       ["לחרוש על משחקי מחשב וסוני", "לזכור מספרים וטלפונים בעל פה"]),
        ("שנינו ביחד!",  ["עקשנות וידיעה בדיוק מה רוצים", "הרכבת לגו במשך שעות"]),
        ("רק מיקה",      ["צורך שיהיה תמיד סדר בחדר", "אהבה גדולה לריקוד והתעמלות"]),
    ]),
]
NETA_GREETING = ("אחי הקטן והאלוף חוגג בר מצווה! 🎉 למרות שלפעמים אנחנו מציקים אחד לשנייה, "
    "תכלס אין בעולם על הצחוקים והשטויות שלנו יחד. אני מבטיחה תמיד להיות שם בשבילך, "
    "לחפות עליך מול אבא ואמא ותמיד אעזור לך להשיג מה שאתה רוצה מההורים 😉.")
NETA_SIGNATURE = "אוהבת אותך הכי בעולם, נטע ✨"

CABINET = [  # quest 7 — the medals Guy placed, top shelf first; (icon, text, proudest?)
    ("⚽", "משחק כדורגל", True),          # shelf 1 — ⭐ his proudest medal
    ("💪", "לא מוותר, גם כשקשה", False),  # shelf 2
    ("💻", "מומחה למחשבים", False),       # shelf 3
]

ENVELOPES = [  # quest 8 — secret-envelope messages, FULL original texts (a curated keepsake subset)
    ("אילנה", "אתה אלוף העולם עבורי, אין דבר העומד בפני הרצון שלך. גאה בך על הדרך שאתה עובר ויכולת ההתמדה שלך והכל מקושט בהומור ציני וחיוך מהמם ❤️"),
    ("שלי", "כוח אמיתי לא נמדד במה שאתה כבר יודע לעשות, אלא ביכולת שלך להתגבר על דברים שפעם חשבת שהם בלתי אפשריים. גיא - הכל תלוי בך! יש בך כוח לנצח הכל! 🫶🏽"),
    ("אמירה", "בחיים כמו בכדורגל - יש לך כוח על להניף את הרגל ולבעוט חזק ומדויק למטרה!"),
    ("אלמוג", "כוח העל שלך הוא שאתה לא מוותר! עברנו יחד דרך עם אתגרים, ובכל זאת המשכת להאמין בעצמך עד שהגעת למטרה! תזכור תמיד שהכוח הזה נמצא בך והוא יעזור לך להגשים את כל המטרות 🦸🏽‍♂️❤️"),
    ("אודליה", "גיא ילד פלא אהוב, אני מתרגשת מאוד ולא מאמינה שאתה כל כך גדול.<br>זכיתי להיות חלק מהמסע שלך. נהניתי לראות את הדרך שאתה עושה, כמה כוחות על ועוצמות יש בך.<br><b>כוח העל</b> שלך הוא למצוא פתרונות טכנולוגיים לכל דבר.<br>אתה חושב אחרת ומצליח לראות דרך גם כשנראה שאין.<br>אתה חושב כמו ממציא אמיתי 💡<br><b>כוח העל</b> שלך הוא הזיכרון המדהים שלך.<br>אתה זוכר פרטים קטנים ומצליח להשתמש בהם בצורה חכמה ומרשימה 🧠<br><b>כוח העל</b> שלך הוא היכולת להצחיק.<br>אתה מביא איתך קלילות ואור שמשמחים את הסביבה 😄<br><b>כוח העל</b> שלך הוא ההתמדה.<br>אתה ממשיך להשקיע ולא מוותר גם כשזה מאתגר 💪<br><b>כוח העל</b> שלך הוא הסקרנות.<br>הרצון שלך להבין ולגלות פותח לך עוד ועוד דלתות 🔍<br><b>כוח העל</b> שלך הוא להיות חבר אמיתי.<br>אתה שם לב לחברים בקבוצה ודואג להם 🤝<br>שתמיד תראה את כוחות העל שיש בך.<br>אוהבת מאוד 🤍"),
]
GUY_POWER_CHOICE = "כוח החברות"  # "הכוח שאני רוצה להשיג השנה"
GUY_EMOTION = "ירדה לי דמעה 🥺"   # how Guy felt after the greeting videos

GUY_CARD = {"title": "גיא אלוף הכדורגל", "weapon": "מוח שלא מוותר", "goal": "לטרוף את העולם"}

LYRICS = [  # "השיר של גיא" — the family's song for Guy (timed table lives in make_movie.py)
    "עוד לפני שהשמש עולה,", "כבר יש לך תוכנית בראש,", "מסך נדלק, משחק מתחיל,", "עולם שלם שאתה רוצה לכבוש.",
    "",
    "צחוק מתגלגל בכל הבית,", "תמיד מוצא סיבה לחייך,", "שואל מיליון שאלות בדרך,", "חוקר עולם, רוצה לדעת איך.",
    "",
    "ואם נופלים אז קמים,", "יש בך משהו שלא נגמר,", "איזה כוח, איזה דבר.",
    "",
    "גיא, אתה לא עוצר,", "ברגע קשה אתה חזק יותר,", "ילד של אור, של חלומות,", "תזכור — אתה לא עוצר.",
    "",
    "נטע תמיד לידך צוחקת,", "מיקה שומרת שלא תיפול,", "יובלי, אוריקי ובן אוהבים אותך,", "כי אתה פשוט גדול.",
    "",
    "במים אתה מוצא את הקצב,", "על הדשא אתה לא מוותר,", "עם חץ וקשת ישר למטרה,", "אתה מראה לכול שאפשר יותר.",
    "",
    "ופתאום שלוש עשרה שנים,", "עברו לנו כמו דקה,", "אנחנו מסתכלים עליך, גיא,", "והלב מתמלא אהבה.",
    "",
    "גיא, אתה לא עוצר,", "ברגע קשה אתה חזק יותר,", "ילד של אור, של חלומות,", "תזכור — אתה לא עוצר.",
]

# ---------------------------------------------------------------- cartoon brain
# Python port of buildCartoonBrainSVG (app.js) — keep visuals in sync with the app.
def brain_svg():
    SIL = 'M186,22 C136,10 92,26 68,58 C40,64 22,92 26,124 C12,152 20,190 44,208 C52,238 86,256 118,250 C142,272 190,274 218,258 C258,268 300,250 316,218 C340,196 344,156 328,130 C336,94 316,60 282,48 C258,20 220,14 186,22 Z'
    STEM = 'M232,256 C238,272 254,282 272,284 C258,290 240,290 228,282 C220,274 222,262 224,256 Z'
    LOBES = [
        ([(92,78,44),(132,58,40),(70,112,36)],   (100, 88)),
        ([(62,160,42),(52,196,34),(92,186,36)],  (72, 178)),
        ([(184,52,44),(226,64,40),(196,96,38)],  (200, 72)),
        ([(262,196,40),(232,222,36),(286,224,32)],(258, 214)),
        ([(150,150,48),(186,180,42),(130,196,38)],(158, 172)),
        ([(286,96,42),(302,140,38),(258,128,40)], (284, 120)),
    ]
    maxv = 4
    lobes, labels = "", ""
    for i, (name, icon, color, v) in enumerate(BRAIN_TRAITS):
        op = 0.30 + (v / maxv) * 0.62
        circles, (lx, ly) = LOBES[i]
        grow = (v - 2) * 3
        lobes += '<g clip-path="url(#cb-clip)">' + "".join(
            f'<circle cx="{cx}" cy="{cy}" r="{r + grow}" fill="{color}" fill-opacity="{op:.2f}" stroke="#4C1D95" stroke-opacity="0.35" stroke-width="2"/>'
            for cx, cy, r in circles) + '</g>'
        lv = BRAIN_LEVELS[v - 1]
        labels += (
            f'<text x="{lx}" y="{ly-8}" text-anchor="middle" font-size="{15+v}" style="paint-order:stroke" stroke="#fff" stroke-width="3">{icon}</text>'
            f'<text x="{lx}" y="{ly+10}" text-anchor="middle" font-size="11" font-weight="800" fill="#3B2A63" style="paint-order:stroke" stroke="#fff" stroke-width="3" font-family="Heebo,sans-serif">{name.split(" ")[0]}</text>'
            f'<text x="{lx}" y="{ly+24}" text-anchor="middle" font-size="10.5" font-weight="700" fill="{color}" style="paint-order:stroke" stroke="#fff" stroke-width="3" font-family="Heebo,sans-serif">{lv}</text>'
            + (f'<text x="{lx+26}" y="{ly-20}" text-anchor="middle" font-size="14">✨</text>' if v >= maxv else ''))
    return (f'<svg viewBox="0 0 360 300" class="cbrain" role="img" aria-label="מפת המוח של גיא">'
            f'<defs><clipPath id="cb-clip"><path d="{SIL}"/></clipPath></defs>'
            f'<path d="{STEM}" fill="#F3D1E5" stroke="#4C1D95" stroke-width="3"/>'
            f'<path d="{SIL}" fill="#FDF3FA" stroke="none"/>{lobes}'
            f'<path d="{SIL}" fill="none" stroke="#4C1D95" stroke-width="4" stroke-linejoin="round"/>{labels}</svg>')

# ---------------------------------------------------------------- page builders
def cover():
    qr_reel, qr_long = qr_datauri(MOVIE_REEL), qr_datauri(MOVIE_LONG)
    return f"""
<section class="page cover">
  <div class="cloud c1"></div><div class="cloud c2"></div><div class="cloud c3"></div>
  <div class="cover-inner">
    <div class="kicker">ספר הגיבור</div>
    <h1 class="booktitle">מסע הגיבורים<br>של גיא</h1>
    <div class="cover-map"><img src="map-v3.jpg"></div>
    <div class="cover-sub">עשרה שלבים · סיפור אחד גדול</div>
    <div class="cover-date">בר המצווה · 19 ביולי 2026</div>
    <div class="cover-qrs">
      <div class="cqr"><img src="{qr_reel}"><div class="cqr-lbl">🎬 סרט המסע</div></div>
      <div class="cqr"><img src="{qr_long}"><div class="cqr-lbl">💌 סרט הברכות המלא</div></div>
    </div>
  </div>
</section>"""

def blessing_pages():
    # ברכה של אמא ואבא — ported from the claude.ai/design project
    # "ברכה לגיא - קלאסי.dc.html" (Frank Ruhl Libre serif, cream paper, gold accent).
    b = lambda t: f'<strong class="bl-strong">{t}</strong>'
    p1 = f"""
<section class="page blpage">
  <div class="bl-titlewrap">
    <h1 class="bl-title">גיא שלנו</h1>
    <div class="bl-div"><div class="bl-l bl-l1"></div><div class="bl-diamond"></div><div class="bl-l bl-l2"></div></div>
  </div>
  <div class="bl-body">
    <p>אנחנו מסתכלים עליך היום, עומד כאן בבית הכנסת, וקשה לנו להאמין שהרגע הזה באמת הגיע.</p>
    <p>אנחנו שומעים אותך קורא את הפרשה, ורואים לא רק ילד שחוגג בר מצווה — אלא ילד {b('שבמשך כל החיים שלו בוחר, פעם אחר פעם, לא לוותר.')}</p>
    <p>כשנולדת, היו לנו הרבה מאוד חששות. הדרך קדימה לא תמיד הייתה ברורה. אבל אם יש משהו שלימדת אותנו לאורך השנים, זה {b('שהדרך שלך תמיד הייתה רק שלך.')} אתה לא מחפש את הדרך הקלה — אתה פשוט מחליט לאן אתה רוצה להגיע, וממשיך לצעוד.</p>
    <p class="bl-mid">מי שמכיר אותך יודע בדיוק מי אתה.</p>
    <p>ילד סקרן, שלא מפסיק לשאול שאלות. ילד עקשן — ולא תמיד פשוט להיות ההורים של ילד עקשן. אבל עם השנים הבנו שהעקשנות הזאת היא אחת המתנות הכי גדולות שלך. היא זו שגורמת לך להאמין בעצמך, להתעקש על מה שחשוב לך, ולהמשיך קדימה גם כשלא קל.</p>
    <p>ומעל הכול — אתה ילד עם לב ענק, שמעניק כל כך הרבה אהבה לכל מי שסביבו.</p>
    <p>אחד הדברים שהכי מרגשים אותנו אצלך הוא לראות איך אתה לא נותן לשום דבר לעצור אותך בדרך שלך.</p>
    <p class="bl-mid">יש סיפור אחד שתמיד יזכיר לנו בדיוק מי אתה.</p>
    <p>לפני כמה שנים, אחרי הניתוח ברגל, היית עם גבס. הרופא ביקש שתלך עם הליכון, כדי להקל עליך. אנחנו כל כך רצינו שתקשיב לו ותעשה לעצמך את החיים קצת יותר קלים. אבל אתה החלטת אחרת. בכל פעם שביקשנו שתישען על ההליכון, פשוט הרמת אותו בידיים והמשכת ללכת בלעדיו. במקום שהוא יעזור לך — הוא רק הכביד עליך.</p>
    <p>באותם רגעים, אני מודה, זה גם קצת הוציא אותי מדעתי.</p>
  </div>
</section>"""
    p2 = f"""
<section class="page blpage">
  <div class="bl-body">
    <p>אבל היום אנחנו מבינים שזו בדיוק הדרך שלך. אתה יודע מה אתה רוצה, אתה מאמין בעצמך, ואתה לא מוותר לעצמך. לפעמים התפקיד שלנו כהורים הוא לעזור לך למצוא את הדרך הנכונה — אבל אין לנו ספק שהעקשנות הזאת היא גם מה שמביא אותך לכל כך הרבה הישגים.</p>
    <p>גם בדרך לבר המצווה ראינו את זה שוב. בהתחלה חשבת שאולי יהיה קל יותר להקליט את הקריאה מראש. זה היה מובן, אפילו טבעי. אבל אז עשית את מה שאתה עושה כל החיים — הסתכלת לאתגר בעיניים ואמרת:</p>
    <p class="bl-big">״אני יכול!״</p>
    <p>לאט לאט, בקצב שלך, צברת ביטחון. ובכל פעם ששמענו אותך קורא את הפרשה בבית, התמלאנו גאווה והתרגשות. לא רק בגלל הקריאה עצמה, אלא בגלל שראינו שוב את אותו ילד שבוחר להאמין בעצמו, ולא נותן לחששות לעצור אותו.</p>
    <p>גיא, אתה תמיד אומר לי שאני האמא הכי טובה בעולם. אבל אם יש מישהו שזכה — זו אני. הזכות להיות אמא שלך מלמדת אותי בכל יום מחדש מה זו נחישות, מה זו אמונה בעצמך, ומה אפשר להשיג כשפשוט מסרבים לוותר.</p>
    <p>אנחנו רוצים שתמיד תזכור דבר אחד:</p>
    <p>{b('לא משנה בני כמה נהיה, ולא משנה לאן החיים ייקחו אותך — אנחנו תמיד נהיה שם בשבילך.')} לפעמים כדי לדחוף אותך קדימה, ולפעמים רק כדי לתת לך חיבוק כשצריך.</p>
    <p>מהרגע הראשון בחיים שלך בחרת ללכת בדרך שלך. היום, כשאנחנו מסתכלים עליך עומד כאן וקורא בתורה בביטחון, אנחנו מבינים שהדרך הזאת תמיד תוביל אותך רחוק.</p>
    <p>יהיו בה עליות, יהיו בה ירידות — אבל יש דבר אחד שאנחנו יודעים בוודאות: שום דבר לא יגרום לך להפסיק להתקדם.</p>
    <p>ואנחנו... תמיד נהיה שם. לפעמים כדי לדחוף אותך קדימה, ולפעמים פשוט כדי ללכת לידך.</p>
    <p>אנחנו גאים בך יותר ממה שמילים יכולות לתאר.</p>
  </div>
  <div class="bl-sign">
    <div class="bl-line"></div>
    <p class="bl-sign-big">מזל טוב, ילד שלנו.</p>
    <p class="bl-sign-sub">אנחנו אוהבים אותך עד אין סוף.</p>
    <p class="bl-sign-who">אמא ואבא</p>
  </div>
</section>"""
    return p1 + p2

def step(no, name, msg, accent, body, cls=""):
    return f"""
<section class="page light step {cls}" style="--accent:{accent}">
  <header class="shead">
    <div class="sno">{no}</div>
    <div class="sname">{name}</div>
    <div class="smsg">״{msg}״</div>
  </header>
  <div class="sbody">{body}</div>
</section>"""

# --- step 1: the family tree with Guy's words -------------------------------
def tree_body():
    short = lambda n: n.replace("סבא ", "").replace("סבתא ", "").replace("אבא ", "").replace("אמא ", "").replace("דודה ", "")
    items = ""
    for idx, cx, cy, cls in TREE_POS:
        m = FAMILY[idx]
        items += (
            f'<div class="tp tp-{cls}" style="left:{cx}%;top:{cy}%"><img src="{m["photo"]}" style="object-position:{m["pos"]}"></div>'
            f'<div class="tl tl-{cls}" style="left:{cx}%;top:{cy + 7.1}%">'
            f'<div class="tl-name">{short(m["name"])}<span class="tl-rel"> · {m["rel"]}</span></div>'
            f'<div class="tl-word">״{m["word"]}״</div></div>')
    return (f'<p class="lead tlead">המשפחה שלך — עם המילה שבחרת לכל אחד ואחת:</p>'
            f'<div class="tree">{items}</div>')

# --- step 2: the family Kahoot ----------------------------------------------
def kahoot_body():
    return (f'<p class="lead">יצרת חידון קהוט על המשפחה — ובערב משחק אחד גדול כולם ניחשו: '
            f'מי החור השחור של האוכל? מי מלך הדרמה? מי אלוף הנחירות ומי חוזר מהסופר עם שלוש שקיות במקום חלב? 😄</p>'
            f'<div class="kwrap"><div class="kbox"><div class="kbadge">K!</div>'
            f'<div class="ktitle">משחק ההכרות של משפחת קלינסקי</div>'
            f'<div class="kscan">רוצים לשחק שוב? סרקו והפעילו את החידון 🎮</div>'
            f'<img class="kqr" src="{qr_datauri(KAHOOT_URL)}"></div></div>'
            f'<p class="note">✅ המשימה הושלמה: הכנת קהוט למשפחה — וכולם גילו כמה טוב אתה מכיר אותם.</p>')

# --- step 3: investigation, full per-image sentences -------------------------
def investigation_body():
    rows = "".join(
        f'<div class="iqrow"><div class="iqimg"><img src="{img}"></div>'
        f'<div class="iqtxt"><div class="iqtitle">תעלומה {i+1} · {title}</div><div class="iqcap">{cap}</div></div></div>'
        for i, (img, title, cap) in enumerate(INVESTIGATION))
    return ('<p class="lead">פתחת את תיק החקירה המשפחתי ופיצחת את כל 4 התעלומות:</p>' + rows)

# --- step 4: the hero's origin, with Guy's choices ---------------------------
def hero_body():
    stations = "".join(
        f'<div class="hstation" style="--sc:{color}"><div class="hs-head"><span class="hs-icon">{icon}</span>{title}</div>'
        f'<div class="hs-text">{text}</div></div>'
        for icon, title, color, text in HERO_STATIONS)
    stones = "".join(f'<span class="stone">{s}</span>' for s in GUY_STONES)
    return (stations
        + f'<div class="sublabel">אבני הכוח שבחרת — מה הרווחת מהקרב הזה:</div><div class="stonewrap">{stones}</div>'
        + f'<div class="bubble"><div class="bubble-label">המשפט שבחרת לומר לגיא התינוק שנלחם בפגייה:</div>'
          f'<div class="bubble-text">״{GUY_BUBBLE}״</div></div>')

# --- step 5: Guy's brain ------------------------------------------------------
def brain_body():
    cards = "".join(
        f'<div class="bcard"><div class="bc-title">{icon} {title}</div><div class="bc-text">{text}</div></div>'
        for icon, title, text in GUY_BRAIN_CARDS)
    return ('<p class="lead">כל מוח בעולם הוא ייחודי — כמו טביעת אצבע. ככה נראה המוח שלך, לפי מה שסימנת:</p>'
        + f'<div class="brainwrap">{brain_svg()}</div>'
        + f'<div class="sublabel">הכרטיסים שסימנת ״זה אני!״:</div><div class="bgrid">{cards}</div>'
        + f'<p class="note big sentence">״{GUY_SENTENCE}״</p>')

# --- step 6: the tribe (two pages) -------------------------------------------
def twins_body():
    out = '<p class="lead">מיינת את כרטיסיות הזיכרון — מתי אתה ומיקה דומים ומתי שונים:</p>'
    for icon, title, img, bins in TWIN_STAGES:
        binhtml = "".join(
            f'<div class="bin"><div class="bin-head">{bname}</div>'
            + "".join(f'<div class="bin-card">{c}</div>' for c in cards) + '</div>'
            for bname, cards in bins)
        out += (f'<div class="stage"><div class="stage-head"><img class="stage-ph" src="{img}">'
                f'<span class="stage-title">{icon} {title}</span></div><div class="bins">{binhtml}</div></div>')
    return out

def neta_body():
    return (f'<div class="netagrid"><div class="neta-photo"><img src="photos/greeter_netta_page9.png"></div>'
        f'<div class="neta-side"><div class="ntt"><img class="ntt-qr" src="{qr_datauri(NETA_TIKTOK)}">'
        f'<div class="ntt-lbl">🎵 הטיקטוק של נטע וגיא<br><span>סרקו לצפייה</span></div></div></div></div>'
        f'<div class="blessing"><div class="bfrom">מעטפת הזהב של נטע — המנטורית הבכירה 💌</div>'
        f'<div class="btext">פתחת את המעטפה הנעולה אחרי שענית נכון על 3 שאלות על נטע — וזו הברכה שחיכתה לך בפנים:</div>'
        f'<div class="btext quote">״{NETA_GREETING}״</div>'
        f'<div class="bsig">{NETA_SIGNATURE}</div></div>'
        f'<p class="note">🏆 פיצחת את תעלומת האחים: כל אחד מכם הוא עולם מלא — ויחד אתם הצוות הכי חזק שיש.</p>')

# --- step 7: the trophy cabinet ----------------------------------------------
def cabinet_body():
    shelves = "".join(
        f'<div class="shelf"><div class="medal{" proud" if proud else ""}">'
        f'<span class="m-icon">{icon}</span><span class="m-text">{text}</span>'
        + ('<span class="m-star">🏆 הכי גאה בזה!</span>' if proud else '') + '</div></div>'
        for icon, text, proud in CABINET)
    return ('<p class="lead">״וואו, תראו איזה הישג מטורף! גיא הלוחם!״ — מילאת את ארון הגביעים שלך:</p>'
        + f'<div class="c7grid"><div class="ph tall7"><img src="photos/guy_soccer_page.png"></div>'
        + f'<div class="cabinet"><div class="cab-title">🏆 ארון הגביעים של גיא</div>{shelves}</div></div>'
        + '<p class="note">בחרת את מדליית <b>משחק כדורגל</b> ⚽ בתור ההישג שאתה הכי גאה בו — '
          'ומי שראה אותך על הדשא יודע בדיוק למה. כל מדליה כאן מספרת סיפור של הצלחה, וזו רק ההתחלה!</p>')

# --- step 8: super powers (flowing pages, full texts) -------------------------
def messages_pages():
    def card(frm, txt):
        return f'<div class="mcard"><div class="mfrom">💌 {frm}</div><div class="mtext">{txt}</div></div>'
    # Paginate into fixed A4 pages so every printed page keeps its top/side margins
    # (the long אודליה card gets its own page instead of flowing flush to the edge).
    chunks = [ENVELOPES[:4], ENVELOPES[4:]]
    out = ""
    for idx, ch in enumerate(chunks):
        if idx == 0:
            head = ('<header class="shead"><div class="sno">8</div>'
                    '<div class="sname">כוחות העל שלי</div>'
                    '<div class="smsg">״יש לי כוחות מיוחדים״</div></header>'
                    '<p class="lead">פתחת מעטפות סודיות שאנשים שאוהבים אותך כתבו לך, הנה כמה למזכרת:</p>')
        else:
            head = ('<header class="shead cont"><div class="sname">כוחות העל שלי…</div>'
                    '<div class="smsg">עוד מעטפה למזכרת 💌</div></header>')
        cards = "".join(card(frm, txt) for frm, txt in ch)
        tail = (f'<p class="note big powerpick">⚡ הכוח שבחרת להשיג השנה: <b>{GUY_POWER_CHOICE}</b></p>'
                if idx == len(chunks) - 1 else '')
        out += (f'<section class="page light step" style="--accent:#673AB7">'
                f'{head}<div class="mcol">{cards}</div>{tail}</section>')
    return out

# --- step 9: greeting-video cards ---------------------------------------------
def greeter_photo(g):
    if g.get("photo") and os.path.exists(os.path.join(PROJ, g["photo"])):
        pos = g.get("pos", "center 28%")
        return f'<div class="gphoto"><img src="{g["photo"]}" style="object-position:{pos}"></div>'
    return '<div class="gphoto placeholder"><div class="ph-emoji">🎬</div><div class="ph-txt">תמונה תתווסף</div></div>'

def greetings_pages():
    def card(g):
        return (f'<figure class="gcard">{greeter_photo(g)}'
                f'<div class="grow"><img class="gqr" src="{qr_datauri(g["yt"])}">'
                f'<div class="gmeta"><figcaption class="gname">{g["name"]}</figcaption>'
                f'<div class="gscan">סרקו לצפייה בברכה 🎬</div></div></div></figure>')
    chunks = [GREETERS[i:i+4] for i in range(0, len(GREETERS), 4)]
    out = ""
    for idx, ch in enumerate(chunks):
        if idx == 0:
            head = ('<header class="shead"><div class="sno">9</div><div class="sname">האנשים שלי</div>'
                    '<div class="smsg">״אני לא לבד במסע״</div></header>'
                    '<p class="lead glead">צפית בכל 11 סרטוני הברכה — סרקו כל קוד כדי לצפות שוב 🎬</p>')
        else:
            head = ('<header class="shead cont"><div class="sname">האנשים שלי…</div>'
                    '<div class="smsg">עוד ברכות 🎬</div></header>')
        cards = "".join(card(g) for g in ch)
        tail = f'<p class="note gnote">💙 איך הרגשת אחרי הסרטונים? <b>״{GUY_EMOTION}״</b></p>' if idx == len(chunks) - 1 else ''
        out += f'<section class="page light step" style="--accent:#00BCD4">{head}<div class="ggrid">{cards}</div>{tail}</section>'
    return out

# --- step 10: the winning card ------------------------------------------------
def card10_body():
    c = GUY_CARD
    return (f'<div class="tcard"><div class="tc-inner">'
        f'<div class="tc-photo"><img src="photos/Guy - final step.jpeg"></div>'
        f'<div class="tc-name">⭐ {c["title"]} ⭐</div>'
        f'<div class="tc-row"><span class="tc-k">🗡️ הנשק הסודי שלי</span><span class="tc-v">{c["weapon"]}</span></div>'
        f'<div class="tc-row"><span class="tc-k">🎯 המטרה שלי לשנה הבאה</span><span class="tc-v">{c["goal"]}</span></div>'
        f'</div></div>'
        f'<p class="note big">זה אני, בן 13 — ואני לא מוותר לעצמי.</p>')

# --- the song page --------------------------------------------------------------
def _song_lines(lst):
    return "".join(f'<div class="lyr{" gap" if not l else ""}">{l}</div>' for l in lst)

def song_page():
    # Spread over two pages, single centered column (matching the Word-doc layout).
    # Split at the blank line after the first chorus: 4 stanzas per page.
    p1, p2 = _song_lines(LYRICS[:18]), _song_lines(LYRICS[19:])
    return f"""
<section class="page light step songpage" style="--accent:#DB2777">
  <header class="shead">
    <div class="sno">🎵</div>
    <div class="sname">השיר של גיא</div>
    <div class="smsg">״גיא, אתה לא עוצר״</div>
  </header>
  <div class="songtop"><img class="songqr" src="{qr_datauri(SONG_URL)}">
    <div class="songlbl">שיר שנכתב במיוחד בשבילך למסע הזה.<br><b>סרקו להאזנה 🎧</b></div></div>
  <div class="lyrics">{p1}</div>
</section>
<section class="page light step songpage" style="--accent:#DB2777">
  <header class="shead cont"><div class="sname">השיר של גיא…</div>
    <div class="smsg">להמשיך לשיר 🎶</div></header>
  <div class="lyrics">{p2}</div>
</section>"""

def celebration_page():
    # 🕍 the real day: photos from the aliyah + QR to the synagogue video
    return f"""
<section class="page light step celebday" style="--accent:#A8873F">
  <header class="shead">
    <div class="sno">🕍</div>
    <div class="sname">העלייה לתורה</div>
    <div class="smsg">״אני יכול!״ — ועשית את זה</div>
  </header>
  <p class="lead">27 ביולי 2026 — עלית לתורה בבית הכנסת, מוקף בכל האנשים שאוהבים אותך, וקראת את הפרשה בקול בטוח. בדיוק כמו שאמרת.</p>
  <div class="celgrid">
    <div class="cph"><img src="photos/bm_day_torah.jpg" style="object-position:center 22%"></div>
    <div class="cph"><img src="photos/bm_day_bimah.jpg" style="object-position:center 35%"></div>
    <div class="cph"><img src="photos/bm_day_family.jpg" style="object-position:center 30%"></div>
    <div class="cph short"><img src="photos/bm_day_cake.jpg" style="object-position:center 45%"></div>
    <div class="cph short wide"><img src="photos/bm_day_minyan.jpg" style="object-position:center 30%"></div>
  </div>
  <div class="celqr">
    <img class="celqr-img" src="{qr_datauri(ALIYAH_URL)}">
    <div class="celqr-lbl">🎥 הרגע הגדול צולם!<br><b>סרקו לצפייה בעלייה לתורה של גיא</b></div>
  </div>
</section>"""

def closing():
    return """
<section class="page closing">
  <div class="cloud c1"></div><div class="cloud c2"></div>
  <div class="cl-inner">
    <h1 class="booktitle">מזל טוב, גיא!</h1>
    <div class="cl-sub">הגיבור שמוכן לבר המצווה</div>
    <div class="cl-photo"><img src="photos/family_last_page.jpg"></div>
    <div class="cl-love">באהבה אינסופית — המשפחה שלך ❤️</div>
    <div class="cover-date">19 ביולי 2026</div>
  </div>
</section>"""

PAGES = [
    cover(), blessing_pages(),
    step("1", "עץ השורשים", "אני חלק מסיפור גדול", "#4CAF50", tree_body()),
    step("2", "משחק הכרות", "אני מכיר את המשפחה שלי", "#9C27B0", kahoot_body()),
    step("3", "חקירה משפחתית", "פיצחתי את התעלומות המשפחתיות", "#2196F3", investigation_body()),
    step("4", "הגיבור שנולד", "כבר בהתחלה הייתי גיבור", "#F44336", hero_body()),
    step("5", "המוח המיוחד שלי", "אני מבין את הגוף והמוח שלי", "#FF9800", brain_body()),
    step("6", "השבט שלי", "אני תאום — ואני גם אני", "#E91E63", twins_body()),
    step("6", "השבט שלי · הברכה של נטע", "אני תאום — ואני גם אני", "#E91E63", neta_body()),
    step("7", "הדרך שעשיתי", "ראו כמה רחוק הגעתי", "#FFC107", cabinet_body()),
    messages_pages(),
    greetings_pages(),
    step("10", "מי אני עכשיו", "זה אני, בן 13 — ולא מוותר לעצמי", "#FF5722", card10_body()),
    song_page(),
    celebration_page(),
    closing(),
]

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Heebo:wght@400;500;700;800;900&family=Bungee&family=Baloo+2:wght@600;700;800&family=Frank+Ruhl+Libre:wght@400;500;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact}
html{font-family:'Heebo','Segoe UI',Arial,sans-serif;color:#120D0E}
body{background:#FBFAF8}
@page{size:A4 portrait;margin:0}
.page{width:210mm;min-height:297mm;page-break-after:always;position:relative;overflow:hidden;
  padding:16mm 15mm}
.page:last-child{page-break-after:auto}
.light{background:#FBFAF8}
/* clouds */
.cloud{position:absolute;border-radius:50%;background:rgba(255,255,255,.85);filter:blur(1px)}
.c1{width:60mm;height:26mm;top:20mm;right:18mm}.c2{width:42mm;height:18mm;top:12mm;left:24mm}
.c3{width:50mm;height:22mm;bottom:40mm;left:20mm}
/* cover */
.cover{background:linear-gradient(180deg,#8fd0ec,#bfe6f4 45%,#e2f4ea);text-align:center;display:flex;align-items:center;justify-content:center}
.cover-inner{position:relative;z-index:2;width:100%}
.kicker{font-family:'Baloo 2';font-weight:800;font-size:28px;color:#fff;background:linear-gradient(90deg,#FF7AB6,#DB2777);display:inline-block;padding:6px 28px;border-radius:999px}
.booktitle{font-family:'Bungee';font-size:58px;line-height:1.06;color:#fff;margin:18px 0 12px;
  -webkit-text-stroke:3px #6D28D9;text-shadow:0 6px 0 rgba(109,40,217,.30)}
.cover-map{width:140mm;margin:6px auto;border-radius:20px;overflow:hidden;border:8px solid #fff;box-shadow:0 18px 40px rgba(0,0,0,.22)}
.cover-map img{width:100%;display:block}
.cover-sub{font-family:'Baloo 2';font-weight:800;font-size:27px;color:#120D0E;margin-top:10px}
.cover-date{font-weight:800;font-size:21px;color:#fff;background:rgba(109,40,217,.6);display:inline-block;padding:7px 24px;border-radius:999px;margin-top:10px}
.cover-qrs{display:flex;justify-content:center;gap:14mm;margin-top:9mm}
.cqr{background:#fff;border-radius:14px;padding:8px 14px 9px;box-shadow:0 8px 22px rgba(0,0,0,.16);text-align:center}
.cqr img{width:24mm;height:24mm;display:block;margin:0 auto}
.cqr-lbl{font-weight:800;font-size:15px;color:#120D0E;margin-top:3px}
/* intro */
.intro{text-align:center;display:flex;flex-direction:column;justify-content:center}
.ititle{font-family:'Bungee';font-size:40px;color:#DB2777;margin-bottom:18px}
.ibody{font-size:24px;line-height:1.85;max-width:150mm;margin:0 auto;font-weight:500}
.iheart{font-size:70px;margin-top:30px}
/* step header (position:relative also fixes the runaway number badge) */
.shead{border-bottom:4px solid var(--accent);padding-bottom:10px;margin-bottom:14px;position:relative}
.sno{font-family:'Bungee';font-size:26px;color:#fff;background:var(--accent);width:52px;height:52px;
  border-radius:16px;display:flex;align-items:center;justify-content:center;position:absolute;top:0;left:0}
.sname{font-family:'Baloo 2';font-weight:800;font-size:38px;color:var(--accent);padding-right:4px}
.smsg{font-size:22px;font-weight:700;color:#5A524D;margin-top:2px}
.sbody{font-size:21px}
.lead{font-size:21px;line-height:1.6;font-weight:600;margin:8px 0}
.note{font-size:20px;line-height:1.65;background:#F6F3F0;border-radius:16px;padding:14px 18px;margin-top:12px}
.note.big{text-align:center;font-weight:800;font-size:25px;background:none}
.sublabel{font-weight:800;font-size:21px;margin:12px 0 6px;color:#5A524D}
/* photos */
.ph{border-radius:18px;overflow:hidden;border:7px solid #fff;box-shadow:0 14px 34px rgba(0,0,0,.18)}
.ph img{width:100%;height:100%;display:block;object-fit:cover}
/* ---- step 1: family tree ---- */
.tlead{text-align:center}
.tree{position:relative;width:168mm;aspect-ratio:2094/2048;margin:2mm auto 0;
  background:url('photos/family-tree-bg.png') center/contain no-repeat #10241A;
  border:7px solid #fff;border-radius:18px;box-shadow:0 14px 34px rgba(0,0,0,.20)}
.tp{position:absolute;transform:translate(-50%,-50%);border-radius:50%;overflow:hidden;
  width:10.5%;aspect-ratio:1;border:2px solid rgba(255,255,255,.75);box-shadow:0 2px 6px rgba(0,0,0,.3);z-index:3}
.tp img{width:100%;height:100%;object-fit:cover;display:block}
.tp-hero{width:11.5%;border:3px solid #FFD600;box-shadow:0 0 10px rgba(255,214,0,.6)}
.tl{position:absolute;transform:translate(-50%,-50%);text-align:center;z-index:4;width:22%}
.tl-name{font-size:12.5px;font-weight:800;color:#fff;white-space:nowrap;line-height:1.05;
  text-shadow:0 1px 2px rgba(0,0,0,.85),0 0 4px rgba(0,0,0,.45)}
.tl-rel{font-weight:600;font-size:10px}
.tl-word{font-size:11.5px;font-weight:700;font-style:italic;color:#fff;line-height:1.12;margin-top:2px;
  text-shadow:0 1px 3px rgba(0,0,0,.9),0 0 5px rgba(0,0,0,.5)}
/* ---- step 2: kahoot ---- */
.kwrap{display:flex;justify-content:center;margin:10mm 0 4mm}
.kbox{background:linear-gradient(135deg,#46178F,#7C4DFF);border-radius:22px;padding:12mm 16mm;text-align:center;
  color:#fff;box-shadow:0 16px 38px rgba(70,23,143,.35)}
.kbadge{font-family:'Bungee';font-size:44px;background:#fff;color:#46178F;width:70px;height:70px;border-radius:18px;
  display:flex;align-items:center;justify-content:center;margin:0 auto 8px;direction:ltr}
.ktitle{font-family:'Baloo 2';font-weight:800;font-size:28px}
.kscan{font-size:19px;font-weight:600;margin:6px 0 10px;color:rgba(255,255,255,.9)}
.kqr{width:44mm;height:44mm;border-radius:12px;background:#fff;padding:6px}
/* ---- step 3: investigation rows ---- */
.iqrow{display:flex;gap:6mm;align-items:center;margin-bottom:5mm;background:#fff;border-radius:16px;
  box-shadow:0 8px 20px rgba(0,0,0,.10);padding:5mm;break-inside:avoid}
.iqimg{flex:0 0 44mm;height:36mm;border-radius:12px;overflow:hidden;border:4px solid #fff;box-shadow:0 6px 16px rgba(0,0,0,.14)}
.iqimg img{width:100%;height:100%;object-fit:cover;display:block}
.iqtxt{flex:1}
.iqtitle{font-family:'Baloo 2';font-weight:800;font-size:21px;color:#2196F3;margin-bottom:3px}
.iqcap{font-size:17.5px;line-height:1.5;font-weight:500}
/* ---- step 4: origin ---- */
.hstation{background:#fff;border-right:9px solid var(--sc);border-radius:14px;padding:10px 16px;margin-bottom:4mm;
  box-shadow:0 8px 20px rgba(0,0,0,.08)}
.hs-head{font-family:'Baloo 2';font-weight:800;font-size:22px;color:#120D0E}
.hs-icon{margin-left:6px}
.hs-text{font-size:18px;line-height:1.55;font-weight:500;margin-top:2px}
.stonewrap{display:flex;flex-wrap:wrap;gap:8px;justify-content:center}
.stone{font-weight:800;font-size:18.5px;background:#FFF4F8;border:2px solid #FFAFC4;border-radius:999px;padding:7px 16px}
.bubble{background:#EAE7FF;border-radius:16px;padding:12px 18px;margin-top:12px;text-align:center}
.bubble-label{font-weight:700;font-size:18px;color:#5A524D}
.bubble-text{font-weight:800;font-size:23px;color:#4C1D95;margin-top:4px}
/* ---- step 5: brain ---- */
.brainwrap{width:118mm;margin:0 auto}
.cbrain{width:100%;display:block}
.bgrid{display:grid;grid-template-columns:1fr 1fr;gap:4mm}
.bcard{background:#fff;border-radius:12px;padding:8px 12px;box-shadow:0 6px 16px rgba(0,0,0,.08);break-inside:avoid}
.bcard:last-child{grid-column:1/-1}
.bc-title{font-weight:800;font-size:18px;color:#FF9800}
.bc-text{font-size:15.5px;line-height:1.45;font-weight:500}
.sentence{color:#DB2777}
/* ---- step 6a: twin sort ---- */
.stage{margin-bottom:6mm}
.stage-head{display:flex;align-items:center;gap:5mm;margin-bottom:3mm}
.stage-ph{width:26mm;height:20mm;object-fit:cover;border-radius:10px;border:3px solid #fff;box-shadow:0 5px 14px rgba(0,0,0,.16)}
.stage-title{font-family:'Baloo 2';font-weight:800;font-size:23px;color:#E91E63}
.bins{display:grid;grid-template-columns:1fr 1fr 1fr;gap:4mm}
.bin{background:#fff;border-radius:14px;box-shadow:0 8px 18px rgba(0,0,0,.10);overflow:hidden}
.bin-head{background:#FFAFC4;color:#120D0E;font-weight:800;font-size:18px;text-align:center;padding:6px}
.bin-card{font-size:15px;font-weight:600;line-height:1.3;background:#FFF4F8;border-radius:8px;margin:5px 7px;padding:6px 8px;text-align:center}
/* ---- step 6b: Neta ---- */
.netagrid{display:flex;gap:6mm;align-items:stretch;margin-bottom:4mm}
.neta-photo{flex:1;height:74mm;border-radius:18px;overflow:hidden;border:7px solid #fff;box-shadow:0 14px 34px rgba(0,0,0,.18)}
.neta-photo img{width:100%;height:100%;object-fit:cover;object-position:center 35%;display:block}
.neta-side{flex:0 0 52mm;display:flex;align-items:center}
.ntt{background:#fff;border-radius:16px;padding:10px;box-shadow:0 10px 24px rgba(0,0,0,.14);text-align:center;width:100%}
.ntt-qr{width:38mm;height:38mm}
.ntt-lbl{font-weight:800;font-size:16.5px;line-height:1.3;margin-top:4px}
.ntt-lbl span{font-weight:600;font-size:14px;color:#968E89}
.blessing{background:#FFF4F8;border-right:10px solid #E91E63;border-radius:16px;padding:14px 20px}
.bfrom{font-family:'Baloo 2';font-weight:800;font-size:25px;color:#E91E63;margin-bottom:4px}
.btext{font-size:19px;line-height:1.6;font-weight:500}
.btext.quote{font-size:21px;font-weight:600;margin-top:8px}
.bsig{font-weight:800;font-size:21px;color:#E91E63;margin-top:8px;text-align:left}
/* ---- step 7: cabinet ---- */
.c7grid{display:flex;gap:7mm;align-items:stretch}
.ph.tall7{flex:0 0 60mm;height:112mm}
.cabinet{flex:1;background:linear-gradient(180deg,#8B5A2B,#6F4518);border-radius:18px;padding:8mm 6mm;
  box-shadow:inset 0 0 0 5px #5C3A14, 0 14px 34px rgba(0,0,0,.25)}
.cab-title{font-family:'Baloo 2';font-weight:800;font-size:24px;color:#FFE0B2;text-align:center;margin-bottom:5mm}
.shelf{background:linear-gradient(180deg,#C89058,#A9743C);border-radius:10px;padding:5mm 4mm 4mm;margin-bottom:5mm;
  box-shadow:0 4px 0 #5C3A14}
.shelf:last-child{margin-bottom:0}
.medal{background:#FFF8E1;border-radius:12px;padding:8px 12px;display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.m-icon{font-size:26px}
.m-text{font-weight:800;font-size:20px}
.medal.proud{background:linear-gradient(135deg,#FFF3C4,#FFE082);box-shadow:0 0 0 3px #FFB300}
.m-star{font-weight:800;font-size:16px;color:#B26A00;background:#fff;border-radius:999px;padding:3px 10px}
/* ---- step 8: messages ---- */
.msgflow{background:#FBFAF8;padding:16mm 15mm;page-break-before:always;page-break-after:always}
.mcol{margin-top:10px}
.mcard{break-inside:avoid;background:#fff;border-top:7px solid var(--accent);border-radius:16px;
  box-shadow:0 10px 24px rgba(0,0,0,.10);padding:16px 24px;margin-bottom:6mm}
.mfrom{font-family:'Baloo 2';font-weight:800;font-size:23px;color:#673AB7;margin-bottom:4px}
.mtext{font-size:18px;line-height:1.5;font-weight:500}
.powerpick{break-inside:avoid;color:#4C1D95}
/* ---- step 9: greeting cards (landscape frames, contain = never cropped) ---- */
.ggrid{display:grid;grid-template-columns:1fr 1fr;gap:6mm;margin-top:10px}
.gcard{background:#fff;border-radius:16px;box-shadow:0 8px 22px rgba(0,0,0,.12);padding:9px 10px 10px;
  border-top:6px solid var(--accent);break-inside:avoid}
.glead{margin:6px 0 0}
.gphoto{width:100%;height:52mm;border-radius:12px;overflow:hidden;background:#F1EDE9;margin-bottom:6px;
  display:flex;align-items:center;justify-content:center}
.gphoto img{width:100%;height:100%;object-fit:cover;object-position:center 28%;display:block}
.gphoto.placeholder{flex-direction:column;color:#968E89;background:linear-gradient(135deg,#F6F3F0,#EBE5E2)}
.ph-emoji{font-size:38px;line-height:1}.ph-txt{font-weight:700;font-size:15px;margin-top:4px}
.grow{display:flex;align-items:center;gap:5mm}
.gqr{width:26mm;height:26mm;flex:0 0 26mm}
.gmeta{flex:1;text-align:right}
.gname{font-family:'Baloo 2';font-weight:800;font-size:22px;color:var(--accent)}
.gscan{font-size:14px;color:#968E89;margin-top:1px}
.gnote{margin-top:5mm}
/* ---- step 10: trading card ---- */
.tcard{width:100mm;margin:4mm auto 0;background:linear-gradient(135deg,#FFD54F,#FB8C00,#FFD54F);
  border-radius:22px;padding:5mm;box-shadow:0 18px 44px rgba(251,140,0,.35)}
.tc-inner{background:#FFFDF6;border-radius:16px;padding:5mm;text-align:center}
.tc-photo{width:100%;height:88mm;border-radius:12px;overflow:hidden;margin-bottom:4mm}
.tc-photo img{width:100%;height:100%;object-fit:cover;object-position:center 25%;display:block}
.tc-name{font-family:'Baloo 2';font-weight:800;font-size:30px;color:#B26A00;background:#FFF3C4;border-radius:999px;padding:6px;margin-bottom:4mm}
.tc-row{background:#F6F3F0;border-radius:12px;padding:8px 12px;margin-bottom:3mm;text-align:right}
.tc-k{display:block;font-weight:700;font-size:16px;color:#968E89}
.tc-v{display:block;font-weight:800;font-size:23px;color:#120D0E}
/* ---- song ---- */
.songtop{display:flex;align-items:center;gap:7mm;justify-content:center;margin:2mm 0 3mm}
.songqr{width:30mm;height:30mm}
.songlbl{font-size:20px;font-weight:600;line-height:1.45}
.songpage{background:#FFF4F8}
.lyrics{text-align:center;max-width:160mm;margin:0 auto;padding:2mm 0}
.lyr{font-size:22px;font-weight:600;line-height:1.68}
.lyr.gap{height:15px}
/* ---- parents' blessing pages (אמא ואבא) — classic design port: serif, cream paper, gold accent.
   NOTE: class is .blpage (NOT .blessing — that name is taken by Neta's greeting box on the step-6 page). */
.blpage{background:#FBF7EF;height:297mm;display:flex;flex-direction:column;
  padding:15mm 21.5mm 14mm 15.5mm;font-family:'Frank Ruhl Libre','David Libre',Georgia,serif;color:#241F17;text-align:right}
.bl-titlewrap{display:flex;flex-direction:column;align-items:center;gap:13px;padding:10mm 0 11mm;text-align:center}
.bl-title{margin:0;font-family:'Frank Ruhl Libre',serif;font-weight:500;font-size:42px;line-height:1.15;letter-spacing:-0.01em;color:#1B1710}
.bl-div{display:flex;align-items:center;gap:12px;width:190px}
.bl-l{flex:1;height:1px}
.bl-l1{background:linear-gradient(to left,transparent,#A8873F)}
.bl-l2{background:linear-gradient(to right,transparent,#A8873F)}
.bl-diamond{width:5px;height:5px;transform:rotate(45deg);background:#A8873F}
.bl-body{flex:1;display:flex;flex-direction:column;justify-content:space-between;font-size:19px;line-height:1.7;font-weight:400}
.bl-body p{margin:0}
.bl-strong{font-weight:700;color:#1B1710}
.bl-mid{font-size:21px;font-weight:700;line-height:1.45;color:#252625}
.bl-big{text-align:center;font-size:30px;font-weight:500;line-height:1.3;color:#1B1710}
.bl-sign{display:flex;flex-direction:column;align-items:center;gap:10px;padding-top:20px;text-align:center}
.bl-sign p{margin:0}
.bl-line{width:64px;height:1px;background:#A8873F;opacity:.55}
.bl-sign-big{font-size:30px;font-weight:500;line-height:1.35;color:#1B1710}
.bl-sign-sub{font-size:19px;font-weight:400;line-height:1.45;color:#4A4034}
.bl-sign-who{margin-top:8px !important;font-family:'Heebo',sans-serif;font-size:12px;font-weight:700;letter-spacing:.3em;color:#A8873F}
/* ---- celebration day (העלייה לתורה) ---- */
.celgrid{display:grid;grid-template-columns:repeat(6,1fr);gap:4mm;margin-top:6px}
.cph{grid-column:span 2;height:82mm;border-radius:14px;overflow:hidden;border:5px solid #fff;
  box-shadow:0 8px 22px rgba(0,0,0,.14);background:#EBE5E2}
.cph img{width:100%;height:100%;object-fit:cover;display:block}
.cph.short{height:74mm}
.cph.wide{grid-column:span 4}
.celqr{display:flex;align-items:center;justify-content:center;gap:7mm;margin-top:6mm;
  background:#FBF7EF;border:2px solid #A8873F;border-radius:16px;padding:5mm 10mm}
.celqr-img{width:30mm;height:30mm}
.celqr-lbl{font-size:20px;font-weight:600;line-height:1.5}
/* closing */
.closing{background:linear-gradient(180deg,#ffd3e3,#bfe6f4);text-align:center;display:flex;align-items:center;justify-content:center}
.cl-inner{position:relative;z-index:2}
.cl-photo{width:95mm;margin:18px auto;border-radius:20px;overflow:hidden;border:8px solid #fff;box-shadow:0 18px 40px rgba(0,0,0,.22)}
.cl-photo img{width:100%;display:block}
.cl-sub{font-family:'Baloo 2';font-weight:800;font-size:30px;color:#120D0E;margin-top:6px}
.cl-love{font-size:24px;font-weight:700;color:#120D0E;margin:14px 0}
@media screen{body{padding:20px}.page,.msgflow{margin:0 auto 20px;box-shadow:0 10px 40px rgba(0,0,0,.25);width:210mm}}
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
print("wrote", OUT, len(doc), "bytes")

if "--pdf" in sys.argv:
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
                    "--no-pdf-header-footer", "--virtual-time-budget=20000",
                    f"--print-to-pdf={PDF}", OUT], check=True)
    print("wrote", PDF)
