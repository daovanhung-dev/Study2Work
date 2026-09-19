# Import/File map — WMB_INTERNSHIP

## Source evidence

| File | Vai trò |
|---|---|
| `lib/views/trang_chu/tien_ich/Chuong_trinh_thuc_te/chuong_trinh_thuc_tap_page.dart` | Source evidence for WMB_INTERNSHIP. |
| `lib/views/trang_chu/tien_ich/Chuong_trinh_thuc_te/chuong_trinh_thuc_tap.dart` | Source evidence for WMB_INTERNSHIP. |
| `lib/views/trang_chu/main/trang_chu.dart` | Source evidence for WMB_INTERNSHIP. |

## View/function mapping

| View | Function | Source |
|---|---|---|
| `ChuongTrinhThucTapPage` | WMB_INTERNSHIP-FN01 | `lib/views/trang_chu/tien_ich/Chuong_trinh_thuc_te/chuong_trinh_thuc_tap_page.dart` |
| `ChuongTrinhThucTapPage` (embedded `ChuongTrinhThucTapForm`) | WMB_INTERNSHIP-FN01 | `lib/views/trang_chu/tien_ich/Chuong_trinh_thuc_te/chuong_trinh_thuc_tap_page.dart` |
| `ThucTapScreen` | WMB_INTERNSHIP-FN02 | `lib/views/trang_chu/tien_ich/Chuong_trinh_thuc_te/chuong_trinh_thuc_tap.dart` |

## Dependency direction

```text
View → controller/helper → NeonDatabase hoặc SQLite helper
View → model
View → MaterialPageRoute/local state
AI path → AIService → external Gemini chỉ khi exact source gọi
```

Không tạo Work HTTP API contract mới. Tên helper có Supabase chỉ là compatibility naming khi implementation current là Neon; không ghi credential literal.
