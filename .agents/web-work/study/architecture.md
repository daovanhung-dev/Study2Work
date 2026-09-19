# Study Web architecture

- `src/main.ts` boots Vue, Vue Query, Pinia and the router.
- `src/App.vue` renders the router view and a Study app name.
- `src/app/router/index.ts` currently maps only `/` to `HomePage.vue`.
- `src/pages/HomePage.vue` is a static subsystem shell.
- `src/styles/main.css` contains the current Study-specific green visual
  baseline; the Work Cobalt token system is not automatically applicable.

Current behavior is a skeleton. Do not document a Study page, auth flow or API
query as implemented without a route/import/request caller in source.
