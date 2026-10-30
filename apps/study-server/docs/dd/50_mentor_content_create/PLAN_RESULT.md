# Plan Result — API #50 Tạo nội dung mới

## Kết quả plan trước authoring

- Task `coding` (secondary `test`, `docs`), scope `server-study`; giữ nguyên toàn bộ worktree có sẵn và chỉ thêm module/route/tests/DD/context liên quan API #50.
- Contract giữ nguyên `POST /api/v1/mentor/content`, Bearer JWT, role Mentor, body `{course_id:int64!, content_type:ContentType!, title:string!, payload:object!}`, response HTTP 201 `DESIGN_RESOURCE_CREATED` và `ApiEnvelope<Content>`.
- Error set chính xác theo catalog: 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 422 `DESIGN_VALIDATION_ERROR`, 500 `DESIGN_INTERNAL_ERROR`; API #50 không khai báo 404.
- AC-22 POST flow: insert Content rồi client reload tree. AC-33 queue đọc `PENDING_REVIEW`; API #50 implements that as a `DERIVED` initial status.
- Request không có `parent_id`/`order`; implementation creates root `parent_id=NULL`, allocates next active root order (first 0), and holds a course row lock until commit. These are `DERIVED` decisions.
- Legacy DDL/migration 006 provides the local BIGINT `contents` base model; V1-PILOT `content_blocks` remains a separate UUID model. API #50 INSERT source and TestClient tests are now present; live schema/migration remains unverified.
- Route, module, middleware mapping and TestClient cases are source-backed locally; no deployment or live DB behavior is claimed.
- Output là 8 sheet Markdown + `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md`, theo Study workflow; không tạo ZIP.

## Source inventory and coverage

| Source | Kind | Evidence used | Status |
|---|---|---|---|
| `docs/lists/list_api.md` | API catalog | #50 contract, exact codes, Content fields | DIRECT |
| `AC_UNICA/00_AC_API_INDEX.md` | AC index | AC-22 actor/precondition and lifecycle API set | DIRECT |
| `AC_03_MENTOR_TEACHING.drawio`, AC-22 | Activity diagram | POST → `INSERT Content` → reload tree | DIRECT logical flow |
| `AC_04_ADMIN_MANAGEMENT.drawio`, AC-33 | Moderation diagram | Queue reads `status=PENDING_REVIEW` | DIRECT queue condition; initial POST status is DERIVED |
| `DB_UNICA_TABLES.md` / legacy `DB.sql` / migration 006 | Legacy schema | `contents` base fields now present in checked-in artifact | Design artifact; live schema unknown |
| `infra/postgres/02_study_db.sql` | V1-PILOT DDL | UUID `content_blocks` linked by `lesson_id`, incompatible with catalog model as-is | Pilot artifact, live schema unknown |
| DD #49, DD #47, worklogs #48/#49/inventory | Related docs | Keep Content distinct from Lecture; reuse candidate direct-owner evidence without promoting it | DERIVED/open |
| Current Study Server router/modules/tests | Runtime source | API #50 router/module + 25 focused TestClient cases | SOURCE_BACKED locally; live DB unverified |
| `app/core/responses.py` and middleware | Runtime helpers | Generic envelope/error behavior; future allowlist integration risk | Current helpers; conditional discrepancy |

## API Requirement Matrix

| Requirement | Source | DD coverage | Status |
|---|---|---|---|
| POST endpoint + Bearer Mentor auth | Catalog #50 | Cover, Overview, Request, Error | DIRECT contract; locally wired and TestClient covered |
| Four required body fields | Catalog #50 | Request + usage matrix | DIRECT types/required; strict shape checks source-backed; enum/subtype rules SOURCE_REQUIRED |
| AC-22 manage-course permission | AC-22 + current Mentor APIs | Overview + Data Mapping | Direct-owner `courses.mentor_id` implementation; assignment policy remains open |
| Insert then reload tree | AC-22 diagram | Overview + Data Mapping + lifecycle note | DIRECT sequence; reload is consumer action |
| Create response Content | Catalog #50 | Response + response-source matrix | DIRECT shape; local INSERT/RETURNING projection implemented |
| Pending moderation queue | AC-33 | Overview + mapping + table | Queue value DIRECT; initial create transition implemented as DERIVED |
| Exact success and errors | Catalog #50 | Overview, Response, Error, Mapping | DIRECT; no extra code/status added |

