# Work Web conventions

`CONTEXT_STATUS: VERIFIED_REACT_EXPRESS_SPLIT`

Work web uses React + TypeScript + Vite. API calls go through `apiRequest` and
the Work API client; response bodies are parsed with Zod before rendering.
React Query handles loading, retry and cache invalidation. Requests use the
relative `/api/v1` base and `Authorization: Bearer <JWT>` with
`credentials: omit`. The only browser-persisted auth value is the required
`access_token`; cookies and query-string tokens are not used. Forms render
server validation/error states. Do not mix Vue patterns from Study web into Work
web.
