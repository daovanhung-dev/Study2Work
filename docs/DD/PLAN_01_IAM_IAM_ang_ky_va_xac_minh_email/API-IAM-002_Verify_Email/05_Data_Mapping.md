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

- Endpoint anonymous; không yêu cầu access token, role hoặc tenant.
- Bắt buộc HTTPS.
- Token verification là authentication-by-possession cho đúng one-time token, không phải Authorization header.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
| --- | --- | --- | --- |
| email_verification_tokens | token_hash/purpose/status/expiry | Raw token phải map tới active REGISTER token | Row lock ở step 2.1. |

### 0.3. Check kết quả

- Token hợp lệ/active/unused: tiếp tục transaction.
- Token không tồn tại, sai purpose, revoked hoặc expired: trả [TOKEN_INVALID_OR_EXPIRED](./06_Error.md#error-token-invalid-or-expired).
- Token đã consumed: trả [TOKEN_ALREADY_USED](./06_Error.md#error-token-already-used).

## 1. Validate data input

<a id="dm-1-1"></a>

### 1.1. Nhận header và request

- `content_type = request.header["Content-Type"]`.
- `idempotency_key = request.header["Idempotency-Key"]`.
- `token_raw = request.body["token"]`.
- `trace_id = request_context.trace_id`.
- `ip_hash = HASH(request_context.ip)`.
- `user_agent_hash = HASH(request_context.user_agent)`.

<a id="dm-1-2"></a>

### 1.2. Validate và hash token

- Nếu `token_raw` thiếu/null/blank: trả [token required](./06_Error.md#error-token-required).
- Nếu `len(token_raw) < 32`: trả [token length](./06_Error.md#error-token-length).
- Nếu `len(token_raw) > 512`: trả [token length](./06_Error.md#error-token-length).
- `token_hash = HASH(token_raw)`; exact keyed hash algorithm SOURCE_REQUIRED.
- Không log `token_raw`.

<a id="dm-1-3"></a>

### 1.3. Rate limit

- Kiểm `10 request/phút/IP`.
- Nếu vượt giới hạn: trả HTTP `429` theo [Error](./06_Error.md#error-rate-limit).

## 2. Get thông tin

<a id="dm-2-1"></a>

### 2.1. Query

**Q-IAM002-01 — Lock verification token**

| Target table | Column get | Chú thích | Remarks |
| --- | --- | --- | --- |
| `email_verification_tokens AS evt` | `evt.id` | Token ID | SELECT FOR UPDATE. |
| `↑` | `evt.user_id` | User ID |  |
| `↑` | `evt.email_id` | Email ID |  |
| `↑` | `evt.purpose` | Purpose | Must REGISTER. |
| `↑` | `evt.status` | Status | ACTIVE/CONSUMED/REVOKED/EXPIRED. |
| `↑` | `evt.expires_at` | Expiry | Compare current UTC. |
| `↑` | `evt.consumed_at` | Consumed time | Distinguish already used. |
| `↑` | `evt.revoked_at` | Revoked time | Invalid branch. |

### 2.2. JOIN

| Target table | Join condition | Join type |
| --- | --- | --- |
| `email_verification_tokens AS evt` | `N/A` | `BASE` |

### 2.3. WHERE

- `evt.token_hash = token_hash`.

### 2.4. ORDER BY

- N/A — `token_hash` unique.
- Lock: `FOR UPDATE`.

<a id="dm-2-2"></a>

### 2.5. Query user/email after token lock

- Read `users` by `users.id = evt.user_id`.
- Read `user_emails` by `user_emails.id = evt.email_id` and `user_emails.user_id = evt.user_id`.
- Selected columns mỗi dòng:
  - `users.id`.
  - `users.status`.
  - `users.row_version`.
  - `user_emails.id`.
  - `user_emails.verified_at`.
  - `user_emails.row_version`.

<a id="dm-2-3"></a>

### 2.6. Idempotency replay/claim

- `operation = "POST /api/v1/auth/verify-email"`.
- Hash idempotency key và canonical body.
- Replay same key/same request after completion.
- Different request hash: `IDEMPOTENCY_KEY_REUSED`.
- Processing request: `REQUEST_IN_PROGRESS`; HTTP SOURCE_REQUIRED.

## 3. Insert/Update thông tin

<a id="dm-3-1"></a>

### 3.1. Target table

- `idempotency_keys`.
- `email_verification_tokens`.
- `users`.
- `user_emails`.
- `auth_sessions`.
- `refresh_tokens`.
- `outbox_events`.

### 3.2. Conditions

- Token row locked by unique token hash.
- `purpose = REGISTER`.
- `status = ACTIVE`.
- `expires_at > current_timestamp`.
- `consumed_at IS NULL`.
- `revoked_at IS NULL`.

### 3.3. Items update/insert

<a id="dm-3-2"></a>

#### 3.3.1. BEGIN TRANSACTION và claim idempotency

- `BEGIN TRANSACTION`.
- Insert idempotency claim theo [07_idempotency_keys_insert.md](./07_idempotency_keys_insert.md#db-map).
- Execute token query `FOR UPDATE`.

<a id="dm-3-3"></a>

#### 3.3.2. Validate locked token

- IF no token row: error `TOKEN_INVALID_OR_EXPIRED`; rollback claim according to idempotency policy.
- IF purpose khác REGISTER: error `TOKEN_INVALID_OR_EXPIRED`.
- IF status = CONSUMED hoặc consumed_at khác null: error `TOKEN_ALREADY_USED`.
- IF status = REVOKED/EXPIRED hoặc expires_at <= now: error `TOKEN_INVALID_OR_EXPIRED`.
- Error path không tạo session/refresh/outbox.

<a id="dm-3-4"></a>

#### 3.3.3. Consume token và activate identity

- Update token theo [08_email_verification_tokens_update.md](./08_email_verification_tokens_update.md#db-map).
- Update user theo [09_users_update.md](./09_users_update.md#db-map).
- Update primary email theo [10_user_emails_update.md](./10_user_emails_update.md#db-map).

<a id="dm-3-5"></a>

#### 3.3.4. Generate session/token variables

- `session_id = UUID_V7()`.
- `refresh_token_id = UUID_V7()`.
- `refresh_family_id = UUID_V7()`.
- `raw_refresh_token = CRYPTO_RANDOM(SOURCE_REQUIRED_LENGTH)`.
- `refresh_token_hash = KEYED_SHA256(raw_refresh_token)` — exact key reference SOURCE_REQUIRED.
- `session_epoch = SOURCE_REQUIRED`; DB users không có canonical authVersion/session epoch source.
- `session_expires_at = current_timestamp + SOURCE_REQUIRED_SESSION_TTL`.
- `refresh_expires_at = current_timestamp + max 30 days` theo BR-IAM-003; exact TTL SOURCE_REQUIRED.
- `access_token = ES256_SIGN(claims, KMS_KEY)`; claims/audience for hosted identity consumer SOURCE_REQUIRED.

<a id="dm-3-6"></a>

#### 3.3.5. Insert session and refresh token

- Insert `auth_sessions` theo [11_auth_sessions_insert.md](./11_auth_sessions_insert.md#db-map).
- Insert `refresh_tokens` theo [12_refresh_tokens_insert.md](./12_refresh_tokens_insert.md#db-map).
- Persist refresh token hash only.

<a id="dm-3-7"></a>

#### 3.3.6. Insert verified outbox event

- Insert `outbox_events` theo [13_outbox_events_insert.md](./13_outbox_events_insert.md#db-map).
- Dùng event catalog `identity.user.verified.v1`.
- Minimum payload:
  - `subject = user_id`.
  - `sourceVersion = users.row_version_after_update`.
  - `verifiedAt = current_timestamp`.
- Không đưa access token/refresh token/email ciphertext vào payload.

<a id="dm-3-8"></a>

#### 3.3.7. Complete idempotency và COMMIT

- Build redacted response; raw tokens chỉ nằm trong secure response channel.
- Update idempotency theo [14_idempotency_keys_update.md](./14_idempotency_keys_update.md#db-map); response_body persistence phải redact/secure token policy SOURCE_REQUIRED.
- Nếu tất cả mutation thành công: `COMMIT`.
- Nếu mutation lỗi trước COMMIT: `ROLLBACK` token/user/email/session/refresh/outbox/idempotency changes.
- Sau COMMIT, worker phát signed event tới Study/Work.

### 3.4. Parameters

| Param | Giá trị | Remarks |
| --- | --- | --- |
| `token_hash` | Hash của raw token | Unique lookup, không log raw token. |
| `user_id` | email_verification_tokens.user_id | Subject. |
| `email_id` | email_verification_tokens.email_id | Primary email record. |
| `session_epoch` | SOURCE_REQUIRED | Blocking DB/session gap. |
| `raw_refresh_token` | Generated secure random | Return once; persist hash. |
| `sourceVersion` | users.row_version after update | Event projection monotonic. |

## 4. Check kết quả execute query

<a id="dm-4-1"></a>

### 4.1. Thành công

- HTTP success status = SOURCE_REQUIRED.
- `success = true`.
- `businessCode = SOURCE_REQUIRED`.
- `message = SOURCE_REQUIRED localized verified message`.
- `data.accessToken = access_token` — DERIVED field name.
- `data.refreshToken = raw_refresh_token` — DERIVED field name.
- `data.accountStatus = "ACTIVE"` — DERIVED field name.
- `meta = {}`.
- `traceId = trace_id`.

<a id="dm-4-2"></a>

### 4.2. Lỗi hệ thống

- Dependency unavailable: rollback và trả `503 DEPENDENCY_UNAVAILABLE`.
- Không trả token/hash/key/SQL/stack trace.

<a id="dm-4-3"></a>

### 4.3. Validate lỗi

- Missing/length invalid token: HTTP `400`, code SOURCE_REQUIRED.
- Invalid/expired/used token: HTTP status SOURCE_REQUIRED theo endpoint code.
- Không tạo session hoặc refresh token ở mọi error branch.

<a id="dm-4-4"></a>

### 4.4. Ngoài trường hợp trên

- Replay same idempotency key phải trả cùng finalized result mà không consume token lần hai.
- Cần xác nhận cách lưu/replay token response an toàn trong idempotency record.

<a id="dm-5-1"></a>

## 5. Reconciliation matrices

### 5.1. Request Usage Matrix

| Request field | Nguồn | Data Mapping step | Validate | SQL/Mutation usage | Branch/Loop | Response usage | Gap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Content-Type | DIRECT | 1.1 | JSON | N/A | Validation | N/A | Code khi sai missing |
| Idempotency-Key | DIRECT | 1.1,2.6,3.3.1 | 16–128 | idempotency_keys | Replay/conflict | Replay response | Secure token replay policy missing |
| token | DIRECT | 1.1–1.2,2.1 | 32–512 | email_verification_tokens lookup | Invalid/expired/used | Indirect account/session result | Hash algorithm/alphabet missing |

### 5.2. Query Matrix

| Query ID | Mục đích | Type | Base table/view | Alias | Columns | JOIN | WHERE | GROUP/HAVING | ORDER | Pagination | Lock | Result variable | Branch |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q-IAM002-01 | Lock token | SELECT | email_verification_tokens | evt | evt.id | N/A | token_hash = input | N/A | N/A | N/A | FOR UPDATE | token_record | Invalid/used/valid |
| Q-IAM002-01 | Lock token | SELECT | email_verification_tokens | evt | evt.user_id | N/A | same | N/A | N/A | N/A | FOR UPDATE | token_record | same |
| Q-IAM002-01 | Lock token | SELECT | email_verification_tokens | evt | evt.email_id | N/A | same | N/A | N/A | N/A | FOR UPDATE | token_record | same |
| Q-IAM002-01 | Lock token | SELECT | email_verification_tokens | evt | evt.status | N/A | same | N/A | N/A | N/A | FOR UPDATE | token_record | same |
| Q-IAM002-01 | Lock token | SELECT | email_verification_tokens | evt | evt.expires_at | N/A | same | N/A | N/A | N/A | FOR UPDATE | token_record | same |
| Q-IAM002-02 | Read user | SELECT | users | u | u.status | N/A | id = token.user_id | N/A | N/A | N/A | Row participates in update | user_record | Activate |
| Q-IAM002-03 | Read email | SELECT | user_emails | ue | ue.verified_at | N/A | id = token.email_id AND user_id = token.user_id | N/A | N/A | N/A | Row participates in update | email_record | Verify |

### 5.3. Mutation Matrix

| Mutation ID | Operation | Target table | Record condition | Fields | Value sources | Audit | Mapping file | Transaction | Failure behavior |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M-IAM002-01 | INSERT | idempotency_keys | New key | Refer mapping | Header/body hash | N/A | 07_idempotency_keys_insert.md | identity_db TX | Rollback/replay |
| M-IAM002-02 | UPDATE | email_verification_tokens | Locked active REGISTER token | Refer mapping | current timestamp/status | No separate audit sourced | 08_email_verification_tokens_update.md | identity_db TX | Rollback |
| M-IAM002-03 | UPDATE | users | Token user | Refer mapping | ACTIVE/current timestamp | Event/outbox | 09_users_update.md | identity_db TX | Rollback |
| M-IAM002-04 | UPDATE | user_emails | Token email | Refer mapping | current timestamp | Event/outbox | 10_user_emails_update.md | identity_db TX | Rollback |
| M-IAM002-05 | INSERT | auth_sessions | Valid token | Refer mapping | Generated/context/SOURCE_REQUIRED epoch | N/A | 11_auth_sessions_insert.md | identity_db TX | Rollback |
| M-IAM002-06 | INSERT | refresh_tokens | Valid token | Refer mapping | Generated hash/family | N/A | 12_refresh_tokens_insert.md | identity_db TX | Rollback |
| M-IAM002-07 | INSERT | outbox_events | After activation/session prepared | Refer mapping | Verified event | Trace linked | 13_outbox_events_insert.md | identity_db TX | Rollback |
| M-IAM002-08 | UPDATE | idempotency_keys | Before commit | Refer mapping | Redacted response | N/A | 14_idempotency_keys_update.md | identity_db TX | Rollback |

### 5.4. Response Source Matrix

| Response field | Type | Source type | Table/column hoặc generator | Data Mapping step | Transform | Null/empty rule | Gap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| success | boolean | Fixed | Branch | 4.1 | true/false | Never null | None |
| businessCode | string | Fixed | SOURCE_REQUIRED | 4.1 | None | Never blank | Success code missing |
| message | string | Localized | SOURCE_REQUIRED catalog | 4.1 | Localization | Never blank | Exact message missing |
| data.accessToken | string | Generated/KMS | ES256_SIGN | 4.1 | JWT | Required success | Exact field/claims missing |
| data.refreshToken | string | Generated | Raw token; DB stores hash | 4.1 | Opaque | Required success | Exact field/transport missing |
| data.accountStatus | string | DB | users.status | 4.1 | Enum string | ACTIVE | Exact field name missing |
| meta | object | Fixed/generated | {} | 4.1 | Object | Always object | None |
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
