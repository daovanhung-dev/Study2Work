# OPEN_QUESTIONS — API #37

**Status:** Draft — Needs Confirmation
**Endpoint:** GET /api/v1/users/me/progress/{course_id}

## Q-01 — Response schema cho tiến độ course

**Evidence:** [API catalog](../../../../../docs/lists/list_api.md) khai báo ApiEnvelope<UserProfile>. AC-18 yêu cầu dashboard tiến độ; UserProfile reusable schema không có field tiến độ.
**Impact:** Không thể xác định data payload mà client cần hiển thị hoặc map candidate reads.
**Decision needed:** Giữ UserProfile và bổ sung progress data ở schema khác, hay đổi response type sang một progress-specific schema? Cập nhật contract có thẩm quyền trước khi chốt DD/implementation.

## Q-02 — Tập dữ liệu và công thức aggregate

**Evidence:** [AC-18](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) nêu “Aggregate lesson + quiz + assignment progress”; không chỉ rõ cách tính.
**Impact:** Chưa thể xác định denominator, weighting, completion, rounding hoặc cách xử lý item bị ẩn/không áp dụng.
**Decision needed:** Chốt tập lesson/quiz/assignment được tính, công thức từng nhóm, công thức tổng hợp và quy tắc làm tròn; hiện DD không tự đặt công thức.

## Q-03 — Chọn quiz attempt và assignment submission

**Evidence:** DB design cho phép nhiều quiz_attempts và assignment_submissions theo user và resource.
**Impact:** Chọn latest, best, latest submitted, mọi attempt hay trạng thái khác sẽ làm kết quả khác nhau.
**Decision needed:** Chốt attempt/submission nào được tính, trạng thái nào được tính, xử lý attempt đang làm/bài chưa chấm và việc hiển thị điểm.

## Q-04 — Enrollment và quyền truy cập course

**Evidence:** Catalog yêu cầu Student JWT; AC-18 precondition chỉ nói Student đã đăng nhập. Enrollment là bảng riêng trong DB design nhưng AC-18 không chỉ định predicate.
**Impact:** Không xác định được có yêu cầu enrollment, published course, active status hoặc quyền khác không.
**Decision needed:** Chốt access predicate, trạng thái enrollment/course cần thỏa và kiểm tra ownership theo principal.

## Q-05 — Ý nghĩa 403, 404 và resource masking

**Evidence:** Catalog liệt kê cả 403 DESIGN_ACCESS_DENIED và 404 DESIGN_RESOURCE_NOT_FOUND. AC-18 không gắn các điều kiện cụ thể cho từng code.
**Impact:** Không rõ course không tồn tại, course ngoài quyền truy cập hay dữ liệu tiến độ không tồn tại trả code nào.
**Decision needed:** Quy định mapping từng điều kiện và liệu resource ngoài quyền có bị mask thành 404 không.

## Q-06 — Course hợp lệ nhưng chưa có tiến độ

**Evidence:** Không có AC/API contract quy định empty-state cho course chưa có activity.
**Impact:** Không rõ trả 200 với aggregate rỗng/zero, UserProfile hiện tại, hay 404.
**Decision needed:** Chốt status và shape cho course tồn tại nhưng chưa có lesson progress, quiz attempt hoặc assignment submission; thống nhất với response schema ở Q-01.

## Q-07 — Path parse/range cho course_id

**Evidence:** Catalog khai báo course_id:int64! nhưng không có error 400/422 trong status set.
**Impact:** Framework/API gateway có thể xử lý path không parse được khác nhau.
**Decision needed:** Chốt miền hợp lệ và status/business code cho giá trị không parse/ngoài miền; nếu cần code mới, cập nhật catalog.

## Q-08 — Identity JWT và live schema

**Evidence:** Endpoint dùng /me nhưng catalog không nêu JWT claim mapping. DB guide/ERD là design; checked-in DB.sql chưa được đối chiếu live. Một số FK nullability giữa table guide và DDL khác nhau.
**Impact:** Chưa thể khóa predicate user_id hoặc tin cậy constraints khi thiết kế query.
**Decision needed:** Chốt principal-to-user mapping và xác minh schema/migration được áp dụng trước implementation.

## Q-09 — Projection UserProfile nếu catalog được giữ

**Evidence:** Reusable UserProfile có bio?:string, còn users trong DB guide/checked-in DDL không có bio column; API #37 không nêu nguồn projection cho UserProfile.
**Impact:** Ngay cả khi giữ catalog response, không xác định được nguồn cho mọi field data.
**Decision needed:** Chốt projection/source cho từng UserProfile field hoặc sửa response contract cùng Q-01.

---
