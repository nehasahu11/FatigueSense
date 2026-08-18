import { useRef, useState } from 'react';
import { UploadCloud, X, ImageIcon, ScanLine, Trash2, Info } from 'lucide-react';
import { MIN_IMAGES, MAX_IMAGES } from '@/lib/api';
import { LoadingState } from './LoadingState';
import { ErrorMessage } from './ErrorMessage';
import { ScoreGauge } from './ScoreGauge';
import { Recommendation } from './Recommendation';
import { SignalBreakdown } from './SignalBreakdown';
import { PrimaryButton } from './PrimaryButton';

const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB, matches the backend upload limit

export function Upload({ mockMode, loading, error, result, onAnalyze, onReset, onViewDashboard }) {
  const inputRef = useRef(null);
  const [images, setImages] = useState([]);
  const [dragOver, setDragOver] = useState(false);
  const [validationError, setValidationError] = useState(null);

  function addFiles(newFiles) {
    if (!newFiles) return;
    const incoming = Array.from(newFiles);
    const valid = [];
    let sizeError = false;
    for (const f of incoming) {
      if (!f.type.startsWith('image/')) continue;
      if (f.size > MAX_FILE_SIZE) {
        sizeError = true;
        continue;
      }
      valid.push(f);
    }
    setValidationError(sizeError ? 'Some images were skipped (max 10MB each).' : null);
    setImages((prev) => [...prev, ...valid].slice(0, MAX_IMAGES));
  }

  function removeAt(index) {
    setImages((prev) => prev.filter((_, i) => i !== index));
  }

  const canAnalyze = images.length >= MIN_IMAGES && images.length <= MAX_IMAGES && !loading;
  const canAdd = images.length < MAX_IMAGES;

  function handleAnalyze() {
    if (!canAnalyze) {
      setValidationError(`Please upload between ${MIN_IMAGES} and ${MAX_IMAGES} images.`);
      return;
    }
    setValidationError(null);
    onAnalyze(images);
  }

  function handleReset() {
    setImages([]);
    setValidationError(null);
    onReset();
  }

  if (loading) {
    return <LoadingState />;
  }

  if (result && !error) {
    return (
      <div className="space-y-5">
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <ScoreGauge score={result.fatigue_score} riskLevel={result.risk_level} />
        </div>
        <Recommendation
          recommendation={result.recommendation}
          riskLevel={result.risk_level}
        />
        <SignalBreakdown signals={result.signals} />
        <div className="flex flex-wrap gap-3">
          <PrimaryButton onClick={handleReset} icon={ScanLine} className="flex-1" full={false}>
            Run Another Test
          </PrimaryButton>
          <button
            onClick={onViewDashboard}
            className="inline-flex items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm font-medium text-slate-600 shadow-sm transition-colors hover:bg-slate-50"
          >
            View Dashboard
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-5">
      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
        <div className="mb-4 flex items-baseline justify-between">
          <h2 className="text-sm font-semibold text-slate-900">Upload Images</h2>
          <span className="text-xs font-medium text-slate-500">
            {images.length}/{MAX_IMAGES} images
          </span>
        </div>

        <div
          onClick={() => canAdd && inputRef.current?.click()}
          onDragOver={(e) => {
            e.preventDefault();
            if (canAdd) setDragOver(true);
          }}
          onDragLeave={() => setDragOver(false)}
          onDrop={(e) => {
            e.preventDefault();
            setDragOver(false);
            addFiles(e.dataTransfer.files);
          }}
          className={`flex cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed px-6 py-8 text-center transition-all ${
            dragOver
              ? 'border-sky-400 bg-sky-50'
              : canAdd
              ? 'border-slate-200 bg-slate-50/50 hover:border-sky-300 hover:bg-sky-50/40'
              : 'border-slate-200 bg-slate-50 opacity-60'
          }`}
        >
          <div className="mb-3 flex h-12 w-12 items-center justify-center rounded-full bg-sky-100">
            <UploadCloud className="h-6 w-6 text-sky-600" />
          </div>
          <p className="text-sm font-medium text-slate-700">
            Drag & drop or click to upload
          </p>
          <p className="mt-1 text-xs text-slate-500">
            {MIN_IMAGES}–{MAX_IMAGES} images required · JPG, PNG up to 10MB
          </p>
          <input
            ref={inputRef}
            type="file"
            accept="image/*"
            multiple
            className="hidden"
            disabled={!canAdd}
            onChange={(e) => {
              addFiles(e.target.files);
              e.target.value = '';
            }}
          />
        </div>

        {images.length > 0 && (
          <div className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-4">
            {images.map((file, i) => (
              <div
                key={i}
                className="group relative aspect-square overflow-hidden rounded-lg border border-slate-200 bg-slate-100"
              >
                <img
                  src={URL.createObjectURL(file)}
                  alt={`Upload ${i + 1}`}
                  className="h-full w-full object-cover"
                />
                <div className="absolute left-1.5 top-1.5 flex h-5 w-5 items-center justify-center rounded-full bg-slate-900/70 text-[10px] font-bold text-white">
                  {i + 1}
                </div>
                <button
                  onClick={() => removeAt(i)}
                  className="absolute right-1.5 top-1.5 flex h-6 w-6 items-center justify-center rounded-full bg-white/90 text-slate-600 shadow-sm opacity-0 transition-opacity group-hover:opacity-100 hover:bg-white hover:text-red-500"
                  aria-label="Remove image"
                >
                  <X className="h-3.5 w-3.5" />
                </button>
              </div>
            ))}
            {canAdd && (
              <button
                onClick={() => inputRef.current?.click()}
                className="flex aspect-square flex-col items-center justify-center rounded-lg border-2 border-dashed border-slate-200 bg-slate-50 text-slate-400 transition-colors hover:border-sky-300 hover:text-sky-500"
              >
                <ImageIcon className="h-6 w-6" />
                <span className="mt-1 text-[11px] font-medium">Add</span>
              </button>
            )}
          </div>
        )}
      </div>

      {validationError && (
        <p className="text-xs font-medium text-amber-700">{validationError}</p>
      )}

      <div className="flex flex-wrap gap-3">
        <PrimaryButton onClick={handleAnalyze} disabled={!canAnalyze} icon={ScanLine} className="flex-1" full={false}>
          Analyze
        </PrimaryButton>
        {images.length > 0 && (
          <button
            onClick={handleReset}
            className="inline-flex items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm font-medium text-slate-600 shadow-sm transition-colors hover:bg-slate-50"
          >
            <Trash2 className="h-4 w-4" />
            Clear
          </button>
        )}
      </div>

      {error && <ErrorMessage message={error} title="Analysis Error" />}

      {mockMode && (
        <div className="flex gap-2.5 rounded-xl border border-amber-200 bg-amber-50/60 p-3.5">
          <Info className="h-4 w-4 shrink-0 text-amber-600 mt-0.5" />
          <p className="text-xs leading-relaxed text-amber-800">
            <span className="font-semibold">Demo mode is active.</span> No
            backend URL is configured, so results are simulated for preview.
            Set <code className="font-mono">VITE_API_BASE_URL</code> in{' '}
            <code className="font-mono">.env</code> to connect the real FastAPI
            backend.
          </p>
        </div>
      )}
    </div>
  );
}
