# Business Code Delta — Plan 14 — Admin Courses

| API | Success code | Meaning |
|---:|---|---|
| 101 | `ADMIN_COURSES_RETRIEVED` | Tra cứu khóa học ở mọi trạng thái. thành công. |
| 102 | `ADMIN_COURSES_CREATED` | Tạo khóa học bản nháp. thành công. |
| 103 | `ADMIN_COURSES_RETRIEVED` | Lấy cấu hình đầy đủ khóa học, curriculum và tác động. thành công. |
| 104 | `ADMIN_COURSES_UPDATED` | Cập nhật thông tin, điều kiện hoàn thành và nhóm cộng đồng khóa học. thành công. |
| 105 | `ADMIN_COURSES_PATHS_UPDATED` | Gán khóa học vào một hoặc nhiều lộ trình. thành công. |
| 106 | `ADMIN_COURSES_CHAPTERS_ORDER_UPDATED` | Sắp xếp thứ tự chương trong khóa học. thành công. |
| 107 | `ADMIN_COURSES_IMPACT_RETRIEVED` | Xem học viên và lộ trình bị ảnh hưởng trước cập nhật khóa học. thành công. |
| 108 | `ADMIN_COURSES_LIFECYCLE_COMPLETED` | Chuyển trạng thái vòng đời khóa học. thành công. |

Shared error codes: `REQUEST_REQUIRED`, `REQUEST_INVALID_FORMAT`, `METHOD_NOT_ALLOWED`, `AUTHENTICATION_REQUIRED`, `ACCESS_DENIED`, `RESOURCE_NOT_FOUND`, `BUSINESS_RULE_VIOLATION`, `CONCURRENT_UPDATE_CONFLICT`, `IDEMPOTENCY_CONFLICT`, `RATE_LIMIT_EXCEEDED`, `DEPENDENCY_UNAVAILABLE`, `INTERNAL_ERROR`.
