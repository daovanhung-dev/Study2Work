# Neon DB Admin API

Local-only FastAPI service for administering the configured Work and Study Neon
PostgreSQL targets. The API owns both database credentials; the Angular client
never sees them. During local web development, Angular's launcher starts this
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

Local UI work uses the DB Admin local account flow. Configure the
`DATABASE_TARGETS` mapping with the `work_server` and `study_server` connection
URLs, set `LOCAL_AUTH_ENABLED=True`, and replace `LOCAL_JWT_SECRET` with a
private random value. `DEV_AUTH` is reserved for isolated tests.

Before the first sign-in, bootstrap the control plane independently from the
Study/Work business migrations:

```bash
uv run python scripts/bootstrap_access.py --dry-run
uv run python scripts/bootstrap_access.py --apply
```

The apply command reads the temporary root password interactively, creates the
`db_admin` schema and app identities, and writes newly generated developer
secrets once to the ignored local file `.local/bootstrap-credentials.json`
with mode `0600`. It never prints a password or accepts one on the command
line. Rotate any database credentials that have previously been exposed before
applying to a live target.

If the default developer accounts already exist and need a shared temporary
password, set it interactively without placing it in shell history:

```bash
uv run python scripts/bootstrap_access.py --set-developer-password
```

This updates `study_dev` on `study_server` and `work_dev` on `work_server`,
resets their first-login flag, and preserves their role/schema ownership and
bindings.

The service uses target-specific SQLAlchemy connections with the psycopg3
driver. Catalog reads come from PostgreSQL system catalogs. SQL requests must
include a configured database target and an existing schema; the backend sets a
transaction-local `search_path` before execution. Read queries rollback and
mutations require a short-lived confirmation token before commit. Legacy DDL,
row CRUD and audit endpoints remain available for compatibility but are not
used by the simplified web workspace. Local JWTs are short-lived and the web
client keeps them in memory only; root-only account management is exposed as a
drawer inside the single workspace.
