import { useEffect, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Link, useLocation, useNavigate, useParams } from "react-router-dom";

import {
  applyToJob,
  createBusinessJob,
  createCv,
  deleteBusinessJob,
  getBusinessApplications,
  getBusinessJobs,
  getJob,
  getJobs,
  getMyApplications,
  getMyCv,
  getStudentCv,
  logout,
  updateBusinessJob,
  updateCv,
  type Job,
} from "../shared/api/work";
import { useAuth } from "../shared/auth/AuthProvider";
import { EmptyState, ErrorState, LoadingState } from "../shared/ui/States";

function text(record: Record<string, unknown> | null | undefined, key: string, fallback = "") {
  const value = record?.[key];
  return value === undefined || value === null ? fallback : String(value);
}

function idOf(record: Record<string, unknown>) {
  return text(record, "id") || text(record, "id_dn") || text(record, "id_sv");
}

function imageOf(record: Record<string, unknown>) {
  const source = text(record, "avt", "/img/logo-nobr.png");
  return source.startsWith("http") || source.startsWith("/") ? source : `/uploads/${source}`;
}

function SectionHeading({ eyebrow, title, action }: { eyebrow: string; title: string; action?: React.ReactNode }) {
  return <div className="section-heading"><div><span className="eyebrow">{eyebrow}</span><h1>{title}</h1></div>{action}</div>;
}

function JobRow({ job, detail = true }: { job: Job; detail?: boolean }) {
  const id = idOf(job);
  return <article className="job-card"><div className="job-logo"><img src={imageOf(job)} alt="Logo doanh nghiệp" /></div><div className="job-card-content"><span className="job-tag">VIỆC LÀM</span><h3>{text(job, "ten_vi_tri", "Vị trí tuyển dụng")}</h3><p className="company">{text(job, "ten_cong_ty", "Doanh nghiệp")}</p><div className="job-meta"><span><i className="fa-solid fa-location-dot" /> {text(job, "dia_diem", "Chưa cập nhật")}</span><span><i className="fa-regular fa-clock" /> {text(job, "thoi_gian", "Toàn thời gian")}</span></div></div>{detail && id && <Link className="btn btn-outline-primary job-action" to={`/student/JobDescription/${id}`}>Xem chi tiết</Link>}</article>;
}

export function StudentHomePage() {
  const [page, setPage] = useState(1);
  const query = useQuery({ queryKey: ["student-jobs", page], queryFn: () => getJobs(page, 6) });
  if (query.isLoading) return <LoadingState />;
  if (query.isError) return <ErrorState retry={() => void query.refetch()} />;
  const totalPages = Number(query.data?.meta.totalPages || 1);
  return <div className="page-container"><section className="workspace-hero"><span className="eyebrow">KHÁM PHÁ CƠ HỘI</span><h1>Tìm <span>việc làm phù hợp</span> với bạn</h1><p>Khám phá những cơ hội mới và tiến gần hơn tới mục tiêu nghề nghiệp.</p></section><SectionHeading eyebrow="DANH SÁCH VIỆC LÀM" title={`Kết quả tìm kiếm (${query.data?.meta.total || 0})`} /><div className="jobs-list">{query.data?.data.length ? query.data.data.map((job, index) => <JobRow key={idOf(job) || index} job={job} />) : <EmptyState message="Chưa có việc làm nào." />}</div>{totalPages > 1 && <div className="pagination-row"><button className="btn btn-outline-secondary" disabled={page <= 1} onClick={() => setPage((current) => current - 1)}>Trước</button><span>Trang {page} / {totalPages}</span><button className="btn btn-outline-secondary" disabled={page >= totalPages} onClick={() => setPage((current) => current + 1)}>Sau</button></div>}</div>;
}

