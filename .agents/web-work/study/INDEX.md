# Study Web context index

## Current Shared screen status — 2026-11-21

SH-02–SH-07 are source-wired to the approved scope and score 100% under the
static UI/UX/logic/API rubric. SH-02 uses API #03 HTTP 200 `LoginData` and
role-home routing; SH-03 uses API #01 and a one-use SH-04 handoff; SH-04 uses
only API #02 accepted-stub semantics; SH-05 performs one #04 refresh/replay on
401 and skips refresh on 403; SH-06 is the minimal 404; SH-07 reads
notification-only API #18 status by UUID with owner-bound access and manual
refresh. ME-14/#63 and AD-20/#93 route accepted operation UUIDs to SH-07, with
AD-20 recipients selected through #68. API #63 content is text. Focused Study
Web tests pass 36/36; browser, live API/DB and deployment remain unverified.
Older task snapshots below are historical where they disagree with this
current status; generic API #18 lifecycle/results remain out of scope.

## Current Mentor screen status — 2026-11-21

ME-01–ME-18 score 100% under the static DD-safe rubric: source-backed UI/UX,
states and API caller mapping are complete, with unsupported behavior visibly
limited or gated. Focused Mentor verification passes 6 spec files / 12 tests.
ME-01 validates #46/#54/#58 independently and previews four rows per widget;
#54 uses its fixed 20-row page without an unsupported `size` query. ME-04's
template compiles. ME-14 consumes the ME-13 history handoff once, validates
#63's accepted 202 Operation UUID before SH-07 navigation, and blocks blind
resend after an ambiguous outcome because #63 has no idempotency key. #63 has
no `course_id`, so the exact selected course cannot be bound server-side.
Source/contract gaps for content mutations, grading, support resolution,
notification delivery, and richer analytics remain gated. The focused Admin
suite now passes 25 spec files / 99 tests. Production build compiles templates
and is blocked only by the out-of-scope ST03 component CSS budget; AD16 and
AD20 have no component-style budget errors. The initial bundle remains over
its warning threshold. An authenticated browser fixture, live API/DB,
migration deployment and production runtime remain unavailable.

## Current source status

SH-03 calls API #01 and, after validating a successful registration result,
offers a user-controlled transition to SH-04 with a one-use in-memory
`id/email` handoff. SH-04 consumes the handoff and calls public API #02 only
after a separate explicit click. Its accepted state requires HTTP 202,
`DESIGN_OPERATION_ACCEPTED` and `data.status="accepted"`. API #02's default
provider is a stub: it sends no email and verifies no account. The handoff is
lost on reload/direct entry; delivery, account lifecycle, safe-integer vs
int64 contract and browser runtime remain open. Payment on ST-06 remains
blocked pending a backend-owned checkout URL/return contract.

GS-06 calls #11 after GS-03 confirms a published course; the current route
returns PUBLIC `Resource[]` ordered by ID and an empty array for a valid course
with no public resources. GS-07 calls #12 with the resource ID. PUBLIC resources
use a validated direct HTTP(S) URL; PRIVATE resources require a Student Bearer,
published parent course, ACTIVE enrollment and a 300-second signed URL. T041
approved PUBLIC/PRIVATE visibility and defaults existing rows to PRIVATE.
Current gaps: no Study writer for `resources` was found (#47 writes
`lesson_uploads`), GS-07 has no MIME-specific preview/expiry UI, response IDs
are limited by JavaScript safe-integer representation, and live runtime is
unverified.

