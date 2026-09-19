# Function list — WMS_STUDENT_UTILITIES

## WMS_STUDENT_UTILITIES-FN01 — LichPhongVanView interaction

- **View:** WMS_STUDENT_UTILITIES-V01
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Sinh viên; production permission chưa có contract.
- **Rule:** WMS_STUDENT_UTILITIES-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** Interview utility UI với local state.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** WIRED, `lib/views/trang_chu/tien_ich/Lich_PV/lich_pv.dart`.

## WMS_STUDENT_UTILITIES-TC01 — LichPhongVanView verification case

- **Covers:** WMS_STUDENT_UTILITIES-FN01 và WMS_STUDENT_UTILITIES-V01.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## WMS_STUDENT_UTILITIES-FN02 — HoTroSinhVienView interaction

- **View:** WMS_STUDENT_UTILITIES-V02
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Sinh viên; production permission chưa có contract.
- **Rule:** WMS_STUDENT_UTILITIES-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** Student support UI.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** WIRED, `lib/views/trang_chu/tien_ich/Hotro_SV/ho_tro_sv.dart`.

## WMS_STUDENT_UTILITIES-TC02 — HoTroSinhVienView verification case

- **Covers:** WMS_STUDENT_UTILITIES-FN02 và WMS_STUDENT_UTILITIES-V02.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## WMS_STUDENT_UTILITIES-FN03 — KhoaHocView interaction

- **View:** WMS_STUDENT_UTILITIES-V03
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Sinh viên; production permission chưa có contract.
- **Rule:** WMS_STUDENT_UTILITIES-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** Student course UI.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** WIRED, `lib/views/trang_chu/tien_ich/Khoa_hoc/khoa_hoc.dart`.

## WMS_STUDENT_UTILITIES-TC03 — KhoaHocView verification case

- **Covers:** WMS_STUDENT_UTILITIES-FN03 và WMS_STUDENT_UTILITIES-V03.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## WMS_STUDENT_UTILITIES-FN04 — TinTucView interaction

- **View:** WMS_STUDENT_UTILITIES-V04
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Sinh viên; production permission chưa có contract.
- **Rule:** WMS_STUDENT_UTILITIES-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** Student news UI.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** WIRED, `lib/views/trang_chu/tien_ich/Tin_Tuc/tin_tuc.dart`.

## WMS_STUDENT_UTILITIES-TC04 — TinTucView verification case

- **Covers:** WMS_STUDENT_UTILITIES-FN04 và WMS_STUDENT_UTILITIES-V04.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## Test matrix

| Test ID | View | Scenario | Result |
|---|---|---|---|
| WMS_STUDENT_UTILITIES-TC01 | WMS_STUDENT_UTILITIES-V01 | LichPhongVanView happy/error/empty state phù hợp | Runtime-unverified |
| WMS_STUDENT_UTILITIES-TC02 | WMS_STUDENT_UTILITIES-V02 | HoTroSinhVienView happy/error/empty state phù hợp | Runtime-unverified |
| WMS_STUDENT_UTILITIES-TC03 | WMS_STUDENT_UTILITIES-V03 | KhoaHocView happy/error/empty state phù hợp | Runtime-unverified |
| WMS_STUDENT_UTILITIES-TC04 | WMS_STUDENT_UTILITIES-V04 | TinTucView happy/error/empty state phù hợp | Runtime-unverified |

