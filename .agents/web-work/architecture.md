# Work Web architecture

`CONTEXT_STATUS: VERIFIED_WORK_WEB`

- Study: `apps/study-client/`, Vue 3/TypeScript/Vite đã được package xác nhận.
- Work: `apps/work-client/web/`, React/TypeScript/Vite đã được package xác nhận.
- `apps/work-client/web/src/app/router/index.tsx` owns the route catalog.
- `src/pages/DomainPage.tsx` is a compatibility route wrapper.
- `src/pages/WorkFeaturePage.tsx` maps public, candidate, enterprise,
  university and operations route families to live query/mutation screens.
- `src/shared/api/work.ts` owns typed Work API requests, Zod parsing and
  mutation headers. No browser code connects to Neon directly.
- React Query owns request lifecycle; page-local form state stays in React.
