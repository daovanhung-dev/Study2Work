---
task_id: "2026-11-18-fix-st06-payment-dd"
date: "2026-11-18"
primary_task_type: "fix"
secondary_task_types: ["coding", "test"]
project_scopes: ["web-work"]
cross_scope_dependencies: ["Study Server API #16/#17/#18 contracts; no backend edits"]
status: "VERIFIED_WITH_BLOCKER"
---

# Worklog: Align ST-06 with DD within current payment gate

## PRIOR_WORKLOG_REVIEW
- primary_task_type: fix
- selector_command: node scripts/select-worklogs.mjs --type fix --limit 3
- prior_worklogs_reviewed:
  - .agents/worklog/2026-11-18/fix-st02-profile-dd.md — preserve Student auth and layout.
  - .agents/worklog/2026-11-18/fix-st03-dd-controls.md — blocked actions remain blocked when contract is unresolved.
  - .agents/worklog/2026-11-18/fix-st04-breadcrumb-links.md — preserve established home/course breadcrumb choices.
- shortage: none

## EXPECTED_BEHAVIOR
- User asks to align ST-06 with DD, frontend only.
- Study FE scope: screens=ST-06; APIs=#16/#17/#18 as cross-screen/payment dependencies.
- DD expects an authenticated Student route, valid Order context, POST #17 only with approved order/provider and action, GET #18 only for a verified payment operation, server-confirmed paid state before ST-07.
- DD prototype shows credit-card icon, checkout breadcrumb and return to ST-05, but source route lacks a real course ID.

## MILESTONES
| Weight | Cumulative progress | Objective | Status |
|---:|---:|---|---|
| 25% | 25% | Confirm DD, frontend and backend runtime contract | DONE |
| 50% | 75% | Fix safe route/UI behavior and truthful backend availability | DONE |
| 25% | 100% | Focused test, build, browser verification and diff review | DONE |

## CURRENT_BEHAVIOR
- ST-06 accepts any nonempty orderId, renders blocked message, has emoji icon and wrong breadcrumb, has no API caller.
- ST-05 only reads course info and never creates an Order.
- Backend #17 route always returns 503 before any payment/operation write; #18 only reads notification operations.
- No valid order/provider handoff or trusted payment result source. Do not issue POST #17 from route entry or introduce retry.
- ST-06 view HTML and API registry had pre-existing dirty changes; preserve them.

## PLAN
- Update ST-06 model/page to validate positive int64 URL order ID and distinguish invalid from payment unavailable.
- Update ST-06 view icon to code-native credit-card SVG, breadcrumb to Kiểm tra đơn hàng, and copy to reflect provider unavailable.
- Keep existing safe destination to course list when ST-05 course ID is unknown; never render a literal :courseId route.
- Add focused state tests, run build and verify live. Do not edit backend, initiate payment, or poll notification operations.

## VERIFICATION
- Pending.

## HANDOFF
- Pending.
