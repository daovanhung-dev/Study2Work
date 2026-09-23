# View inventory — WMB_CONNECTIVITY

Mỗi view được ghi đúng một lần; status phản ánh current source, không phải business approval.

| View ID | Widget | Source file | Status | Current behavior |
|---|---|---|---|---|
| WMB_CONNECTIVITY-V01 | `KiemTraWifiView` | `lib/views/kiem_tra_wifi.dart` | UNWIRED | Connectivity listener/check với retry/exit; không reached từ current main route. |

## WMB_CONNECTIVITY-V01 — KiemTraWifiView

- **Source:** `lib/views/kiem_tra_wifi.dart`
- **Status:** UNWIRED
- **Function:** WMB_CONNECTIVITY-FN01
- **Current behavior:** Connectivity listener/check với retry/exit; không reached từ current main route.
- **UI states:** ghi loading/empty/error/success hoặc static theo exact widget tree; không suy ra state mới.
- **Navigation/side effect:** xem function tương ứng trong [Function_List.md](Function_List.md).

