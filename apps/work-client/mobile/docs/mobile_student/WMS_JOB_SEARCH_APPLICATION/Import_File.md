# Import/File map — WMS_JOB_SEARCH_APPLICATION

## Source evidence

| File | Vai trò |
|---|---|
| `lib/views/tim_kiem_cong_viec/tim_kiem_job.dart` | Source evidence for WMS_JOB_SEARCH_APPLICATION. |
| `lib/views/trang_chu/main/xem_chi_tiet_view.dart` | Source evidence for WMS_JOB_SEARCH_APPLICATION. |
| `lib/views/trang_chu/main/dang_tin_tuyen_dung.dart` | Source evidence for WMS_JOB_SEARCH_APPLICATION. |
| `lib/controllers/tim_kiem_job/tim_kiem_ctrl.dart` | Source evidence for WMS_JOB_SEARCH_APPLICATION. |
| `lib/controllers/ung_tuyen_ctrl.dart` | Source evidence for WMS_JOB_SEARCH_APPLICATION. |
| `lib/helper_db/sinh_vien/helper_supabase.dart` | Source evidence for WMS_JOB_SEARCH_APPLICATION. |
| `lib/models/sinh_vien/jd.dart` | Source evidence for WMS_JOB_SEARCH_APPLICATION. |
| `lib/models/sinh_vien/ung_vien.dart` | Source evidence for WMS_JOB_SEARCH_APPLICATION. |

## View/function mapping

| View | Function | Source |
|---|---|---|
| `TimKiemViecView` | WMS_JOB_SEARCH_APPLICATION-FN01 | `lib/views/tim_kiem_cong_viec/tim_kiem_job.dart` |
| `XemChiTietView` | WMS_JOB_SEARCH_APPLICATION-FN02 | `lib/views/trang_chu/main/xem_chi_tiet_view.dart` |
| `DangTinTuyenDung` | WMS_JOB_SEARCH_APPLICATION-FN03 | `lib/views/trang_chu/main/dang_tin_tuyen_dung.dart` |

## Dependency direction

```text
View → controller/helper → NeonDatabase hoặc SQLite helper
View → model
View → MaterialPageRoute/local state
AI path → AIService → external Gemini chỉ khi exact source gọi
```

Không tạo Work HTTP API contract mới. Tên helper có Supabase chỉ là compatibility naming khi implementation current là Neon; không ghi credential literal.

