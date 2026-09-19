# Function list — WMB_JOB_MANAGEMENT

## WMB_JOB_MANAGEMENT-FN01 — DangTinTuyenDung interaction

- **View:** WMB_JOB_MANAGEMENT-V01
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Doanh nghiệp; production permission chưa có contract.
- **Rule:** WMB_JOB_MANAGEMENT-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** Form đăng tin, tạo map JD và insert bằng company id.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** WIRED, `lib/views/trang_chu/main/dang_tin_tuyen_dung.dart`.

## WMB_JOB_MANAGEMENT-TC01 — DangTinTuyenDung verification case

- **Covers:** WMB_JOB_MANAGEMENT-FN01 và WMB_JOB_MANAGEMENT-V01.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## WMB_JOB_MANAGEMENT-FN02 — QuanLyJob interaction

- **View:** WMB_JOB_MANAGEMENT-V02
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Doanh nghiệp; production permission chưa có contract.
- **Rule:** WMB_JOB_MANAGEMENT-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** Danh sách JD theo company và route detail/post form.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** WIRED, `lib/views/trang_chu/tien_ich/Quan_ly_job/quan_ly_job.dart`.

## WMB_JOB_MANAGEMENT-TC02 — QuanLyJob verification case

- **Covers:** WMB_JOB_MANAGEMENT-FN02 và WMB_JOB_MANAGEMENT-V02.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## WMB_JOB_MANAGEMENT-FN03 — XemChiTietJD interaction

- **View:** WMB_JOB_MANAGEMENT-V03
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Doanh nghiệp; production permission chưa có contract.
- **Rule:** WMB_JOB_MANAGEMENT-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** FutureBuilder load JD detail bằng helper Neon.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** WIRED, `lib/views/trang_chu/tien_ich/Quan_ly_job/chi_tiet_job.dart`.

## WMB_JOB_MANAGEMENT-TC03 — XemChiTietJD verification case

- **Covers:** WMB_JOB_MANAGEMENT-FN03 và WMB_JOB_MANAGEMENT-V03.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## Test matrix

| Test ID | View | Scenario | Result |
|---|---|---|---|
| WMB_JOB_MANAGEMENT-TC01 | WMB_JOB_MANAGEMENT-V01 | DangTinTuyenDung happy/error/empty state phù hợp | Runtime-unverified |
| WMB_JOB_MANAGEMENT-TC02 | WMB_JOB_MANAGEMENT-V02 | QuanLyJob happy/error/empty state phù hợp | Runtime-unverified |
| WMB_JOB_MANAGEMENT-TC03 | WMB_JOB_MANAGEMENT-V03 | XemChiTietJD happy/error/empty state phù hợp | Runtime-unverified |

