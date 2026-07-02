# Study2Work Canonical Project Tree

This document supersedes the older tree proposal. The canonical architecture is now documented in `PROJECT_ARCHITECTURE.md`.

## Runtime Split

```text
Study2Work/
|-- services/
|   `-- api/                  # Server: FastAPI API backend and worker foundation
|-- apps/
|   |-- web-public/           # Client: public web app skeleton
|   |-- web-student/          # Client: student web app skeleton
|   |-- web-mentor/           # Client: mentor web app skeleton
|   |-- web-admin/            # Client: admin web app skeleton
|   `-- mobile-app/           # Client: Flutter mobile app skeleton
|-- packages/                 # Future shared client contracts, UI, utils and config
|-- docs/
|   |-- architecture/         # Canonical architecture docs
|   |-- BD/                   # Business source of truth
|   |-- DD/                   # API DD templates
|   |-- checklists/           # Module and API readiness
|   |-- diagrams/             # Study-only diagrams
|   `-- adr/                  # Architecture decisions
|-- .agent/                   # Agent workflow/context
|-- .codex/                   # Compact coding-agent context
|-- docker-compose.yml
`-- README.md
```

## Server Tree

```text
services/api/
|-- app/
|   |-- core/
|   |-- modules/
|   |   |-- identity/
|   |   |-- profile/
|   |   |-- learning/
|   |   |-- assessment/
|   |   |-- project/
|   |   |-- mentor/
|   |   |-- ai/
|   |   |-- notification/
|   |   |-- community/
|   |   `-- platform/
|   |-- shared/
|   |-- workers/
|   `-- main.py
|-- alembic/
|-- tests/
|-- Dockerfile
|-- pyproject.toml
`-- uv.lock
```

Each server module uses:

```text
module/
|-- presentation/
|-- application/
|-- domain/
`-- infrastructure/
```

## Client Tree

```text
apps/
|-- web-public/
|-- web-student/
|-- web-mentor/
|-- web-admin/
`-- mobile-app/
```

Web apps target Vue 3, TypeScript and Vite when implemented. The mobile app targets Flutter. Current client folders are skeletons only.

## Scope

Only Study workflows belong in this tree: identity/profile, learning, practice and assessment, mentor workflow, project teamwork, AI learning support, community, notification, admin and platform governance.
