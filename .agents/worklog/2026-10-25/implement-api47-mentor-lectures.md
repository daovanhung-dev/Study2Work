---
task_id: "2026-10-25-implement-api47-mentor-lectures"
date: "2026-10-25"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "COMPLETE"
---

# Worklog: Implement API #47 Tạo lecture

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type coding --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-25/implement-api34-upload-assets.md`
    - carry_forward: Dùng legacy BIGINT `uploads` metadata; API #47 chỉ resolve assets cùng Mentor, purpose `LECTURE`, cùng course; không ghi `resources` hoặc mutate `uploads`; live schema chưa xác minh.
  - path: `.agents/worklog/2026-10-25/remove-errordetail-study-server.md`
    - carry_forward: Giữ error envelope/status/business codes/trace behavior; dùng shared response helpers; phân biệt validator baseline toàn repo.
  - path: `.agents/worklog/2026-10-25/reorganize-api34-student-module.md`
    - carry_forward: Giữ source API #34 ở `student/api_34_uploads`; bảo toàn mọi thay đổi worktree sẵn có.
- shortage: `none` (selector có 39 coding worklogs và chọn đủ 3)

## EXPECTED_BEHAVIOR

- Requirement: Wire `POST /api/v1/mentor/courses/{course_id}/lectures` theo DD #47 và quyết định người dùng: `content:int64` được lưu/trả như chuỗi thập phân; chỉ Mentor trực tiếp sở hữu course; không lọc trạng thái course; tạo lecture `PUBLISHED`; asset thiếu hoặc ngoài scope đều trả 404 chung.
- Canonical contract/approved decisions: Request giữ `course_id:int64`, `title:string`, `content:int64`, `asset_refs:string` chứa JSON array ordered unique int64 IDs (`[]` hợp lệ), `order:int32`; response là `ApiEnvelope<Lecture>` với assets từ UploadAsset metadata API #34. Legacy BIGINT schema là source target; live DB chưa xác minh.

## CURRENT_BEHAVIOR

- Source/config: API #47 có route/module; shared auth guard yêu cầu `MENTOR`; source dùng direct `courses.mentor_id`, query `uploads` theo owner/purpose/course, INSERT `lessons` với `PUBLISHED`, decimal-string content và `CURRENT_TIMESTAMP`. Live schema/migration chưa xác minh.
- Runnable tests: API #47 focused suite có 25 tests; lần full-suite gần nhất có 319 tests.
- Runtime wiring: OpenAPI compose có 18 API v1 paths, gồm `POST /api/v1/mentor/courses/{course_id}/lectures` và `POST /api/v1/uploads`.

## SOURCE_TRACE

```text
POST /api/v1/mentor/courses/{course_id}/lectures -> shared Mentor JWT guard -> validate request -> direct course owner check -> resolve scoped uploads -> INSERT lessons and commit -> Lecture envelope -> focused HTTP tests
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| `content:int64` to legacy TEXT | DD marked semantics unresolved; user approved decimal-string persistence and response. | `RESOLVED_BY_USER` | Keep request integer; map with `str(content)` to `lessons.content`. |
| Course access/status | DD listed assignment and status policy as open; user approved direct owner, any course status. | `RESOLVED_BY_USER` | Query `courses.mentor_id`; no course status predicate. |
| Asset non-resolution | DD left missing/out-of-scope mapping open; user approved generic 404. | `RESOLVED_BY_USER` | Do not disclose whether an asset exists outside scope. |
| Live schema | Only legacy DDL/migration artifacts are available; no live metadata probe. | `NOT_VERIFIED_HERE` | Implement against checked-in legacy BIGINT source only; do not claim deployment. |

## CHANGES

- Files changed: API #47 mentor module, route composition, API error classification for parameterized routes, focused API #47 tests, API #47 DD sheets/decision log/reports, server-study context/manifest, this worklog.
- CONTEXT_UPDATES: Applied; validator found only the pre-existing DB Admin baseline and unavailable historical snapshot commit, with no Study Server/API #47 findings.
- Context pages changed: `AGENTS.md`, `architecture.md`, `apis/declared-routes.md`, `core/database-security.md`, `core/runtime.md`, `database.md`, `modules/README.md`, `tests.md`.
- Assumptions: Title max 200 is derived from legacy `lessons.name VARCHAR(200)`; preserve no trim/minimum rule. Required lesson timestamps use `CURRENT_TIMESTAMP` and are not included in the API response.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run --allow-read scripts/select-worklogs.mjs --type coding --limit 3` | Selected three same-type worklogs; all were reviewed. | VERIFIED |
| Focused API #47 tests | `uv run pytest -q tests/modules/mentor/api_47_mentor_lectures_create` — 25 passed; one existing Starlette/httpx deprecation warning. | VERIFIED |
| Full Study Server tests | `uv run pytest -q` — 319 passed; one existing Starlette/httpx deprecation warning. | VERIFIED |
| Ruff | `uv run ruff check app tests` — all checks passed. | VERIFIED |
| OpenAPI/import verification | 18 `/api/v1` paths; API #47 POST and API #34 uploads POST present; request content is integer/int64 and response content is string. | VERIFIED |
| Context manifest | JSON parse passed; source/test paths for all API #47 module files are listed. | VERIFIED |
| DD Markdown checks | 11 files, 10 resolving relative links, 3 valid JSON examples and 31 consistent Markdown table groups; template set SHA256 `3dc7fd2242dd1ed1bd9faba50aadad913a31b97ebf1392d6144bb905c5208137`. | VERIFIED_STATIC_ONLY |
| Context validator | Full and `--skip-drift` runs report missing DB Admin context/source/links; full mode also cannot inspect unavailable historical snapshot commit. No Study Server/API #47 errors. | BLOCKED_BY_REPOSITORY_BASELINE |
| `git diff --check` | No whitespace errors. | VERIFIED |

## PRE_VERIFICATION_CHECKPOINT

Implementation, DD and context edits are complete. Final verification results
are recorded above; context validator baseline is documented without changes
to out-of-scope DB Admin context.

## HANDOFF

- Remaining boundary: Live database schema, migration application and deployment remain unverified; DD stays Draft until those are confirmed.
- Next owner/action: None for local API #47 implementation; validate the target live schema before treating the DD as final or deploying.
