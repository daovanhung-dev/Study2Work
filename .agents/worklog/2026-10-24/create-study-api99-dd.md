---
task_id: "2026-10-24-create-study-api99-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Kiểm kê và tạo DD Study API #99

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Giữ catalog là nguồn contract; phân biệt `DIRECT`, `DERIVED`, `SOURCE_REQUIRED`; không invent schema, enum, hoặc identity mapping.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: Tách expected khỏi current; chỉ gọi API đã lập trình khi có route và matching `view.py`; source presence không chứng minh runtime pass.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: DD Study gồm 8 sheet và 3 report, Markdown-only; ghi AC source và các candidate không được duyệt thành open questions.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Báo số API có/chưa có DD, số API có/chưa có source implementation; sau khi kiểm kê, tiếp tục DD #99 trong chuỗi một API mỗi phiên.
- Canonical contract/approved DD: `docs/lists/list_api.md` row #99; AC-37 index và `AC_04_ADMIN_MANAGEMENT.drawio`; reusable `ApiEnvelope<T>`, `Page<T>`, `PageMeta`, `Discussion`, `DiscussionComment`, `UserSummary`; workflow `server-study/workflows/README.md`; skill `createDD-markdown` đã được registry wire.
- API #99 direct contract: `PATCH /api/v1/admin/discussions/{discussion_id}/moderate`; Bearer JWT, role Admin; path `discussion_id:int64!`; body `{action:string!, reason:string!}`; response `ApiEnvelope<Page<Discussion>>`; success 200 `DESIGN_RESOURCE_UPDATED`; đúng errors 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 422 `DESIGN_VALIDATION_ERROR`, 500 `DESIGN_INTERNAL_ERROR`.

## CURRENT_BEHAVIOR

- Source/config: Catalog có 103 API ID liên tục #01–#103. Có 98 DD folder #01–#98; cả 98 có 8 sheet lõi, 86 có đủ 3 report chuẩn, 12 folder #01–#12 thiếu các report. API #99–#103 chưa có DD folder trước task này. Router `app/api/v1.py` cùng module `view.py` chỉ có cặp cho #01–#09 và #12–#14 (12 API); #99 không có route/module/test.
- Runtime/auth: `validate_current_user_request` hiện yêu cầu role Student; chưa có Admin guard/policy source. Middleware `DESIGN_CONTRACT_PATHS` chưa chứa route #99; business-code fallback khác catalog nếu route tương lai được nối mà allowlist không cập nhật.
- Schema: Legacy `discussions` dùng BIGINT và có `id, course_id, user_id, parent_id, content, status, created_at, updated_at`; không có title, report relation hoặc moderation/audit table. `status` là `VARCHAR(20)` default `ACTIVE`, nhưng token và transitions moderation chưa được duyệt. Pilot `admin_adjustments`/`audit_events` dùng UUID/versioned subject fields; không có bằng chứng tương thích với legacy Discussion ID.
- Runnable tests: Không có test #99; task docs-only, không chạy application tests.
- Runtime wiring: API #99 `UNWIRED / NOT_FOUND`; chưa có hành vi runtime để khẳng định.

## SOURCE_TRACE

```text
Admin Bearer principal -> PATCH moderation theo discussion_id -> validate action/reason và quyền -> cập nhật logical moderation state + audit theo AC-37 -> trả Page<Discussion> -> quyết định xóa riêng qua API #100 hoặc kết thúc
```

## PLAN BEFORE DD AUTHORING

