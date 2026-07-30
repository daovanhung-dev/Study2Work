# Study2Work — Business Code Catalog

## 1. Mục đích

`businessCode` là mã ổn định để frontend, backend, log và contract test nhận biết kết quả nghiệp vụ mà không phụ thuộc vào nội dung `message`.

- Tổng số mã: **423**.
- Mã thành công: **262**.
- Mã lỗi: **161**.
- Study: ánh xạ đủ **157/157 API DD**.
- Work: mã đề xuất theo kiến trúc đích vì tài liệu được cung cấp chưa có bộ Work BD/DD API hoàn chỉnh.

## 2. Quy tắc đặt tên

```text
<DOMAIN>_<RESOURCE>_<RESULT>
```

Ví dụ:

```text
ACCOUNT_LOGIN_SUCCEEDED
COURSE_DETAIL_RETRIEVED
APPLICATION_STATUS_UPDATED
STUDY_EVIDENCE_CONSENT_REQUIRED
```

Quy ước động từ:

| Hậu tố | Dùng khi |
|---|---|
| `LISTED` | Trả danh sách. |
| `LOADED` | Trả view, dashboard, summary hoặc read model. |
| `RETRIEVED` | Trả một resource cụ thể. |
| `CREATED` | Tạo resource. |
| `UPDATED` | Cập nhật resource hoặc trạng thái. |
| `DELETED` | Xóa mềm/xóa resource và vẫn trả envelope. |
| `SUCCEEDED` | Command không phù hợp với CRUD, ví dụ login/logout. |

> Không dùng `message` để điều khiển logic. Không đổi giá trị `businessCode` sau khi đã phát hành; khi cần thay, tạo mã mới và deprecate mã cũ.

## 3. Phân biệt hai loại code

| Vị trí | Mục đích | Ví dụ |
|---|---|---|
| `response.businessCode` | Kết quả tổng thể của request. | `VALIDATION_ERROR` |
| `response.errors[].code` | Lỗi cụ thể theo trường hoặc chi tiết. | `FIELD_REQUIRED` |

Ví dụ:

```json
{
  "success": false,
  "businessCode": "VALIDATION_ERROR",
  "message": "Dữ liệu đầu vào không hợp lệ.",
  "errors": [
    {
      "code": "FIELD_REQUIRED",
      "field": "email",
      "message": "email là bắt buộc."
    }
  ],
  "traceId": "uuid"
}
```

## 4. Mức độ căn cứ

| Giá trị | Ý nghĩa |
|---|---|
| `BD_CONFIRMED` | Có mã xuất hiện trực tiếp trong BD/Sequence. |
| `BD_DERIVED` | Suy ra từ quy tắc nghiệp vụ trong BD. |
| `DD_DERIVED` | Suy ra từ API/endpoint trong DD catalog. |
| `COMMON_PROPOSED` | Mã dùng chung được đề xuất. |
| `TARGET_PROPOSED` | Đề xuất cho kiến trúc đích, chưa phải contract đã phê duyệt. |

## 5. Mã dùng chung Platform

| Code | Loại | HTTP | Message | Căn cứ |
|---|---:|---:|---|---|
| `BUSINESS_RULE_VIOLATION` | ERROR | 409 | Yêu cầu vi phạm quy tắc nghiệp vụ. | `COMMON_PROPOSED` |
| `CONCURRENCY_CONFLICT` | ERROR | 409 | Dữ liệu đã được thay đổi bởi một thao tác khác. | `COMMON_PROPOSED` |
| `DUPLICATE_RESOURCE` | ERROR | 409 | Tài nguyên đã tồn tại. | `COMMON_PROPOSED` |
| `INVALID_REQUEST` | ERROR | 400 | Yêu cầu không hợp lệ. | `COMMON_PROPOSED` |
| `INVALID_STATE_TRANSITION` | ERROR | 409 | Không thể chuyển sang trạng thái yêu cầu. | `COMMON_PROPOSED` |
| `NOT_IMPLEMENTED` | ERROR | 501 | Chức năng chưa được triển khai. | `COMMON_PROPOSED` |
| `RESOURCE_CONFLICT` | ERROR | 409 | Tài nguyên đang ở trạng thái xung đột. | `COMMON_PROPOSED` |
| `RESOURCE_NOT_FOUND` | ERROR | 404 | Không tìm thấy tài nguyên yêu cầu. | `COMMON_PROPOSED` |
| `VALIDATION_ERROR` | ERROR | 422 | Dữ liệu đầu vào không hợp lệ. | `COMMON_PROPOSED` |
| `IDEMPOTENCY_KEY_REQUIRED` | ERROR | 400 | Mutation này yêu cầu Idempotency-Key. | `COMMON_PROPOSED` |
| `IDEMPOTENCY_KEY_REUSED` | ERROR | 409 | Idempotency-Key đã được dùng với payload khác. | `COMMON_PROPOSED` |
| `FILE_TYPE_NOT_ALLOWED` | ERROR | 422 | Loại tệp không được phép. | `COMMON_PROPOSED` |
| `FILE_UPLOAD_FAILED` | ERROR | 500 | Tải tệp lên không thành công. | `COMMON_PROPOSED` |
| `PAYLOAD_TOO_LARGE` | ERROR | 413 | Dữ liệu gửi lên vượt quá giới hạn. | `COMMON_PROPOSED` |
| `UNSUPPORTED_MEDIA_TYPE` | ERROR | 415 | Định dạng nội dung không được hỗ trợ. | `COMMON_PROPOSED` |
| `HEALTH_LIVE` | SUCCESS | 200 | Dịch vụ đang hoạt động. | `TARGET_PROPOSED` |
| `HEALTH_READY` | SUCCESS | 200 | Dịch vụ sẵn sàng nhận request. | `TARGET_PROPOSED` |
| `DATABASE_OPERATION_FAILED` | ERROR | 500 | Thao tác dữ liệu không thành công. | `COMMON_PROPOSED` |
| `DEPENDENCY_UNAVAILABLE` | ERROR | 503 | Dịch vụ phụ thuộc tạm thời không khả dụng. | `COMMON_PROPOSED` |
| `INTERNAL_SERVER_ERROR` | ERROR | 500 | Đã xảy ra lỗi nội bộ hệ thống. | `COMMON_PROPOSED` |
| `SERVICE_UNAVAILABLE` | ERROR | 503 | Dịch vụ tạm thời không khả dụng. | `COMMON_PROPOSED` |
| `ACCESS_TOKEN_EXPIRED` | ERROR | 401 | Access token đã hết hạn. | `COMMON_PROPOSED` |
| `AUTHENTICATION_REQUIRED` | ERROR | 401 | Yêu cầu xác thực người dùng. | `COMMON_PROPOSED` |
| `INVALID_ACCESS_TOKEN` | ERROR | 401 | Access token không hợp lệ. | `COMMON_PROPOSED` |
| `PERMISSION_DENIED` | ERROR | 403 | Người dùng không có quyền thực hiện thao tác. | `COMMON_PROPOSED` |
| `RATE_LIMIT_EXCEEDED` | ERROR | 429 | Đã vượt quá giới hạn request. | `COMMON_PROPOSED` |

## 6. Study — ánh xạ 157 API

### 01. Public Catalog

| API ID | Method | Endpoint | Business code | HTTP | Căn cứ |
|---|---:|---|---|---:|---|
| `S2W-STUDY-API-001` | `GET` | `/api/v1/catalog/overview` | `CATALOG_OVERVIEW_LOADED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-002` | `GET` | `/api/v1/catalog/learning-paths` | `CATALOG_LEARNING_PATHS_LISTED` | 200 | `BD_CONFIRMED` |
| `S2W-STUDY-API-003` | `GET` | `/api/v1/catalog/learning-paths/{slug}` | `CATALOG_LEARNING_PATH_DETAIL_LOADED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-004` | `GET` | `/api/v1/catalog/courses` | `CATALOG_COURSES_LISTED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-005` | `GET` | `/api/v1/catalog/courses/{slug}` | `CATALOG_COURSE_DETAIL_LOADED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-006` | `GET` | `/api/v1/catalog/sample-lessons/{lesson_id}` | `CATALOG_SAMPLE_LESSON_LOADED` | 200 | `BD_CONFIRMED` |
### 02. Tài khoản, xác thực và hồ sơ

