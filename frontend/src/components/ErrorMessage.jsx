import { AlertCircle } from 'lucide-react';

export function ErrorMessage({ message, title = 'Something went wrong' }) {
  return (
    <div className="flex min-h-[200px] flex-col items-center justify-center rounded-2xl border border-red-200 bg-red-50/50 p-8 text-center shadow-sm">
      <div className="flex h-12 w-12 items-center justify-center rounded-full bg-red-100">
        <AlertCircle className="h-6 w-6 text-red-500" />
      </div>
      <p className="mt-4 text-sm font-semibold text-red-700">{title}</p>
      <p className="mt-1 max-w-xs text-sm text-red-600">{message}</p>
    </div>
  );
}
