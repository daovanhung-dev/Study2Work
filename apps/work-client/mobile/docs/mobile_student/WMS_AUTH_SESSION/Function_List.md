# Function list — WMS_AUTH_SESSION

## WMS_AUTH_SESSION-FN01 — DangNhap interaction

- **View:** WMS_AUTH_SESSION-V01
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Sinh viên; production permission chưa có contract.
- **Rule:** WMS_AUTH_SESSION-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** Email/password form, loading/error UI và mở Menu sau login.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** WIRED, `lib/views/dang_nhap/dang_nhap.dart`.

## WMS_AUTH_SESSION-TC01 — DangNhap verification case

- **Covers:** WMS_AUTH_SESSION-FN01 và WMS_AUTH_SESSION-V01.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## WMS_AUTH_SESSION-FN02 — Menu interaction

- **View:** WMS_AUTH_SESSION-V02
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Sinh viên; production permission chưa có contract.
- **Rule:** WMS_AUTH_SESSION-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** Animated shell cho home/search/chat/settings.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** WIRED, `lib/views/dang_nhap/menu.dart`.

## WMS_AUTH_SESSION-TC02 — Menu verification case

- **Covers:** WMS_AUTH_SESSION-FN02 và WMS_AUTH_SESSION-V02.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## WMS_AUTH_SESSION-FN03 — QuenMatKhauView interaction

- **View:** WMS_AUTH_SESSION-V03
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Sinh viên; production permission chưa có contract.
- **Rule:** WMS_AUTH_SESSION-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** Password-recovery form; chưa có reset API/helper.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** UI-ONLY, `lib/views/dang_nhap/quen_mat_khau.dart`.

## WMS_AUTH_SESSION-TC03 — QuenMatKhauView verification case

- **Covers:** WMS_AUTH_SESSION-FN03 và WMS_AUTH_SESSION-V03.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## WMS_AUTH_SESSION-FN04 — Setting interaction

- **View:** WMS_AUTH_SESSION-V04
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Sinh viên; production permission chưa có contract.
- **Rule:** WMS_AUTH_SESSION-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** Thông báo và logout rồi replace về login.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** WIRED, `lib/views/cai_dat/setting.dart`.

## WMS_AUTH_SESSION-TC04 — Setting verification case

- **Covers:** WMS_AUTH_SESSION-FN04 và WMS_AUTH_SESSION-V04.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## Test matrix

| Test ID | View | Scenario | Result |
|---|---|---|---|
| WMS_AUTH_SESSION-TC01 | WMS_AUTH_SESSION-V01 | DangNhap happy/error/empty state phù hợp | Runtime-unverified |
| WMS_AUTH_SESSION-TC02 | WMS_AUTH_SESSION-V02 | Menu happy/error/empty state phù hợp | Runtime-unverified |
| WMS_AUTH_SESSION-TC03 | WMS_AUTH_SESSION-V03 | QuenMatKhauView happy/error/empty state phù hợp | Runtime-unverified |
| WMS_AUTH_SESSION-TC04 | WMS_AUTH_SESSION-V04 | Setting happy/error/empty state phù hợp | Runtime-unverified |

