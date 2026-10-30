# Plan Result — API #52 Publish/unpublish nội dung Mentor

## Kết quả plan trước authoring

- Task docs-only trong scope server-study; Study deliverable là Markdown, không ZIP.
- Giữ contract catalog: PATCH /api/v1/mentor/content/{content_id}, Bearer JWT role Mentor, path content_id:int64!, ApiEnvelope<Content>, HTTP 200 DESIGN_RESOURCE_UPDATED và đúng errors 401/403/404/422/500.
- Catalog và AC-22 chỉ khai báo path; body/action selector vắng mặt dù API title có publish/unpublish. Proposal {published:boolean!} được đánh dấu DERIVED, không thay contract canonical.
- AC-22 quy định logical UPDATE publication status rồi reload cây. AC-33 nêu PENDING_REVIEW và APPROVED/PUBLISHED + audit, nhưng không tách approval khỏi publication.
- Proposal state machine: APPROVED → PUBLISHED sau readiness; PUBLISHED → APPROVED khi unpublish; same target no-op. Không eligible state → 422 candidate. Mọi transition/readiness detail DERIVED.
- Follow-up API #49 ngày 2026-10-25 thêm legacy `contents` base relation vào DDL/migration 006; version-history relation còn thiếu. Pilot content_blocks là UUID/lesson-bound và không thay thế Content BIGINT.
- DD #49–#51 review: #50 create và #51 new revision đề xuất PENDING_REVIEW; #52 phải phối hợp với Admin AC-33 trước khi lifecycle được chốt.
- Current source không có API #52 route/module/test; middleware allowlist thiếu path.
- Output: 8 template sheets + PLAN_RESULT.md + OPEN_QUESTIONS.md + VERIFICATION_REPORT.md.

## Input/source manifest

