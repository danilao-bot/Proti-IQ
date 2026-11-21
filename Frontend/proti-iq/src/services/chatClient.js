/**
 * Proti IQ Chat and Query Client.
 * Connects to /api/v1/chat for structured queries and prompt suggestions.
 */

const API_BASE = import.meta.env.VITE_API_BASE ? import.meta.env.VITE_API_BASE.replace('/hub', '') : 'http://localhost:8000/api/v1';

export async function sendChatQuery({ message, role, crop_id, job, country, age, geriatric_mode }) {
  const res = await fetch(`${API_BASE}/chat/query`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message,
      role: role || 'consumer',
      crop_id: crop_id || 'cowpea',
      job: job || 'milk',
      country: country || 'Nigeria',
      age: age || 35,
      geriatric_mode: Boolean(geriatric_mode)
    })
  });
  if (!res.ok) {
    throw new Error(`Chat query failed with HTTP ${res.status}`);
  }
  return await res.json();
}

export async function getChatSuggestions(role = 'consumer') {
  try {
    const res = await fetch(`${API_BASE}/chat/suggestions?role=${encodeURIComponent(role)}`);
    if (!res.ok) throw new Error();
    const data = await res.json();
    return data.suggestions || [];
  } catch {
    return [
      'How do I eliminate beany off-flavors in plant-based milk?',
      'What is the cheapest local African legume for high protein?',
      'How do I prepare soft, digestible legume scrambles?'
    ];
  }
}

export async function exportDocument(type, payload) {
  const endpoint = `${API_BASE}/export/${type}`;
  const res = await fetch(endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if (!res.ok) throw new Error(`Export failed with HTTP ${res.status}`);
  const blob = await res.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `ProtiIQ-${type.toUpperCase()}-${payload.crop_name || 'Export'}.txt`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  window.URL.revokeObjectURL(url);
}