## Pre-authoring matrix plan

| Matrix | Rows/coverage | Key unresolved areas |
|---|---|---|
| Request Usage | Authorization + all 4 body fields | Principal binding, enum, payload rules, course error mapping |
| Query | Q1 course owner `FOR UPDATE`; Q2 active root order aggregate | Legacy DDL local only; direct-owner/order rules marked DERIVED |
| Mutation | One `contents` INSERT/RETURNING | Local DDL mapping implemented; live schema status remains unknown |
| Response Source | Envelope + all 8 Content fields | ID, enum/payload storage, status enum, parent/order schema/default |
| Error | Exactly 4 catalog error rows | Missing-course branch and detailed validation rules need confirmation |

## Derived proposals and gates

- Initial status `PENDING_REVIEW`: implemented as `DERIVED` from AC-33 queue condition; product confirmation remains open.
- Root placement and zero-based next-active-sibling order: implemented as `DERIVED`; not direct diagram/catalog requirements.
- Direct `courses.mentor_id` check: implemented using API #47/#49 convention; assignment support remains open.
- Physical write targets only checked-in legacy `contents`; no new table/column or audit field is introduced; live schema remains unverified.
- API #53 now exists; full AC-22/AC-33 macro-review findings and unresolved questions are recorded below.

## AC-22/AC-33 Macro-review #49–#53

**Kết quả:** VERIFIED_WITH_OPEN_QUESTIONS — các API đã được đối chiếu liên kết; contract/schema owner vẫn cần chốt các câu hỏi bên dưới.

| Liên kết | Kết quả rà soát | Trạng thái |
|---|---|---|
| #49 read tree ↔ #50 create | AC-22 gọi reload sau POST; API #49 trả flat `Content[]`, loại soft-deleted rows và giữ mọi status. API #50 tạo root ở `PENDING_REVIEW` rồi trả cùng `Content` projection. | `PENDING_REVIEW`/root/order are DERIVED; local request/response projections align. |
| #50 create ↔ #51 update/version | Cùng Content contract; create và revision mới cùng đề xuất PENDING_REVIEW; #51 giữ tree placement. | State transition và version storage DERIVED/SOURCE_REQUIRED. |
| #51 update ↔ #52 publish | Version update và publication-status update là hai thao tác logic riêng; #52 proposal yêu cầu revision APPROVED + readiness trước publish. | AC-33 approve APPROVED/PUBLISHED còn mơ hồ; request body/version selector chưa được catalog khóa. |
| #52 publish ↔ #53 delete | #53 đề xuất PUBLISHED phải unpublish qua #52 trước delete; #53 không đổi Content.status. | DERIVED; xác nhận sau khi chốt body/transition #52. |
| #49/#50/#51/#52 ↔ #53 hierarchy/delete | #53 chặn khi còn direct child qua parent_id, không cascade/reparent; soft delete giữ history và loại item khỏi active views/queue theo proposal. | Dependency set, soft-delete storage và filtering chưa được xác nhận. |
| Shared auth/schema/errors | API #50 now uses shared Mentor guard, direct owner pattern, local BIGINT Content DDL and registered middleware path. Enum/payload subtype, assignment policy and live schema remain unverified. | Runtime source-backed locally; product/schema gaps remain open. |

Không có thay đổi nào biến các proposal thành contract đã duyệt. API #53 và các DD #49–#52 vẫn ở trạng thái Draft — Needs Confirmation.
