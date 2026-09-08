# UNICA Database Tables

Tài liệu này mô tả 16 bảng trong [`DB_UNICA_ERD.drawio`](./DB_UNICA_ERD.drawio),
bao gồm mục đích lưu trữ, quan hệ, các query design đã được mô tả trong DD và
trạng thái sử dụng trong source hiện hành.

## Phạm vi và trạng thái xác minh

ERD là thiết kế database V1. Nó chưa phải schema runtime đã được xác minh. Theo
context hiện hành của repository:

- `ERD V1`: kiểu dữ liệu, khóa, nullable, default và quan hệ được đọc từ ERD.
- `DESIGN_ONLY`: query/API có trong `docs/dd/` hoặc `docs/lists/list_api.md`,
  nhưng chưa được implement/wire vào runtime hiện tại.
- `RUNTIME-VERIFIED`: code hiện tại thực sự có method/query tương ứng.
- `UNWIRED`: implementation có trong source nhưng đường chạy hiện tại không
  đăng ký hoặc không gọi tới nó.
- `NOT_FOUND`: chưa có source xác nhận table-specific method/schema tương ứng.
- `DISCREPANCY`: thiết kế ERD khác với schema/runtime hiện hành; không tự
  reconcile bằng suy đoán.

### Database runtime hiện tại

| Scope | Trạng thái | Bằng chứng hiện tại | Kết luận |
|---|---|---|---|
| Study | `RUNTIME-VERIFIED` | `apps/study-server/app/core/database.py` có `execute_query`, `query_one`, `query_many` | Đây là helper generic, chưa có method nghiệp vụ truy vấn các bảng ERD. Study business module hiện chưa được xác minh runnable. |
| Study | `DECLARED_NOT_RUNNABLE` | `apps/study-server/app/api/v1.py` có `SELECT NOW()` trong `/api/v1/test/db` | Chỉ là DB connectivity check; không truy vấn bảng nghiệp vụ. Đường import hiện tại còn blocker. |
| AI | `UNWIRED` | `apps/ai-server/app/core/database.py` có copied query helpers | Helper không được wiring vào runtime `app/main.py`; không có database runtime usage. |
| Work | `RUNTIME-VERIFIED` | `apps/work-server/prisma/schema.prisma` chỉ có `SystemRecord`/`system_records` | Không có 16 bảng ERD. `HealthService.ready()` chỉ chạy `SELECT 1`; schema `system_records` không được domain service sử dụng. |

Vì vậy, các query cụ thể theo bảng bên dưới được ghi là `DESIGN_ONLY` nếu
nguồn đến từ DD/API contract; không nên hiểu chúng là method đang chạy.

## Tổng quan 16 bảng

| Nhóm | Bảng | Tên tiếng Việt | Vai trò |
|---|---|---|---|
| Account & User | `users` | Người dùng / tài khoản | Lưu tài khoản, thông tin liên hệ, vai trò và trạng thái. |
| Course & Learning | `courses` | Khóa học | Lưu thông tin khóa học do mentor phụ trách. |
| Course & Learning | `lessons` | Bài học | Lưu nội dung và thứ tự bài học trong khóa học. |
| Course & Learning | `resources` | Tài nguyên học tập | Lưu metadata và URL tài nguyên gắn với bài học. |
| Course & Learning | `enrollments` | Ghi danh khóa học | Lưu quyền/tham gia của người dùng vào khóa học. |
| Course & Learning | `lesson_progress` | Tiến độ bài học | Lưu trạng thái và tiến độ học của người dùng theo bài học. |
| Assessment | `quizzes` | Bài kiểm tra | Lưu cấu hình bài kiểm tra thuộc khóa học. |
| Assessment | `quiz_questions` | Câu hỏi bài kiểm tra | Lưu các câu hỏi của bài kiểm tra. |
| Assessment | `quiz_choices` | Lựa chọn câu trả lời | Lưu các lựa chọn của từng câu hỏi và đáp án đúng. |
| Assessment | `quiz_attempts` | Lần làm bài kiểm tra | Lưu mỗi lần người dùng bắt đầu/nộp một bài kiểm tra. |
| Assessment | `quiz_answers` | Câu trả lời trong lần làm bài | Lưu câu trả lời, kết quả đúng/sai và điểm nhận được. |
| Assessment | `assignments` | Bài tập | Lưu đề bài, hạn nộp và điểm tối đa của bài tập. |
| Assessment | `assignment_submissions` | Bài nộp bài tập | Lưu nội dung/file nộp, điểm, phản hồi và trạng thái chấm. |
| Interaction & System | `discussions` | Thảo luận / đánh giá | Lưu bài thảo luận, review và reply theo dạng cây. |
| Interaction & System | `notifications` | Thông báo | Lưu thông báo, người nhận/người gửi và trạng thái đã đọc. |
| Interaction & System | `payments` | Thanh toán | Lưu giao dịch thanh toán của người dùng cho khóa học. |

## 1. `users` — Người dùng / tài khoản

### Mục đích và thông tin lưu trữ

Lưu định danh tài khoản, thông tin hiển thị/liên hệ, credential đã hash, vai
trò và trạng thái hoạt động của người dùng. Đây là bảng gốc được nhiều bảng
khác tham chiếu qua `user_id`, `mentor_id`, `sender_id` hoặc `recipient`.

### Quan hệ

- `users.id` → `courses.mentor_id`: một người dùng có thể mentor nhiều khóa học.
- `users.id` → `enrollments.user_id`: một người dùng có thể có nhiều enrollment.
- `users.id` → `lesson_progress.user_id`: một người dùng có nhiều bản ghi tiến độ.
- `users.id` → `quiz_attempts.user_id`: một người dùng có nhiều lần làm quiz.
- `users.id` → `assignment_submissions.user_id`: một người dùng có nhiều bài nộp.
- `users.id` → `discussions.user_id`: một người dùng có thể tạo nhiều discussion.
- `users.id` → `notifications.user_id` và `notifications.sender_id`: người nhận
  hoặc người gửi nhiều notification.
- `users.id` → `payments.user_id`: một người dùng có nhiều payment.

### Method/query liên quan

