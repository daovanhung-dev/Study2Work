---
task_id: "2026-11-15-admin-screens-ad21-layout"
date: "2026-11-15"
primary_task_type: "coding"
secondary_task_types: ["review", "test", "docs"]
project_scopes: ["web-work (Study Web)", "server-study (API #96 source/contract read)"]
cross_scope_dependencies: ["AD-21 Study Client page -> API #96 Study Server GET projection"]
status: "PARTIAL"
---

# Worklog: Align AD-21 notification status layout with truthful API data

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `PATH=/home/daovanhung/.local/opt/node-v22.23.4/bin:$PATH node scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: `READY`; 104 exact-type worklogs available; three selected; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-15/admin-screens-status.md`
    - carry_forward: The previous continuation added AD-21's three disabled actions and verified 3 focused tests; the overall 25-screen goal remains active/incomplete.
  - path: `.agents/worklog/2026-11-14/admin-screens-coding.md`
    - carry_forward: Full cross-screen DD/source audit and latest resumed blocker/API notes; preserve unresolved permissions/lifecycle/contracts, keep no-op actions disabled, and preserve the dirty worktree.
  - path: `.agents/worklog/2026-11-13/commit-study-api-registry.md`
    - carry_forward: Screen services use the typed API registry and generic transport; do not infer behavior from local source outside the direct catalog contract.
- shortage: `none`

## STUDY_FE_SCOPE

- `screens=AD-21; APIs=#18,#94,#95,#96`
- Screen route is a registered local candidate `/admin/notifications/:notificationId`; linked AD-19/SH-07 navigation and live runtime remain unverified.

## EXPECTED_BEHAVIOR

- Original goal: implement AD-01..AD-25 from each screen DD and Stitch visual/interaction reference, integrating only APIs backed by current Study Server source.
- AD-21 canonical package read: `00-overview.md` through `07-test-cases.md`, `images/README.md`, clean/numbered PNGs, Stitch `AD-21.md`, `code.html`, `AD-21_PLAN.md`, and `AD-21_markers.json`.
- Visual target: identity summary, truthful data boundary, two-column content/pipeline workspace, and conditional SH-07 panel. Native update/cancel/SH-07 actions stay disabled and send no request until their contracts are resolved.
- Data/API contract: #96 GET returns `Notification` fields `id/title/content/channels/status/created_at`; preserve raw channel/status values. Do not claim In-App mapping, per-channel progress/count, recipient, schedule, operation ID, delivery success, provider cancellation, health or RBAC state.

## CURRENT_BEHAVIOR

- Current route/page calls `AD21ApiService.getStatus()` through `AdminApiService` for #96 and uses `renderNotificationStatusFields`.
- The response mapping preserves raw channels/status and formats creation time. It does not include recipient, per-channel delivery state/count, schedule, or Operation ID.
- Current page now has the route heading, a three-cell identity summary, a #96 data-boundary notice, a two-column content/monitoring workspace and the SH-07 panel. The three actions remain native-disabled.
- API #96 is registered as a GET. The local query computes delivery counts internally but the response model contains only the existing `Notification` fields. API DD status is `Draft — Needs Confirmation`; local source does not prove production schema/runtime.
- API #18 is unwired; #94 request body and edit gate are derived; #95 local hard delete does not coordinate provider cancellation. Keep the related buttons disabled.

## SOURCE_TRACE

