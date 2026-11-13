---
task_id: "2026-10-20-implement-study-api21-25"
date: "2026-10-20"
primary_task_type: "coding"
secondary_task_types: ["test"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Lập trình và kiểm thử Study API #21–#25

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `node scripts/select-worklogs.mjs --type coding --limit 3` (Node not in PATH; manually selected latest 3 `coding` worklogs sorted by date DESC, path ASC)
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-11/implement-study-api13-avatar-upload.md`
    - carry_forward: Phân tách rõ ràng giữa router (`app/api/v1.py`), controller/view (`view.py`), database query (`query.py`), request/response schema (`models.py`) và validation (`validate.py`). Quản lý transaction tường minh bằng `db.begin()`.
  - path: `.agents/worklog/2026-09-28/study-api-11-15-validate-error-response.md`
    - carry_forward: Tuân thủ cấu trúc `ApiEnvelope` chuẩn của hệ thống và định dạng lỗi `error_response(...)` với `fieldErrors` trong `meta`.
  - path: `.agents/worklog/2026-09-27/register-routes-11-15.md`
    - carry_forward: Đăng ký router mỏng tại `app/api/v1.py` với tiền tố và tag module rõ ràng.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement:
  - Triển khai lập trình 5 API từ #21 đến #25 cho `apps/study-server` theo kế hoạch đã lập tại `docs/devs/2. hoangxuanlong/note/plan_lap_trinh_api_21_25.md`.
  - Quy tắc `try - except`: Khi trong khối `try` chỉ có 1 loại lỗi xảy ra thì dùng bare `except:` thay vì khai báo lớp lỗi cụ thể (như `except SQLAlchemyError:`), trừ trường hợp cần phân biệt nhiều loại lỗi.
  - Viết đầy đủ unit tests cho cả 5 API và đảm bảo toàn bộ test suite của `study-server` chạy pass.
- Canonical contract/approved DD:
  - `docs/lists/list_api.md` (APIs #21–#25).
  - Sequence diagrams `AC_02_STUDENT_LEARNING.drawio` (`AC-13`, `AC-14`, `AC-15`, `AC-18`).
  - Schema cơ sở dữ liệu `infra/postgres/study-server/DB.sql` và `apps/study-server/docs/diagrams/DB_UNICA_TABLES.md`.

## CURRENT_BEHAVIOR

- Source/config:
  - Cả 5 module đã được lập trình hoàn chỉnh trong `apps/study-server/app/modules/guest/`:
    - `api_21_users_me_progress/` (`models.py`, `query.py`, `validate.py`, `view.py`)
    - `api_22_lessons_access/` (`models.py`, `query.py`, `validate.py`, `view.py`)
    - `api_23_lessons_start/` (`models.py`, `query.py`, `validate.py`, `view.py`)
    - `api_24_lessons_detail/` (`models.py`, `query.py`, `validate.py`, `view.py`)
    - `api_25_lessons_progress/` (`models.py`, `query.py`, `validate.py`, `view.py`)
  - Đã import và mount 5 route tại `apps/study-server/app/api/v1.py`:
    - `GET /api/v1/users/me/progress`
    - `GET /api/v1/lessons/{lesson_id}/access`
    - `POST /api/v1/lessons/{lesson_id}/start`
    - `GET /api/v1/lessons/{lesson_id}`
    - `PATCH /api/v1/lessons/{lesson_id}/progress`
- Runnable tests:
  - Đã tạo 5 test suite trong `apps/study-server/tests/modules/guest/`:
    - `api_21_users_me_progress/test_users_me_progress.py` (5 tests)
    - `api_22_lessons_access/test_lessons_access.py` (6 tests)
    - `api_23_lessons_start/test_lessons_start.py` (7 tests)
    - `api_24_lessons_detail/test_lessons_detail.py` (8 tests)
    - `api_25_lessons_progress/test_lessons_progress.py` (8 tests)
  - Chạy `pytest tests/`: **282 passed** in 14.97s (100% pass).

## SOURCE_TRACE

```text
HTTP Request
  -> FastAPI router (apps/study-server/app/api/v1.py)
  -> View handler (app/modules/guest/api_XX_.../view.py)
  -> Auth dependency & Query validation (validate.py)
  -> DB Queries via Engine (query.py) [infra/postgres/study-server tables: users, courses, enrollments, lessons, modules, resources, lesson_progress]
  -> ApiEnvelope Response / error_response (models.py)
  -> Tests (apps/study-server/tests/modules/guest/api_XX_.../test_*.py)
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| `lesson_progress` position column | `DB.sql` không có cột `position`. | `SOURCE_BACKED / MITIGATED` | `models.py` nhận `position` (optional) theo contract; `query.py` không thực thi update cột `position` để tránh lỗi SQL `column does not exist`. |
| `lesson_progress` unique constraint | `DB.sql` không có ràng buộc `UNIQUE (user_id, lesson_id)`. | `SOURCE_BACKED / MITIGATED` | View logic kiểm tra `SELECT` tồn tại trước khi `INSERT` hoặc `UPDATE` trong transaction atomic. |
| API #21 response schema | `list_api.md` ghi `ApiEnvelope<UserProfile>`, nhưng nghiệp vụ `AC-13` và `AC-18` là tiến độ tổng hợp qua các khóa học. | `RESOLVED_AS_EXPECTED` | Triển khai theo nghiệp vụ tiến độ tổng hợp đúng logic thực tế. |

## CHANGES

- Files created:
  - `apps/study-server/app/modules/guest/api_21_users_me_progress/{__init__.py, models.py, query.py, validate.py, view.py}`
  - `apps/study-server/app/modules/guest/api_22_lessons_access/{__init__.py, models.py, query.py, validate.py, view.py}`
  - `apps/study-server/app/modules/guest/api_23_lessons_start/{__init__.py, models.py, query.py, validate.py, view.py}`
  - `apps/study-server/app/modules/guest/api_24_lessons_detail/{__init__.py, models.py, query.py, validate.py, view.py}`
  - `apps/study-server/app/modules/guest/api_25_lessons_progress/{__init__.py, models.py, query.py, validate.py, view.py}`
  - `apps/study-server/tests/modules/guest/api_21_users_me_progress/{__init__.py, test_users_me_progress.py}`
  - `apps/study-server/tests/modules/guest/api_22_lessons_access/{__init__.py, test_lessons_access.py}`
  - `apps/study-server/tests/modules/guest/api_23_lessons_start/{__init__.py, test_lessons_start.py}`
  - `apps/study-server/tests/modules/guest/api_24_lessons_detail/{__init__.py, test_lessons_detail.py}`
  - `apps/study-server/tests/modules/guest/api_25_lessons_progress/{__init__.py, test_lessons_progress.py}`
  - `docs/devs/2. hoangxuanlong/worklogs/2026-10-20/implement-study-api21-25.md`
- Files modified:
  - `apps/study-server/app/api/v1.py` (mount 5 endpoints)
  - `docs/devs/2. hoangxuanlong/worklogs/worklog.md` (cập nhật dòng 3-7 và bổ sung chi tiết đối chiếu Schema cho các API #21–#25)

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `pytest tests/modules/guest/api_21_users_me_progress` | 5 passed | `VERIFIED` |
| `pytest tests/modules/guest/api_22_lessons_access` | 6 passed | `VERIFIED` |
| `pytest tests/modules/guest/api_23_lessons_start` | 7 passed | `VERIFIED` |
| `pytest tests/modules/guest/api_24_lessons_detail` | 8 passed | `VERIFIED` |
| `pytest tests/modules/guest/api_25_lessons_progress` | 8 passed | `VERIFIED` |
| `pytest tests/` (full test suite) | **282 passed in 14.97s** | `VERIFIED` |

## HANDOFF

- Remaining blockers: Không có blocker.
- Next owner/action: Đưa vào review PR / tích hợp với client web & mobile.

