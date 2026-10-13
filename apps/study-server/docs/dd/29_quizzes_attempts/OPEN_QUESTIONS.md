# Open Questions — API #29 Tạo attempt

**Trạng thái DD:** Draft — Needs Confirmation
**Endpoint:** POST /api/v1/quizzes/{quiz_id}/attempts

Các câu hỏi giữ lại những business rule, error mapping và response details mà API catalog, AC-16 và schema chưa chốt. DD không tự sửa contract nguồn.

<a id="q-29-01-eligibility-owner"></a>

## Q-29-01 — Eligibility thuộc API #28 hay API #29?

**Evidence:** AC-16 đặt bước đọc Quiz/rules/question set qua API #28, tiếp theo là decision “Được phép làm bài?” rồi mới gọi API #29. API catalog yêu cầu Student có Bearer JWT; AC-16 precondition yêu cầu Student có quyền làm quiz và quiz đang mở.

1. API #28 chỉ trả metadata/question set, còn API #29 có trách nhiệm kiểm tra eligibility trước khi tạo attempt?
2. Hay API #28 kiểm tra eligibility, và API #29 chỉ kiểm tra lại các điều kiện tối thiểu trước khi insert?
3. Điều kiện nào xác định Student có quyền làm quiz: enrollment, course status, quiz assignment hay rule khác?
4. Giá trị nào của quizzes.status được xem là “đang mở”?

**Impact:** Quyết định bảng/query cần đọc, nhánh 403/404 và khả năng tạo attempt.

<a id="q-29-02-attempt-limit-expiry-and-conflict"></a>

## Q-29-02 — Attempt limit, expiry, resume và 403/409

**Evidence:** AC-16 ghi “Hết lượt/hết hạn → 403/409”. API #29 catalog liệt kê cả 403 DESIGN_ACCESS_DENIED và 409 DESIGN_STATE_CONFLICT nhưng không ánh xạ điều kiện.

1. Có giới hạn số attempt không? Nếu có, nguồn cấu hình và cách đếm là gì?
2. Deadline được lưu ở đâu và xác định hết hạn theo thời điểm nào?
3. Nếu Student đã có attempt IN_PROGRESS, API #29 tạo attempt mới hay trả/resume attempt cũ?
4. Điều kiện nào trả 403 và điều kiện nào trả 409?
5. Có bảo đảm chống tạo hai attempt đồng thời hoặc idempotency nào không?

**Impact:** Thay đổi eligibility query, conflict branches, persistence và retry behavior.

<a id="q-29-03-student-identity-and-schema"></a>

## Q-29-03 — Ánh xạ Student vào quiz_attempts.user_id

**Evidence:** API catalog chỉ nhận quiz_id trong path và yêu cầu Student Bearer JWT. DB design có quiz_attempts.user_id; exact JWT claim của API #29 chưa được xác định. DB table design đánh dấu quiz_id/user_id required, nhưng checked-in DB.sql cho phép NULL foreign keys.

1. Claim hoặc auth context nào cung cấp user_id cho INSERT?
2. Có yêu cầu xác minh user tồn tại trước khi ghi attempt không?
3. Baseline vật lý nào đúng cho nullability: DB table design hay checked-in DDL?
4. Có xác minh live schema trước khi implementation không?

**Impact:** INSERT mapping, FK guarantees và khả năng từ chối attempt nếu principal không map được.

<a id="q-29-04-initial-response-shape"></a>

## Q-29-04 — Giá trị QuizAttempt trả về ngay sau khi tạo

**Evidence:** Logical QuizAttempt yêu cầu id, quiz_id, status, started_at và answers[]; submitted_at và score là optional. AC-16 chỉ xác nhận trạng thái ban đầu IN_PROGRESS. Bảng quiz_attempts lưu attempt, còn answers thuộc flow API #30.

1. Response phải trả answers là mảng rỗng, omit field hay dùng cách khác?
2. submitted_at và score nên omit hay trả null?
3. started_at lấy từ clock nào và serialize theo timezone/precision nào?
4. AttemptStatus có giá trị nào ngoài IN_PROGRESS?
5. Có thêm response field nào được phép ngoài logical schema không?

**Impact:** Response JSON và output mapping.

<a id="q-29-05-path-and-not-found-mapping"></a>

## Q-29-05 — Path validation và not-found/access mapping

**Evidence:** API catalog định nghĩa quiz_id:int64! và cho phép 422, 404, 403. Catalog không nêu min/max, parse behavior hoặc access masking.

1. quiz_id phải dương hay có range cụ thể?
2. Path không parse được/int64 overflow có trả 422 DESIGN_VALIDATION_ERROR không?
3. Quiz không tồn tại trả 404; quiz tồn tại nhưng không được phép truy cập trả 403 hay được mask thành 404?

**Impact:** Request validation và error response details.

## Quyết định cần có trước khi đổi trạng thái

Các câu hỏi ảnh hưởng eligibility, access control, attempt lifecycle, persistence và response contract cần được Product/API owner chốt trước khi DD được đánh dấu Final hoặc API được triển khai.
