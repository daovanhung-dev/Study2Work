---
title: "Data Mapping"
order: 5
dd_id: "25"
api_name: "Lưu vị trí và trạng thái"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Approved implementation decisions (2026-11-15)

API #25 does not accept or persist `position`; `percent` is validated and persisted in 0..100; the latest `completed` value sets `COMPLETED` or `IN_PROGRESS`, with `completed_at` set/preserved or cleared accordingly. These approved rules supersede older candidate statements below for these fields only. Other contract details remain unresolved.

## Flow xử lý data

~~~text
0. API #25 is registered and requires a STUDENT access token; the authenticated user ID is used for progress ownership.
1. API #25 request has path `lesson_id` and body `percent`, `completed`; `position` is not part of the request.
2. Validate the STUDENT token and bind the authenticated user ID before querying progress.
3. Read the lesson, verify enrollment, then load progress by authenticated user and lesson.
4. Persist lesson progress only. AC-14 mentions a course aggregate, but no target/formula is specified and this API does not write one.
5. The latest `completed` value sets status; false clears `completed_at`, while true preserves or sets it. `percent` is stored independently after 0..100 validation.
6. Trả HTTP 200 DESIGN_RESOURCE_UPDATED với ApiEnvelope<Lesson> theo catalog; response assembly/query chưa được xác nhận.
7. Giữ 401/403/404/422/500 theo catalog; trigger và error payload/message chưa được API #25 xác nhận.
~~~

## Request Usage Matrix

| Request field | Source | Validate | Query/mutation usage | Branch/response usage | Gap |
|---|---|---|---|---|---|
| Authorization | HTTP header `Authorization` | Bearer JWT; role Student theo catalog | Candidate identity/access check | Không trả trong response | Claim mapping và endpoint-specific access policy chưa xác nhận. |
| `lesson_id` | Path parameter | Required int64 theo catalog | Candidate lesson/progress lookup | Lesson response identity | Range, parse-error mapping và lookup predicate chưa xác nhận. |
| `percent` | JSON body | Required int32 | Maps to `lesson_progress.progress_percent` | Not returned in Lesson | Integer 0..100; stored as sent, independent of `completed`. |
| `completed` | JSON body | Required boolean | Sets progress state | Not returned in Lesson | true sets COMPLETED and sets/preserves completed_at; false sets IN_PROGRESS and clears completed_at. |
| Query parameters | N/A | N/A | N/A | N/A | Catalog không khai báo query parameter. |

<a id="0-authentication-and-authorization"></a>

## 0. Authentication and authorization

### 0.1. Thực hiện check quyền

- Design contract yêu cầu Bearer JWT và role Student.
- AC-14 precondition nói Student đã enrolled vào course chứa lesson; flow đặt API #22 access check trước API #23, #24 và #25.
- Thứ tự client gọi API #22 không xác nhận API #25 tự thực hiện authorization khi được gọi trực tiếp.
- API #25 chưa có route/helper binding để chứng minh claim nào cung cấp user identity.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| Authorization header | Bearer JWT | Required; actor role Student | Catalog contract; API #25 runtime chưa wired. |
| JWT claims | User identity | SOURCE_REQUIRED | Claim và binding sang `lesson_progress.user_id` chưa được API #25 xác nhận. |
| API #22 access | `lesson_id` | AC-14 đặt access check trước bước học | Không chứng minh direct-call authorization của API #25. |
| `enrollments` — candidate | `user_id`, `course_id`, `status` | Eligibility predicate SOURCE_REQUIRED | Candidate design only; không chọn status hoặc rule. |

### 0.3. Check kết quả

- Catalog khai báo HTTP 401 `DESIGN_AUTHENTICATION_REQUIRED` cho authentication failure.
- Catalog khai báo HTTP 403 `DESIGN_ACCESS_DENIED` cho role/access denial; API-specific predicate chưa xác nhận.
- Không xác định API #25 kiểm tra enrollment, prerequisite, ownership hoặc publish state thế nào khi gọi độc lập.

<a id="1-request-validation"></a>

## 1. Request validation

| Request field | Source | Contract validation | Branch/usage | Gap |
|---|---|---|---|---|
| Authorization | HTTP header | Bearer JWT; role Student | Authentication/authorization | Token policy, claim và direct-call entitlement chưa xác nhận. |
| `lesson_id` | Path parameter | Required int64 | Candidate lesson/progress context | Min/max, positivity, parse failure và 422 mapping chưa quy định. |
| `percent` | Request body | Required int32 | Progress percentage | Integer 0..100; values outside the range return 422. |
| `completed` | Request body | Required boolean | Completion branch per AC-14 | Missing/null handling beyond required marker and validation mapping chưa xác nhận. |

