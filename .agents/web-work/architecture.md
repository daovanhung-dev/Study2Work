# Work Web architecture

`CONTEXT_STATUS: VERIFIED_REACT_EXPRESS_SPLIT`

- Study: `apps/study-client/`, Vue 3/TypeScript/Vite đã được package xác nhận.
- Work: `apps/work-client/web/`, React/TypeScript/Vite đã được package xác nhận.
- `apps/work-client/web/src/app/router.tsx` owns the public, student and business
  route catalog and role guards.
- `src/pages/PublicPages.tsx` maps public home, role, login and registration
  screens; `src/pages/WorkspacePages.tsx` maps the active student/business flows.
- `src/shared/api/work.ts` owns typed Work API requests, Zod parsing and
  Bearer injection. No browser code connects to Neon directly.
- React Query owns request lifecycle; page-local form state stays in React.
- `apps/work-server` is API-only; React is the sole Work browser rendering layer.
