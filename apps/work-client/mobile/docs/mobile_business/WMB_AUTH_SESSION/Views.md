# View inventory — WMB_AUTH_SESSION

Mỗi view được ghi đúng một lần; status phản ánh current source, không phải business approval.

| View ID | Widget | Source file | Status | Current behavior |
|---|---|---|---|---|
| WMB_AUTH_SESSION-V01 | `DangNhap` | `lib/views/dang_nhap/dang_nhap.dart` | WIRED | Form email/password, loading/error UI, gọi dangNhapDN. |
| WMB_AUTH_SESSION-V02 | `Menu` | `lib/views/dang_nhap/menu.dart` | WIRED | Animated shell cho home, chat, candidates, settings. |
| WMB_AUTH_SESSION-V03 | `QuenMatKhau` | `lib/views/dang_nhap/quen_mat_khau.dart` | UI-ONLY | Password-recovery shell; chưa có reset helper/API. |
| WMB_AUTH_SESSION-V04 | `Setting` | `lib/views/cai_dat/setting.dart` | WIRED | Thông báo và logout bằng cách xóa cache doanh nghiệp. |

## WMB_AUTH_SESSION-V01 — DangNhap

- **Source:** `lib/views/dang_nhap/dang_nhap.dart`
- **Status:** WIRED
- **Function:** WMB_AUTH_SESSION-FN01
- **Current behavior:** Form email/password, loading/error UI, gọi dangNhapDN.
- **UI states:** ghi loading/empty/error/success hoặc static theo exact widget tree; không suy ra state mới.
- **Navigation/side effect:** xem function tương ứng trong [Function_List.md](Function_List.md).

## WMB_AUTH_SESSION-V02 — Menu

- **Source:** `lib/views/dang_nhap/menu.dart`
- **Status:** WIRED
- **Function:** WMB_AUTH_SESSION-FN02
- **Current behavior:** Animated shell cho home, chat, candidates, settings.
- **UI states:** ghi loading/empty/error/success hoặc static theo exact widget tree; không suy ra state mới.
- **Navigation/side effect:** xem function tương ứng trong [Function_List.md](Function_List.md).

## WMB_AUTH_SESSION-V03 — QuenMatKhau

- **Source:** `lib/views/dang_nhap/quen_mat_khau.dart`
- **Status:** UI-ONLY
- **Function:** WMB_AUTH_SESSION-FN03
- **Current behavior:** Password-recovery shell; chưa có reset helper/API.
- **UI states:** ghi loading/empty/error/success hoặc static theo exact widget tree; không suy ra state mới.
- **Navigation/side effect:** xem function tương ứng trong [Function_List.md](Function_List.md).

## WMB_AUTH_SESSION-V04 — Setting

- **Source:** `lib/views/cai_dat/setting.dart`
- **Status:** WIRED
- **Function:** WMB_AUTH_SESSION-FN04
- **Current behavior:** Thông báo và logout bằng cách xóa cache doanh nghiệp.
- **UI states:** ghi loading/empty/error/success hoặc static theo exact widget tree; không suy ra state mới.
- **Navigation/side effect:** xem function tương ứng trong [Function_List.md](Function_List.md).

