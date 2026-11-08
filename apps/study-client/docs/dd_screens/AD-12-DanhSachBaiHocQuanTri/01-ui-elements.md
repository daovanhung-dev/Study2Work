# AD-12 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [AD-12_markers.json](../../screen_stitch/05_admin/AD-12_danh-sach-bai-hoc-quan-tri/AD-12_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `AD-12-EL-001` | `not supplied in marker JSON` | Study2Work Admin brand |
| #2 | `AD-12-EL-002` | `not supplied in marker JSON` | Admin navigation: Tổng quan |
| #3 | `AD-12-EL-003` | `not supplied in marker JSON` | Admin navigation: Người dùng |
| #4 | `AD-12-EL-004` | `not supplied in marker JSON` | Active Admin navigation: Khóa học và Nội dung |
| #5 | `AD-12-EL-005` | `not supplied in marker JSON` | Admin navigation: Kiểm duyệt |
| #6 | `AD-12-EL-006` | `not supplied in marker JSON` | Admin navigation: Báo cáo |
| #7 | `AD-12-EL-007` | `not supplied in marker JSON` | Static SYSTEM NORMAL badge |
| #8 | `AD-12-EL-008` | `not supplied in marker JSON` | Notification bell without handler |
| #9 | `AD-12-EL-009` | `not supplied in marker JSON` | Static Admin identity and avatar |
| #10 | `AD-12-EL-010` | `not supplied in marker JSON` | Global breadcrumb trail |
| #11 | `AD-12-EL-011` | `not supplied in marker JSON` | Static RBAC assurance copy |
| #12 | `AD-12-EL-012` | `not supplied in marker JSON` | Breadcrumb: Quản trị đào tạo |
| #13 | `AD-12-EL-013` | `not supplied in marker JSON` | Current breadcrumb: Quản lý bài học |
| #14 | `AD-12-EL-014` | `not supplied in marker JSON` | Page title: Danh sách bài học hệ thống |
| #15 | `AD-12-EL-015` | `not supplied in marker JSON` | Page subtitle |
| #16 | `AD-12-EL-016` | `not supplied in marker JSON` | Static API #82 Endpoint Active badge |
| #17 | `AD-12-EL-017` | `not supplied in marker JSON` | Add new lesson CTA without catalog create API |
| #18 | `AD-12-EL-018` | `not supplied in marker JSON` | Lesson query filter section heading |
| #19 | `AD-12-EL-019` | `not supplied in marker JSON` | Static claim: Đồng bộ trực tiếp từ CSDL LMS |
| #20 | `AD-12-EL-020` | `not supplied in marker JSON` | Lesson name or lecture-code search input |
| #21 | `AD-12-EL-021` | `not supplied in marker JSON` | Course select with slug options |
| #22 | `AD-12-EL-022` | `not supplied in marker JSON` | Lesson type select |
| #23 | `AD-12-EL-023` | `not supplied in marker JSON` | Lesson status select |
| #24 | `AD-12-EL-024` | `not supplied in marker JSON` | Filter refresh button |
| #25 | `AD-12-EL-025` | `not supplied in marker JSON` | Table header group: seven displayed columns |
| #26 | `AD-12-EL-026` | `not supplied in marker JSON` | Empty-state decorative icon |
| #27 | `AD-12-EL-027` | `not supplied in marker JSON` | Empty-state heading |
| #28 | `AD-12-EL-028` | `not supplied in marker JSON` | Empty-state explanatory copy |
| #29 | `AD-12-EL-029` | `not supplied in marker JSON` | Disabled empty-state refresh-list button |
| #30 | `AD-12-EL-030` | `not supplied in marker JSON` | Reset search filters button |
| #31 | `AD-12-EL-031` | `not supplied in marker JSON` | Visible-row summary |
| #32 | `AD-12-EL-032` | `not supplied in marker JSON` | Previous page button |
| #33 | `AD-12-EL-033` | `not supplied in marker JSON` | Static pagination counter 0/0 |
| #34 | `AD-12-EL-034` | `not supplied in marker JSON` | Next page button |
| #35 | `AD-12-EL-035` | `not supplied in marker JSON` | Compliance notice icon |
| #36 | `AD-12-EL-036` | `not supplied in marker JSON` | Compliance and copyright section heading |
| #37 | `AD-12-EL-037` | `not supplied in marker JSON` | Static SCORM/xAPI/DRM compliance claim |
| #38 | `AD-12-EL-038` | `not supplied in marker JSON` | Static API 82 and SCORM 2004 badge |
| #39 | `AD-12-EL-039` | `not supplied in marker JSON` | Footer copyright and system description |
| #40 | `AD-12-EL-040` | `not supplied in marker JSON` | Privacy policy footer link |
| #41 | `AD-12-EL-041` | `not supplied in marker JSON` | RBAC standard footer link |
| #42 | `AD-12-EL-042` | `not supplied in marker JSON` | Technical support footer link |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả chi tiết từng element

