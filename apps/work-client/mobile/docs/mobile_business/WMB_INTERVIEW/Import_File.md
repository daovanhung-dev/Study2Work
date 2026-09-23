# Import/File map — WMB_INTERVIEW

## Source evidence

| File | Vai trò |
|---|---|
| `lib/views/trang_chu/tien_ich/Lich_phong_van/lich_pv_page.dart` | Source evidence for WMB_INTERVIEW. |
| `lib/views/trang_chu/tien_ich/Lich_phong_van/lich_phong_van.dart` | Source evidence for WMB_INTERVIEW. |
| `lib/views/trang_chu/main/trang_chu.dart` | Source evidence for WMB_INTERVIEW. |

## View/function mapping

| View | Function | Source |
|---|---|---|
| `LichPV` | WMB_INTERVIEW-FN01 | `lib/views/trang_chu/tien_ich/Lich_phong_van/lich_pv_page.dart` |
| `LichPhongVanScreen` | WMB_INTERVIEW-FN02 | `lib/views/trang_chu/tien_ich/Lich_phong_van/lich_phong_van.dart` |

## Dependency direction

```text
View → controller/helper → NeonDatabase hoặc SQLite helper
View → model
View → MaterialPageRoute/local state
AI path → AIService → external Gemini chỉ khi exact source gọi
```

Không tạo Work HTTP API contract mới. Tên helper có Supabase chỉ là compatibility naming khi implementation current là Neon; không ghi credential literal.

