# Neon DB Admin Web

Angular control plane for the local Neon DB Admin API. The development
launcher starts the FastAPI process automatically, so the web app is the only
command that needs to be run during local development. Runtime configuration is
kept in the backend constants module; `.env` is not used.

## Run

Create the local backend constants once:

```bash
cp apps/db-admin-server/app/core/constants.example.py \
   apps/db-admin-server/app/core/constants.py
# Edit apps/db-admin-server/app/core/constants.py and set DATABASE_TARGETS for
# work_server and study_server.
```

Then run Angular (the FastAPI API starts automatically):

```bash
# If Node/npm is installed under ~/.local but is not yet in PATH:
export PATH="$HOME/.local/node-v24.21.0-linux-x64/bin:$HOME/.local/bin:$PATH"
npm install
npm run dev
```

Open `http://127.0.0.2:3000`. Requests to `/api/v1/admin` are proxied to the
internal FastAPI process at `127.0.0.1:3001`; the browser never receives the
Neon connection string.

Press `Ctrl+C` once to stop both processes. The backend can still be started
directly from `apps/db-admin-server/` for backend-only testing, but a second
terminal is not needed for the web flow.

The app keeps access tokens in memory only. Local DB Admin login uses the
username/password form and a short-lived local JWT; the first temporary login
must be followed by a password change. OIDC/Identity redirect remains an auth
fallback and the DB Admin API verifies that token through JWKS.

The workspace keeps database selection, schema selection, the PostgreSQL
catalog tree and the SQL editor in one view. SQL runs only after a database and
schema are selected; read-only queries run immediately after validation, while
mutations require explicit confirmation. The root account can open Manage
access in the same view to provision scoped developer accounts, rotate their
secrets, reassign schemas and inspect control-plane audit events.
