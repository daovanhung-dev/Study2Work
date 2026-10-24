# PLAN_RESULT — Study API #59

## Trạng thái trước authoring

- Plan được lập trước các sheet DD: `VERIFIED`.
- API: #59 — Lấy nội dung request/thread.
- Output: `59_mentor_support_request_detail/`.
- Status DD dự kiến: `Draft — Needs Confirmation`; physical support model, identity scope và nested projection chưa có mapping được duyệt.
- Loại: read-only; không có mutation DB.
- Phạm vi: AC-24 API detail #59. Không tạo code, test, schema, migration, catalog edit, diagram edit hoặc ZIP.

## API Requirement Matrix

| API ID | Contract item | Giá trị | Basis/status |
|---|---|---|---|
| #59 | Method/path | `GET /api/v1/mentor/support/{request_id}` | Catalog + AC-24; DIRECT |
| #59 | Actor/auth | Bearer JWT; role Mentor | Catalog + AC-24; DIRECT |
| #59 | Path | `request_id:int64!` | Catalog; DIRECT |
| #59 | Body/query | Không khai báo | Catalog; DIRECT |
| #59 | Success | HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<SupportRequest>` | Catalog + diagram; DIRECT |
| #59 | Errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 500 `DESIGN_INTERNAL_ERROR` | Catalog + diagram; DIRECT |

## Flow và ranh giới API

- AC-24 actor là Mentor; precondition nói request phải thuộc phạm vi phụ trách.
- #58 mở danh sách request; #59 đọc một request và conversation; #60 gửi reply; #61 đóng request theo nhánh conditional.
- API #59 chỉ đọc. Không ghi message, đổi status hoặc thực hiện resolve.
- Response là một `SupportRequest`, phù hợp endpoint detail. `messages[]` là field bắt buộc theo reusable schema; thứ tự, giới hạn, và visibility của message nội bộ chưa có contract.
- Các vướng mắc list cardinality của #58 vẫn thuộc #58; #59 không tự quyết định response của #58.

## Source và template manifest

| Nguồn | Định dạng | Đã đọc | Dùng để |
|---|---|---:|---|
| `docs/lists/list_api.md` | Markdown | Có | Contract #59 và reusable `SupportRequest`, `SupportMessage`, `UserSummary`, `UploadAsset` |
| `apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md` | Markdown | Có | Actor, precondition/postcondition và AC-24 API sequence |
| `apps/study-server/docs/diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio` | Draw.io | Có | Node #59 “Đọc request + conversation” và #60/#61 side effects |
| `infra/postgres/study-server/DB.sql`, DB table guide, ERD | SQL/Markdown/Draw.io | Có | Legacy model không có support request/message tables |
| `infra/postgres/02_study_db.sql` | SQL | Có | V1-PILOT candidate `support_tickets`/`support_messages`; UUID model không map trực tiếp sang contract |
| Current Study router/modules/tests/middleware | Python | Có | API #59 route/module/test absent; Mentor guard absent; design error allowlist excludes path |
| API Guidelines | Markdown | Có | Envelope/trace convention and error data guideline |
| DD #58 and worklogs #48–#50 | Markdown | Có | Carry forward AC-24 gaps; Study DD matrices and template practice |

Registered `createDD-markdown` is `SOURCE_BACKED` for `server-study`; the Study `docs-dd` workflow requires Markdown and overrides shared ZIP packaging. The eight registered templates and verified SHA-256 values are:

| Template | SHA-256 |
|---|---|
| `00_Cover.md` | `fd5f568c5329d3069fbaff617a6f4ed3b5ffaf050e042c95b7c9100a05f79e63` |
| `01_Lich_su.md` | `d1cec6573433a9551812bf47552f8a44d7c533d790341941047c410e1d57771e` |
| `02_Overview.md` | `c2879c2f0e007395558dfee4167484786c5aadb3fdd63ab135ca111e7c5f8aa6` |
| `03_Request.md` | `37aaa1e9d7f3e83329e81ab38d922c9dff959284d5b7b3ae353878798dd4b7aa` |
| `04_Response.md` | `5bcb43ba5eb487302dd5d5efde4383b9f452f9fed2149f55315d64ff78a19ab8` |
| `05_Data_Mapping.md` | `11bc77bc0522d3af27b9499114991c8819046ac32bde5c1efdc841be088dcc5b` |
| `06_Error.md` | `e0160ea07fdbc74f2cafebd6ed3b21e60029662d28d67f5f6a0b4d95ba72be9b` |
| `07_table.md` | `4c9a0e037872333210aaf44ba9fbf00a0e63343a69d55250e537d2c3c5e2d356` |

