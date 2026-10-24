# Câu hỏi còn mở — API #87 Lấy danh sách quiz

**Trạng thái DD:** Draft — Needs Confirmation
**Endpoint:** GET /api/v1/admin/quizzes
**Nhóm:** AC-35, API #87–#91

Các đề xuất trong DD đều được đánh dấu DERIVED. Catalog và runtime không được sửa để lấp các câu hỏi dưới đây.

## Q-87-01 — Cardinality của response list

**Evidence:** API #87 đặt tên “Lấy danh sách quiz”, AC-35 diagram có bước “Query quizzes”, và request có page. Catalog lại khai báo ApiEnvelope<Quiz>.

**Đề xuất:** Dùng ApiEnvelope<Page<Quiz>> vì catalog đã có reusable Page<T> và request có page. Giữ response hiện tại trong DD là direct contract cho tới khi owner duyệt.

**Cần xác nhận:** data là Quiz đơn, Quiz[], hay Page<Quiz>? Nếu Page, có chấp nhận items/pagination theo reusable PageMeta không?

## Q-87-02 — Quy tắc page, size và thứ tự

**Evidence:** Catalog có page?:int32 nhưng không có default, size, sort, total hoặc order. API #07 dùng page mặc định 1 và fixed size 20; #82 không có pagination.

**Đề xuất DERIVED:** page bắt đầu từ 1, vắng mặt mặc định 1; fixed size 20; quizzes.id ASC làm thứ tự ổn định.

**Cần xác nhận:** Có chấp nhận các default này không? Có cần total/total_pages không?

## Q-87-03 — Nested questions trong list

**Evidence:** Reusable Quiz yêu cầu questions:QuizQuestion[], nhưng AC-35 activity diagram chỉ nêu “Query quizzes”. API #28 detail đọc quiz, questions và choices.

**Đề xuất:** Nếu giữ Quiz response schema, đọc nested data theo batch cho các quiz trên trang; nếu đây là list nhẹ, sửa response contract thành summary type riêng trước khi implement.

**Cần xác nhận:** #87 có trả questions/choices cho mọi quiz không, hay chỉ metadata và dùng endpoint detail khác?

## Q-87-04 — QuestionType và QuizChoice shape

**Evidence:** QuizQuestion yêu cầu type và choices; catalog không định nghĩa enum QuestionType hoặc schema QuizChoice. Legacy quiz_questions không có type column; legacy quiz_choices có id, question_id, choice_text, is_correct. Pilot question_type thuộc schema UUID khác.

**Đề xuất:** Không đưa is_correct hoặc field mới vào response cho tới khi QuizChoice contract được định nghĩa. Không map pilot question_type sang legacy quiz ID.

**Cần xác nhận:** QuizChoice có những property nào, có trả is_correct cho Admin không, và thứ tự choices lấy từ đâu?

## Q-87-05 — Physical model và live schema

**Evidence:** Legacy DB.sql có quizzes BIGSERIAL/quiz_choices; V1-PILOT có UUID assessments/quiz_options. DB context nói live schema chưa xác minh.

**Đề xuất:** Legacy tables chỉ làm mapping candidate vì API contract dùng int64; không tuyên bố đây là schema runtime.

**Cần xác nhận:** Model nào là baseline triển khai cho Study Admin quiz APIs #87–#91? Live metadata nào xác nhận table/column/FK/index/nullability?

## Q-87-06 — Course/status filters

**Evidence:** Catalog khai báo course?:int64 và status?:string; legacy DDL có course_id/status nhưng status enum chưa định nghĩa đầy đủ.

**Đề xuất DERIVED:** Exact equality; không trim/case-normalize status; vắng filter thì không thêm predicate; không đặt status mặc định.

**Cần xác nhận:** course có phải yêu cầu course tồn tại không? Status values/casing hợp lệ là gì? Filter status có bao gồm quiz đã xóa/ẩn nếu policy xuất hiện ở API #90 không?

## Q-87-07 — Nullability và projection

**Evidence:** Legacy quizzes.course_id cho phép NULL trong DDL nhưng Quiz.course_id là required; Quiz schema không gồm status, description, created_at, updated_at.

**Đề xuất:** Không trả field ngoài logical Quiz; giữ mismatch course_id nullability rõ ràng.

**Cần xác nhận:** Row course_id NULL cần sửa dữ liệu, loại khỏi kết quả hay trả lỗi? duration_minutes null được trả null hay omit?

## Q-87-08 — Admin authentication/authorization

**Evidence:** Catalog role Admin; AC-35 yêu cầu quiz-management permission; current Study helper chỉ kiểm tra Student và không có route Admin.

**Cần xác nhận:** Admin claim/role source, permission policy và mapping 401 so với 403 là gì?

## Q-87-09 — Query validation và error mapping

**Evidence:** Catalog chỉ liệt kê 401/403/500; invalid course/page thường đi qua FastAPI request validation. Middleware hiện không có /api/v1/admin/quizzes trong DESIGN_CONTRACT_PATHS.

**Đề xuất:** Không thêm 400/422 vào direct error table; giữ discrepancy giữa catalog và future integration.

**Cần xác nhận:** Invalid int64/int32/status trả code nào? Khi route được wire, có đưa path vào DESIGN_CONTRACT_PATHS để giữ DESIGN_INTERNAL_ERROR mapping không?

## Q-87-10 — Error envelope

**Evidence:** API Guidelines yêu cầu data=null; current error_response thay data=None bằng {} khi serialize.

**Cần xác nhận:** Runtime helper hay guideline là chuẩn bắt buộc khi endpoint Admin được implement?

## Q-87-11 — Empty list và course không tồn tại

**Evidence:** Direct catalog response không mô tả collection; list có thể không có row; error set không có 404.

**Đề xuất DERIVED:** Nếu collection contract được duyệt, empty result trả HTTP 200 với items=[]; không trả 404 chỉ vì list rỗng.

**Cần xác nhận:** course ID không có quiz trả empty list hay 404 sau khi response cardinality được sửa?

## Kết quả macro-review AC-35

- Review #87–#91 hoàn tất ở mức tài liệu: VERIFIED_WITH_OPEN_QUESTIONS.
- Tombstone được đề xuất ẩn mặc định; status filter không tự tạo giá trị DELETED khi enum chưa được duyệt.
- Contract trực tiếp ApiEnvelope<Quiz> vẫn khác list/page intent; review không đổi response type hoặc error set.
- Đề xuất lifecycle liên API và các câu hỏi owner xác nhận được tổng hợp tại [Verification Report nhóm AC-35](../91_admin_quizzes_statistics/VERIFICATION_REPORT.md).

## Ranh giới proposal

- DIRECT: endpoint, actor/auth type, query names/types, ApiEnvelope<Quiz>, HTTP 200 và errors 401/403/500.
- DERIVED: exact filters, page default, fixed page size, stable ordering và empty collection.
- SOURCE_REQUIRED: active schema, Admin policy, QuizChoice/QuestionType, nested-list projection, parse errors và live query behavior.
- DISCREPANCY: response singleton so với list/page semantics; error envelope guideline so với current helper.

Cần chốt các câu hỏi ảnh hưởng contract, schema hoặc quyền truy cập trước khi đổi DD sang Approved/Final hoặc dùng làm implementation contract.
