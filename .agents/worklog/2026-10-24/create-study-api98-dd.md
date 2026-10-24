---
task_id: "2026-10-24-create-study-api98-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #98 — discussion detail

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Giữ contract catalog; source/schema là candidate cần ghi rõ; route/view source không đồng nghĩa runtime verified.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: Tách sơ đồ logical khỏi physical query; giữ response/schema mismatch và `SOURCE_REQUIRED` công khai.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: Gắn nhãn đề xuất `DERIVED`; không đoán relation, enum, Admin guard hay business code.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tạo DD Markdown tiếng Việt cho API #98, lập plan trong worklog trước khi tạo folder, đọc AC-37 diagram và DD liên quan, kiểm tra tĩnh ngay sau authoring. Giữ macro-review AC-37 #97–#100 pending đến khi #100 tồn tại.
- Canonical contract/approved DD: `docs/lists/list_api.md` row #98; reusable `PageMeta`, `Page<Discussion>`, `Discussion`, `DiscussionComment`, `UserSummary`; AC-37 index/page trong `AC_04_ADMIN_MANAGEMENT.drawio`; DD #97 reported queue và DD #42 thread detail; `createDD-markdown` registry wire cho `server-study`; workflow Study Markdown-only.

### API requirement matrix

| Item | Contract | Basis/status |
|---|---|---|
| Method/path | `GET /api/v1/admin/discussions/{discussion_id}` | Catalog + AC-37; DIRECT |
| Actor/auth | Bearer JWT; role Admin | Catalog + diagram; DIRECT role, Admin guard/claims absent in Study source |
| Path | `discussion_id:int64!` | Catalog; DIRECT |
| Body/query | None declared | Catalog; DIRECT |
| Success | HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<Page<Discussion>>` | Catalog + diagram; DIRECT |
| Errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 500 `DESIGN_INTERNAL_ERROR` | Exact catalog set; no 422 |
| AC-37 flow | Queue #97 → open thread/report detail → read discussion/comments/reports → policy decision → #99/#100 if required | Diagram nodes/edges; report persistence/projection unresolved |

## CURRENT_BEHAVIOR

- Source/config: No #98 route/module/test exists. Current router IDs are #01–#09 and #12–#14; shared guard only authorizes Student. `DESIGN_CONTRACT_PATHS` omits #98; if a route is added without integration, generic validation/internal handlers use fallback codes. `error_response` serializes absent `data` as `{}`, while API guidelines specify `null`.
- DB/schema: Legacy `discussions` table has `id`, `course_id`, `user_id`, `parent_id`, `content`, `status`, `created_at`, `updated_at`; FKs can be NULL; there is no `title` or discussion report relation. DB guide lists #97–#100 as design-only; live schema is unverified. Reusable `Discussion` requires `title`, `course_id`, `author`, `status`, `comments`; `PageMeta` requires page/size/total/total_pages.
- Runnable tests: No focused API #98 tests; application tests not run for docs-only task.
- Runtime wiring: `UNWIRED / NOT_FOUND`; no Admin guard or report query source.

## SOURCE_TRACE

```text
Admin selects a #97 queue item -> GET #98 with discussion_id -> authenticate/authorize Admin -> logical read discussion + comments + reports -> candidate one-thread Page<Discussion> -> 200 DESIGN_RESOURCE_RETRIEVED or exact 401/403/404/500 catalog errors -> UI decides dismiss, #99 moderate, or #100 delete
```

## PLAN BEFORE DD AUTHORING

1. Preserve exact catalog method/path, Bearer JWT/Admin, required int64 path, no body/query, `ApiEnvelope<Page<Discussion>>`, HTTP 200 and error codes 401/403/404/500. Do not add 422 or report fields to the response.
2. Follow AC-37 order: #97 queue → #98 detail → read discussion/comments/reports → violation decision → #99/#100 only on their respective branches. Do not perform mutation in this GET.
3. Use one-item `Page<Discussion>` (`page=1,size=1,total=1,total_pages=1`) as an explicitly `DERIVED` proposal based on API #42's single-thread Page pattern. It is a design proposal, not a catalog pagination rule.
4. Propose `discussion_id` as the root thread ID and `comments[]` as direct child discussions ordered `created_at ASC, id ASC`, following #42. Mark root-versus-reply target, recursive/nested replies, and visibility as `DERIVED`/open because AC-37 does not specify them and #97 may select reported replies.
5. Represent AC-37's logical report read in Query Matrix, but do not invent a table/query: legacy DDL has no report relation. `Page<Discussion>` has no reason/severity/report fields, and generic analytics `Report` is a different schema; record the response/diagram discrepancy and decision required.
6. Candidate Discussion mapping may reference only legacy `discussions` and `users` columns as design artifacts. Keep missing `title`, nullable course/user keys, status enum and timestamp timezone gaps explicit; do not derive title from content.
7. Create eight template-backed sheets plus `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md` in `apps/study-server/docs/dd/98_admin_discussions_detail/`; no ZIP, runtime/schema/catalog/diagram edits, or edits to #97.
8. Static-verify exact 11-file manifest, template suffix parity, exact request/response/error contract, every nested field, JSON, links/anchors, tables/fences/whitespace and `git diff --check`. No app tests for docs-only task.
9. Refresh count worklog after #98: expected 98 DD folders / 5 missing, 86 full 11-file packages / 12 legacy core-only, 12 source-programmed / 91 without route+view. Keep AC-37 macro-review for after #100.

### Request usage matrix

| Request item | Source/use | Response/query use | Status |
|---|---|---|---|
| Authorization | Bearer header | Authenticate and authorize Admin before data reads | Admin role DIRECT; Study guard/claim policy `SOURCE_REQUIRED` |
| `discussion_id` | Required path int64 | Candidate discussion lookup by ID | DIRECT type; root-vs-reply and malformed parse behavior unresolved |
| Body/query | None declared | None | DIRECT |

### Query/mutation matrix

| Query | Operation/source | Candidate fields/predicate | Status |
|---|---|---|---|
| Q1 | Logical discussion lookup | Target report's discussion ID; physical relation/key join to report absent | `SOURCE_REQUIRED` for report-to-discussion lookup |
| Q1a | Candidate legacy `discussions` | `id`, `course_id`, `user_id`, `parent_id`, `content`, `status`, timestamps | Candidate physical source only; no title; nullable FKs; no live proof |
| Q2 | Logical report detail read | Report ID, reason, severity, reporter, state, timestamps not defined | AC-37 logical requirement; no physical table/response fields approved |
| Q3 | Candidate direct-child comments | `discussions.parent_id = root.id`, child fields + users | `DERIVED` from #42; reply target, nesting, status/order need confirmation |
| Q4 | Candidate author projection | `users.id`, `full_name`, `avatar_url` | Candidate only; required join/null behavior unresolved |
| Q5 | Page metadata | One Discussion item candidate | `DERIVED` one-item page by #42; report/data cardinality does not map |
| Mutation | None | No INSERT/UPDATE/DELETE/audit write | `N/A — READ-ONLY API` |

### Response source matrix (contract inventory)

| Field | Type | Candidate/source status |
|---|---|---|
| `success` | boolean | Envelope success; DIRECT convention |
| `businessCode` | string | `DESIGN_RESOURCE_RETRIEVED`; DIRECT |
| `message` | string | Exact wording unspecified |
| `data` | `Page<Discussion>` | DIRECT shape; one-item page DERIVED |
| `data.items` | `Discussion[]` | DIRECT shape; candidate one item |
| `data.items[].id` | int64 | Candidate `discussions.id` |
| `data.items[].course_id` | int64 | Candidate `discussions.course_id`; DDL nullable vs required |
| `data.items[].title` | string | No legacy source; `SOURCE_REQUIRED` |
| `data.items[].content` | string | Candidate `discussions.content` |
| `data.items[].author` | `UserSummary` | Candidate `users` join; nullable FK mismatch |
| `data.items[].author.id` | int64 | Candidate `users.id` |
| `data.items[].author.full_name` | string | Candidate `users.full_name` |
| `data.items[].author.avatar_url` | uri? | Candidate `users.avatar_url`; omit if null |
| `data.items[].status` | `DiscussionStatus` | Candidate `discussions.status`; enum/visibility unresolved |
| `data.items[].comments` | `DiscussionComment[]` | Candidate direct children; scope unresolved |
| `comments[].id` | int64 | Candidate child `discussions.id` |
| `comments[].discussion_id` | int64 | Candidate child `parent_id` |
| `comments[].content` | string | Candidate child `discussions.content` |
| `comments[].author` | `UserSummary` | Candidate child `users` join |
| `comments[].author.id` | int64 | Candidate child `user_id` → `users.id` |
| `comments[].author.full_name` | string | Candidate `users.full_name` |
| `comments[].author.avatar_url` | uri? | Candidate `users.avatar_url`; omit if null |
| `comments[].created_at` | date-time | Candidate child `discussions.created_at`; timezone unresolved |
| `data.pagination.page` | int32 | `1` in one-item proposal; DERIVED |
| `data.pagination.size` | int32 | `1` in one-item proposal; DERIVED |
| `data.pagination.total` | int64 | `1` when target exists in one-item proposal; DERIVED |
| `data.pagination.total_pages` | int32 | `1` in one-item proposal; DERIVED |
| `meta` | object | Envelope; endpoint metadata unspecified |
| `traceId` | uuid | Shared request trace convention |
| Report detail fields | Not in `Discussion` | Cannot appear without approved catalog schema change |

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API runtime | No #98 route/module/test; Admin guard absent | `UNWIRED / NOT_FOUND` | DD is design-only |
| Report persistence/projection | AC-37 n5 reads reports; DDL has no discussion report table; response schema has no report fields | `DISCREPANCY / SOURCE_REQUIRED` | Cannot fulfill report detail as cataloged |
| Thread target | #42 proposes root + direct children; AC-37 does not state whether report can target a reply | `DERIVED / SOURCE_REQUIRED` | Root-only proposal may need change |
| Page semantics | Detail path returns Page<Discussion> without query pagination | `DERIVED` | One-item page proposal follows #42; confirmation needed |
| Discussion schema | Required title has no legacy column; course/user FKs nullable in DDL | `DISCREPANCY / SOURCE_REQUIRED` | Full response mapping not source-backed |
| Admin authorization | Catalog requires Admin; shared Study guard only Student | `SOURCE_REQUIRED` | Cannot implement authorization from current helper |
| Error integration | #98 path absent from middleware allowlist; helper error `data` is `{}` vs guideline `null` | `DISCREPANCY / CONDITIONAL_FUTURE_WIRING` | Future route must map exact catalog errors/envelope |

## CHANGES

- Files changed: `apps/study-server/docs/dd/98_admin_discussions_detail/` (8 sheets + 3 reports), this worklog, and `.agents/worklog/2026-10-24/inventory-study-api-dd-counts.md`.
- CONTEXT_UPDATES: None; no runtime/schema/catalog/diagram changed.
- Context pages changed: None planned.
- Assumptions: The one-item/root-plus-direct-comments shape is a labeled `DERIVED` proposal only; report data is not fabricated.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Context/worklog preflight | Router/global context, scope AGENTS/INDEX/workflow/tests and selected #48–#50 worklogs read. | `VERIFIED_STATIC_ONLY` |
| Contract/diagram/schema/source review | #98 catalog, AC-37 index/page/edges, #97/#42 precedents, Discussion ERD/guide/DDL, router/auth/middleware/responses reviewed. | `VERIFIED_STATIC_ONLY` |
| API #98 DD authoring | 11-file Markdown package created; status remains Draft — Needs Confirmation. | `VERIFIED` |
| Static integrity | Exact manifest, 8/8 template suffixes, request/response/error coverage (27 response field rows), JSON, links/anchors, tables, fences, whitespace and `git diff --check`. | `PASS` |
| Runtime tests | Documentation-only. | `NOT_RUN` |

## HANDOFF

- Remaining blockers: report relation and response fields, root/reply policy, Discussion title, Admin guard and future error integration.
- Next owner/action: Continue with API #99. Keep AC-37 group macro-review pending until #100.

## POST-API #100 AC-37 MACRO REVIEW

- Completed after #100 DD was authored.
- #98 remains the read-only detail step before #99/#100; report relation/response, root-versus-reply scope and visibility after soft delete remain unresolved.
- See [API #100 plan result](../../../apps/study-server/docs/dd/100_admin_discussions_delete/PLAN_RESULT.md); no runtime, catalog, schema or diagram changes were made.
