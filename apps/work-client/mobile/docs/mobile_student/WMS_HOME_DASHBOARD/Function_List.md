# Function list — WMS_HOME_DASHBOARD

## WMS_HOME_DASHBOARD-FN01 — TrangChu interaction

- **View:** WMS_HOME_DASHBOARD-V01
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Sinh viên; production permission chưa có contract.
- **Rule:** WMS_HOME_DASHBOARD-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** Student home, profile header, top JD, notifications và utilities.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** WIRED, `lib/views/trang_chu/main/trang_chu.dart`.

## WMS_HOME_DASHBOARD-TC01 — TrangChu verification case

- **Covers:** WMS_HOME_DASHBOARD-FN01 và WMS_HOME_DASHBOARD-V01.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## WMS_HOME_DASHBOARD-FN02 — ThongBao interaction

- **View:** WMS_HOME_DASHBOARD-V02
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Sinh viên; production permission chưa có contract.
- **Rule:** WMS_HOME_DASHBOARD-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** Static notification list và detail dialog.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** UI-ONLY, `lib/views/trang_chu/main/thong_bao.dart`.

## WMS_HOME_DASHBOARD-TC02 — ThongBao verification case

- **Covers:** WMS_HOME_DASHBOARD-FN02 và WMS_HOME_DASHBOARD-V02.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## WMS_HOME_DASHBOARD-FN03 — ThongTinChiTiet interaction

- **View:** WMS_HOME_DASHBOARD-V03
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Sinh viên; production permission chưa có contract.
- **Rule:** WMS_HOME_DASHBOARD-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** Static profile/detail presentation.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** UI-ONLY, `lib/views/trang_chu/main/thong_tin_chi_tiet.dart`.

## WMS_HOME_DASHBOARD-TC03 — ThongTinChiTiet verification case

- **Covers:** WMS_HOME_DASHBOARD-FN03 và WMS_HOME_DASHBOARD-V03.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## WMS_HOME_DASHBOARD-FN04 — XemChiTiet interaction

- **View:** WMS_HOME_DASHBOARD-V04
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Sinh viên; production permission chưa có contract.
- **Rule:** WMS_HOME_DASHBOARD-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** Legacy static detail retained.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** LEGACY, `lib/views/trang_chu/main/xem_chi_tiet.dart`.

## WMS_HOME_DASHBOARD-TC04 — XemChiTiet verification case

- **Covers:** WMS_HOME_DASHBOARD-FN04 và WMS_HOME_DASHBOARD-V04.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## Test matrix

| Test ID | View | Scenario | Result |
|---|---|---|---|
| WMS_HOME_DASHBOARD-TC01 | WMS_HOME_DASHBOARD-V01 | TrangChu happy/error/empty state phù hợp | Runtime-unverified |
| WMS_HOME_DASHBOARD-TC02 | WMS_HOME_DASHBOARD-V02 | ThongBao happy/error/empty state phù hợp | Runtime-unverified |
| WMS_HOME_DASHBOARD-TC03 | WMS_HOME_DASHBOARD-V03 | ThongTinChiTiet happy/error/empty state phù hợp | Runtime-unverified |
| WMS_HOME_DASHBOARD-TC04 | WMS_HOME_DASHBOARD-V04 | XemChiTiet happy/error/empty state phù hợp | Runtime-unverified |
