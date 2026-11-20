/**
 * Proti IQ Backend API Client.
 * Connects to FastAPI for dynamic Groq AI advisory generation and regional rankings.
 */

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api/v1/hub';

export async function requestAdvisory({ role, job, cropId, olderPersonMode = false, stapleVehicle = null }) {
  try {
    const res = await fetch(`${API_BASE}/advisory/formulate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        role,
        job,
        crop_id: cropId,
        older_person_mode: olderPersonMode,
        staple_vehicle: stapleVehicle
      })
    });
    if (!res.ok) {
      throw new Error(`API error HTTP ${res.status}`);
    }
    return await res.json();
  } catch (err) {
    console.warn('Backend API advisory call failed, using client-side fallback:', err);
    return null;
  }
}

export async function fetchFilteredRankings(job, country = 'Nigeria') {
  try {
    const res = await fetch(`${API_BASE}/rankings?job=${encodeURIComponent(job)}&country=${encodeURIComponent(country)}`);
    if (!res.ok) {
      throw new Error(`API error HTTP ${res.status}`);
    }
    return await res.json();
  } catch (err) {
    console.warn('Backend API rankings call failed:', err);
    return null;
  }
}

export async function fetchEmpiricalCropData(cropId) {
  try {
    const res = await fetch(`${API_BASE}/empirical/${encodeURIComponent(cropId)}`);
    if (!res.ok) {
      throw new Error(`API error HTTP ${res.status}`);
    }
    return await res.json();
  } catch (err) {
    console.warn('Backend API empirical call failed:', err);
    return null;
  }
}
