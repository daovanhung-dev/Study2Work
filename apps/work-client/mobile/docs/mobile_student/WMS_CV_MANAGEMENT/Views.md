# View inventory — WMS_CV_MANAGEMENT

Mỗi view được ghi đúng một lần; status phản ánh current source, không phải business approval.

| View ID | Widget | Source file | Status | Current behavior |
|---|---|---|---|---|
| WMS_CV_MANAGEMENT-V01 | `QuanLyCVView` | `lib/views/trang_chu/tien_ich/Quan_ly_CV/quan_ly_cv.dart` | WIRED | CV load/edit form qua CVCtrl. |

## WMS_CV_MANAGEMENT-V01 — QuanLyCVView

- **Source:** `lib/views/trang_chu/tien_ich/Quan_ly_CV/quan_ly_cv.dart`
- **Status:** WIRED
- **Function:** WMS_CV_MANAGEMENT-FN01
- **Current behavior:** CV load/edit form qua CVCtrl.
- **UI states:** ghi loading/empty/error/success hoặc static theo exact widget tree; không suy ra state mới.
- **Navigation/side effect:** xem function tương ứng trong [Function_List.md](Function_List.md).

