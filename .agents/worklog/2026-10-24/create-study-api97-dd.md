---
task_id: "2026-10-24-create-study-api97-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #97 — reported discussions

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Giữ contract catalog; phân biệt thiết kế với source/runtime; không invent schema hay Admin/Mentor identity.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: Dùng ma trận request/query/mutation/response; ghi `SOURCE_REQUIRED` và `DISCREPANCY`; Study chỉ giao Markdown.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: Tách requirement trực tiếp khỏi proposal `DERIVED`; không tạo physical Content/report table khi DDL chưa có bằng chứng.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tạo DD Markdown tiếng Việt cho API #97, lập plan trước folder DD, kiểm tra tĩnh ngay sau authoring. API #97 là API đầu AC-37; macro-review nhóm #97–#100 giữ pending đến sau khi #100 được tạo.
- Canonical contract/approved DD: `docs/lists/list_api.md` row #97; reusable `PageMeta`, `Page<Discussion>`, `Discussion`, `DiscussionComment`, `UserSummary`; AC-37 index và page diagram trong `AC_04_ADMIN_MANAGEMENT.drawio`; template `createDD-markdown` đã wire cho `server-study`; Study workflow yêu cầu Markdown, không ZIP.

### Requirement matrix

| Item | Contract | Basis/status |
|---|---|---|
| Method/path | `GET /api/v1/admin/discussions/reported` | Catalog + AC-37; DIRECT |
| Actor/auth | Bearer JWT, role Admin | Catalog + AC-37; DIRECT role, Admin guard/claim mapping chưa có source |
| Query | `reason?:string`, `severity?:string`, `page?:int32` | Catalog; DIRECT names/types, value semantics/defaults unresolved |
| Body | None declared | Catalog; DIRECT |
| Success | HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<Page<Discussion>>` | Catalog + diagram; DIRECT |
| Errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 500 `DESIGN_INTERNAL_ERROR` | Exact catalog set; do not add 404/422 |
| AC-37 flow | Open reported queue → read reports + discussion summary → select detail #98 | Diagram nodes/edges; report selection/grain unresolved |

## CURRENT_BEHAVIOR

- Source/config: No API #97 route/module/test found. Current router ID/view intersection is #01–#09 and #12–#14 (12 IDs). Shared Study auth validates the API#3 JWT shape and permits Student only; Admin guard/role claim policy is absent. Current middleware design allowlist omits #97 path; if future wiring relies on generic handlers without allowlist changes, validation/internal fallback codes differ from catalog. Current error helper serializes absent error data as `{}`.
- DB/schema: legacy `discussions` candidate has `id`, `course_id`, `user_id`, `parent_id`, `content`, `status`, `created_at`, `updated_at`; it has no `title` and no report relation/`reason`/`severity` columns. DB guide marks #97–#100 design-only; live schema is unverified. The logical `Discussion` response requires `title`, author, status, and comments. `PageMeta` requires page/size/total/total_pages.
- Runnable tests: No API #97 test source; no app tests run for this docs task. Scope test context: #08/#09 tests remain unverified after merge.
- Runtime wiring: API #97 is `UNWIRED / NOT_FOUND`; route/view source count is not a runtime-pass claim.

## SOURCE_TRACE

```text
Admin opens reported queue -> GET #97 with optional reason/severity/page -> Admin auth (not implemented) -> AC-37 logical read of reports + discussion summaries (physical report relation/grain unavailable) -> map Page<Discussion> (title/report fields/pagination unresolved) -> 200 DESIGN_RESOURCE_RETRIEVED or exact 401/403/500 catalog errors -> UI opens #98 detail
```

## PLAN BEFORE DD AUTHORING

1. Preserve the direct method/path, Bearer JWT/Admin, query names/types, no body, response, HTTP 200, and exact three catalog errors; do not add 404/422.
2. Reflect AC-37's read-reports-plus-discussion-summary step but do not claim a physical reports table. Keep `reason`/`severity` as optional string filters without invented enums, taxonomy, casing, trim, or matching rules.
3. Candidate physical evidence is only legacy `discussions` plus `users` and self-reference for comments. Do not issue SQL against guessed `reports`/`discussion_reports`, do not invent status predicate/root-only scope, sort order, join cardinality, or report aggregation.
4. Separate catalog Discussion fields from physical mapping: `title` has no legacy source; report reason/severity and reported timestamp have no response fields or legacy relation; author is a candidate `users` join; comments are self-reference candidates but summary/detail extent is unresolved.
5. Preserve `Page<Discussion>` and list every PageMeta and nested Discussion/DiscussionComment/UserSummary field. Page default/size/order, pagination total grain, comment projection and API #97 summary-vs-Discussion cardinality stay `DERIVED` only if clearly labeled or `SOURCE_REQUIRED`; no direct behavior is fabricated.
6. Keep API #97 read-only; mutation matrix N/A. Map auth, query parse, empty result, mapping/query exceptions only to the exact supported catalog code set; invalid query parse behavior remains unresolved because 422 is absent.
7. Create the eight registered sheet roles plus `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md` under `apps/study-server/docs/dd/97_admin_discussions_reported/`. Do not change source, tests, schema, catalog, diagram or unrelated DDs. Preserve `Draft — Needs Confirmation`.
8. Static-verify exact 11-file set, catalog/diagram contract, complete response fields and error set, JSON examples, template appendix suffix parity, local links/anchors, tables/fences/whitespace and `git diff --check`. No application tests for docs-only work.
9. Refresh `.agents/worklog/2026-10-24/inventory-study-api-dd-counts.md` with pre/post #97 counts; keep AC-37 macro-review pending until #100.

### Request usage matrix

| Request item | Source/use | Query/response use | Rule/status |
|---|---|---|---|
| Authorization | Bearer header | Authenticate and authorize Admin before queue read | Role DIRECT; Study Admin guard/claims `SOURCE_REQUIRED` |
| `reason` | Optional string query | Logical report-filter input | DIRECT name/type; value set/storage/match behavior unresolved |
| `severity` | Optional string query | Logical report-filter input | DIRECT name/type; enum/range/match behavior unresolved |
| `page` | Optional int32 query | Logical Page request | DIRECT name/type; default/min/max/page size unresolved |
| Body | None declared | None | DIRECT |

### Query/mutation matrix

| Query | Operation/source | Candidate fields/predicate | Status |
|---|---|---|---|
| Q1 | Read AC-37 logical reports and discussion summaries | Report relation, join key, report grain, reported condition, reason/severity columns and ordering | `SOURCE_REQUIRED`; diagram is logical evidence only |
| Q1a | Candidate legacy `discussions` read | `id`, `course_id`, `user_id`, `parent_id`, `content`, `status`, timestamps | Schema candidate only; cannot identify reported rows or satisfy title |
| Q1b | Candidate author projection from legacy `users` | `id`, `full_name`, nullable `avatar_url` | Candidate join; author relationship/live schema not verified |
| Q1c | Candidate comment self-reference | Child `discussions.parent_id`, author and content fields | Extent/visibility/order/cardinality unresolved; do not assume full thread on queue |
| Q2 | Count/page metadata | Count grain and shared filter predicate unavailable | `SOURCE_REQUIRED`; PageMeta fields direct, values unspecified |
| Mutation | None | GET is read-only | `N/A — READ-ONLY API` |

### Response source matrix (contract inventory)

| Field | Type | Candidate/source status |
|---|---|---|
| `success` | boolean | Envelope success branch; DIRECT convention |
| `businessCode` | string | `DESIGN_RESOURCE_RETRIEVED`; DIRECT |
| `message` | string | Wording unspecified; no invented literal |
| `data` | `Page<Discussion>` | Catalog direct; report-backed selection `SOURCE_REQUIRED` |
| `data.items[]` | `Discussion[]` | Catalog direct; report-backed selection `SOURCE_REQUIRED` |
| `data.items[].id` | int64 | Candidate `discussions.id`; legacy artifact only |
| `data.items[].course_id` | int64 | Candidate `discussions.course_id`; DDL nullable despite required logical field |
| `data.items[].title` | string | No legacy source; `SOURCE_REQUIRED` |
| `data.items[].content` | string | Candidate `discussions.content` |
| `data.items[].author` | `UserSummary` | Candidate `users.id/full_name/avatar_url`; required join and null handling unresolved |
| `data.items[].status` | `DiscussionStatus` | Candidate `discussions.status`; enum values/queue visibility unresolved |
| `data.items[].comments[]` | `DiscussionComment[]` | Logical schema direct; queue summary extent/source `SOURCE_REQUIRED` |
| `data.items[].comments[].id` | int64 | Candidate child discussion ID |
| `data.items[].comments[].discussion_id` | int64 | Candidate child `parent_id`; FK is nullable in legacy DDL |
| `data.items[].comments[].content` | string | Candidate child `discussions.content` |
| `data.items[].comments[].author` | `UserSummary` | Candidate child author via `users`; missing required author handling unresolved |
| `data.items[].comments[].author.id` | int64 | Candidate child `user_id` → `users.id` |
| `data.items[].comments[].author.full_name` | string | Candidate `users.full_name` |
| `data.items[].comments[].author.avatar_url` | uri? | Candidate `users.avatar_url`; omit when null |
| `data.items[].comments[].created_at` | date-time | Candidate child `discussions.created_at`; DDL timestamp lacks timezone declaration |
| `data.pagination` | `PageMeta` | Direct required shape; `page`, `size`, `total`, `total_pages` values unresolved |
| `meta` | object | Envelope field; endpoint-specific contents unspecified |
| `traceId` | uuid | Request trace per envelope convention |

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API runtime | No #97 route/module/test; router currently only #01–#09/#12–#14 | `UNWIRED / NOT_FOUND` | DD is design-only |
| Report storage | AC-37 diagram reads reports; legacy Study DDL has no report relation for discussions | `SOURCE_REQUIRED` | Cannot define a physical queue query |
| Filter semantics | Catalog only types reason/severity as string; no enum/taxonomy/match behavior | `SOURCE_REQUIRED` | Do not invent values or validation |
| Response report data | AC-37 queue includes report information but `Page<Discussion>` has no report fields | `DISCREPANCY` | Report summary cannot be returned through current schema |
| Discussion title | Reusable Discussion requires title; DB guide/DDL have no title column | `DISCREPANCY / SOURCE_REQUIRED` | Full response projection not source-backed |
| Page behavior | PageMeta requires four values; query only exposes optional page | `SOURCE_REQUIRED` | Default, page size, ordering and total grain need approval |
| Admin authorization | Catalog requires Admin; Study shared guard is Student-only | `SOURCE_REQUIRED` | Implementation needs approved Admin token/guard policy |
| Error integration | Current middleware allowlist excludes #97; helper error data is `{}` while shared guideline expects `null` | `DISCREPANCY / CONDITIONAL_FUTURE_WIRING` | Future integration must preserve direct catalog codes and resolve envelope behavior |

## CHANGES

- Files changed: `apps/study-server/docs/dd/97_admin_discussions_reported/` (8 sheets + 3 reports), this worklog, and `.agents/worklog/2026-10-24/inventory-study-api-dd-counts.md`.
- CONTEXT_UPDATES: None; this task does not change runtime/schema/contracts.
- Context pages changed: None planned.
- Assumptions: None silently adopted; any pagination suggestion in DD will remain explicitly `DERIVED` and require confirmation.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Context and worklog preflight | Root router, global context map, scope AGENTS/INDEX/workflow/tests and selected #48–#50 worklogs read. | `VERIFIED_STATIC_ONLY` |
| Source/contract review | #97 catalog row, reusable schemas, AC-37 index/diagram, Discussion DB guide/DDL, router/auth/middleware/response helper and linked DD precedents inspected. | `VERIFIED_STATIC_ONLY` |
| API #97 DD authoring | 11-file Markdown package created; DD remains Draft — Needs Confirmation. | `VERIFIED` |
| Static integrity | Exact manifest, 8/8 template appendix suffixes, response/request fields, JSON examples, local links/anchors, table widths, code fences, whitespace; `git diff --check`. | `PASS` |
| Runtime tests | Docs-only; not planned. | `NOT_RUN` |

## HANDOFF

- Remaining blockers: report schema and response fields, filter semantics, Discussion title, pagination, Admin guard and error integration.
- Next owner/action: Continue with API #98. Keep AC-37 cross-API macro-review pending until #100.

## POST-API #100 AC-37 MACRO REVIEW

- Completed after #100 DD was authored.
- Sequence #97 queue → #98 detail → #99 moderation → optional #100 soft delete matches the AC-37 page.
- Report fields/source and deleted-item filtering remain unresolved; see [API #100 plan result](../../../apps/study-server/docs/dd/100_admin_discussions_delete/PLAN_RESULT.md).
- No runtime, catalog, schema or diagram changes were made.
