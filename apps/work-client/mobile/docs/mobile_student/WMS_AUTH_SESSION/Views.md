# View inventory — WMS_AUTH_SESSION

Mỗi view được ghi đúng một lần; status phản ánh current source, không phải business approval.

| View ID | Widget | Source file | Status | Current behavior |
|---|---|---|---|---|
| WMS_AUTH_SESSION-V01 | `DangNhap` | `lib/views/dang_nhap/dang_nhap.dart` | WIRED | Email/password form, loading/error UI và mở Menu sau login. |
| WMS_AUTH_SESSION-V02 | `Menu` | `lib/views/dang_nhap/menu.dart` | WIRED | Animated shell cho home/search/chat/settings. |
| WMS_AUTH_SESSION-V03 | `QuenMatKhauView` | `lib/views/dang_nhap/quen_mat_khau.dart` | UI-ONLY | Password-recovery form; chưa có reset API/helper. |
| WMS_AUTH_SESSION-V04 | `Setting` | `lib/views/cai_dat/setting.dart` | WIRED | Thông báo và logout rồi replace về login. |

## WMS_AUTH_SESSION-V01 — DangNhap

- **Source:** `lib/views/dang_nhap/dang_nhap.dart`
- **Status:** WIRED
- **Function:** WMS_AUTH_SESSION-FN01
- **Current behavior:** Email/password form, loading/error UI và mở Menu sau login.
- **UI states:** ghi loading/empty/error/success hoặc static theo exact widget tree; không suy ra state mới.
- **Navigation/side effect:** xem function tương ứng trong [Function_List.md](Function_List.md).

## WMS_AUTH_SESSION-V02 — Menu

- **Source:** `lib/views/dang_nhap/menu.dart`
- **Status:** WIRED
- **Function:** WMS_AUTH_SESSION-FN02
- **Current behavior:** Animated shell cho home/search/chat/settings.
- **UI states:** ghi loading/empty/error/success hoặc static theo exact widget tree; không suy ra state mới.
- **Navigation/side effect:** xem function tương ứng trong [Function_List.md](Function_List.md).

## WMS_AUTH_SESSION-V03 — QuenMatKhauView

- **Source:** `lib/views/dang_nhap/quen_mat_khau.dart`
- **Status:** UI-ONLY
- **Function:** WMS_AUTH_SESSION-FN03
- **Current behavior:** Password-recovery form; chưa có reset API/helper.
- **UI states:** ghi loading/empty/error/success hoặc static theo exact widget tree; không suy ra state mới.
- **Navigation/side effect:** xem function tương ứng trong [Function_List.md](Function_List.md).

## WMS_AUTH_SESSION-V04 — Setting

- **Source:** `lib/views/cai_dat/setting.dart`
- **Status:** WIRED
- **Function:** WMS_AUTH_SESSION-FN04
- **Current behavior:** Thông báo và logout rồi replace về login.
- **UI states:** ghi loading/empty/error/success hoặc static theo exact widget tree; không suy ra state mới.
- **Navigation/side effect:** xem function tương ứng trong [Function_List.md](Function_List.md).

