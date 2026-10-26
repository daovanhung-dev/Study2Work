---
task_id: "2026-10-26-implement-api98-admin-discussions-detail"
date: "2026-10-26"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "PLANNED"
---

# Worklog: Implement Study API #98 Admin discussion detail

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type coding --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-26/implement-api74-admin-course-detail.md`
    - carry_forward: Preserve pre-existing worktree changes; keep SQL constants in `query.py` and DB orchestration in `view.py`; fake DB tests do not establish live schema/deployment.
  - path: `.agents/worklog/2026-10-26/implement-api75-admin-course-update.md`
    - carry_forward: Use the shared role-aware JWT guard and keep contract-derived behavior separate from local fallbacks.
  - path: `.agents/worklog/2026-10-26/implement-api76-admin-course-status.md`
    - carry_forward: Authenticate before path parsing when raw path text is available; document catalog error mapping and preserve unrelated dirty files.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Implement only API #98 `GET /api/v1/admin/discussions/{discussion_id}` for the current one-API session; retain the catalog response and 401/403/404/500 errors.
- Canonical contract/approved DD: `docs/lists/list_api.md` #98 and AC-37 diagram; DD #98 is Draft and records unresolved response/schema gaps. A successful response is `ApiEnvelope<Page<Discussion>>`.
- Local `DERIVED` choices for an executable catalog-compatible fallback: one-item Page; exact path Discussion plus its direct child rows as comments, including all stored statuses and chronological `(created_at, id)` order; title follows API #97's normalized-content snippet capped at 120 characters; malformed/non-positive/out-of-int64 IDs map to catalog 404 after ADMIN auth.
- Report limitation: API #97's checked-in `discussion_reports` relation is a local schema candidate linked by BIGINT Discussion ID, but #98's `Page<Discussion>` has no report fields. Do not invent response fields or misuse envelope metadata; record the remaining AC-37 report-detail discrepancy.

## CURRENT_BEHAVIOR

- Source/config: API #97 is wired with shared `validate_current_user_request(..., role="ADMIN")`, candidate report relation queries, and `Discussion` projection; API #98 has no route/module/test. Middleware allowlist contains #97 only.
- Runnable tests: API #97 HTTP tests use a fake DB and verify read-only behavior; no #98 tests exist yet.
- Runtime wiring: Router source currently documents 57 `/api/v1` paths / 68 operations after #97; API #98 is `UNWIRED / NOT_FOUND`.

## SOURCE_TRACE

```text
FastAPI raw-path route -> API #98 view -> shared ADMIN JWT guard -> signed-int64 path parser -> query_one discussion / query_many direct children -> strict Discussion/comment/Page mapping -> ApiEnvelope response; GET performs no writes; HTTP tests cover auth, parsing, 404, query/projection errors and success.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| AC-37 report detail vs response | Diagram reads discussion/comments/reports; catalog `Page<Discussion>` has no report projection | `DISCREPANCY` | Report rows cannot be exposed without an approved response field/schema; retain the limitation in DD/worklog. |
| Discussion title | Legacy DDL has no title; API #97 uses normalized content clipped to 120 characters | `DERIVED` | Reuse API #97 mapping for consistent catalog projection; title is not stored. |
| Thread semantics | DDL has `discussions.parent_id`; catalog accepts one discussion ID and comments array | `DERIVED` | Treat the exact path row as the Discussion and direct children as comments; do not inherit Student visibility filters. |
| Live DB/report producer | Checked-in migration 014 is not deployment or ingestion evidence | `UNVERIFIED` | Tests establish local behavior only. |

## CHANGES

- Files changed: pending implementation.
- CONTEXT_UPDATES: Add API #98 route/module/middleware wiring and update Study route/module context plus DD/worklog.
- Context pages changed: `.agents/server-study/apis/declared-routes.md`, `.agents/server-study/modules/README.md`, and `.agents/context-manifest.json` if their current registry shape requires an API entry.
- Assumptions: No catalog, DB schema, report payload, or unrelated API behavior changes. Preserve existing worktree modifications and do not stage/commit outside the exact API #98 scope.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| Pending focused #98 HTTP tests | Not run | `NOT_RUN` |
| Pending linked #97 + #98 tests, full Study suite, Ruff, OpenAPI and context validation | Not run | `NOT_RUN` |

## HANDOFF

- Remaining blockers: AC-37 report details have no supported response field; live schema, migration deployment and report writer are not verified.
- Next owner/action: Implement API #98, update the DD's local decisions/limitations, run the requested HTTP and regression checks, and audit exact Git scope before any commit.
