---
task_id: "2026-11-06-design-study-screen-gs02"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["GS-02 public search consumes category metadata/API #05 and course search/API #07; q normalization, category support, paging/result mapping and navigation to GS-01/GS-03 require source trace"]
status: "VERIFIED"
---

# Worklog: Rà soát Detailed Design màn hình Study GS-02

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; selected 3 exact-type docs worklogs of 161; all selected worklogs were read.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs01.md`
    - carry_forward: Keep expected behavior separate from current source; preserve empty-state source assets; current Study Web remains UNWIRED; trace category/search handoff and do not treat fake prototype state as runtime.
  - path: `.agents/worklog/2026-11-06/design-study-screen-sh01.md`
    - carry_forward: One Screen ID per session; inventory and image/HTML can disagree; preserve both assets; don't infer fields, marketing data or navigation without evidence.
  - path: `.agents/worklog/2026-11-06/design-study-screen-sh02.md`
    - carry_forward: Preserve image/HTML hashes; source test files are not runtime proof; separate DD, implementation and runtime statuses; no Study Web route/token behavior is verified.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Resume only after reading `/home/daovh/.codex/attachments/f6127670-d01c-46c9-b22a-2adfcbe78641/goal-objective.md`; it confirms one Screen ID per session and the deliverables/status separation for all 83 screens.
- Requirement: Complete GS-02 only in this session; write/update its plan before DD and annotation; preserve original image/HTML; annotate the design screenshot with ordered unique markers mapped to DD elements; detail events, APIs, states and cross-screen handoffs; update global tracker and worklog.
- Canonical behavior: `apps/study-client/docs/list_screen.md` GS-02 row/F02: proposed `/courses/search?q=`, AC-04, API #05/#07; query synced to URL, debounce and page reset when query changes; category metadata #05 cache-first and #07 concurrent if independent; trim query in UI; API #07 fixed at 20 results per page; do not send category until backend support exists; link GS-01 and GS-03; expected states typing/loading/no-result/error.

## CURRENT_BEHAVIOR

- Source/config: `screen.png` is 987×1600, SHA-256 `6bda913843a92873f4ebed72bc45be5792c31eb38f20b80a1acd681aec04e72f`; it shows a populated search state with q=`React`, six cards, filter sidebar, total 12, six-item paging, recommendation panel, and notification/avatar controls. `code.html` SHA-256 is `f1457fdb231b614cea31f2c0b9b2d42eb846ff80c333bd7dda30a5627e20c1da`; it instead has a public Guest header, GET form `action=/courses/search` with `name=q`, and a no-results card. It omits screenshot suggestions, filters, results, cards and pagination. Script functions for clear/toggle/reset have no matching controls/call sites; referenced IDs are absent, and the query input has no `id`. Current Study Web source/package/router/entrypoint remain absent.
- API and database source: API #05 is registered public GET `/api/v1/categories`; it defaults omitted locale to `vi-VN`, reads `ACTIVE` rows for exact locale ordered by ID, and returns success with `Page<Category>` even when empty. API #07 is registered public GET `/api/v1/courses/search`; it accepts optional `q`, `category`, `page`, `sort`, normalizes q by trim/lowercase (blank becomes no keyword predicate), rejects any non-null category with 422, and validates page>=1 plus allowlisted sort. Search count/list query only `PUBLISHED` rows with bound `LOWER(c.name) LIKE '%q%'`, fixed page size 20, and current default order `created_at DESC, id ASC`; sort allowlist is `id/name/price/created_at` with `asc/desc`. Response maps id/title/description/thumbnail_url/price/status/mentor and pagination; no category/currency/rating/duration/discount/tag fields. The API catalog still declares optional category and reusable `Course.category`; checked-in DDL has separate category/course tables without a course-category relationship.
- Runnable tests: #05 and #07 test source exists; #07 tests cover q trim/lowercase, blank q becoming no filter, fixed size 20 even when an extra `size=5` query is sent, page metadata, category rejection before DB query, validation codes and safe errors. Tests were read, not run; fake sessions do not prove live DB/deployment.
- Runtime wiring: The route/module source is composed under Study Server; no Study Web route or handler is available in the current checkout. HTML prototype native form behavior and screenshot content are not runtime evidence.

## SOURCE_TRACE

- Expected path from GS-02 inventory, AC-04 and F02: Guest search route proposal `/courses/search?q=`, #05 categories cache-first and #07 search concurrent when independent, q trimmed in UI (F02 says trim/lowercase), debounce, URL sync, reset page on q/sort change, fixed 20/page, links GS-01/GS-03. AC-04 describes input → debounce/normalize → category and search APIs → validate → query published courses → empty/results decision. AC says not to request when keyword is empty if not needed.
- Current API caller/callee: `apps/study-server/app/api/v1.py` parses query with `parse_course_search_query` into `CourseSearchQuery`, registers public `GET /api/v1/courses/search` and calls `api_07_courses_search.view.search_courses`. Validator rejects page<1, invalid sort and every non-null category (422 `DESIGN_VALIDATION_ERROR`), normalizes q by trim/lowercase and maps blank to `None`. View counts matching PUBLISHED rows (including missing-mentor integrity count), then lists a page; SQL binds q/status/limit/offset and matches only lowercased `courses.name` with a substring LIKE predicate. Page size is fixed `DEFAULT_SIZE=20`; `size` is not a declared query field. Shared mapper requires mentor and price, serializes price decimal string, and returns safe 500 `DESIGN_INTERNAL_ERROR` for DB/integrity/mapping failures. Empty match is HTTP 200 `DESIGN_RESOURCE_RETRIEVED` with `items=[]`, `total=0`, `total_pages=0`; out-of-range page is HTTP 200 empty items while retaining total/total_pages.
- API #05 trace: route → `get_categories` → exact-locale `ACTIVE_CATEGORIES` query (`id ASC`) → `Category`/single-page map → `DESIGN_RESOURCE_RETRIEVED`, including empty response. Omitted locale defaults to `vi-VN`; no Study Web cache implementation or cache failure policy exists.
- Contract discrepancy: `docs/lists/list_api.md` declares `category?:int64`, reusable optional `Course.category`, and #07 sort/filter surface. Source rejects category; `list_screen.md` G-05 says #06/#07 reject it and checked-in `infra/postgres/study-server/DB.sql` has no course-category FK/table. #07 response has no category, currency, rating, duration, discount, tag or course-count fields needed by multiple screenshot card/filter details.
- Screenshot shows six items and pagination as 1–6 of 12 with page size 6; current #07 always returns 20/page, so 12 matches yield one server page. Screenshot sort label “Phù hợp nhất” is not an API sort field; source default is newest by `created_at`. The screenshot also shows skill, duration, rating and tuition filters that #07 does not accept. These are design/contract blockers, not behaviors to fabricate.
- Study Web source is absent. Prototype `code.html` has a native GET search form but no URL-to-input hydration, debounce, result rendering or current runtime. It defines standalone `toggleLayoutView`, `clearSearchInput`, `setFilterSearch`, `resetFilters`; expected DOM elements/call sites are absent. Its visible UI is only empty state, while screenshot is a loaded state; screenshot header includes authenticated-style account controls while inventory actor is Guest and HTML has login/register.
- Relevant #05/#07 test source was read but not run. AC-04 Draw.io and API catalog are approved design references, not proof of live API/database behavior. No live DB/deployment check was made.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Screenshot versus HTML | Screenshot is loaded results; HTML is Guest header + GET form + no-results card; search/filter/card/paging DOM is absent. | DISCREPANCY | Keep source assets intact; loaded-state interaction and actor/header source-of-truth need design approval. |
| Study Web runtime | No Study application source/package/router/entrypoint in current checkout. | UNWIRED | No URL sync, debounce, cache, client event or navigation can be described as current runtime. |
| Category and facet filters | #07 rejects any category before DB; it has no skill/duration/rating/tuition query fields; checked-in DDL has no course-category relationship. | DISCREPANCY / IMPLEMENTATION BLOCKED | Do not send category or other unsupported filter params; backend/product must align filters and data model. |
| Result card fields and count | #07 returns title/description/thumbnail/price/status/mentor only; screenshot also uses tags, duration, ratings, discount/old price; current response total is paged at 20. | DISCREPANCY | Do not treat screenshot samples as API data; need field/currency/card contract and reconcile 6-per-page screenshot with fixed 20/page. |
| Sort selection | Screenshot shows “Phù hợp nhất”; #07 accepts only id/name/price/created_at with asc/desc, default created_at DESC/id ASC. | DISCREPANCY | Product/BE must map or implement relevance sorting before selecting this UI option. |
| Empty query | AC suggests avoiding request when q is empty if unnecessary; #07 blank q removes the predicate and returns all PUBLISHED courses. HTML invites typing or returning to catalog. | OPEN | Define whether blank search renders prompt or intentionally browses all; do not call #07 and label result as search without decision. |
| Results pagination | Screenshot displays 6 of 12 and two pages; API #07 has fixed size=20 and no `size` field. | DISCREPANCY | Page 2 cannot be derived for 12 results under current response; align the UI or API contract. |
| Suggested terms / promo destinations | Screenshot chips, learning-path CTA, advisor CTA and header links are absent from inventory/API contracts or HTML. | UNWIRED / NOT_FOUND | Record visible content; do not infer search preset semantics or routes/contact service. |

## CHANGES

- Files changed for GS-02: apps/study-client/docs/screen_stitch/02_guest_discovery/GS-02_tim-kiem-khoa-hoc/GS-02_PLAN.md, GS-02.md, GS-02_markers.json, GS-02_markers_overlay.svg, and screen_annotated.png; apps/study-client/docs/screen_stitch/dd_screens/PLAN.md; this worklog.
- Source assets screen.png and code.html were not modified.
- CONTEXT_UPDATES: Corrected architecture/dependency statements that named a Vue app package and runtime despite the current checkout having only docs/assets; current project context states stack/runtime is unverified.
- Context pages changed: `.agents/project/architecture.md`, `.agents/project/dependencies.md`.
- Assumptions: None. Screen content without a route/API/data contract is recorded as source/design gap.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type docs --limit 3` + selected-file review | Selected and read 3 exact-type docs worklogs of 161; no shortage. | VERIFIED |
| GS-02 artifact/static audit | 26 ordered unique markers map to 26 DD elements; 19 sequential events; 17 relative Markdown links resolve; source hashes unchanged; 2134×3200 annotated PNG; same-side marker bounds/spacing valid; SVG contains 26 circles and labels. | VERIFIED |
| Visual review | Full annotation and career-path/pagination crop reviewed; initial #19/#21 callout overlap corrected by moving #19 to y_source=1135, then regenerated and rechecked. | VERIFIED |
| git diff --check | No whitespace errors. | VERIFIED |
| `node scripts/validate-agent-context.mjs` | Exit 1: AGENT_CONTEXT_INVALID. Global validator reports missing db-admin context/source roots and stale tracked source inventory for server-study, web-work/work-web and db-admin. The GS-02 relative DD links all resolve; no GS-02-specific broken file link was found. | FAILED_GLOBAL_BASELINE |
| Tests/runtime | Not run. | NOT_RUN |

## HANDOFF

- Remaining blockers: GS02-B01 through GS02-B09 in GS-02.md; DD remains BLOCKED, implementation blocked, runtime not verified.
- Next owner/action: GS-03 in a separate session; this session covered GS-02 only.
