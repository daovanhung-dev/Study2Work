---
title: "Data Mapping"
order: 5
dd_id: "63"
api_name: "Tạo và phát thông báo"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Luồng xử lý local

1. Xác thực Bearer JWT bằng shared guard với role `MENTOR`; lấy numeric Mentor ID từ `sub`.
2. Parse `recipients` thành ordered positive int64 User IDs và `channels` thành ordered unique `PUSH`/`EMAIL`; sai encoding trả 422.
3. Truy vấn roster legacy: mọi recipient phải là `users.role='STUDENT'`, có `enrollments.status='ACTIVE'`, và cùng nằm trong ít nhất một course có `courses.mentor_id` bằng Mentor ID.
4. Sinh một UUID Operation ID; trong cùng transaction, INSERT một row `notifications` cho mỗi recipient, gắn cùng `operation_id` và `sender_id`.
5. Với mỗi Notification ID × channel, INSERT một `notification_deliveries` row trạng thái `QUEUED` làm durable outbox.
6. Commit toàn bộ batch; nếu DB/outbox không nhận được thì rollback và trả 503. Lỗi projection/logic nội bộ trả 500.
7. Sau commit, trả HTTP 202 `ApiEnvelope<Operation>` với status `QUEUED`, Operation UUID và `meta.notification_ids` theo đúng thứ tự recipient.
8. Worker/provider chưa có trong Study runtime; outbox chỉ chứng minh yêu cầu đã được lưu bền vững, không chứng minh Push/Email đã phát.

### Mục lục

