# PLAN_RESULT — Study API #64

## Kết quả plan trước authoring

- Plan, Requirement/Request/Query/Mutation/Response matrices đã được ghi trong worklog trước khi tạo thư mục DD.
- API: #64 — Theo dõi trạng thái gửi; trạng thái `Draft — Needs Confirmation`.
- Giao phẩm: 8 sheet template + 3 report Markdown; không tạo ZIP.

The source and matrix sections below record the DD planning snapshot before the
API #64 runtime implementation. See the reconciliation at the end and
[VERIFICATION_REPORT.md](./VERIFICATION_REPORT.md) for current local source and
verification status.

## Reconciliation trước và sau implementation API #64

- Trước runtime edits, giữ nguyên contract trực tiếp: GET signed-int64 path,
  Mentor Bearer, no body/query, HTTP 200 `ApiEnvelope<Operation>` và errors
  401/403/404/500. DD tiếp tục ở trạng thái Draft.
- Sau khi đối chiếu producer API #63, dùng local DERIVED fallback: đọc legacy
  BIGINT `notifications` cùng `notification_deliveries`; kiểm tra
  `sender_id == JWT sub`; dựng Operation từ `operation_id`, sender và timestamps;
  aggregate `QUEUED` ưu tiên, sau đó `FAILED`, còn lại all `SENT`.
- Runtime route/module/query/test hiện đã có local source và pass HTTP/OpenAPI
  verification bằng fake DB. Migration 009/live schema, policy approval và
  Push/Email worker/provider delivery vẫn chưa được xác minh.

## Sources đã đối chiếu

| Nguồn | Bằng chứng sử dụng | Trạng thái |
|---|---|---|
| API catalog #64 | GET/path/auth/role/Operation/200 và đúng bốn errors 401/403/404/500 | DIRECT |
| AC-25 index + diagram | #62 → #63 → Push/Email → #64 đọc delivery status; node #18 detached | DIRECT; operation link cần xác nhận |
| Reusable schemas | Operation, NotificationDelivery, Notification, Payment | Shape DIRECT; delivery/Operation mapping mâu thuẫn |
| Legacy DB guide/DDL | Notification BIGINT/user_id/sender_id/is_read; không có delivery table/status | Candidate; không phải live query source |
| V1-PILOT DDL | Notification/delivery UUID; delivery status/channel/attempt rows | Candidate khác model; không ghép legacy |
| Prior DDs #18/#43/#45/#62/#63 | Operation ID/persistence, read-state boundary, roster/create/status flow | Precedent; không thay contract #64 |
| Study router/middleware/test source | Tại thời điểm lập DD chưa có route/query/module/provider/test #64; path ngoài `DESIGN_CONTRACT_PATHS` | `UNWIRED / NOT_FOUND` ở snapshot trước implementation; hiện đã wired local |

## API Requirement Matrix

| API ID | Method/path | Auth | Request | Success/response | Errors | Status |
|---|---|---|---|---|---|---|
| #64 | `GET /api/v1/mentor/notifications/{notification_id}/status` | Bearer JWT; Mentor | `notification_id:int64!`; no body/query | 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<Operation>` | 401 authentication; 403 access; 404 resource; 500 internal | Catalog DIRECT; delivery semantics, mapping và ID handoff open |

## Luồng AC-25 và ranh giới

```text
#62 roster → chọn recipient/title/content → #63 tạo Notification + recipients
→ Push/Email → #64 đọc delivery status → UI hiển thị
```

API #64 là đọc trạng thái delivery theo notification ID. API #18 là generic Operation polling nhưng node diagram rời; không dùng Operation ID thay notification ID. Catalog #63 không khai báo notification ID, còn local API #63 hiện trả `meta.notification_ids` theo mapping DERIVED để gọi #64.

## Ma trận sử dụng request

| Field | Cách dùng trực tiếp | Khoảng trống |
|---|---|---|
| `notification_id:int64!` | Chọn notification cần theo dõi | Legacy ID BIGINT có thể khớp kiểu nhưng không có delivery status; pilot ID UUID không khớp. |
| Authorization | Mentor Bearer | Permission relation và principal mapping chưa rõ. |
| Body/query | Không có | Giữ đúng contract GET. |

## Query / Mutation Matrix

| ID | Operation | Logical target | Result/status |
|---|---|---|---|
| Q1 | SELECT notification + permission scope | Notification | Initial DD snapshot chưa có source; current local implementation reads legacy BIGINT notification and checks `sender_id` against JWT `sub` as DERIVED. |
| Q2 | SELECT/aggregate delivery state | NotificationDelivery | Initial DD snapshot left source unresolved; current local implementation reads migration 009 delivery rows and aggregates their state as DERIVED. |
| M1 | N/A | N/A | GET read-only; không có mutation/provider call. |

## Response Source Matrix

| Response field | Contract | Mapping/gap |
|---|---|---|
| Envelope | `ApiEnvelope<Operation>` | Direct response shape; message/meta/error body convention còn gap. |
| `data.id` | Operation UUID | Current local mapping uses `notifications.operation_id`, separate from path `notification_id`. |
| `data.kind/status/owner_id/timestamps` | Operation fields | Current local mapping uses API #63's kind, aggregate channel state, `sender_id`, `created_at`, and latest delivery `updated_at`; DERIVED. |
| `data.result?:Payment` | Optional Payment | Direct reusable schema nhưng không chứa delivery data. |
| `NotificationDelivery` | notification ID/status/queued/sent/failed | Ý định gần với AC-25; chưa phải response direct và không có approved query source. |

