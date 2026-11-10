# AD-01 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [AD-01_markers.json](../../screen_stitch/05_admin/AD-01_dashboard-quan-tri/AD-01_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `AD-01-EL-001` | `not supplied in marker JSON` | Study2Work LMS Admin brand |
| #2 | `AD-01-EL-002` | `not supplied in marker JSON` | Primary navigation group and five anchors |
| #3 | `AD-01-EL-003` | `not supplied in marker JSON` | System Normal status pill |
| #4 | `AD-01-EL-004` | `not supplied in marker JSON` | Notifications button |
| #5 | `AD-01-EL-005` | `not supplied in marker JSON` | Current Admin identity and avatar block |
| #6 | `AD-01-EL-006` | `not supplied in marker JSON` | Global breadcrumb trail |
| #7 | `AD-01-EL-007` | `not supplied in marker JSON` | RBAC compliance badge |
| #8 | `AD-01-EL-008` | `not supplied in marker JSON` | Dashboard page breadcrumb |
| #9 | `AD-01-EL-009` | `not supplied in marker JSON` | Operations readiness status pill |
| #10 | `AD-01-EL-010` | `not supplied in marker JSON` | Dashboard hero label, title and description |
| #11 | `AD-01-EL-011` | `not supplied in marker JSON` | Disabled date range segmented control |
| #12 | `AD-01-EL-012` | `not supplied in marker JSON` | Refresh metrics button |
| #13 | `AD-01-EL-013` | `not supplied in marker JSON` | System users KPI card |
| #14 | `AD-01-EL-014` | `not supplied in marker JSON` | Learning programs KPI card |
| #15 | `AD-01-EL-015` | `not supplied in marker JSON` | Quality review KPI card |
| #16 | `AD-01-EL-016` | `not supplied in marker JSON` | Online infrastructure KPI card |
| #17 | `AD-01-EL-017` | `not supplied in marker JSON` | Recent system activity panel heading |
| #18 | `AD-01-EL-018` | `not supplied in marker JSON` | Security audit badge |
| #19 | `AD-01-EL-019` | `not supplied in marker JSON` | Activity empty-state icon and copy |
| #20 | `AD-01-EL-020` | `not supplied in marker JSON` | ISO IEC 27001 compliance claim |
| #21 | `AD-01-EL-021` | `not supplied in marker JSON` | No status changes in 24 hours copy |
| #22 | `AD-01-EL-022` | `not supplied in marker JSON` | Disabled audit log button |
| #23 | `AD-01-EL-023` | `not supplied in marker JSON` | Server operations panel heading and overall status dot |
| #24 | `AD-01-EL-024` | `not supplied in marker JSON` | Database status row |
| #25 | `AD-01-EL-025` | `not supplied in marker JSON` | Authentication service status row |
| #26 | `AD-01-EL-026` | `not supplied in marker JSON` | Background task queue status row |
| #27 | `AD-01-EL-027` | `not supplied in marker JSON` | Admin permissions notice |
| #28 | `AD-01-EL-028` | `not supplied in marker JSON` | Direct management shortcuts heading and caption |
| #29 | `AD-01-EL-029` | `not supplied in marker JSON` | Manage users shortcut card |
| #30 | `AD-01-EL-030` | `not supplied in marker JSON` | Manage courses shortcut card |
| #31 | `AD-01-EL-031` | `not supplied in marker JSON` | Moderation queue shortcut card |
| #32 | `AD-01-EL-032` | `not supplied in marker JSON` | Footer copyright and system label |
| #33 | `AD-01-EL-033` | `not supplied in marker JSON` | Privacy policy footer link |
| #34 | `AD-01-EL-034` | `not supplied in marker JSON` | RBAC standards footer link |
| #35 | `AD-01-EL-035` | `not supplied in marker JSON` | Technical support footer link |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả element

Mỗi marker đại diện một component/control. Label, icon và nội dung con được nhóm khi chúng cùng tạo thành một control/card; từng lựa chọn điều khiển được nêu riêng trong dòng tương ứng. Element ID khớp số marker trên ảnh.

