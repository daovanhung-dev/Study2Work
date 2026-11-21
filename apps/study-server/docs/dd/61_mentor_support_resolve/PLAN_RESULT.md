# PLAN_RESULT — Study API #61

## Trạng thái plan

- Plan và source trace được ghi trong worklog trước runtime implementation.
- API: #61 — Đóng yêu cầu hỗ trợ Mentor.
- Output: `61_mentor_support_resolve/` — tám template sheets và ba reports Markdown; không tạo ZIP theo Study workflow.
- DD status: `Draft — Needs Confirmation`; implementation local đã hoàn thành, nhưng schema/lifecycle choices vẫn DERIVED và chưa có live DB evidence.
- Loại: PATCH; logical UPDATE SupportRequest status và `resolved_at`; không ghi message/attachment.

## Source inventory và contract

| Source | Bằng chứng dùng | Trạng thái |
|---|---|---|
| `docs/lists/list_api.md` row #61 | Method/path, Mentor Bearer, int64 path, no body/query, singleton response, success/error set | DIRECT |
| AC-24 index/diagram | #60 reply → decision; YES #61 sets RESOLVED; NO keeps OPEN | DIRECT |
| `infra/postgres/study-server/migrations/008_support_requests.sql` and `DB.sql` | BIGINT request/course/student keys, local status set and `resolved_at` | Checked-in local source; live DB not verified |
| API #58–#60 current source | Numeric Mentor `sub`, direct `courses.mentor_id`, support projection, request locks and transaction ownership | Current local pattern |
| V1-PILOT `infra/postgres/02_study_db.sql` | UUID `support_tickets` model | Conflicts with local BIGINT/catalog; not used |
| Current router/middleware | #58–#60 composed; #61 absent before this task | Pre-edit source state |
| Current DB/response helpers | `query_one/query_many` do not commit; `error_response` uses `data:null`; trace helpers | Current source |
| `createDD-markdown` and template set | Registry wires skill to `server-study`; original appendices preserved | SOURCE_BACKED; Study workflow overrides ZIP packaging |

## API Requirement Matrix

| API ID | Method/path | Actor/auth | Input | Success/response | Errors | Status |
|---|---|---|---|---|---|---|
| #61 | `PATCH /api/v1/mentor/support/{request_id}/resolve` | Bearer JWT; Mentor | `request_id:int64!`; no body/query | HTTP 200 `DESIGN_RESOURCE_UPDATED`; `ApiEnvelope<SupportRequest>` | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 422 `DESIGN_VALIDATION_ERROR`; 500 `DESIGN_INTERNAL_ERROR` | Catalog DIRECT |

## AC-24 behavior and API boundary

```text
#58 list → #59 read request/thread → #60 INSERT SupportMessage
→ “Vấn đề đã được xử lý?”
   ├─ YES → #61 UPDATE request status = RESOLVED
   └─ NO  → không gọi #61; giữ OPEN
→ trả SupportRequest với status/thread hiện tại
```

- #61 chỉ thay đổi `support_requests.status` và `resolved_at`; không ghi thêm message hoặc attachment.
- #60 vẫn giữ status; #61 chỉ chạy khi Mentor xác nhận đã xử lý.
- #61 reuses #58 response model and #59 thread query/projection.
- #58 catalog giữ singleton `ApiEnvelope<SupportRequest>` dù route mang nghĩa danh sách; discrepancy vẫn còn và #61 không sửa #58 contract.

## Local fallback decisions

| Concern | Decision | Basis/status |
|---|---|---|
| Request physical ID | BIGINT `support_requests.id`; course via `support_requests.course_id` | DERIVED from migration 008 and current #58–#60; user authorized reasonable fallback |
| Mentor identity/scope | Numeric JWT `sub` equals direct `courses.mentor_id` | DERIVED from current #58–#60 shared guard and ownership pattern |
| Allowed transitions | OPEN, IN_PROGRESS, WAITING_LEARNER → RESOLVED; RESOLVED no-op success; CANCELLED/unknown → 422 | DERIVED from local migration status set and AC-24 intent |
| Timestamp | DB `CURRENT_TIMESTAMP` on first successful transition; do not replace on retry | DERIVED from local nullable column and update semantics |
| Missing/other owner | Missing → 404; existing other owner → 403 | Catalog plus #59/#60 convention |
| Transaction | Lock row, update under repeated owner predicate, hydrate full thread, validate envelope, commit once | Current DB helper and #59/#60 pattern |

