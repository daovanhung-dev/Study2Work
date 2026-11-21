# Study Server API test report — 2026-11-01

## Trạng thái hiện tại sau sửa

- 10 truy vấn nullable bind đã thêm cast rõ ràng; 10 module focus pass **178 tests**, toàn bộ Study suite pass **1326 tests**.
- Cả 10 API được gọi qua Uvicorn với filter bỏ trống và filter hợp lệ: **20/20 HTTP requests pass**. Neon branch test đã bị xóa và xác nhận không còn tồn tại.
- Kết quả kiểm tra 69 operation ban đầu được giữ bên dưới làm lịch sử; 59 operation đã pass từ lượt trước không được gọi lại sau sửa SQL. API #98 source/DD discrepancy không thay đổi.

## Kết quả lượt kiểm thử ban đầu (trước sửa lỗi)

Phần này giữ nguyên kết quả lượt chạy toàn bộ API ban đầu để làm lịch sử. Tình trạng sau sửa được ghi ở mục **Kết quả sau sửa nullable bind** cuối báo cáo.

- Phạm vi runtime: **67 operation thuộc 66 API module có source**, cộng 2 utility operation (`/api/v1/hello`, `/api/v1/test/db`) = **69/69 operation `/api/v1` được gọi qua HTTP**; thêm `/`, `/health/live`, `/health/ready`.
- Kết quả API operation: **59 PASS / 10 FAIL**. Mỗi operation có kết quả ở bảng bên dưới; status thể hiện phản hồi success path hiện tại.
- Test suite: `uv run pytest -q` → **1324 passed, 0 failed**, 1 Starlette/httpx deprecation warning, 164.34s.
- Các DD được đọc trước khi tạo dữ liệu/chạy test. DD phần lớn còn `Draft — Needs Confirmation`; status ở bảng giữ nguyên trạng thái trong DD. `PASS` chỉ có nghĩa là phản hồi hiện tại đạt kịch bản đã gọi, không tự phê duyệt contract Draft/DERIVED.

## Ma trận 69 operation `/api/v1`

