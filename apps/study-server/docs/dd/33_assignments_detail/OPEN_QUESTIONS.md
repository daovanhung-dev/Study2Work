# Open Questions — Study API #33 Lấy đề bài/rule/deadline

**Trạng thái DD:** Draft — Needs Confirmation
**Endpoint:** `GET /api/v1/assignments/{assignment_id}`

Các câu hỏi dưới đây giữ lại những điểm API catalog, AC-17 và schema design chưa chốt. DD không tự sửa contract nguồn.

<a id="q-33-01-assignment-access"></a>

## Q-33-01 — Student eligibility, assignment access và 403/404

**Evidence:** API catalog yêu cầu Student Bearer JWT; AC-17 precondition nói Student có quyền nộp. Assignment có `course_id`, và enrollment là bảng candidate trong DB design; API #33 chưa có route/query runtime.

1. Predicate nào xác nhận Student được xem assignment/course (enrollment, course status, hay rule khác)?
2. Assignment tồn tại nhưng Student không thuộc/không có quyền với course trả 403 hay được mask thành 404?
3. API có cần áp dụng cùng access rule với API #35 khi gọi trực tiếp không?

**Impact:** Authorization query, 403/404 mapping và khả năng dò assignment ID.

<a id="q-33-02-deadline-and-error-mapping"></a>

## Q-33-02 — Deadline behavior và API #33 error set

**Evidence:** AC-17 đặt precondition “Assignment còn hạn”; decision node n4 ghi “Quá hạn/không có quyền → 403/409”. API #33 catalog chỉ có 401/403/404/500, không có 409.

1. API #33 có từ chối GET khi đã quá hạn, hay vẫn trả Assignment để hiển thị?
2. Nếu từ chối, deadline thuộc 403 hay API catalog cần thêm 409 `DESIGN_STATE_CONFLICT`?
3. Deadline boundary là `now < due_at`, `now <= due_at`, hay rule khác?
4. Nếu rule chỉ được enforce lúc API #35 submit, AC-17/API #33 có cần cập nhật mô tả không?

DB table notes mô tả `due_at = NULL` là không có deadline; câu hỏi này không thay đổi định nghĩa đó.

**Impact:** Endpoint result, status/business-code contract và consistency với submission flow.

<a id="q-33-03-submission-rule-schema"></a>

## Q-33-03 — Nội dung “submission rule” trong response

**Evidence:** AC-17 node n3 yêu cầu “Đọc Assignment + submission rule”; reusable `Assignment` chỉ gồm `id`, `course_id`, `title`, `description?`, `due_at?`, `max_score`.

1. Submission rule gồm những field nào (ví dụ attempts, late policy, text/file constraints), và nguồn canonical nào sở hữu chúng?
2. Các rule có thuộc response `Assignment` của API #33 không, hay chỉ được kiểm tra bởi API #35?
3. Nếu cần trả rule, ai cập nhật approved contract/schema và compatibility policy?

**Impact:** Response shape, validation boundary của API #35 và client contract. DD hiện không thêm property ngoài `Assignment` schema.

<a id="q-33-04-physical-schema-and-serialization"></a>

## Q-33-04 — Nullability, deadline timestamp và decimal serialization

**Evidence:** Logical `Assignment` yêu cầu `course_id:int64` và `max_score:decimal-string`; DB table notes mô tả `course_id` required. Checked-in `DB.sql` lại cho phép NULL ở `course_id` và `max_score` (`max_score` có `DEFAULT 10`). `due_at` là `TIMESTAMP` không timezone trong DDL.

1. Schema canonical nào được duyệt cho `course_id` và `max_score`, và có backfill/constraint nào cần thiết trước khi implement?
2. `max_score` trả decimal-string với scale/rounding/NULL policy nào?
3. `due_at` dùng timezone nào và optional field khi NULL được omit hay trả `null`?

**Impact:** Candidate query mapping, response validity và timestamp/score interoperability. DD không sửa DDL hoặc khẳng định schema live.

<a id="q-33-05-path-validation"></a>

## Q-33-05 — Path validation và status

**Evidence:** Catalog khai báo `assignment_id:int64!` nhưng không có min/max và error set không có 400/422.

1. `assignment_id` phải dương hay chỉ cần parse được int64?
2. Parse failure, overflow hoặc giá trị ngoài miền được ánh xạ thế nào?
3. Nếu framework trả 422 mặc định, API catalog có cần cập nhật để phản ánh không?

**Impact:** Request validation và error contract. DD giữ nguyên error set hiện tại cho tới khi canonical source thay đổi.

## Trạng thái cần duy trì

Giữ `Draft — Needs Confirmation` cho tới khi owner xác nhận access/deadline policy, submission-rule ownership, schema mapping và serialization. Không sửa API catalog, AC diagram, ERD hoặc DDL để tự giải quyết các câu hỏi này.