## Request Usage Matrix

| Request item | Source/use | Query/response use | Rule/status |
|---|---|---|---|
| Authorization | Bearer JWT; require Mentor role | Principal for request-scope authorization | Role DIRECT; Mentor guard, claim shape and subject mapping `SOURCE_REQUIRED` |
| `request_id` | Required path int64 | Logical SupportRequest lookup key | Type DIRECT; pilot ticket primary key is UUID and incompatible |
| Body/query | None | N/A | DIRECT from catalog |
| `X-Trace-Id` | Optional header per API Guidelines | Propagate trace in envelope/header when wired | Shared convention; endpoint absent |

## Query Matrix

| Query | Type | Candidate source/fields | Predicate/order | Status |
|---|---|---|---|---|
| Q1 — request detail | Logical SELECT | No approved physical SupportRequest table. Pilot `support_tickets` has UUID `id`, `learner_id`, `status`, `assigned_to_subject_id`, `created_at`, `resolved_at`; it has no `course_id`. | Intended lookup by `request_id` within Mentor scope; no physical predicate can be approved while ID and identity mappings are unresolved. | `SOURCE_REQUIRED`; no production SQL |
| Q2 — conversation/messages | Logical SELECT | No approved physical SupportMessage relation. Pilot `support_messages` has UUID `id`/`ticket_id`/`author_subject_id`, `body`, `attachment_file_ids`, `is_internal`, `sent_at`. | Intended messages for the selected request; ordering, visibility and limit are unspecified. | `SOURCE_REQUIRED`; pilot candidate only |
| Q3 — student, author and attachment projections | Logical reads/resolvers | No approved numeric UserSummary projection or UploadAsset URL/status resolver. Pilot profiles/files use UUID refs and storage keys. | Map required nested fields only after approved identity and asset services/schema exist. | `SOURCE_REQUIRED`; do not synthesize fields |

No count, pagination, sort, limit, SQL cast, UUID-to-int64 conversion or direct table mapping is selected.

## Mutation Matrix

| Operation | Target | Condition | Fields | Status |
|---|---|---|---|---|
| None | N/A | API #59 is read-only | No INSERT/UPDATE/DELETE | `N/A — READ-ONLY API`; #60/#61 own subsequent actions |

## Response Source Matrix

