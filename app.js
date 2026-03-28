// ===== State Management =====
const STORAGE_KEY = 'bar-mitzvah-quest';

function loadState() {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) return JSON.parse(saved);
    return { completedQuests: [], responses: {}, currentQuest: null };
}

function saveState(state) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

let state = loadState();

// ===== XP Calculation =====
function getXP() {
    return state.completedQuests.length * 100;
}

function updateXPBar() {
    const xp = getXP();
    const pct = (xp / TOTAL_XP) * 100;
    document.getElementById('home-xp-fill').style.width = pct + '%';
    document.getElementById('home-xp-text').textContent = `${xp} / ${TOTAL_XP} XP`;
}

// ===== Screen Navigation =====
function showScreen(id) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.getElementById('screen-' + id).classList.add('active');
    window.scrollTo(0, 0);
}

function showHome() {
    showScreen('home');
    renderQuestMap();
    updateXPBar();
}

// ===== Quest Map =====
function renderQuestMap() {
    const map = document.getElementById('quest-map');
    map.innerHTML = '';

    QUESTS.forEach((quest, idx) => {
        const isCompleted = state.completedQuests.includes(quest.id);
        const isUnlocked = idx === 0 || state.completedQuests.includes(QUESTS[idx - 1].id);
        const isNext = isUnlocked && !isCompleted;

        const node = document.createElement('div');
        node.className = `quest-node ${isCompleted ? 'completed' : ''} ${isNext ? 'next' : ''} ${!isUnlocked ? 'locked' : ''}`;
        node.style.setProperty('--quest-color', quest.color);

        node.innerHTML = `
            <div class="quest-node-icon">${isCompleted ? '✓' : (!isUnlocked ? '🔒' : quest.icon)}</div>
            <div class="quest-node-info">
                <span class="quest-node-number">משימה ${quest.id}</span>
                <span class="quest-node-name">${quest.name}</span>
                <span class="quest-node-subtitle">${quest.subtitle}</span>
            </div>
            ${isCompleted ? '<span class="quest-node-xp">+' + quest.xp + ' XP</span>' : ''}
        `;

        if (isUnlocked) {
            node.addEventListener('click', () => openQuest(quest.id));
        }

        // Connector line between nodes
        if (idx < QUESTS.length - 1) {
            const connector = document.createElement('div');
            connector.className = `quest-connector ${isCompleted ? 'completed' : ''}`;
            map.appendChild(node);
            map.appendChild(connector);
        } else {
            map.appendChild(node);
        }
    });

    // Hero Book button at the end
    const allDone = state.completedQuests.length === QUESTS.length;
    if (allDone) {
        const bookBtn = document.createElement('div');
        bookBtn.className = 'quest-node completed book-node';
        bookBtn.innerHTML = `
            <div class="quest-node-icon">📖</div>
            <div class="quest-node-info">
                <span class="quest-node-name">ספר הגיבור שלי</span>
                <span class="quest-node-subtitle">לחץ לצפייה</span>
            </div>
        `;
        bookBtn.addEventListener('click', () => openHeroBook());
        map.appendChild(bookBtn);
    }
}

