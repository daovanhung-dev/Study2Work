# Business Code Delta — Plan 07 — Learner Exercises and Submissions

| API | Success code | Meaning |
|---:|---|---|
| 048 | `EXERCISES_RETRIEVED` | Lấy danh sách bài tập theo khóa/chương/bài học và trạng thái cá nhân. thành công. |
| 049 | `EXERCISES_RETRIEVED` | Xem đề bài, tiêu chí, hint, tài liệu, hình thức nộp và trạng thái bài nộp. thành công. |
| 050 | `EXERCISES_DRAFT_RETRIEVED` | Lấy bản nháp bài làm hiện tại. thành công. |
| 051 | `EXERCISES_DRAFT_UPDATED` | Tạo/cập nhật bản nháp; chưa tính là đã nộp hoặc hoàn thành. thành công. |
| 052 | `EXERCISE_SUBMISSION_CREATED` | Nộp bài lần đầu và chuyển sang chấm tự động hoặc chờ review. thành công. |
| 053 | `EXERCISES_SUBMISSIONS_LATEST_RETRIEVED` | Lấy bài nộp và kết quả đánh giá mới nhất. thành công. |
| 054 | `EXERCISES_SUBMISSIONS_RETRIEVED` | Lấy lịch sử các lần nộp bài. thành công. |
| 055 | `SUBMISSIONS_RETRIEVED` | Lấy chi tiết một lần nộp và phản hồi tương ứng. thành công. |
| 056 | `EXERCISES_RESUBMISSIONS_CREATED` | Nộp lại khi NEEDS_REVISION hoặc được mở quyền. thành công. |

Shared error codes: `REQUEST_REQUIRED`, `REQUEST_INVALID_FORMAT`, `METHOD_NOT_ALLOWED`, `AUTHENTICATION_REQUIRED`, `ACCESS_DENIED`, `RESOURCE_NOT_FOUND`, `BUSINESS_RULE_VIOLATION`, `CONCURRENT_UPDATE_CONFLICT`, `IDEMPOTENCY_CONFLICT`, `RATE_LIMIT_EXCEEDED`, `DEPENDENCY_UNAVAILABLE`, `INTERNAL_ERROR`.
