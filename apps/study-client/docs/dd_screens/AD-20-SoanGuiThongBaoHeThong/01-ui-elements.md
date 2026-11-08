# AD-20 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [AD-20_markers.json](../../screen_stitch/05_admin/AD-20_soan-gui-thong-bao-he-thong/AD-20_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `AD-20-EL-001` | `not supplied in marker JSON` | Brand / LMS / admin portal |
| #2 | `AD-20-EL-002` | `not supplied in marker JSON` | Shell navigation — Tổng quan |
| #3 | `AD-20-EL-003` | `not supplied in marker JSON` | Shell navigation — Người dùng |
| #4 | `AD-20-EL-004` | `not supplied in marker JSON` | Shell navigation — Khóa học & Nội dung |
| #5 | `AD-20-EL-005` | `not supplied in marker JSON` | Shell navigation — Kiểm duyệt |
| #6 | `AD-20-EL-006` | `not supplied in marker JSON` | Shell navigation — Báo cáo |
| #7 | `AD-20-EL-007` | `not supplied in marker JSON` | System Normal status label |
| #8 | `AD-20-EL-008` | `not supplied in marker JSON` | Header notification bell |
| #9 | `AD-20-EL-009` | `not supplied in marker JSON` | Admin identity/avatar |
| #10 | `AD-20-EL-010` | `not supplied in marker JSON` | Global breadcrumb — Hệ thống / quản trị |
| #11 | `AD-20-EL-011` | `not supplied in marker JSON` | RBAC assurance label |
| #12 | `AD-20-EL-012` | `not supplied in marker JSON` | Local breadcrumb — quản trị thông báo |
| #13 | `AD-20-EL-013` | `not supplied in marker JSON` | Return-to-list AD-19 button |
| #14 | `AD-20-EL-014` | `not supplied in marker JSON` | Screen ID badge |
| #15 | `AD-20-EL-015` | `not supplied in marker JSON` | WCAG AA badge |
| #16 | `AD-20-EL-016` | `not supplied in marker JSON` | Screen title |
| #17 | `AD-20-EL-017` | `not supplied in marker JSON` | Introductory description |
| #18 | `AD-20-EL-018` | `not supplied in marker JSON` | Async information icon |
| #19 | `AD-20-EL-019` | `not supplied in marker JSON` | Async acceptance/delivery notice |
| #20 | `AD-20-EL-020` | `not supplied in marker JSON` | Required notification title label/input/helper |
| #21 | `AD-20-EL-021` | `not supplied in marker JSON` | Recipient segment heading and instruction |
| #22 | `AD-20-EL-022` | `not supplied in marker JSON` | Audience card — all users |
| #23 | `AD-20-EL-023` | `not supplied in marker JSON` | Audience card — enrolled learners |
| #24 | `AD-20-EL-024` | `not supplied in marker JSON` | Audience card — instructors/assistants |
| #25 | `AD-20-EL-025` | `not supplied in marker JSON` | Static segment-filter technical note |
| #26 | `AD-20-EL-026` | `not supplied in marker JSON` | Delivery-channel heading |
| #27 | `AD-20-EL-027` | `not supplied in marker JSON` | In-app Feed checkbox/card |
| #28 | `AD-20-EL-028` | `not supplied in marker JSON` | Email disabled checkbox/card and SMTP note |
| #29 | `AD-20-EL-029` | `not supplied in marker JSON` | Required content heading / basic-format support label |
| #30 | `AD-20-EL-030` | `not supplied in marker JSON` | Rich-text toolbar — bold/italic/link/list |
| #31 | `AD-20-EL-031` | `not supplied in marker JSON` | Notification body textarea |
| #32 | `AD-20-EL-032` | `not supplied in marker JSON` | Priority heading |
| #33 | `AD-20-EL-033` | `not supplied in marker JSON` | Priority card — normal |
| #34 | `AD-20-EL-034` | `not supplied in marker JSON` | Priority card — urgent |
| #35 | `AD-20-EL-035` | `not supplied in marker JSON` | Draft/send safety copy |
| #36 | `AD-20-EL-036` | `not supplied in marker JSON` | Save draft button |
| #37 | `AD-20-EL-037` | `not supplied in marker JSON` | Disabled Send now button |
| #38 | `AD-20-EL-038` | `not supplied in marker JSON` | Preview panel heading |
| #39 | `AD-20-EL-039` | `not supplied in marker JSON` | In-app Feed preview badge |
| #40 | `AD-20-EL-040` | `not supplied in marker JSON` | Preview notification source/time header |
| #41 | `AD-20-EL-041` | `not supplied in marker JSON` | Preview title |
| #42 | `AD-20-EL-042` | `not supplied in marker JSON` | Preview body snippet |
| #43 | `AD-20-EL-043` | `not supplied in marker JSON` | Preview detail link |
| #44 | `AD-20-EL-044` | `not supplied in marker JSON` | Preview priority label |
| #45 | `AD-20-EL-045` | `not supplied in marker JSON` | Preview auto-update note |
| #46 | `AD-20-EL-046` | `not supplied in marker JSON` | Technical workflow panel heading |
| #47 | `AD-20-EL-047` | `not supplied in marker JSON` | Workflow step — Accepted |
| #48 | `AD-20-EL-048` | `not supplied in marker JSON` | Workflow step — Correlation |
| #49 | `AD-20-EL-049` | `not supplied in marker JSON` | Workflow step — Delivered |
| #50 | `AD-20-EL-050` | `not supplied in marker JSON` | Static operation-tracking-code claim |
| #51 | `AD-20-EL-051` | `not supplied in marker JSON` | Footer copyright/system label |
| #52 | `AD-20-EL-052` | `not supplied in marker JSON` | Footer privacy policy link |
| #53 | `AD-20-EL-053` | `not supplied in marker JSON` | Footer RBAC standards link |
| #54 | `AD-20-EL-054` | `not supplied in marker JSON` | Footer technical support link |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả chi tiết từng element