| Trạng thái | Method/query | Loại | Mục đích và điều kiện | Nguồn |
|---|---|---|---|---|
| `DESIGN_ONLY` | `Q1` của API #1 | `SELECT` | Kiểm tra email đã tồn tại: đọc `users.id` với `users.email = email`; có record thì conflict. | [`docs/dd/01_auth_register/05_Data_Mapping.md`](../dd/01_auth_register/05_Data_Mapping.md) |
| `DESIGN_ONLY` | `M1` của API #1 | `INSERT` | Tạo account sau khi Q1 xác nhận email chưa tồn tại; `password_hash` nhận giá trị đã hash; transaction sở hữu bởi use case. | [`docs/dd/01_auth_register/07_users_insert.md`](../dd/01_auth_register/07_users_insert.md) |
| `DESIGN_ONLY` | `Q1.1`–`Q1.10` của API #3 | `SELECT` | Lookup theo `email`, đọc id, profile, `password_hash`, role, status và timestamps để verify login. | [`docs/dd/03_auth_login/05_Data_Mapping.md`](../dd/03_auth_login/05_Data_Mapping.md) |
| `DESIGN_ONLY` | `Q1.1`–`Q1.9` của API #4 | `SELECT` | Lookup user hiện tại theo `users.id = user_id`; không đọc `password_hash`. | [`docs/dd/04_users_me/05_Data_Mapping.md`](../dd/04_users_me/05_Data_Mapping.md) |
| `DESIGN_ONLY` | Mentor join của API #6, #7, #8 | `INNER JOIN` | Đọc `id`, `full_name`, `avatar_url` của mentor qua `courses.mentor_id = users.id`. | [`docs/dd/06_courses/05_Data_Mapping.md`](../dd/06_courses/05_Data_Mapping.md), [`docs/dd/07_courses_search/05_Data_Mapping.md`](../dd/07_courses_search/05_Data_Mapping.md), [`docs/dd/08_courses_detail/05_Data_Mapping.md`](../dd/08_courses_detail/05_Data_Mapping.md) |
| `DESIGN_ONLY` | Author join của API #10 | `INNER JOIN` | Đọc thông tin tác giả review/reply qua `discussions.user_id = users.id`. | [`docs/dd/10_courses_reviews/05_Data_Mapping.md`](../dd/10_courses_reviews/05_Data_Mapping.md) |
| `NOT_FOUND` | Table-specific runtime method | — | Không có business method hiện tại được xác minh gọi tới `users`. | Source status hiện hành |

### Chi tiết trường

| Trường | Kiểu | Khóa/ràng buộc | Mô tả | Nguồn/trạng thái |
|---|---|---|---|---|
| `id` | `BIGSERIAL` | PK, bắt buộc | Định danh duy nhất của tài khoản; được tham chiếu từ các bảng nghiệp vụ khác. | ERD V1; design-only |
| `full_name` | `VARCHAR(150)` | Bắt buộc | Tên hiển thị đầy đủ của người dùng/mentor/tác giả. | ERD V1; DD/API mapping |
| `email` | `VARCHAR(255)` | UNIQUE, bắt buộc | Địa chỉ email dùng để định danh và đăng nhập; dùng trong kiểm tra trùng. | ERD V1; DD API #1/#3 |
| `password_hash` | `VARCHAR(255)` | Bắt buộc | Mật khẩu đã hash; không lưu hoặc trả plaintext. | ERD V1; DD API #1/#3 |
| `role` | `VARCHAR(20)` | Bắt buộc | Vai trò tài khoản, dùng cho authorization/RBAC theo contract. | ERD V1; DD/API contract |
| `avatar_url` | `TEXT` | Nullable | URL ảnh đại diện; có thể rỗng khi người dùng chưa có avatar. | ERD V1; DD/API mapping |
| `phone` | `VARCHAR(20)` | Nullable | Số điện thoại liên hệ của người dùng. | ERD V1; DD/API mapping |
| `status` | `VARCHAR(20)` | Default `ACTIVE` | Trạng thái tài khoản, dùng để quyết định account có được hoạt động/đăng nhập hay không. | ERD V1; DD API #3 |
| `created_at` | `TIMESTAMP` | Bắt buộc | Thời điểm tạo tài khoản. | ERD V1 |
| `updated_at` | `TIMESTAMP` | Bắt buộc | Thời điểm gần nhất tài khoản được cập nhật. | ERD V1 |

## 2. `courses` — Khóa học

### Mục đích và thông tin lưu trữ

Lưu thông tin tổng quan của khóa học: tên, mô tả, ảnh thumbnail, giá, trạng
thái xuất bản và mentor phụ trách.

### Quan hệ

- `courses.mentor_id` → `users.id`.
- `courses.id` → `enrollments.course_id`, `lessons.course_id`, `quizzes.course_id`,
  `assignments.course_id`, `discussions.course_id` và `payments.course_id`.

### Method/query liên quan

| Trạng thái | Method/query | Loại | Mục đích và điều kiện | Nguồn |
|---|---|---|---|---|
| `DESIGN_ONLY` | `Q1`/`Q2` của API #6 | `SELECT` + `COUNT` | Q1 đọc `c.id`, `c.name`, `c.description`, `c.thumbnail_url`, `c.price`, `c.status` và mentor summary; Q2 đọc `COUNT(*)`. Lọc `c.status = 'PUBLISHED'`, áp dụng category/filter theo contract. | [`docs/dd/06_courses/05_Data_Mapping.md`](../dd/06_courses/05_Data_Mapping.md) |
| `DESIGN_ONLY` | `Q1`/`Q2` của API #7 | `SELECT` + `COUNT` | Q1 đọc các field course/mentor như API #6 và tìm trên `c.name`; Q2 đọc `COUNT(*)`. Query page và count dùng cùng published/search/filter predicates. | [`docs/dd/07_courses_search/05_Data_Mapping.md`](../dd/07_courses_search/05_Data_Mapping.md) |
| `DESIGN_ONLY` | `Q1` của API #8 | `SELECT` + mentor join | Đọc `c.id`, `c.name`, `c.description`, `c.thumbnail_url`, `c.price`, `c.status` cùng `m.id`, `m.full_name`, `m.avatar_url`; lọc theo id và `PUBLISHED`, join mentor bắt buộc. | [`docs/dd/08_courses_detail/05_Data_Mapping.md`](../dd/08_courses_detail/05_Data_Mapping.md) |
| `DESIGN_ONLY` | `Q1` của API #9 | `SELECT` | Đọc `c.id`, `c.status` theo `c.id = :course_id AND c.status = 'PUBLISHED'` trước khi đọc lesson. | [`docs/dd/09_courses_curriculum/05_Data_Mapping.md`](../dd/09_courses_curriculum/05_Data_Mapping.md) |
| `DESIGN_ONLY` | `Q1` của API #10 | `SELECT` | Đọc `c.id`, `c.status` theo course id và `PUBLISHED` trước khi đọc reviews. | [`docs/dd/10_courses_reviews/05_Data_Mapping.md`](../dd/10_courses_reviews/05_Data_Mapping.md) |
| `DESIGN_ONLY` | `Q1` của API #11 | `SELECT` | Đọc `c.id`, `c.status` theo course id và `PUBLISHED` trước khi đọc resources thuộc course. | [`docs/dd/11_courses_resources/05_Data_Mapping.md`](../dd/11_courses_resources/05_Data_Mapping.md) |
| `NOT_FOUND` | Table-specific runtime method | — | Chưa có service/repository runtime được xác minh gọi tới `courses`. | Source status hiện hành |

### Chi tiết trường

