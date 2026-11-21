---
task_id: "2026-10-25-implement-api53-mentor-content-delete"
date: "2026-10-25"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Implement API #53 Mentor Content delete

## PRIOR_WORKLOG_REVIEW

- primary_task_type: coding
- selector_command: `deno run -A scripts/select-worklogs.mjs --type coding --limit 3`
- selector result: 46 coding worklogs available; 3 selected; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-25/implement-api34-upload-assets.md`
    - carry_forward: Keep SQL static in `query.py`, orchestration in `view.py`, and verify ownership, transaction, response projection, and error behavior.
  - path: `.agents/worklog/2026-10-25/implement-api47-mentor-lectures.md`
    - carry_forward: Parse raw path IDs as signed int64; reuse Mentor auth and exact catalog error codes; local DDL does not prove live schema.
  - path: `.agents/worklog/2026-10-25/implement-api48-mentor-lecture-detail.md`
    - carry_forward: Lock resource and owning course together when authorization depends on course ownership; test malformed IDs and projection failures.
  - path: `.agents/worklog/2026-10-25/implement-api49-mentor-content-list.md`
    - carry_forward: Reuse `contents.deleted_at IS NULL` as the current active-row predicate and preserve Content tree integrity; direct owner is the existing local fallback.
  - path: `.agents/worklog/2026-10-25/implement-api50-mentor-content-create.md`
    - carry_forward: API #50 locks the course before insert; use the same course lock to serialize deletion against current Content creation.
  - path: `.agents/worklog/2026-10-25/implement-api51-mentor-content-update.md`
    - carry_forward: Reuse the locked Content/Course access projection; keep version history and all lifecycle choices marked DERIVED.
  - path: `.agents/worklog/2026-10-25/implement-api52-mentor-content-publish.md`
    - carry_forward: API #52 owns the local publication-status mutation; its APPROVED/PUBLISHED transition policy is DERIVED.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Catalog row #53 declares `DELETE /api/v1/mentor/content/{content_id}`, Bearer JWT role Mentor, path `content_id:int64!`, no body/query, `ApiEnvelope<DeleteResult>`, HTTP 200 `DESIGN_RESOURCE_DELETED`, and exactly 401/403/404/422/500 with the listed `DESIGN_*` codes.
- Reusable `DeleteResult` is `id:int64`, `status:"deleted"`, `deleted_at:date-time`.
- AC-22 directly states the Mentor manages course content, DELETE/soft-deletes Content, then reloads the content tree.
- Soft-delete implementation column, child behavior, PUBLISHED eligibility, status eligibility, retry semantics, and audit/retention policy are not fully specified by the diagram/catalog. DD proposals remain `Draft — Needs Confirmation`.

## CURRENT_BEHAVIOR

- Source: API #49–#52 Content routes/modules exist; API #53 route/module/test and middleware contract path are absent. Current modules use local `contents`/`courses`, active predicate `deleted_at IS NULL`, shared Mentor auth, signed-int64 parser, static SQL, view-owned transaction, and `ContentResponse` for Content reads/writes.
- API #49 excludes soft-deleted rows and rejects an active child whose parent is absent from the returned tree; such malformed trees become internal errors.
- API #50 locks the owning course before it inserts a Content row. API #51 does not change `parent_id`.
- Local migration 006 defines nullable `contents.deleted_at`; migration 007 attaches version history to Content. Live schema/migration application is unverified.
- Tests: API #49–#52 have local TestClient/fake-DB coverage; the last reported full Study suite had 431 passing tests before API #53.
- Worktree has unrelated/prior API changes; preserve them and do not stage or commit.

## SOURCE_TRACE

```text
FastAPI DELETE route -> API #53 view -> shared Mentor JWT/role validation
  -> strict signed-int64 parse -> SELECT active Content + Course FOR UPDATE
  -> direct courses.mentor_id ownership check
  -> check active direct child -> reject PUBLISHED under DERIVED guard
  -> UPDATE contents.deleted_at with RETURNING id/deleted_at
  -> validate DeleteResult -> commit -> success envelope
Tests: API #53 TestClient/fake-DB tests; #49/#50/#52 interaction checks; full Study suite
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Soft-delete storage | AC-22 says soft delete; local migration 006 and DB.sql define `contents.deleted_at`; live schema unknown | Diagram DIRECT; local source-backed mapping; deployment NOT_VERIFIED | Use only the checked-in local tombstone column; do not claim deployed readiness. |
| Active children | Content has `parent_id`; API #49 requires parent rows to be present in active tree | Child blocking is DERIVED | Return 422 for active direct child to avoid creating an invalid tree; no cascade/reparent. |
| PUBLISHED eligibility | API #52 owns publication status; DD proposes unpublish-first; diagram does not state delete interaction | DERIVED | Return 422 for PUBLISHED; keep DD question open. |
| Other statuses | AC-33 includes pending, approval, rejection; deletion effects on moderation queue are unspecified | DERIVED fallback | Permit non-PUBLISHED states locally without changing status; keep withdrawal/queue policy open. |
| Repeated delete | Catalog allows 404; local active-row convention filters tombstones | DERIVED | Soft-deleted row is unavailable and returns 404; idempotent retry policy remains open. |
| Mentor assignment | Current APIs compare numeric JWT subject with `courses.mentor_id`; assigned-Mentor model is absent | DERIVED fallback | Reuse direct-owner boundary without inventing assignment schema. |
| Path parse error | Catalog has 422 but #49–#52 parse raw path in view and map invalid/out-of-range ID to 404 | Current local convention | Preserve adjacent Content behavior; no body/query is added. |

