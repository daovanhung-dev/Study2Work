import {
  ArrowLeft,
  KeyRound,
  RefreshCw,
  SearchX,
  ShieldAlert,
  TriangleAlert,
} from "lucide-react";
import type { ReactNode } from "react";
import { Link, isRouteErrorResponse, useRouteError } from "react-router-dom";

import { WorkApiError } from "@/shared/api/http";
import { buildIdentityLoginUrl } from "@/shared/session/identity-navigation";
import type { AccountStatus } from "@/shared/session/types";

interface StatePageProps {
  action?: ReactNode;
  code?: string;
  description: string;
  icon: ReactNode;
  label: string;
  title: string;
}

function StatePage({ action, code, description, icon, label, title }: StatePageProps) {
  return (
    <section className="grid min-h-[65vh] place-items-center px-4 py-12">
      <section className="w-full max-w-xl rounded-2xl border border-slate-200 bg-white p-8 shadow-sm sm:p-10">
        <div className="flex size-12 items-center justify-center rounded-xl bg-work-50 text-work-700">
          {icon}
        </div>
        <p className="mt-6 text-sm font-semibold uppercase tracking-[0.16em] text-work-700">{label}</p>
        <h1 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950">{title}</h1>
        <p className="mt-4 text-base leading-7 text-slate-600">{description}</p>
        {code ? <p className="mt-4 font-mono text-xs text-slate-500">{code}</p> : null}
        <div className="mt-7 flex flex-wrap gap-3">{action}</div>
      </section>
    </section>
  );
}

export function AccessRequiredPage({ returnTo }: { returnTo: string }) {
  return (
    <StatePage
      action={
        <>
          <a
            className="inline-flex min-h-11 items-center gap-2 rounded-lg bg-work-700 px-4 py-2 font-semibold text-white transition hover:bg-work-800"
            href={buildIdentityLoginUrl(returnTo)}
          >
            <KeyRound aria-hidden="true" size={18} />
            Đăng nhập
          </a>
          <Link
            className="inline-flex min-h-11 items-center gap-2 rounded-lg border border-slate-300 px-4 py-2 font-semibold text-slate-700 transition hover:border-slate-400 hover:bg-slate-50"
            to="/jobs"
          >
            <ArrowLeft aria-hidden="true" size={18} />
            Xem việc làm
          </Link>
        </>
      }
      code="AUTHENTICATION_REQUIRED"
      description="Bạn cần đăng nhập bằng tài khoản Study2Work để tiếp tục. Liên kết đăng nhập chỉ mang theo đường dẫn nội bộ an toàn."
      icon={<KeyRound aria-hidden="true" size={24} />}
      label="Phiên đăng nhập"
      title="Hãy đăng nhập để tiếp tục"
    />
  );
}

export function ForbiddenPage({ code = "ACCESS_DENIED" }: { code?: string }) {
  return (
    <StatePage
      action={
        <Link
          className="inline-flex min-h-11 items-center gap-2 rounded-lg border border-slate-300 px-4 py-2 font-semibold text-slate-700 transition hover:border-slate-400 hover:bg-slate-50"
          to="/jobs"
        >
          <ArrowLeft aria-hidden="true" size={18} />
          Quay lại việc làm
        </Link>
      }
      code={code}
      description="Tài khoản hiện tại không có quyền truy cập tài nguyên này. Thông tin tenant và tài nguyên khác không được hiển thị."
      icon={<ShieldAlert aria-hidden="true" size={24} />}
      label="Quyền truy cập"
      title="Bạn không có quyền mở màn hình này"
    />
  );
}

