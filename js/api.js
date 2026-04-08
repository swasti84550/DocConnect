// API Configuration
const API_BASE_URL = 'http://127.0.0.1:8000/api';

// Store JWT tokens
let accessToken = localStorage.getItem('accessToken');
let refreshToken = localStorage.getItem('refreshToken');

// ─── Token Refresh ────────────────────────────────────────────────────────────
let _isRefreshing = false;
let _refreshQueue = []; // Queued calls waiting for refresh to complete

async function _refreshAccessToken() {
    const storedRefresh = localStorage.getItem('refreshToken');
    if (!storedRefresh) return false;

    try {
        const response = await fetch(`${API_BASE_URL}/auth/token/refresh/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refresh: storedRefresh })
        });

        if (!response.ok) return false;

        const data = await response.json();
        accessToken = data.access;
        localStorage.setItem('accessToken', data.access);

        // If the backend also rotates the refresh token
        if (data.refresh) {
            refreshToken = data.refresh;
            localStorage.setItem('refreshToken', data.refresh);
        }

        return true;
    } catch (e) {
        return false;
    }
}

// ─── API Helper ───────────────────────────────────────────────────────────────
const api = {
    setTokens: (access, refresh) => {
        accessToken = access;
        refreshToken = refresh;
        localStorage.setItem('accessToken', access);
        localStorage.setItem('refreshToken', refresh);
    },

    clearTokens: () => {
        accessToken = null;
        refreshToken = null;
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        localStorage.removeItem('userData');
    },

    getAuthHeaders: () => {
        return accessToken ? {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json'
        } : {
            'Content-Type': 'application/json'
        };
    },

    // Generic API call with automatic silent token refresh on 401
    call: async (endpoint, method = 'GET', data = null, _retry = false) => {
        try {
            const options = {
                method,
                headers: api.getAuthHeaders()
            };
            if (data) options.body = JSON.stringify(data);

            const response = await fetch(`${API_BASE_URL}${endpoint}`, options);

            // ── Auto-refresh on 401 ──────────────────────────────────────────
            if (response.status === 401 && !_retry) {
                if (localStorage.getItem('refreshToken')) {
                    if (_isRefreshing) {
                        // Queue this call until the in-progress refresh completes
                        return new Promise((resolve, reject) => {
                            _refreshQueue.push({ resolve, reject });
                        }).then(() => api.call(endpoint, method, data, true));
                    }

                    _isRefreshing = true;
                    const refreshed = await _refreshAccessToken();
                    _isRefreshing = false;

                    // Flush queued requests
                    _refreshQueue.forEach(q => q.resolve());
                    _refreshQueue = [];

                    if (refreshed) {
                        // Retry original call with new access token
                        return api.call(endpoint, method, data, true);
                    }
                }

                // Refresh failed or no refresh token — force logout
                if (!window.location.pathname.endsWith('login.html')) {
                    api.clearTokens();
                    alert('Your session has expired. Please log in again.');
                    window.location.href = 'login.html';
                    return;
                }
            }

            const contentType = response.headers.get('content-type');
            let result;
            if (contentType && contentType.includes('application/json')) {
                result = await response.json();
            } else {
                result = { detail: await response.text() };
            }

            if (!response.ok) {
                throw new Error(
                    result.detail || result.error || JSON.stringify(result) || `HTTP ${response.status}`
                );
            }

            return result;
        } catch (error) {
            console.error('API Error:', error.message);
            throw error;
        }
    },

    // ── Auth endpoints ────────────────────────────────────────────────────────
    auth: {
        register: async (userData) => {
            api.clearTokens();
            return await api.call('/auth/register/', 'POST', userData);
        },

        login: async (email, password) => {
            api.clearTokens(); // Clear stale tokens before login
            return await api.call('/auth/login/', 'POST', { email, password });
        },

        getProfile: async () => {
            return await api.call('/auth/profile/', 'GET');
        },

        updateProfile: async (userData) => {
            return await api.call('/auth/profile/', 'PATCH', userData);
        },

        deleteAccount: async () => {
            return await api.call('/auth/profile/', 'DELETE');
        },

        logout: () => {
            api.clearTokens();
            window.location.href = 'login.html';
        }
    },

    // ── Doctor endpoints ──────────────────────────────────────────────────────
    doctors: {
        list: async (params = {}) => {
            const queryString = new URLSearchParams(params).toString();
            return await api.call(`/doctors/?${queryString}`, 'GET');
        },
        getDetail: async (id) => api.call(`/doctors/${id}/`, 'GET'),
        getBookedSlots: async (id, date) => api.call(`/doctors/${id}/booked-slots/?date=${date}`, 'GET'),
        getProfile: async () => api.call('/doctors/profile/', 'GET'),
        updateProfile: async (data) => api.call('/doctors/profile/', 'PATCH', data),
        getAvailability: async () => api.call('/doctors/availability/', 'GET'),
        addAvailability: async (data) => api.call('/doctors/availability/', 'POST', data),
        updateAvailability: async (id, data) => api.call(`/doctors/availability/${id}/`, 'PUT', data),
        deleteAvailability: async (id) => api.call(`/doctors/availability/${id}/`, 'DELETE'),
    },

    // ── Appointment endpoints ─────────────────────────────────────────────────
    appointments: {
        list: async () => api.call('/appointments/', 'GET'),
        getDetail: async (id) => api.call(`/appointments/${id}/`, 'GET'),
        create: async (data) => api.call('/appointments/create/', 'POST', data),
        update: async (id, data) => api.call(`/appointments/${id}/`, 'PUT', data),
        patch: async (id, data) => api.call(`/appointments/${id}/`, 'PATCH', data),
        cancel: async (id) => api.call(`/appointments/${id}/`, 'DELETE'),
        payments: async () => api.call('/appointments/payments/', 'GET'),
        createPayment: async (data) => api.call('/appointments/payments/create/', 'POST', data),
    },

    // ── Message endpoints ─────────────────────────────────────────────────────
    messages: {
        list: async () => api.call('/auth/messages/', 'GET'),
        create: async (data) => api.call('/auth/messages/', 'POST', data),
        read: async (id) => api.call(`/auth/messages/${id}/read/`, 'PATCH', {}),
    }
};

// ─── Auth Helpers ─────────────────────────────────────────────────────────────

/** True if a valid access token exists in localStorage */
function isAuthenticated() {
    return !!localStorage.getItem('accessToken');
}

/** Returns 'doctor', 'patient', or null based on cached userData */
function getUserRole() {
    try {
        const userData = localStorage.getItem('userData');
        return userData ? JSON.parse(userData).role || null : null;
    } catch {
        return null;
    }
}

/** Redirect the user to their role-specific dashboard */
function redirectToDashboard() {
    const role = getUserRole();
    window.location.href = role === 'doctor' ? 'doctor-dashboard.html' : 'patient-dashboard.html';
}

/**
 * Call on protected pages (dashboard, etc.)
 * Redirects to login if not authenticated.
 * Returns true if authenticated, false otherwise.
 */
function requireAuth() {
    if (!isAuthenticated()) {
        window.location.href = 'login.html';
        return false;
    }
    return true;
}

/**
 * Call on guest-only pages (login, signup).
 * If the user is already logged in, redirects to their correct dashboard.
 */
function requireGuest() {
    if (isAuthenticated()) {
        redirectToDashboard();
    }
}
