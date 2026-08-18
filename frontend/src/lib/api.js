import { getUserId } from './userId';
import { generateMockResult } from './mockData';

// No backend configured yet -> fall back to generated results so the UI
// is still demoable without the FastAPI service running.
const API_BASE = import.meta.env.VITE_API_BASE_URL;
const MOCK_MODE = !API_BASE || API_BASE.trim() === '';

export const MIN_IMAGES = 3;
export const MAX_IMAGES = 4;

export function isMockMode() {
  return MOCK_MODE;
}

function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export async function analyzeImages(files) {
  const userId = getUserId();

  if (files.length < MIN_IMAGES || files.length > MAX_IMAGES) {
    throw new Error(`Please upload between ${MIN_IMAGES} and ${MAX_IMAGES} images.`);
  }

  if (MOCK_MODE) {
    await delay(1400 + Math.random() * 800);
    return generateMockResult(userId, files.length);
  }

  const formData = new FormData();
  formData.append('user_id', userId);
  files.forEach((file) => formData.append('images', file));

  const res = await fetch(`${API_BASE}/analyze`, {
    method: 'POST',
    body: formData,
  });

  if (!res.ok) {
    throw new Error(`Analysis failed (${res.status}). Please try again.`);
  }

  const data = await res.json();
  return data.result;
}

export async function getHistory() {
  const userId = getUserId();

  if (MOCK_MODE) {
    await delay(400);
    return readLocalHistory();
  }

  const res = await fetch(
    `${API_BASE}/history?user_id=${encodeURIComponent(userId)}`
  );
  if (!res.ok) {
    throw new Error(`Could not load history (${res.status}).`);
  }
  const data = await res.json();
  return data.history;
}

const MAX_LOCAL_HISTORY = 20;

function historyKey() {
  return `fatiguesense_history_${getUserId()}`;
}

export function saveLocalResult(result) {
  const history = readLocalHistory();
  history.unshift(result);
  const trimmed = history.slice(0, MAX_LOCAL_HISTORY);
  localStorage.setItem(historyKey(), JSON.stringify(trimmed));
}

function readLocalHistory() {
  const raw = localStorage.getItem(historyKey());
  if (!raw) return [];
  try {
    return JSON.parse(raw);
  } catch {
    return [];
  }
}
