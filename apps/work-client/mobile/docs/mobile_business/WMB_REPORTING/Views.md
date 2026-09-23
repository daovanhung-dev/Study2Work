# View inventory — WMB_REPORTING

Mỗi view được ghi đúng một lần; status phản ánh current source, không phải business approval.

| View ID | Widget | Source file | Status | Current behavior |
|---|---|---|---|---|
| WMB_REPORTING-V01 | `EmployeeReportUI` | `lib/views/trang_chu/tien_ich/Thong_ke/thong_ke_bao_cao.dart` | WIRED | Active report UI dùng fl_chart/local presentation data. |
| WMB_REPORTING-V02 | `ThongKeScreen` | `lib/views/trang_chu/tien_ich/Thong_ke/thong_ke.dart` | LEGACY | Legacy statistics screen ngoài active report route. |

## WMB_REPORTING-V01 — EmployeeReportUI

- **Source:** `lib/views/trang_chu/tien_ich/Thong_ke/thong_ke_bao_cao.dart`
- **Status:** WIRED
- **Function:** WMB_REPORTING-FN01
- **Current behavior:** Active report UI dùng fl_chart/local presentation data.
- **UI states:** ghi loading/empty/error/success hoặc static theo exact widget tree; không suy ra state mới.
- **Navigation/side effect:** xem function tương ứng trong [Function_List.md](Function_List.md).

## WMB_REPORTING-V02 — ThongKeScreen

- **Source:** `lib/views/trang_chu/tien_ich/Thong_ke/thong_ke.dart`
- **Status:** LEGACY
- **Function:** WMB_REPORTING-FN02
- **Current behavior:** Legacy statistics screen ngoài active report route.
- **UI states:** ghi loading/empty/error/success hoặc static theo exact widget tree; không suy ra state mới.
- **Navigation/side effect:** xem function tương ứng trong [Function_List.md](Function_List.md).

