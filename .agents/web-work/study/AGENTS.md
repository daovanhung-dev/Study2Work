# Study Web context router

```text
CONTEXT_STATUS: SKELETON_ONLY
SOURCE_STATUS: Angular 22 standalone SPA scaffold exists; business routes, auth, API integration and deployment are not verified
```

Canonical page graph: `INDEX.md`.

For every coding, fix, test, review, or architecture-document task in
`apps/study-client/`, read [`frontend-rules.md`](../../web-study/frontend-rules.md)
before source work. Its layer responsibilities and dependency boundaries are
mandatory. Also read the design guide for UI/UX changes and the app architecture
guide when folder or file organization is involved.

The current checkout has a runnable Angular 22 standalone client-side SPA
scaffold plus Study Web documentation and screen assets under
`apps/study-client/docs/`. The root component renders a temporary readiness
message and `app.routes.ts` has no business routes. No auth or Study API calls
are wired; serving on the CLI dev server does not verify deployment. Recheck
the source tree for each task and do not infer feature behavior from design
files or older snapshots.

[`../../web-study/design.md`](../../web-study/design.md) is the intended visual,
interaction and accessibility target. The app architecture is documented in
[`../../../apps/study-client/gui/architech.md`](../../../apps/study-client/gui/architech.md).
Neither document establishes that a business screen or behavior exists at
runtime.
