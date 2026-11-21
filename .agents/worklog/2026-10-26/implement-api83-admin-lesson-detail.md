---
task_id: "2026-10-26-implement-api83-admin-lesson-detail"
date: "2026-10-26"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: ["AC-34 Admin lesson flow APIs #82-#86", "API #09 reusable Lesson"]
status: "VERIFIED"
---

# Worklog: Implement API #83 Admin lesson detail

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type coding --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-26/implement-api74-admin-course-detail.md`
    - carry_forward: use shared ADMIN guard, parse raw signed-int64 path after auth, map malformed ID to catalog 404, and use safe rollback for read failures.
  - path: `.agents/worklog/2026-10-26/implement-api75-admin-course-update.md`
    - carry_forward: preserve the dirty worktree and keep write/transaction behavior inside view orchestration.
  - path: `.agents/worklog/2026-10-26/implement-api76-admin-course-status.md`
    - carry_forward: separate legacy BIGINT from V1-PILOT UUID schema and do not claim live schema/deployment from local tests.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: `GET /api/v1/admin/lessons/{lesson_id}`, Bearer JWT, Admin role, required signed `int64` path, direct `ApiEnvelope<Lesson>`, HTTP 200 and catalog errors 401/403/404/500.
- Canonical contract/approved DD: API catalog row #83 and AC-34 diagram; DD package `apps/study-server/docs/dd/83_admin_lesson_detail/` remains `Draft — Needs Confirmation`.
- Dependency phrase in AC-34 has no response field/output definition. Keep direct `Lesson` output and do not read dependency tables without a defined purpose. API #86 must check current references at deletion time.
- Source precedence: current executable Study conventions and schema candidates; legacy BIGINT `lessons` is a candidate, while V1-PILOT UUID lessons are incompatible. Do not infer deployed schema.

## CURRENT_BEHAVIOR

- Source/config: API #82 is wired with shared `ADMIN` JWT guard and legacy `lessons` projection. API #83 route/module/test are absent. `error_response` defaults to `data: null`; middleware path-template allowlist contains #82 but not #83.
- Runnable tests: API #09 and #82 suites exist; #83 has no tests. API #74 is the local precedent for raw signed-int64 path parsing, shared Admin guard, keyed detail query, 404 and safe rollback.
- Runtime wiring: FastAPI composition currently contains 48 paths / 53 operations before this task; route import/full app test evidence must be refreshed after changes.
- Schema evidence: legacy `lessons` has BIGSERIAL id, nullable `course_id`, required `name`, nullable `content`/`video_url`, nullable/defaulted `sort_order` and `status`. Required `Lesson.course_id` cannot represent a NULL candidate row. V1-PILOT `lessons` uses UUID/chapter/course-version fields.

## SOURCE_TRACE

```text
GET route -> pass raw path/header/Session/trace -> shared ADMIN JWT guard
-> signed-int64 parser -> one bound query on lessons.id -> strict reusable Lesson mapping
-> 200 direct Lesson envelope; malformed ID or absent row -> catalog 404
-> DB/projection failure -> rollback + safe catalog 500; no writes
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| AC-34 “lesson + dependencies” | Catalog response is direct `Lesson`; no dependency fields; diagram does not define dependency output | `DISCREPANCY / SOURCE_REQUIRED` | Keep response/query limited to Lesson; dependency behavior remains open |
| Admin auth | Current API #82 and shared guard support role `ADMIN`; fine-grained lesson-management policy has no source | `DERIVED / SOURCE_REQUIRED` | Reuse role guard only; retain dedicated permission gap |
| Legacy vs V1-PILOT lesson schema | `infra/postgres/study-server/DB.sql` is BIGINT legacy; `infra/postgres/02_study_db.sql` is UUID pilot | `DISCREPANCY` | Implement against legacy candidate matching current #82; do not claim live compatibility |
| Nullable legacy `course_id` | DDL allows NULL; reusable Lesson requires int64 | `DISCREPANCY` | Reject incomplete projection with safe 500 and rollback |
| Malformed path ID | Catalog has no 422; API #74 maps malformed/out-of-range to 404 | `DERIVED` | Use raw path and custom parser after auth |
| Optional fields / status | API #09 model preserves null `content`/`video_url`; no complete LessonStatus enum exists | `SOURCE_BACKED / SOURCE_REQUIRED` | Preserve optional nulls and source status unchanged |
| Dependencies / live deployment | No live DB verification or defined dependency response | `UNVERIFIED` | No joins, migration or deployment claim |

## CHANGES

- Files changed: API #83 module (`__init__.py`, `models.py`, `query.py`, `validate.py`, `view.py`); `app/api/v1.py`; `app/core/middleware.py`; new API #83 TestClient suite; API #82 OpenAPI regression expectation; API #83 DD (`02_Overview.md`, `03_Request.md`, `04_Response.md`, `05_Data_Mapping.md`, `06_Error.md`, `OPEN_QUESTIONS.md`, `PLAN_RESULT.md`, `VERIFICATION_REPORT.md`); `.agents/context-manifest.json`; `.agents/project/source-status.md`; `.agents/server-study/AGENTS.md`, `architecture.md`, `apis/declared-routes.md`, `modules/README.md`, `tests.md`; this worklog.
- CONTEXT_UPDATES: registered the five API #83 source files and test in both tracked/required manifest paths; documented local route behavior and unresolved schema/policy boundaries.
- Context pages changed: `.agents/server-study/AGENTS.md`, `architecture.md`, `apis/declared-routes.md`, `modules/README.md`, `tests.md`, `.agents/project/source-status.md`, and `.agents/context-manifest.json`.
- Assumptions: legacy BIGINT query matches adjacent #82 implementation; invalid raw `lesson_id` uses catalog 404 following #74; no fine-grained permission claim.
- Scope boundary: preserve all pre-existing dirty files and edits; do not stage or commit.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| Context/router/worklog preflight and current source/schema review | Exact coding worklog selector chose #74/#75/#76; source and schema conflicts recorded before edits | PASS |
| `uv run pytest -q tests/modules/admin/api_83_admin_lesson_detail/test_admin_lesson_detail.py` | 15 passed | PASS |
| `uv run pytest -q` for #83 + #82 + #74 + #09 | 54 passed; one upstream Starlette/httpx deprecation warning | PASS |
| `uv run pytest -q` | 1027 passed; one upstream Starlette/httpx deprecation warning | PASS |
| `uv run ruff check app tests` | All checks passed | PASS |
| OpenAPI composition inspection | 49 `/api/v1` path templates / 54 operations; #83 GET documents int64 path and exact 401/403/404/500 errors, no 422 | PASS |
| DD static review | 11 Markdown files; template appendix parity 8/8; 3/3 JSON blocks parse; 29 tables / 377 body rows; 39 local references including 21 anchors resolve; template and output fingerprints recorded | PASS |
| `git diff --check` | Clean | PASS |
| `deno run --allow-read --allow-env scripts/validate-agent-context.mjs` | Fails on pre-existing DB Admin files/context links absent from checkout and sourceCommit fingerprints pointing to unavailable commit `9a70eb6764a6587093a92d3bd7e4cc0bea1651c4`; no #83 path error reported | FAIL — BASELINE / OUT OF SCOPE |

## HANDOFF

- Remaining blockers: live schema, fine-grained Admin permission, dependency output definition and soft-delete visibility remain source/owner questions. Context validator has unrelated DB Admin/baseline-commit failures; API #83 changes introduced no reported path error.
- Next owner/action: complete local implementation and verification; keep the DD in Draft and report runtime evidence limits.
