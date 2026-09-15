# Neon DB Admin API

Local-only FastAPI service for administering one configured Neon PostgreSQL
database. The API owns the database credential; the Angular client never sees
`URL_DATABASE`. During local web development, Angular's launcher starts this
service automatically. Runtime configuration is read from
`app/core/constants.py`; `.env` is not used.

## Run

```bash
uv sync
uv run --no-env-file --no-dev uvicorn app.main:app --reload --host 127.0.0.1 --port 8010
```

Create the local constants before running directly:

```bash
cp app/core/constants.example.py app/core/constants.py
```

For the complete local UI flow, use the single command from the web app:

```bash
cd ../db-admin-web
npm install
npm run dev
```

Local UI work uses `DEV_AUTH=True` from `app/core/constants.py`. A production
configuration must set `APP_ENV` and configure JWKS, issuer, audience and a
permission-bearing access token in that constants module.

The service uses a request-scoped SQLAlchemy connection with the psycopg3
driver. Catalog reads come from PostgreSQL system catalogs. Mutations require a
short-lived confirmation token, use a dedicated transaction and write a
bounded local audit record plus a structured log entry. DDL drop previews
include a bounded dependent-object impact list where PostgreSQL catalog
metadata can resolve one. Row CRUD uses
`/tables/{schema}/{table}/rows/preview` before the corresponding insert, update
or delete request.
