# Function list — WMB_CHAT

## WMB_CHAT-FN01 — TroChuyen interaction

- **View:** WMB_CHAT-V01
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Doanh nghiệp; production permission chưa có contract.
- **Rule:** WMB_CHAT-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** Partner list và mở ChatView.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** WIRED, `lib/views/tro_chuyen/tro_chuyen.dart`.

## WMB_CHAT-TC01 — TroChuyen verification case

- **Covers:** WMB_CHAT-FN01 và WMB_CHAT-V01.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## WMB_CHAT-FN02 — ChatView interaction

- **View:** WMB_CHAT-V02
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Doanh nghiệp; production permission chưa có contract.
- **Rule:** WMB_CHAT-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** History/send/polling 3 giây, dedup ids, dispose cancellation.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** WIRED, `lib/views/tro_chuyen/chat.dart`.

## WMB_CHAT-TC02 — ChatView verification case

- **Covers:** WMB_CHAT-FN02 và WMB_CHAT-V02.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## Test matrix

| Test ID | View | Scenario | Result |
|---|---|---|---|
| WMB_CHAT-TC01 | WMB_CHAT-V01 | TroChuyen happy/error/empty state phù hợp | Runtime-unverified |
| WMB_CHAT-TC02 | WMB_CHAT-V02 | ChatView happy/error/empty state phù hợp | Runtime-unverified |

