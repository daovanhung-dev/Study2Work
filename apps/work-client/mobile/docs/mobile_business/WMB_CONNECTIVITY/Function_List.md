# Function list — WMB_CONNECTIVITY

## WMB_CONNECTIVITY-FN01 — KiemTraWifiView interaction

- **View:** WMB_CONNECTIVITY-V01
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Doanh nghiệp; production permission chưa có contract.
- **Rule:** WMB_CONNECTIVITY-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** Connectivity listener/check với retry/exit; không reached từ current main route.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** UNWIRED, `lib/views/kiem_tra_wifi.dart`.

## WMB_CONNECTIVITY-TC01 — KiemTraWifiView verification case

- **Covers:** WMB_CONNECTIVITY-FN01 và WMB_CONNECTIVITY-V01.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## Test matrix

| Test ID | View | Scenario | Result |
|---|---|---|---|
| WMB_CONNECTIVITY-TC01 | WMB_CONNECTIVITY-V01 | KiemTraWifiView happy/error/empty state phù hợp | Runtime-unverified |

