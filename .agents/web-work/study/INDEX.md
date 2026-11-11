# Study Web context index

## Current source status

`apps/study-client/` now contains an Angular 22 standalone SPA scaffold plus
documentation/assets. Only the root readiness placeholder is implemented;
business screens, auth, feature-specific Study API calls, and deployment remain
unwired or unverified. The generic `StudyApiService` in `src/app/core/http/` and
the local `/api/v1` proxy are transport infrastructure only. Student screen
behavior must be checked against current source for each task.

## Pages

| Topic | Page | Authority |
|---|---|---|
| Shared HTTP transport and Study API envelope | `src/app/core/http/study-api.service.ts`, `src/app/core/http/api-envelope.ts`, `proxy.conf.json` | Generic transport only; no feature endpoint or production host. |
| Study screen inventory and screen/API traceability | [`list_screen.md`](../../../apps/study-client/docs/list_screen.md) | Screen IDs, routes, API references and design/gate context; not proof of implemented UI. |
| Study endpoint catalog | [`list_endpoint.md`](../../../apps/study-client/docs/list_endpoint.md) | API IDs, method/path and design I/O for 103 endpoints; not proof of runtime wiring. |
| Mandatory frontend layer, UI/business, and dependency rules | [`../../web-study/frontend-rules.md`](../../web-study/frontend-rules.md) | Required for Study Web coding/fix/test/review and architecture-document tasks. |
| Visual, interaction and accessibility target | [`../../web-study/design.md`](../../web-study/design.md) | Intended design only; not runtime evidence. |
| Angular folders, file responsibilities, and boundaries | [`../../../apps/study-client/gui/architech.md`](../../../apps/study-client/gui/architech.md) | Current scaffold and planned feature structure; no business behavior. |
| Skill-formatted screen DD packages | [`../../../apps/study-client/docs/dd_screens/screen-index.md`](../../../apps/study-client/docs/dd_screens/screen-index.md) | 83 source-derived packages; route/API status stays per screen, and the packages do not prove runtime wiring. |

For every Study FE task, follow the mandatory scope preflight in
[`AGENTS.md`](AGENTS.md): read both catalogs, identify the affected screen/API
IDs, and record them in the task worklog. Use `screen-index.md` to locate
relevant screen DD packages and each endpoint row's Overview link to locate
Study API DD. Treat catalogs, screen DDs, and API DDs as design evidence; check
current source when describing runtime behavior. Screen assets in
[`screen_stitch/`](../../../apps/study-client/docs/screen_stitch/) are visual
references and do not establish runtime behavior.
