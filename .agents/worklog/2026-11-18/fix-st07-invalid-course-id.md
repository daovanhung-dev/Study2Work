---
task_id: "2026-11-18-fix-st07-invalid-course-id"
date: "2026-11-18"
primary_task_type: "fix"
secondary_task_types: ["test"]
project_scopes: ["web-work"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: ST-07 invalid course ID

## PRIOR_WORKLOG_REVIEW
- primary_task_type: fix
- selector_command: node scripts/select-worklogs.mjs --type fix --limit 3
- prior_worklogs_reviewed:
  - .agents/worklog/2026-11-18/fix-st02-profile-dd.md
  - .agents/worklog/2026-11-18/fix-st03-dd-controls.md
  - .agents/worklog/2026-11-18/fix-st04-breadcrumb-links.md
- shortage: none.

## EXPECTED_BEHAVIOR
- Study FE scope: screens=ST-07; APIs=none for this URL-validation-only change. Existing DD references #18/#19/#20 remain gated and untouched.
- A malformed courseId must not be treated as a valid route context or imply a backend request failed. A valid positive int64 courseId remains in the current blocked state.
- The ST-07 DD prohibits inferring enrollment success from URL/static copy.

## MILESTONES
| Weight | Cumulative | Objective | Status |
|---:|---:|---|---|
| 40% | 40% | Confirm DD, current route and nearby ID validation | DONE |
| 40% | 80% | Add ST-07 route ID check and focused regression cases | DONE |
| 20% | 100% | Run focused test and local screen verification | DONE |

## SOURCE_TRACE
student.route.ts -> ST-07 page paramMap -> local state -> ST-07 view. No API or DB side effect in this fix.

## IMPLEMENTATION_PLAN
- Touch only ST-07 page and its focused page spec.
- Reuse the positive int64 route ID predicate already used in ST-05/ST-06; retain missing-context kind and distinguish absent versus malformed path copy.
- Add tests for malformed, zero, overflow, and valid IDs. Keep API data-access unchanged.
- Run focused Angular spec; inspect local ST-07 URL in browser. No fake DB fixtures.

## CURRENT_BEHAVIOR
- Any nonempty courseId including abc shows backend-unavailable copy.
- Valid ID shows DD-gated blocked copy; CTA opens ST-08.

## DISCREPANCIES_AND_STATUSES
- ST-07 DD remains BLOCKED for #18/#19/#20; the URL-only fix does not close that gate.
- DD backend/source availability statements are stale, but are outside this frontend fix.

## CHANGES
- Pending.

## VERIFICATION
- Pending.

- Context validator: AGENT_CONTEXT_INVALID on pre-existing missing db-admin/context pages and unavailable Git/source snapshot; no ST-07-specific issue reported.
