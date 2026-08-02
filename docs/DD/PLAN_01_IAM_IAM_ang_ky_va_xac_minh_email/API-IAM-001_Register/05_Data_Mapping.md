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

- API là anonymous; không đọc `Authorization` và không kiểm role/permission.
- Bắt buộc HTTPS.
- Chống account enumeration áp dụng cho duplicate email và public error message.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
| --- | --- | --- | --- |
| N/A | N/A | Anonymous endpoint | Không có RBAC/tenant check. |

### 0.3. Check kết quả

- Tiếp tục xử lý khi request đến qua HTTPS.
- Nếu transport/security gateway từ chối request, response do gateway xử lý; business code cụ thể SOURCE_REQUIRED.

## 1. Validate data input

<a id="dm-1-1"></a>

### 1.1. Nhận request header và body

- `content_type = request.header["Content-Type"]`.
- `idempotency_key = request.header["Idempotency-Key"]`.
- `email_raw = request.body["email"]`.
- `password_raw = request.body["password"]`.
- `agreement_versions = request.body["agreementVersions"]` — DERIVED working field.
- `locale_raw = request.body["locale"]`.
- `trace_id = request_context.trace_id`.
- `request_ip_hash = HASH(request_context.ip)`; không lưu raw IP.
- `user_agent_hash = HASH(request_context.user_agent)`; không lưu raw user agent.

<a id="dm-1-2"></a>

### 1.2. Normalize email

- `email_trimmed = unicode_trim(email_raw)`.
- `email_normalized = normalize_email_domain(email_trimmed)`.
- `email_normalized = lowercase_for_comparison(email_normalized)`.
- `email_ciphertext = envelope_encrypt(email_trimmed)`.
- Không thay đổi hiển thị email của người dùng một cách âm thầm ngoài canonical normalization đã được BR-IAM-001 cho phép.

<a id="dm-1-3"></a>

### 1.3. Validate email và password

