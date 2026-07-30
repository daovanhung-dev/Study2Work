# Business Code Delta — Plan 13 — Admin Learning Paths

| API | Success code | Meaning |
|---:|---|---|
| 094 | `ADMIN_LEARNING_PATHS_RETRIEVED` | Tra cứu lộ trình ở mọi trạng thái vòng đời. thành công. |
| 095 | `ADMIN_LEARNING_PATHS_CREATED` | Tạo lộ trình bản nháp. thành công. |
| 096 | `ADMIN_LEARNING_PATHS_RETRIEVED` | Lấy chi tiết quản trị lộ trình và cấu hình khóa học. thành công. |
| 097 | `ADMIN_LEARNING_PATHS_UPDATED` | Cập nhật thông tin và điều kiện lộ trình. thành công. |
| 098 | `ADMIN_LEARNING_PATHS_COURSES_UPDATED` | Gán và sắp xếp khóa học bắt buộc/tùy chọn trong lộ trình. thành công. |
| 099 | `ADMIN_LEARNING_PATHS_IMPACT_RETRIEVED` | Xem số học viên, khóa học và tiến độ bị ảnh hưởng trước thay đổi. thành công. |
| 100 | `ADMIN_LEARNING_PATHS_LIFECYCLE_COMPLETED` | Chuyển trạng thái DRAFT/IN_REVIEW/PUBLISHED/UPDATED/ARCHIVED. thành công. |

Shared error codes: `REQUEST_REQUIRED`, `REQUEST_INVALID_FORMAT`, `METHOD_NOT_ALLOWED`, `AUTHENTICATION_REQUIRED`, `ACCESS_DENIED`, `RESOURCE_NOT_FOUND`, `BUSINESS_RULE_VIOLATION`, `CONCURRENT_UPDATE_CONFLICT`, `IDEMPOTENCY_CONFLICT`, `RATE_LIMIT_EXCEEDED`, `DEPENDENCY_UNAVAILABLE`, `INTERNAL_ERROR`.
