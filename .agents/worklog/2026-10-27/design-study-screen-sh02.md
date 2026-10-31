---
task_id: "2026-10-27-design-study-screen-sh02"
date: "2026-10-27"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["Study Web SH-02 -> API #03 login -> API #04 Student profile; source-only R-X01 refresh"]
status: "VERIFIED"
---

# Worklog: Thiết kế Study Web screen SH-02

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-27/design-study-screen-sh01.md`
    - carry_forward: SH-01 V5 đã bàn giao; dùng cùng Study ocean palette/brand mark nhưng thiết kế auth cần art direction riêng. Không coi resource design là frontend runtime.
  - path: `.agents/worklog/2026-10-27/study-web-design-guide.md`
    - carry_forward: `.agents/web-study/design.md` là visual target canonical; không thêm font mạng, giữ accessible contrast và 4px rhythm.
  - path: `.agents/worklog/2026-10-25/load-study-server-context.md`
    - carry_forward: Ưu tiên source hiện hành; source/tests cục bộ không chứng minh live DB/deployment.
- shortage: `none` (133 worklog docs khả dụng; đã đọc đủ 3)

## EXPECTED_BEHAVIOR

- Requirement: Theo inventory, thiết kế đúng SH-02 Đăng nhập (`/login`, Guest, AC-02, P0), một screen/phiên; tạo PLAN, ảnh đánh số từng element, SCREEN.md dạng bảng cụ thể, source và ZIP dưới `apps/study-client/docs/dd_screens/resource/SH-02/`.
- Canonical target: `.agents/web-study/design.md` và SH-02 row/F01/state rules trong `apps/study-client/docs/dd_screens/list_screen.md`; API catalog/DD #03 status cần giữ `DISCREPANCY` rõ ràng.

## CURRENT_BEHAVIOR

- Source/config: `find apps/study-client -maxdepth 4 -type f` chỉ thấy inventory/docs/resource đã tạo cho SH-01; không có Vue app source/router hay client auth persistence. SH-02 route là design target.
- API #03: route public `POST /api/v1/auth/login`, JSON `email/password`; current view trim/validate email max 255, từ chối password whitespace-only, active account check, password verify, issue access/opaque refresh tokens, lưu refresh hash rồi commit. Current source success `200 DESIGN_RESOURCE_RETRIEVED` với safe profile + token fields; 401 credentials, 403 mọi status không ACTIVE, 500 safe internal. API DD/catalog normative còn lệch: 201 `DESIGN_RESOURCE_CREATED`, profile-only; errors 422/500. DD #03 `Draft — Needs Confirmation`.
- API #04: `GET /api/v1/users/me` yêu cầu Bearer JWT và role `STUDENT`; role khác trả 403 trước DB access. Current profile source không có `bio`. `R-X01 /auth/refresh` có source nhưng không có catalog API ID/contract.
- Runnable tests: Đã đọc API #03 và #04 test source; không chạy tests (docs/design task). Tests dùng fake DB/current route evidence, không chứng minh live DB/deployment.
- Runtime wiring: `app/api/v1.py` đăng ký POST `/auth/login` và GET `/users/me`; Login view truy cập DB, verify credentials, tạo/persist refresh hash; #04 qua shared role-aware guard rồi query profile. Study Web consumer chưa có.

## SOURCE_TRACE

```text
SH-02 -> POST #03 -> Student only: Bearer GET #04 -> safe internal destination; Mentor/Admin -> G-02 BLOCK; R-X01 refresh remains source-only
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Study Web route/consumer | Current client tree lacks `src`, router and auth API client. | `SOURCE_REQUIRED` | Deliverable marked `DESIGN_TARGET / NOT_IMPLEMENTED`. |
| API #03 success/error contract | Catalog/DD normative: 201/profile-only/422+500; current route: 200/profile+token fields/401+403+500. | `DISCREPANCY / Draft — Needs Confirmation` | Document both; do not author a new API contract or silently resolve status/schema. |
| Role bootstrap | API #04 shared guard only permits STUDENT; inventory G-02 blocks Mentor/Admin. | `BLOCK` | Do not route non-Student to Student `/me` or invent a role dashboard/success state. |
| Client token storage/session | Source emits tokens and supports refresh, but Study Web client/persistence policy absent; refresh has no catalog ID. | `SOURCE_REQUIRED / DISCREPANCY` | No storage mechanism, remember-me, logout or refresh transport invented in UI. |
| Return destination | Inventory §6.2 permits safe allowlisted relative route; frontend router absent and default target is pending. | `DESIGN_TARGET / OPEN_DECISION` | Do not allow external redirect; ST-01 `/student` is candidate, not approved runtime fact. |
| Study Web scope subcontext | `.agents/web-work/AGENTS.md` and INDEX link `.agents/web-work/study/AGENTS.md`, but that path is missing; `.agents/web-study/design.md` exists and was read. | `NOT_FOUND / CONTEXT_MAP_DRIFT` | Use existing canonical design guide; do not create/update broad context as part of UI-only screen task. |

