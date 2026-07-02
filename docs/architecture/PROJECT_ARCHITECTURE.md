# Study2Work Project Architecture

| Field | Value |
|---|---|
| Status | Canonical |
| Updated | 2026-07-02 |
| Scope | Study-only |
| Runtime split | Server and Client |

## 1. Architecture Decision

Study2Work is organized as a monorepo with two runtime sides:

- **Server**: the API backend and async workers under `services/api`.
- **Client**: web and mobile applications under `apps`.

All implementation must stay inside the approved Study scope: identity/profile, learning, practice and assessment, mentor workflow, project teamwork, AI learning support, community, notification, admin and platform governance. Removed career/recruiting workflows are not part of this architecture unless a future approved BD and ADR explicitly expand scope.

## 2. Top-Level Ownership

| Path | Owner | Responsibility |
|---|---|---|
| `services/api` | Server | FastAPI API, domain modules, persistence, migrations, worker bootstrap and backend tests. |
| `apps/web-public` | Client | Public Study website, marketing/content entry points and community-facing pages. |
| `apps/web-student` | Client | Student learning, assessment, project, community, notification and profile surfaces. |
| `apps/web-mentor` | Client | Mentor review, assigned learner/team, workshop and rubric-driven workflow surfaces. |
| `apps/web-admin` | Client | Study admin, content, rubric, mentor scope, analytics, settings, audit and moderation surfaces. |
| `apps/mobile-app` | Client | Flutter mobile Study experience for student-first workflows. |
| `packages` | Client/shared | Future shared web/mobile contracts, UI, utilities and tool configuration. |
| `docs/architecture` | Documentation | Canonical architecture, server/client boundaries and runtime flow documentation. |
| `.agent` and `.codex` | Agent context | Compact rules and project context for coding agents. |
| `docs/checklists` | Delivery control | Module readiness, API DD status, implementation evidence and open questions. |

## 3. Server Modules

The server is a FastAPI modular monolith. Each business module keeps four internal layers: `presentation`, `application`, `domain` and `infrastructure`.

| Study module | Server path | Primary responsibility |
|---|---|---|
| Identity | `services/api/app/modules/identity` | Authentication, sessions, OAuth, verification and RBAC foundations. |
| Profile | `services/api/app/modules/profile` | Current actor profile, learner/mentor profile extension and baseline skills. |
| Learning | `services/api/app/modules/learning` | Learning paths, lessons, progress, bookmarks, comments and live session reads. |
| Assessment | `services/api/app/modules/assessment` | Quiz, assignment submission, grading evidence, rubric and skill matrix. |
| Project | `services/api/app/modules/project` | Team, sprint, task board, work evidence and project submission workflow. |
| Mentor | `services/api/app/modules/mentor` | Mentor review queue, rubric review, feedback and mentor assignment scope. |
| AI | `services/api/app/modules/ai` | Roadmap suggestion, code explanation and learning insight orchestration. |
| Notification | `services/api/app/modules/notification` | Notification feed, templates and async channel dispatch. |
| Community | `services/api/app/modules/community` | Workshops, community events and participation workflows. |
| Platform | `services/api/app/modules/platform` | Health, system metadata, admin/platform support and cross-cutting API utilities. |

## 4. Client Applications

Web clients use the Vue/Vite family when implemented. Mobile uses Flutter. This pass documents target structure only; it does not create runnable clients.

| Client | Audience | Study scope |
|---|---|---|
| `web-public` | Guest/public | Landing, public content, events, help and sign-in entry points. |
| `web-student` | Student | Dashboard, learning, assessment, projects, AI learning help, community, notifications and profile. |
| `web-mentor` | Mentor | Assigned learners/teams, review queue, rubric feedback, workshops and notifications. |
| `web-admin` | Admin | User/mentor scope, content tree, rubric, settings, analytics, audit and moderation. |
| `mobile-app` | Student-first mobile users | Mobile learning, progress, assessment, project updates, community, notification and profile. |

## 5. Dependency Direction

Runtime dependencies are one-way:

```text
Client apps -> Server API -> application/domain -> infrastructure adapters
```

Server internals follow inward dependencies:

```text
presentation -> application -> domain
infrastructure -> application/domain ports
domain -> no framework dependency
```

Clients do not call databases, Redis, Celery workers or provider SDKs directly. Server domain/application code does not depend on FastAPI request/response objects, SQLAlchemy sessions or Celery task objects.

## 6. Interface Contract

- API prefix is `/api/v1`.
- Every response includes a standard envelope with `businessCode`, `message`, `timestamp`, `traceId` and either `data` or `errors`.
- Clients send or receive `X-Trace-Id` for support/debug correlation.
- Study business APIs require an approved API DD before implementation.
- Future generated/shared client contracts should be derived from approved API DD and OpenAPI output, not hand-invented in clients.

## 7. Canonical References

This architecture is aligned with:

- FastAPI larger applications and `APIRouter`: https://fastapi.tiangolo.com/tutorial/bigger-applications/
- SQLAlchemy ORM 2.0: https://docs.sqlalchemy.org/en/20/orm/quickstart.html
- Alembic migrations: https://alembic.sqlalchemy.org/en/latest/tutorial.html
- Celery workers: https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html
- Vite web apps: https://vite.dev/guide/
- pnpm workspaces: https://pnpm.io/workspaces
- Vue style guide: https://vuejs.org/style-guide/
- Vue Router: https://router.vuejs.org/guide/
- Pinia: https://pinia.vuejs.org/introduction.html
- Flutter app architecture: https://docs.flutter.dev/app-architecture
- uv projects: https://docs.astral.sh/uv/concepts/projects/