export function JobDetailPage() {
  const { id = "" } = useParams();
  const query = useQuery({ queryKey: ["job", id], queryFn: () => getJob(id), enabled: Boolean(id) });
  const mutation = useMutation({ mutationFn: () => applyToJob(id) });
  if (query.isLoading) return <LoadingState />;
  if (query.isError || !query.data) return <ErrorState message="Không tìm thấy việc làm." />;
  const job = query.data.data;
  return <div className="page-container detail-page"><Link className="back-link" to="/Student/Home">← Quay lại danh sách</Link><div className="detail-header"><img src={imageOf(job)} alt="Logo doanh nghiệp" /><div><span className="job-tag">ĐANG TUYỂN</span><h1>{text(job, "ten_vi_tri", "Chi tiết tuyển dụng")}</h1><p>{text(job, "ten_cong_ty", "Doanh nghiệp")}</p></div></div><div className="detail-grid"><article className="detail-card"><h2>Thông tin công việc</h2><Info label="Địa điểm" value={text(job, "dia_diem", "Chưa cập nhật")} /><Info label="Mức lương" value={text(job, "muc_luong", "Thương lượng")} /><Info label="Hình thức" value={text(job, "thoi_gian", "Chưa cập nhật")} /><Info label="Cấp bậc" value={text(job, "cap_bac", "Chưa cập nhật")} /><h2>Mô tả công việc</h2><p className="preserve-lines">{text(job, "mo_ta", text(job, "nhiem_vu", "Thông tin đang được cập nhật."))}</p></article><aside className="detail-card apply-card"><h2>Sẵn sàng ứng tuyển?</h2><p>Gửi hồ sơ của bạn tới doanh nghiệp ngay hôm nay.</p><button className="btn btn-primary w-100" disabled={mutation.isPending} onClick={() => mutation.mutate()}>{mutation.isPending ? "Đang gửi..." : "Ứng tuyển ngay"}</button>{mutation.isSuccess && <div className="form-success">Ứng tuyển thành công.</div>}{mutation.isError && <div className="form-error">{mutation.error instanceof Error ? mutation.error.message : "Ứng tuyển thất bại."}</div>}</aside></div></div>;
}

function Info({ label, value }: { label: string; value: string }) {
  return <div className="info-line"><span>{label}</span><strong>{value}</strong></div>;
}

const cvFields = [
  ["hoten", "Họ tên"], ["email", "Email"], ["ngaysinh", "Ngày sinh"], ["gioitinh", "Giới tính"],
  ["sdt", "Số điện thoại"], ["diachi", "Địa chỉ"], ["vitri", "Vị trí mong muốn"], ["nganh", "Ngành"],
  ["muctieunghiep", "Mục tiêu nghề nghiệp"], ["hocvan", "Học vấn"], ["kinhnghiem", "Kinh nghiệm"],
  ["kynang", "Kỹ năng"], ["ngoaingu", "Ngoại ngữ"], ["chungchi", "Chứng chỉ"], ["duan", "Dự án"],
  ["giaithuong", "Giải thưởng"], ["hoatdong", "Hoạt động"], ["portfolio", "Portfolio"], ["luongmongmuon", "Lương mong muốn"],
] as const;

export function CvEditorPage() {
  const location = useLocation();
  const isCreate = location.pathname.toLowerCase().includes("createcv");
  const query = useQuery({ queryKey: ["my-cv"], queryFn: getMyCv, enabled: !isCreate });
  const [values, setValues] = useState<Record<string, string>>({});
  const mutation = useMutation({ mutationFn: (form: FormData) => isCreate ? createCv(form) : updateCv(String(values.id || ""), form), onSuccess: () => void query.refetch() });
  useEffect(() => { if (query.data?.data) { const next: Record<string, string> = {}; for (const [key] of cvFields) next[key] = text(query.data.data, key); next.id = idOf(query.data.data); setValues(next); } }, [query.data]);
  if (!isCreate && query.isLoading) return <LoadingState />;
  if (!isCreate && query.isError && query.error instanceof Error && "status" in query.error && (query.error as { status?: number }).status !== 404) return <ErrorState retry={() => void query.refetch()} />;
  return <div className="page-container form-page"><SectionHeading eyebrow="HỒ SƠ CÁ NHÂN" title={isCreate || !values.id ? "Tạo CV" : "Cập nhật CV"} /><form className="form-card" onSubmit={(event) => { event.preventDefault(); const form = new FormData(event.currentTarget); mutation.mutate(form); }}><div className="form-grid">{cvFields.map(([name, label]) => <label key={name}>{label}{name === "muctieunghiep" || name === "kinhnghiem" || name === "kynang" || name === "hocvan" ? <textarea name={name} value={values[name] || ""} onChange={(event) => setValues({ ...values, [name]: event.target.value })} /> : <input name={name} type={name === "ngaysinh" ? "date" : name === "email" ? "email" : "text"} value={values[name] || ""} onChange={(event) => setValues({ ...values, [name]: event.target.value })} required={name === "hoten" || name === "email"} />}</label>)}<label>Ảnh đại diện<input name="avt" type="file" accept="image/*" /></label></div><div className="form-actions"><Link className="btn btn-light" to="/Student/Home">Hủy</Link><button className="btn btn-primary" disabled={mutation.isPending}>{mutation.isPending ? "Đang lưu..." : "Lưu CV"}</button></div>{mutation.isSuccess && <div className="form-success">Đã lưu CV thành công.</div>}{mutation.isError && <div className="form-error">{mutation.error instanceof Error ? mutation.error.message : "Không thể lưu CV."}</div>}</form></div>;
}

