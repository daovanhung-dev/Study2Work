# Import/File map — WMB_CANDIDATE_MANAGEMENT

## Source evidence

| File | Vai trò |
|---|---|
| `lib/views/ung_vien/ung_vien.dart` | Source evidence for WMB_CANDIDATE_MANAGEMENT. |
| `lib/views/trang_chu/tien_ich/Tim_kiem_nhan_su/tim_kiem_nhan_su.dart` | Source evidence for WMB_CANDIDATE_MANAGEMENT. |
| `lib/views/trang_chu/tien_ich/Loc_cv/loc_cv_filter.dart` | Source evidence for WMB_CANDIDATE_MANAGEMENT. |
| `lib/views/trang_chu/tien_ich/Loc_cv/loc_cv_placeholder.dart` | Source evidence for WMB_CANDIDATE_MANAGEMENT. |
| `lib/controllers/ung_vien/ung_vien_controller.dart` | Source evidence for WMB_CANDIDATE_MANAGEMENT. |
| `lib/controllers/trang_chu/timkiemctrl.dart` | Source evidence for WMB_CANDIDATE_MANAGEMENT. |
| `lib/controllers/AI/ai_service.dart` | Source evidence for WMB_CANDIDATE_MANAGEMENT. |
| `lib/helper_db/helper_cv.dart` | Source evidence for WMB_CANDIDATE_MANAGEMENT. |
| `lib/models/cv.dart` | Source evidence for WMB_CANDIDATE_MANAGEMENT. |
| `lib/models/ung_vien.dart` | Source evidence for WMB_CANDIDATE_MANAGEMENT. |

## View/function mapping

| View | Function | Source |
|---|---|---|
| `UngVien` | WMB_CANDIDATE_MANAGEMENT-FN01 | `lib/views/ung_vien/ung_vien.dart` |
| `EmployeeSearchUI` | WMB_CANDIDATE_MANAGEMENT-FN02 | `lib/views/trang_chu/tien_ich/Tim_kiem_nhan_su/tim_kiem_nhan_su.dart` |
| `LocCV` | WMB_CANDIDATE_MANAGEMENT-FN03 | `lib/views/trang_chu/tien_ich/Loc_cv/loc_cv_filter.dart` |
| `LocCvPlaceholderScreen` | WMB_CANDIDATE_MANAGEMENT-FN04 | `lib/views/trang_chu/tien_ich/Loc_cv/loc_cv_placeholder.dart` |

## Dependency direction

```text
View → controller/helper → NeonDatabase hoặc SQLite helper
View → model
View → MaterialPageRoute/local state
AI path → AIService → external Gemini chỉ khi exact source gọi
```

Không tạo Work HTTP API contract mới. Tên helper có Supabase chỉ là compatibility naming khi implementation current là Neon; không ghi credential literal.

