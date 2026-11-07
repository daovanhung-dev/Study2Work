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

Screen-specific design source is in `apps/study-client/docs/`. Use its inventory
and screen assets as requirements/design evidence, then trace APIs to the
current Study Server source when the screen has backend dependencies.