| API ID | Method | Endpoint | Business code | HTTP | Căn cứ |
|---|---:|---|---|---:|---|
| `S2W-STUDY-API-007` | `POST` | `/api/v1/auth/register` | `ACCOUNT_REGISTERED_PENDING_VERIFICATION` | 201 | `BD_CONFIRMED` |
| `S2W-STUDY-API-008` | `POST` | `/api/v1/auth/login` | `ACCOUNT_LOGIN_SUCCEEDED` | 200 | `BD_CONFIRMED` |
| `S2W-STUDY-API-009` | `POST` | `/api/v1/auth/logout` | `ACCOUNT_LOGOUT_SUCCEEDED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-010` | `POST` | `/api/v1/auth/verification/send` | `ACCOUNT_VERIFICATION_SENT` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-011` | `POST` | `/api/v1/auth/verify-contact` | `ACCOUNT_CONTACT_VERIFIED` | 200 | `BD_CONFIRMED` |
| `S2W-STUDY-API-012` | `GET` | `/api/v1/auth/account-status` | `ACCOUNT_STATUS_LOADED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-013` | `POST` | `/api/v1/auth/password/forgot` | `ACCOUNT_PASSWORD_RESET_REQUESTED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-014` | `POST` | `/api/v1/auth/password/reset` | `ACCOUNT_PASSWORD_RESET_SUCCEEDED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-015` | `PUT` | `/api/v1/auth/password` | `ACCOUNT_PASSWORD_CHANGED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-016` | `GET` | `/api/v1/me/profile` | `ACCOUNT_PROFILE_LOADED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-017` | `PATCH` | `/api/v1/me/profile` | `ACCOUNT_PROFILE_UPDATED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-018` | `POST` | `/api/v1/me/contact-change` | `ACCOUNT_CONTACT_CHANGE_REQUESTED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-019` | `POST` | `/api/v1/me/contact-change/confirm` | `ACCOUNT_CONTACT_CHANGED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-020` | `GET` | `/api/v1/me/navigation-context` | `ACCOUNT_NAVIGATION_CONTEXT_LOADED` | 200 | `DD_DERIVED` |
### 03. Onboarding

| API ID | Method | Endpoint | Business code | HTTP | Căn cứ |
|---|---:|---|---|---:|---|
| `S2W-STUDY-API-021` | `GET` | `/api/v1/onboarding/config` | `ONBOARDING_CONFIG_LOADED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-022` | `GET` | `/api/v1/onboarding/current` | `ONBOARDING_CURRENT_LOADED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-023` | `PATCH` | `/api/v1/onboarding/draft` | `ONBOARDING_DRAFT_SAVED` | 200 | `BD_CONFIRMED` |
| `S2W-STUDY-API-024` | `GET` | `/api/v1/onboarding/recommended-paths` | `ONBOARDING_RECOMMENDED_PATHS_LOADED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-025` | `PUT` | `/api/v1/onboarding/selected-path` | `ONBOARDING_SELECTED_PATH_UPDATED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-026` | `GET` | `/api/v1/onboarding/review` | `ONBOARDING_REVIEW_LOADED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-027` | `POST` | `/api/v1/onboarding/confirm` | `ONBOARDING_COMPLETED` | 200 | `BD_CONFIRMED` |
### 04. Lộ trình học

| API ID | Method | Endpoint | Business code | HTTP | Căn cứ |
|---|---:|---|---|---:|---|
| `S2W-STUDY-API-028` | `GET` | `/api/v1/learning-paths` | `LEARNING_PATHS_LISTED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-029` | `GET` | `/api/v1/learning-paths/{path_id}` | `LEARNING_PATH_DETAIL_LOADED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-030` | `POST` | `/api/v1/learning-paths/{path_id}/activation-preview` | `LEARNING_PATH_ACTIVATION_PREVIEW_LOADED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-031` | `POST` | `/api/v1/learning-paths/{path_id}/activate` | `LEARNING_PATH_ACTIVATED` | 200 | `BD_CONFIRMED` |
| `S2W-STUDY-API-032` | `GET` | `/api/v1/me/learning-paths/active` | `ACTIVE_LEARNING_PATH_LOADED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-033` | `GET` | `/api/v1/me/learning-paths/history` | `LEARNING_PATH_HISTORY_LISTED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-034` | `GET` | `/api/v1/me/learning-paths/{enrollment_id}/summary` | `LEARNING_PATH_ENROLLMENT_SUMMARY_LOADED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-035` | `GET` | `/api/v1/me/learning-paths/next-recommendations` | `LEARNING_PATH_RECOMMENDATIONS_LOADED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-036` | `POST` | `/api/v1/support-requests` | `SUPPORT_REQUEST_CREATED` | 201 | `BD_CONFIRMED` |
| `S2W-STUDY-API-037` | `GET` | `/api/v1/support-requests` | `SUPPORT_REQUESTS_LISTED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-038` | `GET` | `/api/v1/support-requests/{request_id}` | `SUPPORT_REQUEST_DETAIL_LOADED` | 200 | `DD_DERIVED` |
### 05. Khóa học, chương, bài học và tài nguyên

| API ID | Method | Endpoint | Business code | HTTP | Căn cứ |
|---|---:|---|---|---:|---|
| `S2W-STUDY-API-039` | `GET` | `/api/v1/courses/{course_id}` | `COURSE_DETAIL_RETRIEVED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-040` | `GET` | `/api/v1/courses/{course_id}/curriculum` | `COURSE_CURRICULUM_LOADED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-041` | `GET` | `/api/v1/chapters/{chapter_id}` | `CHAPTER_DETAIL_RETRIEVED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-042` | `GET` | `/api/v1/lessons/{lesson_id}/study` | `LESSON_STUDY_LOADED` | 200 | `BD_CONFIRMED` |
| `S2W-STUDY-API-043` | `GET` | `/api/v1/courses/{course_id}/continue` | `COURSE_CONTINUE_CONTEXT_LOADED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-044` | `GET` | `/api/v1/lessons/{lesson_id}/resources` | `LESSON_RESOURCES_LISTED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-045` | `GET` | `/api/v1/resources/{resource_id}/access` | `RESOURCE_ACCESS_GRANTED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-046` | `POST` | `/api/v1/content-issues` | `CONTENT_ISSUE_CREATED` | 201 | `DD_DERIVED` |
| `S2W-STUDY-API-047` | `GET` | `/api/v1/me/content-issues` | `CONTENT_ISSUES_LISTED` | 200 | `DD_DERIVED` |
### 06. Bài tập và đánh giá

| API ID | Method | Endpoint | Business code | HTTP | Căn cứ |
|---|---:|---|---|---:|---|
| `S2W-STUDY-API-048` | `GET` | `/api/v1/exercises` | `EXERCISES_LISTED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-049` | `GET` | `/api/v1/exercises/{assignment_id}` | `EXERCISE_DETAIL_RETRIEVED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-050` | `GET` | `/api/v1/exercises/{assignment_id}/draft` | `EXERCISE_DRAFT_LOADED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-051` | `PUT` | `/api/v1/exercises/{assignment_id}/draft` | `EXERCISE_DRAFT_SAVED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-052` | `POST` | `/api/v1/exercises/{assignment_id}/submissions` | `EXERCISE_SUBMISSION_CREATED` | 200 | `BD_CONFIRMED` |
| `S2W-STUDY-API-053` | `GET` | `/api/v1/exercises/{assignment_id}/submissions/latest` | `EXERCISE_LATEST_SUBMISSION_LOADED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-054` | `GET` | `/api/v1/exercises/{assignment_id}/submissions` | `EXERCISE_SUBMISSIONS_LISTED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-055` | `GET` | `/api/v1/submissions/{submission_id}` | `EXERCISE_SUBMISSION_DETAIL_RETRIEVED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-056` | `POST` | `/api/v1/exercises/{assignment_id}/resubmissions` | `EXERCISE_RESUBMISSION_CREATED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-057` | `GET` | `/api/v1/admin/exercise-submissions` | `ADMIN_EXERCISE_SUBMISSIONS_LISTED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-058` | `GET` | `/api/v1/admin/exercise-submissions/{submission_id}` | `ADMIN_EXERCISE_SUBMISSION_DETAIL_LOADED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-059` | `PATCH` | `/api/v1/admin/exercise-submissions/{submission_id}/review` | `EXERCISE_SUBMISSION_REVIEWED` | 200 | `BD_CONFIRMED` |
| `S2W-STUDY-API-060` | `POST` | `/api/v1/admin/exercise-submissions/{submission_id}/reopen` | `EXERCISE_SUBMISSION_REOPENED` | 200 | `DD_DERIVED` |
### 07. Tiến độ và hoàn thành

| API ID | Method | Endpoint | Business code | HTTP | Căn cứ |
|---|---:|---|---|---:|---|
| `S2W-STUDY-API-061` | `GET` | `/api/v1/me/dashboard` | `LEARNER_DASHBOARD_LOADED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-062` | `GET` | `/api/v1/me/continue-learning` | `CONTINUE_LEARNING_CONTEXT_LOADED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-063` | `GET` | `/api/v1/me/progress/learning-paths/{path_id}` | `LEARNING_PATH_PROGRESS_LOADED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-064` | `GET` | `/api/v1/me/progress/courses/{course_id}` | `COURSE_PROGRESS_LOADED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-065` | `GET` | `/api/v1/me/progress/chapters/{chapter_id}` | `CHAPTER_PROGRESS_LOADED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-066` | `GET` | `/api/v1/me/progress/lessons/{lesson_id}` | `LESSON_PROGRESS_LOADED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-067` | `PATCH` | `/api/v1/lessons/{lesson_id}/progress` | `LESSON_PROGRESS_UPDATED` | 200 | `BD_CONFIRMED` |
| `S2W-STUDY-API-068` | `GET` | `/api/v1/me/learning-history` | `LEARNING_HISTORY_LISTED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-069` | `GET` | `/api/v1/me/completion-summaries/{entity_type}/{entity_id}` | `PROGRESS_SUMMARY_LOADED` | 200 | `BD_CONFIRMED` |
### 08. Cộng đồng Zalo

| API ID | Method | Endpoint | Business code | HTTP | Căn cứ |
|---|---:|---|---|---:|---|
| `S2W-STUDY-API-070` | `GET` | `/api/v1/community-groups` | `COMMUNITY_GROUPS_LISTED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-071` | `GET` | `/api/v1/community-groups/{group_id}` | `COMMUNITY_GROUP_DETAIL_RETRIEVED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-072` | `POST` | `/api/v1/community-groups/{group_id}/open-link` | `COMMUNITY_LINK_OPENED` | 200 | `BD_CONFIRMED` |
| `S2W-STUDY-API-073` | `POST` | `/api/v1/community-groups/{group_id}/reports` | `COMMUNITY_REPORT_CREATED` | 200 | `BD_CONFIRMED` |
| `S2W-STUDY-API-074` | `GET` | `/api/v1/me/community-reports` | `COMMUNITY_REPORTS_LISTED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-075` | `GET` | `/api/v1/admin/community-groups` | `ADMIN_COMMUNITY_GROUPS_LISTED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-076` | `POST` | `/api/v1/admin/community-groups` | `COMMUNITY_GROUP_CREATED` | 201 | `DD_DERIVED` |
| `S2W-STUDY-API-077` | `GET` | `/api/v1/admin/community-groups/{group_id}` | `ADMIN_COMMUNITY_GROUP_DETAIL_LOADED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-078` | `PATCH` | `/api/v1/admin/community-groups/{group_id}` | `COMMUNITY_GROUP_UPDATED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-079` | `PUT` | `/api/v1/admin/community-groups/{group_id}/status` | `COMMUNITY_GROUP_STATUS_UPDATED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-080` | `PUT` | `/api/v1/admin/community-groups/{group_id}/moderators` | `COMMUNITY_GROUP_MODERATORS_UPDATED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-081` | `GET` | `/api/v1/admin/community-reports` | `ADMIN_COMMUNITY_REPORTS_LISTED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-082` | `PATCH` | `/api/v1/admin/community-reports/{report_id}` | `COMMUNITY_REPORT_UPDATED` | 200 | `DD_DERIVED` |
### 09. Thông báo

| API ID | Method | Endpoint | Business code | HTTP | Căn cứ |
|---|---:|---|---|---:|---|
| `S2W-STUDY-API-083` | `GET` | `/api/v1/notifications` | `NOTIFICATIONS_LISTED` | 200 | `BD_CONFIRMED` |
| `S2W-STUDY-API-084` | `GET` | `/api/v1/notifications/unread-count` | `NOTIFICATION_UNREAD_COUNT_LOADED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-085` | `PATCH` | `/api/v1/notifications/{notification_id}/read` | `NOTIFICATION_MARKED_READ` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-086` | `POST` | `/api/v1/notifications/read-all` | `NOTIFICATIONS_MARKED_READ` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-087` | `DELETE` | `/api/v1/notifications/{notification_id}` | `NOTIFICATION_DELETED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-088` | `GET` | `/api/v1/notification-settings/me` | `NOTIFICATION_SETTINGS_LOADED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-089` | `PUT` | `/api/v1/notification-settings/me` | `NOTIFICATION_SETTINGS_UPDATED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-090` | `POST` | `/api/v1/admin/notifications/recipient-preview` | `ADMIN_NOTIFICATION_RECIPIENT_PREVIEW_LOADED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-091` | `POST` | `/api/v1/admin/notifications` | `ADMIN_NOTIFICATION_CREATED` | 201 | `BD_CONFIRMED` |
| `S2W-STUDY-API-092` | `GET` | `/api/v1/admin/notifications` | `ADMIN_NOTIFICATIONS_LISTED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-093` | `POST` | `/api/v1/admin/notifications/{batch_id}/cancel` | `ADMIN_NOTIFICATION_CANCELLED` | 200 | `DD_DERIVED` |
### 10. Admin quản trị nội dung

| API ID | Method | Endpoint | Business code | HTTP | Căn cứ |
|---|---:|---|---|---:|---|
| `S2W-STUDY-API-094` | `GET` | `/api/v1/admin/learning-paths` | `ADMIN_LEARNING_PATHS_LISTED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-095` | `POST` | `/api/v1/admin/learning-paths` | `LEARNING_PATH_CREATED` | 201 | `DD_DERIVED` |
| `S2W-STUDY-API-096` | `GET` | `/api/v1/admin/learning-paths/{path_id}` | `ADMIN_LEARNING_PATH_DETAIL_LOADED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-097` | `PATCH` | `/api/v1/admin/learning-paths/{path_id}` | `LEARNING_PATH_UPDATED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-098` | `PUT` | `/api/v1/admin/learning-paths/{path_id}/courses` | `LEARNING_PATH_COURSES_UPDATED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-099` | `GET` | `/api/v1/admin/learning-paths/{path_id}/impact` | `LEARNING_PATH_IMPACT_LOADED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-100` | `POST` | `/api/v1/admin/learning-paths/{path_id}/lifecycle` | `LEARNING_PATH_LIFECYCLE_UPDATED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-101` | `GET` | `/api/v1/admin/courses` | `ADMIN_COURSES_LISTED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-102` | `POST` | `/api/v1/admin/courses` | `COURSE_CREATED` | 201 | `DD_DERIVED` |
| `S2W-STUDY-API-103` | `GET` | `/api/v1/admin/courses/{course_id}` | `ADMIN_COURSE_DETAIL_LOADED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-104` | `PATCH` | `/api/v1/admin/courses/{course_id}` | `COURSE_UPDATED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-105` | `PUT` | `/api/v1/admin/courses/{course_id}/paths` | `COURSE_PATHS_UPDATED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-106` | `PUT` | `/api/v1/admin/courses/{course_id}/chapters/order` | `COURSE_CHAPTER_ORDER_UPDATED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-107` | `GET` | `/api/v1/admin/courses/{course_id}/impact` | `COURSE_IMPACT_LOADED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-108` | `POST` | `/api/v1/admin/courses/{course_id}/lifecycle` | `COURSE_LIFECYCLE_UPDATED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-109` | `POST` | `/api/v1/admin/courses/{course_id}/chapters` | `CHAPTER_CREATED` | 201 | `DD_DERIVED` |
| `S2W-STUDY-API-110` | `PATCH` | `/api/v1/admin/chapters/{chapter_id}` | `CHAPTER_UPDATED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-111` | `DELETE` | `/api/v1/admin/chapters/{chapter_id}` | `CHAPTER_DELETED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-112` | `PUT` | `/api/v1/admin/chapters/{chapter_id}/items/order` | `CHAPTER_ITEM_ORDER_UPDATED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-113` | `POST` | `/api/v1/admin/chapters/{chapter_id}/lessons` | `LESSON_CREATED` | 201 | `DD_DERIVED` |
| `S2W-STUDY-API-114` | `PATCH` | `/api/v1/admin/lessons/{lesson_id}` | `LESSON_UPDATED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-115` | `DELETE` | `/api/v1/admin/lessons/{lesson_id}` | `LESSON_DELETED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-116` | `PUT` | `/api/v1/admin/lessons/{lesson_id}/preview` | `LESSON_PREVIEW_UPDATED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-117` | `POST` | `/api/v1/admin/lessons/{lesson_id}/lifecycle` | `LESSON_LIFECYCLE_UPDATED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-118` | `POST` | `/api/v1/admin/resources` | `RESOURCE_CREATED` | 201 | `DD_DERIVED` |
| `S2W-STUDY-API-119` | `PATCH` | `/api/v1/admin/resources/{resource_id}` | `RESOURCE_UPDATED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-120` | `DELETE` | `/api/v1/admin/resources/{resource_id}` | `RESOURCE_DELETED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-121` | `GET` | `/api/v1/admin/exercises` | `ADMIN_EXERCISES_LISTED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-122` | `POST` | `/api/v1/admin/exercises` | `EXERCISE_CREATED` | 201 | `DD_DERIVED` |
| `S2W-STUDY-API-123` | `GET` | `/api/v1/admin/exercises/{assignment_id}` | `ADMIN_EXERCISE_DETAIL_LOADED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-124` | `PATCH` | `/api/v1/admin/exercises/{assignment_id}` | `EXERCISE_UPDATED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-125` | `DELETE` | `/api/v1/admin/exercises/{assignment_id}` | `EXERCISE_DELETED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-126` | `POST` | `/api/v1/admin/content/{content_type}/{content_id}/pre-publish-check` | `CONTENT_PRE_PUBLISH_CHECK_COMPLETED` | 200 | `BD_CONFIRMED` |
| `S2W-STUDY-API-127` | `POST` | `/api/v1/admin/content/{content_type}/{content_id}/publish` | `CONTENT_PUBLISHED` | 200 | `BD_CONFIRMED` |
### 11. Admin quản lý học viên và hỗ trợ ngoại lệ

| API ID | Method | Endpoint | Business code | HTTP | Căn cứ |
|---|---:|---|---|---:|---|
| `S2W-STUDY-API-128` | `GET` | `/api/v1/admin/learners` | `ADMIN_LEARNERS_LISTED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-129` | `GET` | `/api/v1/admin/learners/{learner_id}/support-profile` | `LEARNER_SUPPORT_PROFILE_LOADED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-130` | `GET` | `/api/v1/admin/learners/{learner_id}/progress` | `LEARNER_PROGRESS_LOADED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-131` | `GET` | `/api/v1/admin/support-requests` | `ADMIN_SUPPORT_REQUESTS_LISTED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-132` | `GET` | `/api/v1/admin/support-requests/{request_id}` | `ADMIN_SUPPORT_REQUEST_DETAIL_LOADED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-133` | `POST` | `/api/v1/admin/support-requests/{request_id}/resolve` | `SUPPORT_REQUEST_RESOLVED` | 200 | `BD_CONFIRMED` |
| `S2W-STUDY-API-134` | `POST` | `/api/v1/admin/learners/{learner_id}/progress-reset` | `LEARNER_PROGRESS_RESET` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-135` | `POST` | `/api/v1/admin/learners/{learner_id}/active-path/cancel` | `LEARNER_ACTIVE_PATH_CANCELLED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-136` | `POST` | `/api/v1/admin/learners/{learner_id}/active-path/transfer` | `LEARNER_ACTIVE_PATH_TRANSFERRED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-137` | `POST` | `/api/v1/admin/learners/{learner_id}/suspend` | `LEARNER_SUSPENDED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-138` | `POST` | `/api/v1/admin/learners/{learner_id}/unsuspend` | `LEARNER_UNSUSPENDED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-139` | `GET` | `/api/v1/admin/learners/{learner_id}/support-notes` | `LEARNER_SUPPORT_NOTES_LISTED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-140` | `POST` | `/api/v1/admin/learners/{learner_id}/support-notes` | `LEARNER_SUPPORT_NOTE_CREATED` | 201 | `DD_DERIVED` |
| `S2W-STUDY-API-141` | `GET` | `/api/v1/admin/learners/{learner_id}/audit` | `LEARNER_AUDIT_LOGS_LISTED` | 200 | `DD_DERIVED` |
### 12. Báo cáo vận hành

