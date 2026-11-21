# PLAN_RESULT — Study API #97

## Kết quả

- Wired `GET /api/v1/admin/discussions/reported` with the direct catalog
  envelope and success/error codes, plus local `DERIVED` 422 page validation.
- Uses the shared `ADMIN` JWT guard before page parsing and database queries.
- Adds a Study-local legacy BIGINT `discussion_reports` schema candidate in
  migration 014, linked to `discussions.id`. Active queue states are `OPEN` and
  `IN_REVIEW`; reason/severity are exact-match AND filters on the same report.
- Queue grain is one Discussion. Pagination defaults to page 1 / fixed size 20,
  sorted by latest matching report timestamp then discussion ID descending.
- `Discussion.title` derives from normalized content clipped to 120 characters;
  the queue summary returns `comments=[]`. Both are `DERIVED` mappings for
  reusable catalog fields missing from legacy storage or summary behavior.
- Does not add report fields to the catalog response. No report-ingest endpoint
  is included in API #97; live schema, migration deployment, Admin permission
  scope and any report writer remain unverified.
- DD status stays `Draft — Needs Confirmation` because the physical schema and
  projection decisions are local fallbacks.

## AC-37 macro-review

| API | Linked finding |
|---|---|
| #98 | Can reuse `discussion_reports.discussion_id`; its `Page<Discussion>` response still has no report detail fields, and title/thread projection must remain consistent. |
| #99 | Must define action/state/audit behavior and transition active reports out of `OPEN`/`IN_REVIEW`; this API does not mutate them. |
| #100 | Must define delete marker, timestamp, audit and whether deleted discussions remain in the report queue. Migration 014 uses `ON DELETE RESTRICT`, so hard delete must retain/reconcile report evidence or change the approved FK policy. |

## Verification recorded so far

- Focused HTTP tests: 15 passed; linked #92–#95/#97 regression: 102 passed;
  full Study suite: 1315 passed with one upstream Starlette/httpx warning.
- `ruff check app tests` and scoped format check for all touched Python files
  passed. Repo-wide format check reports 60 out-of-scope files that would be
  reformatted; none were rewritten.
- Local OpenAPI exposes 57 `/api/v1` path templates / 68 operations.
- Deno context validation reports existing missing DB Admin context/source
  paths and unavailable source-drift baseline commit; no API #97 source path
  error was reported.
- Markdown, JSON blocks, relative file links, code fences and table column
  counts passed the local checks documented in `VERIFICATION_REPORT.md`.
- All evidence boundaries and the live-schema/report-ingestion limitation are
  recorded in `VERIFICATION_REPORT.md`.
