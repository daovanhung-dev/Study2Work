---
task_id: "2026-10-24-create-study-api86-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #86 — Xóa lesson

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Giữ response/schema gaps explicit; không invent asset/dependency mapping; static review và macro-review phải đúng phạm vi.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: Giữ contract trực tiếp, đánh dấu `DERIVED` và `SOURCE_REQUIRED`; AC-22 delete precedent là soft delete/history-preserving proposal, không phải schema evidence cho lesson.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: Catalog+diagram không đủ physical schema thì không viết SQL giả định; user-facing DD tiếng Việt, đúng 8 sheet + 3 reports và Markdown-only.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tiếp tục một API DD cho #86; lập plan và matrices trước authoring; đọc kỹ AC-34; dùng suy diễn tối giản, gắn nhãn; rà macro nhóm #82–#86 khi đủ DD; viết tiếng Việt và static-check ngay.
- Canonical contract/approved DD: Catalog #86 xác nhận `DELETE /api/v1/admin/lessons/{lesson_id}`, Bearer JWT/Admin, `path{lesson_id:int64!}`, không body/query, `ApiEnvelope<DeleteResult>`, HTTP 200 `DESIGN_RESOURCE_DELETED` và đúng 401/403/404/422/500 codes. `DeleteResult` là `id:int64`, `status:"deleted"`, `deleted_at:date-time`. AC-34 yêu cầu Admin có lesson-management permission, nhánh “Soft delete / delete theo policy”, rồi reload danh sách; catalog còn yêu cầu kiểm tra progress/reference. Skill `createDD-markdown` và workflow `docs-dd` được manifest wire cho `server-study`; Study giao Markdown, không tạo ZIP.

## CURRENT_BEHAVIOR

- Source/config: `app/api/v1.py` không có API #86/Admin lesson route; không có matching API #86 module/view/test. Shared auth chỉ có Student guard; middleware design-code allowlist không có Admin lesson route. Legacy `infra/postgres/study-server/DB.sql` có lessons BIGINT nhưng không có delete marker/`deleted_at`; `resources.lesson_id` và `lesson_progress.lesson_id` tham chiếu lessons mà không khai báo cascade. V1-PILOT Lesson là UUID model khác, không có delete marker; content_blocks, assessment_placements và lesson_progress_facts có FK `ON DELETE RESTRICT` tới lessons. Live schema chưa xác minh.
- Runnable tests: Không chạy; task documentation-only và API #86 không có test source.
- Runtime wiring: `UNWIRED / NOT_FOUND`; source-level route/view pair chưa tồn tại. DeleteResult `deleted_at` chưa có nguồn persistence được chọn.

## SOURCE_TRACE

```text
Admin Bearer principal -> authorize lesson-management permission -> DELETE by lesson_id -> Q1 target lookup -> Q2 resources/progress dependency checks -> DERIVED blocker policy (422 if references exist) -> logical soft-delete candidate (physical marker/timestamp SOURCE_REQUIRED; no cascade/audit invented) -> ApiEnvelope<DeleteResult> or exact catalog errors -> AC-34 reload list
```

## PREAUTHORING MATRICES

### Requirement Matrix

| Requirement | Evidence | Status/decision |
|---|---|---|
| `DELETE /api/v1/admin/lessons/{lesson_id}`; Bearer JWT; Admin; `lesson_id:int64!`; no body/query | Catalog #86 | DIRECT |
| `ApiEnvelope<DeleteResult>`; 200 `DESIGN_RESOURCE_DELETED`; errors 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 422 `DESIGN_VALIDATION_ERROR`, 500 `DESIGN_INTERNAL_ERROR` | Catalog #86 | DIRECT; preserve exact set |
| Admin lesson-management permission; check progress/reference; soft delete/delete according to policy; reload list | AC-34 index/diagram n5/n11/n12/n13 and catalog title | DIRECT intent; exact policy/dependency semantics unresolved |
| `DeleteResult.id`, literal status `deleted`, `deleted_at` datetime | Reusable `DeleteResult` schema | DIRECT response schema; timestamp source absent |
| Propose soft-delete, no cascade; reference exists blocks with catalog 422 | AC-34 policy branch + legacy FK evidence + safer history-preserving default | DERIVED recommendation; owner confirmation required |
| No audit mutation for #86 | AC-34 n12 and #85 n10 explicitly separate | Scope decision: do not copy #85 audit into #86 |

### Request Usage Matrix

