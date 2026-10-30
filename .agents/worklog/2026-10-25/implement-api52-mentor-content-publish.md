---
task_id: "2026-10-25-implement-api52-mentor-content-publish"
date: "2026-10-25"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Implement API #52 Mentor Content publish/unpublish

## PRIOR_WORKLOG_REVIEW

- primary_task_type: coding
- selector_command: `deno run -A scripts/select-worklogs.mjs --type coding --limit 3`
- selector result: 45 coding worklogs available; 3 selected; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-25/implement-api34-upload-assets.md`
    - carry_forward: Keep Study SQL in `query.py`, orchestration in `view.py`, and verify ownership/transaction/response projection before commit.
  - path: `.agents/worklog/2026-10-25/implement-api47-mentor-lectures.md`
    - carry_forward: Preserve strict int64 path parsing, shared Mentor authentication and catalog error codes; treat local schema as unverified deployment evidence.
  - path: `.agents/worklog/2026-10-25/implement-api48-mentor-lecture-detail.md`
    - carry_forward: Lock/read resource and owning course together where mutation authorization depends on course ownership; test malformed ID and row projection failures.
  - path: `.agents/worklog/2026-10-25/implement-api49-mentor-content-list.md`
    - carry_forward: Reuse `ContentResponse`; local legacy BIGINT `contents` model is only a source-backed local fallback and V1-PILOT `content_blocks` is incompatible.
  - path: `.agents/worklog/2026-10-25/implement-api50-mentor-content-create.md`
    - carry_forward: The current API #50 proposal creates `PENDING_REVIEW`; direct `courses.mentor_id` ownership remains a DERIVED fallback.
  - path: `.agents/worklog/2026-10-25/implement-api51-mentor-content-update.md`
    - carry_forward: #51 snapshots content revisions and returns the shared Content projection; its lifecycle/version choices remain DERIVED and must not be presented as approved policy.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Implement `PATCH /api/v1/mentor/content/{content_id}/publish`, Mentor Bearer auth, Content response, HTTP 200 `DESIGN_RESOURCE_UPDATED`, and exactly the catalog error set 401/403/404/422/500.
- Canonical contract: `docs/lists/list_api.md` row #52 declares path `content_id:int64!` only; AC-22 declares PATCH → update publication status → reload tree. Neither defines a body, transition, readiness fields, or physical status model.
- Proposed fallback: A strict `{published: boolean}` body expresses the target state and is `DERIVED`; allow only `APPROVED → PUBLISHED` (status gate as the available readiness signal), `PUBLISHED → APPROVED`, and same-target no-op. Preserve payload/tree fields and do not create a content revision. Keep the DD `Draft — Needs Confirmation` and request-contract discrepancy explicit.

## CURRENT_BEHAVIOR

- Baseline before this task:
- Source/config: APIs #49–#51 use local legacy `contents`/`courses`, `deleted_at IS NULL`, shared strict `ContentResponse`, and direct `courses.mentor_id` ownership. API #51 has `FOR UPDATE OF content, course`; it updates content fields/status and archives a snapshot.
- Runnable tests: API #51 and adjacent APIs have local HTTP TestClient tests using fake Session/query functions; no API #52 test exists before this task.
- Runtime wiring: No API #52 route/module/test is present. `/api/v1/mentor/content/{content_id}/publish` is not yet in `DESIGN_CONTRACT_PATHS`.
- Schema boundary: migration 006 has open-text `contents.status`; migration 007 snapshots content versions but defines no current-version pointer or publication selector. Live database/migration application is unverified.

## SOURCE_TRACE

```text
FastAPI route (new) -> api_52 view -> shared Mentor auth + int64 parser
  -> SELECT Content JOIN Course FOR UPDATE -> direct-owner check
  -> validate derived status transition -> UPDATE contents.status only (if needed)
  -> ContentResponse + DESIGN_RESOURCE_UPDATED -> commit
Tests: new API #52 TestClient module; adjacent #49–#51 tests; full Study suite
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Request direction | Catalog and AC-22 expose path only; DD proposal uses `published:boolean` | DISCREPANCY; fallback DERIVED | Document and wire a concrete client action while keeping DD draft/open question. |
| Readiness fields | Catalog says validate readiness; no approved content-type/payload/asset schema exists | Intent DIRECT; criteria SOURCE_REQUIRED | Gate publish on `APPROVED` status only; do not invent payload rules. |
| Lifecycle | AC-33 says `APPROVED/PUBLISHED + audit`; relation to AC-22 publish is ambiguous; #50/#51 currently use `PENDING_REVIEW` | State names DIRECT; transitions DERIVED | Limit local fallback to APPROVED/PUBLISHED; preserve macro-review questions. |
| Publication storage | Local migration 006 has `contents.status`; no published revision pointer; live schema unverified | Local source; deployment NOT_VERIFIED | Mutate status only and make no live-schema claim. |
| Mentor assignment | Existing #49/#51 compare token subject to `courses.mentor_id`; assignment model is absent | DERIVED fallback | Reuse existing boundary without inventing course-assignment tables. |