| API ID | Method | Endpoint | Business code | HTTP | Căn cứ |
|---|---:|---|---|---:|---|
| `S2W-STUDY-API-142` | `GET` | `/api/v1/admin/reports/overview` | `ADMIN_REPORT_OVERVIEW_LOADED` | 200 | `BD_CONFIRMED` |
| `S2W-STUDY-API-143` | `GET` | `/api/v1/admin/reports/registrations` | `REGISTRATION_REPORT_LOADED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-144` | `GET` | `/api/v1/admin/reports/onboarding` | `ONBOARDING_REPORT_LOADED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-145` | `GET` | `/api/v1/admin/reports/learning-paths` | `LEARNING_PATH_REPORT_LOADED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-146` | `GET` | `/api/v1/admin/reports/courses` | `COURSE_REPORT_LOADED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-147` | `GET` | `/api/v1/admin/reports/assignments` | `ASSIGNMENT_REPORT_LOADED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-148` | `GET` | `/api/v1/admin/reports/community` | `COMMUNITY_REPORT_LOADED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-149` | `GET` | `/api/v1/admin/reports/alerts` | `ADMIN_OPERATION_ALERTS_LOADED` | 200 | `BD_CONFIRMED` |
### 13. Vai trò, phân quyền và audit

| API ID | Method | Endpoint | Business code | HTTP | Căn cứ |
|---|---:|---|---|---:|---|
| `S2W-STUDY-API-150` | `GET` | `/api/v1/admin/rbac/roles` | `RBAC_ROLES_LISTED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-151` | `GET` | `/api/v1/admin/rbac/permissions` | `RBAC_PERMISSIONS_LISTED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-152` | `GET` | `/api/v1/admin/rbac/matrix` | `RBAC_MATRIX_LOADED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-153` | `GET` | `/api/v1/admin/users/{user_id}/roles` | `USER_ROLES_LISTED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-154` | `POST` | `/api/v1/admin/users/{user_id}/roles` | `USER_ROLE_ASSIGNED` | 201 | `DD_DERIVED` |
| `S2W-STUDY-API-155` | `DELETE` | `/api/v1/admin/users/{user_id}/roles/{role_code}` | `USER_ROLE_REVOKED` | 200 | `DD_DERIVED` |
| `S2W-STUDY-API-156` | `GET` | `/api/v1/admin/audit-logs` | `AUDIT_LOGS_LISTED` | 200 | `BD_CONFIRMED` |
| `S2W-STUDY-API-157` | `GET` | `/api/v1/admin/audit-logs/{audit_id}` | `AUDIT_LOG_DETAIL_LOADED` | 200 | `DD_DERIVED` |