| ID | Tên / loại | Vị trí, thuộc tính, mục đích | Nguồn, visibility/state, validation | Event |
|---:|---|---|---|---|
| 1 | Study2Work LMS Admin brand — brand block | Header trái: chữ S, Study2Work, LMS, ADMIN PORTAL. Nhận diện shell. | Static HTML; visible; không có destination/click handler. | — |
| 2 | Primary navigation group — nav/anchors | Năm mục Tổng quan (active), Người dùng, Khóa học & Nội dung, Kiểm duyệt, Báo cáo. HTML có `data-path`; cả năm `href="#"`. | Tổng quan có `aria-current="page"`; `data-path` không phải route mapping. Không có Study Router. | EV-04 |
| 3 | System Normal pill — status badge | Header: chấm xanh và “SYSTEM NORMAL”. | Static claim, không có source/threshold; không chứng minh tình trạng runtime. | — |
| 4 | Notifications — icon button | Header chuông, chấm đỏ; `aria-label="Notifications"`. | Enabled về markup, nhưng không listener, count model hay API. | EV-05 |
| 5 | Current Admin identity — profile block | Tên “TS. Quản Trị Viên”, role “ADMIN / QUẢN TRỊ VIÊN”, avatar icon. | Hard-coded/static; không có profile endpoint hoặc user ID mapping. | — |
| 6 | Global breadcrumb — breadcrumb trail | “Hệ thống > Quản trị trung tâm > Không gian làm việc”. Các node là span; một số chỉ có hover class. | Static; không anchor/handler thực. | — |
| 7 | RBAC compliance badge — status/claim | Shield + “Chuẩn xác thực RBAC” ở breadcrumb bar. | Static claim; không có policy/audit evidence từ dashboard. | — |
| 8 | Dashboard breadcrumb — breadcrumb/context | “Bảng điều khiển quản trị > Tổng quan hệ thống”. | Static spans; không có click handler hoặc route state. | — |
| 9 | Operations readiness pill — status badge | Chấm xanh + “CỔNG VẬN HÀNH SẴN SÀNG”. | Static claim; không gắn với readiness API hay runtime probe. | — |
| 10 | Dashboard hero — section label/title/description | “HỆ THỐNG QUẢN TRỊ TỔNG THỂ”, tiêu đề và phần mô tả giám sát users/courses/moderation. | Static HTML, visible. Copy không định nghĩa KPI hoặc API field. | — |
| 11 | Date range control — segmented buttons | “Hôm nay” selected về hình thức; “7 ngày qua”, “30 ngày qua” còn lại. Ba button đều có `disabled`; không có `from`/`to` value. | Current `DISABLED`. Date format là API `date`; default, inclusivity, timezone và range validation chưa chốt. | EV-02 |
| 12 | Làm mới số liệu — button | Nút refresh kèm icon, `id="refresh-btn"`. | Enabled trong HTML; chỉ local animation/timer 700 ms. Không loading/API state. | EV-03 |
| 13 | System users KPI — metric card | “Người dùng hệ thống”, value `--`, “Tổng tài khoản người dùng”, trạng thái “Đang đồng bộ sổ danh tính”. | Static; không có count, population, status hay profile mapping từ #101. `--` không phải 0. | EV-01 (mapping blocked) |
| 14 | Learning programs KPI — metric card | “Chương trình học”, value `--`, “Khóa học đang hoạt động”, “Chờ máy chủ tổng hợp”. | Static; API #101 proposal `course_records_created` không tương đương khóa đang hoạt động; không map. | EV-01 (mapping blocked) |
| 15 | Quality review KPI — metric card | “Kiểm định chất lượng”, value `--`, yêu cầu kiểm duyệt chờ duyệt và “Kiểm tra hàng đợi”. | Static; không có metric key/endpoint mapping được xác nhận. | EV-01 (mapping blocked) |
| 16 | Online infrastructure KPI — metric card | “Hạ tầng trực tuyến”, value `--`, tỷ lệ tải hệ thống và “Định lượng dịch vụ”. | Static; `Report.metrics[]` không định nghĩa health/load metrics; không có mapping được xác nhận. | EV-01 (mapping blocked) |
| 17 | Recent system activity — panel heading | Icon history và “Hoạt động hệ thống gần đây”. | Static heading; không có query, list endpoint hoặc event history trong #101. | — |
| 18 | Security log badge — label/status | “Ghi vết bảo mật” trong activity panel. | Static; không chứng minh audit logging/list API. | — |
| 19 | Activity empty state — icon/title/description | Icon document, “Chưa có nhật ký hoạt động được ghi nhận” và copy mô tả nhật ký quản trị. | Static placeholder; không phân biệt chưa có event, chưa kích hoạt hay endpoint unavailable. | — |
| 20 | ISO/IEC 27001 claim — compliance label | Lock icon + “Phiên đăng nhập tuân thủ chuẩn ISO/IEC 27001”. | Static claim; không có audit, policy evaluation hoặc evidence source. | — |
| 21 | 24-hour status copy — summary text | “Không có thay đổi trạng thái trong 24 giờ qua”. | Static claim; không có timestamp/query/evidence. | — |
| 22 | View audit log — disabled button | “Xem toàn bộ nhật ký kiểm toán”, lock icon. | `disabled`; không có click event, destination hoặc audit-list API. | EV-07 (currently unavailable) |
| 23 | Server operations panel heading — panel header | Server icon, “Thông báo vận hành máy chủ”, overall green dot. | Static; không gắn service health API/state. | — |
| 24 | Database status row — service status item | Cơ sở dữ liệu, “Cluster lưu trữ phân tán”, status “Hoạt động”. | Static; `/health/ready` chỉ báo dependency được cấu hình, không probe DB; không dùng để xác nhận trạng thái này. | — |
| 25 | Authentication status row — service status item | Dịch vụ xác thực, “SSO & Quản lý phân quyền”, status “Trực tuyến”. | Static; chưa có auth-service health/SSO status source trong dashboard. | — |
| 26 | Background task queue row — service status item | Hàng đợi tác vụ, “Điều phối tiến trình nền”, status “Sẵn sàng”. | Static; không có queue status source/API được gắn vào màn hình. | — |
| 27 | Admin permissions notice — information panel | “Quyền hạn quản trị viên” và copy nói số liệu bị khóa tới khi hoàn tất phân quyền. | Static text; policy/condition/transition chưa có client hoặc #101 contract. | — |
| 28 | Direct management shortcuts heading — section header | “Lối tắt quản lý trực tiếp”, caption “Chuyển hướng không gian quản trị”. | Static; không có event riêng. | — |
| 29 | Manage users shortcut — link/card | “Quản lý người dùng”; mô tả hồ sơ/phân quyền/trạng thái; HTML `href="/admin/users"`. | Native link; candidate AD-02 route theo inventory. Router runtime chưa có. | EV-06 |
| 30 | Manage courses shortcut — link/card | “Quản lý khóa học”; mô tả chương trình/bài giảng/chứng chỉ; `href="/admin/courses"`. | Native link; candidate AD-06 route theo inventory. Router runtime chưa có. | EV-06 |
| 31 | Moderation queue shortcut — link/card | “Hàng đợi kiểm duyệt”; mô tả duyệt bài nộp/đề cương/học liệu; `href="/admin/content/pending"`. | Native link; candidate AD-10 route theo inventory. Router runtime chưa có. | EV-06 |
| 32 | Footer copyright/system label — footer text | “© 2025 Study2Work LMS.” và “Hệ thống quản trị trung tâm.” | Static copy. | — |
| 33 | Privacy policy — footer link | “Quy chế bảo mật dữ liệu”; `href="#"`. | Placeholder anchor, destination chưa xác định. | EV-08 |
| 34 | RBAC standards — footer link | “Tiêu chuẩn phân quyền RBAC”; `href="#"`. | Placeholder anchor, destination chưa xác định. | EV-08 |
| 35 | Technical support — footer link | “Hỗ trợ kỹ thuật hệ thống”; `href="#"`. | Placeholder anchor, destination chưa xác định. | EV-08 |

## 4. Conditional UI & state variations
- States theo inventory: loading/partial/no-data/error
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/05_admin/AD-01_dashboard-quan-tri/AD-01.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
