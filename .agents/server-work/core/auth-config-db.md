# Work auth, config and database core

## Configuration

`apps/work-server/src/utils/constants.ts` is the runtime configuration source.
The Express server does not call `dotenv.config()` or read runtime values from
`.env`. Prisma CLI commands receive the constants through
`scripts/prisma-with-constants.ts`.

## JWT authentication

`src/middleware/auth.middleware.ts` parses exactly one
`Authorization: Bearer <JWT>` header and verifies it with
`src/utils/jwt.ts`. A valid payload must contain numeric `id`, string `email`
and string `role`. The principal is assigned to `request.user`.

`ensureAuthenticated` rejects missing/invalid credentials. HTML requests are
redirected to `/signInRole`; API-style requests receive JSON `401`. Role
failures return/redirect as `403`. Cookies, Passport and server-side sessions
are not read or created.

## Prisma

Services use the shared Prisma client in `src/config/prisma.config.ts` with
Neon PostgreSQL. Do not construct an additional Prisma client in a domain
module.
