# Work Server architecture

## Runtime composition

```text
src/main.ts
  -> shared Prisma $connect()
  -> Express app.listen(PORT)

src/app.ts
  -> urlencoded/json parsers
  -> static public assets
  -> optional JWT Bearer parser
  -> web, student and business routers
```

The runtime is Express 4 with EJS views. `src/utils/constants.ts` is the
runtime configuration source; `.env` is not loaded.

## Authentication

`authenticateToken` parses exactly one `Authorization: Bearer <JWT>` header and
places the validated `{ id, email, role }` principal on `request.user`.
Protected student/business routers apply `ensureAuthenticated` and
`checkRole`. Cookies, Passport and server-side sessions are not authentication
mechanisms.

The EJS client uses `public/js/jwt-client.js` to store the access token locally,
attach Bearer headers to same-origin requests, and navigate protected HTML
pages through authenticated fetches.

## Persistence

All services use the shared Prisma client and the PostgreSQL schema in
`prisma/schema.prisma`, deployed to Neon. The current schema preserves the
legacy Work models and table names.
