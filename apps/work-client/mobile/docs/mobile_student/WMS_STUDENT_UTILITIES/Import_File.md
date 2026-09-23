# Import/File map — WMS_STUDENT_UTILITIES

## Source evidence

| File | Vai trò |
|---|---|
| `lib/views/trang_chu/tien_ich/Lich_PV/lich_pv.dart` | Source evidence for WMS_STUDENT_UTILITIES. |
| `lib/views/trang_chu/tien_ich/Hotro_SV/ho_tro_sv.dart` | Source evidence for WMS_STUDENT_UTILITIES. |
| `lib/views/trang_chu/tien_ich/Khoa_hoc/khoa_hoc.dart` | Source evidence for WMS_STUDENT_UTILITIES. |
| `lib/views/trang_chu/tien_ich/Tin_Tuc/tin_tuc.dart` | Source evidence for WMS_STUDENT_UTILITIES. |
| `lib/views/trang_chu/main/trang_chu.dart` | Source evidence for WMS_STUDENT_UTILITIES. |

## View/function mapping

| View | Function | Source |
|---|---|---|
| `LichPhongVanView` | WMS_STUDENT_UTILITIES-FN01 | `lib/views/trang_chu/tien_ich/Lich_PV/lich_pv.dart` |
| `HoTroSinhVienView` | WMS_STUDENT_UTILITIES-FN02 | `lib/views/trang_chu/tien_ich/Hotro_SV/ho_tro_sv.dart` |
| `KhoaHocView` | WMS_STUDENT_UTILITIES-FN03 | `lib/views/trang_chu/tien_ich/Khoa_hoc/khoa_hoc.dart` |
| `TinTucView` | WMS_STUDENT_UTILITIES-FN04 | `lib/views/trang_chu/tien_ich/Tin_Tuc/tin_tuc.dart` |

## Dependency direction

```text
View → controller/helper → NeonDatabase hoặc SQLite helper
View → model
View → MaterialPageRoute/local state
AI path → AIService → external Gemini chỉ khi exact source gọi
```

Không tạo Work HTTP API contract mới. Tên helper có Supabase chỉ là compatibility naming khi implementation current là Neon; không ghi credential literal.