// ===== Open Quest =====
function openQuest(questId) {
    const quest = QUESTS.find(q => q.id === questId);
    if (!quest) return;

    state.currentQuest = questId;
    saveState(state);

    document.getElementById('quest-badge').textContent = quest.icon;
    document.getElementById('quest-badge').style.background = quest.color;
    document.getElementById('quest-title').textContent = quest.name;

    const body = document.getElementById('quest-body');
    body.innerHTML = '';

    // Intro
    const intro = document.createElement('div');
    intro.className = 'quest-intro';
    intro.innerHTML = `<p>${quest.intro}</p>`;
    body.appendChild(intro);

    // Identity message
    const msg = document.createElement('div');
    msg.className = 'quest-message';
    msg.innerHTML = `<span class="message-label">המסר של המשימה:</span> <em>"${quest.message}"</em>`;
    body.appendChild(msg);

    // Tasks
    quest.tasks.forEach((task, tIdx) => {
        const taskEl = document.createElement('div');
        taskEl.className = 'task-block';
        const savedResponses = state.responses[questId] || {};

        switch (task.type) {
            case 'info':
                taskEl.innerHTML = `<div class="task-info">${task.content.replace(/\n/g, '<br>')}</div>`;
                break;

            case 'story':
                taskEl.innerHTML = `
                    <div class="task-info">${task.content}</div>
                    <div class="story-box">${task.text}</div>
                `;
                break;

            case 'textarea':
            case 'reflection':
                const key = `task_${tIdx}`;
                taskEl.innerHTML = `
                    <label class="task-label">${task.label}</label>
                    <textarea class="task-input" data-quest="${questId}" data-key="${key}"
                        placeholder="${task.placeholder || ''}"
                        rows="4">${savedResponses[key] || ''}</textarea>
                `;
                break;

            case 'family-tree':
                taskEl.innerHTML = `<label class="task-label">${task.content}</label>`;
                const grid = document.createElement('div');
                grid.className = 'family-grid';
                task.members.forEach((member, mIdx) => {
                    const mKey = `member_${mIdx}`;
                    const avatarContent = member.photo
                        ? `<img src="${member.photo}" alt="${member.name}">`
                        : member.name.charAt(0);
                    grid.innerHTML += `
                        <div class="family-member">
                            <div class="member-avatar">${avatarContent}</div>
                            <span class="member-name">${member.name}</span>
                            ${member.relation ? `<span class="member-relation">${member.relation}</span>` : ''}
                            <input type="text" class="task-input-small"
                                data-quest="${questId}" data-key="${mKey}"
                                value="${savedResponses[mKey] || ''}"
                                placeholder="מילה אחת...">
                        </div>
                    `;
                });
                taskEl.appendChild(grid);
                break;

            case 'family-flow':
                taskEl.className = 'task-block family-flow-block';
                const flowMembers = task.members;
                const flowSaved = state.responses[questId] || {};
                let currentIdx = 0;
                let flowDone = false;
                // Find first person without a response to resume
                for (let fi = 0; fi < flowMembers.length; fi++) {
                    if (!flowSaved[`member_${fi}`]) { currentIdx = fi; break; }
                    if (fi === flowMembers.length - 1) { currentIdx = fi; }
                }
                // Check if all members have responses -> show tree
                const allFilled = flowMembers.every((_, fi) => flowSaved[`member_${fi}`]);
                if (allFilled) { flowDone = true; }

                function renderFlowPerson(idx) {
                    const m = flowMembers[idx];
                    const mKey = `member_${idx}`;
                    const isLast = idx === flowMembers.length - 1;
                    const prevGen = idx > 0 ? flowMembers[idx-1].generation : null;
                    const showGenHeader = m.generation !== prevGen;
                    const photoStyle = m.photoPos ? `object-position: ${m.photoPos}` : '';

                    taskEl.innerHTML = `
                        <div class="flow-progress">
                            <div class="flow-progress-bar">
                                <div class="flow-progress-fill" style="width: ${((idx + 1) / flowMembers.length) * 100}%"></div>
                            </div>
                            <span class="flow-progress-text">${idx + 1} / ${flowMembers.length}</span>
                        </div>
                        ${showGenHeader ? `<div class="flow-generation">${m.generation}</div>` : ''}
                        <div class="flow-person ${isLast ? 'flow-person-hero' : ''}">
                            <div class="flow-photo">
                                <img src="${m.photo}" alt="${m.name}" style="${photoStyle}">
                            </div>
                            <h3 class="flow-name">${m.name}</h3>
                            <span class="flow-relation">${m.relation}</span>
                            ${!isLast ? `
                                <label class="flow-input-label">מילה אחת שמתארת את ${m.name}:</label>
                                <input type="text" class="task-input-small flow-word-input"
                                    data-quest="${questId}" data-key="${mKey}"
                                    value="${flowSaved[mKey] || ''}"
                                    placeholder="מילה אחת...">
                            ` : `
                                <div class="flow-hero-message">🎉 זה אתה! סיימת להכיר את כל המשפחה!</div>
                                <label class="flow-input-label">ומילה אחת שמתארת אותך?</label>
                                <input type="text" class="task-input-small flow-word-input"
                                    data-quest="${questId}" data-key="${mKey}"
                                    value="${flowSaved[mKey] || ''}"
                                    placeholder="מילה אחת...">
                            `}
                        </div>
                        <div class="flow-nav">
                            <button class="flow-btn flow-btn-prev" ${idx === 0 ? 'disabled' : ''}>→ הקודם</button>
                            <button class="flow-btn flow-btn-next ${isLast ? 'flow-btn-done' : ''}">${isLast ? '🌳 הצג עץ משפחה' : 'הבא ←'}</button>
                        </div>
                    `;

                    const prevBtn = taskEl.querySelector('.flow-btn-prev');
                    const nextBtn = taskEl.querySelector('.flow-btn-next');
                    const wordInput = taskEl.querySelector('.flow-word-input');

                    if (wordInput) {
                        wordInput.addEventListener('input', () => {
                            if (!state.responses[questId]) state.responses[questId] = {};
                            state.responses[questId][mKey] = wordInput.value;
                            saveState(state);
                        });
                    }

                    prevBtn.addEventListener('click', () => {
                        if (idx > 0) { currentIdx = idx - 1; renderFlowPerson(currentIdx); }
                    });

                    nextBtn.addEventListener('click', () => {
                        if (wordInput && wordInput.value.trim()) {
                            if (!state.responses[questId]) state.responses[questId] = {};
                            state.responses[questId][mKey] = wordInput.value;
                            saveState(state);
                        }
                        if (isLast) {
                            renderFamilyTree();
                        } else {
                            currentIdx = idx + 1;
                            renderFlowPerson(currentIdx);
                        }
                    });
                }

                function renderFamilyTree() {
                    const responses = state.responses[questId] || {};
                    // Group members by generation
                    const gen1 = flowMembers.filter(m => m.generation.includes('דור 1'));
                    const gen2 = flowMembers.filter(m => m.generation.includes('דור 2'));
                    const gen3 = flowMembers.filter(m => m.generation.includes('דור 3'));

                    function memberCard(m, idx) {
                        const word = responses[`member_${flowMembers.indexOf(m)}`] || '';
                        const posStyle = m.photoPos ? `object-position: ${m.photoPos}` : '';
                        const isGuy = m.relation.includes('אתה');
                        return `
                            <div class="tree-member ${isGuy ? 'tree-member-hero' : ''}">
                                <div class="tree-photo">
                                    <img src="${m.photo}" alt="${m.name}" style="${posStyle}">
                                </div>
                                <span class="tree-name">${m.name}</span>
                                <span class="tree-relation">${m.relation}</span>
                                ${word ? `<span class="tree-word">"${word}"</span>` : ''}
                            </div>
                        `;
                    }

                    taskEl.innerHTML = `
                        <div class="family-tree-visual">
                            <h3 class="tree-title">🌳 עץ המשפחה של גיא</h3>

                            <div class="tree-gen-label">סבים וסבתות</div>
                            <div class="tree-row tree-row-4">
                                ${gen1.map(m => memberCard(m)).join('')}
                            </div>

                            <div class="tree-connector-down"></div>

                            <div class="tree-gen-label">הורים ודודות</div>
                            <div class="tree-row tree-row-4">
                                ${gen2.map(m => memberCard(m)).join('')}
                            </div>

                            <div class="tree-connector-down"></div>

                            <div class="tree-gen-label">הילדים</div>
                            <div class="tree-row tree-row-3">
                                ${gen3.map(m => memberCard(m)).join('')}
                            </div>
                        </div>
                        <div class="flow-nav">
                            <button class="flow-btn flow-btn-prev">→ חזרה לרשימה</button>
                        </div>
                    `;

                    taskEl.querySelector('.flow-btn-prev').addEventListener('click', () => {
                        currentIdx = flowMembers.length - 1;
                        renderFlowPerson(currentIdx);
                    });

                    taskEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }

                if (flowDone) {
                    renderFamilyTree();
                } else {
                    renderFlowPerson(currentIdx);
                }
                break;

            case 'kahoot-guide':
                taskEl.innerHTML = `
                    <label class="task-label">${task.content}</label>
                    <ol class="kahoot-steps">
                        ${task.steps.map(s => `<li>${s}</li>`).join('')}
                    </ol>
                `;
                break;

            case 'checklist':
                taskEl.innerHTML = `<label class="task-label">${task.content}</label>`;
                const list = document.createElement('div');
                list.className = 'checklist';
                task.items.forEach((item, cIdx) => {
                    const cKey = `check_${tIdx}_${cIdx}`;
                    list.innerHTML += `
                        <label class="check-item">
                            <input type="checkbox" data-quest="${questId}" data-key="${cKey}"
                                ${savedResponses[cKey] ? 'checked' : ''}>
                            <span>${item}</span>
                        </label>
                    `;
                });
                taskEl.appendChild(list);
                break;

            case 'multiselect':
                taskEl.innerHTML = `<label class="task-label">${task.label}</label>`;
                const opts = document.createElement('div');
                opts.className = 'multiselect';
                task.options.forEach((opt, oIdx) => {
                    const oKey = `multi_${tIdx}_${oIdx}`;
                    opts.innerHTML += `
                        <label class="select-item">
                            <input type="checkbox" data-quest="${questId}" data-key="${oKey}"
                                ${savedResponses[oKey] ? 'checked' : ''}>
                            <span>${opt}</span>
                        </label>
                    `;
                });
                taskEl.appendChild(opts);
                break;

            case 'twin-shared':
                taskEl.innerHTML = `<label class="task-label">${task.label}</label>`;
                const shared = document.createElement('div');
                shared.className = 'twin-inputs';
                for (let i = 0; i < task.count; i++) {
                    const sKey = `shared_${i}`;
                    shared.innerHTML += `
                        <div class="twin-input-row">
                            <span class="twin-number">${i + 1}.</span>
                            <input type="text" class="task-input-small"
                                data-quest="${questId}" data-key="${sKey}"
                                value="${savedResponses[sKey] || ''}"
                                placeholder="${task.placeholder}">
                        </div>
                    `;
                }
                taskEl.appendChild(shared);
                break;

            case 'twin-unique':
                taskEl.innerHTML = `<label class="task-label">${task.label}</label>`;
                const unique = document.createElement('div');
                unique.className = 'twin-inputs';
                for (let i = 0; i < task.count; i++) {
                    const uKey = `unique_${i}`;
                    unique.innerHTML += `
                        <div class="twin-input-row">
                            <span class="twin-number">${i + 1}.</span>
                            <input type="text" class="task-input-small"
                                data-quest="${questId}" data-key="${uKey}"
                                value="${savedResponses[uKey] || ''}"
                                placeholder="${task.placeholder}">
                        </div>
                    `;
                }
                taskEl.appendChild(unique);
                break;

            case 'superpower-survey':
                taskEl.innerHTML = `<label class="task-label">${task.label}</label>`;
                const survey = document.createElement('div');
                survey.className = 'superpower-survey';
                for (let p = 0; p < task.people; p++) {
                    const nKey = `person_name_${p}`;
                    const pKey = `person_power_${p}`;
                    survey.innerHTML += `
                        <div class="survey-person">
                            <input type="text" class="task-input-small"
                                data-quest="${questId}" data-key="${nKey}"
                                value="${savedResponses[nKey] || ''}"
                                placeholder="שם האדם">
                            <select class="task-select" data-quest="${questId}" data-key="${pKey}">
                                <option value="">בחר סופרפאוור...</option>
                                ${task.powers.map(pw => `<option value="${pw}" ${savedResponses[pKey] === pw ? 'selected' : ''}>${pw}</option>`).join('')}
                            </select>
                        </div>
                    `;
                }
                taskEl.appendChild(survey);
                break;

            case 'support-map':
                taskEl.innerHTML = `<label class="task-label">${task.label}</label>`;
                const smap = document.createElement('div');
                smap.className = 'support-map';
                task.categories.forEach(cat => {
                    smap.innerHTML += `<h4 class="support-cat">${cat.name}</h4>`;
                    for (let s = 0; s < cat.slots; s++) {
                        const snKey = `support_${cat.name}_name_${s}`;
                        const smKey = `support_${cat.name}_msg_${s}`;
                        smap.innerHTML += `
                            <div class="support-person">
                                <input type="text" class="task-input-small"
                                    data-quest="${questId}" data-key="${snKey}"
                                    value="${savedResponses[snKey] || ''}"
                                    placeholder="שם">
                                <input type="text" class="task-input-small"
                                    data-quest="${questId}" data-key="${smKey}"
                                    value="${savedResponses[smKey] || ''}"
                                    placeholder="משפט אחד עליו/ה">
                            </div>
                        `;
                    }
                });
                taskEl.appendChild(smap);
                break;

            case 'achievement-picker':
                taskEl.innerHTML = `<label class="task-label">${task.label}</label>
                    <div class="task-info" style="font-style:italic; opacity:0.7">ההורים יוסיפו הישגים כאן</div>`;
                break;
        }

        body.appendChild(taskEl);
    });

    // Show/hide complete button based on completion
    const btn = document.getElementById('btn-complete');
    if (state.completedQuests.includes(questId)) {
        btn.textContent = '✓ המשימה הושלמה!';
        btn.disabled = true;
        btn.classList.add('completed');
    } else {
        btn.textContent = 'סיימתי את המשימה! ✓';
        btn.disabled = false;
        btn.classList.remove('completed');
    }

    // Auto-save on input
    setTimeout(() => {
        body.querySelectorAll('textarea, input[type="text"], select').forEach(el => {
            el.addEventListener('input', () => autoSaveInput(el));
            el.addEventListener('change', () => autoSaveInput(el));
        });
        body.querySelectorAll('input[type="checkbox"]').forEach(el => {
            el.addEventListener('change', () => {
                const qId = el.dataset.quest;
                const key = el.dataset.key;
                if (!state.responses[qId]) state.responses[qId] = {};
                state.responses[qId][key] = el.checked;
                saveState(state);
            });
        });
    }, 100);

    showScreen('quest');
}

