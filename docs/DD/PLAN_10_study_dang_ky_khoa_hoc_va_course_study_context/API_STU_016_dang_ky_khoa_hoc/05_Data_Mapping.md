---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
dd_id: "API-STU-016"
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
| `study_db` | `principal/resource scope` | `Learner active; onboarding không bắt buộc` | Không dùng frontend guard làm hàng rào bảo mật |

### 0.3. Check kết quả

- Nếu authentication/authorization hợp lệ: tiếp tục xử lý.
- Nếu không hợp lệ: trả error branch tương ứng trong [06_Error.md](./06_Error.md).

## 1. Validate data input

- `Header.Authorization`: required=`Yes`, type=`string`, format=`Bearer token`, valid=`N/A`; basis=`DIRECT`.
- `Header.Idempotency-Key`: required=`Yes`, type=`string`, format=`UUID/random`, valid=`N/A`; basis=`DIRECT`.
- `Path.courseId`: required=`Yes`, type=`uuid`, format=`UUID v7`, valid=`N/A`; basis=`DIRECT`.
- `Body.courseVersionId`: required=`No`, type=`uuid`, format=`UUID v7`, valid=`N/A`; basis=`DIRECT`.
- `Body.source`: required=`No`, type=`string`, format=`N/A`, valid=`STANDALONE|PRIMARY_PATH|ADMIN`; basis=`DIRECT`.
- Hash `Idempotency-Key`; claim key trước domain mutation. Cùng key khác request hash trả `IDEMPOTENCY_KEY_REUSED`; request đang chạy trả `REQUEST_IN_PROGRESS`.

## 2. Get thông tin

### 2.1. Query `TBL-STU-001 — identity_projections`

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| `identity_projections AS t_identity` | `t_identity.identity_subject_id` | `identity_subject_id` | `DIRECT` |
| `identity_projections AS t_identity` | `t_identity.account_status` | `account_status` | `DIRECT` |
| `identity_projections AS t_identity` | `t_identity.email_verified` | `email_verified` | `DIRECT` |
| `identity_projections AS t_identity` | `t_identity.identity_version` | `identity_version` | `DIRECT` |
| `identity_projections AS t_identity` | `t_identity.projected_at` | `projected_at` | `DIRECT` |

**WHERE / predicate cho `identity_projections`**

- Điều kiện cụ thể theo endpoint summary và khóa/index canonical; exact SQL giữ `DERIVED` nếu catalog không nêu field-level.

### 2.2. Query `TBL-STU-002 — learner_profiles`

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

### 2.3. Query `TBL-STU-011 — courses`

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| `courses AS t_courses` | `t_courses.id` | `id` | `DIRECT` |
| `courses AS t_courses` | `t_courses.slug` | `slug` | `DIRECT` |
| `courses AS t_courses` | `t_courses.latest_published_version_id` | `latest_published_version_id` | `DIRECT` |
| `courses AS t_courses` | `t_courses.archived_at` | `archived_at` | `DIRECT` |

**WHERE / predicate cho `courses`**

- Điều kiện cụ thể theo endpoint summary và khóa/index canonical; exact SQL giữ `DERIVED` nếu catalog không nêu field-level.

### 2.4. Query `TBL-STU-012 — course_versions`

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| `course_versions AS t_courseve` | `t_courseve.id` | `id` | `DIRECT` |
| `course_versions AS t_courseve` | `t_courseve.course_id` | `course_id` | `DIRECT` |
| `course_versions AS t_courseve` | `t_courseve.version_no` | `version_no` | `DIRECT` |
| `course_versions AS t_courseve` | `t_courseve.status` | `status` | `DIRECT` |
| `course_versions AS t_courseve` | `t_courseve.title` | `title` | `DIRECT` |
| `course_versions AS t_courseve` | `t_courseve.summary` | `summary` | `DIRECT` |
| `course_versions AS t_courseve` | `t_courseve.level` | `level` | `DIRECT` |
| `course_versions AS t_courseve` | `t_courseve.estimated_minutes` | `estimated_minutes` | `DIRECT` |
| `course_versions AS t_courseve` | `t_courseve.published_at` | `published_at` | `DIRECT` |
| `course_versions AS t_courseve` | `t_courseve.content_hash` | `content_hash` | `DIRECT` |

**WHERE / predicate cho `course_versions`**

- `status = PUBLISHED` khi API public/chọn version yêu cầu published.

### 2.5. Query `TBL-STU-027 — course_enrollments`

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| `course_enrollments AS t_courseen` | `t_courseen.id` | `id` | `DIRECT` |
| `course_enrollments AS t_courseen` | `t_courseen.learner_id` | `learner_id` | `DIRECT` |
| `course_enrollments AS t_courseen` | `t_courseen.course_version_id` | `course_version_id` | `DIRECT` |
| `course_enrollments AS t_courseen` | `t_courseen.source_type` | `source_type` | `DIRECT` |
| `course_enrollments AS t_courseen` | `t_courseen.source_path_period_id` | `source_path_period_id` | `DIRECT` |
| `course_enrollments AS t_courseen` | `t_courseen.status` | `status` | `DIRECT` |
| `course_enrollments AS t_courseen` | `t_courseen.enrolled_at` | `enrolled_at` | `DIRECT` |
| `course_enrollments AS t_courseen` | `t_courseen.completed_at` | `completed_at` | `DIRECT` |
| `course_enrollments AS t_courseen` | `t_courseen.last_activity_at` | `last_activity_at` | `DIRECT` |
| `course_enrollments AS t_courseen` | `t_courseen.row_version` | `row_version` | `DIRECT` |

