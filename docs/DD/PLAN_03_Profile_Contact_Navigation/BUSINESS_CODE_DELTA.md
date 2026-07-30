# Business Code Delta — Plan 03 — Profile Contact Navigation

| API | Success code | Meaning |
|---:|---|---|
| 016 | `ME_PROFILE_RETRIEVED` | Lấy hồ sơ tài khoản, hồ sơ học tập và thiết lập cá nhân. thành công. |
| 017 | `ME_PROFILE_UPDATED` | Cập nhật các trường hồ sơ học viên được phép tự sửa. thành công. |
| 018 | `ME_CONTACT_CHANGE_CREATED` | Yêu cầu đổi email/số điện thoại và gửi xác thực kênh mới. thành công. |
| 019 | `ME_CONTACT_CHANGE_CONFIRM_COMPLETED` | Xác nhận kênh liên hệ mới trước khi áp dụng. thành công. |
| 020 | `ME_NAVIGATION_CONTEXT_RETRIEVED` | Xác định màn hình đích sau đăng nhập hoặc khi mở hành động bắt đầu học. thành công. |

Shared error codes: `REQUEST_REQUIRED`, `REQUEST_INVALID_FORMAT`, `METHOD_NOT_ALLOWED`, `AUTHENTICATION_REQUIRED`, `ACCESS_DENIED`, `RESOURCE_NOT_FOUND`, `BUSINESS_RULE_VIOLATION`, `CONCURRENT_UPDATE_CONFLICT`, `IDEMPOTENCY_CONFLICT`, `RATE_LIMIT_EXCEEDED`, `DEPENDENCY_UNAVAILABLE`, `INTERNAL_ERROR`.