| API | Operation / HTTP path | DD và trạng thái DD | Kịch bản / kết quả quan sát | Kết quả |
|---|---|---|---|---|
| Utility | `GET /api/v1/hello` | Không áp dụng DD API | Probe qua HTTP; HTTP 200 | **PASS** |
| Utility | `GET /api/v1/test/db` | Không áp dụng DD API | Probe qua HTTP; HTTP 200; engine được inject từ branch tạm | **PASS** |
| #1 | **register**<br>`POST /api/v1/auth/register` | [#1](../dd/01_auth_register/00_Cover.md)<br>`Draft — Needs Confirmation` | Success path với dữ liệu test riêng; HTTP 201 `DESIGN_RESOURCE_CREATED`<br>email định danh riêng của lượt chạy | **PASS** |
| #3 | **login**<br>`POST /api/v1/auth/login` | [#3](../dd/03_auth_login/00_Cover.md)<br>`Draft — Needs Confirmation` | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_RETRIEVED` | **PASS** |
| #3 | **refresh**<br>`POST /api/v1/auth/refresh` | [DD #3](../dd/03_auth_login/00_Cover.md)<br>Không có DD endpoint refresh riêng; Q-03-04 còn mở | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_RETRIEVED`<br>refresh token rotation | **PASS** |
| #2 | **verification dispatch**<br>`POST /api/v1/auth/verify-email/send` | [#2](../dd/02_auth_verify_email_send/00_Cover.md)<br>`Draft — Needs Confirmation` | Success path với dữ liệu test riêng; HTTP 202 `DESIGN_OPERATION_ACCEPTED`<br>provider mặc định là stub; không gửi email thật | **PASS** |
| #5 | **categories**<br>`GET /api/v1/categories` | [#5](../dd/05_categories/00_Cover.md)<br>`Draft — Needs Confirmation` | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_RETRIEVED` | **PASS** |
| #6 | **courses**<br>`GET /api/v1/courses` | [#6](../dd/06_courses/00_Cover.md)<br>`Draft — Needs Confirmation` | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_RETRIEVED` | **PASS** |
| #7 | **course search**<br>`GET /api/v1/courses/search` | [#7](../dd/07_courses_search/00_Cover.md)<br>`Draft — Needs Confirmation` | Success path với dữ liệu test riêng; HTTP 500 `DESIGN_INTERNAL_ERROR` | **FAIL** |
| #8 | **course detail**<br>`GET /api/v1/courses/{course_id}` | [#8](../dd/08_courses_detail/00_Cover.md)<br>`Draft — Needs Confirmation` | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_RETRIEVED` | **PASS** |
| #9 | **curriculum**<br>`GET /api/v1/courses/{course_id}/curriculum` | [#9](../dd/09_courses_curriculum/00_Cover.md)<br>`Draft — Needs Confirmation` | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_RETRIEVED` | **PASS** |
| #4 | **current user**<br>`GET /api/v1/users/me` | [#4](../dd/04_users_me/00_Cover.md)<br>`Draft — Needs Confirmation` | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_RETRIEVED` | **PASS** |
| #12 | **resource detail**<br>`GET /api/v1/resources/{resource_id}` | [#12](../dd/12_resources_detail/00_Cover.md)<br>`Draft — Needs Confirmation` | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_RETRIEVED` | **PASS** |
| #13 | **avatar upload**<br>`POST /api/v1/users/me/avatar` | [#13](../dd/13_users_me_avatar/00_Cover.md)<br>`Updated per user-approved implementation plan` | Success path với dữ liệu test riêng; HTTP 201 `DESIGN_RESOURCE_CREATED`<br>object storage stub | **PASS** |
| #34 | **upload**<br>`POST /api/v1/uploads` | [#34](../dd/34_uploads/00_Cover.md)<br>Draft — Ready for Review | Success path với dữ liệu test riêng; HTTP 201 `DESIGN_RESOURCE_CREATED`<br>object storage upload/delete stub | **PASS** |
| #14 | **profile update**<br>`PUT /api/v1/users/me/profile` | [#14](../dd/14_users_me_profile/00_Cover.md)<br>`Draft — Needs Confirmation` | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_UPDATED`<br>Source trả 200; source schema không có bio nên field bị bỏ qua (DD discrepancy). | **PASS** |
| #46 | **Mentor courses**<br>`GET /api/v1/mentor/courses` | [#46](../dd/46_mentor_courses/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_RETRIEVED` | **PASS** |
| #47 | **lecture create**<br>`POST /api/v1/mentor/courses/{course_id}/lectures` | [#47](../dd/47_mentor_lectures_create/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 201 `DESIGN_RESOURCE_CREATED` | **PASS** |
| #48 | **lecture detail**<br>`GET /api/v1/mentor/lectures/{lecture_id}` | [#48](../dd/48_mentor_lecture_detail/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_RETRIEVED` | **PASS** |
| #49 | **content tree**<br>`GET /api/v1/mentor/courses/{course_id}/content` | [#49](../dd/49_mentor_content_list/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_RETRIEVED` | **PASS** |
| #50 | **content create**<br>`POST /api/v1/mentor/content` | [#50](../dd/50_mentor_content_create/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 201 `DESIGN_RESOURCE_CREATED` | **PASS** |
| #51 | **content update**<br>`PUT /api/v1/mentor/content/{content_id}` | [#51](../dd/51_mentor_content_update/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_UPDATED` | **PASS** |
| #53 | **content delete**<br>`DELETE /api/v1/mentor/content/{content_id}` | [#53](../dd/53_mentor_content_delete/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_DELETED` | **PASS** |
| #52 | **content publish**<br>`PATCH /api/v1/mentor/content/{content_id}/publish` | [#52](../dd/52_mentor_content_publish/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_UPDATED`<br>Transition sau Admin approval; DERIVED. | **PASS** |
| #54 | **submissions list**<br>`GET /api/v1/mentor/submissions` | [#54](../dd/54_mentor_submissions_list/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 500 `DESIGN_INTERNAL_ERROR` | **FAIL** |
| #55 | **submission detail**<br>`GET /api/v1/mentor/submissions/{submission_id}` | [#55](../dd/55_mentor_submissions_detail/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_RETRIEVED` | **PASS** |
| #56 | **grade submission**<br>`POST /api/v1/mentor/submissions/{submission_id}/grade` | [#56](../dd/56_mentor_submissions_grade/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_UPDATED` | **PASS** |
| #57 | **submission feedback**<br>`POST /api/v1/mentor/submissions/{submission_id}/feedback` | [#57](../dd/57_mentor_submissions_feedback/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_UPDATED` | **PASS** |
| #58 | **support list**<br>`GET /api/v1/mentor/support/requests` | [#58](../dd/58_mentor_support_requests/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 500 `DESIGN_INTERNAL_ERROR` | **FAIL** |
| #59 | **support detail**<br>`GET /api/v1/mentor/support/{request_id}` | [#59](../dd/59_mentor_support_request_detail/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_RETRIEVED` | **PASS** |
| #60 | **support reply**<br>`POST /api/v1/mentor/support/{request_id}/reply` | [#60](../dd/60_mentor_support_reply/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_UPDATED` | **PASS** |
| #61 | **support resolve**<br>`PATCH /api/v1/mentor/support/{request_id}/resolve` | [#61](../dd/61_mentor_support_resolve/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_UPDATED` | **PASS** |
| #62 | **course students**<br>`GET /api/v1/mentor/courses/{course_id}/students` | [#62](../dd/62_mentor_course_students/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_RETRIEVED` | **PASS** |
| #65 | **course progress**<br>`GET /api/v1/mentor/courses/{course_id}/progress` | [#65](../dd/65_mentor_course_progress/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_RETRIEVED` | **PASS** |
| #66 | **course analytics**<br>`GET /api/v1/mentor/courses/{course_id}/analytics` | [#66](../dd/66_mentor_course_analytics/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_RETRIEVED` | **PASS** |
| #67 | **student progress**<br>`GET /api/v1/mentor/courses/{course_id}/students/{student_id}/progress` | [#67](../dd/67_mentor_student_progress/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_RETRIEVED` | **PASS** |
| #63 | **Mentor notification create**<br>`POST /api/v1/mentor/notifications` | [#63](../dd/63_mentor_notifications_create/00_Cover.md)<br>`Draft — Needs Confirmation` | Success path với dữ liệu test riêng; HTTP 202 `DESIGN_OPERATION_ACCEPTED`<br>outbox only; no external delivery | **PASS** |
| #64 | **Mentor notification status**<br>`GET /api/v1/mentor/notifications/{notification_id}/status` | [#64](../dd/64_mentor_notifications_status/00_Cover.md)<br>`Draft — Needs Confirmation` | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_RETRIEVED` | **PASS** |
| #68 | **Admin users list**<br>`GET /api/v1/admin/users` | [#68](../dd/68_admin_users_list/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 500 `DESIGN_INTERNAL_ERROR` | **FAIL** |
| #69 | **Admin user detail**<br>`GET /api/v1/admin/users/{user_id}` | [#69](../dd/69_admin_user_detail/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_RETRIEVED` | **PASS** |
| #70 | **Admin user update**<br>`PUT /api/v1/admin/users/{user_id}` | [#70](../dd/70_admin_user_update/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_UPDATED` | **PASS** |
| #72 | **Admin user delete**<br>`DELETE /api/v1/admin/users/{user_id}` | [#72](../dd/72_admin_user_delete/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_DELETED` | **PASS** |
| #71 | **Admin user status**<br>`PATCH /api/v1/admin/users/{user_id}/status` | [#71](../dd/71_admin_user_status/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_UPDATED` | **PASS** |
| #73 | **Admin courses list**<br>`GET /api/v1/admin/courses` | [#73](../dd/73_admin_courses_list/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 500 `DESIGN_INTERNAL_ERROR` | **FAIL** |
| #74 | **Admin course detail**<br>`GET /api/v1/admin/courses/{course_id}` | [#74](../dd/74_admin_course_detail/00_Cover.md)<br>`Draft — Needs Confirmation` | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_RETRIEVED` | **PASS** |
| #75 | **Admin course update**<br>`PUT /api/v1/admin/courses/{course_id}` | [#75](../dd/75_admin_course_update/00_Cover.md)<br>`Draft — Needs Confirmation` | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_UPDATED` | **PASS** |
| #77 | **Admin course delete**<br>`DELETE /api/v1/admin/courses/{course_id}` | [#77](../dd/77_admin_course_delete/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_DELETED` | **PASS** |
| #76 | **Admin course status**<br>`PATCH /api/v1/admin/courses/{course_id}/status` | [#76](../dd/76_admin_course_status/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_UPDATED` | **PASS** |
| #78 | **pending content**<br>`GET /api/v1/admin/content/pending` | [#78](../dd/78_admin_content_pending/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 500 `DESIGN_INTERNAL_ERROR` | **FAIL** |
| #79 | **content detail**<br>`GET /api/v1/admin/content/{content_id}` | [#79](../dd/79_admin_content_detail/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_RETRIEVED` | **PASS** |
| #80 | **content approve**<br>`PATCH /api/v1/admin/content/{content_id}/approve` | [#80](../dd/80_admin_content_approve/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_UPDATED` | **PASS** |
| #81 | **content reject**<br>`PATCH /api/v1/admin/content/{content_id}/reject` | [#81](../dd/81_admin_content_reject/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_UPDATED` | **PASS** |
| #82 | **Admin lessons list**<br>`GET /api/v1/admin/lessons` | [#82](../dd/82_admin_lessons_list/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 500 `DESIGN_INTERNAL_ERROR` | **FAIL** |
| #83 | **Admin lesson detail**<br>`GET /api/v1/admin/lessons/{lesson_id}` | [#83](../dd/83_admin_lesson_detail/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_RETRIEVED` | **PASS** |
| #84 | **Admin lesson update**<br>`PUT /api/v1/admin/lessons/{lesson_id}` | [#84](../dd/84_admin_lesson_update/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_UPDATED` | **PASS** |
| #86 | **Admin lesson delete**<br>`DELETE /api/v1/admin/lessons/{lesson_id}` | [#86](../dd/86_admin_lesson_delete/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_DELETED` | **PASS** |
| #87 | **Admin quizzes list**<br>`GET /api/v1/admin/quizzes` | [#87](../dd/87_admin_quizzes_list/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 500 `DESIGN_INTERNAL_ERROR` | **FAIL** |
| #88 | **Admin quiz create**<br>`POST /api/v1/admin/quizzes` | [#88](../dd/88_admin_quizzes_create/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 201 `DESIGN_RESOURCE_CREATED` | **PASS** |
| #89 | **Admin quiz update**<br>`PUT /api/v1/admin/quizzes/{quiz_id}` | [#89](../dd/89_admin_quizzes_update/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_UPDATED` | **PASS** |
| #90 | **Admin quiz delete**<br>`DELETE /api/v1/admin/quizzes/{quiz_id}` | [#90](../dd/90_admin_quizzes_delete/00_Cover.md)<br>`Draft — Needs Confirmation` | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_DELETED` | **PASS** |
| #91 | **Admin quiz statistics**<br>`GET /api/v1/admin/quizzes/{quiz_id}/statistics` | [#91](../dd/91_admin_quizzes_statistics/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_RETRIEVED` | **PASS** |
| #92 | **Admin notifications list**<br>`GET /api/v1/admin/notifications` | [#92](../dd/92_admin_notifications_list/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 500 `DESIGN_INTERNAL_ERROR` | **FAIL** |
| #93 | **Admin notification create**<br>`POST /api/v1/admin/notifications` | [#93](../dd/93_admin_notifications_create/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 202 `DESIGN_OPERATION_ACCEPTED`<br>delivery outbox only; no provider send | **PASS** |
| #94 | **Admin notification update**<br>`PUT /api/v1/admin/notifications/{notification_id}` | [#94](../dd/94_admin_notifications_update/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_UPDATED` | **PASS** |
| #95 | **Admin notification delete**<br>`DELETE /api/v1/admin/notifications/{notification_id}` | [#95](../dd/95_admin_notifications_delete/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_DELETED` | **PASS** |
| #96 | **Admin notification status**<br>`GET /api/v1/admin/notifications/{notification_id}/status` | [#96](../dd/96_admin_notifications_status/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_RETRIEVED` | **PASS** |
| #97 | **reported discussions**<br>`GET /api/v1/admin/discussions/reported` | [#97](../dd/97_admin_discussions_reported/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 500 `DESIGN_INTERNAL_ERROR` | **FAIL** |
| #98 | **discussion detail**<br>`GET /api/v1/admin/discussions/{discussion_id}` | [#98](../dd/98_admin_discussions_detail/00_Cover.md)<br>Draft — Needs Confirmation<br>DD `UNWIRED`; source hiện đã wired | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_RETRIEVED`<br>Source tự dựng title từ content và không đọc report relation; ghi nhận hiện trạng, không xem là contract đã duyệt. | **PASS** |
| #85 | **Admin lesson status**<br>`PATCH /api/v1/admin/lessons/{lesson_id}/status` | [#85](../dd/85_admin_lesson_status/00_Cover.md)<br>Draft — Needs Confirmation | Success path với dữ liệu test riêng; HTTP 200 `DESIGN_RESOURCE_UPDATED` | **PASS** |

