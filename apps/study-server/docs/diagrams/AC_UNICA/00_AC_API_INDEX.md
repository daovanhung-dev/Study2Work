# AC / API INDEX — ONLINE LEARNING SYSTEM

## Quy ước

- **1 UC = 1 AC**.
- **1 AC có thể chứa nhiều API**.
- Endpoint trong bộ AC là thiết kế REST đề xuất theo plan hiện tại.

## Tổng quan

- Tổng UC/AC: **30**
- Tổng API unique: **103**
- GUEST / ACCOUNT & DISCOVERY: **6 AC**
- STUDENT / LEARNING & INTERACTION: **10 AC**
- MENTOR / TEACHING & SUPPORT: **6 AC**
- ADMIN / SYSTEM MANAGEMENT: **8 AC**

## AC → API

### GUEST / ACCOUNT & DISCOVERY

#### AC-01 — Đăng ký tài khoản

- Actor: `Guest`
- Precondition: Người dùng chưa đăng nhập; email chưa được sử dụng.
- Postcondition: Tài khoản được tạo; có thể chuyển sang xác thực email/đăng nhập.
- APIs:
  - `POST /api/v1/auth/register`
  - `POST /api/v1/auth/verify-email/send`

#### AC-02 — Đăng nhập

- Actor: `Guest`
- Precondition: Tài khoản đã tồn tại và không bị khóa.
- Postcondition: Client nhận token, profile và điều hướng theo role.
- APIs:
  - `POST /api/v1/auth/login`
  - `GET /api/v1/users/me`

#### AC-03 — Xem danh sách khóa học

- Actor: `Guest`
- Precondition: Hệ thống có khóa học ở trạng thái công khai.
- Postcondition: Danh sách khóa học được hiển thị theo filter/pagination.
- APIs:
  - `GET /api/v1/categories`
  - `GET /api/v1/courses`

#### AC-04 — Tìm kiếm khóa học

- Actor: `Guest`
- Precondition: Người dùng đang ở khu vực khám phá khóa học.
- Postcondition: Kết quả tìm kiếm phù hợp từ khóa/bộ lọc được hiển thị.
- APIs:
  - `GET /api/v1/categories`
  - `GET /api/v1/courses/search`

#### AC-05 — Xem chi tiết khóa học

- Actor: `Guest`
- Precondition: course_id hợp lệ và khóa học công khai.
- Postcondition: Trang chi tiết tổng hợp course, curriculum và reviews.
- APIs:
  - `GET /api/v1/courses/{course_id}`
  - `GET /api/v1/courses/{course_id}/curriculum`
  - `GET /api/v1/courses/{course_id}/reviews`

#### AC-06 — Xem tài nguyên

- Actor: `Guest`
- Precondition: Tài nguyên được phép xem public hoặc user có quyền truy cập.
- Postcondition: Tài nguyên/file URL hợp lệ được mở hoặc tải xuống.
- APIs:
  - `GET /api/v1/courses/{course_id}/resources`
  - `GET /api/v1/resources/{resource_id}`

### STUDENT / LEARNING & INTERACTION

#### AC-11 — Quản lý hồ sơ cá nhân

- Actor: `Student`
- Precondition: Student đã đăng nhập.
- Postcondition: Profile/avatar được cập nhật và phản ánh trên UI.
- APIs:
  - `GET /api/v1/users/me`
  - `PUT /api/v1/users/me/profile`
  - `POST /api/v1/users/me/avatar`

#### AC-12 — Đăng ký khóa học

- Actor: `Student`
- Precondition: Student đăng nhập; course tồn tại.
- Postcondition: Enrollment được tạo; khóa học xuất hiện trong danh sách của Student.
- APIs:
  - `GET /api/v1/courses/{course_id}`
  - `GET /api/v1/courses/{course_id}/enrollment-status`
  - `POST /api/v1/orders`
  - `POST /api/v1/payments`
  - `GET /api/v1/operations/{operation_id}`
  - `POST /api/v1/courses/{course_id}/enrollments`
  - `GET /api/v1/users/me/courses`

