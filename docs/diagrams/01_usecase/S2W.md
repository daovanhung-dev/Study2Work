# Study2Work Use Case Catalog - Study Scope

Nguồn chuẩn: `docs/BD/Study2Work_Study_BD_Codex_Ready.md`.

## Actors

| Actor | Scope |
|---|---|
| Guest | Register, verify email, login, password reset. |
| Student | Learn, practice, submit work, join team, request AI help, read own evidence. |
| Mentor | Review assigned learners, give feedback, inspect scoped progress and project work. |
| Admin | Manage users, mentor scope, learning content, rubric, settings, moderation and audit. |
| System Worker | Executes async grading, notification, analytics and projection tasks. |
| AI Service | Produces non-authoritative roadmap, code explanation and learning insight. |
| Notification Service | Delivers in-app, email and push messages from committed events. |
| Git Provider | Supplies verified repository and pull request evidence. |
| Object Storage | Stores uploaded learning and project artifacts through `file_asset`. |
| Grader Runner | Executes untrusted code outside the main API process. |

## Use Case Groups

| Group | Use cases | BD trace |
|---|---|---|
| Identity & Profile | Register, verify email, OAuth/login, refresh, logout, reset password, my profile, update profile, baseline skills, RBAC and mentor scope | BD 5.1, BR-AUTH, BR-PLATFORM, API AUTH/USER |
| Learning Journey | Placement, path suggestion, enroll path, dashboard, lesson access, progress, bookmark, comment, live sessions | BD 5.2, BR-LEARN, API LEARN |
| Practice & Assessment | Quiz attempt, assignment/code submission, auto grading, mentor review, revision, practice history, skill matrix | BD 5.3, 5.5, BR-ASSESS, BR-MENTOR, API ASSESS/MENTOR/SKILL |
| Project & Teamwork | Team create/join, sprint, task, task transition, work log, PR review, project artifact, team collaboration | BD 5.4, BR-PROJECT, API PROJECT |
| AI Learning Support | Roadmap suggestion, code explanation, debugging hints, learning insight | BD 5.6, BR-AI, API AI |
| Community, Notification & Platform | Workshop registration, notification feed, async notification, admin user/content/rubric/skill/settings, audit, analytics | BD 5.7, BR-ADMIN, API ADMIN/NOTI/SYSTEM |

## Include / Extend Rules

| Source use case | Relationship | Target use case | Reason |
|---|---|---|---|
| Register | include | Verify email | Pending account becomes active only after verification. |
| Login | extend | Refresh token | Authenticated sessions can rotate tokens. |
| Placement | include | Path suggestion | Placement result can seed the learning path. |
| Lesson access | include | Progress recording | Real learning interactions update server-side progress. |
| Assignment submission | include | Auto grading | Submission creates immutable evidence and queues grading. |
| Auto grading | include | Skill matrix | Valid grading output contributes skill evidence. |
| Mentor review | include | Skill matrix | Final review produces evidence-backed projection updates. |
| Task transition | extend | Work log | Task movement may record effort and audit details. |
| PR review | extend | Task transition | Verified PR evidence can move task state. |
| AI roadmap / code explanation | include | Learning insight | AI output is saved as non-authoritative insight. |
| Admin changes | include | Audit | Sensitive platform actions are append-only audited. |

## Scope Rules

- The diagrams cover Study BD v1.0 only.
- Learning evidence is private Study evidence unless a future approved BD expands it.
- AI output never overwrites progress, score, review or skill truth.
- Auto grading and AI run asynchronously when latency or safety requires it.
- All protected flows return the standard envelope with `businessCode`, `timestamp`, `traceId` and safe `data` or `errors`.