> Approved validation: `percent` must be 0..100, is independent of `completed`, and `position` is omitted.

<a id="2-read-progress-context"></a>

## 2. Get thông tin

### 2.1. Query Matrix

| Query ID | Mục đích | Type | Base table/view | Columns | JOIN/WHERE | Result variable | Status |
|---|---|---|---|---|---|---|---|
| Q1 | Resolve lesson context for progress update/response | SELECT | `lessons` | Current source query | `id=:lesson_id` | `lesson_context` | Current API query reads lesson data for the response. |
| Q2 | Resolve existing Student lesson progress | SELECT | `lesson_progress` | Current source query | `(user_id, lesson_id)` | `progress_context` | Migration 019 defines target-schema uniqueness; not yet applied. |
| Q3 | Resolve/update course aggregate | SOURCE_REQUIRED | SOURCE_REQUIRED | SOURCE_REQUIRED | Formula/scope SOURCE_REQUIRED | `course_aggregate` — logical placeholder | AC-14 nêu aggregate nhưng không chỉ định nguồn/đích/công thức. |

### 2.2. Candidate schema references

| Target table | Column/relationship | Evidence | Status |
|---|---|---|---|
| `lesson_progress` | `id`, `user_id`, `lesson_id`, `status`, `progress_percent`, `last_accessed_at`, `completed_at` | `DB_UNICA_TABLES.md` và checked-in `DB.sql`. | DESIGN_ONLY; query/mutation API #25 chưa được xác nhận. |
| `lesson_progress.user_id` | Candidate identity relationship to `users.id` | DB design relationship; authenticated claim mapping absent. | SOURCE_REQUIRED for request binding; DDL permits NULL while ERD marks required. |
| `lesson_progress.lesson_id` | Candidate relationship to `lessons.id` | DB design relationship; request path supplies logical Lesson ID. | DESIGN_ONLY; DDL permits NULL while ERD marks required. |
| `lessons` | Candidate Lesson response fields | DB design/DDL plus reusable `Lesson` schema. | DESIGN_ONLY; response query/projection not confirmed. |
| Course aggregate source/target | No table or formula identified | AC-14 node says “course aggregate”. | SOURCE_REQUIRED; do not add a target table or formula. |

### 2.3. Query rules

- Exact lookup query, identity predicate, selected columns, locks and isolation are SOURCE_REQUIRED.
- Migration 019 defines the `(user_id, lesson_id)` conflict target for `nguyen_anh_duc`; it is not applied yet.
- Candidate schema files are design evidence and do not prove the live schema.

<a id="3-update-lesson-progress-and-aggregate"></a>

## 3. Insert/Update thông tin

### 3.1. Target table

- Candidate target: `lesson_progress` (`DESIGN_ONLY`). AC-14 says update lesson progress; DB design maps API #25 to UPDATE/upsert intent.
- Course aggregate target: `SOURCE_REQUIRED`; no physical table or API-specific query is identified.

### 3.2. Conditions

- Candidate logical identity is authenticated Student plus `lesson_id`; token binding, conflict condition and uniqueness are SOURCE_REQUIRED.
- API request does not declare `user_id`; do not accept one from the body or invent another identity source.
- Whether mutation requires an existing lesson progress row or creates one is not fully specified by API #25 contract/diagram.

### 3.3. Items update/insert

- `position` is not an API #25 request field and is not persisted.
- `percent` maps to `progress_percent` and is validated in 0..100 before persistence.
- `completed = true` sets status to `COMPLETED` and preserves an existing `completed_at` or sets it.
- `completed = false` sets status to `IN_PROGRESS` and clears `completed_at`.
- `last_accessed_at`, `completed_at`, insert defaults and all other field preservation/reset rules are SOURCE_REQUIRED.
- No SQL statement, conflict target, aggregate formula or transaction behavior is approved by available sources.

### 3.4. Parameters

| Param | Giá trị | Remarks |
|---|---|---|
| `lesson_id` | Required int64 path parameter | Candidate lesson/progress identity; lookup predicate unresolved. |
| `percent` | Required int32 request body | Maps to progress_percent; accepted range is 0..100 and value is stored as sent. |
| `completed` | Required boolean request body | true sets COMPLETED; false sets IN_PROGRESS and clears completed_at. |
| `user_id` | Authenticated identity candidate | JWT claim/binding and DB write behavior unresolved. |

### 3.5. Mutation Matrix

