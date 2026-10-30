# Plan Result — API #47 Tạo lecture

## Result

- Runtime status: `SOURCE_BACKED` locally; route, module and HTTP tests are wired.
- DD status: `Draft — Needs Confirmation` until the live target schema/migration is verified.
- Scope: API #47 only, plus the shared validation-error path classification needed for this parameterized route. No migration/API #34 behavior was changed for this task.

## Approved decisions implemented

- Request remains `course_id:int64`, `title:string`, `content:int64`, `asset_refs:string`, `order:int32`.
- `content` is stored in `lessons.content` and returned as a base-10 string.
- Only the Mentor whose numeric JWT subject directly matches `courses.mentor_id` may create; assigned courses are excluded.
- Course status is not filtered.
- `asset_refs` is a JSON string of unique signed-int64 IDs; `[]` is valid and response assets preserve request order.
- Resolve uploads only for the same Mentor, purpose `LECTURE` and path course. Any unresolved/ineligible ID uses generic `404 DESIGN_RESOURCE_NOT_FOUND`.
- Insert lesson status `PUBLISHED`; set `created_at` and `updated_at` to `CURRENT_TIMESTAMP`; do not write `resources` or mutate `uploads`.

## API requirement matrix

| API ID | Method/path | Actor/auth | Request | Success/errors | Status |
|---|---|---|---|---|---|
| 47 | POST `/api/v1/mentor/courses/{course_id}/lectures` | Mentor / Bearer JWT | course_id:int64; title:string; content:int64; asset_refs:string(JSON array of int64 IDs); order:int32 | 201 `DESIGN_RESOURCE_CREATED`; 401/403/404/422/500 catalog codes | SOURCE_BACKED locally |

## Data boundary

| Item | Runtime behavior | Evidence boundary |
|---|---|---|
| Course lookup | Read `courses.id, mentor_id`; direct owner check; no status predicate | Legacy SQL artifact; live schema not verified |
| Asset lookup | Batch read scoped `uploads`; skip query for `[]`; restore request order | API #34 source/migration artifact; live schema not verified |
| Lesson insert | Insert course/name/content/sort_order/status/timestamps and commit | Legacy `lessons` mapping; no deployment claim |
| Error handling | Shared auth and response helpers; validation 422; generic asset 404; rollback DB/insert/commit errors | Local HTTP tests |

## Verification

- Focused API #47 tests: `25 passed`.
- Full Study Server suite: `319 passed`.
- Ruff: `All checks passed!`.
- OpenAPI: 18 `/api/v1` paths; API #47 POST and API #34 `/api/v1/uploads` POST are present; request `content` is int64 and response content is string.
- Context validator: only pre-existing DB Admin missing-context/source/link and unavailable historical-snapshot findings; no Study Server/API #47 finding. `--skip-drift` leaves the DB Admin baseline.
- `git diff --check`: passed. Context manifest JSON parses successfully.

## Remaining boundary

No API decision blocks local implementation. The live schema, migration application, database timestamps and deployment remain unverified; therefore the DD stays Draft.
