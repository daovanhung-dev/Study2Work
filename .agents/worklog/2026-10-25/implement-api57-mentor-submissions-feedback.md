---
task_id: "2026-10-25-implement-api57-mentor-submissions-feedback"
date: "2026-10-25"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: ["API #56 grade/status -> API #57 feedback; API #54/#55 Submission/file projection; legacy assignment_submissions"]
status: "PARTIAL"
---

# Worklog: Implement API #57 Mentor submission feedback

## PRIOR_WORKLOG_REVIEW

- primary_task_type: coding
- selector_command: deno run -A scripts/select-worklogs.mjs --type coding --limit 3
- selector_result: 50 matching coding worklogs; 3 selected; no shortage.
- prior_worklogs_reviewed:
  - path: .agents/worklog/2026-10-25/implement-api34-upload-assets.md
    - carry_forward: preserve scoped upload owner/purpose/course checks; fake DB/source do not prove live schema or object storage.
  - path: .agents/worklog/2026-10-25/implement-api47-mentor-lectures.md
    - carry_forward: shared MENTOR guard, SQL-only query constants, Vietnamese comments/docstrings, caller-owned transaction and live-schema boundary.
  - path: .agents/worklog/2026-10-25/implement-api48-mentor-lecture-detail.md
    - carry_forward: preserve AC-linked producer/consumer review, explicit relation evidence, local DDL versus live schema distinction, and dirty worktree changes.
- shortage: none

## EXPECTED_BEHAVIOR

- Requirement: Implement `POST /api/v1/mentor/submissions/{submission_id}/feedback` for the AC-23 Mentor feedback step after API #56 grade/status.
- Canonical contract: Catalog success is HTTP 200 `DESIGN_RESOURCE_UPDATED` with `ApiEnvelope<Submission>`; allowed errors are 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 422 `DESIGN_VALIDATION_ERROR`, and 500 `DESIGN_INTERNAL_ERROR`. Path is `submission_id:int64!`; body descriptors are `feedback text:string!` and `attachments:string!`. AC-23 says the Mentor with course permission saves feedback after grade, and the response is the updated Submission. The database table guide and legacy DDL expose `assignment_submissions.feedback TEXT NULL`, but no feedback attachment relation. DD #57 remains Draft — Needs Confirmation and identifies wire keys, attachment storage, repeat-call/history, owner identity and status timing as unresolved.
- User clarification carried forward for linked API #54: user asked the agent to provide recommended decisions for `data` cardinality, file association and pagination. Current fallback is a `Submission[]` page, fixed size 20/default page 1, order `submitted_at DESC, id DESC`, and `UploadAsset[]` resolution by exact URL + owner + `SUBMISSION` purpose + course. These remain DERIVED; the reply is not treated as contract-owner approval of the exact values.

## CURRENT_BEHAVIOR

- Source/config: API #54–56 routes were the source baseline; #54 owns reusable `SubmissionResponse`, while #55–56 reuse it and constrain the one legacy `file_url` lookup by asset URL, owner, purpose and course. API #56 locks `assignment_submissions`, LEFT JOINs assignment/course to detect null/orphan relations, checks direct `courses.mentor_id`, updates only score/status, preserves feedback, and owns rollback/commit in `view.py`. `query.py` contains static SQL only. Shared auth checks Bearer JWT, numeric subject and explicit `MENTOR` role. DB helpers do not commit. Middleware uses `DESIGN_CONTRACT_PATHS`; the #57 route was absent at baseline and is now registered.
- Runnable tests: API #56 TestClient suite covers shared Mentor auth, ownership, lock/update, scoped asset projection, transaction and errors; its worklog recorded 27 focused/510 full-suite passes before this API. API #57 now has 28 focused tests; current full Study suite has 538 passes.
- Runtime wiring: API #57 now imports/wires through `app/api/v1.py`, uses the reusable API #54 response, and is classified by the dynamic `DESIGN_CONTRACT_PATHS` template. `error_response` serializes omitted `data` as JSON `null`.

## SOURCE_TRACE

