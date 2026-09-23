# Import/File map — WMB_REPORTING

## Source evidence

| File | Vai trò |
|---|---|
| `lib/views/trang_chu/tien_ich/Thong_ke/thong_ke_bao_cao.dart` | Source evidence for WMB_REPORTING. |
| `lib/views/trang_chu/tien_ich/Thong_ke/thong_ke.dart` | Source evidence for WMB_REPORTING. |
| `lib/views/trang_chu/main/trang_chu.dart` | Source evidence for WMB_REPORTING. |
| `pubspec.yaml` | Source evidence for WMB_REPORTING. |

## View/function mapping

| View | Function | Source |
|---|---|---|
| `EmployeeReportUI` | WMB_REPORTING-FN01 | `lib/views/trang_chu/tien_ich/Thong_ke/thong_ke_bao_cao.dart` |
| `ThongKeScreen` | WMB_REPORTING-FN02 | `lib/views/trang_chu/tien_ich/Thong_ke/thong_ke.dart` |

## Dependency direction

```text
View → controller/helper → NeonDatabase hoặc SQLite helper
View → model
View → MaterialPageRoute/local state
AI path → AIService → external Gemini chỉ khi exact source gọi
```

Không tạo Work HTTP API contract mới. Tên helper có Supabase chỉ là compatibility naming khi implementation current là Neon; không ghi credential literal.

