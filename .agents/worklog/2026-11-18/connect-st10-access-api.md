---
task_id: "2026-11-18-connect-st10-access-api"
date: "2026-11-18"
primary_task_type: "coding"
secondary_task_types: ["test"]
project_scopes: ["web-work"]
cross_scope_dependencies: ["Study Server API #22, #23, #24"]
status: "DONE"
---

# Worklog: ST-10 partial access API connection

## PRIOR_WORKLOG_REVIEW
- primary_task_type: coding
- selector_command: node scripts/select-worklogs.mjs --type coding --limit 3
- prior_worklogs_reviewed:
  - .agents/worklog/2026-11-18/implement-st09-read-apis.md
  - .agents/worklog/2026-11-18/implement-study-auth-session.md
  - .agents/worklog/2026-11-18/review-st10-layout-and-api.md
- shortage: none.

## EXPECTED_BEHAVIOR
- Study FE scope: screens=ST-10; APIs=#22 access (in scope), #23 start and #24 detail (remain blocked).
- DD requires GET #22 before start/content. HTTP 200 is allowed, 403 is denied. Never load or display protected content/media before the full approved flow. No backend edits.
- Only source-backed access check is connected; #23 trigger/retry/idempotency and ST-11 #24 handoff remain open.

## MILESTONES
| Weight | Cumulative | Objective | Status |
|---:|---:|---|---|
| 30% | 30% | Verify #22 source, auth/403 handling and gaps | DONE |
| 50% | 80% | Wire #22 and honest UI states without media or writes | DONE |
| 20% | 100% | Tests, build and live browser check | DONE |

## CURRENT_BEHAVIOR
- ST-10 page/service static blocked; no requests. Frontend #22/#23/#24 descriptors UNWIRED.
- Backend #22 source has route/test, checks JWT Student and ACTIVE/COMPLETED enrollment; 200 DESIGN_RESOURCE_RETRIEVED or 403 DESIGN_ACCESS_DENIED. It returns a LessonResponse including content/video_url and does not check lesson PUBLISHED status. This backend risk cannot be fixed in frontend.
- Auth interceptor redirects every 403 to SH-05; ST-10 DD expects a local denied state. Need a request-scoped opt-out of global 403 redirect for #22 only.
- ST-09 does not hand off a verified lessonId; #23 initiation/retry and #24/ST-11 ownership remain undecided.

## PLAN
- Add request context flag for local 403 handling; default interceptor behavior unchanged.
- Validate route lessonId, call #22 once per route ID, map only safe lesson ID/course ID/title; discard content/video_url and reject malformed success.
- Render checking/allowed/denied/not-found/error states; keep start disabled and do not call #23/#24. Show course-return link from validated #22 course ID only.
- Focused service/page/interceptor tests, build and live negative path. No DB fixtures or write requests.

## CHANGES
- API #22 descriptor is WIRED; ST-10 validates `lessonId`, calls GET `/lessons/{lesson_id}/access`, maps 200 to safe metadata and renders local 403/404/error states. `content` and `video_url` are discarded from view state.
- A request context token lets ST-10 handle its own 403 without changing the default SH-05 redirect for other screens. HTTP 401 still follows the global session flow.
- Progress/FSM/API labels reflect the actual check. A verified course ID provides a return link to ST-09. Start remains disabled; #23/#24 are not called.

## VERIFICATION
- Focused Angular/Vitest suite: 18/18 passing (ST-10 page/service, auth interceptor, API service).
- `npm run build`: passed; existing SH-01 CSS budget warning persists.
- Live IAB at `http://localhost:4200/student/lessons/1/start` with student session: backend returned 403; ST-10 displayed local “Bạn chưa có quyền học bài này”, kept start disabled, and did not redirect to SH-05.
- Backend limitation remains: #22 returns `content`/`video_url` in a successful response and does not itself check lesson `PUBLISHED`. Frontend discards those fields but cannot make the network response private.
