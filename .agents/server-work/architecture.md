# Work Server architecture

## Runtime composition

```text
src/main.ts
  -> shared Prisma $connect()
  -> Express app.listen(PORT)

src/app.ts
  -> JSON parser
  -> static public assets
  -> optional JWT Bearer parser
  -> versioned JSON API router
```

The runtime is an API-only Express 4 server. `src/utils/constants.ts` is the
runtime configuration source; `.env` is not loaded. React owns all browser
views in the separate Work Web package.

## Authentication

`authenticateToken` parses exactly one `Authorization: Bearer <JWT>` header and
places the validated `{ id, email, role }` principal on `request.user`.
Protected student/business API routes apply `ensureAuthenticated` and
`checkRole`. Cookies, Passport and server-side sessions are not authentication
mechanisms.

## Persistence

All services use the shared Prisma client and the PostgreSQL schema in
`prisma/schema.prisma`, deployed to Neon. The current schema preserves the
legacy Work models and table names.
