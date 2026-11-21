---
task_id: "2026-10-25-implement-api48-mentor-lecture-detail"
date: "2026-10-25"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "COMPLETE"
---

# Worklog: Implement API #48 Mentor lecture detail

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run -A scripts/select-worklogs.mjs --type coding --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-25/implement-api34-upload-assets.md`
    - carry_forward: API #34 now stores upload metadata in the legacy BIGINT `uploads` artifact and exposes owner/purpose/course scoped lookup patterns; live DB and real Object Storage remain unverified.
  - path: `.agents/worklog/2026-10-25/implement-api47-mentor-lectures.md`
    - carry_forward: API #47 is the immediate AC-21 producer; it uses Mentor direct-course ownership, `asset_refs` as ordered unique int64 IDs, DRAFT/PUBLISHED behavior as approved for its request, and transaction-owned write flow. Verify whether refs are persisted for #48 before using them.
  - path: `.agents/worklog/2026-10-25/load-study-server-coding-context.md`
    - carry_forward: Preserve all existing dirty Study Server/context/DD/schema/worklog changes; use current source over stale context and distinguish checked-in schema from live DB.
- shortage: `none` (selector found 41 coding worklogs and selected all 3)

## EXPECTED_BEHAVIOR

- Requirement: Implement API #48 from its DD for AC-21, review linked APIs, write a detailed plan before runtime edits, then test the endpoint and update affected Study Server context/worklog.
- Canonical contract/approved DD: `GET /api/v1/mentor/lectures/{lecture_id}`; Mentor Bearer JWT; required int64 path; `ApiEnvelope<Lecture>`; HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; errors limited to 401/403/404/500 and their catalog business codes.

## CURRENT_BEHAVIOR

- Source/config: No API #48 route/module/test exists. API #34 persists all UploadAsset fields in `uploads`; API #47 validates and returns requested assets but INSERTs only `lessons`, so it drops the asset-to-lecture relation. Legacy `uploads` has no `lesson_id`, `lessons` has no asset refs, and `resources` lacks UploadAsset fields. `error_response()` currently serializes omitted data as JSON null.
- Runnable tests: API #47 worklog reports 25 focused tests and 319 full-suite tests in its implementation turn; these are historical, not rerun here. API #48 has no current tests.
- Runtime wiring: `app/api/v1.py` ends Mentor runtime routes at API #47; `DESIGN_CONTRACT_PATHS` contains #46/#47 but not #48. Shared auth returns numeric subject and supports explicit `MENTOR` role; live DB remains unverified.

## IMPLEMENTATION_PLAN

1. Read AC-21/AC-22 and DB design diagrams, then `infra/postgres` and API catalog in the user's conflict order. Evidence: AC-21 is `#46 → #34 upload → Object Storage → #47 → #48`; logical ERD contains `lessons → resources` but no UploadAsset relation; legacy infra `uploads` contains metadata but has no lesson key; catalog requires `Lecture.assets` and only codes 401/403/404/500.
2. Trace API #34/#47 source, route and tests. Finding: #47 validates asset IDs, resolves metadata and returns assets in the create response, but its `INSERT_LECTURE` persists only `lessons`; API #48 cannot know which course uploads belong to that lecture.
3. Resolve the missing physical link with the smallest relation that preserves the contract: add legacy `lesson_uploads(lesson_id, upload_id, asset_position)`, reference existing `lessons`/`uploads`, write it atomically from #47, and read the ordered metadata from #48. Keep V1-PILOT schema separate; do not apply the migration to live DB.
4. Implement #48 with shared Mentor guard, numeric subject, direct course owner predicate matching #46/#47, no PUBLISHED filter, required Lecture fields and ordered UploadAsset join. Return 404 for malformed/out-of-int64 path or absent lecture, 403 for owner mismatch, and 500 for invalid parent/link integrity or DB errors; use only catalog codes.
5. Keep AC-21 assignment support as `SOURCE_REQUIRED`; choose explicit `content: null` when stored content is NULL (DD permits nullable content), and return stored status without enum invention. Verify generated OpenAPI still declares int64 path after using a raw path string for catalog-compatible parse failure handling.
6. Add TestClient coverage for #48 auth/access/not-found/integrity/assets/order/null/error/trace behavior and #47 regression coverage for relation writes, empty refs, ordering and rollback.
7. Update #47/#48 Markdown mapping notes, affected server-study context/manifest and this worklog; run focused tests, full Study suite, Ruff/import/OpenAPI checks, `git diff --check`, and context validator. Report live DB/deployment limits separately.

