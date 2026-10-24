# Open Questions — Study API #31 Khóa attempt và bắt đầu chấm

**Trạng thái DD:** Draft — Needs Confirmation
**Endpoint:** POST /api/v1/attempts/{attempt_id}/submit

Các câu hỏi dưới đây giữ lại nội dung chưa được API catalog, AC-16 hoặc DB design/DDL chốt. DD không tự sửa contract nguồn.

<a id="q-31-01-attempt-ownership"></a>

## Q-31-01 — Attempt ownership và access masking

**Evidence:** API catalog yêu cầu Student Bearer JWT và nhận attempt_id trên path. Candidate quiz_attempts có user_id; AC-16 không mô tả predicate sở hữu attempt.

1. Identity nào trong auth context được ánh xạ sang quiz_attempts.user_id?
2. Attempt của Student khác trả 403 hay được mask thành 404?
3. Có cần kiểm tra enrollment/quiz access lại khi submit không?

**Impact:** Authorization query, error mapping và khả năng đọc/nộp attempt của user khác.

<a id="q-31-02-attempt-state-and-repeat-submit"></a>

## Q-31-02 — Trạng thái attempt, submit lặp và concurrency

**Evidence:** AC-16 ghi UPDATE Attempt = SUBMITTED; API catalog có 409 DESIGN_STATE_CONFLICT. Checked-in DB.sql định nghĩa status VARCHAR(20) DEFAULT IN_PROGRESS nhưng không canonical hóa enum.

1. Những trạng thái nào được submit và trạng thái nào phải bị từ chối?
2. Submit attempt đã SUBMITTED/GRADED/PENDING_GRADE lần nữa trả kết quả idempotent hay 409?
3. Hết hạn được xử lý ở API #31 thế nào và có thuộc 403 hay 409?
4. Cần row lock/conditional update hoặc cơ chế chống submit đồng thời nào?
5. Transaction boundary, rollback và retry behavior là gì?

**Impact:** WHERE predicate, state transition, status code và consistency giữa answer grading với attempt update.

<a id="q-31-03-grading-rules"></a>

## Q-31-03 — Thuật toán chấm tự động và câu chấm tay

**Evidence:** AC-16 ghi tính điểm auto và decision “Có câu cần chấm tay?”; YES → PENDING_GRADE, NO → GRADED. DB design có quiz_questions.score, quiz_choices.is_correct, quiz_answers.is_correct, score_received và quiz_attempts.score nhưng không ghi công thức.

1. Question type nào được chấm tự động và field/rule nào nhận diện câu cần chấm tay?
2. Choice answer được so sánh theo quy tắc nào; câu không trả lời hoặc nhiều lựa chọn được tính ra sao?
3. Điểm câu và điểm tổng được tính, scale, làm tròn và áp dụng passing_score như thế nào?
4. Nếu attempt có câu tự động và câu chấm tay, có lưu partial score trước khi chuyển PENDING_GRADE không?
5. Trạng thái GRADED được gán khi nào nếu có câu chấm tay?

**Impact:** Giá trị update is_correct/score_received/attempt.score và trạng thái cuối cùng.

<a id="q-31-04-answer-storage-discrepancy"></a>

## Q-31-04 — Tương thích answer contract và physical schema

**Evidence:** Logical QuizAnswer cho phép choice_ids hoặc text_answer. DB table design/ERD lưu một choice_id cho mỗi row và không có text-answer column. Checked-in DB.sql khai báo quiz_answers.is_correct NOT NULL; API #30 chưa có nguồn định nghĩa giá trị correctness trước submit.

1. API #30 chỉ hỗ trợ choice hay cả multi-select/text answer? Nguồn schema nào lưu các dạng đó?
2. is_correct của answer chưa được chấm lưu giá trị nào trước API #31?
3. Có thay đổi schema được duyệt để biểu diễn câu trả lời chưa chấm hoặc text/multi-select không?
4. Một question có nhiều row quiz_answers hay một row? DDL không khai báo unique key cho attempt_id + question_id.
5. Có cần xác minh live schema trước khi chốt mapping không?

**Impact:** Khả năng đọc answer, update grading result và lưu trạng thái chưa chấm mà không suy diễn schema.

<a id="q-31-05-response-projection"></a>

## Q-31-05 — QuizAttempt response và disclosure

**Evidence:** API #31 trả ApiEnvelope<QuizAttempt>. Schema QuizAttempt yêu cầu answers[] và có optional submitted_at/score; QuizAnswer có optional choice_ids, text_answer, correct, score. AC-16 chỉ nêu kết quả/trạng thái chấm được trả về ở flow sau API #32.

1. API #31 response trả full answer set hay chỉ attempt summary?
2. Khi status là PENDING_GRADE, score/correct/score_received được omit, null hay trả partial?
3. API #31 có được phép trả đáp án đúng ngay sau khi submit hay chỉ API #32 sau policy kiểm tra?
4. Optional fields nên omit hay trả null?
5. Message, fieldErrors và trace metadata cụ thể có quy ước nào ngoài shared envelope?

**Impact:** Response mapping, answer disclosure và client compatibility.

<a id="q-31-06-timestamp-and-error-mapping"></a>

## Q-31-06 — Timestamp, validation và trigger-to-code mapping

**Evidence:** API catalog khai báo attempt_id:int64! và lỗi 422; quiz_attempts có submitted_at TIMESTAMP nullable. Catalog liệt kê 403, 404, 409 nhưng không gán từng predicate.

1. attempt_id cần dương/range cụ thể nào; parse failure/overflow có ánh xạ 422 ra sao?
2. Timestamp lấy từ clock nào, timezone/precision nào và xử lý retry ra sao?
3. Điều kiện cụ thể nào trả 403, 404 và 409?
4. Lỗi khi grading đã ghi một phần được rollback thế nào?

**Impact:** Request validation, timestamp consistency và error/transaction behavior.

## Trạng thái cần duy trì

Giữ Draft — Needs Confirmation đến khi owner chốt ownership/state, grading rules, answer storage compatibility và response disclosure. Không sửa API catalog, AC diagram, ERD hoặc DDL để tự giải quyết các câu hỏi này.

## Phụ thuộc AC-35 — quiz tombstone proposal

- API #31 nộp attempt đã tồn tại; AC-35 #90 giữ attempt/answer history khi soft-delete quiz có attempt.
- Đề xuất DERIVED: attempt IN_PROGRESS được tạo trước tombstone có thể tiếp tục submit/chấm theo AC-16; owner cần xác nhận.
- Chưa chốt race với DELETE, lock/isolation hoặc cách xử lý khi quiz bị tombstone trong lúc submit.
- Câu hỏi liên quan: [API #90](../90_admin_quizzes_delete/OPEN_QUESTIONS.md) và [API #91](../91_admin_quizzes_statistics/OPEN_QUESTIONS.md).
