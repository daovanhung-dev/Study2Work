# Verification Report — API #82 Lấy danh sách lesson

## Scope

- Runtime: `apps/study-server/app/modules/admin/api_82_admin_lessons_list/` and GET route `/api/v1/admin/lessons`.
- Tests: `apps/study-server/tests/modules/admin/api_82_admin_lessons_list/` plus linked regression/full Study suite.
- Documentation/context: DD #82, AC-34 macro-review note, canonical `.agents/server-study/` pages and worklog.
- DD status: Draft — Needs Confirmation.
- Verification below covers local source and fake DB HTTP tests; it does not prove live schema, migration deployment or authorization policy approval.

## Static checks

| Check | Result | Status |
|---|---|---|
| Focused API #82 HTTP tests | 15 passed; one upstream Starlette/httpx deprecation warning | PASS |
| Linked API #09/#78/#82 regression | 47 passed; same upstream warning | PASS |
| Full Study test suite | 1012 passed; one upstream warning | PASS |
| Scoped Ruff | `ruff check app/api/v1.py app/core/middleware.py app/modules/admin/api_82_admin_lessons_list tests/modules/admin/api_82_admin_lessons_list` — all checks passed | PASS |
| OpenAPI path/schema | 48 `/api/v1` paths / 53 operations; four documented parameters; HTTP 200/401/403/422/500; success model `GetAdminLessonsEnvelope` | PASS |
| DD Markdown / template appendix parity | 11 files; 3 JSON blocks; 30 tables / 375 data rows; 7 balanced fence pairs; 33 local file links; all 8 appendix suffixes byte-identical | PASS |
| Context manifest / validator | New API #82 source/test paths are registered. Deno validator `--skip-drift` reports existing DB Admin missing roots/pages/source links; full validation also reports `CONTEXT_STALE` across currently dirty tracked scopes because the shared worktree has broad uncommitted changes and the manifest remains anchored to its prior source commit. No API #82 path is reported missing. | BASELINE_FAILURE |
| `git diff --check` | Clean after code, DD, context and worklog edits | PASS |

## Findings and limits

- Catalog #82 declares `ApiEnvelope<Lesson>` while endpoint name and AC-34 flow describe a list. Local implementation returns `Lesson[]` as DERIVED fallback and leaves the DD Draft.
- The `type` query has no compatible Lesson field in the reusable schema or inspected DDL. Local implementation rejects it explicitly with 422 `DESIGN_VALIDATION_ERROR` / `UNSUPPORTED_FILTER`; it does not silently ignore the filter.
- Legacy BIGINT and V1-PILOT UUID lesson models are not interchangeable. Legacy `course_id`, `sort_order`, and `status` may be NULL while the reusable Lesson projection requires them. Mapping errors become safe 500 responses.
- Shared auth verifies role `ADMIN`; AC-34 fine-grained lesson-management permission remains without executable policy evidence.
- Fake DB tests do not establish live schema or migration deployment. No runtime deployment claim is made. The global context validator does not pass because of existing DB Admin omissions and stale source fingerprints in the shared dirty worktree; Study Server API #82 source/test paths themselves are in the manifest.

## AC-34 macro-review

- Status: `VERIFIED_WITH_OPEN_QUESTIONS`; this is a document-level consistency review, not owner approval or runtime verification of sibling APIs.
- API #82 list/reload is wired locally. Its direct `ApiEnvelope<Lesson>` catalog type remains discrepant with list intent; #86 deleted-row visibility remains unresolved and is not filtered by #82.
- Sibling API status is maintained in the [consolidated review matrix](../86_admin_lesson_delete/VERIFICATION_REPORT.md#ac-34-macro-review).