## IMPLEMENTATION PLAN (before source edits)

1. Add API #53 response models for `DeleteResult` and its success envelope; keep model declarations only.
2. Add an API #53 signed-int64 path parser matching adjacent Content endpoints.
3. Add static SQL to lock active Content and its Course, query active direct children, and soft-delete through `deleted_at` with `RETURNING id, deleted_at`.
4. Implement view orchestration: authenticate before DB access; parse ID; lock and validate row projection; enforce direct owner; return 422 for active direct children or `PUBLISHED`; soft-delete and validate `DeleteResult`; commit only after the response model is valid; rollback on every failure path.
5. Wire `DELETE /mentor/content/{content_id}` with no request body and add its path to `DESIGN_CONTRACT_PATHS`.
6. Add focused HTTP tests covering the catalog contract, auth, malformed ID, missing/foreign Content, child and PUBLISHED guards, success timestamp/result, SQL/DB failures, and transaction behavior.
7. Update API #53 DD, server-study context pages/manifest as applicable, and this worklog with verified source/test status while preserving draft/open questions.
8. Run focused API #53/#49/#50/#52 tests, full Study tests, Ruff, module-focused mypy, OpenAPI checks, `git diff --check`, and the context validator; report local-only evidence and known validator baseline limitations.

## CHANGES

- Added `api_53_mentor_content_delete` models, raw signed-int64 parser, SQL constants, and orchestration view. The view authenticates Mentor before DB access, locks active Content/Course, checks the current direct owner, blocks active direct children and PUBLISHED status under DERIVED guards, writes `contents.deleted_at = CURRENT_TIMESTAMP`, validates `DeleteResult`, and commits/rolls back in the caller-owned transaction.
- Wired `DELETE /api/v1/mentor/content/{content_id}`. Its route template already existed in `DESIGN_CONTRACT_PATHS` for API #51 PUT, so no duplicate middleware path entry was added. OpenAPI has no request body/query and documents ID int64, literal `deleted`, and date-time `deleted_at`.
- Added API #53 HTTP tests and updated its 11-file DD pack, relevant server-study context pages, context registry source paths, and this worklog. The DD remains `Draft — Needs Confirmation`; child/PUBLISHED/retry/status policy remains DERIVED/open.
- Worktree contains pre-existing API #34/#47–#52 and other project changes. They were preserved; nothing was staged or committed.

## VERIFICATION

- `uv run pytest tests/modules/mentor/api_53_mentor_content_delete/test_mentor_content_delete.py -q`: 18 passed, 1 upstream Starlette/httpx deprecation warning.
- `uv run pytest tests/modules/mentor/api_53_mentor_content_delete tests/modules/mentor/api_49_mentor_content_list tests/modules/mentor/api_50_mentor_content_create tests/modules/mentor/api_51_mentor_content_update tests/modules/mentor/api_52_mentor_content_publish -q`: 113 passed.
- Final `uv run pytest -q`: 449 passed, 1 upstream Starlette/httpx deprecation warning.
- `uv run ruff check` and `uv run ruff format --check` on route, middleware, API #53 module and tests: pass.
- `uv run mypy app/modules/mentor/api_53_mentor_content_delete app/modules/mentor/api_52_mentor_content_publish`: no issues in 10 source files.
- OpenAPI tests verify no DELETE body/query, int64 `content_id` and `DeleteResult` schema (`id:int64`, `status` const `deleted`, `deleted_at:date-time`). Success test verifies response and DB timestamp mapping.
- Compared all eight DD appendix suffixes byte-for-byte with registered Markdown templates; checked relative links and JSON examples: pass.
- `git diff --check` and custom whitespace/final-newline scan for new source/test/worklog files: pass.
- `deno run -A scripts/validate-agent-context.mjs --skip-drift`: fails only on the existing missing DB Admin context/source tree and its broken links (`.agents/db-admin`, `apps/db-admin-*`). No Study Server-specific validation errors were reported. These unrelated files were left unchanged.

## CONTEXT_UPDATES

- Updated `.agents/server-study/AGENTS.md`, `architecture.md`, `apis/declared-routes.md`, `core/runtime.md`, `core/database-security.md`, `database.md`, `modules/README.md`, and `tests.md` for API #53 and the 449-test result.
- Added API #52/#53 source/test paths to `.agents/context-manifest.json` because the registry previously stopped at API #51.
- Updated DD #53 runtime mapping and verification while preserving all template appendix suffixes and unresolved DERIVED policy questions.

## OPEN_ITEMS

- Confirm dependency coverage, PUBLISHED deletion rule, deletion of pending/rejected/approved rows, moderation queue filtering/withdrawal, repeated DELETE semantics, audit/history retention, timestamp timezone, Mentor assignment policy, and live schema/migration deployment before treating DERIVED behavior as approved.
