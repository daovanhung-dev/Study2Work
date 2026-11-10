# AD-06 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [AD-06_markers.json](../../screen_stitch/05_admin/AD-06_danh-sach-khoa-hoc-quan-tri/AD-06_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `AD-06-EL-001` | `not supplied in marker JSON` | Study2Work LMS Admin Portal brand |
| #2 | `AD-06-EL-002` | `not supplied in marker JSON` | Primary Admin navigation group |
| #3 | `AD-06-EL-003` | `not supplied in marker JSON` | SYSTEM NORMAL badge |
| #4 | `AD-06-EL-004` | `not supplied in marker JSON` | Notifications button |
| #5 | `AD-06-EL-005` | `not supplied in marker JSON` | Admin identity and avatar |
| #6 | `AD-06-EL-006` | `not supplied in marker JSON` | Global breadcrumb trail |
| #7 | `AD-06-EL-007` | `not supplied in marker JSON` | RBAC assurance badge |
| #8 | `AD-06-EL-008` | `not supplied in marker JSON` | Local course-management breadcrumb |
| #9 | `AD-06-EL-009` | `not supplied in marker JSON` | API #73 reference badge |
| #10 | `AD-06-EL-010` | `not supplied in marker JSON` | Page title |
| #11 | `AD-06-EL-011` | `not supplied in marker JSON` | Catalog V2 badge |
| #12 | `AD-06-EL-012` | `not supplied in marker JSON` | Page subtitle |
| #13 | `AD-06-EL-013` | `not supplied in marker JSON` | Export report button |
| #14 | `AD-06-EL-014` | `not supplied in marker JSON` | Add new course button |
| #15 | `AD-06-EL-015` | `not supplied in marker JSON` | Total courses KPI card |
| #16 | `AD-06-EL-016` | `not supplied in marker JSON` | Pending review KPI card |
| #17 | `AD-06-EL-017` | `not supplied in marker JSON` | Published courses KPI card |
| #18 | `AD-06-EL-018` | `not supplied in marker JSON` | Participating mentors KPI card |
| #19 | `AD-06-EL-019` | `not supplied in marker JSON` | Course search input |
| #20 | `AD-06-EL-020` | `not supplied in marker JSON` | Status filter select |
| #21 | `AD-06-EL-021` | `not supplied in marker JSON` | Mentor filter select |
| #22 | `AD-06-EL-022` | `not supplied in marker JSON` | Locked category filter badge |
| #23 | `AD-06-EL-023` | `not supplied in marker JSON` | Applied-filter summary |
| #24 | `AD-06-EL-024` | `not supplied in marker JSON` | Reset filters control |
| #25 | `AD-06-EL-025` | `not supplied in marker JSON` | Course table header group: code, name, mentor, fee, status, lessons, actions |
| #26 | `AD-06-EL-026` | `not supplied in marker JSON` | Empty-state illustration |
| #27 | `AD-06-EL-027` | `not supplied in marker JSON` | Empty-state heading |
| #28 | `AD-06-EL-028` | `not supplied in marker JSON` | Empty-state explanatory copy |
| #29 | `AD-06-EL-029` | `not supplied in marker JSON` | Disabled refresh-list button |
| #30 | `AD-06-EL-030` | `not supplied in marker JSON` | View sync manual button |
| #31 | `AD-06-EL-031` | `not supplied in marker JSON` | Static API endpoint source claim |
| #32 | `AD-06-EL-032` | `not supplied in marker JSON` | Displayed result count |
| #33 | `AD-06-EL-033` | `not supplied in marker JSON` | Disabled previous-page button |
| #34 | `AD-06-EL-034` | `not supplied in marker JSON` | Page indicator |
| #35 | `AD-06-EL-035` | `not supplied in marker JSON` | Disabled next-page button |
| #36 | `AD-06-EL-036` | `not supplied in marker JSON` | Governance banner shield icon |
| #37 | `AD-06-EL-037` | `not supplied in marker JSON` | Governance banner heading |
| #38 | `AD-06-EL-038` | `not supplied in marker JSON` | Governance and moderation rule copy |
| #39 | `AD-06-EL-039` | `not supplied in marker JSON` | Assessment standards call-to-action |
| #40 | `AD-06-EL-040` | `not supplied in marker JSON` | Copyright notice |
| #41 | `AD-06-EL-041` | `not supplied in marker JSON` | Admin system footer caption |
| #42 | `AD-06-EL-042` | `not supplied in marker JSON` | Data privacy footer link |
| #43 | `AD-06-EL-043` | `not supplied in marker JSON` | RBAC standards footer link |
| #44 | `AD-06-EL-044` | `not supplied in marker JSON` | Technical support footer link |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả chi tiết từng element

ID phải khớp [annotated screenshot](../../screen_stitch/05_admin/AD-06_danh-sach-khoa-hoc-quan-tri/screen_annotated.png) và [marker map](../../screen_stitch/05_admin/AD-06_danh-sach-khoa-hoc-quan-tri/AD-06_markers.json). Các nhóm có nhiều nhãn hiển thị được liệt kê thành phần riêng bên dưới; element “static” không chứng minh API hay runtime.

