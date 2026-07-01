# API Checklist — Study2Work Study Scope

| Field | Value |
|---|---|
| Checklist ID | `API-CHECKLIST-STUDY` |
| Last updated | `2026-07-01` |
| Scope | Study-only APIs for learning, practice, assessment, mentor workflow, project teamwork, AI learning support, community, notification and platform governance |
| Source BD | `docs/BD/Study2Work_Study_BD_Codex_Ready.md` |
| Diagram source | `docs/diagrams/` |
| API DD template | `docs/DD/Study2Work_API_DD_Template/` |
| Status model | `.agent/context/STATUS_MODEL.md` |

## 1. Scope Guard

This checklist is the single API checklist for the Study scope. It is used before creating one API Detail Design (DD) per API operation.

Do not add employer, recruitment, job, application, shortlist, offer, CV builder, AI CV review or AI interview assistant APIs here unless a separate approved BD/DD expands scope.

## 2. Completion Scale

Use the `DD status` values from `.agent/context/STATUS_MODEL.md`. The numeric completion is a planning indicator for the API DD package:

| Completion | Meaning |
|---:|---|
| 0% | API identified in checklist only; API DD has not started. |
| 20% | API DD folder copied from `docs/DD/Study2Work_API_DD_Template/`; History initialized. |
| 40% | Overview and Request completed with actor, endpoint, permission, field dictionary and validation. |
| 60% | Response and Error completed with envelope, business codes, safe messages and client behavior. |
| 80% | DataMapping completed with runtime flow, table access, transaction, events, logs and tests. |
| 100% | API DD reviewed, approved and traceable to BD, diagrams, OpenAPI/DTO, tests and worklog evidence. |

## 3. Global API DD Requirements

Every API DD created from this checklist must include:

- One API operation only; do not combine create/update/delete in one DD.
- BD trace, use case/activity/sequence diagram trace and affected bounded context.
- HTTP method, endpoint, caller, auth scheme, role, permission and ownership/scope rule.
- Request field dictionary covering path/query/header/body/file, required, nullable, default, enum, format, example and sensitive class.
- Response envelope with `businessCode`, `message`, `timestamp`, `traceId`, `data` or `errors`.
- Error catalog with HTTP status, stable business code, safe message, client action, retry policy, log/alert owner and test ID.
- DataMapping sequence: parse, validate, authenticate, authorize, load, apply business rule, write/query, transaction, audit/outbox/event, response mapping.
- Transaction, idempotency, concurrency, audit and async behavior for mutation APIs.
- Unit, integration/API and negative tests for validation, permission, ownership, state transition and retry/concurrency where relevant.

## 4. Implemented Backend Foundation Endpoint

This endpoint verifies the FastAPI foundation only. It is not a Study business API and does not bypass the API DD approval rule for future business endpoints.

| API | Module | Method | Endpoint | Caller | Purpose | Status | Evidence |
|---|---|---|---|---|---|---|---|
| `SYSTEM-HEALTH-001` | SYSTEM | GET | `/api/v1/health` | Public/system monitor | Return the standard response envelope with service status, environment and trace propagation. | `IMPLEMENTED` | `.agent/worklog/2026-07/0002_context_backend_refactor.md`; `services/api/tests/test_health.py` |

## 5. Canonical APIs From Approved BD Catalogue

These APIs come directly from BD section `10.4 Study API catalogue`. DD work may start from these rows, but code still requires the API DD to reach `APPROVED`.

