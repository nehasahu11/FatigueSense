import { useState } from 'react';
import { Activity, Menu, X, LogOut } from 'lucide-react';

const links = [
  { key: 'dashboard', label: 'Dashboard' },
  { key: 'upload', label: 'Upload Test' },
  { key: 'history', label: 'History' },
];

export function Navbar({ page, onNavigate, mockMode, user, onLogout }) {
  const [menuOpen, setMenuOpen] = useState(false);

  function go(p) {
    onNavigate(p);
    setMenuOpen(false);
  }

  return (
    <header className="sticky top-0 z-30 border-b border-slate-200/80 bg-white/85 backdrop-blur-xl">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3 sm:px-6">
        <button
          onClick={() => go('dashboard')}
          className="flex items-center gap-2.5"
        >
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-sky-600 shadow-md shadow-sky-600/20">
            <Activity className="h-5 w-5 text-white" strokeWidth={2.5} />
          </div>
          <div className="text-left leading-tight">
            <h1 className="text-base font-semibold tracking-tight text-slate-900">
              FatigueSense
            </h1>
            <p className="text-[11px] font-medium text-slate-500">
              AI Fatigue Analysis
            </p>
          </div>
        </button>

        <nav className="hidden items-center gap-1 md:flex">
          {links.map((link) => (
            <button
              key={link.key}
              onClick={() => go(link.key)}
              className={`rounded-lg px-3.5 py-2 text-sm font-medium transition-colors ${
                page === link.key
                  ? 'bg-sky-50 text-sky-700'
                  : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
              }`}
            >
              {link.label}
            </button>
          ))}
          <span
            className={`ml-2 inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-[11px] font-semibold ring-1 ${
              mockMode
                ? 'bg-amber-50 text-amber-700 ring-amber-200'
                : 'bg-emerald-50 text-emerald-700 ring-emerald-200'
            }`}
          >
            <span
              className={`h-1.5 w-1.5 rounded-full ${
                mockMode ? 'bg-amber-500' : 'bg-emerald-500 animate-pulse'
              }`}
            />
            {mockMode ? 'Demo' : 'Live'}
          </span>

          {user && (
            <div className="ml-2 flex items-center gap-2 border-l border-slate-200 pl-3">
              <span className="max-w-[120px] truncate text-sm font-medium text-slate-600">
                {user.name}
              </span>
              <button
                onClick={onLogout}
                className="flex h-8 w-8 items-center justify-center rounded-lg text-slate-400 transition-colors hover:bg-slate-50 hover:text-red-500"
                aria-label="Log out"
                title="Log out"
              >
                <LogOut className="h-4 w-4" />
              </button>
            </div>
          )}
        </nav>

        <button
          onClick={() => setMenuOpen((o) => !o)}
          className="flex h-9 w-9 items-center justify-center rounded-lg border border-slate-200 text-slate-600 md:hidden"
          aria-label="Toggle menu"
        >
          {menuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
        </button>
      </div>

      {menuOpen && (
        <nav className="border-t border-slate-200 bg-white px-4 py-2 md:hidden">
          {links.map((link) => (
            <button
              key={link.key}
              onClick={() => go(link.key)}
              className={`block w-full rounded-lg px-3 py-2.5 text-left text-sm font-medium transition-colors ${
                page === link.key
                  ? 'bg-sky-50 text-sky-700'
                  : 'text-slate-600 hover:bg-slate-50'
              }`}
            >
              {link.label}
            </button>
          ))}
          {user && (
            <button
              onClick={onLogout}
              className="mt-1 flex w-full items-center gap-2 rounded-lg px-3 py-2.5 text-left text-sm font-medium text-red-600 hover:bg-red-50"
            >
              <LogOut className="h-4 w-4" />
              Log out
            </button>
          )}
        </nav>
      )}
    </header>
  );
}
