# Study Web context index

## Current source status

`apps/study-client/` now contains an Angular 22 standalone SPA scaffold plus
documentation/assets. Only the root readiness placeholder is implemented;
business screens, auth, Study API calls, and deployment remain unwired or
unverified. Student screen behavior must be checked against current source for
each task.

## Pages

| Topic | Page | Authority |
|---|---|---|
| Mandatory frontend layer, UI/business, and dependency rules | [`../../web-study/frontend-rules.md`](../../web-study/frontend-rules.md) | Required for Study Web coding/fix/test/review and architecture-document tasks. |
| Visual, interaction and accessibility target | [`../../web-study/design.md`](../../web-study/design.md) | Intended design only; not runtime evidence. |
| Angular folders, file responsibilities, and boundaries | [`../../../apps/study-client/gui/architech.md`](../../../apps/study-client/gui/architech.md) | Current scaffold and planned feature structure; no business behavior. |
| Skill-formatted screen DD packages | [`../../../apps/study-client/docs/dd_screens/screen-index.md`](../../../apps/study-client/docs/dd_screens/screen-index.md) | 83 source-derived packages; route/API status stays per screen, and the packages do not prove runtime wiring. |

Screen-specific design source is in `apps/study-client/docs/`. Use its
[`list_screen.md`](../../../apps/study-client/docs/list_screen.md) inventory,
[`screen_stitch/`](../../../apps/study-client/docs/screen_stitch/) source assets,
and [`dd_screens/`](../../../apps/study-client/docs/dd_screens/screen-index.md)
packages as requirements/design evidence. Trace APIs to current Study Server
source when the screen has backend dependencies.
