# Infrastructure

Local infrastructure is currently defined in the root `docker-compose.yml`.

The historical compose inventory includes:

- Study PostgreSQL
- Study Redis
- Work PostgreSQL
- Work Redis
- MinIO
- Mailhog
- Study API
- Work API
- Work web

The former Learn2Earn MySQL container is deliberately not part of the local
stack; legacy MySQL data is not a runtime dependency of
`apps/work-server` or `apps/work-client/web`. The current Work runtime uses the
Neon PostgreSQL database configured in
`apps/work-server/src/utils/constants.ts`; Redis is not used by the Express
server.

Start the separated Work API and web application with:

```bash
corepack pnpm --filter work_server prisma:validate
corepack pnpm --filter work_server prisma:generate
corepack pnpm dev:work-server
corepack pnpm dev:work-web
```

The Express API listens at `http://127.0.0.1:3002`; Vite serves Work Web at
`http://127.0.0.2:3001` and proxies `/api`, `/uploads`, and `/img` to the API.

Future deployment-specific files should live under this folder.
