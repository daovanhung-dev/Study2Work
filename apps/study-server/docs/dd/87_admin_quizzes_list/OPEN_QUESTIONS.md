# Câu hỏi còn mở — API #87 Lấy danh sách quiz

**Trạng thái DD:** Draft — Needs Confirmation
**Endpoint:** GET /api/v1/admin/quizzes
**Nhóm:** AC-35, API #87–#91

Các đề xuất trong DD đều được đánh dấu DERIVED. Runtime hiện triển khai các fallback được nêu dưới đây; catalog, diagram và schema chưa được sửa để biến chúng thành contract đã duyệt.

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

**Runtime fallback:** Trả `questions: []` và không query child tables. API #88 migration 013 now provides local question_type/choice-order candidates, but AC-35 list node says only “Query quizzes”; #87 keeps a metadata-only projection. Empty array does not assert that Quiz has no questions.

**Cần xác nhận:** #87 có trả questions/choices cho mọi quiz không, hay chỉ metadata và dùng endpoint detail khác?

## Q-87-04 — QuestionType và QuizChoice shape

**Evidence:** Catalog still does not define QuestionType values or QuizChoice fields. API #88 migration 013 adds a local nullable `question_type` and `quiz_choices.sort_order`; the API #88 DD chooses Admin choice `{id,text,is_correct}`. These remain DERIVED and are not owner-approved; pilot IDs/tables are not joined.

**Đề xuất:** Keep API #87 metadata-only; do not load nested child rows from the list route. Treat the #88 shape as a DERIVED Admin projection, and never expose `is_correct` to Student API #28.

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

**Evidence:** Catalog role Admin; runtime #87 dùng shared `ADMIN` guard. AC-35 còn yêu cầu quiz-management permission nhưng Study chưa có policy/claim mapping riêng.

**Cần xác nhận:** Admin claim/role source, permission policy và mapping 401 so với 403 là gì?

## Q-87-09 — Query validation và error mapping

**Evidence:** Catalog chỉ liệt kê 401/403/500. Runtime #87 parse raw query sau auth, trả 422 `DESIGN_VALIDATION_ERROR` cho course/page sai và đã có path trong `DESIGN_CONTRACT_PATHS`.

**Cần xác nhận:** Owner có chấp nhận 422 cho invalid int64/int32 không? Status hiện là exact string, không có enum validation.

## Q-87-10 — Error envelope

**Evidence:** API Guidelines yêu cầu data=null; current `error_response` trả null và API #87 focused tests xác nhận.

**Trạng thái:** Không còn mismatch ở current source. Cần giữ regression khi shared response helper thay đổi.

## Q-87-11 — Empty list và course không tồn tại

**Evidence:** Direct catalog response không mô tả collection; list có thể không có row; error set không có 404.

**Runtime fallback DERIVED:** Empty result trả HTTP 200 với Page `items=[]`; không trả 404 chỉ vì list rỗng. Course tồn tại được kiểm tra riêng không.

**Cần xác nhận:** course ID không có quiz trả empty list hay 404 sau khi response cardinality được sửa?

## Kết quả macro-review AC-35

- Review #87–#91 hoàn tất ở mức tài liệu: VERIFIED_WITH_OPEN_QUESTIONS.
- Tombstone được đề xuất ẩn mặc định; status filter không tự tạo giá trị DELETED khi enum chưa được duyệt.
- Contract trực tiếp ApiEnvelope<Quiz> vẫn khác list/page intent; review không đổi response type hoặc error set.
- Đề xuất lifecycle liên API và các câu hỏi owner xác nhận được tổng hợp tại [Verification Report nhóm AC-35](../91_admin_quizzes_statistics/VERIFICATION_REPORT.md).

## Ranh giới proposal

- DIRECT: endpoint, actor/auth type, query names/types, ApiEnvelope<Quiz>, HTTP 200 và errors 401/403/500.
- DERIVED/current local: shared ADMIN role fallback, ApiEnvelope<Page<Quiz>>, exact filters, page default/size/order, empty Page 200, metadata-only `questions=[]`, tombstone filtering and query 422.
- SOURCE_REQUIRED: active schema, dedicated Admin policy, QuizChoice/QuestionType, nested-list projection, query-422 approval và live query behavior.
- DISCREPANCY: response singleton so với list/page runtime; required nested schema so với metadata-only projection; local 422 ngoài catalog.

Cần chốt các câu hỏi ảnh hưởng contract, schema hoặc quyền truy cập trước khi đổi DD sang Approved/Final hoặc dùng làm implementation contract.
