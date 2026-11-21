# ST-08 — Navigation

## 1. Route definition
- Current route in inventory: `/student/courses`
- Status: candidate/design route; Study Web `UNWIRED` unless source code proves otherwise.
- Route params/types: Không có route param được biểu diễn trong inventory string; route runtime vẫn chưa xác minh.
- Query params/defaults: preserve the inventory route string; detailed parsing rules only from source DD.
- Route guards: see source DD/API contract; do not create role policy.

## 2. Điểm vào
| From screen/route | Trigger | Params | Guard / fallback |
|---|---|---|---|
| [ST-01](../ST-01-TongQuanHocVien/00-overview.md), [ST-04](../ST-04-KiemTraGhiDanhTruocDangKy/00-overview.md), [ST-07](../ST-07-KetQuaDangKyKhoaHoc/00-overview.md) | Theo DD nguồn/inventory | Theo source; không suy diễn | Xem source DD; route chưa xác nhận runtime |

## 3. Điểm ra
| Destination | Trigger | Params | Điều kiện |
|---|---|---|---|
| [ST-09](../ST-09-TongQuanKhoaDangHoc/00-overview.md), [ST-20](../ST-20-TongQuanTienDo/00-overview.md) | Source event/inventory navigation | Theo source DD | Expected links; runtime chưa verify |

## 4. Back / refresh / deep link
- Back behavior: xem source DD; không mặc định browser history.
- Preserve filters/scroll/form state: chỉ nếu source có nêu, nếu không `CẦN_XÁC_NHẬN`.
- Refresh/direct URL: route trong inventory không chứng minh runtime.
- Invalid/missing ID: theo source DD/backend contract; không tự tạo validation.
- Not authenticated/authorized: theo source role guard; xem [Business Rules](05-business-rules.md).

## 5. Diagram
```mermaid
flowchart LR
  S0["ST-08 Khóa học của tôi"] --> S1["ST-09"]
  S0["ST-08 Khóa học của tôi"] --> S2["ST-20"]
```

## Source navigation and flow detail

### Trích từ DD nguồn: E. Ma trận trạng thái và điều hướng

| State | Điều kiện thiết kế | UI/transition hiện có | Gap |
|---|---|---|---|
| Initial / route entry | Student mở route đề xuất `/student/courses`. | HTML được render thẳng thành empty mock; không có app initialization. | Route, session guard và navigation history chưa wired. |
| Loading | Request #20/#21 đang xử lý. | Không có loading indicator trong asset. | Request lifecycle, ordering, cancellation, timeout chưa có source/contract. |
| Empty | AC-13 decision label says `NO → empty state`. | Empty card/copy có sẵn như nội dung tĩnh. | AC-13's `EMPTY` and `HAS DATA` edges both target the same course-render node; destination is ambiguous. #20/#21 empty wire shape and distinction between “no course” and “data not updated” are unresolved. |
| Loaded | #20 trả enrollment/course data hợp lệ. | Chưa có list/card trong HTML/PNG. | Course schema, ordering, paging, card contents và selection chưa được thiết kế. |
| Partial progress | Có courses nhưng một phần progress thiếu/không tải được, theo nhãn inventory. | Không có phần tử tương ứng. | Không rõ thiếu progress là 0, unknown, retry hay lỗi; merge/partial failure policy chưa chốt. |
| Filtered | User áp status filter. | Không có filter control. | Option/default/field semantics và query behavior #20 chưa chốt. |
| API/auth/validation error | API trả một status code đã khai báo hoặc xảy ra lỗi mạng. | Không có error state, copy hoặc recovery action trong asset. | Response error schema, retry, reauth và UI mapping chưa có contract. |

Các state `loading/empty/partial-progress/error` là inventory expectations. Chúng không phải state machine đã được triển khai. Không có transition nào được xác minh khi chạy.

### Trích từ DD nguồn: B. Luồng hoạt động tổng thể

### Tiền điều kiện và nguồn dữ liệu

- AC-13 yêu cầu Student đã đăng nhập; API catalog cũng khai báo Bearer JWT và role Student cho #20/#21.
- API dùng path `/users/me`; catalog không chỉ định user ID trong query/body. Cách backend liên kết JWT với `enrollments.user_id`/progress ownership vẫn là câu hỏi mở trong API DD. Không suy ra claim cụ thể hoặc cách xử lý user/profile không tồn tại.
- Route `/student/courses` là đề xuất. Không có bằng chứng về client session guard, redirect, route history hoặc dữ liệu được cache.
- Dữ liệu dự kiến là course/enrollment list từ #20 và tiến độ aggregate từ #21; khóa ghép dự kiến theo `course_id`. Trường, kiểu, ordering, paging tổng thể, quy tắc progress và empty representation chưa được xác nhận.

### Trình tự thiết kế và giới hạn hiện tại

1. Khi Student đi vào route dự kiến `/student/courses`, thiết kế yêu cầu có session Student hợp lệ. UI runtime/guard chưa tồn tại trong checkout nên bước auth hiện không được thực thi ở client.
2. Thiết kế gọi #20 để lấy khóa đã đăng ký, với query tùy chọn `status` và `page`. `page` có kiểu `int32`; catalog không định nghĩa default, base index, page size, maximum, sort hoặc total metadata.
3. AC-13 gọi thêm #21 và yêu cầu ghép theo `course_id`; inventory cho phép bỏ qua #21 nếu response #20 đã chứa progress. Điều kiện bỏ qua, query #21 và response schemas chưa chốt, nên request order/parallelism chưa thể được triển khai xác định.
4. AC-13 ghi nhánh `NO → empty state; YES → render`, nhưng hai cạnh `EMPTY` và `HAS DATA` của decision node cùng đi tới node “Hiển thị khóa học + % hoàn thành”. Cần làm rõ diagram destination trước khi chốt transition. Asset hiện có minh họa empty state tĩnh, nhưng không có wire response nào ánh xạ vào trạng thái đó.
5. Nếu có course, inventory mong đợi list/filter/progress bar và điều hướng chọn khóa sang ST-09. HTML không có list/card/filter/progress bar; không thể xác định vị trí, label, data fields hoặc card interaction từ asset hiện tại.
6. CTA “Xem tiến độ học tập” và nav links có `href` tới `/student/progress` (ST-20), còn brand/nav overview trỏ `/student` (ST-01). Router/runtime destination và back behavior chưa được xác minh.
7. Khi #20/#21 trả lỗi, catalog liệt kê các mã bên dưới; màn hình hiện tại không có error/loading/partial state UI hoặc retry logic. Không tự đặt retry, timeout hay cache policy.

```mermaid
flowchart LR
  SH02[SH-02: Student sign-in] --> ST01[ST-01: Overview]
  ST07[ST-07: Enrollment result] --> ST08[ST-08: My courses]
  ST08 -->|course card expected; absent in current design| ST09[ST-09: Course overview]
  ST08 -->|CTA / header / footer href| ST20[ST-20: Progress overview]
  ST08 -->|overview link| ST01
```

ST-07 → ST-08 is appropriate only after the enrollment outcome is confirmed by the enrollment/payment flow; a client return or payment callback alone is not proof of enrollment. The ST-08 list API is intended to reload current enrollment data, but that API is not currently source-backed. ST-09 expects a `courseId` path segment (`/student/courses/:courseId`); ST-08 has no course-card payload or verified identifier to pass. ST-20 is a proposed destination and does not receive an identifier in the shown href.
