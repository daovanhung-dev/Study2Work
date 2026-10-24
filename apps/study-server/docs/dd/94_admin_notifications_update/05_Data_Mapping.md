---
title: "Data Mapping"
order: 5
dd_id: "94"
api_name: "Admin cập nhật notification"
source_sheet: "3. Data mapping"
format: markdown
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

1. Xác thực token và kiểm tra Admin notification-management permission.
2. Đọc notification_id path; body chỉ tồn tại nếu proposal DERIVED được duyệt.
3. Nạp target notification và kiểm tra lifecycle eligibility sau khi có status model được duyệt.
4. Nếu audience được đổi theo proposal, resolve selector và cập nhật association bằng transaction được owner xác nhận.
5. Cập nhật Notification fields theo approved mapping; không giả định scheduler enqueue/cancel.
6. Map đúng ApiEnvelope<Notification> và HTTP 200 success hoặc error code catalog.

### Mục lục

- [Step 0 — Authentication and permission](#step-0-authentication-and-permission)
- [Step 1 — Read request](#step-1-read-request)
- [Step 2 — Resolve target and audience](#step-2-resolve-target-and-audience)
- [Step 3 — Update Notification](#step-3-update-notification)
- [Step 4 — Scheduler boundary](#step-4-scheduler-boundary)
- [Step 5 — Map response](#step-5-map-response)
- [Step 6 — Return result or error](#step-6-return-result-or-error)

<a id="step-0-authentication-and-permission"></a>
## Step 0 — Authentication and permission

- Direct auth: Bearer JWT; catalog role Admin.
- AC-36 permission: notification-management permission.
- Resolve principal/permission using approved Study policy before any resource mutation.
- Admin claims, permission key, scope and audit actor column are SOURCE_REQUIRED.
- Missing/invalid auth maps to catalog 401; authenticated but unauthorized maps to catalog 403.

<a id="step-1-read-request"></a>
## Step 1 — Read request

| Input | Direct source | Use | Validation/source boundary |
|---|---|---|---|
| notification_id | Path int64! | Identify notification target | Parse/range and physical key mapping beyond int64 SOURCE_REQUIRED |
| recipients | No direct body field | Proposed explicit audience selector | DERIVED; rules require owner approval |
| segment | No direct body field | Proposed segment selector | DERIVED; enum and expansion SOURCE_REQUIRED |
| title | No direct body field | Proposed full replacement title | DERIVED; blank/length rules SOURCE_REQUIRED |
| content | No direct body field | Proposed full replacement content | DERIVED; blank/length rules SOURCE_REQUIRED |
| channels | No direct body field | Proposed full replacement channel set | DERIVED; tokens and projection SOURCE_REQUIRED |
| scheduled_at | No direct body field | Proposed schedule update | DERIVED; timezone/state/queue effects SOURCE_REQUIRED |
| Query parameters | None declared | No query lookup/filter | N/A |

<a id="step-2-resolve-target-and-audience"></a>
## Step 2 — Resolve target and audience

1. Resolve the notification by notification_id from an owner-approved Admin persistence model.
2. If no target exists, catalog provides 404 DESIGN_RESOURCE_NOT_FOUND; exact lookup source is not yet available.
3. If Draft/Scheduled editability is approved, read status and apply the owner-approved state rule before mutation.
4. If audience input is approved, accept exactly one of recipients or segment as a DERIVED proposal.
5. Resolve recipients/segment only through an approved membership source and eligibility predicate.
6. No SELECT SQL or physical relation can be specified from current sources.

### Query matrix

| Query ID | Purpose | Physical source/columns | Predicate | Status |
|---|---|---|---|---|
| Q1 | Load target Notification | Approved Admin table not found | Logical ID equals path notification_id | SOURCE_REQUIRED; no SQL invented |
| Q2 | Check editable lifecycle state | Status column/model not approved | Draft/Scheduled conceptual guard is a proposal | DERIVED / SOURCE_REQUIRED |
| Q3 | Resolve explicit recipients or segment | Admin audience and recipient relation not found | Selector and membership predicate unresolved | SOURCE_REQUIRED |

<a id="step-3-update-notification"></a>
## Step 3 — Update Notification

- AC-36 direct intent: update Notification.
- Proposed update inputs: title, content, channels, scheduled_at; each is DERIVED because direct request body is absent.
- Preserve id and created_at; do not update read_at or infer a read-state change.
- Do not map channels to legacy type, status to is_read, or scheduled_at to another timestamp.
- Transaction owner, audit, updated timestamp, optimistic-lock policy and rollback are SOURCE_REQUIRED.

### Mutation matrix

| Operation | Target | Fields/condition | Transaction/failure | Status |
|---|---|---|---|---|
| M1 UPDATE | Logical Notification | Proposed title, content, channels, scheduled_at; editable-state check only if approved | Physical target, audit, timestamp and atomicity unknown | Intent DIRECT; field set DERIVED; mapping SOURCE_REQUIRED |
| M2 replace audience | Logical recipient association | Proposed recipients or segment, exactly one | Existing delivery/history handling and transaction unknown | DERIVED; no physical relation |
| M3 scheduler update | No approved target | No enqueue/cancel/retry operation defined | Do not report a scheduler side effect | SOURCE_REQUIRED; not included as executable mutation |

<a id="step-4-scheduler-boundary"></a>
## Step 4 — Scheduler boundary

- AC-36 does not say that PUT enqueues, cancels or dispatches delivery work.
- A changed scheduled_at may require scheduler coordination, but no scheduler API, queue contract, operation ID or persistence source is available.
- Do not claim that this update has taken effect on queued jobs until the owner defines that contract.

<a id="step-5-map-response"></a>
## Step 5 — Map response

| Response field | Logical source | Mapping rule | Status |
|---|---|---|---|
| id | Target Notification | Preserve target identity | DIRECT type; physical source unresolved |
| title | Proposed request | Return approved persisted value | DERIVED / SOURCE_REQUIRED |
| content | Proposed request | Return approved persisted value | DERIVED / SOURCE_REQUIRED |
| channels[] | Proposed request | Return approved enum values | DERIVED / SOURCE_REQUIRED |
| status | Lifecycle state | Use owner-approved state/token | SOURCE_REQUIRED |
| read_at? | Existing notification state | Preserve; this API does not mark read | SOURCE_REQUIRED |
| scheduled_at? | Proposed request/state | Omit/null semantics unresolved | DERIVED / SOURCE_REQUIRED |
| created_at | Existing notification state | Preserve original timestamp | SOURCE_REQUIRED |
| businessCode | Catalog | DESIGN_RESOURCE_UPDATED | DIRECT |
| traceId | Request context | Propagate shared trace convention | Convention; route absent |

<a id="step-6-return-result-or-error"></a>
## Step 6 — Return result or error

- Direct success: HTTP 200 DESIGN_RESOURCE_UPDATED, ApiEnvelope<Notification>.
- Exact direct errors: 401 DESIGN_AUTHENTICATION_REQUIRED, 403 DESIGN_ACCESS_DENIED, 404 DESIGN_RESOURCE_NOT_FOUND, 422 DESIGN_VALIDATION_ERROR, 500 DESIGN_INTERNAL_ERROR.
- Do not add 409/503 or other code from a generic scheduler assumption.
- Field-level 422 and lifecycle rejection triggers require approval; catalog only fixes the available error contract.
- Do not expose SQL, stack trace, provider details, recipient personal data or internal queue IDs.

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
