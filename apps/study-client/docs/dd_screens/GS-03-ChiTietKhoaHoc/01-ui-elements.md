# GS-03 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [GS-03_markers.json](../../screen_stitch/02_guest_discovery/GS-03_chi-tiet-khoa-hoc/GS-03_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `GS-03-EL-001` | `GS03-EL-01` | Header brand and primary navigation group |
| #2 | `GS-03-EL-002` | `GS03-EL-02` | Header login and register actions |
| #3 | `GS-03-EL-003` | `GS03-EL-03` | Breadcrumb navigation |
| #4 | `GS-03-EL-004` | `GS03-EL-04` | Course detail page heading |
| #5 | `GS-03-EL-005` | `GS03-EL-05` | Overview, curriculum and reviews tab group; latter tabs disabled |
| #6 | `GS-03-EL-006` | `GS03-EL-06` | Unavailable-state book icon |
| #7 | `GS-03-EL-007` | `GS03-EL-07` | Unavailable-state heading and explanatory text |
| #8 | `GS-03-EL-008` | `GS03-EL-08` | Return to course list link |
| #9 | `GS-03-EL-009` | `GS03-EL-09` | Footer brand |
| #10 | `GS-03-EL-010` | `GS03-EL-10` | Footer navigation links |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả element

Các ID và thứ tự dưới đây khớp marker trên ảnh. “Default” mô tả tĩnh trong HTML; không gán các trạng thái tương tác mà không có source.

| Marker / Element ID | Tên, loại, vị trí | Thuộc tính / dữ liệu / điều kiện | Trạng thái và sự kiện |
|---|---|---|---|
| #1 `GS03-EL-01` | Header brand và primary navigation, anchor + nav ở đầu trang | Brand `Study2Work` dẫn `/`; nav “Trang chủ” dẫn `/`, “Khóa học” dẫn `/courses`; nav desktop có class `hidden md:flex`, vì vậy bị ẩn dưới breakpoint `md`. Giá trị là literal trong HTML; không lấy từ API. | Default; hover class có trong HTML. `GS03-EV-05` navigation. Router chưa wired. |
| #2 `GS03-EL-02` | Nhóm link Đăng nhập / Đăng ký, header bên phải | Anchors `/login` và `/register`; không có auth state hay callback. | Default; anchor tương tác theo browser. `GS03-EV-05`; đích chưa runtime verified. |
| #3 `GS03-EL-03` | Breadcrumb navigation dưới header | “Trang chủ” → `/`; “Khóa học” → `/courses`; phần hiện tại “Chi tiết khóa học” là text, không phải link. Không có course name/ID trong breadcrumb. | Default. `GS03-EV-05` với hai anchor; current breadcrumb không có event. |
| #4 `GS03-EL-04` | H1 “Chi tiết khóa học”, đầu content | Literal tĩnh. Expected loaded course title không có element trong source. Không có validation hoặc data binding. | Default; không có event. Thiếu course title là gap thiết kế. |
| #5 `GS03-EL-05` | Nhóm tab Tổng quan / Đề cương / Đánh giá, dưới H1 | “Tổng quan” là button active; “Đề cương” và “Đánh giá” có `disabled="disabled"`. Không có `aria-selected`, tab panel relationship, URL sync, click handler hoặc API call trong HTML. | Tổng quan active tĩnh; hai tab disabled. Dự kiến tương tác được mô tả trong `GS03-EV-02` và `GS03-EV-03`, nhưng hiện không kích hoạt được. |
| #6 `GS03-EL-06` | Biểu tượng quyển sách trong unavailable panel | Material Symbol `menu_book` trong vùng icon 80×80, nền xanh nhạt. Chỉ trang trí; không có alt/accessible name riêng ngoài nội dung lân cận. | Default; không có event. Không đại diện trạng thái curriculum đã tải. |
| #7 `GS03-EL-07` | Heading và nội dung empty state | Heading “Thông tin khóa học hiện chưa có sẵn.”; body “Vui lòng kiểm tra lại liên kết hoặc quay lại danh sách khóa học.” Literal, không chứa API error/message hay course data. | Default. Chưa có phân biệt course 404, lỗi mạng, lỗi partial tab hoặc retry. |
| #8 `GS03-EL-08` | Link “Quay lại danh sách khóa học”, CTA trong panel | Anchor `/courses`; không mang `courseId`, query hay state khác. | Default; click thuộc `GS03-EV-04`. Chưa có router runtime. |
| #9 `GS03-EL-09` | Footer brand | Wordmark và icon là `div`, không phải anchor; không có link/click action. | Default; không có event. |
| #10 `GS03-EL-10` | Footer navigation | Static anchors tới `/`, `/courses`, `/login`, `/register`. | Default; `GS03-EV-05`. Router chưa wired. |

### Dữ liệu expected nhưng không có element/marker trong HTML

| Data/UI expected | Bằng chứng nguồn | Current API/source contract | Gap cần đóng |
|---|---|---|---|
| Course title, description, thumbnail, price, status | Inventory GS-03 | #08 trả `id`, `title`, `description?`, `thumbnail_url?`, `price` (decimal serialized as string), `status`; chỉ published course. | Chưa có loaded layout, currency/price formatting rule hay missing-value presentation. Không có category, rating, duration, tags hoặc old price trong model #08. |
| Mentor summary | Inventory và AC-05 | #08 trả `mentor{id, full_name, avatar_url?}`; mapper hiện yêu cầu mentor id/name. | Chưa có vị trí, fallback avatar hoặc click-through behavior. |
| Curriculum list | Inventory GS-04/F02 | #09 trả lesson `id`, `course_id`, `title`, `content?`, `video_url?`, `order`, `status`; query chỉ lấy PUBLISHED lessons. | Không có preview/access policy; chưa có thiết kế item, empty state hoặc lesson click behavior ở GS-03. Không suy ra course lesson được phép mở chỉ vì list là public. |
| Reviews, replies, rating | AC-05, API #10 design docs | Catalog khai báo `Page<Discussion>`; DD #10 draft nêu review title cần thiết nhưng DDL `discussions` không có `title`, rating column hoặc rating table. | API #10 chưa wired; không thể dựng rating average/filter hoặc review card như behavior hiện tại. |
| Enrollment CTA | Inventory GS-03 → ST-04 | #15 trong catalog trả một Enrollment nhưng chỉ nhận `course_id`, là public; F03/G-01 xác định đây là security blocker. | Không có CTA trong HTML. Cần chốt Guest→Student/login handoff, identity/selection của #15 và course ID transport trước khi định nghĩa hành vi. |

## 4. Conditional UI & state variations
- States theo inventory: loading/course-404/partial-tab-error
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/02_guest_discovery/GS-03_chi-tiet-khoa-hoc/GS-03.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
