# AD-24 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [AD-24_markers.json](../../screen_stitch/05_admin/AD-24_bao-cao-tac-dong-cong-dong/AD-24_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `AD-24-EL-001` | `AD24-EL-01` | Study2Work brand / portal mark |
| #2 | `AD-24-EL-002` | `AD24-EL-02` | Navigation: Tổng quan |
| #3 | `AD-24-EL-003` | `AD24-EL-03` | Navigation: Người dùng |
| #4 | `AD-24-EL-004` | `AD24-EL-04` | Navigation: Khóa học & Nội dung |
| #5 | `AD-24-EL-005` | `AD24-EL-05` | Navigation: Kiểm duyệt |
| #6 | `AD-24-EL-006` | `AD24-EL-06` | Navigation: Báo cáo |
| #7 | `AD-24-EL-007` | `AD24-EL-07` | System Normal status badge |
| #8 | `AD-24-EL-008` | `AD24-EL-08` | Notifications bell |
| #9 | `AD-24-EL-009` | `AD24-EL-09` | Admin identity / avatar |
| #10 | `AD-24-EL-010` | `AD24-EL-10` | Global breadcrumb |
| #11 | `AD-24-EL-011` | `AD24-EL-11` | RBAC verification badge |
| #12 | `AD-24-EL-012` | `AD24-EL-12` | Local report breadcrumb |
| #13 | `AD-24-EL-013` | `AD24-EL-13` | Screen ID badge: AD-24 |
| #14 | `AD-24-EL-014` | `AD24-EL-14` | Data-contract status badge |
| #15 | `AD-24-EL-015` | `AD24-EL-15` | Screen title |
| #16 | `AD-24-EL-016` | `AD24-EL-16` | Screen description |
| #17 | `AD-24-EL-017` | `AD24-EL-17` | Export-to-AD-25 CTA |
| #18 | `AD-24-EL-018` | `AD24-EL-18` | From-date control |
| #19 | `AD-24-EL-019` | `AD24-EL-19` | To-date control |
| #20 | `AD-24-EL-020` | `AD24-EL-20` | Learner-segment select |
| #21 | `AD-24-EL-021` | `AD24-EL-21` | Apply-filters button |
| #22 | `AD-24-EL-022` | `AD24-EL-22` | Reset-filters button |
| #23 | `AD-24-EL-023` | `AD24-EL-23` | Active-learners KPI card |
| #24 | `AD-24-EL-024` | `AD24-EL-24` | Completion-rate KPI card |
| #25 | `AD-24-EL-025` | `AD24-EL-25` | Community-interaction-hours KPI card |
| #26 | `AD-24-EL-026` | `AD24-EL-26` | Overall-satisfaction KPI card |
| #27 | `AD-24-EL-027` | `AD24-EL-27` | Visualization / empty-chart panel |
| #28 | `AD-24-EL-028` | `AD24-EL-28` | Empty-chart icon |
| #29 | `AD-24-EL-029` | `AD24-EL-29` | Empty-chart title |
| #30 | `AD-24-EL-030` | `AD24-EL-30` | Empty-chart explanatory copy |
| #31 | `AD-24-EL-031` | `AD24-EL-31` | Refresh-query button |
| #32 | `AD-24-EL-032` | `AD24-EL-32` | Data-contract version badge |
| #33 | `AD-24-EL-033` | `AD24-EL-33` | Planned-metrics section heading/icon |
| #34 | `AD-24-EL-034` | `AD24-EL-34` | Planned-metrics validation-count badge |
| #35 | `AD-24-EL-035` | `AD24-EL-35` | DAU/MAU specification card |
| #36 | `AD-24-EL-036` | `AD24-EL-36` | Mentor interaction-hours specification card |
| #37 | `AD-24-EL-037` | `AD24-EL-37` | Employment-readiness specification card |
| #38 | `AD-24-EL-038` | `AD24-EL-38` | Partner NPS specification card |
| #39 | `AD-24-EL-039` | `AD24-EL-39` | Footer copyright |
| #40 | `AD-24-EL-040` | `AD24-EL-40` | Footer privacy link |
| #41 | `AD-24-EL-041` | `AD24-EL-41` | Footer RBAC standards link |
| #42 | `AD-24-EL-042` | `AD24-EL-42` | Footer support link |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả chi tiết từng element

