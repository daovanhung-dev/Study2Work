---
task_id: "2026-10-25-implement-api56-mentor-submissions-grade"
date: "2026-10-25"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: ["API #55 submission detail -> API #56 grade/status -> API #57 feedback; legacy assignment_submissions/assignments schema"]
status: "PARTIAL"
---

# Worklog: Implement API #56 Mentor submission grade

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run -A scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: 49 matching coding worklogs; 3 selected; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-25/implement-api34-upload-assets.md`
    - carry_forward: Upload metadata is stored in the legacy BIGINT `uploads` artifact; keep owner/purpose/course filters; checked-in DDL does not prove live database or object storage.
  - path: `.agents/worklog/2026-10-25/implement-api47-mentor-lectures.md`
    - carry_forward: Use the shared explicit MENTOR guard, SQL-only query constants, Vietnamese comments/docstrings, caller-owned transaction, and do not claim live schema.
  - path: `.agents/worklog/2026-10-25/implement-api48-mentor-lecture-detail.md`
    - carry_forward: Parse raw signed-int64 paths in the view when catalog errors exclude 422; keep current source above stale DD, preserve dirty worktree, and distinguish design DDL from live schema.
- supplementary_linked_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-25/implement-api54-mentor-submissions-list.md`
    - carry_forward: The user directed us to provide recommended decisions for the three #54 ambiguities. Current fallback: `Page<Submission>`, page 1/fixed size 20/stable submitted_at DESC + id DESC, and constrained URL/owner/purpose/course asset lookup; all remain DERIVED pending contract-owner approval.
  - path: `.agents/worklog/2026-10-25/implement-api55-mentor-submissions-detail.md`
    - carry_forward: #55 uses the shared MENTOR guard and direct `courses.mentor_id` fallback, returns the reusable Submission shape, and keeps rubric/file relation gaps explicit.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Implement `POST /api/v1/mentor/submissions/{submission_id}/grade` for the AC-23 step after API #55 detail and before API #57 feedback. Success is HTTP 200 `DESIGN_RESOURCE_UPDATED` with `ApiEnvelope<Submission>`; only catalog errors 401/403/404/422/500 are allowed.
- Direct contract: required `submission_id:int64`, `score:int32`, and descriptor `rubric items:string`; the reusable Submission contains `score?:decimal-string`, `status`, `feedback`, and `files:UploadAsset[]` but no rubric field.
- Diagram: AC-23 says the Mentor may grade a submission, API #56 updates grade and `status=GRADED`, then API #57 handles feedback. No rubric persistence, status precondition, retry conflict, score scale or transaction is drawn.
- Infrastructure: legacy `assignment_submissions.score NUMERIC(6,2)` and `.status VARCHAR(20)` plus `assignments.max_score NUMERIC(6,2)` are candidate columns; assignment/user/course FKs are nullable. V1-PILOT rubric/criteria use UUID assessment relations without a supported join to the legacy BIGINT submission.

## CURRENT_BEHAVIOR

- Source/config: No API #56 module, route or `DESIGN_CONTRACT_PATHS` template exists. API #55 detail and API #54 list are wired; API #57 remains a separate DD-only feedback mutation. Shared auth already supports explicit MENTOR and returns a numeric subject. DB helpers do not commit.
- Runnable tests: Before implementation, `uv run pytest --collect-only -q` collected 483 tests; API #56 has no test module.
- Import/wiring baseline: `from app.main import app` succeeds; OpenAPI has 25 `/api/v1` path templates and no grade route.
- Worktree: 175 paths were already dirty at task start; preserve them and inspect only API #56 task paths for new changes.

## SOURCE_TRACE

