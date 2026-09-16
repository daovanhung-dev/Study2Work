# Work Server agent entry

Source root: `apps/work-server/`

```text
CONTEXT_MODE: DEEP
RUNTIME_STATUS: VERIFIED_EXPRESS_WEB
STACK: Express 4 + TypeScript + EJS + Prisma/PostgreSQL + Neon
AUTH: JWT Bearer-only
```

## Load theo task

| Task | Context |
|---|---|
| auth/config/Prisma | `src/utils/constants.ts`, `src/utils/jwt.ts`, `src/config/prisma.config.ts` |
| web/API route | `src/routes/` + `src/controllers/` |
| schema/migration | `prisma/schema.prisma` + `prisma/migrations/` |
| tests | runnable npm scripts and targeted smoke checks |

## Critical rules

- Internal imports use NodeNext ESM `.js` suffix.
- Runtime configuration comes from `src/utils/constants.ts`; runtime code does not load `.env`.
- Prisma uses the shared client in `src/config/prisma.config.ts` and Neon PostgreSQL.
- Protected requests must send exactly one `Authorization: Bearer <JWT>` header.
- The server does not authenticate from cookies and does not maintain server-side sessions.
- JWT payloads contain numeric `id`, string `email`, and string `role` (`student` or `business`).
- Role middleware owns access checks for `/student` and `/business` routes.
- HTML authentication failures redirect to the public sign-in role page; API requests receive JSON `401/403` responses.
- Logout is stateless: clients remove their access token; there is no token denylist.
- Preserve existing route paths and Prisma model/table names unless the task explicitly changes the contract.