#### AC-13 — Xem khóa học đã đăng ký

- Actor: `Student`
- Precondition: Student đã đăng nhập và có thể có enrollment.
- Postcondition: Danh sách khóa học kèm tiến độ được hiển thị.
- APIs:
  - `GET /api/v1/users/me/courses`
  - `GET /api/v1/users/me/progress`

#### AC-14 — Học bài học

- Actor: `Student`
- Precondition: Student đã enrolled vào course chứa lesson.
- Postcondition: Lesson được mở; tiến độ được lưu khi học/hoàn thành.
- APIs:
  - `GET /api/v1/lessons/{lesson_id}/access`
  - `POST /api/v1/lessons/{lesson_id}/start`
  - `GET /api/v1/lessons/{lesson_id}`
  - `PATCH /api/v1/lessons/{lesson_id}/progress`

#### AC-15 — Xem nội dung bài học

- Actor: `Student`
- Precondition: Student có quyền xem lesson.
- Postcondition: Nội dung, tài nguyên và điều hướng bài tiếp theo được hiển thị.
- APIs:
  - `GET /api/v1/lessons/{lesson_id}`
  - `GET /api/v1/lessons/{lesson_id}/resources`
  - `GET /api/v1/lessons/{lesson_id}/next`

#### AC-16 — Làm bài kiểm tra

- Actor: `Student`
- Precondition: Student có quyền làm quiz; quiz đang mở.
- Postcondition: Attempt được nộp; kết quả/ trạng thái chấm được trả về.
- APIs:
  - `GET /api/v1/quizzes/{quiz_id}`
  - `POST /api/v1/quizzes/{quiz_id}/attempts`
  - `PUT /api/v1/attempts/{attempt_id}/answers`
  - `POST /api/v1/attempts/{attempt_id}/submit`
  - `GET /api/v1/attempts/{attempt_id}/result`

#### AC-17 — Nộp bài tập

- Actor: `Student`
- Precondition: Assignment còn hạn và Student có quyền nộp.
- Postcondition: Submission được tạo và có trạng thái nhận bài.
- APIs:
  - `GET /api/v1/assignments/{assignment_id}`
  - `POST /api/v1/uploads`
  - `POST /api/v1/assignments/{assignment_id}/submissions`
  - `GET /api/v1/submissions/{submission_id}`

#### AC-18 — Theo dõi tiến độ học tập

- Actor: `Student`
- Precondition: Student đã đăng nhập.
- Postcondition: Dashboard tiến độ và thành tích được hiển thị.
- APIs:
  - `GET /api/v1/users/me/progress`
  - `GET /api/v1/users/me/progress/{course_id}`
  - `GET /api/v1/users/me/achievements`

#### AC-19 — Đặt câu hỏi / Thảo luận

- Actor: `Student`
- Precondition: Student đăng nhập; có quyền tham gia discussion của course.
- Postcondition: Topic/comment được tạo và thread được cập nhật.
- APIs:
  - `GET /api/v1/discussions`
  - `POST /api/v1/discussions`
  - `POST /api/v1/discussions/{discussion_id}/comments`
  - `GET /api/v1/discussions/{discussion_id}`

#### AC-20 — Nhận thông báo

- Actor: `Student`
- Precondition: Student đã đăng nhập.
- Postcondition: Danh sách thông báo/read state được đồng bộ.
- APIs:
  - `GET /api/v1/users/me/notifications`
  - `PATCH /api/v1/notifications/{notification_id}/read`
  - `PATCH /api/v1/notifications/read-all`

### MENTOR / TEACHING & SUPPORT

#### AC-21 — Đăng bài giảng

