import { useState } from "react";
import { useMutation, useQuery } from "@tanstack/react-query";
import { Link, useNavigate, useSearchParams } from "react-router-dom";

import { getJobs, loginBusiness, loginStudent, registerStudent, type Job } from "../shared/api/work";
import { useAuth } from "../shared/auth/AuthProvider";
import { ErrorState, LoadingState } from "../shared/ui/States";

function value(record: Record<string, unknown>, key: string, fallback = "") {
  const result = record[key];
  return result === null || result === undefined ? fallback : String(result);
}

function JobCard({ job }: { job: Job }) {
  const id = value(job, "id");
  return <article className="job-card">
    <div className="job-logo"><img src={value(job, "avt", "/img/logo-nobr.png")} alt="Logo doanh nghiệp" /></div>
    <div className="job-card-content"><span className="job-tag">ĐANG TUYỂN</span><h3>{value(job, "ten_vi_tri", "Vị trí tuyển dụng")}</h3><p className="company">{value(job, "ten_cong_ty", "Doanh nghiệp Study2Work")}</p><div className="job-meta"><span><i className="fa-solid fa-location-dot" /> {value(job, "dia_diem", "Chưa cập nhật")}</span><span><i className="fa-regular fa-clock" /> {value(job, "thoi_gian", "Toàn thời gian")}</span></div></div>
    {id && <Link className="btn btn-outline-primary job-action" to={`/student/JobDescription/${id}`}>Xem chi tiết</Link>}
  </article>;
}

export function HomePage() {
  const [search, setSearch] = useState("");
  const jobs = useQuery({ queryKey: ["public-jobs"], queryFn: () => getJobs(1, 50) });
  const items = (jobs.data?.data || []).filter((job) => `${value(job, "ten_vi_tri")} ${value(job, "ten_cong_ty")} ${value(job, "dia_diem")}`.toLowerCase().includes(search.toLowerCase()));
  return <>
    <section className="hero"><div className="hero-copy"><span className="eyebrow"><i className="fa-solid fa-bolt" /> CƠ HỘI MỚI MỖI NGÀY</span><h1>Tìm việc làm<br /><span>phù hợp với bạn</span></h1><p>Study2Work đồng hành cùng bạn trên hành trình học tập và phát triển sự nghiệp.</p><div className="hero-actions"><Link className="btn btn-primary btn-lg" to="/signUpRole">Bắt đầu ngay <i className="fa-solid fa-arrow-right" /></Link><Link className="btn btn-light btn-lg" to="/signInRole">Đăng nhập</Link></div></div><div className="hero-art"><div className="hero-orb"><i className="fa-solid fa-briefcase" /></div><div className="floating-card"><strong>+1.000</strong><span>việc làm mới</span></div></div></section>
    <section className="search-panel"><div><span className="eyebrow">KHÁM PHÁ CƠ HỘI</span><h2>Việc làm dành cho bạn</h2></div><form className="search-form" onSubmit={(event) => event.preventDefault()}><i className="fa-solid fa-magnifying-glass" /><input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Vị trí, công ty hoặc địa điểm" /><button className="btn btn-primary">Tìm kiếm</button></form></section>
    <section className="content-section"><div className="section-heading"><div><span className="eyebrow">CẬP NHẬT LIÊN TỤC</span><h2>Việc làm nổi bật</h2></div><Link to="/signInRole">Xem tất cả <i className="fa-solid fa-arrow-right" /></Link></div>{jobs.isLoading && <LoadingState />}{jobs.isError && <ErrorState retry={() => void jobs.refetch()} />}{!jobs.isLoading && !jobs.isError && <div className="jobs-list">{items.length ? items.map((job, index) => <JobCard job={job} key={value(job, "id", String(index))} />) : <div className="empty-inline">Chưa có việc làm phù hợp.</div>}</div>}</section>
  </>;
}

