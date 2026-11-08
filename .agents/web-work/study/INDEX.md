# Study Web context index

## Current source status

`apps/study-client/` contains documentation/assets and an ignored compiled
`dist` artifact, but no editable application source or package manifest. The
bundle contains a single `/` home route and no Student screen routes or
course/progress API calls; its serving/deployment is unverified. Student screen
behavior is therefore `UNWIRED` and must be rechecked against current source for
each task.

## Pages

| Topic | Page | Authority |
|---|---|---|
| Visual, interaction and accessibility target | [`../../web-study/design.md`](../../web-study/design.md) | Intended design only; not runtime evidence. |
| Skill-formatted screen DD packages | [`../../../apps/study-client/docs/dd_screens/screen-index.md`](../../../apps/study-client/docs/dd_screens/screen-index.md) | 83 source-derived packages; route/API status stays per screen, and the packages do not prove runtime wiring. |

Screen-specific design source is in `apps/study-client/docs/`. Use its
[`list_screen.md`](../../../apps/study-client/docs/list_screen.md) inventory,
[`screen_stitch/`](../../../apps/study-client/docs/screen_stitch/) source assets,
and [`dd_screens/`](../../../apps/study-client/docs/dd_screens/screen-index.md)
packages as requirements/design evidence. Trace APIs to current Study Server
source when the screen has backend dependencies.
