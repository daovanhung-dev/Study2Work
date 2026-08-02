---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
dd_id: "API-STU-011"
status: "STRUCTURE_CONFLICT — Draft"
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
| `study_db` | `principal/resource scope` | `Learner active` | Không dùng frontend guard làm hàng rào bảo mật |

### 0.3. Check kết quả

- Nếu authentication/authorization hợp lệ: tiếp tục xử lý.
- Nếu không hợp lệ: trả error branch tương ứng trong [06_Error.md](./06_Error.md).

## 1. Validate data input

- `Header.Authorization`: required=`Yes`, type=`string`, format=`Bearer token`, valid=`N/A`; basis=`DIRECT`.
- `Header.If-Match`: required=`Yes`, type=`string`, format=`"<version>"`, valid=`N/A`; basis=`DIRECT`.
- `Header.Idempotency-Key`: required=`Yes`, type=`string`, format=`UUID/random`, valid=`N/A`; basis=`DIRECT`.
- Hash `Idempotency-Key`; claim key trước domain mutation. Cùng key khác request hash trả `IDEMPOTENCY_KEY_REUSED`; request đang chạy trả `REQUEST_IN_PROGRESS`.
- Parse `If-Match`; so sánh với canonical version. Sai version trả `412 VERSION_CONFLICT`; không overwrite.

## 2. Get thông tin

### 2.1. Query `TBL-STU-002 — learner_profiles`

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| `learner_profiles AS t_learnerp` | `t_learnerp.id` | `id` | `DIRECT` |
| `learner_profiles AS t_learnerp` | `t_learnerp.identity_subject_id` | `identity_subject_id` | `DIRECT` |
| `learner_profiles AS t_learnerp` | `t_learnerp.full_name` | `full_name` | `DIRECT` |
| `learner_profiles AS t_learnerp` | `t_learnerp.bio` | `bio` | `DIRECT` |
| `learner_profiles AS t_learnerp` | `t_learnerp.onboarding_completed_at` | `onboarding_completed_at` | `DIRECT` |
| `learner_profiles AS t_learnerp` | `t_learnerp.profile_visibility` | `profile_visibility` | `DIRECT` |
| `learner_profiles AS t_learnerp` | `t_learnerp.row_version` | `row_version` | `DIRECT` |
| `learner_profiles AS t_learnerp` | `t_learnerp.deleted_at` | `deleted_at` | `DIRECT` |

**WHERE / predicate cho `learner_profiles`**

- `identity_subject_id`/`learner_id` lấy server-side từ access token projection.
- Lock: `FOR UPDATE`/advisory lock chỉ khi endpoint source yêu cầu; exact lock scope nêu tại transaction section.

### 2.2. Query `TBL-STU-007 — onboarding_submissions`

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| `onboarding_submissions AS t_onboardi` | `t_onboardi.id` | `id` | `DIRECT` |
| `onboarding_submissions AS t_onboardi` | `t_onboardi.learner_id` | `learner_id` | `DIRECT` |
| `onboarding_submissions AS t_onboardi` | `t_onboardi.schema_version` | `schema_version` | `DIRECT` |
| `onboarding_submissions AS t_onboardi` | `t_onboardi.answers` | `answers` | `DIRECT` |
| `onboarding_submissions AS t_onboardi` | `t_onboardi.submitted_at` | `submitted_at` | `DIRECT` |
| `onboarding_submissions AS t_onboardi` | `t_onboardi.is_current` | `is_current` | `DIRECT` |

**WHERE / predicate cho `onboarding_submissions`**

- `identity_subject_id`/`learner_id` lấy server-side từ access token projection.
- Lock: `FOR UPDATE`/advisory lock chỉ khi endpoint source yêu cầu; exact lock scope nêu tại transaction section.

### 2.3. Query `TBL-STU-010 — learning_path_versions`

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| `learning_path_versions AS t_learning` | `t_learning.id` | `id` | `DIRECT` |
| `learning_path_versions AS t_learning` | `t_learning.path_id` | `path_id` | `DIRECT` |
| `learning_path_versions AS t_learning` | `t_learning.version_no` | `version_no` | `DIRECT` |
| `learning_path_versions AS t_learning` | `t_learning.status` | `status` | `DIRECT` |
| `learning_path_versions AS t_learning` | `t_learning.title` | `title` | `DIRECT` |
| `learning_path_versions AS t_learning` | `t_learning.summary` | `summary` | `DIRECT` |
| `learning_path_versions AS t_learning` | `t_learning.estimated_hours` | `estimated_hours` | `DIRECT` |
| `learning_path_versions AS t_learning` | `t_learning.published_at` | `published_at` | `DIRECT` |
| `learning_path_versions AS t_learning` | `t_learning.content_hash` | `content_hash` | `DIRECT` |

**WHERE / predicate cho `learning_path_versions`**

- `status = PUBLISHED` khi API public/chọn version yêu cầu published.

<a id="3-insertupdate-thong-tin"></a>
## 3. Insert/Update thông tin

### 3.1. Target table

- `TBL-STU-007 — onboarding_submissions` operation `INSERT`.
- `TBL-STU-008 — path_recommendation_runs` operation `INSERT`.
- `TBL-STU-051 — idempotency_keys` operation `INSERT`.
- `TBL-STU-050 — audit_events` operation `INSERT`.
- `TBL-STU-052 — outbox_events` operation `INSERT`.

