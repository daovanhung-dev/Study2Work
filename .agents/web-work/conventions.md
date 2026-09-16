# Work Web conventions

`CONTEXT_STATUS: VERIFIED_REACT_EXPRESS_SPLIT`

Work web uses React 19 + TypeScript + Vite. API calls go through `apiRequest`
and the Work API client; response envelopes and selected data are parsed with
Zod before rendering. React Query handles loading, retry and cache invalidation;
the configured defaults are 15-second stale time and one retry. Requests use the
relative `/api/v1` base, an optional `Authorization: Bearer <JWT>` header and
`credentials: omit`. The only browser-persisted auth value is `access_token`;
cookies and query-string tokens are not used. Forms render server validation and
mutation error states. Do not mix Vue patterns from Study web into Work web.

Presentation follows `.agents/project/design.md`: consume the semantic Cobalt
tokens and shared UI primitives instead of adding local primary colors,
spacing, radii or shadows. Interactive controls must keep visible
`focus-visible`, hover/pressed/disabled states, minimum 44px targets and
reduced-motion behavior. Static routes remain presentation-only when their API
is not wired; local UI state must not be described as persisted backend data.
