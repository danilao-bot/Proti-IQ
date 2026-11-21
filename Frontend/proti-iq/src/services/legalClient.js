/**
 * Legal Content Client for Proti IQ.
 * Fetches authoritative markdown for Privacy Policy, Terms, and Cookies.
 */

const API_BASE = import.meta.env.VITE_API_BASE ? import.meta.env.VITE_API_BASE.replace('/hub', '') : 'http://localhost:8000/api/v1';

export async function fetchLegalDocument(type) {
  try {
    const res = await fetch(`${API_BASE}/legal/${type}`);
    if (!res.ok) throw new Error();
    return await res.json();
  } catch {
    return {
      title: type.toUpperCase(),
      content: 'Legal documentation is currently being synchronized with our compliance repository.'
    };
  }
}
