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
# Edit apps/db-admin-server/app/core/constants.py and set URL_DATABASE.
```

Then run Angular (the FastAPI API starts automatically):

```bash
# If Node/npm is installed under ~/.local but is not yet in PATH:
export PATH="$HOME/.local/node-v24.21.0-linux-x64/bin:$HOME/.local/bin:$PATH"
npm install
npm run dev
```

Open `http://localhost:5175`. Requests to `/api/v1/admin` are proxied to the
internal FastAPI process at `127.0.0.1:8010`; the browser never receives the
Neon connection string.

Press `Ctrl+C` once to stop both processes. The backend can still be started
directly from `apps/db-admin-server/` for backend-only testing, but a second
terminal is not needed for the web flow.

The app keeps access tokens in memory only. Production login is expected to be
provided by the configured OIDC/Identity redirect and the DB Admin API verifies
the resulting token through JWKS.

The catalog page exposes schema/table builders plus an advanced definition
editor for common PostgreSQL objects. The table browser supports pagination,
contains filters, header sorting and primary-key-gated row CRUD; every row
mutation first requests a backend preview token.
