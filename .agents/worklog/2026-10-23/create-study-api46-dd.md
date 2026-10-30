---
task_id: "2026-10-23-create-study-api46-dd"
date: "2026-10-23"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Create Study API #46 DD

## PRIOR_WORKLOG_REVIEW

- primary_task_type: docs
- selector_command: deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3
- prior_worklogs_reviewed:
  - path: .agents/worklog/2026-10-23/create-study-api41-dd.md
    - carry_forward: Preserve catalog fields; mark unsupported choices DERIVED and keep contract/schema discrepancies explicit.
  - path: .agents/worklog/2026-10-23/create-study-api42-dd.md
    - carry_forward: Reconcile connected APIs at group level and preserve source-backed versus proposed behavior.
  - path: .agents/worklog/2026-10-23/create-study-api43-dd.md
    - carry_forward: Read AC flows and source/schema evidence; do not treat a DD or logical table name as runtime wiring.
- shortage: none

## EXPECTED_BEHAVIOR

- Requirement: Create and immediately validate one Vietnamese, source-aware Markdown DD for Study API #46, then define its consistency boundary with connected APIs #47/#48.
- Canonical contract/approved DD: docs/lists/list_api.md API #46; AC-21 page in AC_03_MENTOR_TEACHING.drawio; DB_UNICA diagrams/table guide and checked-in DDL; createDD-markdown skill; Study Markdown-only workflow.

## CURRENT_BEHAVIOR

- Source/config: API #46 has no route in app/api/v1.py, no matching module/view and no focused test. The current API #6 public course list is source-backed, but it filters PUBLISHED and requires Student/public behavior; it is not API #46. Mentor-specific authorization is not implemented in this route graph.
- Runnable tests: Not run; documentation-only task. API #6 tests cover a different endpoint and do not verify #46.
- Runtime wiring: UNWIRED / NOT_FOUND for API #46.
- Schema evidence: DB_UNICA_TABLES.md, DB_UNICA_ERD.drawio and infra/postgres/study-server/DB.sql describe courses.id BIGSERIAL, courses.mentor_id -> users.id, name/description/thumbnail_url/price/status. DB.sql permits nullable mentor_id/status/price. The separate infra/postgres/02_study_db.sql pilot uses UUID course IDs and owner_subject_id, moves draft/published state to course_versions.status, and has no mentor_id relation. Live schema is unverified; these models must not be combined.

## SOURCE_TRACE

Expected flow: GET mentor course list -> validate Bearer/JWT Mentor identity -> validate status/page/size -> select the current mentor's manageable courses and required mentor summary -> count the same scope -> return Page<Course> envelope. Current route/module/test flow is absent.

## PLAN BEFORE DD AUTHORING

Plan locked before creating the API #46 DD folder:

1. Keep the catalog contract exactly: GET /api/v1/mentor/courses; Bearer JWT role Mentor; optional status:CourseStatus; page:int32 default 1; size:int32 default 20; ApiEnvelope<Page<Course>>; HTTP 200 DESIGN_RESOURCE_RETRIEVED; errors only 401 DESIGN_AUTHENTICATION_REQUIRED, 403 DESIGN_ACCESS_DENIED, 422 DESIGN_VALIDATION_ERROR, 500 DESIGN_INTERNAL_ERROR.
2. Read the full AC-21 diagram. It orders #46 list courses and ownership/assignment check before course selection, upload, #47 lecture creation, DB insert and #48 lecture reload. Keep #46 read-only; require #47 to enforce the same course-scope rule. Do not create links to future DD files.
3. Candidate legacy mapping: scope rows by courses.mentor_id = numeric Mentor principal; optional status adds courses.status equality. Do not force PUBLISHED, because AC-21 is mentor management and the flow includes lecture creation for a selected course. Treat a separate assignment relation as SOURCE_REQUIRED; none appears in the legacy ERD/DDL or pilot schema.
4. Reuse the Course/Page contract and public Course projection precedent from API #6: select course fields plus users mentor summary; map courses.name to Course.title, price to decimal-string, and omit optional category because no course-category relation is source-backed. If required response fields (mentor, price, status) cannot be mapped, return the catalog 500 candidate rather than fabricate values.
5. Use page=1, size=20 as DIRECT catalog defaults. DERIVED consistency proposal: page >= 1, size 1..100 and default order created_at DESC, id ASC, matching API #6. Keep maximum/order provisional and list in OPEN_QUESTIONS. No sort parameter is added.
6. Query Q1/Q2 use identical ownership and optional status predicates; use LEFT JOIN users for mentor summary and detect incomplete required mentor mapping. Empty/out-of-range pages return 200 with items=[] and PageMeta; total_pages=0 when total=0. These list semantics are DERIVED where the catalog/diagram is silent.
7. Record the schema conflict between int64/mentor_id legacy artifacts and UUID/owner_subject_id pilot DDL; record missing CourseStatus enumeration, direct-owner versus assigned-course semantics, nullable legacy fields, optional category source gap, error data null-vs-empty helper discrepancy, and unverified live schema.
8. Create 8 ordered template sheets plus PLAN_RESULT.md, OPEN_QUESTIONS.md, and VERIFICATION_REPORT.md in apps/study-server/docs/dd/46_mentor_courses/. Preserve the template appendices and exact error set. Study workflow requires Markdown only and no new ZIP.
9. Static-validate files/front matter, catalog contract/errors, source links, JSON examples, Markdown tables/fences, one-field/condition/error per row, matrix coverage and group boundary. Do not run app tests for this docs-only task.