### Các route ngoài `/api/v1`

| Route | Kết quả quan sát | Trạng thái |
|---|---|---|
| `GET /` | HTTP 200 `SYSTEM_ROOT_LOADED` | **PASS** |
| `GET /health/live` | HTTP 200 `SYSTEM_HEALTH_LIVE` | **PASS** |
| `GET /health/ready` | HTTP 200 `SYSTEM_HEALTH_READY` | **PASS** |

## Baseline lỗi runtime trước sửa

| API | Route | Hiện trạng | Nguyên nhân đã xác minh |
|---|---|---|---|
| #7 Course search | `GET /api/v1/courses/search` | HTTP 500 `DESIGN_INTERNAL_ERROR` | PostgreSQL `AmbiguousParameter: could not determine data type of parameter $N`; truy vấn bind cùng một tham số qua điều kiện dạng `:field IS NULL OR ...` không ép kiểu rõ. Đã tái hiện trực tiếp câu SQL trên branch test. |
| #78 Admin pending content | `GET /api/v1/admin/content/pending` | HTTP 500 `DESIGN_INTERNAL_ERROR` | PostgreSQL `AmbiguousParameter: could not determine data type of parameter $N`; truy vấn bind cùng một tham số qua điều kiện dạng `:field IS NULL OR ...` không ép kiểu rõ. Đã tái hiện trực tiếp câu SQL trên branch test. |
| #54 Mentor submissions list | `GET /api/v1/mentor/submissions` | HTTP 500 `DESIGN_INTERNAL_ERROR` | PostgreSQL `AmbiguousParameter: could not determine data type of parameter $N`; truy vấn bind cùng một tham số qua điều kiện dạng `:field IS NULL OR ...` không ép kiểu rõ. Đã tái hiện trực tiếp câu SQL trên branch test. |
| #58 Mentor support list | `GET /api/v1/mentor/support/requests` | HTTP 500 `DESIGN_INTERNAL_ERROR` | PostgreSQL `AmbiguousParameter: could not determine data type of parameter $N`; truy vấn bind cùng một tham số qua điều kiện dạng `:field IS NULL OR ...` không ép kiểu rõ. Đã tái hiện trực tiếp câu SQL trên branch test. |
| #68 Admin users list | `GET /api/v1/admin/users` | HTTP 500 `DESIGN_INTERNAL_ERROR` | PostgreSQL `AmbiguousParameter: could not determine data type of parameter $N`; truy vấn bind cùng một tham số qua điều kiện dạng `:field IS NULL OR ...` không ép kiểu rõ. Đã tái hiện trực tiếp câu SQL trên branch test. |
| #73 Admin courses list | `GET /api/v1/admin/courses` | HTTP 500 `DESIGN_INTERNAL_ERROR` | PostgreSQL `AmbiguousParameter: could not determine data type of parameter $N`; truy vấn bind cùng một tham số qua điều kiện dạng `:field IS NULL OR ...` không ép kiểu rõ. Đã tái hiện trực tiếp câu SQL trên branch test. |
| #82 Admin lessons list | `GET /api/v1/admin/lessons` | HTTP 500 `DESIGN_INTERNAL_ERROR` | PostgreSQL `AmbiguousParameter: could not determine data type of parameter $N`; truy vấn bind cùng một tham số qua điều kiện dạng `:field IS NULL OR ...` không ép kiểu rõ. Đã tái hiện trực tiếp câu SQL trên branch test. |
| #87 Admin quizzes list | `GET /api/v1/admin/quizzes` | HTTP 500 `DESIGN_INTERNAL_ERROR` | PostgreSQL `AmbiguousParameter: could not determine data type of parameter $N`; truy vấn bind cùng một tham số qua điều kiện dạng `:field IS NULL OR ...` không ép kiểu rõ. Đã tái hiện trực tiếp câu SQL trên branch test. |
| #92 Admin notifications list | `GET /api/v1/admin/notifications` | HTTP 500 `DESIGN_INTERNAL_ERROR` | PostgreSQL `AmbiguousParameter: could not determine data type of parameter $N`; truy vấn bind cùng một tham số qua điều kiện dạng `:field IS NULL OR ...` không ép kiểu rõ. Đã tái hiện trực tiếp câu SQL trên branch test. |
| #97 Admin reported discussions | `GET /api/v1/admin/discussions/reported` | HTTP 500 `DESIGN_INTERNAL_ERROR` | PostgreSQL `AmbiguousParameter: could not determine data type of parameter $N`; truy vấn bind cùng một tham số qua điều kiện dạng `:field IS NULL OR ...` không ép kiểu rõ. Đã tái hiện trực tiếp câu SQL trên branch test. |

