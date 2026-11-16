---
task_id: "2026-11-15-fix-st13-playwright-visual-audit"
date: "2026-11-15"
primary_task_type: "fix"
secondary_task_types: ["coding", "test"]
project_scopes: ["web-work"]
cross_scope_dependencies: []
status: "COMPLETE"
---

# ST-13 Playwright visual audit

## TASK

- Study FE scope: `screens=ST-13; APIs=none`.
- Compare `http://localhost:51280/student/quizzes/quiz-001` with `apps/study-client/docs/dd_screens/ST-13-GioiThieuBaiKiemTra/images/screen-clean.png`; correct small icons and directly related static layout discrepancies.
- Preserve previously approved static-only behavior. No API, auth, quiz timer or active buttons.

## MILESTONES

| Milestone | Weight | Status | Acceptance |
|---|---:|---|---|
| Context and Playwright setup | 25% | COMPLETE | Fix worklogs, Web Study rules, ST-13 DD/source, local browser/package available. |
| Capture and compare | 35% | COMPLETE | Playwright screenshot of live route at 1349px against DD clean PNG, differences identified. |
| Correct and recapture | 30% | COMPLETE | Replace Unicode pseudo-icons with static SVG, refine instructor/rules/history, capture after. |
| Verify and record | 10% | COMPLETE | Build, DOM/console/mobile checks, preview artifact and worklog. |

Progress: 100%.

## PRIOR_WORKLOG_REVIEW

- Selector: `node scripts/select-worklogs.mjs --type fix --limit 3`.
- Read `.agents/worklog/2026-11-15/fix-st12-st26-visual-match.md`, `.agents/worklog/2026-11-15/fix-study-web-node-engine.md`, `.agents/worklog/2026-11-15/install-node-and-run-study-web.md`. No shortage.
- Read `.agents/context-map.md`, `.agents/AGENTS.md`, `.agents/web-work/AGENTS.md`, `.agents/web-work/study/INDEX.md`, registered screen workflow, frontend rules, ST-13 UI elements, source and route catalog.

## EXPECTED_BEHAVIOR

- DD reference shows four distinct metric icons, rules/security/scoring/timer/certificate icons, attempt history icon, and academic support icon. It also shows a compact instructor card and fuller static sample copy in the rules panel.

## CURRENT_BEHAVIOR_AND_DISCREPANCY

- Before capture: `.static-preview/st13-playwright-before.png`, 1349px viewport, HTTP 200, no page errors. Four metric icons were Unicode pseudo-elements; rules/history/help icons were absent or represented by text symbols. Instructor card stretched across the full column; rule cards were shorter than DD.
- After capture: `.static-preview/st13-playwright-after.png`, same viewport and route. Eleven SVG icons render: 4 metrics, 5 rules, 1 history, 1 help. No broken images. Mobile 390px has `scrollWidth=390`, 11 icons and no page errors.
- Remaining visual differences: CSS-drawn quiz cover is approximate; shared portal header/footer use existing common styles. No original cover art is available as a standalone asset in this screen package.

## CHANGES

- `ST13/pages/st13-page.html`: static inline SVG icons and DD sample copy for rules.
- `ST13/pages/st13-page.css`: compact instructor card and DD-like rules/history spacing.
- `ST13/pages/st13-icons.css`: screen-local icon styling.
- `ST13/pages/st13-page.ts`: register screen-local icon stylesheet.
- `.static-preview/README.md`: point ST-13 to Playwright before/after comparison images.

## VERIFICATION

- Playwright desktop route capture: PASS (HTTP 200; no page errors).
- Playwright DOM: PASS (11 icons; 4 metrics, 5 rules, 1 history, 1 help; 0 broken images).
- Playwright mobile width 390: PASS (no horizontal overflow or page errors).
- `npm.cmd run build`: PASS. Existing CSS budget warnings remain in ST-22, shared student static CSS and student layout CSS; ST-13 has no budget warning after splitting its stylesheet.
- Dev server on port 51280 was restarted after Angular's hot reload served a transient JIT error following the stylesheet registration change; final Playwright capture succeeded on the restarted server.
- Automated Angular tests: NOT_RUN. Focused Playwright visual and DOM checks cover this static visual change.
- `node scripts/validate-agent-context.mjs`: BASELINE_INVALID. The output reports missing db-admin context/source entries and ORPHAN_CONTEXT_PAGE findings already present in the preceding ST-12–ST-26 worklog; no agent context page was changed by this ST-13 task.
