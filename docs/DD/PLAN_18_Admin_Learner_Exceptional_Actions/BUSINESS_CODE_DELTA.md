# Business Code Delta — Plan 18 — Admin Learner Exceptional Actions

| API | Success code | Meaning |
|---:|---|---|
| 134 | `ADMIN_LEARNERS_PROGRESS_RESET_COMPLETED` | Reset tiến độ theo phạm vi và lý do bắt buộc. thành công. |
| 135 | `ADMIN_LEARNERS_ACTIVE_PATH_CANCEL_COMPLETED` | Hủy lộ trình ACTIVE theo ngoại lệ. thành công. |
| 136 | `ADMIN_LEARNERS_ACTIVE_PATH_TRANSFER_COMPLETED` | Chuyển lộ trình bảo đảm không tạo hai lộ trình ACTIVE đồng thời. thành công. |
| 137 | `ADMIN_LEARNERS_SUSPEND_COMPLETED` | Tạm ngừng tài khoản vì vi phạm, bảo vệ tài khoản hoặc yêu cầu nội bộ. thành công. |
| 138 | `ADMIN_LEARNERS_UNSUSPEND_COMPLETED` | Mở lại tài khoản và ghi lý do. thành công. |
| 139 | `ADMIN_LEARNERS_SUPPORT_NOTES_RETRIEVED` | Lấy ghi chú nội bộ theo quyền. thành công. |
| 140 | `ADMIN_LEARNERS_SUPPORT_NOTES_CREATED` | Tạo ghi chú nội bộ hoặc phản hồi chính thức. thành công. |
| 141 | `ADMIN_LEARNERS_AUDIT_RETRIEVED` | Xem audit log liên quan riêng đến học viên. thành công. |

Shared error codes: `REQUEST_REQUIRED`, `REQUEST_INVALID_FORMAT`, `METHOD_NOT_ALLOWED`, `AUTHENTICATION_REQUIRED`, `ACCESS_DENIED`, `RESOURCE_NOT_FOUND`, `BUSINESS_RULE_VIOLATION`, `CONCURRENT_UPDATE_CONFLICT`, `IDEMPOTENCY_CONFLICT`, `RATE_LIMIT_EXCEEDED`, `DEPENDENCY_UNAVAILABLE`, `INTERNAL_ERROR`.
