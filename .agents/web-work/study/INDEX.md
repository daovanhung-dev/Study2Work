# Study Web context index

## Current source status

`apps/study-client/` contains an Angular 22 standalone SPA with a readiness
page at `/`, AD-01 at `/admin`, and presentation-only AD-02 at `/admin/users`.
The Mentor FE merge was reverted; screens ME-06 through ME-18 and `/mentor`
routes are absent from current source. The Admin routes use `AdminLayout`. The
readiness route is a root scaffold, not SH-01. AD-02 has an honest disconnected
empty state and disabled search/filter/pagination controls; it has no user
records or auth guard. Auth, deployment and live API behavior remain
unverified.
ST-11 is now wired at `/student/lessons/:lessonId` as the documented static
fallback through `StudentLayout`; lesson content, player behavior, API calls,
other Student destinations and auth remain unwired or unverified.
The typed registry in `src/app/core/constant/api.constants.ts` defines catalog
APIs #1–#103 and source-only route R-X01. `StudyApiService` in
`src/app/core/http/` consumes those descriptors through the local `/api/v1`
proxy and rejects `UNWIRED` entries. `WIRED` records an exact route-source
match and does not verify deployment; API #2 is an email-delivery stub. Check
current source for each screen task.

`src/app/core/localStorage/local-storage.service.ts` provides generic JSON
read/write operations for browser `localStorage`; it has no feature caller and
does not integrate auth tokens.

## Pages

| Topic | Page | Authority |
|---|---|---|
| Shared Study API registry, HTTP transport and envelope | `src/app/core/constant/api.constants.ts`, `src/app/core/http/study-api.service.ts`, `src/app/core/http/api-envelope.ts`, `proxy.conf.json` | 103 catalog descriptors plus source-only R-X01; transport rejects `UNWIRED`; feature callsites and production routing remain unverified. |
| Generic browser storage | `src/app/core/localStorage/local-storage.service.ts` | JSON set/get utility; no feature caller or auth token integration. |
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

## Verified auth update (2026-11-18)

SH-02 now consumes the current Study Server API #03 token payload, stores a tab-scoped session in `sessionStorage`, confirms STUDENT via API #04, and navigates by role. `core/auth/auth.interceptor.ts` sends Bearer tokens and refreshes through source-only R-X01; `student-auth.guard.ts` protects `/student`. `StudentLayout` clears the client session on logout. This source-based wiring follows the user's explicit implementation request; SH-02 DD still records its older API #03 contract discrepancy and is not proof of a successful live login. The currently connected backend database lacks `refresh_tokens`, so live API #03 returns 500 until that schema is corrected.

## ST-09 read-only API update (2026-11-18)

`/student/courses/:courseId` verifies ACTIVE membership by paging authenticated API #20 before reading course lesson progress from #37 and public lesson titles from #09. The page renders sourced course identity and lesson progress, or blocks the view on absent membership/invalid data. It discards #09 `content` and `video_url`; ST-10 access and playback remain gated. The ST-09 DD source audit predates current #20/#37 backend routes and does not settle full course tree, quiz/assignment aggregate, or lesson handoff. The API registry now marks #37 WIRED; that means route source exists, not that every deployment or account has data.

## ST-10 visual and source audit (2026-11-18)

`/student/lessons/:lessonId/start` renders a gated ST-10 handoff with SVG icons and no media. The frontend calls API #22 once per valid route lesson ID, handles 200/403/404/error locally, and retains only safe lesson ID/course ID/title metadata. The current #22 backend response includes `content` and `video_url` and does not check lesson `PUBLISHED` before returning them; this requires a backend contract fix for full protection. #23 start and #24 detail remain unwired until the trigger/retry rule, protected payload handling and ST-11 handoff are settled. The progress bar has no fabricated completion width.