| Request item | Source/use | Query/response use | Rule/status |
|---|---|---|---|
| Authorization | Bearer JWT | Admin lesson-management authorization | DIRECT requirement; claim/policy mapping SOURCE_REQUIRED |
| `lesson_id` | Required path int64 | Q1 lookup, Q2 scope, candidate soft-delete target, `data.id` | DIRECT type; legacy BIGINT physical mapping candidate |
| Body/query | None declared | None | DIRECT absence in catalog/diagram |
| `X-Trace-Id` | Current Study middleware convention | Envelope correlation | Current-source convention; not a business request field |

### Query Matrix

| Step | Type | Source/target | Conditions/effect | Status |
|---|---|---|---|---|
| Q1 | SELECT | Legacy `lessons AS l` candidate | `l.id=:lesson_id`; existence only | DERIVED from legacy DDL; live schema unknown; no row → candidate 404 |
| Q2a | EXISTS | Legacy `resources AS r` candidate | `r.lesson_id=:lesson_id` | Catalog asks reference check; exact live relation/policy SOURCE_REQUIRED |
| Q2b | EXISTS | Legacy `lesson_progress AS lp` candidate | `lp.lesson_id=:lesson_id` | Catalog asks progress check; status predicate/policy SOURCE_REQUIRED |
| Q2a/Q2b result | Branch | Legacy candidates | Any reference exists → candidate block before mutation | 422 code DIRECT; blocker semantics DERIVED |
| M1 | Logical soft-delete | No approved physical target | Mark target deleted and return persisted timestamp | AC-34 permits soft delete; marker/column SOURCE_REQUIRED; no SQL guessed |
| Audit | None proposed | No direct AC-34 #86 audit instruction | Do not copy #85 status audit | N/A for #86 |

### Mutation Matrix

| Mutation | Target | Fields/effect | Status |
|---|---|---|---|
| M1 | Logical lesson soft-delete | Preserve history; no child/reference cascade | DERIVED recommendation within AC-34 policy branch; physical source required |
| Physical delete | Excluded from candidate | No `DELETE FROM lessons` or child mutation | Do not infer hard-delete/cascade from HTTP method or FK artifact |
| Dependency rows | resources, lesson_progress | No delete/update of referenced rows | Scope boundary; candidate block instead |
| Audit | None | No audit event added to #86 | Diagram assigns audit to #85, not #86 |
| Transaction | Q1/Q2/M1 | Check and mutation should be atomic if a physical policy is approved | DERIVED; owner/isolation/locking unresolved |

### Response Source Matrix

| Response item | Candidate source/transform | Status/gap |
|---|---|---|
| Envelope/business codes | Catalog #86 + reusable `ApiEnvelope<T>` | DIRECT; exact codes only |
| `data.id` | Successfully processed lesson ID | DeleteResult DIRECT; physical target binding candidate |
| `data.status` | Literal `deleted` | DIRECT reusable schema; lowercase exact value |
| `data.deleted_at` | Approved persisted deletion timestamp | DIRECT field/type; physical timestamp source SOURCE_REQUIRED; no clock fallback |
| `meta`, `traceId` | Envelope/current middleware | Empty meta candidate; trace propagate/generate convention |
| Error `data` | API guideline says null; current helper defaults absent data to `{}` | DISCREPANCY for future wiring |

## PRIOR SOURCE REVIEW

- AC-34: API #83 detail reads lesson + dependencies before the choice; #84 updates metadata only; #85 changes status + audit; #86 deletes by policy and then reloads. #86 owns no audit branch.
- DD #72 and #77: preserve dependency/history, do not invent soft-delete column or `deleted_at` source, use only catalog-listed codes, and keep blocker 422 as DERIVED where policy is open.
- Legacy DDL: `resources.lesson_id` and `lesson_progress.lesson_id` reference `lessons.id`; no delete marker and no `ON DELETE CASCADE` is declared.
- V1-PILOT DDL: different UUID Lesson model; child FKs to Lesson use `ON DELETE RESTRICT`, but this is not the API int64 runtime model.
- Current source: no API #86 route/module/test; Student-only helper; design error allowlist lacks Admin path; error helper returns `{}` for absent data.

## PLAN BEFORE DD AUTHORING

