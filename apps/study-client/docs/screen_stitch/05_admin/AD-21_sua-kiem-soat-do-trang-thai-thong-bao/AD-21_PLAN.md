# AD-21 — Kế hoạch đặc tả kiểm soát trạng thái thông báo

## Mục tiêu và phạm vi

Hoàn thiện riêng AD-21 theo inventory row 79, AC-36, API #18/#94/#95/#96, màn hình liên quan AD-19/AD-20 và SH-07. Giữ nguyên ảnh/HTML nguồn; lập marker map tuần tự cho mọi vùng UI nhìn thấy; viết DD A–F với event, API, state, điều hướng và blocker có truy vết. Không xử lý AD-22.

| Thuộc tính | Expected / nguồn thiết kế | Current evidence |
|---|---|---|
| Actor / quyền | AC-36: Admin có notification-management permission. | API catalog ghi role=Admin; handlers #94–#96 dùng shared `ADMIN`. Fine-grained permission/scope chưa được xác minh. |
| Route / điều hướng | Inventory candidate `/admin/notifications/:notificationId`; từ AD-19, liên quan SH-07; về AD-19 dự kiến. | Không có tracked Study Web `src/`, router, package manifest hoặc API client. Mọi prototype anchor là `#`; route chưa wired. |
| Notification read | Inventory chỉ ra không có GET detail riêng; dùng #96 để đọc status khi có ID. | #96 source local trả `Notification` (id/title/content/channels/status/created_at) và aggregate trạng thái, không trả counts/per-channel status/recipient/schedule. Đây không phải deployment/live proof. |
| #94 edit | Catalog/AC-36: PUT path-only, `ApiEnvelope<Notification>`, 200/401/403/404/422/500; conditional update. | Source local yêu cầu strict `{title, content}`, title ≤200, khóa row/deliveries, chỉ cập nhật khi ít nhất một delivery và tất cả `QUEUED`; body và eligibility là DERIVED; DD Draft. |
| #95 delete/cancel | Catalog: DELETE path-only, `ApiEnvelope<DeleteResult>`, 200/401/403/404/422/500; AC-36 nói delete/mark cancelled theo policy. | Source local hard-deletes một row BIGINT nếu mọi delivery hiện có đều `QUEUED`; FK candidate cascade; trả `status:"deleted"`. Không dừng provider/worker; cancel-vs-delete và retention cần quyết định. |
| #96 status | Catalog: GET path-only, `ApiEnvelope<Notification>`, 200/401/403/404/500. | Source local read-only, malformed/missing/no-delivery → 404; aggregate precedence `QUEUED` > `FAILED` > `SENT`. Channels ordered; no delivery counts/per-channel states. |
| Operation / SH-07 | Inventory: chỉ sang SH-07/#18 nếu backend cung cấp operation_id hợp lệ. | #18 chưa có route/module/query/test/Study store; ID int64 trong API row nhưng UUID trong AC/reusable schema và #93 metadata. Handoff không thể xác minh. |
| Prototype | Hiển thị identity cards, static notification fields, channel status, cancel/edit and SH-07 actions. | Status, IDs, counters, RBAC/pipeline claims are static. Edit/cancel/SH-07 controls disabled; no input/API/feature handler. |

## Source review và thứ tự

1. Đọc list_screen row 79, API reverse index #018/#094–#096 và global plan/checkpoint; xác nhận chỉ xử lý AD-21.
2. Đối chiếu AC-36 Admin permission, update/delete/status branches, direct API catalog và macro-review #92–#96; giữ nguyên khác biệt path-only contract/local body/effects.
3. Trace router → shared auth → validator → query/transaction → model/response/errors for #94/#95/#96. Inspect API #18 registration/store and SH-07; treat candidate DDL/test history as limited evidence.
4. Inspect AD-19/AD-20 handoff, exact screenshot/HTML and Study Web source tree. Never treat mockup/static copy as runtime state.
5. Save this plan before writing marker JSON/SVG, annotated PNG or `AD-21.md`.
6. Create 47 ordered element markers and map every marker to one DD row; cover shell, breadcrumbs, cards, status labels, disabled actions and footer.
7. Write A–F DD with current static behavior, expected-only flow, API exact contract/current local difference, errors, navigation, state matrix and blockers.
8. Update inventory row 79, reverse index #094/#095/#096 D→R (local source exists; API DD remains Draft), and global plan. Static-audit image/map/document/source hashes, counts, links, `git diff --check`; do not run application tests/runtime.

## Asset and marker plan

- Source image: `screen.png`, 1425×1600, SHA-256 `dc6863cb8033fb99adc21118823a5d72d739e2c2db83b13b2e3b39ba7d2dfa62`.
- HTML source: `code.html`, 272 lines / 25,379 bytes, SHA-256 `5243c7a44d759c726a53fa035ace275ee354026f9e5ff8cd47aee37726cc363a`.
- Source directory initially contained only those two files. Keep both unchanged.
- Marker coordinates use source pixels with top-left origin. Annotated image target is 2850×3200 (2×); marker dots should sit at component edges or adjacent whitespace.

