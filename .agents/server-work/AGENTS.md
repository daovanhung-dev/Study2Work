# Work Server agent entry

Source root: `apps/work-server/`

```text
CONTEXT_MODE: DEEP
RUNTIME_STATUS: VERIFIED_DOMAIN_API
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
- Prisma now owns the clean Work PostgreSQL domain (55 application tables plus `system_records`); the MySQL SQL file is legacy/design-only.
- `WorkModule` owns the implemented candidate, jobs, applications, communication, interviews, tenant/university, payment and operations HTTP surface.
- Protected routes resolve `identity_subject_id`, tenant membership and server-side permissions; public job/company/product routes are explicit `@Public()` exceptions.
- Mutation routes use `If-Match` where revisions/history are versioned and `Idempotency-Key` for retry-sensitive writes. Provider-dependent payment/storage operations remain safe pending/unconfigured and never fake settlement or file-clean status.
