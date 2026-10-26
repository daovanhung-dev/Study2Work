# Open Questions — API #28 Lấy metadata/câu hỏi được phép hiển thị

**Trạng thái DD:** Draft — Needs Confirmation
**Endpoint:** GET /api/v1/quizzes/{quiz_id}

Các câu hỏi dưới đây giữ lại những phần contract hoặc business rule chưa được nguồn chốt. DD giữ nguyên API catalog; không thêm field, table hoặc error code suy đoán.

<a id="q-28-01-student-quiz-state"></a>

## Q-28-01 — Quyền Student và trạng thái quiz

1. Quyền làm quiz dựa trên enrollment, trạng thái course, quyền riêng của quiz hay điều kiện nào khác?
2. Các giá trị nào của quizzes.status được xem là đang mở/được phép hiển thị?
3. API #28 phải kiểm tra entitlement và trạng thái mở, hay chỉ trả metadata/question set để client/API #29 xử lý?
4. Quiz tồn tại nhưng Student không có quyền hoặc quiz đang đóng trả 403, 404 hay response khác?

**Evidence:** API catalog yêu cầu Student Bearer. AC-16 precondition ghi Student có quyền làm quiz và quiz đang mở. DB design có quizzes.course_id/status nhưng không định nghĩa predicate hoặc enum values.

<a id="q-28-02-attempt-expiry-http-409"></a>

## Q-28-02 — Hạn lượt, hết hạn và lệch HTTP 409

1. Có giới hạn số attempt hoặc thời hạn làm quiz không? Nếu có, nguồn dữ liệu và cách tính là gì?
2. Nhánh “Hết lượt/hết hạn → 403/409” trong AC-16 thuộc API #28, API #29 tạo attempt hay cả hai?
3. API #28 có cần đọc quiz_attempts để xác định eligibility không?
4. Nếu cần HTTP 409, owner có duyệt thêm DESIGN_STATE_CONFLICT vào contract API #28 không?

**Evidence:** AC-16 activity diagram gắn nhánh không đủ điều kiện/hết lượt/hết hạn với 403/409 sau bước đọc Quiz/rules/question set. Catalog API #28 chỉ khai báo 401/403/404/500; API #29 mới có 409 DESIGN_STATE_CONFLICT. DD này giữ nguyên catalog cho API #28.

<a id="q-28-03-questiontype-quizchoice"></a>

## Q-28-03 — QuestionType và QuizChoice

1. Owner có duyệt vocabulary `SINGLE_CHOICE`, `MULTIPLE_CHOICE`, `TRUE_FALSE` và nullable `quiz_questions.question_type` từ API #88 migration 013 không? Đây là DERIVED local fallback.
2. QuizChoice fields/property nào sẽ được thêm vào catalog? API #88 locally chooses `{id,text,is_correct}` for Admin only.
3. Owner có duyệt `quiz_choices.sort_order` zero-based từ migration 013 không?
4. Field nào ngoài ID/text được phép Student nhìn thấy?

**Decision already applied:** API #28 response không trả quiz_choices.is_correct theo yêu cầu hiện tại. Câu hỏi này không đề xuất mở đáp án đúng trong response.

**Evidence:** API catalog định nghĩa QuizQuestion gồm id, text, type và choices: QuizChoice[], nhưng không có định nghĩa QuizChoice hoặc enum QuestionType. API #88 migration 013 adds local question_type/order columns; these do not establish owner-approved catalog shape or live deployment.

<a id="q-28-04-logical-physical-schema"></a>

## Q-28-04 — Field vật lý và logical schema

1. Có cần đưa quizzes.description vào Quiz response không? Logical Quiz hiện không có field này.
2. Có cần đưa quizzes.status, created_at, updated_at hoặc quiz_questions.score vào response không? Logical schemas hiện không khai báo các field đó.
3. Có phê duyệt aliases quizzes.name → Quiz.title và time_limit_minutes → duration_minutes không?
4. Quy tắc serialize nullable duration_minutes và decimal-string passing_score là gì?
5. DB table design xem các course/question/choice foreign keys là bắt buộc, còn checked-in DDL cho phép NULL. Nguồn nào là baseline vật lý và live schema có cần được xác minh trước khi triển khai?

**Evidence:** list_api.md khai báo logical Quiz/QuizQuestion. DB_UNICA_TABLES.md, DB ERD và checked-in DB.sql cho các field vật lý khác nhau. Live metadata chưa được xác nhận.

<a id="q-28-05-question-choice-order"></a>

## Q-28-05 — Thứ tự câu hỏi và lựa chọn

1. Có xác nhận trả câu hỏi theo quiz_questions.sort_order tăng dần không?
2. Nếu nhiều question có cùng sort_order, dùng tie-break nào?
3. quiz_choices có cần thứ tự hiển thị ổn định không? Nếu có, field/order rule là gì?

**Evidence:** DB design mô tả quiz_questions.sort_order là thứ tự câu hỏi trong quiz. Migration 013 adds choice sort_order for new local writes; historical rows use default 0 and their original order may be unavailable.

<a id="q-28-06-path-not-found-access"></a>

## Q-28-06 — Path, not-found và access mapping

1. quiz_id có yêu cầu giá trị dương hoặc range cụ thể không?
2. Path không parse được thành int64 trả HTTP/business code nào? Catalog API #28 không liệt kê 400 hoặc 422.
3. DESIGN_RESOURCE_NOT_FOUND áp dụng cho quiz không tồn tại hay còn dùng để che giấu quiz không được phép xem?

**Evidence:** Catalog chỉ ghi quiz_id:int64! và 404 DESIGN_RESOURCE_NOT_FOUND; không quy định min/max, parse-error mapping hoặc access masking.

---

Cần product/API owner chốt các câu hỏi ảnh hưởng tới contract, quyền truy cập và dữ liệu trước khi đổi DD sang trạng thái approved/final hoặc triển khai API.
