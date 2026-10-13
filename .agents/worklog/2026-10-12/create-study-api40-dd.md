---
task_id: "2026-10-12-create-study-api40-dd"
date: "2026-10-12"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["Study Server documentation"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Create Study API #40 discussion-create DD

## PRIOR_WORKLOG_REVIEW

- primary_task_type: docs
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-12/commit-push-study-dds.md`
    - carry_forward: Follow Study Server Markdown DD workflow; no ZIP; preserve earlier DD artifacts.
  - path: `.agents/worklog/2026-10-12/create-study-api27-dd.md`
    - carry_forward: Treat the catalog as the approved contract; keep uncertain design evidence explicit.
  - path: `.agents/worklog/2026-10-12/create-study-api28-dd.md`
    - carry_forward: Keep DDs design-only; map only sourced fields and do not infer runtime behavior.
  - path: `.agents/worklog/2026-10-12/create-study-api39-dd.md`
    - carry_forward: Discussion access, title storage, visibility, FK nullability, and response details remain unresolved; API #40 is not wired.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Create an eight-sheet Markdown DD for API #40 with `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md`, and this worklog. Preserve the existing catalog contract and record source gaps for review. Do not change runtime, catalog, diagrams, ERD, or DDL.
- Canonical contract/approved DD: `POST /api/v1/discussions`; Student Bearer JWT; request `course_id:int64!`, `title:string!`, `content:int64!`; response `ApiEnvelope<Page<Discussion>>`; HTTP 201 `DESIGN_RESOURCE_CREATED`; errors 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 422 `DESIGN_VALIDATION_ERROR`, 500 `DESIGN_INTERNAL_ERROR`.

## CURRENT_BEHAVIOR

- Source/config: Catalog and AC-19 document the operation; AC-19's new-topic branch labels `INSERT Discussion`. Current Study Server runtime has no discussions route or module. Checked-in DB/ERD material is design evidence; live schema was not inspected.
- Runnable tests: No API #40 runtime test exists in the current source scan. Runtime tests were not run because this task is documentation-only and the route is unwired.
- Runtime wiring: `UNWIRED / NOT_FOUND`.

## SOURCE_TRACE

```text
Student client -> POST /api/v1/discussions (catalog / AC-19 design only)
  -> current route/module: NOT_FOUND
  -> candidate DB action from AC-19: INSERT Discussion (not executable/approved SQL)
  -> response contract in catalog: ApiEnvelope<Page<Discussion>>
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| `content` representation | Catalog/AC-19 request is `int64`; reusable `Discussion` says `string`; DB guide/DDL say `TEXT` | OPEN / mismatch preserved | No conversion or validation behavior can be selected |
| Required `title` storage | Request and logical schema require title; ERD and checked-in DDL have no title column | OPEN / source missing | Cannot define physical insert/read mapping |
| `Page<Discussion>` create response | Catalog response has `PageMeta`; request has no paging inputs or create-page rule | OPEN | Pagination values cannot be derived |
| Course permission | AC-19 requires course discussion permission; predicate not defined | OPEN | Access evaluation and 403 cases unclear |
| Status and timestamps | Status enum/policy absent; checked-in DDL default is design-only; timestamps are NOT NULL without defaults | OPEN | Initial status and insert timestamp source unclear |
| FK nullability | DB guide/ERD imply required `course_id`/`user_id`; checked-in DDL permits NULL | OPEN | Candidate insertion constraints differ by source |
| Author/comments response | Discussion requires author/comments; JWT only identifies principal; AC-19 points to API #42 for reload | OPEN | Response assembly is not defined |

## CHANGES

- Files changed: Added `apps/study-server/docs/dd/40_discussions_create/` with eight ordered sheets and three reports; added `.agents/worklog/2026-10-12/create-study-api40-dd.md`. Existing API #27–#39 artifacts were preserved. No ZIP created.
- CONTEXT_UPDATES: None.
- Context pages changed: None.
- Assumptions: “Create API #40” means draft the DD, consistent with the approved plan. The catalog remains authoritative pending review; unresolved content/title/pagination/access/schema issues stay open.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type docs --limit 3` | Selected commit-push-study-dds, API #27 DD, and API #28 DD; API #39 worklog also reviewed | PASS |
| Static DD inspection | Expected files, template fingerprints/order, metadata, table structure, JSON, local links, contract and error set checked | PASS |
| Whitespace/conflict scan | No trailing whitespace or conflict markers | PASS |
| `git diff --check` | No whitespace errors | PASS |
| Runtime tests | Not run; documentation-only scope and API #40 is unwired | NOT_RUN |

## HANDOFF

- Remaining blockers: Product/API and schema owners must resolve the questions in [`OPEN_QUESTIONS.md`](../../../apps/study-server/docs/dd/40_discussions_create/OPEN_QUESTIONS.md) before implementation.
- Next owner/action: Review and confirm the draft; update the canonical contract/schema only after decisions are approved.
