# Work Server architecture

## Runtime composition

```text
src/main.ts
  -> shared Prisma $connect()
  -> Express app.listen(PORT)

src/app.ts
  -> JSON parser
  -> static public assets
  -> `/uploads` static assets
  -> optional JWT Bearer parser
  -> versioned JSON API router
  -> JSON 404/500 envelope handlers
```

The runtime is an API-only Express 4 server. `src/utils/constants.ts` is the
runtime configuration source; `.env` is not loaded. `multer` handles image
uploads into the process `uploads/` directory. React owns all browser views in
the separate Work Web package; unknown server paths return JSON, not HTML.

## Authentication

`authenticateToken` optionally parses one `Authorization: Bearer <JWT>` header
for every request. A valid token places `{ id, email, role }` on `request.user`;
`ensureAuthenticated` and `checkRole` protect the routes after the router-level
auth boundary. Cookies, Passport and server-side sessions are not
authentication mechanisms.

## Persistence

Wired domain services use the shared Prisma client and the PostgreSQL schema in
`prisma/schema.prisma`, deployed to Neon. The current schema preserves the
legacy Work models and table names; empty/unused legacy services are not runtime
modules until a route imports them.
