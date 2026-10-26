---
task_id: "2026-10-25-api51-mentor-content-update"
date: "2026-10-25"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Implement API #51 Mentor Content update

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run -A scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: 44 available; selected 3.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-25/implement-api34-upload-assets.md`
    - carry_forward: Giữ route/module separation, allowlist design error routing và transaction ownership theo các helper Study; chỉ mang convention, không tái dùng upload behavior cho Content.
  - path: `.agents/worklog/2026-10-25/implement-api47-mentor-lectures.md`
    - carry_forward: Mentor access dựa trên direct `courses.mentor_id`; trace DB transaction và owner boundary; không tái dùng Lecture/Upload mapping.
  - path: `.agents/worklog/2026-10-25/implement-api48-mentor-lecture-detail.md`
    - carry_forward: Parse path int64 trong view để khớp catalog error set; map dữ liệu đã kiểm tra trước response; giữ lỗi 404/403/500 hiện hành.
- additional_relevant_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-25/implement-api49-mentor-content-list.md`
    - carry_forward: Legacy `contents` mapping, direct course ownership, soft-delete filter, reusable `ContentResponse` projection.
  - path: `.agents/worklog/2026-10-25/implement-api50-mentor-content-create.md`
    - carry_forward: Request field shape `content_type/title/payload`, `PENDING_REVIEW` precedent, JSONB serialization, commit/rollback conventions.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Implement `PUT /api/v1/mentor/content/{content_id}` for Mentor-owned Content, returning HTTP 200 and `ApiEnvelope<Content>` with `DESIGN_RESOURCE_UPDATED`.
- Canonical contract/approved DD: Catalog #51 declares path `content_id:int64!`, response `ApiEnvelope<Content>`, and errors 401/403/404/422/500, but omits a body. AC-22 says “UPDATE Content + version”. AC-33 review queue reads `PENDING_REVIEW` and reviewer reads content/version/author. The #51 DD remains Draft — Needs Confirmation.
- User precedence for source conflict: diagrams -> infra -> API catalog -> simplest clear fallback. Any behavior beyond direct source evidence must remain labeled `DERIVED` and the DD stays Draft — Needs Confirmation.

## CURRENT_BEHAVIOR

- Source/config: API #51 route/module/test are absent. Router has APIs #49 and #50; middleware design paths include `/api/v1/mentor/content` but not parameterized #51 path. Legacy migration 006 defines `contents` without version history or author fields. V1-PILOT `content_blocks` is a separate UUID/lesson model and is not a compatible substitute.
- Runnable tests: APIs #49/#50 cover the shared Content shape and Mentor direct course ownership. No API #51 test exists.
- Runtime wiring: `validate_current_user_request(..., role="MENTOR")`, `query_one`, `success_response`, `error_response`, and caller-owned Session transactions are existing patterns. API #49 reads active `contents`; API #50 creates a root `PENDING_REVIEW` row.

## SOURCE_TRACE

