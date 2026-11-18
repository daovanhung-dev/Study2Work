---
task_id: "2026-11-18-fix-st06-breadcrumb-labels"
date: "2026-11-18"
primary_task_type: "fix"
secondary_task_types: ["coding"]
project_scopes: ["web-work"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Align ST-06 breadcrumb first two items

## PRIOR_WORKLOG_REVIEW
- primary_task_type: `fix`
- selector_command: `node scripts/select-worklogs.mjs --type fix --limit 3`
- prior_worklogs_reviewed:
  - `.agents/worklog/2026-11-18/fix-st02-profile-dd.md` — preserve student auth/layout.
  - `.agents/worklog/2026-11-18/fix-st03-dd-controls.md` — keep changes screen scoped.
  - `.agents/worklog/2026-11-18/fix-st04-breadcrumb-links.md` — same first two labels and no `/courses` substitute link.
- shortage: `none`

## EXPECTED_BEHAVIOR
- User request: apply the ST-04/ST-05 first two breadcrumb corrections to ST-06.
- DD: first two labels Trang chủ and Khóa học. Remaining items outside this request.
- Study FE scope: screens=ST-06; APIs=none because breadcrumb labels only. #17/#18 unaffected.

## MILESTONES
| Weight | Cumulative progress when achieved | Objective / acceptance criterion | Status |
|---:|---:|---|---|
| 40% | 40% | Check ST-06 DD and current breadcrumb | DONE |
| 40% | 80% | Update exactly the first two items | DONE |
| 20% | 100% | Verify ST-06 live breadcrumb and home navigation | DONE |

## CURRENT_BEHAVIOR
- Tổng quan links to `/student`; Kiểm tra khóa học is static.
- Public `/courses` route absent; user requested no substitute link.

## SOURCE_TRACE
`student.route.ts` -> ST-06 page -> ST-06 UI breadcrumb -> browser navigation. No API/DB side effect.

## DISCREPANCIES_AND_STATUSES
- DD full breadcrumb differs at the third item, but the request explicitly limits this turn to the first two.
- Payment API gate remains outside this change.

## CHANGES
- Changed only ST-06-payment-view.html: `Trang chủ` now links `/`; `Khóa học` remains static.

## VERIFICATION
- Local browser `/student/pay/1`: breadcrumb showed the two corrected labels; small-screen screenshot had no clipping. Clicking Trang chủ opened `/`; Back restored ST-06.

## HANDOFF
- Complete. No API, route, or payment behavior changed.
