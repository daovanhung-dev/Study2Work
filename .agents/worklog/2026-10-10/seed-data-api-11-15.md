---
task_id: "2026-10-10-seed-data-api-11-15"
date: "2026-10-10"
primary_task_type: "coding"
secondary_task_types: ["test"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo Seed Data cho API #11 và API #15 trên Study Server

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `node scripts/select-worklogs.mjs --type coding --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-04/study-db-schema-per-transaction-reapply.md`
    - carry_forward: Phải đảm bảo transaction-local search_path cho schema Neon của Study Server; không thêm public fallback bừa bãi.
  - path: `.agents/worklog/2026-09-28/remove-study-apiresponse.md`
    - carry_forward: Giữ nguyên các thay đổi không liên quan trong worktree; chạy test của Study.
  - path: `.agents/worklog/2026-09-28/study-apierror-direct-json.md`
    - carry_forward: Giới hạn scope Study, ghi nhận baseline khi có context failure không liên quan.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tạo seed data cho API #11 (`/courses/{course_id}/resources`) và API #15 (`/courses/{course_id}/enrollment-status`) trong schema của người dùng (`hoang_xuan_long`) để người dùng kiểm thử qua Thunder Client.
- Canonical contract/approved DD:
  - API #11: Truy vấn `courses` (kiểm tra `status = 'PUBLISHED'`), `lessons` và `resources` (ánh xạ `resource_type` -> `type`). Nếu course không tồn tại, chưa publish, hoặc không có resource, trả 404 `DESIGN_RESOURCE_NOT_FOUND`. Ngược lại trả 200 `DESIGN_RESOURCE_RETRIEVED`.
  - API #15: Truy vấn `courses` và `enrollments`. Nếu có header `Authorization: Bearer <token>`, trích xuất `user_id` và tìm enrollment theo `(course_id, user_id)`. Nếu không có token, fallback lấy enrollment theo `course_id`. Trả 200 `DESIGN_RESOURCE_RETRIEVED` hoặc 404 `DESIGN_RESOURCE_NOT_FOUND`.

## CURRENT_BEHAVIOR

- Source/config:
  - `apps/study-server/app/core/constants.py` cấu hình `DB_SCHEMA = "hoang_xuan_long"` kết nối tới CSDL Neon.
  - Các bảng `users`, `courses`, `lessons`, `resources`, `enrollments` trong schema `hoang_xuan_long` đã có cấu trúc đầy đủ nhưng chưa có bản ghi (0 rows).
- Runnable tests: 11 unit tests trong `tests/modules/guest/api_11_courses_resources` và `api_15_courses_enrollment_status` đang pass với mock database.

## SOURCE_TRACE

```text
Thunder Client -> GET /api/v1/courses/{course_id}/resources -> API #11 view -> courses (PUBLISHED), lessons, resources -> ResourceItem response
Thunder Client -> GET /api/v1/courses/{course_id}/enrollment-status -> API #15 view -> resolve_optional_user_id -> courses, enrollments -> EnrollmentStatusResponse response
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Schema thiếu seed data | Schema `hoang_xuan_long` trên Neon có 0 rows cho users, courses, lessons, resources, enrollments | RESOLVED | Đã tạo SQL script và Python script nạp dữ liệu mẫu và nạp thành công vào DB |

## CHANGES

- Files changed:
  - `infra/postgres/study-server/seed_api_11_15.sql`: SQL seed data độc lập có thể chạy trực tiếp bằng psql / pgAdmin / DBeaver.
  - `apps/study-server/scripts/seed_api_11_15.py`: Python CLI script tự động nạp seed data qua cấu hình ứng dụng và sinh JWT token phục vụ test.
  - `.agents/worklog/2026-10-10/seed-data-api-11-15.md`: Worklog này.
- CONTEXT_UPDATES: Không thay đổi architecture, route hay API contract.
- Context pages changed: None.
- Assumptions: Sử dụng schema `hoang_xuan_long` theo đúng `app.core.constants.DB_SCHEMA`.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `.\.venv\Scripts\python.exe scripts/seed_api_11_15.py` | Áp dụng seed data thành công vào schema `hoang_xuan_long` | PASS |
| `.\.venv\Scripts\pytest.exe tests/modules/guest/api_11_courses_resources tests/modules/guest/api_15_courses_enrollment_status` | 11 passed | PASS |
| Verification API với TestClient và live DB | Trả về 200 OK và 404 đúng theo các kịch bản | PASS |
| `node scripts/validate-agent-context.mjs` | Kiểm tra tính hợp lệ của agent context | PASS |

## HANDOFF

- Remaining blockers: Không.
- Next owner/action: Khởi động Study server và test bằng Thunder Client theo hướng dẫn.