```text
Admin route -> AD21Page -> AD21ApiService.getStatus -> AdminApiService GET API_096 -> Study Server GET /api/v1/admin/notifications/{notification_id}/status -> ADMIN guard/positive int64 -> read-only aggregate query -> AdminNotificationResponse -> renderNotificationStatusFields -> page
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| AD-21 visual hierarchy | Clean/numbered reference has identity cards, notice and 7/5 column workspace; current page is one card plus note. | `DISCREPANCY` | Implement the reference hierarchy with source-backed values. |
| Prototype telemetry | DD/HTML show channel statuses, `0/0`, SMTP and identity/health claims not supplied by #96. | `SOURCE_REQUIRED` | Exclude those values; show aggregate status and explain missing per-channel data. |
| Mutation/operation actions | #94/#95 policy/body is unresolved; #18 has no Study route or compatible ID mapping. | `UNWIRED` / `SOURCE_REQUIRED` | Keep all three native buttons disabled; no handlers or requests. |

## MILESTONES

Progress starts at 0%; bootstrap discovery is not counted again.

| Weight | Cumulative progress when achieved | Objective / acceptance criterion | Status |
|---:|---:|---|---|
| 25% | 25% | Re-read current worktree, selected worklogs, registered screen workflow, all AD-21 DD/assets, catalog, and current #96 source; record the evidenced plan. | COMPLETE |
| 50% | 75% | Implement the AD-21 reference hierarchy using only #96-backed values and explicit unavailable states; keep mutations gated; update component spec. | COMPLETE |
| 25% | 100% | Run relevant tests/build and browser comparison where available, inspect diff/whitespace, and record results/blockers. | COMPLETE_WITH_BROWSER_LIMITATION |

## IMPLEMENTATION_PLAN

- Files in scope: `apps/study-client/src/app/features/admin/AD21/ui/ad21-screen.ui.ts`, `AD21/pages/ad21-page.html`, `ad21-page.css`, and `ad21-page.spec.ts`.
- Update the screen definition title to the approved screen heading visible in the AD-21 DD/Stitch source; retain its current source-bound description.
- Rework the loaded view to show a three-cell identity summary (notification ID, unresolved Operation ID, raw #96 aggregate status), an accurate #96 boundary notice, a two-column read-only notification content/pipeline workspace, and the SH-07 panel.
- Display title, raw channels, content, ID, creation date and raw aggregate status from the current #96 mapping. For recipient, operation and per-channel metrics, state that #96 does not return them; do not add sample values or channel translations.
- Keep update, cancel and SH-07 buttons native-disabled; add no click handlers, navigation, requests, polling or server changes.
- Update focused specs for the new visual landmarks, exact data projection, unavailable fields, raw status preservation and no mutation requests.
- Verification plan: focused AD-21 spec, full Study Client suite, production build, desktop/mobile local route comparison if the browser surface is available, `git diff --check`, scoped whitespace check, and final worklog result.
- Reuse existing StudyIcon and Admin page styling; no new dependency, shared component, route, model or API contract.

## CHANGES

- `apps/study-client/src/app/features/admin/AD21/ui/ad21-screen.ui.ts`: align the screen title with the DD while retaining the source-backed description.
- `apps/study-client/src/app/features/admin/AD21/pages/ad21-page.html`: add the identity summary, truthful data boundary, read-only two-column workspace and SH-07 limitation; preserve native-disabled mutation/navigation controls.
- `apps/study-client/src/app/features/admin/AD21/pages/ad21-page.css`: add responsive desktop/tablet/mobile layout styling scoped to AD21Page.
- `apps/study-client/src/app/features/admin/AD21/pages/ad21-page.spec.ts`: cover visible source fields, missing response fields, raw aggregate status, absence of unsupported telemetry and disabled actions without mutation requests.
- CONTEXT_UPDATES: none expected; no API/business behavior changes.

## VERIFICATION

| Command / evidence | Result | Status |
|---|---|---|
| Focused AD-21 spec: `PATH=/home/daovanhung/.local/opt/node-v22.23.4/bin:$PATH npm test -- --progress=false --include src/app/features/admin/AD21/pages/ad21-page.spec.ts` | 1 spec file, 3 tests passed. | PASS |
| Full Study Client suite: `PATH=/home/daovanhung/.local/opt/node-v22.23.4/bin:$PATH npm test -- --progress=false` | 28 files and 105 tests passed. An earlier process handle could not be retrieved; the command was rerun to obtain terminal evidence. | PASS |
| Production build: `PATH=/home/daovanhung/.local/opt/node-v22.23.4/bin:$PATH npm run build` | Build succeeded; output written to `apps/study-client/dist/study-client`. | PASS |
| Local route HTTP check: `curl -sS -o /dev/null -w '%{http_code}\\n' http://127.0.0.1:4200/admin/notifications/1` | HTTP 200 from local `ng serve`; confirms SPA route serving only, not component/API behavior. | VERIFIED_HTTP_ONLY |
| Browser runtime review via CUA Chrome bridge | `createBrowserTab()` failed with `Cannot read properties of undefined (reading 'timeoutMs')`; no screenshot or visual/keyboard assertion was obtained. | BLOCKED_BY_COMPUTER_USE_BRIDGE |
| `git diff --check` and scoped `awk` trailing-whitespace scan | Both reported no findings. The scoped files are currently untracked in the pre-existing dirty worktree, so the explicit whitespace scan covered them. | PASS |

## HANDOFF

- This AD-21 layout continuation is implemented and has passing focused/full tests and production build. Browser visual/keyboard review remains unverified because the Chrome bridge failed; HTTP 200 is not visual or API acceptance.
- The overall 25-screen goal is still active and incomplete at the previously recorded 85% implementation progress. Missing/unapproved server and product contracts remain open; no change here closes those gates.
- Next action: once the browser bridge is available, compare AD-21 desktop/mobile rendering with the reviewed DD assets; continue the original 25-screen scope only where API/business contracts are evidenced or approved.
