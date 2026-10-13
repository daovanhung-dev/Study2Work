---
task_id: "2026-10-11-create-study-api18-dd"
date: "2026-10-11"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Create Study API #18 operations DD

## PRIOR_WORKLOG_REVIEW

- primary_task_type: docs
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-11/create-study-api16-dd.md`
    - carry_forward: API #16 remains a source-backed draft; preserve missing orders persistence and business-rule gaps as SOURCE_REQUIRED.
  - path: `.agents/worklog/2026-10-11/create-study-api17-dd.md`
    - carry_forward: API #17 records Operation persistence/lifecycle as unresolved and identifies API #18 operation_id UUID/int64 contract conflict; do not resolve by inference.
  - path: `.agents/worklog/2026-10-11/load-api13-detail-design-context.md`
    - carry_forward: createDD-markdown is the canonical Web/API DD workflow; preserve expected/current behavior and use the eight-sheet template.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Create a Markdown DD for API #18, `GET /api/v1/operations/{operation_id}`, in `apps/study-server/docs/dd/18_operations/` and package it as a ZIP.
- Canonical contract/approved DD: `docs/lists/list_api.md` API #18 plus applicable AC diagrams; keep the document Draft — Needs Confirmation while contract conflicts remain open.

## CURRENT_BEHAVIOR

- Source/config: Study Server has no API #18 route/module/query in current app source; `infra/postgres/study-server/DB.sql` has no operations table. A similarly named Work Server design table references `work_users` and has no established mapping to Study API #18.
- Runnable tests: Existing Study tests contain no API #18 test.
- Runtime wiring: `UNWIRED / NOT_FOUND` for API #18.

## SOURCE_TRACE

```text
API #18 catalog / AC references -> no Study Server route or caller/callee -> no Study operations table/query -> catalog-only ApiEnvelope<Operation> response -> no API #18 tests
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| operation_id type | Catalog convention, Operation.id and AC diagrams use UUID; API #18 row uses int64. | DISCREPANCY | Keep both source declarations and request contract unresolved. |
| Authorization | API row says operation owner; catalog summary says owner or Admin; diagrams state Student/Mentor/Admin, owner only. | DISCREPANCY | Do not settle Admin override or role policy. |
| Operation data and lifecycle | Catalog declares generic Operation fields; kind/status values, result shape by operation kind, storage and lifecycle are unspecified. | SOURCE_REQUIRED | Response mapping remains draft and open. |
| Producer response schemas | Operation tracking summary says producer endpoints return Operation, but API #93/#103 rows declare Notification/Report envelopes. | DISCREPANCY | Record producer contract mismatch in DD open questions. |
| Persistence | Study schema/runtime has no operations table/query. Work Server schema has a similarly named table tied to work_users, without a shared contract. | NOT_FOUND / OUT OF SCOPE | Do not map Work table to Study API. |
| Error semantics | Contract lists 403 and 404; does not define wrong-owner versus missing operation behavior. | SOURCE_REQUIRED | Preserve codes; record semantics question. |

## CHANGES

- Files changed: `apps/study-server/docs/dd/18_operations/*`, `apps/study-server/docs/dd/18_operations.zip`, this worklog.
- CONTEXT_UPDATES: None — no canonical context page changed.
- Context pages changed: None.
- Assumptions: Documentation-only scope; no runtime, catalog, database, migration or diagram edits.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| Inline Python structural validator | 11 files; 8 sheet order/front matters/headings; 2 JSON examples; 28 tables; 28 links; fingerprints and archive membership/CRC | PASS |
| unzip -t apps/study-server/docs/dd/18_operations.zip | 11 expected Markdown deliverables; no compressed-data errors | PASS |
| Study source scan: app, tests and infra/postgres/study-server/DB.sql | No API #18 route/query/test or Study operations table found | UNWIRED / NOT_FOUND |
| git diff --check and new-file whitespace scan | No whitespace errors | PASS |
| Study Server application tests | Not run; API #18 is not wired and plan excludes application tests | NOT_RUN |

## HANDOFF

- Remaining blockers: Contract owner decisions for operation_id, authorization, Operation result/lifecycle/storage, producer response schemas and 403/404 semantics.
- Next owner/action: Review the draft and resolve listed questions in canonical contract sources before marking the DD final or implementing the API.
