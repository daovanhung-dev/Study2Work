# SH-02 — UI Elements

[Ảnh gốc](images/screen-clean.png) · [Ảnh marker](images/screen-numbered.png)

## 1. Element mapping
| Marker | Element ID | Loại | Binding/Source | Event |
|---|---|---|---|---|
| #1 | `SH-02-EL-001` | Back link | static `← Về danh sách` | `SH-02-EV-002` |
| #2 | `SH-02-EL-002` | Breadcrumb | `/courses` + current course | `SH-02-EV-002` |
| #3 | `SH-02-EL-003` | Course title | API-001 `title` | — |
| #4 | `SH-02-EL-004` | Topic/level badges | API-001 `topic`, `level` | — |
| #5 | `SH-02-EL-005` | Description | API-001 `description` | — |
| #6 | `SH-02-EL-006` | Chapter accordion | API-001 `chapters[]` | `SH-02-EV-003` |
| #7 | `SH-02-EL-007` | Enroll CTA | auth/enrollment status | `SH-02-EV-004` |
| #8 | `SH-02-EL-008` | Course metadata panel | duration, lesson count | — |

## 2. Chi tiết
### SH-02-EL-001 — Back to catalog
- Link text `← Về danh sách`; click → `SH-02-EV-002` đến `/courses` (không phụ thuộc history).
- Hiển thị ở ready/loading/error/not-found; keyboard focus rõ.

### SH-02-EL-002 — Breadcrumb
- `Khóa học / Chi tiết`; phần `Khóa học` có link về `/courses` dùng `SH-02-EV-002`.

### SH-02-EL-003 — Course title
- H1 từ `CourseDetail.title`; nếu loading skeleton; không render untrusted HTML từ API.

### SH-02-EL-004 — Tags
- Nhãn cấp độ (`Cơ bản`, `Trung cấp`) và chủ đề; mapping enum ở data-flow; Unknown → `Chưa phân loại`.

### SH-02-EL-005 — Description
- Text đa dòng từ API; escape output theo framework; nếu string rỗng → `Chưa có mô tả`.

### SH-02-EL-006 — Chapter accordion
- List `chapters[]`; mỗi chapter gồm title + số bài học; click → `SH-02-EV-003` toggle open.
- Default tất cả đóng; `expandedChapterIds` local state; không gọi API khi expand.
- Không có chapter: `Nội dung đang cập nhật`. Accessible expanded/collapsed state.

### SH-02-EL-007 — CTA đăng ký
- Anonymous: `Đăng nhập để đăng ký`; member chưa enroll: `Đăng ký ngay`; member đã enroll: `Đã đăng ký` disabled.
- Nếu unpublished/404/GET error/loading: CTA không cho click; POST pending spinner và disabled.
- On click → `SH-02-EV-004`; thông báo success/toast phát sinh từ `SH-02-EV-004`.

### SH-02-EL-008 — Thông tin khóa học
- Hiển thị `duration_minutes` → `N giờ M phút` và `lessons_count` → `N bài học`.
- Null duration → `Chưa cập nhật`, không dùng `0 phút` để giả định dữ liệu.

## 3. State & responsive
- Desktop demo 1280×800: main content trái và CTA/info panel phải; mobile panel xếp dưới content.
- Error banner + Retry là conditional UI gọi `SH-02-EV-006`.
- Not-found hiển thị fallback `Không tìm thấy khóa học` và link `/courses`.