`apps/study-client/` contains an Angular 22 standalone SPA with Shared SH-01 at
`/` using APIs #05/#06, source-wired SH-02 at `/login`, SH-03 registration at
`/register` with its API #01 caller, and Guest GS-01–GS-03 routes at
`/courses`, `/courses/search` and `/courses/:courseId`; GS03 owns the
`?tab=curriculum|reviews|resources` tabs and lazy #09/#10/#11 callers, while
GS-06 item selection opens the GS-07 `/resources/:resourceId` route for #12; AD-01 through AD-25
routes are under `/admin`. The routes use lazy-loaded groups and shared
layouts. The former root readiness component remains in source but is no longer
mounted. SH-01 has independent category/course states, informational category
labels, non-clickable published-course cards, trimmed search handoff to GS-02,
existing route links, hidden price until currency is defined, accessible loading
skeletons, keyboard skip link and minimal footer under the approved DD-safe
scope. Its #05/#06 readers validate the success envelope, item/mentor
projections and current pagination; malformed data enters the region error/retry
state. The focused SH-01 spec passes 7/7 and an isolated Angular build of the
current SH-01 component passes. GS-01–GS-07 follow the DD-safe source-backed
scope; focused Guest tests pass 37/37 and API #11/#12 fake-source tests pass
27/27. The full production build compiles Angular templates but is blocked by
the out-of-scope ST03 component CSS budget; the initial bundle also exceeds its
warning threshold. AD16/AD20 have no component-style budget errors. Browser
runtime and live API/DB remain unverified.
Twenty-three Admin screen-level callsites cover sixteen source-backed APIs through
`AdminApiService`: twenty-one GET callsites across fourteen GET APIs and two POST callsites (#88 and #93). `AdminSessionService` uses
API #3 and source-only refresh route R-X01, keeps credentials in tab memory,
and requires the `ADMIN` role; no token persistence or API #4 call is present.
The API wrapper attaches Bearer credentials and ends the local session on
protected 401. `postWithResponse` preserves HTTP status for #88/#93; AD-16
requires 201 and AD-20 requires 202 before showing success or navigating.
AD-01–AD-25 are 100% complete under the static DD-safe
UI/UX/state/logic/API mapping rubric; unsupported writes, reports, campaigns
and exports remain unavailable or disabled. This score does not imply
product-contract or runtime completion. The focused Admin suite passes 25 spec
files / 99 tests. AD-01 route/layout/page and its safe unavailable-data states
are source-wired; dashboard metrics remain unavailable because API #101 has no
local source. AD-24/25 routes/pages also exist, but their report/export data
sources are absent. AD-02 has its own
#68-backed user list and exposes only the source-supported keyword, role, status
and page filters. Its row renderer localizes known ACTIVE/SUSPENDED/DELETED
values while preserving exact-string filter values; unknown statuses use a
neutral label. User int64 IDs use precision-safe display, and only positive JavaScript safe-integer values link to AD-03 and expose the AD-04 edit / AD-05 account-action routes in the seventh table column. Those are navigation handoffs only; mutation controls remain gated in their destination screens. AD-03 keeps edit/status action buttons disabled while permission and mutation contracts are open, and labels its #69 badge from loading/loaded/error state. Create/export/help controls are visible but disabled, and role/status filters remain exact-string inputs because the complete option sets are not source-confirmed. AD-01 through
AD-25 use page-specific layouts; no routed Admin page imports
`AdminScreenSurface` (its only Admin import is in its own unit spec).
AD-04/05/06/08/09/10/12/14/15/16/17/18/19/20/21/22/23/24 have host-prefixed page stylesheets registered globally in Angular; AD-07/13 share a host-scoped detail stylesheet registered in Angular. AD-01 retains component-scoped page styles. AD-02 keeps heading/filter styles in its component CSS and uses `study-ad02-page`-prefixed global CSS for table/empty states. `src/styles.css` provides the Admin-scoped `.page-width` container (AD-01 is 1540px at desktop; other pages are 1520px; tablet/mobile widths are shared). `AdminLayout` uses five primary navigation groups, routes notifications from its bell control, scopes the blue LMS shell palette to the Admin host, and keeps a stable workspace breadcrumb; identity comes from the authenticated profile and no service-health/unread state is inferred. AD-01/02 provide their page-specific breadcrumbs. AD-02 filters and refreshes through source-backed API #68 only; its client validates the exact success code/UserProfile Page/pagination, preserves rows on separate COUNT/LIST mismatch, hides stale totals/paging, retries the applied URL query and recovers empty out-of-range pages. Admin routes and
nav provide presentation navigation, not server authorization. Local source
confirms API #68–#98 route behavior. API #18 has a source-backed, client-wired
notification-only query; generic operation lifecycle/result handling is incomplete. APIs #99–#103 remain
absent. Production API acceptance and deployment remain
unverified.
The Shared group wires SH01Page at `/`, SH02Page at `/login`, SH03Page at
`/register`, SH04Page at `/register/verification`, SH05Page at `/forbidden`,
SH06Page at `/not-found` and SH07Page at `/operations/:operationId`. SH-01 calls #05/#06
independently; under the approved DD-safe behavior categories are informational
and course cards are non-clickable. “Xem tất cả” opens GS-01, the hero search
hands trimmed q to GS-02, and the registration CTA opens SH-03. The screen score
is 100% under the four-axis repository rubric; live API/DB and current-session
browser rendering remain unverified.
SH-02 calls #03 once through `SH02LoginService`, accepts only HTTP 200
`DESIGN_RESOURCE_RETRIEVED` with `LoginData`, stores the response in the
role-specific in-memory session, and navigates to `/student`, `/mentor` or
`/admin`. Student alone calls #04. There is no `returnTo` or persistent token
storage; the catalog/DD is reconciled to the current server contract. SH-03
calls API #01 through `StudyApiService`; a validated 201 shows account-created
status and an explicit one-use in-memory handoff to SH-04. SH-04 consumes the
validated registration ID/email and calls API #02 after a separate user action;
the default stub does not send email or verify the account. Focused tests pass;
account lifecycle, live delivery and deployment remain unverified.
SH-06 has an explicit
`/not-found` route; the root wildcard redirects unknown Angular routes there
with the original path/query cleared, and GS-03 #08 detail 404 uses the same
generic state. #08 500 and #09 curriculum 404 remain separate; static-host
rewriting and blocked SH-06 prototype sections remain unresolved.
ST-02 and ST-03 call API #04 through `StudentApiService`; #04 401 triggers one
R-X01 refresh and one #04 retry, while 403 skips refresh. Final 401 clears the
session and routes to SH-05; safe return is internal-only with `/` fallback.
SH-06 is the minimal generic 404 with `/courses` and `/` links, unknown-route
and #08 404 handoffs; #08 500 stays separate. SH-07 validates a producer UUID,
calls owner-bound API #18 for notification status only, and supports initial
load plus manual refresh. ME-14/#63 and AD-20/#93 hand off their accepted
operation UUIDs; AD-20 recipient selection uses API #68. No polling or payment/
export results are implemented. The SH-02–SH-07 four-axis static score is 100%;
browser, live API/DB and production deployment are unverified.
The 2026-11-21 SH-01 focused spec passes 7/7 and an isolated Angular build
passes. Focused GS-01–GS-07 specs pass 37/37; local API #11/#12 fake-source
tests pass 27/27. The production Study Web build compiles templates but stops
at the out-of-scope ST03 component CSS budget; AD16 and AD20 now pass their component CSS budgets. Current browser
rendering and live API/DB/deployment remain unverified. A prior desktop/mobile
route demo was recorded on 2026-11-17.
The typed registry in `src/app/core/constant/api.constants.ts` defines catalog
APIs #1–#103 and source-only route R-X01. `StudyApiService` in
`src/app/core/http/` consumes those descriptors through the local `/api/v1`
proxy and rejects `UNWIRED` entries. `WIRED` records an exact route-source
match and does not verify deployment; API #2 is an email-delivery stub. Check
current source for each screen task.

Guest source wires GS-01 to #05/#06, GS-02 to #07, GS-03 to #08 and lazy
tab callers #09/#10/#11, GS-06 to #11 and GS-07 to #12. GS-01 category chips
expose #05 metadata only because #06 rejects a category filter. GS-01 validates
the #05/#06 success envelope, item projections, PUBLISHED status and
pagination; it cancels stale requests. Since #06 COUNT and LIST are separate
reads, it preserves returned courses and offers retry while suppressing totals
and page controls when cardinality differs. GS-02 receives GS-01's trimmed
search handoff, validates #07 course pages and PUBLISHED status, cancels stale
searches, and links result cards to GS-03 by response ID. COUNT/LIST mismatch
preserves rows, hides totals/paging and offers retry; error and out-of-range
states provide recovery. GS-03 validates #08 singleton course data and signed
int64 route strings, lazy-loads #09/#10/#11 after #08 confirms PUBLISHED, and
offers retry on detail and curriculum failures. The GS-04 panel displays only
validated lesson title/order sorted by order; preview/access remain gated. GS-05
validates #10 page/review/author/reply projections and ACTIVE status, displays
content/authors/replies/paging, preserves rows on count/list mismatch, retries
errors, and renders no title or rating. GS-06 validates #11 PUBLIC `Resource[]`
and links each ID to GS-07 with course return context; empty `200 []` is distinct
from error. GS-07 validates #12 identity/projection/HTTP(S) URL, distinguishes
401/403/404, retries transient failures, and opens only the authorized URL.
PRIVATE resources use Student Bearer + published course + ACTIVE enrollment and
a 300-second URL. Category filters, enrollment, price formatting, lesson/MIME
preview and rating remain gated. Focused GS specs pass 37/37 and #11/#12 local
fake-source tests pass 27/27. Browser/live API/DB runtime remains unverified.
unresolved. GS-06 is mounted at `?tab=resources` after the
same #08 check and calls #11; T041-approved behavior returns PUBLIC `Resource[]`
in ascending ID order and `200 []` when empty. Selecting a row opens GS-07;
#12 returns a direct URL for PUBLIC resources and applies Student/ACTIVE
enrollment checks plus 300-second signing for PRIVATE resources. No Study
writer for `resources` was found (#47 writes `lesson_uploads`), and live
schema/runtime remain unverified. Student and Mentor route groups are present.
Enrollment and individual Mentor action gates still reflect their source contracts. ME-13
is registered and reads #46/#62 with strict response checks and stale-request
cancellation; clearing a course cancels the roster read without issuing an
empty #62 path. Its Continue gate verifies the selected course is still on the
validated #46 page and every recipient belongs to the loaded #62 roster.
Optional #62 avatars use HTTPS/same-origin HTTP, `no-referrer` and initials
fallback. ME-13 passes selected course and recipients to ME-14 through router
state. ME-14 validates unique int64-safe handoff IDs, previews text, requires
explicit `PUSH`/`EMAIL` channel selection, posts through #63, and routes the
accepted UUID to SH-07. Draft state remains page-local; #63 has no `course_id`,
so it cannot bind dispatch to the exact selected course. Provider delivery and
browser/runtime behavior are unverified. ME-15 is also source-wired to #64: it follows the notification
route ID reactively, validates the exact Operation projection and keeps the
returned Operation UUID separate; it does not poll or infer batch status. The
#63-to-ME-15 ID selection remains unresolved.
ME-16 is source-wired to #65 and validates the local unpaginated
Student-progress Page, cancels stale course reads, safely renders optional
Student avatars with initials fallback, and links validated Student IDs to ME-17. The catalog's `Page<Course>` response still conflicts with the
local #65 `Page<MentorStudentProgress>` response; filters, timeline/risk data,
roster-size limits and runtime remain unresolved. ME-17 is source-wired to #67
with reactive course/Student IDs, stale-request cancellation, lesson/summary
validation, safe optional Student avatars and a guarded return to ME-16. Its local singular
`StudentCourseProgress` still conflicts with the catalog `Page<Course>` shape;
loaded event timelines and assignment/quiz metrics remain unavailable.
ME-18 is source-wired to #66 with reactive course IDs, stale-request
cancellation and strict local summary/count/timestamp consistency validation. It renders only timestamped
Student/lesson proxy counts and latest access, not event history, active
enrollment, completion rate or ETL health; catalog response/metric and AC-26
ordering gaps remain open.
ME-16 is source-wired to #65 and validates the local unpaginated
Student-progress Page, cancels stale course reads, and links validated Student
IDs to ME-17. The catalog's `Page<Course>` response still conflicts with the
local #65 `Page<MentorStudentProgress>` response; filters, timeline/risk data,
roster-size limits and runtime remain unresolved.
GS-05 contract approval remains open; GS-06/GS-07 resource policy is approved and source-wired, while resource-table schema/data availability and live deployment remain unverified.

`src/app/core/localStorage/local-storage.service.ts` provides generic JSON
read/write operations for browser `localStorage`; it has no feature caller and
does not integrate auth tokens.

## Pages

| Topic | Page | Authority |
|---|---|---|
| Shared Study API registry, HTTP transport and envelope | `src/app/core/constant/api.constants.ts`, `src/app/core/http/study-api.service.ts`, `src/app/core/http/api-envelope.ts`, `proxy.conf.json` | 103 catalog descriptors plus source-only R-X01; transport rejects `UNWIRED`; Admin callsites cover 14 source-backed GET API IDs, while production routing remains unverified. |
| Generic browser storage | `src/app/core/localStorage/local-storage.service.ts` | JSON set/get utility; no feature caller or auth token integration. |
| Guest catalog, search, detail, curriculum, reviews and resource flows | `src/app/features/guest/guest.route.ts`, `GS01/`, `GS02/`, `GS03/`, `GS05/`, `GS06/`, `GS07/`, `shared/` | GS-01 #05/#06, GS-02 #07, GS-03 #08, GS04 curriculum panel/#09, GS05 reviews/#10, GS06 #11 and GS07 #12 are source-wired. GS03 owns `tab=curriculum|reviews|resources`; #09/#10/#11 load after #08 success. T041 approves #11 PUBLIC `Resource[]` ordered by ID and empty 200; #12 direct URL for PUBLIC, Student Bearer + ACTIVE enrollment + 300-second signed URL for PRIVATE. No Study writer for `resources` was found (#47 writes `lesson_uploads`); resource preview/MIME policy, ID precision and live runtime remain open. Category filtering and enrollment remain separately gated. |
| Student session and protected API #04 handoff | `src/app/core/auth/student-session.service.ts`, `src/app/core/auth/authorization-error.ts`, `src/app/core/http/student-api.service.ts`, Shared SH-05 route/page | In-memory Student credentials, proactive refresh at local expiry, one R-X01 refresh and one #04 retry after 401, no refresh for 403, final 401 session clear and safe internal return target with `/` fallback. Focused tests pass; runtime not verified. |
| Admin session and authenticated GET transport | `src/app/core/auth/admin-session.service.ts`, `src/app/core/http/admin-api.service.ts`, `src/app/layouts/admin/` | Login API #3, source-only R-X01 refresh, tab-memory-only token pair, ADMIN-role check, Bearer GET calls and 401 local-session clearing. No persistent token storage. |
| Study screen inventory and screen/API traceability | [`list_screen.md`](../../../apps/study-client/docs/list_screen.md) | Screen IDs, routes, API references and design/gate context; not proof of implemented UI. |
| Study endpoint catalog | [`list_endpoint.md`](../../../apps/study-client/docs/list_endpoint.md) | API IDs, method/path and design I/O for 103 endpoints; not proof of runtime wiring. |
| Mandatory frontend layer, UI/business, and dependency rules | [`../../web-study/frontend-rules.md`](../../web-study/frontend-rules.md) | Required for Study Web coding/fix/test/review and architecture-document tasks. |
| Screen folder, route and layout structure | [`../../web-study/frontend-rules.md`](../../web-study/frontend-rules.md) | Target structure: shared/auth/system, guest, student, mentor, admin groups; four direct folders per screen. |
| Screen implementation, DD analysis, demo and fixture cleanup | [`workflows/screen-implementation.md`](workflows/screen-implementation.md) | Registered workflow `study-web-screen-coding`; required for individual screen coding/fix/test/demo. |
| Visual, interaction and accessibility target | [`../../web-study/design.md`](../../web-study/design.md) | Intended design only; not runtime evidence. |
| Angular folders, file responsibilities, and boundaries | [`../../../apps/study-client/gui/architech.md`](../../../apps/study-client/gui/architech.md) | Current scaffold and planned feature structure; no business behavior. |
| Admin screen surfaces and API callers | `src/app/features/admin/AD01/` through `AD25/`, `src/app/shared/ui/admin-screen-surface.*`, `admin-detail-page.css` | All 25 catalog routes have page surfaces; source-backed calls include 21 GET callsites across 14 APIs and POST #88 plus #93 create callsites. AD-03, AD-04, AD-05, AD-06, AD-07, AD-08, AD-09, AD-10, AD-11, AD-12, AD-13, AD-14, AD-15, AD-16, AD-17, AD-18, AD-19, AD-20, AD-21, AD-22, AD-23, AD-24 and AD-25 have custom layouts. AD-04/05/06/08/09/10/12/14/15/16/17/18/19/20/21/22/23/24 page styles use host-prefixed global selectors; AD-07/13 share host-scoped detail styles registered in Angular. AD-04 reads the #69 UserProfile, keeps profile controls and #70 Save disabled because body, role/PII and permission policy remain open, omits unsupported adminNotes and keeps role/status values literal. AD-05 localizes only source-backed ACTIVE/SUSPENDED/DELETED status labels for display, keeps role literal, and validates raw signed-int64 userId before GET #69; #71/#72 actions and the reason field remain disabled because status/session, deletion/retention, permission and audit policy remain open. AD-07/08/09 require the exact locally implemented #74 singleton Page<Course> with one validated Course/mentor and pagination 1/1/1/1; AD-08 also validates raw signed-int64 course IDs before GET #74, returns invalid IDs to AD-06, keeps title/description/price edits local, exposes source-only thumbnail/mentor/status, and leaves #75 save/upload unavailable; screenshot-only identifiers, counts and readiness claims are omitted. AD-09 validates raw signed-int64 course IDs before GET #74, returns invalid IDs to AD-06 and valid IDs to AD-07, and keeps #76/#77 actions disabled while request and lifecycle policy remain open. AD-10 is route/page/Admin-API wired to #78 with exact type/course/page; validates the local Content Page projection and pagination, preserves rows on COUNT/LIST mismatch while hiding stale totals/paging, and supports same-page retry plus empty-out-of-range recovery; its queue status displays the query-guaranteed `PENDING_REVIEW` as “Đang chờ duyệt”; manual refresh repeats the applied query without polling, and only safe Content IDs link to AD-11; AD-11 validates raw signed-int64 `contentId` before GET #79 and skips invalid routes; catalog `Content` vs local Page response remains open; AD-12 requires the exact #82 success code and Lesson[] projection, displays Course/Lesson int64 IDs precision-safely, links only safe Lesson IDs to AD-13, applies raw Course ID and repeats/clears the exact query; search/type/status/Add/pagination remain gated; AD-13 validates raw signed-int64 `lessonId` before GET #83, skips invalid routes, renders the seven Lesson fields without fabricating dependencies/counts or embedding video, and keeps the AD-14 action disabled. AD-14 validates raw signed-int64 `lessonId` before GET #83, keeps title/content/order drafts local, and leaves #84–#86 mutations without Web callers and gated by current contract gaps; AD-15 maps #87 course/status/page, validates the local Quiz Page projection/business code/page metadata, preserves rows on COUNT/LIST mismatch while hiding stale totals/paging, and supports same-query retry and empty-out-of-range recovery; AD-06 validates #73 success code/Course Page/pagination, preserves rows on COUNT/LIST mismatch, hides stale totals/page data, retries the same page and recovers empty out-of-range pages; Course links require positive safe-integer IDs; AD-16 loads course options through #73, requires response `pagination.page` to echo the requested page (current server source behavior, including valid out-of-range pages), and submits create-mode config/questions to #88 using the current nested validator shape (`DERIVED`); edit remains locked because no Quiz detail GET exists and #89 catalog omits its body; AD-17 validates raw `quizId` as positive signed-int64 before GET #91, then displays the local DTO with a visible catalog/DTO mismatch notice and precision-safe int64 formatting; AD-18 preserves route ID text, validates positive signed-int64 bounds, announces invalid IDs, has no detail preview source and keeps delete/reason controls disabled; AD-15 links only positive safe Quiz IDs to AD-18, which returns to AD-15; 99 Admin tests pass; authenticated browser runtime is not verified. AD-19 maps #92 status/channel/page, localizes source-defined QUEUED/SENT/FAILED values, preserves rows on COUNT/LIST mismatch while hiding stale totals/paging, supports same-query retry and empty-out-of-range recovery, and displays delivery-backed notification fields; AD-20 loads explicit recipients through #68, submits title/text/channels through #93, validates the accepted operation UUID and routes to SH-07; segment, provider-delivery and live-runtime behavior remain unverified; AD-21 validates raw `notificationId` as positive signed-int64 before #96, reads the exact status projection, and leaves #94/#95 unavailable; AD-22 maps #97's exact `reason/severity/page` filters and unique Discussion projection; manual refresh repeats the applied query without polling; AD-23 validates raw positive signed-int64 route IDs before GET #98, validates the exact Discussion/direct-comment response (rejects JSON IDs above JavaScript safe-integer precision), and keeps #99/#100 unavailable; AD-24 has no #101/#102 source, so filters, metrics, charts and export remain unavailable. Missing API sources and unresolved actions remain unavailable/disabled. |
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
Admin screen set. Guest GS-01, GS-02, GS-03, GS-05, GS-06 and GS-07 have direct
screen folders; GS-04 is implemented as the curriculum panel owned by GS-03.
Placeholder directories do not prove that other screens, layouts, routes or
modules exist.

Student routes ST-01–ST-26 use the StudentLayout session from API #03; tokens
remain in tab memory and protected requests use the Student Bearer wrapper.
The 100% screen-completion score represents static DD-safe UI, UX, state/logic
and caller/API mapping. It does not verify browser, live API, DB, migration or
deployment runtime. Behaviors without a safe source-backed contract remain
explicitly gated.

ST-01 calls #20 with `status=ACTIVE`, #38 and #43 independently, validates each
projection and preserves valid rows when COUNT/LIST totals disagree; #21 is not
used because its handler returns `UserProfile`, not aggregate progress. ST-02
reads #04. ST-03 uses #04/#13/#14 for supported name, phone and avatar fields;
Bio stays disabled because #14 does not persist it. Avatar upload and profile
update are separate effects. ST-04 calls #08/#15, calls #19 only for a verified
free course and confirms enrollment through #20. #15 now resolves a valid
Student Bearer and returns that Student's latest enrollment, although the API
catalog still lists its actor as Public. Paid courses route toward ST-05, while
#16/order, #17/payment and ST-06/ST-07 paid-result behavior remain gated; #18
is notification-operation lookup and #19 requires a Paid Order for paid courses.

ST-08 calls paged #20, handles out-of-range pages and COUNT/LIST mismatch, and
hides unknown status codes. ST-09 checks ACTIVE enrollment through #20 before
#37 and does not use public #09 as a private learning tree. ST-10 calls #22 on
entry and allows #23 only after explicit Start, exact success/lesson identity,
and `PUBLISHED`; stale reads are cancelled before ST-11 handoff. The #22 source
does not filter lesson status and #23 does not independently check publication.
ST-11 calls #24 after handoff and provides validated loading/error/retry states;
the player and #25/#27 remain gated. #24 checks published lesson/course and
ACTIVE/COMPLETED enrollment. ST-12 validates #26's `resources[]` and passes
selected resource context to GS-07/#12. #26 checks ACTIVE enrollment and
published lesson/course, but the checked-in `resources` table has no confirmed
writer (#47 writes `lesson_uploads`).

ST-13 calls #28 on entry and #29 only after explicit Start; ID and continuation
state are checked. ST-14 calls #28/#30, serializes answer writes and reconciles
local choices from the response. The client sends `choice_ids[]` while the
catalog declares `answer(s):string`; there is no answer-read API or authoritative
timer. ST-15 calls #31 after explicit confirmation and offers #32 after an
ambiguous/closed outcome; ST-16 reads #32 and renders a score only for `GRADED`.
These quiz APIs remain Draft in backend source, so ownership/order, answer
recovery, timer, feedback/question detail and pass decisions stay gated.

ST-17 reads #33. ST-18 separates #34 upload success from #35 submission, and
ST-19 reads #36 and shows score/feedback only for `GRADED`; unknown file details
and URLs stay hidden. #33/#35/#36 remain Draft and server eligibility/disclosure
contracts are incomplete. ST-20 shows recorded #38 awards and does not invent
#21 progress; it handles COUNT/LIST mismatch with retry. ST-21 shows #37
ACTIVE-enrollment aggregate counts/percentage/`has_content`, not a lesson
timeline. ST-22 uses only #38 awards and does not synthesize certificates.

ST-23 calls #39 with course/page filters; current source returns ACTIVE root
threads in fixed 20-item pages and ignores sort. It validates page state,
recovers empty out-of-range pages and preserves rows/retry on COUNT/LIST mismatch.
ST-24 uses ACTIVE #20 course options, #40 create and #39 refresh; it blocks blind
replay after ambiguous writes. #40 accepts `content:string` although catalog says
`int64`. ST-25 uses owner/enrollment-scoped #42/#41, validates the exact thread
projection and offers read-only #42 reload after an ambiguous reply; #41 also
accepts string content despite the catalog declaration. Screenshot-only controls
remain unsupported.

ST-26 calls #43–#45. #43 lists direct and recipient-addressable notifications
in 20-item pages, #44 marks one addressable notification read, and #45 marks all
addressable unread rows and returns `updated_count`. Migration 016 defines
`notification_recipients`; #45's response differs from catalog
`Page<Notification>`. The client formats valid `created_at` timestamps for
`vi-VN`, uses semantic `<time>`, marks loading with `aria-busy`, announces
unread-count changes, recovers an out-of-range page and keeps notification
deep-links gated. These source-backed states and safeguards complete static
screen coverage; runtime remains unverified. Mentor pages call
their source-backed APIs; ME-03 follows changed course IDs, cancels stale
requests, validates #46/#49/#65 response shapes and renders the #49 content
tree and #65 aggregate roster independently. It renders optional #65 Student
avatars only for HTTPS/same-origin URLs with an initials fallback. #65 remains a local
`Page<MentorStudentProgress>` projection that differs from the catalog, and
direct-owner scope may differ from assigned-course expectations. ME-04 calls
#46 (first 100 courses), shared #34 upload with `purpose=LECTURE`, and #47 with
T041-approved Markdown `content:string` and ordered upload IDs; its textarea
also inserts basic Markdown emphasis, headings, lists, quotes and code syntax,
and the supported form uses a responsive two-column layout. ME-04 allows
separate #46 COUNT/LIST totals to differ and blocks duplicate #47 submit while
the write is pending. Successful creation opens ME-05/#48. Direct-owner authorization and immediate
`PUBLISHED` status are source-backed. Assigned courses, upload cleanup,
WYSIWYG/preview/lifecycle fields and live/browser runtime remain open; focused
Mentor tests pass 6 spec files / 12 tests. Other Mentor actions stay gated where
source contracts do not support the DD. Do not infer
authorization from route metadata; live API/schema/browser runtime remains
unverified.

ME-02 is registered at `/mentor/courses` under `MentorLayout` and calls #46
through `ME02CoursesService`/`MentorApiService`. Its request stream cancels
superseded page/filter reads, validates the exact success code, page metadata,
Course/mentor projections and supported status filter, and recovers an empty
out-of-range page. Cards use only #46 fields, including a safe optional
thumbnail; page size remains 20 and status labels map only `DRAFT`/
`PUBLISHED`. The screen now scores 100% under the static DD-safe rubric;
assignment-versus-direct-owner scope and unsupported search/level/sort/KPI/
actions remain open. Runtime is unverified; focused Mentor tests pass.

ME-05 is registered at `/mentor/lectures/:lectureId` and calls #48 through
`MentorApiService`. The page cancels stale route reads, validates the success
envelope/business code/lecture identity and response fields, provides loading,
invalid/not-found/forbidden/error/retry states, renders T041 Markdown as escaped text,
and lists asset metadata without opening an unverified URL. A #48 HTTP 403 is a
non-revealing access-denied state with a course-list link and no retry; transient
errors retain retry. It links to ME-03 and ME-06 with the validated course ID.
The screen now scores 100% under the static DD-safe rubric; unsupported Stitch
player/analytics/discussion/edit/status/file-open features and assigned-course
authorization remain gated; browser/live-schema runtime is unverified.

ME-06 is registered at `/mentor/courses/:courseId/content` and calls #49.
Route ID changes cancel old reads; the page validates the success envelope,
exact business code, course-scoped Content fields, unique IDs, parent
existence and cycles before rendering. It builds the flat response into a
parent-child list using server sibling order, exposes mutation links only after
#49 confirms owner access, gives per-node actions at least 44px hit areas and
wraps them on narrow layouts, and handles invalid/loading/empty/404/403/error-
retry states. The screen now scores 100% under the static DD-safe rubric;
Stitch filters, expand/collapse, reorder, KPI/audit panels, assigned-course
policy and live/browser runtime remain open.

ME-07 is route-reactive and calls #49 in create/edit mode, cancels stale reads,
validates the exact success envelope/code and course-scoped Content records,
and only selects an edit record found in the requested course collection. It
handles invalid/loading/not-found/forbidden/error-retry states and links back
to ME-06. #50/#51 have backend sources but no ME-07 caller; Save remains gated
because ContentType/payload subtype and #51 body are not approved. The screen
now scores 100% under the static DD-safe rubric; unsupported editor/media/
order/version behaviors and live/browser runtime remain open.

ME-08 reads #49 with the selected route `contentId` and `courseId` from the
ME-06 history-state handoff. Route changes cancel stale reads; response code,
course-scoped Content fields, unique IDs and tree integrity are validated
before selection. Invalid context, not-found, forbidden and retryable errors
are separate. #52/#53 remain without ME08 callers while lifecycle/readiness
and deletion-dependency policy remain unapproved. The screen now scores 100%
under the static DD-safe rubric; direct-entry history state and live/browser
runtime remain unverified.

ME-09 calls #54 using only source-supported course/status/page filters; page
size 20 is fixed by the backend and is not sent as a query parameter. Query
changes cancel stale reads; the page validates the exact success envelope/code,
page counts, Submission fields, dates, IDs and file metadata before rendering
or linking to ME-10. Search, deadline, learner
name and assignment/course labels are not sourced. The API Page response is
still DERIVED in its DD; the screen now scores 100% under the static DD-safe
rubric and runtime is unverified.

ME-10 reads #55 reactively, cancels stale detail requests, and validates the
success envelope/code, Submission identity, fields, timestamp and file
metadata. Score/feedback remain read-only; #56/#57 have no ME10 callers while
rubric/attachment serialization and score-scale contracts are unresolved. The
page does not send placeholders or open raw file URLs. The screen now scores
100% under the static DD-safe rubric; runtime is unverified.

ME-11 calls #58 using only `course_id`/`status`, cancels stale filter requests,
validates nested SupportRequest/student/message/timestamp/attachment data, and
links validated IDs to ME-12. Optional Student avatars use HTTPS/same-origin
HTTP with `no-referrer` and initials fallback; detail links use 44px targets
and request-specific accessible names. It does not infer unread counts, SLA,
paging or live updates. The screen now scores 100% under the static DD-safe
rubric; runtime and local migration deployment remain unverified.

ME-12 follows route changes and validates #59/#60 envelope codes, request
identity and nested messages/attachments. Text-only #60 replies
use the backend-validated empty attachment array; an ambiguous reply cannot be
resent until #59 reloads and reconciles the thread. #61 success requires
`RESOLVED`, but its ME12 caller remains disabled until the readiness/satisfaction
gate and confirmation interaction are approved. Reply is available only for
OPEN, IN_PROGRESS or WAITING_LEARNER while terminal-status policy is open.
Confirmed #60 feedback remains visible when the following #59 read fails, and
attachment URLs are not opened while download policy is unresolved. Attachment
upload, loaded design and live runtime remain open; the screen now scores 100%
under the static DD-safe rubric.
