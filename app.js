// ===== Brainrot Characters - actual images on the map =====
const BRAINROT_CHARS = [
    // === STEAL A BRAINROT VOXEL CHARACTERS — positioned per user arrows ===
    { img: 'brainrot/sab-tralalero.png', top: '10%', right: '18%', size: '90px' },
    { img: 'brainrot/sab-shark.png',     top: '6%',  right: '5%',  size: '90px' },
    { img: 'brainrot/sab-spaghetti.png', top: '22%', left: '2%',   size: '90px' },
    { img: 'brainrot/sab-blue.png',      top: '28%', right: '5%',  size: '90px' },
    { img: 'brainrot/sab-giftbox.png',   top: '48%', left: '2%',   size: '90px' },
    { img: 'brainrot/sab-bat.png',       top: '48%', right: '5%',  size: '90px' },
    { img: 'brainrot/sab-67.png',        top: '68%', left: '15%',  size: '90px' },
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
            if (quest.id === 1) {
                // Special: show mini family tree thumbnail
                node.innerHTML = `
                    <div class="map-node-circle map-node-complete-circle map-node-ftree-thumb">
                        <div class="ftree-mini">
                            ${renderMiniFamilyTree()}
                        </div>
                        <span class="map-node-check">✓</span>
                    </div>
                    <div class="map-node-label">${quest.name}</div>
                    <div class="map-node-xp">XP ${quest.xp}+</div>
                `;
            } else {
                node.innerHTML = `
                    <div class="map-node-circle map-node-complete-circle">
                        <span class="map-node-emoji">${quest.mapIcon || quest.icon}</span>
                        <span class="map-node-check">✓</span>
                    </div>
                    <div class="map-node-label">${quest.name}</div>
                    <div class="map-node-xp">XP ${quest.xp}+</div>
                `;
            }
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

function renderMiniFamilyTree() {
    const quest = QUESTS.find(q => q.id === 1);
    if (!quest) return '';
    const flowMembers = quest.tasks[0].members;
    const positions = [
        { idx: 0, cx: 19,   cy: 23.5 },
        { idx: 1, cx: 38.5, cy: 23.5 },
        { idx: 2, cx: 61,   cy: 23.5 },
        { idx: 3, cx: 80,   cy: 23.5 },
        { idx: 6, cx: 10,   cy: 42.6 },
        { idx: 4, cx: 28.2, cy: 42.6 },
        { idx: 5, cx: 69.5, cy: 42.6 },
        { idx: 7, cx: 88.5, cy: 42.6 },
        { idx: 8,  cx: 32.5, cy: 62 },
        { idx: 10, cx: 49,   cy: 62 },
        { idx: 9,  cx: 64.2, cy: 62 },
    ];
    let html = '';
    positions.forEach(pos => {
        const m = flowMembers[pos.idx];
        const posStyle = m.photoPos ? `object-position: ${m.photoPos}` : '';
        const isHero = pos.idx === 10;
        html += `<div class="ftree-mini-photo ${isHero ? 'ftree-mini-hero' : ''}"
                      style="left:${pos.cx}%;top:${pos.cy}%;">
                    <img src="${m.photo}" alt="" style="${posStyle}" loading="lazy">
                 </div>`;
    });
    return html;
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

            case 'investigation-quiz':
                taskEl.innerHTML = `<label class="task-label">${task.label || ''}</label>`;
                const iqWrap = document.createElement('div');
                iqWrap.className = 'iq-container';
                const iqCompletionKey = `iq_completed`;
                const allSolved = task.steps.every((_, si) => savedResponses[`iq_step_${si}`] !== undefined);

                task.steps.forEach((step, sIdx) => {
                    const stepKey = `iq_step_${sIdx}`;
                    const savedAnswer = savedResponses[stepKey];
                    const isSolved = savedAnswer !== undefined;
                    const prevSolved = sIdx === 0 || savedResponses[`iq_step_${sIdx - 1}`] !== undefined;

                    const stepEl = document.createElement('div');
                    stepEl.className = 'iq-step' + (isSolved ? ' solved' : '') + (!prevSolved ? ' locked' : '');
                    stepEl.dataset.step = sIdx;

                    // Bold text within ** markers
                    const storyHtml = step.story.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');

                    stepEl.innerHTML = `
                        <div class="iq-step-header">
                            <span class="iq-step-number">${sIdx + 1}</span>
                            <h3 class="iq-step-title">${step.title}</h3>
                            ${isSolved ? '<span class="iq-check">✓</span>' : ''}
                        </div>
                        <p class="iq-story">${storyHtml}</p>
                        <p class="iq-question">${step.question}</p>
                        <div class="iq-options"></div>
                        <div class="iq-reveal ${isSolved ? 'visible' : ''}">
                            <div class="iq-image-wrap">
                                <img src="photos/${step.image}" alt="${step.caption}" class="iq-image" onerror="this.style.display='none'">
                            </div>
                            <p class="iq-caption">${step.caption}</p>
                            ${step.revealStory ? `<p class="iq-reveal-story">${step.revealStory}</p>` : ''}
                        </div>
                    `;

                    const optionsDiv = stepEl.querySelector('.iq-options');
                    step.options.forEach((opt, oIdx) => {
                        const btn = document.createElement('button');
                        const isCorrect = step.correct === -1 || oIdx === step.correct;
                        const wasChosen = savedAnswer === oIdx;
                        btn.className = 'iq-option-btn' + (wasChosen ? ' correct' : '') + (isSolved && !wasChosen ? ' faded' : '');
                        btn.textContent = `${String.fromCharCode(1488 + oIdx)}. ${opt}`;
                        btn.disabled = isSolved;

                        btn.addEventListener('click', () => {
                            if (stepEl.classList.contains('solved') || stepEl.classList.contains('locked')) return;
                            if (isCorrect) {
                                btn.classList.add('correct');
                                optionsDiv.querySelectorAll('.iq-option-btn').forEach(b => {
                                    b.disabled = true;
                                    if (b !== btn) b.classList.add('faded');
                                });
                                stepEl.classList.add('solved');
                                stepEl.querySelector('.iq-step-header').insertAdjacentHTML('beforeend', '<span class="iq-check">✓</span>');
                                stepEl.querySelector('.iq-reveal').classList.add('visible');
                                if (!state.responses[questId]) state.responses[questId] = {};
                                state.responses[questId][stepKey] = oIdx;
                                saveState(state);
                                // Unlock next step
                                const nextStep = iqWrap.querySelector(`.iq-step[data-step="${sIdx + 1}"]`);
                                if (nextStep) {
                                    nextStep.classList.remove('locked');
                                    setTimeout(() => nextStep.scrollIntoView({ behavior: 'smooth', block: 'center' }), 400);
                                }
                                // Check if all solved
                                const allNowSolved = task.steps.every((_, si) => {
                                    if (si === sIdx) return true;
                                    const r = state.responses[questId] || {};
                                    return r[`iq_step_${si}`] !== undefined;
                                });
                                if (allNowSolved) {
                                    iqWrap.querySelector('.iq-completion').classList.add('visible');
                                }
                            } else {
                                btn.classList.add('wrong');
                                setTimeout(() => btn.classList.remove('wrong'), 600);
                            }
                        });
                        optionsDiv.appendChild(btn);
                    });
                    iqWrap.appendChild(stepEl);
                });

                // Completion message
                const compEl = document.createElement('div');
                compEl.className = 'iq-completion' + (allSolved ? ' visible' : '');
                compEl.innerHTML = `<p>${task.completionMessage}</p>`;
                iqWrap.appendChild(compEl);
                taskEl.appendChild(iqWrap);
                break;

            case 'hero-journey':
                taskEl.innerHTML = '';
                const hjWrap = document.createElement('div');
                hjWrap.className = 'hj-container';
                // Instruction text
                const hjInstruction = document.createElement('div');
                hjInstruction.className = 'hj-instruction';
                hjInstruction.innerHTML = '📂 כדי לגלות את סיפור הגבורה שלך, פתח את 3 תיקי החקירה הבאים:';
                hjWrap.appendChild(hjInstruction);
                // Accordion cards
                const hjAccordion = document.createElement('div');
                hjAccordion.className = 'hj-accordion';
                task.stations.forEach((station, sIdx) => {
                    const sKey = `hj_station_${station.id}`;
                    const isRevealed = savedResponses[sKey] === true;
                    const card = document.createElement('div');
                    card.className = 'hj-card' + (isRevealed ? ' open' : '');
                    card.style.setProperty('--station-color', station.color);
                    // Card header (always visible, clickable)
                    const header = document.createElement('button');
                    header.className = 'hj-card-header';
                    header.setAttribute('aria-expanded', isRevealed ? 'true' : 'false');
                    header.innerHTML = `
                        <span class="hj-card-icon">${station.icon}</span>
                        <span class="hj-card-title">${station.title}</span>
                        <span class="hj-card-hint">${isRevealed ? 'סגור 🔼' : 'לחץ לפתיחה 🔽'}</span>
                    `;
                    // Card body (expandable)
                    const body = document.createElement('div');
                    body.className = 'hj-card-body';
                    body.innerHTML = `<p>${station.text}</p>`;
                    header.addEventListener('click', () => {
                        const isOpen = card.classList.contains('open');
                        if (isOpen) {
                            // Close this card
                            card.classList.remove('open');
                            header.querySelector('.hj-card-hint').textContent = 'לחץ לפתיחה 🔽';
                            header.setAttribute('aria-expanded', 'false');
                        } else {
                            // Open this card
                            card.classList.add('open');
                            header.querySelector('.hj-card-hint').textContent = 'סגור 🔼';
                            header.setAttribute('aria-expanded', 'true');
                            // Save as revealed
                            if (!state.responses[questId]) state.responses[questId] = {};
                            if (!state.responses[questId][sKey]) {
                                state.responses[questId][sKey] = true;
                                saveState(state);
                                updateCompleteButton();
                            }
                        }
                    });
                    card.appendChild(header);
                    card.appendChild(body);
                    hjAccordion.appendChild(card);
                });
                hjWrap.appendChild(hjAccordion);
                taskEl.appendChild(hjWrap);
                break;

            case 'power-stones':
                taskEl.innerHTML = `<label class="task-label">${task.label}</label>`;
                const psGrid = document.createElement('div');
                psGrid.className = 'ps-grid';
                task.stones.forEach((stone, sIdx) => {
                    const psKey = `power_stone_${sIdx}`;
                    const isLit = savedResponses[psKey] === true;
                    const stoneEl = document.createElement('div');
                    stoneEl.className = 'ps-stone' + (isLit ? ' lit' : '');
                    stoneEl.style.setProperty('--stone-color', stone.color);
                    stoneEl.innerHTML = `<span class="ps-icon">${stone.icon}</span><span class="ps-text">${stone.text}</span>`;
                    stoneEl.addEventListener('click', () => {
                        const nowLit = !stoneEl.classList.contains('lit');
                        stoneEl.classList.toggle('lit', nowLit);
                        if (!state.responses[questId]) state.responses[questId] = {};
                        state.responses[questId][psKey] = nowLit;
                        saveState(state);
                        updateCompleteButton();
                    });
                    psGrid.appendChild(stoneEl);
                });
                taskEl.appendChild(psGrid);
                break;

            case 'message-bubbles':
                taskEl.innerHTML = `<label class="task-label">${task.label}</label>`;
                const mbWrap = document.createElement('div');
                mbWrap.className = 'mb-container';
                const mbKey = `msg_bubble_${tIdx}`;
                task.bubbles.forEach((bubble, bIdx) => {
                    const bEl = document.createElement('div');
                    const isSelected = savedResponses[mbKey] === bIdx;
                    bEl.className = 'mb-bubble' + (isSelected ? ' selected' : '');
                    bEl.textContent = bubble;
                    bEl.addEventListener('click', () => {
                        mbWrap.querySelectorAll('.mb-bubble').forEach(b => b.classList.remove('selected'));
                        bEl.classList.add('selected');
                        if (!state.responses[questId]) state.responses[questId] = {};
                        state.responses[questId][mbKey] = bIdx;
                        saveState(state);
                        updateCompleteButton();
                    });
                    mbWrap.appendChild(bEl);
                });
                taskEl.appendChild(mbWrap);
                break;

            case 'story':
                const storyClass = task.style === 'parchment' ? 'story-parchment' : 'story-box';
                const storyText = task.text.replace(/\n/g, '<br>');
                taskEl.innerHTML = `
                    <div class="task-info">${task.content}</div>
                    <div class="${storyClass}">${storyText}</div>
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

                    // Strip prefixes from names (סבא, סבתא, אבא, אמא, דודה)
                    function shortName(fullName) {
                        return fullName.replace(/^(סבא|סבתא|אבא|אמא|דודה)\s+/, '');
                    }

                    // Two-layer positioning: photos on green circles, labels on pink banners
                    // Positions are % of the tree template image (2094x2048)
                    const treeMembers = [
                        // Top row - Grandparents (circles cy=23.5%, banner center=30.5%)
                        { idx: 0, cx: 19,   cy: 23.5, lx: 19,   ly: 30.5, cls: 'ftree-gp' },
                        { idx: 1, cx: 38.5, cy: 23.5, lx: 38.5, ly: 30.5, cls: 'ftree-gp' },
                        { idx: 2, cx: 61,   cy: 23.5, lx: 61,   ly: 30.5, cls: 'ftree-gp' },
                        { idx: 3, cx: 80,   cy: 23.5, lx: 80,   ly: 30.5, cls: 'ftree-gp' },
                        // Middle row - Parents & Aunts (circles cy=42.6%, banner center=49.7%)
                        { idx: 6, cx: 10,   cy: 42.6, lx: 10,   ly: 49.7, cls: 'ftree-parent' },
                        { idx: 4, cx: 28.2, cy: 42.6, lx: 28.2, ly: 49.7, cls: 'ftree-parent' },
                        { idx: 5, cx: 69.5, cy: 42.6, lx: 69.5, ly: 49.7, cls: 'ftree-parent' },
                        { idx: 7, cx: 88.5, cy: 42.6, lx: 88.5, ly: 49.7, cls: 'ftree-parent' },
                        // Bottom row - Children (circles cy=62%, banner center=69%)
                        { idx: 8,  cx: 32.5, cy: 62, lx: 32.5, ly: 69, cls: 'ftree-child' },
                        { idx: 10, cx: 49,   cy: 62, lx: 49,   ly: 69, cls: 'ftree-hero' },
                        { idx: 9,  cx: 64.2, cy: 62, lx: 64.2, ly: 69, cls: 'ftree-child' },
                    ];

                    function memberHTML(pos) {
                        const m = flowMembers[pos.idx];
                        const word = responses[`member_${pos.idx}`] || '';
                        const posStyle = m.photoPos ? `object-position: ${m.photoPos}` : '';
                        const name = shortName(m.name);
                        // Photo circle (centered on green circle)
                        let html = `
                            <div class="ftree-photo-circle ${pos.cls}" style="left: ${pos.cx}%; top: ${pos.cy}%;">
                                <img src="${m.photo}" alt="${name}" style="${posStyle}">
                            </div>
                        `;
                        // Label on pink banner — single line: "name - relation"
                        html += `
                            <div class="ftree-label ${pos.cls}" style="left: ${pos.lx}%; top: ${pos.ly}%;">
                                <div class="ftree-label-name">${name} - ${m.relation}</div>
                                ${word ? `<div class="ftree-label-word">"${word}"</div>` : ''}
                            </div>
                        `;
                        return html;
                    }

                    taskEl.innerHTML = `
                        <div class="ftree">
                            <h3 class="ftree-title">🌳 עץ המשפחה של גיא 🌳</h3>
                            <div class="ftree-map">
                                ${treeMembers.map(pos => memberHTML(pos)).join('')}
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

            case 'drag-select':
                const dsKey = `drag_${tIdx}`;
                taskEl.innerHTML = `<label class="task-label">${task.label}</label>`;
                const dsContainer = document.createElement('div');
                dsContainer.className = 'drag-select-options';
                task.options.forEach((opt, oIdx) => {
                    const btn = document.createElement('div');
                    btn.className = 'drag-select-option' + (savedResponses[dsKey] === opt ? ' selected' : '');
                    btn.textContent = opt;
                    btn.addEventListener('click', () => {
                        dsContainer.querySelectorAll('.drag-select-option').forEach(b => b.classList.remove('selected'));
                        btn.classList.add('selected');
                        if (!state.responses[questId]) state.responses[questId] = {};
                        state.responses[questId][dsKey] = opt;
                        saveState(state);
                        updateCompleteButton();
                    });
                    dsContainer.appendChild(btn);
                });
                taskEl.appendChild(dsContainer);
                break;

            case 'brain-meters':
                taskEl.innerHTML = `<label class="task-label">${task.label}</label>`;
                const metersWrap = document.createElement('div');
                metersWrap.className = 'brain-meters';
                task.traits.forEach(trait => {
                    const mKey = `brain_meter_${trait.id}`;
                    const savedLevel = savedResponses[mKey] || null;
                    const row = document.createElement('div');
                    row.className = 'meter-row';
                    row.innerHTML = `
                        <div class="meter-header">
                            <span class="meter-icon">${trait.icon}</span>
                            <span class="meter-name">${trait.name}</span>
                        </div>
                        <div class="meter-bar-track">
                            <div class="meter-bar-fill" style="background:${trait.color};width:${savedLevel !== null ? ((task.levels.indexOf(savedLevel) + 1) / task.levels.length * 100) : 0}%"></div>
                        </div>
                        <div class="meter-levels"></div>
                    `;
                    const levelsDiv = row.querySelector('.meter-levels');
                    const fillBar = row.querySelector('.meter-bar-fill');
                    task.levels.forEach((level, lIdx) => {
                        const btn = document.createElement('button');
                        btn.className = 'meter-level-btn' + (savedLevel === level ? ' selected' : '');
                        btn.textContent = level;
                        btn.style.setProperty('--meter-color', trait.color);
                        btn.addEventListener('click', () => {
                            levelsDiv.querySelectorAll('.meter-level-btn').forEach(b => b.classList.remove('selected'));
                            btn.classList.add('selected');
                            fillBar.style.width = ((lIdx + 1) / task.levels.length * 100) + '%';
                            if (!state.responses[questId]) state.responses[questId] = {};
                            state.responses[questId][mKey] = level;
                            saveState(state);
                            if (typeof checkAllMetersFilled === 'function') checkAllMetersFilled();
                            updateCompleteButton();
                        });
                        levelsDiv.appendChild(btn);
                    });
                    metersWrap.appendChild(row);
                });
                taskEl.appendChild(metersWrap);
                // Brain bubble map reveal button + section
                const brainSection = document.createElement('div');
                brainSection.className = 'brain-map-section';
                const brainBtn = document.createElement('button');
                brainBtn.className = 'brain-map-reveal-btn';
                brainBtn.textContent = 'גלה את מפת המוח שלי! 🧠';
                brainBtn.disabled = true;

                const brainResult = document.createElement('div');
                brainResult.className = 'brain-map-result';

                function checkAllMetersFilled() {
                    const filled = task.traits.every(t => {
                        const k = `brain_meter_${t.id}`;
                        return state.responses[questId] && state.responses[questId][k];
                    });
                    brainBtn.disabled = !filled;
                    brainBtn.classList.toggle('ready', filled);
                }

                // Brain outline path + bubble positions inside the brain
                const BRAIN_PATH = 'M150,25 C90,25 45,50 35,90 C25,130 30,160 50,185 C60,200 75,215 90,225 C105,235 125,245 150,248 C175,245 195,235 210,225 C225,215 240,200 250,185 C270,160 275,130 265,90 C255,50 210,25 150,25 Z';
                const BUBBLE_POS = [
                    { cx: 100, cy: 75 },   // creativity - top left
                    { cx: 200, cy: 75 },   // senses - top right
                    { cx: 75,  cy: 145 },  // focus - mid left
                    { cx: 225, cy: 145 },  // movement - mid right
                    { cx: 110, cy: 205 },  // feelings - bottom left
                    { cx: 190, cy: 205 },  // memory - bottom right
                ];

                function buildBrainSVG(values, colors, labels, icons, maxVal, isTypical) {
                    const minR = 12, maxR = 38;
                    let defs = `<defs>`;
                    let circles = '';
                    let labelEls = '';

                    for (let i = 0; i < values.length; i++) {
                        const ratio = values[i] / maxVal;
                        const r = minR + ratio * (maxR - minR);
                        const color = isTypical ? '#aab' : colors[i];
                        const pos = BUBBLE_POS[i];
                        const filterId = `glow-${isTypical ? 'typ' : 'usr'}-${i}`;

                        // Glow filter for large bubbles (value >= 3)
                        if (values[i] >= 3 && !isTypical) {
                            defs += `<filter id="${filterId}" x="-50%" y="-50%" width="200%" height="200%">
                                <feGaussianBlur in="SourceGraphic" stdDeviation="4" result="blur"/>
                                <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
                            </filter>`;
                        }

                        const filterAttr = (values[i] >= 3 && !isTypical) ? ` filter="url(#${filterId})"` : '';
                        circles += `<circle cx="${pos.cx}" cy="${pos.cy}" r="${r}" fill="${color}" fill-opacity="0.7"${filterAttr} class="brain-bubble"/>`;

                        // Icon + label
                        labelEls += `<text x="${pos.cx}" y="${pos.cy - 1}" text-anchor="middle" dominant-baseline="central" font-size="${r > 25 ? 20 : 16}" font-family="sans-serif">${icons[i]}</text>`;
                        labelEls += `<text x="${pos.cx}" y="${pos.cy + r + 14}" text-anchor="middle" fill="${color}" font-size="10" font-weight="700" font-family="Heebo,sans-serif">${labels[i]}</text>`;
                    }
                    defs += `</defs>`;

                    const brainFill = isTypical ? '#f0f0f5' : 'linear-gradient(#eef,#e8e0ff)';
                    return `<svg viewBox="0 0 300 280" class="brain-map-svg">
                        ${defs}
                        <path d="${BRAIN_PATH}" fill="${isTypical ? '#f0f0f5' : '#ece6ff'}" stroke="${isTypical ? '#ccc' : '#9B59B6'}" stroke-width="2.5" fill-opacity="0.5"/>
                        ${circles}
                        ${labelEls}
                    </svg>`;
                }

                metersWrap.addEventListener('click', () => setTimeout(checkAllMetersFilled, 50));
                checkAllMetersFilled();

                const brainRevealed = savedResponses['radar_revealed'] === true;

                brainBtn.addEventListener('click', () => {
                    if (!state.responses[questId]) state.responses[questId] = {};
                    state.responses[questId]['radar_revealed'] = true;
                    saveState(state);
                    showBrainMap();
                });

                function showBrainMap() {
                    const traitLabels = task.traits.map(t => t.name.split(' ')[0]);
                    const traitColors = task.traits.map(t => t.color);
                    const traitIcons = task.traits.map(t => t.icon);
                    const userValues = task.traits.map(t => {
                        const level = state.responses[questId] && state.responses[questId][`brain_meter_${t.id}`];
                        return level ? task.levels.indexOf(level) + 1 : 2;
                    });
                    const typicalValues = [2, 2, 2, 2, 2, 2];
                    const maxVal = task.levels.length;

                    const typicalSVG = buildBrainSVG(typicalValues, traitColors, traitLabels, traitIcons, maxVal, true);
                    const userSVG = buildBrainSVG(userValues, traitColors, traitLabels, traitIcons, maxVal, false);

                    brainResult.innerHTML = `
                        <div class="brain-map-charts">
                            <div class="brain-map-box">
                                <div class="brain-map-title">מוח טיפוסי</div>
                                ${typicalSVG}
                                <p class="brain-map-desc">רוב היכולות דורשות כמות אנרגיה דומה</p>
                            </div>
                            <div class="brain-map-box highlight">
                                <div class="brain-map-title">המוח המיוחד שלי! ⭐</div>
                                ${userSVG}
                                <p class="brain-map-desc">מוח עם "כוחות-על" בולטים ואזורים שדורשים פחות אנרגיה. קוראים לזה "פרופיל קופצני", וזה מה שעושה אותך מומחה!</p>
                            </div>
                        </div>
                    `;
                    brainResult.classList.add('visible');
                    brainBtn.style.display = 'none';
                    brainResult.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }

                brainSection.appendChild(brainBtn);
                brainSection.appendChild(brainResult);
                taskEl.appendChild(brainSection);

                if (brainRevealed) showBrainMap();
                break;

            case 'brain-cards':
                taskEl.innerHTML = `<label class="task-label">${task.label}</label>`;
                const cardsGrid = document.createElement('div');
                cardsGrid.className = 'brain-cards-grid';
                task.cards.forEach((card, cIdx) => {
                    const cardKey = `brain_card_${cIdx}`;
                    const isClaimed = savedResponses[cardKey] === true;
                    const cardEl = document.createElement('div');
                    cardEl.className = 'brain-card' + (isClaimed ? ' claimed' : '');
                    cardEl.innerHTML = `
                        <div class="brain-card-inner">
                            <div class="brain-card-front">
                                <span class="brain-card-icon">${card.front.icon}</span>
                                <span class="brain-card-title">${card.front.title}</span>
                            </div>
                            <div class="brain-card-back">
                                <p class="brain-card-desc">${card.back}</p>
                                <button class="btn-claim ${isClaimed ? 'claimed' : ''}">${isClaimed ? '✓ זה אני!' : 'זה אני!'}</button>
                            </div>
                        </div>
                    `;
                    cardEl.addEventListener('click', (e) => {
                        if (e.target.closest('.btn-claim')) return;
                        cardEl.classList.toggle('flipped');
                    });
                    const claimBtn = cardEl.querySelector('.btn-claim');
                    claimBtn.addEventListener('click', (e) => {
                        e.stopPropagation();
                        const nowClaimed = !cardEl.classList.contains('claimed');
                        cardEl.classList.toggle('claimed', nowClaimed);
                        claimBtn.classList.toggle('claimed', nowClaimed);
                        claimBtn.textContent = nowClaimed ? '✓ זה אני!' : 'זה אני!';
                        if (!state.responses[questId]) state.responses[questId] = {};
                        state.responses[questId][cardKey] = nowClaimed;
                        saveState(state);
                        updateCompleteButton();
                    });
                    cardsGrid.appendChild(cardEl);
                });
                taskEl.appendChild(cardsGrid);
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
        btn.classList.remove('completed');
        // Hide the complete button for quests with family-flow until tree is shown
        const hasFlow = quest.tasks.some(t => t.type === 'family-flow');
        if (hasFlow) {
            footer.style.display = 'none';
        } else {
            footer.style.display = '';
        }
        // Validate before enabling
        const { valid } = getQuestValidation(questId);
        btn.disabled = !valid;
        btn.classList.toggle('not-ready', !valid);
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

// ===== Quest Validation =====
function getQuestValidation(questId) {
    const quest = QUESTS.find(q => q.id === questId);
    if (!quest) return { valid: true, missing: [] };
    const responses = state.responses[questId] || {};
    const missing = [];

    quest.tasks.forEach((task, tIdx) => {
        switch (task.type) {
            case 'hero-journey':
                const anyOpened = task.stations.some(s => responses[`hj_station_${s.id}`]);
                if (!anyOpened) missing.push('תיקי החקירה');
                break;
            case 'power-stones':
                const anyStone = task.stones.some((_, i) => responses[`power_stone_${i}`]);
                if (!anyStone) missing.push('אבני הכוח');
                break;
            case 'message-bubbles':
                if (responses[`msg_bubble_${tIdx}`] === undefined) missing.push('המשפט לגיא התינוק');
                break;
            case 'brain-meters':
                const anyMeter = task.traits.some(t => responses[`brain_meter_${t.id}`]);
                if (!anyMeter) missing.push('עוצמות התכונות');
                break;
            case 'brain-cards':
                const anyCard = task.cards.some((_, i) => responses[`brain_card_${i}`]);
                if (!anyCard) missing.push('כרטיסי המוח');
                break;
            case 'drag-select':
                if (responses[`drag_${tIdx}`] === undefined) missing.push('המשפט שמתאים לך');
                break;
        }
    });

    return { valid: missing.length === 0, missing };
}

function updateCompleteButton() {
    const questId = state.currentQuest;
    if (!questId || state.completedQuests.includes(questId)) return;
    const btn = document.getElementById('btn-complete');
    const { valid } = getQuestValidation(questId);
    btn.disabled = !valid;
    btn.classList.toggle('not-ready', !valid);
}

// ===== Complete Quest =====
function completeQuest() {
    const questId = state.currentQuest;
    if (!questId || state.completedQuests.includes(questId)) return;

    const { valid, missing } = getQuestValidation(questId);
    if (!valid) {
        showToast(`עוד לא סיימת! חסר: ${missing.join(', ')}`);
        return;
    }

    // Also check text fields if any
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
