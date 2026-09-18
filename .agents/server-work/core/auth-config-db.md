# Work auth, config and database core

## Configuration

`apps/work-server/src/utils/constants.ts` is the runtime configuration source.
The Express server does not call `dotenv.config()` or read runtime values from
`.env`. The process launcher must provide `DATABASE_URL`,
`DIRECT_DATABASE_URL`, and a `JWT_SECRET` with at least 32 characters; the
optional `JWT_EXPIRES` defaults to `1d`. Missing required values fail fast.
Prisma CLI commands receive the constants through
`scripts/prisma-with-constants.ts`.

## JWT authentication

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

Services use the shared Prisma client in `src/config/prisma.config.ts` with
Neon PostgreSQL. `SinhVien.matkhau` and `DoanhNghiep.matkhau` are
`VARCHAR(255)`. Do not construct an additional Prisma client in a domain
module. API selects exclude both password columns.
