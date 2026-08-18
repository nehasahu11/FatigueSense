export function ProgressBar({ value, color = '#0ea5e9', label }) {
  const clamped = Math.max(0, Math.min(100, value));
  return (
    <div>
      {label && (
        <div className="mb-1.5 flex items-baseline justify-between">
          <span className="text-sm font-medium text-slate-700">{label}</span>
          <span className="text-xs font-semibold text-slate-500">
            {clamped}/100
          </span>
        </div>
      )}
      <div className="h-2 overflow-hidden rounded-full bg-slate-100">
        <div
          className="h-full rounded-full transition-all duration-700 ease-out"
          style={{ width: `${clamped}%`, backgroundColor: color }}
        />
      </div>
    </div>
  );
}
