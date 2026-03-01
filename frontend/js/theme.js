// FoundrIQ – Theme Manager
(function() {
    const THEME_KEY = 'foundriq-theme';

    function getPreferredTheme() {
        const saved = localStorage.getItem(THEME_KEY);
        if (saved) return saved;
        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }

    function applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem(THEME_KEY, theme);
        const toggle = document.getElementById('themeToggle');
        if (toggle) {
            toggle.textContent = theme === 'dark' ? '☀️' : '🌙';
        }
    }

    // Apply on load immediately
    applyTheme(getPreferredTheme());

    // Toggle listener
    document.addEventListener('DOMContentLoaded', () => {
        const toggle = document.getElementById('themeToggle');
        if (toggle) {
            // Re-apply icon after DOM ready
            const currentTheme = document.documentElement.getAttribute('data-theme');
            toggle.textContent = currentTheme === 'dark' ? '☀️' : '🌙';

            toggle.addEventListener('click', () => {
                const current = document.documentElement.getAttribute('data-theme');
                const next = current === 'dark' ? 'light' : 'dark';
                applyTheme(next);
            });
        }
    });
})();