Tại thời điểm lượt chạy ban đầu, các API này trả `FAIL` qua HTTP dù test fake DB pass. Mục cuối báo cáo ghi kết quả sau khi thêm cast SQL.

## Luồng và kiểm tra phụ

- Đã chạy register → login → refresh với refresh token rotation; verification dispatch dùng `StubVerificationEmailProvider`, không gửi email.
- Đã chạy avatar upload #13 và multipart upload #34 bằng object-storage stub; không tạo object ở S3 thật. #47 dùng upload result từ #34.
- Content moderation: create → update → Admin approve → publish; thêm reject và delete trên content riêng.
- Submission: detail → grade → feedback. Support: detail → reply với `attachment_refs=[]` → resolve. Roster, course progress/analytics/student progress, notification create/status, Admin CRUD, quiz statistics, notification status và reported-discussion detail đã chạy.
- Authentication/negative: 57/57 request thiếu Bearer trả 401; hai role-negative trả 403; hai validation-negative trả 422; duplicate register trả 409; hai not-found trả 404.
- API #98 detail success đọc đúng discussion/comment hiện có; dedicated characterization tests bao gồm success, ID sai, auth/role trước query, not-found, query failure/rollback.

## Cách chạy và giới hạn môi trường

- Tạo branch Neon tạm `codex-study-api-test-2026-11-01` từ snapshot `production`; dùng database/schema Study (`neondb.dao_van_hung`) và chỉ áp dụng migrations có sẵn 002–014 trên branch test. Schema branch có 30 bảng sau migration. Dữ liệu sinh cho lượt chạy dùng prefix riêng; không ghi production.
- Chạy Uvicorn loopback `127.0.0.1:3303`, Settings trỏ tới branch tạm; thao tác HTTP qua local server. Không xác minh deployment Ubuntu.
- Email và object storage được stub. Report không xác nhận tích hợp nhà cung cấp ngoài.
- Lần thử harness đầu dùng `create_app(Settings)` trả HTTP 500 ở API #1 vì DB dependency override trả generator như object; harness sau chuyển về default app composition và inject Settings trước khi app khởi tạo. Không thay source runtime.
- Branch được xóa sau khi hoàn tất report; không còn dữ liệu thử trên branch.

