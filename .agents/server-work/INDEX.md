# Work Server context index

Source root: `apps/work-server/`

| Task | Page |
|---|---|
| Runtime/composition | `architecture.md`, `core/runtime-http.md` |
| Auth/config/Prisma | `core/auth-config-db.md` |
| API route | `apis/foundation.md` |
| Module/service behavior | `modules/foundation.md` |
| Prisma schema/migration | `database.md` |
| Tests/validation | `tests.md` |
| Coding/fix workflow | `workflows/README.md` |

Always verify `src/app.ts`, `src/main.ts`, `src/api/v1.ts`, `src/core/`,
`src/modules/`, the compatibility `src/routes/api_routes.ts`, and
`prisma/schema.prisma` before changing a claim in these pages.
