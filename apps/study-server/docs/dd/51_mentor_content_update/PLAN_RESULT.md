# Plan Result — API #51 Cập nhật nội dung Mentor

## Kết quả plan trước authoring

- Task `docs`, scope `server-study`; deliverable là một API DD Markdown, không ZIP.
- Catalog contract giữ nguyên `PUT /api/v1/mentor/content/{content_id}`, Bearer JWT role Mentor, `content_id:int64!`, `ApiEnvelope<Content>`, HTTP 200 `DESIGN_RESOURCE_UPDATED`, errors đúng 401/403/404/422/500.
- Catalog và AC-22 PUT node đều chỉ khai báo path; không có request body dù operation là update. Đây là `DISCREPANCY` cần contract owner xác nhận.
- Body đề xuất `content_type`, `title`, `payload` là full replacement của phần content-bearing fields, dùng các field đã có ở API #50; đây là `DERIVED`, không được trình bày như catalog contract.
- AC-22 xác định logical write `UPDATE Content + version`, sau đó reload cây. AC-33 đọc `content/version/author` và hàng đợi `PENDING_REVIEW`; suy ra revision mới ở trạng thái pending là `DERIVED`.
- Đề xuất giữ revision published trước đó phục vụ đến khi revision mới được review/publish; đây là lifecycle proposal cần macro-review với #50, #52 và AC-33.
- Không có generic Content/version table trong legacy schema; V1-PILOT UUID `content_blocks` và `row_version` không được dùng thay cho contract Content BIGINT.
- Không có route/module/test API #51 hiện tại; không sửa runtime/schema/catalog/diagram/client.
- Output: 8 sheet + 3 report dưới `apps/study-server/docs/dd/51_mentor_content_update/`.

## Input/source manifest

| Source | Đơn vị đọc | Nội dung sử dụng | Trạng thái |
|---|---|---|---|
| `docs/lists/list_api.md` | Row #51 + Content schema | Method/path/auth/path/response/status/errors; body omission | DIRECT contract |
| `AC_UNICA/00_AC_API_INDEX.md` | AC-22 | Mentor manage-course precondition, create/update/delete/publish lifecycle | DIRECT |
| `AC_03_MENTOR_TEACHING.drawio` | Page AC22, nodes/edges | PUT → `UPDATE Content + version` → reload tree | DIRECT logical flow |
| `AC_04_ADMIN_MANAGEMENT.drawio` | Page AC33, nodes/edges | Queue reads `PENDING_REVIEW`; reviewer reads content/version/author | DIRECT moderation condition; update transition DERIVED |
| `DB_UNICA_TABLES.md` + legacy `DB.sql` | Content/course/lesson sections | No generic Content/version mapping; legacy `courses.mentor_id` candidate only | Design artifact; live DB unknown |
| `infra/postgres/02_study_db.sql` | Course/version/content block definitions | UUID/versioned pilot model differs from catalog BIGINT Content | Pilot artifact; live DB unknown |
| DD #50 and #47 | Create Content and mutation precedent | Reuse content-bearing fields and candidate access boundary; do not copy Lesson SQL | Prior DD reference |
| `.agents/server-study/*`, manifest and `createDD-markdown` | Scope pages/registry/skill/template | Markdown-only Study output, 8-sheet template, matrices and review gates | Registered SOURCE_BACKED |
| Current Study router/app/tests/middleware | API route and error wiring | No API #51 route/module/test; path is outside design code allowlist | Current-source scan |

## API Requirement Matrix

| Requirement | Source | DD coverage | Status |
|---|---|---|---|
| PUT path + Mentor Bearer auth | Catalog #51 | Cover, Overview, Request, Error | DIRECT contract; runtime absent |
| `content_id:int64!` path | Catalog + AC-22 | Request + usage matrix | DIRECT |
| Request body | Catalog and diagram omit it | Request records omission and separate body proposal | DISCREPANCY; proposal DERIVED |
| Update Content and version | AC-22 PUT/database node | Overview, mapping, table | DIRECT logical effect; physical version model SOURCE_REQUIRED |
| Content response | Catalog reusable Content | Response and field source matrix | DIRECT shape; persistence projection unresolved |
| Pending review | AC-33 queue | Overview, mapping, table | DIRECT queue condition; new revision state DERIVED |
| Exact response/error codes | Catalog #51 | Response, Error, Mapping | DIRECT; no 409 or extra code |

## Pre-authoring matrices

