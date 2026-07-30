# Business Code Delta — Plan 09 — Progress and Completion

| API | Success code | Meaning |
|---:|---|---|
| 061 | `ME_DASHBOARD_RETRIEVED` | Lấy dashboard ưu tiên hành động học tiếp theo. thành công. |
| 062 | `ME_CONTINUE_LEARNING_RETRIEVED` | Xác định nội dung học tiếp theo trên toàn lộ trình. thành công. |
| 063 | `ME_PROGRESS_LEARNING_PATHS_RETRIEVED` | Lấy tiến độ chi tiết lộ trình và điều kiện còn thiếu. thành công. |
| 064 | `ME_PROGRESS_COURSES_RETRIEVED` | Lấy tiến độ khóa học theo chương, bài học và đánh giá. thành công. |
| 065 | `ME_PROGRESS_CHAPTERS_RETRIEVED` | Lấy tiến độ chương và trạng thái từng nội dung. thành công. |
| 066 | `ME_PROGRESS_LESSONS_RETRIEVED` | Lấy các điều kiện hoàn thành bài học và trạng thái từng điều kiện. thành công. |
| 067 | `LESSON_PROGRESS_UPDATED` | Ghi sự kiện xem video, đọc tài liệu hoặc xác nhận hoàn thành; tái tính tiến độ bài/chương/khóa/lộ trình. thành công. |
| 068 | `ME_LEARNING_HISTORY_RETRIEVED` | Lấy lịch sử lộ trình, khóa học, bài tập và nội dung gần đây. thành công. |
| 069 | `ME_COMPLETION_SUMMARIES_ENTITY_TYPE_RETRIEVED` | Lấy tổng kết khi hoàn thành khóa học hoặc lộ trình. thành công. |

Shared error codes: `REQUEST_REQUIRED`, `REQUEST_INVALID_FORMAT`, `METHOD_NOT_ALLOWED`, `AUTHENTICATION_REQUIRED`, `ACCESS_DENIED`, `RESOURCE_NOT_FOUND`, `BUSINESS_RULE_VIOLATION`, `CONCURRENT_UPDATE_CONFLICT`, `IDEMPOTENCY_CONFLICT`, `RATE_LIMIT_EXCEEDED`, `DEPENDENCY_UNAVAILABLE`, `INTERNAL_ERROR`.
