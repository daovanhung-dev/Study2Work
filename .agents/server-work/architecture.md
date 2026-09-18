# Work Server architecture

## Runtime composition

```text
src/main.ts
  -> loadConfig()
  -> createDependencies()
  -> createApp({ config, dependencies })
  -> Prisma $connect()
  -> Express app.listen(PORT)

src/app.ts
  -> trace middleware / AsyncLocalStorage
  -> JSON parser
  -> static public assets
  -> `/uploads` static assets
  -> optional JWT Bearer parser
  -> `/health/live`, `/health/ready`
  -> `src/api/v1.ts`
  -> centralized JSON 404/exception handlers

src/api/v1.ts
  -> module route adapters
  -> models (Zod) -> validate -> view/use-case -> query/repository -> Prisma
```

The runtime is an API-only Express 4 server. `src/core/config.ts` is the typed
environment configuration source; `.env` is not loaded. `multer` handles image
uploads into the process `uploads/` directory. React owns all browser views in
the separate Work Web package; unknown server paths return JSON, not HTML.

## Authentication

`authenticateToken(config)` optionally parses one `Authorization: Bearer <JWT>` header
for every request. A valid token places `{ id, email, role }` on `request.user`;
`ensureAuthenticated` and `checkRole` protect the routes after the router-level
auth boundary. Cookies, Passport and server-side sessions are not
authentication mechanisms.

## Persistence

Wired domain query/repository modules use the injected Prisma dependency and the
PostgreSQL schema in `prisma/schema.prisma`, deployed to Neon. Compound CV,
application and business-job mutations use transaction boundaries. The current
schema preserves the legacy Work models and table names; legacy services remain
available only for compatibility and are not in the new route graph.
