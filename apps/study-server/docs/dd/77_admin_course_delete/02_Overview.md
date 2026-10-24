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
| Consumer/Actor | Admin có quyền course management. |
| Authentication | Bearer JWT |
| Authorization | Role Admin và quyền course management theo catalog/AC-32; Study chưa có Admin guard. |
| Direct request | `path{course_id:int64!}`; không khai báo body/query. |
| Direct response | `ApiEnvelope<DeleteResult>`; 200 `DESIGN_RESOURCE_DELETED`. |
| DeleteResult | `id:int64`, `status:"deleted"`, `deleted_at:date-time`. |
| Direct errors | 401/403/404/422/500 với đúng mã trong catalog. |
| Basis | Contract và soft-delete intent DIRECT; dependency policy/physical persistence SOURCE_REQUIRED. |
| Status | Draft — Needs Confirmation |
| Current runtime state | `UNWIRED / NOT_FOUND` — không có route, module hoặc focused test API #77. |
| Transaction | Đề xuất dependency check và soft-delete mutation cùng transaction; boundary/locking chưa được xác nhận. |
| Side effects | Soft delete khóa học theo policy; không hard-delete hoặc cascade child rows. Physical effect chưa xác định. |

## Sources

- [Catalog và reusable schemas](../../../../../docs/lists/list_api.md) — API #77, `DeleteResult`, `ApiEnvelope`.
- [AC/API index, AC-32](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — Admin course-management permission và APIs #73–#77.
- [AC-32 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — DELETE → soft delete theo policy → reload management.
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md) — legacy course relationships; ERD là design artifact.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — BIGINT `courses`, `enrollments`, `lessons` và các course-linked relations; không có course deletion timestamp.
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql) — UUID `courses`, `archived_at`, versioned content/enrollment model và restrictive foreign keys; không tương thích trực tiếp với API int64.
- [API #72 delete precedent](../72_admin_user_delete/02_Overview.md), [#73 list](../73_admin_courses_list/02_Overview.md), [#74 detail](../74_admin_course_detail/02_Overview.md), [#75 update](../75_admin_course_update/02_Overview.md), [#76 status](../76_admin_course_status/02_Overview.md) — ranh giới delete, visibility, metadata, status/audit và response.
- [Current router](../../../app/api/v1.py), [auth helper](../../../app/utils/auth.py), [middleware](../../../app/core/middleware.py), [response helper](../../../app/core/responses.py) — source absence và error integration hiện hành.
- [API guidelines](../../../../../contracts/api-guidelines/README.md) — error envelope và hướng dẫn retryable mutation.

## Tables read

| Relation | Candidate fields/relationship | Basis/status |
|---|---|---|
| Legacy `courses` | `id`, course identity | Candidate Q1 only; DDL artifact, live schema unknown. |
| Legacy `enrollments` | `course_id`, `status` | Candidate dependency relation; exact blocker/status policy unknown. |
| Legacy `lessons` | `course_id` | Possible course-content candidate; does not establish generic Content persistence. |
| Legacy course-linked relations | `quizzes`, `assignments`, `discussions`, `payments` | Relationships in legacy DDL/guide; catalog names enrollment/content only, policy coverage unresolved. |
| V1-PILOT `courses` / `course_versions` | UUID IDs, `archived_at`, versioned course/content | Different model; do not map to the int64 `DeleteResult`. |

## Tables write

Physical target/columns are `SOURCE_REQUIRED`. The AC requires a logical soft-delete effect, but neither the legacy course DDL nor the API contract selects a physical marker. Do not write a fabricated `UPDATE`, hard `DELETE`, or child-row cascade.

## Mục chú ý

- Catalog title indicates conditional deletion after enrollment/content checks; AC-32 diagram says soft delete theo policy. Neither source specifies exact relations, active statuses, blocker semantics or error detail.
- Conservative proposal `DERIVED`: if an approved check finds any blocking enrollment/content, return 422; otherwise apply the approved soft-delete policy. The owner must confirm the dependency set and whether any dependency can be retained.
- `DeleteResult.deleted_at` is required by the reusable schema. Legacy `courses` has no deletion timestamp. V1-PILOT `archived_at` belongs to a UUID model and is not automatically equivalent to deletion.
- No physical relation for generic `Content` exists in the legacy ERD/DDL. `lessons.course_id` is only a possible content candidate; do not treat it as the complete Content dependency model.
- #76 explicitly requires status update plus audit; #77 diagram does not specify audit. Do not add an audit mutation to #77 by analogy.
- After delete, hiding the course from #73 list and #74 detail is a group-level proposal; exact visibility/physical predicate remains open. #75/#76 behavior for a deleted target also needs confirmation.
- Current Study has no Admin guard; do not reuse the shared Student guard.
- Current middleware uses exact URL path membership; future dynamic `course_id` matching and error `data` shape need integration work.

## Assumptions

- A blocking dependency can map to catalog 422 `DESIGN_VALIDATION_ERROR`; this is `DERIVED`, not a new business code or a source-confirmed rule.
- Dependency evaluation and soft-delete mutation should be atomic to avoid a check/write race; transaction owner/isolation remain unconfirmed.
- Successful result status is the direct literal `"deleted"`; physical timestamp is not inferred from the system clock without an approved persistence source.

## Conflicts

- `DeleteResult.deleted_at` is required, while the legacy `courses` table has no delete marker/timestamp.
- V1-PILOT `courses.archived_at` is not a direct mapping for legacy BIGINT course deletion; its model and child references use UUID/versioned rows.
- Catalog requires enrollment/content checks but does not define the dependency or block policy. Generic Content persistence is absent from the legacy model.
- Admin authorization, error middleware path mapping and `data:null` guideline differ from current Study source behavior.

## Security note

- Authenticate and authorize Admin/course-management access before Q1 so unauthorized callers cannot distinguish course existence.
- Do not use the Student current-user guard for this endpoint.
- Do not reveal enrollment identities, learner progress, submissions, payment data or raw database errors in the response.
- Do not erase children or history; the diagram selects soft delete, not a cascade.

## Performance note

- Q1 is a candidate primary-key existence read; Q2 should use bounded existence checks after the owner selects the dependency set.
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
