# Kiến trúc repository

## Ownership map đã xác minh

| Area | Path | Stack/role |
|---|---|---|
| Study web | `apps/study-client/` | Vue 3 + TypeScript + Vite |
| Study API | `apps/study-server/` | FastAPI + Python + sync SQLAlchemy core; hiện import-broken |
| Work mobile | `apps/work-client/mobile/` | Hai Flutter app; context chỉ là skeleton |
| Work web | `apps/work-client/web/` | React + TypeScript + Vite |
| Work API | `apps/work-server/` | NestJS + Fastify + TypeScript + Prisma |
| AI API | `apps/ai-server/` | FastAPI + Ollama adapter; copied core phần lớn unwired |
| DB Admin web | `apps/db-admin-web/` | Angular standalone + Angular Material + CodeMirror; local admin UI |
| DB Admin API | `apps/db-admin-server/` | FastAPI + SQLAlchemy/psycopg; dedicated Neon database control plane |
| Shared contracts | `contracts/` | Work OpenAPI, Study->Work events, skill taxonomy |
| Local infra | `docker-compose.yml`, `infra/README.md` | PostgreSQL/Redis/MinIO/Mailhog và Study/Work containers |

Study, Work và AI là deployable/boundary khác nhau. Không import business module
chéo app; giao tiếp qua HTTP/event contract được xác nhận.

## Boundary chính

```text
Study web  -> Study API (contract chưa có OpenAPI hiện hành)
Work web   -> Work API qua VITE_WORK_API_URL

Study producer -> contracts/events/study-work/*.schema.json -> Work consumer
                 (consumer chưa implement)

AI API -> Ollama HTTP API
Work API -> PostgreSQL/Prisma + Identity JWKS
Study API -> PostgreSQL config + optional Redis config; app chưa start được
DB Admin web (one-command local launcher + same-origin proxy)
  -> internal DB Admin API -> one backend-owned Neon PostgreSQL connection + Identity JWKS
```

## Contract boundary

- API envelope chung được mô tả tại `contracts/api-guidelines/README.md`.
- Work runtime surface hiện hành: `contracts/openapi/work/openapi.json`.
- Study OpenAPI chưa tồn tại.
- Study event JSON Schema xác nhận payload/headers, không xác nhận implementation
  consumer hay database table.
- DB Admin API is a new local-only deployable; its envelope and routes are defined
  in `apps/db-admin-server/app/core/contracts.py` and `app/api/routes.py`.

DB Admin is intentionally not mounted into Study, Work or AI. Its local Angular
launcher starts the separate FastAPI runtime and proxies `/api` to loopback;
the frontend only knows a relative API base URL, while the backend-only
`URL_DATABASE` constant remains outside Angular.

## Context loading

Chỉ đọc page kiến trúc này cho task qua nhiều app hoặc khi cần ownership. Task
trong một server đi thẳng từ root router tới scope AGENTS rồi module/API page.