| Trường | Kiểu | Khóa/ràng buộc | Mô tả | Nguồn/trạng thái |
|---|---|---|---|---|
| `id` | `BIGSERIAL` | PK, bắt buộc | Định danh khóa học. | ERD V1; design-only |
| `mentor_id` | `BIGINT` | FK → `users.id`, bắt buộc | Người dùng phụ trách/mentor của khóa học. | ERD V1; DD API #6–#10 |
| `name` | `VARCHAR(200)` | Bắt buộc | Tên vật lý của khóa học; map sang logical `Course.title` trong contract. | ERD V1; DD/API mapping |
| `description` | `TEXT` | Nullable | Mô tả nội dung và phạm vi khóa học. | ERD V1; DD/API mapping |
| `thumbnail_url` | `TEXT` | Nullable | URL ảnh đại diện của khóa học. | ERD V1; DD/API mapping |
| `price` | `NUMERIC(12,2)` | Default `0` | Giá khóa học; contract serialize tiền dưới dạng decimal string. | ERD V1; API contract |
| `status` | `VARCHAR(20)` | Default `DRAFT` | Trạng thái vòng đời/hiển thị; các API public design thường gate bằng `PUBLISHED`. | ERD V1; DD API #6–#11 |
| `created_at` | `TIMESTAMP` | Bắt buộc | Thời điểm tạo khóa học. | ERD V1 |
| `updated_at` | `TIMESTAMP` | Bắt buộc | Thời điểm cập nhật gần nhất. | ERD V1 |

## 3. `lessons` — Bài học

### Mục đích và thông tin lưu trữ

Lưu các bài học thuộc khóa học, gồm nội dung, video, thứ tự trong curriculum và
trạng thái hiển thị.

### Quan hệ

- `lessons.course_id` → `courses.id`.
- `lessons.id` → `resources.lesson_id` và `lesson_progress.lesson_id`.

### Method/query liên quan

| Trạng thái | Method/query | Loại | Mục đích và điều kiện | Nguồn |
|---|---|---|---|---|
| `DESIGN_ONLY` | `Q2` của API #9 | `SELECT` | Đọc `l.id`, `l.course_id`, `l.name`, `l.content`, `l.video_url`, `l.sort_order`, `l.status`; lọc theo `course_id` và `status = 'PUBLISHED'`, sắp xếp theo `sort_order`. | [`docs/dd/09_courses_curriculum/05_Data_Mapping.md`](../dd/09_courses_curriculum/05_Data_Mapping.md) |
| `DESIGN_ONLY` | `Q2` của API #11 | `SELECT`/join | Dùng `l.id`, `l.course_id` để scope resources theo course và nối `resources.lesson_id = lessons.id`. | [`docs/dd/11_courses_resources/05_Data_Mapping.md`](../dd/11_courses_resources/05_Data_Mapping.md) |
| `DESIGN_ONLY` | `Q2` của API #12 | `SELECT`/join | Đọc `l.id`, `l.course_id`, rồi nối `l.course_id = c.id` và đọc `c.status` để kiểm tra parent course public. | [`docs/dd/12_resources_detail/05_Data_Mapping.md`](../dd/12_resources_detail/05_Data_Mapping.md) |
| `NOT_FOUND` | Table-specific runtime method | — | Chưa có runtime method được xác minh gọi tới `lessons`. | Source status hiện hành |

### Chi tiết trường

| Trường | Kiểu | Khóa/ràng buộc | Mô tả | Nguồn/trạng thái |
|---|---|---|---|---|
| `id` | `BIGSERIAL` | PK, bắt buộc | Định danh bài học. | ERD V1 |
| `course_id` | `BIGINT` | FK → `courses.id`, bắt buộc | Khóa học chứa bài học. | ERD V1; DD API #9/#11/#12 |
| `name` | `VARCHAR(200)` | Bắt buộc | Tên bài học; map sang logical `Lesson.title`. | ERD V1; DD API #9 |
| `content` | `TEXT` | Nullable | Nội dung chữ hoặc nội dung chính của bài học. | ERD V1; DD API #9 |
| `video_url` | `TEXT` | Nullable | URL video bài học nếu bài có nội dung video. | ERD V1; DD API #9 |
| `sort_order` | `INT` | Default `0` | Thứ tự bài học trong curriculum; map sang logical `Lesson.order`. | ERD V1; DD API #9 |
| `status` | `VARCHAR(20)` | Default `DRAFT` | Trạng thái bài học; query public design lọc `PUBLISHED`. | ERD V1; DD API #9 |
| `created_at` | `TIMESTAMP` | Bắt buộc | Thời điểm tạo bài học. | ERD V1 |
| `updated_at` | `TIMESTAMP` | Bắt buộc | Thời điểm cập nhật bài học. | ERD V1 |

## 4. `resources` — Tài nguyên học tập

### Mục đích và thông tin lưu trữ

Lưu metadata của tài liệu/tài nguyên đính kèm cho một bài học. Bảng chỉ lưu
thông tin nhận diện và URL; signed URL hoặc object storage là external operation
trong DD, không phải mutation của bảng.

### Quan hệ

- `resources.lesson_id` → `lessons.id`.

### Method/query liên quan

| Trạng thái | Method/query | Loại | Mục đích và điều kiện | Nguồn |
|---|---|---|---|---|
| `DESIGN_ONLY` | `Q2` của API #11 | `SELECT`/join | Đọc `r.id`, `r.lesson_id`, `r.name`, `r.resource_type`, `r.url` qua `resources.lesson_id = lessons.id` và `lessons.course_id = :course_id`. | [`docs/dd/11_courses_resources/05_Data_Mapping.md`](../dd/11_courses_resources/05_Data_Mapping.md) |
| `DESIGN_ONLY` | `Q1` của API #12 | `SELECT` | Đọc `r.id`, `r.lesson_id`, `r.name`, `r.resource_type`, `r.url` theo `resources.id = :resource_id`. | [`docs/dd/12_resources_detail/05_Data_Mapping.md`](../dd/12_resources_detail/05_Data_Mapping.md) |
| `DESIGN_ONLY` | `Q3` của API #12 | External read | Resolve signed URL khi resource private; nguồn visibility/object key chưa có trong ERD. | [`docs/dd/12_resources_detail/05_Data_Mapping.md`](../dd/12_resources_detail/05_Data_Mapping.md) |
| `NOT_FOUND` | Table-specific runtime method | — | Chưa có runtime method được xác minh gọi tới `resources`. | Source status hiện hành |

### Chi tiết trường

| Trường | Kiểu | Khóa/ràng buộc | Mô tả | Nguồn/trạng thái |
|---|---|---|---|---|
| `id` | `BIGSERIAL` | PK, bắt buộc | Định danh tài nguyên. | ERD V1 |
| `lesson_id` | `BIGINT` | FK → `lessons.id`, bắt buộc | Bài học mà tài nguyên được đính kèm. | ERD V1; DD API #11/#12 |
| `name` | `VARCHAR(200)` | Bắt buộc | Tên hiển thị của tài nguyên. | ERD V1; DD API #11/#12 |
| `resource_type` | `VARCHAR(20)` | Bắt buộc | Loại tài nguyên; map sang logical `Resource.type`. Enum cụ thể chưa được đặc tả. | ERD V1; DD API #11/#12 |
| `url` | `TEXT` | Bắt buộc | URL hoặc địa chỉ truy cập tài nguyên. | ERD V1; DD API #11/#12 |
| `created_at` | `TIMESTAMP` | Bắt buộc | Thời điểm tạo metadata tài nguyên. | ERD V1 |

