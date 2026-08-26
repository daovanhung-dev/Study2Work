# Dependency map

## Server map

```text
apps/study-server/app/main.py
  -> app/api/v1.py
       -> app.module.* (NOT_FOUND; blocks import)
  -> app/core/* (response/trace symbol mismatches)
  -> PostgreSQL settings; Redis is config-only
  -> app/service/ai/OllamaService (no live caller)

apps/ai-server/app/main.py
  -> app/api/v1.py
  -> app/module/chat/{chat,model,view}.py
  -> app/service/ai/ollama_service.py
  -> Ollama /api/generate
  x copied app/core/* is UNWIRED

apps/work-server/src/bootstrap.ts
  -> AppModule
     -> config + database + http + auth + health + system
  -> Prisma -> Work PostgreSQL
  -> remote Identity JWKS (protected routes only; current routes public)
  -> Redis URL only (no client)
```

## Client/server boundaries

- Work web reads `VITE_WORK_API_URL`; Work API does not serve client assets.
- Study client and Study API are separate packages, nhưng current Study OpenAPI
  không đủ để suy diễn client/server contract.
- Mobile apps không được deep-load ở context hiện tại.

## Contract dependencies

| Producer/owner | Contract | Consumer | Implementation status |
|---|---|---|---|
| Work API | `contracts/openapi/work/openapi.json` | Work web/clients | Foundation endpoints implemented |
| Study | `study.evidence.upserted.v1.schema.json` | Work | Consumer missing |
| Study | `study.evidence.revoked.v1.schema.json` | Work | Consumer missing |
| Shared | `skill-taxonomy.v1*.json` | Future domain modules | No current server caller |

Event contract yêu cầu signature-first validation, JSON Schema, idempotency và
local snapshot. Không có nghĩa các helper/table tương ứng đã tồn tại.

## Test dependencies

- Study `tests/conftest.py` phụ thuộc `app.main`, hiện chặn collection.
- AI không có tests.
- Work Vitest injects Nest app và mocks readiness Prisma probe.
- Root `tests/smoke_test.py` là stale standalone artifact, không phải test router
  cho package hiện hành.
