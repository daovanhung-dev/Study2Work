import {
  BarChart3,
  BriefcaseBusiness,
  Building2,
  CircleUserRound,
  CreditCard,
  FileText,
  GraduationCap,
  LayoutDashboard,
  Mail,
  Search,
  Settings,
  ShieldCheck,
  ScrollText,
  UsersRound,
  type LucideIcon,
} from "lucide-react";
import { useEffect } from "react";
import { Link, NavLink, Outlet, useParams } from "react-router-dom";

import { clearPrivateWorkQueries } from "@/shared/api/query-client";
import { buildIdentityLoginUrl } from "@/shared/session/identity-navigation";
import { useSessionStore } from "@/shared/session/store";
import { OfflineNotice } from "@/shared/ui/OfflineNotice";

type WorkspaceArea = "candidate" | "enterprise" | "university" | "ops";

interface NavigationItem {
  icon: LucideIcon;
  label: string;
  to: string;
}

function Brand() {
  return (
    <Link className="inline-flex items-center gap-3 rounded-lg text-slate-950" to="/jobs">
      <img
        alt=""
        className="size-9 rounded-lg object-contain"
        height="36"
        src="/brand/study2work-work-mark.png"
        width="36"
      />
      <span className="leading-tight">
        <span className="block text-base font-bold tracking-tight">Study2Work</span>
        <span className="block text-xs font-semibold uppercase tracking-[0.15em] text-work-700">Work</span>
      </span>
    </Link>
  );
}

function publicLinkClass({ isActive }: { isActive: boolean }): string {
  return isActive
    ? "rounded-lg bg-work-50 px-3 py-2 text-sm font-semibold text-work-800"
    : "rounded-lg px-3 py-2 text-sm font-semibold text-slate-600 transition hover:bg-slate-100 hover:text-slate-950";
}

export function PublicLayout() {
  const status = useSessionStore((state) => state.status);
  const session = useSessionStore((state) => state.session);
  const showCandidate = session?.identity.roles.some((role) => role.toUpperCase() === "CANDIDATE");

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <a
        className="sr-only fixed left-4 top-4 z-50 rounded-lg bg-work-700 px-4 py-2 font-semibold text-white focus:not-sr-only"
        href="#main-content"
      >
        Chuyển đến nội dung chính
      </a>
      <OfflineNotice />
      <header className="border-b border-slate-200 bg-white/95 backdrop-blur">
        <div className="mx-auto flex min-h-[4.5rem] max-w-7xl flex-wrap items-center justify-between gap-3 px-4 py-3 sm:px-6 lg:px-8">
          <Brand />
          <nav aria-label="Điều hướng công khai" className="flex items-center gap-1">
            <NavLink className={publicLinkClass} to="/jobs">
              Việc làm
            </NavLink>
            <NavLink className={publicLinkClass} to="/companies/example">
              Doanh nghiệp
            </NavLink>
            {status === "authenticated" && showCandidate ? (
              <NavLink className={publicLinkClass} to="/candidate">
                Không gian của tôi
              </NavLink>
            ) : null}
            {status === "anonymous" ? (
              <a
                className="rounded-lg bg-work-700 px-3 py-2 text-sm font-semibold text-white transition hover:bg-work-800"
                href={buildIdentityLoginUrl("/jobs")}
              >
                Đăng nhập
              </a>
            ) : null}
          </nav>
        </div>
      </header>
      <main id="main-content">
        <Outlet />
      </main>
      <footer className="border-t border-slate-200 bg-white">
        <div className="mx-auto flex max-w-7xl flex-col gap-2 px-4 py-7 text-sm text-slate-500 sm:flex-row sm:items-center sm:justify-between sm:px-6 lg:px-8">
          <p>Study2Work Work · Career workflows with server-authoritative access.</p>
          <p>Không lưu access token, CV hoặc dữ liệu riêng tư trong localStorage.</p>
        </div>
      </footer>
    </div>
  );
}

