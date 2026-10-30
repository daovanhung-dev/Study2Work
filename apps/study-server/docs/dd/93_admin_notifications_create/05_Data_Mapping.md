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
4. [Step 3 — Create Notification and delivery rows](#step-3-create-notification-and-delivery-rows)
5. [Step 4 — Accept and dispatch](#step-4-accept-and-dispatch)
6. [Step 5 — Map response](#step-5-map-response)
7. [Step 6 — Return result or error](#step-6-return-result-or-error)

<a id="step-0-authentication-and-permission"></a>

## Step 0 — Authentication and permission

- Shared `validate_current_user_request(..., role="ADMIN")` runs before body parsing or recipient queries.
- The shared guard supplies the caller ID used as `sender_id`. No fine-grained notification permission is source-backed or checked.
- Local fake-DB HTTP tests cover 401/403 ordering; no live token, database, or deployment check was run.
- Error: [06_Error.md](./06_Error.md#error-401).

<a id="step-1-read-request"></a>

## Step 1 — Read request

| Input | Direct type | Runtime behavior | Status |
|---|---|---|---|
| recipients | Optional int64[] | Required by fallback; non-empty, positive, unique IDs | DERIVED |
| segment | Optional AudienceSegment | Rejected when supplied | DERIVED; values and expansion predicate SOURCE_REQUIRED |
| title | Required string | Nonblank; at most 200 characters | DERIVED from legacy DDL candidate |
| content | Required string | Nonblank; no maximum added | DERIVED |
| channels | Required NotificationChannel[] | Non-empty unique `PUSH` / `EMAIL` | DERIVED from diagram and outbox candidate |

- Preserve request field names and requiredness in the direct contract.
- Unknown fields, invalid JSON, and wrong types return catalog 422. Strings are checked for blankness but otherwise preserved.
- No action, `scheduled_at`, `operation_id`, or `Idempotency-Key` is added to the request.

<a id="step-2-resolve-audience"></a>

## Step 2 — Resolve audience

- Runtime uses only the explicit recipient IDs; it does not infer a default audience or expand segments.
- Query `FIND_ADMIN_NOTIFICATION_RECIPIENTS` selects matching `users.id` values for the supplied IDs. A missing ID returns one generic 422 without identifying which user is absent.
- No role, status, course, or enrollment predicate is added. Fan-out follows recipient request order.
- Do not copy Mentor course checks from #63 or Student ownership from #43–#45.

### Query matrix

| ID | Purpose | Type/source | Columns/conditions | Pagination | Status |
|---|---|---|---|---|---|
| Q1 | Verify explicit recipient IDs exist | `users` legacy schema candidate | `id = ANY(:recipient_ids)` | N/A | Wired locally; candidate schema only |
| Q2 | Read Operation if response uses it | No Study Operation store found | API #18 ID/owner conflict | N/A | SOURCE_REQUIRED |

<a id="step-3-create-notification-and-delivery-rows"></a>

## Step 3 — Create Notification and delivery rows

- AC-36 node n6 requires logical Notification + recipients. Local fallback uses the checked-in legacy BIGINT candidate, one notification row per recipient.
- Insert `user_id`, `sender_id`, `title`, `content`, `type=NULL`, `is_read=FALSE`, `created_at=CURRENT_TIMESTAMP`, and one shared UUID `operation_id`; read `id` and `created_at` with `RETURNING`.
- For each inserted notification, insert one `notification_deliveries` row per requested channel with status `QUEUED`, `queued_at=CURRENT_TIMESTAMP`, and `updated_at=CURRENT_TIMESTAMP`.
- Candidate DDL is checked in but live schema, ownership approval, and worker availability are not verified. Do not use V1-PILOT UUID learner tables.
- See [07_table.md](./07_table.md), [08 recipient mapping](./08_notification_recipients_insert.md), and [09 delivery mapping](./09_notification_deliveries_insert.md).

### Mutation matrix

| ID | Logical operation | Target | Fields/source | Transaction/failure | Mapping |
|---|---|---|---|---|---|
| M1 | INSERT one Notification per recipient | `notifications` candidate | `user_id`, `sender_id`, `title`, `content`, `type=NULL`, `is_read=FALSE`, timestamp, shared UUID | Same DB transaction | [07_table.md](./07_table.md) |
| M2 | Associate recipient | `notifications.user_id` candidate | One recipient key on each notification row | Same DB transaction | [08 mapping](./08_notification_recipients_insert.md) |
| M3 | INSERT delivery outbox rows | `notification_deliveries` candidate | One row per created notification × requested channel; `QUEUED` | Same DB transaction | [09 mapping](./09_notification_deliveries_insert.md) |

<a id="step-4-accept-and-dispatch"></a>

## Step 4 — Accept and dispatch

- DERIVED fallback: POST creates outbox rows for immediate asynchronous Push/Email intent because the diagram has CREATE/SEND and response is 202 accepted. Request has no draft/action/schedule field.
- The transaction commits only after all notification/outbox inserts and response projection succeed. 202 means rows committed locally, not provider delivery success.
- No provider or worker call is wired by this endpoint. The checked-in outbox DDL is not evidence that a worker consumes it.
- SQL `OperationalError` or invalidated DB connection maps to 503; other SQL, mapping, or commit failures map to 500. The view attempts rollback before returning an error.
- See [Q-93-05](./OPEN_QUESTIONS.md#q-93-05-create-draft-or-send) and [Q-93-07](./OPEN_QUESTIONS.md#q-93-07-acceptance-and-operation-lifecycle).

<a id="step-5-map-response"></a>

## Step 5 — Map response

| Path | Logical source | Rule/status |
|---|---|---|
| success | Accepted branch | true by envelope convention |
| businessCode | Catalog | `DESIGN_OPERATION_ACCEPTED` DIRECT |
| data | First Notification row in recipient request order | Endpoint-specific direct shape; batch projection DERIVED |
| data.id | First `notifications.id` | BIGINT/int64 from `RETURNING`; candidate only |
| data.title/content | Request | Preserved in response and insert bindings |
| data.channels[] | Request | `PUSH` / `EMAIL`; DERIVED enum fallback |
| data.status | Delivery outbox state | `QUEUED`; DERIVED Notification projection |
| data.read_at/scheduled_at | No source/input | Omitted |
| data.created_at | First row | Database-returned timestamp |
| meta.operation_id | App-generated UUID | Persisted on each notification row; DERIVED handoff |
| meta.notification_ids[] | All created rows | int64 IDs in recipient request order; DERIVED batch metadata |
| traceId | Request context | Propagated by response helper |

- Operation tracking prose still conflicts with the direct Notification response. Local fallback retains Notification and adds derived batch metadata; owner decision remains open.
- `data` represents only the first recipient row. Consumers needing every created row must use `meta.notification_ids` while this DERIVED response remains in place.

<a id="step-6-return-result-or-error"></a>

## Step 6 — Return result or error

- Success: HTTP 202 `DESIGN_OPERATION_ACCEPTED` after commit.
- Keep only catalog errors 401, 403, 422, 503, and 500.
- Validation predicates and the 503 trigger are local DERIVED behavior; permission remains the shared ADMIN role guard only.
- Do not expose secrets, raw SQL, recipient values, or stack traces.
- See [06_Error.md](./06_Error.md).

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
