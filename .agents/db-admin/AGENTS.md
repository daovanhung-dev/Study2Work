# Neon DB Admin context

```text
CONTEXT_STATUS: VERIFIED
WEB_ROOT: apps/db-admin-web/
SERVER_ROOT: apps/db-admin-server/
DEPLOYMENT: local-only; one Angular command launches Angular + internal FastAPI
DATABASE: one backend-owned Neon PostgreSQL URL from local core/constants.py
```

## Boundary

The Angular standalone client never connects to Neon and never stores a database
credential or access token in browser storage. The FastAPI service owns the
database connection, OIDC/JWKS validation and all PostgreSQL side effects. It is
separate from Study API, Work API and AI API; do not import their business
modules or database models.

## Verified surface

- Frontend entry: `apps/db-admin-web/src/main.ts`; routes cover dashboard,
  catalog, table rows, SQL editor and audit.
- Local `dev`/`start` commands run `scripts/dev.mjs`, which starts FastAPI and
  proxies same-origin `/api` requests to loopback.
- Backend entry: `apps/db-admin-server/app/main.py`; API routes are under
  `/api/v1/admin` and use the repository response envelope.
- Catalog reads `information_schema` and `pg_catalog` for schemas, tables,
  columns, constraints, indexes, sequences, types, views, routines, triggers
  and grants.
- DDL and row mutations use preview/confirmation tokens. SQL validation blocks
  transaction/session-control, role, `ALTER SYSTEM` and `COPY`; read queries
  rollback and mutations commit in isolated transactions with timeouts.
- Row edit/delete (and insert in the UI contract) requires a primary key;
  views and tables without a primary key are read-only in the data browser.
- Audit is bounded in-memory plus structured logger output; it is not a new
  Neon table in this phase.

## Configuration and checks

Backend reads `URL_DATABASE` and all other runtime values from
`apps/db-admin-server/app/core/constants.py`; real auth requires the JWKS,
issuer and audience constants. Local defaults use `DEV_AUTH=True`. The launcher
checks that `constants.py` exists, starts the backend on `127.0.0.1:8010`, and
proxies same-origin `/api` requests to it. The frontend uses a relative API
base URL and in-memory token handling. `.env` is not used.

Run from repository root with the repository's Node runtime on PATH:

```bash
pnpm --filter db-admin-web build
pnpm --filter db-admin-web test
```

Run backend from `apps/db-admin-server/` with the Study virtual environment or
an equivalent environment providing the declared dependencies:

```bash
ruff check app tests
mypy app
PYTHONPATH=. pytest -q
```

No live Neon mutation is part of the verified local test suite.