> **DISCREPANCY:** Một số contract API design đề cập `resources.visibility`,
> nhưng ERD không có cột này. Không thêm cột hoặc predicate visibility khi chưa
> có source xác nhận.

## 5. `enrollments` — Ghi danh khóa học

### Mục đích và thông tin lưu trữ

Lưu quan hệ tham gia giữa người dùng và khóa học, cùng trạng thái enrollment,
thời điểm ghi danh và thời điểm hoàn thành.

### Quan hệ

- `enrollments.user_id` → `users.id`.
- `enrollments.course_id` → `courses.id`.

### Method/query liên quan

| Trạng thái | Method/query | Loại | Mục đích và điều kiện | Nguồn |
|---|---|---|---|---|
| `DESIGN_ONLY` | API #15 `enrollment-status` | `SELECT` | Kiểm tra trạng thái user/course enrollment. Query matrix chi tiết chưa có DD riêng. | [`docs/lists/list_api.md`](../lists/list_api.md) |
| `DESIGN_ONLY` | API #19 `POST .../enrollments` | `INSERT` | Tạo quyền học cho user hiện tại trong course; điều kiện ownership/status theo contract. Query matrix chi tiết chưa có DD riêng. | [`docs/lists/list_api.md`](../lists/list_api.md) |
| `DESIGN_ONLY` | API #20 `GET /users/me/courses` | `SELECT` | Đọc danh sách khóa học đã đăng ký, có filter status/page theo contract. | [`docs/lists/list_api.md`](../lists/list_api.md) |
| `NOT_FOUND` | Table-specific runtime method | — | Chưa có implementation/query runtime được xác minh. | Source status hiện hành |

### Chi tiết trường

| Trường | Kiểu | Khóa/ràng buộc | Mô tả | Nguồn/trạng thái |
|---|---|---|---|---|
| `id` | `BIGSERIAL` | PK, bắt buộc | Định danh bản ghi ghi danh. | ERD V1 |
| `user_id` | `BIGINT` | FK → `users.id`, bắt buộc | Người dùng được ghi danh. | ERD V1; API contract |
| `course_id` | `BIGINT` | FK → `courses.id`, bắt buộc | Khóa học được ghi danh. | ERD V1; API contract |
| `status` | `VARCHAR(20)` | Default `ACTIVE` | Trạng thái quan hệ ghi danh, ví dụ đang active hoặc đã hoàn tất theo business rule tương lai. Các giá trị đầy đủ chưa được đặc tả. | ERD V1; enum chưa đầy đủ |
| `enrolled_at` | `TIMESTAMP` | Bắt buộc | Thời điểm user được ghi danh. | ERD V1 |
| `completed_at` | `TIMESTAMP` | Nullable | Thời điểm hoàn thành khóa học; null khi chưa hoàn thành. | ERD V1 |

## 6. `lesson_progress` — Tiến độ bài học

### Mục đích và thông tin lưu trữ

Lưu tiến độ học của từng user trên từng lesson, gồm trạng thái, phần trăm đã
học và các mốc truy cập/hoàn thành.

### Quan hệ

- `lesson_progress.user_id` → `users.id`.
- `lesson_progress.lesson_id` → `lessons.id`.

### Method/query liên quan

| Trạng thái | Method/query | Loại | Mục đích và điều kiện | Nguồn |
|---|---|---|---|---|
| `DESIGN_ONLY` | API #21, #37 `GET /users/me/progress...` | `SELECT` | Đọc tiến độ tổng hợp hoặc chi tiết theo course; query matrix chi tiết chưa có DD riêng. | [`docs/lists/list_api.md`](../lists/list_api.md) |
| `DESIGN_ONLY` | API #25 `PATCH .../progress` | `UPDATE`/upsert | Lưu vị trí/trạng thái tiến độ của user trên lesson; field contract có `percent` và `completed`, còn mapping vật lý chi tiết chưa có DD riêng. | [`docs/lists/list_api.md`](../lists/list_api.md) |
| `DESIGN_ONLY` | API #65, #67 `GET .../progress` | `SELECT` | Mentor đọc tiến độ toàn lớp hoặc một student trong course; mapping SQL chưa có DD riêng. | [`docs/lists/list_api.md`](../lists/list_api.md) |
| `NOT_FOUND` | Table-specific runtime method | — | Chưa có implementation/query runtime được xác minh. | Source status hiện hành |

### Chi tiết trường

| Trường | Kiểu | Khóa/ràng buộc | Mô tả | Nguồn/trạng thái |
|---|---|---|---|---|
| `id` | `BIGSERIAL` | PK, bắt buộc | Định danh bản ghi tiến độ. | ERD V1 |
| `user_id` | `BIGINT` | FK → `users.id`, bắt buộc | User đang học lesson. | ERD V1; API contract |
| `lesson_id` | `BIGINT` | FK → `lessons.id`, bắt buộc | Lesson được theo dõi tiến độ. | ERD V1; API contract |
| `status` | `VARCHAR(20)` | Default `NOT_STARTED` | Trạng thái học của lesson. Các giá trị ngoài default chưa được canonical hóa. | ERD V1; enum chưa đầy đủ |
| `progress_percent` | `SMALLINT` | Default `0` | Phần trăm tiến độ hoàn thành của lesson. ERD chưa ghi CHECK range. | ERD V1 |
| `last_accessed_at` | `TIMESTAMP` | Nullable | Lần gần nhất user truy cập lesson. | ERD V1 |
| `completed_at` | `TIMESTAMP` | Nullable | Thời điểm lesson được đánh dấu hoàn thành. | ERD V1 |

## 7. `quizzes` — Bài kiểm tra

### Mục đích và thông tin lưu trữ

Lưu cấu hình bài kiểm tra thuộc một khóa học: tên, mô tả, điểm đạt, thời lượng
và trạng thái.

### Quan hệ

- `quizzes.course_id` → `courses.id`.
- `quizzes.id` → `quiz_questions.quiz_id` và `quiz_attempts.quiz_id`.

### Method/query liên quan

| Trạng thái | Method/query | Loại | Mục đích và điều kiện | Nguồn |
|---|---|---|---|---|
| `DESIGN_ONLY` | API #28 `GET /quizzes/{quiz_id}` | `SELECT` | Đọc metadata/câu hỏi được phép hiển thị của quiz. Query matrix chi tiết chưa có DD riêng. | [`docs/lists/list_api.md`](../lists/list_api.md) |
| `DESIGN_ONLY` | API #29–#32 | `SELECT`/liên kết | Tạo attempt, lưu answer, submit và đọc kết quả; quiz là bảng gốc của các flow này. Mapping SQL chi tiết chưa có DD riêng. | [`docs/lists/list_api.md`](../lists/list_api.md) |
| `DESIGN_ONLY` | API #87–#91 | `SELECT`/`INSERT`/`UPDATE`/`DELETE` | Admin list/create/update/delete và thống kê quiz theo contract. Query matrix chi tiết chưa có DD riêng. | [`docs/lists/list_api.md`](../lists/list_api.md) |
| `NOT_FOUND` | Table-specific runtime method | — | Chưa có implementation/query runtime được xác minh. | Source status hiện hành |