export function StudentApplicationsPage() {
  const query = useQuery({ queryKey: ["my-applications"], queryFn: getMyApplications });
  if (query.isLoading) return <LoadingState />;
  if (query.isError) return <ErrorState retry={() => void query.refetch()} />;
  return <div className="page-container"><SectionHeading eyebrow="THEO DÕI HỒ SƠ" title="Kết quả ứng tuyển" /><div className="application-list">{query.data?.data.length ? query.data.data.map((application, index) => { const job = application.JD as Record<string, unknown> | undefined; const business = application.DoanhNghiep as Record<string, unknown> | undefined; return <article className="application-card" key={idOf(application) || index}><div><span className="job-tag">{text(application, "trangthai", "chưa ứng tuyển")}</span><h2>{text(job, "ten_vi_tri", "Việc làm")}</h2><p>{text(business, "hoten", "Doanh nghiệp")}</p></div><time>{text(application, "created_at", "")}</time></article>; }) : <EmptyState message="Bạn chưa có hồ sơ ứng tuyển nào." />}</div></div>;
}

export function BusinessHomePage() {
  return <div className="page-container"><section className="workspace-hero business-hero"><span className="eyebrow">KHÔNG GIAN DOANH NGHIỆP</span><h1>Tìm kiếm <span>nhân tài</span> cho đội ngũ của bạn</h1><p>Đăng tin tuyển dụng và kết nối với những ứng viên phù hợp.</p><Link className="btn btn-primary" to="/Business/PostJob">Đăng tin tuyển dụng <i className="fa-solid fa-arrow-right" /></Link></section><div className="metric-grid"><div className="metric-card"><i className="fa-solid fa-briefcase" /><strong>Quản lý tin tuyển dụng</strong><Link to="/Business/ManganerJD">Xem danh sách →</Link></div><div className="metric-card"><i className="fa-solid fa-users" /><strong>Theo dõi ứng viên</strong><Link to="/Business/ApplyList">Xem ứng viên →</Link></div></div></div>;
}

export function BusinessJobsPage() {
  const queryClient = useQueryClient();
  const query = useQuery({ queryKey: ["business-jobs"], queryFn: getBusinessJobs });
  const mutation = useMutation({ mutationFn: (id: string) => deleteBusinessJob(id), onSuccess: () => void queryClient.invalidateQueries({ queryKey: ["business-jobs"] }) });
  if (query.isLoading) return <LoadingState />;
  if (query.isError) return <ErrorState retry={() => void query.refetch()} />;
  return <div className="page-container"><SectionHeading eyebrow="DOANH NGHIỆP" title="Quản lý tin tuyển dụng" action={<Link className="btn btn-primary" to="/Business/PostJob">+ Đăng tin mới</Link>} /><div className="table-card">{query.data?.data.length ? query.data.data.map((job, index) => <div className="table-row" key={idOf(job) || index}><div><strong>{text(job, "ten_vi_tri", "Vị trí tuyển dụng")}</strong><span>{text(job, "dia_diem", "Chưa cập nhật")} · {text(job, "muc_luong", "Thương lượng")}</span></div><div className="row-actions"><Link className="btn btn-sm btn-outline-primary" to={`/Business/UpdateJD/${idOf(job)}`}>Sửa</Link><button className="btn btn-sm btn-outline-danger" onClick={() => { if (window.confirm("Bạn chắc muốn xóa tin này?")) mutation.mutate(idOf(job)); }}>Xóa</button></div></div>) : <EmptyState message="Bạn chưa đăng tin tuyển dụng nào." />}</div></div>;
}