```text
POST grade route -> Pydantic request + raw int64 path -> shared MENTOR guard -> lock candidate submission and LEFT JOIN assignment/course -> validate direct-owner/integrity/score -> UPDATE score/status -> resolve the same constrained 0/1 UploadAsset as #55 -> validate Submission projection -> commit -> DESIGN_RESOURCE_UPDATED envelope -> TestClient/OpenAPI tests
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Rubric request key/format | Catalog says `rubric items:string!`; no wire spelling, item schema or serialization exists | `DISCREPANCY / SOURCE_REQUIRED` | Fallback plan is required `rubric_items` snake_case and opaque string. Accept it but do not persist or echo it because no physical target or response field is supported; keep DD Draft. |
| Rubric storage | Legacy submission schema has no rubric column/detail relation; V1-PILOT rubric tables do not join this BIGINT model | `SOURCE_REQUIRED` | Do not invent a table, column, or join; persist only score/status shown by AC-23. |
| Score range/type | Request is int32; legacy score/max_score are NUMERIC(6,2); catalog does not define bounds or conversion | `DERIVED` | Use integral exact decimal mapping and fallback `0 <= score <= assignment.max_score`; reject invalid/missing candidate max-score configuration safely. No fractional request or rounding. |
| Mentor access | AC-23 requires course permission; current linked Mentor APIs use numeric subject and direct `courses.mentor_id`; assigned-Mentor relation is absent | `DERIVED / SOURCE_REQUIRED` | Use direct owner and 403, consistent with #54/#55; do not claim assigned-Mentor support. |
| Files | Submission has one legacy `file_url`, while response requires `UploadAsset[]` and no submission FK exists | `DERIVED / SOURCE_REQUIRED` | Reuse #55 exact URL + owner + `SUBMISSION` purpose + course lookup; at most one asset, no match => `[]`. |
| Prior status/regrade | Diagram sets target GRADED; catalog has no 409; no prior-state rule exists | `DERIVED` | Allow repeat grading from any current status; update only score/status and preserve feedback owned by #57. |
| Nullable parent links | Legacy DDL permits null/orphan assignment/course references while diagram/table guide assumes submission relations | `DISCREPANCY` | Detect via LEFT JOIN and return catalog safe 500; live nullability remains unverified. |
| Runtime validation mapping | Middleware matches exact paths and registered FastAPI route templates; dynamic #56 path is absent | `CURRENT_SOURCE_GAP` | Register the route template so malformed bodies and internal errors use `DESIGN_*` codes. |

## IMPLEMENTATION_PLAN

1. Complete the source-priority review: retain AC-23 update order, legacy score/status/max_score candidates and nullable relations, exact catalog request/response/error set, and separate UUID rubric model. Compare #54/#55 upload/access/Submission behavior and #57's feedback ownership. Keep all source gaps classified.
2. Apply the user's simple-fallback instruction explicitly in this worklog and DD: request wire key `rubric_items` is required but opaque and unpersisted; update only legacy score/status; map int score exactly to NUMERIC(6,2), enforce derived `0 <= score <= max_score`, allow repeat grading, preserve feedback, use direct course owner and #55 file lookup.
3. Add an API #56 module. Keep Pydantic models declarative; add request type checks and any derived range helper in `validate.py`; keep `query.py` SQL constants only; make `view.py` own auth, locked source lookup, ownership/integrity checks, update, file lookup, rollback/commit and response mapping.
4. Wire the POST route with raw path parsing but int64 OpenAPI metadata; register `/api/v1/mentor/submissions/{submission_id}/grade` in middleware. Use `SubmissionResponse` from API #54/#55 and preserve optional-field omission. Do not change catalog, diagrams, DB artifacts or API #57 mutation.
5. Add TestClient coverage for success/decimal-string mapping/asset projection, preserving feedback and status target, auth and role before DB access, malformed path, body/type/range errors, missing row, non-owner, null/orphan parents, DB/update/file/commit/mapping failures, trace, rollback/commit, repeat grading and OpenAPI/middleware mapping.
6. Update API #56 Markdown DD and linked API #57 notes only where they state #56 is unwired; update server-study route/runtime/database/security/module/test context and manifest required paths. Preserve template Excel appendix bytes and existing user changes.
7. Run focused and full Study Server TestClient suites, Ruff, app/OpenAPI import checks, DD/link/example/template checks, `git diff --check`, and the registered context validator. Record repository-wide dirty-source/db-admin baseline findings without changing out-of-scope context.

## CHANGES

- Runtime: API #56 module, route and middleware template mapping implemented. DD: API #56 documents updated; linked API #57 stale references corrected.
- CONTEXT_UPDATES: API #56 module/test paths and runtime, route, security, database, module and test context pages updated.
- Context pages to update: `.agents/server-study/AGENTS.md`, `architecture.md`, `apis/declared-routes.md`, `core/runtime.md`, `core/database-security.md`, `database.md`, `modules/README.md`, `tests.md`, and `.agents/context-manifest.json`.
- Assumptions: All undocumented business fallbacks remain DERIVED; rubric is accepted but not persisted. No rubric table/migration, catalog/diagram update, or live database operation was performed.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run -A scripts/select-worklogs.mjs --type coding --limit 3` | 49 matching logs; selected three same-type logs; all three were read. | VERIFIED_PREFLIGHT |
| `cd apps/study-server && uv run python -c 'from app.main import app; ...'` | Import succeeded; 25 API v1 path templates; grade route absent. | VERIFIED_BASELINE |
| `cd apps/study-server && uv run pytest --collect-only -q` | 483 tests collected; API #56 module absent. | VERIFIED_BASELINE |
| Focused API #56 TestClient suite | 27 passed; one upstream Starlette/httpx deprecation warning. | VERIFIED |
| Full Study Server suite | 510 passed; same upstream warning. | VERIFIED |
| Ruff: uv run ruff check app tests | All checks passed. | VERIFIED |
| Import/OpenAPI check | App import passed; POST route present; 27 operations / 26 unique path templates; required score int32 and rubric_items string. | VERIFIED |
| DD checks | 11 files; front matter, JSON examples, local links, code fences, whitespace, and 8 Excel appendix suffixes checked. | VERIFIED |
| git diff --check | No diagnostics. | VERIFIED |
| Context validator: deno run -A scripts/validate-agent-context.mjs | Fails on repository baseline: missing db-admin pages/source and broad dirty-source drift. | BASELINE_INVALID |
| Context validator with --skip-drift | Reports only db-admin missing-context/source errors; no server-study API #56 path error. | BASELINE_INVALID |
| Live database/schema/deployment | Not checked. | NOT_VERIFIED |

## HANDOFF

- Remaining questions: rubric persistence/format, assigned-Mentor access, status lifecycle, upload producer compatibility, live schema and transaction behavior remain unresolved by approved sources; fallback code will be marked derived.
- Next owner/action: API #56 local coding, tests, DD and context updates are complete. Keep rubric persistence marked open; proceed to API #57 in the next one-API session.
