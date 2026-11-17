# Study Web context index

## Current source status

GS-07 is now source-wired at the root route `/resources/:resourceId` to a
contract-blocked gate only. The page does not consume the route ID or call API
#12; access, URL, preview/download behavior and runtime remain unresolved.

`apps/study-client/` contains an Angular 22 standalone SPA with Shared SH-01 at
`/` using APIs #05/#06, presentation-only SH-02 at `/login`, SH-03 registration at
`/register` with its API #01 caller, and partial Guest GS-01–GS-03 routes at
`/courses`, `/courses/search` and `/courses/:courseId`; GS03 owns the
`?tab=curriculum` view and lazy #09 caller; AD-01 through AD-25
routes are under `/admin`. The routes use lazy-loaded groups and shared
layouts. The former root readiness component remains in source but is no longer
mounted. SH-01 has independent category/course states, informational category
labels, non-clickable course cards and trimmed search handoff to GS-02; its
desktop/mobile local browser route rendered while the dev API proxy returned
502, so live API/DB data remains unverified. Nineteen Admin screen-level callers use fourteen distinct
source-backed GET APIs through `AdminApiService`. `AdminSessionService` uses
API #3 and source-only refresh route R-X01, keeps credentials in tab memory,
and requires the `ADMIN` role; no token persistence or API #4 call is present.
The API wrapper attaches Bearer credentials and ends the local session on
protected 401. AD-01 and AD-24/25 remain unavailable because their current
report/export sources are absent. AD-01 has its own page layout but its dashboard
data is unavailable because API #101 has no local source. AD-02 has its own
#68-backed user list and exposes only the source-supported keyword, role, status
and page filters. Unsupported mutation controls remain disabled. AD-01 through
AD-25 use page-specific layouts; no routed Admin page imports
`AdminScreenSurface` (its only Admin import is in its own unit spec).
AD-04/05/06/08/09/10/12/14/15/16/17/18/19/20/21/22/23/24 have host-scoped page stylesheets; AD-07/13 share a host-scoped detail stylesheet registered in Angular. AD-01 retains component-scoped page styles. AD-02 keeps heading/filter styles in its component CSS and uses `study-ad02-page`-prefixed global CSS for table/empty states. `src/styles.css` provides the Admin-scoped `.page-width` container (AD-01 is 1540px at desktop; other pages are 1520px; tablet/mobile widths are shared). `AdminLayout` uses five primary navigation groups, routes notifications from its bell control, scopes the blue LMS shell palette to the Admin host, and keeps a stable workspace breadcrumb; identity comes from the authenticated profile and no service-health/unread state is inferred. AD-01/02 provide their page-specific breadcrumbs. AD-02 filters and refreshes through source-backed API #68 only. Admin routes and
nav provide presentation navigation, not server authorization. Local source
confirms API #68–#98 route behavior. API #18 has a source-backed backend route
and notification-only query; its client descriptor remains `UNWIRED`, and
generic operation lifecycle/result handling is incomplete. APIs #99–#103 remain
absent. Production API acceptance and deployment remain
unverified.
The Shared group wires SH01Page at `/`, SH02Page at `/login`, SH03Page at
`/register`, SH04Page at `/register/verification`, SH06Page at
`/not-found` and SH07Page at `/operations/:operationId`. SH-01 calls #05/#06
independently; category filtering and course card navigation remain blocked by
unresolved contracts/design.
SH-02 remains presentation-only with login/session submit disabled. SH-03 calls
API #01 through `StudyApiService`; a validated 201 shows account-created
status and a user-controlled link to SH-04. SH-04 is a static information gate
that links back to SH-02; it receives no registration ID/email and does not call
API #02 or claim that an email was sent or verified. API #02, account lifecycle,
feature gate and handoff transport remain unresolved. SH-06 has an explicit
`/not-found` route; the root wildcard redirects unknown Angular routes there
with the original path/query cleared, and GS-03 #08 detail 404 uses the same
generic state. #08 500 and #09 curriculum 404 remain separate; static-host
rewriting and blocked SH-06 prototype sections remain unresolved.
SH-07 has a direct `/operations/:operationId` route with an accessible
unavailable gate only; it does not display the path segment or call API #18.
Generic operation tracking remains blocked by the unresolved API #18 and
producer contracts.
Focused SH-01/route/SH-03 tests and production build
pass; local SH-01 route rendering was verified in desktop/mobile headless
browsers, while live API/DB and production runtime remain unverified.
The typed registry in `src/app/core/constant/api.constants.ts` defines catalog
APIs #1–#103 and source-only route R-X01. `StudyApiService` in
`src/app/core/http/` consumes those descriptors through the local `/api/v1`
proxy and rejects `UNWIRED` entries. `WIRED` records an exact route-source
match and does not verify deployment; API #2 is an email-delivery stub. Check
current source for each screen task.

