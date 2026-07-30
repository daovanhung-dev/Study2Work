# Business Code Delta — Plan 19 — Operational Reports

| API | Success code | Meaning |
|---:|---|---|
| 142 | `ADMIN_REPORT_OVERVIEW_LOADED` | Lấy dashboard tổng quan tài khoản, onboarding, học tập, bài tập và cộng đồng. thành công. |
| 143 | `ADMIN_REPORTS_REGISTRATIONS_RETRIEVED` | Báo cáo đăng ký và xác thực. thành công. |
| 144 | `ADMIN_REPORTS_ONBOARDING_RETRIEVED` | Báo cáo bắt đầu/hoàn thành onboarding và điểm rơi theo bước. thành công. |
| 145 | `ADMIN_REPORTS_LEARNING_PATHS_RETRIEVED` | Báo cáo kích hoạt, đang học, hoàn thành, thời gian và đổi/reset theo lộ trình. thành công. |
| 146 | `ADMIN_REPORTS_COURSES_RETRIEVED` | Báo cáo bắt đầu/hoàn thành khóa và điểm nghẽn bài học. thành công. |
| 147 | `ADMIN_REPORTS_ASSIGNMENTS_RETRIEVED` | Báo cáo nộp bài, kết quả, thời gian nộp và backlog review. thành công. |
| 148 | `ADMIN_REPORTS_COMMUNITY_RETRIEVED` | Báo cáo lượt mở link và vấn đề nhóm cộng đồng. thành công. |
| 149 | `ADMIN_OPERATION_ALERTS_LOADED` | Lấy cảnh báo vận hành theo ngưỡng đã cấu hình. thành công. |

Shared error codes: `REQUEST_REQUIRED`, `REQUEST_INVALID_FORMAT`, `METHOD_NOT_ALLOWED`, `AUTHENTICATION_REQUIRED`, `ACCESS_DENIED`, `RESOURCE_NOT_FOUND`, `BUSINESS_RULE_VIOLATION`, `CONCURRENT_UPDATE_CONFLICT`, `IDEMPOTENCY_CONFLICT`, `RATE_LIMIT_EXCEEDED`, `DEPENDENCY_UNAVAILABLE`, `INTERNAL_ERROR`.