export function AccountRestrictedPage({ status }: { status: AccountStatus }) {
  const deletionPending = status === "DELETION_PENDING";

  return (
    <StatePage
      action={
        <Link
          className="inline-flex min-h-11 items-center gap-2 rounded-lg border border-slate-300 px-4 py-2 font-semibold text-slate-700 transition hover:border-slate-400 hover:bg-slate-50"
          to="/jobs"
        >
          <ArrowLeft aria-hidden="true" size={18} />
          Về trang việc làm
        </Link>
      }
      code={deletionPending ? "ACCOUNT_DELETION_PENDING" : "ACCOUNT_SUSPENDED"}
      description={
        deletionPending
          ? "Tài khoản đang trong thời gian xử lý yêu cầu xóa. Các thao tác Work đã được khóa."
          : "Tài khoản này hiện bị hạn chế. Các thao tác Work đã được khóa cho đến khi trạng thái được xử lý."
      }
      icon={<ShieldAlert aria-hidden="true" size={24} />}
      label="Trạng thái tài khoản"
      title={deletionPending ? "Yêu cầu xóa đang được xử lý" : "Tài khoản đang bị hạn chế"}
    />
  );
}

export function MfaRequiredPage() {
  return (
    <StatePage
      action={
        <a
          className="inline-flex min-h-11 items-center gap-2 rounded-lg bg-work-700 px-4 py-2 font-semibold text-white transition hover:bg-work-800"
          href={buildIdentityLoginUrl("/ops")}
        >
          <KeyRound aria-hidden="true" size={18} />
          Xác thực bảo mật
        </a>
      }
      code="STEP_UP_REQUIRED"
      description="Màn hình vận hành yêu cầu MFA hoặc xác thực gần đây. Hoàn tất xác thực tại Identity rồi mở lại thao tác này."
      icon={<KeyRound aria-hidden="true" size={24} />}
      label="Xác thực bổ sung"
      title="Cần xác thực bảo mật"
    />
  );
}

export function NotFoundPage() {
  return (
    <StatePage
      action={
        <Link
          className="inline-flex min-h-11 items-center gap-2 rounded-lg bg-work-700 px-4 py-2 font-semibold text-white transition hover:bg-work-800"
          to="/jobs"
        >
          <ArrowLeft aria-hidden="true" size={18} />
          Xem việc làm
        </Link>
      }
      code="ROUTE_NOT_FOUND"
      description="Đường dẫn này không tồn tại hoặc không còn được hỗ trợ trong Work."
      icon={<SearchX aria-hidden="true" size={24} />}
      label="Không tìm thấy"
      title="Không tìm thấy màn hình"
    />
  );
}

export function RouteErrorPage() {
  const error = useRouteError();
  const responseStatus = isRouteErrorResponse(error) ? error.status : undefined;
  const apiError = error instanceof WorkApiError ? error : undefined;
  const code = apiError?.businessCode ?? (responseStatus ? `HTTP_${responseStatus}` : "UNEXPECTED_ERROR");
  const message =
    apiError?.message ??
    (responseStatus === 404
      ? "Tài nguyên không tồn tại hoặc không thuộc phạm vi truy cập của bạn."
      : "Không thể hoàn tất yêu cầu này. Hãy thử lại; phiên làm việc của bạn vẫn được giữ nguyên.");

  return (
    <StatePage
      action={
        <>
          <button
            className="inline-flex min-h-11 items-center gap-2 rounded-lg bg-work-700 px-4 py-2 font-semibold text-white transition hover:bg-work-800"
            onClick={() => window.location.reload()}
            type="button"
          >
            <RefreshCw aria-hidden="true" size={18} />
            Thử lại
          </button>
          <Link
            className="inline-flex min-h-11 items-center gap-2 rounded-lg border border-slate-300 px-4 py-2 font-semibold text-slate-700 transition hover:border-slate-400 hover:bg-slate-50"
            to="/jobs"
          >
            <ArrowLeft aria-hidden="true" size={18} />
            Về việc làm
          </Link>
        </>
      }
      code={apiError?.traceId ? `${code} · Trace ${apiError.traceId}` : code}
      description={message}
      icon={<TriangleAlert aria-hidden="true" size={24} />}
      label="Không thể tải dữ liệu"
      title={responseStatus === 404 ? "Không tìm thấy tài nguyên" : "Đã xảy ra sự cố"}
    />
  );
}
