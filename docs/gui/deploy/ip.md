# Study2Work local service addresses

Canonical local development map:

| Role | Address | Startup / consumer |
|---|---|---|
| AI server | `http://127.0.0.1:3000` | `cd apps/ai-server && uv run uvicorn app.main:app --host 127.0.0.1 --port 3000` |
| DB Admin server | `http://127.0.0.1:3001` | Started by `apps/db-admin-web/scripts/dev.mjs` or the DB Admin README command |
| Work server | `http://127.0.0.1:3002` | `corepack pnpm dev:work-server` |
| Study server | `http://127.0.0.1:3003` | `cd apps/study-server && uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 3003` |
| DB Admin client | `http://127.0.0.2:3000` | `cd apps/db-admin-web && npm run dev` |
| Work client | `http://127.0.0.2:3001` | `corepack pnpm dev:work-web` |
| Study client | `http://127.0.0.2:3002` | `corepack pnpm dev:study-web` |

## Client-to-server routing

- DB Admin Angular uses relative `/api/v1/admin` and proxies to
  `http://127.0.0.1:3001`.
- Work Web uses relative `/api/v1`, `/uploads` and `/img` and proxies them to
  `http://127.0.0.1:3002`.
- Study Web uses `VITE_STUDY_API_URL` when provided; its local fallback is
  `http://127.0.0.1:3003`.

## Health and system URLs

- DB Admin: `http://127.0.0.1:3001/health/live`
- Work: `http://127.0.0.1:3002/health/live` and
  `http://127.0.0.1:3002/api/v1`
- Study: `http://127.0.0.1:3003/health/live`
- AI: `http://127.0.0.1:3000/`

The service map changes only application startup/client routing. PostgreSQL,
Redis, Ollama, and test fixture addresses remain unchanged. In Docker, app
containers bind internally to `0.0.0.0`; the published host addresses follow
the table above.
