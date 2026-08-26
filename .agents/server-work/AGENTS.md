# Work Server agent entry

Source root: `apps/work-server/`

```text
CONTEXT_MODE: DEEP
RUNTIME_STATUS: VERIFIED_FOUNDATION
STACK: NestJS 11 + Fastify 5 + TypeScript + Prisma/PostgreSQL
```

## Load theo task

| Task | Context |
|---|---|
| bootstrap/trace/envelope/filter | `core/runtime-http.md` |
| auth/JWKS/config/Prisma | `core/auth-config-db.md` |
| root/health module | `modules/foundation.md` |
| API contract | `apis/foundation.md` + Work OpenAPI |
| schema/migration | `database.md` |
| tests | `tests.md` |

## Critical rules

- Internal imports use NodeNext ESM `.js` suffix.
- Respect Nest DI/controller/service/module ownership; do not apply Python four-file/raw-SQL conventions.
- Global guard protects routes by default; `@Public()` is explicit bypass.
- All normal controller outputs pass through global envelope interceptor unless they already are an envelope.
- Global exception filter owns safe error envelope.
- `/health/ready` probes PostgreSQL only. Redis `configured` means URL exists, not that Redis is healthy.
- Current Prisma domain is only `SystemRecord`; do not invent Work domain models from old Flutter/Supabase code.
