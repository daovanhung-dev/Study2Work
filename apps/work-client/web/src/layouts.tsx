import { useState } from "react";
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
  const [menuOpen, setMenuOpen] = useState(false);
  const closeMenu = () => setMenuOpen(false);
  return <><header className="public-header"><Brand /><button className="mobile-menu-toggle" type="button" aria-expanded={menuOpen} aria-controls="public-navigation" aria-label={menuOpen ? "Đóng menu" : "Mở menu"} onClick={() => setMenuOpen((open) => !open)}><i className={menuOpen ? "fa-solid fa-xmark" : "fa-solid fa-bars"} aria-hidden="true" /></button><nav id="public-navigation" className={menuOpen ? "navigation menu-open" : "navigation"}><Link to="/" onClick={closeMenu}>Trang chủ</Link><Link to="/signInRole" onClick={closeMenu}>Đăng nhập</Link><Link className="btn btn-primary" to="/signUpRole" onClick={closeMenu}>Đăng ký</Link></nav></header><main><Outlet /></main><footer className="site-footer"><div><Brand /><p>Nền tảng kết nối sinh viên và doanh nghiệp.</p></div><div><strong>Study2Work</strong><Link to="/coming-soon">Giới thiệu</Link><Link to="/coming-soon">Hỗ trợ</Link></div><div><strong>Liên hệ</strong><span>info@learn2earn.vn</span><span>Hà Nội, Việt Nam</span></div></footer></>;
}

function WorkspaceHeader({ role }: { role: "student" | "business" }) {
  const location = useLocation();
  const [menuOpen, setMenuOpen] = useState(false);
  const isStudent = role === "student";
  const links: Array<[string, string]> = isStudent
    ? [["/Student/Home", "Trang chủ"], ["/Student/CV", "CV"], ["/Student/Interview", "Lịch phỏng vấn"], ["/Student/Result", "Kết quả"]]
    : [["/Business/Home", "Trang chủ"], ["/Business/ManganerJD", "Tin tuyển dụng"], ["/Business/ApplyList", "Ứng viên"]];
  const closeMenu = () => setMenuOpen(false);
  return <header className="workspace-header"><Brand to={isStudent ? "/Student/Home" : "/Business/Home"} /><button className="mobile-menu-toggle" type="button" aria-expanded={menuOpen} aria-controls={`${role}-navigation`} aria-label={menuOpen ? "Đóng menu" : "Mở menu"} onClick={() => setMenuOpen((open) => !open)}><i className={menuOpen ? "fa-solid fa-xmark" : "fa-solid fa-bars"} aria-hidden="true" /></button><nav id={`${role}-navigation`} className={menuOpen ? "navigation menu-open" : "navigation"}>{links.map(([to, label]) => <Link className={location.pathname.toLowerCase() === to.toLowerCase() ? "active" : ""} key={to} to={to} onClick={closeMenu}>{label}</Link>)}<Link to={isStudent ? "/Student/Noti" : "/Business/Notification"} aria-label="Thông báo" onClick={closeMenu}><i className="fa-regular fa-bell" aria-hidden="true" /><span className="sr-only">Thông báo</span></Link><Link to={isStudent ? "/Student/Chat" : "/Business/Chat"} aria-label="Tin nhắn" onClick={closeMenu}><i className="fa-regular fa-comment" aria-hidden="true" /><span className="sr-only">Tin nhắn</span></Link><Link to={isStudent ? "/Student/Setting" : "/Business/Setting"} onClick={closeMenu}>Cài đặt</Link><LogoutButton /></nav></header>;
}

export function StudentLayout() {
  return <><WorkspaceHeader role="student" /><main className="workspace-main"><Outlet /></main><footer className="workspace-footer">© 2024 Study2Work</footer></>;
}

export function BusinessLayout() {
  return <><WorkspaceHeader role="business" /><main className="workspace-main"><Outlet /></main><footer className="workspace-footer">© 2024 Study2Work</footer></>;
}
