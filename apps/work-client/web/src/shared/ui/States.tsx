import { Button } from "./Primitives";

export function LoadingState() {
  return <div className="state-card" role="status" aria-live="polite" aria-busy="true"><span className="ui-spinner" aria-hidden="true" /><p>Đang tải dữ liệu...</p></div>;
}

export function ErrorState({ message = "Không thể tải dữ liệu.", retry }: { message?: string; retry?: () => void }) {
  return <div className="state-card error-state" role="alert"><i className="fa-solid fa-circle-exclamation" aria-hidden="true" /><p>{message}</p>{retry && <Button onClick={retry}>Thử lại</Button>}</div>;
}

export function EmptyState({ message }: { message: string }) {
  return <div className="state-card" role="status"><i className="fa-regular fa-folder-open" aria-hidden="true" /><p>{message}</p></div>;
}