```text
PUT route (absent)
  -> API #51 view/module (absent)
  -> legacy contents row joined to owning courses.mentor_id
  -> planned atomic snapshot + UPDATE of contents
  -> ApiEnvelope<Content>
  -> current auth/response/database helpers; new focused route/view tests
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Request body | Catalog and diagram omit it; PUT needs content fields; API #50 already accepts `content_type`, `title`, `payload`. | `DISCREPANCY`; reuse 3 fields as `DERIVED` | Implement strict full-replacement body and keep DD unapproved. |
| Version persistence | AC-22 says “+ version”; legacy `contents` has no version relation; pilot `content_blocks` is incompatible. | `SOURCE_REQUIRED`; add a legacy version snapshot relation as `DERIVED` fallback | Add additive migration 007 and matching legacy schema documentation; do not claim live migration applied. |
| Review lifecycle | AC-33 reads `PENDING_REVIEW`; #50 creates that state; approval/published handling is split with #52. | New content state is `DERIVED`; prior-state snapshot is direct implementation of version history | Archive pre-update row and set current row `PENDING_REVIEW`; published-serving/promotion behavior remains open for #52/AC-33. |
| Author semantics | Content has no creator/author field; AC-33 says reviewer reads author. | `SOURCE_REQUIRED` | Do not invent an author column or report archive actor as original author. |
| Ownership | API #49 uses direct `courses.mentor_id`; catalog requires Mentor. | Existing source pattern; exact assignment policy remains unavailable | Lock Content and parent Course; 404 absent/deleted Content, 403 owner mismatch. |
| Validation | Catalog allows 422 but does not define body fields or constraints. | `DERIVED` from API #50 shape | Strict required JSON fields; open content type and object payload, no invented enum/key rules. |

## IMPLEMENTATION_PLAN

1. Keep scope to `server-study`, API #51, its legacy DB mapping, directly linked DD/context pages, focused tests, and worklog. Preserve the pre-existing dirty worktree.
2. Add module `api_51_mentor_content_update` with strict request fields `content_type`, `title`, `payload`; reuse the API #49 Content response model. Parse `content_id` as signed int64 in the view so malformed/out-of-range IDs map to catalog 404.
3. In the view, authenticate Mentor before DB access; select and lock active Content plus owning Course; return 404 if absent/deleted and 403 if `courses.mentor_id` differs. Use one transaction to snapshot the pre-update row into `content_versions`, update editable fields and status to `PENDING_REVIEW`, verify returned projection, then commit; rollback on query/mapping/commit failure. Keep course, parent, and order server-managed.
4. Add route with HTTP 200, `UpdateContentEnvelope`, int64 OpenAPI metadata, and middleware route-template allowlist entry so framework body-validation errors keep `DESIGN_VALIDATION_ERROR`.
5. Add additive migration 007 and matching `DB.sql`; document snapshot fields/index/limitations in DB guide and ERD. Do not touch V1-PILOT schema.
6. Update API #51 DD using the registered `createDD-markdown` template: body and history storage are explicitly `DERIVED`; retain `Draft — Needs Confirmation`, exact catalog response/error set, unresolved published-version serving/approval semantics, and no false author provenance. Update linked #51 context/manifest entries only where source wiring changed.
7. Add focused tests for success+snapshot+commit, auth-before-DB, malformed path, absent/deleted Content, owner denial, invalid body, query/mapping/commit rollback, route OpenAPI and middleware error code. Run focused API #51 tests, relevant adjacent #49/#50 tests, lint/type checks available in this repo, diff inspection, and the prescribed context validator; report repository baseline failures separately.

### DERIVED decisions to apply unless direct evidence contradicts

- Body: full replacement of `content_type`, `title`, `payload`, following API #50. All are required; extra fields rejected; `content_type` remains open string; `payload` must be an object.
- Version: add a BIGINT legacy `content_versions` table as pre-update snapshots. Each archived version stores Content fields and tree placement; `archived_by` means the Mentor who superseded the snapshot, not the original author. Current `contents` row is the implicit next version.
- Lifecycle: after every accepted PUT, current row is `PENDING_REVIEW`; prior state/status remains in history. This endpoint alone does not establish that public consumers serve the prior published snapshot or that API #52 promotes a specific revision.
- Keep current response contract without adding a version field; do not introduce a 409 or other catalog error.

## CHANGES

- Files changed: Added API #51 router/module/tests, middleware route-template allowlist, migration 007, matching legacy `DB.sql`, DB table documentation/ERD, API #51 DD table mapping and open questions. Updated Study Server context manifest/pages and this worklog. Applied Ruff formatting to the modified middleware conditional without changing behavior.
- CONTEXT_UPDATES: Added API #51 route/auth/transaction/error behavior, 404 path mapping, fake-DB test scope, migration 007 and live-schema boundary. Updated suite count to 404 and route count to 22.
- Context pages changed: `.agents/server-study/AGENTS.md`, `architecture.md`, `apis/declared-routes.md`, `core/database-security.md`, `core/runtime.md`, `database.md`, `modules/README.md`, `tests.md`, `.agents/context-manifest.json`, `DB_UNICA_TABLES.md`, `DB_UNICA_ERD.drawio`, API #51 DD folder.
- Assumptions: Body fields/full-replacement, history table/sequence, status transition and direct-owner authorization remain DERIVED. `archived_by` is updater provenance only; public published-version serving and AC-33 original author remain unresolved.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run -A scripts/select-worklogs.mjs --type coding --limit 3` | 44 available; selected #34, #47, #48 worklogs, all read; #49 and #50 related logs also read. | VERIFIED |
| `git status --short --branch` | Existing dirty worktree on `develop...origin/develop`; preserved. | VERIFIED |
| API #51 source/module/test existence checks | Route/module/test absent before implementation. | VERIFIED_STATIC_ONLY |
| `uv run pytest -q tests/modules/mentor/api_51_mentor_content_update` | 23 passed; fake DB. | VERIFIED_LOCAL |
| `uv run pytest -q tests/modules/mentor/api_49_mentor_content_list tests/modules/mentor/api_50_mentor_content_create tests/modules/mentor/api_51_mentor_content_update` | 68 passed. | VERIFIED_LOCAL |
| `uv run pytest -q` | 404 passed in Study Server suite. | VERIFIED_LOCAL |
| `uv run ruff check ...` (route, middleware, API #51 module/tests) | All checks passed. | VERIFIED |
| `uv run ruff format --check ...` (same scope) | 8 files already formatted. | VERIFIED |
| `uv run mypy --follow-imports=silent app/modules/mentor/api_51_mentor_content_update` | No issues in 5 source files. | VERIFIED |
| Broader `uv run mypy app/api/v1.py app/core/middleware.py app/modules/mentor/api_51_mentor_content_update` | Reports two existing errors in `guest/_shared/course_catalog/helpers.py` and `guest/api_03_auth_login/view.py`; no API #51 diagnostic. | BASELINE_FAILURE |
| DD link scan, manifest JSON parse, ERD XML parse | No broken API #51 DD links; JSON and XML parse successfully. | VERIFIED_STATIC_ONLY |
| `git diff --check` | No diagnostics. | VERIFIED |
| `node scripts/validate-agent-context.mjs` | Cannot start because `node` is unavailable. | NOT_RUNNABLE |
| `deno run -A scripts/validate-agent-context.mjs` | `AGENT_CONTEXT_INVALID`: missing DB Admin context/source plus broad existing server-study source snapshot drift. | REPOSITORY_BASELINE |
| `deno run -A scripts/validate-agent-context.mjs --skip-drift` | Remaining errors are DB Admin context/source paths absent from this checkout; no API #51-specific error. | REPOSITORY_BASELINE |
| Live DB/migration probe | Not performed; checked-in SQL is not deployment evidence. | NOT_VERIFIED |

## HANDOFF

- Remaining blockers: Contract-owner confirmation of API #51 body/history/status semantics; AC-33 author provenance and API #52 published-version selection; live migration 007 status. Repository-wide context validator remains invalid for the pre-existing DB Admin boundary and source snapshot drift.
- Next owner/action: API #52 is next in the #48–#103 sequence. Keep API #51 fallback marked DERIVED until its request/version/lifecycle contract is approved.
