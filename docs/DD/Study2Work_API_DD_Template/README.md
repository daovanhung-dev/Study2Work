# Study2Work API Detail Design (DD) Template

> **Mục tiêu:** bộ template Markdown cho **một API** của Study2Work. Mỗi API được mô tả đủ rõ để Backend phát triển, Frontend/Mobile tích hợp, QA viết test case, DevOps theo dõi vận hành và AI coding có thể sinh mã nguồn có kiểm soát.

## 1. Phạm vi và cấu trúc

```text
Study2Work_API_DD_Template/
├── README.md
├── HUONG_DAN_NHAP_LIEU_DD.md
├── API_DD_CHECKLIST.md
├── 01_Overview/
│   └── Overview.md
├── 02_History/
│   └── History.md
├── 03_Request/
│   └── Request.md
├── 04_Response/
│   └── Response.md
├── 05_DataMapping/
│   └── DataMapping.md
└── 06_Error/
    └── Error.md
```

> Quy ước: yêu cầu ban đầu có hai mục `Response`; mục mô tả **đầu vào** được chuẩn hóa thành thư mục `03_Request`, còn `04_Response` dùng cho **đầu ra**.

## 2. Cách sử dụng cho một API mới

1. Copy toàn bộ thư mục template vào `docs/api-dd/{{module-code}}/{{api-code}}/`.
2. Đọc `HUONG_DAN_NHAP_LIEU_DD.md` trước khi bắt đầu nhập liệu.
3. Đổi tên các placeholder `{{UPPER_SNAKE_CASE}}` thành dữ liệu thật; không để lại placeholder trong tài liệu đã review.
4. Điền `Overview` trước để chốt API contract, phạm vi nghiệp vụ, role và dependency.
5. Điền `Request` và `Response` như một **hợp đồng không mơ hồ** giữa client và server.
6. Điền `DataMapping` theo đúng thứ tự runtime: nguồn dữ liệu → validate → permission → xử lý nghiệp vụ → DB/cache/external service → transaction → event → response.
7. Điền `Error` trước khi code để FE/BE/QA thống nhất tình huống lỗi và hành vi retry.
8. Cập nhật `History` cho mọi thay đổi, đặc biệt là thay đổi breaking contract hoặc thay đổi rule nghiệp vụ.
9. Chạy checklist ở `API_DD_CHECKLIST.md` trước khi trạng thái tài liệu chuyển sang `Approved`.

## 3. Quy ước định danh Study2Work

### 3.1. Module code

| Module code | Phạm vi đề xuất | Ví dụ API code |
|---|---|---|
| `AUTH` | Authentication, token, session | `AUTH-LOGIN-001` |
| `USER` | User, profile, skill cá nhân | `USER-PROFILE-001` |
| `LEARN` | Roadmap, lesson, quiz, assignment | `LEARN-QUIZ-001` |
| `PROJECT` | Team project, task, sprint, Git | `PROJECT-TEAM-001` |
| `MENTOR` | Review, rubric, mentoring | `MENTOR-REVIEW-001` |
| `PORTFOLIO` | Portfolio, CV, public profile | `PORTFOLIO-CV-001` |
| `EMPLOYER` | Job post, candidate, matching, application | `EMPLOYER-MATCH-001` |
| `AI` | AI tutor, roadmap, CV/interview review | `AI-{{FEATURE}}-001` |
| `NOTI` | Notification, email, queue | `NOTI-{{ACTION}}-001` |
| `SYSTEM` | Audit log, settings, platform operation | `SYSTEM-{{ACTION}}-001` |

### 3.2. Tên thư mục và file

```text
docs/api-dd/{{module-code-lowercase}}/{{api-code-lowercase}}/
```

Ví dụ:

```text
docs/api-dd/auth/auth-login-001/
```

Tên file cố định để tooling/AI có thể tìm thấy:

```text
01_Overview/Overview.md
02_History/History.md
03_Request/Request.md
04_Response/Response.md
05_DataMapping/DataMapping.md
06_Error/Error.md
```

## 4. Chuẩn dữ liệu và API contract

| Nội dung | Chuẩn bắt buộc | Ghi chú |
|---|---|---|
| API version | `/api/v1/...` | Version nằm trong URL cho public/client-facing API. |
| Identifier | `UUID` dạng string | Không làm lộ sequence ID nội bộ nếu không có lý do nghiệp vụ. |
| Timestamp | ISO-8601 UTC | Ví dụ: `2026-07-01T11:45:00Z`. |
| JSON property | `camelCase` | Ví dụ `learningPathId`, `createdAt`. |
| Database column | `snake_case` | Ví dụ `learning_path_id`, `created_at`. |
| Enum | `UPPER_SNAKE_CASE` | Ví dụ `IN_PROGRESS`, `SUBMITTED`. |
| Soft delete | `deleted_at` | Không trả dữ liệu đã xóa trừ API admin/audit được đặc tả. |
| Pagination | khai báo rõ `cursor` hoặc `page/pageSize` | Không tự suy đoán kiểu phân trang. |
| Time zone input | ISO-8601 kèm offset nếu client gửi thời gian | Quy đổi/lưu UTC ở server. |
| Traceability | `traceId` ở response/log | Dùng để tra log và hỗ trợ vận hành. |

