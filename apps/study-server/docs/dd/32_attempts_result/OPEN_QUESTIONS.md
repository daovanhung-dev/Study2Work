# Open Questions — Study API #32 Lấy điểm/kết quả được phép xem

**Trạng thái DD:** Draft — Needs Confirmation
**Endpoint:** GET /api/v1/attempts/{attempt_id}/result

Các câu hỏi dưới đây giữ lại những điều API catalog, AC-16 và DB design chưa chốt. DD không tự sửa contract nguồn.

<a id="q-32-01-attempt-ownership"></a>

## Q-32-01 — Attempt ownership và 403/404 policy

**Evidence:** API catalog yêu cầu Student Bearer JWT và chỉ nhận attempt_id. Current Study auth helper tạo numeric user_id từ JWT subject. Candidate quiz_attempts có user_id; API #32 chưa có route/query runtime.

1. Predicate sở hữu attempt nào được duyệt cho quiz_attempts.user_id?
2. Khi attempt tồn tại nhưng thuộc Student khác, trả 403 hay mask thành 404?
3. Có phân biệt attempt bị xóa/ẩn với attempt không thuộc user không?

**Impact:** Authorization predicate, error mapping và bảo mật việc dò attempt ID.

<a id="q-32-02-result-availability-and-pending-grade"></a>

## Q-32-02 — Thời điểm được đọc và PENDING_GRADE projection

**Evidence:** AC-16 đưa cả nhánh AUTO GRADED và PENDING GRADE tới API #32, rồi ghi hiển thị điểm hoặc trạng thái đang chờ. Catalog chỉ khai báo success 200 và errors 401/403/404/500.

1. API #32 chỉ đọc attempt đã submit hay cho phép attempt ở trạng thái khác?
2. Khi PENDING_GRADE, score được omit, null, partial hay trả theo một rule khác?
3. Result có thể trả 200 với status PENDING_GRADE trong mọi trường hợp manual grading chưa hoàn tất không?
4. Trạng thái nào khác ngoài GRADED/PENDING_GRADE có thể được đọc và các giá trị AttemptStatus chính thức là gì?

**Impact:** Access predicate, response projection và client display branch. Không thêm 409 hoặc 422 khi catalog chưa thay đổi.

<a id="q-32-03-answer-disclosure"></a>

## Q-32-03 — Tiết lộ đáp án và điểm từng câu

**Evidence:** Reusable QuizAnswer có optional correct và score; candidate quiz_answers có is_correct và score_received. API #28 DD loại answer key quiz_choices.is_correct khỏi quiz detail cho Student; API #32 là result endpoint nhưng disclosure policy chưa có.

1. Sau GRADED, API #32 có được trả đúng/sai của câu trả lời Student qua quiz_answers.is_correct không?
2. Có trả điểm từng câu qua score_received không?
3. Có trả lựa chọn Student đã gửi không?
4. Có thời điểm nào cho phép trả answer key từ quiz_choices.is_correct không?

**Impact:** Response schema, answer disclosure và bảo vệ nội dung kiểm tra. Cho tới khi có policy, DD không khẳng định các field correctness/score là được phép trả và không đưa answer key vào ví dụ.

<a id="q-32-04-feedback-field"></a>

## Q-32-04 — Feedback được nhắc trong AC-16

**Evidence:** AC-16 mô tả API #32 đọc score + feedback/status. QuizAttempt schema không có feedback; DB table map, ERD và checked-in DDL của quiz_attempts/quiz_answers cũng không khai báo feedback column.

1. Feedback thuộc cấp attempt hay từng answer?
2. Nguồn lưu trữ nào sở hữu feedback?
3. Có cần bổ sung field vào approved response contract/schema không?

**Impact:** API response contract, persistence mapping và tương thích client. DD không thêm field feedback.

<a id="q-32-05-answer-shape-and-order"></a>

## Q-32-05 — Hình dạng và thứ tự answer collection

**Evidence:** Logical QuizAnswer cho phép choice_ids hoặc text_answer; physical quiz_answers chỉ có một choice_id, không có text_answer column. Catalog yêu cầu QuizAttempt.answers[] nhưng không quy định thứ tự.

1. API #30 có hỗ trợ multi-select hoặc text answer; nếu có thì lưu ở đâu?
2. Một question tạo một hay nhiều quiz_answers rows trong cùng attempt?
3. Collection được sắp xếp theo question order, question_id hay rule nào khác?

**Impact:** Join/aggregation, response mapping và khả năng đọc lại nội dung đã autosave.

<a id="q-32-06-path-validation-and-errors"></a>

## Q-32-06 — Path validation và error mapping

**Evidence:** Catalog định nghĩa attempt_id:int64! nhưng API #32 error set không có 400/422.

1. attempt_id phải dương hay chỉ phải parse được int64?
2. Parse failure, overflow hoặc giá trị ngoài miền được ánh xạ thế nào?
3. Nếu framework runtime mặc định trả 422, canonical API catalog có được cập nhật để phản ánh không?

**Impact:** Request validation và tính nhất quán với error contract. DD giữ nguyên error set hiện có cho tới khi nguồn canonical thay đổi.

## Trạng thái cần duy trì

Giữ Draft — Needs Confirmation cho tới khi owner chốt quyền sở hữu, availability khi chờ chấm, disclosure, feedback và answer mapping. Không sửa API catalog, AC diagram, ERD hoặc DDL để tự giải quyết câu hỏi.
