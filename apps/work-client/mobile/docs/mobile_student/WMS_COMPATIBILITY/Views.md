# View inventory — WMS_COMPATIBILITY

Mỗi view được ghi đúng một lần; status phản ánh current source, không phải business approval.

| View ID | Widget | Source file | Status | Current behavior |
|---|---|---|---|---|
| WMS_COMPATIBILITY-V01 | `EmployeeSearchUI` | `lib/views/trang_chu/tien_ich/Tim_kiem_nhan_su/tim_kiem_nhan_su.dart` | UNWIRED/LEGACY | Candidate/CV search surface dùng out-meta helper và AI prompt; không clear active route. |

## WMS_COMPATIBILITY-V01 — EmployeeSearchUI

- **Source:** `lib/views/trang_chu/tien_ich/Tim_kiem_nhan_su/tim_kiem_nhan_su.dart`
- **Status:** UNWIRED/LEGACY
- **Function:** WMS_COMPATIBILITY-FN01
- **Current behavior:** Candidate/CV search surface dùng out-meta helper và AI prompt; không clear active route.
- **UI states:** ghi loading/empty/error/success hoặc static theo exact widget tree; không suy ra state mới.
- **Navigation/side effect:** xem function tương ứng trong [Function_List.md](Function_List.md).