| API | Module | Method | Endpoint | Caller | DD seed / business purpose | Rules and DD focus | Primary data / side effects | Diagram trace | DD status | Completion |
|---|---|---|---|---|---|---|---|---|---|---:|
| `AUTH-REGISTER-001` | AUTH | POST | `/api/v1/auth/register` | Guest | Create a pending Study account, assign default role and request email verification. | Enforce `BR-AUTH-001`, `BR-AUTH-002`, `BR-AUTH-003`; define duplicate email/phone behavior without account enumeration; never return password/token secrets. | `user`, `user_role`, `verification_token`, `audit_log`; publish `UserRegistered`, `NotificationRequested` after commit. | `02_activity/01_Dang_ky_va_kich_hoat_tai_khoan.puml`, `04_sequence/01_Register_Verify_Email.puml`, `03_class/01_Identity_Profile.puml` | `NOT_STARTED` | 0% |
| `AUTH-LOGIN-001` | AUTH | POST | `/api/v1/auth/login` | Guest | Authenticate credential and create session/access-refresh token pair. | Enforce status lifecycle; non-enumerating credential errors; rate limit and secret masking. | `user`, `session`, `refresh_token`, `audit_log`; update `last_login_at`. | `02_activity/02_Dang_nhap_refresh_logout.puml`, `04_sequence/02_Login_Refresh_Logout.puml` | `NOT_STARTED` | 0% |
| `AUTH-VERIFY-001` | AUTH | POST | `/api/v1/auth/verify-email` | Guest | Validate verification token and activate a pending account. | Token expiry, already-used token, `PENDING -> ACTIVE` transition and safe replay behavior must be explicit. | `user`, `verification_token`, `audit_log`; publish `EmailVerified`. | `02_activity/01_Dang_ky_va_kich_hoat_tai_khoan.puml`, `04_sequence/01_Register_Verify_Email.puml` | `NOT_STARTED` | 0% |
| `AUTH-OAUTH-001` | AUTH | GET/POST | `/api/v1/auth/oauth/{provider}` | Guest | Start and complete Google/GitHub OAuth sign-in for Study identity. | Provider allowlist, callback validation, state/nonce, identity linking and no raw OAuth secret logging. | `user`, `user_role`, `session`, `refresh_token`; audit login/link outcome. | `04_sequence/02_Login_Refresh_Logout.puml`, `03_class/01_Identity_Profile.puml` | `NOT_STARTED` | 0% |
| `AUTH-REFRESH-001` | AUTH | POST | `/api/v1/auth/refresh` | Student/Mentor/Admin | Rotate refresh/access token for an active session. | Refresh token hash lookup, revocation, expiry, rotation replay protection and one-time-use semantics. | `session`, `refresh_token`, `audit_log`; revoke old token, persist new token hash. | `02_activity/02_Dang_nhap_refresh_logout.puml`, `04_sequence/02_Login_Refresh_Logout.puml` | `NOT_STARTED` | 0% |
| `AUTH-LOGOUT-001` | AUTH | POST | `/api/v1/auth/logout` | Student/Mentor/Admin | Revoke current session/refresh token. | Authenticated actor must only revoke own session unless admin flow is separately approved. | `session`, `refresh_token`, `audit_log`; invalidate cache/session if used. | `02_activity/02_Dang_nhap_refresh_logout.puml`, `04_sequence/02_Login_Refresh_Logout.puml` | `NOT_STARTED` | 0% |
| `USER-PROFILE-001` | USER | GET | `/api/v1/me` | Student/Mentor/Admin | Return current actor profile, role and baseline skill projection. | Self-only profile read; no private data of other users; profile is separate from identity root. | `user`, `profile`, `student_profile`, `mentor_profile`, `user_skill`. | `02_activity/03_Cap_nhat_ho_so_va_ky_nang_nen.puml`, `04_sequence/03_Profile_Skills.puml` | `NOT_STARTED` | 0% |
| `USER-PROFILE-002` | USER | PATCH | `/api/v1/me/profile` | Student/Mentor | Update own profile fields and role-specific profile extension. | Self-only update, whitelisted fields, PII classification, audit meaningful profile changes. | `profile`, `student_profile`, `mentor_profile`, `audit_log`. | `02_activity/03_Cap_nhat_ho_so_va_ky_nang_nen.puml`, `04_sequence/03_Profile_Skills.puml` | `NOT_STARTED` | 0% |
| `USER-SKILL-001` | USER | PUT | `/api/v1/me/skills` | Student/Mentor | Update declared baseline skills only; does not set assessed skill level. | `user_skill` is projection/baseline; do not overwrite `skill_assessment` evidence. | `skill`, `user_skill`, `audit_log`. | `02_activity/03_Cap_nhat_ho_so_va_ky_nang_nen.puml`, `04_sequence/03_Profile_Skills.puml` | `NOT_STARTED` | 0% |
| `LEARN-PATH-001` | LEARNING | GET | `/api/v1/learning-paths` | Student | List published or eligible learning paths for the student. | Pagination required; only `PUBLISHED`/eligible paths; no unbounded list. | `learning_path`, `learning_path_stage`, `module`; read-only. | `02_activity/05_Enroll_va_hoc_lesson.puml`, `03_class/02_Learning_Journey.puml` | `NOT_STARTED` | 0% |
| `LEARN-PATH-002` | LEARNING | POST | `/api/v1/learning-paths/{pathId}/enroll` | Student | Enroll or assign a learning path and seed initial progress. | Eligibility, uniqueness, idempotency, `learning_path_enrollment` source of access. | `learning_path_enrollment`, `learning_progress`, `audit_log`; publish `LearningPathEnrolled`. | `02_activity/05_Enroll_va_hoc_lesson.puml`, `04_sequence/05_Enroll_Learning_Path.puml` | `NOT_STARTED` | 0% |
| `LEARN-PLACEMENT-001` | LEARNING | POST | `/api/v1/placement-tests/{testId}/attempts` | Student | Submit placement test, calculate baseline level and create skill evidence. | Quiz snapshot, answer validation, score/level calculation, optional path assignment trace. | `quiz_attempt`, `quiz_answer`, `skill_assessment`; may publish `LearningPathAssigned`. | `02_activity/04_Placement_va_cap_lo_trinh.puml`, `04_sequence/04_Placement_Assign_Path.puml` | `NOT_STARTED` | 0% |
| `LEARN-LESSON-001` | LEARNING | GET | `/api/v1/lessons/{lessonId}` | Student | Read an unlocked lesson and its content. | Enforce `BR-LEARN-001`; enrollment ownership and unlock rule; no draft content to student. | `lesson`, `lesson_content`, `learning_path_enrollment`, `learning_progress`; read-only. | `02_activity/05_Enroll_va_hoc_lesson.puml`, `04_sequence/06_Lesson_Progress.puml` | `NOT_STARTED` | 0% |
| `LEARN-PROGRESS-001` | LEARNING | POST | `/api/v1/lessons/{lessonId}/progress` | Student | Record start, position or completion event for a lesson. | Enforce `BR-LEARN-002`; server-side completion threshold; no client-forced completion. | `learning_progress`, `audit_log`; publish `LessonStarted` or `LessonCompleted`. | `02_activity/06_Tien_do_bookmark_comment_live.puml`, `04_sequence/06_Lesson_Progress.puml` | `NOT_STARTED` | 0% |
| `LEARN-BOOKMARK-001` | LEARNING | PUT | `/api/v1/lessons/{lessonId}/bookmark` | Student | Toggle or upsert a lesson bookmark idempotently. | Enforce bookmark uniqueness `(user_id, lesson_id)` and enrollment visibility. | `bookmark`; idempotent write. | `02_activity/06_Tien_do_bookmark_comment_live.puml`, `04_sequence/07_Bookmark_Comment_Live.puml` | `NOT_STARTED` | 0% |
| `LEARN-COMMENT-001` | LEARNING | POST | `/api/v1/lessons/{lessonId}/comments` | Student/Mentor | Create a lesson discussion comment. | Comment owner, lesson visibility, moderation status and safe content validation. | `lesson_comment`, `audit_log`; may publish moderation/notification event. | `02_activity/06_Tien_do_bookmark_comment_live.puml`, `04_sequence/07_Bookmark_Comment_Live.puml` | `NOT_STARTED` | 0% |
| `LEARN-LIVE-001` | LEARNING | GET | `/api/v1/live-sessions` | Student/Mentor | List live sessions within learner or mentor scope. | Enrollment/scope filtering, pagination, visibility of meeting URL. | `live_session`, `learning_path_enrollment`; read-only. | `02_activity/06_Tien_do_bookmark_comment_live.puml`, `04_sequence/07_Bookmark_Comment_Live.puml` | `NOT_STARTED` | 0% |
| `LEARN-QUIZ-001` | ASSESSMENT | POST | `/api/v1/quizzes/{quizId}/attempts/{attemptId}/submit` | Student | Submit quiz attempt, score answer snapshot and update progress/skill evidence. | Enforce `BR-ASSESS-001`; attempt status/time limit, snapshot version, no client-trusted score. | `quiz_attempt`, `quiz_answer`, `learning_progress`, `skill_assessment`, `audit_log`; publish `QuizSubmitted`. | `02_activity/07_Quiz_attempt_submit_score.puml`, `04_sequence/08_Quiz_Submit.puml` | `NOT_STARTED` | 0% |
| `ASSESS-SUBMISSION-001` | ASSESSMENT | POST | `/api/v1/assignments/{assignmentId}/submissions` | Student | Create assignment/code submission and queue grading when applicable. | Enforce `BR-ASSESS-002`, `BR-ASSESS-003`; deadline, versioning, file safety, idempotency, async grading. | `assignment_submission`, `file_asset`, `audit_log`; publish `AssignmentSubmitted` and grading job. | `02_activity/08_Assignment_submission_auto_grade.puml`, `04_sequence/09_Assignment_Submission.puml` | `NOT_STARTED` | 0% |
| `ASSESS-GRADE-001` | ASSESSMENT | POST | `/api/v1/submissions/{submissionId}/grade` | System Worker | Persist auto-grade outcome from isolated grader. | Service identity only; hidden tests/runner details never exposed; output becomes evidence after validation. | `assignment_submission`, `review_report`, `skill_assessment`; publish `AutoGradingCompleted`. | `02_activity/08_Assignment_submission_auto_grade.puml`, `04_sequence/10_Auto_Grade_Result.puml` | `NOT_STARTED` | 0% |
| `MENTOR-REVIEW-001` | MENTOR | POST | `/api/v1/submissions/{submissionId}/reviews` | Mentor | Create a rubric-based review for an assigned submission. | Enforce `BR-MENTOR-001`, `BR-MENTOR-002`, `BR-ASSESS-004`; rubric version and required criteria. | `review`, `feedback`, `rubric`, `skill_assessment`, `audit_log`; publish `SubmissionReviewed`, `SkillLevelUpdated`. | `02_activity/09_Mentor_review_skill_evidence.puml`, `04_sequence/11_Mentor_Review.puml` | `NOT_STARTED` | 0% |
| `MENTOR-REVIEW-002` | MENTOR | PATCH | `/api/v1/reviews/{reviewId}` | Mentor | Update a draft or pending review before finalization. | Mentor assigned scope, review editable state, optimistic concurrency and immutable finalized review. | `review`, `feedback`, `audit_log`. | `02_activity/09_Mentor_review_skill_evidence.puml`, `04_sequence/11_Mentor_Review.puml` | `NOT_STARTED` | 0% |
| `SKILL-MATRIX-001` | ASSESSMENT | GET | `/api/v1/me/skill-matrix` | Student | Read evidence-backed skill matrix projection for the current student. | Enforce `BR-ASSESS-005`; projection must trace to evidence and not be directly edited by UI. | `user_skill`, `skill_assessment`, `review`; read-only projection. | `02_activity/10_Skill_matrix_dashboard.puml`, `04_sequence/12_Skill_Matrix.puml` | `NOT_STARTED` | 0% |
| `PROJECT-TEAM-001` | PROJECT | POST | `/api/v1/projects/{projectId}/teams` | Student | Create a team for a project according to project policy. | Enforce project availability, team policy and member role rules. | `project`, `team`, `team_member`, `audit_log`; publish `TeamCreated`. | `02_activity/11_Project_team_join.puml`, `04_sequence/13_Project_Team.puml` | `NOT_STARTED` | 0% |
| `PROJECT-TEAM-002` | PROJECT | POST | `/api/v1/teams/{teamId}/members` | Student/Mentor | Join or add a team member according to policy. | Enforce `BR-PROJECT-001`; duplicate membership and mentor scope checks. | `team_member`, `audit_log`; publish `TeamMemberJoined`. | `02_activity/11_Project_team_join.puml`, `04_sequence/13_Project_Team.puml` | `NOT_STARTED` | 0% |
| `PROJECT-SPRINT-001` | PROJECT | POST | `/api/v1/projects/{projectId}/sprints` | Student/Mentor | Create a sprint within a project/team scope. | Project/team scope, sprint date/status policy and audit. | `sprint`, `audit_log`. | `02_activity/12_Sprint_task_worklog.puml`, `04_sequence/14_Sprint_Task.puml` | `NOT_STARTED` | 0% |
| `PROJECT-TASK-001` | PROJECT | POST | `/api/v1/projects/{projectId}/tasks` | Student/Mentor | Create a project task within project/sprint boundary. | Enforce `BR-PROJECT-003`; assignee/team scope and sprint boundary. | `task`, `audit_log`; may publish `TaskAssigned`. | `02_activity/12_Sprint_task_worklog.puml`, `04_sequence/14_Sprint_Task.puml` | `NOT_STARTED` | 0% |
| `PROJECT-TASK-002` | PROJECT | PATCH | `/api/v1/tasks/{taskId}/status` | Student/Mentor | Transition task status and optionally record work evidence. | Enforce `BR-PROJECT-002`, optimistic concurrency and project/team scope. | `task`, `work_log`, `audit_log`; publish `TaskStatusChanged`. | `02_activity/12_Sprint_task_worklog.puml`, `04_sequence/14_Sprint_Task.puml` | `NOT_STARTED` | 0% |
| `PROJECT-PR-001` | PROJECT | POST | `/api/v1/tasks/{taskId}/pull-request-reviews` | Student/Mentor | Record verified PR review evidence against a task. | Verify Git provider data; do not trust webhook/client raw data; task/project scope. | `pull_request_review`, `task_comment`, `audit_log`. | `02_activity/13_Git_PR_project_submission.puml`, `04_sequence/15_Task_PR_Review.puml` | `NOT_STARTED` | 0% |
| `PROJECT-SUBMIT-001` | PROJECT | POST | `/api/v1/projects/{projectId}/submissions` | Student | Submit project artifact/version for a team/project. | Project/team scope, file safety, immutable versioned artifact and audit. | `project_submission`, `file_asset`, `audit_log`; publish `ProjectSubmitted`. | `02_activity/13_Git_PR_project_submission.puml`, `04_sequence/16_Project_Submission.puml` | `NOT_STARTED` | 0% |
| `AI-ROADMAP-001` | AI | POST | `/api/v1/ai/roadmap-suggestions` | Student | Generate a scoped learning roadmap suggestion. | Enforce `BR-AI-001`, `BR-AI-002`; rate limit, consent/context, redaction, async if needed. | `ai_request`, `roadmap_suggestion`, `ai_insight`; provider call/job; never overwrite source of truth. | `02_activity/14_AI_roadmap_code_explanation.puml`, `04_sequence/17_AI_Roadmap.puml` | `NOT_STARTED` | 0% |
| `AI-CODE-001` | AI | POST | `/api/v1/ai/code-explanations` | Student/Mentor | Explain code or debugging concept from authorized context. | Secret/PII redaction, prompt retention, provider failure/retry, output disclaimer. | `ai_request`, `code_explanation_request`, `ai_insight`; provider call/job. | `02_activity/14_AI_roadmap_code_explanation.puml`, `04_sequence/18_AI_Code_Explanation.puml` | `NOT_STARTED` | 0% |
| `ADMIN-CONTENT-001` | ADMIN | POST | `/api/v1/admin/learning-paths` | Admin | Create or modify the learning content tree. | Enforce `BR-ADMIN-001`; content publish state, audit, no student access to draft content. | `learning_path`, `module`, `lesson`, `audit_log`; publish `LearningContentPublished` if applicable. | `02_activity/16_Admin_content_rubric_publish.puml`, `04_sequence/19_Admin_Content_Rubric.puml` | `NOT_STARTED` | 0% |
| `ADMIN-RUBRIC-001` | ADMIN | POST | `/api/v1/admin/rubrics` | Admin | Create, version or publish a rubric. | Rubric versioning, criterion completeness, weights, publish audit. | `rubric`, `rubric_criterion`, `audit_log`. | `02_activity/16_Admin_content_rubric_publish.puml`, `04_sequence/19_Admin_Content_Rubric.puml` | `NOT_STARTED` | 0% |
| `ADMIN-MENTOR-001` | ADMIN | PATCH | `/api/v1/admin/mentors/{mentorId}/scope` | Admin | Assign mentor scope for learner/team/project review access. | Enforce `BR-ADMIN-001`, mentor scope boundaries and audit. | `mentor_profile`, `audit_log`; affects mentor authorization scope. | `02_activity/15_Admin_user_mentor_scope.puml`, `04_sequence/20_Admin_Mentor_Scope.puml` | `NOT_STARTED` | 0% |

