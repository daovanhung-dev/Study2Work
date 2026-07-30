# Business Code Delta — Plan 17 — Admin Learner Lookup and Support Resolution

| API | Success code | Meaning |
|---:|---|---|
| 128 | `ADMIN_LEARNERS_RETRIEVED` | Tra cứu học viên theo tên, liên hệ, mã, lộ trình và trạng thái. thành công. |
| 129 | `ADMIN_LEARNERS_SUPPORT_PROFILE_RETRIEVED` | Lấy hồ sơ hỗ trợ tổng hợp, không trả mật khẩu/OTP. thành công. |
| 130 | `ADMIN_LEARNERS_PROGRESS_RETRIEVED` | Xem tiến độ chi tiết phục vụ hỗ trợ nhưng không sửa trực tiếp. thành công. |
| 131 | `ADMIN_SUPPORT_REQUESTS_RETRIEVED` | Lấy hàng đợi yêu cầu đổi/reset/hủy lộ trình. thành công. |
| 132 | `ADMIN_SUPPORT_REQUESTS_RETRIEVED` | Xem yêu cầu, hồ sơ, tiến độ và lịch sử xử lý trước khi quyết định. thành công. |
| 133 | `SUPPORT_REQUEST_RESOLVED` | Chấp thuận/từ chối yêu cầu và chọn hành động ngoại lệ. thành công. |

Shared error codes: `REQUEST_REQUIRED`, `REQUEST_INVALID_FORMAT`, `METHOD_NOT_ALLOWED`, `AUTHENTICATION_REQUIRED`, `ACCESS_DENIED`, `RESOURCE_NOT_FOUND`, `BUSINESS_RULE_VIOLATION`, `CONCURRENT_UPDATE_CONFLICT`, `IDEMPOTENCY_CONFLICT`, `RATE_LIMIT_EXCEEDED`, `DEPENDENCY_UNAVAILABLE`, `INTERNAL_ERROR`.
