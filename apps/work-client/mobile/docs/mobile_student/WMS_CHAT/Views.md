# View inventory — WMS_CHAT

Mỗi view được ghi đúng một lần; status phản ánh current source, không phải business approval.

| View ID | Widget | Source file | Status | Current behavior |
|---|---|---|---|---|
| WMS_CHAT-V01 | `TroChuyen` | `lib/views/tro_chuyen/tro_chuyen.dart` | WIRED | Partner list và mở ChatView. |
| WMS_CHAT-V02 | `ChatView` | `lib/views/tro_chuyen/chat.dart` | WIRED | History/send/polling 3 giây, dedup ids, dispose cancellation. |

## WMS_CHAT-V01 — TroChuyen

- **Source:** `lib/views/tro_chuyen/tro_chuyen.dart`
- **Status:** WIRED
- **Function:** WMS_CHAT-FN01
- **Current behavior:** Partner list và mở ChatView.
- **UI states:** ghi loading/empty/error/success hoặc static theo exact widget tree; không suy ra state mới.
- **Navigation/side effect:** xem function tương ứng trong [Function_List.md](Function_List.md).

## WMS_CHAT-V02 — ChatView

- **Source:** `lib/views/tro_chuyen/chat.dart`
- **Status:** WIRED
- **Function:** WMS_CHAT-FN02
- **Current behavior:** History/send/polling 3 giây, dedup ids, dispose cancellation.
- **UI states:** ghi loading/empty/error/success hoặc static theo exact widget tree; không suy ra state mới.
- **Navigation/side effect:** xem function tương ứng trong [Function_List.md](Function_List.md).