### API Requirement Matrix

| API ID | Method / endpoint | Actor/auth | Request | Response/status | Basis |
|---|---|---|---|---|---|
| #46 | GET /api/v1/mentor/courses | Mentor / Bearer JWT | Authorization | ApiEnvelope<Page<Course>>; 200; errors 401/403/422/500 exactly as catalog | Catalog + AC-21 |
| #46 | GET /api/v1/mentor/courses | Mentor / Bearer JWT | status?:CourseStatus | Same response/status contract | Catalog + AC-21 |
| #46 | GET /api/v1/mentor/courses | Mentor / Bearer JWT | page?:int32=1 | Same response/status contract | Catalog + AC-21 |
| #46 | GET /api/v1/mentor/courses | Mentor / Bearer JWT | size?:int32=20 | Same response/status contract | Catalog + AC-21 |

### Request Usage Matrix

| Request field | Source | Validation/use | Response use | Evidence/gap |
|---|---|---|---|---|
| Authorization | HTTP header | Require valid Bearer/JWT and MENTOR role; derive numeric principal from current Study JWT shape as proposal | Scopes course query | Contract direct; Mentor guard absent in current source |
| status | Query | If present, exact equality predicate; CourseStatus values unresolved; invalid value maps to catalog 422 only after enum is confirmed | Course.status remains source value | Catalog direct; enum SOURCE_REQUIRED |
| page | Query or default 1 | int32 and >=1 | PageMeta.page | Default direct; range consistent with API #6 as DERIVED |
| size | Query or default 20 | int32 and proposed 1..100 | PageMeta.size and LIMIT | Default direct; max 100 DERIVED from API #6 |

### Query Matrix

| Query | Candidate source | Query item | Rule | Evidence |
|---|---|---|---|---|
| Q1 | courses AS c | c.id | Select course ID | Legacy ERD/DDL candidate; pilot conflict |
| Q1 | courses AS c | c.name AS title | Map physical name to logical title | API #6 precedent |
| Q1 | courses AS c | c.description | Nullable course description | Legacy schema candidate |
| Q1 | courses AS c | c.thumbnail_url | Nullable thumbnail URL | Legacy schema candidate |
| Q1 | courses AS c | c.price | Serialize decimal-string; null cannot satisfy contract | Legacy schema candidate; nullable discrepancy |
| Q1 | courses AS c | c.status | Map CourseStatus; status set/source unresolved | Contract + legacy schema candidate |
| Q1 | courses AS c | c.created_at | Default sort key only | Legacy schema candidate |
| Q1 | courses AS c | c.mentor_id = :mentor_id | Always scope to numeric current Mentor | DERIVED ownership candidate; assignment unsupported |
| Q1 | courses AS c | c.status = :status | Apply only when status is present | Catalog filter; predicate DERIVED |
| Q1 | users AS m | m.id | Required mentor ID | API #6 precedent |
| Q1 | users AS m | m.full_name | Required mentor name | API #6 precedent |
| Q1 | users AS m | m.avatar_url | Optional mentor avatar | API #6 precedent |
| Q1 | courses AS c | ORDER BY c.created_at DESC | Newest first | DERIVED from API #6 |
| Q1 | courses AS c | ORDER BY c.id ASC | Stable tie-breaker | DERIVED from API #6 |
| Q1 | courses AS c | LIMIT :size | Effective page size | Catalog default; max range proposal |
| Q1 | courses AS c | OFFSET (:page-1)*:size | Page offset | Catalog defaults; derived formula |
| Q2 | courses AS c LEFT JOIN users AS m | COUNT(*) | Count same owner/status scope as Q1 | API #6 pattern |
| Q2 | courses AS c LEFT JOIN users AS m | COUNT(*) FILTER (WHERE m.id IS NULL) | Detect incomplete required mentor projection | API #6 pattern |

### Mutation Matrix

| Mutation | Target | Fields/condition | Status |
|---|---|---|---|
| None | N/A | N/A | N/A — READ-ONLY API |

### Response Source Matrix

