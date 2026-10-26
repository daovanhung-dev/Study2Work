# PLAN_RESULT — Study API #63

## Kết quả plan trước authoring

- Plan và các ma trận Requirement/Request/Query/Mutation/Response đã được ghi vào worklog trước khi tạo thư mục DD.
- API: #63 — Tạo và phát thông báo; trạng thái `Draft — Needs Confirmation`.
- Giao phẩm: 8 sheet template + 3 report Markdown; không tạo ZIP.

## Sources đã đối chiếu

| Nguồn | Bằng chứng sử dụng | Trạng thái |
|---|---|---|
| API catalog #63 | POST, Mentor Bearer, 4 body fields/types, 202 Operation và exact errors 401/403/422/503/500 | DIRECT |
| AC-25 index + diagram | Chọn course → #62 → nhập/chọn → #63 → Notification+recipients → Push/Email → #64; node #18 disconnected | DIRECT; handoff #18 cần xác nhận |
| Reusable schemas | Notification, NotificationDelivery, Operation, Payment | Shape DIRECT; Operation result không phù hợp notification |
| Legacy guide/DDL | Notification BIGINT, user_id mỗi recipient row, sender_id, title/content; không có delivery/recipient table | Candidate; chưa phải live source |
| V1-PILOT DDL | UUID notification theo learner + UUID delivery rows; IN_APP/EMAIL và delivery status enum | Candidate khác model; không ghép legacy |
| Prior DDs #18/#43/#45/#50/#62 | Operation gap, Notification schema/read boundary, logical mapping pattern, recipient group conflict | Precedent; không thay contract #63 |
| Study router/middleware hiện tại | Chưa có route/module/provider/test #63; path ngoài DESIGN_CONTRACT_PATHS | `UNWIRED / NOT_FOUND` |

## API Requirement Matrix

| API ID | Method/path | Auth | Request | Success/response | Errors | Status |
|---|---|---|---|---|---|---|
| #63 | `POST /api/v1/mentor/notifications` | Bearer JWT; Mentor | `recipients:string!`, `title:string!`, `content:int64!`, `channels:string!` | 202 `DESIGN_OPERATION_ACCEPTED`; `ApiEnvelope<Operation>` | 401 authentication; 403 access; 422 validation; 503 dependency unavailable; 500 internal | Catalog DIRECT; semantics/encoding open |

## Luồng AC-25 và ranh giới

```text
#62 roster → chọn recipients/title/content → #63 ghi Notification + recipients
→ Push/Email theo channel → #64 đọc delivery status
```

API #63 không xác nhận delivery tại 202. AC/API index cũng liệt kê #18 operation tracker, nhưng diagram node #18 không có edge. #18 ID type và Operation result còn discrepancy.

## Ma trận sử dụng request

| Field | Cách dùng trực tiếp | Khoảng trống / đề xuất |
|---|---|---|
| `recipients:string!` | Chọn người nhận và tạo associations | Encoding/ID chưa rõ; đề xuất CSV unique int64 Student IDs, cần đồng bộ #62. |
| `title:string!` | Notification title | Trim/non-empty DERIVED; max 200 là schema candidate. |
| `content:int64!` | Scalar trực tiếp theo catalog | DISCREPANCY với ô nhập text và Notification.content; đề xuất `string!`. |
| `channels:string!` | Chọn Push/Email | Encoding/tokens chưa rõ; CSV chỉ là đề xuất. |
| `course_id` | Không có field trực tiếp | Đề xuất thêm để thực thi kiểm tra quyền/course enrollment. |
| Idempotency-Key | Guideline cho retryable mutations | DERIVED; storage/behavior chưa có contract riêng. |

## Query / Mutation Matrix

| ID | Operation | Logical target | Result/status |
|---|---|---|---|
| Q1 | SELECT course/enrollment | Verify Mentor course scope + selected recipients | Không thể chốt; body thiếu course_id và schema live chưa chọn. |
| M1 | INSERT | Notification | Diagram DIRECT; physical table/columns conflict. |
| M2 | INSERT | Recipient associations | Diagram DIRECT; legacy không có recipient table. |
| M3 | Create/enqueue | Operation + delivery job | Cần cho 202/flow; không có persistence/queue source trong Study. |
| M4 | External dispatch | Push/Email | Diagram DIRECT; provider/retry/status aggregation SOURCE_REQUIRED. |

## Response Source Matrix

