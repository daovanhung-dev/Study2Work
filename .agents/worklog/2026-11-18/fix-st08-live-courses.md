---
task_id: "2026-11-18-fix-st08-live-courses"
date: "2026-11-18"
primary_task_type: "fix"
secondary_task_types: ["coding", "test"]
project_scopes: ["web-work"]
cross_scope_dependencies: ["Study API #20; API #21 contract gap"]
status: "COMPLETED"
---

# Worklog: Connect ST-08 to real enrolled courses

## PRIOR_WORKLOG_REVIEW
- primary_task_type: `fix`
- selector_command: `node scripts/select-worklogs.mjs --type fix --limit 3`
- prior_worklogs_reviewed:
  - `.agents/worklog/2026-11-18/fix-st02-profile-dd.md` — preserve student auth/layout.
  - `.agents/worklog/2026-11-18/fix-st03-dd-controls.md` — keep changes screen scoped.
  - `.agents/worklog/2026-11-18/fix-st04-breadcrumb-links.md` — follow current route evidence.
- shortage: `none`

## EXPECTED_BEHAVIOR
- User asks to align ST-08 with DD using frontend changes only, no backend edits.
- Study FE scope: screens=ST-08; APIs=#20 read, #21 progress contract reviewed but not mapped because it returns UserProfile.
- DD goal: enrolled courses, true empty/list/error/loading and page/status filter/progress when contract permits; CTA to ST-20; course card to ST-09.

## MILESTONES
| Weight | Cumulative progress when achieved | Objective / acceptance criterion | Status |
|---:|---:|---|---|
| 25% | 25% | Confirm DD, current #20/#21 response and caller patterns | DONE |
| 50% | 75% | Implement #20 read, honest states, paging, DD empty visual and navigation | DONE |
| 25% | 100% | Focused tests/build and live authenticated browser verification | DONE |

## CURRENT_BEHAVIOR
- ST-08 renders hardcoded blocked state and does not call #20. ST-01 calls #20 and reports true empty for current QA account.
- Backend #20 returns CourseSummaryPage by authenticated user; #21 returns UserProfile only.
- No dirty Git changes in ST-08 before edit.

## SOURCE_TRACE
`student.route.ts -> ST08 page -> ST08 data-access -> StudyApiService API_020 -> auth interceptor -> backend #20 -> user-scoped enrollments query -> envelope -> ST08 states/view`. No backend edits.

## DISCREPANCIES_AND_STATUSES
- DD package is stale about #20 route absence; current source and live ST-01 prove #20 works.
- #21 has no per-course progress data. Do not display made-up percentages or call a profile-only response a progress result.
- Status filter enum/default are not approved. Keep UI filter unavailable until contract is decided. Backend supports page pagination; expose previous/next controls.

## CHANGES
- Updated ST08 models, data-access, page, view HTML/CSS and focused tests. API #20 now drives loading, empty, populated, and error states with retry and pagination. DD empty CTA links to ST-20; course cards link to ST-09. No backend source changed.

## VERIFICATION
- Pending.

## HANDOFF
- Pending.
