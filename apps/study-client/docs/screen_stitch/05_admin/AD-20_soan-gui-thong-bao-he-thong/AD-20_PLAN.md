# AD-20 — Kế hoạch đặc tả soạn/gửi thông báo hệ thống

## Mục tiêu và phạm vi

Hoàn thiện riêng AD-20 theo inventory row 78, AC-36 và API #93. Giữ nguyên ảnh/HTML nguồn; lập marker map cho mọi thành phần giao diện nhìn thấy; mô tả A–F, sự kiện, API, trạng thái và liên kết bằng cách tách expected contract khỏi current source. Không xử lý AD-21.

| Thuộc tính | Expected / nguồn thiết kế | Current evidence |
|---|---|---|
| Actor / quyền | Inventory/AC-36: Admin có quyền notification-management. | #93 route dùng shared role guard `ADMIN`; không có fine-grained permission hoặc scope. Đây là fallback hiện hành, chưa chứng minh tương đương AC-36. |
| Route / liên kết | Inventory candidate `/admin/notifications/new`; từ AD-19; liên quan AD-21 và SH-07. | Study Web không có app source/router/API client. Mockup links dùng `#`; AD-19 HTML CTA dùng `/admin/notifications/create`, cũng chưa wired. |
| API #93 | `POST /api/v1/admin/notifications`, Bearer JWT/Admin; recipients?:int64[], segment?:AudienceSegment, title/content/channels required; catalog response `ApiEnvelope<Notification>` at 202. | Local source requires explicit recipient IDs, rejects segment and non-unique/unsupported channels, uses `PUSH|EMAIL`, and returns first Notification plus derived `meta.operation_id:UUID`/`notification_ids`. API DD remains Draft — Needs Confirmation. |
| Operation handoff | Inventory: conditionally open SH-07 only if an `operation_id` is returned; accepted is not delivered. | Catalog #93/AC-36 Notification response conflicts with operation-tracking prose. API #18 row path is int64 while reusable Operation/AC/producer metadata use UUID; #18 has no Study runtime handler/store. SH-07 blocks this handoff. |
| Audience/channel/model | AC-36 shows recipients and conditional Push/Email delivery; inventory mockup shows all users/students/staff and app/email. | Segment predicate, role eligibility, in-app→channel mapping and approved Admin persistence/grain are unresolved. Local legacy BIGINT notification/outbox is a candidate only; no provider/worker call. |
| UI prototype | Mockup depicts title, segment, channel, body, priority, draft/send, preview and accepted/correlation/delivered workflow. | Only title/body input listeners update preview text. Other fields are static browser controls; toolbar/buttons/links have no handlers; Send is disabled. Workflow/priority/permission/SMTP claims are static. |
| Runtime | — | Study Web is UNWIRED; source image and HTML are design artifacts; no frontend/API runtime verification in this task. |

## Source review and order

1. Read list_screen row 78, API reverse index #093, flow F13 and G-12 in `apps/study-client/docs/list_screen.md`; read global row/checkpoint in `dd_screens/PLAN.md`.
2. Compare AC-36 create/send branch, direct API catalog #93, reusable Notification/Operation schemas and generic operation-tracking prose.
3. Read API #93 DD, Q-93-01…10 and verification report; preserve Draft/open-question status.
4. Trace current route → shared ADMIN guard → validator → recipients query → notification/delivery inserts → response/commit/errors; inspect tests without running them. Treat checked-in DDL/migration only as candidates.
5. Check API #18 design/current registration and SH-07 handoff. Preserve Notification-vs-Operation and UUID-vs-int64 discrepancies; do not assert a valid operation poll.
6. Recheck Study Web source tree and inspect exact HTML/screenshot; compare the intended style only with `.agents/web-study/design.md`.
7. The source review and status were recorded in `.agents/worklog/2026-11-07/design-study-screen-ad20.md`. This plan is saved before marker JSON/SVG, annotated PNG or AD-20.md.

## Sơ đồ vùng và marker map