- Nếu `email_raw` thiếu/null/blank: trả lỗi [email required](./06_Error.md#error-email-required).
- Nếu email không hợp lệ theo validator canonical: trả lỗi [email format](./06_Error.md#error-email-format); exact validator SOURCE_REQUIRED.
- Nếu `password_raw` thiếu/null: trả lỗi [password required](./06_Error.md#error-password-required).
- Nếu `len(password_raw) < 12`: trả `PASSWORD_POLICY_FAILED` theo [Error](./06_Error.md#error-password-policy-failed).
- Nếu `len(password_raw) > 128`: trả `PASSWORD_POLICY_FAILED` theo [Error](./06_Error.md#error-password-policy-failed).
- Các rule password ngoài length: `SOURCE_REQUIRED`; không tự tạo complexity rule.
- `password_hash = ARGON2ID(password_raw, argon2_parameters)`.
- `argon2_parameters = SOURCE_REQUIRED`; chỉ persist memory/time/parallelism/version, không persist password.

<a id="dm-1-4"></a>

### 1.4. Validate agreement

- Nếu `agreement_versions` thiếu: trả `AGREEMENT_VERSION_INVALID` theo [Error](./06_Error.md#error-agreement-version-invalid).
- FOR EACH `agreement_version` trong `agreement_versions`:
  - Nếu item null/blank: trả `AGREEMENT_VERSION_INVALID`.
  - Kiểm version hiện hành theo nguồn catalog/schema `SOURCE_REQUIRED`.
- Physical table và column cho acceptance chưa có trong DB canonical; xem [OPEN_QUESTIONS.md](../OPEN_QUESTIONS.md#q-plan01-003).

<a id="dm-1-5"></a>

### 1.5. Validate locale và rate limit

- `locale = locale_raw` nếu có; required/default/allowlist HTTP là SOURCE_REQUIRED.
- Nếu locale ngoài allowlist sau khi allowlist được xác nhận: trả lỗi [locale invalid](./06_Error.md#error-locale-invalid).
- `rate_key = HASH(email_normalized)`.
- Kiểm giới hạn `3 request/giờ/email hash`.
- Nếu vượt giới hạn: trả HTTP `429` theo [Error](./06_Error.md#error-rate-limit).
- Không lưu raw email trong rate limiter.

## 2. Get thông tin

<a id="dm-2-1"></a>

### 2.1. Query

**Q-IAM001-01 — Tìm email đang hoạt động để chống duplicate**

| Target table | Column get | Chú thích | Remarks |
| --- | --- | --- | --- |
| `user_emails AS ue` | `ue.id` | Email record ID | Unique lookup. |
| `↑` | `ue.user_id` | User ID |  |
| `↑` | `ue.email_normalized` | Normalized email | Không trả ra response. |
| `↑` | `ue.replaced_at` | Replacement marker | Active email khi null. |

### 2.2. JOIN

| Target table | Join condition | Join type |
| --- | --- | --- |
| `user_emails AS ue` | `N/A` | `BASE` |

### 2.3. WHERE

- `ue.email_normalized = email_normalized`.
- `ue.replaced_at IS NULL`.

### 2.4. ORDER BY

- N/A — Unique active normalized email constraint; không cần sort/pagination.
- Index/constraint: unique `email_normalized` khi `replaced_at IS NULL`.

<a id="dm-2-2"></a>

### 2.5. Idempotency lookup/claim

- `operation = "POST /api/v1/auth/register"`.
- `key_hash = HASH(idempotency_key)`.
- `request_hash = HASH(canonical_json(request.body))`.
- Tìm `idempotency_keys` theo `(actor_id NULL, operation, key_hash)`.
- Nếu record completed và `request_hash` giống nhau: replay `response_status` + `response_body`; không tạo side effect lần hai.
- Nếu record tồn tại và request hash khác: trả `IDEMPOTENCY_KEY_REUSED` theo [Error](./06_Error.md#error-idempotency-key-reused).
- Nếu request đang xử lý: trả `REQUEST_IN_PROGRESS`; HTTP status SOURCE_REQUIRED.
- Exact transaction boundary của claim/replay cần xác nhận; DD dùng pattern claim trong transaction dưới đây.

## 3. Insert/Update thông tin

<a id="dm-3-1"></a>

### 3.1. Target table

- `idempotency_keys`.
- `users`.
- `user_emails`.
- `password_credentials`.
- `SOURCE_REQUIRED: agreement acceptance physical table`.
- `email_verification_tokens`.
- `security_audit_events`.
- `outbox_events`.

### 3.2. Conditions

- New registration branch chỉ chạy khi không có active `user_emails.email_normalized` trùng.
- Duplicate branch không tạo user/credential/token mới.
- Tất cả domain mutation nằm trong cùng `identity_db` transaction.
- External email provider không được gọi trong transaction.

### 3.3. Items update/insert

<a id="dm-3-2"></a>

#### 3.3.1. BEGIN TRANSACTION và claim idempotency

- `BEGIN TRANSACTION`.
- Insert claim theo [07_idempotency_keys_insert.md](./07_idempotency_keys_insert.md#db-map).
- Recheck active normalized email dưới unique constraint.

<a id="dm-3-3"></a>

#### 3.3.2. Duplicate email branch

- IF active email đã tồn tại:
  - Không insert `users`, `user_emails`, `password_credentials`, token hoặc agreement.
  - Insert redacted audit theo [12_security_audit_events_insert.md](./12_security_audit_events_insert.md#db-map).
  - Complete idempotency record theo [14_idempotency_keys_update.md](./14_idempotency_keys_update.md#db-map).
  - Trả generic accepted response; không tiết lộ account existence.
  - Việc có trả `EMAIL_ALREADY_REGISTERED` hay không đang CONFLICT; xem OPEN_QUESTIONS.
  - `COMMIT`.

<a id="dm-3-4"></a>

#### 3.3.3. New email branch — tạo biến

- `user_id = UUID_V7()`.
- `email_id = UUID_V7()`.
- `credential_id = UUID_V7()`.
- `verification_token_id = UUID_V7()`.
- `raw_verification_token = CRYPTO_RANDOM(SOURCE_REQUIRED_LENGTH)`.
- `verification_token_hash = HASH(raw_verification_token)`; exact keyed hash algorithm SOURCE_REQUIRED.
- `verification_expires_at = current_timestamp + SOURCE_REQUIRED_TTL`.
- `audit_event_id = UUID_V7()`.
- `outbox_event_id = UUID_V7()`.

<a id="dm-3-5"></a>

#### 3.3.4. Insert account, email và credential

- Insert `users` theo [08_users_insert.md](./08_users_insert.md#db-map).
- Insert `user_emails` theo [09_user_emails_insert.md](./09_user_emails_insert.md#db-map).
- Insert `password_credentials` theo [10_password_credentials_insert.md](./10_password_credentials_insert.md#db-map).

<a id="dm-3-6"></a>

#### 3.3.5. Insert agreement acceptance — BLOCKED

- API/sequence yêu cầu insert agreement acceptance.
- DB canonical không định nghĩa table/column/constraint tương ứng.
- Không tạo DB mapping giả.
- Trạng thái: `SOURCE_REQUIRED`; implementation transaction chưa thể chốt Final.

<a id="dm-3-7"></a>

#### 3.3.6. Insert verification token

- Insert `email_verification_tokens` theo [11_email_verification_tokens_insert.md](./11_email_verification_tokens_insert.md#db-map).
- Persist hash, không persist raw token.
- `purpose = "REGISTER"`.
- `status = "ACTIVE"`.

<a id="dm-3-8"></a>

#### 3.3.7. Insert security audit

- Insert audit theo [12_security_audit_events_insert.md](./12_security_audit_events_insert.md#db-map).
- Metadata chỉ chứa allowlisted/redacted keys.
- Event hash chain computation implementation SOURCE_REQUIRED.

<a id="dm-3-9"></a>

#### 3.3.8. Insert outbox

- Insert outbox theo [13_outbox_events_insert.md](./13_outbox_events_insert.md#db-map).
- Endpoint nêu `identity.user.registered`; event catalog không có versioned entry tương ứng.
- Event payload/dataschema SOURCE_REQUIRED.
- Raw token không được nằm trong generic domain event payload; delivery secret handoff mechanism SOURCE_REQUIRED.

<a id="dm-3-10"></a>

#### 3.3.9. Complete idempotency và COMMIT

- Build redacted response containing `verificationExpiresAt`.
- Update idempotency theo [14_idempotency_keys_update.md](./14_idempotency_keys_update.md#db-map).
- Nếu tất cả mutation thành công: `COMMIT`.
- Nếu bất kỳ mutation nào lỗi trước COMMIT: `ROLLBACK` toàn bộ user/email/credential/agreement/token/audit/outbox/idempotency claim theo policy đã xác nhận.
- Sau COMMIT, outbox worker gửi email; provider failure không rollback registration.

### 3.4. Parameters

| Param | Giá trị | Remarks |
| --- | --- | --- |
| `email_normalized` | Normalized từ `email` | Lookup/unique key. |
| `email_ciphertext` | Envelope encryption của email | PII. |
| `password_hash` | Argon2id hash | Không log raw password. |
| `verification_token_hash` | Hash raw token | Raw token chỉ cho delivery. |
| `verification_expires_at` | SOURCE_REQUIRED TTL | Map response. |
| `trace_id` | Request trace ID | Liên kết audit/outbox. |

## 4. Check kết quả execute query

<a id="dm-4-1"></a>

### 4.1. Thành công

- HTTP status: `SOURCE_REQUIRED`; Draft example dùng `202` nhưng không được coi là Final.
- `success = true`.
- `businessCode = SOURCE_REQUIRED`.
- `message = generic registration accepted` với localized exact text SOURCE_REQUIRED.
- `data.verificationExpiresAt = verification_expires_at`.
- `meta = {}`.
- `traceId = trace_id`.

<a id="dm-4-2"></a>

### 4.2. Lỗi hệ thống

- Nếu dependency tạm thời unavailable trước COMMIT: `ROLLBACK` và trả `503 DEPENDENCY_UNAVAILABLE` theo [Error](./06_Error.md#error-dependency-unavailable).
- Không trả stack trace, raw SQL, password, token, email ciphertext hoặc internal table name.

<a id="dm-4-3"></a>

### 4.3. Validate lỗi

- Trả HTTP `400` cho validation có status đã được canonical quy định.
- Map từng field error vào `meta.fieldErrors[]`.
- Business code cụ thể theo [06_Error.md](./06_Error.md).

<a id="dm-4-4"></a>

### 4.4. Ngoài trường hợp trên

- Duplicate email phải dùng generic accepted flow.
- `EMAIL_ALREADY_REGISTERED` chỉ được phát khi product/security owner xác nhận điều kiện không gây enumeration.

<a id="dm-5-1"></a>

## 5. Reconciliation matrices

### 5.1. Request Usage Matrix

| Request field | Nguồn | Data Mapping step | Validate | SQL/Mutation usage | Branch/Loop | Response usage | Gap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `Content-Type` | DIRECT common contract | 1.1 | JSON content type | N/A | Validation branch | N/A | Business code khi sai SOURCE_REQUIRED |
| `Idempotency-Key` | DIRECT | 1.1, 2.5, 3.3.1 | 16–128 | idempotency_keys | Replay/conflict | Replay response | Claim boundary SOURCE_REQUIRED |
| `email` | DIRECT | 1.1–1.5, 2.1, 3.3.4 | Normalize/format | user_emails, rate limiter | Duplicate/new | Indirect expiry response only | Exact email validator SOURCE_REQUIRED |
| `password` | DIRECT | 1.1, 1.3, 3.3.4 | 12–128 + policy | password_credentials | Validation | N/A | Argon2 parameters SOURCE_REQUIRED |
| `agreementVersions` | DERIVED field name | 1.1, 1.4, 3.3.5 | Current version | SOURCE_REQUIRED table | Loop items | N/A | Exact schema/table missing |
| `locale` | DIRECT semantic | 1.1, 1.5, 3.3.4 | Allowlist | users.locale | Validation/default | N/A | Required/default HTTP missing |

### 5.2. Query Matrix

| Query ID | Mục đích | Type | Base table/view | Alias | Columns | JOIN | WHERE | GROUP/HAVING | ORDER | Pagination | Lock | Result variable | Branch |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q-IAM001-01 | Tìm active normalized email | SELECT | user_emails | ue | ue.id | N/A | email_normalized = input | N/A | N/A | N/A | Unique constraint | existing_email | Duplicate/new |
| Q-IAM001-01 | Tìm active normalized email | SELECT | user_emails | ue | ue.user_id | N/A | replaced_at IS NULL | N/A | N/A | N/A | Unique constraint | existing_email | Duplicate/new |
| Q-IAM001-02 | Idempotency replay/claim | SELECT/INSERT | idempotency_keys | ik | ik.request_hash | N/A | actor_id NULL + operation + key_hash | N/A | N/A | N/A | Unique tuple / lock SOURCE_REQUIRED | idempotency_record | Replay/conflict/new |
| Q-IAM001-02 | Idempotency replay/claim | SELECT/INSERT | idempotency_keys | ik | ik.response_body | N/A | same | N/A | N/A | N/A | same | idempotency_record | Replay |

### 5.3. Mutation Matrix

| Mutation ID | Operation | Target table | Record condition | Fields | Value sources | Audit | Mapping file | Transaction | Failure behavior |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M-IAM001-01 | INSERT | idempotency_keys | New key | Mỗi column trong mapping | Header/request hash/defaults | N/A | 07_idempotency_keys_insert.md | identity_db TX | Rollback/replay policy |
| M-IAM001-02 | INSERT | users | New email branch | Mỗi column trong mapping | Generated/default/request locale | Audit separate | 08_users_insert.md | identity_db TX | Rollback |
| M-IAM001-03 | INSERT | user_emails | New email branch | Mỗi column trong mapping | Generated/encrypted/normalized email | Audit separate | 09_user_emails_insert.md | identity_db TX | Rollback |
| M-IAM001-04 | INSERT | password_credentials | New email branch | Mỗi column trong mapping | Argon2 hash/defaults | Audit separate | 10_password_credentials_insert.md | identity_db TX | Rollback |
| M-IAM001-05 | INSERT | SOURCE_REQUIRED agreement table | New email branch | SOURCE_REQUIRED | agreementVersions | Required | Không tạo file giả | identity_db TX | BLOCKED |
| M-IAM001-06 | INSERT | email_verification_tokens | New email branch | Mỗi column trong mapping | Generated/hash/TTL | Audit separate | 11_email_verification_tokens_insert.md | identity_db TX | Rollback |
| M-IAM001-07 | INSERT | security_audit_events | Success/duplicate | Mỗi column trong mapping | Context/redacted metadata | Self | 12_security_audit_events_insert.md | identity_db TX | Rollback |
| M-IAM001-08 | INSERT | outbox_events | New email branch | Mỗi column trong mapping | Generated/event payload | Trace linked | 13_outbox_events_insert.md | identity_db TX | Rollback |
| M-IAM001-09 | UPDATE | idempotency_keys | Before commit | Mỗi column trong mapping | Redacted response | N/A | 14_idempotency_keys_update.md | identity_db TX | Rollback |

### 5.4. Response Source Matrix

| Response field | Type | Source type | Table/column hoặc generator | Data Mapping step | Transform | Null/empty rule | Gap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| success | boolean | Fixed | Branch | 4.1/4.2/4.3 | true/false | Never null | None |
| businessCode | string | Fixed by branch | SOURCE_REQUIRED success; Error catalog | 4.1/4.3 | None | Never blank | Success code missing |
| message | string | Localized | Message catalog SOURCE_REQUIRED | 4.1/4.3 | Localization | Never blank | Exact text missing |
| data | object/null | Mapping | Internal variables | 4.1 | Object/null | Error may null | Exact duplicate branch data rule missing |
| data.verificationExpiresAt | string | DB/generated | email_verification_tokens.expires_at | 4.1 | ISO-8601 UTC | Required success | Token TTL missing |
| meta | object | Fixed/generated | {} / field errors | 4.1/4.3 | Object | Always object | None |
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
