---
title: "Data Mapping"
order: 5
dd_id: "95"
api_name: "Admin xóa hoặc hủy notification"
source_sheet: "3. Data mapping"
format: markdown
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

1. Authenticate Bearer JWT and authorize Admin notification-management permission.
2. Read notification_id; the request has no body or query.
3. Load the target using an owner-approved Admin notification persistence model.
4. Evaluate lifecycle and delivery-start eligibility only from an approved status/aggregate source.
5. If the approved policy allows action, logically remove a draft or mark an eligible scheduled notification cancelled; retain delivery history.
6. If scheduled jobs exist, coordinate cancellation only through an approved scheduler contract; no such runtime call is currently source-backed.
7. Return the exact DeleteResult envelope on success, otherwise one of the catalog error codes.

### Mục lục

- [Step 0 — Authentication and permission](#step-0-authentication-and-permission)
- [Step 1 — Read request](#step-1-read-request)
- [Step 2 — Resolve notification and eligibility](#step-2-resolve-notification-and-eligibility)
- [Step 3 — Apply logical delete/cancel](#step-3-apply-logical-deletecancel)
- [Step 4 — Scheduler boundary](#step-4-scheduler-boundary)
- [Step 5 — Map DeleteResult](#step-5-map-deleteresult)
- [Step 6 — Return result or error](#step-6-return-result-or-error)

<a id="step-0-authentication-and-permission"></a>
## Step 0 — Authentication and permission

- Direct auth: Bearer JWT; catalog role Admin.
- AC-36 requires notification-management permission.
- Resolve the principal and policy through an approved Admin guard before target lookup/mutation.
- Missing/invalid credentials map to 401; denied role/permission maps to 403 using direct catalog codes.
- Claim mapping, tenant/global scope and authorization/404 precedence are SOURCE_REQUIRED.

<a id="step-1-read-request"></a>
## Step 1 — Read request

| Input | Direct source | Use | Validation/source boundary |
|---|---|---|---|
| notification_id | Path int64! | Identify target notification | Positive range, parser behavior and physical key mapping SOURCE_REQUIRED |
| Body | None | No action/reason/policy flag is accepted | N/A |
| Query | None | No selector or filter | N/A |

<a id="step-2-resolve-notification-and-eligibility"></a>
## Step 2 — Resolve notification and eligibility

1. Resolve the target in an owner-approved Admin notification model.
2. If absent, return catalog 404 DESIGN_RESOURCE_NOT_FOUND.
3. Read lifecycle and delivery state from approved source; do not infer state from #96 response because it contains only Notification.
4. Proposed rule DERIVED: conceptual Draft may be removed; conceptual Scheduled may be cancelled only if no delivery has started.
5. Proposed rule DERIVED: if delivery has started, policy disallows cancellation and the existing 422 code is returned.
6. State labels, aggregate criteria, concurrent dispatch race and repeat-request behavior remain unconfirmed.
7. No SELECT SQL can be specified from current sources.

### Query matrix

| Query ID | Purpose | Physical source/columns | Predicate | Status |
|---|---|---|---|---|
| Q1 | Load notification target | No approved Admin campaign table; legacy notifications is partial | Logical id equals path notification_id | SOURCE_REQUIRED; no SQL invented |
| Q2 | Read state and delivery-start eligibility | No approved Admin state/delivery aggregate | Draft/Scheduled and no delivery started are proposed concepts | DERIVED / SOURCE_REQUIRED |
| Q3 | Find scheduled work to cancel | Queue/scheduler/Operation source not found | No job ID or external key in request | SOURCE_REQUIRED; no current call defined |

<a id="step-3-apply-logical-deletecancel"></a>
## Step 3 — Apply logical delete/cancel

### M1 — Remove a draft from active management

- Proposed effect: record a tombstone/removal marker and retain recipient/delivery history.
- Do not physically DELETE notification, recipient or delivery rows without an approved retention policy.
- Tombstone value, timestamp column, audit and transaction are SOURCE_REQUIRED.
- Mapping details: [07_notifications_delete.md](./07_notifications_delete.md).

### M2 — Cancel an eligible scheduled notification

- Proposed effect: mark the notification cancelled before dispatch begins.
- Do not claim that an external queue or provider was cancelled unless an approved scheduler integration confirms it.
- Do not rewrite/delete delivery history. The V1-PILOT delivery table is not the Admin target and is append-only in that separate model.
- Whether cancellation and scheduler acknowledgement are atomic is unresolved.
- Mapping boundary: [08_notification_delivery_cancel.md](./08_notification_delivery_cancel.md).

### Mutation matrix

| ID | Logical operation | Condition | Fields/effect | Transaction/failure | Status |
|---|---|---|---|---|---|
| M1 | Logical draft removal | Proposed Draft state | Remove from active management; retain history | Tombstone/timestamp/transaction unknown | DERIVED; physical mapping SOURCE_REQUIRED |
| M2 | Mark scheduled notification cancelled | Proposed Scheduled and no delivery started | Record cancellation; scheduler cooperation unknown | Dispatch race and cancellation acknowledgement unresolved | DERIVED / SOURCE_REQUIRED |
| M3 | Physical cascade delete | None | No history deletion proposed | No cascade or child deletion inferred | N/A |

- Proposed repeated DELETE against an existing tombstone returns 200 with the original DeleteResult to make retries stable. This is DERIVED, not direct.
- The catalog 422 code is available for a policy rejection; the exact rejection state is not defined.

<a id="step-4-scheduler-boundary"></a>
## Step 4 — Scheduler boundary

- AC-36 shows DELETE/mark cancelled but no queue, worker, provider or scheduler call.
- If a scheduled job exists, an approved implementation must prevent later dispatch after the cancellation marker and define how in-flight sends are handled.
- The current DD does not invent an Operation ID, cancellation endpoint, retry policy or provider acknowledgement.

<a id="step-5-map-deleteresult"></a>
## Step 5 — Map DeleteResult

| Response field | Logical source | Mapping rule | Status |
|---|---|---|---|
| id | Target notification | Preserve target identity | DIRECT type; physical source unresolved |
| status | DeleteResult schema | Always literal deleted | DIRECT |
| deleted_at | Successful logical mutation | Proposed timestamp when removal/cancellation commits | DIRECT field; time source/persistence SOURCE_REQUIRED |
| businessCode | Catalog | DESIGN_RESOURCE_DELETED | DIRECT |
| traceId | Request context | Propagate shared trace convention | Convention; route absent |

- For a scheduled cancellation, the response status literal remains deleted because catalog fixes it; do not serialize NotificationStatus here.
- If a repeat-delete no-op is approved, return the original persisted deleted_at rather than generating a new one.

<a id="step-6-return-result-or-error"></a>
## Step 6 — Return result or error

- Direct success: HTTP 200 DESIGN_RESOURCE_DELETED, ApiEnvelope<DeleteResult>.
- Exact direct errors: 401 DESIGN_AUTHENTICATION_REQUIRED, 403 DESIGN_ACCESS_DENIED, 404 DESIGN_RESOURCE_NOT_FOUND, 422 DESIGN_VALIDATION_ERROR, 500 DESIGN_INTERNAL_ERROR.
- Do not add 409, 410 or 503 for scheduler/policy assumptions.
- Return 422 for disallowed state only as the stated DERIVED policy proposal; catalog does not define its trigger.
- Do not return recipient PII, provider errors, queue identifiers, SQL or stack traces.

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
