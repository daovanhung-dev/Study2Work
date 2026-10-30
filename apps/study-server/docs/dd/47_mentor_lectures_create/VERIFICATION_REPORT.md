# Verification Report — API #47 Tạo lecture

## Scope

Implemented and verified the local API #47 route/module/tests. Its AC-21 follow-through now persists non-empty ordered asset references in `lesson_uploads` in the lesson transaction for API #48. DD remains `Draft — Needs Confirmation` because live database schema and migration deployment are not verified.

## Runtime and contract checks

| Check | Result | Status |
|---|---|---|
| Route composition | OpenAPI includes `POST /api/v1/mentor/courses/{course_id}/lectures`; the current app also wires API #48. | VERIFIED |
| API #34 route retained | OpenAPI includes `POST /api/v1/uploads`. | VERIFIED |
| Request model | `content` is integer with `int64` format; `order` is signed int32; `title` max length is 200; `asset_refs` is a required string. | VERIFIED |
| Response model | Runtime maps `content` to the decimal string from API #47's required integer input; shared Lecture schema permits null for API #48 database reads. | VERIFIED |
| Focused HTTP tests | `26 passed` in API #47 file; includes auth/role, numeric/title validation, asset JSON/range/duplicates/empty, course access, generic asset 404, output ordering, atomic relation write and rollback. | VERIFIED |
| Focused linked API tests | API #47 + #48: `42 passed`. | VERIFIED |
| Full Study Server suite | `336 passed`; one existing Starlette/httpx deprecation warning. | VERIFIED |
| Ruff | `uv run ruff check app tests` — all checks passed. | VERIFIED |
| Context manifest | JSON parses successfully and includes API #47/#48 module/test and migration source paths. | VERIFIED |
| Diff whitespace | `git diff --check` — no errors. | VERIFIED |
| DD Markdown static checks | 11 Markdown files; 10 relative links resolve; 3 JSON examples parse; 31 table groups have consistent column counts. | VERIFIED_STATIC_ONLY |

## DD template baseline

- Template folder: `.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/`.
- Eight template sheets were read in their current order from `00_Cover.md` through `07_table.md`.
- Combined SHA-256 over sorted filenames and file contents: `3dc7fd2242dd1ed1bd9faba50aadad913a31b97ebf1392d6144bb905c5208137`.

## Context validator

`deno run --allow-read --allow-env scripts/validate-agent-context.mjs` reports `AGENT_CONTEXT_INVALID` due pre-existing missing DB Admin context pages, `apps/db-admin-web`/`apps/db-admin-server` source roots and links, plus unavailable historical snapshot commit `9a70eb6764a6587093a92d3bd7e4cc0bea1651c4`. The validator output contains no Study Server/API #47 finding. Running with `--skip-drift` removes the missing-snapshot findings and leaves the same DB Admin baseline failures.

## Source and deployment boundary

- API #47 tests use fake DB query/session responses; they verify application behavior, not a live PostgreSQL schema.
- The checked-in legacy `courses`, `lessons`, `uploads` and `lesson_uploads` DDL/migration artifacts have not been applied or inspected on a live database.
- Object Storage is outside API #47 writes; API #47 only reads the persisted `uploads` metadata.
