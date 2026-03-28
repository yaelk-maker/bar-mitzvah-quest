// ===== Brainrot Characters - actual images on the map =====
const BRAINROT_CHARS = [
    // === STEAL A BRAINROT VOXEL CHARACTERS ONLY (from Figures folder) ===
    { img: 'brainrot/sab-tralalero.png', top: '8%',  left: '2%',   size: '80px',  anim: 'brFloat1', delay: '0s' },
    { img: 'brainrot/sab-shark.png',     top: '10%', right: '8%',  size: '75px',  anim: 'brFloat2', delay: '0.5s' },
    { img: 'brainrot/sab-spaghetti.png', top: '32%', left: '2%',   size: '70px',  anim: 'brBounce', delay: '1s' },
    { img: 'brainrot/sab-blue.png',      top: '38%', right: '8%',  size: '70px',  anim: 'brFloat3', delay: '0.3s' },
    { img: 'brainrot/sab-giftbox.png',   top: '55%', left: '2%',   size: '65px',  anim: 'brFloat1', delay: '0.8s' },
    { img: 'brainrot/sab-bat.png',       top: '58%', right: '8%',  size: '70px',  anim: 'brFloat2', delay: '1.2s' },
    { img: 'brainrot/sab-67.png',        top: '74%', left: '4%',   size: '65px',  anim: 'brBounce', delay: '0.5s' },
];

// ===== Lava particles (subtle embers floating on the map) =====
const ISLAND_DECOS = [
    { emoji: '🔥', top: '85%', left: '10%',  size: '1rem',   opacity: 0.4 },
    { emoji: '🔥', top: '88%', right: '15%', size: '0.9rem', opacity: 0.35 },
    { emoji: '✨', top: '15%', left: '50%',  size: '0.8rem', opacity: 0.3 },
    { emoji: '✨', top: '45%', right: '40%', size: '0.7rem', opacity: 0.25 },
    { emoji: '✨', top: '70%', left: '45%',  size: '0.8rem', opacity: 0.3 },
];

function renderBrainrotChars() {
    const container = document.getElementById('brainrot-container');
    if (!container) return;
    container.innerHTML = '';

    // Render island decorations first
    ISLAND_DECOS.forEach(deco => {
        const el = document.createElement('div');
        el.style.position = 'absolute';
        el.style.top = deco.top;
        if (deco.left) el.style.left = deco.left;
        if (deco.right) el.style.right = deco.right;
        el.style.fontSize = deco.size;
        el.style.opacity = deco.opacity;
        el.style.pointerEvents = 'none';
        el.style.zIndex = '0';
        el.textContent = deco.emoji;
        container.appendChild(el);
    });

    // Render brainrot characters
    BRAINROT_CHARS.forEach((ch, i) => {
        const el = document.createElement('div');
        el.className = 'brainrot';
        el.style.position = 'absolute';
        el.style.top = ch.top;
        if (ch.left) el.style.left = ch.left;
        if (ch.right) el.style.right = ch.right;
        el.style.width = ch.size;
        el.style.height = ch.size;
        el.style.animation = `${ch.anim} 4s ease-in-out infinite ${ch.delay}`;
        el.style.zIndex = '1';
        el.style.pointerEvents = 'none';

        const img = document.createElement('img');
        img.src = ch.img;
        img.alt = '';
        img.style.width = '100%';
        img.style.height = '100%';
        img.style.objectFit = 'contain';
        img.style.filter = 'drop-shadow(3px 5px 10px rgba(0,0,0,0.45)) drop-shadow(0 0 6px rgba(255,255,255,0.2))';
        // If image fails to load, hide this character
        img.onerror = () => { el.style.display = 'none'; };
        el.appendChild(img);
        container.appendChild(el);
    });
}

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
    document.getElementById('home-xp-text').textContent = `XP ${xp} / ${TOTAL_XP}`;
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