**WHERE / predicate cho `course_enrollments`**

- `identity_subject_id`/`learner_id` lấy server-side từ access token projection.
- Owner predicate bắt buộc; không thay pinned version bằng current version.
- Lock: `FOR UPDATE`/advisory lock chỉ khi endpoint source yêu cầu; exact lock scope nêu tại transaction section.

### 2.6. Query `TBL-STU-026 — primary_path_periods`

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| `primary_path_periods AS t_primaryp` | `t_primaryp.id` | `id` | `DIRECT` |
| `primary_path_periods AS t_primaryp` | `t_primaryp.learner_id` | `learner_id` | `DIRECT` |
| `primary_path_periods AS t_primaryp` | `t_primaryp.path_version_id` | `path_version_id` | `DIRECT` |
| `primary_path_periods AS t_primaryp` | `t_primaryp.status` | `status` | `DIRECT` |
| `primary_path_periods AS t_primaryp` | `t_primaryp.started_at` | `started_at` | `DIRECT` |
| `primary_path_periods AS t_primaryp` | `t_primaryp.ended_at` | `ended_at` | `DIRECT` |
| `primary_path_periods AS t_primaryp` | `t_primaryp.end_reason` | `end_reason` | `DIRECT` |
| `primary_path_periods AS t_primaryp` | `t_primaryp.supersedes_period_id` | `supersedes_period_id` | `DIRECT` |

**WHERE / predicate cho `primary_path_periods`**

- `identity_subject_id`/`learner_id` lấy server-side từ access token projection.
- `status = ACTIVE` cho current-period query khi áp dụng.
- Lock: `FOR UPDATE`/advisory lock chỉ khi endpoint source yêu cầu; exact lock scope nêu tại transaction section.

<a id="3-insertupdate-thong-tin"></a>
## 3. Insert/Update thông tin

### 3.1. Target table

- `TBL-STU-027 — course_enrollments` operation `INSERT`.
- `TBL-STU-051 — idempotency_keys` operation `INSERT`.
- `TBL-STU-050 — audit_events` operation `INSERT`.
- `TBL-STU-052 — outbox_events` operation `INSERT`.

### 3.2. Conditions

- `BEGIN TRANSACTION` sau khi validation/business checks/idempotency claim hoàn tất.
- Transaction chỉ bao phủ một database owner.
- Không gọi email/KMS/HTTP/provider trong transaction; side effect dùng outbox.
- Unique `(learner_id, course_version_id)` là hàng rào duplicate; duplicate cùng target trả enrollment hiện có.

### 3.3. Items update/insert

- `INSERT course_enrollments`: refer [07_course_enrollments_insert.md](./07_course_enrollments_insert.md).
- `INSERT idempotency_keys`: refer [08_idempotency_keys_insert.md](./08_idempotency_keys_insert.md).
- `INSERT audit_events`: refer [09_audit_events_insert.md](./09_audit_events_insert.md).
- `INSERT outbox_events`: refer [10_outbox_events_insert.md](./10_outbox_events_insert.md).

### 3.4. Parameters

| Param | Giá trị | Remarks |
|---|---|---|
| `course_enrollments.id` | `Generated UUID v7` | `DIRECT` |
| `course_enrollments.created_at` | `current_timestamp` | `DIRECT` |
| `course_enrollments.updated_at` | `current_timestamp` | `DIRECT` |
| `course_enrollments.row_version` | `1` | `DIRECT` |
| `course_enrollments.learner_id` | `Authenticated learner ID` | `DIRECT` |
| `course_enrollments.course_version_id` | `Resolved current/explicit published version` | `DIRECT` |
| `course_enrollments.source_type` | `Q-13 SOURCE_REQUIRED derivation` | `DIRECT` |
| `course_enrollments.source_path_period_id` | `Q-13/Q-12 resolved period or NULL` | `DIRECT` |
| `course_enrollments.status` | `ENROLLED` | `DIRECT` |
| `course_enrollments.enrolled_at` | `current_timestamp` | `DIRECT` |
| `course_enrollments.first_started_at` | `NULL` | `DIRECT` |
| `course_enrollments.completed_at` | `NULL` | `DIRECT` |
| `course_enrollments.last_activity_at` | `NULL` | `DIRECT` |
| `course_enrollments.hidden_from_my_courses_at` | `NULL` | `DIRECT` |
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
| `audit_events.action` | `COURSE_ENROLLED` | `DERIVED` |
| `audit_events.resource_type` | `COURSE_ENROLLMENT` | `DERIVED` |
| `audit_events.resource_id` | `created course_enrollments.id` | `DERIVED` |
| `audit_events.outcome` | `SUCCESS/DENIED/FAILURE` | `DERIVED` |
| `audit_events.business_code` | `Branch business code; success code SOURCE_REQUIRED when not cataloged` | `DERIVED` |
| `audit_events.trace_id` | `request.traceId` | `DERIVED` |
| `audit_events.tenant_context` | `NULL for non-tenant Study APIs` | `DERIVED` |
| `audit_events.changes` | `Enrollment/course version IDs` | `DERIVED` |
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

- `HTTPStatus = 201 hoặc 200 — exact status SOURCE_REQUIRED`.
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