1. Giữ nguyên method/path, Admin Bearer contract, `discussion_id:int64!`, body `action:string!` và `reason:string!`, không có query, response `ApiEnvelope<Page<Discussion>>`, HTTP 200 và đúng bộ lỗi 401/403/404/422/500.
2. Đọc đầy đủ nhánh AC-37: #97 queue → #98 detail → quyết định vi phạm → #99 `UPDATE moderation state + audit` → quyết định xóa; nếu cần xóa thì chuyển riêng sang #100. #99 không được thực hiện DELETE.
3. Phân biệt `reason` trong body #99 (lý do hành động moderation) với query filter `reason` của #97 (lý do report). Không chuyển report payload/detail của #98 vào response #99.
4. Ghi các action “ẩn/khóa/cảnh báo” theo sơ đồ là ý nghĩa nghiệp vụ mức logical. Token đề xuất `hide|lock|warn` chỉ là `DERIVED`; casing, enum, transition, trạng thái cho từng action và hiệu ứng của `warn` cần xác nhận. Không tự ánh xạ vào `discussions.status`.
5. Ghi mutation logic UPDATE discussion state và append moderation audit theo AC-37; physical mapping là `SOURCE_REQUIRED`. Không bịa bảng/cột. Đánh giá pilot audit tables riêng, ghi rõ UUID subject/resource model không tương thích trực tiếp với legacy BIGINT; không coi chúng là mapping được duyệt.
6. Dùng legacy `discussions` chỉ làm candidate cho row target và Discussion response; không thêm `title` hoặc report relation, không tự giả định row lock/idempotency/transaction boundaries. Giữ nullability của `course_id/user_id`, enum status và timestamps như gap.
7. Giữ response catalog `Page<Discussion>`; one-item Page (`page=1`, `size=1`, `total=1`, `total_pages=1`) là proposal `DERIVED` tham chiếu precedent #42/#98, cần xác nhận. Liệt kê đủ fields `Discussion`, `UserSummary`, `DiscussionComment`, `PageMeta`; không đổi sang `ActionResult`.
8. Candidate action-response semantics có thể trả Discussion đã cập nhật, nhưng trường hợp `warn` không đổi state và cách hình thành `PageMeta` cần hỏi; không bịa dữ liệu response.
9. Viết 8 sheet theo 8 template đã đăng ký và 3 report; append đúng template suffix từng sheet. Tạo `99_admin_discussions_moderate`; không ZIP, runtime, test, schema, catalog hoặc diagram edit.
10. Static-verify manifest 11 file, exact catalog contract/errors, field matrices, JSON, links/anchors, tables, code fences, whitespace, template appendix, và `git diff --check`. Cập nhật inventory worklog sau DD; giữ AC-37 macro-review #97–#100 pending đến khi #100 tồn tại.

### API Requirement Matrix

| API ID | Contract item | Giá trị | Basis/status |
|---|---|---|---|
| #99 | Method/path | `PATCH /api/v1/admin/discussions/{discussion_id}/moderate` | Catalog; DIRECT |
| #99 | Actor/auth | Admin; Bearer JWT | Catalog; DIRECT, Admin guard chưa có source |
| #99 | Path | `discussion_id:int64!` | Catalog; DIRECT |
| #99 | Body | `action:string!`, `reason:string!` | Catalog; DIRECT |
| #99 | Query | Không khai báo | Catalog; DIRECT |
| #99 | Success | HTTP 200 `DESIGN_RESOURCE_UPDATED`; `ApiEnvelope<Page<Discussion>>` | Catalog; DIRECT |
| #99 | Error | 401 `DESIGN_AUTHENTICATION_REQUIRED` | Catalog; DIRECT |
| #99 | Error | 403 `DESIGN_ACCESS_DENIED` | Catalog; DIRECT |
| #99 | Error | 404 `DESIGN_RESOURCE_NOT_FOUND` | Catalog; DIRECT |
| #99 | Error | 422 `DESIGN_VALIDATION_ERROR` | Catalog; DIRECT; exact validation rules unspecified |
| #99 | Error | 500 `DESIGN_INTERNAL_ERROR` | Catalog; DIRECT |
| #99 | Logical mutation | Update moderation state + audit; optional delete is separate #100 | AC-37 diagram; DIRECT flow, persistence `SOURCE_REQUIRED` |

### Request Usage Matrix

| Request item | Source/use | Query/response use | Rule/status |
|---|---|---|---|
| `Authorization` | Bearer JWT | Authenticate Admin principal | DIRECT contract; Admin claims/guard/policy `SOURCE_REQUIRED` |
| `discussion_id` | Required int64 path | Locate target discussion | Type DIRECT; malformed/overflow behavior not separately specified |
| `action` | Required string body | Select moderation action | DIRECT field; allowed tokens/case/transitions `SOURCE_REQUIRED`; hide/lock/warn are logical meanings in AC-37 |
| `reason` | Required string body | Explain and audit this moderation action | DIRECT field; constraints/taxonomy/limits `SOURCE_REQUIRED`; distinct from #97 report filter |
| Body content type | Not explicitly stated in row | JSON example only if body encoding convention is supported | Do not add extra validation contract |
| Query parameters | None declared | None | DIRECT from catalog |

### Query and Mutation Matrix