### Mã nghiệp vụ Study chưa có API DD độc lập

| Business code | HTTP | Message | Căn cứ |
|---|---:|---|---|
| `PROGRESS_RECALCULATED` | 200 | Tính lại tiến độ thành công. | `BD_CONFIRMED` |

## 7. Study — mã lỗi nghiệp vụ

### Account/Auth/Profile

| Business code | HTTP | Message | Căn cứ |
|---|---:|---|---|
| `ACCOUNT_CONTACT_ALREADY_USED` | 409 | Thông tin liên hệ đã được sử dụng. | `DD_DERIVED` |
| `ACCOUNT_EMAIL_ALREADY_EXISTS` | 409 | Email đã được sử dụng. | `BD_DERIVED` |
| `ACCOUNT_INVALID_CREDENTIALS` | 401 | Thông tin đăng nhập không chính xác. | `BD_DERIVED` |
| `ACCOUNT_NOT_VERIFIED` | 403 | Tài khoản chưa được xác minh. | `BD_DERIVED` |
| `ACCOUNT_PASSWORD_RESET_TOKEN_EXPIRED` | 400 | Mã đặt lại mật khẩu đã hết hạn. | `DD_DERIVED` |
| `ACCOUNT_PASSWORD_RESET_TOKEN_INVALID` | 400 | Mã đặt lại mật khẩu không hợp lệ. | `DD_DERIVED` |
| `ACCOUNT_PROFILE_INCOMPLETE` | 409 | Hồ sơ tài khoản chưa đầy đủ. | `BD_DERIVED` |
| `ACCOUNT_SUSPENDED` | 403 | Tài khoản đang bị tạm khóa. | `BD_DERIVED` |
| `ACCOUNT_VERIFICATION_TOKEN_EXPIRED` | 400 | Mã xác minh đã hết hạn. | `DD_DERIVED` |
| `ACCOUNT_VERIFICATION_TOKEN_INVALID` | 400 | Mã xác minh không hợp lệ. | `DD_DERIVED` |
### Admin Content

| Business code | HTTP | Message | Căn cứ |
|---|---:|---|---|
| `CONTENT_ALREADY_PUBLISHED` | 409 | Nội dung đã được xuất bản. | `BD_DERIVED` |
| `CONTENT_HAS_DEPENDENCIES` | 409 | Nội dung đang có dữ liệu phụ thuộc. | `BD_DERIVED` |
| `CONTENT_LIFECYCLE_TRANSITION_INVALID` | 409 | Chuyển trạng thái vòng đời nội dung không hợp lệ. | `BD_DERIVED` |
| `CONTENT_NOT_FOUND` | 404 | Không tìm thấy nội dung quản trị. | `DD_DERIVED` |
| `CONTENT_ORDER_INVALID` | 422 | Thứ tự nội dung không hợp lệ. | `BD_DERIVED` |
| `CONTENT_PRE_PUBLISH_CHECK_FAILED` | 409 | Nội dung chưa đạt kiểm tra trước xuất bản. | `BD_DERIVED` |
### Course Content

