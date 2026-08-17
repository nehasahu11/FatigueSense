const map = {
  low: {
    label: 'Low Risk',
    text: 'text-emerald-700',
    bg: 'bg-emerald-50',
    border: 'border-emerald-200',
    ring: 'ring-emerald-400/30',
    accent: '#10b981',
  },
  moderate: {
    label: 'Moderate Risk',
    text: 'text-amber-700',
    bg: 'bg-amber-50',
    border: 'border-amber-200',
    ring: 'ring-amber-400/30',
    accent: '#f59e0b',
  },
  high: {
    label: 'High Risk',
    text: 'text-orange-700',
    bg: 'bg-orange-50',
    border: 'border-orange-200',
    ring: 'ring-orange-400/30',
    accent: '#f97316',
  },
  extreme: {
    label: 'Extreme Risk',
    text: 'text-red-700',
    bg: 'bg-red-50',
    border: 'border-red-200',
    ring: 'ring-red-400/30',
    accent: '#ef4444',
  },
};

export function riskStyle(level) {
  return map[level] || map.moderate;
}
