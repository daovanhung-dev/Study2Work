---
task_id: "2026-10-12-create-study-api36-dd"
date: "2026-10-12"
primary_task_type: "docs"
secondary_task_types: ["review"]
project_scopes: ["server-study"]
cross_scope_dependencies: ["docs/lists/list_api.md", "apps/study-server/docs/diagrams/"]
status: "VERIFIED"
---

# Worklog: Tạo Study API #36 DD draft

## PRIOR_WORKLOG_REVIEW

- primary_task_type: docs
- selector_command: node scripts/select-worklogs.mjs --type docs --limit 3
- prior_worklogs_reviewed:
  - path: .agents/worklog/2026-10-12/commit-push-study-dds.md
    - carry_forward: Preserve existing DD artifacts; separate design contract from runtime evidence.
  - path: .agents/worklog/2026-10-12/create-study-api27-dd.md
    - carry_forward: Keep Study DDs at Draft — Needs Confirmation, record source gaps, and do not create a ZIP.
  - path: .agents/worklog/2026-10-12/create-study-api28-dd.md
    - carry_forward: Preserve the catalog contract and exact error set; distinguish expected behavior from current behavior.
- shortage: none
- Additional precedent reviewed: API #35 worklog and DDs #33–#35; preserve these untracked artifacts and reuse the Study API DD validation approach.

## EXPECTED_BEHAVIOR

- Requirement: Create a template-based Markdown DD draft for Study API #36, GET /api/v1/submissions/{submission_id}, with the standard sheets and reports. Do not implement runtime, change catalog/diagrams/schema, create a ZIP, or modify DDs/worklogs #27–#35.
- Canonical contract/approved DD: docs/lists/list_api.md is APPROVED_DESIGN_CONTRACT. Student Bearer JWT; path submission_id:int64!; response ApiEnvelope<Submission>; HTTP 200 DESIGN_RESOURCE_RETRIEVED; exact errors 401, 403, 404, 500.

## CURRENT_BEHAVIOR

- Source/config: API #36 has no route/module/query/test in the current Study source. The catalog and AC-17 diagram define the design contract. assignment_submissions is candidate design evidence in DB_UNICA_TABLES.md and checked-in DB.sql; live schema is not verified.
- Runnable tests: No API #36 test exists; runtime tests are outside this documentation-only task.
- Runtime wiring: UNWIRED / NOT_FOUND.

## SOURCE_TRACE

~~~text
Student Bearer request -> role authentication -> candidate submission lookup by path ID
-> access predicate is unresolved -> Submission projection -> ApiEnvelope response
Current API #36 route/module/query/test: UNWIRED / NOT_FOUND
~~~

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Student access predicate and 403/404 mapping | API catalog includes both 403 and 404; AC-17 only shows Student viewing the submitted summary. | SOURCE_REQUIRED | Do not choose owner, enrollment, or resource-masking behavior. |
| Score and feedback visibility | Submission schema includes optional score/feedback; AC-17 only displays submitted status; AC-23 assigns grading to Mentor. | SOURCE_REQUIRED | Do not decide whether or when these fields are disclosed. |
| Files response mapping | Logical Submission.files is UploadAsset[]; candidate table stores one nullable file_url; API #34 representation/binding is unresolved. | DISCREPANCY / DESIGN_ONLY | Keep response contract intact and mark physical mapping unresolved. |
| Foreign-key nullability | DB table notes describe assignment_id/user_id as required; checked-in DDL permits NULL. | DISCREPANCY / DESIGN_ONLY | Candidate source only; do not claim live schema. |
| Status and timestamp semantics | DDL defaults status to SUBMITTED but the enum is incomplete; submitted_at is TIMESTAMP without a timezone rule. | SOURCE_REQUIRED / DESIGN_ONLY | Preserve candidate fields and record semantic gaps. |

## CHANGES

- Files changed: Created `apps/study-server/docs/dd/36_submissions_detail/` with the eight canonical DD sheets, `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, and `VERIFICATION_REPORT.md`; finalized this worklog.
- CONTEXT_UPDATES: None planned; no runtime, contract, schema, or context page changes.
- Context pages changed: None.
- Assumptions: “Create API #36” means create its Study API DD only. Keep Draft — Needs Confirmation and preserve all existing untracked files.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type docs --limit 3` | Selected and read the three listed same-type worklogs. | VERIFIED |
| Catalog / AC-17 / DB design / source inventory review | Sources reviewed; remaining design gaps are documented in the DD and open questions. | VERIFIED |
| Static DD validation | Eight template appendices match; front matter, JSON examples, Markdown tables, relative links/anchors, whitespace, and catalog method/path/auth/request/response/status/error set pass. | VERIFIED |
| `git diff --check` plus explicit scan of untracked DD/worklog files | No whitespace errors. | VERIFIED |
| Runtime tests / live DB | Not run; API #36 is unwired and this task is design documentation only. | OUT OF SCOPE |

## HANDOFF

- Remaining blockers: None for this draft. Authorization, score/feedback visibility, asset mapping, and schema semantics remain open for product/API/architecture confirmation.
- Next owner/action: Review and confirm the open questions before treating the draft as an implementation-ready contract.
