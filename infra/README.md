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
`apps/work-server/prisma/migrations` begins a clean PostgreSQL history and does
not replay or transform the retired MySQL schema.

Start the separated Work API and web application with:

```bash
docker compose up --build work-api work-web
```

The API is published at `http://localhost:8001`; the static Work web application
is published at `http://localhost:5174` and is built with
`VITE_WORK_API_URL=http://localhost:8001/api/v1`.

Future deployment-specific files should live under this folder.
