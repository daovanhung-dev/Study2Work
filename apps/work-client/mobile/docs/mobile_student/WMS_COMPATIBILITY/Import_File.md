# Import/File map — WMS_COMPATIBILITY

## Source evidence

| File | Vai trò |
|---|---|
| `lib/views/trang_chu/tien_ich/Tim_kiem_nhan_su/tim_kiem_nhan_su.dart` | Source evidence for WMS_COMPATIBILITY. |
| `lib/controllers/trang_chu/timkiemctrl.dart` | Source evidence for WMS_COMPATIBILITY. |
| `lib/controllers/AI/ai_service.dart` | Source evidence for WMS_COMPATIBILITY. |
| `lib/helper_db/out_meta/helper_cv.dart` | Source evidence for WMS_COMPATIBILITY. |
| `lib/models/outmeta/cv.dart` | Source evidence for WMS_COMPATIBILITY. |

## View/function mapping

| View | Function | Source |
|---|---|---|
| `EmployeeSearchUI` | WMS_COMPATIBILITY-FN01 | `lib/views/trang_chu/tien_ich/Tim_kiem_nhan_su/tim_kiem_nhan_su.dart` |

## Dependency direction

```text
View → controller/helper → NeonDatabase hoặc SQLite helper
View → model
View → MaterialPageRoute/local state
AI path → AIService → external Gemini chỉ khi exact source gọi
```

Không tạo Work HTTP API contract mới. Tên helper có Supabase chỉ là compatibility naming khi implementation current là Neon; không ghi credential literal.

