---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
---

# Data Mapping

## Flow xử lý data

## Mục lục

- [0. Check quyền](#0-check-quyen)
- [1. Validate data input](#1-validate-data-input)
- [2. Get thông tin](#2-get-thong-tin)
- [3. Phán đoán trạng thái](#3-phan-doan-trang-thai)
- [4. Insert thông tin trong transaction](#4-insert-thong-tin-trong-transaction)
- [5. Check kết quả và map response](#5-check-ket-qua-va-map-response)

## Request Usage Matrix

| Request field | Nguồn | Data Mapping step | Validate | SQL/Mutation usage | Branch/Loop | Response usage | Gap |
|---|---|---|---|---|---|---|---|
| Authorization | Header; Bearer JWT per API catalog | 0.1–0.3 | Authentication required; Student role required. | Supplies logical caller identity for enrollment/progress ownership. | 0.3 | data.user_id is expected to identify the Student. | Exact JWT claim and mapping conflict with the catalog body phrase; see Q-19-01. |
| path course_id | Path /api/v1/courses/{course_id} | 1.1–1.2 | Required int64 per catalog; numeric bounds SOURCE_REQUIRED. | Candidate courses lookup; enrollments.course_id insert. | 2.1/3.1/4.1 | data.course_id | Catalog repeats course_id in body; equality/precedence unresolved. |
| body course_id | JSON body | 1.1–1.2 | Required int64 per catalog; numeric bounds SOURCE_REQUIRED. | Candidate course/enrollment insert input. | 2.1/3.1/4.1 | data.course_id | Duplicate path/body policy unresolved; see Q-19-01. |
| user from JWT | API row notation: body{..., user from JWT:string!} | 0.2/1.3 | Required and type string in catalog shorthand; exact wire field and claim are SOURCE_REQUIRED. | Logical user_id for duplicate check and both inserts. | 2.2/3.1/4.1/4.2 | data.user_id | Enrollment.user_id is int64; current Study JWT helper turns numeric sub into int. |

## Query Matrix

| Query ID | Mục đích | Type | Base table/view | Alias | Columns | JOIN | WHERE | GROUP/HAVING | ORDER | Pagination | Result variable | Branch |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Q1 | Resolve the course referenced by the request | Logical SELECT; physical query SOURCE_REQUIRED | courses | SOURCE_REQUIRED | Candidate id/status/price exist in DB.sql; endpoint-specific selection is not defined. | N/A — no join specified. | Match supplied course_id is DERIVED; publication/paid eligibility predicate is SOURCE_REQUIRED. | N/A | N/A | N/A | course_record | Missing required resource maps to the declared 404; exact lookup/error target is unresolved. |
| Q2 | Check whether this Student already has the course enrollment | Logical duplicate/state check from AC-12; physical query SOURCE_REQUIRED | enrollments | SOURCE_REQUIRED | Candidate id, user_id, course_id, status from DB.sql. | N/A — no join specified. | Logical pair is user identity + course_id; status selection rule SOURCE_REQUIRED. | N/A | N/A | N/A | existing_enrollment | Conflict maps to declared 409 only after its exact condition is approved. |
| Q3 | Resolve lesson IDs used to initialize Progress | Candidate logical SELECT derived from lesson_progress.lesson_id relation | lessons | SOURCE_REQUIRED | Candidate id and course_id exist in DB.sql. | N/A — ERD relates courses to lessons. | Course association is candidate; included lesson statuses and selection are SOURCE_REQUIRED. | N/A | N/A | N/A | lesson_set | The endpoint needs an approved lesson set if Progress is initialized per lesson; cardinality is unresolved. |

## Mutation Matrix

| Mutation ID | Operation | Target table | Record condition | Fields | Value sources | Audit | Mapping file | Transaction | Failure behavior |
|---|---|---|---|---|---|---|---|---|---|
| M1 | INSERT | enrollments | One new logical enrollment for the authenticated Student/course after duplicate and eligibility checks. | id, user_id, course_id, status, enrolled_at, completed_at | JWT identity and request course ID are unresolved; defaults/timestamps require confirmation. | No audit field is declared in the table. | [07_enrollments_insert.md](./07_enrollments_insert.md) | Same logical transaction as M2 per AC-12. | Roll back if the transaction fails; uniqueness/concurrency behavior is SOURCE_REQUIRED. |
| M2 | INSERT one or more rows | lesson_progress | Per approved lesson set for the newly enrolled Student. | id, user_id, lesson_id, status, progress_percent, last_accessed_at, completed_at | Student identity from JWT; lesson IDs and initialization values SOURCE_REQUIRED. | No audit field is declared in the table. | [08_lesson_progress_insert.md](./08_lesson_progress_insert.md) | Same logical transaction as M1 per AC-12. | Roll back M1 and all M2 writes on transaction failure; runtime behavior is not implemented. |

## Response Source Matrix

| Response field | Type | Source type | Table/column or generator | Data Mapping step | Transform | Null/empty rule | Gap |
|---|---|---|---|---|---|---|---|
| HTTP status | integer | Branch constant | API catalog: 201 | 5.1 | Fixed on created branch. | N/A | Design-only contract. |
| success | boolean | Branch constant | Shared ApiEnvelope | 5.1 | true on success; false on error. | Required by envelope. | Endpoint runtime is unwired. |
| businessCode | string | Branch constant | DESIGN_RESOURCE_CREATED or catalog error code | 5.1/5.2 | Fixed by branch. | Required by envelope. | No new business code is introduced. |
| message | string | Branch message | SOURCE_REQUIRED | 5.1/5.2 | No endpoint-specific literal defined. | Required by envelope. | Do not invent message text. |
| data.id | int64 | Inserted Enrollment | enrollments.id | 4.1/5.1 | Generated key per BIGSERIAL design; returned-row mechanism SOURCE_REQUIRED. | Required on success. | Checked-in schema is design evidence only. |
| data.course_id | int64 | Enrollment row | enrollments.course_id | 1.2/4.1/5.1 | Direct mapping after path/body reconciliation. | Required by Enrollment schema. | Request duplicate policy unresolved. |
| data.user_id | int64 | Enrollment row | enrollments.user_id | 0.2/4.1/5.1 | JWT identity mapping. | Required by Enrollment schema. | Contract says string; DB/logical schema uses int64. |
| data.status | EnrollmentStatus | Enrollment row | enrollments.status | 4.1/5.1 | Direct logical mapping. | Required by Enrollment schema. | Enum members and initial state unresolved. |
| data.enrolled_at | date-time | Enrollment row | enrollments.enrolled_at | 4.1/5.1 | Serialize as ISO-8601. | Required by Enrollment schema. | DDL has no default; clock/source unresolved. |
| data.completed_at | date-time, optional | Enrollment row | enrollments.completed_at | 4.1/5.1 | Direct logical mapping. | Optional; null/omit policy unresolved. | DDL column is nullable. |
| meta | object | Envelope metadata | Shared ApiEnvelope | 5.1/5.2 | Object; current success helper defaults to empty object. | Required object. | Endpoint-specific metadata is not specified. |
| traceId | uuid | Request trace | Shared envelope/current trace helper | 5.1/5.2 | UUID string. | Required by shared schema. | API #19 runtime wiring not verified. |

<a id="0-check-quyen"></a>

## 0. Check quyền

### 0.1. Thực hiện check quyền

- Require Bearer JWT per API #19.
- Require role Student per API #19.
- Current Study auth helper reads sub and roles, parses sub as a positive numeric user ID, and normalizes roles; API #19 does not call this helper today.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| Bearer JWT | sub | Current Study helper expects numeric user ID text. | API #19 catalog also says user from JWT:string in body notation; claim/wire mapping is unresolved. |
| Bearer JWT | roles | Student role is required by contract. | Current helper requires STUDENT; endpoint itself is unwired. |

### 0.3. Check kết quả

- Missing or invalid Bearer JWT maps to HTTP 401 / DESIGN_AUTHENTICATION_REQUIRED per catalog.
- A caller denied by role/access maps to HTTP 403 / DESIGN_ACCESS_DENIED per catalog.
- Do not accept a user ID supplied independently of the approved JWT identity rule.

<a id="1-validate-data-input"></a>

## 1. Validate data input

### 1.1. Get request data

- Read path course_id from /api/v1/courses/{course_id}.
- Read body course_id from JSON.
- Read the JWT-derived user item as currently worded in list_api.md; its wire field and claim mapping are SOURCE_REQUIRED.

### 1.2. Validate course_id

- Path course_id is required int64 by the API row.
- Body course_id is required int64 by the API row.
- Whether both IDs must match, and which location is authoritative, is SOURCE_REQUIRED.
- No min/max numeric range is specified by the contract.

### 1.3. Validate user identity

- Catalog type is string and source phrase is user from JWT.
- Current Study auth helper parses numeric JWT sub into int; this does not resolve the catalog's body/string wording.
- Claim name, wire representation and conversion to Enrollment.user_id:int64 are open; see Q-19-01.

<a id="2-get-thong-tin"></a>

## 2. Get thông tin

### 2.1. Query

- The endpoint's resource and anti-duplicate checks are represented by Q1/Q2 in the Query Matrix.
- DB.sql exposes candidate fields for courses and enrollments; no API #19 SQL/query implementation exists.
- The AC-12 pre-flow reads a PUBLISHED course and checks Enrollment through APIs #6/#15; that client flow does not define API #19's direct-call guards.

### 2.2. JOIN

| Target table | Join condition | Join type |
|---|---|---|
| N/A | N/A | No join is specified by the API #19 contract. |

### 2.3. WHERE

- Logical course identity corresponds to supplied course_id; physical predicate SOURCE_REQUIRED.
- Logical existing Enrollment check corresponds to authenticated user and course; status/uniqueness predicate SOURCE_REQUIRED.
- Course-to-lesson selection for Progress initialization is SOURCE_REQUIRED.

### 2.4. ORDER BY

- N/A — no ordering rule is declared; exact lesson-set selection is unresolved.

<a id="3-phan-doan-trang-thai"></a>

## 3. Phán đoán trạng thái

- If the request is authenticated, authorized and eligible, continue to the transaction.
- AC-12 includes anti-duplicate behavior and the catalog declares HTTP 409 / DESIGN_STATE_CONFLICT.
- The existing enrollment statuses that count as duplicate and concurrent-request behavior are not defined.
- Missing-resource handling uses the declared 404 / DESIGN_RESOURCE_NOT_FOUND; the exact resource lookup/semantics are unresolved.

<a id="4-insert-thong-tin-trong-transaction"></a>

## 4. Insert thông tin trong transaction

### 4.1. BEGIN TRANSACTION and insert Enrollment

- AC-12 names the Enrollment and Progress initialization as one transaction.
- Insert the logical Enrollment using mapping [07_enrollments_insert.md](./07_enrollments_insert.md).
- Obtain the created Enrollment fields needed by the response; generated-ID/readback mechanics are SOURCE_REQUIRED.

### 4.2. Initialize Progress

- Resolve the approved lesson set for the course.
- For each lesson in that set, insert the Student/lesson Progress row using [08_lesson_progress_insert.md](./08_lesson_progress_insert.md).
- Lesson set, row count, values, and whether an empty lesson set is valid are SOURCE_REQUIRED.

### 4.3. COMMIT / ROLLBACK

- COMMIT only after the approved Enrollment and Progress mutations succeed.
- ROLLBACK the transaction if either mutation fails; this is the expected atomic interpretation of AC-12's transaction step, not current runtime evidence.
- Duplicate prevention must be concurrency-safe, but no unique constraint or idempotency policy is defined.

<a id="5-check-ket-qua-va-map-response"></a>

## 5. Check kết quả và map response

### 5.1. Thành công

- Return HTTP 201 / DESIGN_RESOURCE_CREATED per API catalog.
- Return ApiEnvelope<Enrollment> with the fields in [04_Response.md](./04_Response.md).
- Enrollment status, timestamp source and optional completed_at representation remain unresolved.

### 5.2. Lỗi

- Return only the catalog-declared status/business-code pairs in [06_Error.md](./06_Error.md).
- Do not add a business code or choose 404/409 condition semantics without owner confirmation.
- System/database failures map to the declared 500 / DESIGN_INTERNAL_ERROR; do not expose database details.

---
## Template reference

- Template: ../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/05_Data_Mapping.md.
- Sheet logic: 3. Data mapping.

