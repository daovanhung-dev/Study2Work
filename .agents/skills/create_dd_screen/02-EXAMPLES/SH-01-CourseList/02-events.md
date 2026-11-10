# SH-01 — Events

## 1. Event index
| Event ID | Trigger | EL | API | Rule / Test |
|---|---|---|---|---|
| `SH-01-EV-001` | Screen mount | EL-001 | API-001 | BR-004 / TC-001 |
| `SH-01-EV-002` | Gõ từ khóa | EL-003 | API-001 | BR-001/002/005 / TC-002/004/006 |
| `SH-01-EV-003` | Thay topic | EL-004 | API-001 | BR-002/003/005 / TC-003 |
| `SH-01-EV-004` | Click course card | EL-006 | — | — / TC-007 |
| `SH-01-EV-005` | Click page | EL-007 | API-001 | BR-003/005 / TC-005 |
| `SH-01-EV-006` | Click Thử lại | conditional EL-006 | API-001 | BR-005 / TC-008 |
| `SH-01-EV-007` | Click Đặt lại bộ lọc | conditional EL-006 | API-001 | BR-002 / TC-003 |

## 2. SH-01-EV-001 — InitialLoad
- **Trigger:** router mount `/courses`.
- **Guard:** screen chưa disposed; không yêu cầu đăng nhập.
- **Input:** default `keyword=''`, `topic='all'`, `page=1`, `pageSize=6`.
- **Steps:** (1) tạo state; (2) `status=loading`, `items=[]`; (3) tăng sequence, gọi `SH-01-API-001`; (4) validate/map response theo data-flow; (5) render cards/count/pagination; (6) 200 empty → empty state.
- **Error:** API/network/timeout → error state với Thử lại; response trễ sau unmount bỏ qua.
- **Output:** danh sách công khai, không navigate; **Test:** TC-001, TC-008.

## 3. SH-01-EV-002 — SearchChanged
- **Trigger:** người dùng nhập/clear `SH-01-EL-003`.
- **Inputs:** `searchKeyword` từ input, `topic` và `pageSize` từ state.
- **Guard/validation:** input max 80; trim (BR-001); xóa timer debounce cũ.
- **Steps:** (1) update raw input; (2) reset `page=1`; (3) đợi 300ms kể từ ký tự cuối; (4) tăng requestSeq, abort/ignore request cũ; (5) set loading; (6) gọi `SH-01-API-001` với keyword đã trim và topic; (7) map response, update total/items; (8) render result/empty.
- **Error/race:** lỗi từ request cũ bỏ qua, lỗi request mới nhất hiển thị Retry; query trống → lấy full list; network retry thủ công.
- **Output:** không navigate; **Rules:** BR-001, BR-002, BR-005; **Tests:** TC-002, TC-004, TC-006.

## 4. SH-01-EV-003 — TopicChanged
- **Trigger:** chọn topic ở `SH-01-EL-004`.
- **Input:** enum topic từ select; keyword hiện tại từ state.
- **Guard:** topic phải thuộc enum (BR-003), nếu giá trị không hợp lệ không gửi request.
- **Steps:** (1) update topic; (2) reset page 1; (3) abort/ignore request cũ; (4) gọi API-001 ngay với keyword/topic/page=1; (5) map response; (6) render list/empty.
- **Error:** status error và Retry nếu thất bại; **Tests:** TC-003, TC-006.

## 5. SH-01-EV-004 — OpenCourseDetail
- **Trigger:** click/Enter trên `SH-01-EL-006` card.
- **Input:** `courseId` từ card object đã render; **Guard:** ID không rỗng.
- **Steps:** (1) lấy id; (2) URL encode path segment; (3) điều hướng `/courses/{courseId}` → `SH-02`; (4) SH-02 tự tải chi tiết.
- **Error:** id rỗng: không navigate, báo telemetry nội bộ (nếu dự án có); **Test:** TC-007.

## 6. SH-01-EV-005 — ChangePage
- **Trigger:** click `Trước`, `Sau` hoặc số trang tại `SH-01-EL-007`.
- **Input:** `targetPage` integer từ nút; **Guard:** 1 ≤ targetPage ≤ totalPages; loading không cho click.
- **Steps:** (1) set page; (2) giữ keyword/topic; (3) gọi API-001; (4) update cards/count/pagination; (5) scroll về đầu khu vực kết quả.
- **Error:** giống EV-001; retry giữ nguyên targetPage; **Rules:** BR-003/005; **Test:** TC-005.

## 7. SH-01-EV-006 — RetryLoad
- **Trigger:** nút `Thử lại` trong error state.
- **Guard:** không có request đang chạy; **Inputs:** keyword/topic/page hiện tại.
- **Steps:** set loading, tăng sequence, gọi lại API-001 với params y nguyên, render success/empty hoặc error.
- **Error:** nếu tiếp tục lỗi vẫn giữ nút Thử lại; **Test:** TC-008.

## 8. SH-01-EV-007 — ResetFilters
- **Trigger:** nút `Đặt lại bộ lọc` trong empty state.
- **Steps:** set `keyword=''`, `topic='all'`, `page=1`, hủy debounce cũ, gọi API-001, render kết quả.
- **Error:** error state và retry; **Test:** TC-003.

## 9. Truy vết
[Data flow](03-data-flow.md) · [API](04-api-integration.md) · [Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Tests](07-test-cases.md)
