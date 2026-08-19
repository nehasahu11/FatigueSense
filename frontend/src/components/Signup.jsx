import { useState } from 'react';
import { UserPlus, Activity } from 'lucide-react';
import { signUp } from '@/lib/auth';
import { PrimaryButton } from './PrimaryButton';

const inputClass =
  'w-full rounded-xl border border-slate-200 px-3.5 py-2.5 text-sm text-slate-900 outline-none transition-colors focus:border-sky-400 focus:ring-2 focus:ring-sky-100';

export function Signup({ onSuccess, onGoLogin }) {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirm, setConfirm] = useState('');
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  function handleSubmit(e) {
    e.preventDefault();
    if (password !== confirm) {
      setError('Passwords do not match.');
      return;
    }
    setSubmitting(true);
    setError(null);
    try {
      const session = signUp(name, email, password);
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
          Create your account
        </h2>
        <p className="mt-1 text-sm text-slate-500">
          Track your fatigue trends over time.
        </p>
      </div>

      <form
        onSubmit={handleSubmit}
        className="space-y-4 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"
      >
        <div>
          <label className="mb-1.5 block text-sm font-medium text-slate-700">
            Name
          </label>
          <input
            type="text"
            required
            autoComplete="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className={inputClass}
            placeholder="Jane Doe"
          />
        </div>
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
            minLength={6}
            autoComplete="new-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className={inputClass}
            placeholder="At least 6 characters"
          />
        </div>
        <div>
          <label className="mb-1.5 block text-sm font-medium text-slate-700">
            Confirm Password
          </label>
          <input
            type="password"
            required
            autoComplete="new-password"
            value={confirm}
            onChange={(e) => setConfirm(e.target.value)}
            className={inputClass}
            placeholder="Repeat password"
          />
        </div>

        {error && <p className="text-xs font-medium text-red-600">{error}</p>}

        <PrimaryButton type="submit" icon={UserPlus} disabled={submitting}>
          {submitting ? 'Creating account…' : 'Sign Up'}
        </PrimaryButton>
      </form>

      <p className="mt-4 text-center text-sm text-slate-500">
        Already have an account?{' '}
        <button
          onClick={onGoLogin}
          className="font-semibold text-sky-600 hover:text-sky-700"
        >
          Log in
        </button>
      </p>
    </div>
  );
}
