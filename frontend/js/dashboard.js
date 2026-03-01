// FoundrIQ – Dashboard Logic
document.addEventListener('DOMContentLoaded', async () => {
    if (!Auth.requireAuth()) return;

    const user = Auth.getUser();
    const userNameEl = document.getElementById('userName');
    const welcomeMsg = document.getElementById('welcomeMsg');
    if (user && userNameEl) userNameEl.textContent = user.full_name || user.email;
    if (user && welcomeMsg) welcomeMsg.textContent = `Welcome back, ${user.full_name || 'Founder'}!`;

    // Logout
    document.getElementById('logoutBtn')?.addEventListener('click', () => Auth.logout());

    // Load dashboard data
    await loadDashboard();
    await loadProjects();
});

async function loadDashboard() {
    try {
        const res = await Auth.fetchWithAuth('/api/dashboard');
        if (!res) return;
        const data = await res.json();

        // Stats
        animateStatValue('statProjects', data.total_projects);
        animateStatValue('statValidation', data.avg_validation_score);
        animateStatValue('statCompetition', data.avg_competition_score);
        animateStatValue('statReports', data.total_reports);

    } catch (err) {
        console.error('Dashboard load error:', err);
    }
}

function animateStatValue(elementId, target) {
    const el = document.getElementById(elementId);
    if (!el) return;

    const isFloat = !Number.isInteger(target);
    const duration = 1500;
    const steps = 60;
    const stepTime = duration / steps;
    let current = 0;
    const increment = target / steps;

    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        el.textContent = isFloat ? current.toFixed(1) : Math.round(current);
    }, stepTime);
}

async function loadProjects() {
    const listEl = document.getElementById('projectList');
    if (!listEl) return;

    try {
        const res = await Auth.fetchWithAuth('/api/projects');
        if (!res) return;
        const projects = await res.json();

        if (projects.length === 0) {
            listEl.innerHTML = `
                <div style="text-align:center;padding:60px 20px;">
                    <div style="font-size:3rem;margin-bottom:16px;">🚀</div>
                    <h3 style="font-size:1.2rem;font-weight:700;margin-bottom:8px;">No Projects Yet</h3>
                    <p style="color:var(--text-secondary);margin-bottom:24px;">Start by analyzing your first business idea</p>
                    <a href="/analyze" class="btn btn-primary">+ New Analysis</a>
                </div>
            `;
            return;
        }

        listEl.innerHTML = projects.map(p => `
            <div class="project-item" data-id="${p.id}">
                <div class="project-info">
                    <h4>${escapeHtml(p.business_idea.substring(0, 80))}${p.business_idea.length > 80 ? '...' : ''}</h4>
                    <p>${escapeHtml(p.target_market)} · ${new Date(p.created_at).toLocaleDateString()}</p>
                </div>
                <div class="project-actions">
                    ${p.validation_score !== null ? `<span class="score-badge ${getScoreClass(p.validation_score)}">${p.validation_score}/100</span>` : ''}
                    ${p.has_report ?
                `<button class="btn btn-ghost btn-sm" onclick="viewReport(${p.id})">View Report</button>` :
                `<button class="btn btn-primary btn-sm" onclick="runAnalysis(${p.id})">Analyze</button>`
            }
                    <button class="btn btn-ghost btn-sm" onclick="deleteProject(${p.id})" style="color:var(--danger);">✕</button>
                </div>
            </div>
        `).join('');

        // Load most recent report if available
        const withReport = projects.find(p => p.has_report);
        if (withReport) {
            await viewReport(withReport.id);
        }

    } catch (err) {
        console.error('Projects load error:', err);
        listEl.innerHTML = '<p style="color:var(--danger);text-align:center;">Failed to load projects</p>';
    }
}

function getScoreClass(score) {
    if (score >= 70) return 'high';
    if (score >= 40) return 'medium';
    return 'low';
}

function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