| Business code | HTTP | Message | Căn cứ |
|---|---:|---|---|
| `CHAPTER_LOCKED` | 409 | Chương học chưa được mở khóa. | `BD_DERIVED` |
| `CHAPTER_NOT_FOUND` | 404 | Không tìm thấy chương học. | `DD_DERIVED` |
| `COURSE_ACCESS_DENIED` | 403 | Học viên không có quyền truy cập khóa học. | `BD_DERIVED` |
| `COURSE_NOT_AVAILABLE` | 409 | Khóa học chưa khả dụng. | `BD_DERIVED` |
| `COURSE_NOT_FOUND` | 404 | Không tìm thấy khóa học. | `DD_DERIVED` |
| `LESSON_LOCKED` | 409 | Bài học chưa được mở khóa. | `BD_DERIVED` |
| `LESSON_NOT_FOUND` | 404 | Không tìm thấy bài học. | `DD_DERIVED` |
| `RESOURCE_ACCESS_DENIED` | 403 | Không có quyền truy cập tài nguyên học tập. | `BD_DERIVED` |
| `RESOURCE_NOT_AVAILABLE` | 404 | Tài nguyên học tập không khả dụng. | `DD_DERIVED` |
### Exercise & Assessment

| Business code | HTTP | Message | Căn cứ |
|---|---:|---|---|
| `EXERCISE_DEADLINE_PASSED` | 409 | Đã quá hạn nộp bài. | `BD_DERIVED` |
| `EXERCISE_NOT_FOUND` | 404 | Không tìm thấy bài tập. | `DD_DERIVED` |
| `EXERCISE_NOT_OPEN` | 409 | Bài tập chưa mở để nộp. | `BD_DERIVED` |
| `EXERCISE_REOPEN_NOT_ALLOWED` | 409 | Không thể mở lại bài nộp. | `BD_DERIVED` |
| `EXERCISE_RESUBMISSION_NOT_ALLOWED` | 409 | Không được phép nộp lại bài. | `BD_DERIVED` |
| `EXERCISE_REVIEW_NOT_ALLOWED` | 409 | Không thể chấm bài trong trạng thái hiện tại. | `BD_DERIVED` |
| `EXERCISE_SUBMISSION_ALREADY_EXISTS` | 409 | Bài nộp đã tồn tại. | `BD_DERIVED` |
| `EXERCISE_SUBMISSION_NOT_FOUND` | 404 | Không tìm thấy bài nộp. | `DD_DERIVED` |
### Learner Support

| Business code | HTTP | Message | Căn cứ |
|---|---:|---|---|
| `ADMIN_REASON_REQUIRED` | 422 | Thao tác quản trị yêu cầu lý do. | `BD_DERIVED` |
| `LEARNER_NOT_FOUND` | 404 | Không tìm thấy học viên. | `DD_DERIVED` |
| `LEARNER_PROGRESS_RESET_NOT_ALLOWED` | 409 | Không thể đặt lại tiến độ học viên. | `BD_DERIVED` |
| `LEARNER_SUSPENSION_NOT_ALLOWED` | 409 | Không thể thay đổi trạng thái khóa của học viên. | `BD_DERIVED` |
| `SUPPORT_REQUEST_ALREADY_RESOLVED` | 409 | Yêu cầu hỗ trợ đã được xử lý. | `BD_DERIVED` |
| `SUPPORT_REQUEST_NOT_FOUND` | 404 | Không tìm thấy yêu cầu hỗ trợ. | `DD_DERIVED` |
### Learning Path

| Business code | HTTP | Message | Căn cứ |
|---|---:|---|---|
| `LEARNING_PATH_ACTIVATION_NOT_ALLOWED` | 409 | Không đủ điều kiện kích hoạt lộ trình. | `BD_DERIVED` |
| `LEARNING_PATH_ACTIVE_ALREADY_EXISTS` | 409 | Học viên đã có một lộ trình đang hoạt động. | `BD_CONFIRMED` |
| `LEARNING_PATH_ENROLLMENT_NOT_FOUND` | 404 | Không tìm thấy đăng ký lộ trình. | `DD_DERIVED` |
| `LEARNING_PATH_NOT_FOUND` | 404 | Không tìm thấy lộ trình học. | `DD_DERIVED` |
| `LEARNING_PATH_NOT_PUBLISHED` | 409 | Lộ trình học chưa được xuất bản. | `BD_DERIVED` |
| `LEARNING_PATH_TRANSFER_NOT_ALLOWED` | 409 | Không thể chuyển lộ trình trong trạng thái hiện tại. | `BD_DERIVED` |
### Notification

| Business code | HTTP | Message | Căn cứ |
|---|---:|---|---|
| `NOTIFICATION_BATCH_CANNOT_CANCEL` | 409 | Không thể hủy đợt gửi thông báo trong trạng thái hiện tại. | `BD_DERIVED` |
| `NOTIFICATION_BATCH_NOT_FOUND` | 404 | Không tìm thấy đợt gửi thông báo. | `DD_DERIVED` |
| `NOTIFICATION_MANDATORY_SETTING_LOCKED` | 409 | Không thể tắt thông báo bắt buộc. | `BD_DERIVED` |
| `NOTIFICATION_NOT_FOUND` | 404 | Không tìm thấy thông báo. | `DD_DERIVED` |
### Onboarding

| Business code | HTTP | Message | Căn cứ |
|---|---:|---|---|
| `ONBOARDING_ALREADY_COMPLETED` | 409 | Onboarding đã hoàn thành. | `BD_DERIVED` |
| `ONBOARDING_NOT_STARTED` | 409 | Onboarding chưa được bắt đầu. | `BD_DERIVED` |
| `ONBOARDING_PATH_NOT_AVAILABLE` | 409 | Lộ trình đã chọn không còn khả dụng. | `BD_DERIVED` |
| `ONBOARDING_REQUIRED_FIELDS_MISSING` | 422 | Thiếu thông tin onboarding bắt buộc. | `BD_DERIVED` |
| `ONBOARDING_SELECTED_PATH_REQUIRED` | 409 | Cần chọn một lộ trình trước khi hoàn thành onboarding. | `BD_DERIVED` |
### Operational Reports

| Business code | HTTP | Message | Căn cứ |
|---|---:|---|---|
| `REPORT_DATA_UNAVAILABLE` | 503 | Dữ liệu báo cáo tạm thời không khả dụng. | `BD_DERIVED` |
| `REPORT_QUERY_INVALID` | 422 | Điều kiện báo cáo không hợp lệ. | `DD_DERIVED` |
### Progress & Completion

| Business code | HTTP | Message | Căn cứ |
|---|---:|---|---|
| `COMPLETION_REQUIREMENTS_NOT_MET` | 409 | Chưa đáp ứng đủ điều kiện hoàn thành. | `BD_DERIVED` |
| `PROGRESS_NOT_FOUND` | 404 | Không tìm thấy dữ liệu tiến độ. | `DD_DERIVED` |
| `PROGRESS_RECALCULATION_FAILED` | 500 | Không thể tính lại tiến độ. | `BD_DERIVED` |
| `PROGRESS_UPDATE_NOT_ALLOWED` | 409 | Không thể cập nhật tiến độ trong trạng thái hiện tại. | `BD_DERIVED` |
| `REQUIRED_EXERCISE_NOT_PASSED` | 409 | Chưa đạt bài tập bắt buộc. | `BD_DERIVED` |
### Public Catalog

| Business code | HTTP | Message | Căn cứ |
|---|---:|---|---|
| `CATALOG_CONTENT_NOT_PUBLISHED` | 404 | Nội dung chưa được công khai. | `DD_DERIVED` |
| `CATALOG_ITEM_NOT_FOUND` | 404 | Không tìm thấy nội dung trong danh mục. | `DD_DERIVED` |
| `SAMPLE_LESSON_NOT_AVAILABLE` | 404 | Bài học mẫu không khả dụng. | `BD_DERIVED` |
### RBAC & Audit

| Business code | HTTP | Message | Căn cứ |
|---|---:|---|---|
| `AUDIT_LOG_NOT_FOUND` | 404 | Không tìm thấy nhật ký audit. | `DD_DERIVED` |
| `RBAC_LAST_ADMIN_ROLE_CANNOT_REVOKE` | 409 | Không thể thu hồi vai trò quản trị cuối cùng. | `BD_DERIVED` |
| `RBAC_PERMISSION_DENIED` | 403 | Không có quyền thực hiện thao tác. | `BD_CONFIRMED` |
| `RBAC_PERMISSION_NOT_FOUND` | 404 | Không tìm thấy quyền. | `DD_DERIVED` |
| `RBAC_ROLE_ALREADY_ASSIGNED` | 409 | Người dùng đã có vai trò này. | `BD_DERIVED` |
| `RBAC_ROLE_NOT_ASSIGNED` | 409 | Người dùng chưa được gán vai trò này. | `BD_DERIVED` |
| `RBAC_ROLE_NOT_FOUND` | 404 | Không tìm thấy vai trò. | `DD_DERIVED` |
### Zalo Community