| ID | Tên / loại / vị trí / mục đích | Thuộc tính, nguồn dữ liệu, validation | Hiển thị / trạng thái / event |
|---:|---|---|---|
| #1 | Study2Work/LMS/Admin Portal brand; header trái. | Logo và text tĩnh; không lấy từ #73. | Visible; click destination chưa có route/handler; EV-08. |
| #2 | Primary Admin navigation group; header giữa (Tổng quan, Người dùng, Khóa học & Nội dung, Kiểm duyệt, Báo cáo). | Năm anchors, HTML `href="#"`; route access từng destination chưa được Study Web source xác nhận. | Visible; active item trong mockup là Khóa học & Nội dung; navigation chưa wired; EV-08. |
| #3 | “SYSTEM NORMAL” badge; header. | Text/green indicator hard-coded; không có health data/endpoint trong AD-06. | Visible nhưng unverified; không dùng để cho phép request; EV-08. |
| #4 | Notifications button/icon; header phải. | Bell + dot tĩnh; không có unread count source hoặc click handler. | Visible; action chưa xác định; EV-08. |
| #5 | Admin identity/avatar block; header phải. | Name/role/avatar tĩnh; #73 trả mentor owner của course, không phải Admin identity. | Visible; identity source/route ngoài contract này; EV-08. |
| #6 | Global breadcrumb trail; hàng dưới header. | Home / Hệ thống / Quản trị trung tâm / Không gian làm việc; markup anchor không có route state. | Visible; destinations chưa wired; EV-08. |
| #7 | “Chuẩn xác thực RBAC” badge; phải breadcrumb. | Static claim; API #73 không trả permission result. | Visible nhưng unverified; không xem là authorization decision; EV-08. |
| #8 | Local breadcrumb “Quản trị đào tạo › Danh sách khóa học”. | Static labels, không có route binding trong HTML. | Visible; route/return behavior chưa wired; EV-08. |
| #9 | API #73 reference badge; cạnh breadcrumb. | Label tĩnh; không chứng minh page gọi #73. | Visible; no action; EV-08. |
| #10 | Page title “Quản lý danh mục khóa học”. | Static heading; API #73 không trả page title. | Visible; presentation only. |
| #11 | “CATALOG V2” badge; cạnh title. | Static version label; không có catalog version negotiation. | Visible, unverified; EV-08. |
| #12 | Subtitle về giám sát, phân quyền mentor và trạng thái xuất bản. | Editorial text; API #73 chỉ cấp course/mentor projection, không trả aggregate/scope permission. | Visible; phải được duyệt nội dung trước implementation; EV-08. |
| #13 | Export report button; hero bên phải. | Button tĩnh, không handler; API #103 là export impact report riêng, không phải course catalog export. | Enabled-looking nhưng unsupported; không gọi #103; EV-08. |
| #14 | Add new course button; hero bên phải. | Button tĩnh, không handler; inventory/API #73–#77 không có Admin course-create endpoint. | Enabled-looking nhưng unsupported; không tạo client-only course; EV-08. |
| #15 | KPI “Tổng khóa học”. | Giá trị 0 hard-coded; #73 `pagination.total` phụ thuộc filter, không định nghĩa aggregate không lọc. | Visible; dữ liệu chưa source-backed; EV-07. |
| #16 | KPI “Chờ kiểm duyệt”. | Giá trị 0 hard-coded; #73 không có review count/aggregate. AC-33 content review không xác lập course KPI. | Visible; moderation relation/definition chưa có; EV-07. |
| #17 | KPI “Đã xuất bản”. | Giá trị 0 hard-coded; #73 có `status` mỗi course nhưng không có aggregate/status enum được duyệt. | Visible; không thể tính chính xác từ page 20 rows; EV-07. |
| #18 | KPI “Giảng viên tham gia”. | Giá trị 0 hard-coded; #73 không trả distinct mentor count; page projection không bảo đảm danh sách mentor đầy đủ. | Visible; no supported source; EV-07. |
| #19 | Search input; đầu hàng bộ lọc. | Text, placeholder tên/mã/giảng viên. Không có max length/normalization/search query contract; DOM input không có listener. | Visible/editable markup, nhưng hiện không đổi kết quả; EV-02. |
| #20 | Status filter select. | Mockup options: `all`, `draft`, `pending`, `published`, `archived` (lowercase). API nhận raw string exact-match; không enum/normalization/allowlist. | Visible; current HTML default `all`; server filter mapping blocked until vocabulary/case approval; EV-03. |
| #21 | Mentor filter select. | Mockup chỉ có option `all`; API expects signed int64. Không có mentor option-list API trong AD-06 contract. | Visible; current default `all`; không gửi literal all; option choices blocked; EV-03. |
| #22 | Category filter locked badge. | Static lock/copy “đang chờ cấu hình liên kết dữ liệu”. Valid category int64 hiện trả 422; legacy DDL không có FK `courses.category_id`. | Visible/disabled conceptually; giữ disabled; EV-03. |
| #23 | Applied-filter summary. | Hard-coded “Tất cả danh mục gốc (API 73)” và “Không có bộ lọc tùy chỉnh nào hoạt động”; không bind state/API. | Visible; summary trong prototype không phản ánh request; EV-07. |
| #24 | “Khôi phục mặc định” reset control. | Anchor/button presentation; listener xóa text, đặt status/mentor thành `all`; không sửa category/URL hoặc gọi API. | Visible/enabled; local reset only; EV-04. |
| #25 | Course table header group; header row có 7 column. | Các cột riêng: **Mã khóa** (không có response field); **Tên khóa học** ← `title`; **Giảng viên hướng dẫn** ← `mentor.full_name`; **Học phí** ← exact decimal-string `price`; **Trạng thái** ← raw `status`; **Số bài học** (không có field/API); **Thao tác** (row action/route chưa implement; direct status action is not confirmed by AC-32). | Visible; empty-state row hiện span 7 cột; data/error/loading rows chưa có; EV-01/EV-06. |
| #26 | Empty-state illustration (folder/search-off). | Decorative icon/animation từ HTML; không phải server sync indicator. | Visible trong prototype empty state; no event; EV-07. |
| #27 | Empty-state heading “Chưa có dữ liệu khóa học quản trị”. | Static copy. #73 message “No courses found.” có thể ứng với items rỗng nhưng không phân loại nguyên nhân/filters. | Visible; target empty-vs-filtered/out-of-range copy cần định nghĩa; EV-07. |
| #28 | Empty-state body về không có kết quả hoặc đang đồng bộ. | Static text gộp empty/filter/sync; #73 không trả sync state. | Visible; claim đồng bộ không được hiển thị như fact; EV-07. |
| #29 | “Làm mới danh sách khóa học” button. | `disabled`; không handler. Future refresh có thể lặp GET #73, nhưng trigger/loading/disable/retry policy chưa duyệt. | Disabled; no refresh event currently; EV-08. |
| #30 | “Xem sổ tay đồng bộ” button. | Enabled-looking button, no `href`/handler/destination. | Visible; unsupported navigation; EV-08. |
| #31 | Static API source claim `/admin/v1/courses/catalog`. | Text sai path; API catalog/current route là `/api/v1/admin/courses`. Không dynamic. | Visible but inaccurate; không dùng làm endpoint/config evidence; EV-08. |
| #32 | Result count “Hiển thị 0 trên 0 khóa học”. | Hai giá trị 0 hard-coded. Candidate mapping có thể dùng `items.length` và `pagination.total`; wording/page range chưa được xác nhận. | Visible; không phản ánh request hiện tại; EV-07. |
| #33 | Previous-page button. | Disabled; no listener. #73 page is optional int32, default 1; size fixed 20; client page navigation not wired. | Disabled; EV-05. |
| #34 | Page indicator `0 / 0`. | Static; response has `pagination.page`, `size`, `total`, `total_pages`. Zero page on empty screen is not server metadata (server returns page 1 by default, total_pages 0). | Visible, currently inconsistent; EV-05/EV-07. |
| #35 | Next-page button. | Disabled; no listener. Future next-page bounds could use pagination metadata, but page calculation/state is not implemented. | Disabled; EV-05. |
| #36 | Governance banner shield icon. | Decorative icon; no moderation/permission source. | Visible; no event; EV-08. |
| #37 | Governance heading “Quy chế quản trị & Kiểm định chất lượng”. | Static editorial copy; no policy document/API link evidence. | Visible; policy destination/content needs owner approval; EV-08. |
| #38 | Governance rule text claiming every new course needs moderation before public publish. | No such rule in #73. AC-32 only references action “according to policy”; AC-33 is separate content-review workflow. | Visible but unverified; do not treat as enforced workflow; EV-08. |
| #39 | “Tiêu chuẩn thẩm định” call-to-action. | Anchor `href="#"`; no verified destination. | Enabled-looking, no route; EV-08. |
| #40 | Copyright notice. | Static “© 2025 Study2Work LMS.” | Visible; no event/data source. |
| #41 | Admin-system footer caption. | Static “Hệ thống quản trị trung tâm.” | Visible; no event/data source. |
| #42 | Data privacy footer link. | Anchor placeholder `href="#"`; no destination in Study Web source. | Visible; navigation not wired; EV-08. |
| #43 | RBAC standards footer link. | Anchor placeholder; does not verify RBAC policy. | Visible; navigation not wired; EV-08. |
| #44 | System technical support footer link. | Anchor placeholder; no support page/service source. | Visible; navigation not wired; EV-08. |

## 4. Conditional UI & state variations
- States theo inventory: initial/loading/ready/empty/out-of-range-empty/unauthorized/forbidden/validation-error/service-error
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/05_admin/AD-06_danh-sach-khoa-hoc-quan-tri/AD-06.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
