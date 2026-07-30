# Business Code Delta — Plan 05 — Learning Paths and Learner Support Requests

| API | Success code | Meaning |
|---:|---|---|
| 028 | `LEARNING_PATHS_RETRIEVED` | Lấy danh sách lộ trình đã xuất bản kèm trạng thái cá nhân. thành công. |
| 029 | `LEARNING_PATHS_RETRIEVED` | Xem cấu trúc lộ trình, trạng thái từng khóa và điều kiện còn thiếu. thành công. |
| 030 | `LEARNING_PATHS_ACTIVATION_PREVIEW_CREATED` | Kiểm tra điều kiện và hiển thị xác nhận trước khi kích hoạt. thành công. |
| 031 | `LEARNING_PATH_ACTIVATED` | Kích hoạt lộ trình duy nhất và mở nội dung đầu tiên. thành công. |
| 032 | `ME_LEARNING_PATHS_ACTIVE_RETRIEVED` | Lấy lộ trình ACTIVE hiện tại và hành động tiếp theo. thành công. |
| 033 | `ME_LEARNING_PATHS_HISTORY_RETRIEVED` | Lấy lịch sử các lộ trình đã tham gia, kể cả hoàn thành/hủy/reset. thành công. |
| 034 | `ME_LEARNING_PATHS_ENROLLMENT_ID_SUMMARY_RETRIEVED` | Xem tổng kết lộ trình hoặc dữ liệu ôn tập lịch sử. thành công. |
| 035 | `ME_LEARNING_PATHS_NEXT_RECOMMENDATIONS_RETRIEVED` | Gợi ý lộ trình tiếp theo sau khi hoàn thành lộ trình hiện tại. thành công. |
| 036 | `SUPPORT_REQUEST_CREATED` | Gửi yêu cầu đổi/reset/hủy lộ trình theo quy trình ngoại lệ. thành công. |
| 037 | `SUPPORT_REQUESTS_RETRIEVED` | Xem danh sách yêu cầu hỗ trợ lộ trình của bản thân. thành công. |
| 038 | `SUPPORT_REQUESTS_RETRIEVED` | Xem chi tiết và kết quả xử lý yêu cầu lộ trình. thành công. |

Shared error codes: `REQUEST_REQUIRED`, `REQUEST_INVALID_FORMAT`, `METHOD_NOT_ALLOWED`, `AUTHENTICATION_REQUIRED`, `ACCESS_DENIED`, `RESOURCE_NOT_FOUND`, `BUSINESS_RULE_VIOLATION`, `CONCURRENT_UPDATE_CONFLICT`, `IDEMPOTENCY_CONFLICT`, `RATE_LIMIT_EXCEEDED`, `DEPENDENCY_UNAVAILABLE`, `INTERNAL_ERROR`.