export function BusinessJobFormPage() {
  const { id = "" } = useParams();
  const isEdit = Boolean(id);
  const jobs = useQuery({ queryKey: ["business-jobs"], queryFn: getBusinessJobs, enabled: isEdit });
  const job = jobs.data?.data.find((item) => idOf(item) === id);
  const navigate = useNavigate();
  const mutation = useMutation({ mutationFn: (form: FormData) => isEdit ? updateBusinessJob(id, form) : createBusinessJob(form), onSuccess: () => navigate("/Business/ManganerJD") });
  if (isEdit && jobs.isLoading) return <LoadingState />;
  return <div className="page-container form-page"><SectionHeading eyebrow="DOANH NGHIỆP" title={isEdit ? "Cập nhật tin tuyển dụng" : "Đăng tin tuyển dụng"} /><form className="form-card" onSubmit={(event) => { event.preventDefault(); mutation.mutate(new FormData(event.currentTarget)); }}><div className="form-grid">{([["ten_vi_tri", "Tên vị trí", true], ["dia_diem", "Địa điểm", true], ["phong_ban", "Phòng ban", false], ["cap_bac", "Cấp bậc", false], ["muc_luong", "Mức lương", false], ["thoi_gian", "Thời gian làm việc", false], ["nganh", "Ngành", false]] as const).map(([name, label, required]) => <label key={name}>{label}<input name={name} defaultValue={text(job, name)} required={required} /></label>)}{([["mo_ta", "Mô tả"], ["nhiem_vu", "Nhiệm vụ"], ["yeu_cau", "Yêu cầu / kỹ năng"]] as const).map(([name, label]) => <label key={name}>{label}<textarea name={name} defaultValue={text(job, name)} /></label>)}<label>Logo / ảnh<input name="avt" type="file" accept="image/*" /></label></div><div className="form-actions"><Link className="btn btn-light" to="/Business/ManganerJD">Hủy</Link><button className="btn btn-primary" disabled={mutation.isPending}>{mutation.isPending ? "Đang lưu..." : "Lưu tin tuyển dụng"}</button></div>{mutation.isError && <div className="form-error">{mutation.error instanceof Error ? mutation.error.message : "Không thể lưu tin tuyển dụng."}</div>}</form></div>;
}

export function BusinessApplicationsPage() {
  const query = useQuery({ queryKey: ["business-applications"], queryFn: getBusinessApplications });
  if (query.isLoading) return <LoadingState />;
  if (query.isError) return <ErrorState retry={() => void query.refetch()} />;
  return <div className="page-container"><SectionHeading eyebrow="DOANH NGHIỆP" title="Danh sách ứng viên" /><div className="table-card">{query.data?.data.length ? query.data.data.map((application, index) => { const student = application.SinhVien as Record<string, unknown> | undefined; const job = application.JD as Record<string, unknown> | undefined; return <div className="table-row" key={idOf(application) || index}><div><strong>{text(student, "hoten", "Ứng viên")}</strong><span>{text(student, "email")} · {text(job, "ten_vi_tri", "Vị trí")}</span></div><Link className="btn btn-sm btn-outline-primary" to={`/Business/CVDetail/${text(student, "id")}`}>Xem CV</Link></div>; }) : <EmptyState message="Hiện chưa có ứng viên nào ứng tuyển." />}</div></div>;
}

export function CvDetailPage() {
  const { id = "" } = useParams();
  const query = useQuery({ queryKey: ["student-cv", id], queryFn: () => getStudentCv(id), enabled: Boolean(id) });
  if (query.isLoading) return <LoadingState />;
  if (query.isError || !query.data) return <ErrorState message="Không tìm thấy CV ứng viên." />;
  const cv = query.data.data;
  return <div className="page-container"><Link className="back-link" to="/Business/ApplyList">← Quay lại danh sách ứng viên</Link><article className="cv-card"><div className="cv-intro"><img src={imageOf(cv)} alt="Ảnh đại diện ứng viên" /><div><span className="eyebrow">HỒ SƠ ỨNG VIÊN</span><h1>{text(cv, "hoten", "Ứng viên")}</h1><p>{text(cv, "email")}</p></div></div><div className="cv-grid">{cvFields.map(([name, label]) => <Info key={name} label={label} value={text(cv, name, "Chưa cập nhật")} />)}</div></article></div>;
}

