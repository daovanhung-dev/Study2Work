---
task_id: "2026-10-10-study-api-11-15-validate-error-response"
date: "2026-10-10"
primary_task_type: "fix"
secondary_task_types: ["coding", "test"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Thay thế ValueError trong validator API #11 và API #15 bằng error_response

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `fix`
- selector_command: `node scripts/select-worklogs.mjs --type fix --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-09-28/study-middleware-single-exception-path.md`
    - carry_forward: Giữ cấu trúc exception handler trong Study, response phải có status, business code, envelope và trace ID.
  - path: `.agents/worklog/2026-09-27/remove-study-exceptions-module.md`
    - carry_forward: Không tạo lại custom exception ngoài kiến trúc; sử dụng helper phản hồi chuẩn `app/core/responses.py`.
  - path: `.agents/worklog/2026-09-18/work-server-constants.md`
    - carry_forward: Phạm vi Study server độc lập với Work server.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Trong `validate.py` của API #11 và API #15, không raise `ValueError` mà trả về trực tiếp envelope lỗi thông qua hàm `error_response` tại `app/core/responses.py`.
- Canonical contract/approved DD:
  - Rule 8 trong `.agents/server-study/AGENTS.md`: Validator trả dữ liệu đã chuẩn hóa khi hợp lệ; khi input sai, trả lỗi bằng `return error_response(...)`. Không raise exception từ validator để view phải bắt `try ... except ValueError`.
  - API #11: Trả `404 DESIGN_RESOURCE_NOT_FOUND` khi `course_id` không hợp lệ (`<= 0` hoặc không phải `int`).
  - API #15: Trả `404 DESIGN_RESOURCE_NOT_FOUND` khi `course_id` không hợp lệ (`<= 0` hoặc không phải `int`).

## CURRENT_BEHAVIOR

- Source/config:
  - Trước khi sửa: `validate_course_id(course_id)` trong cả 2 API raise `ValueError("course_id must be an integer.")`, và trong `view.py` phải bọc `try ... except ValueError` để gọi `_not_found_error`.
  - Sau khi sửa: `validate_course_id(course_id, *, trace_id)` trả về `int | JSONResponse`. Nếu input không hợp lệ, gọi trực tiếp `return error_response(...)`. Trong `view.py`, chỉ cần kiểm tra `if isinstance(validated_course_id, JSONResponse): return validated_course_id`.

## SOURCE_TRACE

```text
Request -> API v1 route -> get_course_resources / get_enrollment_status -> validate_course_id(course_id, trace_id=trace_id)
  -> nếu không hợp lệ: return error_response(...) -> JSONResponse (404 DESIGN_RESOURCE_NOT_FOUND)
  -> nếu hợp lệ: tiếp tục luồng query DB
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Validator dùng ValueError | `validate_course_id` trước đó raise `ValueError` trái với convention Rule 8 | RESOLVED | Đã chuyển sang trả `error_response(...)` trực tiếp |

## CHANGES

- Files changed:
  - `apps/study-server/app/modules/guest/api_11_courses_resources/validate.py`
  - `apps/study-server/app/modules/guest/api_11_courses_resources/view.py`
  - `apps/study-server/app/modules/guest/api_15_courses_enrollment_status/validate.py`
  - `apps/study-server/app/modules/guest/api_15_courses_enrollment_status/view.py`
  - `apps/study-server/tests/modules/guest/api_11_courses_resources/test_courses_resources.py`
  - `apps/study-server/tests/modules/guest/api_15_courses_enrollment_status/test_enrollment_status.py`
  - `.agents/worklog/2026-10-10/study-api-11-15-validate-error-response.md`
- CONTEXT_UPDATES: Không thay đổi architecture, route hay API contract.
- Context pages changed: None.
- Assumptions: Giữ mã lỗi `404 DESIGN_RESOURCE_NOT_FOUND` theo đúng DD của API #11 và API #15.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `.\.venv\Scripts\pytest.exe tests/modules/guest/api_11_courses_resources tests/modules/guest/api_15_courses_enrollment_status` | 15 passed | PASS |
| `.\.venv\Scripts\pytest.exe` (full suite) | 180 passed | PASS |
| `.\.venv\Scripts\ruff.exe check app/modules/guest/api_11_courses_resources app/modules/guest/api_15_courses_enrollment_status` | 0 errors | PASS |

## HANDOFF

- Remaining blockers: Không.
- Next owner/action: Tiếp tục kiểm thử các API qua Thunder Client.

