# AD-19 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [AD-19_markers.json](../../screen_stitch/05_admin/AD-19_danh-sach-thong-bao-quan-tri/AD-19_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `AD-19-EL-001` | `not supplied in marker JSON` | Brand / LMS header |
| #2 | `AD-19-EL-002` | `not supplied in marker JSON` | Shell navigation — Tổng quan |
| #3 | `AD-19-EL-003` | `not supplied in marker JSON` | Shell navigation — Người dùng |
| #4 | `AD-19-EL-004` | `not supplied in marker JSON` | Shell navigation — Khóa học & Nội dung |
| #5 | `AD-19-EL-005` | `not supplied in marker JSON` | Shell navigation — Kiểm duyệt |
| #6 | `AD-19-EL-006` | `not supplied in marker JSON` | Shell navigation — Báo cáo |
| #7 | `AD-19-EL-007` | `not supplied in marker JSON` | System Normal status copy (static) |
| #8 | `AD-19-EL-008` | `not supplied in marker JSON` | Header notifications icon (no handler) |
| #9 | `AD-19-EL-009` | `not supplied in marker JSON` | Admin identity and avatar (static) |
| #10 | `AD-19-EL-010` | `not supplied in marker JSON` | Global breadcrumb |
| #11 | `AD-19-EL-011` | `not supplied in marker JSON` | RBAC assurance badge/copy (static) |
| #12 | `AD-19-EL-012` | `not supplied in marker JSON` | Local breadcrumb — Quản trị thông báo |
| #13 | `AD-19-EL-013` | `not supplied in marker JSON` | Screen title |
| #14 | `AD-19-EL-014` | `not supplied in marker JSON` | Screen description |
| #15 | `AD-19-EL-015` | `not supplied in marker JSON` | Create notification CTA — AD-20 candidate |
| #16 | `AD-19-EL-016` | `not supplied in marker JSON` | Metric card — total notifications |
| #17 | `AD-19-EL-017` | `not supplied in marker JSON` | Metric card — published |
| #18 | `AD-19-EL-018` | `not supplied in marker JSON` | Metric card — scheduled |
| #19 | `AD-19-EL-019` | `not supplied in marker JSON` | Metric card — drafts |
| #20 | `AD-19-EL-020` | `not supplied in marker JSON` | Title search input (no handler) |
| #21 | `AD-19-EL-021` | `not supplied in marker JSON` | Channel select |
| #22 | `AD-19-EL-022` | `not supplied in marker JSON` | Status select |
| #23 | `AD-19-EL-023` | `not supplied in marker JSON` | Reset filters button |
| #24 | `AD-19-EL-024` | `not supplied in marker JSON` | Table column — notification ID |
| #25 | `AD-19-EL-025` | `not supplied in marker JSON` | Table column — title |
| #26 | `AD-19-EL-026` | `not supplied in marker JSON` | Table column — recipient |
| #27 | `AD-19-EL-027` | `not supplied in marker JSON` | Table column — delivery channel |
| #28 | `AD-19-EL-028` | `not supplied in marker JSON` | Table column — send time |
| #29 | `AD-19-EL-029` | `not supplied in marker JSON` | Table column — status |
| #30 | `AD-19-EL-030` | `not supplied in marker JSON` | Table column — actions |
| #31 | `AD-19-EL-031` | `not supplied in marker JSON` | Empty-state illustration |
| #32 | `AD-19-EL-032` | `not supplied in marker JSON` | Empty-state title |
| #33 | `AD-19-EL-033` | `not supplied in marker JSON` | Empty-state explanatory copy |
| #34 | `AD-19-EL-034` | `not supplied in marker JSON` | Refresh list button (timer only) |
| #35 | `AD-19-EL-035` | `not supplied in marker JSON` | Result count summary |
| #36 | `AD-19-EL-036` | `not supplied in marker JSON` | Pagination — first page (disabled) |
| #37 | `AD-19-EL-037` | `not supplied in marker JSON` | Pagination — previous page (disabled) |
| #38 | `AD-19-EL-038` | `not supplied in marker JSON` | Pagination — current/total display |
| #39 | `AD-19-EL-039` | `not supplied in marker JSON` | Pagination — next page (disabled) |
| #40 | `AD-19-EL-040` | `not supplied in marker JSON` | Pagination — last page (disabled) |
| #41 | `AD-19-EL-041` | `not supplied in marker JSON` | Policy banner information icon |
| #42 | `AD-19-EL-042` | `not supplied in marker JSON` | Policy banner title |
| #43 | `AD-19-EL-043` | `not supplied in marker JSON` | Policy banner description (static 30-minute claim) |
| #44 | `AD-19-EL-044` | `not supplied in marker JSON` | Policy / guideline link (unmapped target) |
| #45 | `AD-19-EL-045` | `not supplied in marker JSON` | Footer copyright and system label |
| #46 | `AD-19-EL-046` | `not supplied in marker JSON` | Footer privacy link (href #) |
| #47 | `AD-19-EL-047` | `not supplied in marker JSON` | Footer RBAC standards link (href #) |
| #48 | `AD-19-EL-048` | `not supplied in marker JSON` | Footer technical support link (href #) |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả chi tiết từng element

