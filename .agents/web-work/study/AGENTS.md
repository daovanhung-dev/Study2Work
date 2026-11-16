# Study Web context router

```text
CONTEXT_STATUS: VERIFIED_WITH_UNWIRED_COMPONENTS
SOURCE_STATUS: Angular 22 SPA has AD-01 through AD-25 routes; 19 screen callers use 14 source-backed Admin GET APIs through an in-memory login session; deployment/runtime are not verified
```

Canonical page graph: `INDEX.md`.

## Mandatory Study screen/API scope preflight

For **every task** that touches `apps/study-client`—coding, fixes, tests,
reviews, documentation, or configuration—before detailed inspection or changes:

1. Read [`list_screen.md`](../../../apps/study-client/docs/list_screen.md) and
   [`list_endpoint.md`](../../../apps/study-client/docs/list_endpoint.md).
2. Identify the affected screen IDs/names/routes and Study API IDs from those
   catalogs. Record `Study FE scope: screens=<...>; APIs=<...>` in the task
   worklog. For either dimension outside the task scope, record `none` and why.
3. For each affected screen, use
   [`dd_screens/screen-index.md`](../../../apps/study-client/docs/dd_screens/screen-index.md)
   to find and read the DD sections relevant to the task. Read the matching
   Study API DD under `apps/study-server/docs/dd/` when the task depends on that
   API's request/response contract or business behavior; the endpoint catalog
   links to each API's Overview.
4. If a relevant DD is missing, record `NOT_FOUND`. If DD, catalog, or current
   source disagree, record `DISCREPANCY` and keep design behavior separate from
   current runtime behavior. Catalogs and DDs do not prove runtime wiring.

This preflight applies even when a task is expected to have no screen/API
impact; in that case, read both catalogs and record
`Study FE scope: screens=none; APIs=none` with the reason before proceeding.

For every coding, fix, test, review, or architecture-document task in
`apps/study-client/`, read [`frontend-rules.md`](../../web-study/frontend-rules.md)
before source work. Its layer responsibilities and dependency boundaries are
mandatory. Also read the design guide for UI/UX changes and the app architecture
guide when folder or file organization is involved.

For work implementing or fixing an individual screen, also follow the
registered `study-web-screen-coding` workflow at
[`workflows/screen-implementation.md`](workflows/screen-implementation.md).
It requires reading the full screen DD/image package, analyzing the referenced
HTML, writing a plan before coding, verifying event/API/data-flow behavior, and
testing/demoing with immediate cleanup of isolated fake DB fixtures.

The current checkout has a runnable Angular 22 standalone client-side SPA
scaffold plus Study Web documentation and screen assets under
`apps/study-client/docs/`. `app.routes.ts` lazy-loads the root readiness page
from `features/system` and the Admin route group. `admin.routes.ts` maps AD-01
through AD-25 beneath `AdminLayout`. Nineteen screen-level data-access callers
use fourteen distinct source-backed Admin GET APIs through `AdminApiService`.
`AdminSessionService` authenticates with API #3, refreshes through source-only
route R-X01, keeps credentials in tab memory only, and accepts only the
`ADMIN` role; API #4 and browser storage are not used. `AdminApiService` attaches
Bearer credentials and clears the local session on protected 401 responses.
The server-side Admin guard remains authoritative; this client wiring does not
prove deployment or API acceptance. AD-01 and AD-24/25 have no current report
sources, and #99–#103 and #18 export/operation behavior are absent or
incomplete. Mutation controls remain disabled where request, permission,
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
`features/system` here is only the requested root scaffold route; it does not
move SH-* screens out of the canonical `shared` group or implement SH-01. The
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
persisted. Other feature auth, production routing and deployment remain
unverified. Recheck the source tree for each task and do not infer feature
behavior from design files or older snapshots.

[`../../web-study/design.md`](../../web-study/design.md) is the intended visual,
interaction and accessibility target. The app architecture is documented in
[`../../../apps/study-client/gui/architech.md`](../../../apps/study-client/gui/architech.md).
Neither document establishes that a business screen or behavior exists at
runtime.
