# View inventory — WMB_CANDIDATE_MANAGEMENT

Mỗi view được ghi đúng một lần; status phản ánh current source, không phải business approval.

| View ID | Widget | Source file | Status | Current behavior |
|---|---|---|---|---|
| WMB_CANDIDATE_MANAGEMENT-V01 | `UngVien` | `lib/views/ung_vien/ung_vien.dart` | WIRED | Candidate/application list, status actions, candidate detail. |
| WMB_CANDIDATE_MANAGEMENT-V02 | `EmployeeSearchUI` | `lib/views/trang_chu/tien_ich/Tim_kiem_nhan_su/tim_kiem_nhan_su.dart` | WIRED | Candidate search dùng CV helper và AI prompt helper. |
| WMB_CANDIDATE_MANAGEMENT-V03 | `LocCV` | `lib/views/trang_chu/tien_ich/Loc_cv/loc_cv_filter.dart` | SOURCE-ONLY | Local project/job/skill filter; chưa remote persistence. |
| WMB_CANDIDATE_MANAGEMENT-V04 | `LocCvPlaceholderScreen` | `lib/views/trang_chu/tien_ich/Loc_cv/loc_cv_placeholder.dart` | PLACEHOLDER | Placeholder retained ngoài active route. |

## WMB_CANDIDATE_MANAGEMENT-V01 — UngVien

- **Source:** `lib/views/ung_vien/ung_vien.dart`
- **Status:** WIRED
- **Function:** WMB_CANDIDATE_MANAGEMENT-FN01
- **Current behavior:** Candidate/application list, status actions, candidate detail.
- **UI states:** ghi loading/empty/error/success hoặc static theo exact widget tree; không suy ra state mới.
- **Navigation/side effect:** xem function tương ứng trong [Function_List.md](Function_List.md).

## WMB_CANDIDATE_MANAGEMENT-V02 — EmployeeSearchUI

- **Source:** `lib/views/trang_chu/tien_ich/Tim_kiem_nhan_su/tim_kiem_nhan_su.dart`
- **Status:** WIRED
- **Function:** WMB_CANDIDATE_MANAGEMENT-FN02
- **Current behavior:** Candidate search dùng CV helper và AI prompt helper.
- **UI states:** ghi loading/empty/error/success hoặc static theo exact widget tree; không suy ra state mới.
- **Navigation/side effect:** xem function tương ứng trong [Function_List.md](Function_List.md).

## WMB_CANDIDATE_MANAGEMENT-V03 — LocCV

- **Source:** `lib/views/trang_chu/tien_ich/Loc_cv/loc_cv_filter.dart`
- **Status:** SOURCE-ONLY
- **Function:** WMB_CANDIDATE_MANAGEMENT-FN03
- **Current behavior:** Local project/job/skill filter; chưa remote persistence.
- **UI states:** ghi loading/empty/error/success hoặc static theo exact widget tree; không suy ra state mới.
- **Navigation/side effect:** xem function tương ứng trong [Function_List.md](Function_List.md).

## WMB_CANDIDATE_MANAGEMENT-V04 — LocCvPlaceholderScreen

- **Source:** `lib/views/trang_chu/tien_ich/Loc_cv/loc_cv_placeholder.dart`
- **Status:** PLACEHOLDER
- **Function:** WMB_CANDIDATE_MANAGEMENT-FN04
- **Current behavior:** Placeholder retained ngoài active route.
- **UI states:** ghi loading/empty/error/success hoặc static theo exact widget tree; không suy ra state mới.
- **Navigation/side effect:** xem function tương ứng trong [Function_List.md](Function_List.md).

