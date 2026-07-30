# Business Code Delta — Plan 02 — Authentication Core

| API | Success code | Meaning |
|---:|---|---|
| 007 | `ACCOUNT_REGISTERED_PENDING_VERIFICATION` | Tạo tài khoản học viên ở trạng thái chờ xác thực. thành công. |
| 008 | `ACCOUNT_LOGIN_SUCCEEDED` | Đăng nhập và trả ngữ cảnh điều hướng theo trạng thái tài khoản. thành công. |
| 009 | `AUTH_LOGOUT_COMPLETED` | Đăng xuất phiên hiện tại. thành công. |
| 010 | `AUTH_VERIFICATION_SEND_COMPLETED` | Gửi hoặc gửi lại link/OTP xác thực có giới hạn chống spam. thành công. |
| 011 | `ACCOUNT_CONTACT_VERIFIED` | Xác nhận email/điện thoại và chuyển tài khoản sang VERIFIED. thành công. |
| 012 | `AUTH_ACCOUNT_STATUS_RETRIEVED` | Lấy trạng thái tài khoản, xác thực, onboarding và quyền học hiện tại. thành công. |
| 013 | `AUTH_PASSWORD_FORGOT_COMPLETED` | Khởi tạo quy trình khôi phục mật khẩu mà không tiết lộ tài khoản có tồn tại. thành công. |
| 014 | `AUTH_PASSWORD_RESET_COMPLETED` | Đặt mật khẩu mới bằng token/OTP khôi phục. thành công. |
| 015 | `AUTH_PASSWORD_UPDATED` | Đổi mật khẩu khi đã đăng nhập. thành công. |

Shared error codes: `REQUEST_REQUIRED`, `REQUEST_INVALID_FORMAT`, `METHOD_NOT_ALLOWED`, `AUTHENTICATION_REQUIRED`, `ACCESS_DENIED`, `RESOURCE_NOT_FOUND`, `BUSINESS_RULE_VIOLATION`, `CONCURRENT_UPDATE_CONFLICT`, `IDEMPOTENCY_CONFLICT`, `RATE_LIMIT_EXCEEDED`, `DEPENDENCY_UNAVAILABLE`, `INTERNAL_ERROR`.