## Kiểm tra test và định dạng

- Full suite: `uv run pytest -q` → **1324 passed**.
- Regression/API #98 focus: `uv run pytest -q tests/modules/admin/api_98_admin_discussions_detail tests/modules/admin/api_92_admin_notifications_list tests/modules/admin/api_93_admin_notifications_create tests/modules/admin/api_94_admin_notifications_update tests/modules/admin/api_95_admin_notifications_delete` → **96 passed**.
- `uv run ruff check` và `uv run ruff format --check` trên các file test đã đổi: pass.

## Discrepancies và DD-only API

- **API #98:** DD hiện `Draft — Needs Confirmation`/`UNWIRED`, yêu cầu thread + report detail và để ngỏ quan hệ report/title/status. Source có route và test hiện tại chỉ trả thread/comments, tự dựng title từ content, không đọc report relation. Đây là discrepancy source-vs-DD; kết quả HTTP không phê duyệt hành vi.
- **API #14:** DD còn khác source/schema hiện tại; source không có cột `bio`, nên request `bio` không được lưu/phản hồi, dù PUT trả 200.
- **API #3 refresh:** được kiểm thử như operation riêng trên route, nhưng DD #3 chỉ mô tả login; câu hỏi refresh Q-03-04 còn mở.

| API | DD | Runtime source/route | Kết quả |
|---|---|---|---|
| #99 | [Admin discussion moderation](../dd/99_admin_discussions_moderate/00_Cover.md) — Draft — Needs Confirmation | Chưa có module/route | **NOT_RUN** |
| #100 | [Admin discussion delete](../dd/100_admin_discussions_delete/00_Cover.md) — Draft — Needs Confirmation | Chưa có module/route | **NOT_RUN** |
| #101 | [Admin reports summary](../dd/101_admin_reports_summary/00_Cover.md) — Draft — Needs Confirmation | Chưa có module/route | **NOT_RUN** |
| #102 | [Admin reports impact](../dd/102_admin_reports_community_impact/00_Cover.md) — Draft — Needs Confirmation | Chưa có module/route | **NOT_RUN** |
| #103 | [Admin reports export](../dd/103_admin_reports_community_impact_export/00_Cover.md) — Draft — Needs Confirmation | Chưa có module/route | **NOT_RUN** |

