---
title: "Overview"
order: 2
dd_id: "86"
api_name: "Xóa lesson"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #86 |
| Module | ADMIN / SYSTEM MANAGEMENT — AC-34 |
| Method | DELETE |
| Endpoint | /api/v1/admin/lessons/{lesson_id} |
| Purpose | Admin yêu cầu xóa lesson theo policy sau khi kiểm tra progress/reference. |
| Consumer/Actor | Admin có lesson-management permission |
| Authentication | Bearer JWT |
| Authorization | Role Admin theo catalog và lesson-management permission theo AC-34; Study chưa có Admin guard/policy. |
| Direct request | path lesson_id:int64!; không body/query. |
| Direct response | ApiEnvelope<DeleteResult>; HTTP 200 DESIGN_RESOURCE_DELETED. |
| DeleteResult | id:int64, status:"deleted", deleted_at:date-time. |
| Direct errors | 401/403/404/422/500 với đúng mã catalog. |
| Basis | Method/path/auth/input/response/status/error set và delete-policy intent DIRECT; blocker policy DERIVED; physical delete marker/timestamp SOURCE_REQUIRED. |
| Status | Draft — Needs Confirmation |
| Current implementation | UNWIRED / NOT_FOUND — không có route, module hoặc test API #86 trong Study source. |
| Transaction | DERIVED proposal: target/dependency checks và approved soft-delete mutation nguyên tử; caller, locking và isolation chưa xác định. |
| Side effects | Candidate logical soft-delete; không cascade resource/progress, không cập nhật metadata/status, không thêm audit ngoài nhánh #85. |

## Sources

- [Catalog và reusable schemas](../../../../../docs/lists/list_api.md) — API #86, DeleteResult, ApiEnvelope và exact business codes.
- [AC/API index, AC-34](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — Admin lesson-management permission và APIs #82–#86.
- [AC-34 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — node n5 đọc lesson + dependencies; n11 DELETE; n12 soft delete/delete theo policy; n13 reload danh sách.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — candidate BIGINT lessons, resources.lesson_id và lesson_progress.lesson_id references; không có delete marker.
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql) — UUID/versioned Lesson và child FK RESTRICT; model khác catalog int64.
- [API #82 list](../82_admin_lessons_list/02_Overview.md), [#83 detail](../83_admin_lesson_detail/02_Overview.md), [#84 update](../84_admin_lesson_update/02_Overview.md), [#85 status](../85_admin_lesson_status/02_Overview.md) — ranh giới của nhóm AC-34.
- [API #72 user delete](../72_admin_user_delete/02_Overview.md) and [#77 course delete](../77_admin_course_delete/02_Overview.md) — precedent cho DeleteResult, dependency check và soft-delete gap.
- [Current router](../../../app/api/v1.py), [auth helper](../../../app/utils/auth.py), [middleware](../../../app/core/middleware.py), [response helper](../../../app/core/responses.py) — current runtime/error boundary.
- [API guidelines](../../../../../contracts/api-guidelines/README.md) — error envelope expectation.

## Tables read

| Relation | Candidate fields/relationship | Basis/status |
|---|---|---|
| Legacy lessons | id, course_id, name, content, video_url, sort_order, status, created_at, updated_at | BIGINT DDL artifact; no soft-delete marker or deleted_at. |
| Legacy resources | lesson_id references lessons.id | Candidate reference check; live FK/policy unknown. |
| Legacy lesson_progress | lesson_id references lessons.id | Candidate progress check; status-based policy unknown. |
| V1-PILOT lessons | UUID id, chapter_id, course_version_id, title, summary, position, estimated_minutes, is_preview | Different model; no deletion marker. |
| V1-PILOT content_blocks / assessment_placements / lesson_progress_facts | lesson_id UUID FKs with ON DELETE RESTRICT | Separate pilot dependencies; do not mix with BIGINT API model. |

## Tables write

| Relation | Candidate fields/effect | Basis/status |
|---|---|---|
| Lesson persistence | Logical soft-delete effect and persisted deletion timestamp | AC-34 permits soft-delete; physical relation/marker SOURCE_REQUIRED. |
| Dependency rows | None | No delete/update/cascade of resources or progress. |
| Audit | None proposed | AC-34 #86 branch does not mention audit; #85 owns explicit status audit. |

## Mục chú ý

- Catalog #86 requires checking progress/reference; exact reference set and blocker conditions are not fully defined.
- AC-34 says “Soft delete / delete theo policy”. DERIVED recommendation: prefer soft-delete to preserve lesson history and block deletion with a catalog 422 when a legacy reference/progress row exists. Owner confirmation is required.
- Legacy Study DDL has resources.lesson_id and lesson_progress.lesson_id references but no deleted_at/soft-delete marker. No SQL mutation is specified against a guessed column.
- V1-PILOT uses UUID lesson IDs and restrictive child FKs; it is not the physical schema for this int64 endpoint.
- DeleteResult.deleted_at is required, but current checked-in lesson schemas do not supply a deletion timestamp.
- API #85 explicitly writes status + audit; API #86 does not copy that audit effect.
- Admin guard/policy and live schema are not verified in Study source.
- API guideline expects error data:null; current helper defaults absent error data to {}.

## Assumptions

- Candidate effect is logical soft-delete; hard delete and cascade are not selected.
- Candidate policy blocks when any approved progress/reference dependency exists and maps to 422 DESIGN_VALIDATION_ERROR; exact blocker set is DERIVED.
- Successful response requires a persisted deleted_at from an approved source; no application-clock fallback is proposed.
- Dependency checks and approved soft-delete should share a transaction to avoid a check/write race; this is DERIVED.

## Conflicts

- Catalog title asks for conditional progress/reference checks; exact relation set and behavior are not specified.
- AC-34 offers “Soft delete / delete theo policy”; chosen soft-delete is a DERIVED recommendation pending confirmation.
- DeleteResult requires deleted_at while legacy/V1-PILOT lesson schemas have no deletion timestamp.
- Legacy BIGINT references and V1-PILOT UUID restrictive references cannot be combined.
- Current Admin guard, route and endpoint-specific error handling are absent.

## Security note

- Authenticate Bearer JWT, Admin role and lesson-management permission before looking up the lesson or dependencies.
- Do not use the Student guard for this Admin endpoint.
- Do not reveal learner identities, progress details, resource URLs, raw SQL or stack traces.
- Do not remove dependency/history rows.

## Performance note

- Q1 checks one lesson ID; Q2 uses bounded EXISTS checks for the approved relation set.
- Do not load complete progress/resource rows when an existence check is sufficient.
- Live indexes, query plan, transaction isolation and DB availability are unknown.

---

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
