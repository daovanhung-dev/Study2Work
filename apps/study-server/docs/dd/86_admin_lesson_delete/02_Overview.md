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
| Consumer/Actor | Admin; fine-grained lesson-management permission chưa có source |
| Authentication | Bearer JWT |
| Authorization | Shared ADMIN role guard đã có; policy lesson-management riêng của AC-34 chưa có source. |
| Direct request | path lesson_id:int64!; không body/query. |
| Direct response | ApiEnvelope<DeleteResult>; HTTP 200 DESIGN_RESOURCE_DELETED. |
| DeleteResult | id:int64, status:"deleted", deleted_at:date-time. |
| Direct errors | 401/403/404/422/500 với đúng mã catalog. |
| Basis | Method/path/auth/input/response/status/error set DIRECT; legacy `DELETED` marker, blockers và `updated_at` mapping DERIVED. |
| Status | Draft — Needs Confirmation |
| Current implementation | SOURCE_BACKED locally — shared ADMIN guard, lock/dependency checks, soft-delete transaction and HTTP tests. |
| Transaction | API #86 view locks the target, checks dependencies, writes the tombstone, maps the response, and commits; failures roll back. |
| Side effects | Sets legacy candidate `lessons.status='DELETED'` and `updated_at`; preserves dependency and #85 audit rows. |

## Sources

- [Catalog và reusable schemas](../../../../../docs/lists/list_api.md) — API #86, DeleteResult, ApiEnvelope và exact business codes.
- [AC/API index, AC-34](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — Admin lesson-management permission và APIs #82–#86.
- [AC-34 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — node n5 đọc lesson + dependencies; n11 DELETE; n12 soft delete/delete theo policy; n13 reload danh sách.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — candidate BIGINT lessons; resource, progress, upload-link and status-audit relations; no dedicated `deleted_at` column.
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql) — UUID/versioned Lesson và child FK RESTRICT; model khác catalog int64.
- [API #82 list](../82_admin_lessons_list/02_Overview.md), [#83 detail](../83_admin_lesson_detail/02_Overview.md), [#84 update](../84_admin_lesson_update/02_Overview.md), [#85 status](../85_admin_lesson_status/02_Overview.md) — ranh giới của nhóm AC-34.
- [API #72 user delete](../72_admin_user_delete/02_Overview.md) and [#77 course delete](../77_admin_course_delete/02_Overview.md) — precedent cho DeleteResult, dependency check và soft-delete gap.
- [Current router](../../../app/api/v1.py), [auth helper](../../../app/utils/auth.py), [middleware](../../../app/core/middleware.py), [response helper](../../../app/core/responses.py) — current runtime/error boundary.
- [API guidelines](../../../../../contracts/api-guidelines/README.md) — error envelope expectation.

## Tables read

| Relation | Candidate fields/relationship | Basis/status |
|---|---|---|
| Legacy lessons | id, course_id, name, content, video_url, sort_order, status, created_at, updated_at | BIGINT DDL artifact; `DELETED` marker and timestamp mapping are DERIVED. |
| Legacy resources | lesson_id references lessons.id | Any row is a DERIVED blocker; live FK/policy unknown. |
| Legacy lesson_progress | lesson_id references lessons.id | Any row is a DERIVED blocker; no status filter is applied. |
| Legacy lesson_uploads | lesson_id references lessons.id, upload_id references uploads.id | Any row is a DERIVED blocker; link and asset are preserved. |
| lesson_status_audit_logs | lesson_id FK to lessons.id | Retained as history; does not block logical soft-delete. |
| V1-PILOT lessons | UUID id, chapter_id, course_version_id, title, summary, position, estimated_minutes, is_preview | Different model; no deletion marker. |
| V1-PILOT content_blocks / assessment_placements / lesson_progress_facts | lesson_id UUID FKs with ON DELETE RESTRICT | Separate pilot dependencies; do not mix with BIGINT API model. |

## Tables write

| Relation | Candidate fields/effect | Basis/status |
|---|---|---|
| Lesson persistence | lessons.status, lessons.updated_at | Set `DELETED` and `CURRENT_TIMESTAMP`; return DB timestamp as `deleted_at` following API #77. |
| Dependency rows | Read only | Check progress, resources, and lesson uploads; no child mutation or cascade. |
| Audit | Existing #85 history only | Preserve `lesson_status_audit_logs`; #86 inserts no audit row. |

## Mục chú ý

- Catalog #86 requires checking progress/reference. The local DERIVED policy blocks any `lesson_progress`, `resources`, or `lesson_uploads` row with catalog 422.
- AC-34 says “Soft delete / delete theo policy”. The local fallback sets `lessons.status='DELETED'` to preserve history; active Admin, Mentor, and resource reads/writes hide or reject the tombstone.
- Legacy Study DDL has no Lesson `deleted_at`. The local fallback sets `updated_at=CURRENT_TIMESTAMP` and maps the returned DB timestamp to `DeleteResult.deleted_at`, following API #77.
- V1-PILOT uses UUID lesson IDs and restrictive child FKs; it is not the physical schema for this int64 endpoint.
- DeleteResult.deleted_at is required; the local fallback uses the persisted legacy `updated_at` returned by the mutation.
- API #85 explicitly writes status + audit; API #86 does not copy that audit effect.
- Shared ADMIN role is enforced locally; fine-grained lesson-management permission and live schema are not verified.
- Error helper emits `data:null`; API #86 HTTP tests confirm the blocker response.

## Assumptions

- Logical soft-delete uses the legacy status marker; hard delete, schema migration, and cascade are not selected.
- `lesson_progress`, `resources`, and `lesson_uploads` are local blockers. Existing status audit history is retained and is not a blocker.
- Repeated DELETE returns 404 because the lock query excludes rows already marked `DELETED`.
- Lock, dependency checks, and mutation share one transaction; fake-session tests do not verify live FK lock behavior.

## Conflicts

- Catalog title asks for conditional progress/reference checks; exact relation set and behavior are not specified.
- AC-34 offers “Soft delete / delete theo policy”; the status marker and timestamp alias are DERIVED pending owner confirmation.
- DeleteResult `deleted_at` maps to DB-returned legacy `updated_at`; live column metadata remains unverified.
- Legacy BIGINT references and V1-PILOT UUID restrictive references cannot be combined.
- Fine-grained AC-34 permission remains unsupported; shared ADMIN guard and endpoint error mapping are wired locally.

## Security note

- Authenticate Bearer JWT and shared ADMIN role before looking up the lesson or dependencies; dedicated permission is unsupported.
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
