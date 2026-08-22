import { useState } from 'react';
import { ScanLine, ChevronRight, Clock, Trash2 } from 'lucide-react';
import { RiskBadge } from './RiskBadge';
import { ScoreGauge } from './ScoreGauge';
import { Recommendation } from './Recommendation';
import { SignalBreakdown } from './SignalBreakdown';
import { PrimaryButton } from './PrimaryButton';

function formatDateTime(iso) {
  return new Date(iso).toLocaleString(undefined, {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

export function History({ history, onGoUpload }) {
  const [selected, setSelected] = useState(null);

  if (history.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center rounded-2xl border border-dashed border-slate-200 bg-slate-50/50 p-10 text-center">
        <p className="text-sm font-semibold text-slate-700">No history yet</p>
        <p className="mt-1 max-w-xs text-sm text-slate-500">
          Your past analyses will appear here once you run your first test.
        </p>
        <PrimaryButton onClick={onGoUpload} icon={ScanLine} full={false} className="mt-5 px-5 py-2.5">
          Start a Test
        </PrimaryButton>
      </div>
    );
  }

  if (selected) {
    return (
      <div className="space-y-5">
        <button
          onClick={() => setSelected(null)}
          className="inline-flex items-center gap-1.5 text-sm font-medium text-sky-600 hover:text-sky-700"
        >
          <ChevronRight className="h-4 w-4 rotate-180" />
          Back to History
        </button>
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-sm font-semibold text-slate-900">
              Analysis Detail
            </h2>
            <RiskBadge level={selected.risk_level} />
          </div>
          <ScoreGauge
            score={selected.fatigue_score}
            riskLevel={selected.risk_level}
          />
          <div className="mt-3 flex items-center justify-center gap-1.5 text-xs text-slate-400">
            <Clock className="h-3.5 w-3.5" />
            {formatDateTime(selected.created_at)}
          </div>
        </div>
        <Recommendation
          recommendation={selected.recommendation}
          riskLevel={selected.risk_level}
        />
        {selected.signals && selected.signals.length > 0 && (
          <SignalBreakdown signals={selected.signals} />
        )}
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <div className="mb-2 flex items-center justify-between">
        <h2 className="text-sm font-semibold text-slate-900">
          Analysis History
        </h2>
        <span className="text-xs font-medium text-slate-500">
          {history.length} {history.length === 1 ? 'entry' : 'entries'}
        </span>
      </div>

      {history.map((item) => (
        <button
          key={item.analysis_id}
          onClick={() => setSelected(item)}
          className="flex w-full items-center gap-4 rounded-xl border border-slate-200 bg-white p-4 text-left shadow-sm transition-all hover:border-sky-200 hover:shadow-md"
        >
          <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-slate-50">
            <span className="text-lg font-bold text-slate-700">
              {item.fatigue_score}
            </span>
          </div>
          <div className="min-w-0 flex-1">
            <div className="flex items-center gap-2">
              <RiskBadge level={item.risk_level} size="sm" />
            </div>
            <p className="mt-1 flex items-center gap-1 text-xs text-slate-400">
              <Clock className="h-3 w-3" />
              {formatDateTime(item.created_at)}
            </p>
          </div>
          <ChevronRight className="h-5 w-5 shrink-0 text-slate-300" />
        </button>
      ))}

      <button
        onClick={onGoUpload}
        className="mt-3 inline-flex w-full items-center justify-center gap-2 rounded-xl border border-sky-200 bg-sky-50 px-5 py-3 text-sm font-semibold text-sky-700 transition-colors hover:bg-sky-100"
      >
        <ScanLine className="h-4 w-4" />
        Run New Test
      </button>
    </div>
  );
}
