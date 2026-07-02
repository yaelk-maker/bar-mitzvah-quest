// Family progress view — READ-ONLY.
// Subscribes to the shared Firebase state and renders: progress header,
// per-step status list, and the completed keepsake chapters (reusing
// BOOK_RENDERERS / buildFamilyTreeHTML / buildCartoonBrainSVG from app.js).
// This file never writes to Firebase or localStorage quest state.

let famState = { completedQuests: [], responses: {} };
let famGotData = false;

function famSetStatus(text, ok) {
    const el = document.getElementById('fam-status');
    if (!el) return;
    el.textContent = text;
    el.classList.toggle('ok', !!ok);
}

function famRender() {
    const done = famState.completedQuests || [];
    const responses = famState.responses || {};
    const total = QUESTS.length;
    const currentQuest = QUESTS.find(q => !done.includes(q.id)) || null;

    // --- progress header ---
    const xp = done.length * 100;
    const pct = Math.round((done.length / total) * 100);
    document.getElementById('fam-progress').innerHTML = `
        <div class="fam-count"><span class="fam-num">${done.length} / ${total}</span> שלבים הושלמו</div>
        <div class="fam-xpbar"><div class="fam-xpfill" style="width:${pct}%"></div></div>
        <div class="fam-xptext"><span class="fam-num">XP ${xp} / ${total * 100}</span></div>
        ${done.length === total
            ? `<div class="fam-current fam-done-all">🎉 גיא סיים את כל המסע! מזל טוב!</div>`
            : currentQuest
                ? `<div class="fam-current">🎯 השלב הנוכחי: <strong>${currentQuest.name}</strong></div>`
                : ''}
    `;

    // --- steps list ---
    document.getElementById('fam-steps').innerHTML = QUESTS.map((q, idx) => {
        const isDone = done.includes(q.id);
        const isCurrent = currentQuest && currentQuest.id === q.id;
        const cls = isDone ? 'done' : isCurrent ? 'current' : 'locked';
        const badge = isDone ? '<span class="fam-badge fam-badge-done">✓ הושלם</span>'
                    : isCurrent ? '<span class="fam-badge fam-badge-here">כאן עכשיו</span>'
                    : '<span class="fam-badge fam-badge-lock">🔒</span>';
        return `
            <div class="fam-step ${cls}" style="--step-color:${q.color}">
                <span class="fam-step-no">${idx + 1}</span>
                <span class="fam-step-icon">${q.icon}</span>
                <span class="fam-step-name">${q.name}</span>
                ${badge}
            </div>`;
    }).join('');

    // --- completed keepsake chapters (read-only render, same as the Hero Book) ---
    const book = document.getElementById('fam-book');
    if (!done.length) {
        book.innerHTML = `<div class="book-page bk-empty"><p>📖 המסע רק מתחיל — כל שלב שגיא יסיים יופיע כאן!</p></div>`;
        return;
    }
    book.innerHTML = `<h2 class="fam-book-title">📖 מתוך ספר הגיבור של גיא</h2>` +
        QUESTS.filter(q => done.includes(q.id)).map(quest => {
            const r = responses[quest.id] || {};
            const renderer = BOOK_RENDERERS[quest.id];
            const inner = renderer ? renderer(quest, r) : '';
            return `
                <div class="book-page" style="border-color:${quest.color}">
                    <div class="book-chapter-header" style="background:${quest.color}">
                        <span class="chapter-icon">${quest.icon}</span>
                        <h3>${quest.artifact.title}</h3>
                    </div>
                    <p class="book-message"><em>"${quest.message}"</em></p>
                    <div class="book-responses">${inner}</div>
                </div>`;
        }).join('');
}

document.addEventListener('DOMContentLoaded', async () => {
    const fbOk = await initFirebase();

    // Same family passcode gate as the app (shared per-session unlock).
    await showPasscodeScreen();

    famRender(); // empty skeleton until data arrives

    if (fbOk && dbRef) {
        // Live subscription — re-renders whenever Guy makes progress.
        dbRef.on('value', (snap) => {
            const v = snap.val();
            famGotData = true;
            if (v) famState = v;
            famRender();
            famSetStatus('🔄 מתעדכן בזמן אמת', true);
        });
        setTimeout(() => {
            if (!famGotData) famSetStatus('⚠️ אין חיבור כרגע — ננסה שוב אוטומטית');
        }, 8000);
    } else {
        famSetStatus('⚠️ אין חיבור לענן — נסו לרענן מאוחר יותר');
    }
});
