---
task_id: "2026-10-25-implement-api61-mentor-support-resolve"
date: "2026-10-25"
primary_task_type: "coding"
secondary_task_types: ["docs", "test"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Implement Study Server API #61 Mentor support resolve

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run -A scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: 54 matching worklogs; selected and read all three; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-25/implement-api34-upload-assets.md`
    - carry_forward: UploadAsset IDs are numeric BIGINT locally; Mentor LECTURE files bind to direct course ownership; live DB/Object Storage are unverified.
  - path: `.agents/worklog/2026-10-25/implement-api47-mentor-lectures.md`
    - carry_forward: SQL constants stay in query.py; caller owns transaction; resolve ordered unique int64 asset refs without weakening owner/purpose scope.
  - path: `.agents/worklog/2026-10-25/implement-api48-mentor-lecture-detail.md`
    - carry_forward: Trace API caller/callee and linked writes; response projections validate before commit; preserve local DDL versus live-schema boundary.
- related_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-25/implement-api60-mentor-support-reply.md`
    - carry_forward: #60 locks the BIGINT request row, uses numeric Mentor JWT `sub` as `courses.mentor_id`, reloads the full thread with the shared projection, and commits only after response validation; fake DB tests do not prove live schema.
  - path: `.agents/worklog/2026-10-25/implement-api59-mentor-support-request-detail.md`
    - carry_forward: Reuse the shared SupportRequest/message/UploadAsset projection; missing request is 404, existing other-owner request is 403, and query/helper calls do not own commit.
  - path: `.agents/worklog/2026-10-25/implement-api58.md`
    - carry_forward: User authorized choosing the clearest reasonable fallback for unresolved support schema and scope; local implementation uses numeric BIGINT `support_requests` with `course_id` and direct `courses.mentor_id` scope. This is checked-in local source, not live-schema approval.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Implement API #61 from its current DD/catalog and AC-24 position after #58 list, #59 detail, and #60 reply; keep API #61 as the status-resolution branch.
- Diagram AC-24 sends the YES branch after #60 to PATCH #61 and explicitly updates request status to `RESOLVED`; NO keeps it `OPEN`.
- Catalog #61 directly requires Mentor Bearer JWT, path `request_id:int64`, no body/query, HTTP 200 `DESIGN_RESOURCE_UPDATED`, singleton `ApiEnvelope<SupportRequest>`, and exact errors 401/403/404/422/500.
- Checked-in migration 008 and `DB.sql` define local BIGINT `support_requests(id, course_id, student_id, status, created_at, resolved_at)`, with `OPEN`, `IN_PROGRESS`, `WAITING_LEARNER`, `RESOLVED`, `CANCELLED`; existing #58–#60 source uses the same model. V1-PILOT UUID tickets are incompatible with this catalog and local current source.
- DERIVED fallback selected under the user's instruction: use the same numeric BIGINT request key and direct course-owner scope as #58–#60; resolve any active status (`OPEN`, `IN_PROGRESS`, `WAITING_LEARNER`) to `RESOLVED`; `RESOLVED` is an idempotent success preserving its first `resolved_at`; `CANCELLED` or unknown state returns catalog 422. Set `resolved_at` with DB `CURRENT_TIMESTAMP` once.

## CURRENT_BEHAVIOR (PRE-EDIT)

- API #61 had no route/module/test before this task. Router composed #58 list, #59 detail and #60 reply; middleware design-contract path set lacked `/resolve`.
- #59/#60 use `validate_current_user_request(..., role="MENTOR")`, numeric JWT `sub`, shared `map_support_request` / `append_support_messages`, `query.py` SQL constants, and caller-owned commit/rollback. #60 already has a `FOR UPDATE` request lookup pattern.
- Current shared response model is singleton `SupportRequestResponse` with full chronological messages and scoped UploadAsset projection. `error_response` emits `data: null`; DD's former `{}` concern is stale.
- API #59/#60 focused tests and full suite last passed at 34 and 584 respectively in the #60 worklog; final regression now includes #61 and the current full suite.

## SOURCE_TRACE

```text
PATCH /mentor/support/{request_id}/resolve
  -> shared MENTOR guard (numeric sub)
  -> strict signed-int64 path parser (catalog 422)
  -> SELECT support request/course/student FOR UPDATE
  -> classify 404 / 403 / current status
  -> conditional UPDATE to RESOLVED for active state; no-op for RESOLVED
  -> reuse API #59 owner-scoped thread query + shared response projection
  -> validate full success envelope -> caller-owned commit; rollback on any failure
  -> HTTP route/error/OpenAPI tests
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Physical SupportRequest model and Mentor scope | Legacy V1-PILOT has incompatible UUID `support_tickets`; local checked-in migration 008 and #58–#60 source use BIGINT `support_requests` and direct `courses.mentor_id`. User authorized a reasonable fallback. | `DERIVED_FOR_LOCAL_IMPLEMENTATION` | Reuse existing #58–#60 model/scope; make no DDL or catalog change; live schema remains unverified. |
| Active-state set and retry semantics | AC-24 states only YES→RESOLVED and NO keeps OPEN; local DDL lists three active statuses, RESOLVED and CANCELLED. | `DERIVED` | `OPEN`, `IN_PROGRESS`, `WAITING_LEARNER`→RESOLVED; already RESOLVED succeeds without changing timestamp; CANCELLED/unknown→422. |
| Response and transaction | #59/#60 provide current shared full-thread projection; DB helpers do not commit. | `SOURCE_BACKED_LOCAL_PATTERN` | Lock, mutate, read ordered thread, validate response and commit once. |
| Error data shape | Current `error_response` defaults to `data:null`, contrary to old DD note. | `RESOLVED_FROM_CURRENT_SOURCE` | Use standard helper and document current null behavior. |

## IMPLEMENTATION_PLAN

1. DONE — Review AC-24 diagram → checked-in migration 008/`DB.sql` → API catalog; record the local fallback and keep V1-PILOT UUID divergence visible.
2. DONE — Trace #58–#60 routes, shared Mentor guard, SQL/query/view transaction boundaries, response projection, middleware errors and tests; confirm #61 is not wired.
3. DONE BEFORE RUNTIME EDITS — Reconcile #61 DD to current local source and explicitly label owner/schema/lifecycle/timestamp decisions `DERIVED`; preserve all original template appendices and Draft status.
4. DONE — Implement API #61 module, route, middleware allowlist entry, focused tests, #61 DD/reports, and directly affected server-study context/manifest/worklog. #58–#60 behavior, catalog, diagrams and DDL were not changed for this task.
5. DONE — Review #58–#61 flow and run focused API #59–#61 tests, full Study suite, Ruff, OpenAPI, DD integrity, diff and context validation; live schema limits are recorded.

## CHANGES

- Runtime: added PATCH API #61 with strict path parsing, MENTOR auth, row lock, direct-owner conditional update, active-state transition, idempotent RESOLVED retry, 422 for CANCELLED/unsupported state and full API #59 thread projection. Commit follows successful envelope validation; failures roll back.
- Tests: added 13 HTTP cases covering the three active states, resolved retry, cancelled state, missing/other owner, concurrent conditional miss, malformed/overflow path, auth, projection/query/commit failure and OpenAPI.
- DD: reconciled all eight sheets plus reports; preserved all original template appendices and `Draft — Needs Confirmation`; marked local BIGINT/owner/lifecycle/timestamp decisions DERIVED.
- Context: updated Study route, architecture, runtime, database/security, module and test pages, project source-status and six context-manifest source paths.
- Worktree: preserved unrelated dirty changes; no commit/push, migration apply or live DB operation.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| `deno run -A scripts/select-worklogs.mjs --type coding --limit 3` | 54 matching; selected three worklogs read. | `VERIFIED_PREFLIGHT` |
| Related-worklog review | Read API #58, #59 and #60 logs; local BIGINT support model and route/projection pattern align. | `VERIFIED_STATIC` |
| Diagram → infra → catalog review | AC-24 YES/NO flow, migration 008/DB.sql BIGINT support schema, API #61 exact route/response/errors reviewed. | `VERIFIED_STATIC` |
| Runtime trace | Before edits, #58–#60 routes and MENTOR guard, DB SQL/helpers, transaction behavior, shared projection, middleware and tests were reviewed; #61 route was absent. | `VERIFIED_STATIC_PRE_EDIT` |
| `uv run pytest tests/modules/mentor/api_59_mentor_support_request_detail tests/modules/mentor/api_60_mentor_support_reply tests/modules/mentor/api_61_mentor_support_resolve -q` | 47 passed; one upstream Starlette/httpx deprecation warning. | `PASS` |
| `uv run pytest -q` | 597 passed; one upstream Starlette/httpx deprecation warning. | `PASS` |
| Ruff | API #61 module/tests, router and middleware all pass. | `PASS` |
| OpenAPI composition | 31 `/api/v1` path templates, 32 operations; resolve is PATCH with signed-int64 path and no request body. | `PASS` |
| DD appendix/link/JSON checks | Eight appendices byte-match templates; 28 local links and two JSON examples validate; no Markdown fences are unclosed. | `PASS` |
| Context manifest | Six API #61 module/test paths are registered and exist. | `PASS` |
| `git diff --check` | No whitespace errors. | `PASS` |
| `node scripts/validate-agent-context.mjs` | Node executable unavailable in environment. | `NOT_RUN_NODE_UNAVAILABLE` |
| `deno run -A scripts/validate-agent-context.mjs --skip-drift` | Reports pre-existing missing DB Admin context/source paths outside Study. | `BASELINE_FAILURE_OUT_OF_SCOPE` |
| `deno run -A scripts/validate-agent-context.mjs` | Reports broad tracked-source drift in the already dirty workspace, including local implementation changes, plus missing DB Admin context; no validator repair outside API #61 scope. | `BASELINE_FAILURE_WORKTREE_DRIFT` |

## HANDOFF

- Remaining boundaries: #61 lifecycle/identity/schema choices are DERIVED; live database, migration deployment and real PostgreSQL concurrency are not verified. API #58 cardinality discrepancy remains open.
- Next API under the one-API-per-session objective: #62.
