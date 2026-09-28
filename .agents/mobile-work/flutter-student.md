# Flutter Student deep context

`CONTEXT_STATUS: SOURCE_BACKED`

Source root: `apps/work-client/mobile/lib/features/student/legacy/` during
the migration to the unified `study2work_mobile` project.

Đây là role Student trong Flutter project dùng flavor `student`. Các helper/model
legacy được giữ dưới boundary Student; shared app/core code nằm ngoài thư mục
này và không được copy lại vào role source.

## Bootstrap và route graph

Root `lib/main.dart` đọc flavor, khởi tạo `ProviderScope` và
`MaterialApp.router`. Legacy `Menu` vẫn giữ state/index và một số
`MaterialPageRoute` nội bộ trong giai đoạn compatibility migration.

```text
main.dart
  -> views/dang_nhap/dang_nhap.dart (DangNhap)
      -> Riverpod authRepositoryProvider -> StudentAuthRepository
          -> controllers/dang_nhap/dangnhap_ctrl.dart
          -> helper_db/sinh_vien/helper_supabase.dart -> NeonDatabase -> Neon
          -> helper_db/sinh_vien/helper_db.dart -> SQLite sinhvien.db
      -> AuthNavigationState -> `/student` -> views/dang_nhap/menu.dart (Menu)
          -> TrangChu | TimKiemViecView | TroChuyen | Setting
```

| Entry/destination | Current behavior | Data dependency |
|---|---|---|
| `DangNhap` | Email/password form, loading/error state, opens `Menu` after login. | `dangNhapDN`, Neon `SinhVien`, local SQLite cache. |
| `Menu` | Animated role shell; keeps existing destination indexes and route flow. | No remote call; composes views. |
| `TrangChu` | Student home, profile header, top JD, notifications and utilities. | `TrangChuCtrl`, student SQLite helper, Neon JD/helper queries. |
| `TimKiemViecView` | Loads all JD, filters locally by keyword/location/type, opens detail and application. | `TimKiemCtrl`, `JD`, `UngTuyenCtrl`. |
| `TroChuyen` | Loads business conversation partners and opens `ChatView`. | `getChats`, local cached student id, `DoanChat`. |
| `Setting` | Opens notifications and logs out by clearing local account row. | `dangXuat`, `SinhVienSQLiteHelper`. |

## Controllers

| File | Public surface | Responsibility and side effect | Status |
|---|---|---|---|
| `controllers/dang_nhap/dangnhap_ctrl.dart` | `dangNhapDN`, `autoLogin`, global `student` | Authenticates directly in Neon, stores `SinhVien` and majors in SQLite; `autoLogin` rechecks cached credentials in Neon. | Wired login; `autoLogin` is source-backed but not the main startup path. |
| `controllers/cai_dat/cai_dat.dart` | `dangXuat` | Deletes the local `sinhvien` row. | Wired |
| `controllers/trang_chu/trang_chu_ctrl.dart` | `getTopJd`, `getNameSV`, `getImgSV` | Home facade over Neon top JD and SQLite profile cache. | Wired |
| `controllers/tim_kiem_job/tim_kiem_ctrl.dart` | `TimKiemCtrl.loadJobs`, `filterJobs` | Loads `JD` list once and applies in-memory filters. | Wired |
| `controllers/trang_chu/xem_chi_tiet.dart` | `getAllJD`, `xemChiTiet`, `getJDByNganh`, `getJDByDoanhNghiep`, `updateJD`, `deleteJD` | Direct JD query/detail/update/delete controller. | Source-backed; active detail consumes read path. |
| `controllers/ung_tuyen_ctrl.dart` | `UngTuyenCtrl.ungTuyen` | Gets cached student id, resolves JD company id, inserts a non-duplicate `UngVien`. | Wired |
| `controllers/trang_chu/quan_ly_CV/quan_ly_job_cv.dart` | `CVCtrl.getCVById`, `update` | Reads cached student id, loads CV and delegates CV update. | Wired |
| `controllers/chat/chat_controller.dart` | `getChat`, `guiTinNhan`, `startMessagePolling*` | Reads/writes `Chat`; polling starts an immediate fetch, polls every 3 seconds, emits unseen integer ids only. | Wired |
| `controllers/chat/nhung_doan_chat_controller.dart` | `getChats` | Joins `DoanChat` to `DoanhNghiep` and returns partner id/name summaries. | Wired |
| `core/data/gemini/gemini_client.dart` | `GeminiClient`, `AIService.sendMessage` | Direct HTTP POST to Gemini; returns first candidate text or a generic error string. | Shared core boundary; direct external side effect. |
| `controllers/trang_chu/timkiemctrl.dart` | `timKiem` | Builds a fixed-major prompt and invokes `AIService`; currently discards the returned text. | Source-backed/incomplete result contract. |
| `controllers/trang_chu/hien_thi_danh_sach_top_cv.dart` | `getTopCV` | Reads TopCV ids then projects matching CV rows. | No active caller found. |
| `controllers/lay_ten.dart` | `getNameSV`, `getNameDN` | Direct name lookup helpers. | No active caller found. |
| `controllers/ung_vien_controller.dart` | `xemChiTiet` | CV projection for candidate-detail map keys. | No active caller found; separate from `ung_tuyen_ctrl.dart`. |
| `controllers/AI/view_test.dart` | `AITestScreen` | Manual AI test UI. | Unwired |

