---
task_id: "2026-11-18-review-st05-dd-api-runtime"
date: "2026-11-18"
primary_task_type: "review"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["Study API #08, #16; downstream #17"]
status: "VERIFIED"
---

# Worklog: ST-05 DD, API and runtime audit

## PRIOR_WORKLOG_REVIEW
- primary_task_type: review
- selector_command: node scripts/select-worklogs.mjs --type review --limit 3
- prior_worklogs_reviewed:
  - .agents/worklog/2026-11-18/review-st03-dd-api-runtime.md
  - .agents/worklog/2026-11-18/review-st08-dd-api-runtime.md
- shortage: 1 missing; read all available.

## EXPECTED_BEHAVIOR
- Study FE scope: screens=ST-05; APIs=#08,#16. ST-04 and ST-06 are navigation dependencies.
- DD: authenticated Student; revalidate course through #08; show amount/provider and explicit confirmation; POST #16 once only after approved values/action; retain returned Order ID for ST-06. Static DD prototype only documents unavailable card.
- DD status is BLOCKED and its backend/source snapshot is stale.

## MILESTONES
| Weight | Cumulative | Objective | Status |
|---:|---:|---|---|
| 35% | 35% | Compare DD, source screenshot and API contract | DONE |
| 35% | 70% | Trace frontend, backend and related route/test source | DONE |
| 30% | 100% | Check live valid/invalid course and return navigation | DONE |

## CURRENT_BEHAVIOR
- Student route is guarded. ST-05 calls #08 and renders course title/description or missing/error; #16 has no frontend caller and API descriptor remains UNWIRED.
- Backend #16 route now exists and inserts a PENDING Order with server-derived amount and VND after Student auth; provider accepts any nonempty string, with no approved enum/idempotency policy.
- Current frontend does not show price/amount/provider or explicit confirmation, and does not hand off to ST-06.
- With live seed course 1, #08 supplied title/description. Return link opened /student/enroll/1.
- With malformed courseId abc, page displayed missing but return link pointed at /student/enroll/abc.

## FINDINGS
- P1 current-state: Missing #16 flow and checkout terms; ST-05 cannot create Order or reach ST-06. Keep mutation gated until approved provider/amount/duplicate policy.
- P2 current-state: Invalid courseId is interpolated into return link, yielding another invalid ST-04 path.
- P2 current-state: static DD icon is shopping_cart_checkout but frontend uses emoji; ready card differs from DD unavailable card and shows no price.
- Documentation drift: DD says #16 route absent; backend source now has route and Order write.

## VERIFICATION
- Read DD package, frontend route/page/service/view/tests, backend #16 handler/validation/query/models, and rendered DD HTML image.
- Authenticated local browser at /student/checkout/1: real seed course title and description, no confirm/order/payment action, back link verified.
- Authenticated local browser at /student/checkout/abc: missing state with invalid back link.
- No test/build run per read-only code-review skill. No source edits.

## HANDOFF
- Frontend #16 wiring needs an approved provider choice and clear user confirmation; backend #17 remains unavailable, so a created Order cannot proceed to payment.
