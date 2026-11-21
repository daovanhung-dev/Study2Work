# Study Web context router

```text
CONTEXT_STATUS: SOURCE_BACKED
SOURCE_STATUS: Angular 22 SPA routes `/` to readiness scaffold, `/admin` to AD-01, `/admin/users` to AD-02, and `/student/lessons/:lessonId` to the ST-11 static fallback; other Student screens and functional player behavior remain unverified; Student auth source now has a memory token service, guarded routes, and cookie-backed refresh, while runtime/deployment remain unverified; the Mentor FE merge was reverted, so ME-06..ME-18 routes/screens are absent
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

The current checkout has an Angular 22 standalone SPA with routes in
`app.routes.ts` for the root readiness page and the Admin route group.
`admin.routes.ts` renders AD-01 at `/admin` and AD-02 at `/admin/users` through
`AdminLayout`; AD-02 remains presentation-only. The Mentor FE merge was
reverted; ME-06 through ME-18 screens and their route group are absent from
current source. Recheck source for screen details.
`features/system` here is only the requested root scaffold route; it does not
move SH-* screens out of the canonical `shared` group or implement SH-01. The
Admin route has no client auth guard and no report API. The shared registry in
`src/app/core/constant/api.constants.ts` defines API IDs #1–#103 from the
endpoint catalog and source-only refresh route R-X01. `StudyApiService`
consumes these typed descriptors through the local `/api/v1` transport and rejects entries marked
`UNWIRED`; `WIRED` means an exact current server route source match, not a
deployment check. API #2 is marked `STUB` because its default provider accepts
requests without sending email. Feature-specific API calls, auth flow, token
storage and deployment remain unwired or unverified. Recheck the source tree
for each task and do not infer feature behavior from design files or older
snapshots.

[`../../web-study/design.md`](../../web-study/design.md) is the intended visual,
interaction and accessibility target. The app architecture is documented in
[`../../../apps/study-client/gui/architech.md`](../../../apps/study-client/gui/architech.md).
Neither document establishes that a business screen or behavior exists at
runtime.