### Chi tiết trường

| Trường | Kiểu | Khóa/ràng buộc | Mô tả | Nguồn/trạng thái |
|---|---|---|---|---|
| `id` | `BIGSERIAL` | PK, bắt buộc | Định danh bài kiểm tra. | ERD V1 |
| `course_id` | `BIGINT` | FK → `courses.id`, bắt buộc | Khóa học chứa bài kiểm tra. | ERD V1; API contract |
| `name` | `VARCHAR(200)` | Bắt buộc | Tên bài kiểm tra; contract logical dùng `Quiz.title`. | ERD V1; API contract |
| `description` | `TEXT` | Nullable | Mô tả/hướng dẫn của bài kiểm tra. | ERD V1 |
| `passing_score` | `NUMERIC(5,2)` | Default `0` | Ngưỡng điểm đạt bài kiểm tra. | ERD V1; API contract |
| `time_limit_minutes` | `INT` | Nullable | Giới hạn thời gian làm bài, tính theo phút. | ERD V1; API contract |
| `status` | `VARCHAR(20)` | Default `DRAFT` | Trạng thái phát hành/cấu hình của quiz. Enum đầy đủ chưa được đặc tả. | ERD V1 |
| `created_at` | `TIMESTAMP` | Bắt buộc | Thời điểm tạo quiz. | ERD V1 |
| `updated_at` | `TIMESTAMP` | Bắt buộc | Thời điểm cập nhật quiz. | ERD V1 |

## 8. `quiz_questions` — Câu hỏi bài kiểm tra

### Mục đích và thông tin lưu trữ

Lưu nội dung và thứ tự các câu hỏi thuộc quiz, cùng số điểm tối đa của từng
câu.

### Quan hệ

- `quiz_questions.quiz_id` → `quizzes.id`.
- `quiz_questions.id` → `quiz_choices.question_id` và `quiz_answers.question_id`.

### Method/query liên quan

| Trạng thái | Method/query | Loại | Mục đích và điều kiện | Nguồn |
|---|---|---|---|---|
| `DESIGN_ONLY` | API #28 `GET /quizzes/{quiz_id}` | `SELECT` | Đọc câu hỏi thuộc quiz để hiển thị đề. | [`docs/lists/list_api.md`](../lists/list_api.md) |
| `DESIGN_ONLY` | API #30 answers | `SELECT`/liên kết | Dùng question id khi autosave/chấm câu trả lời. Chi tiết query chưa có DD riêng. | [`docs/lists/list_api.md`](../lists/list_api.md) |
| `DESIGN_ONLY` | API #87–#91 | `SELECT`/mutation | Quản trị câu hỏi thông qua flow quản lý quiz; mapping SQL chưa được đặc tả. | [`docs/lists/list_api.md`](../lists/list_api.md) |
| `NOT_FOUND` | Table-specific runtime method | — | Chưa có implementation/query runtime được xác minh. | Source status hiện hành |

### Chi tiết trường

| Trường | Kiểu | Khóa/ràng buộc | Mô tả | Nguồn/trạng thái |
|---|---|---|---|---|
| `id` | `BIGSERIAL` | PK, bắt buộc | Định danh câu hỏi. | ERD V1 |
| `quiz_id` | `BIGINT` | FK → `quizzes.id`, bắt buộc | Quiz chứa câu hỏi. | ERD V1; API contract |
| `question_text` | `TEXT` | Bắt buộc | Nội dung câu hỏi. | ERD V1; API contract |
| `sort_order` | `INT` | Default `0` | Thứ tự câu hỏi trong quiz. | ERD V1 |
| `score` | `NUMERIC(5,2)` | Default `1` | Điểm tối đa của câu hỏi. | ERD V1; API contract |

## 9. `quiz_choices` — Lựa chọn câu trả lời

### Mục đích và thông tin lưu trữ

Lưu các phương án trả lời của một câu hỏi và đánh dấu phương án đúng.

### Quan hệ

- `quiz_choices.question_id` → `quiz_questions.id`.
- `quiz_choices.id` → `quiz_answers.choice_id`.

### Method/query liên quan

| Trạng thái | Method/query | Loại | Mục đích và điều kiện | Nguồn |
|---|---|---|---|---|
| `DESIGN_ONLY` | API #28 `GET /quizzes/{quiz_id}` | `SELECT` | Đọc choices để dựng câu hỏi/đề kiểm tra. | [`docs/lists/list_api.md`](../lists/list_api.md) |
| `DESIGN_ONLY` | API #30 answers | `SELECT`/liên kết | Đối chiếu choice được chọn với question khi lưu/chấm answer. Chi tiết query chưa có DD riêng. | [`docs/lists/list_api.md`](../lists/list_api.md) |
| `NOT_FOUND` | Table-specific runtime method | — | Chưa có implementation/query runtime được xác minh. | Source status hiện hành |

### Chi tiết trường

| Trường | Kiểu | Khóa/ràng buộc | Mô tả | Nguồn/trạng thái |
|---|---|---|---|---|
| `id` | `BIGSERIAL` | PK, bắt buộc | Định danh lựa chọn. | ERD V1 |
| `question_id` | `BIGINT` | FK → `quiz_questions.id`, bắt buộc | Câu hỏi sở hữu lựa chọn. | ERD V1; API contract |
| `choice_text` | `TEXT` | Bắt buộc | Nội dung phương án trả lời. | ERD V1; API contract |
| `is_correct` | `BOOLEAN` | Default `FALSE` | Đánh dấu phương án có phải đáp án đúng hay không. | ERD V1; API contract |

## 10. `quiz_attempts` — Lần làm bài kiểm tra

### Mục đích và thông tin lưu trữ

Lưu mỗi phiên/lần người dùng làm một quiz, từ lúc bắt đầu đến lúc nộp, cùng
điểm và trạng thái xử lý.

### Quan hệ

- `quiz_attempts.quiz_id` → `quizzes.id`.
- `quiz_attempts.user_id` → `users.id`.
- `quiz_attempts.id` → `quiz_answers.attempt_id`.

### Method/query liên quan

| Trạng thái | Method/query | Loại | Mục đích và điều kiện | Nguồn |
|---|---|---|---|---|
| `DESIGN_ONLY` | API #29 `POST .../attempts` | `INSERT` | Tạo attempt cho user trên quiz. | [`docs/lists/list_api.md`](../lists/list_api.md) |
| `DESIGN_ONLY` | API #30 `PUT .../answers` | `SELECT`/`UPDATE` | Kiểm tra attempt và autosave answers. | [`docs/lists/list_api.md`](../lists/list_api.md) |
| `DESIGN_ONLY` | API #31 `POST .../submit` | `UPDATE` | Khóa attempt, chấm và chuyển trạng thái submit. | [`docs/lists/list_api.md`](../lists/list_api.md) |
| `DESIGN_ONLY` | API #32 `GET .../result` | `SELECT` | Đọc điểm/kết quả của attempt theo quyền xem. | [`docs/lists/list_api.md`](../lists/list_api.md) |
| `NOT_FOUND` | Table-specific runtime method | — | Chưa có implementation/query runtime được xác minh. | Source status hiện hành |

