import { riskStyle } from '@/lib/riskStyle';

export function RiskBadge({ level, size = 'md' }) {
  const style = riskStyle(level);
  const padding =
    size === 'sm' ? 'px-2 py-0.5 text-[11px]' : 'px-3 py-1 text-xs';
  return (
    <span
      className={`inline-flex items-center rounded-full font-semibold ring-1 ${padding} ${style.bg} ${style.text} ${style.border} ${style.ring}`}
    >
      {style.label}
    </span>
  );
}
