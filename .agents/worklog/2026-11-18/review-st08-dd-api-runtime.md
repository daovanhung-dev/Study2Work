---
task_id: "2026-11-18-review-st08-dd-api-runtime"
date: "2026-11-18"
primary_task_type: "review"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["Study API #20, #21"]
status: "VERIFIED"
---

# Worklog: ST-08 DD, API and runtime audit

## PRIOR_WORKLOG_REVIEW
- primary_task_type: `review`
- selector_command: `node scripts/select-worklogs.mjs --type review --limit 3`
- prior_worklogs_reviewed:
  - `.agents/worklog/2026-11-18/review-st03-dd-api-runtime.md` — distinguish DD gates from current source and do not edit reviewed code.
- shortage: `2 missing`

## EXPECTED_BEHAVIOR
- Study FE scope: screens=ST-08; APIs=#20,#21.
- DD requires authenticated student course list, status filter, progress bars, loading/empty/partial/error states, navigation to ST-09 and ST-20. #20 first; #21 only as contract supports progress.
- DD image only documents static empty-state presentation. Source DD status BLOCKED and stale source inventory.

## MILESTONES
| Weight | Cumulative progress when achieved | Objective / acceptance criterion | Status |
|---:|---:|---|---|
| 35% | 35% | Read ST-08 DD and visual source | DONE |
| 35% | 70% | Trace frontend and backend #20/#21 | DONE |
| 30% | 100% | Check authenticated local ST-08/ST-01 states and report | DONE |

## CURRENT_BEHAVIOR
- `/student/courses` is guarded by `studentAuthGuard` and renders a hardcoded blocked state. No ST-08 API caller.
- Backend #20 now exists and returns `CourseSummaryPage` filtered by authenticated Student ID; #21 exists but returns UserProfile, not aggregate progress.
- ST-01 already calls #20 and displays an empty result for the current QA account. ST-08 shows unavailable for the same account and never reads that result.
- ST-08 CTA goes to `/student`, whereas DD empty-state CTA goes to `/student/progress`; icon is emoji rather than local_library line icon.

## SOURCE_TRACE
`student.route.ts -> ST08 page -> blocked-only service -> UI`. No ST-08 API call. `ST01 page -> ST01 service -> StudyApiService API_020 -> backend get_user_courses -> authenticated enrollments query` is a working related path.

## DISCREPANCIES_AND_STATUSES
- P1 current-state: ST-08 never calls available #20; list, true empty, filter and course navigation cannot run.
- P2 current-state: #21 returns profile only, so progress bars and merge cannot be implemented from its current payload.
- P2 current-state: CTA and icon diverge from static DD; CTA destination is valid but does not deliver expected progress navigation.
- Documentation drift: ST-08 DD says #20/#21 route absent and Study Web unwired; current code has both backend routes and client route, but ST-08 remains unwired.

## CHANGES
- Reviewed source, DD and local UI only; no source/test/config changes. Worklog is the only write.

## VERIFICATION
- Local browser: ST-07 link opened ST-08; ST-08 blocked card shown. ST-08 CTA opened ST-01. ST-01 #20 widget returned empty for current account; #21 reported profile-only contract gap. Returning via ST-01 link still showed blocked ST-08.
- Tests/build/linters not run under read-only review skill. Existing ST-08 test only asserts static blocked state.

## HANDOFF
- Wire #20 to ST-08 using a screen-appropriate adapter; distinguish real empty/list/error. Keep progress pending until #21 returns a course progress DTO and rules are approved. Update stale DD after contract decision.
