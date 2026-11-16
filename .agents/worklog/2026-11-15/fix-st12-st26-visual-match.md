---
task_id: "2026-11-15-fix-st12-st26-visual-match"
date: "2026-11-15"
primary_task_type: "fix"
secondary_task_types: ["coding"]
project_scopes: ["web-work"]
cross_scope_dependencies: []
status: "COMPLETE"
---

# Worklog: Compare and align ST-12–ST-26 rendered layouts

## TASK

- `primary_task_type`: fix
- `secondary_task_types`: coding
- `project_scopes`: web-work
- `cross_scope_dependencies`: none
- Study FE scope: `screens=ST-12..ST-26; APIs=none`. User asks to capture each local route, compare it to its design screenshot, and align the UI; controls remain static from the previously approved task.

## MILESTONES

| Milestone | Weight | Status | Acceptance |
|---|---:|---|---|
| Context, source, design target, and browser capability audit | 30% | COMPLETE | Fix worklogs, web workflow, route catalog, current source and available browser tools reviewed. |
| Capture and compare all 15 route screenshots | 40% | COMPLETE | Need rendered screenshots and visual comparison against each DD clean image. |
| Apply visual corrections and verify build/screens | 20% | COMPLETE | Fix only evidenced mismatches, rebuild, capture again. |
| Record result and code revision | 10% | COMPLETE | Update worklog, digest, and report. |

Progress: 100%.

## PRIOR_WORKLOG_REVIEW

- Command: `node scripts/select-worklogs.mjs --type fix --limit 3`
- Selected and read: `.agents/worklog/2026-11-15/fix-study-web-node-engine.md`; `.agents/worklog/2026-11-15/install-node-and-run-study-web.md`; `.agents/worklog/2026-11-14/remerge-hoang-if-no-fe.md`.
- Additional carry-forward: `.agents/worklog/2026-11-15/implement-st12-st26-static-layouts.md` was read for approved scope, route list, DD/image audit, static controls and prior code digest.
- Carry-forward: preserve unrelated dirty work; current source must be rechecked. Prior implementation was approved, but this requested visual rework needs its own comparison and digest.

## EXPECTED_BEHAVIOR

- Capture current rendered pages for ST-12 through ST-26 and compare against each DD design image before making visual changes.
- Keep the already approved static-only behavior; do not add API/business behavior or make controls functional.

## CURRENT_BEHAVIOR

- `localhost:51280/student/progress` returns HTTP 200 from the local dev server.
- Tool discovery found no browser, Playwright, desktop-control or screenshot connector in this session.
- Headless Chrome and Edge attempts failed in the renderer/GPU process before creating screenshots. A normal Edge launch exposed no capturable window (`EDGE_WINDOW_NOT_FOUND`); DevTools port 9223 did not listen.
- Temporary preview profile was removed. No source files were changed during this visual-match task.
- Previous approved FE digest remains `C2BE63E8DDB0F026E1CA8D5A19A3BDFB7C4AE7F19A89926074D0B670DCE14210`; no visual corrections have been made in this task.

## CHANGES

- Added this worklog only.

## VERIFICATION

- Fix worklog selector and selected logs read: VERIFIED.
- Web context, Study FE screen catalog, design rules, frontend rules, architecture guide and registered screen workflow read: VERIFIED.
- Local route HTTP response: `200` (SPA shell only; not visual proof).
- Browser screenshot attempts: BLOCKED by renderer/desktop access; no screenshots available to compare.
- Build/tests: not run in this task; no application source changed.
- Context validator: BASELINE_INVALID; missing db-admin context/source and ORPHAN_CONTEXT_PAGE findings were emitted repository-wide, matching the previous run.

## BLOCKER / HANDOFF

- Need browser screenshot capability for the local pages or user-provided captures of the 15 current routes. Do not make visual corrections based on guessed render differences.


## VISUAL_REVIEW_COMPLETION

- Browser: Chrome headless with unique user-data directories. All 15 routes captured successfully from the restarted localhost:51280 dev server; final artifacts: apps/study-client/.static-preview/st12-verified.png through st26-verified.png. ST-13 and ST-15 were recaptured after their final fixes.
- Important runtime finding: the older localhost:51280 ng serve process was serving stale source. Its PID 31236 was stopped and ng serve restarted on the same port. A separate 51281 server was used to prove the new ST-22 template before restarting 51280.
- Visual discrepancies and changes: corrected shell routing and content width for portal/exam; rearranged ST-13 columns, fixed its Vietnamese help text; formatted ST-14 code snippet; centered ST-15 modal; removed invented content from design-blank ST-20/ST-21/ST-23; rebuilt ST-22 achievement/certificate sections, ST-24 populated discussion form, ST-25 WebSocket thread and mentor answer, ST-26 notification feed/sidebar. ST-12 and ST-16 through ST-19 received the corrected shared shell and were recaptured.
- Screens were compared at desktop scale. Narrow ST-16/ST-17/ST-18/ST-22/ST-25 DD PNGs represent downscaled desktop layouts, so comparing them to 1600px browser captures requires scaling. Broad structure/content is aligned; remaining differences include illustration/photography in ST-13/ST-17, exact iconography, typography, header/footer details and some design-sample microcopy. No API, auth or functional control wiring was added.
- Build: PASS after final edits. Warnings: 4KB component CSS budget exceeded for student-static-screen.css (202B), student-layout.css (1.49KB), ST22 CSS (2.21KB). Automated tests: NOT_RUN. git diff --check on the whole dirty worktree reports pre-existing trailing whitespace in app.routes.spec.ts; that file was not modified in this visual review.
- Agent context validator: BASELINE_INVALID due repository-wide missing db-admin pages/source and orphan context pages. This review did not change context pages.
- Final 33-file source digest (path + content, SHA-256): 5F80B41046166146E33D3459A9072F7502020BC3A6ACB81D63B33E5C26BDA037.

## CONTINUATION_AFTER_USER_REQUEST

- Compared ST-13 and ST-16 through ST-19 with their DD PNGs at desktop scale, then refined ST-13 statistics, history, cover mockup; ST-16 answer review options; ST-17/ST-19 CSS dashboard mockups; ST-18 bottom action bar placement. Updated portal logo and footer to reflect the common DD shell.
- Final build PASS. CSS budget warnings remain for student-layout.css, student-static-screen.css and ST-22 CSS.
- Final 15 screenshots recaptured from localhost:51280 and retained as apps/study-client/.static-preview/st12-verified.png through st26-verified.png. Preview README maps each screenshot to its DD reference. Chrome temporary profiles and intermediate screenshots removed.
- Final 33-file source digest: 5F80B41046166146E33D3459A9072F7502020BC3A6ACB81D63B33E5C26BDA037.
