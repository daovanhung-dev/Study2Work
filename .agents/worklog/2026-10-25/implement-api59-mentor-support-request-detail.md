---
task_id: "2026-10-25-implement-api59-mentor-support-request-detail"
date: "2026-10-25"
primary_task_type: "coding"
secondary_task_types: ["docs", "test"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Implement Study Server API #59

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run -A scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: 52 matching worklogs; selected and read all three; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-25/implement-api34-upload-assets.md`
    - carry_forward: Resolve UploadAsset only through owner/purpose/course-scoped metadata; local DDL and fake tests do not prove live DB or object availability.
  - path: `.agents/worklog/2026-10-25/implement-api47-mentor-lectures.md`
    - carry_forward: Require explicit shared MENTOR guard, direct `courses.mentor_id` scope, SQL-only query constants, safe errors and transaction ownership.
  - path: `.agents/worklog/2026-10-25/implement-api48-mentor-lecture-detail.md`
    - carry_forward: Preserve catalog error set; malformed signed-int64 path values map to 404; detail reads distinguish missing from another direct owner.
- related_worklog_reviewed:
  - path: `.agents/worklog/2026-10-25/implement-api58.md`
    - carry_forward: API #58 selected a local DERIVED legacy BIGINT support schema, direct course-owner predicate, full ordered thread, role-purpose constrained UploadAsset links and no live-schema claim. API #59 should reuse these choices.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Catalog/DD: `GET /api/v1/mentor/support/{request_id}`; Bearer JWT role Mentor; required int64 path; HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<SupportRequest>`; catalog errors are 401, 403, 404 and 500. It is read-only.
- AC-24 flow: #58 lists support requests, #59 reads one request and its conversation, #60 sends a reply, and #61 conditionally resolves the request. #59 does not mutate request/message state.
- User's project rule allows a simple DERIVED fallback only after diagram → infrastructure → catalog review. API #58's user-directed fallback is now current local source and is reused without claiming live-schema approval.

## CURRENT_BEHAVIOR

- API #59 is wired at `GET /api/v1/mentor/support/{request_id}` and registered in `DESIGN_CONTRACT_PATHS`. The view uses shared MENTOR auth, signed-int64 parsing, direct course ownership, read-only request/thread queries, ordered upload mapping and the API #58 response models.
- API #58 now wires `support_requests`, `support_messages`, and `support_message_uploads` as checked-in legacy BIGINT DDL/migration 008. Its response mapping uses numeric UserSummary IDs, all messages ordered by `created_at ASC, id ASC`, ordered asset links, and owner/course/role-purpose/UPLOADED filters. The live database/migration state is not verified.
- API #48 is the closest detail-route pattern: shared MENTOR guard, raw path string with int64 OpenAPI metadata, signed-int64 parser mapping malformed values to catalog 404, query by ID, then direct-owner authorization. API #55 follows the same missing-versus-owner outcome shape.
- `error_response` defaults error `data` to JSON null. Shared `MENTOR` guard, response helpers, `query_one`/`query_many`, and middleware route-template support are available.
- Focused API #59 tests: 13 passed. Current full Study suite after implementation: 563 passed with one upstream Starlette/httpx deprecation warning.

## SOURCE_TRACE

```text
GET /api/v1/mentor/support/{request_id}
  -> shared MENTOR JWT guard
  -> strict signed-int64 path parser
  -> SELECT request/course/student by request ID with LEFT JOIN integrity projections
  -> 404 if missing; 403 if present but course is not directly owned
  -> SELECT that request's ordered messages and scoped UploadAsset links
  -> validate reusable SupportRequest projection
  -> 200 DESIGN_RESOURCE_RETRIEVED / catalog 401,403,404,500
  -> focused HTTP tests, context updates and OpenAPI
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Planned behavior |
|---|---|---|---|
| Physical support schema and int64 IDs | API #59 DD predates #58; current local API #58 source adds the matching legacy BIGINT support tables, but no live DB proof exists. | `RESOLVED_FOR_LOCAL_IMPLEMENTATION — DERIVED` | Query the three API #58 tables plus `courses`, `users`, and existing `uploads`; preserve int64 IDs. |
| Mentor scope | AC-24 requires Mentor scope; #58 and current Mentor APIs use numeric subject plus direct `courses.mentor_id`. | `DERIVED_FROM_CURRENT_LOCAL_CONTRACT` | Reuse shared MENTOR guard and direct owner predicate for both request and message queries. |
| Missing vs other owner | Catalog includes both 404 and 403; #48/#55 return 404 when absent and 403 for a present resource with a different direct owner. | `DERIVED_FROM_API_PATTERN` | Keep that order; query by ID, then check owner. |
| Message order, bound, and visibility | #58 local schema has no internal/private flag; #58 explicitly returns the full chronological thread. No page/limit exists in #59 contract. | `DERIVED_FROM_API58` | Return all stored messages ordered `created_at ASC, id ASC`; empty thread is `[]`. No internal-message class exists in selected schema. |
| User and attachment projection | #58 models and link rules already map numeric users and `support_message_uploads` to API #34 uploads. | `DERIVED_FROM_API58` | Reuse models and identical owner/course/role-purpose/UPLOADED checks; do not expose partial/broken assets. |
| Nullability | #58 current response model omits nullable fields when null. | `DERIVED_FROM_CURRENT_RUNTIME` | Omit `avatar_url` and `resolved_at` when null. |
| Malformed/overflow path | #59 catalog excludes 422; #48 path parser maps malformed/out-of-range values to 404. | `DERIVED_FROM_API48` | Return 404 `DESIGN_RESOURCE_NOT_FOUND`; preserve the exact #59 catalog error set. |
| Live schema/deployment | Only checked-in legacy DDL/migration is available. | `NOT_VERIFIED_HERE` | Do not apply migration or claim live DB behavior. |

## IMPLEMENTATION_PLAN

1. Before runtime edits, update API #59 DD sheets/reports to record the inherited API #58 schema and explicitly mark local choices as DERIVED: numeric BIGINT IDs, direct course ownership, 404 missing versus 403 other owner, full messages ordered ascending by timestamp/ID, empty `messages: []`, no internal-message flag in the selected schema, constrained UploadAsset projection, omit nullable fields, and malformed path → catalog 404. Keep the API contract path/success/error set unchanged and DD status `Draft — Needs Confirmation`.
2. Add `app/modules/mentor/api_59_mentor_support_request_detail/` with: response envelope reusing API #58 `SupportRequestResponse`; strict signed-int64 path parser in `validate.py`; SQL constants only in `query.py`; a `view.py` orchestrator for shared MENTOR auth, request lookup, 404/403 ordering, bulk thread/asset mapping, safe 500/rollback and read-only response.
3. SQL Q1 reads one request with LEFT JOINs to `courses` and Student `users` so missing required parents become integrity errors, while retaining request ID lookup. SQL Q2 reads only that request's messages and links, repeats direct owner scope, constrains uploads exactly as API #58, and orders assets by `asset_position` after message chronology.
4. Add a thin `GET /mentor/support/{request_id}` route using raw path text plus int64 OpenAPI metadata so malformed/overflow values can map to the catalog 404. Add the exact route template to `DESIGN_CONTRACT_PATHS`.
5. Add focused TestClient tests for 401/403 role, invalid/missing ID 404, other-owner 403, complete SupportRequest/thread/asset mapping, stable ordering, empty thread, broken relations/links, safe DB failures, trace/no commit, and OpenAPI.
6. Update only server-study context/manifest pages affected by the new route/module/schema reads/test count; keep API #60/#61 code and contracts outside this session.
7. Run focused tests, full Study suite, Ruff, OpenAPI path/operation count, manifest/source checks, `git diff --check`, and context validator. Record repository-baseline validator failures separately; do not apply migration to any live database.

## CHANGES

- Runtime: added API #59 response envelope, signed-int64 parser, SQL-only query constants, Mentor-scoped view and route after the static #58 list route. Added the exact route template to `DESIGN_CONTRACT_PATHS`.
- Tests: added 13 focused TestClient cases for auth-before-DB, malformed/missing IDs, owner denial, request/thread/assets, ordering, empty thread, broken parent/link, safe query failure, read-only transaction, trace and OpenAPI.
- DD: reconciled the eight API #59 sheets and reports with the API #58 fallback; preserved all Excel appendix content and kept status `Draft — Needs Confirmation` with DERIVED/live-schema limits explicit.
- CONTEXT_UPDATES: updated server-study route, architecture, runtime, database/security, module and test pages; added API #59 files/tests to `.agents/context-manifest.json`; refreshed suite/path counts.
- Assumptions: Inherited API #58 local fallback is used as the only support schema for this implementation; it remains DERIVED and unverified in live DB. No migration was applied and no commit was created.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| `deno run -A scripts/select-worklogs.mjs --type coding --limit 3` | 52 matching worklogs; selected and read the three listed worklogs. | `VERIFIED_PREFLIGHT` |
| API #59 DD / #58–#61 linked contract review | API #59 contract and gaps read; linked AC-24 actions and #58 local schema/source reviewed. | `VERIFIED_STATIC` |
| Current API #48/#55 patterns and middleware/auth/response helpers | Detail path behavior, direct owner, error helpers, route wiring and query/view boundaries reviewed. | `VERIFIED_STATIC` |
| `uv run pytest tests/modules/mentor/api_59_mentor_support_request_detail/test_mentor_support_request_detail.py -q` | 13 passed; one upstream Starlette/httpx deprecation warning. | `PASS` |
| `uv run pytest -q` | 563 passed; one upstream Starlette/httpx deprecation warning. | `PASS` |
| `uv run ruff check app tests` | All checks passed. | `PASS` |
| OpenAPI composition | 29 `/api/v1` path templates, 30 operations; `request_id` is integer/int64; success `data` references singleton response envelope. | `PASS` |
| DD front matter/template appendix + manifest path checks | Eight sheets retain DD ID/status; all template appendices match; all six API #59 manifest source paths exist. | `PASS` |
| `git diff --check` | No whitespace errors. | `PASS` |
| `node scripts/validate-agent-context.mjs` | Node is unavailable (`node: command not found`); equivalent Deno invocation was run. | `NOT_RUN_NODE_UNAVAILABLE` |
| `deno run -A scripts/validate-agent-context.mjs` | Fails on pre-existing DB Admin missing context/source entries and broad server-study source drift from the uncommitted workspace. | `BASELINE_FAILURE` |
| `deno run -A scripts/validate-agent-context.mjs --skip-drift` | Remaining errors are DB Admin context/source paths outside this task. | `BASELINE_FAILURE_OUT_OF_SCOPE` |

## HANDOFF

- API #59 local source, focused/full tests, Ruff, OpenAPI, DD appendix/front matter and manifest source checks pass. The global validator cannot pass until unrelated DB Admin context/source paths are restored; full validation also reports existing workspace source drift.
- Live DB schema, migration 008 application, deployed endpoint/authorization and storage URL reachability remain unverified. The support detail policy and schema remain DERIVED pending business-owner review.
- Next API under the continuing one-API-per-session task is #60; no #60 behavior was implemented here.
