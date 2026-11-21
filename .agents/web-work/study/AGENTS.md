# Study Web context router

Companion screen and API map: [INDEX.md](INDEX.md).

Current Shared screen update (2026-11-21): SH-02–SH-07 are source-wired to the approved scoped behavior and score 100% under the static UI/UX/logic/API rubric; browser/live API/deployment remain unverified. SH-02 uses API #03 HTTP 200 `LoginData` and role-home routing with no `returnTo`; SH-03 uses API #01 plus a one-use handoff; SH-04 uses API #02's accepted stub only. SH-05 retries only Student #04 once after R-X01 on 401, skips refresh on 403, and has safe internal back or `/` fallback. SH-06 is a minimal 404 with `/courses` and `/` links. SH-07 is notification-only: API #18 UUID owner-bound lookup, manual refresh, producers ME-14/#63 and AD-20/#93, with Admin recipients selected via #68. API #63 `content` is text. This current status supersedes older Shared-screen blocker notes below; generic API #18 lifecycle/results remain out of scope.

```text
CONTEXT_STATUS: VERIFIED_WITH_UNWIRED_COMPONENTS
GS07_SOURCE_STATUS: `/resources/:resourceId` consumes the ID and calls #12. PUBLIC resources use validated direct HTTP(S); PRIVATE resources require Student Bearer, a published parent course, ACTIVE enrollment and a 300-second signed URL. MIME-specific preview and expiry UX are incomplete; runtime is unverified.
SOURCE_STATUS: Angular 22 SPA routes `/` to Shared SH-01 with independent API #05/#06 callers and search handoff, SH-02 presentation at /login, SH-03 API #01 registration caller at /register, partial Guest GS-01–GS-03 at /courses, /courses/search and /courses/:courseId (#05–#08 callers); GS03 owns the `?tab=curriculum|reviews|resources` panels. The app root wildcard redirects unknown routes to SH-06 and clears the original path/query; GS-03 #08 detail 404 also routes to SH-06, while #08 500 and #09 curriculum 404 stay separate. #09 and #10 load lazily after #08 succeeds; GS06 calls #11 after #08 published-course success, validates and renders PUBLIC Resource[] (ID ascending; valid empty is 200 []). Selecting an item opens GS07/#12. T041 approves PUBLIC/PRIVATE access: PRIVATE requires Student Bearer, published parent, ACTIVE enrollment and a signed URL with 300-second TTL. No Study writer for resources was found (#47 writes lesson_uploads); live schema/storage/runtime and MIME-specific preview remain open. AD-01 through AD-25 and ST-11 through ST-26; ST-26 calls #43–#45 for notification list/read actions and recovers an out-of-range page or steps back on a COUNT/LIST empty-positive-total race; deep links and screenshot-only panels remain unsupported and the #45 response discrepancy remains open. ME-02 is source-wired at `/mentor/courses` and calls #46 with response validation, stale-request cancellation, pagination recovery and source-backed course cards; direct-owner scope still differs from AC-21 assignment expectations. Other Mentor screens have individual source-backed callers documented in the Study Web index, while unsupported actions remain gated. SH-01/GS-01 loaded catalog states and GS-03/GS05/GS06 presentations remain partial or derived where their DD assets do not specify runtime states. Enrollment remains open. Focused Study Web tests and local stub-backed browser renders are recorded per continuation; live API/DB runtime remains unverified. `admin.routes.ts` maps AD-01
through AD-25 beneath `AdminLayout`. Nineteen screen-level data-access callers
use fourteen distinct source-backed Admin GET APIs through `AdminApiService`.
`AdminSessionService` authenticates with API #3, refreshes through source-only
route R-X01, keeps credentials in tab memory only, and accepts only the
`ADMIN` role; API #4 and browser storage are not used. `AdminApiService` attaches
Bearer credentials and clears the local session on protected 401 responses.
The server-side Admin guard remains authoritative; this client wiring does not
prove deployment or API acceptance. AD-01 and AD-24/25 have no current report
sources; APIs #99–#103 are absent. API #18 has a backend route and the Study
client uses it for the approved notification-only SH-07 status read; generic
lifecycle/result behavior remains incomplete. Mutation
controls remain disabled where request, permission,
transition, deletion, moderation, delivery, report or export policy is open.
AD-01 and AD-02 also have page-specific layouts: AD-01's `/admin` route,
AdminLayout session gate and safe unavailable-data page are source-wired; its
dashboard data source is absent because API #101 is not implemented. AD-02
reads users through API #68 and maps
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
at `/register`, and SH04 at `/register/verification`. SH-02 calls API #03
once, validates HTTP 200 `DESIGN_RESOURCE_RETRIEVED` with `LoginData`, writes
the matching in-memory role session, calls #04 only for Student verification,
and routes to the role home without `returnTo`. SH-03 calls API #01 through
`StudyApiService`; after a validated 201 it offers an explicit continuation
and transfers positive JS-safe `id`/email once through an in-memory handoff.
SH-04 consumes that handoff and calls API #02 only after a separate user click;
the default provider is a stub and does not send/verify email. Refresh/direct
entry loses the handoff; live delivery, account lifecycle and browser runtime
remain unverified. SH05 is source-wired at `/forbidden`; `StudentApiService`
routes exact API #04 401/403 authorization envelopes with normalized history
state, and SH-05 offers login only for a validated 401 handoff. For exact #04,
server 401 triggers one R-X01 refresh and one retry; 403 skips refresh. Safe
return is internal-only with `/` fallback. SH06 is the generic `/not-found`
page plus unknown-route and #08 404 handoffs; 500 remains separate. SH07 calls
owner-bound API #18 for notification operations only, loads on entry and manual
refresh, and is linked from ME-14/#63 and AD-20/#93 (recipients from #68).
Focused screen/API tests pass. Full build is blocked by unrelated dirty
GS-06/GS-07/ME-04 source/template issues. Browser, live API/DB and deployment
remain unverified.
Recheck the source tree for each task
and do not infer feature behavior from design files or older snapshots.

[`../../web-study/design.md`](../../web-study/design.md) is the intended visual,
interaction and accessibility target. The app architecture is documented in
[`../../../apps/study-client/gui/architech.md`](../../../apps/study-client/gui/architech.md).
Neither document establishes that a business screen or behavior exists at
runtime.
