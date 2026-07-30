# Business Code Delta — Plan 08 — Admin Exercise Review

| API | Success code | Meaning |
|---:|---|---|
| 057 | `ADMIN_EXERCISE_SUBMISSIONS_RETRIEVED` | Lấy hàng đợi bài cần chấm và lọc theo trạng thái. thành công. |
| 058 | `ADMIN_EXERCISE_SUBMISSIONS_RETRIEVED` | Xem đầy đủ bài nộp, rubric và lịch sử chấm. thành công. |
| 059 | `EXERCISE_SUBMISSION_REVIEWED` | Chấm bài thủ công, ghi điểm, kết quả và phản hồi. thành công. |
| 060 | `ADMIN_EXERCISE_SUBMISSIONS_REOPEN_COMPLETED` | Mở lại quyền nộp bài trong trường hợp ngoại lệ. thành công. |

Shared error codes: `REQUEST_REQUIRED`, `REQUEST_INVALID_FORMAT`, `METHOD_NOT_ALLOWED`, `AUTHENTICATION_REQUIRED`, `ACCESS_DENIED`, `RESOURCE_NOT_FOUND`, `BUSINESS_RULE_VIOLATION`, `CONCURRENT_UPDATE_CONFLICT`, `IDEMPOTENCY_CONFLICT`, `RATE_LIMIT_EXCEEDED`, `DEPENDENCY_UNAVAILABLE`, `INTERNAL_ERROR`.
