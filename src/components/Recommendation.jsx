import { Lightbulb } from 'lucide-react';
import { riskStyle } from '@/lib/riskStyle';

export function Recommendation({ recommendation, riskLevel }) {
  const style = riskStyle(riskLevel);
  return (
    <div className={`rounded-2xl border p-5 shadow-sm sm:p-6 ${style.bg} ${style.border}`}>
      <div className="flex gap-3">
        <div
          className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl shadow-md"
          style={{ backgroundColor: style.accent }}
        >
          <Lightbulb className="h-5 w-5 text-white" />
        </div>
        <div>
          <h3 className={`text-sm font-semibold ${style.text}`}>
            Recommendation
          </h3>
          <p className="mt-1 text-sm leading-relaxed text-slate-700">
            {recommendation}
          </p>
        </div>
      </div>
    </div>
  );
}
