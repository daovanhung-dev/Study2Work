# SPEC: Remaining unambiguous Study Web interactions, ST-11–ST-26

- Revision: 1
- Status: Draft for user approval
- Scope approval: User approved FE-only implementation of DD interactions that are clear; blocked behavior stays unavailable.
- Related baseline: existing FE API integration source and its approved SPEC/PLAN remain unchanged.
- Trace source: screen DD event packages, current Study Client source, and user-approved PD-01–PD-06 in `.agents/worklog/2026-11-17/study-client-api-integration-st11-st26.md`.

## Goal

Complete the remaining FE interactions that have enough approved behavior to implement without changing the Study Server, authentication, database, migrations, or canonical DD/API files. Do not add fabricated business data or imply blocked behavior is live.

## Scope

### R1 — ST-14 question navigation (ST14-EV-04, navigation subset)

1. Display one question at a time from the questions returned by API #28.
2. Use the exact array order returned by the API; do not sort or infer a separate question order.
3. Start at the first question when the response contains questions. Previous and next controls move by one array index; disable previous at the first item and next at the last item. Question-grid buttons select the corresponding item.
4. Navigation changes only the displayed question. It does not call an API, submit the attempt, change answer values, or claim a saved/answered state.
5. Keep `selectedChoices` keyed by question ID so selections made in this page instance remain visible when navigating away and back.
6. If the quiz has no questions, do not show navigation controls.
7. Preserve ST-13 as the sole owner of POST #29 and the attempt ID handoff, as previously approved by the user.

The unanswered filter is excluded because the current attempt's saved answers are not hydrated on ST-14. Review flags, timer/expiry, keyboard shortcuts, resume/restore, and save ordering/retry are also excluded until their source contracts are resolved.

### R2 — ST-26 all/unread filter (ST26-EV-04/05)

1. Provide only the “Tất cả thông báo” and “Chưa đọc” filters. Category tabs are excluded.
2. “Tất cả” requests API #43 with `page=1` and omits `unread_only`. “Chưa đọc” requests `unread_only=true` and `page=1`. Send no undeclared query parameters.
3. Mark-one and mark-all actions continue using #44/#45. After either successful mutation, reload page 1 using the currently selected all/unread filter; do not optimistically change rows or counts.
4. Display row read state or the mark-one action only when the response provides the approved `is_read` property. Do not derive unread count from the current page or screenshot.
5. Keep deep-link destinations, category filters, notification preferences, weekly metrics, and coordinator links unavailable because the current contract has no approved destination or fields.

PD-06 approved `is_read` and direct-recipient semantics, but current ST-26/API catalog schema still omits `is_read`. Record this as a contract discrepancy; the FE may consume the optional property if the API returns it, and this task does not change the catalog or backend.

## Existing behavior retained

Keep the existing API integrations and actions already present on ST-11–ST-26, including lesson/resource loads, quiz start/answer save/submit/result, assignment load/upload/submit/submission, progress/achievement/discussion loads and mutations, and notification mark-read actions. Do not reimplement or broaden their request contracts in this task.

## Screen coverage and limits

| Screen | Current main FE behavior | Remaining DD behavior in this task |
|---|---|---|
| ST-11 | Lesson load/player progress and lesson navigation calls exist. | No new action; course-return/footer/resource URL policy remains unresolved. |
| ST-12 | Resource list/detail load and return link exist. | No new action; safe open/download and help destination remain blocked. |
| ST-13 | Quiz load and explicit start/attempt handoff exist. | No new action; history and lesson handoff remain blocked. |
| ST-14 | Quiz load, answer selection/save and submit navigation exist. | Add bounded question navigation/grid only; filter/flag/timer/shortcuts/restore remain blocked. |
| ST-15 | Submit confirmation and explicit #31 action exist. | No new action; flush/order/ambiguous recovery and screenshot counts remain blocked. |
| ST-16 | #32 result and GRADED disclosure are represented. | No new action; answer review/filter lacks approved projection/order and related destinations. |
| ST-17 | Assignment load and submit-route link exist. | No new action; deadline eligibility, checklist, resources and mentor destinations remain blocked. |
| ST-18 | Assignment load, text, #34 upload and #35 submit exist. | No new action; URL mapping, preview/removal, draft lifecycle and integrity policy remain blocked. |
| ST-19 | Submission load/display exists. | No new action; file access, rubric/comments and related destinations remain blocked. |
| ST-20 | Progress/achievement requests and links exist. | No new action; progress DTO/aggregation and empty-state routes remain unresolved. |
| ST-21 | Course-progress request and return link exist. | No new action; response is not an approved progress DTO; lesson access handoff remains blocked. |
| ST-22 | Achievement list request/display exists. | No new action; proof/PDF/share/filter fields or destinations are unavailable. |
| ST-23 | Discussion list and create/open links exist. | No new action; course filter, sort selector and pagination need query decisions. |
| ST-24 | Topic form and create request exist. | No new action; course options, tags, formatting/preview and attachment mapping remain blocked. |
| ST-25 | Thread load and general reply exist. | No new action; vote/bookmark/targeted reply and Markdown/source destinations remain blocked. |
| ST-26 | Notification list, mark-one and mark-all exist. | Add all/unread filters with the approved #43 query mapping above; category/deep-link/settings/statistics remain blocked. |

## Out of scope

- Any Study Server/BE, auth/token, database, migration, API catalog, canonical DD, route inventory, or deployment edits.
- Fake records, screenshot sample values, local success simulation, invented counts, route destinations, URL probing, or client-side authorization decisions.
- Guessing behavior for controls whose DD/API contract is marked BLOCKED, Draft, or unresolved.

## Acceptance criteria

- AC-1: ST-14 question controls move through only the API-returned array and preserve this page instance's selected choices; navigation itself makes no network request.
- AC-2: ST-26 all/unread controls send only the approved query parameters and the active filter survives successful #44/#45 refresh.
- AC-3: No fake totals, unread counts, answer state, timer, categories, or deep links are introduced.
- AC-4: Existing actions and loading/error behavior remain intact.
- AC-5: Build and focused browser interaction verification pass; any API/server/auth limitation is reported separately from FE behavior.
- AC-6: Final source diff is reviewed without staging or changing unrelated dirty work.

## Verification plan

After PLAN approval and implementation: run the Study Client production build and focused Playwright interaction checks for ST-14 and ST-26 at desktop and mobile viewports. Use only isolated test interception if the required API is unavailable; label such runs as FE interaction checks, not real API verification. Do not retain credentials, cookies, or raw request captures.
