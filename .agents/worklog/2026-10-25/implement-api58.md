---
task_id: "2026-10-25-implement-api58"
date: "2026-10-25"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "COMPLETE"
---

# Worklog: Implement Study Server API #58

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run -A scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: Initial context pass found 51 matching worklogs; resumed coding preflight found 52 matching, 3 selected; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-25/implement-api34-upload-assets.md`
    - carry_forward: Preserve upload owner/purpose/course scoping and object metadata transaction semantics; local DDL/tests do not prove live DB or Object Storage.
  - path: `.agents/worklog/2026-10-25/implement-api47-mentor-lectures.md`
    - carry_forward: Shared explicit MENTOR guard, SQL-only query constants, caller-owned transaction, exact error envelope and live-schema boundary.
  - path: `.agents/worklog/2026-10-25/implement-api48-mentor-lecture-detail.md`
    - carry_forward: Preserve linked-API trace, verify producer/consumer persistence, record DERIVED choices and keep dirty worktree changes intact.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: `GET /api/v1/mentor/support/requests`; Bearer JWT with Mentor role; optional `course_id:int64` and `status:string`; HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; source contract currently declares `ApiEnvelope<SupportRequest>`; errors 401, 403 and 500.
- AC-24 flow: Mentor opens the support-request list, selects one request through API #59, sends a reply through API #60, and may resolve it through API #61. API #60 owns SupportMessage insertion; API #61 owns the RESOLVED status update.
- Cardinality conflict: AC-24 names a list endpoint and list action, but catalog and diagram declare one `SupportRequest`. Neither declares page, page size, order, empty-list behavior or a collection wrapper. Latest user direction authorizes Codex to choose the simplest coherent fallback.
- Linked contract review: #59 returns one request with its thread; #60 inserts a reply without resolving the request; #61 resolves without inserting a message. These DDs retain the same unresolved support model, identity, course, message and attachment questions.
- Source priority applied: AC-24 diagram first, checked-in infrastructure second, API catalog third. Fallback selected: use the Study Server legacy BIGINT conventions already used by Mentor APIs; add a normalized support request/message/asset-link schema; scope by direct `courses.mentor_id`; return `SupportRequest[]` without pagination, including full `messages[]` because that is required by the reusable schema. These are derived implementation decisions, not live schema facts.

## CURRENT_BEHAVIOR

- Source/config: No API #58 route, module, query, view or test exists in `apps/study-server/app` or `apps/study-server/tests`. The router currently wires APIs through #57. Shared auth can parse a positive numeric JWT subject and require `MENTOR`, but no mapping to the pilot support assignment UUID is present.
- Runtime/error wiring: `/api/v1/mentor/support/requests` is absent from `DESIGN_CONTRACT_PATHS`; current validation/unhandled handlers therefore use generic `VALIDATION_ERROR`/`INTERNAL_SERVER_ERROR` for an unwired endpoint. No live database was queried.
- Persistence evidence: `infra/postgres/study-server/DB.sql` has no support tables. `.agents/server-study/database.md` classifies `infra/postgres/02_study_db.sql` as V1-PILOT and explicitly says it does not prove that its tables are available to the current runtime; the DB helper applies configured `search_path` without verifying live metadata. The pilot defines UUID support tables but lacks a course relation and does not match the int64 legacy contract. The user authorized a coherent BIGINT fallback; live schema remains unverified.
- Runnable tests: No API #58 tests exist. No tests were run in this context-preparation turn because no implementation was made.
- Runtime boundary: The V1-PILOT DDL is design evidence, not proof of the configured or deployed runtime schema.
- Worktree: Already broadly dirty before API #58 work began. Preserve existing files and avoid cleanup/staging/commit.

## SOURCE_TRACE

```text
GET /api/v1/mentor/support/requests [UNWIRED]
  -> expected MENTOR JWT guard (shared helper supports role validation)
  -> approved support request persistence [SOURCE_REQUIRED]
  -> course filter and Mentor-scope predicate [SOURCE_REQUIRED]
  -> SupportRequest + student/messages/attachments mapping [SOURCE_REQUIRED]
  -> 200 DESIGN_RESOURCE_RETRIEVED / 401 / 403 / 500; 422 behavior is not in #58 catalog
Linked flow: #59 reads detail/thread; #60 inserts SupportMessage; #61 updates request to RESOLVED.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Collection cardinality | AC-24 list action/path vs catalog and diagram `ApiEnvelope<SupportRequest>` | `RESOLVED_BY_USER_DIRECTED_FALLBACK` | Change #58 success data to `SupportRequest[]`; no page query exists, so no pagination is added. |
| Physical support model and identifiers | Legacy Study Server APIs/auth use BIGINT; support schema is absent; pilot UUID model is not runtime evidence | `RESOLVED_BY_USER_DIRECTED_FALLBACK` | Add `support_requests`, `support_messages`, and ordered message-upload relation in source DDL plus migration 008. |
| Course relation/filter and Mentor authorization | Request requires `course_id`; existing Mentor APIs scope through numeric JWT subject and direct `courses.mentor_id` | `RESOLVED_BY_USER_DIRECTED_FALLBACK` | Store course/student BIGINT FKs; scope every request through `courses.mentor_id = :mentor_id`. |
| Nested response projection | `SupportRequest` requires student, messages and UploadAsset; #59 reads the same thread separately | `RESOLVED_BY_USER_DIRECTED_FALLBACK` | Include full messages in chronological order; resolve uploads through explicit link rows and owner/course/purpose/status checks. |
| Status and validation behavior | Catalog leaves status as string; pilot DDL lists candidate lifecycle values; `course_id` is int64 | `RESOLVED_BY_USER_DIRECTED_FALLBACK` | Exact status match; DDL allows `OPEN`, `IN_PROGRESS`, `WAITING_LEARNER`, `RESOLVED`, `CANCELLED`; add 422 validation mapping for invalid int64 query. |
| Live database/deployment | Only checked-in source/migration artifacts are available | `NOT_VERIFIED_HERE` | Do not claim migration application or live endpoint DB behavior. |