Marker coordinates use the original 1600×1411 screen coordinate space. JSON, SVG and annotated image use the same ordered IDs.

| ID | Tọa độ nguồn (x,y) | Tên / loại / vị trí | Thuộc tính, nguồn và ràng buộc | Hiển thị / trạng thái hiện tại | Event |
|---:|---|---|---|---|
| 1 | 12,65 | Study2Work LMS brand; logo/wordmark, header trái | Text/logo tĩnh trong HTML; không phải auth identity. | Hiện trong shell; không có trạng thái tương tác được wire. | — |
| 2 | 356,65 | Tổng quan; nav link | Anchor href #; không có route target. | Hiện; hover style chỉ là CSS. | EV-10 |
| 3 | 491,65 | Người dùng; nav link | Anchor href #; không có route target. | Hiện; hover style chỉ là CSS. | EV-10 |
| 4 | 660,65 | Khóa học & Nội dung; nav link | Anchor href #; không có route target. | Hiện; hover style chỉ là CSS. | EV-10 |
| 5 | 856,65 | Kiểm duyệt; nav link | Anchor href #; không có route target. | Hiện; hover style chỉ là CSS. | EV-10 |
| 6 | 982,65 | Báo cáo; nav link | Anchor href #; không có route target. | Hiện; hover style chỉ là CSS. | EV-10 |
| 7 | 1154,65 | System Normal; status pill | Chuỗi và pulse CSS tĩnh, không đọc health API. | Hiện; không phải trạng thái runtime. | — |
| 8 | 1281,65 | Notifications; icon button | aria-label Notifications; không có handler/request/target. | Hiện, nhìn như enabled; chức năng không wire. | EV-10 |
| 9 | 1460,65 | Admin identity/avatar; profile summary | Tên, role label và icon hard-coded. Không suy token claims từ text. | Hiện; không có profile API. | — |
| 10 | 20,110 | Global breadcrumb; breadcrumb group | Home, Hệ thống, Quản trị trung tâm, Không gian làm việc; một số spans chỉ có cursor style. | Hiện; không có router state. | EV-10 |
| 11 | 1580,110 | RBAC assurance; badge/copy | Chuỗi Chuẩn xác thực RBAC và icon tĩnh; không chứng minh quyền được kiểm tra. | Hiện; không nhận state từ auth server. | — |
| 12 | 390,151 | Breadcrumb cục bộ; navigation text | Quản trị truyền thông > Thông báo hệ thống theo screenshot. Không có href/state. | Hiện; nội dung tĩnh. | — |
| 13 | 720,174 | Screen title; heading | Quản lý thông báo và bản tin hệ thống; text tĩnh. | Hiện trong empty screenshot. | — |
| 14 | 872,266 | Screen description; supporting text | Mô tả theo dõi/soạn/điều phối; không phải API capability proof. | Hiện; tĩnh. | — |
| 15 | 1543,194 | Soạn thông báo mới (AD-20); CTA anchor/button | href /admin/notifications/create. Inventory AD-20 là /admin/notifications/new. | Enabled-looking; target/router unresolved. | EV-06 |
| 16 | 392,301 | Tổng số thông báo; metric card | Giá trị 0 và copy “Thời gian thực”; không có metric field/API mapping. | Static 0; không tính từ Page hiện tại. | — |
| 17 | 777,301 | Đã phát hành; metric card | Giá trị 0, “Kênh hợp lệ”; status definition/API nguồn không có. | Static 0; không tính từ page. | — |
| 18 | 1162,301 | Đã lên lịch; metric card | Giá trị 0, “Hàng đợi truyền tin”; scheduled_at/metric source chưa có. | Static 0; không tính từ page. | — |
| 19 | 1545,301 | Bản nháp lưu tạm; metric card | Giá trị 0; #92 query hiện chỉ gồm notification có delivery rows. | Static 0; draft semantics chưa có. | — |
| 20 | 879,489 | Tìm kiếm tiêu đề; text input | Placeholder tìm theo tiêu đề; không có required/length/debounce contract hoặc event listener. API #92 không có search query. | Có thể nhập trong HTML nhưng không lọc/gọi request. | EV-02 |
| 21 | 925,459 | Kênh phát hành; select | Options: all, app, email, system. Local filter values chỉ EMAIL/PUSH; mapping chưa được duyệt. | HTML select có thể thao tác; không gửi request. | EV-03 |
| 22 | 1198,459 | Trạng thái; select | Options: all, draft, scheduled, published. Local status values FAILED/QUEUED/SENT. | HTML select có thể thao tác; không gửi request. | EV-03 |
| 23 | 1421,459 | Đặt lại; button | Reset input/select bằng JS. Không có API request hay pagination reset. | Enabled-looking; thay đổi control state cục bộ. | EV-04 |
| 24 | 78,568 | Table header — Mã thông báo | Column header; candidate mapping id:int64 only if an approved list item exists. | Header only; no data row. | — |
| 25 | 270,568 | Table header — Tiêu đề bản tin | Candidate field title:string. | Header only; no data row. | — |
| 26 | 610,568 | Table header — Đối tượng nhận | No recipient field in catalog Notification or local #92 projection. | Header only; unmapped column. | — |
| 27 | 858,568 | Table header — Kênh truyền tin | Candidate channels:NotificationChannel[]; local EMAIL/PUSH aggregate. | Header only; no row or approved enum display. | — |
| 28 | 1076,568 | Table header — Thời điểm gửi | No send-time field in catalog Notification; optional scheduled_at is not sent_at and local source omits it. | Header only; unmapped column. | — |
| 29 | 1282,568 | Table header — Trạng thái | Candidate status field; enum values absent from catalog and differ from mockup. | Header only; no mapped badge/state. | — |
| 30 | 1485,568 | Table header — Thao tác | No action control in empty row; AD-21 relationship expected by inventory. | Header only; row action not defined/wired. | EV-07 |
| 31 | 861,724 | Empty-state illustration; decorative icon | Static icon indicating no notification. | Visible in screenshot; does not prove an empty API response. | — |
| 32 | 555,837 | Empty-state title | “Chưa có thông báo nào trong danh sách”. Static copy. | Visible; no runtime state binding. | — |
| 33 | 1086,875 | Empty-state explanatory text | Suggests none recorded or data syncing; no sync state/API backs the claim. | Visible; do not represent as verified server state. | — |
| 34 | 633,965 | Làm mới danh sách thông báo; button | Handler spins/disables 800ms then restores; no fetch/XHR. | Enabled-looking; local timer animation only. | EV-05 |
| 35 | 291,1110 | “Hiển thị 0 trên 0 thông báo”; result summary | Placeholder values; local Page could provide total only if approved. | Static 0/0. | EV-01, EV-08 |
| 36 | 1277,1114 | Pagination — first page; button | aria-label Trang đầu tiên; disabled in HTML. | Disabled. | EV-08 |
| 37 | 1329,1114 | Pagination — previous page; button | aria-label Trang trước; disabled in HTML. | Disabled. | EV-08 |
| 38 | 1394,1114 | Pagination indicator | Static 0 / 0; local Page metadata only in derived source. | Static; not connected to page state. | EV-08 |
| 39 | 1456,1114 | Pagination — next page; button | aria-label Trang kế tiếp; disabled in HTML. | Disabled. | EV-08 |
| 40 | 1508,1114 | Pagination — last page; button | aria-label Trang cuối cùng; disabled in HTML. | Disabled. | EV-08 |
| 41 | 74,1234 | Policy information icon | Decorative icon in policy banner. | Visible; no policy API. | — |
| 42 | 567,1234 | Policy banner title | Quy chuẩn phát hành thông báo nội bộ LMS. No source policy identified in AC-36/#92. | Static. | — |
| 43 | 1189,1234 | Policy banner description | Claims minimum 30-minute review before Email/mobile delivery. Not established by catalog, AC-36 or #92 source. | Static; not a validated rule. | — |
| 44 | 1532,1234 | Xem quy chuẩn phát hành; link | href /admin/guidelines/notifications; no matching inventory item/router target found. | Enabled-looking; destination unresolved. | EV-09 |
| 45 | 64,1352 | Copyright/system label | Copyright 2025 and system text; static. | Visible. | — |
| 46 | 1020,1352 | Privacy policy; footer link | href #; destination not wired. | Visible anchor; no target. | EV-10 |
| 47 | 1221,1352 | RBAC standards; footer link | href #; destination not wired. | Visible anchor; no target. | EV-10 |
| 48 | 1430,1352 | System technical support; footer link | href #; destination not wired. | Visible anchor; no target. | EV-10 |

### Design-system review

The source screenshot uses a cobalt primary (#004ac6) and Plus Jakarta Sans from a remote font import. The Study Web guide defines ocean-primary #0B5F8A, Inter if already available (otherwise system sans-serif), responsive reflow, and content width up to about 1120px. The screenshot is retained unchanged as the design input; a future implementation should follow the Study Web guide after layout approval. No permission is implied to add a new route, API field, data flow or backend behavior. Accessibility details must be verified in implementation; screenshot alone does not establish keyboard, focus, responsive or reduced-motion behavior.

## 4. Conditional UI & state variations
- States theo inventory: unwired/loading/empty/ready/unauthorized/forbidden/validation-error/dependency-error/server-error
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/05_admin/AD-19_danh-sach-thong-bao-quan-tri/AD-19.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