## CHANGES

- Files changed: API #52 module (`models.py`, `query.py`, `validate.py`, `view.py`, `__init__.py`), `app/api/v1.py`, `app/core/middleware.py`, API #52 tests, targeted API #52 DD/worklog/context pages.
- CONTEXT_UPDATES: Updated declared routes, runtime, module inventory, test inventory, and scope instructions with API #52 local implementation and verification boundaries.
- Context pages changed: `.agents/server-study/AGENTS.md`, `architecture.md`, `apis/declared-routes.md`, `core/database-security.md`, `core/runtime.md`, `database.md`, `modules/README.md`, and `tests.md`.
- Assumptions: The boolean target body, APPROVED/PUBLISHED transitions, same-target no-op, status-only readiness gate, and direct-owner access are DERIVED. No new error code, schema, audit field, readiness join, or revision write will be introduced.

## IMPLEMENTATION PLAN (before source edits)

1. Add a strict request model for `published: bool`; reject coercions and unknown fields.
2. Add signed-int64 path parsing using the adjacent API pattern.
3. Add SQL constants to lock active Content and its Course, and update only `contents.status` with expected-state predicate plus `RETURNING` projection.
4. In the view: authenticate before DB access; map malformed path/missing Content to 404; authorize stored course owner; allow publish only from APPROVED and unpublish only from PUBLISHED; return 422 for unsupported state; treat same target as no-op; rollback on failure; verify response projection before commit.
5. Wire PATCH route and exact middleware design path; reuse `ContentResponse` and catalog response envelope.
6. Add focused tests for auth/role, body validation, path, not-found/ownership, each transition, readiness/status rejection, idempotency, projection/query/commit failures, and trace/business codes.
7. Update #52 DD and Study Server context to distinguish local verified behavior from canonical contract/schema gaps; retain `Draft — Needs Confirmation` and DERIVED labels.
8. Run focused #52 + #49–#51 tests, full Study suite, Ruff, narrow mypy if available, OpenAPI route/request/error contract inspection, `git diff --check`, and context validator (record tool/baseline limitations).

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| Source review: AC-22/AC-33 → local DDL → catalog/DD → #49–#51 source/tests | Completed before implementation plan | PASS |
| `uv run pytest tests/modules/mentor/api_52_mentor_content_publish -q` | 27 passed; 1 upstream Starlette/httpx deprecation warning | PASS |
| `uv run pytest -q` | 431 passed; includes APIs #49–#51 | PASS |
| `uv run ruff check ...` + `uv run ruff format --check ...` | All checks passed; 8 files already formatted | PASS |
| `uv run mypy app/modules/mentor/api_52_mentor_content_publish` | Success: no issues found in 5 source files | PASS |
| Broader `uv run mypy app/api/v1.py app/modules/mentor/api_52_mentor_content_publish` | Reports two existing errors in guest course catalog helper and API #03 auth login; no API #52 diagnostic | PARTIAL; unrelated baseline issues |
| `python3 -m compileall -q ...` | Route, middleware, API #52 module and tests compiled | PASS |
| Focused OpenAPI/trace/middleware tests | Int64 path, strict required boolean body, HTTP 200, trace propagation and `DESIGN_VALIDATION_ERROR` pass | PASS; request body remains DERIVED |
| `git diff --check` on scoped tracked files + trailing-whitespace scan on 18 scoped files | No diagnostics or trailing whitespace | PASS |
| `node scripts/validate-agent-context.mjs` | Node is not installed in this environment | NOT_AVAILABLE |
| `deno run -A scripts/validate-agent-context.mjs --skip-drift` | Reports only the existing out-of-scope missing DB Admin context/source tree; no Study Server entries reported | BLOCKED_BY_BASELINE |
| `deno run -A scripts/validate-agent-context.mjs` | Reports the same missing DB Admin tree plus broad `CONTEXT_STALE` source snapshots across the existing worktree, including files already changed by prior Study API work | BLOCKED_BY_BASELINE; no global snapshot refresh attempted |

## HANDOFF

- Remaining blockers: Canonical request body, full readiness rules, approval/publication semantics, and deployed schema remain unconfirmed; local runtime fallback is DERIVED. Context validator remains red on the pre-existing missing DB Admin tree and broad repository source snapshot drift outside this API-specific update.
- Next owner/action: Contract owner should resolve the request body, readiness, approval/publication and revision questions before treating the local fallback as canonical.
