# Flutter Business deep context

`CONTEXT_STATUS: SOURCE_BACKED`

Source root: `apps/work-client/mobile/lib/features/business/legacy/` during
the migration to the unified `study2work_mobile` project.

Đây là role Business trong Flutter project dùng flavor `business`. Các
helper/model legacy được giữ dưới boundary Business; shared app/core code nằm
ngoài thư mục này và không được copy lại vào role source.

## Bootstrap và route graph

Root `lib/main.dart` khởi tạo Flutter binding, đọc flavor và giữ hỗ trợ
`sqfliteFfiInit()` trên desktop non-Android/iOS cho Business. Top-level app dùng
`MaterialApp.router`/go_router; legacy screens vẫn có một số
`MaterialPageRoute` nội bộ trong giai đoạn migration.

```text
main.dart
  -> views/dang_nhap/dang_nhap.dart (DangNhap)
      -> Riverpod authRepositoryProvider -> BusinessAuthRepository
          -> controllers/dang_nhap/dangnhap_ctrl.dart
          -> helper_db/helper_supabase.dart -> NeonDatabase -> Neon
          -> helper_db/helper_db.dart -> SQLite doanhnghiep.db
      -> AuthNavigationState -> `/business` -> views/dang_nhap/menu.dart (Menu)
          -> TrangChu | TroChuyen | UngVien | Setting
```

| Entry/destination | Current behavior | Data dependency |
|---|---|---|
| `DangNhap` | Company email/password login and transition to `Menu`. | `DNSupabase.ktDangNhap/getDN`, `HelperDB.saveDoanhNghiep`, `saveNganh`. |
| `Menu` | Animated destination shell for home, chat, candidates and settings. | No remote call; composes views. |
| `TrangChu` | Company home, job posting/management, top CV, candidate search and report utilities. | `HelperDB`, `DNSupabase`, top-CV controller and local UI screens. |
| `TroChuyen` | Loads students with a conversation and opens `ChatView`. | `getChats`, cached company id, `DoanChat`. |
| `UngVien` | Candidate/application list, status actions, candidate details. | `UngTuyenCtrl`, `DNSupabase`, `CV`, `UngVien`. |
| `Setting` | Notifications and local company logout. | `dangXuat`, `HelperDB.clearDoanhNghiep`. |

## Controllers

| File | Public surface | Responsibility and side effect | Status |
|---|---|---|---|
| `controllers/dang_nhap/dangnhap_ctrl.dart` | `dangNhapDN`, globals `dn`, `dnSb` | Checks company credentials in Neon, maps `DoanhNghiep`, saves local company and majors. | Wired |
| `controllers/cai_dat/cai_dat.dart` | `dangXuat` | Deletes cached `doanhnghiep` rows. | Wired |
| `controllers/chat/chat_controller.dart` | `getChat`, `guiTinNhan`, `startMessagePolling*` | Reads/writes `Chat`; three-second polling with initial id seeding and deduplication. | Wired |
| `controllers/chat/nhung_doan_chat_controller.dart` | `getChats` | Joins `DoanChat` with `SinhVien` to list conversation partners. | Wired |
| `controllers/trang_chu/quan_ly_job/quan_ly_job_ctrl.dart` | `getJob` | Reads cached company id, queries its JDs and maps to `JD`. | Wired |
| `controllers/trang_chu/hien_thi_danh_sach_top_cv.dart` | `getTopCV` | Queries TopCV ids and returns selected CV projections in stable id order. | Wired from home |
| `controllers/trang_chu/xem_chi_tiet.dart` | `xemChiTiet` | Reads a CV detail projection by id. | Wired from home/detail composition |
| `controllers/ung_vien/ung_vien_controller.dart` | `getCV`, `ungTuyen`, `delCV`, `getTrangThai` | Reads candidate CVs, changes application status, removes application, creates conversation and sends notification message. | Wired |
| `controllers/lay_ten.dart` | `getNameSV`, `getNameDN` | Direct participant name lookup helpers. | No active caller found |
| `controllers/trang_chu/timkiemctrl.dart` | `timKiem` | Builds fixed-major Gemini prompt; discards returned text. | Source-backed/incomplete result contract |
| `core/data/gemini/gemini_client.dart` | `GeminiClient`, `AIService.sendMessage` | Direct HTTP Gemini call using `GEMINI_API_KEY`; returns first candidate or generic error. | Shared core boundary; direct external side effect |
| `controllers/AI/view_test.dart` | `AITestScreen` | Manual AI test UI. | Unwired |

