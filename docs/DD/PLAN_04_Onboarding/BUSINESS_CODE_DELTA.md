# Business Code Delta — Plan 04 — Onboarding

| API | Success code | Meaning |
|---:|---|---|
| 021 | `ONBOARDING_CONFIG_RETRIEVED` | Lấy cấu hình bước onboarding, mục tiêu, công nghệ và lựa chọn nền tảng. thành công. |
| 022 | `ONBOARDING_CURRENT_RETRIEVED` | Lấy trạng thái onboarding, bản nháp và bước cần tiếp tục. thành công. |
| 023 | `ONBOARDING_DRAFT_SAVED` | Lưu hợp lệ dữ liệu từng bước và cho phép tiếp tục sau khi thoát. thành công. |
| 024 | `ONBOARDING_RECOMMENDED_PATHS_RETRIEVED` | Sinh danh sách lộ trình gợi ý từ hồ sơ onboarding. thành công. |
| 025 | `ONBOARDING_SELECTED_PATH_UPDATED` | Chọn duy nhất một lộ trình để xác nhận; chưa kích hoạt. thành công. |
| 026 | `ONBOARDING_REVIEW_RETRIEVED` | Lấy toàn bộ thông tin xác nhận trước khi hoàn tất onboarding. thành công. |
| 027 | `ONBOARDING_COMPLETED` | Xác nhận dữ liệu và chuyển tài khoản sang READY_TO_LEARN. thành công. |

Shared error codes: `REQUEST_REQUIRED`, `REQUEST_INVALID_FORMAT`, `METHOD_NOT_ALLOWED`, `AUTHENTICATION_REQUIRED`, `ACCESS_DENIED`, `RESOURCE_NOT_FOUND`, `BUSINESS_RULE_VIOLATION`, `CONCURRENT_UPDATE_CONFLICT`, `IDEMPOTENCY_CONFLICT`, `RATE_LIMIT_EXCEEDED`, `DEPENDENCY_UNAVAILABLE`, `INTERNAL_ERROR`.