Marker centers are in source `screen.png` pixels. The numbered image, JSON map and element IDs below are one-to-one. Prototype states describe only HTML/JS, not future API states.

| Marker / Element ID | Tên, loại, vị trí và mục đích | Thuộc tính / nguồn / điều kiện, trạng thái | Sự kiện |
|---|---|---|---|
| #1 / AD24-EL-01 | Study2Work brand / portal mark, top-left shell. | Static logo text and “S” mark; no route behavior is established. | EV-08 |
| #2 / AD24-EL-02 | Nav “Tổng quan”, header anchor. | `href="#"`; target is not wired. | EV-08 |
| #3 / AD24-EL-03 | Nav “Người dùng”, header anchor. | `href="#"`; target is not wired. | EV-08 |
| #4 / AD24-EL-04 | Nav “Khóa học & Nội dung”, header anchor. | `href="#"`; target is not wired. | EV-08 |
| #5 / AD24-EL-05 | Nav “Kiểm duyệt”, header anchor. | `href="#"`; target is not wired. | EV-08 |
| #6 / AD24-EL-06 | Nav “Báo cáo”, header anchor. | `href="#"`; target is not wired. | EV-08 |
| #7 / AD24-EL-07 | “System Normal” badge, header. | Static text and pulsing dot; no health API/feed. Read-only visual. | — |
| #8 / AD24-EL-08 | Notifications bell button. | `aria-label="Notifications"`; no handler, menu or notification request. | EV-08 |
| #9 / AD24-EL-09 | Admin identity/avatar, header. | Static “TS. Quản Trị Viên / ADMIN / QUẢN TRỊ VIÊN”; no current-user source. | — |
| #10 / AD24-EL-10 | Global breadcrumb, shell. | Static `Hệ thống > Quản trị trung tâm > Không gian làm việc`; no route links. | EV-08 |
| #11 / AD24-EL-11 | RBAC verification badge, shell. | Static label; not evidence of server authorization. | — |
| #12 / AD24-EL-12 | Local breadcrumb. | Static `Báo cáo & Thống kê > Tác động cộng đồng`; no wired navigation behavior. | — |
| #13 / AD24-EL-13 | Screen ID badge. | Static `MÃ HỆ THỐNG: AD-24`; no API field. | — |
| #14 / AD24-EL-14 | Data-contract status badge. | Static “Hợp đồng dữ liệu cấp máy chủ”; it does not prove a current server contract is wired. | — |
| #15 / AD24-EL-15 | Page title, H1. | Static “Báo cáo tác động cộng đồng và đào tạo”. | — |
| #16 / AD24-EL-16 | Supporting description. | Static summary of learning interaction/completion/reach; no metric binding. | — |
| #17 / AD24-EL-17 | Export-to-AD-25 CTA, anchor. | `href="/admin/reports/export"`; no query parameters, URL state or API call. Target is an inventory candidate. | EV-07 |
| #18 / AD24-EL-18 | “Từ ngày” date input. | `<input type="date" id="filter-date-from" value="2025-01-01">`; current local value only. No min/max/validation/listener. Candidate #101 type `date`, #102 type `string`; exact serialization/default unresolved. | EV-02 |
| #19 / AD24-EL-19 | “Đến ngày” date input. | `<input type="date" id="filter-date-to" value="2025-03-31">`; no comparison with start date or approved default rule. | EV-02 |
| #20 / AD24-EL-20 | “Phân khúc học viên” select. | `id="filter-segment"`; values `all`, `interns`, `graduates`, `alumni`; `all` selected. Catalog #102 only allows a string; no approved option mapping. | EV-03 |
| #21 / AD24-EL-21 | “Áp dụng bộ lọc” button. | Enabled `type="button"`; handler toggles `opacity-80` for 300 ms and performs no validation/request/state update. | EV-04 |
| #22 / AD24-EL-22 | Reset-filters icon button. | `id="btn-reset-filters"`, title “Thiết lập lại bộ lọc”; sets fixed date values and `all`, no request/URL update. | EV-05 |
| #23 / AD24-EL-23 | Active-learners KPI card. | Title “Tổng học viên tích cực”; value `--`, unit “người”, static wait message; no API mapping or formula. | — |
| #24 / AD24-EL-24 | Completion-rate KPI card. | Title “Tỷ lệ hoàn thành chuyên đề”; value `--`, unit `%`, static wait message; no numerator/denominator/status/date rule. | — |
| #25 / AD24-EL-25 | Community-interaction-hours KPI card. | Title “Giờ học tương tác cộng đồng”; value `--`, unit “giờ”, static wait message; no duration source or unit conversion. | — |
| #26 / AD24-EL-26 | Overall-satisfaction KPI card. | Title “Chỉ số hài lòng chung”; value `--`, scale `/ 5.0`, static wait message; no survey/respondent/aggregation source. | — |
| #27 / AD24-EL-27 | Visualization / empty-chart panel. | Large white panel with no chart series, axes, range, legend or data source. | — |
| #28 / AD24-EL-28 | Empty-chart icon. | Decorative insights icon; no data semantics. | — |
| #29 / AD24-EL-29 | Empty-chart heading. | Static “Chưa có biểu đồ phân tích trực quan”; not a runtime API empty-result state. | — |
| #30 / AD24-EL-30 | Empty-chart explanatory copy. | Says metrics are being standardized and visualization will appear when contract activates; static design copy, not server response. | — |
| #31 / AD24-EL-31 | “Làm mới truy vấn dữ liệu” button. | `id="btn-refresh-telemetry"`; changes text and pointer-event/opacity for 900 ms, then resets; no API refresh/poll. | EV-06 |
| #32 / AD24-EL-32 | Data-contract version label. | Static `Phiên bản chuẩn hóa dữ liệu: v2.4-draft`; no version endpoint or contract version field. | — |
| #33 / AD24-EL-33 | Planned-metrics section heading/icon. | Static “Danh mục chỉ tiêu đo lường dự kiến triển khai”; informational section, not returned by Report. | — |
| #34 / AD24-EL-34 | “4 Hạng mục đang xác thực” badge. | Static count label; not an API count/state. | — |
| #35 / AD24-EL-35 | DAU/MAU specification card. | Static definition mentions daily forum participation over learner base; not a formula contract or source mapping. | — |
| #36 / AD24-EL-36 | Mentor interaction-hours specification card. | Static claim about 1-on-1 discussion/project feedback; no event/duration source confirmed. | — |
| #37 / AD24-EL-37 | Employment-readiness specification card. | Static claim about certification threshold/partner requirements; no outcome/certification source confirmed. | — |
| #38 / AD24-EL-38 | Partner NPS specification card. | Static partner survey after 30 days; no survey source/population/calculation confirmed. | — |
| #39 / AD24-EL-39 | Footer copyright. | Static text. | — |
| #40 / AD24-EL-40 | Footer privacy link. | Anchor `href="#"`; no destination. | EV-08 |
| #41 / AD24-EL-41 | Footer RBAC standards link. | Anchor `href="#"`; no destination. | EV-08 |
| #42 / AD24-EL-42 | Footer support link. | Anchor `href="#"`; no destination. | EV-08 |

## 4. Conditional UI & state variations
- States theo inventory: loading/no-data/partial/ready
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/05_admin/AD-24_bao-cao-tac-dong-cong-dong/AD-24.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
