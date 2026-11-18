---
task_id: "2026-11-18-review-st10-layout-and-api"
date: "2026-11-18"
primary_task_type: "coding"
secondary_task_types: ["review", "test"]
project_scopes: ["web-work"]
cross_scope_dependencies: ["Study Server API #22, #23, #24"]
status: "COMPLETE"
---

# Worklog: ST-10 visual and API audit

## PRIOR_WORKLOG_REVIEW
- primary_task_type: coding
- selector_command: node scripts/select-worklogs.mjs --type coding --limit 3
- prior_worklogs_reviewed:
  - .agents/worklog/2026-11-18/implement-st09-read-apis.md
  - .agents/worklog/2026-11-18/implement-study-auth-session.md
  - .agents/worklog/2026-11-15/implement-st11-static-layout.md
- shortage: none.

## EXPECTED_BEHAVIOR
- Study FE scope: screens=ST-10; APIs=#22 access, #23 start, #24 detail.
- Compare all eight ST-10 DD files, clean/numbered design images, source HTML and live Angular UI. Match the iconography and composition without fabricating a successful entitlement state.
- Preserve no-media-before-access and disabled start while #23 initiation, idempotency and ST-11 handoff remain undecided.

## MILESTONES
| Weight | Cumulative | Objective | Status |
|---:|---:|---|---|
| 40% | 40% | Read DD/images, frontend and backend contracts | DONE |
| 40% | 80% | Check live UI and correct visual differences | DONE |
| 20% | 100% | Focused verification and report API gaps | DONE |

## CURRENT_BEHAVIOR
- Angular ST-10 route exists, but page returns a static blocked state and does not call #22/#23/#24. Header/footer are owned by StudentLayout.
- Frontend #22/#23/#24 descriptors remain UNWIRED. Current backend now has all three routes and module tests, so DD source absence is stale.
- #22 and #23 source responses contain content/video_url; #23 writes lesson_progress. DD does not settle whether #23 runs automatically or on click, retry/idempotency policy, nor #24 ownership across ST-10/ST-11. ST-09 does not hand off a verified lessonId.
- Current ST-10 UI lacks reference shield, FSM, security, player, and API-row icons; CSS contains unused legacy selectors and a fake 34% progress bar.

## PLAN
- Read source HTML for visual anchors and compare live desktop/mobile.
- Replace emoji/text symbols with inline SVG icons matching the numbered design; restore FSM icon rail and three API status rows, using honest source status text.
- Keep access/start/content request flow blocked and no player mounted. Do not touch backend or synthesize API response.
- Run focused ST-10 tests, build, and live browser verification. Record remaining DD/contract discrepancies.

## CHANGES
- Updated ST-10 local HTML/CSS: coherent left card, inline SVG shield/lock/progress/player/FSM/API icons, three API rows, responsive reflow, no fake progress fill. Kept shared header/footer unchanged.
- Corrected static copy to distinguish existing backend routes from unwired frontend and removed unsupported session-token/permanent-lock assertions.
- Added focused direct-route test for blocked state, disabled start and absent media; updated Study context index. No backend edits and no API requests added.

## VERIFICATION
- `npm run build`: passed, with pre-existing SH-01 CSS size warning.
- `npm test -- --include=src/app/features/student/ST10/**/*.spec.ts`: 2/2 passed.
- In-app browser `/student/lessons/1/start`: observed real gated ST-10 at narrow width, inspected main card, FSM rail, API rows and footer. Start remains disabled; no player mounted. A new tab without auth correctly redirected to login.
- `git diff --check` across entire dirty repo found pre-existing blank lines in unrelated ST-04/ST-07/ST-09/API registry files; no ST-10 errors in output.
- Context validator remains invalid due pre-existing missing db-admin paths, orphan pages and source-drift access failures.
- API discrepancy: current backend now implements #22/#23/#24 although DD says NOT_FOUND. #22 returns content/video and does not check lesson PUBLISHED status; #23 can write progress and return content/video without course/lesson PUBLISHED check. #24 checks publication and enrollment. Frontend remains unwired pending safe #23 trigger/retry and ST-11 handoff.