const studentLabels: Record<string, string> = { Setting: "Cài đặt", Profile: "Hồ sơ sinh viên", "Update-Profile": "Cập nhật hồ sơ", PostJobs: "Kết quả việc làm", Apply: "Hồ sơ đã ứng tuyển", Noti: "Thông báo", Chat: "Tin nhắn", TopCV: "Top CV", Interview: "Lịch phỏng vấn" };
const businessLabels: Record<string, string> = { Setting: "Cài đặt doanh nghiệp", UpdateInformation: "Thông tin doanh nghiệp", EditInfoApply: "Cập nhật ứng viên", LinkUniversity: "Kết nối trường đại học", Notification: "Thông báo", Chat: "Tin nhắn" };

export function StudentStaticPage() {
  const { page = "" } = useParams();
  if (page === "Setting") return <StudentSettingsPage />;
  if (page === "Profile") return <StudentProfilePage />;
  if (page === "Update-Profile") return <ProfileUpdatePage />;
  if (page === "Noti") return <NotificationPage audience="student" />;
  if (page === "Chat") return <ChatPage audience="student" />;
  if (page === "TopCV") return <TopCvPage />;
  if (page === "Interview") return <InterviewPage />;
  return <StaticWorkspacePage eyebrow="SINH VIÊN" title={studentLabels[page] || "Không gian sinh viên"} description="Tính năng này giữ nguyên bố cục và trải nghiệm Study2Work hiện tại." />;
}

export function BusinessStaticPage() {
  const { page = "" } = useParams();
  if (page === "Setting") return <BusinessSettingsPage />;
  if (page === "UpdateInformation") return <BusinessInformationPage />;
  if (page === "EditInfoApply") return <ApplicantEditPage />;
  if (page === "LinkUniversity") return <UniversityLinkPage />;
  if (page === "Notification") return <NotificationPage audience="business" />;
  if (page === "Chat") return <ChatPage audience="business" />;
  return <StaticWorkspacePage eyebrow="DOANH NGHIỆP" title={businessLabels[page] || "Không gian doanh nghiệp"} description="Tính năng này giữ nguyên bố cục và trải nghiệm Study2Work hiện tại." />;
}

function StaticWorkspacePage({ eyebrow, title, description }: { eyebrow: string; title: string; description: string }) {
  return <div className="page-container"><SectionHeading eyebrow={eyebrow} title={title} /><div className="placeholder-panel"><i className="fa-regular fa-compass" /><h2>{title}</h2><p>{description}</p><span>Giao diện đang sẵn sàng cho dữ liệu API tương ứng.</span></div></div>;
}

function StudentSettingsPage() {
  const user = useAuth().user;
  const [emailNotice, setEmailNotice] = useState(true);
  const [smsNotice, setSmsNotice] = useState(false);
  const [saved, setSaved] = useState(false);
  return <div className="page-container static-screen"><SectionHeading eyebrow="CÀI ĐẶT" title="Cài đặt tài khoản" /><div className="settings-grid"><article className="detail-card"><h2>Thông tin cá nhân</h2><p className="muted-copy">Quản lý thông tin hiển thị và bảo mật tài khoản Study2Work.</p><label className="static-field">Tên hiển thị<input defaultValue="Sinh viên Study2Work" /></label><label className="static-field">Email<input type="email" defaultValue={user?.email || ""} /></label><button className="btn btn-primary" onClick={() => setSaved(true)}>Lưu thay đổi</button>{saved && <div className="form-success">Đã lưu thay đổi trên giao diện.</div>}</article><article className="detail-card"><h2>Thông báo</h2><p className="muted-copy">Bật hoặc tắt các phương thức nhận thông báo.</p><Toggle label="Email" checked={emailNotice} onChange={setEmailNotice} /><Toggle label="SMS" checked={smsNotice} onChange={setSmsNotice} /><button className="btn btn-outline-primary" onClick={() => setSaved(true)}>Lưu tùy chọn</button></article></div><article className="detail-card danger-zone"><h2>Vùng nguy hiểm</h2><p className="muted-copy">Xóa tài khoản sẽ khiến toàn bộ dữ liệu bị xóa vĩnh viễn.</p><button className="btn btn-outline-danger" onClick={() => window.alert("Thao tác này cần được xác nhận với bộ phận hỗ trợ.")}>Xóa tài khoản</button></article></div>;
}