| Response field | Contract/source | Candidate mapping | Rule/status |
|---|---|---|---|
| success | ApiEnvelope | Branch constant | DIRECT contract |
| businessCode | ApiEnvelope | DESIGN_RESOURCE_RETRIEVED or catalog error code | DIRECT contract |
| message | ApiEnvelope | Safe branch message | Text is not specified |
| data.items | Page<Course> | Q1 rows | Empty array on no matches; DERIVED |
| data.items[].id | int64 | courses.id | Legacy candidate; pilot UUID conflict |
| data.items[].title | string | courses.name | Alias; API #6 precedent |
| data.items[].description | string? | courses.description | Null when source NULL |
| data.items[].thumbnail_url | uri? | courses.thumbnail_url | Null when source NULL |
| data.items[].price | decimal-string | courses.price | Decimal-safe conversion; null source is integrity gap |
| data.items[].status | CourseStatus | courses.status | Required enum/source gap; null source cannot map |
| data.items[].mentor | UserSummary | users joined by courses.mentor_id | Required; missing ID/name is integrity failure |
| data.items[].category | Category? | No source-backed course-category relation | Omit optional field as API #6 precedent |
| data.pagination.page | int32 | Effective page | Request/default 1 |
| data.pagination.size | int32 | Effective size | Request/default 20; proposed max 100 |
| data.pagination.total | int64 | Q2 COUNT(*) | Same filters as Q1 |
| data.pagination.total_pages | int32 | ceil(total/size) | 0 when total=0; DERIVED |
| meta | object | Envelope metadata | Empty object unless fieldErrors |
| traceId | uuid | Request trace context | Standard contract; current helper behavior noted |

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #46 runtime | No route/module/focused test | UNWIRED / NOT_FOUND | DD is design-only |
| Course identity/ownership schema | Legacy int64 mentor_id versus V1-PILOT UUID owner_subject_id/course_versions | DISCREPANCY / SOURCE_REQUIRED | No single executable mapping can be claimed |
| Managed versus assigned scope | AC-21 says owns/assigned; only legacy courses.mentor_id is present | DERIVED / SOURCE_REQUIRED | Direct ownership is provisional; assigned courses need an approved relationship |
| CourseStatus | Catalog type exists; allowed values are not defined; runtime model is string | SOURCE_REQUIRED | Cannot finalize enum validation |
| Legacy nullable required values | DB.sql permits NULL price/status/mentor_id while Course requires price/status/mentor | DISCREPANCY | Candidate integrity failure for missing required mapping; schema constraints need confirmation |
| Error data | API guidelines specify null; current error_response emits {} for None | DISCREPANCY | Expected and current envelope shapes differ |

## CHANGES

- Files changed: `apps/study-server/docs/dd/46_mentor_courses/` (8 sheets + 3 reports) and this worklog.
- CONTEXT_UPDATES: None planned; no runtime, catalog, diagram or schema changes.
- Context pages changed: None.
- Assumptions: Where approved sources are silent, use the simplest DERIVED proposal and preserve every schema/contract conflict as an open question.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog selector and review | Selector selected and all three docs worklogs #41–#43 were read; no shortage. | VERIFIED |
| Context and skill registry | server-study is wired to createDD-markdown; skill loaded; Study workflow overrides ZIP packaging. | VERIFIED |
| AC-21 diagram parse | Full AC-21 node and edge flow read; confirms #46 -> ownership/assignment -> upload -> #47 insert -> #48 reload. | VERIFIED |
| Catalog and schema/source coverage | API #46 row, Course schema, ERD/table guide, both DDL models, API #6 DD/source precedent and current route/test scope reviewed. | VERIFIED |
| Runtime tests | Not run; docs-only. | NOT_RUN |
| Context validator | Deno fallback reports missing DB Admin pages/source and unavailable baseline commit `9a70eb6764a6587093a92d3bd7e4cc0bea1651c4`; unrelated to this Study DD. | BLOCKED_UNRELATED_REPO_CONTEXT |
| DD authoring/validation | 11 files present; all 8 sheet appendices match canonical template byte-for-byte; JSON, table widths, fences, local paths/anchors, catalog contract and exact error set passed. | VERIFIED |

## HANDOFF

- Remaining blockers: Confirm live schema, mentor assignment model, CourseStatus values, legacy nullability, and optional category mapping before implementation approval.
- Next owner/action: API #48 DD and macro-review were completed on 2026-10-24; continue with API #49. See the follow-up below.

## FOLLOW-UP — 2026-10-24 AC-21 MACRO REVIEW

- Updated the #46 Overview, Plan Result, Open Questions and Verification Report after comparing the completed #47/#48 DDs.
- Result: #46/#47/#48 consistently use the same direct-owner candidate, avoid a PUBLISHED filter in the Mentor management flow, keep legacy BIGINT separate from V1-PILOT UUID schema, and retain the unresolved asset projection/error-envelope gaps.
- Assignment relation and Mentor ID mapping remain SOURCE_REQUIRED; the review does not claim runtime consistency.
- Follow-up files: `apps/study-server/docs/dd/46_mentor_courses/` and `apps/study-server/docs/dd/47_mentor_lectures_create/`.
