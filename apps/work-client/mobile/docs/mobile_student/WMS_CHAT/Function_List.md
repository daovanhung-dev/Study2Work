# Function list — WMS_CHAT

## WMS_CHAT-FN01 — TroChuyen interaction

- **View:** WMS_CHAT-V01
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Sinh viên; production permission chưa có contract.
- **Rule:** WMS_CHAT-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** Partner list và mở ChatView.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** WIRED, `lib/views/tro_chuyen/tro_chuyen.dart`.

## WMS_CHAT-TC01 — TroChuyen verification case

- **Covers:** WMS_CHAT-FN01 và WMS_CHAT-V01.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## WMS_CHAT-FN02 — ChatView interaction

- **View:** WMS_CHAT-V02
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Sinh viên; production permission chưa có contract.
- **Rule:** WMS_CHAT-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** History/send/polling 3 giây, dedup ids, dispose cancellation.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** WIRED, `lib/views/tro_chuyen/chat.dart`.

## WMS_CHAT-TC02 — ChatView verification case

- **Covers:** WMS_CHAT-FN02 và WMS_CHAT-V02.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## Test matrix

| Test ID | View | Scenario | Result |
|---|---|---|---|
| WMS_CHAT-TC01 | WMS_CHAT-V01 | TroChuyen happy/error/empty state phù hợp | Runtime-unverified |
| WMS_CHAT-TC02 | WMS_CHAT-V02 | ChatView happy/error/empty state phù hợp | Runtime-unverified |