| Step | Operation | Target/source | Candidate columns/effect | Evidence status |
|---|---|---|---|---|
| Q1 | SELECT/target existence | Legacy `discussions` | Candidate `id = :discussion_id` | Legacy DDL only; live schema unknown |
| M1 | UPDATE | Logical discussion moderation state | Action-dependent state change | AC-37 logical requirement DIRECT; physical table/column/value/transition `SOURCE_REQUIRED` |
| M2 | INSERT/append audit | Logical moderation audit | Actor identity | AC-37 audit intent; persistence mapping `SOURCE_REQUIRED` |
| M2 | INSERT/append audit | Logical moderation audit | Action | AC-37 audit intent; persistence mapping `SOURCE_REQUIRED` |
| M2 | INSERT/append audit | Logical moderation audit | Reason | AC-37 audit intent; persistence mapping `SOURCE_REQUIRED` |
| M2 | INSERT/append audit | Logical moderation audit | Before state | Snapshot shape and persistence `SOURCE_REQUIRED` |
| M2 | INSERT/append audit | Logical moderation audit | After state | Snapshot shape and persistence `SOURCE_REQUIRED` |
| M2 | INSERT/append audit | Logical moderation audit | Trace identifier | Persistence mapping `SOURCE_REQUIRED` |
| M3 | DELETE | None | No delete in #99; route to #100 only if Admin chooses deletion | DIRECT AC-37 separation |
| Q2 | SELECT response row | Updated Discussion | Candidate legacy discussion plus user/comment projection | Projection and updated-state behavior unresolved; do not invent joins/response values |

### Response Source Matrix (required fields to trace in DD)

| Response field | Contract type | Candidate source/transform | Evidence status |
|---|---|---|---|
| `success` | boolean | Envelope | DIRECT convention |
| `businessCode` | string | Catalog literal | DIRECT: `DESIGN_RESOURCE_UPDATED` |
| `message` | string | Application message | Exact text unspecified |
| `data.items` | `Discussion[]` | Updated target candidate | DIRECT shape; membership/cardinality unresolved |
| `data.pagination.page` | int32 | No request page | One-item proposal only, DERIVED |
| `data.pagination.size` | int32 | No request page size | One-item proposal only, DERIVED |
| `data.pagination.total` | int64 | Mutation result count | Value and semantics unresolved |
| `data.pagination.total_pages` | int32 | Mutation result count | Value and semantics unresolved |
| `data.items[].id` | int64 | `discussions.id` candidate | Legacy candidate; live mapping unverified |
| `data.items[].course_id` | int64 | `discussions.course_id` candidate | Nullable in legacy DDL; required in schema |
| `data.items[].title` | string | No legacy column | `SOURCE_REQUIRED`; do not derive from content |
| `data.items[].content` | string | `discussions.content` candidate | Legacy candidate |
| `data.items[].author` | `UserSummary` | Candidate user relation | User ID nullable in legacy DDL |
| `data.items[].author.id` | int64 | Candidate `users.id` | Legacy candidate |
| `data.items[].author.full_name` | string | Candidate `users.full_name` | Legacy candidate |
| `data.items[].author.avatar_url` | uri? | Candidate `users.avatar_url` | Optional; null serialization unresolved |
| `data.items[].status` | `DiscussionStatus` | Candidate `discussions.status` | Tokens/transitions unresolved |
| `data.items[].comments` | `DiscussionComment[]` | Candidate child discussions | Admin visibility, nesting and membership unresolved |
| `data.items[].comments[].id` | int64 | Candidate child `discussions.id` | Legacy candidate |
| `data.items[].comments[].discussion_id` | int64 | Candidate child `parent_id` | Legacy candidate; FK nullable |
| `data.items[].comments[].content` | string | Candidate child `content` | Legacy candidate |
| `data.items[].comments[].author` | `UserSummary` | Candidate child author | Nullable user FK gap |
| `data.items[].comments[].author.id` | int64 | Candidate `users.id` | Legacy candidate |
| `data.items[].comments[].author.full_name` | string | Candidate `users.full_name` | Legacy candidate |
| `data.items[].comments[].author.avatar_url` | uri? | Candidate `users.avatar_url` | Optional; null serialization unresolved |
| `data.items[].comments[].created_at` | date-time | Candidate child `created_at` | Legacy timestamp lacks timezone in DDL |
| `meta` | object | Envelope | Endpoint-specific metadata not defined |
| `traceId` | uuid | Request trace | Envelope convention |

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| #99 runtime | No route/module/test in current Study source | `UNWIRED / NOT_FOUND` | Design-only DD; no runtime claim |
| Action enum/state transitions | Catalog says string; AC-37 names hide/lock/warn but gives no tokens or transitions | `SOURCE_REQUIRED / DERIVED` | No physical status update can be finalized |
| Audit persistence | AC-37 requires audit; legacy DDL has no audit relation; pilot audit uses UUID/versioned IDs | `SOURCE_REQUIRED / DISCREPANCY` | Do not map pilot tables to legacy Discussion IDs |
| Discussion schema | Legacy has BIGINT status row but no title; course/user IDs nullable | `DISCREPANCY` | Cannot fully construct required Discussion payload from legacy DDL alone |
| Admin authorization | Catalog requires Admin; current shared helper enforces Student | `SOURCE_REQUIRED` | Role/claim policy unresolved |
| Response page | Catalog requires Page<Discussion>, request has no pagination | `DERIVED / SOURCE_REQUIRED` | One-item metadata proposal needs approval |
| Delete branch | Diagram routes deletion to #100 after #99 moderation | `DIRECT` | #99 must not delete |

