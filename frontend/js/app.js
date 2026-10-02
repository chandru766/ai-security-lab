const API_BASE = '/api';
let currentToken = null;
let currentLabId = null;
let currentModuleId = null;
let currentLessonId = null;
let currentQuizAttemptId = null;
window.LEARNING_MODULES_CACHE = null;
window.LABS_CACHE = null;

function showToast(message) {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.style.opacity = 1;
    setTimeout(() => toast.style.opacity = 0, 3000);
}

function getHeaders() {
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${currentToken}`
    };
}

document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const u = document.getElementById('username').value;
    const p = document.getElementById('password').value;
    const formData = new FormData();
    formData.append('username', u);
    formData.append('password', p);

    try {
        const res = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            body: formData
        });
        if (res.ok) {
            const data = await res.json();
            currentToken = data.access_token;
            document.getElementById('login-container').classList.add('hidden');
            document.getElementById('dashboard-container').classList.remove('hidden');
            
            const userRes = await fetch(`${API_BASE}/auth/me`, { headers: getHeaders() });
            const userData = await userRes.json();
            document.getElementById('current-user').textContent = userData.username;
            
            initDashboard();
        } else {
            document.getElementById('login-error').textContent = 'Invalid credentials';
            document.getElementById('login-error').classList.remove('hidden');
        }
    } catch (e) {
        document.getElementById('login-error').textContent = 'Connection error';
        document.getElementById('login-error').classList.remove('hidden');
    }
});

document.getElementById('logout-btn').addEventListener('click', () => {
    currentToken = null;
    document.getElementById('dashboard-container').classList.add('hidden');
    document.getElementById('login-container').classList.remove('hidden');
});

// ROUTING
window.addEventListener('hashchange', handleRoute);

function handleRoute() {
    if (!currentToken) return;
    const hash = window.location.hash || '#/home';
    
    document.querySelectorAll('.section').forEach(el => el.classList.add('hidden'));
    document.querySelectorAll('.nav-links a').forEach(el => el.classList.remove('active'));
    
    if (hash.startsWith('#/labs/')) {
        document.getElementById('section-lab-detail').classList.remove('hidden');
        document.getElementById('nav-labs').classList.add('active');
        openLab(hash.split('/')[2]);
    } else if (hash === '#/labs') {
        document.getElementById('section-labs').classList.remove('hidden');
        document.getElementById('nav-labs').classList.add('active');
        loadLabs();
    } else if (hash.startsWith('#/learning/')) {
        document.getElementById('section-learning-detail').classList.remove('hidden');
        document.getElementById('nav-learning').classList.add('active');
        openModule(hash.split('/')[2]);
    } else if (hash === '#/learning') {
        document.getElementById('section-learning').classList.remove('hidden');
        document.getElementById('nav-learning').classList.add('active');
        loadLearning();
    } else if (hash === '#/events') {
        document.getElementById('section-events').classList.remove('hidden');
        document.getElementById('nav-events').classList.add('active');
        loadEvents();
    } else if (hash === '#/progress') {
        document.getElementById('section-progress').classList.remove('hidden');
        document.getElementById('nav-progress').classList.add('active');
        loadProgress();
    } else if (hash === '#/reports') {
        document.getElementById('section-reports').classList.remove('hidden');
        document.getElementById('nav-reports').classList.add('active');
        loadReports();
    } else {
        document.getElementById('section-home').classList.remove('hidden');
        document.getElementById('nav-home').classList.add('active');
        loadHomeDashboard();
    }
}

async function initDashboard() {
    // Mode toggle setup
    const res = await fetch(`${API_BASE}/system/mode`, { headers: getHeaders() });
    const data = await res.json();
    updateModeUI(data.mode);
    
    document.getElementById('security-mode-toggle').addEventListener('change', async (e) => {
        const newMode = e.target.checked ? 'SECURE' : 'VULNERABLE';
        const mRes = await fetch(`${API_BASE}/system/mode`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify({ mode: newMode })
        });
        const mData = await mRes.json();
        updateModeUI(mData.mode);
    });
    
    document.getElementById('current-year').textContent = new Date().getFullYear();
    
    // Initial fetch of health for footer
    fetchHealthStatus();
    
    handleRoute();
}

async function fetchHealthStatus() {
    try {
        const healthRes = await fetch(`${API_BASE}/system/health`, { headers: getHeaders(), cache: 'no-store' });
        if(healthRes.ok) {
            const healthData = await healthRes.json();
            const fStatus = document.getElementById('footer-system-status');
            if (fStatus) {
                fStatus.innerHTML = `
                    <div class="flex justify-between text-muted" style="font-size:0.8rem; margin-bottom:0.2rem;"><span class="text-cyan">●</span> Lab Environment <span class="text-green">${healthData.services.lab_environment}</span></div>
                    <div class="flex justify-between text-muted" style="font-size:0.8rem; margin-bottom:0.2rem;"><span class="text-cyan">●</span> Database <span class="text-green">${healthData.services.database}</span></div>
                    <div class="flex justify-between text-muted" style="font-size:0.8rem;"><span class="text-cyan">●</span> Security Monitoring <span class="text-green">${healthData.services.security_monitoring}</span></div>
                `;
            }
            return healthData;
        }
    } catch(e) { console.error(e); }
    return null;
}

function updateModeUI(mode) {
    const isSecure = mode === 'SECURE';
    document.getElementById('security-mode-toggle').checked = isSecure;
    const label = document.getElementById('mode-label');
    label.textContent = mode;
    label.className = isSecure ? 'text-green' : 'text-red';
}

// ==========================================
// HOME DASHBOARD
// ==========================================
async function loadHomeDashboard() {
    try {
        const dashRes = await fetch(`${API_BASE}/system/dashboard`, { headers: getHeaders(), cache: 'no-store' });
        if(dashRes.ok) {
            const dashData = await dashRes.json();
            
            // Render Findings
            const tbody = document.getElementById('home-findings-table');
            if(dashData.recent_findings.length === 0) {
                tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;" class="text-muted">No findings detected yet.</td></tr>';
            } else {
                tbody.innerHTML = dashData.recent_findings.map(f => `
                    <tr>
                        <td><span class="badge badge-red">${f.severity}</span></td>
                        <td>${f.finding}</td>
                        <td class="font-mono text-muted">${f.lab}</td>
                        <td class="text-amber">${f.status}</td>
                        <td class="text-muted" style="font-size:0.8rem;">${new Date(f.time).toLocaleTimeString()}</td>
                    </tr>
                `).join('');
            }
            
            // Render Activity
            const actDiv = document.getElementById('recent-activity-content');
            if(dashData.recent_activity.length === 0) {
                actDiv.innerHTML = '<div class="text-muted">No recent activity.</div>';
            } else {
                actDiv.innerHTML = dashData.recent_activity.map(a => `
                    <div class="timeline-item ${a.type === 'FINDING' ? 'threat' : 'success'}">
                        <div style="font-weight:600; font-size:0.85rem; margin-bottom:0.2rem;">${a.type}</div>
                        <div style="font-size:0.9rem;">${a.desc}</div>
                        <div style="font-size:0.75rem; color:var(--text-muted); margin-top:0.2rem;">${a.time ? new Date(a.time).toLocaleString() : ''}</div>
                    </div>
                `).join('');
            }
            
            // Render Threat Overview
            const threatDiv = document.getElementById('threat-overview-content');
            const totalThreats = Object.values(dashData.threat_overview).reduce((a, b) => a + b, 0);
            if(totalThreats === 0) {
                threatDiv.innerHTML = '<div class="text-muted">No threats identified.</div>';
            } else {
                threatDiv.innerHTML = Object.entries(dashData.threat_overview).map(([k, v]) => {
                    const pct = Math.round((v / totalThreats) * 100);
                    return `
                    <div style="margin-bottom: 1rem;">
                        <div class="flex justify-between" style="font-size:0.85rem; margin-bottom:0.3rem;">
                            <span>${k}</span>
                            <span class="text-muted">${v}</span>
                        </div>
                        <div class="progress-bar-bg">
                            <div class="progress-bar-fill" style="width:${pct}%; background:var(--threat-red); box-shadow:var(--glow-red);"></div>
                        </div>
                    </div>`;
                }).join('');
            }
            
            // Update Findings stat
            document.getElementById('stat-security-findings').textContent = totalThreats;
        }

        const healthData = await fetchHealthStatus();
        if(healthData) {
            document.getElementById('system-status-list').innerHTML = Object.entries(healthData.services).map(([k, v]) => `
                <div class="flex justify-between items-center mb-2" style="font-family:var(--font-mono); font-size:0.85rem;">
                    <span class="text-muted">${k.toUpperCase().replace('_', ' ')}</span>
                    <span class="text-green">${v}</span>
                </div>
            `).join('');
        }
        
        // Labs total and completed stats
        const progRes = await fetch(`${API_BASE}/system/progress`, { headers: getHeaders(), cache: 'no-store' });
        const progData = await progRes.json();
        
        const labsRes = await fetch(`${API_BASE}/labs/`, { headers: getHeaders(), cache: 'no-store' });
        const labsData = await labsRes.json();
        document.getElementById('stat-total-labs').textContent = labsData.length;
        document.getElementById('stat-completed-labs').textContent = progData.filter(p => p.completed).length;
        
        // Modules stats
        const lProgRes = await fetch(`${API_BASE}/learning/progress`, { headers: getHeaders(), cache: 'no-store' });
        const lProgData = await lProgRes.json();
        document.getElementById('stat-total-modules').textContent = lProgData.modules_total;
        
    } catch(e) {
        console.error("Dashboard load failed", e);
    }
}


// ==========================================
// LABS CATALOG
// ==========================================
async function loadLabs() {
    const res = await fetch(`${API_BASE}/labs/`, { headers: getHeaders(), cache: 'no-store' });
    const labs = await res.json();
    window.LABS_CACHE = labs;
    renderLabGrid(labs);
}

function renderLabGrid(labs) {
    document.getElementById('lab-grid').innerHTML = labs.map(lab => `
        <div class="card" onclick="window.location.hash='#/labs/${lab.id}'" style="cursor:pointer;">
            <div class="text-cyan font-mono" style="font-size:0.8rem; margin-bottom:0.5rem; letter-spacing:1px;">${lab.id.toUpperCase()}</div>
            <h3 class="mb-2" style="font-size: 1.1rem;">${lab.title}</h3>
            <div class="flex gap-2 mb-3">
                <span class="badge badge-amber">${lab.difficulty}</span>
                <span class="badge badge-blue">${lab.category}</span>
            </div>
            <p class="text-muted" style="font-size: 0.9rem; flex-grow: 1; margin-bottom: 1.5rem;">${lab.description}</p>
            <button class="btn-secondary btn-small" style="width:100%;">OPEN LAB</button>
        </div>
    `).join('');
}

function filterLabs() {
    const q = document.getElementById('lab-search').value.toLowerCase();
    const activeFilter = document.querySelector('#lab-filters .active').textContent;
    let filtered = window.LABS_CACHE || [];
    
    if (activeFilter !== 'ALL') {
        filtered = filtered.filter(l => l.category.toUpperCase().includes(activeFilter.toUpperCase()));
    }
    if (q) {
        filtered = filtered.filter(l => l.title.toLowerCase().includes(q) || l.description.toLowerCase().includes(q) || l.id.toLowerCase().includes(q));
    }
    renderLabGrid(filtered);
}

function setLabFilter(filter) {
    document.querySelectorAll('#lab-filters button').forEach(b => b.classList.remove('active'));
    event.target.classList.add('active');
    filterLabs();
}

// ==========================================
// LAB DETAIL
// ==========================================
async function openLab(labId) {
    currentLabId = labId;
    const res = await fetch(`${API_BASE}/labs/${labId}`, { headers: getHeaders(), cache: 'no-store' });
    const data = await res.json();
    
    document.getElementById('lab-title').textContent = data.title;
    document.getElementById('lab-difficulty').textContent = data.difficulty;
    document.getElementById('lab-category').textContent = data.category;
    document.getElementById('lab-scenario').textContent = data.description;
    
    document.getElementById('lab-objectives-dynamic').innerHTML = `
        <li style="margin-bottom:0.5rem;"><span class="text-green mr-2">✓</span> Understand target</li>
        <li style="margin-bottom:0.5rem;"><span class="text-cyan mr-2">○</span> Identify attack surface</li>
        <li style="margin-bottom:0.5rem;"><span class="text-cyan mr-2">○</span> Execute attack</li>
    `;
    
    const hRes = await fetch(`${API_BASE}/labs/${labId}/hint`, { headers: getHeaders() });
    const hData = await hRes.json();
    document.getElementById('lab-hint').textContent = hData.hint;
    document.getElementById('lab-hint').classList.add('hidden');
    
    document.getElementById('chat-box').innerHTML = '';
}

function showHint() {
    document.getElementById('lab-hint').classList.remove('hidden');
}

async function sendAttack() {
    const payload = document.getElementById('attack-payload').value;
    if (!payload) return;
    
    const chat = document.getElementById('chat-box');
    chat.innerHTML += `<div class="msg user"><b>USER:</b> ${payload}</div>`;
    chat.scrollTop = chat.scrollHeight;
    document.getElementById('attack-payload').value = '';
    
    const res = await fetch(`${API_BASE}/labs/attack`, {
        method: 'POST',
        headers: getHeaders(),
        body: JSON.stringify({ payload: payload, lab_id: currentLabId })
    });
    
    const data = await res.json();
    chat.innerHTML += `<div class="msg ai"><b>TARGET:</b> ${data.response}</div>`;
    chat.scrollTop = chat.scrollHeight;
    
    document.getElementById('inspector-request').textContent = JSON.stringify({
        endpoint: `/api/labs/attack`,
        payload: payload,
        lab_id: currentLabId,
        method: "POST"
    }, null, 2);
    
    document.getElementById('inspector-response').textContent = JSON.stringify(data, null, 2);
    
    if (data.evidence) {
        document.getElementById('inspector-evidence').textContent = data.evidence;
    }
    
    if (data.vulnerable) {
        showToast("Vulnerability Successfully Exploited!");
    } else {
        showToast("Attack Blocked or Ineffective.");
    }
}

function switchTab(tab) {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-content > div').forEach(d => d.classList.add('hidden'));
    
    event.target.classList.add('active');
    document.getElementById(`tab-${tab}`).classList.remove('hidden');
}

async function resetLab() {
    await fetch(`${API_BASE}/labs/${currentLabId}/reset`, { method: 'POST', headers: getHeaders() });
    document.getElementById('chat-box').innerHTML = '';
    document.getElementById('inspector-request').textContent = 'Waiting for request...';
    document.getElementById('inspector-response').textContent = 'Waiting for response...';
    document.getElementById('inspector-evidence').textContent = 'No evidence captured yet.';
    showToast("Lab Environment Reset.");
}

// ==========================================
// LEARNING ACADEMY
// ==========================================
async function updateOverallLearningProgress() {
    const res = await fetch(`${API_BASE}/learning/progress`, { headers: getHeaders(), cache: 'no-store' });
    if (!res.ok) return;
    const data = await res.json();
    
    document.getElementById('academy-mods-stat').textContent = `Modules: ${data.modules_completed} / ${data.modules_total}`;
    document.getElementById('academy-quiz-stat').textContent = `Quiz Avg: ${data.quiz_average}%`;
    
    const pct = data.modules_total > 0 ? (data.modules_completed / data.modules_total) * 100 : 0;
    document.getElementById('academy-progress-bar').style.width = `${pct}%`;
}

async function loadLearning() {
    await updateOverallLearningProgress();
    const res = await fetch(`${API_BASE}/learning/`, { headers: getHeaders(), cache: 'no-store' });
    const modules = await res.json();
    window.LEARNING_MODULES_CACHE = modules;
    renderLearningGrid(modules);
}

function renderLearningGrid(modules) {
    document.getElementById('learning-grid').innerHTML = modules.map(m => {
        let pct = m.lessons_total > 0 ? (m.lessons_completed / m.lessons_total) * 100 : 0;
        return `
        <div class="card" onclick="window.location.hash='#/learning/${m.id}'" style="cursor:pointer;">
            <div class="flex justify-between items-center mb-2">
                <span class="font-mono text-cyan" style="font-size:0.8rem; letter-spacing:1px;">${m.id.toUpperCase()}</span>
                <span class="badge ${m.completed ? 'badge-green' : 'badge-amber'}">${m.completed ? 'COMPLETED' : 'IN PROGRESS'}</span>
            </div>
            <h3 class="mb-2" style="font-size: 1.1rem;">${m.title}</h3>
            <p class="text-muted" style="font-size: 0.85rem; flex-grow: 1; margin-bottom: 1.5rem;">${m.description}</p>
            
            <div class="flex justify-between items-center text-muted" style="font-size: 0.75rem; margin-bottom: 0.5rem; font-weight:600;">
                <span>LESSONS: ${m.lessons_completed}/${m.lessons_total}</span>
                <span>${Math.round(pct)}%</span>
            </div>
            <div class="progress-bar-bg mb-2">
                <div class="progress-bar-fill" style="width: ${pct}%; background: ${m.completed ? 'var(--secure-green)' : 'var(--primary-cyan)'}; box-shadow: ${m.completed ? 'var(--glow-green)' : 'var(--glow-cyan)'};"></div>
            </div>
        </div>
        `;
    }).join('');
}

function searchLearning() {
    const q = document.getElementById('learning-search').value.toLowerCase();
    if (!q && window.LEARNING_MODULES_CACHE) {
        renderLearningGrid(window.LEARNING_MODULES_CACHE);
        return;
    }
    const filtered = window.LEARNING_MODULES_CACHE.filter(m => m.title.toLowerCase().includes(q) || m.description.toLowerCase().includes(q));
    renderLearningGrid(filtered);
}

async function openModule(modId) {
    currentModuleId = modId;
    currentLessonId = null;
    const res = await fetch(`${API_BASE}/learning/${modId}`, { headers: getHeaders(), cache: 'no-store' });
    const data = await res.json();
    
    document.getElementById('module-detail-title').textContent = data.module.title;
    
    const list = document.getElementById('lesson-list');
    list.innerHTML = data.lessons.map(l => `
        <li>
            <a href="javascript:void(0)" onclick="loadLesson('${l.id}')" style="display: flex; align-items: center; gap: 0.8rem; padding: 0.6rem; border-radius: 4px; text-decoration: none; color: ${l.completed ? 'var(--text-muted)' : 'var(--text-main)'}; background: var(--bg-dark); border: 1px solid var(--border-color); transition: background 0.2s;">
                <span class="${l.completed ? 'text-green' : 'text-cyan'}">${l.completed ? '✓' : '○'}</span>
                <span style="${l.completed ? 'text-decoration: line-through; opacity:0.8;' : ''}">${l.title}</span>
            </a>
        </li>
    `).join('');
    
    const labList = document.getElementById('related-labs-list');
    if (data.module.related_labs.length > 0) {
        labList.innerHTML = data.module.related_labs.map(labId => `
            <li><a href="#/labs/${labId}" class="btn-secondary btn-small" style="display: block; text-align: center; text-decoration: none;">LAUNCH ${labId.toUpperCase()}</a></li>
        `).join('');
    } else {
        labList.innerHTML = '<li class="text-muted" style="font-size: 0.8rem; text-align:center;">No direct labs for this module.</li>';
    }
    
    document.getElementById('lesson-detail-title').textContent = "SELECT A LESSON";
    document.getElementById('lesson-content-area').innerHTML = '<p class="text-muted">Please select a lesson from the sidebar.</p>';
    document.getElementById('lesson-navigation-area').classList.add('hidden');
}

async function loadLesson(lessonId) {
    currentLessonId = lessonId;
    const res = await fetch(`${API_BASE}/learning/${currentModuleId}/lessons/${lessonId}`, { headers: getHeaders(), cache: 'no-store' });
    const data = await res.json();
    
    document.getElementById('lesson-detail-title').textContent = data.title;
    document.getElementById('lesson-content-area').innerHTML = `<div style="font-size:0.95rem; line-height:1.7;">${data.content}</div>`;
    document.getElementById('lesson-navigation-area').classList.remove('hidden');
}

async function markLessonComplete() {
    if (!currentLessonId) return;
    await fetch(`${API_BASE}/learning/${currentModuleId}/lessons/${currentLessonId}/complete`, { 
        method: 'POST', headers: getHeaders() 
    });
    showToast("Lesson Marked Complete");
    openModule(currentModuleId);
    updateOverallLearningProgress();
}

async function openQuiz() {
    const startRes = await fetch(`${API_BASE}/learning/${currentModuleId}/quiz/start`, { method: 'POST', headers: getHeaders(), cache: 'no-store' });
    if (!startRes.ok) {
        showToast("Failed to start quiz.");
        return;
    }
    const startData = await startRes.json();
    currentQuizAttemptId = startData.attempt_id;
    
    const res = await fetch(`${API_BASE}/learning/quiz/${currentQuizAttemptId}`, { headers: getHeaders(), cache: 'no-store' });
    const data = await res.json();
    const questions = data.questions;
    
    document.getElementById('lesson-detail-title').textContent = "MODULE QUIZ";
    document.getElementById('lesson-navigation-area').classList.add('hidden');
    
    let html = `<div id="quiz-form">`;
    html += `<div style="margin-bottom: 1.5rem; font-family:var(--font-mono); color: var(--primary-cyan);">QUESTIONS: ${questions.length}</div>`;
    
    html += questions.map((q, i) => `
        <div class="panel">
            <div class="panel-content">
                <p class="mb-3" style="font-size:1.05rem;"><strong>Q${i+1}: ${q.question}</strong></p>
                ${q.options.map((opt, optIdx) => `
                    <label style="display:flex; align-items:flex-start; gap:0.8rem; margin-bottom:0.8rem; cursor: pointer; padding:0.5rem; border-radius:4px; background:var(--bg-dark); border:1px solid var(--border-color); transition: border-color 0.2s;">
                        <input type="radio" name="q_${q.question_id}" value="${optIdx}" style="width:auto; margin:0; margin-top:4px;"> 
                        <span style="font-size:0.9rem;">${opt}</span>
                    </label>
                `).join('')}
                <div id="q-result-${q.question_id}" class="mt-2" style="font-size: 0.9rem; padding:0.5rem; border-radius:4px;"></div>
            </div>
        </div>
    `).join('');
    html += `<button id="btn-submit-quiz" class="btn-primary mt-2" onclick="submitQuiz(${questions.length})">SUBMIT ATTEMPT</button></div><div id="quiz-result-area" class="mt-4 font-mono"></div>`;
    
    document.getElementById('lesson-content-area').innerHTML = html;
}

async function submitQuiz(totalQuestions) {
    const answers = {};
    const radios = document.querySelectorAll('#quiz-form input[type="radio"]:checked');
    
    if (radios.length < totalQuestions) {
        showToast("Please answer all questions before submitting.");
        return;
    }
    
    radios.forEach(r => {
        const qId = parseInt(r.name.replace('q_', ''));
        answers[qId] = parseInt(r.value);
    });
    
    document.getElementById('btn-submit-quiz').disabled = true;
    
    const res = await fetch(`${API_BASE}/learning/quiz/submit`, {
        method: 'POST', headers: getHeaders(), body: JSON.stringify({ attempt_id: currentQuizAttemptId, answers })
    });
    
    const data = await res.json();
    const resultArea = document.getElementById('quiz-result-area');
    resultArea.innerHTML = `
        <div style="font-size: 1.5rem; font-weight: bold; margin-bottom: 0.5rem; color: ${data.passed ? 'var(--secure-green)' : 'var(--threat-red)'}; text-shadow: ${data.passed ? 'var(--glow-green)' : 'var(--glow-red)'};">
            ${data.passed ? 'ACCESS GRANTED: QUIZ PASSED' : 'ACCESS DENIED: QUIZ FAILED'}
        </div>
        <div style="font-size: 1.2rem; color:var(--text-main);">Score: ${Math.round(data.score)}%</div>
    `;
    
    data.results.forEach(r => {
        const resDiv = document.getElementById(`q-result-${r.question_id}`);
        resDiv.style.background = r.is_correct ? 'rgba(0, 255, 136, 0.1)' : 'rgba(255, 51, 51, 0.1)';
        resDiv.style.border = `1px solid ${r.is_correct ? 'var(--secure-green)' : 'var(--threat-red)'}`;
        if (r.is_correct) {
            resDiv.innerHTML = `<span class="text-green font-bold">✓ CORRECT</span><br><br><span class="text-muted"><i>${r.explanation}</i></span>`;
        } else {
            resDiv.innerHTML = `<span class="text-red font-bold">✗ INCORRECT</span><br>Correct Option: ${r.correct_index + 1}<br><br><span class="text-muted"><i>${r.explanation}</i></span>`;
        }
    });
    
    document.querySelectorAll('#quiz-form input[type="radio"]').forEach(r => r.disabled = true);
    
    resultArea.innerHTML += `<div style="margin-top: 1.5rem;">
        ${data.passed ? 
            `<button class="btn-primary" onclick="openModule('${currentModuleId}')">CONTINUE ACADEMY</button>` : 
            `<button class="btn-threat" onclick="openQuiz()">RETRY QUIZ</button>`
        }
    </div>`;
    
    updateOverallLearningProgress();
}

async function bookmarkCurrentLesson() {
    if (!currentLessonId) return;
    await fetch(`${API_BASE}/learning/bookmarks`, { method: 'POST', headers: getHeaders(), body: JSON.stringify({ lesson_id: currentLessonId }) });
    showToast("Bookmark Saved.");
}

function toggleNotesPanel() {
    const panel = document.getElementById('notes-panel');
    panel.classList.toggle('hidden');
}

async function saveNotes() {
    if (!currentLessonId) return;
    const content = document.getElementById('lesson-notes-text').value;
    await fetch(`${API_BASE}/learning/notes`, { method: 'POST', headers: getHeaders(), body: JSON.stringify({ lesson_id: currentLessonId, content: content }) });
    showToast("Note Saved to Database.");
}

// ==========================================
// EVENTS / SIEM
// ==========================================
async function loadEvents() {
    const res = await fetch(`${API_BASE}/system/events`, { headers: getHeaders(), cache: 'no-store' });
    const events = await res.json();
    
    const tbody = document.getElementById('events-tbody');
    if (events.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;" class="text-muted">No security events logged.</td></tr>';
        return;
    }
    
    tbody.innerHTML = events.map(e => `
        <tr>
            <td class="font-mono text-muted" style="font-size:0.8rem;">${new Date(e.timestamp).toISOString()}</td>
            <td><span class="text-cyan">${e.username}</span></td>
            <td>${e.attack_type}</td>
            <td><span class="badge ${e.severity === 'HIGH' ? 'badge-red' : (e.severity === 'MEDIUM' ? 'badge-amber' : 'badge-blue')}">${e.severity}</span></td>
            <td class="${e.result === 'Vulnerable' ? 'text-red' : 'text-green'}">${e.result.toUpperCase()}</td>
            <td class="font-mono">${e.endpoint}</td>
        </tr>
    `).join('');
}

// ==========================================
// PROGRESS
// ==========================================
async function loadProgress() {
    const res = await fetch(`${API_BASE}/system/progress`, { headers: getHeaders(), cache: 'no-store' });
    const prog = await res.json();
    
    const lProgRes = await fetch(`${API_BASE}/learning/progress`, { headers: getHeaders(), cache: 'no-store' });
    const lProgData = await lProgRes.json();
    
    // Update summary blocks
    const compLabs = prog.filter(p => p.completed).length;
    document.getElementById('prog-lab-text').textContent = `${compLabs} / 15`;
    document.getElementById('prog-lab-bar').style.width = `${(compLabs/15)*100}%`;
    
    document.getElementById('prog-acad-text').textContent = `${lProgData.modules_completed} / ${lProgData.modules_total}`;
    document.getElementById('prog-acad-bar').style.width = `${(lProgData.modules_completed/15)*100}%`;
    
    const totalAttacks = prog.reduce((sum, p) => sum + p.successful_attacks, 0);
    document.getElementById('prog-vuln-text').textContent = totalAttacks;

    // Table
    const tbody = document.getElementById('progress-tbody');
    if(prog.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;" class="text-muted">No lab attempts yet.</td></tr>';
    } else {
        tbody.innerHTML = prog.map(p => `
            <tr>
                <td class="font-mono text-cyan">${p.lab_id.toUpperCase()}</td>
                <td><span class="badge ${p.completed ? 'badge-green' : 'badge-red'}">${p.completed ? 'YES' : 'NO'}</span></td>
                <td class="font-mono">${p.successful_attacks}</td>
                <td class="text-muted" style="font-size:0.85rem;">${p.timestamp ? new Date(p.timestamp).toLocaleString() : 'N/A'}</td>
            </tr>
        `).join('');
    }
}

// ==========================================
// REPORTS
// ==========================================
async function loadReports() {
    // Currently only generation is supported in the API
}

async function generateReport() {
    const res = await fetch(`${API_BASE}/system/report`, { headers: getHeaders(), cache: 'no-store' });
    const report = await res.json();
    
    const tbody = document.getElementById('reports-tbody');
    const d = new Date().toISOString();
    
    tbody.innerHTML = `
        <tr>
            <td class="font-mono text-cyan">REP-${Math.floor(Math.random() * 10000)}</td>
            <td class="text-muted" style="font-size:0.85rem;">${d}</td>
            <td>${document.getElementById('current-user').textContent}</td>
            <td class="text-red font-bold">${report.vulnerabilities_exploited} Vulns</td>
            <td><button class="btn-secondary btn-small">DOWNLOAD PDF</button></td>
        </tr>
    ` + (tbody.innerHTML.includes('No reports') ? '' : tbody.innerHTML);
    
    showToast("Security Assessment Report Generated");
}
