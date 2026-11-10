# SH-02 — Events

## 1. Index
| ID | Trigger | Element | API | Test |
|---|---|---|---|---|
| `SH-02-EV-001` | route mount/courseId change | route | API-001 | TC-001/002/007 |
| `SH-02-EV-002` | Back/breadcrumb click | EL-001/002 | — | TC-008 |
| `SH-02-EV-003` | Chapter header click | EL-006 | — | TC-009 |
| `SH-02-EV-004` | Enroll CTA click | EL-007 | API-002 if authenticated | TC-003/004/005/006 |
| `SH-02-EV-005` | Login return/deep-link | router/auth | API-001 | TC-003 |
| `SH-02-EV-006` | Retry detail load | conditional error CTA | API-001 | TC-010 |

## 2. SH-02-EV-001 — LoadDetail
- **Trigger:** mount `/courses/:courseId` hoặc path param đổi.
- **Input/source:** `courseId` từ router; `isAuthenticated` từ auth provider.
- **Guard:** validate ID nonempty, <=64 chars (BR-005); invalid → not-found không gọi API.
- **Steps:** (1) reset old course/accordion/enroll state; (2) set loading; (3) tăng requestSeq; (4) call GET API-001 có optional auth; (5) ignore stale response; (6) map DTO → CourseDetail; (7) render title/tags/chapters/info/CTA.
- **Errors:** 404/422 → not-found; 5xx/network/timeout → error + retry; route change midflight → ignore old response.
- **Output:** stay `/courses/:courseId`; **Rules:** BR-001/005; **Tests:** TC-001/002/007.

## 3. SH-02-EV-002 — BackToCatalog
- **Trigger:** click back link `EL-001` hoặc breadcrumb link `EL-002`.
- **Steps:** navigate `/courses` directly, no parameter; avoid relying on browser back-stack.
- **Output:** SH-01 mount mới theo defaults; **Test:** TC-008.

## 4. SH-02-EV-003 — ToggleChapter
- **Trigger:** click/keyboard Enter/Space chapter header in `EL-006`.
- **Input/source:** `chapterId` thuộc `course.chapters` từ API-001.
- **Guard:** only success and chapter ID exists in current course.
- **Steps:** if chapterId present in expandedChapterIds remove it; else append; update `aria-expanded` and chapter preview; no API.
- **Output:** local UI only; **Test:** TC-009.

## 5. SH-02-EV-004 — EnrollCourse
- **Trigger:** click CTA `EL-007`.
- **Input/source:** courseId route, auth session, `course.isEnrolled` from GET.
- **Guards:** fetch success; not pending; not already enrolled (BR-003/004).
- **Steps:** (1) if anonymous, navigate `/login?returnUrl=<encoded current path>` and stop; (2) authenticated: set submitting/disabled; (3) POST API-002 `{course_id: courseId}`; (4) 201: set isEnrolled=true, success toast; (5) 409 ALREADY_ENROLLED: set isEnrolled=true, no error toast; (6) stop pending and render CTA disabled.
- **Errors:** 401 → login, 403 → forbidden toast, 404 → not-found, 422 → invalid request message, 5xx/network → error message+allow manual retry; **không auto retry POST**.
- **Race:** double click does not create two POST; backend enforces uniqueness.
- **Navigation:** login only for anonymous/401; **Rules:** BR-002/003/004; **Tests:** TC-003/004/005/006.

## 6. SH-02-EV-005 — ReturnFromLogin
- **Trigger:** user completes login outside this demo and browser follows returnUrl `/courses/{courseId}`.
- **Guard:** returnUrl must be a validated same-origin relative route; no automatic POST.
- **Steps:** (1) navigate back detail; (2) screen invokes EV-001 with new auth session; (3) CTA shows `Đăng ký ngay` unless GET reports enrolled; (4) user explicitly clicks again to enroll.
- **Error:** login failure stays at login flow, outside SH-02 scope; **Test:** TC-003.

## 7. SH-02-EV-006 — RetryDetail
- **Trigger:** click Retry on error banner.
- **Steps:** validate same courseId, set loading, increase requestSeq, repeat GET API-001; success/not-found/error handled as EV-001.
- **Test:** TC-010.

[API](04-api-integration.md) · [Data](03-data-flow.md) · [Navigation](06-navigation.md) · [Tests](07-test-cases.md)
