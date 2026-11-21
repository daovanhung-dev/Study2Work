---
task_id: "2026-11-07-design-study-screen-st06"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: ["static verification"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["AC-12; APIs #17/#18; ST-05 → ST-06 → ST-07 payment/enrollment flow"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study ST-06

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 233; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Keep expected/current behavior separate, preserve original assets, trace client-to-server through guard/query/effects/response/test, and do not infer provider, order, operation, or payment behavior from a mockup.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Recheck Study Web wiring each screen session; distinguish API catalog/Draft DD from current route and test source; fake-session tests and checked-in schema do not prove live runtime/deployment.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Preserve identity/ID handoffs and privacy/security blockers; label prototype controls static/unwired; use exact source for fields and statuses; stop after one Screen ID.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Continue the 83-screen objective with one Screen ID only; read current screen inventory and contracts; save `<SCREEN_ID>_PLAN.md` before markers/render/DD; preserve source assets; author A–F with 1:1 marker mapping, traceable events/API/state/navigation; update inventory/global plan/worklog; perform static audit; do not start another Screen ID in this session.
- Canonical contract/approved DD: Inventory row 20 defines ST-06 “Thực hiện thanh toán”, candidate `/student/pay/:orderId`, AC-12, APIs #17/#18, links ST-07 and SH-07, states pending/running/failed/cancelled/succeeded; inventory requests safe retry. It describes POST #17 → operation_id → conditional GET #18 and says client callback is not proof of payment. AC-12 expects payment gateway success to continue to enrollment and failure/cancel to stop the flow. API #17/#18 catalog and Draft DD remain contract evidence, not runtime proof.

## CURRENT_BEHAVIOR

- Source/config: ST-06 source assets are only `screen.png` (1280×1024; SHA-256 `d1dc527fdad7c423a42aa6eac0caf57137ad7eebe3e7c6184f55c79b00289a36`) and `code.html` (9,303 characters; SHA-256 `c74f162474fdaed4708d6a5f049b47e0552fa8da04a5e9748416abd1bbdc3c2b`). Original PNG is almost blank. HTML is static public shell/status content with 15 anchors and no form/control, API call, event attribute or handler; the return CTA uses literal `/student/checkout/:courseId` while breadcrumb uses `/student/checkout`.
- Runtime wiring: Study Web has docs/dist/node_modules only and no editable `src`, router, or package manifest. Current Study Server search found no #17/#18 route/module/query/test. API #17/#18 are catalog/Draft DD only.
- Data boundary: API #17 requires Student Bearer, `{order_id:int64!,provider:string!}`, returns 202 `DESIGN_OPERATION_ACCEPTED`/`ApiEnvelope<Operation>`, and declares 401/403/422/503/500. API #18 GET accepts `operation_id:int64` in its row and returns 200 Operation with 401/403/404/500, but shared convention/Operation schema/AC-12 use UUID; owner-only versus owner/Admin also conflicts. Neither API is wired.
- AC-12 sequence: #17 → payment gateway → decision success/failure; #18 node appears separately and is not connected to the sequence. The catalog does not define polling cadence or retry/idempotency behavior.
- Checked-in `payments` DDL has no `order_id`; there is no Study Order or Operation table in the reviewed ERD/DDL. `payments.user_id/course_id` are nullable in DB.sql while DB_UNICA_TABLES says required. Live DB/deployment are unverified.
- No application tests or runtime have been run in this session.

## SOURCE_TRACE

```text
Expected: ST-05 approved Order handoff → POST #17 with `order_id` and approved provider → receive Operation → conditional GET #18 → trusted gateway/payment result → ST-07 server-verified enrollment result.
Current: static ST-06 HTML has no payment data or caller; #17/#18 are unwired. ST-05 uses logical Order `data.id`; API #17 expects `order_id:int64`. #17 Operation uses UUID ID in shared schema, while API #18 row expects int64. Do not infer payment success, retries or identifier continuity.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| ST-06 API/flow | Catalog and Draft DD #17/#18 plus AC-12 reviewed; #18 UUID/int64, owner policy, lifecycle, result and #17 gateway/provider/order mapping remain open. | `DISCREPANCY / DESIGN_ONLY` | Do not invent provider, gateway, polling cadence, retry/idempotency, callback verification, paid-status, or ID mapping. |
| Study Web route/runtime | Current app tree has no editable source/router/package manifest; candidate `/student/pay/:orderId` is not wired. | `UNWIRED / NOT_FOUND` | No implementation/runtime claim. |
| Screen assets and return links | Original screenshot is almost blank; HTML renders a static payment-not-found/finished state. CTA uses literal route template and breadcrumb omits ID. | `DISCREPANCY` | Preserve assets; use a separate HTML render only after plan; do not interpolate guessed IDs. |
| Retry requirement | Inventory requests safe retry; #17/#18 contracts and Draft DD do not define idempotency, status preconditions or retry safety. | `DISCREPANCY / SOURCE_REQUIRED` | Document retry as blocked, not as implemented behavior. |

## CHANGES

- ST-06 assets authored: `ST-06_PLAN.md`, `ST-06.md`, `ST-06_markers.json`, `ST-06_markers_overlay.svg`, `screen_rendered_from_html.png`, and `screen_annotated.png`.
- Original `screen.png` and `code.html` were preserved. Rendered image and annotation are separate derived assets.
- Updated ST-06 inventory row in `apps/study-client/docs/list_screen.md`; API reverse-index rows remain `D` because #17/#18 are catalog/Draft-only and unwired.
- Updated ST-06 row and appended the ST-06 checkpoint in `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`.
- Fixed one broken local link in `ST-06_PLAN.md` to the server-study route context.
- CONTEXT_UPDATES: none. Context pages changed: none. No application source or test files changed.
- Assumptions: none; unresolved contract decisions remain explicit blockers.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Goal/router/context/worklog preflight | Goal objective reread; root router, context map, exact-type docs worklog selection (`READY`, 3/233), and the three selected worklogs reviewed. | `VERIFIED_PREFLIGHT` |
| Screen/API/AC/source trace | ST-06 HTML/assets, inventory/global plan, AC-12, API #17/#18 catalog and Draft DD/open questions, Study Web tree, Study Server route/test search, Payment DDL/ERD, and ST-05 handoff reviewed. | `VERIFIED_STATIC_REVIEW` |
| Marker and document audit | JSON and SVG parse; 14 sequential unique marker IDs, in-viewport targets, non-overlapping callouts, 14 SVG groups/labels, and exact 1:1 mapping to 14 DD element rows. Six event sections EV-01…EV-06 and A–F sections present. Markdown local links resolve. | `PASS_STATIC` |
| Image/source preservation | Original `screen.png` 1280×1024 SHA-256 `d1dc527fdad7c423a42aa6eac0caf57137ad7eebe3e7c6184f55c79b00289a36` and `code.html` SHA-256 `c74f162474fdaed4708d6a5f049b47e0552fa8da04a5e9748416abd1bbdc3c2b` unchanged. HTML render and annotation are 2560×2048; render SHA-256 `e85a80b20fbf23451ada56ce78ce8b2146ae3816eec308c46e9d14a7944c6a4e`; annotation SHA-256 `1e68414509dc9ee4b52b600d5084b66c58ddfa2614eabf7d3bd44d150f31f4cc`. Annotation visually reviewed. | `PASS_STATIC` |
| Inventory/artifact audit | 83 inventory IDs match 83 screen folders; 81/83 have all four core artifacts; remaining IDs are ST-01 and ST-07. | `PASS_STATIC` |
| Scoped `git diff --check` | Run after ST-06 DD, plan, tracker and worklog updates. | `PASS` |
| Application tests/runtime | Not run; this is a documentation task and #17/#18/Study Web remain unwired. | `NOT_RUN` |

## HANDOFF

- ST-06 documentation and assets are complete for this session; design remains `DD BLOCKED`, implementation is `IMPLEMENTATION BLOCKED`, and runtime is `NOT VERIFIED` until the payment and Operation blockers above are resolved.
- No context pages changed, so `node scripts/validate-agent-context.mjs` was not needed.
- Stop after ST-06. ST-07 is the next screen in the AC-12 flow and must be handled in its own session.
