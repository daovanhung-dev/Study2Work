---
task_id: "2026-10-26-implement-api84-admin-lesson-update"
date: "2026-10-26"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "PARTIAL"
---

# Worklog: Implement Admin Lesson Update API #84

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type coding --limit 3` (Node is unavailable)
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-26/implement-api76-admin-course-status.md`
    - carry_forward: Reuse Admin guard, signed-int64 raw path validation, safe transaction handling, catalog error codes, and isolated state ownership.
  - path: `.agents/worklog/2026-10-26/implement-api75-admin-course-update.md`
    - carry_forward: PUT without a catalog body used a documented full-replacement DERIVED fallback; validate and project before commit, then rollback on failure.
  - path: `.agents/worklog/2026-10-26/implement-api74-admin-course-detail.md`
    - carry_forward: Follow existing direct Admin detail response shape and safe projection/mapping conventions.
- Additional reviewed worklogs: API #83 detail and selected API #74–#76 logs were read; the API #83 path/auth and error-envelope conventions are current.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Implement `PUT /api/v1/admin/lessons/{lesson_id}` for an Admin, returning one `ApiEnvelope<Lesson>` with HTTP 200 `DESIGN_RESOURCE_UPDATED`; preserve catalog errors 401/403/404/422/500.
- Canonical contract/approved DD: Catalog #84 and AC-34 diagram directly specify method, path, Admin JWT, signed int64 path, direct Lesson response, success/error codes, and an UPDATE action followed by list reload. They do not specify body fields or mutation columns. DD #84 is Draft — Needs Confirmation.
- Explicit DERIVED implementation fallback, selected for this coding task: full-replacement JSON body with required `title: string` (maximum 200 characters from legacy DDL/API #47 precedent), `content: string | null`, `video_url: string | null`, and `order: int32`. Null content/video URL clears the respective nullable field. No URL-format constraint is added because reusable `Lesson.video_url` is `str | None`.
- Mutation fallback: one bound `UPDATE lessons` by `id`, setting name/content/video_url/sort_order and `updated_at=CURRENT_TIMESTAMP`, returning the direct Lesson projection. Preserve `course_id`, `status`, `created_at`, lesson uploads/resources/progress, and audit data. No live DB/migration claim is made.

## CURRENT_BEHAVIOR

- Source/config at task start: APIs #82 and #83 were wired at the Admin lesson list/detail routes. No API #84 module or PUT route existed. The trace middleware already listed `/api/v1/admin/lessons/{lesson_id}`. Shared auth supported `role="ADMIN"`. `error_response` defaulted `data` to `None`.
- Runnable tests: API #83 tests cover direct Lesson mapping, Admin auth, signed-int64 path behavior, not-found, safe DB errors, and rollback. API #75 tests cover update request, transaction, commit and rollback patterns. API #47 tests/source show lesson creation and `lesson_uploads` are separate concerns.
- Runtime wiring at task start: API #84 was `UNWIRED` / `NOT_FOUND`; no endpoint behavior had been verified for it. Existing route template for #83 can serve both GET and PUT.

## SOURCE_TRACE

```text
Typed JSON body validation in FastAPI -> PUT router (#84) -> Admin update view -> shared ADMIN auth -> raw signed-int64 path validation -> one UPDATE ... RETURNING through query_one -> Lesson #09 projection -> commit after valid mapping -> ApiEnvelope<Lesson>
```

- Existing callers/adjacent behavior: AC-34 client reloads through API #82; #83 reads the same `lessons` projection; #85 owns status changes; #86 owns deletion/reference policy; #47 creates lessons and separately links UploadAsset rows through `lesson_uploads`.
- Database side effect: candidate legacy `lessons` columns only. No mutation of `lesson_uploads`, `resources`, `lesson_progress`, course association, status or audit records.
- Tests affected: new focused API #84 HTTP tests; linked #82/#83/#47/#48/#85/#86 boundaries remain unchanged.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Request body | Catalog row and AC-34 node specify path only; PUT node says UPDATE; API #75 precedent used a body proposal | `DISCREPANCY` / DERIVED fallback | Implement four-field full replacement and retain DD Draft status. |
| Physical schema | Legacy `DB.sql` has BIGINT `lessons`; V1-PILOT uses UUID/versioned lesson model | `SOURCE_REQUIRED` for live target | Code follows legacy API #09/#82/#83 mapping; no live-schema claim. |
| Response nullability | Legacy `course_id` is nullable; reusable `Lesson.course_id` is required | `DISCREPANCY` | Reject incomplete projection safely, rollback, and return 500. |
| Timestamp owner | Legacy DDL has `updated_at`; API #75 uses server timestamp; no lesson trigger was found in checked Study DDL | `DERIVED` | Set updated_at in the update statement; verify only against checked repository DDL. |
| Admin permission | Catalog says role Admin; AC-34 says lesson-management permission; current shared guard enforces ADMIN role | `DISCREPANCY` | Reuse current guard and record that no separate fine-grained permission policy exists. |
| Body/auth order | FastAPI validates the typed body before invoking the endpoint; auth runs in the view | `DISCREPANCY` | Invalid unauthenticated body may return 422 before 401; no DB query or mutation occurs. |
| Error data shape | API guideline/current response helper specify null data on errors | `VERIFIED` | DD claims that helper returns `{}` are stale and must be corrected. |

## CHANGES

- Files changed: `apps/study-server/app/api/v1.py`; `apps/study-server/app/modules/admin/api_84_admin_lesson_update/{__init__.py,models.py,query.py,validate.py,view.py}`; `apps/study-server/tests/modules/admin/api_84_admin_lesson_update/test_admin_lesson_update.py`; `.agents/context-manifest.json`; `.agents/server-study/{AGENTS.md,architecture.md,apis/declared-routes.md,core/runtime.md,modules/README.md,tests.md,workflows/README.md}`; and all 11 Markdown files in `apps/study-server/docs/dd/84_admin_lesson_update/`.
- CONTEXT_UPDATES: Registry, current scope/route/module/test pages, workflow history and DD #84 now describe the DERIVED fallback, local verification, and remaining live-schema/permission gaps.
- Context pages changed: `.agents/context-manifest.json`, `.agents/server-study/AGENTS.md`, `architecture.md`, `apis/declared-routes.md`, `core/runtime.md`, `modules/README.md`, `tests.md`, and `workflows/README.md`. `INDEX.md` did not need routing changes.
- Assumptions: Signed int64 path failures map to 422 because #84 directly includes 422 and the adjacent PUT #75 uses 422; the GET #83 404 behavior is not copied. Required body members use strict types and forbid extras. Empty title is not newly prohibited; max 200 is the only title constraint. Order uses the legacy INT/int32 shape with no positivity or uniqueness rule. A nullable legacy `course_id` that cannot satisfy Lesson remains a safe 500.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `.venv/bin/pytest -q tests/modules/admin/api_84_admin_lesson_update/test_admin_lesson_update.py` | 23 passed; one Starlette/httpx deprecation warning | `VERIFIED` |
| `.venv/bin/pytest -q tests/modules/guest/api_09_courses_curriculum/test_courses_curriculum.py tests/modules/mentor/api_47_mentor_lectures_create/test_mentor_lectures_create.py tests/modules/mentor/api_48_mentor_lecture_detail/test_mentor_lecture_detail.py tests/modules/admin/api_82_admin_lessons_list/test_admin_lessons_list.py tests/modules/admin/api_83_admin_lesson_detail/test_admin_lesson_detail.py tests/modules/admin/api_84_admin_lesson_update/test_admin_lesson_update.py` | 104 passed; one Starlette/httpx deprecation warning | `VERIFIED` |
| `.venv/bin/pytest -q` from `apps/study-server/` | 1050 passed; one Starlette/httpx deprecation warning | `VERIFIED` |
| `.venv/bin/ruff check app tests` from `apps/study-server/` | All checks passed | `VERIFIED` |
| OpenAPI inspection via `create_app(...).openapi()` | 49 `/api/v1` route templates / 55 operations; lesson path has GET and PUT | `VERIFIED` |
| DD static check | 11 files; 8/8 appendix parity; 32 tables/385 rows; 4 JSON blocks parse; 14 balanced fence markers; 40 local paths resolve; no trailing whitespace | `VERIFIED` |
| `git diff --check` from repository root | No diagnostics | `VERIFIED` |
| `deno run --allow-read --allow-env scripts/validate-agent-context.mjs` | Fails on pre-existing missing `.agents/db-admin`/`apps/db-admin-*` sources and unavailable baseline source commit `9a70eb6764a6587093a92d3bd7e4cc0bea1651c4`; no API #84/server-study missing-path finding was reported. `--skip-drift` removes baseline commit findings but still fails on missing DB Admin scope. | `PARTIAL` |

## HANDOFF

- Remaining blockers: The repo-wide context validator cannot pass while the unrelated DB Admin scope files and baseline commit are absent. Live DB schema, timestamp triggers and fine-grained lesson-management policy remain unverified.
- Next owner/action: API #84 implementation is complete locally; continue the broader sequence with API #85. Do not claim live DB/deployment verification.
