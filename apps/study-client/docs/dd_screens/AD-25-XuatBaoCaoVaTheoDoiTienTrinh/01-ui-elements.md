# AD-25 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [AD-25_markers.json](../../screen_stitch/05_admin/AD-25_xuat-bao-cao-va-theo-doi-tien-trinh/AD-25_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `AD-25-EL-001` | `AD25-EL-01` | Study2Work brand / portal mark |
| #2 | `AD-25-EL-002` | `AD25-EL-02` | Main navigation group |
| #3 | `AD-25-EL-003` | `AD25-EL-03` | System Normal status badge |
| #4 | `AD-25-EL-004` | `AD25-EL-04` | Notifications button |
| #5 | `AD-25-EL-005` | `AD25-EL-05` | Admin identity / avatar |
| #6 | `AD-25-EL-006` | `AD25-EL-06` | Global breadcrumb |
| #7 | `AD-25-EL-007` | `AD25-EL-07` | RBAC verification badge |
| #8 | `AD-25-EL-008` | `AD25-EL-08` | Local report breadcrumb |
| #9 | `AD-25-EL-009` | `AD25-EL-09` | Screen ID badge: AD-25 |
| #10 | `AD-25-EL-010` | `AD25-EL-10` | Back-to-AD-24 anchor |
| #11 | `AD-25-EL-011` | `AD25-EL-11` | Page title |
| #12 | `AD-25-EL-012` | `AD25-EL-12` | Page description |
| #13 | `AD-25-EL-013` | `AD25-EL-13` | Worker-node badge |
| #14 | `AD-25-EL-014` | `AD25-EL-14` | Export security policy banner |
| #15 | `AD-25-EL-015` | `AD25-EL-15` | RBAC L3 badge |
| #16 | `AD-25-EL-016` | `AD25-EL-16` | Export configuration panel title |
| #17 | `AD-25-EL-017` | `AD25-EL-17` | Step 1/2 badge |
| #18 | `AD-25-EL-018` | `AD25-EL-18` | Format section heading and help |
| #19 | `AD-25-EL-019` | `AD25-EL-19` | CSV format option |
| #20 | `AD-25-EL-020` | `AD25-EL-20` | Excel XLSX format option |
| #21 | `AD-25-EL-021` | `AD25-EL-21` | PDF format option |
| #22 | `AD-25-EL-022` | `AD25-EL-22` | Dataset scope section heading and help |
| #23 | `AD-25-EL-023` | `AD25-EL-23` | Course summary scope |
| #24 | `AD-25-EL-024` | `AD25-EL-24` | Learner progress scope |
| #25 | `AD-25-EL-025` | `AD25-EL-25` | Community impact scope |
| #26 | `AD-25-EL-026` | `AD25-EL-26` | Time-range section heading and timezone |
| #27 | `AD-25-EL-027` | `AD25-EL-27` | Current week period option |
| #28 | `AD-25-EL-028` | `AD25-EL-28` | Current month period option |
| #29 | `AD-25-EL-029` | `AD25-EL-29` | Custom period option |
| #30 | `AD-25-EL-030` | `AD25-EL-30` | Processing-time note |
| #31 | `AD-25-EL-031` | `AD25-EL-31` | Start export task button |
| #32 | `AD-25-EL-032` | `AD25-EL-32` | Progress panel heading |
| #33 | `AD-25-EL-033` | `AD25-EL-33` | Monitor V2 badge |
| #34 | `AD-25-EL-034` | `AD25-EL-34` | Operation ID card |
| #35 | `AD-25-EL-035` | `AD25-EL-35` | Operation status card |
| #36 | `AD-25-EL-036` | `AD25-EL-36` | Empty download-result panel |
| #37 | `AD-25-EL-037` | `AD25-EL-37` | Disabled download button |
| #38 | `AD-25-EL-038` | `AD25-EL-38` | SH-07 queue handoff callout |
| #39 | `AD-25-EL-039` | `AD25-EL-39` | Export policy section heading |
| #40 | `AD-25-EL-040` | `AD25-EL-40` | Signed-link policy card |
| #41 | `AD-25-EL-041` | `AD25-EL-41` | Audit-log policy card |
| #42 | `AD-25-EL-042` | `AD25-EL-42` | Temporary-file deletion policy card |
| #43 | `AD-25-EL-043` | `AD25-EL-43` | Footer copyright |
| #44 | `AD-25-EL-044` | `AD25-EL-44` | Privacy-policy footer link |
| #45 | `AD-25-EL-045` | `AD25-EL-45` | RBAC-standards footer link |
| #46 | `AD-25-EL-046` | `AD25-EL-46` | System-support footer link |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả chi tiết từng element

