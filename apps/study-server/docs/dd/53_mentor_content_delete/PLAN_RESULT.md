# Plan Result — API #53 Xóa nội dung Mentor

## Kết quả plan trước authoring

- Contract giữ nguyên: DELETE /api/v1/mentor/content/{content_id}; Bearer JWT role Mentor; path content_id:int64!; không body/query; ApiEnvelope<DeleteResult>; HTTP 200 DESIGN_RESOURCE_DELETED; exact errors 401/403/404/422/500.
- AC-22 trực tiếp xác nhận quyền quản lý course, DELETE/soft delete Content, rồi reload cây.
- Content.parent_id cho phép suy ra direct-child dependency. Đề xuất chặn xóa khi còn child chưa xóa, trả 422, không cascade/reparent. Physical query SOURCE_REQUIRED.
- Đề xuất PUBLISHED phải được unpublish qua #52 trước; đây là DERIVED để giữ #52 là chủ sở hữu publication state.
- Soft delete giữ revision/review history và loại target khỏi active views theo proposal. Không tạo tên tombstone column, ContentStatus mới, audit table hoặc SQL.
- Source hiện không có API #53 route/module/test; không có generic Content table tương thích trong DDL.

## Input/source manifest

| Source | Phạm vi đọc | Bằng chứng dùng | Trạng thái |
|---|---|---|---|
| docs/lists/list_api.md | Row #53, Content, DeleteResult | Contract, field/status/error set | DIRECT |
| AC_UNICA/00_AC_API_INDEX.md | AC-22/AC-33 | Điều hướng diagram | DIRECT index |
| AC_03_MENTOR_TEACHING.drawio | Page AC-22 nodes/edges | Permission, soft delete, reload | DIRECT |
| AC_04_ADMIN_MANAGEMENT.drawio | Page AC-33 nodes/edges | PENDING_REVIEW, approval/rejection/audit | DIRECT; approval/publication ambiguity retained |
| DD #49–#52 | Overview/request/mapping/open questions/reports | Tree, create, revision, publication proposals | Related design evidence |
| Legacy DB.sql | Table inventory | No generic Content model | Legacy artifact; live schema unknown |
| V1-PILOT 02_study_db.sql | lessons/content_blocks/review DDL | UUID and lesson-bound schema | Not equivalent to catalog Content |
| app/api/v1.py, modules, tests | Route/module/test scan | No #53 implementation | Current source |
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
| content_id | Q1 target lookup and DeleteResult.id | Type DIRECT; parse mapping needs runtime integration |
| Body/query | None | DIRECT omission |

### Query Matrix

| Query | Purpose | Logical source/predicate | Status |
|---|---|---|---|
| Q1 | Load target/course scope | Content.id = content_id; read course_id/status | Physical relation/columns SOURCE_REQUIRED |
| Q2 | Check dependency | child.parent_id = target.id and child not soft-deleted | parent_id DIRECT; active predicate DERIVED; physical query SOURCE_REQUIRED |

### Mutation Matrix

| Mutation | Condition | Logical effect | Status |
|---|---|---|---|
| M1 | Authorized, not PUBLISHED under proposal, no direct child | Soft-delete target and preserve history | Effect DIRECT; guards/history DERIVED; physical mapping SOURCE_REQUIRED |
| Cascade/reparent | A direct child exists | No child mutation | DERIVED safeguard |
| Audit/schema writes | No approved mapping | Not prescribed | SOURCE_REQUIRED |

### Response Source Matrix

| Field | Source | Status |
|---|---|---|
| businessCode | Catalog | DIRECT exact code |
| data.id | Target Content | Contract DIRECT; physical source SOURCE_REQUIRED |
| data.status | DeleteResult literal deleted | DIRECT |
| data.deleted_at | Successful operation time | Field DIRECT; generator/storage DERIVED/SOURCE_REQUIRED |
| meta/traceId | Envelope/request context | Convention; endpoint absent |

## Assumptions and conflicts

- Direct child via parent_id is the only dependency relation inferable from reusable Content.
- PUBLISHED first goes through #52; deletion does not change Content.status.
- Soft delete preserves history and hides target from active views; storage/filter remain unconfirmed.
- Open: full dependency set, other status eligibility, pending queue withdrawal, repeat DELETE, physical tombstone/audit, Mentor access mapping, Content persistence and #49 tree response.
