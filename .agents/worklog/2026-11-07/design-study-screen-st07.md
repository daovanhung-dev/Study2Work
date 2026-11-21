---
task_id: "2026-11-07-design-study-screen-st07"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: ["static verification"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["AC-12; APIs #18/#19/#20; ST-06 → ST-07 → ST-08/#20 payment/enrollment flow"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study ST-07

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 234; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Keep expected/current behavior separate; inspect Study Web wiring each session; trace caller through backend/auth/query/effects/response/test; preserve source assets and avoid claims from static mockups or API catalogs.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Compare API catalog/AC with current route/source and response; retain policy/identity gaps; use exact field semantics; do not claim fake tests prove live schema or deployment.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Preserve numeric identity handoffs only where source-backed; separate catalog/Draft from runtime; retain route/PII/policy discrepancies; do not infer actions or fields from prototype assets.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete ST-07 only in this session; inspect the inventory, global plan and current assets/contracts/source; write `ST-07_PLAN.md` before marker/render/DD work; preserve original assets; create/verify an ordered 1:1 marker map and annotated image; author A–F DD with source-backed events, API boundary, states, navigation and blockers; update ST-07 inventory row, global plan checkpoint and this worklog; distinguish `DD READY`, `IMPLEMENTATION BLOCKED` and `RUNTIME VERIFIED`.
- Canonical contract/approved DD: Inventory row 21 names ST-07 “Kết quả đăng ký khóa học”, candidate `/student/enroll/result/:courseId`, AC-12, APIs #18/#19/#20, links ST-08 and ST-09, and states awaiting-confirmation/enrolled/conflict/failure. It says only after the backend proves free/paid entitlement should #19 create enrollment; #20 then refreshes My Courses. AC-12 paid flow requires trusted payment success before enrollment; API #18 ID/access/lifecycle and #19/#20 contracts must be checked against current source.

## CURRENT_BEHAVIOR

- Source/config: ST-07 folder initially contains only `screen.png` (1280×1024; SHA-256 `d667f387fcecd0eb4bfe048a048932f4d555c9c3872018b69f4941dbca4d6500`) and `code.html` (8,913 bytes; SHA-256 `c2661fe474dd1d0ed0f50dafca99310e2ec681899bb55ae554337a0c05436c58`). Original PNG is nearly blank. HTML shows a static public shell/card: “Chưa thể xác nhận kết quả đăng ký.”, supporting copy that activation is not recorded, and a static “Về khóa học của tôi” link to `/student/courses`. It has 14 literal anchors, no form/input/button/select/textarea, no event attributes/listeners and only a Tailwind config script; no API call or dynamic result mapping. It uses remote Plus Jakarta Sans/Material Symbols and Tailwind CDN, outside the Study Web guide's no-new-remote-import target.
- Runtime wiring: Study Web context/tree says documentation/assets, ignored `dist` and dependencies only; editable app source/package/router is absent and serving is unverified. Current Study Server `app/api/v1.py` composes APIs through #98; exact route/source/test scans found no #18, #19 or #20 endpoint/module/query/model/focused test. #19/#20 API DDs mark `UNWIRED / NOT_FOUND`; API #18 is likewise absent. Tests were read/search-only; none were run.
- Data/persistence: API catalog #19 is POST `.../courses/{course_id}/enrollments`, Student Bearer, path and body both declare `course_id:int64`, body additionally says `user from JWT:string`, 201 `DESIGN_RESOURCE_CREATED`, `ApiEnvelope<Enrollment>`, errors 401/403/404/422/409/500. AC-12 expects Enrollment + Progress initialization in one transaction with duplicate prevention. #19 Draft DD leaves identity wire field, eligibility/404, duplicate/concurrency/409, lesson set/defaults/status/timestamps and DB nullability open. API #20 is GET `/users/me/courses`, Student Bearer, optional `status:string` and `page:int32`, response `ApiEnvelope<UserProfile>`, errors 401/403/422/500; AC-13 expects an Enrollment + Course list, with progress fetched separately by #21. #20 DD leaves response/pagination/empty/filter/JWT binding open. Checked-in DDL defines `enrollments` and `lesson_progress`; table docs say FK columns are required but SQL leaves them nullable and has no enrollment pair unique constraint. DDL defaults are design evidence only; live DB is unverified.
- Cross-screen context: candidate route carries `courseId`; it carries no `operationId`. ST-06 expects a trusted payment outcome before ST-07 but its #18 identifier/access/lifecycle and handoff remain unresolved. AC-12's sequence is #19 → Enrollment/Progress transaction → #20 → “Đã đăng ký”/open course; #18 is a detached node, and AC-12 has no explicit ST-07 route/UI step. Inventory adds ST-07 and states awaiting-confirmation/enrolled/conflict/failure. Keep this as a `DISCREPANCY`; do not invent a second enrollment POST, payment status mapping, or course-detail target.
- Runnable tests: no #18/#19/#20 focused tests found by route/test inventory; no tests run in this docs session.

## SOURCE_TRACE

```text
Expected: AC-12 free branch or trusted paid confirmation → POST #19 creates Enrollment + Progress transaction → GET #20 reloads courses → display registered/open course. Inventory models this result surface as ST-07 and lists #18/#19/#20.
Current: ST-07 is a static, unconnected HTML page; Study Web has no route/client and Study Server has no #18/#19/#20 runtime route. #19/#20 are Draft-only and their response/data contracts are incomplete; #18 cannot be tied to route state because ST-07 route has only courseId.
DISCREPANCY: AC-12 result is a final sequence node, not an explicit ST-07 navigation; #18 is detached; `ApiEnvelope<UserProfile>` for #20 does not encode AC-13's course list. No inferred handoff or auto-submit can be treated as current behavior.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| AC-12 result vs ST-07 screen | AC-12 sequence performs #19 transaction, #20 reload, then displays “Đã đăng ký” and opens course; it has no explicit ST-07 route. Inventory separately assigns ST-07, includes #18, and adds awaiting-confirmation/conflict/failure UI states. | `DISCREPANCY / CONTRACT GAP` | Do not invent which screen owns #19, whether it auto-submits on route entry, or the failure/result handoff. |
| Payment Operation handoff | ST-07 route has `courseId` only; AC-12 #18 node is detached and API #18 row says int64 while AC/reusable Operation use UUID; owner/Admin policy/lifecycle are unresolved. | `DESIGN_ONLY / BLOCKER` | Do not call #18 without an approved operation ID, caller policy, status mapping and poll/terminal rules. |
| API #19 eligibility/idempotency | Catalog/Draft DD and AC-12 describe Student POST and duplicate prevention; exact course/payment entitlement guard, body identity field, duplicate predicate and 409/concurrency behavior remain open. DDL lacks pair uniqueness. | `DESIGN_ONLY / BLOCKER` | Do not auto-POST #19 from repeated page load; no safe retry or repeat semantics are established. |
| API #20 result mapping | Catalog/Draft DD returns `ApiEnvelope<UserProfile>` while AC-13 needs Enrollment + Course collection; status/page/empty/JWT binding are unresolved. | `DISCREPANCY / DESIGN_ONLY` | Cannot determine a course membership from the declared UserProfile response; do not gate “enrolled” on an invented shape. |
| Study Web/runtime and prototype | HTML has static unconfirmed copy and CTA only; candidate route/client is absent; source assets are static. | `UNWIRED / STATIC_ONLY` | Current copy is not evidence of enrollment failure or backend state; no runtime claims. |

## CHANGES

- ST-07 assets authored: `ST-07_PLAN.md`, `ST-07.md`, `ST-07_markers.json`, `ST-07_markers_overlay.svg`, `screen_rendered_from_html.png`, and `screen_annotated.png`.
- Original `screen.png` and `code.html` were preserved; the rendered image and annotation are separate assets.
- Updated ST-07 inventory row in `apps/study-client/docs/list_screen.md`; API #18/#19/#20 reverse-index rows remain `D` because their current Study runtime routes are absent and API DDs remain Draft.
- Updated ST-07 row and appended the session checkpoint in `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`.
- CONTEXT_UPDATES: none. Context pages changed: none. No application source/test files changed.
- Assumptions: none; unresolved decisions remain explicit blockers.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Goal/router/context/worklog preflight | Objective reread; root router, context map, worklog contract/template reviewed; exact docs selector `READY` 3/234; AD-01, AD-02 and AD-03 worklogs fully read. Registry confirms no skill applies to UI-only DD. | `VERIFIED_PREFLIGHT` |
| Screen/API/AC/source trace | ST-07 HTML/assets, inventory/global plan, AC-12/AC-13, API #18/#19/#20 catalog and Draft DD/open questions, Study Web tree/design guide, Study Server composition/route/test inventory, Enrollment/Progress DDL, and ST-06 handoff reviewed. | `VERIFIED_STATIC_REVIEW` |
| HTML rendering | Chrome 155 headless CDP, `file://code.html`, CSS viewport 1280×1024, DPR 2; `document.readyState=complete`, fonts loaded and Tailwind config present. Separate `screen_rendered_from_html.png` is 2560×2048. | `PASS_STATIC` |
| Marker/document audit | JSON and SVG parse; 13 sequential unique marker IDs; target bounds in viewport; marker circles do not overlap; 13 SVG groups/labels; exact 1:1 mapping to 13 DD element rows; A–F and EV-01…EV-07 present; local links resolve. | `PASS_STATIC` |
| Image/source preservation | Original `screen.png` 1280×1024 SHA-256 `d667f387fcecd0eb4bfe048a048932f4d555c9c3872018b69f4941dbca4d6500` and `code.html` SHA-256 `c2661fe474dd1d0ed0f50dafca99310e2ec681899bb55ae554337a0c05436c58` unchanged. Render SHA-256 `8b86fe81abb2cc75e062c6dddd015e17669abe0084ebe8fccc122bc6696ae140`; annotated PNG 2560×2048 SHA-256 `bd5f7f4ad0a1a1b0dc62f14b097e8cda99fa9cbbc19148a3cb32dc67ea8e9db3`; annotation visually reviewed. | `PASS_STATIC` |
| Inventory/artifact audit | 83 inventory IDs match 83 screen folders; 82/83 have all four core artifacts; only ST-01 remains incomplete. | `PASS_STATIC` |
| Scoped `git diff --check` and authored-text whitespace | Tracked inventory/global-plan diff clean; no trailing whitespace in ST-07 DD, plan, marker JSON/SVG or worklog. | `PASS` |
| Application tests/runtime | Not run; this is a docs task and routes #18/#19/#20 and Study Web remain unwired. | `NOT_RUN` |

## HANDOFF

- ST-07 assets and documentation are complete for this session. Design remains `DD BLOCKED`; implementation is `IMPLEMENTATION BLOCKED`; runtime is `NOT VERIFIED` until the enrollment/payment contracts and routes are resolved and wired.
- No context pages changed, so `node scripts/validate-agent-context.mjs` was not needed.
- Stop after ST-07. ST-08 is the next screen in a separate session.