Source coordinate space: 1242×1600 pixels, origin top-left. Markers describe 54 visible components/controls, including shell/footer affordances and the static workflow panel. Repeated decorative icons are grouped with their owning component. Place each number in nearby whitespace or low-content padding so text and input controls remain legible. Annotated output target: 2484×3200 (2×).

| # | Element / region | Planned marker point (x,y) |
|---:|---|---:|
| 1 | Brand / LMS / admin portal | 195,45 |
| 2 | Shell navigation — Tổng quan | 277,47 |
| 3 | Shell navigation — Người dùng | 365,47 |
| 4 | Shell navigation — Khóa học & Nội dung | 514,47 |
| 5 | Shell navigation — Kiểm duyệt | 658,47 |
| 6 | Shell navigation — Báo cáo | 759,47 |
| 7 | System Normal status label | 898,47 |
| 8 | Header notification bell | 997,47 |
| 9 | Admin identity/avatar | 1190,47 |
| 10 | Global breadcrumb — Hệ thống / quản trị | 400,74 |
| 11 | RBAC assurance label | 1048,92 |
| 12 | Local breadcrumb — quản trị thông báo | 510,145 |
| 13 | Return-to-list AD-19 button | 1226,160 |
| 14 | Screen ID badge | 40,183 |
| 15 | WCAG AA badge | 292,183 |
| 16 | Screen title | 690,238 |
| 17 | Introductory description | 820,280 |
| 18 | Async information icon | 44,424 |
| 19 | Async acceptance/delivery notice | 1193,424 |
| 20 | Required notification title label/input/helper | 780,533 |
| 21 | Recipient segment heading and instruction | 776,610 |
| 22 | Audience card — all users | 55,650 |
| 23 | Audience card — enrolled learners | 528,650 |
| 24 | Audience card — instructors/assistants | 776,650 |
| 25 | Static segment-filter technical note | 776,810 |
| 26 | Delivery-channel heading | 777,845 |
| 27 | In-app Feed checkbox/card | 397,875 |
| 28 | Email disabled checkbox/card and SMTP note | 776,930 |
| 29 | Required content heading / basic-format support label | 486,983 |
| 30 | Rich-text toolbar — bold/italic/link/list | 240,1023 |
| 31 | Notification body textarea | 770,1228 |
| 32 | Priority heading | 777,1282 |
| 33 | Priority card — normal | 391,1310 |
| 34 | Priority card — urgent | 772,1310 |
| 35 | Draft/send safety copy | 455,1444 |
| 36 | Save draft button | 598,1454 |
| 37 | Disabled Send now button | 778,1454 |
| 38 | Preview panel heading | 842,490 |
| 39 | In-app Feed preview badge | 1204,480 |
| 40 | Preview notification source/time header | 1201,526 |
| 41 | Preview title | 1203,613 |
| 42 | Preview body snippet | 1203,657 |
| 43 | Preview detail link | 840,710 |
| 44 | Preview priority label | 1204,711 |
| 45 | Preview auto-update note | 844,778 |
| 46 | Technical workflow panel heading | 1194,838 |
| 47 | Workflow step — Accepted | 840,884 |
| 48 | Workflow step — Correlation | 840,955 |
| 49 | Workflow step — Delivered | 840,1044 |
| 50 | Static operation-tracking-code claim | 840,1120 |
| 51 | Footer copyright/system label | 139,1556 |
| 52 | Footer privacy policy link | 746,1556 |
| 53 | Footer RBAC standards link | 919,1556 |
| 54 | Footer technical support link | 1115,1556 |

## Event và dữ liệu cần đặc tả trong DD