## 6. Candidate APIs Required For Full Study Coverage

The rows below are inferred from BD functional sections, commands/queries and diagrams, but they are not present in BD section `10.4 Study API catalogue`. Keep them as `OPEN_QUESTION` and do not create final DD/code until Product/Tech Lead approves the business code and endpoint.

| Candidate API | Source gap | Proposed method / endpoint | Caller | Why needed for full project coverage | DD focus if approved | Status | Completion |
|---|---|---|---|---|---|---|---:|
| `AUTH-PASSWORD-RESET-REQUEST-001` | BD 5.1 and use case catalog mention password reset; no API code in 10.4. | POST `/api/v1/auth/password-reset/request` | Guest | Start forgot-password flow with non-enumerating response. | Email/phone privacy, rate limit, token generation hash, notification after commit. | `BLOCKED` / `OPEN_QUESTION` | 0% |
| `AUTH-PASSWORD-RESET-CONFIRM-001` | Password reset completion missing from API catalogue. | POST `/api/v1/auth/password-reset/confirm` | Guest | Confirm reset token and rotate credential safely. | Token expiry/replay, password policy, session invalidation, audit, no plaintext secrets. | `BLOCKED` / `OPEN_QUESTION` | 0% |
| `LEARN-DASHBOARD-001` | BD 5.2 requires student/mentor dashboards; no read API listed. | GET `/api/v1/me/learning-dashboard` | Student | Render current path, progress, blockers and next lesson. | Read-model boundaries, pagination where needed, private data visibility. | `BLOCKED` / `OPEN_QUESTION` | 0% |
| `ASSESS-QUIZ-ATTEMPT-001` | BD 5.3 and command `StartQuizAttempt`; catalogue only has submit. | POST `/api/v1/quizzes/{quizId}/attempts` | Student | Create/start quiz attempt and freeze question snapshot before submit. | Attempt limit, time window, snapshot, idempotency and no answer leakage. | `BLOCKED` / `OPEN_QUESTION` | 0% |
| `ASSESS-PRACTICE-HISTORY-001` | BD 5.3/use case catalog mention practice history. | GET `/api/v1/me/practice-history` | Student | Show own quiz/assignment/lab evidence history. | Evidence visibility, pagination, filter/sort, no hidden grading detail. | `BLOCKED` / `OPEN_QUESTION` | 0% |
| `MENTOR-DASHBOARD-001` | BD 5.5 requires mentor dashboard. | GET `/api/v1/mentor/dashboard` | Mentor | Show assigned learners, submissions, progress and review SLA. | Mentor scope, read projection, aggregation, pagination and privacy. | `BLOCKED` / `OPEN_QUESTION` | 0% |
| `MENTOR-REVIEW-QUEUE-001` | BD 5.5 requires review queue. | GET `/api/v1/mentor/review-queue` | Mentor | List submissions/projects waiting for assigned mentor review. | Scope predicate, status filter, sorting, empty state and stale data handling. | `BLOCKED` / `OPEN_QUESTION` | 0% |
| `PROJECT-BOARD-001` | Command/query `GetProjectBoard`; no read API listed. | GET `/api/v1/projects/{projectId}/board` | Student/Mentor | Render task board/sprint state. | Team/project scope, read model, task status filtering, pagination if large. | `BLOCKED` / `OPEN_QUESTION` | 0% |
| `PROJECT-WORKLOG-001` | BD 5.4/use case catalog mention work logs. | POST `/api/v1/tasks/{taskId}/work-logs` | Student/Mentor | Record effort/evidence against a task. | Task/project scope, date/duration validation, audit and task status relation. | `BLOCKED` / `OPEN_QUESTION` | 0% |
| `PROJECT-COMMENT-001` | BD 5.4 mentions task comments/team chat. | POST `/api/v1/tasks/{taskId}/comments` | Student/Mentor | Add task discussion in project scope. | Content moderation, scope, notification event, safe rich text. | `BLOCKED` / `OPEN_QUESTION` | 0% |
| `PROJECT-FILE-001` | BD requires file sharing and `file_asset`; no file/task attachment API listed. | POST `/api/v1/tasks/{taskId}/attachments` | Student/Mentor | Attach a scanned file asset to a task. | Upload scan status, file ownership, object storage abstraction, no raw storage URL. | `BLOCKED` / `OPEN_QUESTION` | 0% |
| `PROJECT-GIT-LINK-001` | BD 5.4 mentions Git repository link. | POST `/api/v1/projects/{projectId}/git-repository-links` | Student/Mentor | Link a verified Git provider repository to a project. | Provider verification, webhook trust boundary, scope, audit. | `BLOCKED` / `OPEN_QUESTION` | 0% |
| `AI-INSIGHT-001` | BD 5.6 mentions learning insight. | GET or POST `/api/v1/ai/learning-insights` | Student/Mentor | Create/read AI learning insight from authorized context. | Clarify sync/async behavior, source context, non-authoritative output and retention. | `BLOCKED` / `OPEN_QUESTION` | 0% |
| `NOTI-FEED-001` | Use case catalog mentions notification feed; no API listed. | GET `/api/v1/notifications` | Student/Mentor/Admin | Read in-app notification feed. | User ownership, pagination, unread count, safe payload. | `BLOCKED` / `OPEN_QUESTION` | 0% |
| `NOTI-READ-001` | Notification read state missing. | PATCH `/api/v1/notifications/{notificationId}/read` | Student/Mentor/Admin | Mark notification as read. | Ownership, idempotent update, timestamp source and audit if needed. | `BLOCKED` / `OPEN_QUESTION` | 0% |
| `NOTI-TEMPLATE-001` | BD 5.7 includes notification templates. | POST `/api/v1/admin/notification-templates` | Admin | Create/update notification template. | Admin permission, template versioning, channel validation, audit. | `BLOCKED` / `OPEN_QUESTION` | 0% |
| `NOTI-DISPATCH-001` | BD events need async delivery but no internal dispatch API/job contract listed. | POST `/api/v1/internal/notifications/dispatch` | System Worker | Dispatch notification from committed event/outbox. | Service identity, retry/DLQ, channel provider failure, trace propagation. | `BLOCKED` / `OPEN_QUESTION` | 0% |
| `COMMUNITY-EVENT-001` | BD 5.7 includes workshops/community events. | GET `/api/v1/community-events` | Student/Mentor/Admin | List public/eligible Study workshops/events. | Visibility, pagination, event status and capacity display. | `BLOCKED` / `OPEN_QUESTION` | 0% |
| `COMMUNITY-REGISTRATION-001` | BD 5.7 includes event registrations. | POST `/api/v1/community-events/{eventId}/registrations` | Student | Register for a Study community event/workshop. | Capacity race, uniqueness `(event_id,user_id)`, cancellation policy if needed. | `BLOCKED` / `OPEN_QUESTION` | 0% |
| `ADMIN-USER-001` | BD 5.7 mentions activate/suspend user and mentor management. | PATCH `/api/v1/admin/users/{userId}/status` | Admin | Activate/suspend/delete user account according to state machine. | `user.status` transition, admin permission, reason, audit and session invalidation. | `BLOCKED` / `OPEN_QUESTION` | 0% |
| `ADMIN-SKILL-001` | BD 5.7 mentions skill taxonomy management. | POST `/api/v1/admin/skills` | Admin | Create/update skill taxonomy. | Unique `skill.code`, impact on projections, audit and migration of renamed skills. | `BLOCKED` / `OPEN_QUESTION` | 0% |
| `ADMIN-SETTING-001` | BD 5.7 includes platform settings. | PATCH `/api/v1/admin/settings/{settingKey}` | Admin | Update typed platform setting. | Setting schema validation, environment/scope, audit and rollback. | `BLOCKED` / `OPEN_QUESTION` | 0% |
| `ADMIN-FEATURE-FLAG-001` | BD 5.7 includes feature flags. | PATCH `/api/v1/admin/feature-flags/{flagKey}` | Admin | Enable/disable feature flag by environment/scope. | Flag type, rollout scope, audit, cache invalidation. | `BLOCKED` / `OPEN_QUESTION` | 0% |
| `ADMIN-MODERATION-001` | BD 5.7 includes moderation. | PATCH `/api/v1/admin/moderation-cases/{caseId}` | Admin | Resolve comment/community moderation case. | Moderator permission, state transition, audit, visibility update. | `BLOCKED` / `OPEN_QUESTION` | 0% |
| `ADMIN-ANALYTICS-001` | BD 5.7 mentions Study analytics. | GET `/api/v1/admin/analytics/study` | Admin | Read Study analytics snapshot. | Aggregation source, time range filters, no PII leakage, pagination/export policy. | `BLOCKED` / `OPEN_QUESTION` | 0% |
| `FILE-ASSET-001` | BD requires canonical `file_asset`, but no upload API listed. | POST `/api/v1/file-assets` | Student/Mentor/Admin | Create file asset record and upload binding for learning/project artifacts. | Storage abstraction, scan policy, ownership, mime/size/checksum validation. | `BLOCKED` / `OPEN_QUESTION` | 0% |
| `FILE-ASSET-002` | Consumers need safe file access; no download API listed. | GET `/api/v1/file-assets/{fileAssetId}/download-url` | Student/Mentor/Admin | Generate scoped temporary access to a file asset. | Ownership/scope, scan status, expiry, no raw permanent storage URL. | `BLOCKED` / `OPEN_QUESTION` | 0% |

