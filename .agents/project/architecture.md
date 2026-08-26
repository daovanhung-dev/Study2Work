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
```

## Contract boundary

- API envelope chung được mô tả tại `contracts/api-guidelines/README.md`.
- Work runtime surface hiện hành: `contracts/openapi/work/openapi.json`.
- Study OpenAPI chưa tồn tại.
- Study event JSON Schema xác nhận payload/headers, không xác nhận implementation
  consumer hay database table.

## Context loading

Chỉ đọc page kiến trúc này cho task qua nhiều app hoặc khi cần ownership. Task
trong một server đi thẳng từ root router tới scope AGENTS rồi module/API page.
