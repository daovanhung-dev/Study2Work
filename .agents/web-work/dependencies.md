# Work Web dependencies

`CONTEXT_STATUS: VERIFIED_REACT_EXPRESS_SPLIT`

Work web uses the relative `/api/v1` API base and Vite's `envDir` points to an
empty directory, so the client does not read repository `.env` or `VITE_*`
runtime variables. Vite binds at `127.0.0.2:3001` and proxies `/api`,
`/uploads`, and `/img` to the Express Work server at `127.0.0.1:3002` during
development; production uses a same-origin reverse proxy. The browser never
receives Neon credentials. The package declares
React, React Router, React Query, Zod, Zustand, Lucide and Vitest; runtime API
requests use native `fetch` in `apiRequest` (Axios is declared but is not the
current request path). React is the only Work presentation layer; Express owns
the API/data boundary.
