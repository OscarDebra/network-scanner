/**
 * api.js
 * Centralised API calls to the Flask backend.
 * All endpoints are relative so they work via the nginx proxy,
 * meaning the frontend never needs to know the backend's IP directly.
 */
 
const BASE = '/api';
 
export async function fetchScan() {
  const res = await fetch(`${BASE}/scan`);
  if (!res.ok) throw new Error(`Scan failed: ${res.status}`);
  return res.json();
}
 
export async function fetchDevices() {
  const res = await fetch(`${BASE}/devices`);
  if (!res.ok) throw new Error(`Failed to fetch devices: ${res.status}`);
  return res.json();
}
 
export async function fetchHistory() {
  const res = await fetch(`${BASE}/history`);
  if (!res.ok) throw new Error(`Failed to fetch history: ${res.status}`);
  return res.json();
}
 
export async function fetchHealth() {
  const res = await fetch(`${BASE}/health`);
  if (!res.ok) throw new Error('Backend unreachable');
  return res.json();
}