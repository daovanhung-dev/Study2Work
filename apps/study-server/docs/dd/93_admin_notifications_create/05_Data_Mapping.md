---
title: "Data Mapping"
order: 5
dd_id: "93"
api_name: "Tạo/phát notification"
source_sheet: "3. Data mapping"
format: markdown
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

### Mục lục

1. [Step 0 — Authentication and permission](#step-0-authentication-and-permission)
2. [Step 1 — Read request](#step-1-read-request)
3. [Step 2 — Resolve audience](#step-2-resolve-audience)
4. [Step 3 — Create Notification](#step-3-create-notification)
5. [Step 4 — Accept and dispatch](#step-4-accept-and-dispatch)
6. [Step 5 — Map response](#step-5-map-response)
7. [Step 6 — Return result or error](#step-6-return-result-or-error)

<a id="step-0-authentication-and-permission"></a>

## Step 0 — Authentication and permission

- Read Authorization and validate Bearer JWT; missing/invalid maps to 401 DESIGN_AUTHENTICATION_REQUIRED.
- Check role Admin and AC-36 notification-management permission before audience resolution.
- Permission key, claim mapping, caller ID and 403 precedence are SOURCE_REQUIRED.
- Current source has no #93 route or verified Admin guard: UNWIRED / NOT_FOUND.
- Error: [06_Error.md](./06_Error.md#error-401).

<a id="step-1-read-request"></a>

## Step 1 — Read request

| Input | Direct type | Use | Status |
|---|---|---|---|
| recipients | Optional int64[] | Explicit audience candidate | Selector rule open |
| segment | Optional AudienceSegment | Segment candidate | Values/expansion SOURCE_REQUIRED |
| title | Required string | Notification title | Blank/length rules absent |
| content | Required string | Notification content | Blank/length rules absent |
| channels | Required NotificationChannel[] | Delivery intent | Enum/provider mapping absent |

- Preserve names, types and requiredness.
- Do not add action, scheduled_at, operation_id or an undeclared header.
- DERIVED proposal: exactly one audience selector, non-empty channels, nonblank title/content; not approved.

<a id="step-2-resolve-audience"></a>

## Step 2 — Resolve audience

- Contract does not define both/neither selector behavior, empty lists, duplicate IDs, segment values, or recipient eligibility.
- AC-36 does not identify a physical audience source.
- Do not copy Mentor course checks from #63 or Student ownership from #43–#45.
- No executable SELECT, partial-recipient behavior or ordering is specified: SOURCE_REQUIRED.

### Query matrix

| ID | Purpose | Type/source | Columns/conditions | Pagination | Status |
|---|---|---|---|---|---|
| Q1 | Resolve recipient IDs or segment | No approved table/view | Predicate and scope undefined | N/A | SOURCE_REQUIRED |
| Q2 | Read Operation if response uses it | No Study Operation store found | API #18 ID/owner conflict | N/A | SOURCE_REQUIRED |

<a id="step-3-create-notification"></a>

## Step 3 — Create Notification

- AC-36 node n6 requires logical Notification + recipients.
- Use title/content as logical Notification values.
- Treat channels as delivery intent; do not map to legacy notifications.type.
- Admin identity mapping, physical target, ID/status/time generation, audit and rollback are SOURCE_REQUIRED.
- Legacy notifications is only a partial candidate; V1-PILOT UUID learner model is separate.
- See [07_table.md](./07_table.md); it is not an executable INSERT.

### Mutation matrix

| ID | Logical operation | Target | Fields/source | Transaction/failure | Mapping |
|---|---|---|---|---|---|
| M1 | INSERT Notification | No approved target | See 07_table.md per-field candidates; ID/status/time unknown | Boundary SOURCE_REQUIRED | [07_table.md](./07_table.md) |
| M2 | INSERT recipient association | No compatible table | Explicit recipients or segment expansion | Duplicate/partial-write behavior SOURCE_REQUIRED | [08 mapping](./08_notification_recipients_insert.md) |
| M3 | Accept async send operation | Queue/Operation store not found | Logical Notification/audience/channels | DERIVED only | No physical mapping |

- A simple proposal writes Notification and recipient associations consistently.
- Transaction mechanism and durable acceptance boundary need confirmation.

<a id="step-4-accept-and-dispatch"></a>

## Step 4 — Accept and dispatch

- Diagram n7 calls Push/Email only if action is Send; request has no action or schedule field.
- DERIVED proposal: POST creates and enqueues immediate dispatch because purpose is create/send and response is 202 accepted.
- Accept only after the logical request is durably queued; queue/outbox/Operation store is SOURCE_REQUIRED.
- 202 means accepted for processing, not provider delivery success.
- 503 before acceptance is a plausible dependency trigger, not a verified branch.
- Provider failure after 202 belongs to delivery lifecycle; #96 status aggregation is SOURCE_REQUIRED.
- API Guidelines recommend Idempotency-Key for retryable mutations; #93 does not declare that header.
- See [Q-93-05](./OPEN_QUESTIONS.md#q-93-05-create-draft-or-send).

<a id="step-5-map-response"></a>

## Step 5 — Map response

| Path | Logical source | Rule/status |
|---|---|---|
| success | Accepted branch | true by envelope convention |
| businessCode | Catalog | DESIGN_OPERATION_ACCEPTED DIRECT |
| data.id | Notification | int64; allocator SOURCE_REQUIRED |
| data.title | Request title | Logical copy; storage projection SOURCE_REQUIRED |
| data.content | Request content | Logical copy; storage projection SOURCE_REQUIRED |
| data.channels[] | Request | Enum/storage SOURCE_REQUIRED |
| data.status | NotificationStatus | Initial value SOURCE_REQUIRED |
| data.read_at | Optional field | Value/omit rule SOURCE_REQUIRED |
| data.scheduled_at | Optional field | No request input; mapping SOURCE_REQUIRED |
| data.created_at | Persistence clock | Timezone/precision SOURCE_REQUIRED |
| meta/traceId | Envelope/request context | Shape/route wiring not verified |

- Operation summary conflicts with the direct Notification response; do not add Operation fields.

<a id="step-6-return-result-or-error"></a>

## Step 6 — Return result or error

- Success: HTTP 202 DESIGN_OPERATION_ACCEPTED.
- Keep only catalog errors 401, 403, 422, 503 and 500.
- Validation, permission, queue, rollback and envelope details remain unresolved.
- See [06_Error.md](./06_Error.md); never expose secrets, raw SQL or stack traces.
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
