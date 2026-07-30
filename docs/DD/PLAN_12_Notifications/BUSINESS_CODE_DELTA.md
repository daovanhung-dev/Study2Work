# Business Code Delta — Plan 12 — Notifications

| API | Success code | Meaning |
|---:|---|---|
| 083 | `NOTIFICATIONS_LISTED` | Lấy trung tâm thông báo in-app có lọc và phân trang. thành công. |
| 084 | `NOTIFICATIONS_UNREAD_COUNT_RETRIEVED` | Lấy tổng số thông báo chưa đọc theo nhóm. thành công. |
| 085 | `NOTIFICATIONS_READ_UPDATED` | Đánh dấu một thông báo đã đọc. thành công. |
| 086 | `NOTIFICATIONS_READ_ALL_COMPLETED` | Đánh dấu đã đọc toàn bộ hoặc theo nhóm. thành công. |
| 087 | `NOTIFICATIONS_DELETED` | Ẩn/xóa thông báo khỏi trung tâm theo chính sách. thành công. |
| 088 | `NOTIFICATION_SETTINGS_ME_RETRIEVED` | Lấy thiết lập các kênh và loại thông báo có thể tùy chỉnh. thành công. |
| 089 | `NOTIFICATION_SETTINGS_ME_UPDATED` | Cập nhật thông báo không bắt buộc; không cho tắt sự kiện bảo mật/học tập bắt buộc. thành công. |
| 090 | `ADMIN_NOTIFICATIONS_RECIPIENT_PREVIEW_CREATED` | Xem trước nhóm người nhận trước khi gửi thông báo thủ công. thành công. |
| 091 | `ADMIN_NOTIFICATION_CREATED` | Gửi hoặc lên lịch thông báo tới nhóm học viên liên quan. thành công. |
| 092 | `ADMIN_NOTIFICATIONS_RETRIEVED` | Xem lịch sử thông báo thủ công và trạng thái gửi. thành công. |
| 093 | `ADMIN_NOTIFICATIONS_CANCEL_COMPLETED` | Hủy lô thông báo chưa gửi. thành công. |

Shared error codes: `REQUEST_REQUIRED`, `REQUEST_INVALID_FORMAT`, `METHOD_NOT_ALLOWED`, `AUTHENTICATION_REQUIRED`, `ACCESS_DENIED`, `RESOURCE_NOT_FOUND`, `BUSINESS_RULE_VIOLATION`, `CONCURRENT_UPDATE_CONFLICT`, `IDEMPOTENCY_CONFLICT`, `RATE_LIMIT_EXCEEDED`, `DEPENDENCY_UNAVAILABLE`, `INTERNAL_ERROR`.