Coordinate là pixel của source `screen.png` (1242×1600, gốc trên trái). Marker ID ánh xạ 1:1 với `AD-20_markers.json` và `screen_annotated.png`.

| # | Element / loại | Thuộc tính, nguồn, điều kiện và trạng thái | Sự kiện |
|---:|---|---|---|
| 1 | Brand / LMS / admin portal — brand block | Copy/logo tĩnh; nguồn mockup; visible. Không xác nhận identity/runtime. | EV-12 |
| 2 | Tổng quan — navigation link | Link `#`; không có route destination. Visible, inert. | EV-02 |
| 3 | Người dùng — navigation link | Link `#`; không có route destination. Visible, inert. | EV-02 |
| 4 | Khóa học & Nội dung — navigation link | Link `#`; không có route destination. Visible, inert. | EV-02 |
| 5 | Kiểm duyệt — navigation link | Link `#`; không có route destination. Visible, inert. | EV-02 |
| 6 | Báo cáo — navigation link | Link `#`; không có route destination. Visible, inert. | EV-02 |
| 7 | System Normal — status badge | Copy trạng thái tĩnh; không có health API/source. Không hiển thị như health thật. | EV-12 |
| 8 | Bell — icon/control | Không có handler, unread data hay notification list route. | EV-12 |
| 9 | Admin identity/avatar — account block | Text/avatar tĩnh, không có session/profile source hoặc menu handler. | EV-12 |
| 10 | Global breadcrumb — navigation | Hierarchy “Hệ thống / Quản trị trung tâm / Không gian làm việc”; anchors không route. | EV-02 |
| 11 | RBAC assurance copy — badge | “Chuẩn xác thực RBAC” là static claim; không chứng minh policy/access decision. | EV-12 |
| 12 | Local breadcrumb — navigation | “Quản trị truyền thông / Thông báo hệ thống / Soạn thông báo mới”; không có route handler. | EV-02 |
| 13 | Return-to-list AD-19 — button/link | Label “Quay lại danh sách thông báo (AD-19)”; href `#`; candidate return destination only. | EV-02 |
| 14 | Screen ID badge | Static text `AD-20`; informational. | — |
| 15 | WCAG AA badge | Static claim; không phải audit evidence. | — |
| 16 | Page title — heading | “Soạn và phát hành thông báo toàn hệ thống”; static h1. | — |
| 17 | Intro description — text | Static description of centralized notices/alerts. Không mở rộng request contract. | — |
| 18 | Async info icon | Decorative icon trong banner; no click handler. | — |
| 19 | Async accepted/delivered banner — informational panel | Copy nói accepted khác delivered; đây là design guidance, không bind API lifecycle. | — |
| 20 | Notification title — required label/input/helper | `#notice-title`, text input, empty by default; helper says title shown in message/dashboard. Current script mirrors trimmed value to preview; no submit validation. API catalog requires string; local validator rejects blank and caps 200 (fallback). | EV-03 |
| 21 | Recipient heading/instruction — section label | Required copy “Recipients & Segment”; no actual recipient list/data source. | EV-04 |
| 22 | All users — audience radio card | `value=all`, checked by default. Copy claims all active accounts; no eligibility predicate/source; cannot map to #93 recipients. | EV-04 |
| 23 | Enrolled learners — audience radio card | `value=students`; static copy claims at least one open course. No course query/predicate; no #93 segment mapping. | EV-04 |
| 24 | Instructors & assistants — audience radio card | `value=staff`; static role claim. No role enumeration/recipient resolver; no #93 segment mapping. | EV-04 |
| 25 | Segment technical note — info card | Static copy says detailed segment filter awaits server configuration; no config loaded. | EV-04 |
| 26 | Delivery-channel heading | Static heading; catalog `NotificationChannel` values remain unspecified. | EV-05 |
| 27 | In-app Feed — checkbox/card | `value=app`, checked by default; copy mentions Web/LMS feed. No handler. Cannot assume `app` maps to local `PUSH`. | EV-05 |
| 28 | Email — disabled checkbox/card | `value=email`, disabled; “Chờ dịch vụ SMTP” static note. Runtime SMTP/provider availability not verified. | EV-05 |
| 29 | Required content heading / basic-format hint | Required label and static helper; does not guarantee rich-text support. | EV-06 |
| 30 | Editor toolbar — button group | Bold/italic/link/list buttons; no click handlers, no editor schema. | EV-06 |
| 31 | Notification body — textarea | `#notice-body`, empty by default, resizable; current script mirrors trimmed text into preview and restores sample on blank. No max length is defined by API catalog. | EV-06 |
| 32 | Priority heading | Static label; #93 has no priority field. | EV-07 |
| 33 | Normal — priority radio card | `value=normal`, checked by default; preview label is static. No API mapping. | EV-07 |
| 34 | Urgent — priority radio card | `value=urgent`, unchecked; copy claims alert treatment, unsupported by #93. | EV-07 |
| 35 | Draft/send safety copy — note | Static lock note says wait for recipient segment confirmation. Not a backend lock or validation. | EV-08, EV-09 |
| 36 | Save draft — button | Enabled-looking button; no handler. #93 has no draft/action/status field or confirmed draft endpoint. | EV-08 |
| 37 | Send now — disabled button | Disabled in markup; title says wait for segment and task-link configuration. No click handler; no confirmation dialog. | EV-09 |
| 38 | Preview heading | Static “Mô phỏng hiển thị (Xem trước)” section label. | EV-10 |
| 39 | In-app Feed badge | Static preview channel label. Does not confirm selected/accepted server channel. | EV-10 |
| 40 | Preview notification source/time | Static Study2Work source label and “Vừa xong”; not API data or send time. | EV-10 |
| 41 | Preview title | Sample title; updated by EV-03 only. Does not show persisted Notification. | EV-03, EV-10 |
| 42 | Preview body | Sample snippet; updated by EV-06 only. Does not show parsed rich text or persisted Notification. | EV-06, EV-10 |
| 43 | Preview detail link | Anchor `#`; no notification detail route or ID. | EV-10 |
| 44 | Preview priority badge | Static “Độ ưu tiên: Bình thường”; does not follow radio state. | EV-07, EV-10 |
| 45 | Preview auto-update note | Static copy says preview updates automatically; title/body do update locally. | EV-03, EV-06, EV-10 |
| 46 | Technical workflow heading | Static status panel heading. | EV-11 |
| 47 | Accepted step | Static copy says template validated and pushed to task queue; not response/queue evidence. | EV-11 |
| 48 | Correlation step | Static copy claims server filters recipients by permission; local #93 does no role/status/course filter. | EV-11 |
| 49 | Delivered step | Static copy claims notification distributed to device/mailboxes; no provider/worker is called by #93 view. | EV-11 |
| 50 | Operation tracking code claim — note | Static copy says code generated automatically; local metadata UUID is not an Operation record and #18 is unwired. | EV-11 |
| 51 | Footer copyright/system copy | Static footer; no product/version source. | EV-12 |
| 52 | Privacy policy link | Anchor `#`; target is not specified. | EV-02 |
| 53 | RBAC standards link | Anchor `#`; target is not specified. | EV-02 |
| 54 | Technical support link | Anchor `#`; target is not specified. | EV-02 |

## 4. Conditional UI & state variations
- States theo inventory: unwired/initial/editing/preview/draft-blocked/send-blocked/accepted/validation-error/unauthorized/forbidden/dependency-error/server-error/operation-unresolved
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/05_admin/AD-20_soan-gui-thong-bao-he-thong/AD-20.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