## Discrepancy và khuyến nghị đơn giản

- Catalog response Operation lệch mục tiêu diagram là delivery status; đề xuất #64 trả `NotificationDelivery` và #18 giữ job tracking riêng, cần đổi contract.
- #63 phải bàn giao `notification_id:int64` nếu client gọi #64; giữ `operation_id:uuid` riêng cho #18.
- Chọn một schema Study canonical; không dùng `is_read` làm delivery status, không gộp legacy BIGINT với pilot UUID.
- Chốt delivery status/count grain và retry aggregation trước khi viết query; pilot table lưu attempts, không lưu recipient ID.
- Chốt access predicate và 403/404 privacy policy; không tự suy từ `sender_id` candidate.

## Cổng kế hoạch

- Contract direct #64 được giữ nguyên trong matrices: PASS.
- AC-25 node/edge và detached #18 được ghi rõ: PASS.
- Prior DD #18/#43/#45/#62/#63 được đối chiếu: PASS.
- Requirement/Request/Query/Mutation/Response matrices lập trước authoring: PASS.
- Physical query, auth relation, response bridge và delivery aggregation were recorded SOURCE_REQUIRED/open before runtime edits: PASS.
- Macro-review #62–#64 + #18: `VERIFIED_WITH_OPEN_QUESTIONS`; xem nhóm findings dưới đây.

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


## Macro-review AC-25 #62–#64 + API #18

**Trạng thái:** `VERIFIED_WITH_OPEN_QUESTIONS` — review nhóm đã hoàn tất; catalog/diagram policy vẫn chưa được phê duyệt dù local fallback đã được implement.

| Mắt xích | Kết quả review | Ảnh hưởng/việc cần chốt |
|---|---|---|
| #62 roster | Catalog trả `Page<Course>` dù path `/students` và diagram cần active learners; không có page/size input. | Chưa có learner ID/projection ổn định để #63 dùng. |
| #63 create/send | `recipients:string!` thiếu encoding và course scope; `content:int64` lệch nhập text; response 202 Operation không có notification_id. | Client không thể xác thực recipient set đầy đủ hoặc gọi #64 bằng ID direct. |
| #64 delivery status | Path dùng notification_id:int64 nhưng response là Operation; `NotificationDelivery` gần với delivery intent nhưng enum/counts/physical query chưa rõ. | Không map delivery status/counters từ direct Operation. |
| #18 job polling | Node trong diagram AC-25 rời; row path int64 lệch UUID schema/diagram; owner, result và Study storage còn mở. | Job state và per-notification delivery phải tách, ID handoff cần contract. |
| Persistence/auth | Initial DDL snapshot lacked delivery rows; API #63 now writes a local BIGINT outbox, while pilot UUID attempts remain a separate schema. | API #64 uses the local #63 rows as DERIVED; do not treat `is_read` as send state or claim live deployment. |

**Khuyến nghị DERIVED để thống nhất contract:** (1) #62 trả learner projection với pagination được khai báo; (2) #63 nhận course scope và recipient IDs/channel/content có encoding rõ, đồng thời bàn giao notification_id và operation_id riêng; (3) #64 trả delivery summary có enum/count grain được duyệt; (4) #18 theo dõi operation job riêng. Đây là đề xuất đổi contract, không phải behavior direct hiện tại; local APIs #62–#64 hiện dùng fallback đã ghi trong từng DD.

## Reconciliation trước implementation API #64

- Giữ nguyên direct catalog `GET /api/v1/mentor/notifications/{notification_id}/status`, int64 path, HTTP 200 `DESIGN_RESOURCE_RETRIEVED`, `ApiEnvelope<Operation>`, và chỉ các lỗi 401/403/404/500.
- Dùng local legacy BIGINT `notifications` và `notification_deliveries` do API #63 hiện ghi; API #63 đã persist `operation_id`, `sender_id`, `created_at` và một row cho mỗi channel trong cùng acceptance transaction. Không dùng `is_read` hoặc UUID V1-PILOT relation.
- API #63 `meta.notification_ids` cung cấp path key; #64 ánh xạ `operation_id` thành Operation UUID, `sender_id` thành owner, `created_at` thành submitted time và `MAX(delivery.updated_at)` thành updated time.
- Chỉ sender Mentor khớp JWT `sub` được đọc; owner mismatch là 403, còn ID/path hoặc dispatch-status resource thiếu là 404. Đây là local DERIVED policy.
- Aggregate status theo trạng thái outbox hiện có: bất kỳ `QUEUED` thì `QUEUED`; nếu không, bất kỳ `FAILED` thì `FAILED`; nếu toàn bộ `SENT` thì `SENT`. Trạng thái partial bị tóm tắt là FAILED; direct Operation không xuất counts.
- Omit `completed_at` và Payment-shaped `result` vì Study không có Operation persistence/lifecycle/result mapping tương ứng. Không thêm table, provider call hoặc API #18 behavior.
- Các quyết định thực thi được ghi là DERIVED trong DD; không đổi catalog contract hoặc trạng thái `Draft — Needs Confirmation`. Migration 009 vẫn chỉ là checked-in artifact, chưa xác minh live.