function autoSaveInput(el) {
    const qId = el.dataset.quest;
    const key = el.dataset.key;
    if (!state.responses[qId]) state.responses[qId] = {};
    state.responses[qId][key] = el.value;
    saveState(state);
}

// ===== Complete Quest =====
function completeQuest() {
    const questId = state.currentQuest;
    if (!questId || state.completedQuests.includes(questId)) return;

    // Simple validation - check if at least one text field is filled
    const body = document.getElementById('quest-body');
    const textInputs = body.querySelectorAll('textarea, input[type="text"]');
    let hasContent = false;
    textInputs.forEach(el => {
        if (el.value.trim()) hasContent = true;
    });

    if (!hasContent && textInputs.length > 0) {
        showToast('צריך למלא לפחות שדה אחד לפני שממשיכים!');
        return;
    }

    state.completedQuests.push(questId);
    saveState(state);

    // XP animation
    showXPGain(QUESTS.find(q => q.id === questId));

    setTimeout(() => showHome(), 2000);
}

// ===== XP Animation =====
function showXPGain(quest) {
    const overlay = document.createElement('div');
    overlay.className = 'xp-overlay';
    overlay.innerHTML = `
        <div class="xp-popup">
            <div class="xp-popup-icon">${quest.icon}</div>
            <h3>משימה הושלמה!</h3>
            <div class="xp-gain">+${quest.xp} XP</div>
            <p class="xp-message">"${quest.message}"</p>
            ${quest.id < QUESTS.length ? '<p class="xp-next">המשימה הבאה נפתחה! 🔓</p>' : '<p class="xp-next">סיימת את כל המשימות! 🎉</p>'}
        </div>
    `;
    document.body.appendChild(overlay);
    setTimeout(() => overlay.classList.add('visible'), 50);
    setTimeout(() => {
        overlay.classList.remove('visible');
        setTimeout(() => overlay.remove(), 300);
    }, 2000);
}