Guest source wires GS-01 to #05/#06, GS-02 to #07 and GS-03 to #08. GS-07
is source-wired to a contract-blocked gate only; resource details/actions
remain `DD BLOCKED` and browser/deployment runtime is unverified. GS-01
category chips expose #05 metadata only because #06 rejects a category filter.
GS-01 loaded states and the GS-03 loaded overview/curriculum presentation are
derived; DD visual approval and browser/live API/DB runtime remain unverified.
GS-05 public review reads are source-wired through API #10 after GS03
confirms a published course. GS-06 is now mounted at `?tab=resources` after
the same #08 published-course check and shows only a contract-blocked status;
it deliberately sends no #11/#12 requests and exposes no resource actions.
API #11 has local route/module/query/test source but returns only the first
resource row as a singleton; the collection contract conflicts with its Draft
DD. API #12 remains a public direct-URL read without visibility/access checks
or a signer. Student and Mentor route groups are present. Enrollment, resource,
and individual Mentor action gates still reflect their source contracts.
GS-05/GS-06 contract approval and live schema/deployment are unresolved.

`src/app/core/localStorage/local-storage.service.ts` provides generic JSON
read/write operations for browser `localStorage`; it has no feature caller and
does not integrate auth tokens.

## Pages

| Topic | Page | Authority |
|---|---|---|
| Shared Study API registry, HTTP transport and envelope | `src/app/core/constant/api.constants.ts`, `src/app/core/http/study-api.service.ts`, `src/app/core/http/api-envelope.ts`, `proxy.conf.json` | 103 catalog descriptors plus source-only R-X01; transport rejects `UNWIRED`; Admin callsites cover 14 source-backed GET API IDs, while production routing remains unverified. |
| Generic browser storage | `src/app/core/localStorage/local-storage.service.ts` | JSON set/get utility; no feature caller or auth token integration. |
| Guest catalog, search, detail, curriculum, reviews and resources-gate source | `src/app/features/guest/guest.route.ts`, `GS01/`, `GS02/`, `GS03/`, `GS05/`, `GS06/`, `GS07/`, `shared/` | GS-01 #05/#06, GS-02 #07, GS-03 #08, GS04 curriculum panel/#09, GS05 reviews/#10, GS06 gated resources and GS07 contract-blocked root route are source-wired. GS07 does not consume its ID or call #12. GS03 owns `tab=curriculum|reviews|resources`; #09/#10 load lazily after #08 success, while GS06 makes no #11/#12 call. API #11 current singleton/first-row source conflicts with its Draft collection use; API #12 is public/direct-URL without resource access checks. Category filtering, enrollment and API #10/#11/#12 contract approval remain open; loaded projections are partial/derived, and live runtime is unverified. |
| Admin session and authenticated GET transport | `src/app/core/auth/admin-session.service.ts`, `src/app/core/http/admin-api.service.ts`, `src/app/layouts/admin/` | Login API #3, source-only R-X01 refresh, tab-memory-only token pair, ADMIN-role check, Bearer GET calls and 401 local-session clearing. No persistent token storage. |
| Study screen inventory and screen/API traceability | [`list_screen.md`](../../../apps/study-client/docs/list_screen.md) | Screen IDs, routes, API references and design/gate context; not proof of implemented UI. |
| Study endpoint catalog | [`list_endpoint.md`](../../../apps/study-client/docs/list_endpoint.md) | API IDs, method/path and design I/O for 103 endpoints; not proof of runtime wiring. |
| Mandatory frontend layer, UI/business, and dependency rules | [`../../web-study/frontend-rules.md`](../../web-study/frontend-rules.md) | Required for Study Web coding/fix/test/review and architecture-document tasks. |
| Screen folder, route and layout structure | [`../../web-study/frontend-rules.md`](../../web-study/frontend-rules.md) | Target structure: shared/auth/system, guest, student, mentor, admin groups; four direct folders per screen. |
| Screen implementation, DD analysis, demo and fixture cleanup | [`workflows/screen-implementation.md`](workflows/screen-implementation.md) | Registered workflow `study-web-screen-coding`; required for individual screen coding/fix/test/demo. |
| Visual, interaction and accessibility target | [`../../web-study/design.md`](../../web-study/design.md) | Intended design only; not runtime evidence. |
| Angular folders, file responsibilities, and boundaries | [`../../../apps/study-client/gui/architech.md`](../../../apps/study-client/gui/architech.md) | Current scaffold and planned feature structure; no business behavior. |
| Admin screen surfaces and API callers | `src/app/features/admin/AD01/` through `AD25/`, `src/app/shared/ui/admin-screen-surface.*`, `admin-detail-page.css` | All 25 catalog routes have page surfaces; 19 callers cover 14 source-backed GET APIs. AD-03, AD-04, AD-05, AD-06, AD-07, AD-08, AD-09, AD-10, AD-11, AD-12, AD-13, AD-14, AD-15, AD-16, AD-17, AD-18, AD-19, AD-20, AD-21, AD-22, AD-23, AD-24 and AD-25 have custom layouts. AD-04/05/06/08/09/10/12/14/15/16/17/18/19/20/21/22/23/24 page styles and shared AD-07/13 detail styles are host-scoped and registered in Angular. AD-04 reads the #69 UserProfile, keeps profile controls and #70 Save disabled because body, role/PII and permission policy remain open, omits unsupported adminNotes and keeps role/status values literal. AD-05 reads #69 and keeps #71/#72 actions and the reason field disabled because status/session, deletion/retention, permission and audit policy remain open. AD-08 reads #74 and keeps title/description/price edits local, exposes source-only thumbnail/mentor/status, and leaves #75 save/upload unavailable; screenshot-only identifiers, counts and readiness claims are omitted. AD-09 reads #74, preserves the route ID for AD-07 navigation, and keeps #76/#77 actions disabled while request and lifecycle policy remain open. AD-10 maps #78's exact `type/course/page` query; AD-12 displays #82 lesson fields and links safe numeric IDs to AD-13; AD-13 reads the #83 Lesson projection, renders its seven fields without fabricating dependencies/counts or embedding video, and keeps the AD-14 action disabled. AD-14 also loads #83, keeps title/content/order drafts local, and leaves #84–#86 mutations gated by current contract gaps; AD-15 maps #87's `course/status/page` query and omits the placeholder question count; AD-16 allows create-mode fields as in-memory drafts, disables edit fields because no Quiz detail GET exists, and keeps question creation/save locked under the #88/#89 contract gaps; AD-17 displays the current local #91 DTO with a visible catalog/DTO mismatch notice and precision-safe int64 formatting; AD-18 displays the raw route ID in a read-only page, has no detail preview source and keeps delete/reason controls disabled; AD-15 links only positive safe Quiz IDs to AD-18, which returns to AD-15; focused specs pass, but browser runtime is not verified. AD-19 maps #92's `status/channel/page` query and displays delivery-backed notification fields; AD-20 provides a local-only title/content preview and keeps recipient/channel/send gates closed because #93/#18 remain unresolved; AD-21 reads the exact #96 status projection and leaves #94/#95 unavailable; AD-22 maps #97's exact `reason/severity/page` filters and unique Discussion projection; AD-23 reads #98's direct-child comments and keeps #99/#100 unavailable; AD-24 has no #101/#102 source, so filters, metrics, charts and export remain unavailable. Missing API sources and unresolved actions remain unavailable/disabled. |
| Skill-formatted screen DD packages | [`../../../apps/study-client/docs/dd_screens/screen-index.md`](../../../apps/study-client/docs/dd_screens/screen-index.md) | 83 source-derived packages; route/API status stays per screen, and the packages do not prove runtime wiring. |

