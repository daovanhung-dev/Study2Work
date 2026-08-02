---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
dd_id: "API-IAM-020"
status: "NEEDS USER DECISION — Draft"
---

# Data Mapping

## Flow xử lý data

## 0. Check quyền

### 0.1. Thực hiện check quyền

- Lấy access/refresh credential theo [03_Request.md](./03_Request.md).
- Xác thực token/session; access JWT kiểm `iss`, `aud`, `exp`, `nbf`, `jti`, `sid`, `authVersion` theo nguồn canonical.
- Kiểm account/projection còn `ACTIVE` khi endpoint yêu cầu.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| `identity_db` | `principal/resource scope` | `Authenticated via recovery flow` | Không dùng frontend guard làm hàng rào bảo mật |

### 0.3. Check kết quả

- Nếu authentication/authorization hợp lệ: tiếp tục xử lý.
- Nếu không hợp lệ: trả error branch tương ứng trong [06_Error.md](./06_Error.md).

## 1. Validate data input

- `Header.Idempotency-Key`: required=`Yes`, type=`string`, format=`UUID/random`, valid=`N/A`; basis=`DIRECT`.
- `Body.SOURCE_REQUIRED`: required=`Yes`, type=`string`, format=`recovery flow proof`, valid=`N/A`; basis=`SOURCE_REQUIRED`.
- Không triển khai field `SOURCE_REQUIRED` trước khi source gap được quyết định.
- Hash `Idempotency-Key`; claim key trước domain mutation. Cùng key khác request hash trả `IDEMPOTENCY_KEY_REUSED`; request đang chạy trả `REQUEST_IN_PROGRESS`.

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

<a id="3-insertupdate-thong-tin"></a>
## 3. Insert/Update thông tin

### 3.1. Target table

- `TBL-IAM-001 — users` operation `UPDATE`.
- `TBL-IAM-009 — auth_sessions` operation `INSERT`.
- `TBL-IAM-010 — refresh_tokens` operation `INSERT`.
- `TBL-IAM-016 — idempotency_keys` operation `INSERT`.
- `TBL-IAM-017 — security_audit_events` operation `INSERT`.
- `TBL-IAM-018 — outbox_events` operation `INSERT`.

### 3.2. Conditions

- `BEGIN TRANSACTION` sau khi validation/business checks/idempotency claim hoàn tất.
- Transaction chỉ bao phủ một database owner.
- Không gọi email/KMS/HTTP/provider trong transaction; side effect dùng outbox.

### 3.3. Items update/insert

- `UPDATE users`: refer [07_users_update.md](./07_users_update.md).
- `INSERT auth_sessions`: refer [08_auth_sessions_insert.md](./08_auth_sessions_insert.md).
- `INSERT refresh_tokens`: refer [09_refresh_tokens_insert.md](./09_refresh_tokens_insert.md).
- `INSERT idempotency_keys`: refer [10_idempotency_keys_insert.md](./10_idempotency_keys_insert.md).
- `INSERT security_audit_events`: refer [11_security_audit_events_insert.md](./11_security_audit_events_insert.md).
- `INSERT outbox_events`: refer [12_outbox_events_insert.md](./12_outbox_events_insert.md).

### 3.4. Parameters

| Param | Giá trị | Remarks |
|---|---|---|
| `users.status` | `ACTIVE` | `DIRECT` |
| `users.deletion_requested_at` | `NULL` | `DIRECT` |
| `users.updated_at` | `current_timestamp` | `DIRECT` |
| `users.row_version` | `row_version + 1` | `DIRECT` |
| `auth_sessions.id` | `Generated UUID v7` | `DIRECT` |
| `auth_sessions.created_at` | `current_timestamp` | `DIRECT` |
| `auth_sessions.updated_at` | `current_timestamp` | `DIRECT` |
| `auth_sessions.row_version` | `1` | `DIRECT` |
| `auth_sessions.user_id` | `Recovered users.id` | `DIRECT` |
| `auth_sessions.status` | `ACTIVE` | `DIRECT` |
| `auth_sessions.session_epoch` | `SOURCE_REQUIRED` | `DIRECT` |
| `auth_sessions.last_seen_at` | `current_timestamp` | `DIRECT` |
| `auth_sessions.expires_at` | `Session expiry policy` | `DIRECT` |
| `refresh_tokens.id` | `Generated UUID v7` | `DIRECT` |
| `refresh_tokens.created_at` | `current_timestamp` | `DIRECT` |
| `refresh_tokens.session_id` | `Created session ID` | `DIRECT` |
| `refresh_tokens.family_id` | `Generated UUID v7` | `DIRECT` |
| `refresh_tokens.token_hash` | `Hash generated token` | `DIRECT` |
| `refresh_tokens.status` | `ACTIVE` | `DIRECT` |
| `refresh_tokens.issued_at` | `current_timestamp` | `DIRECT` |
| `refresh_tokens.expires_at` | `Policy expiry` | `DIRECT` |
| `idempotency_keys.id` | `Generated UUID v7` | `DIRECT` |
| `idempotency_keys.created_at` | `current_timestamp` | `DIRECT` |
| `idempotency_keys.updated_at` | `current_timestamp` | `DIRECT` |
| `idempotency_keys.row_version` | `1` | `DIRECT` |
| `idempotency_keys.actor_id` | `Authenticated actor ID hoặc NULL` | `DIRECT` |
| `idempotency_keys.operation` | `method + normalized path` | `DIRECT` |
| `idempotency_keys.key_hash` | `Hash(Idempotency-Key)` | `DIRECT` |
| `idempotency_keys.request_hash` | `Hash(canonical request)` | `DIRECT` |
| `idempotency_keys.response_status` | `NULL until complete` | `DIRECT` |
| `idempotency_keys.response_body` | `NULL until complete` | `DIRECT` |
| `idempotency_keys.locked_until` | `current_timestamp + processing lease` | `DIRECT` |
| `idempotency_keys.completed_at` | `NULL until complete` | `DIRECT` |
| `idempotency_keys.expires_at` | `Retention from API/global policy` | `DIRECT` |
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
| `outbox_events.id` | `Generated UUID v7` | `DIRECT` |
| `outbox_events.created_at` | `current_timestamp` | `DIRECT` |
| `outbox_events.aggregate_type` | `Endpoint aggregate type` | `DIRECT` |
| `outbox_events.aggregate_id` | `Domain aggregate ID` | `DIRECT` |
| `outbox_events.event_type` | `Event type từ API source` | `DIRECT` |
| `outbox_events.event_version` | `SOURCE_REQUIRED — Q-15` | `DIRECT` |
| `outbox_events.payload` | `SOURCE_REQUIRED — Q-15, redacted JSON` | `DIRECT` |
| `outbox_events.available_at` | `current_timestamp` | `DIRECT` |
| `outbox_events.dedupe_key` | `Generated business dedupe key` | `DIRECT` |
| `outbox_events.trace_id` | `request.traceId` | `DIRECT` |

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
