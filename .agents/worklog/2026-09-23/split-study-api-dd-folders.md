---
task_id: "2026-09-23-split-study-api-dd-folders"
date: "2026-09-23"
primary_task_type: "coding"
secondary_task_types: ["test", "docs", "context-maintenance"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tách Study API modules theo DD API

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type coding --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-09-22/implement-study-api2-verify-email-send.md`
    - carry_forward: Giữ canonical envelope, trace handling, source-backed boundary và không suy diễn live DB từ schema/source artifact.
  - path: `.agents/worklog/2026-09-22/implement-study-api4-users-me.md`
    - carry_forward: Bảo toàn namespace/runtime contract hiện tại, query parameterized và không thay đổi public response behavior.
  - path: `.agents/worklog/2026-09-22/implement-study-api5-categories.md`
    - carry_forward: Dùng `apps/study-server/.venv` cho focused/full checks; context validator có thể báo source drift nền.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Mỗi API runtime #1–#7 có module folder riêng theo API ID/DD mapping.
- Public routes, request/response contract, business code, SQL behavior, transaction behavior và database contract không thay đổi.
- API #6 và #7 tách riêng; types/helper dùng chung nằm dưới shared course-catalog boundary.
- API #8–#13 tiếp tục unwired, không tạo skeleton.

## CURRENT_BEHAVIOR

- `guest/courses` đang gộp API #6 và #7 trong cùng `models.py`, `query.py`, `view.py`.
- API #1–#5 đang dùng folder semantic không có API ID.
- Router và tests import trực tiếp các folder cũ.
- Context pages và manifest còn mô tả các path cũ.
- Baseline Study suite đã verified ở 134 tests; live DB chưa được verify.

## SOURCE_TRACE

```text
DD API #1–#7
-> guest/api_0N_* module boundary
-> app/api/v1.py route imports
-> focused tests under tests/modules/guest/api_0N_*
-> full Study test suite + Ruff/Mypy + context validator
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #6/#7 shared current folder | `app/modules/guest/courses/*` owns both list and search flows | RESOLVED_FOR_IMPLEMENTATION | Split API-specific models/query/view and extract only shared course types/helpers |
| API #8–#13 source | DD folders exist, runtime modules/routes do not | UNWIRED / OUT_OF_SCOPE | Do not create skeleton or behavior |
| Live database | Source/schema artifacts exist but live metadata is not verified | SOURCE_REQUIRED | No migration or live DB operation |
| Context snapshot | Full validator reports pre-existing source drift | CONTEXT_STALE | Run validator with drift status; do not refresh snapshot solely to clear it |

## CHANGES

- API #1–#5 runtime modules moved to API-ID folders under
  `apps/study-server/app/modules/guest/`.
- API #6 and #7 were split into `api_06_courses` and
  `api_07_courses_search`; shared course response models, pagination, sort
  allow-list/order building, row mapping and decimal-price serialization live
  under `_shared/course_catalog`.
- Router imports and tests now use the API-ID namespaces. Public routes,
  response envelopes, business codes, SQL predicates, transaction behavior and
  database contract remain unchanged. API #3 retains login and refresh.
- API #8–#13 remain unwired; no source skeleton, migration or live DB operation
  was added.
- CONTEXT_UPDATES: updated `server-study` route, architecture, runtime,
  module, register and test pages plus manifest required source paths.
- Context pages changed: `.agents/server-study/apis/declared-routes.md`,
  `.agents/server-study/architecture.md`,
  `.agents/server-study/core/runtime.md`,
  `.agents/server-study/modules/README.md`,
  `.agents/server-study/modules/register-account.md`,
  `.agents/server-study/tests.md`, and `.agents/context-manifest.json`.
- Assumptions: API #3 owns login and refresh because refresh has no separate DD;
  public paths remain unchanged; live database metadata remains unverified.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run --allow-read scripts/select-worklogs.mjs --type coding --limit 3` | Selected 3 matching coding worklogs; all read | VERIFIED |
| Focused API #1–#7 pytest paths | `102 passed` | VERIFIED |
| `.venv/bin/pytest -q` | `134 passed, 1 warning` | VERIFIED |
| `.venv/bin/ruff check app tests` | `All checks passed` | VERIFIED |
| `.venv/bin/mypy app` | `Success: no issues found in 60 source files` | VERIFIED |
| composition-root import check | `8 /api/v1` | VERIFIED |
| `git diff --check` and legacy import/path grep | clean; no matches | VERIFIED |
| `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs --skip-drift` | `AGENT_CONTEXT_OK` | VERIFIED |
| full context validator | `CONTEXT_STALE` in pre-existing repository snapshots across scopes | RECORDED_DISCREPANCY |

## HANDOFF

- Remaining blockers: no runtime or static-check blockers.
- Context limitation: the full validator still reports repository-wide source
  snapshot drift, including deleted legacy paths; the drift was recorded and
  not used as a reason to rewrite unrelated context snapshots.
- Next owner/action: review the API-ID module split; API #8–#13 require a
  separate source-backed implementation task.