| Response field | Contract | Mapping/gap |
|---|---|---|
| Envelope | ApiEnvelope | Success code direct; safe message/trace uses shared convention. |
| `data.id` | Operation UUID | Schema dùng chung trực tiếp; row API #18 lại khai báo path int64. |
| `data.kind/status/owner_id/timestamps` | Operation fields | Enum/lifecycle/owner mapping/storage SOURCE_REQUIRED. |
| `data.completed_at?` | Date-time tùy chọn | Chưa có ngữ nghĩa/source completion. |
| `data.result?:Payment` | Optional Payment | Schema dùng chung trực tiếp nhưng không phù hợp với notification operation. |
| `notification_id:int64` cho #64 | Không có trong Operation schema | Thiếu handoff; bổ sung mapping result hoặc sửa #64. |

## Discrepancy và các khuyến nghị đơn giản

- `content:int64` mâu thuẫn với ô nhập text trong diagram và Notification schema string; đề xuất đổi thành `content:string!`.
- #63 thiếu `course_id`; đề xuất bổ sung và server kiểm tra recipients với course roster.
- Giữ direct `recipients:string!` và `channels:string!`; chỉ dùng CSV sau khi duyệt token và ID key.
- Response Operation của #63 không lộ notification_id cho #64; Operation.result Payment không phù hợp. Cần thống nhất #18/#64 trước khi code.
- Legacy và V1-PILOT notification schemas khác nhau; không tự tạo SQL/table; live schema chưa xác minh.
- 202 nghĩa là đã tiếp nhận, không phải đã phát; queue/outbox, idempotency, retry và partial-delivery lifecycle còn mở.

## Template fingerprints

| Template | SHA-256 |
|---|---|
| `00_Cover.md` | `fd5f568c5329d3069fbaff617a6f4ed3b5ffaf050e042c95b7c9100a05f79e63` |
| `01_Lich_su.md` | `d1cec6573433a9551812bf47552f8a44d7c533d790341941047c410e1d57771e` |
| `02_Overview.md` | `c2879c2f0e007395558dfee4167484786c5aadb3fdd63ab135ca111e7c5f8aa6` |
| `03_Request.md` | `37aaa1e9d7f3e83329e81ab38d922c9dff959284d5b7b3ae353878798dd4b7aa` |
| `04_Response.md` | `5bcb43ba5eb487302dd5d5efde4383b9f452f9fed2149f55315d64ff78a19ab8` |
| `05_Data_Mapping.md` | `11bc77bc0522d3af27b9499114991c8819046ac32bde5c1efdc841be088dcc5b` |
| `06_Error.md` | `e0160ea07fdbc74f2cafebd6ed3b21e60029662d28d67f5f6a0b4d95ba72be9b` |
| `07_table.md` | `4c9a0e037872333210aaf44ba9fbf00a0e63343a69d55250e537d2c3c5e2d356` |

## Cổng kế hoạch

- Contract trực tiếp được giữ nguyên trong Requirement Matrix: PASS.
- Diagram AC-25 node/edge đã đọc đầy đủ và ranh giới API được ghi: PASS.
- Các API tham khảo #18/#43/#45/#50/#62/#93 được dùng có kiểm soát: PASS.
- Request/Query/Mutation/Response matrices lập trước authoring: PASS.
- Contract conflicts, schema gaps và simple derived recommendations phân tách: PASS.
- Macro-review AC-25 #62–#64 và API #18 đã hoàn tất ở mức tài liệu: `VERIFIED_WITH_OPEN_QUESTIONS`; unresolved decisions được ghi trong reports nhóm.

## Reconciliation khi triển khai API #63

- Giữ direct request fields/types, exact 202 response type và error set của catalog; không thêm `course_id` hoặc Idempotency-Key.
- Dùng CSV positive Student `users.id` và CSV `PUSH`/`EMAIL` theo fallback `DERIVED`; toàn bộ recipient set phải cùng có mặt trong ít nhất một ACTIVE roster do Mentor trực tiếp sở hữu.
- Giữ `content:int64` và lưu decimal text vào legacy Notification `content`; ý nghĩa free-form message còn là discrepancy cần contract owner xác nhận.
- Chọn legacy BIGINT Notification rows và migration 009 delivery outbox vì phù hợp API #62 IDs và API #64 `notification_id:int64`; không ghép V1-PILOT UUID schema.
- Một Notification row được ghi cho mỗi recipient; UUID Operation group được lưu trên các rows; response `meta.notification_ids` công bố IDs để gọi API #64.
- Trả 202 sau khi toàn bộ rows commit với status `QUEUED`; worker/provider chưa có, nên endpoint chứng minh acceptance/outbox persistence trong local tests chứ không chứng minh Push/Email delivery.
- Fallbacks là local implementation decisions, không đổi trạng thái DD `Draft — Needs Confirmation` hoặc xác nhận live schema.
