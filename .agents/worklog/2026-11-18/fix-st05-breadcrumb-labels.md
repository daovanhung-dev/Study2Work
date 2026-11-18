---
task_id: "2026-11-18-fix-st05-breadcrumb-labels"
date: "2026-11-18"
primary_task_type: "fix"
secondary_task_types: ["coding"]
project_scopes: ["web-work"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Align ST-05 breadcrumb labels

## PRIOR_WORKLOG_REVIEW
- primary_task_type: `fix`
- selector_command: `node scripts/select-worklogs.mjs --type fix --limit 3`
- prior_worklogs_reviewed:
  - `.agents/worklog/2026-11-18/fix-st02-profile-dd.md` — preserve student auth/layout.
  - `.agents/worklog/2026-11-18/fix-st03-dd-controls.md` — keep changes screen scoped.
  - `.agents/worklog/2026-11-18/fix-st04-breadcrumb-links.md` — use same labels and no `/courses` substitute link.
- shortage: `none`

## EXPECTED_BEHAVIOR
- User request: ST-05 breadcrumb mirrors ST-04 for the first two entries.
- DD: Trang chủ > Khóa học > Kiểm tra ghi danh > Kiểm tra đơn hàng.
- Study FE scope: screens=ST-05; APIs=none, navigation labels only. Existing #08/#16 behavior unaffected.

## MILESTONES
| Weight | Cumulative progress when achieved | Objective / acceptance criterion | Status |
|---:|---:|---|---|
| 40% | 40% | Check DD, current breadcrumb and routes | DONE |
| 40% | 80% | Update only two ST-05 breadcrumb items | DONE |
| 20% | 100% | Verify rendered ST-05 and Trang chủ navigation | DONE |

## CURRENT_BEHAVIOR
- `Tổng quan` links to `/student`; `Kiểm tra khóa học` is static; `Kiểm tra ghi danh` links to ST-04 using courseId.
- `/courses` public route is absent; user previously requested no substitute destination.

## SOURCE_TRACE
`student.route.ts` -> ST-05 page -> ST-05 UI breadcrumb -> browser navigation. No API/DB side effect.

## DISCREPANCIES_AND_STATUSES
- DD specifies `/courses` but current router lacks it; retain second crumb as static text.
- ST-05 payment/order DD gate remains outside this change.

## CHANGES
- Changed only ST-05-order-check-view.html: home label/href and static course label.

## VERIFICATION
- Live browser `/student/checkout/1`: breadcrumb showed all four DD labels; small-screen screenshot had no clipping; click Trang chủ opened `/`; Back restored ST-05. Existing Kiểm tra ghi danh link still targets `/student/enroll/1`.

## HANDOFF
- Complete; no `/courses` route was created and no API/order logic was changed.