### Chi tiết trường

| Trường | Kiểu | Khóa/ràng buộc | Mô tả | Nguồn/trạng thái |
|---|---|---|---|---|
| `id` | `BIGSERIAL` | PK, bắt buộc | Định danh lần làm bài. | ERD V1 |
| `quiz_id` | `BIGINT` | FK → `quizzes.id`, bắt buộc | Quiz được thực hiện. | ERD V1; API contract |
| `user_id` | `BIGINT` | FK → `users.id`, bắt buộc | Người thực hiện attempt. | ERD V1; API contract |
| `started_at` | `TIMESTAMP` | Bắt buộc | Thời điểm bắt đầu làm bài. | ERD V1; API contract |
| `submitted_at` | `TIMESTAMP` | Nullable | Thời điểm nộp bài; null khi còn đang làm. | ERD V1; API contract |
| `score` | `NUMERIC(6,2)` | Nullable | Điểm tổng kết; null trước khi chấm/nộp. | ERD V1; API contract |
| `status` | `VARCHAR(20)` | Default `IN_PROGRESS` | Trạng thái vòng đời attempt. Các giá trị đầy đủ chưa được canonical hóa. | ERD V1; enum chưa đầy đủ |

## 11. `quiz_answers` — Câu trả lời trong lần làm bài

### Mục đích và thông tin lưu trữ

Lưu kết quả lựa chọn của người dùng cho từng question trong một attempt. ERD
hiện mô hình hóa answer thông qua `choice_id`; chưa có cột text answer.

### Quan hệ

- `quiz_answers.attempt_id` → `quiz_attempts.id`.
- `quiz_answers.question_id` → `quiz_questions.id`.
- `quiz_answers.choice_id` → `quiz_choices.id`.

### Method/query liên quan

| Trạng thái | Method/query | Loại | Mục đích và điều kiện | Nguồn |
|---|---|---|---|---|
| `DESIGN_ONLY` | API #30 `PUT .../answers` | `INSERT`/`UPDATE` | Lưu hoặc cập nhật câu trả lời trong attempt; question/choice phải thuộc quan hệ tương ứng. SQL cụ thể chưa có DD riêng. | [`docs/lists/list_api.md`](../lists/list_api.md) |
| `DESIGN_ONLY` | API #31 `.../submit` | `SELECT`/update | Đọc answers để chấm và cập nhật điểm/trạng thái attempt. | [`docs/lists/list_api.md`](../lists/list_api.md) |
| `DESIGN_ONLY` | API #32 `.../result` | `SELECT` | Đọc answers/kết quả được phép hiển thị. | [`docs/lists/list_api.md`](../lists/list_api.md) |
| `NOT_FOUND` | Table-specific runtime method | — | Chưa có implementation/query runtime được xác minh. | Source status hiện hành |

### Chi tiết trường

| Trường | Kiểu | Khóa/ràng buộc | Mô tả | Nguồn/trạng thái |
|---|---|---|---|---|
| `id` | `BIGSERIAL` | PK, bắt buộc | Định danh bản ghi answer. | ERD V1 |
| `attempt_id` | `BIGINT` | FK → `quiz_attempts.id`, bắt buộc | Attempt chứa câu trả lời. | ERD V1; API contract |
| `question_id` | `BIGINT` | FK → `quiz_questions.id`, bắt buộc | Câu hỏi được trả lời. | ERD V1; API contract |
| `choice_id` | `BIGINT` | FK → `quiz_choices.id`, bắt buộc | Lựa chọn mà user đã chọn. | ERD V1; API contract |
| `is_correct` | `BOOLEAN` | Bắt buộc | Kết quả đúng/sai của câu trả lời sau khi chấm. | ERD V1 |
| `score_received` | `NUMERIC(5,2)` | Default `0` | Điểm thực nhận cho câu trả lời. | ERD V1; API contract |

> **DISCREPANCY:** API contract logical `QuizAnswer` có thể mô tả
> `choice_ids` hoặc `text_answer`, nhưng ERD V1 chỉ có một `choice_id`; không
> mở rộng schema khi chưa có requirement/schema canonical.

## 12. `assignments` — Bài tập

### Mục đích và thông tin lưu trữ

Lưu đề bài thuộc khóa học, mô tả, hạn nộp và điểm tối đa.

### Quan hệ

- `assignments.course_id` → `courses.id`.
- `assignments.id` → `assignment_submissions.assignment_id`.

### Method/query liên quan

| Trạng thái | Method/query | Loại | Mục đích và điều kiện | Nguồn |
|---|---|---|---|---|
| `DESIGN_ONLY` | API #33 `GET /assignments/{assignment_id}` | `SELECT` | Đọc đề bài, rule/deadline và điểm tối đa. Query matrix chi tiết chưa có DD riêng. | [`docs/lists/list_api.md`](../lists/list_api.md) |
| `DESIGN_ONLY` | API #35 `POST .../submissions`, #36 `GET /submissions/{submission_id}` | `SELECT`/`INSERT` | Tạo và đọc bài nộp của student theo assignment. Mapping SQL cụ thể chưa được đặc tả. | [`docs/lists/list_api.md`](../lists/list_api.md) |
| `DESIGN_ONLY` | API #54–#57 | `SELECT`/`UPDATE` | Mentor đọc submissions, lưu điểm và feedback. Mapping SQL cụ thể chưa được đặc tả. | [`docs/lists/list_api.md`](../lists/list_api.md) |
| `NOT_FOUND` | Table-specific runtime method | — | Chưa có implementation/query runtime được xác minh. | Source status hiện hành |

### Chi tiết trường

| Trường | Kiểu | Khóa/ràng buộc | Mô tả | Nguồn/trạng thái |
|---|---|---|---|---|
| `id` | `BIGSERIAL` | PK, bắt buộc | Định danh bài tập. | ERD V1 |
| `course_id` | `BIGINT` | FK → `courses.id`, bắt buộc | Khóa học chứa bài tập. | ERD V1; API contract |
| `name` | `VARCHAR(200)` | Bắt buộc | Tên bài tập; logical contract dùng `Assignment.title`. | ERD V1; API contract |
| `description` | `TEXT` | Nullable | Nội dung/yêu cầu của bài tập. | ERD V1; API contract |
| `due_at` | `TIMESTAMP` | Nullable | Hạn nộp bài tập; null nếu không có deadline. | ERD V1; API contract |
| `max_score` | `NUMERIC(6,2)` | Default `10` | Điểm tối đa dùng để chấm bài nộp. | ERD V1; API contract |
| `created_at` | `TIMESTAMP` | Bắt buộc | Thời điểm tạo bài tập. | ERD V1 |
| `updated_at` | `TIMESTAMP` | Bắt buộc | Thời điểm cập nhật bài tập. | ERD V1 |

## 13. `assignment_submissions` — Bài nộp bài tập