## Tóm tắt trạng thái ở lượt chạy ban đầu

| Nhóm | Kết quả |
|---|---|
| Coded `/api/v1` operations | 67 numbered API-module operations: 57 PASS / 10 FAIL; plus 2 utility operations PASS = 59 PASS / 10 FAIL trên tổng 69 |
| System routes | 3 PASS |
| Pytest | 1324 passed / 0 failed |
| API #99–#103 | 5 NOT_RUN — DD-only; no module/route |
| Production schema/data | Không ghi; không xác minh trực tiếp |

## Kết quả sau sửa nullable bind — 2026-11-01

Đã ép kiểu tường minh cho nullable bind trong SQL constants của API #7, #54, #58, #68, #73, #78, #82, #87, #92 và #97. Route, kiểu filter, auth, predicate và response contract được giữ nguyên. Test module xác nhận filter `NULL` và filter có giá trị; với cặp truy vấn count/list, test cũng đối chiếu biểu thức cast giữa hai câu SQL.

| API | Kịch bản HTTP trên Uvicorn | Kết quả quan sát |
|---|---|---|
| #7 `GET /api/v1/courses/search` | Bỏ `q`; `q` khớp course fixture | 200 / `DESIGN_RESOURCE_RETRIEVED` cho cả hai; 1 row mỗi lần gọi |
| #54 `GET /api/v1/mentor/submissions` | Bỏ filter; `course_id` + `status=SUBMITTED` | 200 cho cả hai; 1 submission |
| #58 `GET /api/v1/mentor/support/requests` | Bỏ filter; `course_id` + `status=OPEN` | 200 cho cả hai; 1 request |
| #68 `GET /api/v1/admin/users` | Bỏ filter; `role=MENTOR`, `status=ACTIVE`, keyword fixture | 200 cho cả hai; filter trả 1 user |
| #73 `GET /api/v1/admin/courses` | Bỏ filter; `status=PUBLISHED` + mentor fixture | 200 cho cả hai; 1 course |
| #78 `GET /api/v1/admin/content/pending` | Bỏ filter; `type=QUIZ` + course fixture | 200 cho cả hai; 1 content |
| #82 `GET /api/v1/admin/lessons` | Bỏ filter; course + `status=PUBLISHED` | 200 cho cả hai; 1 lesson |
| #87 `GET /api/v1/admin/quizzes` | Bỏ filter; course + `status=DRAFT` | 200 cho cả hai; 1 quiz |
| #92 `GET /api/v1/admin/notifications` | Bỏ filter; `status=QUEUED` + `channel=PUSH` | 200 cho cả hai; 1 notification |
| #97 `GET /api/v1/admin/discussions/reported` | Bỏ filter; `reason=SPAM` + `severity=HIGH` | 200 cho cả hai; 1 discussion |

