# Study Web context router

```text
CONTEXT_STATUS: UNWIRED
SOURCE_STATUS: editable application source/package manifest absent; an ignored compiled dist artifact contains only the root home route
```

Canonical page graph: `INDEX.md`.

The current checkout has Study Web documentation and screen assets under
`apps/study-client/docs/`, plus an ignored `apps/study-client/dist/` build
artifact. Its compiled bundle contains Vue/Vue Router code and only a `/` home
route; it contains no Student screen routes or course/progress API calls. Build
provenance and serving/deployment are unknown. Editable application source and
the package manifest are absent, so this artifact does not establish an
implementable Study Web feature route. Recheck the source tree for each task;
do not infer feature behavior from design files or older snapshots.

[`../../web-study/design.md`](../../web-study/design.md) is the intended visual,
interaction and accessibility target. It does not establish that a screen or
behavior exists at runtime.
