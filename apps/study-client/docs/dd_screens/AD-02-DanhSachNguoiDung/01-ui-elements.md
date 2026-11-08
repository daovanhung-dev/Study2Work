# AD-02 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [AD-02_markers.json](../../screen_stitch/05_admin/AD-02_danh-sach-nguoi-dung/AD-02_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `AD-02-EL-001` | `not supplied in marker JSON` | Study2Work LMS Admin brand |
| #2 | `AD-02-EL-002` | `not supplied in marker JSON` | Primary navigation group: overview, users, courses/content, moderation, reports |
| #3 | `AD-02-EL-003` | `not supplied in marker JSON` | System Normal status pill |
| #4 | `AD-02-EL-004` | `not supplied in marker JSON` | Notifications button |
| #5 | `AD-02-EL-005` | `not supplied in marker JSON` | Admin identity and avatar block |
| #6 | `AD-02-EL-006` | `not supplied in marker JSON` | Global breadcrumb trail |
| #7 | `AD-02-EL-007` | `not supplied in marker JSON` | RBAC verification badge |
| #8 | `AD-02-EL-008` | `not supplied in marker JSON` | Admin users page breadcrumb |
| #9 | `AD-02-EL-009` | `not supplied in marker JSON` | API #68 badge |
| #10 | `AD-02-EL-010` | `not supplied in marker JSON` | Authentication system label |
| #11 | `AD-02-EL-011` | `not supplied in marker JSON` | Security level label |
| #12 | `AD-02-EL-012` | `not supplied in marker JSON` | Page title |
| #13 | `AD-02-EL-013` | `not supplied in marker JSON` | Page description |
| #14 | `AD-02-EL-014` | `not supplied in marker JSON` | Export report button |
| #15 | `AD-02-EL-015` | `not supplied in marker JSON` | Add user button |
| #16 | `AD-02-EL-016` | `not supplied in marker JSON` | Keyword search input |
| #17 | `AD-02-EL-017` | `not supplied in marker JSON` | Role filter select |
| #18 | `AD-02-EL-018` | `not supplied in marker JSON` | Status filter select |
| #19 | `AD-02-EL-019` | `not supplied in marker JSON` | Reset filters button |
| #20 | `AD-02-EL-020` | `not supplied in marker JSON` | Active filter summary |
| #21 | `AD-02-EL-021` | `not supplied in marker JSON` | Server synchronization status |
| #22 | `AD-02-EL-022` | `not supplied in marker JSON` | User table column header row |
| #23 | `AD-02-EL-023` | `not supplied in marker JSON` | Empty-state illustration |
| #24 | `AD-02-EL-024` | `not supplied in marker JSON` | Empty-state title |
| #25 | `AD-02-EL-025` | `not supplied in marker JSON` | Empty-state explanation |
| #26 | `AD-02-EL-026` | `not supplied in marker JSON` | Refresh list button |
| #27 | `AD-02-EL-027` | `not supplied in marker JSON` | Input guide button |
| #28 | `AD-02-EL-028` | `not supplied in marker JSON` | Visible account count |
| #29 | `AD-02-EL-029` | `not supplied in marker JSON` | Previous page button |
| #30 | `AD-02-EL-030` | `not supplied in marker JSON` | Current page and total pages |
| #31 | `AD-02-EL-031` | `not supplied in marker JSON` | Next page button |
| #32 | `AD-02-EL-032` | `not supplied in marker JSON` | Security notice icon |
| #33 | `AD-02-EL-033` | `not supplied in marker JSON` | Security notice heading |
| #34 | `AD-02-EL-034` | `not supplied in marker JSON` | Security notice body copy |
| #35 | `AD-02-EL-035` | `not supplied in marker JSON` | Footer copyright and workspace label |
| #36 | `AD-02-EL-036` | `not supplied in marker JSON` | Privacy policy footer link |
| #37 | `AD-02-EL-037` | `not supplied in marker JSON` | RBAC standards footer link |
| #38 | `AD-02-EL-038` | `not supplied in marker JSON` | Technical support footer link |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả element

Mỗi dòng khớp một marker cùng số trong [AD-02_markers.json](../../screen_stitch/05_admin/AD-02_danh-sach-nguoi-dung/AD-02_markers.json) và [AD-02_markers.svg](../../screen_stitch/05_admin/AD-02_danh-sach-nguoi-dung/AD-02_markers.svg). Tọa độ tính trên ảnh gốc 1600×1425.

