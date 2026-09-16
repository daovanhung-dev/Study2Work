import { Link, Outlet, useLocation, useNavigate } from "react-router-dom";

import { logout } from "./shared/api/work";
import { useAuth } from "./shared/auth/AuthProvider";

function Brand({ to = "/" }: { to?: string }) {
  return <Link className="brand" to={to}><img src="/img/logo-nobr.png" alt="Study2Work" /><span>Study2Work</span></Link>;
}

function LogoutButton() {
  const navigate = useNavigate();
  const clear = useAuth().clear;
  return <button className="btn btn-link nav-logout" onClick={async () => { try { await logout(); } finally { clear(); navigate("/"); } }}>Đăng xuất</button>;
}

export function PublicLayout() {
  return <><header className="public-header"><Brand /><nav><Link to="/">Trang chủ</Link><Link to="/signInRole">Đăng nhập</Link><Link className="btn btn-primary" to="/signUpRole">Đăng ký</Link></nav></header><main><Outlet /></main><footer className="site-footer"><div><Brand /><p>Nền tảng kết nối sinh viên và doanh nghiệp.</p></div><div><strong>Study2Work</strong><Link to="/coming-soon">Giới thiệu</Link><Link to="/coming-soon">Hỗ trợ</Link></div><div><strong>Liên hệ</strong><span>info@learn2earn.vn</span><span>Hà Nội, Việt Nam</span></div></footer></>;
}

function WorkspaceHeader({ role }: { role: "student" | "business" }) {
  const location = useLocation();
  const isStudent = role === "student";
  const links = isStudent
    ? [["/Student/Home", "Trang chủ"], ["/Student/CV", "CV"], ["/Student/Interview", "Lịch phỏng vấn"], ["/Student/Result", "Kết quả"]]
    : [["/Business/Home", "Trang chủ"], ["/Business/ManganerJD", "Tin tuyển dụng"], ["/Business/ApplyList", "Ứng viên"]];
  return <header className="workspace-header"><Brand to={isStudent ? "/Student/Home" : "/Business/Home"} /><nav>{links.map(([to, label]) => <Link className={location.pathname.toLowerCase() === to.toLowerCase() ? "active" : ""} key={to} to={to}>{label}</Link>)}<Link to={isStudent ? "/Student/Noti" : "/Business/Notification"} aria-label="Thông báo"><i className="fa-regular fa-bell" /></Link><Link to={isStudent ? "/Student/Chat" : "/Business/Chat"} aria-label="Tin nhắn"><i className="fa-regular fa-comment" /></Link><Link to={isStudent ? "/Student/Setting" : "/Business/Setting"}>Cài đặt</Link><LogoutButton /></nav></header>;
}

export function StudentLayout() {
  return <><WorkspaceHeader role="student" /><main className="workspace-main"><Outlet /></main><footer className="workspace-footer">© 2024 Study2Work</footer></>;
}

export function BusinessLayout() {
  return <><WorkspaceHeader role="business" /><main className="workspace-main"><Outlet /></main><footer className="workspace-footer">© 2024 Study2Work</footer></>;
}
