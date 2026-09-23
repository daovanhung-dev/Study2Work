# Function list — WMB_HOME_DASHBOARD

## WMB_HOME_DASHBOARD-FN01 — TrangChu interaction

- **View:** WMB_HOME_DASHBOARD-V01
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Doanh nghiệp; production permission chưa có contract.
- **Rule:** WMB_HOME_DASHBOARD-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** Dashboard tới jobs, top CV, candidates, internship, interview, school link, reports.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** WIRED, `lib/views/trang_chu/main/trang_chu.dart`.

## WMB_HOME_DASHBOARD-TC01 — TrangChu verification case

- **Covers:** WMB_HOME_DASHBOARD-FN01 và WMB_HOME_DASHBOARD-V01.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## WMB_HOME_DASHBOARD-FN02 — ThongBao interaction

- **View:** WMB_HOME_DASHBOARD-V02
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Doanh nghiệp; production permission chưa có contract.
- **Rule:** WMB_HOME_DASHBOARD-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** Static notification list và detail dialog.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** UI-ONLY, `lib/views/trang_chu/main/thong_bao.dart`.

## WMB_HOME_DASHBOARD-TC02 — ThongBao verification case

- **Covers:** WMB_HOME_DASHBOARD-FN02 và WMB_HOME_DASHBOARD-V02.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## WMB_HOME_DASHBOARD-FN03 — ThongTinChiTiet interaction

- **View:** WMB_HOME_DASHBOARD-V03
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Doanh nghiệp; production permission chưa có contract.
- **Rule:** WMB_HOME_DASHBOARD-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** Static profile/detail presentation.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** UI-ONLY, `lib/views/trang_chu/main/thong_tin_chi_tiet.dart`.

## WMB_HOME_DASHBOARD-TC03 — ThongTinChiTiet verification case

- **Covers:** WMB_HOME_DASHBOARD-FN03 và WMB_HOME_DASHBOARD-V03.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## WMB_HOME_DASHBOARD-FN04 — XemChiTiet interaction

- **View:** WMB_HOME_DASHBOARD-V04
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Doanh nghiệp; production permission chưa có contract.
- **Rule:** WMB_HOME_DASHBOARD-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** Static detail screen retained beside active variant.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** LEGACY, `lib/views/trang_chu/main/xem_chi_tiet.dart`.

## WMB_HOME_DASHBOARD-TC04 — XemChiTiet verification case

- **Covers:** WMB_HOME_DASHBOARD-FN04 và WMB_HOME_DASHBOARD-V04.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## WMB_HOME_DASHBOARD-FN05 — XemChiTietView interaction

- **View:** WMB_HOME_DASHBOARD-V05
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Doanh nghiệp; production permission chưa có contract.
- **Rule:** WMB_HOME_DASHBOARD-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** FutureBuilder CV/detail và notification navigation.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** WIRED, `lib/views/trang_chu/main/xem_chi_tiet_view.dart`.

## WMB_HOME_DASHBOARD-TC05 — XemChiTietView verification case

- **Covers:** WMB_HOME_DASHBOARD-FN05 và WMB_HOME_DASHBOARD-V05.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## Test matrix

| Test ID | View | Scenario | Result |
|---|---|---|---|
| WMB_HOME_DASHBOARD-TC01 | WMB_HOME_DASHBOARD-V01 | TrangChu happy/error/empty state phù hợp | Runtime-unverified |
| WMB_HOME_DASHBOARD-TC02 | WMB_HOME_DASHBOARD-V02 | ThongBao happy/error/empty state phù hợp | Runtime-unverified |
| WMB_HOME_DASHBOARD-TC03 | WMB_HOME_DASHBOARD-V03 | ThongTinChiTiet happy/error/empty state phù hợp | Runtime-unverified |
| WMB_HOME_DASHBOARD-TC04 | WMB_HOME_DASHBOARD-V04 | XemChiTiet happy/error/empty state phù hợp | Runtime-unverified |
| WMB_HOME_DASHBOARD-TC05 | WMB_HOME_DASHBOARD-V05 | XemChiTietView happy/error/empty state phù hợp | Runtime-unverified |

