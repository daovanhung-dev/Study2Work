# Function list — WMS_JOB_SEARCH_APPLICATION

## WMS_JOB_SEARCH_APPLICATION-FN01 — TimKiemViecView interaction

- **View:** WMS_JOB_SEARCH_APPLICATION-V01
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Sinh viên; production permission chưa có contract.
- **Rule:** WMS_JOB_SEARCH_APPLICATION-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** Load all JD, lọc keyword/location/type, mở detail/apply.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** WIRED, `lib/views/tim_kiem_cong_viec/tim_kiem_job.dart`.

## WMS_JOB_SEARCH_APPLICATION-TC01 — TimKiemViecView verification case

- **Covers:** WMS_JOB_SEARCH_APPLICATION-FN01 và WMS_JOB_SEARCH_APPLICATION-V01.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## WMS_JOB_SEARCH_APPLICATION-FN02 — XemChiTietView interaction

- **View:** WMS_JOB_SEARCH_APPLICATION-V02
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Sinh viên; production permission chưa có contract.
- **Rule:** WMS_JOB_SEARCH_APPLICATION-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** JD detail FutureBuilder và application path.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** WIRED, `lib/views/trang_chu/main/xem_chi_tiet_view.dart`.

## WMS_JOB_SEARCH_APPLICATION-TC02 — XemChiTietView verification case

- **Covers:** WMS_JOB_SEARCH_APPLICATION-FN02 và WMS_JOB_SEARCH_APPLICATION-V02.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## WMS_JOB_SEARCH_APPLICATION-FN03 — DangTinTuyenDung interaction

- **View:** WMS_JOB_SEARCH_APPLICATION-V03
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Sinh viên; production permission chưa có contract.
- **Rule:** WMS_JOB_SEARCH_APPLICATION-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** Student copy dùng out-meta business helper nhưng không nằm trong active menu graph.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** UNWIRED/LEGACY, `lib/views/trang_chu/main/dang_tin_tuyen_dung.dart`.

## WMS_JOB_SEARCH_APPLICATION-TC03 — DangTinTuyenDung verification case

- **Covers:** WMS_JOB_SEARCH_APPLICATION-FN03 và WMS_JOB_SEARCH_APPLICATION-V03.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## Test matrix

| Test ID | View | Scenario | Result |
|---|---|---|---|
| WMS_JOB_SEARCH_APPLICATION-TC01 | WMS_JOB_SEARCH_APPLICATION-V01 | TimKiemViecView happy/error/empty state phù hợp | Runtime-unverified |
| WMS_JOB_SEARCH_APPLICATION-TC02 | WMS_JOB_SEARCH_APPLICATION-V02 | XemChiTietView happy/error/empty state phù hợp | Runtime-unverified |
| WMS_JOB_SEARCH_APPLICATION-TC03 | WMS_JOB_SEARCH_APPLICATION-V03 | DangTinTuyenDung happy/error/empty state phù hợp | Runtime-unverified |

