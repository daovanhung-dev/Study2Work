# Work Web module context

- App shell: `src/App.tsx`, `src/main.tsx`, `src/layouts.tsx` — React Query,
  auth restoration, public/workspace layouts.
- Routing/auth: `src/app/router.tsx`, `src/shared/auth/` — public routes,
  student/business guards, local token restoration and role checks.
- API boundary: `src/shared/api/work.ts` — relative `/api/v1`, envelope/Zod
  parsing, Bearer header and 401 token clearing.
- Public pages: `src/pages/PublicPages.tsx` — home job list, role selection,
  login and student registration.
- Workspace pages: `src/pages/WorkspacePages.tsx` — student jobs/CV/applications
  and business jobs/applications/CV detail; unsupported workspace features remain
  static/placeholder screens.
- UI foundation: `src/styles/main.css`, `src/shared/ui/Primitives.tsx` and
  `src/shared/ui/States.tsx` — Cobalt tokens, responsive layout, shared
  controls and loading/error/empty states.

When editing a feature, trace route -> page -> query/mutation -> API endpoint,
then verify loading/error/empty states and the direct Work API contract.
