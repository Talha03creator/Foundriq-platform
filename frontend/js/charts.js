// FoundrIQ – Lightweight Chart Library (Canvas-based)
const Charts = {

    // ── Line Chart ────────────────────────────
    drawLineChart(canvasId, data, options = {}) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        const dpr = window.devicePixelRatio || 1;

        // High DPI
        const rect = canvas.getBoundingClientRect();
        canvas.width = rect.width * dpr;
        canvas.height = rect.height * dpr;
        ctx.scale(dpr, dpr);

        const w = rect.width;
        const h = rect.height;
        const padding = { top: 20, right: 20, bottom: 40, left: 50 };
        const chartW = w - padding.left - padding.right;
        const chartH = h - padding.top - padding.bottom;

        const labels = options.labels || Object.keys(data);
        const values = Object.values(data).filter(v => typeof v === 'number');
        const maxVal = Math.max(...values) * 1.15;
        const minVal = 0;

        ctx.clearRect(0, 0, w, h);

        // Get theme colors
        const style = getComputedStyle(document.documentElement);
        const textColor = style.getPropertyValue('--text-muted').trim() || '#94a3b8';
        const gridColor = style.getPropertyValue('--border-color').trim() || 'rgba(0,0,0,0.08)';

        // Grid lines
        const gridLines = 5;
        ctx.strokeStyle = gridColor;
        ctx.lineWidth = 0.5;
        ctx.fillStyle = textColor;
        ctx.font = '11px Inter, sans-serif';
        ctx.textAlign = 'right';

        for (let i = 0; i <= gridLines; i++) {
            const y = padding.top + (chartH / gridLines) * i;
            const val = Math.round(maxVal - (maxVal / gridLines) * i);
            ctx.beginPath();
            ctx.moveTo(padding.left, y);
            ctx.lineTo(w - padding.right, y);
            ctx.stroke();
            ctx.fillText('$' + val.toLocaleString(), padding.left - 8, y + 4);
        }

        // X labels
        ctx.textAlign = 'center';
        ctx.fillStyle = textColor;
        const monthLabels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

        // Points
        const points = values.map((val, i) => ({
            x: padding.left + (chartW / (values.length - 1)) * i,
            y: padding.top + chartH - ((val - minVal) / (maxVal - minVal)) * chartH
        }));

        // Labels
        points.forEach((p, i) => {
            ctx.fillText(monthLabels[i] || `M${i + 1}`, p.x, h - padding.bottom + 20);
        });

        // Gradient fill
        const gradient = ctx.createLinearGradient(0, padding.top, 0, h - padding.bottom);
        gradient.addColorStop(0, 'rgba(99, 102, 241, 0.2)');
        gradient.addColorStop(1, 'rgba(99, 102, 241, 0.01)');

        ctx.beginPath();
        ctx.moveTo(points[0].x, h - padding.bottom);
        points.forEach(p => ctx.lineTo(p.x, p.y));
        ctx.lineTo(points[points.length - 1].x, h - padding.bottom);
        ctx.closePath();
        ctx.fillStyle = gradient;
        ctx.fill();

        // Line
        ctx.beginPath();
        ctx.strokeStyle = '#6366f1';
        ctx.lineWidth = 2.5;
        ctx.lineJoin = 'round';
        ctx.lineCap = 'round';
        points.forEach((p, i) => {
            if (i === 0) ctx.moveTo(p.x, p.y);
            else ctx.lineTo(p.x, p.y);
        });
        ctx.stroke();

        // Dots
        points.forEach(p => {
            ctx.beginPath();
            ctx.arc(p.x, p.y, 4, 0, Math.PI * 2);
            ctx.fillStyle = '#6366f1';
            ctx.fill();
            ctx.beginPath();
            ctx.arc(p.x, p.y, 2, 0, Math.PI * 2);
            ctx.fillStyle = '#ffffff';
            ctx.fill();
        });
    },

    // ── Risk Gauge ────────────────────────────
    drawGauge(canvasId, value, maxVal = 100) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        const dpr = window.devicePixelRatio || 1;

        const rect = canvas.getBoundingClientRect();
        canvas.width = rect.width * dpr;
        canvas.height = rect.height * dpr;
        ctx.scale(dpr, dpr);

        const w = rect.width;
        const h = rect.height;
        const cx = w / 2;
        const cy = h - 10;
        const radius = Math.min(cx, cy) - 10;

        ctx.clearRect(0, 0, w, h);

        // Background arc
        ctx.beginPath();
        ctx.arc(cx, cy, radius, Math.PI, 0);
        ctx.lineWidth = 16;
        ctx.strokeStyle = getComputedStyle(document.documentElement).getPropertyValue('--bg-tertiary').trim() || '#f1f3f8';
        ctx.lineCap = 'round';
        ctx.stroke();

        // Value arc
        const pct = Math.min(value / maxVal, 1);
        const endAngle = Math.PI + pct * Math.PI;

        let color;
        if (pct < 0.33) color = '#10b981';
        else if (pct < 0.66) color = '#f59e0b';
        else color = '#ef4444';

        ctx.beginPath();
        ctx.arc(cx, cy, radius, Math.PI, endAngle);
        ctx.lineWidth = 16;
        ctx.strokeStyle = color;
        ctx.lineCap = 'round';
        ctx.stroke();

        // Value text
        ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--text-primary').trim() || '#0f172a';
        ctx.font = 'bold 28px Inter, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(value, cx, cy - 15);

        // Label
        ctx.font = '12px Inter, sans-serif';
        ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--text-muted').trim() || '#94a3b8';
        ctx.fillText('Competition Score', cx, cy + 5);
    },

    // ── Bar Chart ─────────────────────────────
    drawBarChart(canvasId, data, options = {}) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        const dpr = window.devicePixelRatio || 1;

        const rect = canvas.getBoundingClientRect();
        canvas.width = rect.width * dpr;
        canvas.height = rect.height * dpr;
        ctx.scale(dpr, dpr);

        const w = rect.width;
        const h = rect.height;
        const padding = { top: 20, right: 20, bottom: 40, left: 50 };

        const entries = Object.entries(data);
        const maxVal = Math.max(...entries.map(e => e[1])) * 1.15;
        const barWidth = (w - padding.left - padding.right) / entries.length * 0.6;
        const gap = (w - padding.left - padding.right) / entries.length * 0.4;

        ctx.clearRect(0, 0, w, h);

        const textColor = getComputedStyle(document.documentElement).getPropertyValue('--text-muted').trim() || '#94a3b8';

        entries.forEach(([label, value], i) => {
            const x = padding.left + (barWidth + gap) * i + gap / 2;
            const barH = ((value / maxVal) * (h - padding.top - padding.bottom));
            const y = h - padding.bottom - barH;

            const gradient = ctx.createLinearGradient(x, y, x, h - padding.bottom);
            gradient.addColorStop(0, '#6366f1');
            gradient.addColorStop(1, '#a78bfa');

            ctx.fillStyle = gradient;
            ctx.beginPath();
            ctx.roundRect(x, y, barWidth, barH, [4, 4, 0, 0]);
            ctx.fill();

            ctx.fillStyle = textColor;
            ctx.font = '10px Inter, sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText(label, x + barWidth / 2, h - padding.bottom + 16);
        });
    },

    // ── Animated progress bar ─────────────────
    animateProgress(elementId, value, max = 100) {
        const el = document.getElementById(elementId);
        if (!el) return;
        const pct = Math.round((value / max) * 100);
        el.style.width = '0%';
        setTimeout(() => {
            el.style.transition = 'width 1.5s cubic-bezier(0.4, 0, 0.2, 1)';
            el.style.width = pct + '%';
        }, 100);
    }
};
