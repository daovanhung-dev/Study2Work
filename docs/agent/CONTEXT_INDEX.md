# Context Index

Index này giúp chọn đúng tài liệu cần đọc theo module/task. Không đọc toàn bộ `docs/` nếu task chỉ chạm một module.

## Global Read Order

1. `AGENTS.md`
2. `docs/agent/CONTEXT_INDEX.md`
3. `docs/worklog/INDEX.md`
4. Checklist module trong `docs/checklists/<MODULE_CODE>.md`
5. BD/DD/skill/worklog liên quan theo bảng bên dưới

## Global Sources

| Source | Use |
|---|---|
| `docs/BD/Study2Work_Study_BD_Codex_Ready.md` | Nguồn nghiệp vụ Study canonical. |
| `docs/DD/DD_Module_Creation_Guide_EN.md` | Quy trình tạo DD module. |
| `docs/DD/DD_Module_Template/` | Cấu trúc chuẩn DD. |
| `docs/architecture/Study2Work_Domain_Model_Coding_Practice.md` | Domain model, aggregate, events, ownership. |
| `docs/architecture/Study2Work_BusinessCode_Debug.md` | BusinessCode, error, logging, trace. |
| `docs/diagrams/` | Use case, activity, ERD, sequence khi cần trace flow. |
| `docs/guilines/Study2Work_folder_functions.md` | Tham khảo skeleton; BD Study override khi mâu thuẫn. |

## Conflicts And Scope Guards

| ID | Status | Description |
|---|---|---|
| `CONFLICT-TECH-001` | OPEN | BD Study chọn FastAPI/Python canonical; repo hiện là skeleton NestJS-like rỗng. Cần ADR-001 trước khi coding backend chính thức. |
| `CONFLICT-SCOPE-001` | OPEN | Skeleton/docs cũ có Career/Employer/Recruitment/CV/Job; BD Study loại trừ các phần này khỏi Study implementation. |
| `OPEN-QUESTION-CMD-001` | OPEN | Manifests/scripts/config hiện rỗng nên chưa có command build/test/lint/format xác thực. |

## Module Map

| Module | BD refs | Current DD | Features | Read for task | Checklist | Skills | Worklog |
|---|---|---|---|---|---|---|---|
| `AUTH` | BD 3.1, 3.2, 5.1, BR-AUTH, API AUTH | `docs/DD/AUTH/` nếu tồn tại; hiện `NOT_STARTED` | Register, verify email, OAuth, login, refresh, logout, profile/RBAC | BD auth sections, BusinessCode, sequence auth diagrams | `docs/checklists/AUTH.md` | `docs/skills/INDEX.md` | `docs/worklog/INDEX.md` |
| `LEARNING` | BD 4.2, 5.2, BR-LEARN, API LEARN | `docs/DD/LEARNING/` nếu tồn tại; hiện `NOT_STARTED` | Placement, learning path, lesson, progress, bookmark, comment, live session | BD learning, ERD learning, sequence lesson/progress | `docs/checklists/LEARNING.md` | `docs/skills/INDEX.md` | `docs/worklog/INDEX.md` |
| `ASSESSMENT` | BD 5.3, 5.5, BR-ASSESS, BR-MENTOR, API ASSESS/MENTOR/SKILL | `docs/DD/ASSESSMENT/` nếu tồn tại; hiện `NOT_STARTED` | Quiz, assignment, lab, auto grading, rubric, mentor review, skill matrix | BD assessment, ERD assessment, sequence quiz/submission/review | `docs/checklists/ASSESSMENT.md` | `docs/skills/INDEX.md` | `docs/worklog/INDEX.md` |
| `PROJECT` | BD 5.4, BR-PROJECT, API PROJECT | `docs/DD/PROJECT/` nếu tồn tại; hiện `NOT_STARTED` | Team, sprint, task board, Git/PR review, project submission, teamwork artifacts | BD project, domain project, sequence project/task if available | `docs/checklists/PROJECT.md` | `docs/skills/INDEX.md` | `docs/worklog/INDEX.md` |
| `AI` | BD 5.6, BR-AI, API AI | `docs/DD/AI/` nếu tồn tại; hiện `NOT_STARTED` | AI roadmap, code explanation, debugging hints, learning insight | BD AI, trace/security rules, BusinessCode | `docs/checklists/AI.md` | `docs/skills/INDEX.md` | `docs/worklog/INDEX.md` |
| `ADMIN` | BD 5.7, BR-ADMIN, BR-PLATFORM, API ADMIN | `docs/DD/ADMIN/` nếu tồn tại; hiện `NOT_STARTED` | User/mentor/content management, settings, analytics, moderation, audit | BD admin/platform, BusinessCode, UI/admin refs with Study-only filter | `docs/checklists/ADMIN.md` | `docs/skills/INDEX.md` | `docs/worklog/INDEX.md` |
| `COMMUNITY` | BD 3.3, 5.7 | `docs/DD/COMMUNITY/` nếu tồn tại; hiện `NOT_STARTED` | Lesson comments, workshops/live sessions, registrations, engagement | BD community, UI community refs with Study-only filter | `docs/checklists/COMMUNITY.md` | `docs/skills/INDEX.md` | `docs/worklog/INDEX.md` |
| `NOTIFICATION` | BD 8.4, 9.2, 14.2 | `docs/DD/NOTIFICATION/` nếu tồn tại; hiện `NOT_STARTED` | Notification templates, in-app/email/push, async delivery | BD notification/platform sections, BusinessCode NOTI/SYSTEM | `docs/checklists/NOTIFICATION.md` | `docs/skills/INDEX.md` | `docs/worklog/INDEX.md` |

## Task Type Map

| Task type | Minimum docs to read |
|---|---|
| Create/upgrade DD | BD module section, `docs/DD/DD_Module_Creation_Guide_EN.md`, `docs/DD/DD_Module_Template/`, checklist module. |
| Implement backend/API | BD + approved DD + checklist + BusinessCode/trace docs + code entrypoints. Resolve `CONFLICT-TECH-001` first for backend stack. |
| Implement UI/mobile | BD + approved DD Views/Function_List + UI screen refs filtered by Study-only scope. |
| Fix bug | Checklist module + latest related worklogs + DD/BD for affected rule + failing test/evidence. |
| Add tests | BD acceptance conditions + DD function/view/test checklist + current code test structure. |
| Update status | `docs/agent/STATUS_MODEL.md`, checklist module, worklog index. |

## Current State Snapshot

- No module DD exists yet outside `docs/DD/DD_Module_Template/`.
- No worklog sessions exist yet.
- No reusable skills exist yet because there is no repeated worklog evidence.
- Initial checklist files are bootstrapped for Study modules only.