Tọa độ là pixel trên `screen.png` gốc 1600×1301; vị trí marker là tâm vòng tròn trên ảnh chú thích 2×. “Static” nghĩa là HTML mẫu, không phải dữ liệu/runtime. Mỗi số khớp duy nhất với `AD-12_markers.json`.

| # | Tên / loại / vị trí (x,y) | Thuộc tính, nguồn và trạng thái | Sự kiện |
|---:|---|---|---|
| 1 | Brand Study2Work Admin / logo `(16,62)` | Wordmark viết tĩnh trong HTML; không chứng minh tenant/role. | EV-09 |
| 2 | Nav “Tổng quan” / link `(355,62)` | `href="#"`; không có destination runtime. | EV-09 |
| 3 | Nav “Người dùng” / link `(480,62)` | `href="#"`; không route handler. | EV-09 |
| 4 | Nav “Khóa học & Nội dung” / active nav `(680,62)` | Active style tĩnh; không xác định route current. | EV-09 |
| 5 | Nav “Kiểm duyệt” / link `(845,62)` | `href="#"`; không điều hướng. | EV-09 |
| 6 | Nav “Báo cáo” / link `(965,62)` | `href="#"`; không route handler. | EV-09 |
| 7 | `SYSTEM NORMAL` / badge `(1158,62)` | Static status; không health check/monitoring source. | EV-09 |
| 8 | Chuông thông báo / button `(1280,62)` | Không handler/unread data source trong prototype. | EV-09 |
| 9 | Admin identity/avatar `(1546,62)` | Tên, role và avatar tĩnh; không bind session/profile. | EV-09 |
| 10 | Breadcrumb hệ thống / navigation `(18,107)` | “Hệ thống > Quản trị trung tâm > Không gian làm việc”; static shell. | EV-09 |
| 11 | “Chuẩn xác thực RBAC” / assurance copy `(1579,107)` | Static text; không phải kết quả authorization. | EV-09 |
| 12 | Breadcrumb “Quản trị đào tạo” `(18,178)` | Static crumb; destination không có route source. | EV-09 |
| 13 | Crumb “Quản lý bài học” `(300,178)` | Current section label; không có breadcrumb state source. | EV-09 |
| 14 | H1 “Danh sách bài học hệ thống” `(520,221)` | Static title; page scope từ inventory. | EV-09 |
| 15 | Subtitle mô tả danh mục/video/tài liệu `(650,273)` | Static; không cam kết API trả mọi loại nội dung nêu trong copy. | EV-09 |
| 16 | Badge “API #82 Endpoint Active” `(1338,270)` | Static badge; không probe endpoint/runtime. | EV-09 |
| 17 | “Thêm bài học mới” / CTA `(1585,270)` | Button tĩnh; create API/destination chưa có trong AC-34/#82–#86. Disabled/hidden behavior cần quyết định. | EV-08 |
| 18 | “Bộ lọc truy vấn bài giảng” / section heading `(35,338)` | Heading tĩnh cho vùng filter; không có filter state. | EV-02–EV-06 |
| 19 | “Đồng bộ trực tiếp từ CSDL LMS” / claim `(1575,338)` | Static copy; #82 không cung cấp sync status. | EV-09 |
| 20 | Search input `(523,367)` | Placeholder tìm tên bài học/mã bài giảng; không query `q`, search field hoặc lesson code trong #82/response. | EV-02 |
| 21 | Course select `(910,418)` | Prototype options dùng course slug; API cần `course:int64`; option source/mapping chưa được duyệt. | EV-03 |
| 22 | Lesson type select `(1157,418)` | Prototype options `video/reading/assignment/quiz`; current #82 từ chối mọi `type` supplied với 422. | EV-04 |
| 23 | Status select `(1408,418)` | Prototype labels `active/draft/hidden`; API nhận exact string, không có enum/alias mapping được xác nhận. | EV-05 |
| 24 | “Làm mới” filter button `(1539,418)` | HTML button không có handler; target refresh cần dùng query đã được xác nhận. | EV-06 |
| 25 | Table header group `(1570,492)` | Bảy cột: mã bài học, tiêu đề, khóa học, định dạng, thứ tự, trạng thái, thao tác. #82 map có `id/title/course_id/order/status`, thiếu lesson code, course title, format và page metadata. | EV-01, EV-07 |
| 26 | Empty-state decorative icon `(733,619)` | Static icon; không biểu diễn lỗi hay trạng thái sync. | EV-01 |
| 27 | Empty heading “Chưa có dữ liệu bài học” `(664,751)` | Static; server `data: []` chỉ nghĩa không có row phù hợp. | EV-01 |
| 28 | Empty explanatory copy `(460,798)` | Nêu filter/no data/đang chờ đồng bộ; phần “đang chờ đồng bộ” không được #82 chứng minh. | EV-01 |
| 29 | “Làm mới danh sách bài học” / disabled button `(500,888)` | HTML `disabled`; không event hiện tại. | EV-06 |
| 30 | “Đặt lại bộ lọc tìm kiếm” / button `(1102,888)` | Không handler; reset semantics/filter defaults chưa được implement. | EV-06 |
| 31 | Summary “Hiển thị 0 trên 0 bài học” `(39,1055)` | Static `0/0`; #82 không trả total/count riêng, không thể tính tổng trang. | EV-01 |
| 32 | Previous page / disabled button `(1360,1055)` | Static disabled pagination control; #82 không có page/offset. | EV-01 |
| 33 | Page counter `0/0` `(1457,1092)` | Static; không ánh xạ tới response. | EV-01 |
| 34 | Next page / disabled button `(1554,1055)` | Static disabled pagination control; API không phân trang. | EV-01 |
| 35 | Compliance notice icon `(38,1195)` | Decorative shield; không phải compliance verification. | EV-09 |
| 36 | “Tiêu chuẩn tuân thủ & Bản quyền nội dung” / heading `(95,1137)` | Static informational heading; không có compliance endpoint/policy evidence. | EV-09 |
| 37 | SCORM/xAPI/DRM claim `(1337,1193)` | Static claim về HLS/SCORM/xAPI/DRM; không có feature evidence trong #82. | EV-09 |
| 38 | Badge “API 82 • SCORM 2004” `(1564,1192)` | Static badge; API #82 không mang metadata SCORM. | EV-09 |
| 39 | Copyright/system footer `(17,1289)` | Copyright 2025 và mô tả hệ thống viết cứng. | EV-09 |
| 40 | Privacy policy / footer link `(887,1288)` | `href="#"`; destination/chính sách không được xác minh từ prototype. | EV-09 |
| 41 | RBAC standard / footer link `(1114,1288)` | `href="#"`; không liên kết policy có thể kiểm tra. | EV-09 |
| 42 | Technical support / footer link `(1378,1288)` | `href="#"`; không destination/runtime handler. | EV-09 |

### Data mapping khi owner chốt contract

| Local #82 field | Type/current nullability | Mapping UI có thể xác minh | Giới hạn |
|---|---|---|---|
| `id` | integer | lesson ID; candidate path ID cho AD-13/#83 | Không chứng minh lesson code. |
| `course_id` | integer theo response model | numeric course ID | Không phải slug/course title; DDL legacy column nullable. |
| `title` | string, từ `lessons.name` | title | Không có keyword search. |
| `content` | nullable string | Không có column trong mockup list rõ ràng | Không suy ra body preview. |
| `video_url` | nullable string | Không có format/streaming claim được hỗ trợ | Không suy ra HLS/DRM/SCORM. |
| `order` | integer từ `sort_order` | thứ tự | DDL legacy `sort_order` nullable. |
| `status` | string | raw status nếu owner duyệt mapping | Không có enum/alias; DDL legacy nullable. |

## 4. Conditional UI & state variations
- States theo inventory: loading/empty/ready/error
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/05_admin/AD-12_danh-sach-bai-hoc-quan-tri/AD-12.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
