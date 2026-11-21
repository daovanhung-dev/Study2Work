# Verification Report — API #84 Cập nhật lesson

## Scope

- Updated the 11-file Markdown DD package to reflect the local API #84 implementation and its DERIVED request/schema choices.
- Added the Study Server route/module and focused HTTP tests; updated server-study context registry and runtime/test pages.
- Catalog, AC-34 diagram, DDL/migrations and deployment were not changed.
- DD status remains Draft — Needs Confirmation because the body is absent from direct catalog/diagram evidence and live schema/permissions are unverified.

## Results

- API #84 focused tests: 23 passed.
- Linked #09/#47/#48/#82–#84 regression: 104 passed.
- Full Study Server suite: 1050 passed.
- Ruff across all Study `app` and `tests`: passed.
- OpenAPI: 49 unique `/api/v1` route templates / 55 operations; PUT shares GET #83's `/admin/lessons/{lesson_id}` template and exposes the required DERIVED JSON body.
- DD package: exact 11 Markdown files; all 8 sheet appendix suffixes match the registered templates byte-for-byte.
- Static Markdown checks across the package: 32 tables / 385 data rows with consistent widths; 14 balanced fence markers; 4 JSON examples parse; all 40 local Markdown path references resolve; final newline and no trailing whitespace.
- `git diff --check`: passed. Repo-wide context validator did not pass because the existing DB Admin context/source tree is missing and the recorded baseline commit `9a70eb6764a6587093a92d3bd7e4cc0bea1651c4` is unavailable; `--skip-drift` still reports only the missing DB Admin scope. It reported no API #84/server-study path omission.

## Findings and limits

- The direct catalog and AC-34 diagram specify only `lesson_id`; request body fields and update-column mapping remain DERIVED implementation choices.
- Runtime targets the checked-in legacy BIGINT `lessons` candidate. The V1-PILOT UUID/versioned lesson model is separate, and no live database metadata/migration application was checked.
- API #84 enforces the shared JWT `ADMIN` role. AC-34's fine-grained lesson-management permission has no separate policy in current Study source.
- A legacy row with null `course_id` cannot satisfy reusable API #09 `Lesson`; API #84 safely rolls back and returns 500 instead of inventing a value.
- Tests use fake DB sessions. They verify local HTTP validation, binding, transaction and response behavior, not live PostgreSQL compatibility or deployment.

## AC-34 macro-review

- Status: `VERIFIED_WITH_OPEN_QUESTIONS`; source/document consistency review is not owner approval or live runtime verification.
- API #84 changes metadata only; #85 owns status, #86 owns delete/reference behavior, and AC-34 reloads through #82.
- See the [consolidated review matrix](../86_admin_lesson_delete/VERIFICATION_REPORT.md#ac-34-macro-review).
