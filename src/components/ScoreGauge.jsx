import { riskStyle } from '@/lib/riskStyle';

export function ScoreGauge({ score, riskLevel }) {
  const style = riskStyle(riskLevel);
  const radius = 80;
  const stroke = 12;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;

  return (
    <div className="flex flex-col items-center">
      <div className="relative h-48 w-48">
        <svg className="h-full w-full -rotate-90" viewBox="0 0 200 200">
          <circle
            cx="100"
            cy="100"
            r={radius}
            fill="none"
            stroke="#e2e8f0"
            strokeWidth={stroke}
          />
          <circle
            cx="100"
            cy="100"
            r={radius}
            fill="none"
            stroke={style.accent}
            strokeWidth={stroke}
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            className="transition-all duration-1000 ease-out"
            style={{ filter: `drop-shadow(0 0 6px ${style.accent}55)` }}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-5xl font-bold tracking-tight text-slate-900">
            {score}
          </span>
          <span className="mt-0.5 text-xs font-medium text-slate-500">/ 100</span>
        </div>
      </div>
    </div>
  );
}
