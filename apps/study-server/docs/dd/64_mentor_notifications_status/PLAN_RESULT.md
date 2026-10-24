# PLAN_RESULT — Study API #64

## Kết quả plan trước authoring

- Plan, Requirement/Request/Query/Mutation/Response matrices đã được ghi trong worklog trước khi tạo thư mục DD.
- API: #64 — Theo dõi trạng thái gửi; trạng thái `Draft — Needs Confirmation`.
- Giao phẩm: 8 sheet template + 3 report Markdown; không tạo ZIP.

## Sources đã đối chiếu

| Nguồn | Bằng chứng sử dụng | Trạng thái |
|---|---|---|
| API catalog #64 | GET/path/auth/role/Operation/200 và đúng bốn errors 401/403/404/500 | DIRECT |
| AC-25 index + diagram | #62 → #63 → Push/Email → #64 đọc delivery status; node #18 detached | DIRECT; operation link cần xác nhận |
| Reusable schemas | Operation, NotificationDelivery, Notification, Payment | Shape DIRECT; delivery/Operation mapping mâu thuẫn |
| Legacy DB guide/DDL | Notification BIGINT/user_id/sender_id/is_read; không có delivery table/status | Candidate; không phải live query source |
| V1-PILOT DDL | Notification/delivery UUID; delivery status/channel/attempt rows | Candidate khác model; không ghép legacy |
| Prior DDs #18/#43/#45/#62/#63 | Operation ID/persistence, read-state boundary, roster/create/status flow | Precedent; không thay contract #64 |
| Study router/middleware/test source | Không có route/query/module/provider/test #64; path ngoài `DESIGN_CONTRACT_PATHS` | `UNWIRED / NOT_FOUND` |

## API Requirement Matrix

| API ID | Method/path | Auth | Request | Success/response | Errors | Status |
|---|---|---|---|---|---|---|
| #64 | `GET /api/v1/mentor/notifications/{notification_id}/status` | Bearer JWT; Mentor | `notification_id:int64!`; no body/query | 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<Operation>` | 401 authentication; 403 access; 404 resource; 500 internal | Catalog DIRECT; delivery semantics, mapping và ID handoff open |

## Luồng AC-25 và ranh giới

```text
#62 roster → chọn recipient/title/content → #63 tạo Notification + recipients
→ Push/Email → #64 đọc delivery status → UI hiển thị
```

API #64 là đọc trạng thái delivery theo notification ID. API #18 là generic Operation polling nhưng node diagram rời; không dùng Operation ID thay notification ID. Catalog #63 không công bố notification ID trong response, nên đường đi client bị chặn.

## Ma trận sử dụng request

| Field | Cách dùng trực tiếp | Khoảng trống |
|---|---|---|
| `notification_id:int64!` | Chọn notification cần theo dõi | Legacy ID BIGINT có thể khớp kiểu nhưng không có delivery status; pilot ID UUID không khớp. |
| Authorization | Mentor Bearer | Permission relation và principal mapping chưa rõ. |
| Body/query | Không có | Giữ đúng contract GET. |

## Query / Mutation Matrix

| ID | Operation | Logical target | Result/status |
|---|---|---|---|
| Q1 | SELECT notification + permission scope | Notification | Physical table/owner relation chưa xác nhận; không viết SQL. |
| Q2 | SELECT/aggregate delivery state | NotificationDelivery | Aggregate/status semantics chưa chốt; pilot attempt rows không có recipient key. |
| M1 | N/A | N/A | GET read-only; không có mutation/provider call. |

## Response Source Matrix

| Response field | Contract | Mapping/gap |
|---|---|---|
| Envelope | `ApiEnvelope<Operation>` | Direct response shape; message/meta/error body convention còn gap. |
| `data.id` | Operation UUID | Không có mapping từ `notification_id:int64`. |
| `data.kind/status/owner_id/timestamps` | Operation fields | Persistence, lifecycle, enums và owner source SOURCE_REQUIRED. |
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
- Physical query, auth relation, response bridge và delivery aggregation ghi SOURCE_REQUIRED/open: PASS.
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

**Trạng thái:** `VERIFIED_WITH_OPEN_QUESTIONS` — review logic nhóm đã hoàn tất; contract/schema/runtime chưa được sửa hoặc xác nhận.

| Mắt xích | Kết quả review | Ảnh hưởng/việc cần chốt |
|---|---|---|
| #62 roster | Catalog trả `Page<Course>` dù path `/students` và diagram cần active learners; không có page/size input. | Chưa có learner ID/projection ổn định để #63 dùng. |
| #63 create/send | `recipients:string!` thiếu encoding và course scope; `content:int64` lệch nhập text; response 202 Operation không có notification_id. | Client không thể xác thực recipient set đầy đủ hoặc gọi #64 bằng ID direct. |
| #64 delivery status | Path dùng notification_id:int64 nhưng response là Operation; `NotificationDelivery` gần với delivery intent nhưng enum/counts/physical query chưa rõ. | Không map delivery status/counters từ direct Operation. |
| #18 job polling | Node trong diagram AC-25 rời; row path int64 lệch UUID schema/diagram; owner, result và Study storage còn mở. | Job state và per-notification delivery phải tách, ID handoff cần contract. |
| Persistence/auth | Legacy BIGINT notification chỉ lưu `is_read`; pilot dùng UUID attempts không có recipient ID; Mentor scope chưa có source. | Không viết physical query hoặc coi read state là send state. |

**Khuyến nghị DERIVED để thống nhất trước implementation:** (1) #62 trả learner projection với pagination được khai báo; (2) #63 nhận course scope và recipient IDs/channel/content có encoding rõ, đồng thời bàn giao notification_id và operation_id riêng; (3) #64 trả delivery summary có enum/count grain được duyệt; (4) #18 theo dõi operation job riêng. Đây là đề xuất thay đổi contract, không phải behavior direct hiện tại.
