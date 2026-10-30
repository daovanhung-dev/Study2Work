# Open Questions — Study API #30 Autosave/lưu câu trả lời

**Trạng thái DD:** Draft — Needs Confirmation
**Endpoint:** PUT /api/v1/attempts/{attempt_id}/answers

Các câu hỏi dưới đây ghi lại những nội dung chưa được khóa bởi API catalog, AC-16, DB design/DDL hoặc current runtime. DD giữ nguyên contract nguồn và không chọn thay Product/API owner.

<a id="q-30-01-answer-contract"></a>

## Q-30-01 — Request answer field và answer representation

**Evidence:** API catalog ghi body question_id:int64! và answer(s):string!. Reusable schema QuizAnswer định nghĩa choice_ids?:int64[] và text_answer?:string; chưa xác định answer(s) có phải tên JSON field hay notation.

1. Tên JSON property thực tế là answer, answers, choice_ids, text_answer, hay tên khác?
2. Giá trị string mã hóa một choice ID, nhiều choice ID, text answer, hay một định dạng khác?
3. API #30 hỗ trợ loại câu hỏi nào và multiplicity đáp án nào?
4. Giới hạn độ dài, whitespace/empty behavior và validation values là gì?

**Impact:** Request shape, validation, persistence mapping và response answer projection.

<a id="q-30-02-storage-and-grading"></a>

## Q-30-02 — Physical answer storage và trường chấm điểm

**Evidence:** Logical QuizAnswer cho phép choice_ids hoặc text_answer. DB_UNICA_TABLES.md/ERD và checked-in DB.sql chỉ có một quiz_answers.choice_id, cùng is_correct và score_received; DDL khai báo is_correct NOT NULL. AC-16 đặt nộp bài và auto-grading sau API #30 tại API #31.

1. API #30 chỉ autosave lựa chọn hay còn phải hỗ trợ text/multi-select answer?
2. Nếu text/multi-select được hỗ trợ, nguồn schema nào lưu đủ các giá trị đó?
3. Giá trị is_correct nào được ghi trước khi API #31 chấm bài, hoặc có cần thay đổi schema/flow không?
4. score_received có được để default 0 đến API #31 không?
5. Baseline nullability nào là canonical: table design yêu cầu FK hay checked-in DDL cho phép nullable FK?
6. Có cần xác minh live schema trước khi chốt mapping không?

**Impact:** Candidate INSERT/UPDATE mapping, khả năng ghi answer trước khi chấm và compatibility với schema.

<a id="q-30-03-upsert-key-and-concurrency"></a>

## Q-30-03 — Upsert key, transaction và concurrent autosave

**Evidence:** AC-16 gọi bước này là UPSERT AttemptAnswer. ERD/DDL có quiz_answers.id là primary key nhưng không khai báo unique key cho (attempt_id, question_id).

1. Bản ghi answer được xác định để update bằng key nào?
2. Mỗi attempt/question chỉ có một row hay có thể có nhiều answer rows?
3. Nếu client gửi autosave lặp/đồng thời, cần bảo đảm kết quả nào?
4. Transaction, retry hoặc Idempotency-Key có được yêu cầu không?

**Impact:** Lookup condition, INSERT/UPDATE branch, unique constraint và rollback behavior.

<a id="q-30-04-attempt-access-and-state"></a>

## Q-30-04 — Quyền trên attempt và trạng thái cho phép autosave

**Evidence:** API catalog yêu cầu Student Bearer JWT; DB candidate quiz_attempts có user_id và status. Current auth helper ánh xạ JWT sub thành numeric user ID. AC-16 đặt autosave trước API #31 submit, nhưng không định nghĩa predicate ownership/status cho API #30.

1. API #30 có chỉ cho owner của attempt autosave không?
2. Attempt không thuộc user hiện tại trả 403 hay được mask thành 404?
3. Chỉ IN_PROGRESS được sửa hay có trạng thái/expiry khác được phép?
4. Attempt đã submit/expired trả mã nào? API #30 catalog hiện không liệt kê 409.
5. Có cần kiểm tra question_id thuộc quiz của attempt trước khi upsert không, và vi phạm trả 404 hay 422?

**Impact:** Authorization/query predicates, error mapping và bảo vệ answer của user khác.

<a id="q-30-05-response-shape-and-answer-disclosure"></a>

## Q-30-05 — Response QuizAttempt và dữ liệu answer được trả

**Evidence:** API catalog yêu cầu ApiEnvelope<QuizAttempt>. Logical QuizAttempt có answers:QuizAnswer[]; QuizAnswer có các field optional choice_ids, text_answer, correct và score. Contract không nói API #30 trả toàn bộ attempt hay chỉ answer vừa lưu.

1. Response trả attempt cùng tất cả answers, chỉ answer vừa lưu, hay một projection khác?
2. choice_ids/text_answer trong response theo representation nào?
3. API #30 có được trả correct hoặc score trước API #31 grading không?
4. submitted_at/score optional được omit hay trả null khi chưa submit/chấm?
5. AttemptStatus allowed values và status sau autosave là gì?

**Impact:** Response fields, mapping và không tiết lộ đáp án/chấm điểm ngoài policy.

<a id="q-30-06-messages-and-trace"></a>

## Q-30-06 — Message và trace metadata

**Evidence:** Shared API guideline định nghĩa ApiEnvelope với message, meta, traceId và error data=null; API catalog không định nghĩa message text hoặc field-error details cho API #30.

1. Message/localization key nào được dùng cho success và từng error?
2. Validation errors có field-level detail nào trong meta.fieldErrors?
3. Incoming X-Trace-Id optional/required semantics có cần ghi rõ trong API #30 không?

**Impact:** Response copy và request/response trace contract.

## Trạng thái cần duy trì

Cho đến khi các câu hỏi ảnh hưởng request shape, persistence, authorization và response được chốt, giữ DD ở Draft — Needs Confirmation; không sửa API catalog/diagram/DDL để tự giải quyết.

## Phụ thuộc AC-35 — quiz tombstone proposal

- API #30 ghi answer cho attempt đã tồn tại; AC-35 #90 giữ attempt/answer history khi soft-delete quiz có attempt.
- Đề xuất DERIVED: attempt IN_PROGRESS được tạo trước tombstone có thể tiếp tục autosave để không làm mất câu trả lời; owner cần xác nhận.
- Chưa chốt phối hợp transaction/lock giữa autosave và API #90; không thêm status/error behavior ngoài catalog.
- Câu hỏi liên quan: [API #90](../90_admin_quizzes_delete/OPEN_QUESTIONS.md) và [API #91](../91_admin_quizzes_statistics/OPEN_QUESTIONS.md).
