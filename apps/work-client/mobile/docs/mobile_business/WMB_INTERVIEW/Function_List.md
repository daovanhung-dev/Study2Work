# Function list — WMB_INTERVIEW

## WMB_INTERVIEW-FN01 — LichPV interaction

- **View:** WMB_INTERVIEW-V01
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Doanh nghiệp; production permission chưa có contract.
- **Rule:** WMB_INTERVIEW-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** Active interview schedule/form/dialog local state.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** WIRED, `lib/views/trang_chu/tien_ich/Lich_phong_van/lich_pv_page.dart`.

## WMB_INTERVIEW-TC01 — LichPV verification case

- **Covers:** WMB_INTERVIEW-FN01 và WMB_INTERVIEW-V01.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## WMB_INTERVIEW-FN02 — LichPhongVanScreen interaction

- **View:** WMB_INTERVIEW-V02
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Doanh nghiệp; production permission chưa có contract.
- **Rule:** WMB_INTERVIEW-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** Legacy interview screen ngoài active route.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** LEGACY, `lib/views/trang_chu/tien_ich/Lich_phong_van/lich_phong_van.dart`.

## WMB_INTERVIEW-TC02 — LichPhongVanScreen verification case

- **Covers:** WMB_INTERVIEW-FN02 và WMB_INTERVIEW-V02.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## Test matrix

| Test ID | View | Scenario | Result |
|---|---|---|---|
| WMB_INTERVIEW-TC01 | WMB_INTERVIEW-V01 | LichPV happy/error/empty state phù hợp | Runtime-unverified |
| WMB_INTERVIEW-TC02 | WMB_INTERVIEW-V02 | LichPhongVanScreen happy/error/empty state phù hợp | Runtime-unverified |

