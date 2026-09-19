# View inventory — WMB_INTERNSHIP

Mỗi view được ghi đúng một lần; status phản ánh current source, không phải business approval.

| View ID | Widget | Source file | Status | Current behavior |
|---|---|---|---|---|
| WMB_INTERNSHIP-V01 | `ChuongTrinhThucTapPage` | `lib/views/trang_chu/tien_ich/Chuong_trinh_thuc_te/chuong_trinh_thuc_tap_page.dart` | WIRED | Listing page và form entry. |
| WMB_INTERNSHIP-V02 | `ThucTapScreen` | `lib/views/trang_chu/tien_ich/Chuong_trinh_thuc_te/chuong_trinh_thuc_tap.dart` | LEGACY | Legacy internship screen ngoài active route. Form component được ghi trong WMB_INTERNSHIP-V01. |

## WMB_INTERNSHIP-V01 — ChuongTrinhThucTapPage

- **Source:** `lib/views/trang_chu/tien_ich/Chuong_trinh_thuc_te/chuong_trinh_thuc_tap_page.dart`
- **Status:** WIRED
- **Function:** WMB_INTERNSHIP-FN01
- **Current behavior:** Listing page và form entry.
- **UI states:** ghi loading/empty/error/success hoặc static theo exact widget tree; không suy ra state mới.
- **Navigation/side effect:** xem function tương ứng trong [Function_List.md](Function_List.md).

## WMB_INTERNSHIP-V02 — ThucTapScreen

- **Source:** `lib/views/trang_chu/tien_ich/Chuong_trinh_thuc_te/chuong_trinh_thuc_tap.dart`
- **Status:** LEGACY
- **Function:** WMB_INTERNSHIP-FN02
- **Current behavior:** Legacy internship screen ngoài active route.
- **UI states:** ghi loading/empty/error/success hoặc static theo exact widget tree; không suy ra state mới.
- **Navigation/side effect:** xem function tương ứng trong [Function_List.md](Function_List.md).
