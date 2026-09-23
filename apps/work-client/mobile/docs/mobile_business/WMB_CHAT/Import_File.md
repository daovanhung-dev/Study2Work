# Import/File map — WMB_CHAT

## Source evidence

| File | Vai trò |
|---|---|
| `lib/views/tro_chuyen/tro_chuyen.dart` | Source evidence for WMB_CHAT. |
| `lib/views/tro_chuyen/chat.dart` | Source evidence for WMB_CHAT. |
| `lib/controllers/chat/chat_controller.dart` | Source evidence for WMB_CHAT. |
| `lib/controllers/chat/nhung_doan_chat_controller.dart` | Source evidence for WMB_CHAT. |
| `lib/helper_db/helper_supabase.dart` | Source evidence for WMB_CHAT. |
| `lib/models/chat.dart` | Source evidence for WMB_CHAT. |

## View/function mapping

| View | Function | Source |
|---|---|---|
| `TroChuyen` | WMB_CHAT-FN01 | `lib/views/tro_chuyen/tro_chuyen.dart` |
| `ChatView` | WMB_CHAT-FN02 | `lib/views/tro_chuyen/chat.dart` |

## Dependency direction

```text
View → controller/helper → NeonDatabase hoặc SQLite helper
View → model
View → MaterialPageRoute/local state
AI path → AIService → external Gemini chỉ khi exact source gọi
```

Không tạo Work HTTP API contract mới. Tên helper có Supabase chỉ là compatibility naming khi implementation current là Neon; không ghi credential literal.

