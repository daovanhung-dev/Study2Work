# ST-01 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [ST-01_markers.json](../../screen_stitch/03_student/ST-01_tong-quan-hoc-vien/ST-01_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `ST-01-EL-001` | `ST01-EL-01` | Study2Work logo and brand |
| #2 | `ST-01-EL-002` | `ST01-EL-02` | Primary navigation group |
| #3 | `ST-01-EL-003` | `ST01-EL-03` | Static learner name, role and avatar |
| #4 | `ST-01-EL-004` | `ST01-EL-04` | Specification gate and zero-synthetic-data banner |
| #5 | `ST-01-EL-005` | `ST01-EL-05` | Breadcrumb |
| #6 | `ST-01-EL-006` | `ST01-EL-06` | Screen ID and DESIGN_ONLY labels |
| #7 | `ST-01-EL-007` | `ST01-EL-07` | Page title and introduction |
| #8 | `ST-01-EL-008` | `ST01-EL-08` | Gate status card |
| #9 | `ST-01-EL-009` | `ST01-EL-09` | Course widget heading |
| #10 | `ST-01-EL-010` | `ST01-EL-10` | Course gated empty-state panel |
| #11 | `ST-01-EL-011` | `ST01-EL-11` | Course link to ST-08 |
| #12 | `ST-01-EL-012` | `ST01-EL-12` | Progress widget heading |
| #13 | `ST-01-EL-013` | `ST01-EL-13` | Progress no-data panel |
| #14 | `ST-01-EL-014` | `ST01-EL-14` | Progress link to ST-20 |
| #15 | `ST-01-EL-015` | `ST01-EL-15` | Achievement widget heading |
| #16 | `ST-01-EL-016` | `ST01-EL-16` | Achievement gated panel and activation note |
| #17 | `ST-01-EL-017` | `ST01-EL-17` | Notification widget heading |
| #18 | `ST-01-EL-018` | `ST01-EL-18` | Notification gateway-blocked panel |
| #19 | `ST-01-EL-019` | `ST01-EL-19` | Notification link to ST-26 |
| #20 | `ST-01-EL-020` | `ST01-EL-20` | Developer hand-off heading |
| #21 | `ST-01-EL-021` | `ST01-EL-21` | Developer hand-off description |
| #22 | `ST-01-EL-022` | `ST01-EL-22` | API endpoint list heading |
| #23 | `ST-01-EL-023` | `ST01-EL-23` | API #20 endpoint row |
| #24 | `ST-01-EL-024` | `ST01-EL-24` | API #21 endpoint row |
| #25 | `ST-01-EL-025` | `ST01-EL-25` | API #38 endpoint row |
| #26 | `ST-01-EL-026` | `ST01-EL-26` | API #43 endpoint row |
| #27 | `ST-01-EL-027` | `ST01-EL-27` | Accessibility and experience checklist heading |
| #28 | `ST-01-EL-028` | `ST01-EL-28` | Target-size checklist item |
| #29 | `ST-01-EL-029` | `ST01-EL-29` | Rhythm and grid checklist item |
| #30 | `ST-01-EL-030` | `ST01-EL-30` | Ocean identity checklist item |
| #31 | `ST-01-EL-031` | `ST01-EL-31` | Visual-boundary checklist item |
| #32 | `ST-01-EL-032` | `ST01-EL-32` | Safe navigation note |
| #33 | `ST-01-EL-033` | `ST01-EL-33` | Footer copyright |
| #34 | `ST-01-EL-034` | `ST01-EL-34` | Static WCAG 2.1 AA badge |
| #35 | `ST-01-EL-035` | `ST01-EL-35` | Terms of service link |
| #36 | `ST-01-EL-036` | `ST01-EL-36` | Privacy policy link |
| #37 | `ST-01-EL-037` | `ST01-EL-37` | Help link |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả chi tiết element

Marker `#1…#37` nằm trên [ảnh chú thích](../../screen_stitch/03_student/ST-01_tong-quan-hoc-vien/screen_annotated.png), map một-một qua [JSON](../../screen_stitch/03_student/ST-01_tong-quan-hoc-vien/ST-01_markers.json). Hình chỉ có static hand-off state; chưa có runtime loading/hover/focus/error state. Các component dùng design-only data gate không có input validation.

