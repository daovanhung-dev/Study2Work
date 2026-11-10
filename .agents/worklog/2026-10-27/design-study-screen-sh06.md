---
task_id: "2026-10-27-design-study-screen-sh06"
date: "2026-10-27"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["Study Web SH-06 404 state -> API #08 GET /api/v1/courses/{course_id}; GS-01 course list; SH-01 public fallback"]
status: "PARTIAL"
---

# Worklog: Thiết kế Study Web screen SH-06

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-27/design-study-screen-sh01.md`
    - carry_forward: Dùng Study ocean tokens, shared brand mark và link rõ tới Home/course discovery; design resource là intended UI, không phải runtime. Giữ constraints source-backed về public course content.
  - path: `.agents/worklog/2026-10-27/design-study-screen-sh02.md`
    - carry_forward: Phân biệt UI target với current API source; giữ route/navigation target explicit, không invent auth/persistence. @Chrome trước đó không khả dụng; thử lại trong turn hiện tại.
  - path: `.agents/worklog/2026-10-27/design-study-screen-sh03.md`
    - carry_forward: Ghi discrepancy giữa inventory và API source; tạo plan trước ảnh; không biến email/registration placeholders thành runtime behavior.
- shortage: `none` (137 worklog docs khả dụng; đã đọc đủ 3 được chọn)

## EXPECTED_BEHAVIOR

- Requirement: Thiết kế đúng một screen trong phiên này theo inventory: SH-06 “Trang không tồn tại / tài nguyên không còn”, state view `/not-found`, AC-05, API #08. Tạo plan trước ảnh; xuất clean/annotated images (element markers), detailed Vietnamese `SCREEN.md` dạng bảng, editable sources và ZIP dưới `apps/study-client/docs/dd_screens/resource/SH-06/`.
- Canonical target: `.agents/web-study/design.md`; SH-06, GS-01/GS-03, F02, state matrix, 404/non-disclosure/navigation rules trong `apps/study-client/docs/dd_screens/list_screen.md`.
- Required distinctions: `route-404` và `resource-404` là biến thể; 404 không tiết lộ draft/private; không chuyển 500/service failure thành 404; recover về GS-01 hoặc SH-01.
- Scope: một screen state-view với các variants trong cùng folder; không thiết kế GS-01/GS-03 như screens riêng ở phiên này.

## CURRENT_BEHAVIOR

- Source/config: `apps/study-client/` contains `docs/dd_screens/list_screen.md` and design resources SH-01..SH-05 only; no Vue app entrypoint/router/API client is present. Current API #08 is implemented in `apps/study-server/app/modules/guest/api_08_courses_detail/`; `app/api/v1.py` imports/registers `GET /courses/{course_id}`.
- API #08 view: validates `course_id`; invalid ID returns HTTP 404 `DESIGN_RESOURCE_NOT_FOUND`. Query filters `courses.status = 'PUBLISHED'`; missing and non-published course rows both return the same safe 404. Query exceptions roll back and return safe 500 `DESIGN_INTERNAL_ERROR`; mapping failure also returns 500. Success is 200 with singleton `CoursePage` and a public mentor projection. The endpoint is read-only.
- Runnable tests: Read `apps/study-server/tests/modules/guest/api_08_courses_detail/test_courses_detail.py`; it covers invalid ID, missing row, query failure ->500, success mapping and route GET 200 using FakeSession/monkeypatch. Tests not run in this design task.
- Runtime/docs status: `.agents/server-study/apis/declared-routes.md` reports API #08 source/import/HTTP test wired; `apps/study-server/docs/dd/08_courses_detail/00_Cover.md` remains `Draft — Needs Confirmation`. `list_screen.md` still labels API #08 `D` and GS-03 says #08–#10 are not wired. This is a documented discrepancy; source wins for current API behavior, but live schema/deployment is not established.
- Runtime wiring: Study Web `/not-found` route and consumer are absent. Route 404 can be a client router fallback; resource 404 can be mapped from API #08 404. API 500/network must remain service-error handling, never be rendered as SH-06.

## SOURCE_TRACE

```text
Expected route-404: unmatched Study Web route -> SH-06 ROUTE_NOT_FOUND -> GS-01 /courses or SH-01 /
Expected resource-404: GS-03 -> public GET #08 -> 404 for invalid/missing/unpublished -> SH-06 RESOURCE_NOT_FOUND
Current: app/api/v1.py route -> get_course_detail -> parse course_id -> SELECT only PUBLISHED + public mentor -> singleton CoursePage / safe 404 / safe 500; no Study Web caller/router in checkout
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Study Web router/client | Scoped file inventory currently contains no app source/router. | `NOT_FOUND / SOURCE_REQUIRED` | UI route, history and navigation are design targets, not implementation. |
| API #08 source vs screen inventory | Current `app/api/v1.py`, module view/query/validator and test source show a registered public route; inventory API list marks #08 `D` and GS-03 says #08–#10 not wired. API DD is Draft. | `DISCREPANCY` | Use current source for 404/500 behavior; preserve DD/inventory uncertainty and no live-schema claim. |
| API #08 success schema | Current source returns one course inside `CoursePage`; inventory G-06 notes singleton `Page<Course>` discrepancy for detail. | `DISCREPANCY / DRAFT` | SH-06 renders no course payload; do not invent course title/thumbnail on 404. |
| API #08 unpublished privacy | Query filters only `PUBLISHED`; missing and unpublished both map to same 404. | `SOURCE_BACKED` | Keep resource copy generic and identical for missing/unpublished; never expose draft/private status. |
| 500 vs 404 | Query/mapping failures are safe `500 DESIGN_INTERNAL_ERROR`, distinct from resource-not-found. | `SOURCE_BACKED` | Route API 500/network to service error; never convert to SH-06. |
| ChatGPT @Chrome | CUA `getState()` returns no apps/browsers; `createBrowserTab("chrome", ...)` says Chrome unavailable (repeated from SH-05). | `TOOL_UNAVAILABLE` | Local design/export can continue, but no ChatGPT website artifact may be claimed. |

