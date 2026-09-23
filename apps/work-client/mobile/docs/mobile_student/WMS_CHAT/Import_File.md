# Import/File map — WMS_CHAT

## Source evidence

| File | Vai trò |
|---|---|
| `lib/views/tro_chuyen/tro_chuyen.dart` | Source evidence for WMS_CHAT. |
| `lib/views/tro_chuyen/chat.dart` | Source evidence for WMS_CHAT. |
| `lib/controllers/chat/chat_controller.dart` | Source evidence for WMS_CHAT. |
| `lib/controllers/chat/nhung_doan_chat_controller.dart` | Source evidence for WMS_CHAT. |
| `lib/helper_db/sinh_vien/helper_supabase.dart` | Source evidence for WMS_CHAT. |
| `lib/models/sinh_vien/chat.dart` | Source evidence for WMS_CHAT. |

## View/function mapping

| View | Function | Source |
|---|---|---|
| `TroChuyen` | WMS_CHAT-FN01 | `lib/views/tro_chuyen/tro_chuyen.dart` |
| `ChatView` | WMS_CHAT-FN02 | `lib/views/tro_chuyen/chat.dart` |

## Dependency direction

```text
View → controller/helper → NeonDatabase hoặc SQLite helper
View → model
View → MaterialPageRoute/local state
AI path → AIService → external Gemini chỉ khi exact source gọi
```

Không tạo Work HTTP API contract mới. Tên helper có Supabase chỉ là compatibility naming khi implementation current là Neon; không ghi credential literal.

