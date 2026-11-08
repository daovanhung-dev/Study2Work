# AD-10 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [AD-10_markers.json](../../screen_stitch/05_admin/AD-10_hang-doi-kiem-duyet-noi-dung/AD-10_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `AD-10-EL-001` | `not supplied in marker JSON` | Study2Work LMS Admin brand |
| #2 | `AD-10-EL-002` | `not supplied in marker JSON` | Admin navigation: Tổng quan |
| #3 | `AD-10-EL-003` | `not supplied in marker JSON` | Admin navigation: Người dùng |
| #4 | `AD-10-EL-004` | `not supplied in marker JSON` | Admin navigation: Khóa học và Nội dung |
| #5 | `AD-10-EL-005` | `not supplied in marker JSON` | Active Admin navigation: Kiểm duyệt |
| #6 | `AD-10-EL-006` | `not supplied in marker JSON` | Admin navigation: Báo cáo |
| #7 | `AD-10-EL-007` | `not supplied in marker JSON` | Static SYSTEM NORMAL badge |
| #8 | `AD-10-EL-008` | `not supplied in marker JSON` | Notifications button without handler |
| #9 | `AD-10-EL-009` | `not supplied in marker JSON` | Static Admin identity and avatar |
| #10 | `AD-10-EL-010` | `not supplied in marker JSON` | Global breadcrumb trail |
| #11 | `AD-10-EL-011` | `not supplied in marker JSON` | Static RBAC assurance badge |
| #12 | `AD-10-EL-012` | `not supplied in marker JSON` | Local content moderation breadcrumb |
| #13 | `AD-10-EL-013` | `not supplied in marker JSON` | Static API #78 ACTIVE badge |
| #14 | `AD-10-EL-014` | `not supplied in marker JSON` | Pending Content queue page title |
| #15 | `AD-10-EL-015` | `not supplied in marker JSON` | Static description of moderation queue |
| #16 | `AD-10-EL-016` | `not supplied in marker JSON` | Static portal status card |
| #17 | `AD-10-EL-017` | `not supplied in marker JSON` | Static Admin RBAC tier card |
| #18 | `AD-10-EL-018` | `not supplied in marker JSON` | Keyword input for title or lecturer; no handler |
| #19 | `AD-10-EL-019` | `not supplied in marker JSON` | Content type select with synthetic values |
| #20 | `AD-10-EL-020` | `not supplied in marker JSON` | Course select with slug values, not int64 IDs |
| #21 | `AD-10-EL-021` | `not supplied in marker JSON` | Refresh button with local animation only |
| #22 | `AD-10-EL-022` | `not supplied in marker JSON` | Seven-column pending Content table header |
| #23 | `AD-10-EL-023` | `not supplied in marker JSON` | Static empty-queue icon |
| #24 | `AD-10-EL-024` | `not supplied in marker JSON` | Static empty-queue heading |
| #25 | `AD-10-EL-025` | `not supplied in marker JSON` | Static empty-queue explanation |
| #26 | `AD-10-EL-026` | `not supplied in marker JSON` | Disabled check-new-content button |
| #27 | `AD-10-EL-027` | `not supplied in marker JSON` | Static 30-second sync frequency claim |
| #28 | `AD-10-EL-028` | `not supplied in marker JSON` | Static shown/total Content count |
| #29 | `AD-10-EL-029` | `not supplied in marker JSON` | Disabled previous-page button |
| #30 | `AD-10-EL-030` | `not supplied in marker JSON` | Static current page number 1 |
| #31 | `AD-10-EL-031` | `not supplied in marker JSON` | Disabled next-page button |
| #32 | `AD-10-EL-032` | `not supplied in marker JSON` | Static moderation-policy notice icon |
| #33 | `AD-10-EL-033` | `not supplied in marker JSON` | Static Study2Work moderation standard heading |
| #34 | `AD-10-EL-034` | `not supplied in marker JSON` | Static copyright and pedagogical standards copy |
| #35 | `AD-10-EL-035` | `not supplied in marker JSON` | Rubric link with href hash |
| #36 | `AD-10-EL-036` | `not supplied in marker JSON` | Static footer copyright |
| #37 | `AD-10-EL-037` | `not supplied in marker JSON` | Privacy policy footer link with href hash |
| #38 | `AD-10-EL-038` | `not supplied in marker JSON` | RBAC standards footer link with href hash |
| #39 | `AD-10-EL-039` | `not supplied in marker JSON` | Technical support footer link with href hash |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả chi tiết từng element

