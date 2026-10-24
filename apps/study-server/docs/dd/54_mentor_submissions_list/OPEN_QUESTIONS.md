# Open Questions — Study API #54 Lấy submissions

**Trạng thái DD:** Draft — Needs Confirmation
**Endpoint:** GET /api/v1/mentor/submissions

Các câu hỏi dưới đây ảnh hưởng response contract, phân trang, quyền truy cập hoặc khả năng map Submission. DD giữ nguyên catalog và không tự chọn câu trả lời.

## Q-54-01 — Cardinality và empty-result response

**Bằng chứng**

- Catalog và AC-23 đặt tên API là lấy submissions/đọc submissions.
- API catalog khai báo ApiEnvelope<Submission>, là một object.
- AC-23 chuyển từ danh sách sang chọn một submission rồi gọi API #55.

**Cần xác nhận**

1. data là một Submission, Submission[] hay Page<Submission>?
2. Nếu là collection, array/pagination metadata nằm ở đâu và có tương thích ngược không?
3. Khi không có submissions, trả collection rỗng hay một trạng thái khác?

**Ảnh hưởng:** Response schema, ví dụ JSON, empty state và API client.

## Q-54-02 — Pagination, ordering và query validation

**Bằng chứng**

- Request có page?:int32.
- Không có size, default, min/max, sort, count hoặc PageMeta trong API contract.
- Error catalog không có 422.

**Cần xác nhận**

1. Page bắt đầu từ 0 hay 1; giá trị mặc định và phạm vi là gì?
2. Page size cố định hay cần query size; có stable order và total count không?
3. Query sai kiểu/ngoài phạm vi trả business code nào khi API không khai báo 422?

**Ảnh hưởng:** Query contract, error mapping, response metadata và giới hạn tải.

## Q-54-03 — Status filter

**Bằng chứng**

- Query status là string tùy chọn.
- Reusable Submission dùng SubmissionStatus nhưng không liệt kê enum.
- AC-17 đặt trạng thái ban đầu là SUBMITTED; AC-23 ghi grading cập nhật status thành GRADED.

**Cần xác nhận**

1. Danh sách đầy đủ status nào được lọc?
2. Blank value, casing và status không hợp lệ được xử lý thế nào?
3. Có status nào bị ẩn khỏi danh sách chấm không?

**Ảnh hưởng:** Validation, filter predicate và trạng thái hiển thị.

## Q-54-04 — Mentor identity và course authorization

**Bằng chứng**

- AC-23 yêu cầu Mentor có quyền chấm submissions của course.
- course_id tùy chọn nên API cần quy tắc phạm vi khi field này vắng mặt.
- Study auth helper hiện có Student guard; không có Mentor identity/assignment mapping.
- Candidate courses.mentor_id chỉ mô tả direct owner, không xác nhận assigned Mentors.

**Cần xác nhận**

1. Mentor identity lấy từ JWT claim nào và map sang users.id thế nào?
2. Quyền dựa trên direct ownership, assignment hay quan hệ khác?
3. Khi không truyền course_id, trả submissions của tất cả courses được phép chấm hay yêu cầu chọn course?
4. Course tồn tại nhưng không thuộc quyền Mentor trả 403 hay được mask?

**Ảnh hưởng:** Authorization và dữ liệu có thể lộ giữa courses.

## Q-54-05 — Persistence và mapping của Submission.files

**Bằng chứng**

- Logical Submission.files là UploadAsset[].
- Candidate assignment_submissions có một file_url nullable.
- Không có source được duyệt cho asset ID, tên, content type, size, status hoặc association.

**Cần xác nhận**

1. UploadAsset được lưu ở đâu và liên kết với submission bằng khóa nào?
2. URL là public hay signed; API #54 có trả file_url hay resolve asset metadata?
3. File list có thể rỗng không và thứ tự của files là gì?

**Ảnh hưởng:** Response projection, storage access và data model.

## Q-54-06 — Ý nghĩa của 409

**Bằng chứng**

- Catalog khai báo 409 DESIGN_STATE_CONFLICT.
- AC-23 không có nhánh conflict cho API GET danh sách.

**Cần xác nhận**

1. Điều kiện nào của API #54 tạo state conflict?
2. 409 có thuộc endpoint này hay là lỗi sót trong catalog?

**Ảnh hưởng:** Error contract và test cases; không suy ra từ empty result/status filter.

## Q-54-07 — Baseline schema và nullability

**Bằng chứng**

- ERD/table guide cho quan hệ assignment và course là required.
- Checked-in V1-PILOT DDL cho phép NULL ở assignment_submissions.assignment_id, assignment_submissions.user_id và assignments.course_id.
- Live schema chưa được xác minh.

**Cần xác nhận**

1. Schema artifact nào là baseline cho API #54?
2. Null/orphan relation được xử lý ra sao nếu DDL hiện hành vẫn cho phép?
3. Live schema cần được xác minh trước khi chuyển DD sang implementation-ready?

**Ảnh hưởng:** Joins, completeness, authorization scope và deployment readiness.

## Q-54-08 — Error envelope data

**Bằng chứng**

- API Guidelines yêu cầu data: null ở error response.
- Current error_response() chuyển data=None thành {}.
- API #54 chưa có route để xác nhận behavior.

**Cần xác nhận**

1. Endpoint mới phải giữ {} theo helper hiện tại hay thay đổi helper/convention để trả null?

**Ảnh hưởng:** Contract conformance và error examples.

## Trạng thái cần duy trì

Giữ Draft — Needs Confirmation tới khi cardinality, pagination, status, quyền Mentor và asset mapping được quyết định. Macro-review AC-23 #54–#57 đã hoàn tất ở mức tài liệu; các câu hỏi contract/source nêu trên vẫn mở.
