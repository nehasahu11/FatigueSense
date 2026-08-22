import { getUserId } from "./userId";
import { generateMockResult } from "./mockData";

const API_BASE = import.meta.env.VITE_API_BASE_URL;
const MOCK_MODE = !API_BASE || API_BASE.trim() === "";

export const MIN_IMAGES = 1;
export const MAX_IMAGES = 4;

export function isMockMode() {
  return MOCK_MODE;
}

function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// =====================================================
// ANALYZE IMAGES
// =====================================================

export async function analyzeImages(files) {
  const userId = getUserId();

  // Validate number of images
  if (files.length < MIN_IMAGES || files.length > MAX_IMAGES) {
    throw new Error(
      `Please upload between ${MIN_IMAGES} and ${MAX_IMAGES} images.`,
    );
  }

  // ===================================================
  // MOCK MODE
  // ===================================================

  if (MOCK_MODE) {
    await delay(1400 + Math.random() * 800);

    return generateMockResult(userId, files.length);
  }

  // ===================================================
  // REAL BACKEND MODE
  // ===================================================

  const formData = new FormData();

  formData.append("user_id", userId);

  files.forEach((file) => {
    formData.append("images", file);
  });

  // Send request to FastAPI
  const res = await fetch(`${API_BASE}/analyze`, {
    method: "POST",
    body: formData,
  });

  // ===================================================
  // HANDLE HTTP ERROR
  // ===================================================

  if (!res.ok) {
    let errorMessage;

    try {
      const errorData = await res.json();

      errorMessage = errorData.detail || `Analysis failed (${res.status}).`;
    } catch {
      errorMessage = `Analysis failed (${res.status}).`;
    }

    throw new Error(errorMessage);
  }

  // ===================================================
  // READ BACKEND RESPONSE
  // ===================================================

  const data = await res.json();

  // Backend may return the result directly
  // or inside { result: ... }
  const result = data.result ?? data;

  // ===================================================
  // CONVERT BACKEND COMPONENTS TO FRONTEND SIGNALS
  // ===================================================

  const components = result.analysis?.components ?? {};

  const signals = [
    {
      key: "eye_closure",
      label: "Eye Closure",
      value: Number(components.eye_closure_score ?? 0),
      description: "Measures fatigue related to prolonged or closed eyes.",
    },

    {
      key: "eye_state",
      label: "Eye State",
      value: Number(components.eye_state_score ?? 0),
      description: "Evaluates whether the eyes appear open or closed.",
    },

    {
      key: "blink",
      label: "Blinking",
      value: Number(components.blink_score ?? 0),
      description: "Evaluates blinking patterns associated with fatigue.",
    },

    {
      key: "yawn",
      label: "Yawning",
      value: Number(components.yawn_score ?? 0),
      description: "Detects yawning as a possible fatigue signal.",
    },

    {
      key: "dark_circle",
      label: "Under-Eye Darkness",
      value: Number(components.dark_circle_score ?? 0),
      description:
        "Measures under-eye darkness as an additional fatigue indicator.",
    },
  ];

  // Return backend result + signals
  return {
    ...result,
    signals,
  };
}

// =====================================================
// HISTORY
// =====================================================

export async function getHistory() {
  const userId = getUserId();

  // ===================================================
  // MOCK MODE
  // ===================================================

  if (MOCK_MODE) {
    await delay(400);

    return readLocalHistory();
  }

  // ===================================================
  // REAL BACKEND MODE
  // ===================================================

  const res = await fetch(
    `${API_BASE}/history?user_id=${encodeURIComponent(userId)}`,
  );

  if (!res.ok) {
    throw new Error(`Could not load history (${res.status}).`);
  }

  const data = await res.json();

  return data.history ?? [];
}

// =====================================================
// LOCAL HISTORY
// =====================================================

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

  if (!raw) {
    return [];
  }

  try {
    return JSON.parse(raw);
  } catch {
    return [];
  }
}
