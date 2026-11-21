---
task_id: "2026-10-25-implement-api50-mentor-content-create"
date: "2026-10-25"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Implement API #50 Mentor content create

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run -A scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: `available: 44`, `selected: 3`, `status: READY`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-25/implement-api34-upload-assets.md`
    - carry_forward: API #34 uses injectable storage and scoped upload metadata; local DDL and fake providers do not prove production storage or live DB behavior.
  - path: `.agents/worklog/2026-10-25/implement-api47-mentor-lectures.md`
    - carry_forward: Mentor APIs use the shared role guard, direct `courses.mentor_id` ownership and caller-owned transaction; keep SQL as constants and execution in `view.py`.
  - path: `.agents/worklog/2026-10-25/implement-api48-mentor-lecture-detail.md`
    - carry_forward: API #48 reads a legacy BIGINT lecture projection and ordered upload links; it does not define generic Content persistence or lifecycle.
- shortage: `none` (44 coding logs available; selector returned three)
- additional related context reviewed: `.agents/worklog/2026-10-25/implement-api49-mentor-content-list.md` for the adjacent Content tree contract and local `contents` mapping.

## EXPECTED_BEHAVIOR

- Requirement: Implement the next endpoint in the active Study Server API sequence, API #50, while preserving unrelated pre-existing worktree changes.
- Canonical contract: `POST /api/v1/mentor/content`; Bearer JWT, Mentor role; body `{course_id:int64!, content_type:ContentType!, title:string!, payload:object!}`; HTTP 201 `DESIGN_RESOURCE_CREATED`; `ApiEnvelope<Content>`; declared errors are 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 422 `DESIGN_VALIDATION_ERROR`, and 500 `DESIGN_INTERNAL_ERROR`.
- AC-22 says the Mentor must manage the course and the flow inserts Content before the client reloads the tree. Do not add a 404 code or request fields absent from the catalog.

## CURRENT_BEHAVIOR

- Source/config: API #50 route/module is composed; request fields use strict types and reject extras; shared auth requires `MENTOR`; local legacy `contents` DDL/migration 006 provides BIGINT IDs, JSONB object payload, open text type/status, parent/order and soft-delete fields. API #50 uses a derived direct-owner rule, absent/non-owned course → 403, initial `PENDING_REVIEW`, root placement and zero-based next active-root order. Live schema and migration deployment are unverified.
- Runnable tests: Focused API #50 suite passes 25 tests; full Study suite passes 381 tests. Test DB queries are fakes.
- Runtime wiring: `POST /api/v1/mentor/content` is in `app/api/v1.py` and `DESIGN_CONTRACT_PATHS`; the composed app exposes 21 `/api/v1` OpenAPI paths.

## SOURCE_TRACE

```text
POST /api/v1/mentor/content
  -> strict request model + shared MENTOR guard
  -> lock course row and compare numeric JWT subject with courses.mentor_id
  -> allocate non-negative active-root order
  -> INSERT contents with JSONB payload, root parent and PENDING_REVIEW
  -> validate RETURNING projection, commit in view, return 201 Content envelope
  -> TestClient verifies auth/validation/access/transaction/trace/OpenAPI
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Initial status, root placement and order | AC-33 queue reads `PENDING_REVIEW`; body has no parent/order; current code creates root and allocates non-negative order starting at 0. | `DERIVED` | Behavior is implemented locally and documented; product confirmation remains open. |
| Course authorization | Current Mentor APIs and legacy schema support direct `courses.mentor_id`; no assignment relation is source-backed. | `DERIVED_FROM_CURRENT_STUDY_PATTERN` | Local implementation grants direct owner only; assigned/co-managing Mentor policy remains open. |
| Missing course mapping | Catalog #50 has no 404; implementation maps missing/non-owned to 403. | `DERIVED` | Uses only declared status/code; product semantics remain open. |
| Type/payload contract | Catalog has `ContentType` and object payload but no enum members or subtype schema. | `SOURCE_REQUIRED` | Keep type open string and validate only JSON object shape. |
| Live schema | Local DDL/migration 006 exists; no live metadata or migration deployment was checked. | `NOT_VERIFIED_HERE` | Local tests/source do not establish production availability. |
| Context validator | Full validation reports missing DB Admin context/source and repository snapshot drift; `--skip-drift` leaves DB Admin baseline findings only. | `BLOCKED_BY_REPOSITORY_BASELINE` | No out-of-scope DB Admin changes made; no API #50 missing-source/page finding in skip-drift output. |

## CHANGES

- Files changed for API #50: `app/api/v1.py`, `app/core/middleware.py`, `app/modules/mentor/api_50_mentor_content_create/*`, focused TestClient tests, API #50 DD Markdown, and server-study context/manifest/worklog pages.
- Runtime: Added a thin HTTP 201 route, strict request/envelope models, SQL-only course lock/order/insert statements, Mentor access/transaction/response orchestration and error mapping. Root-order allocation clamps the next value to zero for legacy negative root orders.
- DD: Recorded derived status/root/order/access choices and preserved `Draft — Needs Confirmation`; refreshed verification and AC-22/AC-33 macro-review evidence. No new schema artifact was added in this task.
- CONTEXT_UPDATES: Updated `.agents/context-manifest.json` source/test paths and server-study architecture, routes, runtime, DB/security, database, modules, and test pages.
- Assumptions: `PENDING_REVIEW`, root placement/order and 403 for absent course are explicit derived implementation decisions, not product-approved rules. Live DB/schema, migration, assignment access, type/status enums and payload subtype remain unverified/open.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run -A scripts/select-worklogs.mjs --type coding --limit 3` | Found 44 same-type logs; selected API #34/#47/#48 worklogs, all read. | VERIFIED |
| API #50 focused tests | `uv run pytest -q tests/modules/mentor/api_50_mentor_content_create/test_mentor_content_create.py` — 25 passed; one upstream Starlette/httpx deprecation warning. | VERIFIED |
| Full Study Server tests | `uv run pytest -q` — 381 passed; same warning. | VERIFIED |
| Ruff | `uv run ruff check app tests` — all checks passed. | VERIFIED |
| Import/OpenAPI | `uv run python3 -c 'from app.main import app; paths=[p for p in app.openapi()["paths"] if p.startswith("/api/v1/")]; print(f"api_v1_paths={len(paths)}"); print("api50_present=" + str("/api/v1/mentor/content" in paths)); assert "/api/v1/mentor/content" in paths'` — 21 paths and API #50 route present; int64 schema covered by focused test. | VERIFIED |
| Manifest JSON | `python3 -m json.tool .agents/context-manifest.json` — parses. | VERIFIED |
| `git diff --check` | No diagnostics. | VERIFIED |
| Context validator | `deno run -A scripts/validate-agent-context.mjs` fails on repository DB Admin context/source gaps and snapshot drift; `--skip-drift` reports DB Admin baseline only, with no API #50 required-source/page finding. | BLOCKED_BY_REPOSITORY_BASELINE |

## HANDOFF

- Remaining blockers: Product confirmation for DERIVED defaults and course policy; authoritative live schema/migration status; Content enum/payload/version and moderation lifecycle rules. Repository-wide context validator remains invalid due unrelated DB Admin baseline gaps.
- Next owner/action: Continue the active API sequence with API #51 in a separate coding session, preserving this worktree and the explicit local/live verification boundary.
