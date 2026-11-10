---
task_id: "2026-11-06-design-study-screen-gs07"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["GS-07 API #12 resource detail; resourceId from GS-06 or ST-12; return navigation to GS-06 or ST-12 context; SH-06 404 mapping"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study GS-07

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 166 exact-type docs worklogs available; selected 3; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs01.md`
    - carry_forward: Study Web remains `UNWIRED`; separate current source from design expectation; checked-in tests/DDL do not prove runtime/live schema.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs02.md`
    - carry_forward: keep mock content distinct from API data, preserve original asset hashes, and do not infer route behavior from static links.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs03.md`
    - carry_forward: #08/#09 source-backed, #10 declared/not runnable; avoid assuming wiring or behavior from assets.
- additional handoff read: `.agents/worklog/2026-11-06/design-study-screen-gs06.md`; preserve one-screen-per-session scope, API/runtime distinctions, and recheck #12 access/signer discrepancy.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Objective: complete GS-07 only this session; write a detailed plan before annotation/DD; preserve original PNG/HTML; produce markers, annotated image, DD, tracker update and verification worklog.
- Inventory: proposed `/resources/:resourceId`; AC-06; API #12; preview supported media and fallback download only when valid/allowed; links to/from GS-06, shared resource flow with ST-12.
- AC-06 expects public or authorized resource access, forbidden response for no access, and signed URL for private storage. Catalog/current #12 semantics do not currently implement that full expectation.

## CURRENT_BEHAVIOR

- Objective file `/home/daovh/.codex/attachments/f6127670-d01c-46c9-b22a-2adfcbe78641/goal-objective.md` was read before continuing; goal remains active and is one Screen ID per session.
- Before this session's DD/annotation work, GS-07 contained original `screen.png`/`code.html` and the saved `GS-07_PLAN.md`. Original image is 1588×1600, SHA-256 `11068f47467e5f5f47a074c833912a17816ce3cb4f95e34b59e5b2163b56259b`; HTML SHA-256 `e6550d5ba83fa27acc9f704b7599609ded9ab549175eaaadb4d03885e8bb058b`.
- PNG is a static gated viewer. HTML has no API/network call or embedded preview element; zoom/fullscreen/download controls disabled. Six local `switchHandOffState` tabs alter text and code samples only.
- API #12 route/view/query/validator/model and test source are present. Route has no auth dependency; direct `resources.url` returned; model omits visibility; parent PUBLISHED check applies only for non-null lesson_id. Current source/catalog outcomes: 200/404/500, no signer, 403, or expiry.
- Study Web UI/router is `UNWIRED`; no runtime or live DB verified. Tests are read only/not run.

## SOURCE_TRACE

- Required router and context: `.agents/AGENTS.md`, `.agents/context-map.md`, `.agents/worklog/README.md`, `.agents/worklog/TEMPLATE.md`, `.agents/skills/INDEX.md`; `node scripts/select-worklogs.mjs --type docs --limit 3`; selected docs worklogs GS-01..GS-03 read, plus GS-06 handoff.
- Cross-scope/web/server context: `.agents/project/INDEX.md`, `architecture.md`, `dependencies.md`; `.agents/web-work/{AGENTS.md,INDEX.md}`, `.agents/web-work/study/{AGENTS.md,INDEX.md}`, `.agents/server-study/{AGENTS.md,INDEX.md}`, `.agents/server-study/database.md`, `.agents/web-study/design.md`, `.agents/context-manifest.json`.
- Goal/screen sources: objective file path above; `apps/study-client/docs/list_screen.md` GS-07/F02/F04/G-07/API #12 and linked IDs; `apps/study-server/docs/diagrams/AC_UNICA/AC_01_GUEST_ACCOUNT.drawio` AC-06.
- Assets: `apps/study-client/docs/screen_stitch/02_guest_discovery/GS-07_xem-tai-tai-nguyen/{screen.png,code.html,GS-07_PLAN.md}`.
- API declaration/current chain: `docs/lists/list_api.md`; `apps/study-server/docs/dd/12_resources_detail/`; `apps/study-server/app/api/v1.py`; `apps/study-server/app/modules/guest/api_12_resources_detail/{view,query,validate,models}.py`; corresponding test source (read only).
- DB candidate: `infra/postgres/study-server/DB.sql`; current DB status is checked-in only/live schema not verified.
- Related screen evidence: GS-06 plan/DD/worklog; SH-06 DD; ST-12 inventory row; global `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`.
- `createDD-markdown` excludes `web-ui-only-dd` in registry; no canonical UI-only DD skill exists, so no API DD authoring skill was invoked.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Resource access/signer | AC-06 public-or-authorized/private-signed URL differs from public/no-Bearer catalog/current direct URL response; no visibility/access check/signer in #12 source. | `DISCREPANCY` / `BLOCKER` | Safe preview/download cannot be specified. |
| #12 response | Query/model returns id/name/type/url/lesson_id; no visibility/signed_url/expiry; URL direct from DB. | `SOURCE_BACKED` | Do not treat mock signer semantics as current. |
| 403/410/423/501 | Prototype/AC states have no matching current #12 contract/source (current 404/500; simulator has 423 and 403/410 samples). | `EXPECTED_ONLY` | Error and expiry UI mapping unresolved. |
| Parent resource gate | Current parent-course check runs only where lesson_id is non-null; no visibility/enrollment test. | `SOURCE_BACKED` / `BLOCKER` | 200 does not establish access to private resource. |
| Study Web routes | No app/router/client implementation; anchors `href="#"`. | `UNWIRED` | Entry/back/navigation/runtime unverified. |
| Preview/download | No viewer node or network handler; controls disabled. | `STATIC_PROTOTYPE` | MIME, URL safety, fallback and download behavior unresolved. |

## CHANGES

- `GS-07_PLAN.md` was saved before writing this DD or creating annotations.
- Added `GS-07.md` with current/expected trace, element/event/state/API #12 details, discrepancy and blockers.
- Added `GS-07_markers.json`, `GS-07_markers_overlay.svg` and `screen_annotated.png`; 26 ordered markers map to 26 DD rows.
- Updated global tracker to 14/83 complete sets, 69 missing sets; GS-07 is DD BLOCKED/IMPLEMENTATION BLOCKED/RUNTIME NOT VERIFIED; GS-08 is next.
- No context page/registry changed; no tests run.

## VERIFICATION

| Check | Result | Status |
|---|---|---|
| Objective/context/worklog preflight | Objective reread before continuing; selector `READY`, exact-type docs worklogs GS-01..GS-03 individually reviewed and GS-06 handoff reviewed; no shortage. | VERIFIED |
| GS-07 expected/current source trace | Inventory/AC-06, prototype, API #12 catalog/DD/current route/view/query/validator/model and test source, DB candidate, GS-06/ST-12/SH-06 links reviewed; tests not run. | VERIFIED |
| Plan-before-authoring | `GS-07_PLAN.md` existed before DD and annotation creation. | VERIFIED |
| Source image preservation | SHA-256 unchanged for `screen.png` (`11068f47467e5f5f47a074c833912a17816ce3cb4f95e34b59e5b2163b56259b`) and `code.html` (`e6550d5ba83fa27acc9f704b7599609ded9ab549175eaaadb4d03885e8bb058b`); source 1588×1600. | VERIFIED |
| Marker/document audit | Static Python audit confirmed 26 ordered unique IDs, coordinates within 1588×1600 bounds, and 26 matching DD rows; SVG has 26 circles and labels. | VERIFIED |
| Annotated image | `rsvg-convert` generated 3336×3200 output from the SVG; final preview visually inspected, callouts align in side gutters and do not cover screen content. | VERIFIED |
| Relative links/tracker | DD relative links resolve; tracker records 14/83, 69 incomplete, GS-07 separate statuses, GS-08 next. | VERIFIED |
| Whitespace | New/updated text files checked for final newline and trailing spaces; `git diff --check` passed. | VERIFIED |
| Tests/runtime | Backend tests not run; no browser/deployed runtime or live DB verification claimed. | NOT_RUN |

## HANDOFF

- GS-07 artifact set and tracker/worklog verification are complete. Continue at GS-08 in a separate session; leave the overall objective active.