Marker centers are source `screen.png` pixels; `screen_annotated.png` is a 2× render. All IDs map one-to-one to the marker JSON and plan. Current HTML attributes/states are not approved future export API values.

| Marker / Element ID | Tên, loại, vị trí | Thuộc tính, nguồn, điều kiện/trạng thái | Sự kiện |
|---|---|---|---|
| #1 / AD25-EL-01 | Study2Work brand/portal mark, header left. | Static mark and text; no current route link or identity source. | — |
| #2 / AD25-EL-02 | Main navigation group, header. | Five anchors use `href="#"`; destinations are not wired. | EV-09 |
| #3 / AD25-EL-03 | “System Normal” badge, header. | Static text/dot; no health endpoint or service status source. | — |
| #4 / AD25-EL-04 | Notifications icon button, header. | `type="button"`, `aria-label="Notifications"`; no handler/menu/request. | EV-09 |
| #5 / AD25-EL-05 | Admin identity/avatar, header. | Static “TS. Quản Trị Viên / ADMIN / QUẢN TRỊ VIÊN”; no current-user endpoint binding. | — |
| #6 / AD25-EL-06 | Global breadcrumb. | Static system/workspace path; not an implemented route trail. | EV-09 |
| #7 / AD25-EL-07 | RBAC verification badge. | Static label; not authentication, permission or audit evidence. | — |
| #8 / AD25-EL-08 | Local “Báo cáo & Thống kê > Xuất dữ liệu báo cáo” breadcrumb. | The parent anchor has `href="#"`; current target is not defined. | EV-09 |
| #9 / AD25-EL-09 | Screen ID badge. | Static `AD-25 • EXPORT TASK MANAGER`; no API data. | — |
| #10 / AD25-EL-10 | “Quay lại báo cáo tác động (AD-24)” anchor. | `href="#"`; does not navigate to AD-24 or transfer query state. | EV-08 |
| #11 / AD25-EL-11 | Page title, H1. | Static “Trích xuất dữ liệu và theo dõi tiến trình xuất báo cáo”. | — |
| #12 / AD25-EL-12 | Page description. | Static description of server-side batch export; no backend mapping. | — |
| #13 / AD25-EL-13 | Worker-node badge. | Static “Cụm xử lý ngầm (Worker Node 04)”; no worker registry/health source. | — |
| #14 / AD25-EL-14 | Export-security banner (shield, heading and explanatory copy). | Static copy asserts server processing, checksum and no browser cache; none is enforced by this page. | — |
| #15 / AD25-EL-15 | “TUÂN THỦ RBAC L3” badge, banner. | Static compliance assertion; no policy level field or guard mapping. | — |
| #16 / AD25-EL-16 | Export-configuration panel heading. | Static section title; no API state. | — |
| #17 / AD25-EL-17 | “BƯỚC 1/2” label. | Static step count; no step transition or second-step screen/flow exists in HTML. | — |
| #18 / AD25-EL-18 | Format section heading/help. | Static label “Yêu cầu chọn 01 định dạng”; no runtime validation is wired to it. | — |
| #19 / AD25-EL-19 | CSV format card/radio. | `name="file_format"`, `value="csv"`, initially checked; native local selection only. API #103 format string has no approved enum/default mapping. | EV-02 |
| #20 / AD25-EL-20 | Excel/XLSX format card/radio. | `name="file_format"`, `value="xlsx"`; native local selection only. | EV-02 |
| #21 / AD25-EL-21 | PDF format card/radio. | `name="file_format"`, `value="pdf"`; native local selection only. | EV-02 |
| #22 / AD25-EL-22 | Dataset-scope section heading/help. | Static “Cho phép chọn nhiều mục”; no min/max selection or scope mapping contract. | — |
| #23 / AD25-EL-23 | Course-summary checkbox row. | `name="scope_course"`, checked; no explicit `value` attribute; label says course counts/enrollment/completion. Not mapped to #103 filters. | EV-03 |
| #24 / AD25-EL-24 | Learner-progress checkbox row. | `name="scope_learner"`, checked; no explicit `value`; mockup description has project/mentor data claims without source mapping. | EV-03 |
| #25 / AD25-EL-25 | Community-impact checkbox row. | `name="scope_impact"`, unchecked; no explicit `value`; text claims employment/business impact not approved by #102. | EV-03 |
| #26 / AD25-EL-26 | Time-range section heading and timezone note. | Static period label and `GMT+7`; timezone/default date semantics are not an API #103 contract. | — |
| #27 / AD25-EL-27 | “Tuần hiện tại” radio card. | `name="time_range"`, `value="week"`; no date boundary calculation. | EV-04 |
| #28 / AD25-EL-28 | “Tháng hiện tại” radio card. | `name="time_range"`, `value="month"`, initially checked; no date boundary calculation. | EV-04 |
| #29 / AD25-EL-29 | “Tùy chỉnh kỳ” radio card. | `name="time_range"`, `value="custom"`; no date inputs or custom selection flow. | EV-04 |
| #30 / AD25-EL-30 | Processing-time note. | Static “Thời gian xử lý phụ thuộc khối lượng dữ liệu thực tế”; no estimate/progress source. | — |
| #31 / AD25-EL-31 | “Bắt đầu tạo tác vụ xuất file” submit button. | `id="btn-create-task"`, `type="submit"`; form inline handler prevents default, no loading/disabled/error state transition. | EV-05 |
| #32 / AD25-EL-32 | Progress-panel heading. | Static “Theo dõi trạng thái tiến trình”; no polling or refresh source. | — |
| #33 / AD25-EL-33 | “MONITOR V2” badge. | Static version text; no monitor service or version endpoint. | — |
| #34 / AD25-EL-34 | Operation ID card. | Static “Chưa phát sinh tác vụ” plus Celery auto-ID claim; no ID field/state and no Celery integration. | EV-01 |
| #35 / AD25-EL-35 | Operation status card. | Static “Sẵn sàng khởi tạo” and confirmation copy; it is not an `Operation.status` response. | EV-01 |
| #36 / AD25-EL-36 | Empty result/download panel. | Static folder icon, heading and no-link text; no `ExportAsset` source or expiry state. | EV-01 |
| #37 / AD25-EL-37 | “Tải tệp báo cáo” button. | `type="button"`, `disabled`, `aria-disabled="true"`; no URL, anchor, checksum validation or handler. | EV-06 |
| #38 / AD25-EL-38 | SH-07 queue handoff callout. | Static “Chuyển sang SH-07 khi có Operation ID được cấp” and queue badge; no link, route, ID or status mapping. | EV-07 |
| #39 / AD25-EL-39 | Export policy section heading. | Static section title; no policy API. | — |
| #40 / AD25-EL-40 | Signed-link policy card. | Static “Signed URL” maximum 120 minutes claim; no URL issuer/TTL source. | — |
| #41 / AD25-EL-41 | Audit-log policy card. | Static claim that configuration/download, IP and Admin session are logged; no audit endpoint/event source. | — |
| #42 / AD25-EL-42 | Temporary-file deletion policy card. | Static permanent-delete-after-24-hours claim; no retention/cleanup source. | — |
| #43 / AD25-EL-43 | Copyright footer. | Static `© 2025 Study2Work LMS`; no event. | — |
| #44 / AD25-EL-44 | Privacy-policy footer link. | `href="#"`; no destination. | EV-09 |
| #45 / AD25-EL-45 | RBAC-standards footer link. | `href="#"`; no destination. | EV-09 |
| #46 / AD25-EL-46 | System-support footer link. | `href="#"`; no destination. | EV-09 |

## 4. Conditional UI & state variations
- States theo inventory: expected: queued/processing/ready/failed/expired; current: static/submit-blocked/download-disabled
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/05_admin/AD-25_xuat-bao-cao-va-theo-doi-tien-trinh/AD-25.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