| Mutation ID | Operation | Target table | Record condition | Fields | Value sources | Audit | Mapping file | Transaction | Failure behavior |
|---|---|---|---|---|---|---|---|---|---|
| M1 | UPDATE/upsert intent | `lesson_progress` — candidate | User/lesson conflict condition SOURCE_REQUIRED | Exact insert/update columns SOURCE_REQUIRED | Request fields plus authenticated identity candidate | SOURCE_REQUIRED | [07_lesson_progress_update.md](./07_lesson_progress_update.md) | SOURCE_REQUIRED | SOURCE_REQUIRED; rollback not defined. |
| M2 | Update course aggregate per AC-14 | SOURCE_REQUIRED | SOURCE_REQUIRED | SOURCE_REQUIRED | Aggregate formula/source SOURCE_REQUIRED | SOURCE_REQUIRED | No physical mapping file; target not identified. | SOURCE_REQUIRED | Atomicity/partial-failure behavior SOURCE_REQUIRED. |

<a id="4-result-and-error-mapping"></a>

## 4. Check kết quả execute query

### 4.1. Response Source Matrix

| Response field | Type | Source type | Table/column or generator | Data Mapping step | Transform | Null/empty rule | Gap |
|---|---|---|---|---|---|---|---|
| `success` | boolean | ApiEnvelope schema | Envelope field | 4.2–4.6 | Per reusable schema | Schema declares field | Runtime serialization not verified. |
| `businessCode` | string | API catalog | Branch code | 4.2–4.6 | Fixed per catalog | N/A | No additional code is created. |
| `message` | string | ApiEnvelope schema | Envelope field | 4.2–4.6 | SOURCE_REQUIRED | Text policy unspecified | Message content not defined. |
| `data.id` | int64 | Lesson schema; candidate table | `lessons.id` | 4.2 | Candidate direct mapping | Required in Lesson schema | Query/projection and post-mutation payload not confirmed. |
| `data.course_id` | int64 | Lesson schema; candidate table | `lessons.course_id` | 4.2 | Candidate direct mapping | Required in Lesson schema | DDL nullability differs from design; query not confirmed. |
| `data.title` | string | Lesson schema; candidate table | `lessons.name` | 4.2 | `name` → `title` candidate | Required in Lesson schema | Query not confirmed. |
| `data.content` | string? | Lesson schema; candidate table | `lessons.content` | 4.2 | Candidate direct mapping | Null/omit unresolved | Query and serialization not confirmed. |
| `data.video_url` | uri? | Lesson schema; candidate table | `lessons.video_url` | 4.2 | Candidate TEXT-to-URI mapping | Null/omit unresolved | Query and serialization not confirmed. |
| `data.order` | int32 | Lesson schema; candidate table | `lessons.sort_order` | 4.2 | `sort_order` → `order` candidate | Required in Lesson schema | Query not confirmed. |
| `data.status` | LessonStatus | Lesson schema; candidate table | `lessons.status` | 4.2 | Candidate direct mapping | Enum values unspecified | Query and enum not confirmed. |
| `meta` | object | ApiEnvelope schema | Envelope field | 4.2–4.6 | Per reusable schema | Members unspecified | API-specific metadata not declared. |
| `traceId` | uuid | ApiEnvelope schema | Envelope field/generator | 4.2–4.6 | Per reusable schema | Required in reusable schema | API #25 runtime generation/propagation not verified. |

### 4.2. Thành công

- Catalog: HTTPStatus = 200; businessCode = `DESIGN_RESOURCE_UPDATED`.
- Response type: `ApiEnvelope<Lesson>` per catalog; Lesson query/projection and post-update assembly are SOURCE_REQUIRED.
- AC-14 only describes progress mutation/aggregate and completion branch; it does not define Lesson response assembly.

### 4.3. Lỗi hệ thống

- Catalog: HTTPStatus = 500; businessCode = `DESIGN_INTERNAL_ERROR`.
- Error, transaction and response assembly are implemented in current source; remaining contract details are listed in OPEN_QUESTIONS.md.

### 4.4. Validate lỗi

- Catalog: HTTPStatus = 422; businessCode = `DESIGN_VALIDATION_ERROR`.
- Trigger beyond the request field types/required markers, including range/relationship rules, is not specified.

### 4.5. Authentication/authorization/resource errors

- Preserve catalog 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED` and 404 `DESIGN_RESOURCE_NOT_FOUND`.
- Direct-call access predicate, missing-resource condition and 403/404 split are SOURCE_REQUIRED.

### 4.6. Transaction and aggregate failure

- AC-14 describes progress and course aggregate updates but does not specify atomicity, transaction boundary or behavior if only one update succeeds.
- Do not claim rollback or consistency behavior; see [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).

---
## Phụ lục đối chiếu template Markdown

- Template: [05_Data_Mapping.md](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/05_Data_Mapping.md).
- Sheet nguồn: 3. Data mapping.
