---
task_id: "2026-11-07-design-study-screen-ad07"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["AD-06 numeric Course.id → AD-07 / AC-32 / API #74; AD-07 → AD-08/#75, AD-09/#76/#77, AD-12/#82 course filter"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study AD-07

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 212; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Keep expected/current behavior separate; preserve source assets; UI-only DD has no canonical skill; treat Study Web as UNWIRED; trace AC/API source; do not infer KPI, route or permissions from mockups.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Separate AC-31 Admin permission from local ADMIN claim; no invented role/status/filter behavior; API test-source/fake DB does not prove live schema/runtime; keep unsupported UI actions blocked.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Preserve numeric ID handoff; distinguish API catalog, local source and UI prototype; do not infer audit/policy or runtime from mocks/tests; preserve blockers.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete AD-07 only in this session; inspect current inventory and cross-scope evidence; write `AD-07_PLAN.md` before marker map, annotation or screen DD; preserve original assets; create ordered one-to-one markers and annotated image; author A–F DD; update `list_screen.md`, `dd_screens/PLAN.md` and this worklog; distinguish DD readiness, implementation block and runtime verification.
- Current inventory pointer: AD-07 is Admin course detail, proposed `/admin/courses/:courseId`, AC-32 / API #74; numeric Course ID is handed off from AD-06. Verify source and contract before using this as final behavior.

## CURRENT_BEHAVIOR

- `screen.png` is 1411×1600 sRGB, SHA-256 `e937dc87f86f6c8404c04f4d8a2cafd15706ec43a87bdfead3ae465f010deaa7`; `code.html` is 26,564 bytes, SHA-256 `279eef430668a5f05024c989d86da4a2523c71d65721a93c412f19bfe375097e`. Both source assets remain unchanged.
- Prototype HTML renders a static Admin course detail shell, blank metadata fields, zero metric text, empty curriculum, quality/policy claims, links, and disabled AD-08/AD-09/AD-12 buttons. It has 12 anchors and 4 buttons; all anchors use `href="#"`; there are no form inputs, selects, table rows, fetch/XHR calls, route handlers, or data binding. The only script is a Tailwind config. This is a design artifact, not current app behavior.
- Study Web remains `UNWIRED`: `.agents/web-work/study/AGENTS.md` and `INDEX.md` describe no editable client source/package/router; the current `apps/study-client` source tree has no implementation for the proposed route.
- AC-32 diagram: Admin with course-management permission opens management, GET #73, then GET #74 reads course/owner/counters, then chooses PUT #75 update, PATCH #76 status, or DELETE #77 by policy and reloads list. Diagram-level counter requirement has no response field in #74 catalog/model.
- API catalog #74: `GET /api/v1/admin/courses/{course_id}`, Bearer JWT/Admin, required signed-int64 path, `ApiEnvelope<Page<Course>>`; 200 `DESIGN_RESOURCE_RETRIEVED`; 401/403/404/500. API DD is `Draft — Needs Confirmation`.
- Local #74 route is registered in `apps/study-server/app/api/v1.py`. View calls shared ADMIN guard before path parsing or DB, parses signed int64 (including negative values; no positive guard), queries by bound `course_id` without status filter, maps through shared `Course`, and returns a singleton `CoursePage` with page/size/total/total_pages all 1. Malformed/out-of-int64 and missing rows return 404; query/projection/mapping failures return safe 500 with rollback; it does not commit. Local source does not check AC-32's separate course-management permission.
- The Course projection is `id`, `title`, nullable `description`, nullable `thumbnail_url`, decimal-string `price`, `status`, and `mentor{id,full_name,avatar_url|null}`. The SQL only joins `courses` and `users`; it does not return course code, counters, category, curriculum, lessons, or enrollments. Legacy `DB.sql` is only a candidate schema and conflicts with versioned pilot DB artifacts; live schema is not verified.
- Existing API #74 unit tests cover singleton projection/nulls/decimal, guard ordering, malformed/overflow and signed-negative path behavior, not-found, query/mapping safe 500, and OpenAPI. Their fake session/query doubles are not live DB evidence. No tests or runtime were run in this session. Historical HTTP report is isolated/temp-schema evidence only.
- API #82 catalog and local route/module support optional `course:int64`; the local view binds that value as `course_id` for an exact lesson filter. Passing AD-07's numeric Course ID as `/admin/lessons?course=<id>` is technically supported by current API source, but the screen route handoff is still a candidate because the inventory only lists `/admin/lessons`. API #82 DD remains Draft and its catalog `ApiEnvelope<Lesson>` conflicts with local list response `ApiEnvelope<Lesson[]>`.

## SOURCE_TRACE

```text
Expected: AC-32 Admin course-management permission -> AD-06 numeric Course.id -> AD-07 GET #74 -> course/owner/counters per diagram -> AD-08/#75 or AD-09/#76/#77 by selected operation/policy -> reload list.
Current: route + API #74 source are locally wired; shared ADMIN JWT guard -> signed-int64 path parser -> bound Course/UserSummary read -> singleton Page<Course>. Counters and dedicated permission are absent; Study Web UI is UNWIRED; AD-07 HTML links/buttons are inert/disabled. API #82 supports exact `course` filtering; `/admin/lessons?course=<id>` is a route-handoff candidate, with owner confirmation and API #82 cardinality still open.
```

Trace reviewed: `apps/study-client/docs/list_screen.md` rows 64–70 and flow F11; `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md` rows AD-06–AD-12; AC-32 diagram; `docs/lists/list_api.md` #74/#82; API #74 route, view, query, validation, envelope, shared Course model/mapper; API #74 tests and DD/open questions; API #82 route/view/query/validation and Draft DD; legacy `infra/postgres/study-server/DB.sql`; Study Web context. API #8 public detail is explicitly out of scope.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #74 Course projection vs AC-32 counters | Catalog/model/SQL contain Course and mentor only; AC-32 says “counters” but defines no field or count. | DISCREPANCY / OPEN | Do not render or calculate counters until owner defines them. |
| AC-32 permission vs local API authorization | AC-32 precondition is course-management permission; local #74 checks shared JWT role `ADMIN` only. | DISCREPANCY / OPEN | Permission mapping/guard is an implementation blocker. |
| Prototype fields vs API #74 | Course code, metrics, curriculum/lessons, ISO/copyright/outcome claims are static HTML and not in API #74 projection. | DESIGN-ONLY / UNCONFIRMED | Mark unsupported values as blocked; do not bind fabricated fields. |
| AD-07 → AD-12 / API #82 | Catalog/local source support `course?:int64` exact filtering; candidate query handoff is `/admin/lessons?course=<Course.id>`. Inventory only lists base route; API #82 DD has a `Lesson` vs `Lesson[]` response mismatch. | DERIVED / OPEN | Candidate handoff is technically supported, but route choice and #82 response contract still need confirmation. |
| Study Web and navigation | No editable UI/router; prototype anchors use `#`; outgoing action buttons are disabled. | UNWIRED | Runtime not verified; route handoffs remain design targets. |
| Database source | Local legacy BIGINT DDL differs from versioned pilot artifacts; no live DB/deployment evidence. | DERIVED / UNVERIFIED | Do not present local DDL as deployed schema. |

## CHANGES

- Files changed: AD-07_PLAN.md, AD-07.md, AD-07_markers.json, AD-07_markers.svg, screen_annotated.png; AD-07 inventory row and API #074 reverse status in list_screen.md; AD-07 row/checkpoint in dd_screens/PLAN.md; this worklog.
- CONTEXT_UPDATES: none.
- Context pages changed: none.
- Assumptions: none. `/admin/lessons?course=<Course.id>` is recorded as an API #82-supported handoff candidate, pending route approval and #82 response-contract resolution.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type docs --limit 3` | `READY`, 3/212 exact-type docs worklogs selected; all three selected worklogs read in full. | VERIFIED |
| Read current assets, AC-32, API #74 catalog/DD/route/module/model/tests, API #82 filter source/DD, candidate DDL and Study Web context | Findings recorded under `CURRENT_BEHAVIOR`, `SOURCE_TRACE`, and `DISCREPANCIES_AND_STATUSES`; source/test evidence is separate from runtime. | VERIFIED |
| Static artifact audit (hashes, dimensions, marker JSON/SVG, 56 C rows, links, A–F sections, inventory/folders/core bundles, whitespace) | Original hashes unchanged; source 1411×1600, annotated 2822×3200; 56 sequential unique in-bounds markers match SVG and DD; local links resolve; 83 IDs/folders match; 60/83 core bundles; no trailing whitespace. | VERIFIED |
| `git diff --check -- apps/study-client/docs/list_screen.md apps/study-client/docs/screen_stitch/dd_screens/PLAN.md apps/study-client/docs/screen_stitch/05_admin/AD-07_chi-tiet-khoa-hoc-quan-tri` | Passed with no whitespace errors. | VERIFIED |
| Application tests or Study Web runtime | Not run; current Study Web source is `UNWIRED`, and goal calls for static artifact verification. Existing API tests were reviewed as source only. | NOT RUN |

## HANDOFF

- Remaining blockers: DD and implementation remain blocked by permission/counter/cardinality/schema decisions, prototype-only data, AD-08/09 policy, AD-12 query-route plus #82 response cardinality, and missing Study Web wiring. Runtime is not verified.
- Next owner/action: process AD-08 in a separate session after this AD-07 session is complete.
