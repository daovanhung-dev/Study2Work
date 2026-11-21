---
task_id: "2026-10-11-create-study-api22-dd"
date: "2026-10-11"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD cho Study API #22

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `/home/daovanhung/.local/node-v24.21.0-linux-x64/bin/node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `35 available; selected 3; shortage none`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-11/create-study-api16-dd.md`
    - carry_forward: Tách expected/current behavior; giữ missing business/schema evidence ở SOURCE_REQUIRED; contract thiết kế không chứng minh runtime.
  - path: `.agents/worklog/2026-10-11/create-study-api17-dd.md`
    - carry_forward: Giữ API/DB gaps và discrepancy thành câu hỏi; không tự thêm provider, query hoặc behavior.
  - path: `.agents/worklog/2026-10-11/create-study-api18-dd.md`
    - carry_forward: Dùng template 8 sheet; giữ UNWIRED/NOT_FOUND; không tạo ZIP cho Study API DD theo workflow hiện hành.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tạo Markdown DD draft cho API #22 `GET /api/v1/lessons/{lesson_id}/access` trong `apps/study-server/docs/dd/22_lessons_access/`, gồm 8 sheet template và `OPEN_QUESTIONS.md`, `PLAN_RESULT.md`, `VERIFICATION_REPORT.md`; không tạo ZIP.
- Canonical contract/approved DD: `docs/lists/list_api.md` ghi Student Bearer JWT, `path{lesson_id:int64!}`, `ApiEnvelope<Lesson>`, HTTP/business codes 200/401/403/404/500. AC-14 ghi kiểm tra enrollment/prerequisite; nhánh từ chối là 403 kèm lý do.
- Approved handling: Draft — Needs Confirmation; không suy diễn access predicate, query/SQL, 403 reason shape, 404 semantics hoặc side effect.

## CURRENT_BEHAVIOR

- Source/config: `apps/study-server/app/api/v1.py` không khai báo endpoint API #22. `apps/study-server/app/modules/` không có module API #22; shared Student auth helper hiện có không xác minh API-specific behavior. `DB_UNICA_TABLES.md`, `DB_UNICA_ERD.drawio` và `infra/postgres/study-server/DB.sql` có thiết kế bảng lessons/enrollments; live schema chưa được xác minh.
- Runnable tests: Test inventory không có test API #22.
- Runtime wiring: `UNWIRED / NOT_FOUND`; route, module, API-specific query và focused test chưa có.

## SOURCE_TRACE

```text
Student -> API #22 catalog / AC-14
-> abstract enrollment/prerequisite check -> denied: 403 with reason; allowed: continue
-> catalog response ApiEnvelope<Lesson>
Current Study router/module/query/test -> NOT_FOUND / UNWIRED
Candidate lessons/enrollments tables -> checked-in design only; no API #22 query mapping
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Access predicate | AC-14 names enrollment/prerequisite checks but defines no statuses or prerequisite rules. | `SOURCE_REQUIRED` | Keep check abstract; do not define predicate or SQL. |
| Authenticated identity binding | Contract requires Student Bearer; API #22 has no source binding JWT identity to enrollment lookup. | `SOURCE_REQUIRED` | Do not specify API-specific claim/query binding. |
| 403 reason | Diagram says “403 + reason”; catalog only defines `DESIGN_ACCESS_DENIED`. | `DISCREPANCY` / `SOURCE_REQUIRED` | Preserve code and leave reason field/message shape open. |
| 404 semantics | Catalog declares `DESIGN_RESOURCE_NOT_FOUND` without identifying the resource condition. | `SOURCE_REQUIRED` | Do not assign missing lesson/course/visibility behavior. |
| Query/schema/runtime | DB design has lessons/enrollments; no API #22 query or route is present and live schema is unverified. | `DESIGN_ONLY` / `UNWIRED` / `NOT_FOUND` | Record candidate table relationships only; no runtime claim. |

## CHANGES

- Files changed: Created `apps/study-server/docs/dd/22_lessons_access/` with eight template sheets and `OPEN_QUESTIONS.md`, `PLAN_RESULT.md`, `VERIFICATION_REPORT.md`; finalized this worklog.
- CONTEXT_UPDATES: None expected; documentation-only.
- Context pages changed: None expected.
- Assumptions: Preserve existing user changes. Keep API #22 Draft — Needs Confirmation; no runtime/catalog/diagram/schema edits; no ZIP.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog selector and selected worklog review | Selected and read #16–#18 docs worklogs; shortage none. | `VERIFIED` |
| Contract/AC/schema/runtime review | Compared API #22 catalog and reusable schemas, AC-14 index/diagram, DB tables/ERD/DDL, current router/auth helper and route/module/test inventory. | `VERIFIED` |
| Inline static Markdown/JSON/table/link checker | 11 deliverables; eight ordered sheets; two JSON examples; 50 relative links; template/output fingerprints; table widths, code fences, front matter and whitespace passed. | `VERIFIED` |
| `git diff --check` | No whitespace errors in tracked diff. | `VERIFIED` |
| Authored DD/worklog whitespace scan | No trailing whitespace in new DD/worklog files. | `VERIFIED` |
| Application tests | Not run; documentation-only scope and API #22 is not wired. | `NOT_RUN` |
| Context validator | Not required; no canonical context page/manifest changed. | `NOT_REQUIRED` |

## HANDOFF

- Remaining blockers: Product/architecture confirmation is required for access predicate, identity binding, 403 reason shape, 404 semantics and query mapping before the DD can be marked Ready/Final or used as an implementation contract.
- Next owner/action: Review `OPEN_QUESTIONS.md` and update canonical contract/diagram/schema if decisions change.