## Database and helpers

| File | Purpose | Important contract |
|---|---|---|
| `core/data/neon/neon_client.dart` | Shared `NeonClient`, singleton `NeonDatabase`; normalizes SSL URL, removes `channel_binding`, sets pool/timeout defaults, converts `BigInt` ids and exposes `query`, `execute`, `initialize`, `close`. | All remote SQL is parameterized PostgreSQL SQL; direct Neon is prototype-only. |
| `helper_db/sinh_vien/helper_db.dart` | SQLite singleton for `sinhvien.db`. | Creates `sinhvien` and `bannganh`; login replaces the cached account and stores majors. |
| `helper_db/sinh_vien/helper_supabase.dart` | Compatibility-named Neon helper. | Student CRUD/login, majors, DoanChat, top JD, JD lookup, application insert and CV update. No Supabase runtime import. |
| `helper_db/sinh_vien/helper_cv.dart` | Generic CV CRUD/search helper. | Neon `Cv` CRUD, `ILIKE` search, JSON encode for `social`, empty/false fallback on caught errors. |
| `helper_db/sinh_vien/helper_widget.dart` | Student-local UI builders. | Rich label/value, primary button wrapper, text field and dropdown. |
| `helper_db/out_meta/helper_db_error.dart` | Legacy/business-shaped SQLite helper. | Creates `doanhnghiep` and `bannganh`; retained for compatibility screens. |
| `helper_db/out_meta/helper_supabase_error.dart` | Legacy/business-shaped Neon helper. | Company login/profile, candidate CV query and JD insert/detail. |
| `helper_db/out_meta/helper_cv.dart` | Legacy CV helper using `models/outmeta/cv.dart`. | Same Neon CV CRUD/search shape as the student helper. |
| `helper_db/out_meta/helper_widget.dart` | Legacy UI helper copy. | Same local widget primitives as student helper. |

## Models

| File | Model(s) and mapping |
|---|---|
| `models/sinh_vien/sinh_vien.dart` | `SinhVien`; nullable profile/login fields, map conversion and id parsing. |
| `models/sinh_vien/jd.dart` | Student `JD`; maps `doanhnghiep_id`/`doanh_nghiep_id`, job fields and asset avatar. |
| `models/sinh_vien/cv.dart` | Student `CV`; nullable profile fields, `DateTime` and JSONB `social` parsing, copy/json/map helpers. |
| `models/sinh_vien/nganh_nghe.dart` | `Nganh`; lowercase `nganh` local-cache mapping. |
| `models/sinh_vien/ung_vien.dart` | `UngVien`; application ids/status/timestamp and JSON mapping. |
| `models/sinh_vien/chat.dart` | `Chat`; message ids, participants, content, timestamp and status mapping. |
| `models/sinh_vien/doan_chat.dart` | `DoanChat`; student/business conversation relation and creation timestamp. |
| `models/outmeta/cv.dart` | Compatibility `CV` duplicate with the same CV fields and JSONB/date parsing. |
| `models/outmeta/jd.dart` | Legacy JD shape without the student company/avatar fields. |
| `models/outmeta/doanh_nghiep.dart` | Legacy company SQLite map model. |
| `models/outmeta/dn_supabase.dart` | Legacy Supabase-named company model; no active import found. |
| `models/outmeta/nganh_nghe.dart` | Legacy major model using uppercase `Nganh` key. |
| `models/models.dart` | Older uppercase-key `DoanhNghiep` model; no active import found. |

## Views

