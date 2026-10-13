---
task_id: "2026-10-11-create-study-api21-dd"
date: "2026-10-11"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD cho Study API #21

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `/home/daovanhung/.local/node-v24.21.0-linux-x64/bin/node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: 34 available; selected three; shortage none.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-11/create-study-api16-dd.md`
    - carry_forward: Giữ contract và runtime tách biệt; không suy diễn schema/API từ module khác; ghi rõ SOURCE_REQUIRED khi thiếu bằng chứng.
  - path: `.agents/worklog/2026-10-11/create-study-api17-dd.md`
    - carry_forward: Không tự giải quyết discrepancy; phân loại rõ thiết kế, source hiện tại và NOT_FOUND.
  - path: `.agents/worklog/2026-10-11/create-study-api18-dd.md`
    - carry_forward: Dùng tám sheet template; giữ UNWIRED / NOT_FOUND; tạo OPEN_QUESTIONS, PLAN_RESULT và VERIFICATION_REPORT.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tạo DD Markdown API #21 `GET /api/v1/users/me/progress` tại `apps/study-server/docs/dd/21_users_me_progress/`, cùng reports và worklog; không tạo ZIP.
- Canonical contract/approved DD: `docs/lists/list_api.md` khai báo Student Bearer JWT, query `course_id list hoặc aggregate?:string`, response `ApiEnvelope<UserProfile>`, 200/401/403/500. AC-13 và AC-18 mô tả gọi tổng hợp tiến độ và ghép course/progress; DB design là căn cứ thiết kế, không phải live schema proof.
- Trạng thái tài liệu: `Draft — Needs Confirmation`; không tự quyết semantics query, công thức aggregate hoặc payload.

## CURRENT_BEHAVIOR

- Source/config: Router `apps/study-server/app/api/v1.py` không khai báo `/users/me/progress`; inventory app không có module API #21. `lesson_progress` cùng quan hệ lesson/course có trong DB design/DDL checked-in, nhưng API query chưa được triển khai.
- Runnable tests: Inventory Study tests không có test API #21.
- Runtime wiring: `UNWIRED / NOT_FOUND`. Shared Student JWT helper và response envelope hiện có, nhưng chưa được API #21 gọi.

## SOURCE_TRACE

~~~text
Student -> API #21 catalog / AC-13 + AC-18
-> design-only aggregation from lesson_progress and course/lesson relations
-> ApiEnvelope<UserProfile> per catalog (payload mapping unresolved)
Current Study route/module/query/test -> NOT_FOUND / UNWIRED
~~~

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Query semantics | Catalog says `course_id list hoặc aggregate?:string`, without a clear type/grammar or behavior. | SOURCE_REQUIRED | Keep exact declaration and leave validation/query semantics open. |
| Aggregation | AC-18 names user-level aggregation and lesson/quiz/assignment progress; formula, inclusion rules and granularity are absent. | SOURCE_REQUIRED | Do not invent percentage/status calculations. |
| Response shape | Catalog declares `ApiEnvelope<UserProfile>` while use cases require progress aggregate data. | DISCREPANCY / SOURCE_REQUIRED | Preserve catalog type and mark payload mapping unresolved. |
| Current-user scope | Endpoint is `/me`; DB design has `lesson_progress.user_id`, but API-specific JWT-to-query binding is absent. | SOURCE_REQUIRED | Record candidate identity relationship without claiming runtime predicate. |
| Runtime | No API #21 route/module/query/test found. | UNWIRED / NOT_FOUND | Do not claim endpoint or tests are verified. |

## CHANGES

- Files changed: Created eight template sheets and OPEN_QUESTIONS.md, PLAN_RESULT.md, VERIFICATION_REPORT.md under apps/study-server/docs/dd/21_users_me_progress/; completed this worklog.
- CONTEXT_UPDATES: None expected; docs-only task.
- Context pages changed: None expected.
- Assumptions: Preserve existing user changes; no runtime/catalog/diagram/schema edits; use Draft and open questions; no ZIP.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| /home/daovanhung/.local/node-v24.21.0-linux-x64/bin/node scripts/select-worklogs.mjs --type docs --limit 3 | Selected #16–#18 worklogs; all read; no shortage. | VERIFIED |
| Source/contract/diagram/schema/runtime inventory review | Compared API catalog, AC-13/AC-18, DB design and checked-in DDL, current route/auth/envelope, module and test inventory. | VERIFIED |
| Inline Python DD static checker | 11 Markdown deliverables; eight ordered sheets and three reports; 41 local links/anchors; two JSON examples; table widths, front matter, code fences, catalog tokens and output fingerprints passed. | VERIFIED |
| Authored DD/worklog whitespace scan | No trailing whitespace in the 11 DD files or this worklog. | VERIFIED |
| git diff --check | No whitespace errors. | VERIFIED |
| API #21 route/module/test inventory | No route, module, query implementation or focused test found. | UNWIRED / NOT_FOUND |
| Study Server runtime tests | Not run; documentation-only scope and API #21 is not wired. | NOT_RUN |
| Context validator | Not required; no canonical context page or manifest changed. | NOT_REQUIRED |

## HANDOFF

- Remaining blockers: Contract-owner decisions listed in OPEN_QUESTIONS.md are needed before DD can be marked Ready/Final or used as implementation contract.
- Next owner/action: Resolve query grammar, aggregate formula/scope, response schema, identity binding and empty-result wire shape in canonical sources; then update the DD.
