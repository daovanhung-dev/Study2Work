# Study Web context index

## Current source status

`apps/study-client/` contains an Angular 22 standalone SPA with a readiness
page at `/`, AD-01 at `/admin`, and presentation-only AD-02 at `/admin/users`;
the routes use lazy-loaded groups and share `AdminLayout`. The readiness route
is a root scaffold, not SH-01. AD-02 has an honest disconnected empty state and
disabled search/filter/pagination controls; it has no user records, API call or
auth guard. DD/API #68 remains blocked for functional implementation, and the
unguarded Admin routes provide navigation only. Other business screens, auth,
feature-specific Study API calls, and deployment remain unwired or unverified.
The typed registry in `src/app/core/constant/api.constants.ts` defines catalog
APIs #1–#103 and source-only route R-X01. `StudyApiService` in
`src/app/core/http/` consumes those descriptors through the local `/api/v1`
proxy and rejects `UNWIRED` entries. `WIRED` records an exact route-source
match and does not verify deployment; API #2 is an email-delivery stub. Check
current source for each screen task.

## Pages

| Topic | Page | Authority |
|---|---|---|
| Shared Study API registry, HTTP transport and envelope | `src/app/core/constant/api.constants.ts`, `src/app/core/http/study-api.service.ts`, `src/app/core/http/api-envelope.ts`, `proxy.conf.json` | 103 catalog descriptors plus source-only R-X01; transport rejects `UNWIRED`; feature callsites and production routing remain unverified. |
| Study screen inventory and screen/API traceability | [`list_screen.md`](../../../apps/study-client/docs/list_screen.md) | Screen IDs, routes, API references and design/gate context; not proof of implemented UI. |
| Study endpoint catalog | [`list_endpoint.md`](../../../apps/study-client/docs/list_endpoint.md) | API IDs, method/path and design I/O for 103 endpoints; not proof of runtime wiring. |
| Mandatory frontend layer, UI/business, and dependency rules | [`../../web-study/frontend-rules.md`](../../web-study/frontend-rules.md) | Required for Study Web coding/fix/test/review and architecture-document tasks. |
| Screen folder, route and layout structure | [`../../web-study/frontend-rules.md`](../../web-study/frontend-rules.md) | Target structure: shared/auth/system, guest, student, mentor, admin groups; four direct folders per screen. |
| Screen implementation, DD analysis, demo and fixture cleanup | [`workflows/screen-implementation.md`](workflows/screen-implementation.md) | Registered workflow `study-web-screen-coding`; required for individual screen coding/fix/test/demo. |
| Visual, interaction and accessibility target | [`../../web-study/design.md`](../../web-study/design.md) | Intended design only; not runtime evidence. |
| Angular folders, file responsibilities, and boundaries | [`../../../apps/study-client/gui/architech.md`](../../../apps/study-client/gui/architech.md) | Current scaffold and planned feature structure; no business behavior. |
| Admin presentation routes and shared shell | `src/app/features/admin/admin.routes.ts`, `src/app/layouts/admin/`, `src/app/features/admin/AD02/` | `/admin` renders AD-01 and `/admin/users` renders presentation-only AD-02; API #68, auth and user data remain unwired/blocked. |
| Skill-formatted screen DD packages | [`../../../apps/study-client/docs/dd_screens/screen-index.md`](../../../apps/study-client/docs/dd_screens/screen-index.md) | 83 source-derived packages; route/API status stays per screen, and the packages do not prove runtime wiring. |

For every Study FE task, follow the mandatory scope preflight in
[`AGENTS.md`](AGENTS.md): read both catalogs, identify the affected screen/API
IDs, and record them in the task worklog. Use `screen-index.md` to locate
relevant screen DD packages and each endpoint row's Overview link to locate
Study API DD. Treat catalogs, screen DDs, and API DDs as design evidence; check
current source when describing runtime behavior. Screen assets in
[`screen_stitch/`](../../../apps/study-client/docs/screen_stitch/) are visual
references and do not establish runtime behavior.

The structure in `frontend-rules.md` is the intended next implementation
structure. The current placeholder directories do not yet prove that those
groups, layouts, routes or screen modules are implemented.
