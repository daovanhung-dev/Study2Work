# Plan Result — API #49 Lấy cây nội dung course

## Kết quả plan trước authoring

- Task `docs`, scope `server-study`; worktree DD #39–#48 và worklogs được giữ nguyên.
- Contract giữ nguyên `GET /api/v1/mentor/courses/{course_id}/content`, Bearer JWT Mentor, path `course_id:int64!`, no body/query, `ApiEnvelope<Content>`, HTTP 200 và đúng errors 401/403/404/500.
- AC-22 sequence là GET → đọc sections/lessons/content → Mentor chọn nhánh CRUD/publish; #49 là read-only, thao tác còn lại thuộc #50–#53.
- Response tree có discrepancy: purpose/diagram mô tả cây nhưng catalog trả một `Content`; không tự đổi thành collection/nested children.
- Legacy `courses.mentor_id` chỉ là candidate direct-owner check theo #46/#47. Generic Content tree không có bảng trong legacy DB guide/ERD. Pilot DDL có UUID `chapters/lessons/content_blocks`, không gộp vào contract BIGINT.
- Q2 content query, payload shape, enum members, tree cardinality/order/visibility, Mentor ID binding và empty-tree/404 behavior là `SOURCE_REQUIRED`.
- Output là 8 sheet Markdown + 3 report. Study workflow cấm ZIP output. Không sửa runtime/schema/catalog/diagram.

## Source inventory and coverage

| Source | Kind | Evidence used | Status |
|---|---|---|---|
| `docs/lists/list_api.md` | Catalog contract | API #49 row; `Content` schema; exact success/errors | DIRECT |
| `AC_UNICA/00_AC_API_INDEX.md` | AC flow | AC-22 actor/precondition and #49–#53 endpoint set | DIRECT |
| `AC_03_MENTOR_TEACHING.drawio`, AC22 | Activity diagram | GET → read sections/lessons/content → branch CRUD/publish | DIRECT |
| `DB_UNICA_TABLES.md` / `DB_UNICA_ERD.drawio` | Legacy DB design | 16 tables; courses/lessons; no generic Content/sections table | DESIGN_ONLY |
| `infra/postgres/02_study_db.sql` | V1-PILOT DDL | UUID course_versions/chapters/lessons/content_blocks with different model | Pilot artifact, live DB unknown |
| DD #46–#48 | Related DDs | Legacy direct-owner candidate; distinguish AC-21 Lecture from AC-22 Content | DERIVED / OPEN |
| Current `app/api/v1.py`, modules, tests | Runtime source | No API #49 route/module/test | CURRENT: UNWIRED / NOT_FOUND |
| `app/core/responses.py`, `app/core/middleware.py` | Envelope/error dispatch | `error_response` defaults missing data to `{}`; API #49 path is outside `DESIGN_CONTRACT_PATHS`, so generic validation/exception fallbacks apply if future route is wired without allowlist update | CURRENT helper behavior; conditional future discrepancy |
| Registry + DD templates | Authoring | `createDD-markdown` wired to server-study; eight Markdown templates | WIRED |

## API Requirement Matrix

| API ID | Method | Endpoint | Auth/RBAC | Consumer | Purpose | Input/output baseline | Business rule | Tables/side effects | Folder/status |
|---|---|---|---|---|---|---|---|---|---|
| #49 | GET | `/api/v1/mentor/courses/{course_id}/content` | Bearer JWT; role Mentor | Mentor | Read course content before AC-22 mutation choice | path `course_id:int64!`; `ApiEnvelope<Content>`; HTTP 200 | Mentor must have management permission; exact access logic unresolved | Candidate SELECT legacy course; tree SELECT source-required; no mutation | `49_mentor_content_list`; Draft — Needs Confirmation |

### Contract matrix

| Item | Contract | Basis/status |
|---|---|---|
| Request | `course_id:int64!`; no body/query | Catalog DIRECT |
| Response | Content: `id:int64`, `course_id:int64`, `content_type:ContentType`, `title:string`, `payload:object`, `status:ContentStatus`, `parent_id?:int64`, `order:int32` | Catalog DIRECT; physical mapping SOURCE_REQUIRED |
| Success | 200 `DESIGN_RESOURCE_RETRIEVED` | Catalog DIRECT |
| Errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 500 `DESIGN_INTERNAL_ERROR` | Catalog DIRECT; detailed branches partly unresolved |
| Envelope | `success`, `businessCode`, `message`, `data`, `meta`, `traceId` | Reusable schema DIRECT; current helper error `data` differs from guideline |

