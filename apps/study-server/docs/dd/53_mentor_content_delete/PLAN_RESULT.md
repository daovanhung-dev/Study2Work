# Plan Result — API #53 Xóa nội dung Mentor

## Kết quả plan trước authoring

- Contract giữ nguyên: DELETE /api/v1/mentor/content/{content_id}; Bearer JWT role Mentor; path content_id:int64!; không body/query; ApiEnvelope<DeleteResult>; HTTP 200 DESIGN_RESOURCE_DELETED; exact errors 401/403/404/422/500.
- AC-22 trực tiếp xác nhận quyền quản lý course, DELETE/soft delete Content, rồi reload cây.
- Content.parent_id cho phép suy ra direct-child dependency. Local fallback chặn khi còn active child, trả 422, không cascade/reparent; guard này vẫn DERIVED. Query dùng local migration 006 mapping.
- PUBLISHED phải được unpublish qua #52 trước theo DERIVED guard; non-PUBLISHED states hiện được phép xóa, nhưng pending-review queue effect remains open.
- Soft delete dùng local `contents.deleted_at = CURRENT_TIMESTAMP`, giữ row/history và loại target khỏi API #49 active list. Không tạo ContentStatus mới hoặc audit table.
- API #53 route/module/tests are implemented locally. Fake-DB tests verify orchestration/contract only; live schema, migration application and deletion policy remain unverified/open.

## Input/source manifest

| Source | Phạm vi đọc | Bằng chứng dùng | Trạng thái |
|---|---|---|---|
| docs/lists/list_api.md | Row #53, Content, DeleteResult | Contract, field/status/error set | DIRECT |
| AC_UNICA/00_AC_API_INDEX.md | AC-22/AC-33 | Điều hướng diagram | DIRECT index |
| AC_03_MENTOR_TEACHING.drawio | Page AC-22 nodes/edges | Permission, soft delete, reload | DIRECT |
| AC_04_ADMIN_MANAGEMENT.drawio | Page AC-33 nodes/edges | PENDING_REVIEW, approval/rejection/audit | DIRECT; approval/publication ambiguity retained |
| DD #49–#52 | Overview/request/mapping/open questions/reports | Tree, create, revision, publication proposals | Related design evidence |
| Legacy DB.sql + migration 006 | Content base inventory | Local `contents` includes `parent_id`/`deleted_at` | Legacy artifact; live schema unknown |
| V1-PILOT 02_study_db.sql | lessons/content_blocks/review DDL | UUID and lesson-bound schema | Not equivalent to catalog Content |
| app/api/v1.py, modules, tests | Route/module/test scan | DELETE route, module, middleware contract path reuse and HTTP tests | Current source |
| Registered DD_API_Template_MD | Eight templates and appendix suffixes | Markdown structure | Registry-wired |
| Worklogs #48–#52 and count log | Prior decisions and status | Source gaps/lifecycle | Reviewed |

## API Requirement Matrix

| API ID | Method/path | Auth/input | Response/success | Errors | Behavior/status |
|---|---|---|---|---|---|
| #53 | DELETE /api/v1/mentor/content/{content_id} | Bearer Mentor; content_id:int64!; no body/query | ApiEnvelope<DeleteResult>; 200 DESIGN_RESOURCE_DELETED | 401/403/404/422/500 with catalog DESIGN_* | Soft delete DIRECT; dependency/unpublish guards DERIVED |

## Pre-authoring matrices

### Request Usage Matrix

| Request item | Mapping use | Status |
|---|---|---|
| Authorization | Authenticate Mentor and check course permission | Role DIRECT; principal/assignment SOURCE_REQUIRED |
| content_id | Q1 target lookup and DeleteResult.id | Type DIRECT; raw signed-int64 parsing; invalid path maps to 404 by local Content convention |
| Body/query | None | DIRECT omission |

### Query Matrix

| Query | Purpose | Logical source/predicate | Status |
|---|---|---|---|
| Q1 | Lock target/course scope | `contents` joined to `courses`; `deleted_at IS NULL` | Local source-backed mapping; live schema unverified |
| Q2 | Check dependency | active child with same course and `parent_id = target.id` | Local SQL mapping; child-block rule DERIVED |

### Mutation Matrix

| Mutation | Condition | Logical effect | Status |
|---|---|---|---|
| M1 | Authorized, not PUBLISHED and no active direct child | Set `contents.deleted_at = CURRENT_TIMESTAMP`; return id/status/deleted_at | Local implementation; guards DERIVED; live migration unverified |
| Cascade/reparent | A direct child exists | No child mutation | DERIVED safeguard |
| Audit/schema writes | No approved mapping | Not prescribed | SOURCE_REQUIRED |

### Response Source Matrix

| Field | Source | Status |
|---|---|---|
| businessCode | Catalog | DIRECT exact code |
| data.id | Target Content | Contract DIRECT; local source `contents.id` |
| data.status | DeleteResult literal deleted | DIRECT |
| data.deleted_at | `UPDATE ... RETURNING deleted_at` | Field DIRECT; local source-backed mapping; timezone/live schema unverified |
| meta/traceId | Envelope/request context | Current `success_response` convention; covered by HTTP test |

## Assumptions and conflicts

- Direct child via parent_id is the only dependency relation inferable from reusable Content.
- PUBLISHED first goes through #52; deletion does not change Content.status.
- Soft delete preserves history and hides target from active views; storage/filter remain unconfirmed.
- Open: full dependency set, other status eligibility, pending queue withdrawal, repeat DELETE, live migration/deployment, audit, Mentor assignment policy, delete eligibility and #51 version history.
