# Import/File map — WMS_CV_MANAGEMENT

## Source evidence

| File | Vai trò |
|---|---|
| `lib/views/trang_chu/tien_ich/Quan_ly_CV/quan_ly_cv.dart` | Source evidence for WMS_CV_MANAGEMENT. |
| `lib/controllers/trang_chu/quan_ly_CV/quan_ly_job_cv.dart` | Source evidence for WMS_CV_MANAGEMENT. |
| `lib/helper_db/sinh_vien/helper_supabase.dart` | Source evidence for WMS_CV_MANAGEMENT. |
| `lib/helper_db/sinh_vien/helper_cv.dart` | Source evidence for WMS_CV_MANAGEMENT. |
| `lib/models/sinh_vien/cv.dart` | Source evidence for WMS_CV_MANAGEMENT. |

## View/function mapping

| View | Function | Source |
|---|---|---|
| `QuanLyCVView` | WMS_CV_MANAGEMENT-FN01 | `lib/views/trang_chu/tien_ich/Quan_ly_CV/quan_ly_cv.dart` |

## Dependency direction

```text
View → controller/helper → NeonDatabase hoặc SQLite helper
View → model
View → MaterialPageRoute/local state
AI path → AIService → external Gemini chỉ khi exact source gọi
```

Không tạo Work HTTP API contract mới. Tên helper có Supabase chỉ là compatibility naming khi implementation current là Neon; không ghi credential literal.

