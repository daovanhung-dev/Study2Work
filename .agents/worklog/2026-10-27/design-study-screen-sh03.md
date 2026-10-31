---
task_id: "2026-10-27-design-study-screen-sh03"
date: "2026-10-27"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["Study Web SH-03 -> Study API #01 register -> SH-04 / API #02 email handoff"]
status: "PARTIAL"
---

# Worklog: Thiết kế Study Web screen SH-03

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-27/design-study-screen-sh01.md`
    - carry_forward: SH-01 dùng ocean palette, 4px rhythm và callout/table; giữ artwork riêng, không xem resource design là frontend runtime.
  - path: `.agents/worklog/2026-10-27/design-study-screen-sh02.md`
    - carry_forward: Giữ evidence source/contract tách biệt; API discrepancies, source-only behavior và role gates phải được ghi rõ. SH-03 là screen tiếp theo theo inventory.
  - path: `.agents/worklog/2026-10-27/study-web-design-guide.md`
    - carry_forward: `.agents/web-study/design.md` là visual target canonical; không nạp font từ mạng; giữ accessible contrast, keyboard states và 4px spacing.
- shortage: `none` (134 worklog docs khả dụng; đã đọc đủ 3 được chọn)

## EXPECTED_BEHAVIOR

- Requirement: Hoàn tất đúng một screen trong phiên này: SH-03 Đăng ký học viên, route target `/register`, Guest, AC-01, API #01. Tạo plan source-backed trước khi thiết kế; ảnh sạch và ảnh đánh số từng element; Markdown mô tả chi tiết kích thước, typography, semantics, events/states/responsive theo bảng; ZIP nằm dưới `apps/study-client/docs/dd_screens/resource/SH-03/`.
- Canonical target: `.agents/web-study/design.md`; SH-03 inventory, F01 và route/state/security rules trong `apps/study-client/docs/dd_screens/list_screen.md`. SH-04 và API #02 là dependency sau đăng ký, không phải màn hình được thiết kế lại trong phiên này.

## CURRENT_BEHAVIOR

- Source/config: `apps/study-client/` chỉ có `docs/dd_screens/list_screen.md` và SH-01/SH-02 design resources; chưa có Study Web runtime/router/client API source. `.agents/web-work/AGENTS.md` trỏ tới `.agents/web-work/study/AGENTS.md` nhưng Study subcontext path không tồn tại; `.agents/web-study/design.md` là visual target đã đọc.
- API #01 current source: public `POST /api/v1/auth/register`, HTTP 201; body `email/password/full_name`; email trim + EmailStr + max 255; password chỉ chặn blank/whitespace, không có strength policy; họ tên trim, 1–150. Tạo Argon2id hash, query duplicate, INSERT `users` với role `STUDENT`, commit; lỗi duplicate 409 `Email đã tồn tại.`, validation 422 fieldErrors, internal 500 an toàn. Success `DESIGN_RESOURCE_CREATED` trả profile, không có password/hash. Route không gọi #02; view chỉ log `verification_dispatch_pending` sau commit. Current INSERT bỏ qua status; local DDL default chưa chứng minh live status.
- API #01 expected/DD: HTTP 201, `data.id`/`data.email` cần cho SH-04, errors 409/422/500. DD `Draft — Needs Confirmation`; profile `bio` và user/profile/status/verification policy còn open questions. Current source #01 không có column/table profile đã xác nhận và không emit `bio`.
- API #02 current source: public `POST /api/v1/auth/verify-email/send`, HTTP 202; input `user_id` integer + email; default provider là stub trả `accepted`, không gửi email/token/link. Provider exception được ánh xạ 500 đồng bộ; chưa có queue/retry worker. #02 thuộc SH-04, không phải request trực tiếp trong SH-03.
- Runnable tests: Đã đọc API #01/#02 test source; không chạy tests trong docs/design task. Các test source dùng fake DB/provider; không chứng minh live DB/schema/deployment hay email delivery.
- Runtime wiring: Study Server route được đăng ký trong `app/api/v1.py`. Study Web consumer chưa tồn tại. Inventory F01 target flow SH-03 #01 201 → SH-04 #02 → SH-02 khác với current #01 tự dispatch; ghi `DISCREPANCY`, không khẳng định email đã gửi/verified.

## SOURCE_TRACE

```text
Expected inventory flow: SH-03 form -> POST API #01 -> 201 `data.id`/`data.email` -> SH-04 -> POST API #02 -> later SH-02; 409 email conflict remains on SH-03.
Current source trace: guest form -> route `/auth/register` -> validator (before DB) -> duplicate lookup -> Argon2id hash -> `INSERT users`/commit -> safe 201 profile envelope; route does not call #02 and only logs pending dispatch. Separate SH-04 route calls public #02 -> injected provider; default stub returns 202/`accepted`, no actual email send.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Study Web runtime | Current scoped tree listing contains inventory/design resources and no source entrypoint. | `SOURCE_REQUIRED` | Mark route and UI interactions as design target unless wiring evidence is found. |
| API #01 contract and account model | DD #01 is `Draft — Needs Confirmation`; `bio`, default status, profile mapping, verification enablement and email normalization/case policy are open. Current source only inserts `users`, returns source profile and relies on DB default for status. | `DISCREPANCY / SOURCE_REQUIRED` | Do not display status or invent profile/consent fields; use only `data.id`/`data.email` for target handoff. |
| API #01 → #02 sequencing | Inventory F01 says SH-03 → SH-04 → #02; current #01 only logs pending dispatch and does not invoke #02. | `DISCREPANCY / OPEN_DECISION` | Design the inventory target handoff but state it is not wired; do not claim API #02 ran from #01. |
| Email delivery | API #02 default provider is a stub with `accepted`; no message, token, link, verification or retry worker exists in source. | `SOURCE_REQUIRED / BLOCK` | SH-03 and SH-04 copy cannot claim that an email was sent or the address verified. |
| Consent/terms | Inventory says consent only if supported by a contract; API #01 request and current source have no consent field, no approved terms copy/link was found. | `NOT_FOUND` | No terms checkbox or implied acceptance. |
| Study Web context subpage | Web router/index point to `.agents/web-work/study/*`, both files absent; canonical `.agents/web-study/design.md` exists and is read. | `NOT_FOUND / CONTEXT_MAP_DRIFT` | Use canonical visual guide; no unrelated context repair in this screen task. |

