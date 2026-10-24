# Câu hỏi còn mở — API #89 Cập nhật quiz

**Trạng thái DD:** Draft — Needs Confirmation
**Endpoint:** PUT /api/v1/admin/quizzes/{quiz_id}
**Nhóm:** AC-35, API #87–#91

Catalog contract được giữ nguyên. Body và persistence proposal chưa phải quyết định đã duyệt.

<a id="q-89-01-request-body"></a>
## Q-89-01 — Request body của PUT

**Evidence:** Catalog #89 chỉ khai báo path quiz_id:int64!; AC-35 mô tả “UPDATE quiz/question set”; API #88 nhận config:string! và questions:string!.

**Đề xuất DERIVED:** Reuse cùng hai string fields và nested JSON shape của #88 để update metadata/question set.

**Cần xác nhận:** API #89 có nhận body không? Nếu có, fields/types có giống #88 không? Có được đổi course qua config.course_id không?

<a id="q-89-02-put-semantics"></a>
## Q-89-02 — PUT full replacement hay partial update

**Evidence:** HTTP method PUT; request schema không có trong catalog/diagram; body candidate của #88 không có nested question/choice IDs.

**Đề xuất DERIVED:** config và questions là full replacement; thiếu required field thì 422 theo catalog.

**Cần xác nhận:** Field omit giữ giá trị cũ hay bị xóa/reset? duration_minutes null/omit nghĩa là gì? questions rỗng có được phép xóa toàn bộ không?

<a id="q-89-03-attempt-history"></a>
## Q-89-03 — Attempts, answers và lịch sử câu hỏi

**Evidence:** Legacy quiz_attempts.quiz_id gắn với Quiz; quiz_answers.question_id/choice_id tham chiếu question/choice; AC-35 #90 ghi soft delete nếu đã có attempts. Legacy model không có version cho question set.

**Đề xuất DERIVED:** Không thay child IDs khi có attempt/answer history; candidate trả 422 DESIGN_VALIDATION_ERROR trước mọi write.

**Cần xác nhận:** Có cấm update cả metadata và questions sau attempt không? Cần versioning/snapshot hay tạo Quiz version mới? API #29/#30 có cần khóa cùng Quiz khi tạo attempt/answer để tránh race?

<a id="q-89-04-question-type-and-choice"></a>
## Q-89-04 — QuestionType, QuizChoice và ordering

**Evidence:** QuizQuestion response yêu cầu type; legacy quiz_questions không có type; legacy quiz_choices không có order; QuizChoice chưa có logical schema.

**Cần xác nhận:** Enum/type lưu ở đâu? QuizChoice có field nào? Có trả is_correct cho Admin không? Choice order được lưu/khôi phục thế nào?

<a id="q-89-05-validation-and-course"></a>
## Q-89-05 — Validation và thay course

**Evidence:** Proposed config có course_id/title/duration/passing_score; legacy DDL có VARCHAR(200), NUMERIC(5,2) và nullable course FK, contract không có limits.

**Cần xác nhận:** Có cho chuyển quiz sang course khác không? Course phải tồn tại/trạng thái gì? Title, passing_score, duration có range/precision nào?

<a id="q-89-06-admin-permission"></a>
## Q-89-06 — Admin permission

**Evidence:** Catalog role=Admin; AC-35 yêu cầu quiz-management permission; current helper chỉ xác minh Student.

**Cần xác nhận:** Admin role/permission claim và policy scope nào sẽ được dùng? 401/403 mapping có giữ catalog không?

<a id="q-89-07-physical-schema"></a>
## Q-89-07 — Physical model và live schema

**Evidence:** Legacy BIGINT quizzes/questions/choices có fields candidate nhưng thiếu QuestionType/order; V1-PILOT dùng UUID assessment/question/options; live DB chưa xác minh.

**Cần xác nhận:** Model nào là baseline API #87–#91? Live metadata nào xác nhận table/FK/nullability/default/cascade?

<a id="q-89-08-errors-envelope"></a>
## Q-89-08 — Error mapping và envelope

**Evidence:** Direct errors 401/403/404/422/500; path chưa có middleware allowlist; API Guidelines yêu cầu data=null nhưng current helper serialize {}.

**Cần xác nhận:** Khi wire dynamic path, middleware map đủ catalog codes thế nào? Error data chuẩn null hay object rỗng?

<a id="q-89-09-concurrency"></a>
## Q-89-09 — Đồng thời update và tạo attempt

**Evidence:** Full replacement có thể xóa question/choice IDs trong khi APIs #29–#31 tạo attempt/answers; current source không có quiz Admin hoặc attempt runtime được xác minh.

**Đề xuất:** Cần transaction/locking hoặc versioning coordination giữa #89 và #29/#30 trước triển khai.

**Cần xác nhận:** Isolation/row lock nào được dùng và bên nào lấy cùng lock? Có row_version/optimistic concurrency không?

<a id="q-89-10-ac35-macro"></a>
## Q-89-10 — Tính nhất quán nhóm #87–#91

**Evidence:** #87 có list/cardinality mismatch; #88 body/schema proposals; #90 delete phụ thuộc attempts; #91 hiện đã có statistics DD nhưng response shape còn conflict.

**Kết quả macro-review:** Review tài liệu #87–#91 hoàn tất với trạng thái VERIFIED_WITH_OPEN_QUESTIONS. Đề xuất DERIVED là #89 từ chối update quiz có attempt/answer history hoặc tombstone; #90 giữ lịch sử khi soft-delete; #29 chặn attempt mới; #30–#32 bảo toàn attempt đã tạo; #91 đọc aggregate trên history còn lưu.

**Cần owner xác nhận:** Request body/replacement, Quiz status/tombstone, attempt-in-progress policy, error envelope, QuestionType/QuizChoice, response projection và schema vật lý. Xem [Verification Report nhóm AC-35](../91_admin_quizzes_statistics/VERIFICATION_REPORT.md).

## Ranh giới proposal

- DIRECT: PUT/path/auth role/response/success/error codes.
- DERIVED: config/questions body, full child replacement, 404 mapping, history guard 422, atomic transaction và question order candidate.
- SOURCE_REQUIRED: Admin permission, live schema, QuestionType/QuizChoice, attempt/version policy, course move và field validation.
- DISCREPANCY: catalog path-only so với diagram update set; logical QuizQuestion so với legacy persistence.

Cần chốt body, persistence, attempt history và security policy trước khi DD được Approved/Final hoặc dùng làm implementation contract.