| Business code | HTTP | Message | Căn cứ |
|---|---:|---|---|
| `COMMUNITY_GROUP_INACTIVE` | 409 | Nhóm cộng đồng không hoạt động. | `BD_DERIVED` |
| `COMMUNITY_GROUP_NOT_FOUND` | 404 | Không tìm thấy nhóm cộng đồng. | `DD_DERIVED` |
| `COMMUNITY_REPORT_ALREADY_RESOLVED` | 409 | Báo cáo cộng đồng đã được xử lý. | `BD_DERIVED` |
| `COMMUNITY_REPORT_NOT_FOUND` | 404 | Không tìm thấy báo cáo cộng đồng. | `DD_DERIVED` |
| `COMMUNITY_RULES_NOT_ACCEPTED` | 409 | Cần chấp nhận nội quy trước khi mở liên kết. | `BD_DERIVED` |

## 8. Work — mã theo kiến trúc đích

> Toàn bộ phần này là `TARGET_PROPOSED`. Không áp dụng trực tiếp cho route HTML/EJS của Work prototype.

### Application

| Business code | Loại | HTTP | Message |
|---|---:|---:|---|
| `APPLICATIONS_LISTED` | SUCCESS | 200 | Đã tải danh sách ứng tuyển. |
| `APPLICATION_CREATED` | SUCCESS | 201 | Ứng tuyển thành công. |
| `APPLICATION_DETAIL_LOADED` | SUCCESS | 200 | Đã tải chi tiết ứng tuyển. |
| `APPLICATION_HIRED` | SUCCESS | 200 | Xác nhận tuyển dụng thành công. |
| `APPLICATION_HISTORY_LOADED` | SUCCESS | 200 | Đã tải lịch sử trạng thái ứng tuyển. |
| `APPLICATION_NOTE_CREATED` | SUCCESS | 201 | Tạo ghi chú ứng tuyển thành công. |
| `APPLICATION_REJECTED` | SUCCESS | 200 | Từ chối ứng viên thành công. |
| `APPLICATION_SHORTLISTED` | SUCCESS | 200 | Đưa ứng viên vào danh sách rút gọn thành công. |
| `APPLICATION_SNAPSHOT_LOADED` | SUCCESS | 200 | Đã tải snapshot CV và việc làm của ứng tuyển. |
| `APPLICATION_STATUS_UPDATED` | SUCCESS | 200 | Cập nhật trạng thái ứng tuyển thành công. |
| `APPLICATION_WITHDRAWN` | SUCCESS | 200 | Rút ứng tuyển thành công. |
| `APPLICATION_ALREADY_EXISTS` | ERROR | 409 | Ứng viên đã ứng tuyển việc làm này. |
| `APPLICATION_CV_REQUIRED` | ERROR | 422 | Cần chọn CV để ứng tuyển. |
| `APPLICATION_NOT_ALLOWED` | ERROR | 409 | Không thể ứng tuyển trong trạng thái hiện tại. |
| `APPLICATION_NOT_FOUND` | ERROR | 404 | Không tìm thấy ứng tuyển. |
| `APPLICATION_SNAPSHOT_MISSING` | ERROR | 500 | Thiếu snapshot bất biến của ứng tuyển. |
| `APPLICATION_STATUS_TRANSITION_INVALID` | ERROR | 409 | Chuyển trạng thái ứng tuyển không hợp lệ. |
| `APPLICATION_WITHDRAWAL_NOT_ALLOWED` | ERROR | 409 | Không thể rút ứng tuyển trong trạng thái hiện tại. |
### CV

| Business code | Loại | HTTP | Message |
|---|---:|---:|---|
| `CVS_LISTED` | SUCCESS | 200 | Đã tải danh sách CV. |
| `CV_CREATED` | SUCCESS | 201 | Tạo CV thành công. |
| `CV_DELETED` | SUCCESS | 200 | Xóa CV thành công. |
| `CV_DETAIL_LOADED` | SUCCESS | 200 | Đã tải chi tiết CV. |
| `CV_EXPORTED` | SUCCESS | 200 | Xuất CV thành công. |
| `CV_SNAPSHOT_CREATED` | SUCCESS | 201 | Tạo snapshot CV thành công. |
| `CV_TEMPLATE_APPLIED` | SUCCESS | 200 | Áp dụng mẫu CV thành công. |
| `CV_UPDATED` | SUCCESS | 200 | Cập nhật CV thành công. |
| `CV_VERSION_ACTIVATED` | SUCCESS | 200 | Kích hoạt phiên bản CV thành công. |
| `CV_VERSION_CREATED` | SUCCESS | 201 | Tạo phiên bản CV thành công. |
| `CV_EXPORT_FAILED` | ERROR | 500 | Xuất CV không thành công. |
| `CV_INCOMPLETE` | ERROR | 409 | CV chưa đủ thông tin bắt buộc. |
| `CV_NOT_FOUND` | ERROR | 404 | Không tìm thấy CV. |
| `CV_SNAPSHOT_IMMUTABLE` | ERROR | 409 | Không thể sửa snapshot CV bất biến. |
| `CV_VERSION_NOT_FOUND` | ERROR | 404 | Không tìm thấy phiên bản CV. |
### Enterprise

| Business code | Loại | HTTP | Message |
|---|---:|---:|---|
| `ENTERPRISES_LISTED` | SUCCESS | 200 | Đã tải danh sách doanh nghiệp. |
| `ENTERPRISE_CREATED` | SUCCESS | 201 | Tạo doanh nghiệp thành công. |
| `ENTERPRISE_DETAIL_LOADED` | SUCCESS | 200 | Đã tải chi tiết doanh nghiệp. |
| `ENTERPRISE_MEMBERS_LISTED` | SUCCESS | 200 | Đã tải danh sách thành viên doanh nghiệp. |
| `ENTERPRISE_MEMBER_INVITED` | SUCCESS | 201 | Mời thành viên doanh nghiệp thành công. |
| `ENTERPRISE_MEMBER_JOINED` | SUCCESS | 200 | Tham gia doanh nghiệp thành công. |
| `ENTERPRISE_MEMBER_REMOVED` | SUCCESS | 200 | Xóa thành viên khỏi doanh nghiệp thành công. |
| `ENTERPRISE_MEMBER_ROLE_UPDATED` | SUCCESS | 200 | Cập nhật vai trò thành viên doanh nghiệp thành công. |
| `ENTERPRISE_PROFILE_UPDATED` | SUCCESS | 200 | Cập nhật hồ sơ doanh nghiệp thành công. |
| `ENTERPRISE_VERIFICATION_APPROVED` | SUCCESS | 200 | Phê duyệt xác minh doanh nghiệp thành công. |
| `ENTERPRISE_VERIFICATION_REJECTED` | SUCCESS | 200 | Từ chối xác minh doanh nghiệp thành công. |
| `ENTERPRISE_VERIFICATION_SUBMITTED` | SUCCESS | 201 | Gửi hồ sơ xác minh doanh nghiệp thành công. |
| `ENTERPRISE_ALREADY_EXISTS` | ERROR | 409 | Doanh nghiệp đã tồn tại. |
| `ENTERPRISE_INVITATION_EXPIRED` | ERROR | 400 | Lời mời tham gia doanh nghiệp đã hết hạn. |
| `ENTERPRISE_INVITATION_INVALID` | ERROR | 400 | Lời mời tham gia doanh nghiệp không hợp lệ. |
| `ENTERPRISE_MEMBER_ALREADY_EXISTS` | ERROR | 409 | Người dùng đã là thành viên doanh nghiệp. |
| `ENTERPRISE_MEMBER_NOT_FOUND` | ERROR | 404 | Không tìm thấy thành viên doanh nghiệp. |
| `ENTERPRISE_NOT_FOUND` | ERROR | 404 | Không tìm thấy doanh nghiệp. |
| `ENTERPRISE_NOT_VERIFIED` | ERROR | 403 | Doanh nghiệp chưa được xác minh. |
| `ENTERPRISE_VERIFICATION_ALREADY_PENDING` | ERROR | 409 | Hồ sơ xác minh doanh nghiệp đang chờ xử lý. |
### IAM

