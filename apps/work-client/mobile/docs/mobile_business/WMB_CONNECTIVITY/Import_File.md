# Import/File map — WMB_CONNECTIVITY

## Source evidence

| File | Vai trò |
|---|---|
| `lib/views/kiem_tra_wifi.dart` | Source evidence for WMB_CONNECTIVITY. |
| `lib/views/dang_nhap/dang_nhap.dart` | Source evidence for WMB_CONNECTIVITY. |
| `lib/main.dart` | Source evidence for WMB_CONNECTIVITY. |

## View/function mapping

| View | Function | Source |
|---|---|---|
| `KiemTraWifiView` | WMB_CONNECTIVITY-FN01 | `lib/views/kiem_tra_wifi.dart` |

## Dependency direction

```text
View → controller/helper → NeonDatabase hoặc SQLite helper
View → model
View → MaterialPageRoute/local state
AI path → AIService → external Gemini chỉ khi exact source gọi
```

Không tạo Work HTTP API contract mới. Tên helper có Supabase chỉ là compatibility naming khi implementation current là Neon; không ghi credential literal.