## Query and mutation trace

```text
PATCH route
→ validate_current_user_request(role="MENTOR")
→ parse signed-int64 path (malformed/overflow: 422)
→ SELECT support_requests/course/users FOR UPDATE
→ classify 404 / 403 / state
→ UPDATE active state with course-owner predicate and RETURNING status/resolved_at
→ query chronological API #59 thread + scoped UploadAssets
→ shared SupportRequest projection + envelope validation
→ commit once; errors rollback
```

The path, owner and SQL use parameterized inputs. SQL constants remain in `query.py`; transaction and orchestration stay in `view.py`.

## State handling

- Active `OPEN`, `IN_PROGRESS`, `WAITING_LEARNER`: set `status='RESOLVED'`, `resolved_at=COALESCE(resolved_at, CURRENT_TIMESTAMP)`.
- `RESOLVED`: skip UPDATE and return current resource; a nullable timestamp on a pre-existing resolved row is preserved.
- `CANCELLED` or an unsupported state: return `422 DESIGN_VALIDATION_ERROR`, without mutation.
- State matrix and retry semantics are implementation choices, not direct AC-24 contract.

## Response/error mapping

- Reuse `SupportRequestResponse`, `map_support_request`, and `append_support_messages` used by #59/#60.
- Return full request/thread at `200 DESIGN_RESOURCE_UPDATED`; message order `created_at ASC, id ASC`; linked uploads use existing role/purpose/owner/course/status constraints.
- Error codes remain exactly 401/403/404/422/500. `error_response` serializes `data:null`; field/path errors use `meta.fieldErrors`.
- No `409`, `503`, resolution reason, message mutation, or pagination was introduced.

## Template fingerprints

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

## Macro-review AC-24 #58–#61

### Kết luận

`LOCAL_IMPLEMENTATION_COMPLETE_WITH_DERIVED_CONTRACT_CHOICES`: the chain now has source-backed routes and HTTP tests for #58–#61 in the local worktree. Shared business/schema choices remain DERIVED; fake-DB verification does not establish live schema, migration deployment or production behavior.

| API | Vai trò theo catalog/AC-24 | Kết quả review |
|---|---|---|
| #58 | Đọc support requests theo query filters | GET list source exists; preserve catalog's singleton response declaration as a visible cardinality discrepancy. |
| #59 | Đọc một request và conversation | GET detail returns the shared full thread; direct course owner and projection are DERIVED local choices. |
| #60 | Gửi reply | POST inserts message and ordered links; it preserves request status and returns the full thread. |
| #61 | Resolve sau nhánh YES | PATCH changes only status/timestamp; active state set, retry semantics and timestamp are DERIVED; NO branch stays OPEN. |

### Shared open questions

1. #58 plural/list flow conflicts with catalog's singleton `ApiEnvelope<SupportRequest>`.
2. Migration 008 and direct course-owner scope are local fallback choices; live schema and deployment need independent verification.
3. Product approval remains open for identity/scope and #61 transition/timestamp behavior.
4. Message visibility, reply-after-resolve/cancel policy and concurrency behavior in live PostgreSQL remain unverified.
5. V1-PILOT UUID support tickets remain incompatible and are not used by the current local fallback.

### Review status

- AC-24 sequence and mutation ownership: `VERIFIED_STATIC_AND_LOCAL_HTTP_TESTS`.
- Routes #58–#61: composed and local HTTP tests pass.
- Local persistence/projection behavior: `SOURCE_BACKED_WITH_DERIVED_CHOICES`.
- Live schema/deployment: `NOT_VERIFIED`.
- DD package: eight sheets and three reports; every sheet remains `Draft — Needs Confirmation`.

## Deliverable manifest

| Nhóm | Kết quả |
|---|---|
| Sheets | `00_Cover.md` through `07_table.md`, all present |
| Reports | `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md` |
| Tổng | 11 Markdown files; no ZIP per Study workflow |