### Mục đích và thông tin lưu trữ

Lưu bài nộp của user cho assignment, có thể gồm nội dung text hoặc URL file,
cùng kết quả chấm và feedback.

### Quan hệ

- `assignment_submissions.assignment_id` → `assignments.id`.
- `assignment_submissions.user_id` → `users.id`.

### Method/query liên quan

| Trạng thái | Method/query | Loại | Mục đích và điều kiện | Nguồn |
|---|---|---|---|---|
| `DESIGN_ONLY` | API #35, #36, #54–#57 | `SELECT`/`INSERT`/`UPDATE` | Tạo, xem hoặc chấm bài nộp theo assignment/user; endpoint/query matrix chi tiết chưa có DD riêng. | [`docs/lists/list_api.md`](../lists/list_api.md) |
| `NOT_FOUND` | Table-specific runtime method | — | Chưa có implementation/query runtime được xác minh. | Source status hiện hành |

### Chi tiết trường

| Trường | Kiểu | Khóa/ràng buộc | Mô tả | Nguồn/trạng thái |
|---|---|---|---|---|
| `id` | `BIGSERIAL` | PK, bắt buộc | Định danh bài nộp. | ERD V1 |
| `assignment_id` | `BIGINT` | FK → `assignments.id`, bắt buộc | Bài tập được nộp. | ERD V1; API contract |
| `user_id` | `BIGINT` | FK → `users.id`, bắt buộc | Người nộp bài. | ERD V1; API contract |
| `content` | `TEXT` | Nullable | Nội dung text của bài nộp nếu có. | ERD V1; API contract |
| `file_url` | `TEXT` | Nullable | URL file bài nộp nếu có. | ERD V1; API contract |
| `submitted_at` | `TIMESTAMP` | Bắt buộc | Thời điểm gửi bài nộp. | ERD V1; API contract |
| `score` | `NUMERIC(6,2)` | Nullable | Điểm được chấm; null khi chưa chấm. | ERD V1; API contract |
| `feedback` | `TEXT` | Nullable | Nhận xét/phản hồi của người chấm. | ERD V1; API contract |
| `status` | `VARCHAR(20)` | Default `SUBMITTED` | Trạng thái bài nộp trong flow chấm. Enum đầy đủ chưa được đặc tả. | ERD V1 |

## 14. `discussions` — Thảo luận / đánh giá

### Mục đích và thông tin lưu trữ

Lưu nội dung thảo luận/review trong một khóa học. `parent_id` cho phép mô hình
hóa reply dạng self-reference: row không có parent là thread/review gốc, row có
parent là comment/reply.

### Quan hệ

- `discussions.course_id` → `courses.id`.
- `discussions.user_id` → `users.id`.
- `discussions.parent_id` → `discussions.id` và nullable.

### Method/query liên quan

| Trạng thái | Method/query | Loại | Mục đích và điều kiện | Nguồn |
|---|---|---|---|---|
| `DESIGN_ONLY` | `Q1` của API #10 | `SELECT` | Gate `courses.id = :course_id` và `courses.status = 'PUBLISHED'`. | [`docs/dd/10_courses_reviews/05_Data_Mapping.md`](../dd/10_courses_reviews/05_Data_Mapping.md) |
| `DESIGN_ONLY` | `Q2` của API #10 | `SELECT` + author join | Đọc `d.id`, `d.course_id`, `d.user_id`, `d.content`, `d.status`, `d.created_at` cho review gốc; lọc `course_id`, `parent_id IS NULL`, `status = 'ACTIVE'`, sort/pagination design-only; join `u.id`, `u.full_name`, `u.avatar_url`. | [`docs/dd/10_courses_reviews/05_Data_Mapping.md`](../dd/10_courses_reviews/05_Data_Mapping.md) |
| `DESIGN_ONLY` | `Q3` của API #10 | `SELECT` + author join | Đọc `r.id`, `r.parent_id`, `r.user_id`, `r.content`, `r.created_at` cho replies với `parent_id IN (:review_ids)` và `status = 'ACTIVE'`; join `cu.id`, `cu.full_name`, `cu.avatar_url`. | [`docs/dd/10_courses_reviews/05_Data_Mapping.md`](../dd/10_courses_reviews/05_Data_Mapping.md) |
| `DESIGN_ONLY` | `Q4` của API #10 | `COUNT` | Đếm review gốc theo cùng scope/visibility predicate với Q2. | [`docs/dd/10_courses_reviews/05_Data_Mapping.md`](../dd/10_courses_reviews/05_Data_Mapping.md) |
| `DESIGN_ONLY` | API #39–#42 | `SELECT`/`INSERT` | Student đọc thread, tạo topic/reply và reload thread; mapping SQL chi tiết chưa có DD riêng. | [`docs/lists/list_api.md`](../lists/list_api.md) |
| `DESIGN_ONLY` | API #97–#100 | `SELECT`/`UPDATE`/`DELETE` | Contract admin cho reported discussions, moderation và delete; query matrix chi tiết chưa có DD riêng. | [`docs/lists/list_api.md`](../lists/list_api.md) |
| `NOT_FOUND` | Table-specific runtime method | — | Chưa có implementation/query runtime được xác minh. | Source status hiện hành |

### Chi tiết trường

| Trường | Kiểu | Khóa/ràng buộc | Mô tả | Nguồn/trạng thái |
|---|---|---|---|---|
| `id` | `BIGSERIAL` | PK, bắt buộc | Định danh discussion/review/reply. | ERD V1; DD API #10 |
| `course_id` | `BIGINT` | FK → `courses.id`, bắt buộc | Khóa học chứa discussion. | ERD V1; DD API #10 |
| `user_id` | `BIGINT` | FK → `users.id`, bắt buộc | Tác giả discussion. | ERD V1; DD API #10 |
| `parent_id` | `BIGINT` | FK → `discussions.id`, nullable | Discussion cha; null nghĩa là thread/review gốc. | ERD V1; DD API #10 |
| `content` | `TEXT` | Bắt buộc | Nội dung review, bài thảo luận hoặc reply. | ERD V1; DD API #10 |
| `status` | `VARCHAR(20)` | Default `ACTIVE` | Trạng thái hiển thị/moderation. Query review design lọc `ACTIVE`. | ERD V1; DD API #10 |
| `created_at` | `TIMESTAMP` | Bắt buộc | Thời điểm tạo discussion. | ERD V1; DD API #10 |
| `updated_at` | `TIMESTAMP` | Bắt buộc | Thời điểm cập nhật discussion. | ERD V1 |

> **DISCREPANCY:** Một số contract logical đề cập `discussions.title` hoặc
> rating, nhưng ERD hiện không có cột `title` hoặc cột/bảng rating. Không tự
> thêm field hoặc rating predicate.

## 15. `notifications` — Thông báo

### Mục đích và thông tin lưu trữ

Lưu nội dung thông báo, người nhận/người gửi, loại thông báo và cờ đã đọc.
Hai FK tới `users` cho phép notification có người nhận cụ thể hoặc người gửi
hệ thống/người dùng.

### Quan hệ

