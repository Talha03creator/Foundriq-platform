// FoundrIQ – Authentication Module
const API_BASE = window.location.origin;

const Auth = {
    getToken() {
        return localStorage.getItem('foundriq_token');
    },

    getUser() {
        const user = localStorage.getItem('foundriq_user');
        return user ? JSON.parse(user) : null;
    },

    setAuth(token, user) {
        localStorage.setItem('foundriq_token', token);
        localStorage.setItem('foundriq_user', JSON.stringify(user));
    },

    logout() {
        localStorage.removeItem('foundriq_token');
        localStorage.removeItem('foundriq_user');
        window.location.href = '/';
    },

    isAuthenticated() {
        return !!this.getToken();
    },

    requireAuth() {
        if (!this.isAuthenticated()) {
            window.location.href = '/login';
            return false;
        }
        return true;
    },

    authHeaders() {
        return {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.getToken()}`,
        };
    },

    async register(email, fullName, password) {
        const res = await fetch(`${API_BASE}/api/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, full_name: fullName, password }),
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'Registration failed');
        this.setAuth(data.access_token, data.user);
        return data;
    },

    async login(email, password) {
        const res = await fetch(`${API_BASE}/api/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password }),
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'Login failed');
        this.setAuth(data.access_token, data.user);
        return data;
    },

    async fetchWithAuth(url, options = {}) {
        const res = await fetch(`${API_BASE}${url}`, {
            ...options,
            headers: { ...this.authHeaders(), ...options.headers },
        });
        if (res.status === 401) {
            this.logout();
            return null;
        }
        return res;
    }
};
