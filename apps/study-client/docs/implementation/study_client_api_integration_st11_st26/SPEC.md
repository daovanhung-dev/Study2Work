# SPEC: Study Web ST-11–ST-26 API integration (FE only)

## Status
- Revision: 2
- Approval: APPROVED BY USER on 2026-11-17 (SPEC v2 plus approved clarification A-01).
- Revised scope: user clarified FE-only on 2026-11-17. No Study Server implementation.
- Screens: apps/study-client/docs/dd_screens/ST-11 through ST-26.
- API paths, methods, and request/response contracts: current screen DDs and apps/study-client/docs/list_endpoint.md.
- Numeric ID contract and PD-01–PD-06 display/business defaults were approved by the user on 2026-11-17.

## Expected behavior
Connect the existing Study Web screens to the API paths, methods, payloads, and response fields described by their DDs. Preserve approved layouts and icons. Replace sample data with API responses; do not invent records.

This is frontend-only. Build the FE request descriptors/client calls even for APIs that are currently absent from Study Server. A missing server route may return 404; the FE must display the returned error state and must not substitute fake data. The FE does not connect directly to the database.

Keep route IDs as supplied and substitute them into the DD path without converting them to another value. Numeric IDs are expected by the API contract. Do not map a placeholder such as lesson-001 to an invented number. If a placeholder is used, the request may be rejected by the server; an actual numeric ID is needed for a successful request.

The user deferred auth/token and SH-02. Add no login page, token store, interceptor, token issuance, or guard. Protected calls may return 401 until a later auth integration.

## Current behavior after this FE change
- Routes ST-11–ST-26 call the corresponding StudentApiService methods. Read requests start on page load; writes remain behind an explicit learner action or media progress event.
- StudyApiService.request still rejects descriptors marked UNWIRED for existing callers. The Student FE uses requestDeclared for the documented descriptors without changing catalog status.
- Study Server currently wires only #12 and #34 from this screen API set. Other routes still require backend implementation; a request reaching the configured proxy does not prove a server route or database operation exists.
- #12 reads one public resource; #34 uploads a file and does not create a submission.
- Browser verification on the isolated FE dev server (port 51281) reached the configured proxy, but it returned 502 because the Study Server target at 127.0.0.1:3003 did not respond. Successful API response rendering and authenticated requests remain unverified.

## Scope
1. Add FE request descriptors and connect the ST-11–ST-26 screens to their mapped API calls.
2. Use paths, HTTP methods, query parameters, request bodies, and response shapes from the linked DD/API catalog. Do not alter those documents in this task.
3. Reuse the existing FE StudyApiService, ApiEnvelope, loading/error patterns, and page components.
4. Keep existing visual layouts and responsive behavior. Show loading, empty, validation, unauthorized, and API error states as appropriate.
5. Preserve the six approved behavior defaults as FE expectations: lesson/resource eligibility and ordering; quiz attempt/answer/grading states; assignment version and feedback states; progress and persisted achievements; discussion text/order; direct-recipient notifications and read state.
6. Use no fabricated data. Keep route parameter values unchanged when building API paths.

## Screen/API traceability
| Screen | API use |
|---|---|
| ST-11 Lesson player | #24 GET lesson; #25 save progress; #26 list resources; #27 get next lesson |
| ST-12 Lesson resources | #26 list resources; #12 read selected resource |
| ST-13 Quiz introduction | #28 get quiz; #29 create/resume attempt only after Start is pressed |
| ST-14 Quiz attempt | #28 load quiz; use attemptId from the route; #30 save answers; #31 submit |
| ST-15 Confirm quiz submission | #30 save pending answers; #31 submit |
| ST-16 Quiz result | #32 get result |
| ST-17 Assignment detail | #33 get assignment |
| ST-18 Assignment submission | #33 load assignment; #34 upload with course_id; #35 submit |
| ST-19 Submission/feedback | #36 get submission |
| ST-20 Progress overview | #21 progress; #38 achievements |
| ST-21 Course progress | #37 course progress |
| ST-22 Achievements | #38 achievements |
| ST-23 Discussion list | #39 list |
| ST-24 Create discussion | #40 create; #39 reload |
| ST-25 Discussion thread | #42 load; #41 reply |
| ST-26 Notifications | #43 list; #44 mark one read; #45 mark all read |

## Approved FE behavior defaults
- Lessons/resources: present ACTIVE enrollment/PUBLISHED access states returned by API. Position uses seconds and percent uses 0–100. Display #26 resources in API order. Use #27 next-lesson response; null means no next lesson.
- Quizzes: render IN_PROGRESS attempts for resume; do not invent attempt limits. Send selected choice IDs. Keep submitted, PENDING_GRADE, and GRADED states distinct; hide score/correct answers before GRADED.
- Assignments: send text and ordered upload IDs; upload includes course_id. Display the latest version returned by API; show score/feedback only after review.
- Progress/achievements: display completed/total from dedicated #21/#37 progress responses. Display persisted #38 awards only; no screenshot/sample awards.
- Discussions: title/content are text. Follow API order: root topics newest first, replies oldest first. Mutations use the single-resource responses in the approved contract.
- Notifications: display direct-recipient items, use is_read and unread count, sort newest first, page size 20; no invented deep links.

## Out of scope
- All Study Server/backend code, server tests, endpoint implementations, security or DB changes.
- API DD/catalog updates; this task consumes them as written.
- Database connection from browser, repository migrations, live database inspection/change, and sample-data seeding.
- Login/token/auth interceptor/guard and SH-02.
- Mentor/Admin endpoints, unrelated screens, visual redesign, and new UI/icon dependencies.

## Traceability and acceptance
| Requirement | Acceptance |
|---|---|
| R1: cover all screens | Every ST-11–ST-26 route uses only the API operations mapped above. |
| R2: follow DD contracts | FE uses the documented method, path, query, body, and response shape without changing backend contracts. |
| R3: issue requests for unwired APIs | FE descriptors are no longer blocked locally as UNWIRED; requests reach the configured API base URL. |
| R4: represent server outcomes honestly | 401/404/validation/server errors show a usable FE state; no fake successful content is displayed. |
| R5: retain visual design | Existing layout, responsive behavior, and icon styling remain intact. |
| R6: honor approved defaults | UI uses approved statuses and ordering; it does not invent records or convert placeholder IDs. |
| R7: no backend/DB scope creep | No Study Server files, API DD/catalog, migrations, or live database are changed. |

## Known limits
- Most mapped server routes are currently UNWIRED, so FE requests may return 404.
- Student endpoints require authentication; until a later auth integration they may return 401.
- Existing sample route IDs such as lesson-001 are not numeric int64 IDs and cannot produce successful calls to those contracts.
- This revision proposes FE-only implementation and waits for user approval before source edits.

## Approved clarification A-01
- User explicitly approved on 2026-11-17: ST-13 calls API #29 only after the learner presses Start, then navigates to ST-14 with the attempt ID returned by #29. ST-14 must not call #29 again; it uses the route attempt ID for #30 answer saves and hands off to ST-15 for #31 submit.