// ===== Toast =====
function showToast(msg) {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = msg;
    document.body.appendChild(toast);
    setTimeout(() => toast.classList.add('visible'), 50);
    setTimeout(() => {
        toast.classList.remove('visible');
        setTimeout(() => toast.remove(), 300);
    }, 2500);
}

// ===== Hero Book =====
function openHeroBook() {
    const body = document.getElementById('book-body');
    body.innerHTML = '';

    // Title page
    body.innerHTML += `
        <div class="book-page title-page">
            <h1>ספר הגיבור שלי</h1>
            <h2>גיא</h2>
            <p>בר מצווה תשפ"ו</p>
        </div>
    `;

    // Each quest becomes a chapter
    QUESTS.forEach(quest => {
        const responses = state.responses[quest.id] || {};
        const page = document.createElement('div');
        page.className = 'book-page';
        page.style.borderColor = quest.color;

        let content = `
            <div class="book-chapter-header" style="background: ${quest.color}">
                <span class="chapter-icon">${quest.icon}</span>
                <h3>${quest.artifact.title}</h3>
            </div>
            <p class="book-message"><em>"${quest.message}"</em></p>
            <div class="book-responses">
        `;

        // Collect text responses
        Object.entries(responses).forEach(([key, value]) => {
            if (typeof value === 'string' && value.trim()) {
                content += `<p class="book-response">${value}</p>`;
            }
        });

        content += '</div>';
        page.innerHTML = content;
        body.appendChild(page);
    });

    showScreen('book');
}

// ===== PDF Export =====
function exportPDF() {
    showToast('פתח את תפריט ההדפסה (Ctrl+P) ובחר "שמור כ-PDF"');
    setTimeout(() => window.print(), 500);
}

function exportPresentation() {
    showToast('המצגת תיפתח בקרוב...');
    // Future: generate slides from quest data
}

// ===== Init =====
document.addEventListener('DOMContentLoaded', () => {
    showHome();
});
