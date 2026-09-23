# Import/File map — WMB_JOB_MANAGEMENT

## Source evidence

| File | Vai trò |
|---|---|
| `lib/views/trang_chu/main/dang_tin_tuyen_dung.dart` | Source evidence for WMB_JOB_MANAGEMENT. |
| `lib/views/trang_chu/tien_ich/Quan_ly_job/quan_ly_job.dart` | Source evidence for WMB_JOB_MANAGEMENT. |
| `lib/views/trang_chu/tien_ich/Quan_ly_job/chi_tiet_job.dart` | Source evidence for WMB_JOB_MANAGEMENT. |
| `lib/controllers/trang_chu/quan_ly_job/quan_ly_job_ctrl.dart` | Source evidence for WMB_JOB_MANAGEMENT. |
| `lib/helper_db/helper_supabase.dart` | Source evidence for WMB_JOB_MANAGEMENT. |
| `lib/models/jd.dart` | Source evidence for WMB_JOB_MANAGEMENT. |

## View/function mapping

| View | Function | Source |
|---|---|---|
| `DangTinTuyenDung` | WMB_JOB_MANAGEMENT-FN01 | `lib/views/trang_chu/main/dang_tin_tuyen_dung.dart` |
| `QuanLyJob` | WMB_JOB_MANAGEMENT-FN02 | `lib/views/trang_chu/tien_ich/Quan_ly_job/quan_ly_job.dart` |
| `XemChiTietJD` | WMB_JOB_MANAGEMENT-FN03 | `lib/views/trang_chu/tien_ich/Quan_ly_job/chi_tiet_job.dart` |

## Dependency direction

```text
View → controller/helper → NeonDatabase hoặc SQLite helper
View → model
View → MaterialPageRoute/local state
AI path → AIService → external Gemini chỉ khi exact source gọi
```

Không tạo Work HTTP API contract mới. Tên helper có Supabase chỉ là compatibility naming khi implementation current là Neon; không ghi credential literal.

