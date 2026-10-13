---
task_id: "2026-10-12-create-study-api37-dd"
date: "2026-10-12"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo Study API #37 DD draft

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-12/commit-push-study-dds.md`
    - carry_forward: DD #16–#26 là design drafts; không suy ra runtime từ DD và không chỉnh sửa artifacts cũ.
  - path: `.agents/worklog/2026-10-12/create-study-api27-dd.md`
    - carry_forward: Giữ Draft + open questions; không invent schema, access predicate hoặc công thức; Study không tạo ZIP.
  - path: `.agents/worklog/2026-10-11/create-study-api28-dd.md`
    - carry_forward: Giữ approved catalog contract; ghi discrepancy/UNWIRED riêng; không thêm status code ngoài contract.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tạo API Detail Design draft cho API #37 `GET /api/v1/users/me/progress/{course_id}` theo template Markdown Study Server, gồm tám sheets, ba reports và worklog; không tạo ZIP.
- Canonical contract/approved DD: `docs/lists/list_api.md` là `APPROVED_DESIGN_CONTRACT`; Student Bearer JWT, `course_id:int64!`, `ApiEnvelope<UserProfile>`, HTTP 200/401/403/404/500 cùng các `DESIGN_*` code trong catalog. Người dùng xác nhận giữ catalog và ghi gap response trong draft.

## CURRENT_BEHAVIOR

- Source/config: `apps/study-server/app/api/v1.py` có routes #1–#7, #12–#14; không có route #37 hoặc module progress. `DB_UNICA_TABLES.md`, ERD và `infra/postgres/study-server/DB.sql` là design/checked-in DDL evidence; live schema chưa xác minh.
- Runnable tests: Không tìm thấy test API #37; runtime tests không chạy trong phạm vi docs-only.
- Runtime wiring: API #37 là `UNWIRED / NOT_FOUND` trong Study Server hiện tại.

## SOURCE_TRACE

```text
Student -> GET /api/v1/users/me/progress/{course_id} (approved design contract)
-> AC-18 mô tả aggregate lesson + quiz + assignment progress
-> candidate reads: lesson_progress/lessons/courses, quiz_attempts/quizzes,
   assignment_submissions/assignments
-> current Study router/modules/tests không có API #37
-> tạo DD-only draft, giữ schema/query/business gaps mở
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Response schema | Catalog declares `ApiEnvelope<UserProfile>`; AC-18 requires detailed progress data; `UserProfile` has no progress fields. | `DISCREPANCY / SOURCE_REQUIRED` | Preserve catalog and do not invent progress fields. |
| Progress calculation | AC-18 names lesson, quiz and assignment progress; no formula, denominator, completion or attempt-selection rule exists. | `SOURCE_REQUIRED` | Candidate reads only; no aggregate result can be finalized. |
| Runtime endpoint | Current router, modules and tests contain no API #37. | `UNWIRED / NOT_FOUND` | DD is design-only. |
| Database state | Design docs/DDL provide candidate tables; live metadata is unverified and DDL FK nullability differs from logical table guide. | `DESIGN_ONLY / NOT_VERIFIED` | No runtime schema claim. |

## CHANGES

- Files changed: `apps/study-server/docs/dd/37_users_me_progress_course/` (8 sheets, PLAN_RESULT.md, OPEN_QUESTIONS.md, VERIFICATION_REPORT.md); this worklog.
- CONTEXT_UPDATES: None.
- Context pages changed: None.
- Assumptions: Preserve API catalog response/status set; create Draft — Needs Confirmation; mark unresolved payload, query, authorization and empty-result decisions in `OPEN_QUESTIONS.md`; no runtime/catalog/diagram/schema changes.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type docs --limit 3` | Selected and read the three listed docs worklogs. | VERIFIED |
| Source review | Read API #37 catalog row, AC-18 index/diagram, relevant ERD/table design/DDL, API #21 progress DD, API guidelines and current Study router/auth/response sources. | VERIFIED |
| Source archive scan | Scanned diagrams, docs/lists and create_dd_api source roots; no archive files found to extract. | VERIFIED |
| Template fingerprint | Confirmed all 8 recorded SHA-256 values match the canonical template folder. | VERIFIED |
| DD inventory/front matter/template appendix/table/link/JSON/contract/read-only mapping checks | All 8 sheets and 3 reports present; required front matter and template appendices retained; table widths, relative links, JSON blocks, response/status/error contract, and N/A mutation mapping passed. | VERIFIED |
| Whitespace | No trailing whitespace or extra EOF blank lines; `git diff --no-index --check` passed on all 11 new Markdown files. | VERIFIED |
| Runtime tests | Not run; docs-only scope and API #37 is not wired. | NOT_RUN |

## HANDOFF

- Remaining design questions: Response schema, aggregation formula, query filters, access rules, empty-result behavior, JWT identity mapping and path validation are recorded in `OPEN_QUESTIONS.md`; resolve them before DD moves to Ready/Final or implementation.
- Next owner/action: Review `OPEN_QUESTIONS.md` and update the approved contract/design sources before closing the questions.
