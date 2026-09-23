# Import/File map — WMB_AUTH_SESSION

## Source evidence

| File | Vai trò |
|---|---|
| `lib/main.dart` | Source evidence for WMB_AUTH_SESSION. |
| `lib/views/dang_nhap/dang_nhap.dart` | Source evidence for WMB_AUTH_SESSION. |
| `lib/views/dang_nhap/menu.dart` | Source evidence for WMB_AUTH_SESSION. |
| `lib/views/dang_nhap/quen_mat_khau.dart` | Source evidence for WMB_AUTH_SESSION. |
| `lib/views/cai_dat/setting.dart` | Source evidence for WMB_AUTH_SESSION. |
| `lib/controllers/dang_nhap/dangnhap_ctrl.dart` | Source evidence for WMB_AUTH_SESSION. |
| `lib/controllers/cai_dat/cai_dat.dart` | Source evidence for WMB_AUTH_SESSION. |
| `lib/helper_db/helper_db.dart` | Source evidence for WMB_AUTH_SESSION. |
| `lib/helper_db/helper_supabase.dart` | Source evidence for WMB_AUTH_SESSION. |

## View/function mapping

| View | Function | Source |
|---|---|---|
| `DangNhap` | WMB_AUTH_SESSION-FN01 | `lib/views/dang_nhap/dang_nhap.dart` |
| `Menu` | WMB_AUTH_SESSION-FN02 | `lib/views/dang_nhap/menu.dart` |
| `QuenMatKhau` | WMB_AUTH_SESSION-FN03 | `lib/views/dang_nhap/quen_mat_khau.dart` |
| `Setting` | WMB_AUTH_SESSION-FN04 | `lib/views/cai_dat/setting.dart` |

## Dependency direction

```text
View → controller/helper → NeonDatabase hoặc SQLite helper
View → model
View → MaterialPageRoute/local state
AI path → AIService → external Gemini chỉ khi exact source gọi
```

Không tạo Work HTTP API contract mới. Tên helper có Supabase chỉ là compatibility naming khi implementation current là Neon; không ghi credential literal.

