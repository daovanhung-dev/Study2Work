# WMS_CHAT / Trò chuyện sinh viên - doanh nghiệp

## Evidence và status

| Trục | Giá trị |
|---|---|
| Lifecycle | Current |
| DD decision | Draft |
| Implementation | Implemented |
| Verification | Static-verified; Runtime-unverified |
| Source baseline | 212455f627846c0a3dc56107ee162415014d85b5 |
| Evidence | User request, mobile-work context và exact Flutter source |
| Business source | Chưa có BD/BRD mobile; unresolved decisions là OPEN QUESTION |

## Mục đích và boundary

- **Mục đích:** Liệt kê business partner, đọc/gửi message và polling message mới.
- **Actor:** Sinh viên
- **Trong phạm vi:** View/controller/helper/model trace và side effect đã có evidence.
- **Ngoài phạm vi:** API/schema mới, migration, runtime implementation và production behavior chưa được chốt.
- **Boundary:** TroChuyen → getChats → ChatView → getChat/guiTinNhan → Timer 3 giây → dedup → dispose cancel.

## Current data flow

| Nhóm | Evidence |
|---|---|
| Data | DoanChat/Chat trong Neon; cached student id từ SQLite. |
| Integration | `lib/views/tro_chuyen/tro_chuyen.dart`; `lib/views/tro_chuyen/chat.dart`; `lib/controllers/chat/chat_controller.dart` |
| Side effect | TroChuyen → getChats → ChatView → getChat/guiTinNhan → Timer 3 giây → dedup → dispose cancel. |
| Security | Không ghi credential literal; direct client data access là prototype boundary. |

## WMS_CHAT-BR01 — Current source rule

Rows hiện có seed seenIds; chỉ id mới emit; overlap skip; timer cancel trong dispose.

- Cách kiểm tra: đối chiếu exact source paths trong [Import_File.md](Import_File.md).
- Status: CURRENT_SOURCE_RULE, chưa phải approved business requirement.

## Open questions

- **OPEN QUESTION:** Cần chốt unread/read, retry/timeout, retention và moderation.
- BA/PO phải chốt các rule chưa có evidence trước khi code feature mới.

## Traceability

| Requirement/evidence | Feature | Rule | Functions | Views | Source | Tests |
|---|---|---|---|---|---|---|
| User request + current source inventory | WMS_CHAT-F01 | WMS_CHAT-BR01 | WMS_CHAT-FN01..FN02 | WMS_CHAT-V01..V02 | [Import_File.md](Import_File.md) | WMS_CHAT-TC01..TC02 |