async function viewReport(projectId) {
    try {
        const res = await Auth.fetchWithAuth(`/api/projects/${projectId}`);
        if (!res) return;
        const project = await res.json();
        if (!project.report) return;

        const report = project.report;

        // Show charts
        const chartsRow = document.getElementById('chartsRow');
        if (chartsRow) chartsRow.style.display = 'grid';

        // Revenue chart
        if (report.revenue_forecast) {
            const forecast = { ...report.revenue_forecast };
            delete forecast.currency;
            setTimeout(() => Charts.drawLineChart('revenueChart', forecast), 200);
        }

        // Gauge
        if (report.competition_score !== undefined) {
            setTimeout(() => Charts.drawGauge('gaugeChart', report.competition_score), 300);
        }

        // Risk badge
        const riskBadge = document.getElementById('riskBadge');
        if (riskBadge && report.risk_level) {
            riskBadge.textContent = `Risk: ${report.risk_level}`;
            riskBadge.className = `score-badge ${report.risk_level === 'Low' ? 'high' : report.risk_level === 'High' ? 'low' : 'medium'}`;
        }

        // SWOT
        if (report.swot) {
            const swotSection = document.getElementById('swotSection');
            if (swotSection) swotSection.style.display = 'block';

            renderSwotList('swotStrengths', report.swot.strengths);
            renderSwotList('swotWeaknesses', report.swot.weaknesses);
            renderSwotList('swotOpportunities', report.swot.opportunities);
            renderSwotList('swotThreats', report.swot.threats);
        }

        // Strategy steps
        if (report.strategy_steps && report.strategy_steps.length > 0) {
            const stratSection = document.getElementById('strategySection');
            const timeline = document.getElementById('strategyTimeline');
            if (stratSection && timeline) {
                stratSection.style.display = 'block';
                timeline.innerHTML = report.strategy_steps.map(s => `
                    <div class="strategy-step">
                        <h4><span style="color:var(--accent-primary)">Step ${s.step}:</span> ${escapeHtml(s.title)}</h4>
                        <p>${escapeHtml(s.description)}</p>
                        <div class="step-meta">
                            <span>📅 ${escapeHtml(s.timeline)}</span>
                            <span>🎯 ${escapeHtml(s.priority)} Priority</span>
                        </div>
                    </div>
                `).join('');
            }
        }

    } catch (err) {
        console.error('Report view error:', err);
    }
}

function renderSwotList(elementId, items) {
    const el = document.getElementById(elementId);
    if (!el || !items) return;
    el.innerHTML = items.map(item => `<li>${escapeHtml(item)}</li>`).join('');
}

async function runAnalysis(projectId) {
    const overlay = document.getElementById('loadingOverlay');
    const loadingText = document.getElementById('loadingText');
    if (overlay) overlay.classList.remove('hidden');
    if (loadingText) loadingText.textContent = '🧠 AI is analyzing your business...';

    try {
        const res = await Auth.fetchWithAuth(`/api/analysis/${projectId}`, { method: 'POST' });
        if (!res) return;
        const data = await res.json();
        if (overlay) overlay.classList.add('hidden');

        // Reload
        await loadDashboard();
        await loadProjects();
        await viewReport(projectId);
    } catch (err) {
        console.error('Analysis error:', err);
        if (overlay) overlay.classList.add('hidden');
        alert('Analysis failed. Please try again.');
    }
}

async function deleteProject(projectId) {
    if (!confirm('Delete this project and its report?')) return;

    try {
        await Auth.fetchWithAuth(`/api/projects/${projectId}`, { method: 'DELETE' });
        await loadDashboard();
        await loadProjects();
    } catch (err) {
        console.error('Delete error:', err);
    }
}

// Redraw charts on theme change
const themeObserver = new MutationObserver(() => {
    // Wait a tick for CSS vars to update
    setTimeout(() => {
        if (document.getElementById('chartsRow')?.style.display !== 'none') {
            // Charts will re-render on next viewReport call
        }
    }, 100);
});
themeObserver.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
