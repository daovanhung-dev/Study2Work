# Workflow: Implement and demo a Study Web screen

```text
SCOPE: apps/study-client/
FRAMEWORK: ANGULAR 22
TRIGGER: coding, fixing, testing, or demonstrating one Study Web screen
REGISTRY_KEY: study-web-screen-coding
```

Follow this workflow together with [`study/AGENTS.md`](../AGENTS.md) and
[`frontend-rules.md`](../../../web-study/frontend-rules.md). The screen
inventory, screen DD, screenshots and `screen_stitch` HTML describe expected
design/behavior; they do not prove current routes, API wiring or runtime.

## 1. Select the screen and record scope

1. Complete the mandatory preflight in `study/AGENTS.md`: read
   `apps/study-client/docs/list_screen.md` and `list_endpoint.md`, identify the
   screen ID/name/route and API IDs, and record
   `Study FE scope: screens=<...>; APIs=<...>` in the worklog.
2. Use `apps/study-client/docs/dd_screens/screen-index.md` to locate the exact
   package. Treat the index as a locator: if its stack or paths conflict with
   current source or the package files, record `DISCREPANCY` and use the
   actual package/source as evidence. Record the DD status and any gate/open
   question before coding.
3. Read current Angular source for the route, page, shared UI, transport and
   related tests. Load Study Server API/DB context only for the API or persisted
   data that this screen actually needs. The current Study OpenAPI page is a
   placeholder; do not invent a contract.

## 2. Read and analyze the full screen package

For the selected screen, read every package file before writing the plan:

- `images/README.md`
- `images/screen-clean.png` and `images/screen-numbered.png`
- `00-overview.md` through `07-test-cases.md`
- the matching HTML under `apps/study-client/docs/screen_stitch/`
- linked marker JSON or screen plan when the package references them

Open both PNGs visually. Map each numbered marker to its element ID in the DD;
compare the clean and numbered versions and check their provenance in the image
README. Treat the HTML as design reference, not runnable Study Web source: it may
use remote assets, inline handlers, or behavior that is not implemented in the
Angular client.

If the clean image, numbered image, marker map, HTML and DD disagree, record a
`DISCREPANCY`, identify which artifact is blank/derived/stale, and resolve the
expected behavior from the source DD and approved requirements before coding.
For example, the SH-02 clean PNG is blank while its numbered PNG shows a login
mockup; its DD traces the mockup to `screen_stitch` HTML and marks the screen
`DD BLOCKED / RUNTIME NOT VERIFIED`. Do not silently treat one asset as the
authoritative runtime screenshot or close an unresolved gate by guessing.

## 3. Trace behavior and write the implementation plan

Crosswalk the UI elements and markers to the DD events, business rules, data
flow, API integration, navigation and test cases. For each event, record:

- trigger and visible result;
- data read/written and the responsible layer;
- API ID/method/path and request/response/error contract when applicable;
- loading, success, empty, validation, unauthorized and service-error states
  that the DD specifies;
- navigation destination and parameters;
- dependencies that remain `UNWIRED`, `SOURCE_REQUIRED`, `NOT_FOUND` or
  `DISCREPANCY`.

Before coding, write a plan in the task worklog that names the screen/group
folders, layout and route changes, page and local UI components, reusable
components found under `src/app/shared/`, services/models, events, APIs, data
flows, tests, demo setup and fixture-cleanup steps. Search existing shared UI
first; place a component in `src/app/shared/` when it is reused by multiple
screens. Keep screen-only dialogs and widgets in that screen's `ui/` folder.

If the DD is `BLOCKED` or an unresolved decision affects the behavior being
implemented, implement only independently specified presentation/behavior and
leave the dependent action blocked or clearly disabled as the DD requires.
Record the blocker; do not invent route policy, API fields, validation,
permissions, session rules or response behavior.

## 4. Implement in the registered Study Web structure

Map inventory IDs to compact screen folder names, for example `SH-02` becomes
`SH02`:

```text
src/app/
├── features/
│   ├── shared/                 # Shared / Auth / System screens (SH-*)
│   │   ├── SH02/
│   │   │   ├── data-access/
│   │   │   ├── models/
│   │   │   ├── pages/
│   │   │   └── ui/
│   │   └── shared.route.ts     # All routes owned by this group
│   ├── guest/                  # GS-*
│   ├── student/                # ST-*
│   ├── mentor/                 # ME-*
│   └── admin/                  # AD-*
├── layouts/
│   ├── shared/
│   ├── guest/
│   ├── student/
│   ├── mentor/
│   └── admin/
└── shared/                     # Reusable neutral UI across screens
```

Every screen folder has exactly these four direct subfolders:
`data-access/`, `models/`, `pages/`, and `ui/`. `pages/` contains the main
standalone Angular component and its `.ts`, `.html`, and `.css` files;
`data-access/` contains screen services such as `*.service.ts`; `models/`
contains typed screen/API shapes and data filtering or conversion; `ui/` contains
screen-local child components such as popups. Do not add `domain/` or another
fifth direct folder to a screen.

Create one `<group>.route.ts` in the root of each feature group, using the
singular `.route.ts` suffix, to define all screen routes in that group. Each
group has one layout in `layouts/<group>/`; the layout hosts its child route
outlet. `app.routes.ts` composes only the group layouts and group route files
whose requirements and dependencies have been verified. A route from the DD
remains a design candidate until it is wired in source.

Before connecting or reorganizing routes, use this checklist:

1. Inspect the root component/template and shared layouts for content rendered
   outside a `RouterOutlet`. Static scaffold placed beside the outlet remains
   visible on every child URL; put route-specific content inside its page or
   layout instead of leaving it at the app root.
2. Record the intended behavior for `/` and the feature URL. Distinguish a root
   readiness/system page from the Shared (`SH-*`) screen group and from a
   fallback route. If “system route” or another route label leaves those
   behaviors ambiguous and the choice changes navigation, resolve that meaning
   before wiring routes. Do not add an unspecified wildcard or fallback.
3. Inspect the existing route graph and guard/auth configuration. Preserve
   verified guards; do not infer a role or access policy from a route name. An
   unguarded route provides navigation only and does not control access.
4. Add or update route tests that open `/` and the feature URL directly, assert
   the expected page at each URL, and verify root-only scaffold is absent from
   the feature route. Include both URLs in the browser demo when both are in
   scope.

## 5. Test and demonstrate the screen

1. Add or update focused Angular tests for the DD test cases, events, data
   conversion and error/loading states. Inspect `package.json` and
   `angular.json` for the actual test command. If no runnable test target exists,
   add the needed test setup within the screen implementation task or record
   `DECLARED_NOT_RUNNABLE`; do not report unrun tests as passing.
2. Run the app locally and demonstrate the actual route in a browser. Compare
   layout and states with the analyzed DD/assets; exercise every in-scope event,
   keyboard behavior and relevant responsive sizes. Fix any mismatch and repeat
   the focused test/demo until the acceptance cases pass or a documented blocker
   prevents completion.
3. When persisted backend data is needed, seed fake rows directly only in a
   confirmed disposable local/test database. Verify the connection target and
   current schema/source before inserting; checked-in DDL alone is not proof of
   the live schema. Never seed a production or shared user database. Do not log
   credentials or tokens.
4. Record the exact primary keys/IDs of rows created for the demo. Immediately
   after each demo, delete only those fixture rows in dependency-safe order and
   query by their recorded IDs to confirm cleanup. Do not truncate tables or
   delete pre-existing rows. If the DB target is not isolated or cleanup cannot
   be verified, stop before/after the unsafe step as applicable, report the
   blocker and do not claim the demo complete.

## 6. Completion evidence

The worklog records the screen/API scope, DD and image files read, current-source
trace, implementation plan, changed files, automated test command/results,
browser demo results, fake-data IDs and cleanup confirmation. Keep DD/design
expectations separate from current behavior. Mark remaining `BLOCKED`,
`UNWIRED`, `DECLARED_NOT_RUNNABLE`, `NOT_FOUND` and `DISCREPANCY` states
explicitly; a static screenshot or successful dev-server start does not prove
feature/API runtime behavior.