- `notifications.user_id` → `users.id`, nullable.
- `notifications.sender_id` → `users.id`, nullable.

### Method/query liên quan

| Trạng thái | Method/query | Loại | Mục đích và điều kiện | Nguồn |
|---|---|---|---|---|
| `DESIGN_ONLY` | API #43 `GET /users/me/notifications` | `SELECT` | Đọc notification của user, có filter unread/page theo contract. Physical query chưa có DD riêng. | [`docs/lists/list_api.md`](../lists/list_api.md) |
| `DESIGN_ONLY` | API #44–#45 | `UPDATE` | Đánh dấu một hoặc tất cả notification đã đọc. Query matrix chi tiết chưa có DD riêng. | [`docs/lists/list_api.md`](../lists/list_api.md) |
| `DESIGN_ONLY` | API #63–#64 | `INSERT`/external dispatch/`SELECT` | Mentor tạo/phát notification và theo dõi trạng thái gửi; dispatch có thể trả operation bất đồng bộ. | [`docs/lists/list_api.md`](../lists/list_api.md) |
| `DESIGN_ONLY` | API #92–#96 | `SELECT`/`INSERT`/`UPDATE`/`DELETE` | Admin đọc, tạo/phát, cập nhật, xóa/cancel và xem delivery status. Query matrix chi tiết chưa có DD riêng. | [`docs/lists/list_api.md`](../lists/list_api.md) |
| `NOT_FOUND` | Table-specific runtime method | — | Chưa có implementation/query runtime được xác minh. | Source status hiện hành |

### Chi tiết trường

| Trường | Kiểu | Khóa/ràng buộc | Mô tả | Nguồn/trạng thái |
|---|---|---|---|---|
| `id` | `BIGSERIAL` | PK, bắt buộc | Định danh notification. | ERD V1 |
| `user_id` | `BIGINT` | FK → `users.id`, nullable | Người nhận notification; nullable cho trường hợp broadcast/segment theo design. | ERD V1; API contract |
| `sender_id` | `BIGINT` | FK → `users.id`, nullable | Người gửi hoặc actor tạo notification; nullable khi hệ thống gửi. | ERD V1; API contract |
| `title` | `VARCHAR(200)` | Bắt buộc | Tiêu đề hiển thị. | ERD V1; API contract |
| `content` | `TEXT` | Bắt buộc | Nội dung thông báo. | ERD V1; API contract |
| `type` | `VARCHAR(30)` | Nullable | Phân loại notification; danh mục giá trị chưa được đặc tả trong ERD. | ERD V1 |
| `is_read` | `BOOLEAN` | Default `FALSE` | Cho biết người nhận đã đọc notification hay chưa. | ERD V1 |
| `created_at` | `TIMESTAMP` | Bắt buộc | Thời điểm tạo notification. | ERD V1; API contract |

## 16. `payments` — Thanh toán

### Mục đích và thông tin lưu trữ

Lưu giao dịch thanh toán của người dùng cho khóa học, gồm số tiền, provider,
mã giao dịch, trạng thái và thời điểm thanh toán thành công.

### Quan hệ

- `payments.user_id` → `users.id`.
- `payments.course_id` → `courses.id`.

### Method/query liên quan

| Trạng thái | Method/query | Loại | Mục đích và điều kiện | Nguồn |
|---|---|---|---|---|
| `DESIGN_ONLY` | API #17 `POST /payments` | `INSERT`/external payment | Khởi tạo hoặc xác nhận payment cho course; provider xử lý external và có thể trả operation. | [`docs/lists/list_api.md`](../lists/list_api.md) |
| `DESIGN_ONLY` | API #16 `POST /orders` và API #19 enrollment | `SELECT`/liên kết | Payment liên quan tới course/user trong flow tạo order và cấp quyền học; ERD không có bảng `orders`. | [`docs/lists/list_api.md`](../lists/list_api.md) |
| `NOT_FOUND` | Table-specific runtime method | — | Chưa có implementation/query runtime được xác minh. | Source status hiện hành |

### Chi tiết trường

| Trường | Kiểu | Khóa/ràng buộc | Mô tả | Nguồn/trạng thái |
|---|---|---|---|---|
| `id` | `BIGSERIAL` | PK, bắt buộc | Định danh bản ghi thanh toán. | ERD V1 |
| `user_id` | `BIGINT` | FK → `users.id`, bắt buộc | Người thực hiện thanh toán. | ERD V1; API contract |
| `course_id` | `BIGINT` | FK → `courses.id`, bắt buộc | Khóa học được thanh toán. | ERD V1; API contract |
| `amount` | `NUMERIC(12,2)` | Bắt buộc | Số tiền của giao dịch; contract serialize dưới dạng decimal string. | ERD V1; API contract |
| `provider` | `VARCHAR(50)` | Bắt buộc | Nhà cung cấp/cổng thanh toán. | ERD V1; API contract |
| `transaction_code` | `VARCHAR(100)` | UNIQUE | Mã giao dịch từ provider hoặc hệ thống thanh toán. | ERD V1; API contract |
| `status` | `VARCHAR(20)` | Default `PENDING` | Trạng thái xử lý thanh toán. Enum đầy đủ chưa được đặc tả. | ERD V1; API contract |
| `paid_at` | `TIMESTAMP` | Nullable | Thời điểm payment thành công; null khi pending/failed hoặc chưa xác nhận. | ERD V1; API contract |
| `created_at` | `TIMESTAMP` | Bắt buộc | Thời điểm tạo bản ghi payment. | ERD V1 |

## Tổng hợp discrepancy và giới hạn sử dụng

1. 16 bảng trong tài liệu là cấu trúc `ERD V1`; context database hiện hành không
   xác nhận đây là schema đang chạy của Study, Work hoặc AI.
2. Work runtime hiện chỉ có `system_records`, không có domain model tương ứng
   với ERD UNICA. Readiness query `SELECT 1` không chứng minh bảng nghiệp vụ tồn
   tại.
3. Study và AI có helper truy vấn generic, nhưng không có table-specific
   repository/service được xác minh. Study runtime còn có import blocker; AI
   database core là copied/unwired.
4. Các query trong DD là design contract. Chúng mô tả intended data flow cho
   API, không phải bằng chứng method đã được implement hoặc endpoint đã runnable.
5. `categories`, `orders`, `content`, `uploads`, `achievements` và các bảng
   logical khác được API contract nhắc tới nhưng không nằm trong 16 bảng của ERD
   này; tài liệu không tự bổ sung chúng vào schema.

## Nguồn tham chiếu

- [`DB_UNICA_ERD.drawio`](./DB_UNICA_ERD.drawio)
- [`AGENTS.md`](../../AGENTS.md)
- [Project database context](../../.agents/project/database.md)
- [Project source status](../../.agents/project/source-status.md)
- [Study database context](../../.agents/server-study/database.md)
- [Work database context](../../.agents/server-work/database.md)
- [AI database context](../../.agents/server-ai/database.md)
- [`docs/dd/` API data mappings](../dd/)
- [`docs/lists/list_api.md`](../lists/list_api.md)
