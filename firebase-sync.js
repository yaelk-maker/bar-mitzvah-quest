// Firebase Cloud Sync — keeps quest progress in Firebase Realtime Database
// localStorage remains the fast local cache; Firebase is the source of truth.

const FIREBASE_CONFIG = {
    apiKey: "AIzaSyCAGHba3CYBq-5jUd4P2kn8NVbnjuTdmy0",
    authDomain: "bar-mitzvah-quest-c7280.firebaseapp.com",
    databaseURL: "https://bar-mitzvah-quest-c7280-default-rtdb.firebaseio.com",
    projectId: "bar-mitzvah-quest-c7280",
    storageBucket: "bar-mitzvah-quest-c7280.firebasestorage.app",
    messagingSenderId: "172950888190",
    appId: "1:172950888190:web:79c4c2947c0995f0e54faf"
};

const FAMILY_PASSCODE = "1907";

let firebaseReady = false;
let dbRef = null;

function initFirebase() {
    if (!FIREBASE_CONFIG.apiKey) {
        console.warn("Firebase not configured — running in local-only mode");
        return Promise.resolve(false);
    }
    try {
        firebase.initializeApp(FIREBASE_CONFIG);
        dbRef = firebase.database().ref('quest-progress');
        firebaseReady = true;
        return Promise.resolve(true);
    } catch (e) {
        console.error("Firebase init failed:", e);
        return Promise.resolve(false);
    }
}

function showPasscodeScreen() {
    return new Promise((resolve) => {
        if (sessionStorage.getItem('quest-passcode-ok')) {
            resolve(true);
            return;
        }

        const overlay = document.createElement('div');
        overlay.id = 'passcode-overlay';
        overlay.innerHTML = `
            <div class="passcode-box">
                <h2>🔐 כניסה למסע</h2>
                <p>הכנס את הסיסמה כדי להמשיך</p>
                <input type="password" id="passcode-input" placeholder="סיסמה..." autocomplete="off" />
                <button id="passcode-btn">כניסה</button>
                <div id="passcode-error" style="display:none">סיסמה שגויה, נסה שוב</div>
            </div>
        `;
        document.body.appendChild(overlay);

        const input = document.getElementById('passcode-input');
        const btn = document.getElementById('passcode-btn');
        const error = document.getElementById('passcode-error');

        function tryPasscode() {
            if (input.value === FAMILY_PASSCODE) {
                sessionStorage.setItem('quest-passcode-ok', '1');
                overlay.remove();
                resolve(true);
            } else {
                error.style.display = 'block';
                input.value = '';
                input.focus();
            }
        }

        btn.addEventListener('click', tryPasscode);
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') tryPasscode();
        });
        input.focus();
    });
}

async function syncFromCloud() {
    if (!firebaseReady || !dbRef) return null;
    try {
        const snapshot = await dbRef.once('value');
        return snapshot.val();
    } catch (e) {
        console.error("Firebase read failed:", e);
        return null;
    }
}

function syncToCloud(state) {
    if (!firebaseReady || !dbRef) return;
    try {
        dbRef.set(state);
    } catch (e) {
        console.error("Firebase write failed:", e);
    }
}

const LAST_RESET_KEY = 'quest-last-reset';

function mergeStates(local, cloud) {
    if (!cloud) return local;
    if (!local) return cloud;

    // Cross-device reset: if cloud has a newer resetAt than what we've seen,
    // wipe local and trust cloud as source of truth.
    const cloudReset = cloud.resetAt || 0;
    const lastSeenReset = parseInt(localStorage.getItem(LAST_RESET_KEY) || '0', 10);
    if (cloudReset > lastSeenReset) {
        localStorage.setItem(LAST_RESET_KEY, String(cloudReset));
        return {
            completedQuests: cloud.completedQuests || [],
            responses: cloud.responses || {},
            currentQuest: cloud.currentQuest || null,
            resetAt: cloudReset
        };
    }

    const merged = {
        completedQuests: [...new Set([
            ...(local.completedQuests || []),
            ...(cloud.completedQuests || [])
        ])].sort((a, b) => a - b),
        responses: { ...cloud.responses, ...local.responses },
        currentQuest: local.currentQuest || cloud.currentQuest || null,
        resetAt: Math.max(local.resetAt || 0, cloudReset)
    };

    Object.keys(cloud.responses || {}).forEach(key => {
        if (local.responses && local.responses[key]) {
            merged.responses[key] = { ...cloud.responses[key], ...local.responses[key] };
        }
    });

    return merged;
}

// Cross-device reset — bump resetAt so all other devices wipe on next load.
// Usage from browser console:
//   resetAllProgress()         -> full reset (all quests)
//   resetAllProgress([10])     -> reset only specific quest ids
async function resetAllProgress(questIds) {
    const now = Date.now();
    let newState;

    if (!questIds || questIds.length === 0) {
        // Full reset
        newState = {
            completedQuests: [],
            responses: {},
            currentQuest: null,
            resetAt: now
        };
    } else {
        // Partial reset — keep others, remove specified ids
        const current = JSON.parse(localStorage.getItem('bar-mitzvah-quest') || '{}');
        const responses = { ...(current.responses || {}) };
        questIds.forEach(id => delete responses[id]);
        newState = {
            completedQuests: (current.completedQuests || []).filter(id => !questIds.includes(id)),
            responses,
            currentQuest: null,
            resetAt: now
        };
    }

    localStorage.setItem('bar-mitzvah-quest', JSON.stringify(newState));
    localStorage.setItem(LAST_RESET_KEY, String(now));

    if (firebaseReady && dbRef) {
        await dbRef.set(newState);
    }

    console.log('✓ Progress reset. Other devices will sync on next load.');
    location.reload();
}
window.resetAllProgress = resetAllProgress;
