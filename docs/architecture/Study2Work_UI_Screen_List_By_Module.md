# Study2Work Study-Only UI Screen Map

This document replaces the older broad UI list. The Client architecture is documented in `CLIENT_ARCHITECTURE.md`.

## Web Public

| ID | Screen | Purpose |
|---|---|---|
| `PUB-01` | Landing | Present Study2Work Study value proposition and entry points. |
| `PUB-02` | Public learning catalog | Show published Study learning paths and public content teasers. |
| `PUB-03` | Community events | Show public workshops and community events. |
| `PUB-04` | Help/FAQ | Explain account, learning, mentor and support flows. |
| `PUB-05` | Sign-in entry | Route guests to register, verify email, login or OAuth. |

## Web Student / Mobile Student

| ID | Screen | Purpose |
|---|---|---|
| `STD-01` | Dashboard | Current path, next lesson, progress, review alerts and notifications. |
| `STD-02` | Profile and skills | Current actor profile and declared baseline skills. |
| `STD-03` | Placement | Placement attempt and assigned learning path result. |
| `STD-04` | Learning paths | List eligible or enrolled learning paths. |
| `STD-05` | Lesson reader | Lesson content, progress, bookmark and comment surfaces. |
| `STD-06` | Quiz attempt | Start/submit quiz and display safe result feedback. |
| `STD-07` | Assignment submission | Submit assignment/code artifact and view grading state. |
| `STD-08` | Skill matrix | Evidence-backed skill projection. |
| `STD-09` | Project board | Team project, sprint, task and evidence tracking. |
| `STD-10` | AI learning help | Roadmap suggestion and code explanation requests. |
| `STD-11` | Community | Events, workshops and eligible registrations. |
| `STD-12` | Notifications | In-app notification feed and read state. |

## Web Mentor

| ID | Screen | Purpose |
|---|---|---|
| `MEN-01` | Dashboard | Assigned learners, teams, review queue and SLA signals. |
| `MEN-02` | Review queue | Submissions/projects waiting for review. |
| `MEN-03` | Rubric review | Apply rubric version and create feedback. |
| `MEN-04` | Learner progress | Read assigned learner progress and skill evidence. |
| `MEN-05` | Project/team scope | View assigned team project status and task evidence. |
| `MEN-06` | Workshops | Manage eligible live sessions/workshops. |
| `MEN-07` | Notifications | Mentor notification feed. |

## Web Admin

| ID | Screen | Purpose |
|---|---|---|
| `ADM-01` | Dashboard | Study analytics snapshot and operational alerts. |
| `ADM-02` | User management | Activate/suspend users and inspect audit evidence. |
| `ADM-03` | Mentor scope | Assign mentor learner/team/project review scope. |
| `ADM-04` | Learning content | Create, edit and publish content tree. |
| `ADM-05` | Rubrics | Create, version and publish rubrics. |
| `ADM-06` | Notification templates | Manage channel templates and dispatch policy. |
| `ADM-07` | Settings and flags | Typed platform settings and feature flags. |
| `ADM-08` | Moderation | Resolve comments/community moderation cases. |
| `ADM-09` | Audit | Search admin/system audit records. |

## Shared System Screens

| ID | Screen | Purpose |
|---|---|---|
| `SYS-01` | Error states | 401, 403, 404, 500 and empty-state surfaces. |
| `SYS-02` | Account settings | Profile, password/session and notification preferences. |
| `SYS-03` | File attachment state | Safe upload status and scan/result visibility. |

## Implementation Rule

Screens are not implementation approval. A screen may consume an API only after the corresponding API DD is approved or the user explicitly requests a prototype.
