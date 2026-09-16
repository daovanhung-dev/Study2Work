export function LoadingState() {
  return <div className="state-card"><div className="spinner-border text-primary" role="status" /><p>Đang tải dữ liệu...</p></div>;
}

export function ErrorState({ message = "Không thể tải dữ liệu.", retry }: { message?: string; retry?: () => void }) {
  return <div className="state-card error-state"><i className="fa-solid fa-circle-exclamation" /><p>{message}</p>{retry && <button className="btn btn-primary" onClick={retry}>Thử lại</button>}</div>;
}

export function EmptyState({ message }: { message: string }) {
  return <div className="state-card"><i className="fa-regular fa-folder-open" /><p>{message}</p></div>;
}
