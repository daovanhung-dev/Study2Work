# Work Web conventions

`CONTEXT_STATUS: VERIFIED_WORK_WEB`

Work web uses React + TypeScript + Vite. API calls go through `apiRequest` and
the Work API client; response bodies are parsed with Zod before rendering.
React Query handles loading, retry and cache invalidation. Mutation requests
use `Idempotency-Key`; revision-aware writes may include `If-Match`. Forms
render server validation/conflict/error states and do not persist tokens or
sensitive data in localStorage, analytics or query strings. Do not mix Vue
patterns from Study web into Work web.