function Toggle({ label, checked, onChange }: { label: string; checked: boolean; onChange: (value: boolean) => void }) {
  return <label className="toggle-row"><span>{label}</span><input type="checkbox" checked={checked} onChange={(event) => onChange(event.target.checked)} /><span className="toggle-track" aria-hidden="true" /></label>;
}

function StudentProfilePage() {
  const user = useAuth().user;
  return <div className="page-container static-screen"><div className="profile-banner"><div className="profile-avatar"><img src="/img/logo-nobr.png" alt="Ảnh đại diện sinh viên" /></div><div><span className="eyebrow">HỒ SƠ SINH VIÊN</span><h1>Sinh viên Study2Work</h1><p>{user?.email || "Chưa cập nhật email"}</p><span className="profile-chip">Sẵn sàng tìm kiếm cơ hội</span></div><Link className="btn btn-light" to="/Student/Update-Profile">Cập nhật hồ sơ</Link></div><div className="profile-grid"><article className="detail-card"><h2><i className="fa-regular fa-id-card" /> Thông tin cá nhân</h2><Info label="Email" value={user?.email || "Chưa cập nhật"} /><Info label="Chuyên ngành" value="Chưa cập nhật" /><Info label="Địa điểm" value="Hà Nội, Việt Nam" /></article><article className="detail-card"><h2><i className="fa-solid fa-bolt" /> Mục tiêu nghề nghiệp</h2><p className="preserve-lines">Hoàn thiện hồ sơ và kết nối với những cơ hội phù hợp với kỹ năng, chuyên ngành của bạn.</p><div className="skill-list"><span>Học tập</span><span>Phát triển kỹ năng</span><span>Ứng tuyển</span></div></article></div></div>;
}

function ProfileUpdatePage() {
  const [saved, setSaved] = useState(false);
  return <div className="page-container form-page static-screen"><SectionHeading eyebrow="HỒ SƠ SINH VIÊN" title="Cập nhật thông tin" /><form className="form-card" onSubmit={(event) => { event.preventDefault(); setSaved(true); }}><div className="form-grid"><label>Họ tên<input name="hoten" required placeholder="Nguyễn Văn A" /></label><label>Email<input name="email" type="email" required placeholder="you@example.com" /></label><label>Số điện thoại<input name="sdt" placeholder="098xxxxxxx" /></label><label>Chuyên ngành<input name="chuyennganh" placeholder="Công nghệ thông tin" /></label><label className="full-field">Giới thiệu<textarea name="gioithieu" placeholder="Chia sẻ ngắn về mục tiêu nghề nghiệp của bạn..." /></label></div><div className="form-actions"><Link className="btn btn-light" to="/Student/Profile">Hủy</Link><button className="btn btn-primary">Lưu thông tin</button></div>{saved && <div className="form-success">Đã lưu thông tin trên giao diện.</div>}</form></div>;
}

function NotificationPage({ audience }: { audience: "student" | "business" }) {
  const [filter, setFilter] = useState("all");
  const title = audience === "student" ? "Thông báo" : "Thông báo doanh nghiệp";
  const rows = audience === "student" ? ["Mời phỏng vấn vị trí phù hợp", "Nhắc nhở cập nhật hồ sơ cá nhân", "CV của bạn đã được xem"] : ["Có ứng viên mới ứng tuyển", "Nhắc nhở cập nhật tin tuyển dụng", "Hệ thống Study2Work đã cập nhật"];
  return <div className="page-container static-screen"><SectionHeading eyebrow="THÔNG BÁO" title={title} action={<button className="btn btn-outline-secondary" onClick={() => setFilter("all")}>Đánh dấu đã đọc</button>} /><div className="filter-pills">{["all", "unread", "recruit", "system"].map((item) => <button className={filter === item ? "active" : ""} key={item} onClick={() => setFilter(item)}>{item === "all" ? "Tất cả" : item === "unread" ? "Chưa đọc" : item === "recruit" ? "Tuyển dụng" : "Hệ thống"}</button>)}</div><div className="notification-list">{rows.map((row, index) => <article className={`notification-card ${index === 0 && filter !== "system" ? "unread" : ""}`} key={row}><div className="notification-icon"><i className={audience === "student" ? "fa-solid fa-briefcase" : "fa-solid fa-user-plus"} /></div><div><strong>{row}</strong><p>Thông tin được hiển thị theo trải nghiệm hiện tại của Study2Work.</p><small>Hôm nay · 09:{20 + index}</small></div><button className="btn btn-sm btn-light" onClick={() => window.alert("Đã mở thông báo.")}>Xem</button></article>)}</div></div>;
}