## CHANGES

- Files changed: `.agents/worklog/2026-10-27/design-study-screen-sh06.md`; `apps/study-client/docs/dd_screens/resource/SH-06/PLAN.md`; `SCREEN.md`; `build.py`; transparent paper illustration; 12 editable SVG views; 12 PNG views; `SH-06_design_handoff_v1.zip`.
- CONTEXT_UPDATES: None planned; no runtime contract/source change.
- Context pages changed: None planned; this is a UI-only design artifact.
- Assumptions: Client routes/navigation remain design targets because Study Web source is absent. API #08 behavior follows current server source; inventory/DD discrepancy remains explicit. Keep route/resource 404 copy generic and avoid fabricated backend details.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| `git status --short --branch` | `develop...origin/develop`; existing SH-01..SH-05 worklogs/resources are untracked and preserved. | VERIFIED |
| `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3` | Selected/read SH-01, SH-02, SH-03 worklogs; 137 available, no shortage. | VERIFIED |
| Global context, context map, worklog README/TEMPLATE, web/server context indexes | Read task routing, scope and cross-scope page graph. `.agents/web-work/study/` entry referenced by map is absent from current filesystem; UI-only DD has no canonical skill in manifest. | VERIFIED_STATIC_ONLY / NOT_FOUND |
| `.agents/web-study/design.md`, inventory SH-06/GS-01/GS-03/F02/state rules | Read canonical visual tokens and required 404/non-disclosure/navigation distinctions. | VERIFIED_STATIC_ONLY |
| API #08 route/view/query/validator/models and test source | Verified current route registration in `app/api/v1.py`; source filters `PUBLISHED`, maps invalid/missing/unpublished to 404, DB/mapping failure to 500; tests cover the branches with fakes. Tests not run. | VERIFIED_STATIC_ONLY |
| API #08 DD/catalog vs inventory | DD cover remains Draft; inventory marks #08 `D` and GS-03 says not wired; current route source and `.agents/server-study/apis/declared-routes.md` say wired/tested. Singleton `CoursePage` discrepancy recorded. | DISCREPANCY |
| SH-01 related screen | Read SH-01 SCREEN.md; brand/Home and `/courses` destination patterns reviewed. | VERIFIED_STATIC_ONLY |
| ChatGPT via @Chrome | `getState()` has no browser; `createBrowserTab` unavailable. Retried this turn. | NOT_AVAILABLE |
| `PLAN.md` | Detailed plan created before any image generation; separates route-404/resource-404, shows current API 404/500 semantics, 12 element target map, route links and mobile layouts. | VERIFIED_STATIC_ONLY |
| `ui-ux-pro-max` search and Study design guide | Search recommends helpful recovery action for empty/error states and a minimal, spacious style; canonical Study tokens and interaction/accessibility guidance remained authoritative. | VERIFIED_STATIC_ONLY |
| `python3 build.py` | Generated 12 editable SVGs and 12 PNGs for two states at 1440×960, 390×844 and 320×844. | VERIFIED |
| Visual audit/fix | Reviewed clean route desktop/mobile/compact, resource desktop/mobile/compact, and annotated views. First compact annotation placed markers too close to text; moved leader endpoints to component bounds and reduced compact badges to 16px. A second pass moved one obscured accent dot to the halo edge. Re-rendered and checked both states; text, CTA, brand and art remain visible without marker overlap and all dots remain visible. | VERIFIED_VISUALLY |
| SVG/PNG integrity | Python standard-library check parsed 12 SVGs, verified exactly 12 markers only in annotated variants, verified each paper asset reference, PNG signatures and all canvas dimensions. | VERIFIED |
| ZIP integrity | `SH-06_design_handoff_v1.zip` contains 28 files under `SH-06/`; `ZipFile.testzip()` returned no corrupt entry. | VERIFIED |
| ChatGPT via @Chrome | Rechecked CUA app/browser inventory: empty; Chrome tab creation unavailable. Tool inventory exposes no alternative browser/Playwright surface. | NOT_AVAILABLE |

## HANDOFF

- Screen deliverable is complete as a local design handoff. The user's requested ChatGPT website prompt/download workflow remains incomplete because `@Chrome` is unavailable; no ChatGPT website authorship is claimed.
- Overall screen-design goal remains active. Next screen in a later session: SH-07 per `list_screen.md`, after the browser surface is available or with the same provenance limitation explicitly noted.
