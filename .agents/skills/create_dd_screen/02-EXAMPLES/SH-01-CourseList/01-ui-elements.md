# SH-01 — UI Elements

[Ảnh sạch](images/screen-clean.png) · [Ảnh có marker](images/screen-numbered.png)

## 1. Marker mapping
| Marker | Element ID | Loại | Binding/source | Events |
|---|---|---|---|---|
| #1 | `SH-01-EL-001` | Top navigation | static `Study2Work`, link `/courses` | `SH-01-EV-001` (mount) |
| #2 | `SH-01-EL-002` | Heading | static `Khám phá khóa học` | — |
| #3 | `SH-01-EL-003` | Search input | `searchKeyword` (user input) | `SH-01-EV-002` |
| #4 | `SH-01-EL-004` | Topic selector | `topic` (`all`, `programming`, `backend`) | `SH-01-EV-003` |
| #5 | `SH-01-EL-005` | Result summary | `totalItems` (API.pagination.total_items) | — |
| #6 | `SH-01-EL-006` | Course card list | `items[]` (API DTO → ViewModel) | `SH-01-EV-004` |
| #7 | `SH-01-EL-007` | Pagination | `page`, `totalPages` | `SH-01-EV-005` |

## 2. Đặc tả element

### SH-01-EL-001 — Header
- Vùng trên cùng toàn chiều rộng, logo `Study2Work`, tab `Khóa học` active.
- Có trong loading/success/empty/error. Tab active không phát thêm request nếu ở trang hiện tại.
- Semantic: `nav`, link có text; màn desktop ví dụ 1280px, mobile thu gọn menu nếu có thiết kế riêng.

### SH-01-EL-002 — Page title
- H1 `Khám phá khóa học`; nội dung tĩnh, không nhận dữ liệu API; luôn hiển thị.

### SH-01-EL-003 — Tìm kiếm
- Input type `search`; placeholder `Tìm tên khóa học...`; binding `searchKeyword: string`.
- Khi gõ: `SH-01-EV-002`; debounce 300 ms; chuỗi được chuẩn hóa theo `SH-01-BR-001` trước khi gọi API.
- Không khóa input trong lúc loading; nếu query cũ đang chạy, loại bỏ/ignore response cũ.
- Label có thể đọc bằng screen reader `Tìm khóa học`.

### SH-01-EL-004 — Bộ lọc chủ đề
- Select có nhãn `Chủ đề`, 3 lựa chọn: `Tất cả` → `all`, `Lập trình` → `programming`, `Backend` → `backend`.
- Default `all`; change → `SH-01-EV-003`; state phải đồng bộ với query hiện tại.
- Nếu topic hợp lệ nhưng không có kết quả, hiển thị Empty (không xem là lỗi).

### SH-01-EL-005 — Tổng kết kết quả
- Hiển thị `totalItems` theo định dạng `<số> khóa học`, với totalItems là integer không âm; **không** dùng số lượng items của riêng trang hiện tại.
- Khi loading: `Đang tải...`; khi lỗi: `Không có dữ liệu` (không hiển thị số stale).

### SH-01-EL-006 — Course card repeatable
- Card template: thumbnail placeholder, title, level label, chủ đề, mô tả ngắn; ví dụ `Lập trình Python căn bản`.
- Source: `CourseListItem[]` từ `SH-01-API-001`, mapping ở [Data](03-data-flow.md).
- Click/keyboard Enter → `SH-01-EV-004` với `courseId` card được chọn; không điều hướng nếu id rỗng.
- Rendering: mỗi card dùng anchor có accessible name là title; ảnh lỗi dùng fallback placeholder.
- Empty: thay card grid bằng text `Không có khóa học phù hợp` + nút `Đặt lại bộ lọc` → `SH-01-EV-007`.
- Error: thay grid bằng banner `Không tải được danh sách` + nút `Thử lại` → `SH-01-EV-006`.

### SH-01-EL-007 — Phân trang
- Hiển thị khi `totalPages > 1`; các nút `Trước`, số trang, `Sau`.
- Disabled `Trước` khi page=1, `Sau` khi page=totalPages, tất cả disabled khi loading.
- Click → `SH-01-EV-005`, có `targetPage` hợp lệ.

## 3. Responsive và trạng thái
- Mock ảnh là **desktop** 1280 × 800. Ở mobile 1 cột cards; filter xuống hàng; nội dung chi tiết cần tuân theo design token dự án thật.
- `loading`: skeleton card; `empty`: text + reset; `error`: banner retry; `success`: card grid.
- Nút reset/thử lại là **conditional UI**, không có marker trên ảnh success.
