# Implement Study API #13 avatar upload

## TASK_CLASSIFICATION

```yaml
primary_task_type: coding
secondary_task_types:
  - docs
  - test
project_scopes:
  - server-study
cross_scope_dependencies: []
```

## PRIOR_WORKLOG_REVIEW

Preflight selector: `deno run -A scripts/select-worklogs.mjs --type coding --limit 3`.

Selected and reviewed before implementation:
- `.agents/worklog/2026-10-11/centralize-study-auth-token-helpers.md`
- `.agents/worklog/2026-10-04/study-db-schema-per-transaction-reapply.md`
- `.agents/worklog/2026-09-28/remove-study-apiresponse.md`

Selector reported 30 available coding worklogs and no shortage. Root `AGENTS.md`, `.agents/AGENTS.md`, `.agents/context-map.md`, `.agents/server-study/AGENTS.md`, scope index, worklog README, the API #13 DD packet, and relevant current route/auth/response/middleware/provider/dependency files were reviewed for this task.

## EXPECTED_BEHAVIOR

Implement `POST /api/v1/users/me/avatar` per the approved plan: Student Bearer auth; strict JSON Data URL for PNG/JPEG/WebP; decoded payload <= 5 MiB with MIME/signature agreement; S3-compatible upload at `avatars/{user_id}` using configured process environment and a public URL; `201 ApiEnvelope<AvatarUploadResult>` with only `avatar_url`; no DB access or mutation; safe 500 errors; injectable provider. Update API contract, DD, AC-11, server-study context/manifest, and dependencies/lockfile.

## CURRENT_BEHAVIOR

Before edits, `app/api/v1.py` has no API #13 route and the API #13 module/tests do not exist. API #14 already supplies the shared Student Bearer guard. No object-storage adapter or boto3 dependency exists in Study Server. Worktree was clean at preflight (`develop...origin/develop`).

## TRACE_AND_DISCREPANCIES

- Route registration: `app/api/v1.py` -> module view; use existing router and response envelope conventions.
- Authentication: `app/utils/auth.py::validate_current_user_request`, already used by API #14.
- Request validation: module validator plus canonical middleware mapping for 422.
- Storage side effect: new injectable S3 adapter only; API #13 must not invoke DB/query code.
- Expected/current discrepancy: API #13 DD is an unresolved draft with gaps; the user's approved choices resolve input format, MIME set, size limit, storage configuration/key, timeout/retry, and response shape for this task.

## IMPLEMENTATION

- Added API #13 request/result models, Data URL/Base64/MIME/signature/decoded-size validation, route and view using the shared Student guard.
- Added a lazy S3-compatible provider with process-environment configuration, fixed per-user object key, public URL mapping and one-attempt timeout config; no DB dependency.
- Added boto3 to `pyproject.toml` and regenerated `uv.lock`.
- Added parser, route, storage failure, missing configuration, no-DB and S3 Stubber tests. The first focused run passed 25 tests; one exact 5 MiB boundary test was added afterward and will be included in final verification.
- Updated API list contract, AC-11 response type, API #13 DD packet, `.env.example`, server-study architecture/routes/modules/tests/source-status pages and context manifest.

## VERIFICATION

- `uv run pytest -q`: `217 passed, 1 warning` (Starlette deprecation from TestClient/httpx).
- `uv run ruff check app tests`: `All checks passed`; Ruff format check passes for all 7 changed Python files in scope.
- `uv run mypy app/modules/guest/api_13_users_me_avatar app/service/object_storage/avatar.py tests/modules/guest/api_13_users_me_avatar`: pass, 6 source files.
- Full `uv run mypy app tests`: 124 errors across 16 files outside API #13; no API #13 errors remain. Full-repository `ruff format --check` also reports 19 out-of-scope files; changed files are formatted.
- Route/import/OpenAPI check: 13 router routes; API #13 path exists in router and OpenAPI.
- DD check: relative links, JSON examples and Markdown table widths pass.
- `node scripts/validate-agent-context.mjs`: reports pre-existing `db-admin` context/source missing from this checkout plus manifest source drift. `--skip-drift` still reports only the missing `db-admin` context/source. No `db-admin` files were changed.
- `git diff --check`: pass.

No external storage call, credential verification, or deployment was performed, as scoped.

## CONTEXT_UPDATES

- Updated source-backed server-study pages and required source paths in `.agents/context-manifest.json`; test count and route status reflect final local verification. The context validator remains blocked by unrelated `db-admin` gaps and existing manifest drift.
