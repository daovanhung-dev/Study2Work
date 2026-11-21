---
task_id: "2026-11-07-design-study-screen-ad08"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["AD-07 numeric Course.id / GET #74 → AD-08 PUT #75 → re-read #74; AC-32 → AD-09 status/delete #76/#77"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study AD-08

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 213; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Keep expected/current evidence distinct; do not map static UI fields/KPIs to APIs without support; preserve assets; Study Web remains UNWIRED until current source proves wiring; do not claim tests/runtime were run.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: API source may be locally present while DD remains Draft; keep ADMIN role versus fine-grained permission separate; fake DB tests do not prove live schema; UI-only DD has no canonical skill.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Preserve numeric ID handoff and trace auth/path/query/response/errors; do not infer privacy or action behavior from mockups; retain local-source versus catalog discrepancies.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete AD-08 only in this session; inspect inventory and cross-scope sources; write `AD-08_PLAN.md` before marker map, annotation, or DD; preserve original assets; create ordered one-to-one markers and annotated image; author A–F DD; update screen inventory, global `dd_screens/PLAN.md`, and this worklog; distinguish DD readiness, implementation status, and runtime verification.
- Inventory pointer: AD-08 is Admin course edit at proposed `/admin/courses/:courseId/edit`, AC-32, APIs #74/#75; numeric Course ID arrives from AD-07; intended flow GET #74 → PUT #75 → revalidate #74; API #75 body and thumbnail upload are marked unconfirmed. Verify all behavior against current source and canonical materials.

## CURRENT_BEHAVIOR

- `screen.png` exists (1385×1600; SHA-256 `db8bbcdf5dd04644598aa8a80c7f1b3fcc5bf0475e43e81011cb88cc8f73863f`); `code.html` exists (SHA-256 `23f62355c9f93092505ff8be0a6e0d9aad31b9a8ed4dec0156f66bbc96021c32`). Preserve both.
- Prototype is static HTML. It has disabled title, course-code, mentor, price, description, thumbnail, and Save controls. Save is disabled with `aria-disabled=true`; there is no fetch/axios/XHR, event listener, inline event handler, or UI API client call in the file. The thumbnail upload text and reference-card content are static.
- Prototype Back-to-detail copy says AD-07 but its `href` is `/admin/courses`; Cancel also targets `/admin/courses` (the proposed AD-06 list). Other shell/local breadcrumb links point to `#`; notification is a button with no handler. The page claims #74 metadata mutation paused and #75 multipart upload locked, but those are static labels, not runtime status evidence.
- The Study Web checkout contains only docs/assets and ignored `dist`; no app package, router, entrypoint, or source client was found outside `node_modules`/`dist`. Study Web is `UNWIRED`; runtime is `NOT VERIFIED`.
- Catalog #75 is `PUT /api/v1/admin/courses/{course_id}`, Bearer JWT/Admin, int64 path, `ApiEnvelope<Page<Course>>`, success `DESIGN_RESOURCE_UPDATED`, and errors 401/403/404/422/500. Catalog and AC-32 do not define a request body.
- Local Study server registers #75 in `app/api/v1.py` and `modules/admin/api_75_admin_course_update/`. The strict candidate body requires `title:string`, `description:string|null`, `thumbnail_url:string|null`, `price:string`, rejects extras, and requires all four keys. Shared authorization checks `ADMIN`; this is not proof of AC-32 fine-grained course-management permission.
- Current local validation: signed int64 path; title max 200 without trim/nonblank rule; description/thumbnail allow null; thumbnail has no URI scheme/host/length validation; price decimal string, no exponent/rounding, at most two fractional and ten integer digits; negative values are accepted. These are local/DERIVED candidate rules, not approved product contract.
- Local SQL updates only `name`, `description`, `thumbnail_url`, `price`, `updated_at` in legacy `courses`, leaves status/mentor unchanged, then reads API #74 projection in the same transaction and returns a singleton `Page<Course>`. No thumbnail upload/multipart API is called. Query/readback/projection/commit failures return safe 500 and rollback; missing target returns 404. The UPDATE body/projection/transaction semantics remain subject to API DD approval.
- The legacy candidate DDL uses BIGINT ID, nullable mentor/description/thumbnail, `name VARCHAR(200)`, `price NUMERIC(12,2)`, status; a separate V1-PILOT DDL defines UUID/versioned courses. Neither proves live schema or deployment.
- Existing API #75 tests and verification report document historical focused 27, linked 113, and full Study 872 passing with fake DB/session fixtures; tests were not run in this screen task, and these counts do not establish live DB, deployment, or runtime UI behavior.

## SOURCE_TRACE

```text
Expected: AD-07 numeric Course.id -> AD-08 load/re-read via GET #74 -> edit only owner-approved Course fields -> PUT #75 -> apply returned data or approved #74 revalidation -> return to AD-07/list.
Current: Study Web has no route/client; prototype form is disabled and static. Local Study API #75 accepts four DERIVED full-replacement fields, updates legacy metadata columns, reads Course projection via #74 and returns it in singleton Page<Course>; UI revalidation/cache and return route are not implemented or approved.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #75 body/validation | Catalog/AC omit body; local route/model/validator require title, description, thumbnail_url, price and candidate bounds. API DD `Draft — Needs Confirmation`. | `DISCREPANCY` / `DERIVED` | Must not present local fields/rules as approved; owner decisions block DD readiness. |
| Thumbnail/upload | Prototype describes disabled PNG/JPG upload and multipart lock; local #75 only accepts a nullable `thumbnail_url` string and has no multipart endpoint in the #75 module. | `UNSUPPORTED` | Upload constraints, provider, flow, and URL policy are unresolved; do not design an upload call. |
| Route and UI runtime | Proposed route in inventory; no Study Web app source/router/client; prototype back/cancel both target `/admin/courses`. | `UNWIRED` / `DISCREPANCY` | No runtime event is verified; correct destination and return behavior need a route contract. |
| Authorization | AC-32 says Admin with course-management permission; local #75 uses shared JWT `ADMIN` guard. | `OPEN` | Do not equate role with fine-grained permission. |
| Schema and response | Legacy BIGINT DDL versus V1-PILOT UUID/versioned schema; local #75 returns singleton Page<Course> readback via #74. | `OPEN` / `DERIVED` | Live schema and final mutation response cardinality remain unconfirmed. |
| Revalidation | Inventory says GET #74 → PUT #75 → revalidate #74; local #75 reads the updated projection and returns it. | `DISCREPANCY` | Confirm whether UI should use response, issue a second GET, or invalidate cache; no client policy exists. |

## CHANGES

- Files changed: AD-08 plan, DD, marker JSON/SVG, 2× annotated PNG; AD-08 inventory row and API #075 reverse index; global screen plan/checkpoint; final AD-08 worklog.
- CONTEXT_UPDATES: none.
- Context pages changed: none.
- Assumptions: none.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type docs --limit 3` | `READY`, 3/213 exact-type docs worklogs selected; all selected worklogs read in full. | VERIFIED |
| `identify` + `sha256sum` for AD-08 source assets | 1385×1600 screenshot; both source hashes recorded above. | VERIFIED |
| HTML parser inventory of interactive tags | 21 anchor/button/form/input/select/textarea nodes; disabled form fields and Save; no fetch/axios/XHR/handler code. | VERIFIED |
| Study Web source-file search | No package/router/entrypoint/app source outside docs/assets, ignored `dist`, and `node_modules`. | VERIFIED (`UNWIRED`) |
| API #75 route/model/validator/view/query/DD/tests + schema candidate review | Local route/module and historical fake-DB test report found; catalog/body and schema/live-state discrepancies recorded above. | VERIFIED (source review only; tests not run) |
| AD-08 artifact audit | 61 sequential unique marker JSON/SVG entries; all coordinates in source bounds; SVG circles match JSON; C table has exactly 61 sequential rows; A–F present; local Markdown links resolve. | VERIFIED |
| Image/source audit | `screen.png` 1385×1600; `screen_annotated.png` 2770×3200; original screen/code hashes unchanged; annotated image reviewed after marker adjustments. | VERIFIED |
| Inventory/core bundle audit | 83 unique inventory IDs match 83 screen folders; 61/83 have all four core artifacts, 22 remain incomplete. | VERIFIED |
| `git diff --check` | No whitespace errors. | VERIFIED |

## HANDOFF

- Remaining work: none for AD-08. DD remains blocked on owner/API decisions; do not begin another Screen ID in this session. AD-09 is the next screen for a separate session.
- Next owner/action: continue AD-08.
