# Business Code Delta — Plan 15 — Admin Chapters and Lessons

| API | Success code | Meaning |
|---:|---|---|
| 109 | `ADMIN_COURSES_CHAPTERS_CREATED` | Tạo chương trong khóa học. thành công. |
| 110 | `ADMIN_CHAPTERS_UPDATED` | Cập nhật tiêu đề, mục tiêu, điều kiện mở khóa/hoàn thành chương. thành công. |
| 111 | `ADMIN_CHAPTERS_DELETED` | Xóa chương khi được phép hoặc từ chối nếu ảnh hưởng nội dung đã xuất bản. thành công. |
| 112 | `ADMIN_CHAPTERS_ITEMS_ORDER_UPDATED` | Sắp xếp bài học/bài tập trong chương. thành công. |
| 113 | `ADMIN_CHAPTERS_LESSONS_CREATED` | Tạo bài học mới trong chương. thành công. |
| 114 | `ADMIN_LESSONS_UPDATED` | Cập nhật nội dung, video, ví dụ, điều kiện và tính bắt buộc của bài học. thành công. |
| 115 | `ADMIN_LESSONS_DELETED` | Xóa/ẩn bài học khi hợp lệ, bảo toàn lịch sử nếu đã có người học. thành công. |
| 116 | `ADMIN_LESSONS_PREVIEW_UPDATED` | Bật/tắt và cấu hình phạm vi bài học mẫu công khai. thành công. |
| 117 | `ADMIN_LESSONS_LIFECYCLE_COMPLETED` | Xuất bản, cập nhật, ẩn hoặc lưu trữ bài học. thành công. |

Shared error codes: `REQUEST_REQUIRED`, `REQUEST_INVALID_FORMAT`, `METHOD_NOT_ALLOWED`, `AUTHENTICATION_REQUIRED`, `ACCESS_DENIED`, `RESOURCE_NOT_FOUND`, `BUSINESS_RULE_VIOLATION`, `CONCURRENT_UPDATE_CONFLICT`, `IDEMPOTENCY_CONFLICT`, `RATE_LIMIT_EXCEEDED`, `DEPENDENCY_UNAVAILABLE`, `INTERNAL_ERROR`.