- Actor: `Mentor`
- Precondition: Mentor đăng nhập và sở hữu/được phân công course.
- Postcondition: Lecture mới được tạo và hiển thị trong course.
- APIs:
  - `GET /api/v1/mentor/courses`
  - `POST /api/v1/uploads`
  - `POST /api/v1/mentor/courses/{course_id}/lectures`
  - `GET /api/v1/mentor/lectures/{lecture_id}`

#### AC-22 — Quản lý nội dung

- Actor: `Mentor`
- Precondition: Mentor có quyền quản lý course.
- Postcondition: Nội dung được tạo/cập nhật/xóa/publish theo thao tác.
- APIs:
  - `GET /api/v1/mentor/courses/{course_id}/content`
  - `POST /api/v1/mentor/content`
  - `PUT /api/v1/mentor/content/{content_id}`
  - `DELETE /api/v1/mentor/content/{content_id}`
  - `PATCH /api/v1/mentor/content/{content_id}/publish`

#### AC-23 — Chấm bài

- Actor: `Mentor`
- Precondition: Mentor có quyền chấm submission của course.
- Postcondition: Điểm và feedback được lưu; Student có thể nhận kết quả.
- APIs:
  - `GET /api/v1/mentor/submissions`
  - `GET /api/v1/mentor/submissions/{submission_id}`
  - `POST /api/v1/mentor/submissions/{submission_id}/grade`
  - `POST /api/v1/mentor/submissions/{submission_id}/feedback`

#### AC-24 — Hỗ trợ học viên

- Actor: `Mentor`
- Precondition: Mentor có request hỗ trợ thuộc phạm vi phụ trách.
- Postcondition: Phản hồi được gửi và request có thể được resolved.
- APIs:
  - `GET /api/v1/mentor/support/requests`
  - `GET /api/v1/mentor/support/{request_id}`
  - `POST /api/v1/mentor/support/{request_id}/reply`
  - `PATCH /api/v1/mentor/support/{request_id}/resolve`

#### AC-25 — Gửi thông báo

- Actor: `Mentor`
- Precondition: Mentor có quyền gửi thông báo tới học viên thuộc course.
- Postcondition: Notification được tạo và trạng thái phát được theo dõi.
- APIs:
  - `GET /api/v1/mentor/courses/{course_id}/students`
  - `POST /api/v1/mentor/notifications`
  - `GET /api/v1/operations/{operation_id}`
  - `GET /api/v1/mentor/notifications/{notification_id}/status`

#### AC-26 — Theo dõi tiến độ

- Actor: `Mentor`
- Precondition: Mentor có quyền xem analytics của course.
- Postcondition: Tiến độ lớp, từng Student và analytics được hiển thị.
- APIs:
  - `GET /api/v1/mentor/courses/{course_id}/progress`
  - `GET /api/v1/mentor/courses/{course_id}/students/{student_id}/progress`
  - `GET /api/v1/mentor/courses/{course_id}/analytics`

### ADMIN / SYSTEM MANAGEMENT

#### AC-31 — Quản lý người dùng

- Actor: `Admin`
- Precondition: Admin đăng nhập và có quyền user management.
- Postcondition: Danh sách/chi tiết user được cập nhật theo thao tác quản trị.
- APIs:
  - `GET /api/v1/admin/users`
  - `GET /api/v1/admin/users/{user_id}`
  - `PUT /api/v1/admin/users/{user_id}`
  - `PATCH /api/v1/admin/users/{user_id}/status`
  - `DELETE /api/v1/admin/users/{user_id}`

#### AC-32 — Quản lý khóa học

- Actor: `Admin`
- Precondition: Admin có quyền course management.
- Postcondition: Course được cập nhật trạng thái/nội dung quản trị hoặc xóa theo policy.
- APIs:
  - `GET /api/v1/admin/courses`
  - `GET /api/v1/admin/courses/{course_id}`
  - `PUT /api/v1/admin/courses/{course_id}`
  - `PATCH /api/v1/admin/courses/{course_id}/status`
  - `DELETE /api/v1/admin/courses/{course_id}`