## CHANGES

- Files changed: `apps/study-client/docs/dd_screens/resource/SH-03/PLAN.md`, `build.py`, clean/annotated SVG+PNG, transparent artwork SVG+PNG, `SCREEN.md`, ZIP and this worklog.
- CONTEXT_UPDATES: None.
- Context pages changed: None.
- Assumptions: Idle registration form is the default screenshot; no email/password sample data. No terms control is designed because no contract/approved copy supports it. SH-04 is a linked separate screen, not a SH-03 child screen.
- Authoring provenance: A plan and package prompt were submitted to ChatGPT in the requested Chrome session; ChatGPT returned progress notes and an artwork preview but did not deliver its ZIP before the Chrome automation inventory lost all browser sessions. Final deliverables here were rendered locally from editable SVG with installed Chrome headless, then audited. ChatGPT output was not downloaded or included.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| `git status --short --branch` | Branch `develop...origin/develop`; existing SH-01/SH-02 resources and worklogs are untracked and preserved. | VERIFIED |
| `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3` | Selected 3 `docs` worklogs from 134 available; all selected files were read. | VERIFIED |
| Root/global context and `.agents/context-map.md` | Classification, progressive-load order, cross-scope project-context condition and worklog contract reviewed. | VERIFIED_STATIC_ONLY |
| `.agents/web-study/design.md`, SH-03 row/F01 inventory | Visual target and expected registration flow read; API source trace completed below. | VERIFIED_STATIC_ONLY |
| `.agents/server-study/AGENTS.md`, `INDEX.md`, `modules/register-account.md`; #01/#02 source, route, DD and test source | Current inputs, validation, transaction, response, error, provider stub and contract open questions traced. Test source read, not run. | VERIFIED_STATIC_ONLY |
| AC-01 draw.io flow text | Actor/precondition, 3 form values, #01 201, duplicate 409, target #02 email handoff and linked-screen outcome reviewed. | VERIFIED_STATIC_ONLY |
| `ui-ux-pro-max` search `registration form validation inline field errors web --domain ux -n 5` | Confirmed web guidance for visible labels, inline errors and focusable linked error summary; applied only where compatible with source behavior. | VERIFIED_STATIC_ONLY |
| `apps/study-client/docs/dd_screens/resource/SH-03/PLAN.md` | Authored source-backed plan with 19 targets, exact desktop geometry, all API/source discrepancies, screen links, states, responsive behavior and image brief before generating the screen. | VERIFIED_STATIC_ONLY |
| ChatGPT @Chrome | Uploaded only `SH-03/PLAN.md` in a dedicated ChatGPT tab and submitted package requirements. ChatGPT showed an artwork preview and progress notes, but the requested package did not finish before the browser disappeared from CUA inventory (`No browser is available`). | PARTIAL / TOOL_UNAVAILABLE |
| `python3 apps/study-client/docs/dd_screens/resource/SH-03/build.py` | Rendered SVG artwork and screen with local Chrome headless; PNG dimensions are 1440×960, 1440×960 and 470×313. | VERIFIED |
| `apps/study-client/docs/dd_screens/resource/SH-03/SCREEN.md` and annotated SVG | Exactly 19 element rows and exactly 19 numbered badge circles, IDs #1–#19. | VERIFIED |
| ZIP integrity and content check | `SH-03_design_handoff_v1.zip` passes `zipfile.testzip`; contains 9 required files, and each archived member byte-matches its current file. | VERIFIED |
| Visual review via `view_image` | Inspected clean PNG, annotated PNG and transparent artwork at original resolution; corrected the password field from fake masked content to its empty placeholder, rebuilt and reviewed again. | VERIFIED_VISUAL |
| Automated/application tests | None run; this is a static visual/documentation package, not a Study Web implementation. | NOT_RUN |

## HANDOFF

- Completed artifact work: SH-03 has clean and annotated screenshots, transparent illustration, editable SVG sources, detailed Vietnamese `SCREEN.md`, source-backed `PLAN.md`, repeatable `build.py` and verified ZIP under `apps/study-client/docs/dd_screens/resource/SH-03/`.
- Remaining workflow gap: ChatGPT's response/ZIP could not be recovered because Chrome automation reported no available browser. If the requested browser session becomes available again, use it to review the finished local package and make only concrete visual fixes; do not resubmit a duplicate initial request.
- Next screen in the multi-screen task: continue with the next `list_screen.md` item in a later screen session, preserving this folder and the existing SH-01/SH-02 outputs.
