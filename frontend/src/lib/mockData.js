const recommendations = {
  low: [
    'Your fatigue indicators look healthy. Maintain your current sleep schedule and keep taking short breaks every 90 minutes during focused work.',
    'No significant fatigue signals detected. Continue your routine and stay hydrated to keep energy levels stable.',
  ],
  moderate: [
    'Mild fatigue signals are present. Consider a 15-20 minute break, hydrate, and avoid driving for the next hour if possible.',
    'You are showing early signs of fatigue. A brief walk or light stretching is recommended before resuming concentrated tasks.',
  ],
  high: [
    'Strong fatigue signals detected. Rest is strongly recommended. Avoid operating machinery or driving, and aim for a proper sleep within the next few hours.',
    'Your results indicate significant fatigue. Step away from demanding tasks, hydrate, and take a restorative break before continuing.',
  ],
  extreme: [
    'Critical fatigue levels detected. Stop all safety-sensitive activities immediately. Get adequate sleep before resuming any demanding work.',
    'Your fatigue score is in the extreme range. Immediate rest is essential. Do not drive or perform hazardous tasks until you have slept.',
  ],
};

const signalTemplates = [
  {
    key: 'eye_openness',
    label: 'Eye Openness',
    description: 'Reduced eyelid aperture is a strong indicator of drowsiness.',
  },
  {
    key: 'facial_tension',
    label: 'Facial Tension',
    description: 'Relaxed facial muscles often correlate with mental fatigue.',
  },
  {
    key: 'posture_slouch',
    label: 'Posture Slouch',
    description: 'Forward head posture and shoulder drop suggest physical tiredness.',
  },
  {
    key: 'gaze_stability',
    label: 'Gaze Stability',
    description: 'Unsteady or drifting gaze patterns indicate reduced alertness.',
  },
  {
    key: 'micro_expressions',
    label: 'Micro-Expressions',
    description: 'Yawning and lowered brow micro-movements signal fatigue onset.',
  },
];

function pick(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function clamp(n, min, max) {
  return Math.max(min, Math.min(max, n));
}

function riskFromScore(score) {
  if (score < 30) return 'low';
  if (score < 60) return 'moderate';
  if (score < 85) return 'high';
  return 'extreme';
}

export function generateMockResult(userId, imageCount, baseline) {
  const center = baseline ?? 35 + Math.random() * 45;
  const score = clamp(Math.round(center + (Math.random() * 16 - 8)), 4, 98);
  const risk = riskFromScore(score);

  const signals = signalTemplates.map((tpl) => ({
    ...tpl,
    value: clamp(Math.round(score + (Math.random() * 24 - 12)), 0, 100),
  }));

  return {
    analysis_id:
      'mock-' + Math.random().toString(36).slice(2) + Date.now().toString(36),
    user_id: userId,
    fatigue_score: score,
    risk_level: risk,
    recommendation: pick(recommendations[risk]),
    signals,
    image_count: imageCount,
    created_at: new Date().toISOString(),
  };
}