// ===== Quest Map - Treasure Map =====
function renderQuestMap() {
    const map = document.getElementById('quest-map');
    const svg = document.getElementById('map-path-svg');
    map.innerHTML = '';

    // Build ALL quest statuses
    const allQuests = QUESTS.map((quest, idx) => {
        const isCompleted = state.completedQuests.includes(quest.id);
        const isUnlocked = idx === 0 || state.completedQuests.includes(QUESTS[idx - 1].id);
        const isNext = isUnlocked && !isCompleted;
        const isLocked = !isCompleted && !isNext;
        return { quest, idx, isCompleted, isNext, isLocked };
    });

    // Render ALL quest nodes on the map
    allQuests.forEach(({ quest, idx, isCompleted, isNext, isLocked }) => {
        const pos = MAP_POSITIONS[idx];
        const node = document.createElement('div');
        node.className = `map-node ${isCompleted ? 'map-node-done' : ''} ${isNext ? 'map-node-next' : ''} ${isLocked ? 'map-node-locked' : ''}`;
        node.style.left = pos.x + '%';
        node.style.top = pos.y + '%';
        node.style.setProperty('--node-color', quest.color);

        if (isCompleted) {
            node.innerHTML = `
                <div class="map-node-circle map-node-complete-circle">
                    <span class="map-node-emoji">${quest.mapIcon || quest.icon}</span>
                    <span class="map-node-check">✓</span>
                </div>
                <div class="map-node-label">${quest.name}</div>
                <div class="map-node-xp">XP ${quest.xp}+</div>
            `;
            node.addEventListener('click', () => openQuest(quest.id));
        } else if (isNext) {
            node.innerHTML = `
                <div class="map-node-circle map-node-next-circle">
                    <span class="map-node-emoji">${quest.mapIcon || quest.icon}</span>
                </div>
                <div class="map-node-label">${quest.name}</div>
                <div class="map-node-subtitle">${quest.subtitle}</div>
                <div class="map-node-start">התחל →</div>
            `;
            node.addEventListener('click', () => openQuest(quest.id));
        } else {
            // Locked quest - grey circle with lock, NO name
            node.innerHTML = `
                <div class="map-node-circle map-node-locked-circle">
                    <span class="map-node-emoji">🔒</span>
                </div>
                <div class="map-node-step">${idx + 1}</div>
            `;
        }

        map.appendChild(node);
    });

    // Draw SVG path connecting ALL quests
    drawMapPath(svg, allQuests);

    // Hero Book node if all done
    if (state.completedQuests.length === QUESTS.length) {
        const bookNode = document.createElement('div');
        bookNode.className = 'map-node map-node-treasure';
        bookNode.style.left = '55%';
        bookNode.style.top = '95%';
        bookNode.innerHTML = `
            <div class="map-node-circle map-node-treasure-circle">
                <span class="map-node-emoji">📖</span>
            </div>
            <div class="map-node-label">ספר הגיבור שלי</div>
            <div class="map-node-start">פתח →</div>
        `;
        bookNode.addEventListener('click', () => openHeroBook());
        map.appendChild(bookNode);
    }
}