- [0. Xác thực](#step-0-auth)
- [1. Nhận và kiểm tra request](#step-1-request)
- [2. Kiểm tra recipient scope](#step-2-recipient-scope)
- [3. Ghi Notification và outbox](#step-3-persist-notification)
- [4. Dựng Operation và response](#step-4-operation-response)
- [5. Lỗi và rollback](#step-5-errors)

<a id="step-0-auth"></a>

## 0. Xác thực

- Gọi `validate_current_user_request(..., role="MENTOR")` trước khi truy cập DB.
- Principal ID là numeric JWT `sub`; dùng làm `notifications.sender_id`.
- Không nhận sender ID từ request body.

<a id="step-1-request"></a>

## 1. Nhận và kiểm tra request

| Field | Kiểu trực tiếp | Quy tắc local | Trạng thái |
|---|---|---|---|
| `recipients` | string! | CSV positive int64 `users.id`; item rỗng/sai range trả 422; bỏ ID lặp giữ vị trí đầu. | DERIVED từ API #62 `UserSummary[]`. |
| `title` | string! | Giữ nguyên text; tối đa 200 ký tự theo legacy `notifications.title`. | Max length lấy từ local DDL; live schema chưa xác minh. |
| `content` | int64! | Ghi giá trị thập phân vào legacy `notifications.content` TEXT. | DERIVED mapping; ý nghĩa free-form text vẫn lệch diagram. |
| `channels` | string! | CSV token `PUSH`/`EMAIL`; item rỗng hoặc token khác trả 422; bỏ duplicate giữ vị trí đầu. | DERIVED từ labels AC-25. |

- Bốn field và JSON types giữ nguyên theo catalog.
- Không thêm `course_id`, Idempotency-Key hoặc batch limit vào request.
- Vì thiếu `course_id`, scope check chỉ chứng minh có một common course Mentor sở hữu, không chứng minh đó chính là course đang mở trên UI.

<a id="step-2-recipient-scope"></a>

## 2. Kiểm tra recipient scope

- Query legacy `courses` → `enrollments` → `users`.
- Lọc `courses.mentor_id = :mentor_id`, `enrollments.status = 'ACTIVE'`, `users.role = 'STUDENT'` và `users.id = ANY(:recipient_ids)`.
- Chỉ chấp nhận nếu một course có số `DISTINCT users.id` bằng số recipient ID đã parse.
- Không áp dụng course status predicate; API #62 và các Mentor APIs liên quan dùng direct ownership, không lọc course status.
- Không tìm được common course → 403 `DESIGN_ACCESS_DENIED`; không tiết lộ recipient nào ngoài scope.

<a id="step-3-persist-notification"></a>

## 3. Ghi Notification và outbox

### 3.1. Notification rows

- Mỗi Student nhận một legacy BIGINT `notifications` row.
- `user_id` là Student ID; `sender_id` là Mentor ID; `title` giữ nguyên; `content` là decimal string.
- Một UUID `operation_id` được dùng chung cho tất cả notification rows trong cùng POST.
- `created_at` được cấp bởi DB và dùng làm Operation `submitted_at`/`updated_at` lúc mới QUEUED.
- `type` không được suy ra thành channel; để NULL theo legacy DDL.

### 3.2. Delivery outbox rows

- Mỗi Notification × channel tạo một `notification_deliveries` row.
- `channel` là `PUSH` hoặc `EMAIL`; trạng thái ban đầu `QUEUED`.
- Migration 009 thêm bảng delivery BIGINT và nullable `notifications.operation_id`; `DB.sql` chỉ là checked-in local schema artifact.
- Unique `(notification_id, channel)` ngăn tạo hai delivery row cùng channel cho một notification.
- No worker/provider consumes the outbox in this task; delivery state remains QUEUED until a future worker updates it.

<a id="step-4-operation-response"></a>

## 4. Dựng Operation và response

| Field | Mapping | Trạng thái |
|---|---|---|
| `data.id` | UUID `operation_id` dùng chung trên notification rows. | Schema direct; local persistence derived. |
| `data.kind` | `NOTIFICATION_DISPATCH`. | DERIVED; OperationKind enum chưa được catalog định nghĩa. |
| `data.status` | `QUEUED` sau khi commit thành công. | DERIVED; không đồng nghĩa provider đã gửi. |
| `data.owner_id` | Numeric Mentor JWT `sub`. | Local source pattern. |
| `data.submitted_at` | DB `created_at` của notification đầu tiên. | DB clock local. |
| `data.updated_at` | Cùng timestamp với submitted_at tại thời điểm chấp nhận. | DERIVED initial state. |
| `data.completed_at` | Omitted. | Operation mới queued chưa hoàn tất. |
| `data.result` | Omitted. | Reusable schema chỉ khai báo optional `Payment`; không gán result sai nghĩa. |
| `meta.notification_ids` | Mảng int64 Notification IDs theo thứ tự recipient request. | DERIVED handoff để client gọi #64 từng ID. |

- Success status/business code giữ nguyên catalog: 202 `DESIGN_OPERATION_ACCEPTED`.
- `success_response(...)` giữ envelope và trace ID hiện hành.
- API #64 response/aggregation và API #18 generic Operation polling vẫn thuộc session riêng; không thay runtime của hai API trong #63.

<a id="step-5-errors"></a>

## 5. Lỗi và rollback

- Missing/invalid Bearer → 401 `DESIGN_AUTHENTICATION_REQUIRED`.
- Sai role Mentor hoặc recipient set không có common directly owned ACTIVE course → 403 `DESIGN_ACCESS_DENIED`.
- Body type/CSV/range/channel sai → 422 `DESIGN_VALIDATION_ERROR`.
- DB không sẵn sàng khi xác minh hoặc ghi outbox → rollback, 503 `DESIGN_DEPENDENCY_UNAVAILABLE`.
- Projection bất thường hoặc lỗi nội bộ khác → rollback, 500 `DESIGN_INTERNAL_ERROR`.
- Không trả 202 trước commit; mọi notification/delivery rows trong một request cùng commit hoặc cùng rollback.
- Error response dùng shared `error_response(...)`; error `data` là JSON null và trace ID được giữ trong body/header.

## Request Usage Matrix

| Item | Source | Query/mutation use | Boundary |
|---|---|---|---|
| Authorization | Header | Shared MENTOR guard; numeric principal is sender | Direct auth contract; local numeric identity pattern. |
| `recipients` | Body string | Parse IDs; check common ACTIVE Student roster; insert one notification per ID | CSV encoding DERIVED. |
| `title` | Body string | Insert into `notifications.title` | Local DDL maximum 200. |
| `content` | Body int64 | Convert to decimal text and insert | DERIVED; human text contract conflict remains. |
| `channels` | Body string | Parse tokens; insert one QUEUED row per channel | CSV `PUSH`/`EMAIL` DERIVED. |
| `operation_id` | Generated UUID | Group notification rows; return Operation.id | No separate Study operations table. |

## Query Matrix

| Query | SQL constant | Purpose |
|---|---|---|
| Q1 | `FIND_COMMON_MENTOR_COURSE_FOR_RECIPIENTS` | Ensure every requested ID is a Student with ACTIVE enrollment in at least one directly owned course. |
| M1 | `INSERT_NOTIFICATION` | Persist one legacy Notification per recipient with shared Operation UUID. |
| M2 | `INSERT_NOTIFICATION_DELIVERY` | Persist each channel as a QUEUED outbox row. |

`query.py` contains SQL constants only. `view.py` binds parameters, runs every query, validates returned projections and owns commit/rollback.

## Macro-review: #62 → #63 → #64 and #18

- API #62 returns distinct legacy Student IDs; #63 parses those IDs as CSV and revalidates role/enrollment/owner before any write.
- #63 preserves the catalog's string recipient field and does not receive course_id; common-course inference is a DERIVED limitation.
- #63 returns Operation UUID in `data.id` and int64 notification IDs in `meta.notification_ids`; #64 can be called once per notification row.
- The new outbox schema provides local input for a future #64 status query, but #64's `Operation` response/result and aggregate semantics are not implemented here.
- API #18 UUID path and generic Operation persistence/lifecycle conflicts remain unresolved; this task does not implement #18.
- Checked-in DDL and fake-session HTTP tests do not establish live schema, migration deployment or actual provider delivery.

---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `3. Data mapping`
- Dimension: `B1:BB61`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `63`
- Số vùng merge: `0`

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 2 | `B2` | Flow xử lý data |  |
| 4 | `D4` | 0. |  |
| 4 | `E4` | Check quyền |  |
| 5 | `E5` | ・ |  |
| 5 | `F5` | Thực hiện check quyền |  |
| 6 | `E6` | ・ |  |
| 6 | `F6` | Get count khi get data từ … |  |
| 7 | `G7` | Table get |  |
| 7 | `K7` | : |  |
| 8 | `G8` | Conditions |  |
| 8 | `K8` | : |  |
| 10 | `E10` | ・ |  |
| 10 | `F10` | Trường hợp giá trị get được lớn hơn 0, thực hiện các xử lý tiếp theo |  |
| 11 | `E11` | ・ |  |
| 11 | `F11` | Trường hợp giá trị get được bằng 0, trả về status 2 |  |
| 13 | `D13` | 1. |  |
| 13 | `E13` | validate data input |  |
| 14 | `F14` | refer sheet [４．Error] |  |
| 16 | `D16` | 2. |  |
| 16 | `E16` | Get thông tin… |  |
| 18 | `F18` | Table get |  |
| 18 | `K18` | Column get |  |
| 18 | `P18` | Chú thích |  |
| 18 | `U18` | Remarks |  |
| 29 | `F29` | Target table / join condition |  |
| 30 | `F30` | Target table |  |
| 30 | `N30` | Join condition |  |
| 30 | `AL30` | 結合種類 |  |
| 31 | `F31` | txn_ams_t0320 AS a |  |
| 32 | `F32` | txn_amm_v0002 AS b |  |
| 32 | `N32` | ON a . chy_typ = b . kbn_typ AND b . dmin_cd = A AND b . kbnknr_cd = 001 |  |
| 32 | `AL32` | LEFT JOIN |  |
| 33 | `F33` | txn_amm_v0002 AS c |  |
| 33 | `N33` | ON a . chy_typ = c . kbn_typ AND c . dmin_cd = A AND c . kbnknr_cd = Z02 |  |
| 33 | `AL33` | LEFT JOIN |  |
| 35 | `F35` | ・ |  |
| 35 | `G35` | Điều kiện get data |  |
| 37 | `F37` | ・ |  |
| 37 | `G37` | Điều kiện sort |  |
| 41 | `D41` | 3. |  |
| 41 | `E41` | Insert/Update thông tin … |  |
| 42 | `E42` | Update table…. |  |
| 43 | `E43` | ・ |  |
| 43 | `F43` | Items update |  |
| 44 | `F44` | ・ |  |
| 44 | `G44` | Refer sheet [xxxx] |  |
| 45 | `E45` | ・ |  |
| 45 | `F45` | Điều kiện get data |  |
| 46 | `F46` | ・ |  |
| 46 | `G46` | auth_user. id = user hiện tại theo token |  |
| 48 | `D48` | 4. |  |
| 48 | `E48` | check kết quả execute query  |  |
| 49 | `E49` | 1. Thành công |  |
| 50 | `F50` | HTTPStatus = 200 |  |
| 51 | `F51` | Trả về kết quả status = 1 |  |
| 52 | `E52` | 2. Lỗi hệ thống phát sinh |  |
| 53 | `F53` | HTTPStatus = 500 |  |
| 54 | `F54` | Trả về kết quả status = 2 |  |
| 55 | `E55` | 3. Validate lỗi |  |
| 56 | `F56` | HTTPStatus = 400 |  |
| 57 | `F57` | Trả về kết quả status = 2 |  |
| 58 | `E58` | 4. Ngoài trường hợp trên |  |
| 59 | `F59` | Trả về kết quả status = 2 |  |

</details>
