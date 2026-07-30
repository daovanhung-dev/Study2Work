# Business Code Delta — Plan 10 — Learner Community

| API | Success code | Meaning |
|---:|---|---|
| 070 | `COMMUNITY_GROUPS_RETRIEVED` | Lấy các nhóm cộng đồng phù hợp theo quyền, lộ trình, khóa học hoặc chủ đề. thành công. |
| 071 | `COMMUNITY_GROUPS_RETRIEVED` | Xem thông tin nhóm và quy tắc; link chỉ trả khi đủ quyền. thành công. |
| 072 | `COMMUNITY_LINK_OPENED` | Xác nhận đã đọc quy tắc, ghi nhận sự kiện mở link và trả liên kết Zalo. thành công. |
| 073 | `COMMUNITY_REPORT_CREATED` | Báo link hỏng, spam/lừa đảo, sai nội dung, moderator hoặc quy tắc. thành công. |
| 074 | `ME_COMMUNITY_REPORTS_RETRIEVED` | Theo dõi báo cáo cộng đồng đã gửi. thành công. |

Shared error codes: `REQUEST_REQUIRED`, `REQUEST_INVALID_FORMAT`, `METHOD_NOT_ALLOWED`, `AUTHENTICATION_REQUIRED`, `ACCESS_DENIED`, `RESOURCE_NOT_FOUND`, `BUSINESS_RULE_VIOLATION`, `CONCURRENT_UPDATE_CONFLICT`, `IDEMPOTENCY_CONFLICT`, `RATE_LIMIT_EXCEEDED`, `DEPENDENCY_UNAVAILABLE`, `INTERNAL_ERROR`.
