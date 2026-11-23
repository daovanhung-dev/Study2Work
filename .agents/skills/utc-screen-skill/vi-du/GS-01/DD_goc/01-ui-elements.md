# GS-01 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [GS-01_markers.json](../../screen_stitch/02_guest_discovery/GS-01_danh-sach-khoa-hoc/GS-01_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `GS-01-EL-001` | `GS01-EL-01` | Header nav item Khóa học (active) |
| #2 | `GS-01-EL-002` | `GS01-EL-02` | Header search input and search icon |
| #3 | `GS-01-EL-003` | `GS01-EL-03` | Header link Đăng nhập |
| #4 | `GS-01-EL-004` | `GS01-EL-04` | Header CTA Đăng ký |
| #5 | `GS-01-EL-005` | `GS01-EL-05` | Page title Danh sách khóa học |
| #6 | `GS-01-EL-006` | `GS01-EL-06` | Supporting description |
| #7 | `GS-01-EL-007` | `GS01-EL-07` | Main search input and search icon |
| #8 | `GS-01-EL-008` | `GS01-EL-08` | Button Tìm kiếm and arrow icon |
| #9 | `GS-01-EL-009` | `GS01-EL-09` | Empty-state book illustration |
| #10 | `GS-01-EL-010` | `GS01-EL-10` | Empty-state heading |
| #11 | `GS-01-EL-011` | `GS01-EL-11` | Empty-state explanatory copy |
| #12 | `GS-01-EL-012` | `GS01-EL-12` | Footer brand Study2Work |
| #13 | `GS-01-EL-013` | `GS01-EL-13` | Footer link Trang chủ |
| #14 | `GS-01-EL-014` | `GS01-EL-14` | Footer link Khóa học |
| #15 | `GS-01-EL-015` | `GS01-EL-15` | Footer link Đăng nhập |
| #16 | `GS-01-EL-016` | `GS01-EL-16` | Footer link Đăng ký |

## 3. Đặc tả từng element

### Trích từ DD nguồn: 3. Element được đánh số

Marker #1–#16 ánh xạ một-một với 16 vùng nhìn thấy trong ảnh gốc. Vị trí là theo screenshot 1280×1114; trạng thái hover/focus chưa được thể hiện. Vùng không hiện trong ảnh được nêu riêng ở §4, không nhận marker giả.

| # / Element ID | Tên, loại, vị trí | Thuộc tính và nguồn dữ liệu | Hiển thị / trạng thái / sự kiện |
|---|---|---|---|
| #1 `GS01-EL-01` | Header nav item `Khóa học`, navigation item, header giữa-trái. | Nhãn tĩnh trong thiết kế; route mục tiêu `/courses` chỉ là proposal. | Hiện và active theo screenshot. `GS01-EV-08`; current HTML `href="#"`, không có router. |
| #2 `GS01-EL-02` | Header search input + icon, header giữa-phải. | Text input; nội dung nhập là chuỗi người dùng. Placeholder/giới hạn/chuẩn hóa chưa được khóa trong contract. | Hiện, không có loading/validation behavior được duyệt. `GS01-EV-02`; current DOM không có listener/form. |
| #3 `GS01-EL-03` | Link `Đăng nhập`, header phải. | Nhãn tĩnh; mục tiêu đề xuất SH-02 `/login`. | Hiện. `GS01-EV-09`; hiện `href="#"` và `data-path` mock. |
| #4 `GS01-EL-04` | CTA `Đăng ký`, header phải. | Nhãn tĩnh; mục tiêu đề xuất SH-03 `/register`. | Hiện. `GS01-EV-10`; hiện `href="#"` và `data-path` mock. |
| #5 `GS01-EL-05` | Tiêu đề `Danh sách khóa học`, heading H1, phần đầu nội dung. | Văn bản tĩnh trong ảnh; không lấy từ API. | Hiện trong empty state. Không có event. |
| #6 `GS01-EL-06` | Mô tả hỗ trợ dưới H1, text block. | Văn bản tĩnh theo design source; nội dung/copy cho các trạng thái loaded/error chưa được duyệt. | Hiện trong empty state. Không có event. |
| #7 `GS01-EL-07` | Search input chính + icon, dưới phần giới thiệu. | Text input; giá trị do Guest nhập. Giới hạn, debounce, trim và route handoff chưa được xác nhận cho GS-01. | Hiện. `GS01-EV-03`; current DOM không có listener/form. |
| #8 `GS01-EL-08` | Button `Tìm kiếm` + arrow, cạnh input chính. | Button; input #7 là nguồn dự kiến. Không có API/body xác nhận trên màn này. | Hiện/enabled theo screenshot, nhưng handler current không được gắn do lỗi script. `GS01-EV-04`. |
| #9 `GS01-EL-09` | Minh họa sách của empty state, decorative image/icon. | Asset inline/visual trong thiết kế; không đại diện cho dữ liệu catalog. | Hiện khi nguồn ảnh đang ở empty state. Không tương tác; accessibility nên đánh dấu decorative nếu đúng mục đích sau khi được kiểm tra source. |
| #10 `GS01-EL-10` | Heading empty state, text. | Nội dung tĩnh từ ảnh/HTML. Copy hiện gộp không có dữ liệu với “đang cập nhật”; cần tách rõ theo state. | Chỉ thấy trong source empty state. Không có event. |
| #11 `GS01-EL-11` | Mô tả empty state, text. | Nội dung tĩnh từ ảnh/HTML; không chứa kết quả API. | Chỉ thấy trong source empty state. Không có event. |
| #12 `GS01-EL-12` | Footer brand `Study2Work`, brand text. | Nhãn/brand tĩnh trong screenshot; HTML header brand là discrepancy khác, không ánh xạ vào element này. | Hiện trong footer. Không có event được xác nhận. |
| #13 `GS01-EL-13` | Footer link `Trang chủ`. | Nhãn tĩnh; route mục tiêu `/` proposal SH-01. | Hiện. `GS01-EV-11`; current `href="#"`. |
| #14 `GS01-EL-14` | Footer link `Khóa học`. | Nhãn tĩnh; route mục tiêu `/courses` proposal GS-01. | Hiện. `GS01-EV-11`; current `href="#"`. |
| #15 `GS01-EL-15` | Footer link `Đăng nhập`. | Nhãn tĩnh; route mục tiêu `/login` proposal SH-02. | Hiện. `GS01-EV-11`; current `href="#"`. |
| #16 `GS01-EL-16` | Footer link `Đăng ký`. | Nhãn tĩnh; route mục tiêu `/register` proposal SH-03. | Hiện. `GS01-EV-11`; current `href="#"`. |

**Quy tắc element:** PNG không chứa card, select, category chips, result count, pagination hoặc reset-filter control. Không có điều kiện enable/disable, hover/focus, loading card hay validation contract được xác nhận ngoài trạng thái nhìn thấy. Element mới cần source/design approval trước khi bổ sung vào map.

## 4. Conditional UI & state variations
- States theo inventory: loading/empty/ready/query-error
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/02_guest_discovery/GS-01_danh-sach-khoa-hoc/GS-01.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
