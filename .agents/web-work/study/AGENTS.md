# Study Web context router

Companion screen and API map: [INDEX.md](INDEX.md).

```text
CONTEXT_STATUS: VERIFIED_WITH_UNWIRED_COMPONENTS
GS07_SOURCE_STATUS: Root `/resources/:resourceId` route mounts a contract-blocked gate only; the route ID is not consumed, API #12 has no Study Web caller, and resource actions remain blocked. Browser/deployment runtime is unverified.
SOURCE_STATUS: Angular 22 SPA routes `/` to Shared SH-01 with independent API #05/#06 callers and search handoff, SH-02 presentation at /login, SH-03 API #01 registration caller at /register, partial Guest GS-01–GS-03 at /courses, /courses/search and /courses/:courseId (#05–#08 callers); GS03 owns the `?tab=curriculum|reviews|resources` panels. The app root wildcard redirects unknown routes to SH-06 and clears the original path/query; GS-03 #08 detail 404 also routes to SH-06, while #08 500 and #09 curriculum 404 stay separate. #09 and #10 load lazily after #08 succeeds; GS06 currently renders a contract-blocked panel and intentionally makes no #11/#12 call. API #11 route/module/query/tests exist locally but return only the first resource as a singleton; #11/#12 DDs and access/cardinality policy remain Draft/open. AD-01 through AD-25 and ST-11 through ST-26; Mentor remains unwired, SH-01/GS-01 loaded catalog states and GS-03/GS05/GS06 presentations are partial or derived because their DD assets do not fully specify runtime states. Enrollment remains open. Focused Study Web tests and local stub-backed browser renders are recorded per continuation; live API/DB runtime remains unverified. `admin.routes.ts` maps AD-01
through AD-25 beneath `AdminLayout`. Nineteen screen-level data-access callers
use fourteen distinct source-backed Admin GET APIs through `AdminApiService`.
`AdminSessionService` authenticates with API #3, refreshes through source-only
route R-X01, keeps credentials in tab memory only, and accepts only the
`ADMIN` role; API #4 and browser storage are not used. `AdminApiService` attaches
Bearer credentials and clears the local session on protected 401 responses.
The server-side Admin guard remains authoritative; this client wiring does not
prove deployment or API acceptance. AD-01 and AD-24/25 have no current report
sources; APIs #99–#103 are absent. API #18 has a backend route but only
notification-specific operation handling; the client descriptor remains
`UNWIRED` and generic lifecycle/result behavior is incomplete. Mutation
controls remain disabled where request, permission,
transition, deletion, moderation, delivery, report or export policy is open.
AD-01 and AD-02 also have page-specific layouts: AD-01 has no dashboard data
source because API #101 is absent; AD-02 reads users through API #68 and maps
only the supported keyword, role, status and page filters. AD-03, AD-04,
AD-05, AD-06, AD-07, AD-08, AD-09, AD-10, AD-11, AD-12, AD-13, AD-14,
AD-15, AD-16, AD-17, AD-18, AD-19, AD-20, AD-21, AD-22, AD-23, AD-24
and AD-25 also have screen-specific layouts. No routed Admin page imports
`AdminScreenSurface`; its current import is in its dedicated unit spec. AD-07 and AD-13 share a
host-scoped global detail stylesheet to stay within the component-style budget.
AD-04, AD-05, AD-06, AD-08, AD-09, AD-10, AD-12, AD-14, AD-15, AD-16, AD-17, AD-18, AD-19, AD-20, AD-21, AD-22, AD-23 and AD-24 have host-scoped page stylesheets registered globally in `angular.json`.
`src/styles.css` also defines the Admin-scoped `.page-width` container consumed by routed child templates; `AdminLayout` component CSS cannot style those children because Angular scopes it to the shell template. AD-01 retains its component page styles; AD-02 keeps heading/filter styles in its component CSS and uses `study-ad02-page`-prefixed global styles for the table/empty state. AD-01 uses the 1540px reference container while the remaining routed screens use the 1520px reference container, with shared tablet/mobile widths.
The shared `AdminLayout` shell follows the Admin DD's five primary navigation groups and routes notifications through the bell control. Its blue palette and compact LMS/ADMIN PORTAL brand are scoped to the Admin host; displayed role/name come from the authenticated session. Do not display service health or unread counts without live source data.
The shared breadcrumb stays at `Hệ thống > Quản trị trung tâm > Không gian làm việc`; each routed screen owns its page breadcrumb. AD-01/02 provide their own page-level breadcrumb in addition to the shell path. AD-02 may refresh its current source-supported API #68 GET query; its available filters remain keyword, role, status and page.
Recheck each screen's worklog and current server source before adding a caller
or enabling an action.
`features/system` retains the readiness component source but it is not mounted
in the route table; `/` is SH-01 in the canonical `shared` group. SH-01 uses
independent #05/#06 requests and forwards trimmed search text to GS-02 without
calling #07 from the landing page. Its local browser route rendered on desktop
and mobile; the development API proxy returned 502 for both data regions, so
live API/DB and published-data states remain unverified. The
Admin route has no router guard; `AdminLayout` gates screen content on its
in-memory session and the API wrapper requires a token before protected reads.
The shared registry in
`src/app/core/constant/api.constants.ts` defines API IDs #1–#103 from the
endpoint catalog and source-only refresh route R-X01. `StudyApiService`
consumes these typed descriptors through the local `/api/v1` transport and rejects entries marked
`UNWIRED`; `WIRED` means an exact current server route source match, not a
deployment check. API #2 is marked `STUB` because its default provider accepts
requests without sending email. Admin login/read callsites are implemented for
the source-backed subset; Admin refresh is source-only R-X01, and no token is
persisted. Shared/Auth currently includes SH01 at `/`, SH02 at `/login`, SH03
at `/register`, and static SH04 at `/register/verification`. SH-02
submit/session remains disabled. SH-03 calls API #01 through
`StudyApiService`; its user-initiated SH04 link carries no ID/email and does
not call API #02. SH05 is not wired; route/error-context, Shared/Student
session/recovery, safe-return and production UI decisions remain blocked. SH06
is the explicit generic `/not-found` page plus unknown-route and #08 detail-404
handoffs; 500 and #09 curriculum-404 remain separate. SH07 exposes the
`/operations/:operationId` gate without calling API #18. Focused SH-01/route,
SH-03 and SH-04 tests and a production build pass; browser production
routing/deployment remain unverified. Recheck the source tree for each task
and do not infer feature behavior from design files or older snapshots.

[`../../web-study/design.md`](../../web-study/design.md) is the intended visual,
interaction and accessibility target. The app architecture is documented in
[`../../../apps/study-client/gui/architech.md`](../../../apps/study-client/gui/architech.md).
Neither document establishes that a business screen or behavior exists at
runtime.
