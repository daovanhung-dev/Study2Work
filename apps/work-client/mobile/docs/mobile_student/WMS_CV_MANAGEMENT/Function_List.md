# Function list — WMS_CV_MANAGEMENT

## WMS_CV_MANAGEMENT-FN01 — QuanLyCVView interaction

- **View:** WMS_CV_MANAGEMENT-V01
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Sinh viên; production permission chưa có contract.
- **Rule:** WMS_CV_MANAGEMENT-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** CV load/edit form qua CVCtrl.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** WIRED, `lib/views/trang_chu/tien_ich/Quan_ly_CV/quan_ly_cv.dart`.

## WMS_CV_MANAGEMENT-TC01 — QuanLyCVView verification case

- **Covers:** WMS_CV_MANAGEMENT-FN01 và WMS_CV_MANAGEMENT-V01.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## Test matrix

| Test ID | View | Scenario | Result |
|---|---|---|---|
| WMS_CV_MANAGEMENT-TC01 | WMS_CV_MANAGEMENT-V01 | QuanLyCVView happy/error/empty state phù hợp | Runtime-unverified |

