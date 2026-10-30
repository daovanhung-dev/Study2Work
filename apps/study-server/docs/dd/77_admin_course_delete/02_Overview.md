---
title: "Overview"
order: 2
dd_id: "77"
api_name: "Xóa khóa học Admin theo policy AC-32"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #77 |
| Module | ADMIN / SYSTEM MANAGEMENT — AC-32 |
| Method | DELETE |
| Endpoint | `/api/v1/admin/courses/{course_id}` |
| Purpose | Admin yêu cầu xóa khóa học theo policy sau khi kiểm tra enrollment/content. |
| Consumer/Actor | Admin; course-management permission riêng chưa có policy source. |
| Authentication | Bearer JWT |
| Authorization | Shared JWT role `ADMIN`; fallback cho permission riêng chưa được xác nhận. |
| Direct request | `path{course_id:int64!}`; không khai báo body/query. |
| Direct response | `ApiEnvelope<DeleteResult>`; 200 `DESIGN_RESOURCE_DELETED`. |
| DeleteResult | `id:int64`, `status:"deleted"`, `deleted_at:date-time`. |
| Direct errors | 401/403/404/422/500 với đúng mã trong catalog. |
| Basis | Contract/soft-delete intent DIRECT; blocker set, status marker and timestamp mapping DERIVED; live schema SOURCE_REQUIRED. |
| Status | Draft — Needs Confirmation |
| Current runtime state | `SOURCE_BACKED / LOCAL_TESTED` — route/module/focused HTTP tests tồn tại; tests dùng fake DB session. |
| Transaction | `view.py` khóa course, kiểm tra dependency, cập nhật marker và commit trong một transaction; lỗi rollback. |
| Side effects | Đặt `courses.status='DELETED'`, cập nhật `updated_at`; giữ nguyên enrollment/content, không hard-delete, cascade hoặc audit. |

## Sources

- [Catalog và reusable schemas](../../../../../docs/lists/list_api.md) — API #77, `DeleteResult`, `ApiEnvelope`.
- [AC/API index, AC-32](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — Admin course-management permission và APIs #73–#77.
- [AC-32 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — DELETE → soft delete theo policy → reload management.
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md) — legacy course relationships; ERD là design artifact.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — BIGINT `courses`, `enrollments`, `lessons` và các course-linked relations; không có course deletion timestamp.
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql) — UUID `courses`, `archived_at`, versioned content/enrollment model và restrictive foreign keys; không tương thích trực tiếp với API int64.
- [API #72 delete precedent](../72_admin_user_delete/02_Overview.md), [#73 list](../73_admin_courses_list/02_Overview.md), [#74 detail](../74_admin_course_detail/02_Overview.md), [#75 update](../75_admin_course_update/02_Overview.md), [#76 status](../76_admin_course_status/02_Overview.md) — ranh giới delete, visibility, metadata, status/audit và response.
- [Current router](../../../app/api/v1.py), [auth helper](../../../app/utils/auth.py), [middleware](../../../app/core/middleware.py), [response helper](../../../app/core/responses.py) — route, shared ADMIN guard, route-template errors and response integration.
- [API guidelines](../../../../../contracts/api-guidelines/README.md) — error envelope và hướng dẫn retryable mutation.

## Tables read

| Relation | Candidate fields/relationship | Basis/status |
|---|---|---|
| Legacy `courses` | `id`, `status`, `updated_at` | Candidate lock/soft-delete target; DDL artifact, live schema unknown. |
| Legacy `enrollments` | `course_id` | Any matching enrollment blocks; status is not filtered. This policy is DERIVED. |
| Legacy `contents` | `course_id`, `deleted_at` | Active generic Content rows block; soft-deleted rows do not. DERIVED from API #53 marker. |
| Legacy `lessons`, `quizzes`, `assignments` | `course_id` | Any matching row blocks as course learning content; DERIVED conservative dependency set. |
| V1-PILOT `courses` / `course_versions` | UUID IDs, `archived_at`, versioned course/content | Different model; do not map to the int64 `DeleteResult`. |

## Tables write

The implementation updates the existing legacy candidate `courses.status` to `DELETED` and `updated_at` to the DB current timestamp. No new course column, table or migration is added. This mapping is `DERIVED` from API #72 and does not establish the live schema.

## Mục chú ý

- Catalog names enrollment/content checks and AC-32 says soft delete theo policy; neither source specifies exact relations or status semantics.
- Runtime fallback `DERIVED`: any enrollment row, any lesson/quiz/assignment row, or any active generic Content row blocks with catalog 422; no child row is changed.
- `DeleteResult.deleted_at` maps to persisted `courses.updated_at` returned by the soft-delete UPDATE, following API #72. V1-PILOT `archived_at` is unrelated to this legacy BIGINT model.
- #76 explicitly requires status update plus audit; #77 diagram does not specify audit. Do not add an audit mutation to #77 by analogy.
- APIs #73/#74 currently read status `DELETED` like other Admin-visible statuses. #75/#76 behavior on a deleted target is not changed by this one-API implementation; restore/visibility semantics remain open.
- Shared Admin guard runs before path parsing/DB; dedicated course-management permission remains unresolved.
- Middleware matches the shared FastAPI route template, and current `error_response()` emits `data:null`.

## Assumptions

- Existing enrollment/content dependencies block with catalog 422 `DESIGN_VALIDATION_ERROR`; blocker set is `DERIVED`, not owner-confirmed.
- Dependency checks and marker update run in one request transaction after the course row is locked.
- Successful `status="deleted"` is direct; `deleted_at` maps to the DB-returned `updated_at` alias, a `DERIVED` fallback.

## Conflicts

- `DeleteResult.deleted_at` is required, while legacy `courses` has no dedicated deletion timestamp; runtime reuses `updated_at` by API #72 precedent.
- V1-PILOT `courses.archived_at` is not a direct mapping for legacy BIGINT course deletion; its model and child references use UUID/versioned rows.
- Catalog requires enrollment/content checks but does not define their policy; checked-in relations/blocker semantics are DERIVED.
- Shared `ADMIN` role is the local guard; dedicated course-management permission remains unresolved. Route is wired; local tests do not verify live schema or DB policy.

## Security note

- Authenticate and authorize Admin/course-management access before Q1 so unauthorized callers cannot distinguish course existence.
- Do not use the Student current-user guard for this endpoint.
- Do not reveal enrollment identities, learner progress, submissions, payment data or raw database errors in the response.
- Do not erase children or history; the diagram selects soft delete, not a cascade.

## Performance note

- Dependency checks use bounded `EXISTS` projections under the locked candidate course row.
- Avoid loading full enrollment/content collections when an existence check is sufficient.
- Exact indexes, query plan and schema availability are unknown; do not claim live performance.

## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `Overview`
- Dimension: `A1:BA10`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `4`
- Số vùng merge: `0`

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 1 | `A1` | 【Khái quát】 |  |
| 3 | `B3` | Get thông tin…. |  |
| 5 | `A5` | 【Mục chú ý】 |  |
| 7 | `B7` | Không có |  |

</details>
