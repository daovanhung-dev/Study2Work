---
task_id: "2026-10-12-create-study-api33-dd"
date: "2026-10-12"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo Study API #33 DD draft

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-12/commit-push-study-dds.md`
    - carry_forward: Giữ các DD hiện có ở trạng thái draft; task này không gồm commit/push.
  - path: `.agents/worklog/2026-10-12/create-study-api27-dd.md`
    - carry_forward: Dùng Draft — Needs Confirmation, open questions, không ZIP; tách contract thiết kế khỏi current runtime.
  - path: `.agents/worklog/2026-10-12/create-study-api28-dd.md`
    - carry_forward: Giữ nguyên contract/error set và không tự chốt rule còn thiếu.
- shortage: `none`
- Additional recent precedent reviewed: `.agents/worklog/2026-10-12/create-study-api29-dd.md`, `create-study-api30-dd.md`, `create-study-api31-dd.md` and `create-study-api32-dd.md`.

## EXPECTED_BEHAVIOR

- Requirement: Tạo API Detail Design draft cho API #33 `GET /api/v1/assignments/{assignment_id}` theo Markdown template của Study Server, gồm 8 sheet, `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md` và worklog. Không tạo ZIP, không sửa runtime, API catalog, diagrams hoặc schema.
- Canonical contract/approved DD: `docs/lists/list_api.md` đánh dấu catalog `APPROVED_DESIGN_CONTRACT`; API #33 yêu cầu Student Bearer JWT, path `assignment_id:int64!`, `ApiEnvelope<Assignment>`, HTTP 200 `DESIGN_RESOURCE_RETRIEVED` và lỗi 401/403/404/500.

## CURRENT_BEHAVIOR

- Source/config: `apps/study-server/app/api/v1.py`, module scan và tests scan không có API #33 assignment implementation. `app/utils/auth.py` hiện có helper xác thực Bearer/JWT và Student role. Assignment mapping trong `DB_UNICA_TABLES.md`, ERD và checked-in `DB.sql` là design evidence; live schema chưa được xác minh.
- Runnable tests: Không tìm thấy test API #33; runtime tests không thuộc phạm vi DD-only.
- Runtime wiring: API #33 hiện `UNWIRED / NOT_FOUND`.

## SOURCE_TRACE

```text
Student Bearer -> GET /api/v1/assignments/{assignment_id} (approved design contract)
-> candidate SELECT assignments by id -> ApiEnvelope<Assignment>
Current Study router/module/test: UNWIRED / NOT_FOUND
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #33 runtime | Current Study router, modules and tests have no assignment detail route. | `UNWIRED / NOT_FOUND` | DD remains design-only. |
| Deadline/access branch | AC-17 diagram says overdue/no permission maps to 403/409; API #33 catalog has 403 but no 409. | `DISCREPANCY / SOURCE_REQUIRED` | Preserve catalog codes; record owner decision. |
| Submission rules | AC-17 says read assignment + submission rule; `Assignment` contract has no rule fields. | `SOURCE_REQUIRED` | Do not invent response fields or rule behavior. |
| Physical schema | DDL permits nullable `course_id` and `max_score`, while logical contract requires both fields and DB table notes describe `course_id` as required. | `DISCREPANCY / DESIGN_ONLY` | Candidate mapping only; live schema unverified. |

## CHANGES

- Files changed: Created eight API #33 template sheets plus `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md` under `apps/study-server/docs/dd/33_assignments_detail/`, and finalized this worklog.
- CONTEXT_UPDATES: None; no runtime or canonical source contract changes.
- Context pages changed: None.
- Assumptions: Follow API #27–#32 Draft — Needs Confirmation policy; no ZIP; preserve error set and all existing artifacts; unresolved access, deadline, rules and schema semantics remain open.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type docs --limit 3` | Selected and read the three worklogs listed above. | `VERIFIED` |
| Source review | API catalog, AC-17 index/activity diagram, assignment/enrollment DB design, ERD/DDL, auth helper, current route/module/test surface and canonical template reviewed. | `VERIFIED` |
| Inline Python DD validation | 11-file inventory, eight-sheet order/front matter, canonical template appendices/fingerprints, JSON examples, local links/anchors, table widths, code fences, whitespace/conflict markers, API catalog fields/error set and AC-17 403/409 conflict checks passed. | `VERIFIED` |
| `git diff --check` and new-file whitespace scan | No tracked diff errors; new API #33 Markdown and worklog contain no trailing whitespace. | `VERIFIED` |
| Runtime tests | Not run; API #33 is not wired and task scope is documentation-only. | `NOT_RUN` |
| Context validator | Not required unless agent context changes. | `NOT_REQUIRED` |

## HANDOFF

- Remaining blockers: Owner decisions listed in `OPEN_QUESTIONS.md` are required before final approval or implementation; they do not block this draft deliverable.
- Next owner/action: Review access/deadline behavior, submission-rule response scope, schema discrepancies and path/date-time semantics.