1. Xác nhận API #86 catalog row, reusable DeleteResult, AC-34 node/edges và postcondition; giữ exact request/response/status/error contract.
2. Đọc hết nhóm #82–#85 và status/delete precedent #72/#77; phân định ranh giới metadata (#84), status+audit (#85), delete (#86).
3. Đọc router/auth/middleware/response source và legacy/V1 schema/dependency relations; xác định rõ `UNWIRED`, schema conflict, live-schema boundary.
4. Lập Requirement, Request Usage, Query, Mutation và Response Source matrices trước khi tạo folder.
5. Chỉ suy diễn tối thiểu ngoài diagram: đề xuất logical soft-delete, chặn khi có legacy reference/progress bằng catalog 422, không phát minh marker/timestamp column, audit table, cascade hoặc error code.
6. Tạo 8 registered template sheets + PLAN_RESULT/OPEN_QUESTIONS/VERIFICATION_REPORT trong folder #86; giữ exact appendix tails, tiếng Việt, Draft — Needs Confirmation và không tạo ZIP.
7. Chạy static package/contract/JSON/table/fence/link/whitespace checks; cập nhật verification reports, inventory worklog và #82–#86 macro-review.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Delete policy | Diagram cho phép soft-delete hoặc policy delete; catalog yêu cầu check progress/reference | `DIRECT INTENT / DERIVED POLICY` | Propose history-preserving soft-delete; block existing references with catalog 422, needs confirmation |
| Physical deletion marker/timestamp | Legacy lessons không có deleted_at; pilot lesson khác UUID model và cũng không có deletion marker | `SOURCE_REQUIRED / DISCREPANCY` | DeleteResult.deleted_at không thể map từ current artifacts; không viết mutation SQL |
| Dependency set | Legacy resources/progress references; V1-PILOT has distinct restrictive refs | `CANDIDATE / SOURCE_REQUIRED` | Keep schemas separate and no cascade |
| Runtime/Admin access | No API #86 route/view/test; Student-only guard | `UNWIRED / NOT_FOUND` | DD is design-only; no runtime claim |

## CHANGES

- Files changed: API #86 DD folder and this worklog; API #85 appendix/report boundary correction; AC-34 macro-review updates to DD #82–#85 and their worklogs; API #84/#86 data-mapping reload notes. The API-count worklog was already refreshed after #86 appeared.
- CONTEXT_UPDATES: None planned.
- Context pages changed: None planned.
- Assumptions: Preserve existing user changes; keep soft-delete, dependency-blocker and body/status proposals labeled as DERIVED; no runtime/schema change.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog selector and review | Deno selector returned #48/#49/#50; all three read in full; no shortage. | `VERIFIED` |
| Contract/source/template/diagram inspection | Catalog #86, reusable DeleteResult, AC-34 nodes/edges, DD #72/#77 and #82–#85 boundaries, route/auth/middleware/response, legacy/V1 DDL and manifest registry reviewed; matrices recorded. | `VERIFIED_STATIC_ONLY` |
| API #86 DD static validation | Exact 11-file package; all 8 template suffixes match; exact catalog success/error set and DeleteResult fields retained; 3 JSON blocks parse; 33 tables / 373 data rows consistent; 16 fences balanced; 36 links/anchors resolve; whitespace clean. | `PASS — STATIC` |
| API #82–#86 package recheck | All five folders have 11 Markdown files and 8/8 registered appendix suffixes; JSON, tables, fences, links/anchors and whitespace pass. | `PASS — STATIC` |
| API #85 appendix repair | Heading boundaries are line-starts; all 8 suffixes byte-match registered template; prior literal `\\n` report endings removed; full #82–#86 static validation now passes. | `PASS — STATIC` |
| AC-34 macro-review #82–#86 | Compared diagram flow and cross-DD contracts; updated overview/open questions/reports and linked worklogs; unresolved source/owner gaps remain explicit. | `VERIFIED_WITH_OPEN_QUESTIONS` |
| Current inventory | 103 catalog IDs; 86 DD folders / 17 missing; 74 full 11-file packages / 12 legacy core-only; 12 route-plus-view IDs / 91 without. | `VERIFIED_STATIC_ONLY` |
| `git diff --check` and whitespace | No diagnostics; custom scan also covers untracked DD and worklog Markdown. | `PASS` |
| Application tests | Not run; docs-only and APIs #82–#86 are unwired. | `NOT_RUN` |
| Context validator | No `.agents/server-study` page or registry changed. | `NOT_APPLICABLE` |

## HANDOFF

- Remaining blockers: Owner confirmation of deletion policy/dependency blocker semantics, physical soft-delete marker and persisted timestamp source, Admin policy, selected schema, transaction and error integration; related #82–#85 contract gaps remain open.
- Next owner/action: API #86 DD and the AC-34 #82–#86 document-level review are verified with open questions retained. Continue at API #87 in the next API-DD session.
