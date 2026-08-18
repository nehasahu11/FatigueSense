import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  ReferenceLine,
} from 'recharts';

function formatDate(iso) {
  const d = new Date(iso);
  return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
}

export function TrendChart({ history }) {
  const data = [...history]
    .reverse()
    .map((h) => ({
      label: formatDate(h.created_at),
      score: h.fatigue_score,
      date: h.created_at,
      risk: h.risk_level,
    }));

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
      <div className="mb-4 flex items-center justify-between">
        <h3 className="text-sm font-semibold text-slate-900">Fatigue Trend</h3>
        <span className="text-xs font-medium text-slate-500">
          {data.length} {data.length === 1 ? 'analysis' : 'analyses'}
        </span>
      </div>

      {data.length === 0 ? (
        <div className="flex h-52 flex-col items-center justify-center text-center">
          <p className="text-sm font-medium text-slate-400">No history yet</p>
          <p className="mt-1 text-xs text-slate-400">
            Run your first analysis to start tracking your fatigue trend.
          </p>
        </div>
      ) : data.length === 1 ? (
        <div className="flex h-52 flex-col items-center justify-center text-center">
          <p className="text-2xl font-bold text-slate-900">{data[0].score}</p>
          <p className="mt-1 text-xs text-slate-500">
            First analysis recorded. Run another to see your trend.
          </p>
        </div>
      ) : (
        <div className="h-56 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data} margin={{ top: 8, right: 8, left: -20, bottom: 0 }}>
              <defs>
                <linearGradient id="scoreGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#0284c7" stopOpacity={0.3} />
                  <stop offset="100%" stopColor="#0284c7" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" vertical={false} />
              <XAxis
                dataKey="label"
                tick={{ fontSize: 11, fill: '#94a3b8' }}
                axisLine={false}
                tickLine={false}
              />
              <YAxis
                domain={[0, 100]}
                tick={{ fontSize: 11, fill: '#94a3b8' }}
                axisLine={false}
                tickLine={false}
              />
              <ReferenceLine y={60} stroke="#f59e0b" strokeDasharray="4 4" strokeOpacity={0.4} />
              <ReferenceLine y={85} stroke="#ef4444" strokeDasharray="4 4" strokeOpacity={0.4} />
              <Tooltip
                contentStyle={{
                  borderRadius: 12,
                  border: '1px solid #e2e8f0',
                  fontSize: 12,
                  boxShadow: '0 4px 12px rgba(0,0,0,0.08)',
                }}
                labelStyle={{ fontWeight: 600, color: '#0f172a' }}
                formatter={(value) => [`${value}/100`, 'Fatigue Score']}
              />
              <Area
                type="monotone"
                dataKey="score"
                stroke="#0284c7"
                strokeWidth={2.5}
                fill="url(#scoreGradient)"
                dot={{ r: 4, fill: '#0284c7', strokeWidth: 2, stroke: '#fff' }}
                activeDot={{ r: 6 }}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}
