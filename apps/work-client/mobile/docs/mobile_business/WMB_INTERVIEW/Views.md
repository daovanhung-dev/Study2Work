# View inventory — WMB_INTERVIEW

Mỗi view được ghi đúng một lần; status phản ánh current source, không phải business approval.

| View ID | Widget | Source file | Status | Current behavior |
|---|---|---|---|---|
| WMB_INTERVIEW-V01 | `LichPV` | `lib/views/trang_chu/tien_ich/Lich_phong_van/lich_pv_page.dart` | WIRED | Active interview schedule/form/dialog local state. |
| WMB_INTERVIEW-V02 | `LichPhongVanScreen` | `lib/views/trang_chu/tien_ich/Lich_phong_van/lich_phong_van.dart` | LEGACY | Legacy interview screen ngoài active route. |

## WMB_INTERVIEW-V01 — LichPV

- **Source:** `lib/views/trang_chu/tien_ich/Lich_phong_van/lich_pv_page.dart`
- **Status:** WIRED
- **Function:** WMB_INTERVIEW-FN01
- **Current behavior:** Active interview schedule/form/dialog local state.
- **UI states:** ghi loading/empty/error/success hoặc static theo exact widget tree; không suy ra state mới.
- **Navigation/side effect:** xem function tương ứng trong [Function_List.md](Function_List.md).

## WMB_INTERVIEW-V02 — LichPhongVanScreen

- **Source:** `lib/views/trang_chu/tien_ich/Lich_phong_van/lich_phong_van.dart`
- **Status:** LEGACY
- **Function:** WMB_INTERVIEW-FN02
- **Current behavior:** Legacy interview screen ngoài active route.
- **UI states:** ghi loading/empty/error/success hoặc static theo exact widget tree; không suy ra state mới.
- **Navigation/side effect:** xem function tương ứng trong [Function_List.md](Function_List.md).