## Database and helpers

| File | Purpose | Important contract |
|---|---|---|
| `core/data/neon/neon_client.dart` | Shared `NeonClient`, singleton `NeonDatabase`; SSL URL validation/normalization, parameterized SQL, `BigInt` normalization and pool lifecycle. | Direct Neon PostgreSQL; no Work HTTP API. |
| `helper_db/helper_db.dart` | SQLite singleton for `doanhnghiep.db`. | Creates `doanhnghiep` and `bannganh`; stores one local company/session and majors. |
| `helper_db/helper_supabase.dart` | Compatibility-named Neon helper. | Company login/profile, JD insert/detail, candidate CV/application/status/delete, DoanChat and Chat operations. No Supabase runtime import. |
| `helper_db/helper_cv.dart` | Generic CV CRUD/search helper. | Neon `Cv` operations and JSONB/date mapping; some methods are compatibility utilities rather than menu entrypoints. |
| `helper_db/helper_widget.dart` | Business-local UI builders. | Rich label/value, primary button wrapper, text field and dropdown. |

## Models

| File | Model and mapping |
|---|---|
| `models/doanh_nghiep.dart` | `DoanhNghiep`; maps Neon company fields to SQLite-compatible map. |
| `models/dn_supabase.dart` | `DoanhNghiepSB`; compatibility-named JSON/SQLite account model. |
| `models/jd.dart` | `JD`; business job-description fields and row conversion. |
| `models/cv.dart` | `CV`; full candidate CV, `sinhvien_id`, JSONB `social`, date and JSON mapping. |
| `models/ung_vien.dart` | `UngVien`; application ids, company/student relation, status and timestamps. |
| `models/chat.dart` | `DoanChat`; conversation relation and creation timestamp. |
| `models/nganh_nghe.dart` | `Nganh`; accepts lowercase `nganh` and legacy uppercase `Nganh` on read. |

## Views

| File | Widget/screen | Current behavior and wiring |
|---|---|---|
| `views/dang_nhap/dang_nhap.dart` | `DangNhap` | Active company login UI with animated loading; invokes `dangNhapDN`. |
| `views/dang_nhap/menu.dart` | `Menu` | Active animated shell for home/chat/candidates/settings. |
| `views/dang_nhap/quen_mat_khau.dart` | `QuenMatKhau` | UI-only password-recovery shell; no reset backend contract. |
| `views/kiem_tra_wifi.dart` | `KiemTraWifiView` | Connectivity listener/check screen with retry/exit; not reached from current main route. |
| `views/cai_dat/setting.dart` | `Setting` | Active settings, notification navigation and local logout. |
| `views/trang_chu/main/trang_chu.dart` | `TrangChu` | Active business dashboard composing jobs, posting, top CV, candidate search, internship, interview, school link and reports. |
| `views/trang_chu/main/dang_tin_tuyen_dung.dart` | `DangTinTuyenDung` | Active job-post form; inserts JD using company id and helper. |
| `views/trang_chu/main/thong_bao.dart` | `ThongBao` | Static notification list/detail dialog. |
| `views/trang_chu/main/thong_tin_chi_tiet.dart` | `ThongTinChiTiet` | Static detail/profile presentation. |
| `views/trang_chu/main/xem_chi_tiet_view.dart` | `XemChiTietView` | CV/detail presentation using controller projection and notification navigation. |
| `views/trang_chu/main/xem_chi_tiet.dart` | `XemChiTiet` | Legacy static detail screen retained beside active detail view. |
| `views/trang_chu/tien_ich/Quan_ly_job/quan_ly_job.dart` | `QuanLyJob` | Active company JD list; routes to `XemChiTietJD` or posting form. |
| `views/trang_chu/tien_ich/Quan_ly_job/chi_tiet_job.dart` | `XemChiTietJD` | Active JD detail FutureBuilder using Neon compatibility helper. |
| `views/trang_chu/tien_ich/Chuong_trinh_thuc_te/chuong_trinh_thuc_tap_page.dart` | `ChuongTrinhThucTapPage`, form | Active internship-program listing/form with local state. |
| `views/trang_chu/tien_ich/Chuong_trinh_thuc_te/chuong_trinh_thuc_tap.dart` | `ThucTapScreen` | Legacy screen retained outside active page route. |
| `views/trang_chu/tien_ich/Lich_phong_van/lich_pv_page.dart` | `LichPV` | Active interview schedule with local form/dialog state. |
| `views/trang_chu/tien_ich/Lich_phong_van/lich_phong_van.dart` | `LichPhongVanScreen` | Legacy screen retained outside active page route. |
| `views/trang_chu/tien_ich/Lien_ket_nha_truong/lien_ket_nha_truong.dart` | `LienKetScreen` | University-linking UI shell; no backend contract. |
| `views/trang_chu/tien_ich/Loc_cv/loc_cv_filter.dart` | `LocCV` | Local project/job/skill filter UI; no remote persistence. |
| `views/trang_chu/tien_ich/Loc_cv/loc_cv_placeholder.dart` | `LocCvPlaceholderScreen` | Placeholder retained outside active route. |
| `views/trang_chu/tien_ich/Thong_ke/thong_ke_bao_cao.dart` | `EmployeeReportUI` | Active report UI using `fl_chart` and local presentation data. |
| `views/trang_chu/tien_ich/Thong_ke/thong_ke.dart` | `ThongKeScreen` | Legacy statistics screen retained outside active report route. |
| `views/trang_chu/tien_ich/Tim_kiem_nhan_su/tim_kiem_nhan_su.dart` | `EmployeeSearchUI` | Active candidate search UI using CV helper and AI prompt helper. |
| `views/tro_chuyen/tro_chuyen.dart` | `TroChuyen` | Active conversation-partner list and chat navigation. |
| `views/tro_chuyen/chat.dart` | `ChatView` | Active chat with history/send/polling and timer cancellation. |
| `views/ung_vien/ung_vien.dart` | `UngVien` | Active candidate/application list, status actions and candidate detail. |
| `lib/dn.dart` | `TempScreen` | Empty placeholder, not wired. |

