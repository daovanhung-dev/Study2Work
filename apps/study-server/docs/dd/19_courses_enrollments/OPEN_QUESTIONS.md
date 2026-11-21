# OPEN_QUESTIONS

Các câu hỏi dưới đây chặn việc chuyển DD sang Ready/Final hoặc dùng làm hướng dẫn triển khai API #19. Bản Draft giữ contract đã có và không tự chọn câu trả lời.

## Q-19-01 — Body field và nguồn identity từ JWT

<a id="q-19-01"></a>

**Bằng chứng**

- API #19 trong list_api.md ghi path course_id:int64! và body course_id:int64!, user từ JWT:string!.
- Enrollment schema định nghĩa user_id:int64.
- Current Study auth helper đọc JWT sub, chuyển sub dạng số sang int và đọc roles.

**Vấn đề**

- Không rõ user là JSON field do client gửi hay identity chỉ được lấy từ JWT; tên wire field/claim và quy tắc chuyển string sang user_id chưa được xác định.

**Ảnh hưởng**

- Request validation, authorization, duplicate query, hai INSERT và data.user_id chưa thể chốt.

**Cần quyết định**

- Xác nhận schema body chính thức, claim identity, kiểu/format và liệu body có được gửi user identity hay không; nếu sửa contract, cập nhật nguồn canonical trước khi DD/API được chốt.

## Q-19-02 — Eligibility và semantics 404

<a id="q-19-02"></a>

**Bằng chứng**

- AC-12 có precondition course tồn tại; trước API #19, flow đọc Course PUBLISHED và kiểm tra Enrollment qua các API khác.
- API #19 row vẫn liệt kê 404 DESIGN_RESOURCE_NOT_FOUND.
- AC-12 gọi API #19 cho course miễn phí hoặc sau khi thanh toán thành công.

**Vấn đề**

- Chưa rõ API #19 tự xác thực course tồn tại/published và quyền đủ điều kiện hay dựa vào bước trước; chưa rõ cách xác nhận điều kiện paid course khi endpoint được gọi trực tiếp.
- Chưa xác định resource nào tạo ra 404.

**Ảnh hưởng**

- Không thể chốt query guard, eligibility, hoặc semantics 404 mà không thêm rule.

**Cần quyết định**

- Xác nhận các guard bắt buộc bên trong API #19 cho course không tồn tại, course không còn published, course miễn phí/đã thanh toán và direct call.

## Q-19-03 — Chống đăng ký trùng, concurrency và 409

<a id="q-19-03"></a>

**Bằng chứng**

- AC-12 yêu cầu chống đăng ký trùng và catalog khai báo 409 DESIGN_STATE_CONFLICT.
- DB.sql không có unique constraint trên enrollments(user_id, course_id) hoặc lesson_progress(user_id, lesson_id).
- Enrollment.status có default ACTIVE trong DB.sql nhưng enum/status-selection policy chưa được đặc tả.

**Vấn đề**

- Chưa rõ status nào được tính là đã đăng ký, xử lý repeated request/parallel request ra sao, và 409 được tạo bằng check hay constraint.

**Ảnh hưởng**

- Không thể cam kết chống race hoặc chốt idempotency và 409 behavior từ source hiện có.

**Cần quyết định**

- Phê duyệt duplicate predicate, repeated-call behavior, concurrency guarantee và constraint/idempotency strategy nếu cần.

## Q-19-04 — Lesson set và giá trị khởi tạo Progress

<a id="q-19-04"></a>

**Bằng chứng**

- AC-12 ghi INIT Progress trong transaction nhưng không mô tả lesson selection.
- lesson_progress có lesson_id; DB_UNICA_ERD liên kết lessons với courses và lesson_progress.
- DB.sql có default NOT_STARTED và 0 cho status/progress_percent.

**Vấn đề**

- Chưa rõ tạo row cho mọi lesson, lesson đang published hay tập lesson khác; chưa rõ empty curriculum, initial fields và có dùng DB defaults không.

**Ảnh hưởng**

- Không thể xác định số lượng INSERT, query lesson set, hoặc giá trị khởi tạo mỗi cột.

**Cần quyết định**

- Cung cấp predicate/cardinality của lesson set, hành vi với course không có lesson và giá trị khởi tạo cho từng Progress field.

## Q-19-05 — Transaction boundary và lỗi giữa hai mutation

<a id="q-19-05"></a>

**Bằng chứng**

- AC-12 gọi bước “INSERT Enrollment + INIT Progress Transaction”.
- Study DB helper hiện không commit; caller/use-case chịu trách nhiệm transaction khi có module.
- API #19 chưa có runtime handler, query hoặc test.

**Vấn đề**

- AC xác nhận transaction intent nhưng chưa mô tả commit boundary, rollback response, xử lý lỗi một phần hoặc retry sau commit không rõ kết quả.

**Ảnh hưởng**

- Không thể chốt atomicity/rollback/idempotency guarantees cho client và database.

**Cần quyết định**

- Xác nhận hai mutation luôn cùng một transaction và policy khi mutation/commit lỗi hoặc client retry.

## Q-19-06 — Nullability và DDL defaults của hai bảng

<a id="q-19-06"></a>

**Bằng chứng**

- DB_UNICA_TABLES mô tả enrollments.user_id/course_id và lesson_progress.user_id/lesson_id là FK bắt buộc.
- Checked-in DB.sql khai báo FK nhưng không có NOT NULL cho bốn cột này.
- DB.sql đặt default cho enrollments.status và lesson_progress.status/progress_percent; API #19 không xác nhận use of defaults.

**Vấn đề**

- Tài liệu bảng và DDL không khớp nullability; không rõ nguồn nào được phê duyệt làm baseline cho mapping vật lý.

**Ảnh hưởng**

- Required-column mapping, constraint behavior và giá trị default chưa thể coi là schema runtime.

**Cần quyết định**

- Xác nhận baseline schema/DDL được duyệt và liệu endpoint phải cung cấp hay dựa vào từng default.

## Q-19-07 — EnrollmentStatus và timestamp mapping

<a id="q-19-07"></a>

**Bằng chứng**

- Enrollment schema có status:EnrollmentStatus, enrolled_at:date-time và completed_at optional.
- DB.sql khai báo status default ACTIVE, enrolled_at NOT NULL không default và completed_at nullable.
- Catalog/AC-12 không định nghĩa enum members hoặc nguồn timestamp.

**Vấn đề**

- Initial status, clock/timezone source, completed_at null/omit rule và enum values chưa được xác nhận.

**Ảnh hưởng**

- Không thể chốt insert values, response serialization hoặc status validation.

**Cần quyết định**

- Xác nhận EnrollmentStatus registry, initial state, enrolled_at source/precision và completed_at representation.

