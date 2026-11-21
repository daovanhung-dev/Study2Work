---
task_id: "2026-10-12-create-study-api39-dd"
date: "2026-10-12"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo Study API #39 DD draft

## PRIOR_WORKLOG_REVIEW

- primary_task_type: docs
- selector_command: node scripts/select-worklogs.mjs --type docs --limit 3
- prior_worklogs_reviewed:
  - path: .agents/worklog/2026-10-12/commit-push-study-dds.md
    - carry_forward: API DD là design-only; không suy ra runtime từ DD.
  - path: .agents/worklog/2026-10-12/create-study-api27-dd.md
    - carry_forward: Giữ Draft + open questions, không tự đặt access/schema/business rule; Study không tạo ZIP.
  - path: .agents/worklog/2026-10-12/create-study-api28-dd.md
    - carry_forward: Giữ nguyên approved catalog contract và error set; ghi SOURCE_REQUIRED/DISCREPANCY/UNWIRED.
  - path: .agents/worklog/2026-10-12/create-study-api38-dd.md
    - carry_forward: PageMeta không cho phép tự thêm query/default; giữ source gaps mở và chỉ ghi candidate mapping.
- shortage: none

## EXPECTED_BEHAVIOR

- Requirement: Tạo DD draft cho Study API #39 GET /api/v1/discussions theo template Markdown, AC-19 và contract trong docs/lists/list_api.md; tạo 8 sheets, PLAN_RESULT.md, OPEN_QUESTIONS.md, VERIFICATION_REPORT.md và worklog; không tạo ZIP.
- Canonical contract/approved DD: API catalog khai báo Student Bearer JWT; query course_id?:int64, page?:int32, sort?:string; ApiEnvelope<Page<Discussion>>; HTTP/business codes 200 DESIGN_RESOURCE_RETRIEVED, 401 DESIGN_AUTHENTICATION_REQUIRED, 403 DESIGN_ACCESS_DENIED, 500 DESIGN_INTERNAL_ERROR.

## CURRENT_BEHAVIOR

- Source/config: Current apps/study-server/app/api/v1.py, app modules and tests contain no discussion/API #39 runtime route or test. DB guide/ERD/checked-in DDL are design evidence only. The DDL has no discussions.title and allows NULL course_id/user_id, while the DB guide/ERD describe those relations as required.
- Runnable tests: No API #39 discussion test was found; runtime tests were not run for this documentation-only task.
- Runtime wiring: API #39 is UNWIRED / NOT_FOUND; live database metadata was not checked.

## SOURCE_TRACE

~~~text
User request -> approved API #39 catalog + AC-19 -> candidate discussions/users projection from DB guide, ERD and checked-in DDL -> current router/module/test scan (API absent) -> documentation-only DD draft
~~~

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #39 runtime | Router/module/test scan has no discussion API. | UNWIRED / NOT_FOUND | DD describes approved design only. |
| Discussion.title | Catalog requires title; ERD and checked-in DDL have no title column. | SOURCE_REQUIRED / DISCREPANCY | No mapping from content is inferred. |
| Discussion FKs | DB guide/ERD mark course_id and user_id required; DDL permits NULL. | DISCREPANCY / DESIGN_ONLY | Candidate joins may not satisfy required response fields; live schema unknown. |
| Access/visibility | AC-19 mentions course participation/public threads but no predicate or status allowlist. | SOURCE_REQUIRED | No course access or visibility filter is invented. |
| Pagination/sort | Request has page/sort, response has PageMeta.size; defaults, size and sort policy absent. | SOURCE_REQUIRED | Preserve contract without adding parameters/defaults. |
| Comments scope | Discussion schema has comments[]; API #42 separately reads topic + comments. | DISCREPANCY / SOURCE_REQUIRED | API #39 list projection remains open. |
| Query validation | Catalog error set excludes 400/422. | SOURCE_REQUIRED | No validation error code added. |

## CHANGES

- Files changed: Eight sheets and three reports under apps/study-server/docs/dd/39_discussions/; this worklog.
- CONTEXT_UPDATES: None.
- Context pages changed: None.
- Assumptions: Use Draft — Needs Confirmation; preserve API #39 catalog contract; no ZIP per Study workflow; keep unknown business rules open; do not modify runtime/catalog/diagrams/DDL or API #38.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| node scripts/select-worklogs.mjs --type docs --limit 3 | Selected and reviewed the three listed docs worklogs; additional adjacent API #38 worklog was reviewed. | VERIFIED |
| API catalog, AC-19 diagram/index, DB discussion guide/ERD/DDL, API #10/#38 DD and current source review | Confirmed contract, design-only evidence, gaps and absence of API #39 runtime route/module/test. | VERIFIED |
| Template SHA-256 and sheet inventory | Eight template hashes recorded in VERIFICATION_REPORT.md; 8 sheets retain template order and audit appendices. | VERIFIED |
| Inline Python static DD validation + git diff --check | Validated package inventory, sheet metadata/order, template/output hashes, contiguous table widths, local links, two JSON examples, exact API #39 contract/error set, read-only/title gap/runtime status, whitespace and conflict markers. | VERIFIED |
| Runtime tests | Not run; docs-only task and API #39 is not wired. | NOT_RUN |
| Context validator | Not run; no agent context page or manifest changed. | NOT_REQUIRED |

## HANDOFF

- Remaining blockers: Product/API owner decisions listed in OPEN_QUESTIONS.md before approval or implementation.
- Next owner/action: Review the open questions and update canonical design sources before marking this DD Ready/Final.
