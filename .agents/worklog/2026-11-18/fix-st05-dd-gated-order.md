---
task_id: "2026-11-18-fix-st05-dd-gated-order"
date: "2026-11-18"
primary_task_type: "fix"
secondary_task_types: ["coding", "test"]
project_scopes: ["web-work"]
cross_scope_dependencies: ["Study Server API #08/#16; no backend edits"]
status: "VERIFIED_WITH_BLOCKER"
---

# Worklog: ST-05 DD alignment with gated order

## PRIOR_WORKLOG_REVIEW
- primary_task_type: fix
- selector_command: node scripts/select-worklogs.mjs --type fix --limit 3
- prior_worklogs_reviewed:
  - .agents/worklog/2026-11-18/fix-st02-profile-dd.md
  - .agents/worklog/2026-11-18/fix-st03-dd-controls.md
  - .agents/worklog/2026-11-18/fix-st04-breadcrumb-links.md
- shortage: none

## EXPECTED_BEHAVIOR
- User requests ST-05 frontend DD alignment and API connection, without backend changes.
- User confirmed payment_provider and duplicate-order policy are not approved; later clarified the DD sample has no create-order button, so no button is rendered.
- Study FE scope: screens=ST-05; APIs=#08 read, #16 create-order adapter prepared but no UI mutation.
- DD: authenticated Student; revalidate #08; show course/price and provider once approved; explicit confirm then one #16 POST; Order handoff to ST-06 only after verified creation.

## MILESTONES
| Weight | Cumulative | Objective | Status |
|---:|---:|---|---|
| 25% | 25% | Confirm DD, current source and user gate | DONE |
| 50% | 75% | Align states/visual, safe route links and #16 adapter without activating mutation | DONE |
| 25% | 100% | Focused tests/build and live browser verification | DONE |

## CURRENT_BEHAVIOR
- ST-05 reads #08 and displays course title/description; does not show price, order action, or #16 caller.
- Backend #16 exists and inserts PENDING orders in VND, but accepts any nonempty provider and has no duplicate policy. Backend #17 remains unavailable.
- Current malformed course ID is propagated to the ST-04 return link.
- ST-05 HTML has pre-existing user breadcrumb edits; preserve them.

## PLAN
- Validate route course ID before #08 and avoid invalid return links.
- Use code-native shopping cart icon and DD unavailable headline while displaying price exactly as #08 returns, with a clear draft-price label.
- Keep order creation absent from the DD gated view while provider/duplicate policy remains unresolved.
- Add typed #16 client adapter using the current endpoint/envelope, but do not call it from ST-05 until the gate is resolved.
- Keep all changes in frontend; verify focused tests, build, browser, and diff.

## VERIFICATION
- Pending.

## HANDOFF
- Pending.
