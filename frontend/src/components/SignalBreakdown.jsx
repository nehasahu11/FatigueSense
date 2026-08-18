export function SignalBreakdown({ signals }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
      <h3 className="mb-4 text-sm font-semibold text-slate-900">
        Fatigue Signal Breakdown
      </h3>
      <div className="space-y-4">
        {signals.map((signal) => (
          <div key={signal.key}>
            <div className="mb-1.5 flex items-baseline justify-between">
              <span className="text-sm font-medium text-slate-700">
                {signal.label}
              </span>
              <span className="text-xs font-semibold text-slate-500">
                {signal.value}/100
              </span>
            </div>
            <div className="h-2 overflow-hidden rounded-full bg-slate-100">
              <div
                className="h-full rounded-full bg-sky-500 transition-all duration-700 ease-out"
                style={{ width: `${signal.value}%` }}
              />
            </div>
            <p className="mt-1 text-[11px] leading-relaxed text-slate-400">
              {signal.description}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
