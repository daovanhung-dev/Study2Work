# Study Web subcontext

```text
CONTEXT_STATUS: SOURCE_BACKED_SKELETON
STACK: Vue 3 + Vite + Vue Router + Pinia + Vue Query + Zod
RUNTIME_STATUS: STATIC_HOME_SHELL
API_STATUS: STUDY_OPENAPI_NOT_FOUND
```

Source root: `apps/study-client/`. This is a separate Vue application, not a
React Work Web module. The current route graph contains only `/`, and the home
page displays the Study subsystem label, configured API base URL and
`/health/live` text; it does not perform a live API request.

Load order:

```text
web-work/AGENTS.md
→ study/INDEX.md
→ exact Vue source + package config + tests
```

Do not infer Study API request/response fields from the Work client or from the
placeholder Study OpenAPI README. The shared envelope type guard is present and
tested; the current HTTP helper only defines the base URL boundary.