For every Study FE task, follow the mandatory scope preflight in
[`AGENTS.md`](AGENTS.md): read both catalogs, identify the affected screen/API
IDs, and record them in the task worklog. Use `screen-index.md` to locate
relevant screen DD packages and each endpoint row's Overview link to locate
Study API DD. Treat catalogs, screen DDs, and API DDs as design evidence; check
current source when describing runtime behavior. Screen assets in
[`screen_stitch/`](../../../apps/study-client/docs/screen_stitch/) are visual
references and do not establish runtime behavior.

The canonical four-folder screen structure is implemented for the current
Admin screen set, partially for Guest GS-01–GS-03, and present for GS-05
reviews and GS-06/GS-07 gated presentations. Placeholder directories do not prove
that remaining screens, layouts, routes or modules exist.

Student routes ST-01–ST-26 now use the StudentLayout session from API #03;
tokens remain in tab memory and protected requests use the Student Bearer
wrapper. ST-02 is a #04 profile gate; ST-03 is a #04/#13/#14 contract gate.
ST-04 calls public #08 but keeps unsafe #15 uncalled. ST-05 calls #08 but keeps
#16 uncalled because its descriptor is UNWIRED and checked-in DDL lacks
`orders`. ST-06/ST-07 keep payment/result behavior gated. ST-01 calls #20/#38;
ST-08 calls paged #20; ST-09 checks ACTIVE enrollment via #20 before #37 and
does not use public #09 as a private learning tree. ST-10 calls #22 on entry
and explicit #23 only after `PUBLISHED`; ST-11 calls #24 after handoff. #21
returns UserProfile rather than progress; #43–#45 remain SOURCE_ONLY due to a
missing checked-in `notification_recipients` relation. ST-11–ST-25 have
screen-local callers for source-supported behavior; unsupported actions stay
gated. Mentor routes and screen-local callers exist, with individual actions
gated where source contracts do not support the DD. Do not infer authorization
from route metadata; live API/schema/browser runtime remains unverified.
