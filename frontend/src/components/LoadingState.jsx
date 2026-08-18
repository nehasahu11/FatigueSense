import { Loader2 } from 'lucide-react';

export function LoadingState({
  message = 'Analyzing your images…',
  subMessage = 'Detecting fatigue signals across all uploaded images',
  minHeight = 320,
}) {
  return (
    <div
      className="flex flex-col items-center justify-center rounded-2xl border border-slate-200 bg-white p-8 shadow-sm"
      style={{ minHeight }}
    >
      <Loader2 className="h-10 w-10 animate-spin text-sky-500" />
      <p className="mt-4 text-sm font-medium text-slate-600">{message}</p>
      {subMessage && (
        <p className="mt-1 text-xs text-slate-400">{subMessage}</p>
      )}
    </div>
  );
}
