---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
dd_id: "API-IAM-021"
status: "PARTIALLY COMPLETED — SOURCE GAPS"
---

# Data Mapping

## Flow xử lý data

## 0. Check quyền

### 0.1. Thực hiện check quyền

- Lấy access/refresh credential theo [03_Request.md](./03_Request.md).
- Xác thực token/session; access JWT kiểm `iss`, `aud`, `exp`, `nbf`, `jti`, `sid`, `authVersion` theo nguồn canonical.
- Kiểm account/projection còn `ACTIVE` khi endpoint yêu cầu.
- Kiểm permission `PERM-IAM-001` server-side.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| `identity_db` | `principal/resource scope` | ``PERM-IAM-001`` | Không dùng frontend guard làm hàng rào bảo mật |

### 0.3. Check kết quả

- Nếu authentication/authorization hợp lệ: tiếp tục xử lý.
- Nếu không hợp lệ: trả error branch tương ứng trong [06_Error.md](./06_Error.md).

## 1. Validate data input

- `Header.Authorization`: required=`Yes`, type=`string`, format=`Bearer token`, valid=`N/A`; basis=`DIRECT`.
- `Query.page`: required=`No`, type=`integer`, format=`integer`, valid=`N/A`; basis=`DIRECT`.
- `Query.pageSize`: required=`No`, type=`integer`, format=`integer`, valid=`N/A`; basis=`DIRECT`.
- `Query.status`: required=`No`, type=`string`, format=`N/A`, valid=`account_status`; basis=`DIRECT`.
- `Query.emailHash`: required=`No`, type=`string`, format=`exact hash`, valid=`N/A`; basis=`DERIVED`.
- `Query.role`: required=`No`, type=`string`, format=`role code`, valid=`N/A`; basis=`DIRECT`.
- Normalize email: trim Unicode và lowercase canonical trước compare; không log raw email trong rate key/audit.

## 2. Get thông tin

### 2.1. Query `TBL-IAM-001 — users`

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| `users AS t_users` | `t_users.id` | `id` | `DIRECT` |
| `users AS t_users` | `t_users.status` | `status` | `DIRECT` |
| `users AS t_users` | `t_users.row_version` | `row_version` | `DIRECT` |
| `users AS t_users` | `t_users.email_verified_at` | `email_verified_at` | `DIRECT` |
| `users AS t_users` | `t_users.privileged_mfa_required` | `privileged_mfa_required` | `DIRECT` |
| `users AS t_users` | `t_users.deletion_requested_at` | `deletion_requested_at` | `DIRECT` |
| `users AS t_users` | `t_users.anonymized_at` | `anonymized_at` | `DIRECT` |

**WHERE / predicate cho `users`**

- Owner/subject ID lấy từ token/session hoặc endpoint-specific lookup.
- Lock: `FOR UPDATE`/advisory lock chỉ khi endpoint source yêu cầu; exact lock scope nêu tại transaction section.

### 2.2. Query `TBL-IAM-002 — user_emails`

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| `user_emails AS t_useremai` | `t_useremai.id` | `id` | `DIRECT` |
| `user_emails AS t_useremai` | `t_useremai.user_id` | `user_id` | `DIRECT` |
| `user_emails AS t_useremai` | `t_useremai.email_normalized` | `email_normalized` | `DIRECT` |
| `user_emails AS t_useremai` | `t_useremai.is_primary` | `is_primary` | `DIRECT` |
| `user_emails AS t_useremai` | `t_useremai.verified_at` | `verified_at` | `DIRECT` |
| `user_emails AS t_useremai` | `t_useremai.replaced_at` | `replaced_at` | `DIRECT` |

**WHERE / predicate cho `user_emails`**

- Owner/subject ID lấy từ token/session hoặc endpoint-specific lookup.

### 2.3. Query `TBL-IAM-015 — user_role_assignments`

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| `user_role_assignments AS t_userrole` | `t_userrole.user_id` | `user_id` | `DIRECT` |
| `user_role_assignments AS t_userrole` | `t_userrole.role_id` | `role_id` | `DIRECT` |
| `user_role_assignments AS t_userrole` | `t_userrole.valid_from` | `valid_from` | `DIRECT` |
| `user_role_assignments AS t_userrole` | `t_userrole.valid_until` | `valid_until` | `DIRECT` |
| `user_role_assignments AS t_userrole` | `t_userrole.revoked_at` | `revoked_at` | `DIRECT` |

