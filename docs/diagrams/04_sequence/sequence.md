# Study2Work Sequence Diagram Catalog - Study Scope

Source of truth: `docs/BD/Study2Work_Study_BD_Codex_Ready.md`.

| # | File | Flow | API code |
|---:|---|---|---|
| 01 | `01_Register_Verify_Email.puml` | Register and verify email | AUTH-REGISTER-001 / AUTH-VERIFY-001 |
| 02 | `02_Login_Refresh_Logout.puml` | Login, refresh and logout | AUTH-LOGIN-001 / AUTH-REFRESH-001 / AUTH-LOGOUT-001 |
| 03 | `03_Profile_Skills.puml` | Profile and baseline skills | USER-PROFILE-001 / USER-PROFILE-002 / USER-SKILL-001 |
| 04 | `04_Placement_Assign_Path.puml` | Placement and path assignment | LEARN-PLACEMENT-001 |
| 05 | `05_Enroll_Learning_Path.puml` | Enroll learning path | LEARN-PATH-002 |
| 06 | `06_Lesson_Progress.puml` | Lesson access and progress | LEARN-LESSON-001 / LEARN-PROGRESS-001 |
| 07 | `07_Bookmark_Comment_Live.puml` | Bookmark, comment and live session | LEARN-BOOKMARK-001 / LEARN-COMMENT-001 / LEARN-LIVE-001 |
| 08 | `08_Quiz_Submit.puml` | Quiz submit | LEARN-QUIZ-001 |
| 09 | `09_Assignment_Submission.puml` | Assignment submission | ASSESS-SUBMISSION-001 |
| 10 | `10_Auto_Grade_Result.puml` | Auto grade result | ASSESS-GRADE-001 |
| 11 | `11_Mentor_Review.puml` | Mentor review | MENTOR-REVIEW-001 / MENTOR-REVIEW-002 |
| 12 | `12_Skill_Matrix.puml` | Skill matrix | SKILL-MATRIX-001 |
| 13 | `13_Project_Team.puml` | Project team | PROJECT-TEAM-001 / PROJECT-TEAM-002 |
| 14 | `14_Sprint_Task.puml` | Sprint and task | PROJECT-SPRINT-001 / PROJECT-TASK-001 / PROJECT-TASK-002 |
| 15 | `15_Task_PR_Review.puml` | Task PR review | PROJECT-PR-001 |
| 16 | `16_Project_Submission.puml` | Project submission | PROJECT-SUBMIT-001 |
| 17 | `17_AI_Roadmap.puml` | AI roadmap suggestion | AI-ROADMAP-001 |
| 18 | `18_AI_Code_Explanation.puml` | AI code explanation | AI-CODE-001 |
| 19 | `19_Admin_Content_Rubric.puml` | Admin content and rubric | ADMIN-CONTENT-001 / ADMIN-RUBRIC-001 |
| 20 | `20_Admin_Mentor_Scope.puml` | Admin mentor scope | ADMIN-MENTOR-001 |

## Standard sequence contract

Every sequence includes:

- API endpoint and API business code.
- Request DTO and response DTO.
- Standard envelope with `businessCode`, `message`, `timestamp`, `traceId`, and `data` or `errors`.
- Validation, authentication, RBAC, ownership/scope and state transition check.
- Transaction boundary with PostgreSQL read/write notes.
- Audit log and after-commit outbox/worker side effects when needed.
- Safe error codes: E401, E403, E404, E409, E422, E500, E502, E504.
