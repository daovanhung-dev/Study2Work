# Business Code Delta — Plan 01 — Public Catalog

| API | Success code | Meaning |
|---:|---|---|
| 001 | `CATALOG_OVERVIEW_RETRIEVED` | Lấy nội dung giới thiệu Study và điều hướng đến danh mục. thành công. |
| 002 | `CATALOG_LEARNING_PATHS_LISTED` | Tìm kiếm, lọc và phân trang lộ trình đã công khai. thành công. |
| 003 | `CATALOG_LEARNING_PATHS_SLUG_RETRIEVED` | Xem chi tiết lộ trình công khai và hành động phù hợp trạng thái người xem. thành công. |
| 004 | `CATALOG_COURSES_RETRIEVED` | Tìm kiếm, lọc danh sách khóa học công khai. thành công. |
| 005 | `CATALOG_COURSES_SLUG_RETRIEVED` | Xem thông tin khóa học, curriculum công khai và lộ trình sử dụng khóa học. thành công. |
| 006 | `CATALOG_SAMPLE_LESSON_LOADED` | Xem phần bài học mẫu được Admin cho phép công khai; không tạo tiến độ. thành công. |

Shared error codes: `REQUEST_REQUIRED`, `REQUEST_INVALID_FORMAT`, `METHOD_NOT_ALLOWED`, `AUTHENTICATION_REQUIRED`, `ACCESS_DENIED`, `RESOURCE_NOT_FOUND`, `BUSINESS_RULE_VIOLATION`, `CONCURRENT_UPDATE_CONFLICT`, `IDEMPOTENCY_CONFLICT`, `RATE_LIMIT_EXCEEDED`, `DEPENDENCY_UNAVAILABLE`, `INTERNAL_ERROR`.
