---
task_id: "2026-11-18-fix-st04-breadcrumb-links"
date: "2026-11-18"
primary_task_type: "fix"
secondary_task_types: ["coding"]
project_scopes: ["web-work"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Fix ST-04 breadcrumb labels and links

## PRIOR_WORKLOG_REVIEW
- primary_task_type: `fix`
- selector_command: `node scripts/select-worklogs.mjs --type fix --limit 3`
- prior_worklogs_reviewed:
  - `.agents/worklog/2026-11-18/fix-st02-profile-dd.md` — preserve auth and student shell.
  - `.agents/worklog/2026-11-18/fix-st03-dd-controls.md` — keep changes screen scoped.
  - `.agents/worklog/2026-11-15/fix-st12-st26-visual-match.md` — verify rendered UI.
- shortage: `none`

## EXPECTED_BEHAVIOR
- User request: ST-04 breadcrumb first item says Trang chủ and second item matches DD. User said to leave navigation alone when `/courses` does not exist.
- DD: prototype breadcrumb is Trang chủ > Khóa học > Kiểm tra ghi danh, with `/` and `/courses` links. Current app has no public `/courses` route. User requested no substitute destination.
- Study FE scope: screens=ST-04; APIs=none because only navigation presentation changes. Existing #08/#15 behavior stays unchanged.

## MILESTONES
| Weight | Cumulative progress when achieved | Objective / acceptance criterion | Status |
|---:|---:|---|---|
| 40% | 40% | Confirm DD labels and valid runtime destinations | DONE |
| 40% | 80% | Update only ST-04 breadcrumb markup/styles | DONE |
| 20% | 100% | Check navigation and small-screen display live | DONE |

## CURRENT_BEHAVIOR
- ST-04 first crumb says Tổng quan and links `/student`; second crumb is unclickable text Kiểm tra khóa học.
- `/courses` currently redirects to not-found; `/` contains `featured-courses-section`.

## SOURCE_TRACE
`student.route.ts` -> ST-04 page -> ST-04 UI breadcrumb -> browser navigation. No API or DB side effect.

## DISCREPANCIES_AND_STATUSES
- DD `/courses` destination is not registered in current Angular router; do not add a substitute route or link for the second crumb.
- DD G-01 API #15 remains blocked, outside this breadcrumb change.

## CHANGES
- Changed only `ST-04-enroll-check-view.html`: home label/href and static course label. No CSS/API/route changes.

## VERIFICATION
- Verified in local browser at `/student/enroll/1`: breadcrumb reads `Trang chủ > Khóa học > Kiểm tra ghi danh`; click Trang chủ opened `/`; browser Back returned to ST-04. Small-screen screenshot shows breadcrumb without clipping. No course-link click because no target route exists.

## HANDOFF
- Pending.