function ChatPage({ audience }: { audience: "student" | "business" }) {
  const [search, setSearch] = useState("");
  const [message, setMessage] = useState("");
  const [sent, setSent] = useState<string[]>([]);
  const partner = audience === "student" ? "Công ty Study2Work" : "Nguyễn Văn A";
  return <div className="page-container static-screen"><SectionHeading eyebrow="TIN NHẮN" title={audience === "student" ? "Trò chuyện với doanh nghiệp" : "Trò chuyện với ứng viên"} /><div className="chat-layout"><aside className="detail-card chat-contacts"><input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Tìm theo tên hoặc vị trí..." /><button className="chat-contact active"><i className="fa-solid fa-circle-user" /><span><strong>{partner}</strong><small>{search ? `Tìm kiếm: ${search}` : "Trao đổi về cơ hội tuyển dụng"}</small></span></button><button className="chat-contact"><i className="fa-solid fa-circle-user" /><span><strong>Study2Work Support</strong><small>Hỗ trợ tài khoản</small></span></button></aside><section className="detail-card chat-window"><div className="chat-title"><strong>{partner}</strong><small>Đang hoạt động</small></div><div className="chat-body"><div className="chat-bubble received">Xin chào! Mình có thể hỗ trợ gì cho bạn?</div>{sent.map((item) => <div className="chat-bubble sent" key={item}>{item}</div>)}</div><form className="chat-compose" onSubmit={(event) => { event.preventDefault(); if (message.trim()) { setSent([...sent, message.trim()]); setMessage(""); } }}><input value={message} onChange={(event) => setMessage(event.target.value)} placeholder="Nhập tin nhắn..." /><button className="btn btn-primary">Gửi</button></form></section></div></div>;
}

function TopCvPage() {
  const [search, setSearch] = useState("");
  return <div className="page-container static-screen"><SectionHeading eyebrow="KHÁM PHÁ HỒ SƠ" title="Top CV sinh viên" /><div className="search-strip"><input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Tìm theo tên sinh viên, vị trí..." /><button className="btn btn-primary">Tìm kiếm</button></div><div className="table-card"><div className="table-header"><strong>Danh sách CV nổi bật</strong><span>{search ? `Kết quả cho “${search}”` : "Cập nhật liên tục"}</span></div>{["Sinh viên Công nghệ thông tin", "Ứng viên Marketing", "Thực tập sinh Kinh doanh"].map((name, index) => <div className="table-row" key={name}><div><strong>{name}</strong><span>Hồ sơ Study2Work · Cập nhật gần đây</span></div><button className="btn btn-sm btn-outline-primary" onClick={() => window.alert("Chi tiết CV sẽ được mở khi API Top CV được kết nối.")}>Xem CV</button></div>)}</div></div>;
}

function InterviewPage() {
  const [filter, setFilter] = useState("all");
  const events = ["Phỏng vấn Frontend Intern", "Trao đổi hồ sơ cùng Study2Work", "Phỏng vấn vòng HR"];
  return <div className="page-container static-screen"><SectionHeading eyebrow="LỊCH PHỎNG VẤN" title="Lịch phỏng vấn" /><div className="filter-pills">{["all", "upcoming", "done", "cancel"].map((item) => <button className={filter === item ? "active" : ""} key={item} onClick={() => setFilter(item)}>{item === "all" ? "Tất cả" : item === "upcoming" ? "Sắp diễn ra" : item === "done" ? "Đã diễn ra" : "Đã hủy"}</button>)}</div><div className="interview-list">{events.map((event, index) => <article className="interview-card" key={event}><div className="calendar-icon"><strong>{12 + index}</strong><small>THÁNG 6</small></div><div><span className="job-tag">{index === 0 ? "SẮP DIỄN RA" : "LỊCH HẸN"}</span><h2>{event}</h2><p><i className="fa-regular fa-clock" /> 09:00 · Hình thức online</p></div><button className="btn btn-outline-primary" onClick={() => window.alert("Đã mở chi tiết lịch phỏng vấn.")}>Chi tiết</button></article>)}</div></div>;
}