| # | Element | Expected mapping / rule | Prototype hiện tại |
|---:|---|---|---|
| 1 | Study2Work LMS Admin brand | Brand/header; route home chỉ dùng khi được inventory xác nhận. | Static logo/brand. |
| 2 | Primary navigation group | Overview, Users, Courses/Content, Moderation, Reports; mỗi link trỏ đúng Screen ID/route đã duyệt. | Năm anchor `href="#"`; Users chỉ có `aria-current`. |
| 3 | System Normal pill | Chỉ hiển thị health khi có source/API health contract. | Static status; #68 không kiểm tra health. |
| 4 | Notifications button | Mở notification destination khi có route/API. | Không listener. |
| 5 | Admin identity/avatar | Lấy từ approved Admin session/profile source. | Static “TS. Quản Trị Viên”; #68 không trả caller identity. |
| 6 | Global breadcrumb trail | Dùng route hierarchy đã duyệt; mỗi crumb là link khi có đích. | Static labels; không route. |
| 7 | RBAC verification badge | Không tuyên bố compliance/version nếu không có nguồn được duyệt. | Static “Chuẩn xác thực RBAC”. |
| 8 | User-list breadcrumb | “Quản trị người dùng → Danh sách tài khoản”; current item là AD-02. | Static text. |
| 9 | API #68 badge | Nội bộ/design hint; không phải trạng thái runtime hay version contract. | Static “API #68 • RBAC V2.4”. |
| 10 | Authentication system label | Chỉ dùng như section label; không thay auth guard. | Static “Hệ thống xác thực”. |
| 11 | Security level label | Cần nguồn chính sách/định nghĩa security tier trước khi trình bày như assurance. | Static “Bảo Mật Cấp 3”. |
| 12 | Page title | “Quản lý tài khoản người dùng”. | Static title. |
| 13 | Page description | Mô tả tra cứu/quản trị; không hứa thao tác ngoài API/flow được duyệt. | Copy khái quát về phân loại/quản trị. |
| 14 | Export report button | Chỉ enable khi có user-list export contract, permission và result/file flow. | Button không có handler/API. |
| 15 | Add user button | Chỉ enable khi AC/API create-user và route form được duyệt. | Button không có handler; AC-31 #68–#72 không khai báo create. |
| 16 | Keyword search input | #68 chỉ tìm literal substring trên full_name/email; bỏ “mã người dùng” khỏi hint hoặc bổ sung contract trước khi tìm ID. | Placeholder nói tên/email/mã user; không request. |
| 17 | Role filter select | Gửi role exact-match theo enum/string values được owner duyệt; không tự map UI label/value. | Values `student`, `instructor`, `admin`; không có change listener. |
| 18 | Status filter select | Gửi status exact-match theo values được duyệt; không tự map `locked` sang trạng thái khác. | Values `active`, `locked`, `pending`; không có change listener. |
| 19 | Reset filters button | Xóa filter state trên URL và tải page phù hợp sau khi client policy chốt. | Xóa ba controls local và focus search; không update URL/refetch. |
| 20 | Active filter summary | Hiển thị filter đang áp dụng, không chỉ giá trị trong control chưa submit. | Static “Tất cả tài khoản”; chưa gắn state. |
| 21 | Server synchronization status | Chỉ render khi có sync status source/API. | Static “Đồng bộ máy chủ: Vừa xong”. |
| 22 | User table column header | ID, full name, email, role, status, created date, actions; fields map từ #68 như §A. | Header có bảy cột, không có row data. |
| 23 | Empty-state illustration | Trang trí; không dùng để phân biệt lỗi với no-match nếu không có text/state. | Icon tài khoản trống/bị gạch. |
| 24 | Empty-state title | Với `items=[]`, dùng copy nói rõ danh sách hiện không có kết quả. | “Chưa có dữ liệu tài khoản người dùng”. |
| 25 | Empty-state explanation | Nêu filter/no-match; không tuyên bố sync đang chờ nếu API không xác nhận. | Copy khẳng định đang chờ đồng bộ auth server. |
| 26 | Refresh list button | Gọi lại #68 với filter/page hiện hành; disable/loading chống request lặp theo UI policy. | Disabled; không listener. |
| 27 | Input guide button | Link tới nội dung hướng dẫn có đích; không gắn hành vi chưa có. | Button không có handler. |
| 28 | Visible account count | Dựa vào `items.length` và `pagination.total`; empty page hiển thị 0/total. | Hiển thị tĩnh 0 trên 0. |
| 29 | Previous page button | Disabled ở page 1 hoặc không có trang trước; cập nhật query URL khi chuyển trang. | Disabled. |
| 30 | Current page / total pages | Dùng `pagination.page` và `pagination.total_pages`; empty display policy cần chốt vì API page=1, total_pages=0 nhưng mockup ghi 0/0. | Static `0 / 0`. |
| 31 | Next page button | Disabled khi `page >= total_pages`; server size cố định 20. | Disabled. |
| 32 | Security notice icon | Decorative; status/assurance phải có text, không chỉ màu/icon. | Icon shield static. |
| 33 | Security notice heading | Chỉ trình bày chính sách được approved và có owner. | “Chính sách bảo mật hệ thống”. |
| 34 | Security notice body copy | Không khẳng định audit log được ghi nếu không có audit contract/evidence. | Khẳng định truy xuất được ghi nhật ký hệ thống định danh; API #68 không ghi/đọc audit log. |
| 35 | Footer copyright/workspace | Static product attribution; không biểu thị runtime version. | “© 2025 Study2Work LMS” và workspace label. |
| 36 | Privacy policy footer link | Link tới chính sách hiện hành khi route/document có đích. | `href="#"`. |
| 37 | RBAC standards footer link | Link tới nội dung thật; badge/footer copy không chứng minh RBAC compliance. | `href="#"`. |
| 38 | Technical support footer link | Chỉ link khi có support destination. | `href="#"`. |

## 4. Conditional UI & state variations
- States theo inventory: loading/empty/ready/filter-error
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/05_admin/AD-02_danh-sach-nguoi-dung/AD-02.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
