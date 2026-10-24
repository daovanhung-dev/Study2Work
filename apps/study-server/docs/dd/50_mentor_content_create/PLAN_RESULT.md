# Plan Result — API #50 Tạo nội dung mới

## Kết quả plan trước authoring

- Task `docs`, scope `server-study`; giữ nguyên worktree hiện hữu ngoài thư mục API #50.
- Contract giữ nguyên `POST /api/v1/mentor/content`, Bearer JWT, role Mentor, body `{course_id:int64!, content_type:ContentType!, title:string!, payload:object!}`, response HTTP 201 `DESIGN_RESOURCE_CREATED` và `ApiEnvelope<Content>`.
- Error set chính xác theo catalog: 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 422 `DESIGN_VALIDATION_ERROR`, 500 `DESIGN_INTERNAL_ERROR`; API #50 không khai báo 404.
- AC-22 POST flow: insert Content rồi reload content tree. AC-33 mô tả queue đọc trạng thái `PENDING_REVIEW`; suy ra trạng thái ban đầu của API #50 là đề xuất `DERIVED`, cần xác nhận.
- Request không có `parent_id` hoặc `order`; đề xuất root `parent_id=null` và order nối tiếp trong root siblings là `DERIVED`, cần xác nhận.
- Legacy DB có `courses`/`lessons`, không có generic Content table. V1-PILOT `content_blocks` dùng mô hình UUID gắn lesson, không thay thế catalog Content BIGINT. Không tạo physical INSERT giả.
- Route/module/test API #50 không tìm thấy; DD mô tả design contract, không chứng minh runtime.
- Output là 8 sheet Markdown + `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md`, theo Study workflow; không tạo ZIP.

## Source inventory and coverage

| Source | Kind | Evidence used | Status |
|---|---|---|---|
| `docs/lists/list_api.md` | API catalog | #50 contract, exact codes, Content fields | DIRECT |
| `AC_UNICA/00_AC_API_INDEX.md` | AC index | AC-22 actor/precondition and lifecycle API set | DIRECT |
| `AC_03_MENTOR_TEACHING.drawio`, AC-22 | Activity diagram | POST → `INSERT Content` → reload tree | DIRECT logical flow |
| `AC_04_ADMIN_MANAGEMENT.drawio`, AC-33 | Moderation diagram | Queue reads `status=PENDING_REVIEW` | DIRECT queue condition; initial POST status is DERIVED |
| `DB_UNICA_TABLES.md` / legacy `DB.sql` | Legacy schema | Courses/lessons exist; generic Content table absent | Design artifact, live schema unknown |
| `infra/postgres/02_study_db.sql` | V1-PILOT DDL | UUID `content_blocks` linked by `lesson_id`, incompatible with catalog model as-is | Pilot artifact, live schema unknown |
| DD #49, DD #47, worklogs #48/#49/inventory | Related docs | Keep Content distinct from Lecture; reuse candidate direct-owner evidence without promoting it | DERIVED/open |
| Current Study Server router/modules/tests | Runtime source | API #50 route/module/test absent | UNWIRED / NOT_FOUND |
| `app/core/responses.py` and middleware | Runtime helpers | Generic envelope/error behavior; future allowlist integration risk | Current helpers; conditional discrepancy |

## API Requirement Matrix

| Requirement | Source | DD coverage | Status |
|---|---|---|---|
| POST endpoint + Bearer Mentor auth | Catalog #50 | Cover, Overview, Request, Error | DIRECT contract; runtime absent |
| Four required body fields | Catalog #50 | Request + usage matrix | DIRECT types/required; detailed constraints partly SOURCE_REQUIRED |
| AC-22 manage-course permission | AC-22 | Overview + Data Mapping | DIRECT precondition; principal/access implementation SOURCE_REQUIRED |
| Insert then reload tree | AC-22 diagram | Overview + Data Mapping + lifecycle note | DIRECT sequence; reload is consumer action |
| Create response Content | Catalog #50 | Response + response-source matrix | DIRECT shape; persistence projection unresolved |
| Pending moderation queue | AC-33 | Overview + mapping + table | Queue value DIRECT; initial create transition DERIVED |
| Exact success and errors | Catalog #50 | Overview, Response, Error, Mapping | DIRECT; no extra code/status added |

## Pre-authoring matrix plan

| Matrix | Rows/coverage | Key unresolved areas |
|---|---|---|
| Request Usage | Authorization + all 4 body fields | Principal binding, enum, payload rules, course error mapping |
| Query | Candidate Q1 course/owner lookup; no approved Content pre-read | Legacy-only owner candidate; assignment relation absent |
| Mutation | One logical INSERT Content | Physical table, ID strategy, transaction, columns and projection SOURCE_REQUIRED |
| Response Source | Envelope + all 8 Content fields | ID, enum/payload storage, status enum, parent/order schema/default |
| Error | Exactly 4 catalog error rows | Missing-course branch and detailed validation rules need confirmation |

## Derived proposals and gates

- Initial status `PENDING_REVIEW`: `DERIVED` from AC-22 create and AC-33 queue precondition; product/source confirmation needed.
- Root placement (`parent_id=null`) and sibling order allocation: `DERIVED`; review before implementation.
- Legacy `courses.id/mentor_id` access query: candidate only; do not treat as live schema or complete authorization.
- Content physical write remains `SOURCE_REQUIRED`; no SQL INSERT or new table/column is proposed as if approved.
- API #53 now exists; full AC-22/AC-33 macro-review findings and unresolved questions are recorded below.

## AC-22/AC-33 Macro-review #49–#53

**Kết quả:** VERIFIED_WITH_OPEN_QUESTIONS — các API đã được đối chiếu liên kết; contract/schema owner vẫn cần chốt các câu hỏi bên dưới.

| Liên kết | Kết quả rà soát | Trạng thái |
|---|---|---|
| #49 read tree ↔ #50 create | AC-22 gọi reload sau POST; #49 catalog vẫn trả một Content, chưa định nghĩa tree cardinality. #50 đề xuất node mới ở root/PENDING_REVIEW. | Shape/root/visibility cần xác nhận. |
| #50 create ↔ #51 update/version | Cùng Content contract; create và revision mới cùng đề xuất PENDING_REVIEW; #51 giữ tree placement. | State transition và version storage DERIVED/SOURCE_REQUIRED. |
| #51 update ↔ #52 publish | Version update và publication-status update là hai thao tác logic riêng; #52 proposal yêu cầu revision APPROVED + readiness trước publish. | AC-33 approve APPROVED/PUBLISHED còn mơ hồ; request body/version selector chưa được catalog khóa. |
| #52 publish ↔ #53 delete | #53 đề xuất PUBLISHED phải unpublish qua #52 trước delete; #53 không đổi Content.status. | DERIVED; xác nhận sau khi chốt body/transition #52. |
| #49/#50/#51/#52 ↔ #53 hierarchy/delete | #53 chặn khi còn direct child qua parent_id, không cascade/reparent; soft delete giữ history và loại item khỏi active views/queue theo proposal. | Dependency set, soft-delete storage và filtering chưa được xác nhận. |
| Shared auth/schema/errors | Mentor course permission cần thiết; generic Content BIGINT model, enum/payload/version, principal binding và middleware path wiring chưa có source runtime. | SOURCE_REQUIRED; không DD nào là implementation-ready. |

Không có thay đổi nào biến các proposal thành contract đã duyệt. API #53 và các DD #49–#52 vẫn ở trạng thái Draft — Needs Confirmation.
