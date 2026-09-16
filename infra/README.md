# Infrastructure

Local infrastructure is currently defined in the root `docker-compose.yml`.

Expected local services:

- Study PostgreSQL
- Study Redis
- Work PostgreSQL
- Work Redis
- MinIO
- Mailhog
- Study API
- Work API
- Work web

The Work services use PostgreSQL and Redis only. The former Learn2Earn MySQL
container is deliberately not part of the local stack; legacy MySQL data is not a
runtime dependency of `apps/work-server` or `apps/work-client/web`.
`apps/work-server/prisma/migrations` is the runtime source of truth. The
reviewable PostgreSQL design is at
`infra/postgres/work-server/schema.sql`; `infra/mysql/work-server/schema.sql`
is retained as legacy/design-only and is not executed by Work.

Start the separated Work API and web application with:

```bash
cp apps/work-server/src/constants.example.ts apps/work-server/src/constants.ts
# edit ACTIVE_PROFILE = "docker"
corepack pnpm --filter work-api work:compose -- up --build work-api work-web
```

The API is published at `http://localhost:8001`; the static Work web application
is published at `http://localhost:5174`. Compose and Prisma use the selected
Work profile from `apps/work-server/src/constants.ts`.

Future deployment-specific files should live under this folder.
