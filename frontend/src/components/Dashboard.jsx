import { Sparkles, ScanLine, TrendingUp, Clock } from 'lucide-react';
import { ScoreGauge } from './ScoreGauge';
import { Recommendation } from './Recommendation';
import { SignalBreakdown } from './SignalBreakdown';
import { TrendChart } from './TrendChart';
import { RiskBadge } from './RiskBadge';
import { LoadingState } from './LoadingState';
import { PrimaryButton } from './PrimaryButton';

export function Dashboard({ result, history, loading, onGoUpload }) {
  if (loading && !result) {
    return <LoadingState />;
  }

  if (!result) {
    return (
      <div className="space-y-5">
        <div className="flex flex-col items-center justify-center rounded-2xl border border-dashed border-slate-200 bg-slate-50/50 p-10 text-center">
          <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-sky-100">
            <Sparkles className="h-7 w-7 text-sky-500" />
          </div>
          <p className="mt-4 text-sm font-semibold text-slate-700">
            No analysis yet
          </p>
          <p className="mt-1 max-w-xs text-sm text-slate-500">
            Run your first fatigue analysis to see your score, risk level, and
            personalized recommendation here.
          </p>
          <PrimaryButton
            onClick={onGoUpload}
            icon={ScanLine}
            full={false}
            className="mt-5 px-5 py-2.5"
          >
            Start a Test
          </PrimaryButton>
        </div>
        <TrendChart history={history} />
      </div>
    );
  }

  return (
    <div className="space-y-5">
      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-sm font-semibold text-slate-900">Latest Result</h2>
          <RiskBadge level={result.risk_level} />
        </div>
        <ScoreGauge score={result.fatigue_score} riskLevel={result.risk_level} />
        <div className="mt-4 flex items-center justify-center gap-1.5 text-xs text-slate-400">
          <Clock className="h-3.5 w-3.5" />
          {new Date(result.created_at).toLocaleString(undefined, {
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
          })}
        </div>
      </div>

      <Recommendation
        recommendation={result.recommendation}
        riskLevel={result.risk_level}
      />

      {result.signals && result.signals.length > 0 && (
        <SignalBreakdown signals={result.signals} />
      )}

      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
        <div className="mb-3 flex items-center gap-2">
          <TrendingUp className="h-4 w-4 text-sky-600" />
          <h3 className="text-sm font-semibold text-slate-900">Your Trend</h3>
        </div>
        <TrendChart history={history} />
      </div>

      <PrimaryButton onClick={onGoUpload} icon={ScanLine}>
        Run Another Test
      </PrimaryButton>
    </div>
  );
}