| File | Widget/screen | Current behavior and wiring |
|---|---|---|
| `views/dang_nhap/dang_nhap.dart` | `DangNhap` | Active login UI; includes animated loader, shimmer and bouncing dots. |
| `views/dang_nhap/menu.dart` | `Menu` | Active animated shell for home/search/chat/settings. |
| `views/dang_nhap/quen_mat_khau.dart` | `QuenMatKhauView` | UI-only password-recovery form; no reset API/helper. |
| `views/cai_dat/setting.dart` | `Setting` | Active settings; notification route and logout then login replacement. |
| `views/trang_chu/main/trang_chu.dart` | `TrangChu` | Active home; composes JD detail, notifications, CV, interview, support, course, news and search destinations. |
| `views/trang_chu/main/thong_bao.dart` | `ThongBao` | Static notification list and detail dialog. |
| `views/trang_chu/main/thong_tin_chi_tiet.dart` | `ThongTinChiTiet` | Static detail/profile presentation. |
| `views/trang_chu/main/xem_chi_tiet_view.dart` | `XemChiTietView` | Active FutureBuilder JD detail and application path. |
| `views/trang_chu/main/xem_chi_tiet.dart` | `XemChiTiet` | Legacy static detail screen retained beside active view. |
| `views/trang_chu/main/dang_tin_tuyen_dung.dart` | `DangTinTuyenDung` | Student copy exists and uses out-meta business helpers, but is not in the active student menu graph. |
| `views/tim_kiem_cong_viec/tim_kiem_job.dart` | `TimKiemViecView` | Active search/filter list; opens `XemChiTietView` and can apply. |
| `views/trang_chu/tien_ich/Quan_ly_CV/quan_ly_cv.dart` | `QuanLyCVView` | Active CV load/edit form via `CVCtrl`. |
| `views/trang_chu/tien_ich/Lich_PV/lich_pv.dart` | `LichPhongVanView` | Student interview utility UI with local state. |
| `views/trang_chu/tien_ich/Hotro_SV/ho_tro_sv.dart` | `HoTroSinhVienView` | Student support UI. |
| `views/trang_chu/tien_ich/Khoa_hoc/khoa_hoc.dart` | `KhoaHocView` | Student course UI. |
| `views/trang_chu/tien_ich/Tin_Tuc/tin_tuc.dart` | `TinTucView` | Student news UI. |
| `views/trang_chu/tien_ich/Tim_kiem_nhan_su/tim_kiem_nhan_su.dart` | `EmployeeSearchUI` | Candidate/CV search surface using out-meta helper and AI prompt helper; no clear active home route found. |
| `views/tro_chuyen/tro_chuyen.dart` | `TroChuyen` | Active partner list; opens chat with selected business. |
| `views/tro_chuyen/chat.dart` | `ChatView` | Active chat; uses cached student id, Neon messages, timer polling and dispose cancellation. |
| `lib/sv.dart` | `TempScreen` | Empty placeholder, not wired. |

## Theme, assets and config

`theme/design_tokens.dart`, `theme/app_theme.dart` and `theme/app_components.dart`
form an app-local Cobalt Material 3 layer. The student app declares all files
under `assets/`; direct code references include `logo-nobr.png`, `logo.jpg`,
`bg_trangchu.jpg`, `avt.jpg`, `manager.png`, `calendar.png`,
`online-learning.png`, `help-desk.png`, `newspaper.png` and `tien_ich1.png`.
Other declared images are retained assets without a current direct reference.

`android/app/build.gradle.kts` uses application id `com.s2w.work.students`,
while the Android namespace and Kotlin activity package remain
`com.example.work_server`. Android files are host/build configuration, not a
second application architecture.

## Feature flows

### Login/session

```text
DangNhap
  -> dangNhapDN(email, password)
  -> SinhVienSupabaseHelper.login/getByEmail
  -> NeonDatabase.query
  -> SinhVienSQLiteHelper.insertSinhVien + saveNganh
  -> StudentAuthRepository -> AuthNavigationState -> `/student` -> Menu
```

Logout only deletes the local `sinhvien` row. There is no JWT/session token and
no Work HTTP API call in this client.

### Job/application

```text
TrangChu / TimKiemViecView
  -> TimKiemCtrl or TrangChuCtrl/XemChiTietController
  -> Neon JD/TopJD queries
  -> JD model
  -> UngTuyenCtrl
  -> getIdDnByIdJd + insertUngVien
  -> Neon UngVien
```

### CV

`QuanLyCVView` obtains the cached student id from SQLite, loads the CV from
Neon and delegates update to `SinhVienSupabaseHelper`. Generic CV helpers also
expose insert/list/detail/search/delete, but their active caller coverage is
not equivalent to the dedicated student CV screen.

### Chat

`TroChuyen` queries `DoanChat` partners. `ChatView` queries `Chat` ordered by
timestamp/id, inserts messages with UTC time and starts a three-second polling
timer. Existing rows seed `seenIds`; only new ids reach the UI callback, and
the timer must be cancelled in `dispose()`.
