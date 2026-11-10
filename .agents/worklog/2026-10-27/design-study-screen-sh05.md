---
task_id: "2026-10-27-design-study-screen-sh05"
date: "2026-10-27"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["SH-05 auth state -> API #04 GET /users/me; source-only R-X01 POST /auth/refresh; SH-02 login; SH-01 safe public fallback"]
status: "PARTIAL"
---

# Worklog: Thiết kế Study Web screen SH-05

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-27/design-study-screen-sh01.md`
    - carry_forward: Dùng đúng Study ocean tokens, 4px rhythm, shared brand mark; screen resources là design target, không chứng minh frontend runtime. SH-01 đã có CTA public có thể dùng làm safe fallback.
  - path: `.agents/worklog/2026-10-27/design-study-screen-sh02.md`
    - carry_forward: SH-02 là trang đăng nhập liên quan; tách API #03 login 401 khỏi API #04 403, preserve chỉ relative allowlisted return route. Client token storage/auth interceptor chưa được source-backed.
  - path: `.agents/worklog/2026-10-27/design-study-screen-sh03.md`
    - carry_forward: Worktree chưa có Study Web app/router; API source là current behavior, screen flows trong inventory là expected design target; giữ ranh giới `NOT_IMPLEMENTED`.
- shortage: `none` (136 worklog docs khả dụng; đã đọc đủ 3 được chọn)

## EXPECTED_BEHAVIOR

- Requirement: Thiết kế một screen trong phiên này: SH-05 “Không đủ quyền / session hết hạn”, state view `/forbidden`, AC-02/AC-11, kèm ảnh clean/annotated và `SCREEN.md` dạng bảng mô tả mọi element nhỏ, kích thước, typography, events, states, responsive; plan trước khi tạo ảnh; ZIP dưới `apps/study-client/docs/dd_screens/resource/SH-05/`.
- Canonical target: `.agents/web-study/design.md`; SH-05 inventory row, auth rules, state matrix, safe return guidance trong `apps/study-client/docs/dd_screens/list_screen.md`.
- Expected states: `401` may attempt runtime R-X01 refresh once then login preserving a safe internal return; `403` is access denied and must not loop refresh; `token-refresh-failed` has explicit recovery. Show 401 session, 403 access-denied and terminal refresh-failure as separate visual variants under the same screen folder. No child screens are listed.

## CURRENT_BEHAVIOR

- Study Web source: `apps/study-client/` currently contains the inventory and design resources only; no `src`, router, auth interceptor, token persistence or route guard. The `.agents/context-map.md` and manifest point to `.agents/web-work/study/*`, but that directory is absent in this checkout (`find` returned no directory). `.agents/web-study/design.md` exists and is the visual target.
- API #04 current source: wired `GET /api/v1/users/me`, one `Authorization: Bearer <jwt>`, no body/path/query. Shared auth validates bearer/JWT claims and requires `STUDENT` before profile query. Missing/malformed/invalid/expired token, invalid claims or missing user row -> 401 `DESIGN_AUTHENTICATION_REQUIRED`; a valid token without STUDENT -> 403 `DESIGN_ACCESS_DENIED` before profile query; query/mapping/config error -> safe 500 `DESIGN_INTERNAL_ERROR`. Read-only; no role/permission detail is exposed.
- R-X01 current source (not catalog API ID): `POST /api/v1/auth/refresh`, JSON `{refresh_token}`. Success 200 rotates the opaque refresh token atomically (revoke old + insert new hash + commit) and returns new auth payload. Invalid/missing/reused/expired refresh -> 401; inactive account -> 403; persistence/token failure -> safe 500. API #04 DD is Draft — Needs Confirmation; R-X01 has no separate API DD/catalog entry.
- Tests: Read API #04 tests and login/refresh tests; they use fake DB/session and verify auth/role/error branches and one-time atomic rotation. Tests not executed; they do not prove live DB/deployment or a Study Web consumer.

## SOURCE_TRACE

```text
SH-02 login #03 -> expected client token storage -> GET #04 /users/me
  -> missing/invalid JWT or missing user row: 401
  -> valid non-STUDENT role: 403 before profile query
  -> safe server/config failure: 500
401 handling expected by inventory: one coordinated R-X01 refresh -> success rotates old token, retry original once -> terminal SH-05/login on failed refresh
R-X01 current: invalid/replayed/expired token 401; inactive account 403; successful rotation is a DB mutation; no source-backed client caller exists.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Study Web implementation | No app source/router/auth client; despite `SOURCE_BACKED_SKELETON` entry in context manifest, required files and `.agents/web-work/study/` are absent. | `NOT_FOUND / SOURCE_REQUIRED` | All images/routes/actions are design target, not implementation. |
| Safe return behavior | Inventory requires preservation and general rule permits only allowlisted relative internal routes; no client implementation exists. | `EXPECTED_BEHAVIOR / SOURCE_REQUIRED` | Specify safe target/fallback, reject absolute/external targets; do not put tokens in URL. |
| R-X01 | Runtime refresh endpoint is wired but outside API V1 catalog and has no dedicated DD. | `SOURCE_BACKED / OUT_OF_CATALOG` | Keep retry/rotation semantics source-backed; preserve open client error mapping. |
| 403 provenance | API #04 403 means role lacks STUDENT; R-X01 403 means inactive account. | `DISCREPANCY` | Use generic access-denied copy; do not claim one specific cause or reveal roles/status. |
| Refresh failure UI | Inventory lists `token-refresh-failed`, but no UI/client consumer specifies 500/network mapping. | `SOURCE_REQUIRED / OPEN_DECISION` | Design a terminal, honest state without auto-refresh/retry loop; don't claim expiry unless response is 401. |
| API #04 contract | DD remains Draft; current missing-user->401 semantics and permission/claim details remain open. | `DRAFT / OPEN_QUESTIONS` | Keep copy generic; don't show permission fields or account lifecycle detail. |

## CHANGES

- Files changed: Worklog plus `apps/study-client/docs/dd_screens/resource/SH-05/`: `PLAN.md`, `SCREEN.md`, deterministic `build.py`, 12 editable SVGs, 12 PNGs (3 state variants × desktop/mobile clean/annotated) and `SH-05_design_handoff_v1.zip`.
- CONTEXT_UPDATES: None planned; no API/client runtime or route contract changes.
- Context pages changed: None.
- Assumptions: The 401 terminal view routes to SH-02 with only a relative allowlisted return destination. The 403 view never refreshes and goes to a safe previous route, with SH-01 as public fallback. Refresh failure is not described as token expiry unless it is specifically the refresh endpoint's 401 response. No logout, help-center, role switch, retry-refresh button, token display or account detail is invented.
- Design mode: Calm transactional system state in Study light-first ocean palette; use a custom vector access-threshold illustration rather than alarm/error-red decoration. Shared header/wordmark continues SH-01/02; content and art stay distinct from SH-04.
- ChatGPT authoring: Tried CUA `getState()` and `createBrowserTab("chrome", "https://chatgpt.com", ...)`; no browser surfaces were available and Chrome tab creation returned `Browser is not available: chrome`. Artifacts are locally authored SVGs rendered with installed Chrome headless; they are not claimed as ChatGPT website exports.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| `git status --short --branch` | Existing SH-01..SH-04 resources/worklogs were untracked and preserved; branch `develop...origin/develop`. | VERIFIED |
| `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3` + selected files | Selected/read SH-01, SH-02, SH-03 worklogs; no shortage (136 available). | VERIFIED |
| Root/global/scope context and manifest | Read router, context-map, web-work entry/index, server-study context, project dependency/boundary pages and skill registry. Study web subcontext path is missing although referenced by manifest/map; `createDD-markdown` excludes Web UI-only DD. | VERIFIED_STATIC_ONLY / NOT_FOUND |
| `.agents/web-study/design.md`, SH-05 inventory/auth flow/state rules; SH-02 `SCREEN.md` | Read canonical Study tokens, SH-05 401/403/refresh/safe-return intent, related login recovery, route and no-client-runtime disclosures. | VERIFIED_STATIC_ONLY |
| API #04 route/view/models/query/auth helper/DD/error/open questions/test source | Read header contract, Student role gate, 401/403/500 mapping, query-free unauthorized branch and test coverage. Tests not run. | VERIFIED_STATIC_ONLY |
| R-X01 route/view/validator/models/token helper/refresh test source | Read refresh request shape, 200 token-pair rotation, 401 invalid/replayed, 403 inactive account, 500 safe failures and atomic behavior tested with fakes. Tests not run. | VERIFIED_STATIC_ONLY |
| CUA ChatGPT browser | `getState()` returned `{apps:[], browsers:[]}`; `createBrowserTab("chrome", "https://chatgpt.com", ...)` returned `Browser is not available: chrome`. | BLOCKED_EXTERNAL_TOOL |
| `python3 apps/study-client/docs/dd_screens/resource/SH-05/build.py` | Rendered 12 clean/annotated SVGs and 12 PNGs with Chrome headless; includes 1440×960 desktop and 390×844 mobile for each state. | VERIFIED |
| SVG/PNG/marker/ZIP integrity audit | Parsed all 12 SVG XML documents; verified exact #1–#12 markers only on annotated SVGs; verified all 12 PNG dimensions; created ZIP with 27 files and `ZipFile.testzip()` returned no error. | VERIFIED |
| Visual review | Reviewed three desktop clean variants, desktop annotated variants, three mobile clean/annotated variants; rendered all three states at 320×844 for narrow-width review. No text/action clipping, marker loss or horizontal overflow observed. | VERIFIED_VISUALLY |
| App tests | Not run; static design artifact task. | NOT_RUN |

## HANDOFF

- SH-05 artifact set is complete locally and packaged. Remaining external workflow: re-author/send the plan through ChatGPT website and use its downloaded files only if @Chrome is available in a later session; this was not possible in the current CUA surface.
- Study Web runtime and approved token/redirect implementation are absent, so route/actions remain design targets. Server/API tests were not run.
- Next screen in a later one-screen session: SH-06. Preserve SH-01..SH-05 artifacts and existing untracked worktree files.
