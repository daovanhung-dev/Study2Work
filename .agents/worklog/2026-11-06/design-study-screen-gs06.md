---
task_id: "2026-11-06-design-study-screen-gs06"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["GS-06 passes courseId from GS-03 to API #11; selected resourceId passes to API #12 and GS-07; ST-12 shares resource access semantics"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study GS-06

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 165 exact-type docs worklogs available; selected 3; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs01.md`
    - carry_forward: Study Web remains `UNWIRED`; keep expected/current behavior separate and do not claim DDL/test artifacts prove runtime/live schema.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs02.md`
    - carry_forward: keep mock/screenshot data distinct from API-supported data; preserve original asset hashes; source HTML links do not prove route behavior.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs03.md`
    - carry_forward: API #08/#09 source-backed, API #10 declared/not runnable; do not assume route/cache/orchestration from static assets.
- additional handoff read: `.agents/worklog/2026-11-06/design-study-screen-gs05.md`; preserve one-screen-per-session scope, API/runtime distinctions, and continue only GS-06 in this session.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Objective: handle GS-06 only this session, with a plan before annotation/DD, preserve source image/HTML, create marker map/annotated image and source-traced DD, then update the global screen tracker and worklog.
- Canonical inventory: Guest tab `/courses/:courseId?tab=resources`, AC-06, APIs #11/#12; open #11 on tab, select resource ID, call #12 before opening; linked GS-03, GS-07 and ST-12. The inventory explicitly forbids guessing resource visibility.
- AC-06 adds public-or-authorized access, 403/404 branches and Object Storage signed URL for private resources. These expectations conflict with public/no-Bearer catalog semantics and current #12 source; preserve as unresolved contract differences.

## CURRENT_BEHAVIOR

- Before edits, GS-06 directory contained only original `screen.png` and `code.html`. PNG was valid at 1486×1600; SHA-256 recorded in `GS-06_PLAN.md`. It is a static gated/empty hand-off mock with contract/state cards and no resource rows.
- HTML has no JavaScript/API binding/router. Most anchors use `href="#"`; `Xem tài liệu tích hợp API` points to `#technical-contract-block`; the download button is disabled. Prototype data and proposed `items/total`, signed URL TTL, RBAC and 410 copy are not runtime evidence.
- API #11 exists in catalog and API DD only. No current route/module/query/test was found in Study Server app/tests. Catalog/DD declares `ApiEnvelope<Resource>` singleton despite list endpoint/one-to-many relationship. `resources.visibility` has no checked-in DDL field.
- API #12 route/view/query/validator/model exist and are registered. Current view returns direct `resources.url`; route has no auth dependency; visibility is excluded by response model. Parent course must be `PUBLISHED` only when `lesson_id` is non-null; a null `lesson_id` skips parent lookup. Current errors are 404/500; no signer, 403, TTL or 410 exists in source.
- Study Web remains `UNWIRED`; no deployed/runtime behavior was verified.

## SOURCE_TRACE

- Objective file: `/home/daovh/.codex/attachments/f6127670-d01c-46c9-b22a-2adfcbe78641/goal-objective.md` reread before continuing.
- Required context/preflight was carried forward and inspected: `.agents/AGENTS.md`, `.agents/context-map.md`, `.agents/worklog/README.md`, `TEMPLATE.md`, `.agents/project/INDEX.md`, architecture/dependencies, `.agents/web-work/{AGENTS.md,INDEX.md}`, `.agents/web-work/study/{AGENTS.md,INDEX.md}`, `.agents/server-study/{AGENTS.md,INDEX.md}`, `.agents/skills/INDEX.md`, `.agents/web-study/design.md`.
- Expected flow: `apps/study-client/docs/list_screen.md` GS-06 row, F02/G-07 and API index; AC-06 nodes in `apps/study-server/docs/diagrams/AC_UNICA/AC_01_GUEST_ACCOUNT.drawio`.
- Assets: `apps/study-client/docs/screen_stitch/02_guest_discovery/GS-06_tai-nguyen-khoa-hoc/{screen.png,code.html}`.
- API declarations: `docs/lists/list_api.md`; `apps/study-server/docs/dd/11_courses_resources/` and `12_resources_detail/` request/overview/response docs.
- API #12 current chain and test source: `apps/study-server/app/api/v1.py`; `app/modules/guest/api_12_resources_detail/{view,query,validate,models}.py`; `tests/modules/guest/api_12_resources_detail/test_resources_detail.py` (read only; not run).
- DDL candidate: `infra/postgres/study-server/DB.sql` courses/lessons/resources; live schema is not verified.
- Related design patterns reviewed: GS-05 plan/DD/marker/worklog; global `screen_stitch/dd_screens/PLAN.md`.
- Per-screen plan was written before marker/DD creation. 23 component markers were then mapped to documentation rows; the annotated preview was visually inspected.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| #11 runtime/cardinality | Catalog and API DD only; no app/test route; contract body is a single Resource. | `DECLARED_NOT_RUNNABLE` / `DISCREPANCY` | Cannot produce a reliable resource collection, empty/list state, ordering or paging. |
| Resource visibility | AC-06 requires public or authorized; DDL and current model do not contain visibility. | `BLOCKER` | No visibility/access decision can be implemented from current source. |
| #12 authorization/signing | Current source is public, returns direct URL and conditionally checks PUBLISHED parent; does not check user access or sign URL. | `SOURCE_BACKED` plus `DISCREPANCY` with AC-06 | Do not open private resource or claim secure signed-link behavior. |
| 403/410 | AC-06/prototype references 403 and prototype says 410/TTL; catalog/current #12 only 404/500. | `EXPECTED_ONLY` / `BLOCKER` | Error UI and retry/signing behavior need approved contract. |
| Empty vs contract block | Prototype empty text combines “no resources” with unresolved contract. | `DISCREPANCY` | DD keeps true empty contingent on a confirmed successful empty collection. |
| Study Web | Current source context has no wired screen/router/client. | `UNWIRED` | Route, cache, navigation and runtime remain unverified. |

## CHANGES

- Added `GS-06_PLAN.md` before authoring the screen DD or annotated image.
- Added `GS-06.md`, `GS-06_markers.json`, `GS-06_markers_overlay.svg`, and `screen_annotated.png`; original `screen.png`/`code.html` preserved.
- Updated global `screen_stitch/dd_screens/PLAN.md`: GS-06 status, 13/83 complete sets, 70 remaining, and GS-07 next.
- Added this worklog. No context registry/page update was needed; no context page was changed.
- `DD READY`: no. `IMPLEMENTATION BLOCKED`: yes. `RUNTIME VERIFIED`: no.

## VERIFICATION

| Check | Result | Status |
|---|---|---|
| Objective/context/worklog preflight | Objective reread; task routing and context-map/worklog preflight carried forward; selector `READY`, exact-type docs logs GS-01..GS-03 read plus GS-05 handoff; no shortage. | VERIFIED |
| GS-06 source trace | Inventory/F02/G-07, AC-06, API #11/#12 catalog/DD, current #12 route/view/query/validator/model/test source, checked-in DDL candidate, Study Web status and original screenshot/HTML reviewed. Source tests were not run. | VERIFIED |
| Plan-before-authoring | `GS-06_PLAN.md` written before marker overlay and DD. | VERIFIED |
| Marker/document audit | Static script confirmed 23 ordered unique numbers/element IDs, 23 corresponding DD rows in same order, and 23 SVG circles plus 23 labels. | VERIFIED |
| Image preservation/dimensions | Original `screen.png` SHA-256 remains `b90795438d5369466bb101e8f6730265667f8ecc45c0d047d66495410da87dcd`; source 1486×1600; annotated image 3132×3200. | VERIFIED |
| Visual review | Final annotated preview inspected; all 23 callouts stay in side gutters, point to the intended component row and do not cover primary copy or controls. | VERIFIED |
| Tracker | `PLAN.md` records 13/83 complete sets, 70 remaining; GS-06 is `DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED`; next is GS-07. | VERIFIED |
| `git diff --check` | Passed before this final worklog update; repeat after this worklog update. | VERIFIED |
| Tests/runtime | Not run; no test or runtime verification claimed. | NOT_RUN |

## HANDOFF

- GS-06 is the only screen in this session. Remaining blockers are API #11 collection/runtime contract, resource visibility/access, #12 private authorization/signer/expiry, loaded/list/error designs and Study Web route wiring.
- After final static audit, continue at GS-07 in a separate session. GS-07 must revisit API #12 and preserve the same access/signer discrepancies.
