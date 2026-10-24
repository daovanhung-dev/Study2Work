# Câu hỏi còn mở — API #88 Tạo quiz mới

**Trạng thái DD:** Draft — Needs Confirmation
**Endpoint:** POST /api/v1/admin/quizzes
**Nhóm:** AC-35, API #87–#91

Nội dung ngoài contract trực tiếp được gắn DERIVED hoặc SOURCE_REQUIRED. Không dùng proposal làm runtime fact khi chưa được duyệt.

<a id="q-88-01-embedded-json"></a>
## Q-88-01 — JSON schema trong config và questions

**Evidence:** Catalog chỉ định config:string! và questions:string!; AC-35 không mô tả nested fields.

**Đề xuất DERIVED:** config là JSON object {course_id,title,duration_minutes?,passing_score}; questions là JSON array {text,type,choices[]}.

**Cần xác nhận:** Hai chuỗi có thực sự chứa JSON không? Có thể khai báo nested object/array trực tiếp trong catalog? Số question/choice tối thiểu là bao nhiêu?

<a id="q-88-02-questiontype"></a>
## Q-88-02 — QuestionType và persistence

**Evidence:** QuizQuestion yêu cầu type. Legacy quiz_questions không có type column. V1-PILOT có SINGLE_CHOICE/MULTIPLE_CHOICE/TRUE_FALSE nhưng gắn với assessment UUID.

**Đề xuất:** Dùng các giá trị pilot làm enum candidate để thảo luận; không coi là enum direct và không map pilot row sang legacy Quiz ID.

**Cần xác nhận:** Enum values nào được duyệt? Schema BIGINT nào lưu type? Có migration/schema source nào được phê duyệt?

<a id="q-88-03-quizchoice"></a>
## Q-88-03 — QuizChoice input/output và answer key

**Evidence:** QuizChoice không có logical definition. Legacy choices có choice_text/is_correct; pilot options có label_markdown/is_correct. API #28 không trả is_correct cho Student.

**Đề xuất DERIVED cho create input:** choices[] gồm text:string và is_correct:boolean. Không trả is_correct trong Quiz response mặc định khi output schema chưa định nghĩa.

**Cần xác nhận:** API #88 có được nhận is_correct không? Admin response có cần trả answer key không? QuizChoice output object gồm field nào?

<a id="q-88-04-validation-scoring"></a>
## Q-88-04 — Validation question, đáp án và điểm

**Evidence:** Legacy question score default 1, choice is_correct default false. Pilot spec yêu cầu đáp án đúng khi publish nhưng dùng schema khác.

**Cần xác nhận:** Mỗi question phải có ít nhất một đáp án đúng không? SINGLE/MULTIPLE/TRUE_FALSE giới hạn đáp án thế nào? Có score input hay luôn dùng default? Passing score có range/scale nào?

<a id="q-88-05-physical-model"></a>
## Q-88-05 — Schema vật lý và live database

**Evidence:** Legacy quiz/question/choice BIGINT nhưng thiếu type; V1-PILOT assessment/question/option UUID. Live schema chưa xác minh.

**Đề xuất:** Dùng legacy chỉ làm candidate theo API int64; không ghép table/ID giữa hai model.

**Cần xác nhận:** Model nào là baseline của APIs #87–#91? Live metadata nào xác nhận PK/FK/nullability/default/index?

<a id="q-88-06-course-access"></a>
## Q-88-06 — Course reference và quyền Admin

**Evidence:** course_id chỉ có trong config proposal; AC-35 yêu cầu quiz-management permission; Admin guard chưa có trong Study.

**Đề xuất DERIVED:** Kiểm tra courses.id; ID không tồn tại trả 422 vì contract không có 404. Không lọc status/owner khi chưa có rule.

**Cần xác nhận:** Course phải ở trạng thái nào? Admin permission claim/policy ra sao? Chấp nhận 422 khi course không tồn tại không?

<a id="q-88-07-status-lifecycle"></a>
## Q-88-07 — Quiz status và khả năng làm bài

**Evidence:** Legacy DDL default DRAFT; body/Quiz response không có status. AC-16 yêu cầu quiz đang mở; AC-35 chưa có API status riêng.

**Cần xác nhận:** Quiz chuyển khỏi DRAFT bằng cách nào? API #89 có status semantics không? Có publication flow ngoài #87–#91 không?

<a id="q-88-08-ordering"></a>
## Q-88-08 — Thứ tự question và choice

**Evidence:** Legacy quiz_questions có sort_order; quiz_choices không có order column.

**Đề xuất DERIVED:** Lấy index của questions array làm sort_order zero-based. Không tuyên bố lưu bền vững order của choices.

**Cần xác nhận:** Choice order có cần ổn định sau lần create không? Nếu có, field nào được duyệt?

<a id="q-88-09-error-envelope"></a>
## Q-88-09 — Error mapping và envelope

**Evidence:** Catalog có 401/403/422/500. Path ngoài middleware allowlist; current helper serialize data=None thành {}.

**Cần xác nhận:** Khi wire route, update allowlist và đảm bảo error data=null thế nào? Course-not-found→422 proposal có được duyệt không?

<a id="q-88-10-ac35-macro"></a>
## Q-88-10 — Tính nhất quán nhóm #87–#91

**Evidence:** #87 list intent nhưng response direct Quiz; #89 catalog chỉ có path, diagram ghi update quiz/question set; #90 phụ thuộc attempts; #91 dùng Quiz contract.

**Đề xuất:** Giữ direct contract API #88; không tự sửa body/list/delete/stats contract API khác.

**Kết quả macro-review:** Review #87–#91 đã hoàn tất ở mức tài liệu với trạng thái VERIFIED_WITH_OPEN_QUESTIONS.

**Cần owner xác nhận:** #87 cardinality; body/replacement của #89; tombstone và attempt history của #90; response statistics của #91; QuestionType/QuizChoice; lifecycle DRAFT → mở.

## Ranh giới proposal

- DIRECT: POST/path, Admin Bearer role, body names/types, ApiEnvelope<Quiz>, HTTP 201, DESIGN_RESOURCE_CREATED, errors 401/403/422/500.
- DERIVED: embedded JSON shape, choice create fields, course existence→422, atomic transaction và question ordering.
- SOURCE_REQUIRED: live DB, Admin policy, QuestionType/QuizChoice, correct-answer rules, choice order và lifecycle.
- DISCREPANCY: logical type so với legacy table; BIGINT API model so với UUID pilot; current error helper so với guidelines.

Cần chốt câu hỏi ảnh hưởng contract, schema hoặc quyền trước khi DD được Approved/Final hoặc dùng làm implementation contract.