function workspaceNavigation(area: WorkspaceArea, tenantId?: string): NavigationItem[] {
  if (area === "candidate") {
    return [
      { icon: LayoutDashboard, label: "Tổng quan", to: "/candidate" },
      { icon: CircleUserRound, label: "Hồ sơ", to: "/candidate/profile" },
      { icon: FileText, label: "CV & portfolio", to: "/candidate/cvs" },
      { icon: Search, label: "Khám phá việc làm", to: "/candidate/discover" },
      { icon: BriefcaseBusiness, label: "Ứng tuyển", to: "/candidate/applications" },
      { icon: Mail, label: "Lời mời", to: "/candidate/invitations" },
    ];
  }

  if (area === "enterprise") {
    const root = `/enterprise/${encodeURIComponent(tenantId ?? "")}`;
    return [
      { icon: LayoutDashboard, label: "Tổng quan", to: root },
      { icon: BriefcaseBusiness, label: "Tin tuyển dụng", to: `${root}/jobs` },
      { icon: Search, label: "Tìm ứng viên", to: `${root}/talent/search` },
      { icon: UsersRound, label: "ATS", to: `${root}/ats` },
      { icon: Mail, label: "Lời mời", to: `${root}/talent/invitations` },
      { icon: CreditCard, label: "Thanh toán", to: `${root}/billing-topjd` },
      { icon: Settings, label: "Cài đặt", to: `${root}/settings` },
    ];
  }

  if (area === "university") {
    const root = `/university/${encodeURIComponent(tenantId ?? "")}`;
    return [
      { icon: LayoutDashboard, label: "Tổng quan", to: root },
      { icon: ShieldCheck, label: "Xác minh", to: `${root}/verification` },
      { icon: UsersRound, label: "Thành viên", to: `${root}/members` },
      { icon: GraduationCap, label: "Liên kết học viên", to: `${root}/affiliations` },
      { icon: Building2, label: "Đối tác", to: `${root}/partnerships` },
      { icon: BarChart3, label: "Báo cáo", to: `${root}/reports` },
    ];
  }

  return [
    { icon: LayoutDashboard, label: "Tổng quan", to: "/ops" },
    { icon: UsersRound, label: "Người dùng", to: "/ops/users" },
    { icon: BriefcaseBusiness, label: "Tin tuyển dụng", to: "/ops/jobs" },
    { icon: Building2, label: "Tenant", to: "/ops/tenants" },
    { icon: ScrollText, label: "Audit", to: "/ops/audit" },
    { icon: Settings, label: "Vận hành", to: "/ops/settings" },
  ];
}

function workspaceTitle(area: WorkspaceArea): string {
  return {
    candidate: "Không gian ứng viên",
    enterprise: "Không gian doanh nghiệp",
    university: "Không gian trường đại học",
    ops: "Vận hành Work",
  }[area];
}

function workspaceLinkClass({ isActive }: { isActive: boolean }): string {
  return isActive
    ? "flex min-h-11 items-center gap-3 rounded-lg bg-work-50 px-3 py-2 text-sm font-semibold text-work-800"
    : "flex min-h-11 items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium text-slate-600 transition hover:bg-slate-100 hover:text-slate-950";
}

export function WorkspaceLayout({ area }: { area: WorkspaceArea }) {
  const { enterpriseId, universityId } = useParams();
  const identity = useSessionStore((state) => state.session?.identity);
  const tenantId = area === "enterprise" ? enterpriseId : area === "university" ? universityId : undefined;
  const navigation = workspaceNavigation(area, tenantId);

  useEffect(() => {
    clearPrivateWorkQueries();
  }, [area, tenantId]);

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <a
        className="sr-only fixed left-4 top-4 z-50 rounded-lg bg-work-700 px-4 py-2 font-semibold text-white focus:not-sr-only"
        href="#workspace-content"
      >
        Chuyển đến nội dung chính
      </a>
      <OfflineNotice />
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex min-h-[4.5rem] max-w-[1440px] items-center justify-between gap-4 px-4 py-3 sm:px-6">
          <div className="flex min-w-0 items-center gap-4">
            <Brand />
            <span className="hidden h-7 w-px bg-slate-200 sm:block" />
            <p className="hidden text-sm font-medium text-slate-600 sm:block">{workspaceTitle(area)}</p>
          </div>
          <div className="flex min-w-0 items-center gap-2 text-right">
            <CircleUserRound aria-hidden="true" className="shrink-0 text-slate-400" size={20} />
            <span className="truncate text-sm font-medium text-slate-700">
              {identity?.displayName ?? "Phiên Work"}
            </span>
          </div>
        </div>
      </header>
      <div className="mx-auto grid max-w-[1440px] lg:grid-cols-[15rem_minmax(0,1fr)]">
        <aside className="border-b border-slate-200 bg-white p-3 lg:min-h-[calc(100vh-73px)] lg:border-b-0 lg:border-r">
          <nav aria-label={workspaceTitle(area)} className="flex gap-1 overflow-x-auto lg:flex-col">
            {navigation.map(({ icon: Icon, label, to }) => (
              <NavLink className={workspaceLinkClass} end={to === "/candidate" || to === `/enterprise/${tenantId}` || to === `/university/${tenantId}` || to === "/ops"} key={to} to={to}>
                <Icon aria-hidden="true" className="shrink-0" size={18} />
                <span className="whitespace-nowrap">{label}</span>
              </NavLink>
            ))}
          </nav>
        </aside>
        <main className="min-w-0 p-4 sm:p-6 lg:p-8" id="workspace-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