## 5. Chuẩn response envelope của dự án

Mỗi API cần ghi rõ có dùng đúng envelope dưới đây không. Nếu khác, bắt buộc ghi lý do trong `Overview` và mô tả toàn bộ khác biệt tại `Response`.

### 5.1. Thành công có payload

```json
{
  "businessCode": "{{MODULE}}-{{ACTION}}-SUCCESS",
  "message": "{{SUCCESS_MESSAGE}}",
  "timestamp": "2026-07-01T11:45:00Z",
  "traceId": "6a0ae20b-8407-4f0e-93c3-0279d8171c5e",
  "data": {}
}
```

### 5.2. Thành công rỗng / danh sách rỗng

```json
{
  "businessCode": "{{MODULE}}-{{ACTION}}-SUCCESS",
  "message": "{{SUCCESS_MESSAGE}}",
  "timestamp": "2026-07-01T11:45:00Z",
  "traceId": "6a0ae20b-8407-4f0e-93c3-0279d8171c5e",
  "data": [],
  "pagination": {
    "page": 1,
    "pageSize": 20,
    "totalItems": 0,
    "totalPages": 0
  }
}
```

### 5.3. Lỗi

```json
{
  "businessCode": "{{MODULE}}-{{ERROR_TYPE}}-{{NNN}}",
  "message": "{{SAFE_CLIENT_MESSAGE}}",
  "timestamp": "2026-07-01T11:45:00Z",
  "traceId": "6a0ae20b-8407-4f0e-93c3-0279d8171c5e",
  "errors": [
    {
      "field": "{{REQUEST_FIELD_OR_NULL}}",
      "code": "{{FIELD_ERROR_CODE}}",
      "message": "{{SAFE_FIELD_MESSAGE}}"
    }
  ]
}
```

**Không** trả stack trace, raw SQL, password/token, internal host, secret, hoặc thông tin giúp suy luận dữ liệu nhạy cảm của tài khoản khác.

## 6. Quy tắc mô tả quyền và dữ liệu nhạy cảm

- Mọi API phải nêu rõ **authentication scheme**, role, permission và điều kiện ownership/relationship.
- Quyền chỉ ghi kiểu `Student` là chưa đủ; cần nêu điều kiện như: `Student chỉ xem/sửa dữ liệu thuộc userId trong JWT`, `Mentor chỉ review submission được phân công`, `Employer chỉ xem candidate profile có visibility phù hợp`.
- Đánh dấu từng field nhạy cảm: `PII`, `credential`, `token`, `internal`, `public`.
- Password, refresh token, OTP, verification token, access token chỉ được ghi ví dụ giả lập; không chèn secret thật vào DD.

## 7. Tham chiếu domain và dữ liệu của Study2Work

Khi điền DD, liên kết đúng bounded context/aggregate/table để tránh cross-domain coupling không chủ đích:

| Context | Aggregate/Entity thường gặp | Bảng thường gặp |
|---|---|---|
| Identity & Access | `User`, `Session`, `Role` | `user`, `role`, `permission`, `user_role`, `session`, `refresh_token` |
| Profile | `Profile`, `StudentProfile`, `UserSkill` | `profile`, `student_profile`, `mentor_profile`, `employer_profile`, `skill`, `user_skill` |
| Learning Journey | `LearningPath`, `Module`, `Lesson` | `learning_path`, `module`, `lesson`, `lesson_content`, `learning_progress` |
| Practice & Assessment | `Quiz`, `Assignment`, `Submission`, `Review` | `quiz`, `quiz_attempt`, `assignment`, `assignment_submission`, `rubric`, `review`, `skill_assessment` |
| Project & Teamwork | `Project`, `Team`, `Task`, `Sprint` | `project`, `team`, `team_member`, `sprint`, `task`, `work_log`, `pull_request_review` |
| Career & Employer | `Portfolio`, `CV`, `JobPost`, `Application` | `portfolio`, `cv`, `job_post`, `application`, `shortlist`, `interview`, `offer`, `match_score` |
| AI Assistant | `AIRequest`, `AIInsight`, `ReviewReport` | `ai_conversation`, `ai_request`, `ai_insight`, `review_report` |
| Platform | `Notification`, `AuditLog`, `SystemSetting` | `notification`, `audit_log`, `system_setting`, `feature_flag` |

## 8. Definition of Done cho một API DD

Một DD chỉ được coi là hoàn thành khi:

- Request/response có đủ mọi field, kiểu, nullable, default, range, enum, ví dụ và dữ liệu nhạy cảm.
- Mọi HTTP status, business code, empty case, validation case và system failure được phân biệt.
- DataMapping thể hiện rõ tất cả input source, biến khởi tạo, truy vấn/ghi DB, table/column, repository method, transaction, cache, event và external dependency.
- Rule nghiệp vụ có ID hoặc tham chiếu tới Business Rule Catalog / Use Case / Activity / Sequence liên quan.
- Permission và ownership check không mơ hồ.
- Error code ổn định, safe message, retry policy và log/alert owner đầy đủ.
- History có người thay đổi, ngày, version, loại thay đổi và khả năng tương thích.
- QA có thể viết test case; FE/mobile có thể tích hợp; BE có thể code mà không phải tự đoán contract.
