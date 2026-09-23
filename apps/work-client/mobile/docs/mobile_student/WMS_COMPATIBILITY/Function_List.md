# Function list — WMS_COMPATIBILITY

## WMS_COMPATIBILITY-FN01 — EmployeeSearchUI interaction

- **View:** WMS_COMPATIBILITY-V01
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Sinh viên; production permission chưa có contract.
- **Rule:** WMS_COMPATIBILITY-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** Candidate/CV search surface dùng out-meta helper và AI prompt; không clear active route.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** UNWIRED/LEGACY, `lib/views/trang_chu/tien_ich/Tim_kiem_nhan_su/tim_kiem_nhan_su.dart`.

## WMS_COMPATIBILITY-TC01 — EmployeeSearchUI verification case

- **Covers:** WMS_COMPATIBILITY-FN01 và WMS_COMPATIBILITY-V01.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## Test matrix

| Test ID | View | Scenario | Result |
|---|---|---|---|
| WMS_COMPATIBILITY-TC01 | WMS_COMPATIBILITY-V01 | EmployeeSearchUI happy/error/empty state phù hợp | Runtime-unverified |