export function RolePage({ register = false }: { register?: boolean }) {
  const roles = [
    {
      icon: "fa-user-graduate",
      tone: "student",
      badge: register ? "HỌC TẬP & ỨNG TUYỂN" : "SINH VIÊN",
      name: "Sinh viên",
      description: register
        ? "Tạo hồ sơ học tập, rèn kỹ năng và ứng tuyển thực tập/việc làm phù hợp."
        : "Quản lý CV, xem cơ hội thực tập và theo dõi đơn ứng tuyển.",
      to: register ? "/signUpStudent" : "/SignInStudent",
      action: register ? "Tôi là sinh viên" : "Đăng nhập sinh viên",
    },
    {
      icon: "fa-building",
      tone: "business",
      badge: register ? "TUYỂN DỤNG & KẾT NỐI" : "DOANH NGHIỆP",
      name: "Doanh nghiệp",
      description: register
        ? "Đăng tin tuyển dụng và kết nối sinh viên phù hợp với nhu cầu nhân sự."
        : "Quản lý tin tuyển dụng, ứng viên và kết nối với sinh viên.",
      to: register ? "/signUpBusiness" : "/signInBusiness",
      action: register ? "Tôi là doanh nghiệp" : "Đăng nhập doanh nghiệp",
    },
    {
      icon: "fa-school",
      tone: "university",
      badge: "NHÀ TRƯỜNG",
      name: "Nhà trường",
      description: "Theo dõi sinh viên, doanh nghiệp hợp tác và thống kê việc làm.",
      to: "/coming-soon",
      action: "Tôi đại diện nhà trường",
    },
  ];
  return <section className="role-page"><div className="role-container"><div className="role-header"><div className="role-header-left"><div className="role-logo"><img src="/img/logo-nobr.png" alt="Study2Work" /></div><div className="role-title"><h1>Study2Work</h1><span>{register ? "Chọn vai trò để tiếp tục trải nghiệm nền tảng" : "Đăng nhập theo đúng vai trò của bạn"}</span></div></div><div className="role-header-right">{register ? "Đã có tài khoản? " : "Chưa có tài khoản? "}<Link to={register ? "/signInRole" : "/signUpRole"}>{register ? "Đăng nhập" : "Đăng ký ngay"}</Link></div></div><div className="role-main"><div className="role-intro"><h2>{register ? "Chọn vai trò của bạn trên Study2Work" : "Đăng nhập với vai trò phù hợp"}</h2><p>Hệ thống sẽ cá nhân hóa giao diện, chức năng và nội dung theo đúng vai trò mà bạn lựa chọn.</p></div><div className="role-grid">{roles.map((role) => <div className="role-card" key={role.name}><div><div className={`role-icon ${role.tone}`}><i className={`fas ${role.icon}`} /></div><span className="role-badge"><i className="fas fa-circle" /> {role.badge}</span><div className="role-name">{role.name}</div><div className="role-desc">{role.description}</div></div><div className="role-actions"><Link to={role.to} className="btn-role-primary">{role.action}<i className="fas fa-arrow-right" /></Link><Link to="/coming-soon" className="btn-role-ghost">Xem trước giao diện <i className="fas fa-eye" /></Link></div></div>)}</div></div><div className="role-footer"><span><i className="fas fa-shield-alt" /> Dữ liệu của bạn được bảo mật theo chính sách của Study2Work.</span><Link to={register ? "/" : "/"}>Quay lại trang chủ</Link></div></div></section>;
}

export function LoginPage({ role }: { role: "student" | "business" }) {
  const navigate = useNavigate();
  const [params] = useSearchParams();
  const { setAuth } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const mutation = useMutation({ mutationFn: () => role === "student" ? loginStudent(email, password) : loginBusiness(email, password), onSuccess: (result) => { setAuth(result.data); navigate(params.get("returnTo") || (role === "student" ? "/student/Home" : "/business/Home")); } });
  return <section className="auth-page"><div className="auth-card"><span className="eyebrow">STUDY2WORK</span><h1>Chào mừng trở lại</h1><p>Đăng nhập {role === "student" ? "tài khoản sinh viên" : "tài khoản doanh nghiệp"} của bạn.</p><form onSubmit={(event) => { event.preventDefault(); mutation.mutate(); }}><label>Email<input type="email" value={email} onChange={(event) => setEmail(event.target.value)} required placeholder="you@example.com" /></label><label>Mật khẩu<input type="password" value={password} onChange={(event) => setPassword(event.target.value)} required placeholder="Nhập mật khẩu" /></label>{mutation.isError && <div className="form-error">{mutation.error instanceof Error ? mutation.error.message : "Đăng nhập thất bại."}</div>}<button className="btn btn-primary w-100" disabled={mutation.isPending}>{mutation.isPending ? "Đang đăng nhập..." : "Đăng nhập"}</button></form><div className="auth-footer"><Link to="/signInRole">← Chọn vai trò khác</Link>{role === "student" && <Link to="/signUpStudent">Tạo tài khoản</Link>}</div></div></section>;
}