#### AC-33 — Duyệt nội dung

- Actor: `Admin`
- Precondition: Có content ở trạng thái pending review.
- Postcondition: Content được approve hoặc reject với lý do.
- APIs:
  - `GET /api/v1/admin/content/pending`
  - `GET /api/v1/admin/content/{content_id}`
  - `PATCH /api/v1/admin/content/{content_id}/approve`
  - `PATCH /api/v1/admin/content/{content_id}/reject`

#### AC-34 — Quản lý bài học

- Actor: `Admin`
- Precondition: Admin có lesson management permission.
- Postcondition: Lesson được cập nhật/trạng thái thay đổi/xóa theo thao tác.
- APIs:
  - `GET /api/v1/admin/lessons`
  - `GET /api/v1/admin/lessons/{lesson_id}`
  - `PUT /api/v1/admin/lessons/{lesson_id}`
  - `PATCH /api/v1/admin/lessons/{lesson_id}/status`
  - `DELETE /api/v1/admin/lessons/{lesson_id}`

#### AC-35 — Quản lý kiểm tra

- Actor: `Admin`
- Precondition: Admin có quiz management permission.
- Postcondition: Quiz được tạo/cập nhật/xóa; statistics có thể được xem.
- APIs:
  - `GET /api/v1/admin/quizzes`
  - `POST /api/v1/admin/quizzes`
  - `PUT /api/v1/admin/quizzes/{quiz_id}`
  - `DELETE /api/v1/admin/quizzes/{quiz_id}`
  - `GET /api/v1/admin/quizzes/{quiz_id}/statistics`

#### AC-36 — Quản lý thông báo

- Actor: `Admin`
- Precondition: Admin có notification management permission.
- Postcondition: Notification được tạo/cập nhật/xóa và theo dõi trạng thái.
- APIs:
  - `GET /api/v1/admin/notifications`
  - `POST /api/v1/admin/notifications`
  - `GET /api/v1/operations/{operation_id}`
  - `PUT /api/v1/admin/notifications/{notification_id}`
  - `DELETE /api/v1/admin/notifications/{notification_id}`
  - `GET /api/v1/admin/notifications/{notification_id}/status`

#### AC-37 — Kiểm duyệt ý kiến

- Actor: `Admin`
- Precondition: Có discussion bị report hoặc cần moderation.
- Postcondition: Discussion được giữ/ẩn/khóa/xóa theo quyết định moderation.
- APIs:
  - `GET /api/v1/admin/discussions/reported`
  - `GET /api/v1/admin/discussions/{discussion_id}`
  - `PATCH /api/v1/admin/discussions/{discussion_id}/moderate`
  - `DELETE /api/v1/admin/discussions/{discussion_id}`

#### AC-38 — Báo cáo tác động cộng đồng

- Actor: `Admin`
- Precondition: Admin có quyền xem báo cáo/analytics.
- Postcondition: Báo cáo tổng hợp được hiển thị hoặc export.
- APIs:
  - `GET /api/v1/admin/reports/summary`
  - `GET /api/v1/admin/reports/community-impact`
  - `GET /api/v1/admin/reports/community-impact/export`
  - `GET /api/v1/operations/{operation_id}`

## API → AC / UC