## Request Usage Matrix

| Request field | Source | Data Mapping step | Validate | SQL/mutation usage | Branch/loop | Response use | Gap |
|---|---|---:|---|---|---|---|---|
| Authorization | Header | 1 | Bearer JWT and Mentor role per catalog | Principal for Q1 candidate access check | 401/403 | Not echoed | Mentor guard and numeric/UUID binding missing |
| `course_id` | Path | 1–2 | Required int64 | Bind Q1; intended scope Q2 | course missing/access | Intended `Content.course_id` | DB ID type/content projection unresolved |
| Body/query | None | N/A | None | None | None | None | DIRECT no input |

## Query Matrix

| Query ID | Purpose | Type | Base source | Columns | Join | Where | Order/pagination | Result/branch |
|---|---|---|---|---|---|---|---|---|
| Q1 | Course existence and direct-owner candidate | SELECT | Legacy `courses AS c` | `c.id`, `c.mentor_id` | None | `c.id = :course_id` | N/A | Candidate; owner mismatch → 403 only as DERIVED |
| Q2 | Read content hierarchy | SELECT | SOURCE_REQUIRED | SOURCE_REQUIRED | SOURCE_REQUIRED | course scope intended; exact predicates unknown | sibling order and visibility unknown; no pagination contract | Cannot map full Content/tree |

Q1 candidate SQL only for legacy schema:

```sql
SELECT c.id, c.mentor_id
FROM courses AS c
WHERE c.id = :course_id;
```

No executable Q2 SQL is approved.

## Mutation Matrix

| Mutation ID | Operation | Target table | Record condition | Fields | Value sources | Audit | Mapping file | Transaction | Failure behavior |
|---|---|---|---|---|---|---|---|---|---|
| None | None | N/A | Read-only API | None | N/A | N/A | N/A | N/A | N/A — no mutation |

## Response Source Matrix

| Response field | Type | Source type/table/column | Mapping/transform | Null/empty rule | Gap/status |
|---|---|---|---|---|---|
| `success` | boolean | Envelope branch | true on success | N/A | Convention |
| `businessCode` | string | Catalog literal | Exact per branch | Required | DIRECT |
| `message` | string | Application | Safe localized message | Exact copy unspecified | DERIVED |
| `data.id` | int64 | No generic Content source | None | Required | SOURCE_REQUIRED |
| `data.course_id` | int64 | Path or stored node | Decision required | Required | SOURCE_REQUIRED |
| `data.content_type` | ContentType | No source/enum values | None | Required | SOURCE_REQUIRED |
| `data.title` | string | No generic Content source | None | Required | SOURCE_REQUIRED |
| `data.payload` | object | No JSON schema | None | Required object | SOURCE_REQUIRED |
| `data.status` | ContentStatus | No source/enum values | None | Required | SOURCE_REQUIRED |
| `data.parent_id` | int64? | No generic parent relation | None | Optional null/omit unresolved | SOURCE_REQUIRED |
| `data.order` | int32 | No approved generic order column | None | Required | SOURCE_REQUIRED |
| `meta` | object | Envelope | No pagination fields | Empty/null helper behavior unresolved | Open |
| `traceId` | uuid | Request trace | Propagate trace | Required | Runtime route absent |

## Authoring/review decisions

1. Keep expected contract and current source separate; mark API #49 `UNWIRED / NOT_FOUND`.
2. Do not map pilot `content_blocks.content_json` to contract `payload` because IDs, version/parent relations and lifecycle differ.
3. Do not infer `children[]`, root nodes, empty array or page metadata from `parent_id?`.
4. Do not add `PUBLISHED` filter, sort order, validation code or mutation.
5. Keep open questions actionable and block a final implementation-ready query until schema/contract owners decide.
6. Record current middleware fallback: error data defaults to `{}`; unlisted paths use generic validation/internal codes. Add API #49 path to the design contract dispatch during future implementation if catalog codes must be preserved.
6. API #53 has now been authored; the full AC-22/AC-33 macro-review is recorded below.

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
