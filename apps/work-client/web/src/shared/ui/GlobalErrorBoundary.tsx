import { Component, type ErrorInfo, type ReactNode } from "react";

interface GlobalErrorBoundaryProps {
  children: ReactNode;
  onReset?: () => void;
}

interface GlobalErrorBoundaryState {
  error: Error | null;
}

export class GlobalErrorBoundary extends Component<
  GlobalErrorBoundaryProps,
  GlobalErrorBoundaryState
> {
  override state: GlobalErrorBoundaryState = { error: null };

  static getDerivedStateFromError(error: Error): GlobalErrorBoundaryState {
    return { error };
  }

  override componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    if (import.meta.env.DEV) {
      console.error("Unhandled Work web error", error, errorInfo);
    }
  }

  private reset = (): void => {
    this.props.onReset?.();
    this.setState({ error: null });
  };

  override render(): ReactNode {
    if (!this.state.error) {
      return this.props.children;
    }

    return (
      <main className="grid min-h-screen place-items-center bg-slate-50 p-6" role="alert">
        <section className="w-full max-w-lg rounded-2xl border border-rose-200 bg-white p-7 shadow-lg">
          <p className="text-sm font-semibold uppercase tracking-[0.18em] text-rose-700">
            Application error
          </p>
          <h1 className="mt-3 text-2xl font-semibold text-slate-950">
            Không thể hiển thị màn hình này
          </h1>
          <p className="mt-3 text-slate-600">
            Phiên làm việc của bạn không bị thay đổi. Hãy thử hiển thị lại màn hình.
          </p>
          <button
            className="mt-6 min-h-11 rounded-lg bg-work-700 px-4 py-2 font-semibold text-white transition hover:bg-work-800 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-work-700"
            onClick={this.reset}
            type="button"
          >
            Thử lại
          </button>
        </section>
      </main>
    );
  }
}
