---
task_id: "2026-11-18-implement-st09-read-apis"
date: "2026-11-18"
primary_task_type: "coding"
secondary_task_types: ["test"]
project_scopes: ["web-work"]
cross_scope_dependencies: ["Study Server API #09, #20, #37"]
status: "COMPLETE"
---

# Worklog: ST-09 verified read-only API flow

## PRIOR_WORKLOG_REVIEW
- primary_task_type: coding
- selector_command: node scripts/select-worklogs.mjs --type coding --limit 3
- prior_worklogs_reviewed:
  - .agents/worklog/2026-11-18/implement-study-auth-session.md
  - .agents/worklog/2026-11-15/implement-st11-static-layout.md
  - .agents/worklog/2026-11-15/implement-st12-st26-static-layouts.md
- shortage: none.

## EXPECTED_BEHAVIOR
- Study FE scope: screens=ST-09; APIs=#20 membership, #37 course progress, #09 public curriculum. #22/ST-10 is downstream and remains out of scope.
- DD order: verify authenticated course membership with #20 before loading #37 and public #09. Public #09 must never prove entitlement or media access.
- DD loaded tree/per-lesson progress and lessonId handoff are unresolved; only render sourced course identity, aggregate progress and public lesson titles, with no player/lesson action.

## MILESTONES
| Weight | Cumulative | Objective | Status |
|---:|---:|---|---|
| 35% | 35% | Verify DD/source contracts and access sequence | DONE |
| 45% | 80% | Wire read-only APIs and honest states | DONE |
| 20% | 100% | Focused tests and live local browser | DONE |

## CURRENT_BEHAVIOR
- Student guard protects /student/courses/:courseId. ST-09 service returns blocked and makes no requests.
- Backend #20 returns paginated user-scoped CourseSummaryPage; backend #37 returns CourseProgress using ACTIVE enrollment JOIN; #09 returns only PUBLISHED public lessons but includes content/video_url fields that must not be exposed here.
- Frontend registry marks #20/#09 WIRED, #37 UNWIRED despite backend route source. ST-08 already consumes #20 for course list.
- DD response claims ApiEnvelope<UserProfile> for #20/#37 and backend-route absence are stale; current source wins for wire shape. UI specification for loaded per-lesson state remains DD BLOCKED.

## SOURCE_TRACE
Student route/guard -> ST-09 page -> screen data-access -> StudyApiService descriptors -> auth interceptor -> backend #20, then #37/#09. No mutation or DB fixture.

## IMPLEMENTATION_PLAN
- Validate route ID; start loading only for valid ID.
- In ST-09 data-access, query ACTIVE #20 pages until matching course or exhausted; strictly validate envelope and IDs. Do not fetch #37/#09 unless membership is verified.
- After membership, fetch #37 and #09. Map only backend-confirmed aggregate fields and public lesson id/title/order; discard public content/video_url. Treat malformed payloads and errors as unavailable, not enrolled.
- Update #37 registry to WIRED based on current backend source. Keep #22/ST-10 disabled.
- Use existing gated design for missing/not-enrolled/errors; add minimal verified summary for sourced data. Do not invent per-lesson progress or playback.
- Focused service/page tests, build, live negative-path check. Current QA account has no enrollment; no test DB fixture will be created.

## CHANGES
- Added strict ST-09 read-only data access: #20 ACTIVE membership search across pages, then #37 lesson progress, then #09 published public lesson titles. No #37/#09 request before membership; public content and media fields are discarded.
- Page handles invalid ID, loading, no active enrollment, API failure and verified course. It renders only sourced name, lesson progress and public lesson titles. ST-10 action remains disabled. No backend or write endpoint changed.
- Updated #37 registry to WIRED, registry test counts, ST-09 service/page tests and Study context index.

## VERIFICATION
- `npm test -- --include=src/app/features/student/ST09/**/*.spec.ts --include=src/app/core/http/study-api.service.spec.ts`: 3 files, 21 tests passed.
- `npm run build`: passed. Existing SH-01 CSS budget warning remains.
- In-app browser `/student/courses/1`, logged-in QA account: #20 found no active enrollment; screen showed `Bạn chưa ghi danh khóa học này.`, ST-10 disabled. No enrolled QA account was available for live positive verification; tests cover the positive response path.
- `node scripts/validate-agent-context.mjs`: failed on pre-existing missing db-admin/source paths, orphan context pages and git access.
