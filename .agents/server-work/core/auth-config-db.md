# Work auth, config and database core

## Configuration

`apps/work-server/src/utils/constants.ts` is the tracked static runtime
configuration source. `apps/work-server/src/core/config.ts` validates and
normalizes those values for the application. The Express server does not call
`dotenv.config()` and does not read configuration from `.env` or `process.env`.
The required `DATABASE_URL`, `DIRECT_DATABASE_URL`, and `JWT_SECRET` constants
fail fast if missing or invalid; `JWT_SECRET` must contain at least 32
characters and `JWT_EXPIRES` defaults to `1d`. Prisma CLI commands receive the
database constants through `scripts/prisma-with-constants.ts`.

## JWT authentication

`src/core/security/access-token.ts` owns HS256 signing/verification and
`src/middleware/auth.middleware.ts` parses exactly one
`Authorization: Bearer <JWT>` header and verifies it with
`src/utils/jwt.ts`. A valid payload must contain numeric `id`, string `email`
and string `role`. The principal is assigned to `request.user`.

`ensureAuthenticated` rejects missing/invalid credentials with a JSON `401`.
Role failures return JSON `403`; there is no content-aware HTML redirect.
Cookies, Passport and server-side sessions are not read or created.

New and changed passwords use bcrypt cost 12. Login verifies bcrypt hashes and
supports a legacy plaintext row only for compatibility; a successful legacy
login best-effort rehashes that row. The canonical request key is `password`;
`matkhau` remains a deprecated compatibility alias.

## Prisma

`src/core/database.ts` creates Prisma and `src/core/dependencies.ts` injects it
into `createApp` and module views. `src/config/prisma.config.ts` is retained as
a compatibility export. `SinhVien.matkhau` and `DoanhNghiep.matkhau` are
`VARCHAR(255)`. Do not construct an additional Prisma client in a domain
module. API selects exclude both password columns.
