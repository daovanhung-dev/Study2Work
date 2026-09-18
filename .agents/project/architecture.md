# Kiến trúc repository

## Ownership map đã xác minh

| Area | Path | Stack/role |
|---|---|---|
| Study web | `apps/study-client/` | Vue 3 + TypeScript + Vite |
| Study API | `apps/study-server/` | FastAPI + Python + sync SQLAlchemy core; current composition import được |
| Work mobile | `apps/work-client/mobile/` | Hai Flutter app độc lập; direct Neon SQL + SQLite cache |
| Work web | `apps/work-client/web/` | React + TypeScript + Vite |
| Work API | `apps/work-server/` | Express 4 + TypeScript + Prisma/PostgreSQL/Neon; JSON API-only |
| AI API | `apps/ai-server/` | FastAPI + Ollama adapter; copied core phần lớn unwired |
| DB Admin web | `apps/db-admin-web/` | Angular standalone + Angular Material + CodeMirror; local admin UI |
| DB Admin API | `apps/db-admin-server/` | FastAPI + SQLAlchemy/psycopg; dedicated Neon database control plane |
| Shared contracts | `contracts/` | Work OpenAPI, Study->Work events, skill taxonomy |
| Local infra | `docker-compose.yml`, `infra/README.md` | PostgreSQL/Redis/MinIO/Mailhog và Study/Work containers |

Study, Work và AI là deployable/boundary khác nhau. Work Web gọi Work API qua HTTP;
Work mobile hiện kết nối trực tiếp Neon và không gọi Work API. Không import
business module chéo app.

## Local application addresses

| Role | Address |
|---|---|
| AI server | `127.0.0.1:3000` |
| DB Admin server | `127.0.0.1:3001` |
| Work server | `127.0.0.1:3002` |
| Study server | `127.0.0.1:3003` |
| DB Admin client | `127.0.0.2:3000` |
| Work client | `127.0.0.2:3001` |
| Study client | `127.0.0.2:3002` |

These are local application endpoints. PostgreSQL, Redis, Ollama and test
fixture addresses are separate dependencies and retain their existing values.

## Boundary chính

```text
Study web  -> Study API (contract chưa có OpenAPI hiện hành)
Work web   -> relative `/api/v1` -> Work Express JSON API
Work mobile -> Neon PostgreSQL qua `postgres` + local SQLite cache
Work mobile -> Gemini HTTP API cho `AIService`

Study producer -> contracts/events/study-work/*.schema.json -> Work consumer
                 (consumer chưa implement)

AI API -> Ollama HTTP API
Work API -> Express -> Prisma -> PostgreSQL/Neon
Study API -> PostgreSQL config + optional Redis config; current app import được,
register test collection còn stale import blocker
DB Admin web (one-command local launcher + same-origin proxy)
  -> internal DB Admin API -> one backend-owned Neon PostgreSQL connection + Identity JWKS
```

## Contract boundary

- API envelope chung được mô tả tại `contracts/api-guidelines/README.md`.
- Work source-aligned surface: `contracts/openapi/work/legacy-web.openapi.json`.
  `contracts/openapi/work/openapi.json` và README contract mô tả target/health
  surface không được route Express hiện tại phục vụ; đây là discrepancy.
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