| Business code | Loại | HTTP | Message |
|---|---:|---:|---|
| `WORK_AUTH_CONTEXT_LOADED` | SUCCESS | 200 | Đã tải ngữ cảnh xác thực Work. |
| `WORK_ROLES_LISTED` | SUCCESS | 200 | Đã tải danh sách vai trò Work. |
| `WORK_ROLE_ASSIGNED` | SUCCESS | 200 | Gán vai trò Work thành công. |
| `WORK_ROLE_REVOKED` | SUCCESS | 200 | Thu hồi vai trò Work thành công. |
| `WORK_USER_PROJECTION_CREATED` | SUCCESS | 201 | Tạo user projection trong Work thành công. |
| `WORK_USER_PROJECTION_LOADED` | SUCCESS | 200 | Đã tải user projection trong Work. |
| `WORK_USER_PROJECTION_UPDATED` | SUCCESS | 200 | Cập nhật user projection trong Work thành công. |
| `TENANT_ACCESS_DENIED` | ERROR | 403 | Không có quyền truy cập tenant doanh nghiệp. |
| `TENANT_CONTEXT_REQUIRED` | ERROR | 400 | Yêu cầu ngữ cảnh doanh nghiệp. |
| `WORK_PERMISSION_DENIED` | ERROR | 403 | Không có quyền thực hiện thao tác trong Work. |
| `WORK_ROLE_ALREADY_ASSIGNED` | ERROR | 409 | Người dùng đã có vai trò Work này. |
| `WORK_ROLE_NOT_FOUND` | ERROR | 404 | Không tìm thấy vai trò Work. |
| `WORK_USER_PROJECTION_NOT_FOUND` | ERROR | 404 | Không tìm thấy user projection trong Work. |
### Interview

| Business code | Loại | HTTP | Message |
|---|---:|---:|---|
| `INTERVIEWS_LISTED` | SUCCESS | 200 | Đã tải danh sách lịch phỏng vấn. |
| `INTERVIEW_CANCELLED` | SUCCESS | 200 | Hủy lịch phỏng vấn thành công. |
| `INTERVIEW_CONFIRMED` | SUCCESS | 200 | Xác nhận tham gia phỏng vấn thành công. |
| `INTERVIEW_CREATED` | SUCCESS | 201 | Tạo lịch phỏng vấn thành công. |
| `INTERVIEW_DETAIL_LOADED` | SUCCESS | 200 | Đã tải chi tiết lịch phỏng vấn. |
| `INTERVIEW_OUTCOME_RECORDED` | SUCCESS | 200 | Ghi nhận kết quả phỏng vấn thành công. |
| `INTERVIEW_RESCHEDULED` | SUCCESS | 200 | Đổi lịch phỏng vấn thành công. |
| `INTERVIEW_UPDATED` | SUCCESS | 200 | Cập nhật lịch phỏng vấn thành công. |
| `INTERVIEW_NOT_FOUND` | ERROR | 404 | Không tìm thấy lịch phỏng vấn. |
| `INTERVIEW_OUTCOME_ALREADY_RECORDED` | ERROR | 409 | Kết quả phỏng vấn đã được ghi nhận. |
| `INTERVIEW_RESCHEDULE_NOT_ALLOWED` | ERROR | 409 | Không thể đổi lịch phỏng vấn trong trạng thái hiện tại. |
| `INTERVIEW_TIME_CONFLICT` | ERROR | 409 | Thời gian phỏng vấn bị trùng lịch. |
### Job

| Business code | Loại | HTTP | Message |
|---|---:|---:|---|
| `ENTERPRISE_JOBS_LISTED` | SUCCESS | 200 | Đã tải danh sách việc làm của doanh nghiệp. |
| `JOBS_LISTED` | SUCCESS | 200 | Đã tải danh sách việc làm. |
| `JOB_APPLICANTS_SUMMARY_LOADED` | SUCCESS | 200 | Đã tải tổng quan ứng viên của việc làm. |
| `JOB_ARCHIVED` | SUCCESS | 200 | Lưu trữ việc làm thành công. |
| `JOB_CLOSED` | SUCCESS | 200 | Đóng việc làm thành công. |
| `JOB_CREATED` | SUCCESS | 201 | Tạo việc làm thành công. |
| `JOB_DELETED` | SUCCESS | 200 | Xóa việc làm thành công. |
| `JOB_DETAIL_LOADED` | SUCCESS | 200 | Đã tải chi tiết việc làm. |
| `JOB_PAUSED` | SUCCESS | 200 | Tạm dừng việc làm thành công. |
| `JOB_PUBLISHED` | SUCCESS | 200 | Đăng việc làm thành công. |
| `JOB_PUBLISH_CHECK_COMPLETED` | SUCCESS | 200 | Kiểm tra trước đăng việc hoàn tất. |
| `JOB_UPDATED` | SUCCESS | 200 | Cập nhật việc làm thành công. |
| `JOB_ALREADY_CLOSED` | ERROR | 409 | Việc làm đã đóng. |
| `JOB_DEADLINE_PASSED` | ERROR | 409 | Đã quá hạn ứng tuyển. |
| `JOB_LIFECYCLE_TRANSITION_INVALID` | ERROR | 409 | Chuyển trạng thái việc làm không hợp lệ. |
| `JOB_NOT_FOUND` | ERROR | 404 | Không tìm thấy việc làm. |
| `JOB_NOT_PUBLISHED` | ERROR | 404 | Việc làm chưa được công khai. |
| `JOB_PUBLISH_CHECK_FAILED` | ERROR | 409 | Việc làm chưa đạt kiểm tra trước đăng. |
### Matching

| Business code | Loại | HTTP | Message |
|---|---:|---:|---|
| `MATCHING_FEEDBACK_RECORDED` | SUCCESS | 201 | Ghi nhận phản hồi gợi ý thành công. |
| `MATCHING_RECOMMENDATIONS_LOADED` | SUCCESS | 200 | Đã tải danh sách gợi ý phù hợp. |
| `MATCHING_SCORE_EXPLAINED` | SUCCESS | 200 | Đã tải giải thích điểm phù hợp. |
| `MATCHING_DATA_INSUFFICIENT` | ERROR | 409 | Chưa đủ dữ liệu để tính mức độ phù hợp. |
| `MATCHING_SCORE_UNAVAILABLE` | ERROR | 503 | Điểm phù hợp tạm thời không khả dụng. |
### Moderation

| Business code | Loại | HTTP | Message |
|---|---:|---:|---|
| `MODERATION_CASE_APPROVED` | SUCCESS | 200 | Phê duyệt hồ sơ kiểm duyệt thành công. |
| `MODERATION_CASE_DETAIL_LOADED` | SUCCESS | 200 | Đã tải chi tiết hồ sơ kiểm duyệt. |
| `MODERATION_CASE_ESCALATED` | SUCCESS | 200 | Chuyển cấp hồ sơ kiểm duyệt thành công. |
| `MODERATION_CASE_REJECTED` | SUCCESS | 200 | Từ chối hồ sơ kiểm duyệt thành công. |
| `MODERATION_QUEUE_LISTED` | SUCCESS | 200 | Đã tải hàng đợi kiểm duyệt. |
| `MODERATION_REPORT_CREATED` | SUCCESS | 201 | Tạo báo cáo kiểm duyệt thành công. |
| `MODERATION_REPORT_RESOLVED` | SUCCESS | 200 | Xử lý báo cáo kiểm duyệt thành công. |
| `MODERATION_CASE_ALREADY_RESOLVED` | ERROR | 409 | Hồ sơ kiểm duyệt đã được xử lý. |
| `MODERATION_CASE_NOT_FOUND` | ERROR | 404 | Không tìm thấy hồ sơ kiểm duyệt. |
| `MODERATION_REASON_REQUIRED` | ERROR | 422 | Thao tác kiểm duyệt yêu cầu lý do. |
### Notification

| Business code | Loại | HTTP | Message |
|---|---:|---:|---|
| `WORK_NOTIFICATIONS_LISTED` | SUCCESS | 200 | Đã tải danh sách thông báo Work. |
| `WORK_NOTIFICATIONS_MARKED_READ` | SUCCESS | 200 | Đánh dấu tất cả thông báo Work đã đọc thành công. |
| `WORK_NOTIFICATION_MARKED_READ` | SUCCESS | 200 | Đánh dấu thông báo Work đã đọc thành công. |
| `WORK_NOTIFICATION_SETTINGS_LOADED` | SUCCESS | 200 | Đã tải cài đặt thông báo Work. |
| `WORK_NOTIFICATION_SETTINGS_UPDATED` | SUCCESS | 200 | Cập nhật cài đặt thông báo Work thành công. |
| `WORK_NOTIFICATION_UNREAD_COUNT_LOADED` | SUCCESS | 200 | Đã tải số thông báo Work chưa đọc. |
| `WORK_NOTIFICATION_MANDATORY_SETTING_LOCKED` | ERROR | 409 | Không thể tắt thông báo Work bắt buộc. |
| `WORK_NOTIFICATION_NOT_FOUND` | ERROR | 404 | Không tìm thấy thông báo Work. |
### Portfolio

