# VERIFICATION_REPORT — Study API #58

## Kết quả

- API #58: `SOURCE_BACKED_WITH_DERIVED_PROJECTIONS`; route, view, SQL constants, response models and HTTP tests are wired locally.
- DD status remains `Draft — Needs Confirmation`. The collection response, legacy BIGINT support schema, lifecycle values, no-pagination behavior and attachment relation are implementation fallbacks selected under the user's direction; they are not live-schema evidence or contract-owner approval.
- Runtime DB, migration application and deployment were not accessed or verified.

## Deliverable scope

| Nhóm | Kết quả |
|---|---|
| API module | `api_58_mentor_support_requests` models/query/view added; route and exact-path middleware contract wired. |
| Persistence | Legacy `DB.sql` plus migration 008 define `support_requests`, `support_messages` and ordered `support_message_uploads`. Migration remains unapplied here. |
| Contract | DD updated; catalog and AC-24 diagram synchronized to collection shape and 422 query-validation behavior. |
| Tests | Focused API #58 TestClient module covers response, auth/scope, filtering, errors and OpenAPI. |
| Context | Server-study pages and context manifest updated to include API #58 and its source boundaries. |

## Checks

| Check | Result | Status |
|---|---|---|
| Focused API #58 tests | 12 passed; one upstream Starlette/httpx deprecation warning from TestClient. | PASS |
| Full Study Server suite | 550 passed; same upstream warning. | PASS |
| Ruff | `uv run ruff check app tests` reported all checks passed. | PASS |
| OpenAPI | Focused test verifies collection response and int64 `course_id`; `app.openapi()` reports 28 API v1 path templates and 29 operations. | PASS |
| Live database / migration | Not queried or applied. | NOT VERIFIED |
| Agent context validator | Full run returns `AGENT_CONTEXT_INVALID` for missing DB Admin context/source and reports broad existing `CONTEXT_STALE` source drift. `--skip-drift` leaves only the unrelated missing DB Admin context/source errors; Study context references validate. | FAILED — REPOSITORY BASELINE |
| `git diff --check` | No whitespace errors. | PASS |

## AC-24 linked API review

Reviewed #59 detail, #60 reply and #61 resolve boundaries. API #59 can reuse the selected request/message model and direct course-owner predicate. API #60 owns message insertion; API #61 owns status resolution. They remain outside this implementation and must make their own decisions about write payloads, transitions and retries.