| Response field | Contract type | Candidate source | Mapping/status |
|---|---|---|---|
| `success` | boolean | Envelope branch | Shared envelope convention |
| `businessCode` | string | Catalog | Exact literal `DESIGN_RESOURCE_RETRIEVED` on success |
| `message` | string | Application | Safe localized text; exact wording unspecified (`DERIVED`) |
| `data.id` | int64 | No approved source; pilot ticket ID is UUID | `SOURCE_REQUIRED` |
| `data.course_id` | int64 | No approved support/course relation | `SOURCE_REQUIRED` |
| `data.student` | UserSummary | No approved projection; pilot profile ID is UUID and name nullable | `SOURCE_REQUIRED` |
| `data.student.id` | int64 | No numeric identity mapping | `SOURCE_REQUIRED` |
| `data.student.full_name` | string | No approved non-null projection | `SOURCE_REQUIRED` |
| `data.student.avatar_url` | uri? | No approved file/avatar URL resolver | `SOURCE_REQUIRED`; null/omit rule unconfirmed |
| `data.status` | SupportStatus | Pilot status varchar is a candidate only | Enum members and mapping `SOURCE_REQUIRED` |
| `data.messages[]` | SupportMessage[] | No approved message-source mapping | Required collection; complete thread visibility/limit/order unspecified |
| `data.messages[].id` | int64 | Pilot message ID is UUID | `SOURCE_REQUIRED` |
| `data.messages[].author` | UserSummary | No approved learner/staff identity projection | `SOURCE_REQUIRED` |
| `data.messages[].author.id` | int64 | Pilot author subject ID is UUID | `SOURCE_REQUIRED` |
| `data.messages[].author.full_name` | string | No approved non-null identity projection | `SOURCE_REQUIRED` |
| `data.messages[].author.avatar_url` | uri? | No approved profile/file resolver | `SOURCE_REQUIRED`; null/omit rule unconfirmed |
| `data.messages[].content` | string | Pilot `support_messages.body` is a candidate | Candidate alias only; model not approved |
| `data.messages[].attachments[]` | UploadAsset[] | Pilot file refs are UUIDs; no approved URL/status resolver | Required field; projection `SOURCE_REQUIRED` |
| `data.messages[].attachments[].id` | int64 | Pilot file object ID is UUID | `SOURCE_REQUIRED` |
| `data.messages[].attachments[].name` | string | Pilot `original_name` candidate | Candidate only; model not approved |
| `data.messages[].attachments[].url` | uri | No approved URL/signer source | `SOURCE_REQUIRED`; do not expose storage key |
| `data.messages[].attachments[].content_type` | string | Pilot MIME columns are candidate only | Field selection `SOURCE_REQUIRED` |
| `data.messages[].attachments[].size_bytes` | int64 | Pilot size column candidate | Candidate only; model not approved |
| `data.messages[].attachments[].status` | UploadStatus | No approved scan-status mapping | Enum/mapping `SOURCE_REQUIRED` |
| `data.messages[].created_at` | date-time | Pilot `sent_at` candidate | Candidate alias only |
| `data.created_at` | date-time | Pilot ticket `created_at` candidate | Candidate only |
| `data.resolved_at` | date-time? | Pilot ticket `resolved_at` candidate | Candidate only; null-versus-omit rule unconfirmed |
| `meta` | object | Envelope convention | No pagination contract; empty-object candidate |
| `traceId` | uuid | Request trace | Propagate/generate per API Guidelines when wired |

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Runtime/API route | No API #59 route/module/test; path absent from `DESIGN_CONTRACT_PATHS` | `UNWIRED / NOT_FOUND` | DD is design-only; future wiring must add compatible error dispatch. |
| Data model and ID | Legacy model lacks support tables; pilot uses UUID where contract requires int64 | `DISCREPANCY / SOURCE_REQUIRED` | No physical query or field mapping can be finalized. |
| Mentor access | AC-24 requires an in-scope request; guard and principal-to-assignment mapping absent | `SOURCE_REQUIRED` | Authorization predicate and 403/404 privacy ordering unresolved. |
| Thread projection | Contract requires message authors and attachments; identity and URL/status resolvers absent | `SOURCE_REQUIRED` | Full success projection is blocked. |
| Message policy | Contract has `messages[]`; no order, bound, internal-message visibility or empty rule | `SOURCE_REQUIRED` | Do not select pilot `is_internal` visibility or chronological ordering by assumption. |
| Envelope error data | API Guidelines expect null; current helper defaults omitted error data to `{}` | `DISCREPANCY / CONDITIONAL_FUTURE_WIRING` | Revisit during route wiring; not current API #59 behavior. |

## Authoring and verification plan

1. Create the eight registered Markdown sheets with status `Draft — Needs Confirmation`, using their exact template appendix tails.
2. Preserve all direct contract values and exact error set. Use examples only as schema illustrations, not as proof of enum or persistence values.
3. Keep query and response matrices source-aware; no SQL or physical mapping where the selected schema does not satisfy the contract.
4. Add `OPEN_QUESTIONS.md` for schema/ID, Mentor scope, nested identities/assets, message visibility/order/bounds, and malformed path behavior.
5. Add `VERIFICATION_REPORT.md` with static-only status, exact 11-file manifest, links/anchors, JSON and table/fence/whitespace checks; runtime tests remain `NOT_RUN`.
6. Keep AC-24 #58–#61 macro-review pending until #60 and #61 DDs exist; do not mark implementation-ready.
