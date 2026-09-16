# Work Web architecture

`CONTEXT_STATUS: VERIFIED_REACT_EXPRESS_SPLIT`

- Study: `apps/study-client/`, Vue 3/TypeScript/Vite đã được package xác nhận.
- Work: `apps/work-client/web/`, React/TypeScript/Vite đã được package xác nhận.
- `apps/work-client/web/src/app/router.tsx` owns public routes plus duplicated
  lower/upper-case student and business paths, with role guards.
- `src/pages/PublicPages.tsx` maps home, role, login and registration screens;
  `src/pages/WorkspacePages.tsx` maps job, CV, application and business flows,
  with static placeholders for notifications/chat/settings/interview/university.
- `src/shared/api/work.ts` owns relative `/api/v1` requests, envelope parsing,
  response schemas and Bearer injection. No browser code connects to Neon.
- `App.tsx` provides React Query and auth; page-local form state stays in React.
- `apps/work-server` is API-only; React is the sole Work browser rendering layer.

## Presentation foundation

- `src/styles/main.css` is the source-backed Cobalt token layer: semantic
  colors, spacing/controls, focus states, responsive breakpoints and reduced
  motion rules live there.
- `src/shared/ui/Primitives.tsx` provides the shared Button, Field, PageHeader,
  StatusBadge and Surface primitives; `States.tsx` provides the common loading,
  error and empty states.
- `layouts.tsx` owns the responsive public/workspace menu. It only changes
  presentation and closes the menu after existing links are selected; route
  aliases, role guards, logout and Outlet destinations remain unchanged.
