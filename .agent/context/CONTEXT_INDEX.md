# Context Index

This index tells agents which project documents to read for each task. Use progressive disclosure: read only the context needed for the current module and task.

## Global Read Order

1. `AGENTS.md`
2. `.agent/AGENT_GUIDE.md`
3. `.agent/context/CONTEXT_INDEX.md`
4. `.agent/worklog/INDEX.md`
5. The relevant module checklist in `docs/checklists/<MODULE_CODE>.md`
6. BD, API DD, diagrams, architecture notes, and previous worklogs relevant to the task

## Global Sources

| Source | Use |
|---|---|
| `docs/BD/Study2Work_Study_BD_Codex_Ready.md` | Canonical Study-scope business source of truth. |
| `docs/architecture/PROJECT_ARCHITECTURE.md` | Canonical server/client split, top-level ownership, module map and dependency boundaries. |
| `docs/architecture/SERVER_ARCHITECTURE.md` | Canonical server architecture, API flow, persistence, migrations and worker rules. |
| `docs/architecture/CLIENT_ARCHITECTURE.md` | Canonical web/mobile client architecture, app responsibilities and API consumption rules. |
| `docs/architecture/RUNTIME_FLOWS.md` | Canonical synchronous, mutation, async, migration and error/trace flows. |
| `docs/checklists/API.md` | Study API checklist, API DD status, API readiness, blockers, and open questions. |
| `docs/DD/Study2Work_API_DD_Template/` | Template for one API Detail Design package per API operation. |
| `.agent/context/STATUS_MODEL.md` | Shared status values for DD, coding, bugs, tests, worklogs, and retrospectives. |
| `docs/architecture/Study2Work_Domain_Model_Coding_Practice.md` | Study-only domain architecture summary; BD overrides it if conflict exists. |
| `docs/architecture/Study2Work_BusinessCode_Debug.md` | Study-only business code and trace summary; API checklist overrides it if conflict exists. |
| `docs/diagrams/` | Study-only use case, activity, class, and sequence diagrams. |
| `.codex/BACKEND_ARCHITECTURE.md` | Canonical backend architecture for future coding agents. |
| `.codex/PROJECT_CONTEXT.md` | Compact project context for future coding agents. |

## Scope Guards

| ID | Status | Description |
|---|---|---|
| `DECISION-ARCH-001` | ACCEPTED | Runtime split is Server (`services/api`) and Client (`apps/*`). |
| `DECISION-TECH-001` | ACCEPTED | Canonical Study backend is Python 3.12+ with FastAPI, Pydantic v2, SQLAlchemy 2.0, Alembic, PostgreSQL, Redis, and Celery. |
| `DECISION-SCOPE-001` | ACCEPTED | Study implementation excludes removed non-Study workflows unless a future approved BD, ADR and API DD expand scope. |
| `OPEN-QUESTION-DD-001` | OPEN | No per-API DD is approved yet. Business API implementation must wait for an approved API DD unless the user explicitly asks for a prototype. |

## Module Map

| Module | BD refs | Current DD | Features | Read for task | Checklist | Worklog |
|---|---|---|---|---|---|---|
| `AUTH` | BD 3.1, 3.2, 5.1, BR-AUTH, API AUTH | API DD required before implementation | Register, verify email, OAuth, login, refresh, logout, profile/RBAC | BD auth sections, API checklist, sequence auth diagrams, BusinessCode rules | `docs/checklists/AUTH.md` | `.agent/worklog/INDEX.md` |
| `LEARNING` | BD 4.2, 5.2, BR-LEARN, API LEARN | API DD required before implementation | Placement, learning path, lesson, progress, bookmark, comment, live session | BD learning sections, API checklist, diagrams | `docs/checklists/LEARNING.md` | `.agent/worklog/INDEX.md` |
| `ASSESSMENT` | BD 5.3, 5.5, BR-ASSESS, BR-MENTOR, API ASSESS/MENTOR/SKILL | API DD required before implementation | Quiz, assignment, lab, auto grading, rubric, mentor review, skill matrix | BD assessment sections, diagrams, grading safety boundary | `docs/checklists/ASSESSMENT.md` | `.agent/worklog/INDEX.md` |
| `PROJECT` | BD 5.4, BR-PROJECT, API PROJECT | API DD required before implementation | Team, sprint, task board, Git/PR review, project submission, teamwork artifacts | BD project sections, diagrams, task state machine | `docs/checklists/PROJECT.md` | `.agent/worklog/INDEX.md` |
| `AI` | BD 5.6, BR-AI, API AI | API DD required before implementation | AI roadmap, code explanation, debugging hints, learning insight | BD AI sections, trace/security rules, async worker guidance | `docs/checklists/AI.md` | `.agent/worklog/INDEX.md` |
| `ADMIN` | BD 5.7, BR-ADMIN, BR-PLATFORM, API ADMIN | API DD required before implementation | User/mentor/content management, settings, analytics, moderation, audit | BD admin/platform sections, BusinessCode rules, Study-only scope filter | `docs/checklists/ADMIN.md` | `.agent/worklog/INDEX.md` |
| `COMMUNITY` | BD 3.3, 5.7 | API DD required before implementation | Lesson comments, workshops/live sessions, registrations, engagement | BD community sections, API checklist, diagrams | `docs/checklists/COMMUNITY.md` | `.agent/worklog/INDEX.md` |
| `NOTIFICATION` | BD 8.4, 9.2, 14.2 | API DD required before implementation | Notification templates, in-app/email/push, async delivery | BD notification/platform sections, BusinessCode NOTI/SYSTEM | `docs/checklists/NOTIFICATION.md` | `.agent/worklog/INDEX.md` |

## Task Type Map

| Task type | Minimum docs to read |
|---|---|
| Create or update API DD | BD module/API section, related diagrams, `docs/checklists/API.md`, `docs/DD/Study2Work_API_DD_Template/`. |
| Implement server API | BD + approved API DD + `docs/checklists/API.md` + `docs/architecture/SERVER_ARCHITECTURE.md` + affected code. |
| Implement UI/mobile | BD + approved API DD request/response/error contract + `docs/architecture/CLIENT_ARCHITECTURE.md` + Study-only UI refs. |
| Fix bug | Checklist module + latest related worklogs + API DD/BD for the affected rule + failing evidence. |
| Add tests | BD acceptance conditions + API DD test checklist + current test structure. |
| Update status | `.agent/context/STATUS_MODEL.md`, relevant checklist, `.agent/worklog/INDEX.md`. |

## Current State Snapshot

- Canonical backend foundation is `services/api`.
- Canonical client side is `apps/*`.
- Superseded legacy server skeletons are not canonical for Study backend implementation.
- API DD template exists at `docs/DD/Study2Work_API_DD_Template/`.
- No per-API DD is approved yet.
- Worklog sessions are stored under `.agent/worklog/`.
- Reusable skills are stored under `.agent/skills/`.
