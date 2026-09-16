# Work Web dependencies

`CONTEXT_STATUS: VERIFIED_REACT_EXPRESS_SPLIT`

Work web uses the relative `/api/v1` API base and does not read `.env` or
`VITE_*` runtime variables. Vite proxies `/api`, `/uploads`, and `/img` to the
Express Work server during development; production uses a same-origin reverse
proxy. The browser never receives Neon credentials. The current client uses
React Query, Zod, Zustand and the typed `apiRequest` JWT boundary. React is the
only Work presentation layer; the Express API remains the data owner.
