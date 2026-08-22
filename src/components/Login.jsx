import { useState } from 'react';
import { LogIn, Activity } from 'lucide-react';
import { logIn } from '@/lib/auth';
import { PrimaryButton } from './PrimaryButton';

const inputClass =
  'w-full rounded-xl border border-slate-200 px-3.5 py-2.5 text-sm text-slate-900 outline-none transition-colors focus:border-sky-400 focus:ring-2 focus:ring-sky-100';

export function Login({ onSuccess, onGoSignup }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  function handleSubmit(e) {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      const session = logIn(email, password);
      onSuccess(session);
    } catch (err) {
      setError(err.message);
      setSubmitting(false);
    }
  }

  return (
    <div className="w-full max-w-sm">
      <div className="mb-6 flex flex-col items-center text-center">
        <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-sky-600 shadow-md shadow-sky-600/20">
          <Activity className="h-6 w-6 text-white" strokeWidth={2.5} />
        </div>
        <h2 className="mt-3 text-2xl font-bold tracking-tight text-slate-900">
          Welcome back
        </h2>
        <p className="mt-1 text-sm text-slate-500">
          Log in to see your fatigue history.
        </p>
      </div>

      <form
        onSubmit={handleSubmit}
        className="space-y-4 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"
      >
        <div>
          <label className="mb-1.5 block text-sm font-medium text-slate-700">
            Email
          </label>
          <input
            type="email"
            required
            autoComplete="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className={inputClass}
            placeholder="you@example.com"
          />
        </div>
        <div>
          <label className="mb-1.5 block text-sm font-medium text-slate-700">
            Password
          </label>
          <input
            type="password"
            required
            autoComplete="current-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className={inputClass}
            placeholder="••••••••"
          />
        </div>

        {error && <p className="text-xs font-medium text-red-600">{error}</p>}

        <PrimaryButton type="submit" icon={LogIn} disabled={submitting}>
          {submitting ? 'Logging in…' : 'Log In'}
        </PrimaryButton>
      </form>

      <p className="mt-4 text-center text-sm text-slate-500">
        Don't have an account?{' '}
        <button
          onClick={onGoSignup}
          className="font-semibold text-sky-600 hover:text-sky-700"
        >
          Sign up
        </button>
      </p>
    </div>
  );
}
