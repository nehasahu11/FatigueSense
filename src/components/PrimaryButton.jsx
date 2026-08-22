// Pulled this out after noticing the same button markup copy-pasted into
// Dashboard, History, and Upload. Just wraps the common styles + icon slot.
export function PrimaryButton({
  icon: Icon,
  children,
  full = true,
  className = '',
  ...props
}) {
  return (
    <button
      className={`inline-flex items-center justify-center gap-2 rounded-xl bg-sky-600 px-5 py-3 text-sm font-semibold text-white shadow-md shadow-sky-600/20 transition-colors hover:bg-sky-700 disabled:cursor-not-allowed disabled:opacity-40 disabled:shadow-none ${
        full ? 'w-full' : ''
      } ${className}`}
      {...props}
    >
      {Icon && <Icon className="h-4 w-4" />}
      {children}
    </button>
  );
}