function drawMapPath(svg, allQuests) {
    svg.setAttribute('viewBox', '0 0 100 100');

    // Clear existing paths (keep defs at index 0)
    while (svg.children.length > 1) svg.removeChild(svg.lastChild);

    if (allQuests.length < 2) return;

    // Build path through ALL quest positions
    const points = allQuests.map(({ idx }) => {
        const pos = MAP_POSITIONS[idx];
        return { x: pos.x, y: pos.y };
    });

    // Create smooth curve through points
    let d = `M ${points[0].x} ${points[0].y}`;
    for (let i = 1; i < points.length; i++) {
        const prev = points[i - 1];
        const curr = points[i];
        const cpx1 = prev.x + (curr.x - prev.x) * 0.5;
        const cpy1 = prev.y;
        const cpx2 = prev.x + (curr.x - prev.x) * 0.5;
        const cpy2 = curr.y;
        d += ` C ${cpx1} ${cpy1}, ${cpx2} ${cpy2}, ${curr.x} ${curr.y}`;
    }

    // Outer lava glow
    const glow = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    glow.setAttribute('d', d);
    glow.setAttribute('fill', 'none');
    glow.setAttribute('stroke', 'rgba(255,120,0,0.3)');
    glow.setAttribute('stroke-width', '8');
    glow.setAttribute('stroke-linecap', 'round');
    glow.setAttribute('filter', 'url(#pathGlow)');
    svg.appendChild(glow);

    // Dark outline
    const trailBorder = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    trailBorder.setAttribute('d', d);
    trailBorder.setAttribute('fill', 'none');
    trailBorder.setAttribute('stroke', '#2a1a0a');
    trailBorder.setAttribute('stroke-width', '5.5');
    trailBorder.setAttribute('stroke-linecap', 'round');
    trailBorder.setAttribute('stroke-linejoin', 'round');
    svg.appendChild(trailBorder);

    // Main lava path (orange/amber)
    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.setAttribute('d', d);
    path.setAttribute('fill', 'none');
    path.setAttribute('stroke', '#ff8f00');
    path.setAttribute('stroke-width', '3.5');
    path.setAttribute('stroke-dasharray', '10 6');
    path.setAttribute('stroke-linecap', 'round');
    svg.appendChild(path);

    // Green completed overlay for completed segments
    const completedCount = allQuests.filter(v => v.isCompleted).length;
    if (completedCount >= 1) {
        // Draw solid green from first to last completed + next
        const greenEnd = Math.min(completedCount, points.length - 1);
        const greenPoints = points.slice(0, greenEnd + 1);
        if (greenPoints.length >= 2) {
            let cd = `M ${greenPoints[0].x} ${greenPoints[0].y}`;
            for (let i = 1; i < greenPoints.length; i++) {
                const prev = greenPoints[i - 1];
                const curr = greenPoints[i];
                cd += ` C ${prev.x + (curr.x - prev.x) * 0.5} ${prev.y}, ${prev.x + (curr.x - prev.x) * 0.5} ${curr.y}, ${curr.x} ${curr.y}`;
            }
            const donePath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
            donePath.setAttribute('d', cd);
            donePath.setAttribute('fill', 'none');
            donePath.setAttribute('stroke', '#76ff03');
            donePath.setAttribute('stroke-width', '3.5');
            donePath.setAttribute('stroke-linecap', 'round');
            svg.appendChild(donePath);
        }
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
                        // Always save the word input
                        if (wordInput) {
                            if (!state.responses[questId]) state.responses[questId] = {};
                            state.responses[questId][mKey] = wordInput.value;
                            saveState(state);
                        }
                        if (isLast) {
                            // Show the family tree
                            renderFamilyTree();
                        } else {
                            currentIdx = idx + 1;
                            renderFlowPerson(currentIdx);
                        }
                    });
                }

                function renderFamilyTree() {
                    const responses = state.responses[questId] || {};

                    function card(m, size) {
                        const word = responses[`member_${flowMembers.indexOf(m)}`] || '';
                        const posStyle = m.photoPos ? `object-position: ${m.photoPos}` : '';
                        const isGuy = m.relation.includes('אתה');
                        const sz = size || 'sm';
                        return `
                            <div class="ftree-card ftree-${sz} ${isGuy ? 'ftree-hero' : ''}">
                                <div class="ftree-photo"><img src="${m.photo}" alt="${m.name}" style="${posStyle}"></div>
                                <div class="ftree-info">
                                    <div class="ftree-name">${m.name}</div>
                                    <div class="ftree-relation">${m.relation}</div>
                                    ${word ? `<div class="ftree-word">"${word}"</div>` : ''}
                                </div>
                            </div>
                        `;
                    }

                    // Specific family members
                    const sM = flowMembers[0];
                    const sR = flowMembers[1];
                    const sA = flowMembers[2];
                    const sS = flowMembers[3];
                    const dad = flowMembers[4];
                    const mom = flowMembers[5];
                    const auntI = flowMembers[6];
                    const auntJ = flowMembers[7];
                    const neta = flowMembers[8];
                    const mika = flowMembers[9];
                    const guy = flowMembers[10];

                    taskEl.innerHTML = `
                        <div class="ftree">
                            <h3 class="ftree-title">🌳 עץ המשפחה של גיא 🌳</h3>

                            <!-- CANOPY: Grandparents + Parents inside the green tree crown -->
                            <div class="ftree-canopy">
                                <!-- Grandparents -->
                                <div class="ftree-gen">
                                    <div class="ftree-gen-label">סבים וסבתות</div>
                                    <div class="ftree-row ftree-gp-row">
                                        <div class="ftree-couple">
                                            ${card(sM, 'sm')}
                                            <span class="ftree-connector-h">❤️</span>
                                            ${card(sR, 'sm')}
                                        </div>
                                        <div class="ftree-couple">
                                            ${card(sA, 'sm')}
                                            <span class="ftree-connector-h">❤️</span>
                                            ${card(sS, 'sm')}
                                        </div>
                                    </div>
                                </div>

                                <!-- Branch lines -->
                                <div class="ftree-lines">
                                    <div class="ftree-vline"></div>
                                    <div class="ftree-vline"></div>
                                </div>

                                <!-- Parents & Aunts -->
                                <div class="ftree-gen">
                                    <div class="ftree-gen-label">הורים ודודות</div>
                                    <div class="ftree-row ftree-parents-row">
                                        ${card(auntI, 'sm')}
                                        <div class="ftree-couple ftree-couple-main">
                                            ${card(dad, 'md')}
                                            <span class="ftree-connector-h ftree-heart-big">💕</span>
                                            ${card(mom, 'md')}
                                        </div>
                                        ${card(auntJ, 'sm')}
                                    </div>
                                </div>
                            </div>

                            <!-- TRUNK -->
                            <div class="ftree-trunk"></div>

                            <!-- BASE: Children on the grass -->
                            <div class="ftree-gen ftree-gen-kids">
                                <div class="ftree-gen-label ftree-gen-label-special">הילדים 🌟</div>
                                <div class="ftree-row ftree-kids-row">
                                    ${card(neta, 'md')}
                                    ${card(guy, 'lg')}
                                    ${card(mika, 'md')}
                                </div>
                            </div>
                        </div>
                        <div class="flow-nav" style="margin-top:16px">
                            <button class="flow-btn flow-btn-prev">→ חזרה לרשימה</button>
                        </div>
                    `;

                    taskEl.querySelector('.flow-btn-prev').addEventListener('click', () => {
                        currentIdx = flowMembers.length - 1;
                        const ft = document.querySelector('.quest-footer');
                        if (ft) ft.style.display = 'none';
                        renderFlowPerson(currentIdx);
                    });

                    const ft = document.querySelector('.quest-footer');
                    if (ft) ft.style.display = '';

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
    const footer = document.querySelector('.quest-footer');
    if (state.completedQuests.includes(questId)) {
        btn.textContent = '✓ המשימה הושלמה!';
        btn.disabled = true;
        btn.classList.add('completed');
        footer.style.display = '';
    } else {
        btn.textContent = 'סיימתי את המשימה! ✓';
        btn.disabled = false;
        btn.classList.remove('completed');
        // Hide the complete button for quests with family-flow until tree is shown
        const hasFlow = quest.tasks.some(t => t.type === 'family-flow');
        if (hasFlow) {
            footer.style.display = 'none';
        } else {
            footer.style.display = '';
        }
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
    renderBrainrotChars();
    showHome();
});