1. EV-01 — Initial route/load: inventory route `/admin/notifications/new` is candidate only. There is no Study Web router/runtime. Do not claim an API call, auth gate or initial data request exists. A future implementation requires approved Admin permission and #93 mapping.
2. EV-02 — Shell/breadcrumb/return/footer navigation: visible anchors use `href="#"`; no target route is wired. AD-19 is the expected predecessor, AD-21 is a related consumer, and SH-07 is blocked by the operation contract. Do not infer browser history, route params or transfer data.
3. EV-03 — Title input: native input; the only current effect is trimming for preview display and replacing preview title with fallback copy when blank. No submit validation or API request runs.
4. EV-04 — Audience radio change: default `all` card is checked; the other cards are learner/staff. Selection changes only native control state; no IDs, enum token, predicate or role eligibility are resolved. #93 currently rejects any supplied `segment` and needs explicit recipient IDs; do not translate a card to a recipient list.
5. EV-05 — Channel checkbox change: app/in-app is checked; Email is disabled with a mock SMTP notice. There is no handler. Catalog #93 does not enumerate channel tokens; local fallback accepts only `PUSH|EMAIL`, so `In-app Feed` cannot be mapped without approval.
6. EV-06 — Body input/editor: textarea text mirrors to preview after trim; empty input restores sample copy. B/I/link/list controls have no handlers and the textarea remains plain text. No markup sanitization, rich-text schema or API submit is evidenced.
7. EV-07 — Priority radio change: `normal` is default and `urgent` is selectable, but API #93 has no priority field and preview priority text remains static. No request mapping or dispatch precedence may be inferred.
8. EV-08 — Save draft: visible button has no handler and #93 request has no `action`, `status` or `scheduled_at`; no draft creation API is confirmed. Keep action blocked until Product/API defines a draft contract.
9. EV-09 — Send now: button is statically disabled with a confirmation/configuration title; no click handler exists. Do not enable it or claim confirmation, network request or successful send before audience/permission/dispatch decisions.
10. EV-10 — Preview/detail affordance: preview title/body only reflect local input; the details link is not a working route. It does not call #96 or represent a server notification.
11. EV-11 — Workflow/status panel: Accepted/Correlation/Delivered and generated operation-code copy are static. No timer, polling, worker/provider call or delivery state is present. HTTP 202/local #93 commit cannot be displayed as delivery success; SH-07 handoff remains blocked.
12. EV-12 — Other shell status/notification/account controls: displayed System Normal, bell and account information have no verified runtime source or handler. Treat as static copy; no health/RBAC/session claims.

## Blocker cần giữ mở

- Catalog/AC-36 #93 response is `Notification`; generic operation-tracking prose says `Operation`; local source uses first Notification plus derived UUID metadata. Preserve all three shapes as a discrepancy.
- #18 `operation_id` row is int64; reusable schema, AC diagrams and #93 metadata use UUID. No generic Study Operation store/route exists. SH-07 cannot be opened based solely on the current metadata.
- AC-36 notification-management permission differs from the current shared `ADMIN` guard; no tenant/scope/eligibility rule exists.
- Audience segment tokens/predicates, recipient eligibility, campaign-vs-recipient grain, selected channel set and app-to-PUSH mapping are unapproved. Current local validator/outbox rules are fallback only.
- No request field chooses draft vs send or carries priority/schedule. Local #93 commits QUEUED rows but does not call a provider or worker; delivery is not verified.
- API #93 direct Notification response contract, validation/error triggers, local legacy BIGINT target and live migration/schema approval remain open.
- Study Web UI/router/API client is absent; screenshot controls and navigation are design-only. Static preview and technical claims are not runtime behavior.

## Acceptance audit to perform

- [ ] Preserve original `screen.png`/`code.html`; record unchanged hashes.
- [ ] Generate unique sequential markers #1–#54 with in-bounds source coordinates and one matching DD row each.
- [ ] Ensure JSON, SVG and DD coordinates agree; render 2484×3200 PNG and visually inspect it for legibility/coverage.
- [ ] Complete DD sections A–F and describe each observed affordance/event, expected/current API shape, validation/error boundary, state and navigation blocker.
- [ ] Check API #093 reverse index and screen row 78; keep API contract as D and update screen doc/tracker status accurately.
- [ ] Verify inventory/folder count remains 83/83 and core artifact count advances 72/83 → 73/83.
- [ ] Run static artifact/relative-link/hash/dimension/marker checks and `git diff --check`; do not run application tests/runtime for this documentation task.
