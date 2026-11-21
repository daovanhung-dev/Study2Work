---
task_id: "2026-10-25-implement-api34-upload-assets"
date: "2026-10-25"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "COMPLETE"
---

# Worklog: Implement API #34 UploadAsset

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type coding --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-25/remove-errordetail-study-server.md`
    - carry_forward: Preserve Study HTTP errors through `error_response`; do not use built-in `ValueError`; record repository validator baseline separately from API behavior.
  - path: `.agents/worklog/2026-10-25/reuse-jwt-role-guard.md`
    - carry_forward: Use the shared auth facade; preserve all existing role/error behavior and API #46's internal error message while extending the guard for API #34's accepted-role set.
  - path: `.agents/worklog/2026-10-24/api46-mentor-courses.md`
    - carry_forward: Legacy numeric identity and direct `courses.mentor_id` ownership are the approved Mentor pattern; local DDL does not prove live schema.
- shortage: `none` (selector found 37 coding logs and selected 3)

## EXPECTED_BEHAVIOR

- Requirement: Implement `POST /api/v1/uploads` for multipart binary upload and durable `UploadAsset` metadata, supporting `SUBMISSION`/Student and `LECTURE`/Mentor. Mentor lecture uploads require an owned legacy course; a Student-supplied course must have an `ACTIVE` enrollment. Store public URLs, actual byte count and status `UPLOADED`; compensate an object upload if metadata persistence fails.
- Canonical contract/approved decisions: Catalog API #34 statuses 201/401/403/422/503/500; fields `file`, `purpose`, optional `course_id`; `UploadAsset` response. User approved a legacy BIGINT uploads table, purposes/role pairing, any binary/no MIME or size policy, public URL, `UPLOADED`, Student enrollment checks, and API #47 `asset_refs` as JSON string array (empty allowed, duplicates rejected, order retained). API #47 remains unwired until `content:int64` semantics are confirmed.

## CURRENT_BEHAVIOR

- Source/config: API #34 route/module/test and durable uploads metadata are absent. `python-multipart` is not a direct Study dependency. API #13 has an injectable S3-compatible avatar-only provider with the shared `OBJECT_STORAGE_*` environment names. Shared auth accepts one explicit role. Legacy DDL has `courses`, `enrollments` and `lessons`; live DB metadata is not verified.
- Runnable tests: `.agents/server-study/tests.md` records 276 passing tests in the current tree; not rerun at task start.
- Runtime wiring: `DESIGN_CONTRACT_PATHS` does not contain `/api/v1/uploads`; API #47 has no route/module and remains outside this implementation.

## SOURCE_TRACE

```text
POST /api/v1/uploads -> validate Bearer and accepted role -> validate purpose/course access -> stream to S3-compatible storage -> insert uploads metadata in caller-owned transaction -> cleanup object on DB failure -> UploadAsset envelope
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Durable UploadAsset persistence | No Study uploads table or metadata resolver exists; user approved adding a legacy BIGINT table/migration. | `RESOLVED_BY_USER` | Add source migration/artifact; do not apply it to live DB. |
| API #47 content mapping | `content:int64` meaning remains unresolved by user decision. | `SOURCE_REQUIRED` | Keep API #47 runtime unwired; record only its approved asset-reference contract updates. |
| Live database/storage | Only checked-in DDL and injectable provider source are available; no live probes are requested. | `NOT_VERIFIED_HERE` | Tests and source do not establish deployment or live schema availability. |

## CHANGES

- Files changed: API #34 route/auth/module/storage provider/tests, multipart dependency and lock, legacy `uploads` DDL and migration, API catalog, DD #34/#47, server-study context manifest/pages, and this worklog.
- API #34: Added `POST /api/v1/uploads`, accepts STUDENT/SUBMISSION and MENTOR/LECTURE, validates ACTIVE enrollment or direct course ownership, stores arbitrary file bytes using server-generated UUID keys, persists BIGINT UploadAsset metadata with `UPLOADED`, and best-effort deletes the object after metadata failure.
- API #47: Updated only the approved asset reference contract (JSON string array of ordered int64 IDs; empty allowed; duplicates rejected; same Mentor, `LECTURE`, same course). The route remains `UNWIRED` while `content:int64` semantics remain unresolved.
- CONTEXT_UPDATES: Updated `.agents/context-manifest.json` and the server-study route, architecture, DB/security, database, modules, tests and entry pages. Context validator was run; repository baseline failures are recorded below.
- Assumptions: Server-generated UUID object keys; multipart filename or `upload`; multipart content type or `application/octet-stream`; no client URL or object key is accepted. Migration is checked-in source only; no live DB or Object Storage operation was performed.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `git status --short --branch` | Clean `develop...origin/develop` before task changes. | VERIFIED |
| `deno run --allow-read scripts/select-worklogs.mjs --type coding --limit 3` | Selected and read all three same-type worklogs. | VERIFIED |
| `uv run --group dev pytest tests/modules/api_34_uploads/test_uploads.py -q` | 18 passed; 1 Starlette/httpx deprecation warning. | VERIFIED |
| `uv run --group dev pytest -q` | 294 passed; 1 Starlette/httpx deprecation warning. | VERIFIED |
| `uv run --group dev ruff check app tests` | All checks passed. | VERIFIED |
| `uv lock --check` | Resolved 63 packages; lock is current. | VERIFIED |
| Import/OpenAPI inspection | `/api/v1/uploads` is registered as multipart/form-data; `file` and `purpose` are required, `course_id` optional int64, purpose enum is SUBMISSION/LECTURE. | VERIFIED |
| DD static checks | Required sheets present; 29 relative links resolve; 5 JSON examples parse; no trailing whitespace. | VERIFIED_STATIC_ONLY |
| `git diff --check` | No whitespace errors. | VERIFIED |
| `node scripts/validate-agent-context.mjs` | `AGENT_CONTEXT_INVALID`: missing DB Admin pages/source roots/links and broad pre-existing `CONTEXT_STALE` snapshots. No Study Server-specific missing source path was reported; `--skip-drift` still fails on DB Admin baseline. | BLOCKED_BY_REPOSITORY_BASELINE |
| API #34 contract/DD, API #47 open questions, current auth/DB/router/middleware/storage/dependency/test fixture sources | Read before implementation; source tracing covered route, guard, access queries, Object Storage, transaction, envelope and focused tests. | VERIFIED_STATIC_ONLY |

## HANDOFF

- Remaining blockers: API #47 awaits confirmation of `content:int64` semantics. The repository-wide context validator remains invalid because DB Admin context/source is missing and context snapshots are stale outside this task. Live DB migration and Object Storage behavior are not verified.
- Next owner/action: Before wiring API #47, confirm whether `content:int64` is content or an ID reference, then define the corresponding persistence/resolution contract. Apply `004_uploads.sql` only through the separately approved DB migration workflow.
