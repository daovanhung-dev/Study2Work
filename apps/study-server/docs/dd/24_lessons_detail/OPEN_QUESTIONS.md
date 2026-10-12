# OPEN_QUESTIONS

Các quyết định dưới đây cần xác nhận trước khi chuyển DD sang Ready/Final hoặc dùng làm implementation contract. Bản Draft giữ contract đã công bố và không tự chọn câu trả lời.

<a id="q-24-01"></a>

## Q-24-01 — Entitlement predicate và JWT identity

**Bằng chứng**

- API catalog yêu cầu Bearer JWT và role Student.
- AC-14 precondition nói Student đã enrolled vào course chứa lesson; sơ đồ đặt API #22 enrollment/prerequisite check trước API #24.
- AC-15 precondition nói Student có quyền xem lesson.
- Checked-in DDL/DB design có quan hệ `enrollments.user_id`, `course_id`, `status`; API #24 chưa có query hoặc auth binding.

**Vấn đề**

- Chưa xác định enrollment status nào cấp quyền, prerequisite nào phải đạt hoặc nguồn nào đánh giá prerequisite.
- Chưa xác định JWT claim nào được bind vào enrollment lookup của API #24.
- Chưa rõ API #24 phải tự kiểm tra entitlement khi được gọi trực tiếp hay có policy dùng chung đã được phê duyệt.

**Ảnh hưởng**

- Không thể chốt authorization predicate, query, thứ tự kiểm tra hoặc điều kiện trả 403.
- Không thể coi client gọi API #22 trước đó là ranh giới bảo mật cho API #24.

**Cần quyết định**

- Xác nhận token identity binding, enrollment eligibility/status, prerequisite source/evaluation và yêu cầu server-side entitlement cho lời gọi API #24 độc lập.

<a id="q-24-02"></a>

## Q-24-02 — Phạm vi trạng thái publish

**Bằng chứng**

- AC-15 diagram ghi `Kiểm tra access + trạng thái publish` trước bước đọc lesson/content.
- Candidate schema có `lessons.status` và `courses.status`; adjacent public-course design dùng status `PUBLISHED` trong một số API.
- API #24 không có query/predicate trong current source.

**Vấn đề**

- Chưa rõ publish gate áp dụng cho lesson, parent course hay cả hai.
- Chưa có enum đầy đủ hoặc policy xác nhận giá trị nào được xem là published.
- Không được chuyển điều kiện của API #9/#12 sang API #24 nếu chưa được xác nhận.

**Ảnh hưởng**

- Không thể chốt filter, join, visibility hoặc hành vi khi lesson/course chưa publish.

**Cần quyết định**

- Xác nhận entity/status được kiểm tra, allowed values và cách xử lý khi lesson hoặc parent course không published.

<a id="q-24-03"></a>

## Q-24-03 — 403/404 semantics và error payload

**Bằng chứng**

- Catalog khai báo 403 `DESIGN_ACCESS_DENIED` và 404 `DESIGN_RESOURCE_NOT_FOUND`.
- AC-14 diagram nói nhánh access denial của API #22 trả 403 + reason; AC-15 không định nghĩa error payload cho API #24.
- Reusable `ApiEnvelope<T>` không mô tả error-specific `data`, message hoặc reason field.

**Vấn đề**

- Chưa rõ lesson không tồn tại, không có quyền và lesson/course chưa publish phân biệt 403/404 ra sao.
- Chưa biết message/error data/reason có cấu trúc nào; reason của API #22 không tự động áp dụng cho API #24.

**Ảnh hưởng**

- Không thể chốt client-visible error payload, message hoặc che giấu resource visibility.

**Cần quyết định**

- Xác nhận 403/404 condition, visibility policy và error envelope/message fields cho API #24.

<a id="q-24-04"></a>

## Q-24-04 — Query, projection và schema baseline

**Bằng chứng**

- Catalog response là `ApiEnvelope<Lesson>` với fields `id`, `course_id`, `title`, `content?`, `video_url?`, `order`, `status`.
- DB design mô tả candidate mapping từ `lessons.name` sang `title` và `sort_order` sang `order`.
- Checked-in `DB.sql` là thiết kế, không xác nhận live schema; API #24 query chưa tồn tại.
- DDL khai báo `lessons.course_id BIGINT REFERENCES courses(id)` không có `NOT NULL`; DB_UNICA_TABLES mô tả quan hệ này là bắt buộc và schema catalog đòi `course_id:int64`.

**Vấn đề**

- Chưa có approved query/projection, join, access/publish filters hoặc live schema baseline.
- Có nullability discrepancy giữa DDL checked-in và DB design/schema kỳ vọng cho `course_id`.

**Ảnh hưởng**

- Các cột trong DD chỉ là candidate design mapping; không thể dùng làm SQL đã phê duyệt hoặc claim về runtime.

**Cần quyết định**

- Cung cấp/duyệt query/projection và schema có thẩm quyền; giải quyết nullability của `course_id` trước khi implementation.

<a id="q-24-05"></a>

## Q-24-05 — Optional/null serialization và LessonStatus

**Bằng chứng**

- Catalog đánh dấu `content` và `video_url` là optional; DDL cho phép NULL.
- Catalog định kiểu `video_url` là URI và `status` là `LessonStatus` nhưng không liệt kê enum values.

**Vấn đề**

- Chưa rõ giá trị NULL được trả là `null`, bị lược bỏ hay được chuẩn hóa; chưa có URI serialization/validation rule.
- Chưa có danh sách giá trị hợp lệ và capitalization/casing của `LessonStatus`.

**Ảnh hưởng**

- Không thể khóa OpenAPI/schema validation hoặc ví dụ response thành wire behavior đã xác nhận.

**Cần quyết định**

- Xác nhận optional field serialization, URI rule và enum `LessonStatus`.

<a id="q-24-06"></a>

## Q-24-06 — Path validation và status khi lesson_id không hợp lệ

**Bằng chứng**

- Catalog chỉ khai báo `path{lesson_id:int64!}`.
- API #24 codes không liệt kê 422; runtime route hiện không tồn tại.

**Vấn đề**

- Chưa có min/max hoặc positivity rule; không rõ contract muốn phản hồi gì khi path không parse thành int64 hoặc ID không hợp lệ.

**Ảnh hưởng**

- Không thể chốt mapping framework validation/resource lookup cho path lỗi mà không mở rộng contract.

**Cần quyết định**

- Xác nhận range/positivity policy và HTTP/business mapping cho path value không hợp lệ; giữ nguyên catalog hiện tại cho tới khi có quyết định.