~~~text
POST route -> strict FeedbackSubmissionRequest + signed-int64 path validation -> shared MENTOR Bearer/role guard -> SELECT submission/assignment/course FOR UPDATE -> direct-owner and relation-integrity checks -> UPDATE only assignment_submissions.feedback with repeated owner predicate -> constrained UploadAsset lookup using the #54/#55 contract -> reusable SubmissionResponse validation -> commit -> DESIGN_RESOURCE_UPDATED envelope; failures rollback -> API #57 TestClient/OpenAPI/middleware checks
~~~

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| `feedback text` wire key | Catalog descriptor has no JSON spelling; DD OPEN_QUESTIONS marks it unresolved | `DERIVED` | Use required strict `feedback_text` snake_case; do not trim or impose length/non-empty rules absent source evidence. |
| `attachments` representation and persistence | Catalog declares required string; AC-23 gives no format; legacy DDL/table guide show no target relation; response Submission has no attachment field | `SOURCE_REQUIRED / DISCREPANCY` | Accept required strict opaque string but do not persist, echo or map it to `file_url`/`Submission.files`; keep DD Draft and limitation explicit. |
| Update versus history insert | AC-23 diagram says INSERT/UPDATE; only candidate legacy `feedback` field exists and no history relation/semantics are approved | `DERIVED / SOURCE_REQUIRED` | Use a single-column UPDATE overwrite; do not invent a history table or an undocumented 409. |
| Mentor authorization relation | AC-23 says course permission; linked #54–56 use numeric JWT subject and direct `courses.mentor_id`; no assigned-Mentor join is evidenced | `DERIVED / SOURCE_REQUIRED` | Apply shared MENTOR guard plus direct course owner predicate; assigned-Mentor access remains unsupported. |
| Status timing and score ownership | AC-23 UI sequence puts grade before feedback, but DD/catalog give no direct-call precondition | `DERIVED` | Do not require `status=GRADED`; preserve existing score/status and update feedback only. |
| Nullable/orphan assignment/course references | Legacy DDL allows nullable assignment FK; API #55–56 use LEFT JOIN to distinguish broken parent links | `DISCREPANCY` | Missing submission returns 404; broken parent/owner projection returns safe 500; owner mismatch returns 403. Live nullability is unverified. |
| Asset collection projection | `Submission.files` exists in catalog; legacy submission stores one `file_url`, no FK; #54–56 use URL/owner/purpose/course constrained lookup | `DERIVED / SOURCE_REQUIRED` | Reuse same zero-or-one student UploadAsset projection; do not conflate it with request `attachments`. |
| Request path/body error routing | Catalog includes 422 and middleware only classifies registered design path templates | `CURRENT_SOURCE_GAP` | Validate signed-int64 path/body as 422; register `/api/v1/mentor/submissions/{submission_id}/feedback` so errors use `DESIGN_*`. |

## IMPLEMENTATION_PLAN

1. Implement the catalog path, body and response shape: raw path declared with OpenAPI int64 metadata and checked as signed int64; strict required JSON keys `feedback_text` and `attachments`; response envelope wraps the existing reusable `SubmissionResponse` and emits only the supported error codes.
2. Keep layering consistent: request/response Pydantic models in API #57 `models.py`, SQL text constants only in `query.py`, and auth, DB calls, integrity checks, response projection, rollback and commit in `view.py`; use a small `validate.py` helper for signed-int64 parsing if needed.
3. In the view, authenticate Bearer/numeric subject/MENTOR before DB access; lock the submission and LEFT JOIN assignment/course; map absent row to 404, broken candidate keys/relations to safe 500 and a different direct owner to 403. Preserve current score/status.
4. Update only `assignment_submissions.feedback`; repeat direct-owner predicate in the UPDATE; return the row; overwrite the existing field for repeated calls. Do not persist request `attachments`, create history, require GRADED, or return a new error code.
5. Reuse the #54 `SubmissionResponse`; when `file_url` exists, look up at most one upload with exact URL, submission owner, `SUBMISSION` purpose and parent course. No match yields `files: []`; validate the full projection before committing.
6. Make the view own the write transaction: rollback on query, authorization, mapping or commit failure; commit once only after the update and Submission projection validate. Return HTTP 200 `DESIGN_RESOURCE_UPDATED`.
7. Wire the POST route and register its dynamic template in `DESIGN_CONTRACT_PATHS`; add focused TestClient coverage for success, opaque attachments not leaking, auth-before-DB, malformed path/body, missing/non-owner/broken relations, preserved score/status, update predicates, scoped file lookup, DB/mapping/commit failures, rollback/commit, trace and OpenAPI.
8. Update API #57 DD sheets/reports and Study Server context/manifest to describe the implemented DERIVED fallback while retaining `Draft — Needs Confirmation`, unresolved attachment/history/identity questions, and the live-schema boundary. Do not modify diagram, catalog or DDL because their evidence does not resolve these choices.
9. Run focused and full Study Server tests, Ruff, app/OpenAPI checks, DD integrity checks, `git diff --check`, and the agent-context validator. Record validator baseline errors separately; do not alter unrelated DB Admin context or clean/stage/commit the existing dirty worktree.

