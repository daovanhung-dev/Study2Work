---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
---

# Data Mapping

## Flow xử lý data

### Mục lục

- [0. Check quyền](#dm-0-1)
- [1. Validate data input](#dm-1-1)
- [2. Get thông tin](#dm-2-1)
- [3. Insert/Update thông tin](#dm-3-1)
- [4. Check kết quả execute query](#dm-4-1)
- [5. Reconciliation matrices](#dm-5-1)

## 0. Check quyền

<a id="dm-0-1"></a>

### 0.1. Thực hiện check quyền

- Endpoint được catalog là anonymous.
- Không có Authorization/session header trong contract.
- `RESEND_COOLDOWN` chỉ được lộ khi ownership đã chứng minh, nhưng ownership proof contract SOURCE_REQUIRED.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
| --- | --- | --- | --- |
| N/A | N/A | Anonymous generic flow | Ownership-proven cooldown branch chưa implementable. |

### 0.3. Check kết quả

- Anonymous caller luôn đi generic accepted response đối với unknown/non-pending/cooldown account.
- Chỉ phát `RESEND_COOLDOWN` khi source bổ sung ownership proof mechanism.

## 1. Validate data input

<a id="dm-1-1"></a>

### 1.1. Nhận request

- `content_type = request.header["Content-Type"]`.
- `email_raw = request.body["email"]`.
- `trace_id = request_context.trace_id`.
- `request_ip_hash = HASH(request_context.ip)`.

<a id="dm-1-2"></a>

### 1.2. Normalize và validate email

- `email_trimmed = unicode_trim(email_raw)`.
- `email_normalized = lowercase_for_comparison(normalize_email_domain(email_trimmed))`.
- Nếu email thiếu hoặc malformed: public response/error policy SOURCE_REQUIRED; Draft Error ghi validation 400 nhưng không được coi Final.
- `email_hash = HASH(email_normalized)`.

<a id="dm-1-3"></a>

### 1.3. Rate limit

- Kiểm `3 request/giờ/email hash`.
- Không lưu raw email trong rate key.
- Nếu vượt giới hạn: HTTP `429`; businessCode SOURCE_REQUIRED.

## 2. Get thông tin

<a id="dm-2-1"></a>

### 2.1. Query

**Q-IAM003-01 — Resolve active email and account status**

| Target table | Column get | Chú thích | Remarks |
| --- | --- | --- | --- |
| `user_emails AS ue` | `ue.id` | Email ID | Active primary lookup. |
| `↑` | `ue.user_id` | User ID |  |
| `↑` | `ue.email_normalized` | Normalized email | Never response. |
| `users AS u` | `u.status` | Account status | Used only internally. |

### 2.2. JOIN

| Target table | Join condition | Join type |
| --- | --- | --- |
| `user_emails AS ue` | `N/A` | `BASE` |
| `users AS u` | `u.id = ue.user_id` | `INNER JOIN` |

### 2.3. WHERE

- `ue.email_normalized = email_normalized`.
- `ue.replaced_at IS NULL`.

### 2.4. ORDER BY

- N/A — active normalized email is unique.

<a id="dm-2-2"></a>

### 2.5. Query latest REGISTER token

- Chỉ chạy nếu account tồn tại và `u.status = PENDING_EMAIL_VERIFICATION`.
- Base table: `email_verification_tokens AS evt`.
- Selected columns:
  - `evt.id`.
  - `evt.status`.
  - `evt.created_at`.
  - `evt.expires_at`.
  - `evt.revoked_at`.
- WHERE mỗi condition:
  - `evt.user_id = ue.user_id`.
  - `evt.email_id = ue.id`.
  - `evt.purpose = "REGISTER"`.
  - `evt.status = "ACTIVE"`.
- ORDER BY `evt.created_at DESC`.
- LIMIT `1`.
- Index available: `(user_id,status,expires_at DESC)`; exact cooldown-optimal index gap noted.

<a id="dm-2-3"></a>

### 2.6. Branch account/cooldown

- IF email không tồn tại: return generic accepted; no mutation.
- IF account không pending: return generic accepted; no mutation.
- IF active token exists and `current_timestamp < evt.created_at + 10 minutes`:
  - Anonymous caller: return generic accepted.
  - Ownership-proven caller: may return `RESEND_COOLDOWN`, but proof mechanism SOURCE_REQUIRED.
- ELSE: continue conditional transaction.

## 3. Insert/Update thông tin

<a id="dm-3-1"></a>

### 3.1. Target table

- `email_verification_tokens` update old active REGISTER tokens.
- `email_verification_tokens` insert new token.
- `outbox_events` insert email delivery event.

### 3.2. Conditions

- User/email resolved internally and account status pending.
- Cooldown 10 minutes elapsed.
- Transaction uses Identity DB only.
- External email provider not called inside transaction.

### 3.3. Items update/insert

<a id="dm-3-2"></a>

#### 3.3.1. Generate new token variables

- `new_token_id = UUID_V7()`.
- `raw_token = CRYPTO_RANDOM(SOURCE_REQUIRED_LENGTH)`.
- `new_token_hash = HASH(raw_token)`; exact algorithm SOURCE_REQUIRED.
- `new_expires_at = current_timestamp + SOURCE_REQUIRED_TTL`.
- `outbox_event_id = UUID_V7()`.

<a id="dm-3-3"></a>

#### 3.3.2. BEGIN TRANSACTION and revoke old token(s)

- `BEGIN TRANSACTION`.
- Lock eligible active REGISTER token rows for the user/email.
- Update old token(s) theo [07_email_verification_tokens_update.md](./07_email_verification_tokens_update.md#db-map).
- `status = REVOKED`.
- `revoked_at = current_timestamp`.

<a id="dm-3-4"></a>

#### 3.3.3. Insert new token

- Insert new token theo [08_email_verification_tokens_insert.md](./08_email_verification_tokens_insert.md#db-map).
- Persist hash only.
- `purpose = REGISTER`.
- `status = ACTIVE`.

<a id="dm-3-5"></a>

#### 3.3.4. Insert email delivery outbox

- Insert outbox theo [09_outbox_events_insert.md](./09_outbox_events_insert.md#db-map).
- Exact event type/payload/dataschema SOURCE_REQUIRED.
- Generic domain event payload không chứa raw token.
- Secure raw token handoff to delivery worker SOURCE_REQUIRED.

<a id="dm-3-6"></a>

#### 3.3.5. COMMIT/ROLLBACK

- Nếu update old token + insert new token + outbox thành công: `COMMIT`.
- Nếu bất kỳ mutation lỗi: `ROLLBACK`; old token remains according to pre-transaction state.
- Sau COMMIT, worker sends email; delivery failure retries asynchronously and does not reveal account state to caller.

### 3.4. Parameters

| Param | Giá trị | Remarks |
| --- | --- | --- |
| `email_normalized` | Normalized request email | Internal lookup only. |
| `user_id` | Resolved user ID | Never response. |
| `email_id` | Resolved email ID | Never response. |
| `new_token_hash` | Hash raw token | Persisted. |
| `new_expires_at` | SOURCE_REQUIRED TTL | Not returned unless response contract later defines. |
| `trace_id` | Request trace | Outbox correlation. |

## 4. Check kết quả execute query

<a id="dm-4-1"></a>

### 4.1. Thành công

- Account missing, not pending, cooldown active, mutation successful: all return same generic accepted contract to anonymous caller.
- HTTP status = SOURCE_REQUIRED.
- `success = true`.
- `businessCode = SOURCE_REQUIRED`.
- `message = generic accepted localized text`.
- `data = SOURCE_REQUIRED`; Draft uses null.
- `meta = {}`.
- `traceId = trace_id`.

<a id="dm-4-2"></a>

### 4.2. Lỗi hệ thống

- Dependency failure before COMMIT: rollback and return `503 DEPENDENCY_UNAVAILABLE` if public error policy allows.
- Do not return account state, email, token/hash, SQL or stack trace.

<a id="dm-4-3"></a>

### 4.3. Validate lỗi

- Malformed email public behavior SOURCE_REQUIRED.
- Rate limit uses 429 and Retry-After when known.

<a id="dm-4-4"></a>

### 4.4. Ngoài trường hợp trên

- `RESEND_COOLDOWN` branch remains disabled/blocked until ownership proof contract exists.

<a id="dm-5-1"></a>

## 5. Reconciliation matrices

### 5.1. Request Usage Matrix

| Request field | Nguồn | Data Mapping step | Validate | SQL/Mutation usage | Branch/Loop | Response usage | Gap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Content-Type | DIRECT common | 1.1 | JSON | N/A | Validation | N/A | Error code missing |
| email | DIRECT | 1.1–2.6 | Normalize/format | user_emails/users/token lookup; rate key | Unknown/non-pending/cooldown/eligible | Never echo | Public malformed behavior + max length missing |

### 5.2. Query Matrix

| Query ID | Mục đích | Type | Base table/view | Alias | Columns | JOIN | WHERE | GROUP/HAVING | ORDER | Pagination | Lock | Result variable | Branch |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q-IAM003-01 | Resolve account | SELECT | user_emails | ue | ue.id | users u ON u.id = ue.user_id | email_normalized + replaced_at null | N/A | N/A | N/A | N/A | account_record | Unknown/pending/non-pending |
| Q-IAM003-01 | Resolve account | SELECT | users | u | u.status | same | same | N/A | N/A | N/A | N/A | account_record | same |
| Q-IAM003-02 | Latest active token | SELECT | email_verification_tokens | evt | evt.id | N/A | user_id/email_id/purpose/status | N/A | created_at DESC | LIMIT 1 | Lock only in mutation branch | latest_token | Cooldown/eligible |
| Q-IAM003-02 | Latest active token | SELECT | email_verification_tokens | evt | evt.created_at | N/A | same | N/A | same | LIMIT 1 | same | latest_token | same |

### 5.3. Mutation Matrix

| Mutation ID | Operation | Target table | Record condition | Fields | Value sources | Audit | Mapping file | Transaction | Failure behavior |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M-IAM003-01 | UPDATE | email_verification_tokens | Pending account and cooldown elapsed; active REGISTER token | Refer mapping | REVOKED/current time | No audit source | 07_email_verification_tokens_update.md | identity_db TX | Rollback |
| M-IAM003-02 | INSERT | email_verification_tokens | Same branch | Refer mapping | Generated/hash/TTL | No audit source | 08_email_verification_tokens_insert.md | identity_db TX | Rollback |
| M-IAM003-03 | INSERT | outbox_events | New token inserted | Refer mapping | SOURCE_REQUIRED delivery event | Trace linked | 09_outbox_events_insert.md | identity_db TX | Rollback |

### 5.4. Response Source Matrix

| Response field | Type | Source type | Table/column hoặc generator | Data Mapping step | Transform | Null/empty rule | Gap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| success | boolean | Fixed | Generic branch | 4.1 | true | Never null | None |
| businessCode | string | Fixed | SOURCE_REQUIRED | 4.1 | None | Never blank | Missing |
| message | string | Localized | SOURCE_REQUIRED | 4.1 | Generic enumeration-safe | Never blank | Exact text missing |
| data | object/array/null | Fixed/source | SOURCE_REQUIRED | 4.1 | Draft null | SOURCE_REQUIRED | Missing |
| meta | object | Fixed | {} | 4.1 | Object | Always object | None |
| traceId | string | Generated | Request context | 4.1 | None | Never null | None |

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