### Request Usage Matrix

| Input | Use | Status/gap |
|---|---|---|
| Authorization | Mentor auth and stored-course access | Role DIRECT; identity/assignment SOURCE_REQUIRED |
| `content_id` | Load target, select current logical version | DIRECT path; physical relation SOURCE_REQUIRED |
| Proposed `content_type/title/payload` | Replace editable content fields | DERIVED body; enum, validation, schema SOURCE_REQUIRED |
| Existing `course_id` | Read from stored Content and preserve | DERIVED immutability proposal; physical mapping SOURCE_REQUIRED |
| Existing `status` | Read current state; apply proposed pending transition to new revision | DERIVED; lifecycle confirmation required |
| Existing `parent_id` | Preserve stored value | DERIVED; physical mapping SOURCE_REQUIRED |
| Existing `order` | Preserve stored value | DERIVED; physical mapping SOURCE_REQUIRED |

### Query Matrix

| Query | Purpose | Source/condition | Status |
|---|---|---|---|
| Q1 | Load Content | Logical `Content.id = :content_id` | Relation/columns SOURCE_REQUIRED |
| Q2 | Check course direct owner | Legacy candidate `courses.id/mentor_id` from stored course | DERIVED only; assignment and identity missing |
| Q3 | Resolve current version | Content version relation/current selector | SOURCE_REQUIRED |

### Mutation Matrix

| Mutation | Logical target | Fields/effect | Status |
|---|---|---|---|
| M1 | Content + version | Replace `content_type` from proposed body | AC-22 logical effect DIRECT; body DERIVED; physical mapping SOURCE_REQUIRED |
| M1 | Content + version | Replace `title` from proposed body | Body DERIVED; physical mapping SOURCE_REQUIRED |
| M1 | Content + version | Replace `payload` from proposed body | Body DERIVED; payload schema SOURCE_REQUIRED |
| M1 | Content + version | Preserve `id` | Preserve rule DERIVED; physical mapping SOURCE_REQUIRED |
| M1 | Content + version | Preserve `course_id` | Preserve rule DERIVED; physical mapping SOURCE_REQUIRED |
| M1 | Content + version | Preserve `parent_id` | Preserve rule DERIVED; physical mapping SOURCE_REQUIRED |
| M1 | Content + version | Preserve `order` | Preserve rule DERIVED; physical mapping SOURCE_REQUIRED |
| M1 | Content + version | Advance revision; set new revision `PENDING_REVIEW` candidate | Version effect DIRECT; transition DERIVED; macro-review required |

### Response Source Matrix

| Response field | Candidate source | Status |
|---|---|---|
| Envelope + `businessCode` | Current envelope convention + catalog code | DIRECT shape/code; helper integration conditional |
| `data.id/course_id` | Existing Content | Physical mapping SOURCE_REQUIRED |
| `data.content_type/title/payload` | Proposed request/new revision | DERIVED body; type/schema SOURCE_REQUIRED |
| `data.status` | Proposed review state | DERIVED `PENDING_REVIEW` |
| `data.parent_id/order` | Existing Content | Preserve in proposal; mapping SOURCE_REQUIRED |
| Version field | Not in catalog Content | Do not add to response |

## Pair review API #50 ↔ #51

- Shared contract model is `Content`; #50 creates it and #51 targets it by ID.
- #50 supplies `course_id/content_type/title/payload`; #51 reuses only `content_type/title/payload` as a proposed full update body and derives course from the stored target.
- Both propose a pending-review state for newly authored content/revision. This is not confirmed by AC-22 as a create/update transition; retain `DERIVED` status.
- #50 proposes root/order defaults for creation; #51 preserves stored tree placement. Physical Content schema/version model is still the shared blocker.
- #52 publish/unpublish and AC-33 approval may change state differently; after #53, the full macro-review is recorded below and the ambiguity remains open.

## Derived proposals and gates

- Body: full replacement `{content_type, title, payload}` from existing Content contract fields; confirm method/requiredness and field mutability.
- Version: each successful PUT creates/advances a logical revision; preserve prior history. Exact revision model, conflict policy, and metadata are SOURCE_REQUIRED.
- Review: new revision is proposed as `PENDING_REVIEW`; existing published revision remains active pending review/publish. Confirm against #52 and AC-33.
- Keep error set exactly 401/403/404/422/500; no concurrency code added.
- No physical SQL UPDATE/INSERT is included until approved Content/version persistence exists.

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
