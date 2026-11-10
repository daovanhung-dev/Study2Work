---
task_id: "2026-11-07-design-study-screen-st05"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: ["static verification"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["AC-12; APIs #08/#16; ST-04 → ST-05 → ST-06 → ST-07 → ST-08 enrollment flow"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study ST-05

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 232; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Keep expected/current evidence separate, trace current source and API effects, preserve original assets, and do not claim UI/runtime or test behavior from design/static artifacts.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Do not infer fields or business rules from a mockup; compare catalog/API DD with current route, auth, query, response and test source; fake sessions and source tests do not establish live DB/deployment.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Use registry to identify UI-only DD skill boundary; preserve exact ID handoff and security/PII blockers; document current source discrepancies, not assumptions.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Continue the 83-screen goal with ST-05 only in this session. Read current inventory/AC/API/source, write `ST-05_PLAN.md` before annotation/DD artifacts, preserve source assets, map every visible element 1:1 to markers and DD, author A–F with detailed event/API/state/route traceability, update inventory/global plan/worklog, run static checks, and keep DD/implementation/runtime states distinct.
- Inventory row 19: ST-05 “Kiểm tra đơn hàng / checkout”, candidate route `/student/checkout/:courseId`, AC-12, APIs #08 and #16; show amount/provider and require explicit confirmation before creating Order; revalidate #08 then POST #16 once per user action; keep `order_id`; links to ST-06 and ST-04; expected states `confirming/order-creating/422/order-error`; P2. The current tracker gate says Order table and payment policy lack source-backed evidence.
- Current global plan row ST-05: W2/P2, APIs #08/#16, `CHƯA_BẮT_ĐẦU`; gate says Order table/payment policy unproven. AC-12 and #16 catalog/API DD determine expected contract; current server source must be checked independently.

## CURRENT_BEHAVIOR

- Target folder `apps/study-client/docs/screen_stitch/03_student/ST-05_kiem-tra-don-hang-checkout/` contains only `screen.png` (1280×1024; SHA-256 `9f03e86f469e9d09a1cb9cdeb5486a56f84343dc0067d80cafe7a8925e225657`) and `code.html` (9,096 characters; SHA-256 `21a1cc9001c2051c46c0cf1db4b66e6f0262bc2046e9206f956bca2716fe77fa`). No ST-05 plan/DD/marker/annotated image existed at preflight.
- `screen.png` is almost blank and cannot serve as an element map. The HTML is a static public shell with breadcrumb and payment-unavailable status card; it has no form, button, input, fetch/XHR, API path, or client event handler. Its CTA says return to enrollment check but links to `/courses`.
- Study Web contains `docs`, `dist`, and `node_modules`, with no editable `src`, router, or package manifest; checkout route is not wired. Study Server has source-backed read-only API #08 route/module/query/test, but no API #16 `/orders` route/module/query/test was found. API #16 remains catalog/Draft design only.
- AC-12 requires an authenticated Student; its sequence reads #08 and #15 before branching to the free or paid path. The inventory also requires a second #08 revalidation before user-confirmed #16; AC-12 does not specify that second call or stale-price behavior.
- API #16 contract: Student Bearer JWT; request `{course_id:int64!, payment_provider:PaymentProvider!}`; successful response is logical Order `{id,course_id,user_id,amount,currency,status,created_at}` with 201 `DESIGN_RESOURCE_CREATED`; catalog errors are 401/403/422/500. AC-12 sets initial Order `PENDING` in the paid branch. Provider values/meaning, amount/currency source, Order table/columns/constraints, transaction, idempotency, and direct-call eligibility are unresolved. ERD V1 and checked-in `DB.sql` have no `orders` table; `payments` is a separate later API #17 concept. Live DB/deployment are unverified.
- No tests or application runtime have been run in this session.

## SOURCE_TRACE

```text
Expected boundary: ST-04 / courseId → inventory-specified #08 revalidation → approved checkout/order terms → explicit Student confirmation → one POST #16 action → retain contract `data.id` as the order identifier only after mapping is approved → ST-06 handoff.
Current boundary: prototype shows a static payment-unavailable state and `/courses` CTA; no confirm control or current #16 caller/runtime exists. API #08 is read-only and source-backed; #16 order creation, persistence and live schema are not.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #16 / order and payment contract | Catalog, AC-12, API #16 Draft DD, route search, ERD/table index, and checked-in DDL reviewed. | `DISCREPANCY / BLOCKED` | Preserve catalog's provider field and limited errors; do not infer provider values, pricing, currency, schema, duplicate semantics, retries, or persistence from mockup/`payments`. |
| Study Web route/runtime | Current app tree has no editable source/router/package manifest; no ST-05 UI route is wired. | `UNWIRED / NOT_FOUND` | Candidate inventory route remains design-only. |
| Original screenshot vs HTML | Hashes and HTML structure reviewed; original screenshot is almost blank while HTML contains static error UI. | `DISCREPANCY` | Keep original assets; derive a separate visual render from HTML only after ST-05 plan is saved. |
| Revalidation sequence | Inventory requires a second #08 read before #16; AC-12 only places #08 before #15/branch. | `DISCREPANCY / SOURCE_REQUIRED` | Record the inventory sequence as target and the unspecified AC timing/staleness rule as a blocker; do not reconcile by inference. |

## CHANGES

- Files changed: this worklog; ST-05 plan, DD, markers JSON/SVG, HTML-derived render and annotated image; ST-05 inventory row; global screen plan row/checkpoint.
- Original `screen.png` and `code.html` remain unchanged. Render SHA-256 `e64076e96e4dc62ca856c28c683821274d7c591806c7084495ac2d107b344f07`; annotated SHA-256 `9f11165765094c6d6be5943d09bc4fbf8686e37f0feb5d023f5c954f1fe2626a`.
- CONTEXT_UPDATES: none.
- Context pages changed: none.
- Assumptions: none. Open contract issues remain explicit blockers; no implementation behavior was inferred.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Goal/router/context/worklog preflight | Goal objective, root router, `.agents/AGENTS.md`, context map, worklog contract/template reviewed; exact docs selector `READY` 3/232; AD-01, AD-02, AD-03 worklogs read fully. | `VERIFIED_PREFLIGHT` |
| Context/skill registry | Cross-scope project index/dependency/contract pages and web/study/server-study context loaded; manifest confirms `createDD-markdown` excludes web-UI-only DD. | `VERIFIED_PREFLIGHT` |
| Screen/API/AC/source trace | Current HTML, #08 route/module/query/test source, #16 catalog/DD, AC-12, current route tree, ERD/table index and checked-in DDL reviewed. | `VERIFIED_STATIC_REVIEW` |
| HTML-derived render | Chrome headless CDP at 1280×1024 CSS, scale 2; `document.readyState=complete`, fonts loaded, Tailwind CDN present; generated separate 2560×2048 render. | `VERIFIED_STATIC_RENDER` |
| Marker/DD alignment | 13 sequential unique markers, centers in bounds/non-overlapping, 13 SVG groups, 13 matching DD element IDs; all local Markdown links resolve; marker JSON parses and overlay SVG parses. | `VERIFIED_STATIC_AUDIT` |
| Image/source preservation | Original PNG 1280×1024 and HTML hashes unchanged; derived render and annotated image 2560×2048; annotated image visually reviewed. | `VERIFIED_STATIC_AUDIT` |
| Inventory/artifact count | 83/83 inventory IDs have folders; four-core-artifact count 80/83; incomplete IDs ST-01, ST-06, ST-07. | `VERIFIED_STATIC_AUDIT` |
| Diff/whitespace | Scoped `git diff --check` clean; newly authored text files have no trailing whitespace. Existing `list_screen.md` lines 3–6 retain prior trailing spaces; source `code.html` has no final newline and is unchanged. | `VERIFIED_STATIC_AUDIT` |
| Application tests/runtime | Not run, per docs task scope. | `NOT_RUN` |

## HANDOFF

- Remaining blockers: Order schema/constraints/transactions/idempotency; provider enum and #17 relationship; amount/currency/stale-price policy; direct-call eligibility; inventory-vs-AC-12 #08 revalidation order; Student route/auth guard; explicit confirmation UI; CTA return path; #16 runtime and `data.id`→`order_id` handoff.
- Stop after ST-05; ST-06 is the next flow screen for a separate session.
