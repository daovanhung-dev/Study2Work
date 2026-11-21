# VERIFICATION_REPORT — Study API #97

## Scope

Implemented the local API #97 read path, HTTP response projection, query
validation, middleware error classification and Study legacy schema candidate.
No database migration was applied to a live database.

## DD structure and fingerprints

- The registered Markdown template has 8 required sheets. All 8 core output
  filenames match; the folder also contains `OPEN_QUESTIONS.md`,
  `PLAN_RESULT.md`, and this report. Study workflow requires Markdown output
  without a new ZIP.
- Template fingerprint (SHA-256 over ordered filename and per-file hashes):
  `4e21dc80c696a5426b5d470a727d2e0e193e27e0f8560c5597e40315196a7507`.
- Output fingerprint (same method, excluding this report to avoid a
  self-referential hash):
  `42f6406a7889f9df4a50007c3c0654968b7a537bc8bb182156b9fde3884602bc`.
- Validation found 11/11 expected Markdown files, no invalid JSON code blocks,
  unclosed code fences, broken relative file links or inconsistent table
  column counts. Request, response, data mapping and table fields are each
  represented as separate rows.

## Checks

| Check | Result | Evidence boundary |
|---|---|---|
| Focused API #97 HTTP tests | 15 passed | FastAPI `TestClient` with fake DB rows; does not verify PostgreSQL execution |
| Linked #92–#95 plus #97 regression | 102 passed | Verifies adjacent Admin notification OpenAPI counts and API #97 behavior; not a live DB check |
| Full Study suite | 1315 passed; one upstream Starlette/httpx deprecation warning | Current local Study suite |
| Ruff check | Passed: `ruff check app tests` | Static lint over the Study Server app and tests |
| Ruff format | All 12 touched Python files pass scoped check | Repo-wide check reports 60 files outside this task's Python paths would be reformatted; none were rewritten |
| OpenAPI composition | 57 `/api/v1` paths / 68 operations; #97 GET present | Imported local `app.main`; no deployment claim |
| Migration review | Static review only | Migration 014 and `DB.sql` agree; migration was not applied |
| Markdown / JSON / links | Passed; 0 detected issues | Required files, JSON fences, code fences, relative file links and table column counts checked |
| Agent context validator | Exited invalid on existing repository baseline issues | Missing DB Admin context/source paths and unavailable baseline commit for drift checks; it reported no API #97 source/context path error |
| Linked AC-37 review | #98–#100 DD reviewed | Those runtime routes are not present to execute; report/detail/state/audit/delete decisions remain open in their DDs |

## Focused HTTP coverage

- Successful Page projection, exact reason/severity bindings, page offset and
  trace header.
- Default page and empty queue metadata.
- Invalid page rejected before queries.
- Missing token and non-Admin rejected before page parsing or DB query.
- Missing required course/author/status projection maps to 500 and rollback.
- SQLAlchemy query failure and malformed count projection map to 500.
- GET path performs no commit.

## Source gaps retained

The current Study contract/source set has no approved report relation or
report-ingest producer, and legacy `discussions` has no `title` column. The
catalog response has no report detail/count fields although AC-37 describes a
reported-discussion queue. These gaps remain explicit DERIVED fallbacks and
open questions; the implementation does not claim an approved live schema or
add unlisted response fields.

## Runtime boundary

The route is composed and local HTTP tests pass. The new relation is a
`DERIVED` Study migration candidate, not a verified live table. Tests do not
prove migration deployment, actual report insertion, a report-ingest producer,
PostgreSQL execution, fine-grained Admin policy or production behavior. The DD
remains `Draft — Needs Confirmation` because schema and projection choices are
local fallbacks.