## IMPLEMENTATION_PLAN

1. Add BIGINT legacy tables in `DB.sql` plus migration 008: `support_requests` (id, course_id, student_id, status, created_at, resolved_at), `support_messages` (id, request_id, author_id, content, created_at), and ordered `support_message_uploads` (message_id, upload_id, asset_position). Add FKs/indexes; keep the separate V1-PILOT UUID artifact unchanged.
2. Use shared `validate_current_user_request(..., role="MENTOR")`; scope through `courses.mentor_id`. A supplied existing course owned by another Mentor returns catalog 403; a missing course yields an empty list because #58 declares no 404.
3. Resolve list cardinality to `ApiEnvelope<SupportRequest[]>`; no pagination; empty results return `[]`; combine optional course/status filters with AND; exact status match; stable request order `created_at DESC, id DESC`.
4. Return full `SupportRequest` items, including all messages in `created_at ASC, id ASC` order because `messages[]` is required by the reusable schema. Resolve attached UploadAssets through link rows and existing `uploads`, constrained by matching owner, course, role-purpose (`STUDENT/SUBMISSION`, `MENTOR/LECTURE`) and `UPLOADED` status. Treat broken links/projections as safe 500 errors.
5. Keep SQL strings in `query.py`; implement guard, course check, two read-only queries, grouping/mapping and rollback in `view.py`; keep router thin. Use current null omission convention for optional `resolved_at`; do not commit.
6. Update the API #58 DD before source edits to record these fallback decisions; reconcile API catalog/AC-24 diagram and add 422 validation code for malformed/out-of-range `course_id`.
7. Add focused TestClient cases for list/thread/assets/empty collection, AND filters/order/scope, 401/403/422/500, corrupt projections, read-only transaction behavior, trace envelope and OpenAPI. Review linked #59–#61; do not implement them in this API session.
8. Update server-study context/manifest and worklog. Run focused/full Study tests, Ruff, OpenAPI/import checks, `git diff --check`, context validator; keep live DB/deployment claims separate.

The user explicitly authorized Codex to choose the most reasonable and understandable fallback. The decisions above are derived and must be reflected in the DD before runtime edits.

## CHANGES

- Added `apps/study-server/app/modules/mentor/api_58_mentor_support_requests/` with strict response/query models, SQL-only constants and a read-only view using the shared MENTOR guard.
- Wired `GET /api/v1/mentor/support/requests` in `app/api/v1.py` and registered its exact route for design error mapping in `app/core/middleware.py`.
- Added TestClient coverage for collection/thread/assets, empty results, auth/scope, filters/order, query validation, safe failures, rollback, and OpenAPI.
- Added the selected legacy BIGINT support schema to `infra/postgres/study-server/DB.sql` and migration 008. No live migration was applied.
- Updated API #58 DD, catalog, AC-24 diagram, server-study context pages, and `.agents/context-manifest.json`. Kept all fallback choices explicitly DERIVED and live DB/deployment unverified.
- Reviewed linked APIs #59–#61; implementation remains limited to #58.
- Preserved the broadly dirty worktree and existing unrelated API #34/#47–#57 changes; no cleanup, staging, or commit was performed.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Coding worklog preflight | 52 matching coding logs; selected and read the 3 newest; no shortage. | `VERIFIED_PREFLIGHT` |
| Focused API #58 TestClient suite | 12 passed; one upstream Starlette/httpx deprecation warning. | `PASS` |
| Full Study Server suite | 550 passed; one upstream Starlette/httpx deprecation warning. | `PASS` |
| Ruff | `uv run ruff check app tests`: all checks passed. | `PASS` |
| OpenAPI | Focused test confirms collection response and int64 `course_id`; `app.openapi()` reports 28 API v1 path templates and 29 operations. | `PASS` |
| Live database / migration application | Not accessed or applied. | `NOT_VERIFIED_HERE` |
| Agent context validator | Full run reports missing DB Admin context/source and broad existing source drift; `--skip-drift` shows only unrelated DB Admin gaps and no Study page/reference errors. | `FAILED — BASELINE` |
| `git diff --check` | No whitespace errors. | `PASS` |

## HANDOFF

- API #58 is locally implemented and verified. The checked-in BIGINT schema/migration and contract fallbacks are not proof of deployed behavior; DD remains `Draft — Needs Confirmation`.
- API #59–#61 are not implemented in this task. API #59 should reuse the selected support tables and direct `courses.mentor_id` scope, with its own verification.
- Next task in the user's one-API-per-session goal: API #59.
