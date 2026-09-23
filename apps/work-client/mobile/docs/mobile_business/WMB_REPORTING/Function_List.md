# Function list — WMB_REPORTING

## WMB_REPORTING-FN01 — EmployeeReportUI interaction

- **View:** WMB_REPORTING-V01
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Doanh nghiệp; production permission chưa có contract.
- **Rule:** WMB_REPORTING-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** Active report UI dùng fl_chart/local presentation data.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** WIRED, `lib/views/trang_chu/tien_ich/Thong_ke/thong_ke_bao_cao.dart`.

## WMB_REPORTING-TC01 — EmployeeReportUI verification case

- **Covers:** WMB_REPORTING-FN01 và WMB_REPORTING-V01.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## WMB_REPORTING-FN02 — ThongKeScreen interaction

- **View:** WMB_REPORTING-V02
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Doanh nghiệp; production permission chưa có contract.
- **Rule:** WMB_REPORTING-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** Legacy statistics screen ngoài active report route.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** LEGACY, `lib/views/trang_chu/tien_ich/Thong_ke/thong_ke.dart`.

## WMB_REPORTING-TC02 — ThongKeScreen verification case

- **Covers:** WMB_REPORTING-FN02 và WMB_REPORTING-V02.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## Test matrix

| Test ID | View | Scenario | Result |
|---|---|---|---|
| WMB_REPORTING-TC01 | WMB_REPORTING-V01 | EmployeeReportUI happy/error/empty state phù hợp | Runtime-unverified |
| WMB_REPORTING-TC02 | WMB_REPORTING-V02 | ThongKeScreen happy/error/empty state phù hợp | Runtime-unverified |