| Element ID / marker | Tên, loại, vị trí | Thuộc tính, nguồn, điều kiện hiển thị và state | Event |
|---|---|---|---|
| ST01-EL-01 / #1 | Study2Work LMS logo/brand; header trái | Static brand/icon. HTML anchor `href="#"`; home destination chưa xác nhận. | EV-09 |
| ST01-EL-02 / #2 | Nhóm primary nav: Trang chủ, Khóa học, Tiến độ, Thảo luận, Thông báo | 5 label tĩnh; các anchor dùng `href="#"`, `data-path` không phải route. Visibility theo prototype. | EV-09 |
| ST01-EL-03 / #3 | Learner name, role, avatar; header phải | “Nguyễn Văn A”/“Học viên” là static sample. Không có field/source API mapping ở ST-01; không xác minh danh tính. | EV-01, EV-09 |
| ST01-EL-04 / #4 | Specification gate / zero synthetic data banner | Static warning, API D labels và “Hand-off”; không phản ánh trạng thái kết nối runtime. | EV-01, EV-10 |
| ST01-EL-05 / #5 | Breadcrumb Study2Work LMS → ST-01 | Anchor `href="#"`; destination/back behavior chưa có source. | EV-09 |
| ST01-EL-06 / #6 | Screen ID và DESIGN_ONLY tags | Text label tĩnh; không interactive, không có validation/data binding. | — |
| ST01-EL-07 / #7 | Page title và introduction | Static heading/copy; không lấy từ API. | — |
| ST01-EL-08 / #8 | “Trạng thái cổng / Hợp đồng chờ kích hoạt” card | Static status claim và icon; không phải health check hoặc API response. | EV-01, EV-10 |
| ST01-EL-09 / #9 | Course widget heading, icon, API #20 chip | Static label “Khóa học đang học”; chip design-only. | EV-02 |
| ST01-EL-10 / #10 | Course gated empty-state panel | Lock icon, copy “Chưa nạp được danh sách…”; không phải response empty/error của #20. Không có course card. | EV-02, EV-10 |
| ST01-EL-11 / #11 | CTA “Đi đến Khóa học của tôi (ST-08)” | Styled anchor with `href="#"`, `data-path`; target `/student/courses` chỉ theo inventory. | EV-06 |
| ST01-EL-12 / #12 | Progress widget heading, icon, API #21 chip | Static label “Tiến độ tổng quan”; no progress values. | EV-03 |
| ST01-EL-13 / #13 | Progress no-data panel | Copy explicitly avoids fake chart/KPI/percentage; panel static, không có formula/value source. | EV-03, EV-10 |
| ST01-EL-14 / #14 | CTA “Xem chi tiết tiến độ (ST-20)” | Styled anchor with `href="#"`; target `/student/progress` theo inventory, không có data handoff. | EV-07 |
| ST01-EL-15 / #15 | Achievement widget heading, icon, API #38 chip | Static title; không có achievement records hoặc count. | EV-04 |
| ST01-EL-16 / #16 | Achievement gated panel và activation note | No-certificate copy và “chữ ký kiểm định từ hệ thống chấm điểm ST-22” là claim trong prototype, không có signature API/schema. | EV-04, EV-10 |
| ST01-EL-17 / #17 | Notification widget heading, icon, API #43 chip | Static title “Thông báo mới nhất”; không chứng minh sorting “latest”. | EV-05 |
| ST01-EL-18 / #18 | Gateway-blocked panel | Static SSE/Webhook/gateway copy; no live transport health or notification payload. | EV-05, EV-10 |
| ST01-EL-19 / #19 | CTA “Mở hòm thư thông báo (ST-26)” | Styled anchor `href="#"`; ST-26 `/student/notifications` là target inventory. | EV-08 |
| ST01-EL-20 / #20 | Developer Hand-off Matrix heading | Static developer-facing panel heading, not student business data. | — |
| ST01-EL-21 / #21 | Hand-off description | Static explanatory copy; no API call or behavior. | — |
| ST01-EL-22 / #22 | API endpoint list heading | Static “Design-Only” matrix heading. | — |
| ST01-EL-23 / #23 | API #20 row | HTML path `/api/v1/courses/enrolled` mismatches catalog `/api/v1/users/me/courses`; status D is design label, not runtime probe. | — |
| ST01-EL-24 / #24 | API #21 row | HTML path `/api/v1/students/progress` mismatches catalog `/api/v1/users/me/progress`. | — |
| ST01-EL-25 / #25 | API #38 row | HTML path `/api/v1/achievements` mismatches catalog `/api/v1/users/me/achievements`. | — |
| ST01-EL-26 / #26 | API #43 row | HTML path `/api/v1/notifications/latest` mismatches catalog `/api/v1/users/me/notifications`; `latest` order is unresolved. | — |
| ST01-EL-27 / #27 | Accessibility/experience checklist heading | Static checklist. Passing status is not independently verified. | — |
| ST01-EL-28 / #28 | Target size criterion | Copy claims controls ≥44px/WCAG 2.5.5; not an app audit. | — |
| ST01-EL-29 / #29 | Rhythm/grid criterion | Static 4px/8px claim; target design guide gives spacing rhythm but screenshot is not implementation proof. | — |
| ST01-EL-30 / #30 | Ocean identity/AA criterion | Static copy claims ocean identity/AA; HTML config instead uses cobalt tokens, and no contrast test is attached. | — |
| ST01-EL-31 / #31 | Zero-line-border/visual boundary criterion | Static visual claim only. | — |
| ST01-EL-32 / #32 | Safe navigation note for ST-08/ST-20/ST-26 | Static assertion about session preservation; no route/session implementation source. | EV-06, EV-07, EV-08 |
| ST01-EL-33 / #33 | Footer copyright | Static “© 2025” copy; not a runtime/legal version source. | — |
| ST01-EL-34 / #34 | WCAG 2.1 AA badge | Static assertion, not accessibility verification. | — |
| ST01-EL-35 / #35 | Terms of service footer anchor | `href="#"`; canonical destination absent. | EV-09 |
| ST01-EL-36 / #36 | Privacy policy footer anchor | `href="#"`; canonical destination absent. | EV-09 |
| ST01-EL-37 / #37 | Help footer anchor | `href="#"`; support destination absent. | EV-09 |

## 4. Conditional UI & state variations
- States theo inventory: partial-widget/empty/loading/403
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/03_student/ST-01_tong-quan-hoc-vien/ST-01.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