export function RegisterPage() {
  const navigate = useNavigate();
  const [message, setMessage] = useState("");
  const mutation = useMutation({ mutationFn: (form: FormData) => registerStudent(form), onSuccess: () => { setMessage("Tạo tài khoản thành công. Đang chuyển tới trang đăng nhập..."); window.setTimeout(() => navigate("/SignInStudent"), 700); } });
  return <section className="auth-page"><div className="auth-card"><span className="eyebrow">TẠO TÀI KHOẢN</span><h1>Tham gia Study2Work</h1><p>Tạo hồ sơ sinh viên để bắt đầu tìm kiếm cơ hội.</p><form onSubmit={(event) => { event.preventDefault(); mutation.mutate(new FormData(event.currentTarget)); }}><label>Họ tên<input name="hoten" required /></label><label>Email<input name="email" type="email" required /></label><label>Mật khẩu<input name="matkhau" type="password" minLength={6} required /></label><label>Chuyên ngành<input name="chuyennganh" /></label><label>Ảnh đại diện<input name="avt" type="file" accept="image/*" /></label>{message && <div className="form-success">{message}</div>}{mutation.isError && <div className="form-error">{mutation.error instanceof Error ? mutation.error.message : "Đăng ký thất bại."}</div>}<button className="btn btn-primary w-100" disabled={mutation.isPending}>{mutation.isPending ? "Đang tạo..." : "Tạo tài khoản"}</button></form><div className="auth-footer"><Link to="/signUpRole">← Chọn vai trò khác</Link><Link to="/SignInStudent">Đã có tài khoản</Link></div></div></section>;
}

export function BusinessRegisterPage() {
  const [submitted, setSubmitted] = useState(false);
  return <section className="auth-page"><div className="auth-card business-auth-card"><div className="business-logo">DN</div><span className="eyebrow">DOANH NGHIỆP</span><h1>Tạo tài khoản doanh nghiệp</h1><p>Đăng ký để đăng tin tuyển dụng và kết nối ứng viên.</p><form onSubmit={(event) => { event.preventDefault(); setSubmitted(true); }}><label>Tên công ty<input name="hoten" required placeholder="VD: Công ty Minh Long" /></label><label>Email doanh nghiệp<input name="email" type="email" required placeholder="company@example.com" /></label><label>Số điện thoại<input name="sodienthoai" required placeholder="098xxxxxxx" /></label><label>Mật khẩu<input name="matkhau" type="password" required minLength={6} placeholder="Tối thiểu 6 ký tự" /></label><label>Nhập lại mật khẩu<input name="matkhauConfirm" type="password" required minLength={6} placeholder="Nhập lại mật khẩu" /></label>{submitted && <div className="form-success">Đăng ký doanh nghiệp đang được hoàn thiện. Vui lòng liên hệ bộ phận hỗ trợ.</div>}<button className="btn btn-primary w-100" type="submit">Tạo tài khoản</button></form><div className="auth-footer"><Link to="/signUpRole">← Chọn vai trò khác</Link><Link to="/signInBusiness">Đã có tài khoản</Link></div><small>Hỗ trợ doanh nghiệp: support@learn2earn.vn</small></div></section>;
}

export function ComingSoonPage() {
  return <section className="state-page"><div className="state-icon"><i className="fa-solid fa-rocket" /></div><span className="eyebrow">COMING SOON</span><h1>Tính năng đang được hoàn thiện</h1><p>Study2Work sẽ sớm mang tính năng này đến với bạn.</p><Link className="btn btn-primary" to="/">Về trang chủ</Link></section>;
}

export function ErrorRolePage() {
  return <section className="state-page"><div className="state-icon danger"><i className="fa-solid fa-lock" /></div><span className="eyebrow">KHÔNG CÓ QUYỀN TRUY CẬP</span><h1>Bạn không thể mở trang này</h1><p>Vui lòng đăng nhập bằng tài khoản đúng vai trò.</p><Link className="btn btn-primary" to="/signInRole">Đăng nhập lại</Link></section>;
}