| Method | Endpoint | AC / UC sử dụng |
|---|---|---|
| `GET` | `/api/v1/admin/content/pending` | **AC-33** — Duyệt nội dung |
| `GET` | `/api/v1/admin/content/{content_id}` | **AC-33** — Duyệt nội dung |
| `PATCH` | `/api/v1/admin/content/{content_id}/approve` | **AC-33** — Duyệt nội dung |
| `PATCH` | `/api/v1/admin/content/{content_id}/reject` | **AC-33** — Duyệt nội dung |
| `GET` | `/api/v1/admin/courses` | **AC-32** — Quản lý khóa học |
| `DELETE` | `/api/v1/admin/courses/{course_id}` | **AC-32** — Quản lý khóa học |
| `GET` | `/api/v1/admin/courses/{course_id}` | **AC-32** — Quản lý khóa học |
| `PUT` | `/api/v1/admin/courses/{course_id}` | **AC-32** — Quản lý khóa học |
| `PATCH` | `/api/v1/admin/courses/{course_id}/status` | **AC-32** — Quản lý khóa học |
| `GET` | `/api/v1/admin/discussions/reported` | **AC-37** — Kiểm duyệt ý kiến |
| `DELETE` | `/api/v1/admin/discussions/{discussion_id}` | **AC-37** — Kiểm duyệt ý kiến |
| `GET` | `/api/v1/admin/discussions/{discussion_id}` | **AC-37** — Kiểm duyệt ý kiến |
| `PATCH` | `/api/v1/admin/discussions/{discussion_id}/moderate` | **AC-37** — Kiểm duyệt ý kiến |
| `GET` | `/api/v1/admin/lessons` | **AC-34** — Quản lý bài học |
| `DELETE` | `/api/v1/admin/lessons/{lesson_id}` | **AC-34** — Quản lý bài học |
| `GET` | `/api/v1/admin/lessons/{lesson_id}` | **AC-34** — Quản lý bài học |
| `PUT` | `/api/v1/admin/lessons/{lesson_id}` | **AC-34** — Quản lý bài học |
| `PATCH` | `/api/v1/admin/lessons/{lesson_id}/status` | **AC-34** — Quản lý bài học |
| `GET` | `/api/v1/admin/notifications` | **AC-36** — Quản lý thông báo |
| `POST` | `/api/v1/admin/notifications` | **AC-36** — Quản lý thông báo |
| `DELETE` | `/api/v1/admin/notifications/{notification_id}` | **AC-36** — Quản lý thông báo |
| `PUT` | `/api/v1/admin/notifications/{notification_id}` | **AC-36** — Quản lý thông báo |
| `GET` | `/api/v1/admin/notifications/{notification_id}/status` | **AC-36** — Quản lý thông báo |
| `GET` | `/api/v1/admin/quizzes` | **AC-35** — Quản lý kiểm tra |
| `POST` | `/api/v1/admin/quizzes` | **AC-35** — Quản lý kiểm tra |
| `DELETE` | `/api/v1/admin/quizzes/{quiz_id}` | **AC-35** — Quản lý kiểm tra |
| `PUT` | `/api/v1/admin/quizzes/{quiz_id}` | **AC-35** — Quản lý kiểm tra |
| `GET` | `/api/v1/admin/quizzes/{quiz_id}/statistics` | **AC-35** — Quản lý kiểm tra |
| `GET` | `/api/v1/admin/reports/community-impact` | **AC-38** — Báo cáo tác động cộng đồng |
| `GET` | `/api/v1/admin/reports/community-impact/export` | **AC-38** — Báo cáo tác động cộng đồng |
| `GET` | `/api/v1/admin/reports/summary` | **AC-38** — Báo cáo tác động cộng đồng |
| `GET` | `/api/v1/admin/users` | **AC-31** — Quản lý người dùng |
| `DELETE` | `/api/v1/admin/users/{user_id}` | **AC-31** — Quản lý người dùng |
| `GET` | `/api/v1/admin/users/{user_id}` | **AC-31** — Quản lý người dùng |
| `PUT` | `/api/v1/admin/users/{user_id}` | **AC-31** — Quản lý người dùng |
| `PATCH` | `/api/v1/admin/users/{user_id}/status` | **AC-31** — Quản lý người dùng |
| `GET` | `/api/v1/assignments/{assignment_id}` | **AC-17** — Nộp bài tập |
| `POST` | `/api/v1/assignments/{assignment_id}/submissions` | **AC-17** — Nộp bài tập |
| `PUT` | `/api/v1/attempts/{attempt_id}/answers` | **AC-16** — Làm bài kiểm tra |
| `GET` | `/api/v1/attempts/{attempt_id}/result` | **AC-16** — Làm bài kiểm tra |
| `POST` | `/api/v1/attempts/{attempt_id}/submit` | **AC-16** — Làm bài kiểm tra |
| `POST` | `/api/v1/auth/login` | **AC-02** — Đăng nhập |
| `POST` | `/api/v1/auth/register` | **AC-01** — Đăng ký tài khoản |
| `POST` | `/api/v1/auth/verify-email/send` | **AC-01** — Đăng ký tài khoản |
| `GET` | `/api/v1/categories` | **AC-03** — Xem danh sách khóa học<br>**AC-04** — Tìm kiếm khóa học |
| `GET` | `/api/v1/courses` | **AC-03** — Xem danh sách khóa học |
| `GET` | `/api/v1/courses/search` | **AC-04** — Tìm kiếm khóa học |
| `GET` | `/api/v1/courses/{course_id}` | **AC-05** — Xem chi tiết khóa học<br>**AC-12** — Đăng ký khóa học |
| `GET` | `/api/v1/courses/{course_id}/curriculum` | **AC-05** — Xem chi tiết khóa học |
| `GET` | `/api/v1/courses/{course_id}/enrollment-status` | **AC-12** — Đăng ký khóa học |
| `POST` | `/api/v1/courses/{course_id}/enrollments` | **AC-12** — Đăng ký khóa học |
| `GET` | `/api/v1/courses/{course_id}/resources` | **AC-06** — Xem tài nguyên |
| `GET` | `/api/v1/courses/{course_id}/reviews` | **AC-05** — Xem chi tiết khóa học |
| `GET` | `/api/v1/discussions` | **AC-19** — Đặt câu hỏi / Thảo luận |
| `POST` | `/api/v1/discussions` | **AC-19** — Đặt câu hỏi / Thảo luận |
| `GET` | `/api/v1/discussions/{discussion_id}` | **AC-19** — Đặt câu hỏi / Thảo luận |
| `POST` | `/api/v1/discussions/{discussion_id}/comments` | **AC-19** — Đặt câu hỏi / Thảo luận |
| `GET` | `/api/v1/lessons/{lesson_id}` | **AC-14** — Học bài học<br>**AC-15** — Xem nội dung bài học |
| `GET` | `/api/v1/lessons/{lesson_id}/access` | **AC-14** — Học bài học |
| `GET` | `/api/v1/lessons/{lesson_id}/next` | **AC-15** — Xem nội dung bài học |
| `PATCH` | `/api/v1/lessons/{lesson_id}/progress` | **AC-14** — Học bài học |
| `GET` | `/api/v1/lessons/{lesson_id}/resources` | **AC-15** — Xem nội dung bài học |
| `POST` | `/api/v1/lessons/{lesson_id}/start` | **AC-14** — Học bài học |
| `POST` | `/api/v1/mentor/content` | **AC-22** — Quản lý nội dung |
| `DELETE` | `/api/v1/mentor/content/{content_id}` | **AC-22** — Quản lý nội dung |
| `PUT` | `/api/v1/mentor/content/{content_id}` | **AC-22** — Quản lý nội dung |
| `PATCH` | `/api/v1/mentor/content/{content_id}/publish` | **AC-22** — Quản lý nội dung |
| `GET` | `/api/v1/mentor/courses` | **AC-21** — Đăng bài giảng |
| `GET` | `/api/v1/mentor/courses/{course_id}/analytics` | **AC-26** — Theo dõi tiến độ |
| `GET` | `/api/v1/mentor/courses/{course_id}/content` | **AC-22** — Quản lý nội dung |
| `POST` | `/api/v1/mentor/courses/{course_id}/lectures` | **AC-21** — Đăng bài giảng |
| `GET` | `/api/v1/mentor/courses/{course_id}/progress` | **AC-26** — Theo dõi tiến độ |
| `GET` | `/api/v1/mentor/courses/{course_id}/students` | **AC-25** — Gửi thông báo |
| `GET` | `/api/v1/mentor/courses/{course_id}/students/{student_id}/progress` | **AC-26** — Theo dõi tiến độ |
| `GET` | `/api/v1/mentor/lectures/{lecture_id}` | **AC-21** — Đăng bài giảng |
| `POST` | `/api/v1/mentor/notifications` | **AC-25** — Gửi thông báo |
| `GET` | `/api/v1/mentor/notifications/{notification_id}/status` | **AC-25** — Gửi thông báo |
| `GET` | `/api/v1/mentor/submissions` | **AC-23** — Chấm bài |
| `GET` | `/api/v1/mentor/submissions/{submission_id}` | **AC-23** — Chấm bài |
| `POST` | `/api/v1/mentor/submissions/{submission_id}/feedback` | **AC-23** — Chấm bài |
| `POST` | `/api/v1/mentor/submissions/{submission_id}/grade` | **AC-23** — Chấm bài |
| `GET` | `/api/v1/mentor/support/requests` | **AC-24** — Hỗ trợ học viên |
| `GET` | `/api/v1/mentor/support/{request_id}` | **AC-24** — Hỗ trợ học viên |
| `POST` | `/api/v1/mentor/support/{request_id}/reply` | **AC-24** — Hỗ trợ học viên |
| `PATCH` | `/api/v1/mentor/support/{request_id}/resolve` | **AC-24** — Hỗ trợ học viên |
| `PATCH` | `/api/v1/notifications/read-all` | **AC-20** — Nhận thông báo |
| `PATCH` | `/api/v1/notifications/{notification_id}/read` | **AC-20** — Nhận thông báo |
| `GET` | `/api/v1/operations/{operation_id}` | **AC-12** — Đăng ký khóa học<br>**AC-25** — Gửi thông báo<br>**AC-36** — Quản lý thông báo<br>**AC-38** — Báo cáo tác động cộng đồng |
| `POST` | `/api/v1/orders` | **AC-12** — Đăng ký khóa học |
| `POST` | `/api/v1/payments` | **AC-12** — Đăng ký khóa học |
| `GET` | `/api/v1/quizzes/{quiz_id}` | **AC-16** — Làm bài kiểm tra |
| `POST` | `/api/v1/quizzes/{quiz_id}/attempts` | **AC-16** — Làm bài kiểm tra |
| `GET` | `/api/v1/resources/{resource_id}` | **AC-06** — Xem tài nguyên |
| `GET` | `/api/v1/submissions/{submission_id}` | **AC-17** — Nộp bài tập |
| `POST` | `/api/v1/uploads` | **AC-17** — Nộp bài tập<br>**AC-21** — Đăng bài giảng |
| `GET` | `/api/v1/users/me` | **AC-02** — Đăng nhập<br>**AC-11** — Quản lý hồ sơ cá nhân |
| `GET` | `/api/v1/users/me/achievements` | **AC-18** — Theo dõi tiến độ học tập |
| `POST` | `/api/v1/users/me/avatar` | **AC-11** — Quản lý hồ sơ cá nhân |
| `GET` | `/api/v1/users/me/courses` | **AC-12** — Đăng ký khóa học<br>**AC-13** — Xem khóa học đã đăng ký |
| `GET` | `/api/v1/users/me/notifications` | **AC-20** — Nhận thông báo |
| `PUT` | `/api/v1/users/me/profile` | **AC-11** — Quản lý hồ sơ cá nhân |
| `GET` | `/api/v1/users/me/progress` | **AC-13** — Xem khóa học đã đăng ký<br>**AC-18** — Theo dõi tiến độ học tập |
| `GET` | `/api/v1/users/me/progress/{course_id}` | **AC-18** — Theo dõi tiến độ học tập |