### 3.2. Conditions

- `BEGIN TRANSACTION` sau khi validation/business checks/idempotency claim hoàn tất.
- Transaction chỉ bao phủ một database owner.
- Không gọi email/KMS/HTTP/provider trong transaction; side effect dùng outbox.

### 3.3. Items update/insert

- `INSERT onboarding_submissions`: refer [07_onboarding_submissions_insert.md](./07_onboarding_submissions_insert.md).
- `INSERT path_recommendation_runs`: refer [08_path_recommendation_runs_insert.md](./08_path_recommendation_runs_insert.md).
- `INSERT idempotency_keys`: refer [09_idempotency_keys_insert.md](./09_idempotency_keys_insert.md).
- `INSERT audit_events`: refer [10_audit_events_insert.md](./10_audit_events_insert.md).
- `INSERT outbox_events`: refer [11_outbox_events_insert.md](./11_outbox_events_insert.md).

### 3.4. Parameters

| Param | Giá trị | Remarks |
|---|---|---|
| `onboarding_submissions.id` | `Generated UUID v7` | `DIRECT` |
| `onboarding_submissions.created_at` | `current_timestamp` | `DIRECT` |
| `onboarding_submissions.learner_id` | `Authenticated learner ID` | `DIRECT` |
| `onboarding_submissions.schema_version` | `Current schema version SOURCE_REQUIRED` | `DIRECT` |
| `onboarding_submissions.answers` | `Completed answer snapshot` | `DIRECT` |
| `onboarding_submissions.submitted_at` | `current_timestamp` | `DIRECT` |
| `onboarding_submissions.supersedes_id` | `Previous current record or NULL` | `DIRECT` |
| `onboarding_submissions.is_current` | `true` | `DIRECT` |
| `path_recommendation_runs.id` | `Generated UUID v7` | `DIRECT` |
| `path_recommendation_runs.created_at` | `current_timestamp` | `DIRECT` |
| `path_recommendation_runs.learner_id` | `Authenticated learner ID` | `DIRECT` |
| `path_recommendation_runs.onboarding_submission_id` | `Created completed submission ID` | `DIRECT` |
| `path_recommendation_runs.algorithm_version` | `SOURCE_REQUIRED` | `DIRECT` |
| `path_recommendation_runs.input_snapshot` | `Completed answer snapshot` | `DIRECT` |
| `path_recommendation_runs.ranked_path_version_ids` | `Deterministic ranked UUID array` | `DIRECT` |
| `path_recommendation_runs.reason_snapshot` | `SOURCE_REQUIRED item-level schema — Q-10` | `DIRECT` |
| `path_recommendation_runs.generated_at` | `current_timestamp` | `DIRECT` |
| `path_recommendation_runs.expires_at` | `SOURCE_REQUIRED policy expiry` | `DIRECT` |
| `idempotency_keys.id` | `Generated UUID v7` | `DIRECT` |
| `idempotency_keys.created_at` | `current_timestamp` | `DIRECT` |
| `idempotency_keys.updated_at` | `current_timestamp` | `DIRECT` |
| `idempotency_keys.row_version` | `1` | `DIRECT` |
| `idempotency_keys.actor_subject_id` | `identity subject/learner ID` | `DIRECT` |
| `idempotency_keys.operation` | `method + normalized path` | `DIRECT` |
| `idempotency_keys.key_hash` | `Hash(Idempotency-Key)` | `DIRECT` |
| `idempotency_keys.request_hash` | `Hash(canonical request)` | `DIRECT` |
| `idempotency_keys.response_status` | `NULL until complete` | `DIRECT` |
| `idempotency_keys.response_body` | `NULL until complete` | `DIRECT` |
| `idempotency_keys.locked_until` | `current_timestamp + processing lease` | `DIRECT` |
| `idempotency_keys.completed_at` | `NULL until complete` | `DIRECT` |
| `idempotency_keys.expires_at` | `current_timestamp + 24h unless source overrides` | `DIRECT` |
| `audit_events.id` | `Generated UUID v7` | `DERIVED` |
| `audit_events.occurred_at` | `current_timestamp` | `DERIVED` |
| `audit_events.actor_subject_id` | `Authenticated subject ID` | `DERIVED` |
| `audit_events.action` | `ONBOARDING_COMPLETED` | `DERIVED` |
| `audit_events.resource_type` | `ONBOARDING_SUBMISSION` | `DERIVED` |
| `audit_events.resource_id` | `created onboarding_submissions.id` | `DERIVED` |
| `audit_events.outcome` | `SUCCESS/DENIED/FAILURE` | `DERIVED` |
| `audit_events.business_code` | `Branch business code; success code SOURCE_REQUIRED when not cataloged` | `DERIVED` |
| `audit_events.trace_id` | `request.traceId` | `DERIVED` |
| `audit_events.tenant_context` | `NULL for non-tenant Study APIs` | `DERIVED` |
| `audit_events.changes` | `Redacted category changes` | `DERIVED` |
| `audit_events.metadata` | `Redacted metadata JSON` | `DERIVED` |
| `audit_events.prev_hash` | `Previous chain hash or NULL` | `DERIVED` |
| `audit_events.event_hash` | `Hash canonical event payload` | `DERIVED` |
| `audit_events.legal_hold_until` | `NULL unless approved hold` | `DERIVED` |
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