## CHANGES

- Files created/updated: `apps/study-client/docs/dd_screens/resource/SH-02/PLAN.md`, `SCREEN.md`, `SH-02_clean.svg`, `SH-02_annotated.svg`, `SH-02_clean.png`, `SH-02_annotated.png`, `learning-book-hero.png`, `build.py`, `SH-02_design_handoff_v1.zip`; worklog này.
- CONTEXT_UPDATES: None; no architecture/route/API behavior changed.
- Context pages changed: None.
- Assumptions: Main screenshot shows the idle Guest login screen. Dynamic error/loading/role states remain in SCREEN.md. `returnTo` is safe relative/allowlisted only. No sample credentials or live data in image.
- Design-intelligence review: used `ui-ux-pro-max` form validation search; web findings recommend inline field errors plus focusable summary for multi-field validation; retained only because compatible with `meta.fieldErrors` and visible labels.
- Visual craft: applied `imagegen` to create a transparent custom open-book hero asset; composed it into the Study palette with code-authored SVG typography and components. Iterated after visual review: replaced generic vector book art, changed desktop frame from 1440×1320 to 1440×960, and rechecked all 17 callouts.
- Tool boundary: CUA reported no available apps/browsers and `createBrowserTab("chrome", ...)` reported Chrome unavailable. Therefore the ChatGPT website UI/ZIP download workflow was not used; image generation used the integrated imagegen tool, then a local Python/SVG generator and installed Chrome headless rendered and packaged the deliverable. No claim of ChatGPT website interaction.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| `git status --short --branch` | Existing untracked SH-01 resources and SH-01 worklog preserved; no tracked modifications before SH-02. | VERIFIED |
| `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3` and selected worklogs | Selected/read 3 exact-type entries; no shortage (133 available). | VERIFIED |
| `.agents/web-study/design.md`, SH-02 inventory/F01/state rules | Design target, route/API/dependency/state and security constraints read. | VERIFIED_STATIC_ONLY |
| Project/scope context + manifest | Read web-work and server-study context graph, cross-scope ownership and skill registry. Web Study subcontext referenced by web-work is absent; UI-only DD has no canonical createDD skill. | VERIFIED_STATIC_ONLY / NOT_FOUND |
| API #03/#04 route, models, validator, views, queries, shared auth/response, focused test source; DD #03 | Current request/source/HTTP branches and DD discrepancy reviewed; test source not executed. | VERIFIED_STATIC_ONLY |
| `ui-ux-pro-max` search (`form validation inline error summary`, domain `ux`) | Verified web result: inline field errors and focusable linked error summary for multi-error validation. | VERIFIED_STATIC_ONLY |
| Plan review | Detailed source-backed plan authored before composition; visual target, 17 target map, API discrepancies, responsive/accessibility and role blocker specified. | VERIFIED_STATIC_ONLY |
| `python3 apps/study-client/docs/dd_screens/resource/SH-02/build.py` | Generated exact SCREEN.md, clean/annotated SVG and 1440×960 PNGs; packaged ZIP with the source artwork and plan. Exit 0; Chrome headless renderer. | VERIFIED_ARTIFACT |
| Visual review (`view_image`) | Inspected clean and annotated renders at full resolution; adjusted viewport/layout/art; all callouts are unique and visually avoid the copy and controls. | VERIFIED_ARTIFACT |
| Static artifact audit (Python stdlib) | ZIP integrity passed; all 8 archive members byte-match their folder files; PNG dimensions verified; SCREEN.md contains 17 numbered element rows; annotated SVG contains markers #1–#17. | VERIFIED_ARTIFACT |
| ChatGPT website through @Chrome | CUA returned no browser surface; `createBrowserTab("chrome", ...)` unavailable. Integrated imagegen and local renderer used instead. | NOT_AVAILABLE |
| Tests | No project tests run; this is a design-document artifact task, not a client implementation. | NOT_RUN |

## HANDOFF

- SH-02 artifacts are complete and visually reviewed. Integrated imagegen plus the local SVG/Chrome-headless workflow was used because @Chrome CUA was unavailable; output provenance is recorded above.
- Remaining source/product decisions are not mocked as resolved: API #03 contract discrepancy, Student-only #04/G-02 for Mentor/Admin, token persistence and default destination remain explicit in `SCREEN.md`.
- Next screen in inventory order: SH-03 registration; continue the one-screen-per-session workflow.
