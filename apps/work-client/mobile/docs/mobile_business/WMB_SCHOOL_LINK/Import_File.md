# Import/File map — WMB_SCHOOL_LINK

## Source evidence

| File | Vai trò |
|---|---|
| `lib/views/trang_chu/tien_ich/Lien_ket_nha_truong/lien_ket_nha_truong.dart` | Source evidence for WMB_SCHOOL_LINK. |
| `lib/views/trang_chu/main/trang_chu.dart` | Source evidence for WMB_SCHOOL_LINK. |

## View/function mapping

| View | Function | Source |
|---|---|---|
| `LienKetScreen` | WMB_SCHOOL_LINK-FN01 | `lib/views/trang_chu/tien_ich/Lien_ket_nha_truong/lien_ket_nha_truong.dart` |

## Dependency direction

```text
View → controller/helper → NeonDatabase hoặc SQLite helper
View → model
View → MaterialPageRoute/local state
AI path → AIService → external Gemini chỉ khi exact source gọi
```

Không tạo Work HTTP API contract mới. Tên helper có Supabase chỉ là compatibility naming khi implementation current là Neon; không ghi credential literal.

