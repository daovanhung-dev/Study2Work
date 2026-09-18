# Neon DB Admin context

```text
CONTEXT_STATUS: VERIFIED
WEB_ROOT: apps/db-admin-web/
SERVER_ROOT: apps/db-admin-server/
DEPLOYMENT: local-only; one Angular command launches Angular + internal FastAPI
DATABASE: two backend-owned Neon PostgreSQL targets (`work_server`, `study_server`)
```

Canonical page graph: `INDEX.md`.

## Boundary

The Angular standalone client never connects to Neon and never stores a database
credential or access token in browser storage. The FastAPI service owns the
database connection, OIDC/JWKS validation and all PostgreSQL side effects. It is
separate from Study API, Work API and AI API; do not import their business
modules or database models.

## Verified surface

- Frontend entry: `apps/db-admin-web/src/main.ts`; the authenticated workspace
  keeps target selection, schema selection, catalog tree and SQL editor in one
  view. Login remains a separate auth fallback route.
- Local `dev`/`start` commands run `scripts/dev.mjs`, which starts FastAPI and
  proxies same-origin `/api` requests to loopback.
- Backend entry: `apps/db-admin-server/app/main.py`; API routes are under
  `/api/v1/admin` and use the repository response envelope. `GET /databases`
  lists configured target IDs without connection details; catalog and SQL
  requests select the target explicitly.
- Catalog reads `information_schema` and `pg_catalog` for schemas, tables,
  columns, constraints, indexes, sequences, types, views, routines, triggers
  and grants.
- SQL requests require a configured target and schema. The backend validates the
  target, checks the schema, sets a transaction-local `search_path`, blocks
  transaction/session-control, role, `ALTER SYSTEM` and `COPY`; read queries
  rollback and mutations commit only after confirmation.
- Legacy DDL and row CRUD routes remain backend-compatible but are not exposed
  by the simplified UI.
- Audit keeps a bounded in-memory fallback and structured logger output, and
  the control-plane bootstrap adds durable `db_admin.admin_audit_events` rows
  for local auth, access management, catalog and target-scoped SQL actions.
- Local password auth is available at `/auth/login`, `/auth/change-password`
  and `/auth/me`. It uses Argon2id application hashes and short-lived local
  JWTs; tokens remain in frontend memory only. OIDC/JWKS remains the fallback.
- Root-only access management is exposed at `/access/accounts` and
  `/access/audit`; developer principals receive only their assigned target and
  schema in database/catalog responses.
- `sql/db_admin/001_bootstrap.sql` and `scripts/bootstrap_access.py` are an
  independent operator bootstrap for the `db_admin` control schema, the shared
  app root identity and the target-local developer role/schema bindings.
- `scripts/bootstrap_access.py --set-developer-password` interactively resets
  the default `study_dev` and `work_dev` app/ PostgreSQL passwords without
  writing plaintext credentials to source, logs or audit; it preserves the
  existing schema ownership and bindings and re-enables first-login change.

## Configuration and checks

Backend reads `DATABASE_TARGETS` and all other runtime values from
`apps/db-admin-server/app/core/constants.py`; local password auth requires a
private `LOCAL_JWT_SECRET` of at least 32 characters. When local auth is off,
real auth requires the JWKS, issuer and audience constants. `DEV_AUTH=True` is
reserved for tests. The launcher checks that `constants.py` exists, starts the
backend on `127.0.0.1:8010`, and proxies same-origin `/api` requests to it. The
frontend uses a relative API base URL and in-memory token handling. `.env` is
not used.

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
