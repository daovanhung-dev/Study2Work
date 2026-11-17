# PLAN: Study Web ST-11–ST-26 API integration (FE only)

## Status
- Revision: 1
- Approval: APPROVED BY USER on 2026-11-17 (PLAN v1 plus approved clarification A-01).
- Parent SPEC: revision 2, FE-only.
- Parent SPEC SHA-256: 154E60CB69D2FFD6899A1B340A1FFDB9078C41DD880BE999A2711DE2D79C3D0F (SPEC v2 plus approved A-01)
- Scope: apps/study-client only. No Study Server, API DD/catalog, migration, or database edits.

## Implementation steps

### 1. Preserve the shared API registry and add an explicit FE path for documented-but-unwired calls
- Keep existing descriptor IDs, methods, paths, and UNWIRED status as they are declared in api.constants.ts.
- Preserve the current StudyApiService.request behavior for callers that rely on its UNWIRED guard.
- Add an explicit request method for Student FE flows that sends a request using the registered DD descriptor even if its backend status is UNWIRED. Reuse the same URL encoding, HttpClient, ApiEnvelope, body, headers, and query handling.
- Do not mark a backend-unwired endpoint WIRED just to get past the FE guard.

### 2. Add a typed Student API facade
- Add feature-scoped request methods and response types under apps/study-client/src/app/features/student.
- Use the existing descriptors for #12, #21, #24–#45; preserve exact DD paths and methods.
- Pass route parameters into the path unchanged; do not translate textual placeholders to guessed numbers.
- Use the documented bodies, headers, query values, and envelope shapes. Use FormData for the existing #34 upload path.

### 3. Connect screens in vertical slices
- Lessons/resources: ST-11 and ST-12 using #24–#27, #26, and #12.
- Quizzes: ST-13–ST-16 using #28–#32.
- Assignments: ST-17–ST-19 using #33–#36.
- Progress/achievements: ST-20–ST-22 using #21, #37, and #38.
- Discussions: ST-23–ST-25 using #39–#42.
- Notifications: ST-26 using #43–#45.
- Replace sample fields with API-bound data and connect existing buttons/forms to their mapped request. Preserve the layouts and icon assets.

### 4. Add honest request states
- Show loading, empty, validation, 401 unauthorized, and server/API error states in the relevant screen region.
- Do not show static sample business data as if it came from the API.
- Keep writes behind the existing user action; do not submit on page load.
- On a failed write, preserve the user-entered form/answer state so the user can retry where the API contract permits it.

### 5. Verify the FE-only result
- Run npm run build from apps/study-client.
- Use the already requested Playwright browser inspection for the 16 routes to check layout, request URLs, and error states. Since most Study Server routes are absent and auth is deferred, expect 404/401 responses; do not claim successful backend integration.
- Do not run automated test commands unless the user explicitly asks.
- Record build/browser outcomes and any environment blockers in the task worklog.

## Target FE files

- apps/study-client/src/app/core/http/study-api.service.ts: explicit request path for documented-but-unwired descriptors while preserving existing guarded behavior.
- apps/study-client/src/app/features/student/data/: Student API facade and typed API models.
- apps/study-client/src/app/features/student/ST11/pages through ST26/pages: API binding and request states in the existing page components/templates.
- Other Study Client source files only if required by the existing route or shared error-state pattern.

No file under apps/study-server, apps/study-client/docs/dd_screens, apps/study-server/docs/dd, or infra/postgres is in the edit plan.

## Acceptance checklist
- All mapped ST-11–ST-26 pages issue requests through the registered DD method/path.
- Existing callers of StudyApiService.request retain the UNWIRED rejection behavior.
- The new explicit Student request path can send requests for the documented UNWIRED descriptors without falsely changing their backend status.
- API errors, including expected 401/404 outcomes, appear in the FE without fabricated fallback data.
- Submission and answer actions are user-triggered and use their mapped API methods.
- The existing approved layouts and icons remain intact.
- Only Study Client FE source and this task worklog are changed.

## Risks and limits
- Most backend routes do not exist yet; request delivery is verifiable, successful API responses are not.
- Auth/token integration is deferred; protected requests may return 401.
- Existing sample route IDs such as lesson-001 are not valid int64 IDs; they are not converted to invented numeric IDs.
- PLAN v1 was approved by the user on 2026-11-17; clarification A-01 below is also explicitly approved and implementation is authorized under both approvals.

## Verification result
- `npm.cmd run build`: PASS, with existing CSS budget warnings.
- Playwright opened and captured all 16 routes on the isolated FE dev server. Read requests returned 502 through the configured proxy (`127.0.0.1:3003` unavailable); no Angular template/runtime errors were observed. Write endpoints were not triggered during browser inspection.
- Automated tests: NOT_RUN (not requested).

## Approved clarification A-01

- User explicitly approved on 2026-11-17: ST-13 calls API #29 only after the learner presses Start, then navigates to ST-14 with the attempt ID returned by #29. ST-14 must not call #29 again; it uses the route attempt ID for #30 answer saves and hands off to ST-15 for #31 submit.
- This clarification resolves the #29 call-site conflict in the screen DDs and amends the ST-13/ST-14 rows above. The user approved this exact behavior in chat; it is not a backend or database change.