**WHERE / predicate cho `user_role_assignments`**

- Điều kiện cụ thể theo endpoint summary và khóa/index canonical; exact SQL giữ `DERIVED` nếu catalog không nêu field-level.

### 2.4. Query `TBL-IAM-012 — roles`

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| `roles AS t_roles` | `t_roles.id` | `id` | `DIRECT` |
| `roles AS t_roles` | `t_roles.code` | `code` | `DIRECT` |
| `roles AS t_roles` | `t_roles.is_privileged` | `is_privileged` | `DIRECT` |
| `roles AS t_roles` | `t_roles.disabled_at` | `disabled_at` | `DIRECT` |

**WHERE / predicate cho `roles`**

- Điều kiện cụ thể theo endpoint summary và khóa/index canonical; exact SQL giữ `DERIVED` nếu catalog không nêu field-level.

<a id="3-insertupdate-thong-tin"></a>
## 3. Insert/Update thông tin

### 3.1. Target table

- `TBL-IAM-017 — security_audit_events` operation `INSERT`.

### 3.2. Conditions

- `BEGIN TRANSACTION` sau khi validation/business checks/idempotency claim hoàn tất.
- Transaction chỉ bao phủ một database owner.
- Không gọi email/KMS/HTTP/provider trong transaction; side effect dùng outbox.

### 3.3. Items update/insert

- `INSERT security_audit_events`: refer [07_security_audit_events_insert.md](./07_security_audit_events_insert.md).

### 3.4. Parameters

| Param | Giá trị | Remarks |
|---|---|---|
| `security_audit_events.id` | `Generated UUID v7` | `DIRECT` |
| `security_audit_events.occurred_at` | `current_timestamp` | `DIRECT` |
| `security_audit_events.actor_id` | `token/session actor hoặc NULL cho anonymous` | `DIRECT` |
| `security_audit_events.subject_id` | `subject user ID khi có` | `DIRECT` |
| `security_audit_events.action` | `Endpoint-specific action` | `DIRECT` |
| `security_audit_events.outcome` | `SUCCESS/DENIED/FAILURE` | `DIRECT` |
| `security_audit_events.reason_code` | `Branch business code hoặc NULL` | `DIRECT` |
| `security_audit_events.trace_id` | `request.traceId` | `DIRECT` |
| `security_audit_events.session_id` | `current session ID hoặc NULL` | `DIRECT` |
| `security_audit_events.ip_hash` | `hash(request IP) hoặc NULL` | `DIRECT` |
| `security_audit_events.user_agent_hash` | `hash(User-Agent) hoặc NULL` | `DIRECT` |
| `security_audit_events.metadata` | `Redacted metadata JSON` | `DIRECT` |
| `security_audit_events.prev_hash` | `Previous chain hash hoặc NULL` | `DIRECT` |
| `security_audit_events.event_hash` | `Hash canonical event payload` | `DIRECT` |
| `security_audit_events.legal_hold_until` | `NULL trừ source approved` | `DIRECT` |

- Nếu tất cả mutation thành công: `COMMIT`.
- Nếu có business/system failure sau khi transaction bắt đầu: `ROLLBACK` toàn bộ domain mutation, audit/outbox trong boundary.

## 4. Check kết quả execute query

### 4.1. Thành công

- `HTTPStatus = 200`.
- `success = true`.
- `businessCode = SOURCE_REQUIRED` nếu success catalog chưa định nghĩa.
- Map từng response path theo [04_Response.md](./04_Response.md).
- `meta` luôn là object.
- `traceId` lấy từ request context.

### 4.2. Lỗi hệ thống

- `ROLLBACK` nếu transaction đã bắt đầu.
- `HTTPStatus = 500`.
- Không trả stack trace, SQL, token, secret hoặc private key reference.
- Refer [06_Error.md](./06_Error.md).

### 4.3. Validate lỗi

- Trả HTTP status/business code theo từng row trong [06_Error.md](./06_Error.md).
- Field-level error đặt tại `meta.fieldErrors` khi source định nghĩa field cụ thể.

### 4.4. Ngoài trường hợp trên

- Không silently ignore filter/field không được hỗ trợ.
- Gap `SOURCE_REQUIRED`, `CONFLICT` hoặc `NEEDS USER DECISION` không được biến thành runtime contract.

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