## 7. API DD Creation Workflow

For each API that is not `BLOCKED`:

1. Read `docs/BD/Study2Work_Study_BD_Codex_Ready.md`, especially module function, business rule, state, data and API sections.
2. Read the related activity, sequence and class diagrams in `docs/diagrams/`.
3. Read this API checklist row and confirm `DD status`, completion and open questions.
4. Copy `docs/DD/Study2Work_API_DD_Template/` to `docs/api-dd/<module-code-lowercase>/<api-code-lowercase>/`.
5. Fill `01_Overview`, `03_Request`, `04_Response`, `05_DataMapping`, `06_Error`, `02_History` and `API_DD_CHECKLIST.md`.
6. Update this checklist row with DD path, status, completion, reviewer/evidence and remaining open questions.
7. Do not implement the API until the API DD is `APPROVED` or the user explicitly asks for a prototype.

## 8. API Checklist Update Columns For Future Work

When an API DD is created, update the API row or add a short note with:

| Field | Required value |
|---|---|
| DD path | `docs/api-dd/<module>/<api-code>/` |
| DD status | `NOT_STARTED`, `DRAFT`, `IN_REVIEW`, `APPROVED`, `BLOCKED` or `SUPERSEDED` |
| Completion | Numeric percent using section 2 scale |
| Evidence | Worklog, review note, command output or issue link |
| Open questions | `OPEN_QUESTION` IDs with owner/date |
| Blockers | ADR/API catalog decisions, BD conflict, missing diagram, missing data rule or missing permission |