function BusinessSettingsPage() {
  const user = useAuth().user;
  const [saved, setSaved] = useState(false);
  return <div className="page-container static-screen"><SectionHeading eyebrow="DOANH NGHIỆP" title="Cài đặt doanh nghiệp" /><div className="settings-grid"><article className="detail-card"><h2>Thông tin công ty</h2><Info label="Tên" value="Công ty Study2Work" /><Info label="Email" value={user?.email || "company@example.com"} /><Info label="Địa chỉ" value="Hà Nội, Việt Nam" /><Link className="btn btn-outline-primary" to="/Business/UpdateInformation">Sửa thông tin</Link></article><article className="detail-card"><h2>Đổi mật khẩu</h2><label className="static-field">Mật khẩu hiện tại<input type="password" /></label><label className="static-field">Mật khẩu mới<input type="password" /></label><label className="static-field">Nhập lại<input type="password" /></label><button className="btn btn-primary" onClick={() => setSaved(true)}>Cập nhật mật khẩu</button>{saved && <div className="form-success">Đã ghi nhận thay đổi trên giao diện.</div>}</article></div></div>;
}

function BusinessInformationPage() {
  const user = useAuth().user;
  const [saved, setSaved] = useState(false);
  return <div className="page-container form-page static-screen"><SectionHeading eyebrow="DOANH NGHIỆP" title="Cập nhật thông tin doanh nghiệp" /><form className="form-card" onSubmit={(event) => { event.preventDefault(); setSaved(true); }}><div className="form-grid"><label>Tên công ty<input required defaultValue="Công ty Study2Work" /></label><label>Email<input required type="email" defaultValue={user?.email || ""} /></label><label>Số điện thoại<input placeholder="098xxxxxxx" /></label><label>Địa chỉ<input placeholder="Hà Nội, Việt Nam" /></label><label className="full-field">Giới thiệu<textarea placeholder="Giới thiệu về doanh nghiệp..." /></label></div><div className="form-actions"><Link className="btn btn-light" to="/Business/Setting">Hủy</Link><button className="btn btn-primary">Lưu thông tin</button></div>{saved && <div className="form-success">Đã lưu thông tin trên giao diện.</div>}</form></div>;
}

function ApplicantEditPage() {
  const [saved, setSaved] = useState(false);
  return <div className="page-container form-page static-screen"><SectionHeading eyebrow="ỨNG VIÊN" title="Cập nhật thông tin ứng viên" /><form className="form-card" onSubmit={(event) => { event.preventDefault(); setSaved(true); }}><div className="form-grid"><label>Tên ứng viên<input placeholder="Nguyễn Văn A" /></label><label>Trạng thái<select defaultValue="Đang xem xét"><option>Đang xem xét</option><option>Mời phỏng vấn</option><option>Đã tuyển</option></select></label><label className="full-field">Ghi chú<textarea placeholder="Thêm ghi chú cho hồ sơ ứng viên..." /></label></div><div className="form-actions"><Link className="btn btn-light" to="/Business/ApplyList">Hủy</Link><button className="btn btn-primary">Lưu thay đổi</button></div>{saved && <div className="form-success">Đã lưu thay đổi trên giao diện.</div>}</form></div>;
}

function UniversityLinkPage() {
  const [sent, setSent] = useState(false);
  return <div className="page-container static-screen"><SectionHeading eyebrow="KẾT NỐI" title="Kết nối nhà trường" /><article className="detail-card connection-card"><div className="connection-icon"><i className="fa-solid fa-school" /></div><h2>Mở rộng mạng lưới tuyển dụng</h2><p className="muted-copy">Gửi yêu cầu kết nối tới nhà trường để tiếp cận nguồn ứng viên phù hợp. Tính năng backend đang được giữ ở trạng thái compatibility.</p><form onSubmit={(event) => { event.preventDefault(); setSent(true); }}><label className="static-field">Tên nhà trường<input required placeholder="Nhập tên nhà trường" /></label><label className="static-field">Lời nhắn<textarea placeholder="Giới thiệu nhu cầu hợp tác..." /></label><button className="btn btn-primary">Gửi yêu cầu kết nối</button></form>{sent && <div className="form-success">Đã ghi nhận yêu cầu trên giao diện.</div>}</article></div>;
}

export function LogoutPage() {
  const navigate = useNavigate();
  const clear = useAuth().clear;
  useEffect(() => { void logout().finally(() => { clear(); navigate("/", { replace: true }); }); }, [clear, navigate]);
  return <LoadingState />;
}
