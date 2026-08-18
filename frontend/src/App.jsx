import { useEffect, useState } from 'react';
import { Navbar } from '@/components/Navbar';
import { Upload } from '@/components/Upload';
import { Dashboard } from '@/components/Dashboard';
import { History } from '@/components/History';
import { Login } from '@/components/Login';
import { Signup } from '@/components/Signup';
import { getSession, logOut } from '@/lib/auth';
import {
  analyzeImages,
  getHistory,
  isMockMode,
  saveLocalResult,
} from '@/lib/api';

function App() {
  const [user, setUser] = useState(() => getSession());
  const [authPage, setAuthPage] = useState('login');
  const [page, setPage] = useState('dashboard');
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const mock = isMockMode();

  useEffect(() => {
    if (!user) return;
    getHistory()
      .then((h) => {
        setHistory(h);
        if (h.length > 0) setResult(h[0]);
      })
      .catch(() => {});
  }, [user]);

  async function handleAnalyze(files) {
    setLoading(true);
    setError(null);
    try {
      const res = await analyzeImages(files);
      setResult(res);
      saveLocalResult(res);
      setHistory((prev) => [res, ...prev].slice(0, 20));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong.');
    } finally {
      setLoading(false);
    }
  }

  function handleReset() {
    setResult(null);
    setError(null);
  }

  function navigate(p) {
    setError(null);
    setPage(p);
  }

  function handleLogout() {
    logOut();
    setUser(null);
    setResult(null);
    setHistory([]);
    setPage('dashboard');
  }

  if (!user) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-50 px-4 py-10 text-slate-900">
        {authPage === 'login' ? (
          <Login onSuccess={setUser} onGoSignup={() => setAuthPage('signup')} />
        ) : (
          <Signup onSuccess={setUser} onGoLogin={() => setAuthPage('login')} />
        )}
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <Navbar
        page={page}
        onNavigate={navigate}
        mockMode={mock}
        user={user}
        onLogout={handleLogout}
      />

      <main className="mx-auto max-w-4xl px-4 py-8 sm:px-6 sm:py-10">
        {page === 'dashboard' && (
          <Dashboard
            result={result}
            history={history}
            loading={loading}
            onGoUpload={() => navigate('upload')}
          />
        )}

        {page === 'upload' && (
          <div className="space-y-6">
            <div className="text-center">
              <h2 className="text-2xl font-bold tracking-tight text-slate-900 sm:text-3xl">
                Run a Fatigue Analysis
              </h2>
              <p className="mx-auto mt-2 max-w-lg text-sm leading-relaxed text-slate-600">
                Upload 3–4 images and our AI analyzes visual fatigue signals to
                give you a fatigue score, risk level, and personalized
                recommendation.
              </p>
            </div>
            <Upload
              mockMode={mock}
              loading={loading}
              error={error}
              result={result}
              onAnalyze={handleAnalyze}
              onReset={handleReset}
              onViewDashboard={() => navigate('dashboard')}
            />
          </div>
        )}

        {page === 'history' && (
          <History history={history} onGoUpload={() => navigate('upload')} />
        )}

        <footer className="mt-12 border-t border-slate-200 pt-6 text-center">
          <p className="text-xs text-slate-400">
            FatigueSense provides informational analysis only and is not a
            substitute for professional medical advice.
          </p>
        </footer>
      </main>
    </div>
  );
}

export default App;
