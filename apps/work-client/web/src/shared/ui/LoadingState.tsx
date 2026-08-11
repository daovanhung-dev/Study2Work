interface LoadingStateProps {
  label?: string;
  compact?: boolean;
}

export function LoadingState({
  label = "Đang tải dữ liệu…",
  compact = false,
}: LoadingStateProps) {
  return (
    <div
      aria-busy="true"
      aria-live="polite"
      className={
        compact
          ? "flex items-center gap-3 text-sm text-slate-600"
          : "grid min-h-64 place-items-center rounded-2xl border border-slate-200 bg-white p-6 text-slate-600"
      }
    >
      <span aria-hidden="true" className="size-3 animate-pulse rounded-full bg-work-600" />
      <span>{label}</span>
    </div>
  );
}
