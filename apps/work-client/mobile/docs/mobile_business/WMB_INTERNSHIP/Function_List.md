# Function list — WMB_INTERNSHIP

## WMB_INTERNSHIP-FN01 — ChuongTrinhThucTapPage interaction

- **View:** WMB_INTERNSHIP-V01
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Doanh nghiệp; production permission chưa có contract.
- **Rule:** WMB_INTERNSHIP-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** Listing page và form entry.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** WIRED, `lib/views/trang_chu/tien_ich/Chuong_trinh_thuc_te/chuong_trinh_thuc_tap_page.dart`.

## WMB_INTERNSHIP-TC01 — ChuongTrinhThucTapPage verification case

- **Covers:** WMB_INTERNSHIP-FN01 và WMB_INTERNSHIP-V01.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## WMB_INTERNSHIP-FN02 — ThucTapScreen interaction

- **View:** WMB_INTERNSHIP-V02
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Doanh nghiệp; production permission chưa có contract.
- **Rule:** WMB_INTERNSHIP-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** Legacy internship screen ngoài active route.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** LEGACY, `lib/views/trang_chu/tien_ich/Chuong_trinh_thuc_te/chuong_trinh_thuc_tap.dart`.

## WMB_INTERNSHIP-TC02 — ThucTapScreen verification case

- **Covers:** WMB_INTERNSHIP-FN02 và WMB_INTERNSHIP-V02.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## Test matrix

| Test ID | View | Scenario | Result |
|---|---|---|---|
| WMB_INTERNSHIP-TC01 | WMB_INTERNSHIP-V01 | ChuongTrinhThucTapPage happy/error/empty state phù hợp | Runtime-unverified |
| WMB_INTERNSHIP-TC02 | WMB_INTERNSHIP-V02 | ThucTapScreen happy/error/empty state phù hợp | Runtime-unverified |