## SOURCE_TRACE

```text
GET /api/v1/mentor/lectures/{lecture_id} -> shared MENTOR JWT guard -> signed-int64 path parser -> lessons LEFT JOIN courses -> direct owner check -> ordered lesson_uploads links LEFT JOIN scoped uploads -> nullable LectureResponse envelope -> TestClient/OpenAPI verification.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Required assets projection | #34 persists metadata; #47 consumes refs but does not persist their lecture relation; diagrams/legacy infra provide no existing link. | `RESOLVED_BY_IMPLEMENTATION_DECISION` | Add a normalized ordered `lesson_uploads` link in the legacy artifact and use it for read-after-create. |
| Assigned-course access | AC-21 includes owned or assigned course; current #46/#47 source uses numeric `courses.mentor_id` and no assignment relation was found in diagrams or infra. | `SOURCE_REQUIRED` | Implement direct-owner access consistently; do not claim assigned-course support. |
| Path parse and nullable content | Catalog excludes 422; DD allows nullable content and leaves malformed path mapping open. | `RESOLVED_BY_IMPLEMENTATION_DECISION` | Map malformed/out-of-range path to catalog 404; serialize SQL NULL content as JSON null. |
| Legacy versus V1-PILOT schema | DD/diagrams distinguish BIGINT lessons from UUID/versioned pilot tables; live schema is unknown. | `NOT_VERIFIED_HERE` | Any local query targets only evidence-backed checked-in source and does not claim deployment. |

## CHANGES

- Runtime: API #48 route/middleware wiring and read-only mentor lecture module; shared Lecture content is nullable; API #47 writes ordered `lesson_uploads` rows atomically with the lesson.
- Schema artifact: legacy DB.sql relation and migration 005, referencing only checked-in legacy `lessons`/`uploads` identifiers.
- Tests: API #48 TestClient coverage for linked and empty assets, auth/access, malformed/missing ID, integrity/DB errors, nullable content and OpenAPI; API #47 relation persistence/rollback regression coverage.
- DD/context: update #47/#48 mapping and verification evidence; wire API #48 route/module/test/migration into canonical server-study context and manifest.
- CONTEXT_UPDATES: Applied to `.agents/context-manifest.json` and server-study `AGENTS.md`, architecture, declared routes, core/database-security, core/runtime, database, modules and tests pages.
- Assumptions: Direct ownership matches #46/#47; assigned-course support and live migration/deployment remain unverified; malformed/out-of-range path maps to catalog 404 as an implementation decision.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run -A scripts/select-worklogs.mjs --type coding --limit 3` | Found 41 same-type logs; all three selected worklogs were read. | VERIFIED |
| DD #48 read | All 8 sheets and 3 reports read; contract and open blockers recorded above. | VERIFIED_STATIC_ONLY |
| `uv run pytest tests/modules/mentor/api_47_mentor_lectures_create/test_mentor_lectures_create.py tests/modules/mentor/api_48_mentor_lecture_detail/test_mentor_lecture_detail.py -q` | 42 passed; one existing Starlette/httpx deprecation warning. | VERIFIED |
| `uv run pytest -q` | 336 passed; one existing Starlette/httpx deprecation warning. | VERIFIED |
| `uv run ruff check app tests` | All checks passed. | VERIFIED |
| `git diff --check` | No whitespace errors. | VERIFIED |
| DD links and manifest sources | 37 local links checked, none broken; manifest JSON parses and all required server-study source paths exist. | VERIFIED_STATIC_ONLY |
| `node scripts/validate-agent-context.mjs` | `AGENT_CONTEXT_INVALID` from missing DB Admin context/source plus broad historical source-snapshot drift, including pre-existing Study paths. `--skip-drift` leaves only the DB Admin baseline failures; no API #48 required-source or context-link finding. | BLOCKED_BY_REPOSITORY_BASELINE |

## HANDOFF

- Remaining boundaries: Context validator remains invalid because of unrelated missing DB Admin context/source; live schema/migration and assigned-course behavior remain outside local verification.
- Next owner/action: API #48 local implementation and review are complete; a separate coding session can start API #49, preserving this session boundary and the documented live-schema/assignment limits.