Tọa độ `(x,y)` tính bằng pixel trên `screen.png` 1600×1461 và lưu chính xác trong [marker map](../../screen_stitch/05_admin/AD-10_hang-doi-kiem-duyet-noi-dung/AD-10_markers.json). Label, value, status card, count và policy copy hiện đều là nội dung prototype; chúng không xác nhận runtime data hoặc policy. Các hàng gộp chỉ khi một marker đại diện cho cùng một nhóm UI như header bảng.

| ID | Element / vị trí / mục đích | Thuộc tính, nguồn dữ liệu, validation | Hiển thị / trạng thái | Event |
|---:|---|---|---|---|
| #1 | Brand Study2Work/LMS Admin, header `(12,35)`; nhận diện portal. | Logo chữ “S”, tên và ADMIN PORTAL tĩnh; không lấy từ API. | Visible, static. | EV-08. |
| #2 | Nav “Tổng quan”, header `(322,12)`. | Anchor `href="#"`; không có route đích. | Visible, inactive style. | EV-08. |
| #3 | Nav “Người dùng”, header `(460,12)`. | Anchor `href="#"`; không có route đích. | Visible, inactive style. | EV-08. |
| #4 | Nav “Khóa học & Nội dung”, header `(680,12)`. | Anchor `href="#"`; không có route đích. | Visible, inactive style. | EV-08. |
| #5 | Nav “Kiểm duyệt”, header `(851,12)`. | Anchor `href="#"`, `aria-current="page"`; trạng thái active chỉ là HTML/style. | Visible, active style. | EV-08. |
| #6 | Nav “Báo cáo”, header `(989,12)`. | Anchor `href="#"`; không có route đích. | Visible, inactive style. | EV-08. |
| #7 | Badge “SYSTEM NORMAL”, header `(1144,12)`; hiển thị trạng thái cổng. | Text hard-coded, không có health/monitoring API. | Visible theo breakpoint; static. | EV-08. |
| #8 | Nút notification, header `(1284,12)`. | Button `aria-label="Notifications"`; không có handler, payload hay unread API. | Visible, enabled native button nhưng no-op. | EV-08. |
| #9 | Tên/role và avatar Admin, header `(1576,12)`. | “TS. Quản Trị Viên” và “ADMIN / QUẢN TRỊ VIÊN” hard-coded; không gắn session/profile. | Visible theo breakpoint; static. | EV-08. |
| #10 | Global breadcrumb, hàng header thứ hai `(17,96)`. | Home icon và nhãn vị trí tĩnh; một số span có cursor style nhưng không route. | Visible. | EV-08. |
| #11 | Badge “Chuẩn xác thực RBAC”, header `(1577,96)`. | Icon/text tĩnh; không phải kết quả authorization. | Visible theo breakpoint; static. | EV-08. |
| #12 | Breadcrumb “Kiểm duyệt đào tạo > Hàng đợi nội dung chờ duyệt”, `(17,169)`. | Nội dung tĩnh; không đồng bộ router/history. | Visible. | EV-08. |
| #13 | Badge “API #78 ACTIVE”, `(588,170)`. | Copy hard-coded; không đọc trạng thái deploy/API. | Visible, static. | EV-08. |
| #14 | Tiêu đề “Hàng đợi kiểm duyệt nội dung”, vùng title `(675,260)`. | Heading tĩnh. | Visible. | Không có. |
| #15 | Mô tả queue dưới heading `(1000,310)`. | Copy tĩnh; không xác nhận SLA hoặc workflow đã hoạt động. | Visible. | Không có. |
| #16 | Status card “Trạng thái cổng / Cổng ghi nhận tự động”, `(1296,295)`. | Dot và text tĩnh; không có monitoring/status source. | Visible, static. | EV-08. |
| #17 | Status card “Chuẩn RBAC / Cấp Admin Đào Tạo”, `(1544,302)`. | Badge tĩnh; không chứng minh role/permission đã được kiểm tra. | Visible, static. | EV-08. |
| #18 | Search input theo title/lecturer, filters row `(593,433)`. | `<input type="text">`; không `name`, value mặc định rỗng, placeholder là copy; không có max length/validation hoặc handler. #78 không có keyword query. | Visible, editable; hiện chỉ nhận text DOM. | EV-02. |
| #19 | Select định dạng, `(921,401)`. | Option hiện có: `all`, `video`, `doc`, `quiz`; không có name/handler. API nhận raw exact `type`, enum/casing chưa xác nhận. | Visible, mặc định `all`; native select. | EV-03. |
| #20 | Select khóa học, `(1307,401)`. | Option hiện có `all`, `fe`, `be`, `devops`, `data`; giá trị mẫu là slug, không phải `course:int64`; không có name/handler. | Visible, mặc định `all`; native select. | EV-04. |
| #21 | Nút “Làm mới hàng đợi”, `(1546,434)`. | Button `id=btn-refresh-queue`; script thêm spin/disabled rồi gỡ sau 700 ms. Không request. | Visible; transient local loading; không có server result. | EV-05. |
| #22 | Header table bảy cột, `(1577,541)`: content ID, title, type, course, lecturer, submitted time, action. | `<th scope="col">`; không có row data trong mockup. #78 không đủ dữ liệu cho course title/lecturer/time. | Header visible; table body ở empty state. | EV-01/EV-06. |
| #23 | Icon empty queue, `(725,744)`. | Icon `rule` và vòng nền tĩnh. | Visible chỉ trong empty prototype. | Không có. |
| #24 | Heading “Hàng đợi kiểm duyệt hiện đang trống”, `(1090,857)`. | Copy tĩnh; không bind response. | Visible trong screenshot empty. | EV-01. |
| #25 | Empty explanation, `(1085,900)`. | Copy nói không có Content và tự động xếp vào queue; đây là claim mockup, không phải SLA/producer evidence. | Visible trong screenshot empty. | EV-01. |
| #26 | Nút “Kiểm tra nội dung mới”, `(949,990)`. | `button disabled`; không handler/API. | Visible, disabled. | EV-05; không trigger được. |
| #27 | Copy “Tần suất đồng bộ tự động: 30 giây/lần”, `(950,1041)`. | Text hard-coded; HTML không có interval/timer tương ứng. | Visible, static. | EV-05. |
| #28 | Summary “Hiển thị 0 trên 0 nội dung chờ duyệt”, `(381,1194)`. | Values hard-coded; local API nếu dùng có `pagination.total`, nhưng UI mapping chưa wire. | Visible, static `0/0`. | EV-01/EV-07. |
| #29 | Nút Previous, `(1248,1195)`. | Native button disabled trong mockup. | Visible, disabled. | EV-07; không trigger được. |
| #30 | Current page `1`, `(1400,1161)`. | Text tĩnh; local API page mặc định 1 là DERIVED fallback. | Visible, static. | EV-07. |
| #31 | Nút Next, `(1542,1195)`. | Native button disabled trong mockup. | Visible, disabled. | EV-07; không trigger được. |
| #32 | Icon notice chuẩn thẩm định, `(49,1314)`. | Icon shield/check tĩnh; không phải enforcement signal. | Visible. | EV-08. |
| #33 | Heading “TIÊU CHUẨN THẨM ĐỊNH STUDY2WORK”, `(470,1283)`. | Copy tĩnh; rubric contract/source chưa được nối. | Visible. | EV-08. |
| #34 | Nội dung bản quyền/sư phạm, `(1041,1325)`. | Statement tĩnh; không được #78 xác nhận. | Visible. | EV-08. |
| #35 | Link “Xem bộ rubric thẩm định”, `(1543,1317)`. | Anchor `href="#"`; không destination/resource id. | Visible, link no-op. | EV-08. |
| #36 | Footer copyright và “Hệ thống quản trị trung tâm”, `(12,1432)`. | Text `© 2025` tĩnh. | Visible. | Không có. |
| #37 | Footer privacy link, `(1091,1432)`. | Anchor `href="#"`; không policy URL. | Visible. | EV-08. |
| #38 | Footer RBAC standards link, `(1294,1432)`. | Anchor `href="#"`; không policy URL. | Visible. | EV-08. |
| #39 | Footer technical support link, `(1580,1432)`. | Anchor `href="#"`; không support destination. | Visible. | EV-08. |

## 4. Conditional UI & state variations
- States theo inventory: loading/empty/ready/error
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/05_admin/AD-10_hang-doi-kiem-duyet-noi-dung/AD-10.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
