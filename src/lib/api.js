import { getUserId } from './userId';
import { generateMockResult } from './mockData';


// ============================================================
// CONFIGURATION
// ============================================================

const API_BASE = import.meta.env.VITE_API_BASE_URL;

const MOCK_MODE =
  !API_BASE ||
  API_BASE.trim() === '';


// ============================================================
// IMAGE LIMITS
// ============================================================

export const MIN_IMAGES = 3;
export const MAX_IMAGES = 4;


// ============================================================
// MOCK MODE
// ============================================================

export function isMockMode() {
  return MOCK_MODE;
}


// ============================================================
// DELAY HELPER
// ============================================================

function delay(ms) {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}


// ============================================================
// ANALYZE IMAGES
// ============================================================

export async function analyzeImages(files) {
  const userId = getUserId();

  // ----------------------------------------------------------
  // Validate image count
  // ----------------------------------------------------------

  if (
    files.length < MIN_IMAGES ||
    files.length > MAX_IMAGES
  ) {
    throw new Error(
      `Please upload between ${MIN_IMAGES} and ${MAX_IMAGES} images.`
    );
  }

  // ----------------------------------------------------------
  // Mock mode
  // ----------------------------------------------------------

  if (MOCK_MODE) {
    await delay(
      1400 + Math.random() * 800
    );

    return generateMockResult(
      userId,
      files.length
    );
  }

  // ----------------------------------------------------------
  // Create multipart form data
  // ----------------------------------------------------------

  const formData = new FormData();

  formData.append(
    'user_id',
    userId
  );

  files.forEach((file) => {
    formData.append(
      'images',
      file
    );
  });

  // ----------------------------------------------------------
  // Send request to FastAPI
  // ----------------------------------------------------------

  const res = await fetch(
    `${API_BASE}/analyze`,
    {
      method: 'POST',
      body: formData,
    }
  );

  // ----------------------------------------------------------
  // Read response
  // ----------------------------------------------------------

  let data;

  try {
    data = await res.json();
  } catch {
    throw new Error(
      `Backend returned an invalid response (${res.status}).`
    );
  }

  // ----------------------------------------------------------
  // Handle HTTP errors
  // ----------------------------------------------------------

  if (!res.ok) {

    const message =
      typeof data.detail === 'string'
        ? data.detail
        : 'Analysis failed. Please try again.';

    throw new Error(message);
  }

  // ----------------------------------------------------------
  // Validate response structure
  // ----------------------------------------------------------

  if (!data.result) {
    throw new Error(
      'No analysis result was returned by the backend.'
    );
  }

  // ----------------------------------------------------------
  // Handle workflow-level errors
  // ----------------------------------------------------------

  if (
    data.result.success === false
  ) {
    throw new Error(
      data.result.error ||
      'The uploaded images could not be analyzed.'
    );
  }

  // ----------------------------------------------------------
  // Return successful result
  // ----------------------------------------------------------

  return data.result;
}


// ============================================================
// GET HISTORY
// ============================================================

export async function getHistory() {
  const userId = getUserId();

  // ----------------------------------------------------------
  // Mock mode
  // ----------------------------------------------------------

  if (MOCK_MODE) {
    await delay(400);

    return readLocalHistory();
  }

  // ----------------------------------------------------------
  // Backend request
  // ----------------------------------------------------------

  const res = await fetch(
    `${API_BASE}/history?user_id=${encodeURIComponent(userId)}`
  );

  // ----------------------------------------------------------
  // Read response
  // ----------------------------------------------------------

  let data;

  try {
    data = await res.json();
  } catch {
    throw new Error(
      `Backend returned an invalid response (${res.status}).`
    );
  }

  // ----------------------------------------------------------
  // Handle errors
  // ----------------------------------------------------------

  if (!res.ok) {

    const message =
      typeof data.detail === 'string'
        ? data.detail
        : `Could not load history (${res.status}).`;

    throw new Error(message);
  }

  // ----------------------------------------------------------
  // Return history
  // ----------------------------------------------------------

  return data.history || [];
}


// ============================================================
// LOCAL HISTORY
// ============================================================

const MAX_LOCAL_HISTORY = 20;


function historyKey() {
  return `fatiguesense_history_${getUserId()}`;
}


export function saveLocalResult(result) {
  const history = readLocalHistory();

  history.unshift(result);

  const trimmed =
    history.slice(
      0,
      MAX_LOCAL_HISTORY
    );

  localStorage.setItem(
    historyKey(),
    JSON.stringify(trimmed)
  );
}


function readLocalHistory() {
  const raw =
    localStorage.getItem(
      historyKey()
    );

  if (!raw) {
    return [];
  }

  try {
    return JSON.parse(raw);

  } catch {
    return [];
  }
}