## CHANGES

- Files changed: Added `apps/study-server/app/modules/mentor/api_57_mentor_submissions_feedback/{__init__.py,models.py,query.py,validate.py,view.py}`, wired `app/api/v1.py` and `app/core/middleware.py`, added `tests/modules/mentor/api_57_mentor_submissions_feedback/test_mentor_submission_feedback.py`, updated the 11 API #57 DD Markdown artifacts, and updated server-study context pages plus `.agents/context-manifest.json`.
- CONTEXT_UPDATES: Recorded API #57 route, transaction, auth, database candidate and test behavior; added all new source/test paths to the manifest. Existing DB Admin context/source omissions and unrelated dirty-source drift remain unchanged.
- Assumptions: User instructed the agent to provide recommended decisions for API #54's three ambiguities; current Page<Submission>/pagination/file lookup values remain DERIVED rather than approved. API #57 `feedback_text` wire key, direct-owner identity, overwrite semantics and accepted-but-unused attachments remain DERIVED/SOURCE_REQUIRED. Attachments are not stored or returned; no new table, column, status or business code was introduced.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| deno run -A scripts/select-worklogs.mjs --type coding --limit 3 | 50 matching; selected and read all three same-type worklogs. | VERIFIED_PREFLIGHT |
| Exact API #54–56 source, API #57 DD, AC-23, table guide, catalog, legacy DDL and middleware review | Confirmed shared Submission response, direct-owner scope, transaction ownership and no feedback-attachment target; see evidence sections above. | VERIFIED_SOURCE_REVIEW |
| `cd apps/study-server && uv run pytest tests/modules/mentor/api_57_mentor_submissions_feedback/test_mentor_submission_feedback.py -q` | 28 passed; one upstream Starlette/httpx deprecation warning. | VERIFIED |
| `cd apps/study-server && uv run pytest -q` | 538 passed; one upstream Starlette/httpx deprecation warning. | VERIFIED |
| `cd apps/study-server && uv run ruff check app tests` | All checks passed. | VERIFIED |
| App import/OpenAPI | API #57 route present; `submission_id` format int64; 27 `/api/v1` path templates. | VERIFIED |
| API #57 DD integrity checks | 11 files; front matter/status, fences, JSON examples and local links passed. | VERIFIED |
| `git diff --check` | Passed after final context/report/worklog edits. | VERIFIED |
| `deno run -A scripts/validate-agent-context.mjs` | Fails on pre-existing missing DB Admin context/source and broad dirty-source drift; no API #57 path error observed. | BASELINE_INVALID |
| `deno run -A scripts/validate-agent-context.mjs --skip-drift` | Reports only existing missing DB Admin context/source errors. | BASELINE_INVALID |
| Live database/schema/deployment | Not checked. | NOT_VERIFIED |

## HANDOFF

- Remaining blockers: Contract owner has not approved API #57's wire key, attachment storage/format, update/history semantics or identity mapping; current fallback is local-only and attachments are not persisted.
- Next owner/action: API #57 local implementation, tests, DD and context updates are complete. Keep this multi-API goal active for API #58 next; live schema, migration/deployment, client and AC-23 end-to-end behavior remain unverified.