## Theme, assets and platform

`theme/design_tokens.dart`, `theme/app_theme.dart` and `theme/app_components.dart`
form the business-local Cobalt Material 3 foundation. Business-specific assets
include job, internship, CV-filter, school-link, report and utility icons; the
active home dashboard references these assets directly. `bg_login.png`,
`bg_trangchu.jpg`, `logo.jpg`, `logo-nobr.png` and `avt.jpg` are used by login,
settings, notification, detail and conversation surfaces. `icon_login.png` is
declared but has no current direct code reference.

`android/app/build.gradle.kts` uses application id `com.s2w.work.business`.
The Android namespace/activity package remains `com.example.work_server`.
Desktop SQLite support is configured only in `main.dart`; it does not create a
shared package with the student app.

## Feature flows

### Login/session

```text
DangNhap
  -> dangNhapDN(email, password)
  -> DNSupabase.ktDangNhap + getDN + getNganh
  -> NeonDatabase.query
  -> HelperDB.saveDoanhNghiep + saveNganh
  -> BusinessAuthRepository -> AuthNavigationState -> `/business` -> Menu
```

Logout clears the cached company rows. There is no JWT/session token and no
Work HTTP API call in this client.

### Job posting/management

`DangTinTuyenDung` builds a map of JD fields, `DNSupabase.insertJD` converts
iterables to comma-separated values, quotes columns and executes parameterized
SQL. `QuanLyJob` calls `getJob`, which scopes the query to the local company id;
`XemChiTietJD` loads a selected JD through the compatibility helper.

### Candidate/application

```text
UngVien view
  -> UngTuyenCtrl
  -> DNSupabase.getCV/getUngVien
  -> CV/UngVien models
  -> ungTuyen(sinhvienId)
  -> update UngVien.trangthai
  -> insert DoanChat
  -> insert Chat notification
```

The same helper exposes delete and status-list operations. Candidate detail is
also available through the CV projection controller used by home/detail views.

### Chat

`TroChuyen` loads distinct students from `DoanChat`. `ChatView` reads `Chat`
rows ordered by timestamp/id, sends messages with UTC timestamps and polls
every three seconds. Existing ids are seeded and duplicate ids are ignored;
the screen must cancel its timer in `dispose()`.
