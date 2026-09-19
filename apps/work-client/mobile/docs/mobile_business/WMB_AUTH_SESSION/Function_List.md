# Function list — WMB_AUTH_SESSION

## WMB_AUTH_SESSION-FN01 — DangNhap interaction

- **View:** WMB_AUTH_SESSION-V01
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Doanh nghiệp; production permission chưa có contract.
- **Rule:** WMB_AUTH_SESSION-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** Form email/password, loading/error UI, gọi dangNhapDN.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** WIRED, `lib/views/dang_nhap/dang_nhap.dart`.

## WMB_AUTH_SESSION-TC01 — DangNhap verification case

- **Covers:** WMB_AUTH_SESSION-FN01 và WMB_AUTH_SESSION-V01.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## WMB_AUTH_SESSION-FN02 — Menu interaction

- **View:** WMB_AUTH_SESSION-V02
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Doanh nghiệp; production permission chưa có contract.
- **Rule:** WMB_AUTH_SESSION-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** Animated shell cho home, chat, candidates, settings.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** WIRED, `lib/views/dang_nhap/menu.dart`.

## WMB_AUTH_SESSION-TC02 — Menu verification case

- **Covers:** WMB_AUTH_SESSION-FN02 và WMB_AUTH_SESSION-V02.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## WMB_AUTH_SESSION-FN03 — QuenMatKhau interaction

- **View:** WMB_AUTH_SESSION-V03
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Doanh nghiệp; production permission chưa có contract.
- **Rule:** WMB_AUTH_SESSION-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** Password-recovery shell; chưa có reset helper/API.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** UI-ONLY, `lib/views/dang_nhap/quen_mat_khau.dart`.

## WMB_AUTH_SESSION-TC03 — QuenMatKhau verification case

- **Covers:** WMB_AUTH_SESSION-FN03 và WMB_AUTH_SESSION-V03.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## WMB_AUTH_SESSION-FN04 — Setting interaction

- **View:** WMB_AUTH_SESSION-V04
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Doanh nghiệp; production permission chưa có contract.
- **Rule:** WMB_AUTH_SESSION-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** Thông báo và logout bằng cách xóa cache doanh nghiệp.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** WIRED, `lib/views/cai_dat/setting.dart`.

## WMB_AUTH_SESSION-TC04 — Setting verification case

- **Covers:** WMB_AUTH_SESSION-FN04 và WMB_AUTH_SESSION-V04.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## Test matrix

| Test ID | View | Scenario | Result |
|---|---|---|---|
| WMB_AUTH_SESSION-TC01 | WMB_AUTH_SESSION-V01 | DangNhap happy/error/empty state phù hợp | Runtime-unverified |
| WMB_AUTH_SESSION-TC02 | WMB_AUTH_SESSION-V02 | Menu happy/error/empty state phù hợp | Runtime-unverified |
| WMB_AUTH_SESSION-TC03 | WMB_AUTH_SESSION-V03 | QuenMatKhau happy/error/empty state phù hợp | Runtime-unverified |
| WMB_AUTH_SESSION-TC04 | WMB_AUTH_SESSION-V04 | Setting happy/error/empty state phù hợp | Runtime-unverified |

