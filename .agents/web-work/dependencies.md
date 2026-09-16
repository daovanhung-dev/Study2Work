# Work Web dependencies

`CONTEXT_STATUS: VERIFIED_WORK_WEB`

Work web receives its API base from the public projection of
`apps/work-server/src/constants.ts`, injected by `vite.config.ts`; it does not
read `VITE_*` runtime environment variables. The browser never receives Neon
credentials and Work API does not serve the web bundle. The current client uses
React Query, Zod and the existing `apiRequest` session boundary. Identity refresh
remains owned by the Identity service; the Work API receives access Bearer
tokens only. Vite uses a public-only virtual module for both development and
production and disables automatic `.env` file loading.