| Source | Đơn vị đọc | Nội dung sử dụng | Trạng thái |
|---|---|---|---|
| docs/lists/list_api.md | Row #52, Content schema | Request/path/response/status/errors | DIRECT contract |
| AC_UNICA/00_AC_API_INDEX.md | AC-22 | Mentor permission and endpoint sequence | DIRECT |
| AC_03_MENTOR_TEACHING.drawio | Page AC22 nodes/edges | PATCH → UPDATE publication status → reload tree | DIRECT logical effect |
| AC_04_ADMIN_MANAGEMENT.drawio | Page AC33 nodes/edges | PENDING_REVIEW queue; APPROVED/PUBLISHED + audit | DIRECT evidence; relation to #52 unresolved |
| DD #49, #50, #51 | Overview/request/mapping/open questions | Tree/read semantics, create initial state and update version proposal | Related design evidence; proposals remain DERIVED |
| Legacy DB guide, `DB.sql`, migration 006 | course/Content base relations | `contents` base model present locally; no version-history relation | Legacy design artifact; live DB unknown |
| infra/postgres/02_study_db.sql | course_versions/chapters/lessons/content_blocks | UUID, lesson-bound model | V1-PILOT artifact; not equivalent |
| apps/study-server/app/api/v1.py | Route declarations | No #52 route; 12 catalog IDs route matched | Current source |
| middleware.py/responses.py | DESIGN_CONTRACT_PATHS and error serialization | Path absent; missing error data becomes {} | Current source |
| Registered createDD-markdown templates | Eight sheet templates/appendices | Required Markdown structure and appendix tails | Registry-wired template |
| .agents/worklog/2026-10-24/* | Worklog preflight + linked API context | #48–#50 selected and read; #51/count worklog also read | Workflow evidence |

## API Requirement Matrix

| Requirement | Source | DD coverage | Status |
|---|---|---|---|
| PATCH path, Bearer Mentor, int64 path | Catalog #52 | Cover, Overview, Request, Error | DIRECT; route absent |
| Canonical body/query omitted | Catalog + AC-22 | Request records omission | DIRECT |
| Proposed target-state boolean | Needed to select publish/unpublish | Request/Mapping/Open Questions | DERIVED; contract confirmation required |
| Readiness validation | Catalog name/purpose | Mapping/Error | Intent DIRECT; exact criteria SOURCE_REQUIRED |
| Publication-status update + reload tree | AC-22 | Overview/Mapping/table | Logical effect DIRECT |
| Approved/published lifecycle | AC-33 | Mapping/table/Open Questions | State names DIRECT; transition DERIVED |
| Content response and exact errors | Catalog | Response/Error/Mapping | Shape/code set DIRECT; physical mapping unresolved |

## Pre-authoring matrices

### Request Usage Matrix

| Input | Use | Status/gap |
|---|---|---|
| Authorization | Mentor auth and stored-course access | Role DIRECT; principal/assignment SOURCE_REQUIRED |
| content_id | Load Content/current status | Path DIRECT; lookup SOURCE_REQUIRED |
| Canonical body | None declared | DIRECT omission |
| Proposed published | Explicit target state | DERIVED; not approved contract |
| Query | None | DIRECT omission |

### Query Matrix

| Query | Purpose | Logical data | Status |
|---|---|---|---|
| Q1 | Load target | Content identity, course_id, ContentStatus, current revision | Physical relation SOURCE_REQUIRED |
| Q2 | Authorize Mentor | Stored course and owner/assignment | Legacy courses.mentor_id DERIVED candidate only |
| Q3 | Validate readiness | Approved status and subtype completeness | Readiness intent DIRECT; rules/schema SOURCE_REQUIRED |

No executable SQL is supplied for generic Content. Do not infer table/column names.

### Mutation Matrix

| Branch | Proposed condition | Logical effect | Status |
|---|---|---|---|
| Publish | desired state true; APPROVED; readiness passes | Set PUBLISHED | DERIVED transition |
| Unpublish | desired state false; PUBLISHED | Set APPROVED | DERIVED transition |
| Already target | Existing state equals desired state | No-op | DERIVED idempotency |
| Pending/rejected/other | Not publish eligible | No mutation; 422 candidate | DERIVED; enum incomplete |
| Content revision | Any #52 branch | Preserve payload/version; no new revision | DERIVED separation from #51 |

### Response Source Matrix

| Field | Candidate source | Status |
|---|---|---|
| Envelope and businessCode | Study convention + catalog | DIRECT shape/code; runtime absent |
| data.id | Path-selected Content | Physical mapping SOURCE_REQUIRED |
| data.course_id | Stored Content | SOURCE_REQUIRED |
| data.content_type/title/payload | Stored Content | Enum/persistence/source unresolved |
| data.status | Resulting state | APPROVED/PUBLISHED terms direct; transition DERIVED |
| data.parent_id/order | Stored Content | Null/omit and physical mapping SOURCE_REQUIRED |
| meta/traceId | Envelope/request trace | Helper alignment; runtime absent |

## Pair review API #50 ↔ #52

- #50 creates logical Content with a DERIVED PENDING_REVIEW initial state proposal. #52 proposal does not allow publishing pending content; it requires an approved state and readiness.
- Content schema and persistence remain the shared blocker; no Content table/enum/payload mapping was invented.
- The request/action contract remains incomplete because #50 creates content but #52's catalog body does not select publish or unpublish.

## Pair review API #51 ↔ #52

- #51 proposes a new Content revision enters PENDING_REVIEW while publication state/version is handled separately.
- #52 proposal updates publication status only and creates no new revision.
- Exact current-revision selection and behavior while a new revision is pending remain open; must align with AC-33 approval.

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

## Implementation follow-up — 2026-10-25

API #52 is now implemented locally in `app/modules/mentor/api_52_mentor_content_publish` and wired through `app/api/v1.py` plus `DESIGN_CONTRACT_PATHS`. The strict `{published:boolean}` body, APPROVED→PUBLISHED/PUBLISHED→APPROVED transitions, same-target no-op, APPROVED status readiness gate, and direct `courses.mentor_id` check are DERIVED fallbacks; catalog and AC-22 still declare path only. The view locks Content/Course and changes only `contents.status`; it does not create a revision. Fake DB tests do not establish live PostgreSQL schema/deployment or AC-33 approval behavior. See the current implementation addendum in `VERIFICATION_REPORT.md` after final verification.
