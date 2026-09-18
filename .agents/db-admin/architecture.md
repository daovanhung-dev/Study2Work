# DB Admin architecture

DB Admin is an independent local deployable composed of an Angular Web app and
a FastAPI server. The Angular launcher in `apps/db-admin-web/scripts/dev.mjs`
starts the backend and proxies same-origin `/api` requests; Study, Work and AI
do not mount or import this application.

The browser owns UI state only. Database connections, OIDC/JWKS or local auth,
permissions and PostgreSQL side effects belong to `apps/db-admin-server/`.
