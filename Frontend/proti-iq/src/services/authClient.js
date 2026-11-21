/**
 * Authentication and Session Client for Proti IQ.
 * Manages JWT storage, onboarding submissions, and data deletion requests.
 */

const API_BASE = import.meta.env.VITE_API_BASE ? import.meta.env.VITE_API_BASE.replace('/hub', '') : 'http://localhost:8000/api/v1';

const TOKEN_KEY = 'proti_iq_session_token';

export function getStoredToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function setStoredToken(token) {
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearStoredToken() {
  localStorage.removeItem(TOKEN_KEY);
}

export async function submitOnboarding(data) {
  const res = await fetch(`${API_BASE}/auth/onboard`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Onboarding failed with HTTP ${res.status}`);
  }
  const result = await res.json();
  if (result.session_token) {
    setStoredToken(result.session_token);
  }
  return result;
}

export async function fetchSession() {
  const token = getStoredToken();
  if (!token) return { authenticated: false };

  try {
    const res = await fetch(`${API_BASE}/auth/session`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (!res.ok) {
      clearStoredToken();
      return { authenticated: false };
    }
    const data = await res.json();
    if (!data.authenticated) {
      clearStoredToken();
    }
    return data;
  } catch (e) {
    console.warn('Session check network error:', e);
    return { authenticated: false };
  }
}

export async function requestDataDeletion() {
  const token = getStoredToken();
  if (!token) throw new Error('No active session token found.');

  const res = await fetch(`${API_BASE}/auth/delete-data`, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}` }
  });
  if (!res.ok) {
    throw new Error('Data deletion failed on server.');
  }
  clearStoredToken();
  return await res.json();
}
