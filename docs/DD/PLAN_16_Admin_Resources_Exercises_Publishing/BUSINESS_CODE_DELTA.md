# Business Code Delta — Plan 16 — Admin Resources Exercises and Publishing

| API | Success code | Meaning |
|---:|---|---|
| 118 | `ADMIN_RESOURCES_CREATED` | Tạo tài liệu/tài nguyên và gắn nguồn, quyền sử dụng. thành công. |
| 119 | `ADMIN_RESOURCES_UPDATED` | Cập nhật mô tả, nguồn, quyền, liên kết và tính bắt buộc. thành công. |
| 120 | `ADMIN_RESOURCES_DELETED` | Ẩn/xóa tài nguyên không còn hợp lệ. thành công. |
| 121 | `ADMIN_EXERCISES_RETRIEVED` | Tra cứu cấu hình bài tập. thành công. |
| 122 | `ADMIN_EXERCISES_CREATED` | Tạo bài tập và cấu hình hình thức nộp/chấm. thành công. |
| 123 | `ADMIN_EXERCISES_RETRIEVED` | Lấy đầy đủ cấu hình bài tập, đáp án/rubric và thống kê ảnh hưởng. thành công. |
| 124 | `ADMIN_EXERCISES_UPDATED` | Cập nhật đề, hạn, đáp án, rubric, bắt buộc và quyền nộp lại. thành công. |
| 125 | `ADMIN_EXERCISES_DELETED` | Xóa/ẩn bài tập nếu hợp lệ, không phá lịch sử bài nộp. thành công. |
| 126 | `CONTENT_PRE_PUBLISH_CHECK_COMPLETED` | Chạy checklist trước xuất bản cho một nội dung được định danh trên URL. thành công. |
| 127 | `CONTENT_PUBLISHED` | Xuất bản, lưu trữ hoặc áp dụng cập nhật quan trọng cho nội dung sau khi kiểm tra điều kiện. thành công. |

Shared error codes: `REQUEST_REQUIRED`, `REQUEST_INVALID_FORMAT`, `METHOD_NOT_ALLOWED`, `AUTHENTICATION_REQUIRED`, `ACCESS_DENIED`, `RESOURCE_NOT_FOUND`, `BUSINESS_RULE_VIOLATION`, `CONCURRENT_UPDATE_CONFLICT`, `IDEMPOTENCY_CONFLICT`, `RATE_LIMIT_EXCEEDED`, `DEPENDENCY_UNAVAILABLE`, `INTERNAL_ERROR`.
