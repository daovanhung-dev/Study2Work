# Work Server agent entry

Source root: `apps/work-server/`

```text
CONTEXT_MODE: DEEP
RUNTIME_STATUS: VERIFIED_EXPRESS_STUDY_STYLE_COMPATIBILITY_API
STACK: Express 4 + TypeScript + Prisma/PostgreSQL + Neon
AUTH: JWT Bearer-only
```

Canonical page graph: `INDEX.md`.

## Load theo task

| Task | Context |
|---|---|
| auth/config/Prisma | `src/core/config.ts`, `src/core/security/`, `src/core/database.ts`, `src/config/prisma.config.ts` |
| API route | `src/api/v1.ts` + `src/modules/*/routes.ts` |
| schema/migration | `prisma/schema.prisma` + `prisma/migrations/` |
| tests | package scripts, TypeScript/Prisma validation, and source-aligned client tests |

## Critical rules

- Internal imports use NodeNext ESM `.js` suffix.
- Runtime configuration comes from `src/core/config.ts`; runtime code does not load `.env`.
  `DATABASE_URL`, `DIRECT_DATABASE_URL`, and `JWT_SECRET` are required; the JWT
  secret must be at least 32 characters. `JWT_EXPIRES` is optional.
- Prisma is created through `src/core/database.ts` and injected through `createApp`; the
  compatibility export in `src/config/prisma.config.ts` remains for legacy callers.
- `src/app.ts` is `createApp(options)` and mounts trace/config/auth middleware plus
  `src/api/v1.ts` at `/api/v1`; `src/routes/api_routes.ts` is a re-export only.
- Protected requests must send exactly one `Authorization: Bearer <JWT>` header.
- The server does not authenticate from cookies and does not maintain server-side sessions.
- JWT payloads contain numeric `id`, string `email`, and string `role` (`student` or `business`).
- New account passwords are stored as bcrypt cost 12 hashes. Legacy plaintext
  rows can authenticate once and are best-effort rehashed after successful login.
- API projections exclude `matkhau`; password hashes must never be returned in
  registration, `/me`, application relations, or Prisma response data.
- Role middleware owns access checks for the versioned API routes.
- Domain modules follow `models.ts -> validate.ts -> view.ts -> query.ts`; only query
  files call Prisma, and async route errors reach the centralized exception handler.
- `GET /api/v1`, `/health/live`, and `/health/ready` are wired. Readiness probes the
  injected Prisma dependency; Redis is optional configuration only.
- Authentication failures return JSON `401/403` responses; browser navigation and pages are owned by React.
- React Work Web consumes the versioned API at `/api/v1`; the server does not mount browser views.
- Logout is stateless: clients remove their access token; there is no token denylist.
- Supabase config/dependency and several legacy service files exist but are not used by the current API router.
- Preserve existing API route paths and Prisma model/table names unless the task explicitly changes the contract.
