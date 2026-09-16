# Work Server agent entry

Source root: `apps/work-server/`

```text
CONTEXT_MODE: DEEP
RUNTIME_STATUS: VERIFIED_EXPRESS_REACT_API
STACK: Express 4 + TypeScript + React Web API + Prisma/PostgreSQL + Neon
AUTH: JWT Bearer-only
```

## Load theo task

| Task | Context |
|---|---|
| auth/config/Prisma | `src/utils/constants.ts`, `src/utils/jwt.ts`, `src/config/prisma.config.ts` |
| API route | `src/routes/` + `src/services/` |
| schema/migration | `prisma/schema.prisma` + `prisma/migrations/` |
| tests | runnable npm scripts and targeted smoke checks |

## Critical rules

- Internal imports use NodeNext ESM `.js` suffix.
- Runtime configuration comes from `src/utils/constants.ts`; runtime code does not load `.env`.
- Prisma uses the shared client in `src/config/prisma.config.ts` and Neon PostgreSQL.
- Protected requests must send exactly one `Authorization: Bearer <JWT>` header.
- The server does not authenticate from cookies and does not maintain server-side sessions.
- JWT payloads contain numeric `id`, string `email`, and string `role` (`student` or `business`).
- Role middleware owns access checks for the versioned API routes.
- Authentication failures return JSON `401/403` responses; browser navigation is owned by React.
- React Work Web consumes the versioned API at `/api/v1`; the server does not mount browser views.
- Logout is stateless: clients remove their access token; there is no token denylist.
- Preserve existing API route paths and Prisma model/table names unless the task explicitly changes the contract.