## CHANGES

- Files changed: API #99 DD folder (8 sheets + 3 reports), this worklog, and `.agents/worklog/2026-10-24/inventory-study-api-dd-counts.md`.
- CONTEXT_UPDATES: None planned.
- Context pages changed: None planned; no runtime/schema/catalog/diagram change.
- Assumptions: Keep action token examples and one-item Page labeled DERIVED; retain all unresolved DB/auth/response semantics as open questions.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog selector/review | Deno selector selected #48/#49/#50; all three read in full. | `VERIFIED` |
| Catalog inventory | 103 unique contiguous endpoint IDs (#01–#103). | `VERIFIED_STATIC_ONLY` |
| DD inventory (pre-authoring snapshot) | 98 numbered folders; 98 have 8 core sheets; 86 have 3 reports; #99–#103 absent. | `VERIFIED_STATIC_ONLY` |
| Source inventory | #01–#09 and #12–#14 have router marker plus matching view.py (12); #99 absent. | `VERIFIED_STATIC_ONLY` |
| AC-37 diagram | Parsed page; #99 update moderation state + audit, then decision to use separate API #100 or finish. | `VERIFIED_STATIC_ONLY` |
| Schema/auth review | Legacy Discussion DDL, DB guide, pilot admin audit tables and current Student-only auth helper inspected. | `VERIFIED_STATIC_ONLY` |
| DD manifest/front matter | Exactly 11 Markdown files (8 sheets + 3 reports); front matter present on all 8 sheets. | `VERIFIED` |
| Template appendices | All 8 sheet appendix suffixes equal the registered templates exactly. | `VERIFIED` |
| Contract/response coverage | Method/path, actor, request, response and exact error set matched; 32 envelope/Page/Discussion/UserSummary/DiscussionComment response fields are listed individually. | `VERIFIED_STATIC_ONLY` |
| JSON/local Markdown checks | Both JSON blocks parse; local links resolve; tables, fences, final newline and whitespace pass. | `VERIFIED` |
| `git diff --check` | No diagnostics. | `PASS` |
| Post-DD inventory | 99 DD folders, all with 8 core sheets; 87 include all three reports; 4 folders remain (#100–#103). 12 route+view pairs; 91 without. | `VERIFIED_STATIC_ONLY` |
| Runtime tests | Not run; docs-only. | `NOT_RUN` |

## HANDOFF

- Remaining blockers: Confirm action tokens/transitions, Admin claims/guard, audit persistence, Discussion response projection, and Page metadata.
- Next owner/action: Continue with API #101. AC-37 macro-review #97–#100 completed; unresolved action/state/audit/projection questions remain open.

## POST-API #100 AC-37 MACRO REVIEW

- Completed after #100 DD was authored; the sequence keeps moderation (#99) separate from soft delete (#100).
- Logical audit intent is consistent across #99/#100, but persistence/actor mapping remains `SOURCE_REQUIRED`; the legacy Discussion ID and pilot UUID audit design are not reconciled.
- See [API #100 plan result](../../../apps/study-server/docs/dd/100_admin_discussions_delete/PLAN_RESULT.md). No runtime, catalog, schema or diagram changes were made.