| Business code | Loại | HTTP | Message |
|---|---:|---:|---|
| `PORTFOLIO_ASSET_ATTACHED` | SUCCESS | 201 | Gắn tài nguyên vào portfolio thành công. |
| `PORTFOLIO_ASSET_REMOVED` | SUCCESS | 200 | Gỡ tài nguyên khỏi portfolio thành công. |
| `PORTFOLIO_PROJECTS_LISTED` | SUCCESS | 200 | Đã tải danh sách dự án portfolio. |
| `PORTFOLIO_PROJECT_CREATED` | SUCCESS | 201 | Tạo dự án portfolio thành công. |
| `PORTFOLIO_PROJECT_DELETED` | SUCCESS | 200 | Xóa dự án portfolio thành công. |
| `PORTFOLIO_PROJECT_DETAIL_LOADED` | SUCCESS | 200 | Đã tải chi tiết dự án portfolio. |
| `PORTFOLIO_PROJECT_HIDDEN` | SUCCESS | 200 | Ẩn dự án portfolio thành công. |
| `PORTFOLIO_PROJECT_PUBLISHED` | SUCCESS | 200 | Công khai dự án portfolio thành công. |
| `PORTFOLIO_PROJECT_UPDATED` | SUCCESS | 200 | Cập nhật dự án portfolio thành công. |
| `PORTFOLIO_ASSET_NOT_FOUND` | ERROR | 404 | Không tìm thấy tài nguyên portfolio. |
| `PORTFOLIO_PROJECT_NOT_FOUND` | ERROR | 404 | Không tìm thấy dự án portfolio. |
| `PORTFOLIO_PROJECT_NOT_PUBLISHED` | ERROR | 404 | Dự án portfolio chưa được công khai. |
### Student Profile

| Business code | Loại | HTTP | Message |
|---|---:|---:|---|
| `CAREER_PREFERENCES_UPDATED` | SUCCESS | 200 | Cập nhật nguyện vọng nghề nghiệp thành công. |
| `CAREER_PROFILE_COMPLETENESS_LOADED` | SUCCESS | 200 | Đã tải mức độ hoàn thiện hồ sơ nghề nghiệp. |
| `CAREER_PROFILE_CREATED` | SUCCESS | 201 | Tạo hồ sơ nghề nghiệp thành công. |
| `CAREER_PROFILE_LOADED` | SUCCESS | 200 | Đã tải hồ sơ nghề nghiệp. |
| `CAREER_PROFILE_UPDATED` | SUCCESS | 200 | Cập nhật hồ sơ nghề nghiệp thành công. |
| `DECLARED_SKILLS_UPDATED` | SUCCESS | 200 | Cập nhật kỹ năng tự khai báo thành công. |
| `CAREER_PROFILE_INCOMPLETE` | ERROR | 409 | Hồ sơ nghề nghiệp chưa đầy đủ. |
| `CAREER_PROFILE_NOT_FOUND` | ERROR | 404 | Không tìm thấy hồ sơ nghề nghiệp. |
### Study Evidence

| Business code | Loại | HTTP | Message |
|---|---:|---:|---|
| `STUDY_EVIDENCE_DETAIL_LOADED` | SUCCESS | 200 | Đã tải chi tiết minh chứng học tập. |
| `STUDY_EVIDENCE_INTEGRITY_VERIFIED` | SUCCESS | 200 | Xác minh tính toàn vẹn minh chứng thành công. |
| `STUDY_EVIDENCE_LISTED` | SUCCESS | 200 | Đã tải danh sách minh chứng học tập. |
| `STUDY_EVIDENCE_SHARED` | SUCCESS | 200 | Chia sẻ minh chứng học tập thành công. |
| `STUDY_EVIDENCE_SHARING_REVOKED` | SUCCESS | 200 | Thu hồi chia sẻ minh chứng thành công. |
| `STUDY_EVIDENCE_VISIBILITY_UPDATED` | SUCCESS | 200 | Cập nhật phạm vi hiển thị minh chứng thành công. |
| `STUDY_EVIDENCE_CONSENT_REQUIRED` | ERROR | 403 | Cần sự đồng ý của người dùng để chia sẻ minh chứng. |
| `STUDY_EVIDENCE_INTEGRITY_FAILED` | ERROR | 409 | Không xác minh được tính toàn vẹn của minh chứng. |
| `STUDY_EVIDENCE_NOT_FOUND` | ERROR | 404 | Không tìm thấy minh chứng học tập. |
| `STUDY_EVIDENCE_PRIVATE` | ERROR | 403 | Minh chứng học tập đang ở chế độ riêng tư. |
| `STUDY_EVIDENCE_REVOKED` | ERROR | 409 | Minh chứng học tập đã bị thu hồi. |

## 9. Integration Study → Work

| Business code | Loại | HTTP | Message |
|---|---:|---:|---|
| `INTEGRATION_EVENT_REPLAYED` | SUCCESS | 200 | Phát lại sự kiện tích hợp thành công. |
| `INTEGRATION_EVENT_STATUS_LOADED` | SUCCESS | 200 | Đã tải trạng thái sự kiện tích hợp. |
| `STUDY_EVIDENCE_EVENT_ACCEPTED` | SUCCESS | 202 | Tiếp nhận sự kiện minh chứng học tập thành công. |
| `STUDY_EVIDENCE_SNAPSHOT_REVOKED` | SUCCESS | 200 | Thu hồi snapshot minh chứng thành công. |
| `STUDY_EVIDENCE_SNAPSHOT_UPSERTED` | SUCCESS | 200 | Đồng bộ snapshot minh chứng thành công. |
| `INTEGRATION_EVENT_DUPLICATE` | ERROR | 409 | Sự kiện tích hợp đã được xử lý. |
| `INTEGRATION_EVENT_EXPIRED` | ERROR | 400 | Sự kiện tích hợp nằm ngoài thời gian cho phép. |
| `INTEGRATION_EVENT_SCHEMA_INVALID` | ERROR | 422 | Payload sự kiện không đúng schema. |
| `INTEGRATION_EVENT_TYPE_UNSUPPORTED` | ERROR | 422 | Loại sự kiện tích hợp không được hỗ trợ. |
| `INTEGRATION_EVIDENCE_VERSION_CONFLICT` | ERROR | 409 | Phiên bản minh chứng bị xung đột. |
| `INTEGRATION_PLATFORM_USER_NOT_FOUND` | ERROR | 404 | Không tìm thấy platformUserId trong Work. |
| `INTEGRATION_PROCESSING_FAILED` | ERROR | 500 | Xử lý sự kiện tích hợp không thành công. |
| `INTEGRATION_SIGNATURE_INVALID` | ERROR | 401 | Chữ ký sự kiện tích hợp không hợp lệ. |

## 10. `errors[].code` dùng cho validation

| Error detail code | Ý nghĩa |
|---|---|
| `FIELD_REQUIRED` | Trường dữ liệu là bắt buộc. |
| `FIELD_INVALID` | Giá trị trường dữ liệu không hợp lệ. |
| `FIELD_TOO_SHORT` | Giá trị trường dữ liệu quá ngắn. |
| `FIELD_TOO_LONG` | Giá trị trường dữ liệu quá dài. |
| `FIELD_OUT_OF_RANGE` | Giá trị nằm ngoài phạm vi cho phép. |
| `FIELD_FORMAT_INVALID` | Định dạng trường dữ liệu không hợp lệ. |
| `FIELD_NOT_UNIQUE` | Giá trị trường dữ liệu đã tồn tại. |
| `FILE_REQUIRED` | Tệp đính kèm là bắt buộc. |
| `FILE_SIZE_EXCEEDED` | Kích thước tệp vượt giới hạn. |
| `FILE_MIME_INVALID` | MIME type của tệp không hợp lệ. |
| `DATE_RANGE_INVALID` | Khoảng thời gian không hợp lệ. |
| `ENUM_VALUE_INVALID` | Giá trị enum không được hỗ trợ. |
| `REFERENCE_NOT_FOUND` | Không tìm thấy dữ liệu tham chiếu. |

## 11. Quy tắc triển khai

1. Mỗi response có đúng một `businessCode`.
2. Một endpoint có thể trả nhiều mã lỗi nhưng chỉ có một mã thành công chính.
3. Frontend dùng `businessCode`; `message` chỉ để hiển thị.
4. `404` có thể được dùng thay `403` khi cần che sự tồn tại của resource.
5. `204 No Content` không có response body, vì vậy không có `businessCode`.
6. Không đưa SQL, stack trace, token hoặc PII vào `message` hay `errors`.
7. Mọi mã mới phải cập nhật đồng thời Markdown, JSON, Python/TypeScript và contract test.

## 12. Ví dụ sử dụng

```json
{
  "success": true,
  "businessCode": "COURSE_DETAIL_RETRIEVED",
  "message": "Đã tải chi tiết khóa học.",
  "data": {},
  "meta": {},
  "traceId": "7d61fc96-5cac-4e4d-9154-7b6a5f844878"
}
```

## 13. File máy đọc

- `business-codes.json`: catalog đầy đủ có metadata.
- `business_codes.py`: enum cho FastAPI/Python.
- `business-codes.ts`: constant và union type cho TypeScript.
