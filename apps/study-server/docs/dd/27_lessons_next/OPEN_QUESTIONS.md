# Open Questions — API #27 Tìm bài tiếp theo

**Trạng thái DD:** Draft — Needs Confirmation
**Endpoint:** GET /api/v1/lessons/{lesson_id}/next

Các câu hỏi sau cần product/API owner xác nhận trước khi chốt thiết kế. Tài liệu hiện giữ contract đã có trong API catalog và không tự đặt SQL hoặc quy tắc chọn bài.

## Q-27-01 — Quyền truy cập và trạng thái publish

1. Student cần enrollment/quyền nào để gọi API? Có cần kiểm tra quyền ở course hay lesson?
2. API có chỉ trả lesson/course đã publish không? Trạng thái nào được xem là publish?
3. Khi lesson tồn tại nhưng Student không có quyền hoặc lesson chưa publish, trả 403 hay che giấu bằng 404?

**Evidence hiện có:** API catalog yêu cầu Bearer JWT và Student. AC-15 yêu cầu Student có quyền xem lesson; activity diagram có bước kiểm tra access/trạng thái publish trong luồng xem nội dung. Không có predicate, claim mapping hay masking rule dành riêng cho API #27.

<a id="q-27-02-curriculum-order-and-duplicates"></a>

## Q-27-02 — Thứ tự curriculum và lesson trùng thứ tự

1. Bài kế được chọn trong cùng course/curriculum nào?
2. sort_order tăng dần có phải quy tắc chọn bài không?
3. Nếu nhiều lesson có cùng sort_order, cần tie-break theo id hay tiêu chí khác?
4. Lesson draft/ẩn/archived có tham gia thứ tự hoặc bị bỏ qua không?

**Evidence hiện có:** AC-15 ghi bước “Đọc thứ tự curriculum”; DB design có lessons.course_id, lessons.sort_order, lessons.status. API #9 có ordering candidate nhưng chưa phải contract API #27.

<a id="q-27-03-current-lesson-and-no-next-result"></a>

## Q-27-03 — Lesson hiện tại không tồn tại và không có bài kế

1. Nếu lesson_id không tồn tại, trả 404 DESIGN_RESOURCE_NOT_FOUND hay mã khác?
2. Nếu lesson hiện tại tồn tại nhưng là bài cuối, trả 404, 200 với data: null, hay kết quả khác?
3. Có cần phân biệt hai trường hợp trên với lesson không được phép xem không?

**Evidence hiện có:** Catalog liệt kê 404 DESIGN_RESOURCE_NOT_FOUND; catalog không gắn mã này với một điều kiện cụ thể. Contract response là ApiEnvelope<Lesson>, chưa nêu nullability cho kết quả terminal.

## Q-27-04 — Lesson payload và schema dữ liệu

1. API #27 có trả đầy đủ logical Lesson gồm id, course_id, title, content?, video_url?, order và status không?
2. content hoặc video_url null thì serialize thành null hay omit?
3. Các giá trị hợp lệ của LessonStatus là gì và có khớp cột lessons.status không?
4. course_id có bắt buộc trong schema đang chạy? Logical Lesson/ERD xem là required, trong khi checked-in DDL cho phép NULL.
5. video_url có cần validate/chuẩn hóa trước khi ánh xạ thành URI không?

**Evidence hiện có:** API catalog khai báo ApiEnvelope<Lesson>; checked-in DB design/DDL cung cấp các cột candidate. Live schema và API #27 projection chưa được xác minh.

<a id="q-27-05-path-constraints"></a>

## Q-27-05 — Ràng buộc path và lỗi parse

1. lesson_id có phải số dương không, và giới hạn giá trị nào cần áp dụng?
2. Path không parse được thành int64 trả lỗi HTTP/business code nào? Catalog API #27 không liệt kê 400 hoặc 422.

**Evidence hiện có:** Catalog ghi lesson_id:int64!; chưa ghi min/max, positivity hoặc parse-error mapping.
