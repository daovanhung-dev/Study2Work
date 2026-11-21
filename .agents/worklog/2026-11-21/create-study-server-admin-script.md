---
task_id: "2026-11-21-create-study-server-admin-script"
date: "2026-11-21"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "COMPLETE"
---

# Worklog: Create Study Server Admin account CLI

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `node scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: `READY`; 162 available; 3 selected; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-21/commit-admin-ad-screens.md`
    - carry_forward: Preserve workspace state; prior screen commits do not establish live database/deployment state.
  - path: `.agents/worklog/2026-11-21/complete-ad01-ad25-dd-safe.md`
    - carry_forward: Admin authorization currently uses role `ADMIN`; live DB/schema and deployment remain unverified.
  - path: `.agents/worklog/2026-11-21/complete-gs01-gs07-dd-safe.md`
    - carry_forward: Use current source and scope context; report only checks actually run; retain database/runtime boundary.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Provide an operator-run CLI that creates an active Admin account in a specifically configured Study Server PostgreSQL schema.
- Decisions: hidden password prompt and confirmation; reject duplicate email without promoting/resetting existing users; require explicit DB URL/schema/environment; block production unless explicitly enabled and separately confirmed.
- No public API, DB schema, or migration change.

## CURRENT_BEHAVIOR

- `users` has BIGSERIAL ID, unique email, password hash, role, and status; the API #01 registration flow normalizes email, trims and limits full name to 150 characters, hashes with Argon2id, and creates `STUDENT`.
- `get_settings()` builds from static constants; it does not load environment or `.env`. `build_engine(Settings)` applies validated configured schema search path. Reuse `hash_password` and `normalize_email`; do not use `get_engine()` or print the default database URL.
- Existing seed scripts are destructive/upsert-oriented test data and are not suitable for administrator bootstrap.

## SOURCE_TRACE

```text
CLI -> explicit target settings -> build_engine/schema search_path -> Session transaction -> duplicate check -> bound INSERT(role=ADMIN,status=ACTIVE) -> commit -> report id/email only
```

## IMPLEMENTATION_PLAN

- Add `apps/study-server/scripts/create_admin.py`, requiring `STUDY_ADMIN_DATABASE_URL`, `STUDY_ADMIN_DB_SCHEMA`, and `STUDY_ADMIN_APP_ENV`; construct explicit `Settings` and engine without the cached default configuration.
- Prompt for name/email and hidden password twice, reuse current email normalization and Argon2id hashing, and enforce current name/password rules without inventing a new password policy.
- Display the credential-redacted target and require confirmation; production additionally requires `--allow-production` plus typed confirmation. Reject existing email and rollback on DB/constraint errors.
- Add focused script tests and README instructions, run focused pytest/Ruff and scoped diff/context validation.

## TARGET_UPDATES

| Target | From → to | Evidence / reason |
|---|---:|---|
| `Tạo script bootstrap tài khoản Admin cho Study Server` | `0% → 0%` | Initial state; acceptance requires safe target selection, hashed password, uniqueness handling, production protection and verification. |
| `Tạo script bootstrap tài khoản Admin cho Study Server` | `0% → 100%` | CLI, explicit target validation, hidden password confirmation, duplicate/race handling, production gate, README guidance and 17 focused tests implemented; Ruff and CLI help checks pass. No live database account was created. |

## VERIFICATION

- `uv run pytest -q tests/scripts/test_create_admin.py`: 17 passed; one existing Starlette/httpx deprecation warning.
- `uv run ruff check scripts/create_admin.py scripts/__init__.py tests/scripts/test_create_admin.py`: all checks passed.
- `uv run python scripts/create_admin.py --help`: exit 0; CLI exposes only the explicit `--allow-production` flag, with account credentials remaining prompt-only.
- `git diff --check --` on the script, tests, README, worklog and tracker paths: exit 0.
- No live database was contacted for account creation; target inspection/insert behavior is covered with fake sessions.

## CHANGES

- Added the explicit-configuration Admin bootstrap CLI and namespace package marker under `apps/study-server/scripts/`.
- Added unit coverage for missing/non-PostgreSQL config, production gate and typed phrase, credential-redacted target display, input normalization/hash, active Admin insert, duplicate rejection and schema mismatch.
- Added README instructions for operator configuration and use.

## HANDOFF

- Operator must supply the three `STUDY_ADMIN_*` environment variables and run the script interactively. Production requires `--allow-production` and the production confirmation phrase.
- The script does not create an account during tests or implementation; live schema/deployment remains unverified.