| # | Element / region | Planned marker (x,y) |
|---:|---|---:|
| 1 | Study2Work / LMS / Admin Portal brand | 252,35 |
| 2 | Shell navigation — Tổng quan | 306,60 |
| 3 | Shell navigation — Người dùng | 427,60 |
| 4 | Shell navigation — Khóa học & Nội dung | 610,60 |
| 5 | Shell navigation — Kiểm duyệt | 781,60 |
| 6 | Shell navigation — Báo cáo | 887,60 |
| 7 | System Normal status badge | 1113,60 |
| 8 | Header notification bell and unread dot | 1161,60 |
| 9 | Admin identity / role / avatar | 1400,60 |
| 10 | Global breadcrumb — Hệ thống / Quản trị trung tâm / Không gian làm việc | 19,86 |
| 11 | RBAC assurance label | 1401,86 |
| 12 | Local notification breadcrumb | 20,149 |
| 13 | Return to list AD-19 anchor | 1402,164 |
| 14 | Screen ID badge and candidate route | 608,181 |
| 15 | Page heading | 858,237 |
| 16 | Supporting description | 799,281 |
| 17 | Admin permission environment badge | 1402,271 |
| 18 | Technical identity panel heading/icon | 485,355 |
| 19 | Active protection badge | 1375,365 |
| 20 | Notification ID card | 472,520 |
| 21 | Operation ID card | 914,520 |
| 22 | Publishing status card | 1354,520 |
| 23 | Missing-detail / locked-actions notice | 1370,710 |
| 24 | Notification content panel heading/icon | 795,822 |
| 25 | Static-view badge | 642,804 |
| 26 | Notification title label and placeholder field | 778,920 |
| 27 | Channel label / placeholder field | 807,976 |
| 28 | In-App channel chip | 640,1004 |
| 29 | Email channel chip | 800,1004 |
| 30 | Content label and placeholder area | 778,1088 |
| 31 | Locked-content safety note | 778,1218 |
| 32 | Recipient label and placeholder field | 778,1315 |
| 33 | Disabled Update draft button | 538,1394 |
| 34 | Delivery progress panel heading/icon | 1372,813 |
| 35 | In-App channel delivery card/status | 1356,871 |
| 36 | In-App completion bar and 0/0 row | 872,958 |
| 37 | Email channel delivery card/status | 1355,1017 |
| 38 | Email queue bar/status row | 872,1112 |
| 39 | Disabled Cancel release button | 1368,1183 |
| 40 | Cancel action safety note | 1367,1230 |
| 41 | SH-07 operation portal card heading/icon | 1367,1323 |
| 42 | SH-07 handoff description | 1370,1417 |
| 43 | Disabled SH-07 portal link | 1370,1457 |
| 44 | Footer copyright and system label | 407,1570 |
| 45 | Footer privacy policy link | 785,1570 |
| 46 | Footer RBAC standards link | 987,1570 |
| 47 | Footer technical support link | 1218,1570 |

## Event plan

- `EV-01` Initial route/load: candidate route only. No current Study Web router, auth gate, request, data hydration, timer, cache or status update exists.
- `EV-02` Shell/breadcrumb navigation: shell items and breadcrumb text are not functional routes; anchors have `href="#"`; current page identity does not carry a validated notification ID.
- `EV-03` Header Notifications button: button has accessible label but no handler or destination; unread dot is static.
- `EV-04` Return to AD-19: visible anchor has `href="#"`; expected return context/data contract is not implemented.
- `EV-05` Update draft: button is disabled. If later enabled, contract must resolve #94's missing request body; local `{title,content}`/QUEUED-only behavior is DERIVED and does not establish draft or schedule editing.
- `EV-06` Cancel release: button is disabled. #95 is documented as path-only DELETE; local source hard-deletes a queued legacy row and does not stop external dispatch. Do not describe this as cancellation.
- `EV-07` SH-07 handoff: button is disabled. No compatible Operation ID/API #18 route exists; do not navigate or poll.
- `EV-08` Footer destinations: all three anchors are `#`; URLs/content destination contract absent.

## Acceptance and known blockers

- Marker IDs #1–#47 must be unique, sequential, in image bounds, and map one-to-one to element rows in `AD-21.md`; JSON/SVG/image coordinates must match.
- Source image/HTML hashes stay unchanged; annotated PNG is 2850×3200 and visually checked at full page.
- Inventory/folders remain 83/83; core artifacts rise from 73/83 to 74/83 after the four required DD assets are added.
- API reverse rows #094/#095/#096 become `R` for local registered source; API DD status stays Draft. #018 stays `D`/UNWIRED.
- Do not equate expected `draft/scheduled/sending/delivered/failed` with local `QUEUED/SENT/FAILED`; do not infer recipient/channel counts, delivery progress, notification cancellation, or Operation handoff.
- DD state: `DD BLOCKED`; implementation: `IMPLEMENTATION BLOCKED`; runtime: `RUNTIME NOT VERIFIED` until permissions, lifecycle/model/schema, API #18 and Study Web source are resolved.