Kết quả này xác nhận 20/20 request trên schema test và fixture của lượt sửa. Đây không phải lần chạy lại toàn bộ 69 operation. API #98 vẫn giữ nguyên discrepancy source/DD đã mô tả ở trên.

## Xác minh source sau sửa và môi trường

- Focused modules: `uv run pytest -q tests/modules/guest/api_07_courses_search tests/modules/mentor/api_54_mentor_submissions_list tests/modules/mentor/api_58_mentor_support_requests tests/modules/admin/api_68_admin_users_list tests/modules/admin/api_73_admin_courses_list tests/modules/admin/api_78_admin_content_pending tests/modules/admin/api_82_admin_lessons_list tests/modules/admin/api_87_admin_quizzes_list tests/modules/admin/api_92_admin_notifications_list tests/modules/admin/api_97_admin_discussions_reported` → **178 passed**.
- Full suite sau sửa: `uv run pytest -q` → **1326 passed, 0 failed**, một Starlette/httpx TestClient deprecation warning (168.34s).
- `uv run ruff check app tests` và `git diff --check` → pass.
- Tạo Neon branch tạm `codex-study-null-cast-2026-11-01` từ snapshot `production`; áp dụng các migration SQL 002–014 trong schema `dao_van_hung`; tạo Student qua register, tạo Mentor/Admin và dữ liệu quan hệ riêng trên branch; lấy token qua login API. Không ghi production.
- Uvicorn chạy trên `127.0.0.1:3303`; email và object storage là stub. Không xác minh email/S3 thật hoặc deployment Ubuntu.
- Dừng Uvicorn, xóa branch `br-flat-dew-b3ongn2c`, rồi tìm theo tên branch và xác nhận không còn kết quả.
- `node scripts/validate-agent-context.mjs` sau khi cập nhật context: exit 1 (`AGENT_CONTEXT_INVALID`). Validator vẫn báo thiếu toàn bộ context/source `web-work/study-web` và `db-admin`, broken links tương ứng, cùng `CONTEXT_STALE` ở nhiều scope gồm Study. Đây là lỗi toàn repo ngoài phạm vi đã chốt; không sửa trong task này.
