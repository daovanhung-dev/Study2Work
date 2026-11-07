---
task_id: "2026-11-07-design-study-screen-st04"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: ["static verification"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["AC-12; APIs #08/#15; GS-03 → ST-04 → ST-05 → ST-07 → ST-08 enrollment flow"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study ST-04

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 231; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Separate expected/current evidence; retain source assets; distinguish Study Web `UNWIRED` and catalog/API Draft from runtime; trace guard, query, effects and response; do not claim tests/runtime without executing them.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Do not infer fields or business rules from mockups; verify current caller/callee and validation; preserve API contract/source discrepancies and live-schema limits; no tests/runtime claim without evidence.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Keep role/identity policy and data mapping separate from local source; trace exact API and handoff; fake DB/test source does not establish live deployment; UI-only DD has no canonical skill.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete ST-04 only in this session; inspect current inventory/AC/API/source; save `ST-04_PLAN.md` before marker map, annotation or DD; preserve original assets; create ordered one-to-one markers and annotated image; author DD sections A–F with traceable elements/events/APIs/states/navigation/open decisions; update inventory, reverse API index, global screen plan and this worklog; keep DD, implementation and runtime statuses separate.
- Inventory row 18: ST-04 “Kiểm tra ghi danh trước đăng ký”, proposed `/student/enroll/:courseId`, AC-12, APIs #08/#15; display price, current entitlement and free/paid branch without claiming enrollment; GET #08 first and #15 only after backend confirms identity/selection; links ST-05, ST-07, ST-08; P1; API #15 is public in the catalog but does not identify a user.
- Global screen plan row ST-04: W2/P1 and `CHƯA_BẮT_ĐẦU`; current gate states API #15 is public but user identity is unspecified. Neighbor screens identify ST-04 as upstream of order/payment/result.
- Objective requires complete A–F, map every visible element to markers and detailed events, retain source assets, document blocker evidence, and verify artifacts before updating global progress.

## CURRENT_BEHAVIOR

- At task start, target folder contained only original `screen.png` (1280×1024, SHA-256 `7df0dac4e7598c3b336d5c5d78f5fd9a851526712aa7dd0fd7224a6ffe61ad7f`) and `code.html` (8,553 bytes, SHA-256 `24b0e361877b15db88298a29d806a2a17f0151e6685df71647d103477276f4fa`). `screen.png` is near-blank and does not match the complete static error page in `code.html`. This session added the plan, A–F DD, marker JSON/SVG, separate HTML render and annotated render; original assets remain unchanged.
- `code.html` renders a public Study shell, breadcrumb, centered card with “Kiểm tra ghi danh”, static “Chưa thể xác nhận thông tin ghi danh” text, explanatory copy, a single “Quay lại danh sách khóa học” anchor to `/courses`, and a footer. Header/footer links are static anchors. There is no form/input/button, fetch/XHR, router client or business event handler. Tailwind CDN/config and remote font links are present for styling.
- Current Study Web source is absent: no editable app entry/router/package/client exists in `apps/study-client`; ignored `dist` is not route evidence. The target route is a proposal and is `UNWIRED`.
- API #08 route/module/query/model/test source exists and is composed in `app/api/v1.py`. It is public GET by `course_id`; the current query selects only `PUBLISHED` courses and reads course fields plus mentor fields, returning a singleton `CoursePage` with decimal-string price. Invalid ID/not found map to 404; query/mapping errors map to 500. It is read-only. Current SQL uses `LEFT JOIN users`; shared mapper rejects missing mentor fields as a mapping error, while API #08 DD says `INNER JOIN`. Focused test source exists but was not run; tests use a fake session.
- API #15 is catalog/API-DD-only: Public GET, path `course_id:int64`, response `ApiEnvelope<Enrollment>`, 200/404/500. The response includes `user_id`, while the request has no identity field and a course can have multiple enrollments. Its Draft DD marks identity/row selection, 404 meaning, visibility and enum as open. No #15 route/module/query/view/model/test was found in current Study source.
- AC-12 expects an authenticated Student and an existing course: #08 → #15 → if already enrolled, My Courses; else free course → #19; paid course → #16 order → #17 payment → #18 operation → server-confirmed payment → #19 enrollment → #20 My Courses. The diagram itself includes a Public #15 with no identity input and an `operation_status` #18 node without a connection to the enrollment flow.
- Legacy `DB.sql` defines BIGINT `courses`, `enrollments` with nullable user/course IDs and opaque status; no unique user/course row rule is established there. V1-PILOT instead defines UUID versioned courses and `course_enrollments(learner_id,course_version_id)` with a unique pair. These are different design/schema artifacts; neither proves live DB mapping.
- Inventory row ST-04 is W2/P1. This session updated its status with API #08 `R`, #15 `D`, and `DD BLOCKED`; ST-05–ST-07 remain downstream screens for separate sessions.

## SOURCE_TRACE

```text
Expected: AC-12 Student login + existing course → public #08 course detail → public #15 existing-enrollment check → either already enrolled/My Courses, free/#19, or paid/ST-05 #16 → ST-06 #17 payment + conditional #18 → server-verified payment → #19 → #20/My Courses.
Current: no editable Study Web route/client. Static HTML displays only a generic inability-to-confirm status and back link. #08 is wired locally and returns published Course data; #15 is design-only with no current handler. No current server path implements the AC-12 status/order/payment/enroll chain.
DISCREPANCY: AC-12 requires signed-in Student and selects an Enrollment, but #15 is Public, takes only course_id and returns a user-scoped Enrollment with no unique selector. The source PNG is near-blank while HTML contains a complete error-state page.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| #15 identity and row selection | Catalog and AC-12 expose Public `course_id` only; response is one Enrollment with `user_id`; legacy schema has no established unique pair rule. API #15 Draft DD Q-15-01/Q-15-04 say source-required. | `DISCREPANCY / BLOCKER` | Cannot truthfully determine whether the logged-in Student has access or which enrollment to return; do not add JWT/query/user ID or choose a row by inference. |
| AC-12 actor vs prototype shell | AC-12 precondition is logged-in Student; HTML shows public nav with Sign In/Sign Up and a generic static error card. | `DISCREPANCY / DESIGN_ONLY` | Authentication/session guard and guest recovery behavior are not wired or defined by this screen. |
| #08 contract vs current source | Catalog/API DD declare `ApiEnvelope<Page<Course>>`; local route returns the singleton page with published price/status/mentor. API #08 DD says INNER JOIN, while local query uses LEFT JOIN and mapper rejects missing mentor. | `SOURCE_BACKED_WITH_DD_DISCREPANCY` | Use current source only as current behavior; preserve join behavior discrepancy and keep API DD Draft. |
| API/runtime flow | #08 route and test source exist; #15 and downstream #16/#17/#18/#19/#20 Student enrollment handlers are absent from current Study Server. | `PARTIAL / UNWIRED` | Do not claim end-to-end enrollment, payment verification or Enrollment mutation. |
| Image source | `screen.png` is 1280×1024 and visually near-blank; `code.html` contains a complete but static error-state page. | `ASSET_DISCREPANCY` | Preserve original PNG and render the valid HTML as a separately named evidence image for marker placement. |
| Schema/lifecycle | Legacy BIGINT `enrollments` and V1-PILOT UUID/versioned `course_enrollments` differ; no live schema/deployment check is present. | `SCHEMA_UNVERIFIED` | Do not map identifiers, enums or enrollment uniqueness across artifacts. |
| Study Web | Current editable Study Web source/router/package is absent. | `UNWIRED / NOT_FOUND` | Candidate `/student/enroll/:courseId` is not a current route; no runtime verification. |

## CHANGES

- Added `ST-04_PLAN.md`, `ST-04.md`, `ST-04_markers.json`, `ST-04_markers_overlay.svg`, `screen_rendered_from_html.png`, and `screen_annotated.png`. The blank original `screen.png` and HTML prototype remain byte-for-byte unchanged.
- Updated `list_screen.md` ST-04 row with separate #08 `R` / #15 `D` source statuses and the blocked DD state; updated API reverse-index #008 from `D` to `R` based on current local #08 route/module/query/model/focused-test source.
- Updated global `dd_screens/PLAN.md` ST-04 row and appended the session checkpoint; inventory/folders are 83/83 and core artifacts are 79/83.
- CONTEXT_UPDATES: none; no agent context page changed.
- No business or API behavior was inferred. DD remains blocked by #15 identity/selection and unresolved enrollment/payment contract.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Goal objective/router/context/worklog preflight | Objective, root router, `.agents/AGENTS.md`, `.agents/context-map.md`, worklog README/TEMPLATE and selected prior docs worklogs reviewed; selector READY 3/231. | VERIFIED_PREFLIGHT |
| Screen selection | Current plan/artifact audit shows ST-04 is the first missing W2/P1 enrollment prerequisite before ST-05–ST-07; ST-01 is W3 and separately gated. | VERIFIED_SELECTION |
| Source/contract review | AC-12, API #08/#15 catalog/DD, #08 current route/view/query/validator/model/mapper/envelope/test source, Student Web source boundary, and legacy vs V1-PILOT schema evidence reviewed. | VERIFIED_STATIC |
| Plan-before-artifact order | `ST-04_PLAN.md` was saved before rendering/marker/DD work; plan now records render provenance and measured targets. | VERIFIED |
| Render and original preservation | Chrome headless/CDP rendered 1280×1024 CSS at 2× into 2560×2048 after fonts loaded; original `screen.png` and `code.html` SHA-256 match preflight values. Render and annotated image visually inspected. | VERIFIED_STATIC |
| Marker/DD alignment | 13 markers are 1–13, unique, in bounds and non-overlapping; JSON coordinates equal SVG and map one-to-one to 13 DD element IDs. JSON and SVG XML parse. | VERIFIED_STATIC |
| Links/images/inventory | All local links in ST-04 plan/DD resolve; image sizes are valid; inventory and folders 83/83; core artifacts 79/83 (ST-01, ST-05–ST-07 missing at least one core asset). | VERIFIED_STATIC |
| Diff hygiene | `git diff --check -- apps/study-client/docs/list_screen.md apps/study-client/docs/screen_stitch/dd_screens/PLAN.md` passed; scoped custom whitespace/newline audit passed for new screen artifacts. | VERIFIED |
| Application tests/runtime | Not run; no test or live runtime result is claimed. | NOT_RUN |

## HANDOFF

- This session completed all planned ST-04 artifacts, inventory/API-index/global-plan updates, and static audit.
- Remaining ST-04 blockers: #15 identity and enrollment-row selection; AC-12 authenticated Student vs public #15/shell; #08 Draft INNER JOIN vs current LEFT JOIN + mapper error; missing #15/#16–#20 current runtime chain; legacy vs pilot schema difference; Study Web route/client absent. These keep DD and implementation blocked; runtime is not verified.
- Stop after ST-04. ST-05 is the suitable next Screen ID for a separate session; do not begin it here.
