---
task_id: "2026-10-20-analyze-and-plan-study-api21-25"
date: "2026-10-20"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Phân tích và lập kế hoạch lập trình Study API #21–#25

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3` (Node not in PATH; manually selected latest 3 `docs` worklogs sorted by date DESC, path ASC)
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-12/create-study-api27-dd.md`
    - carry_forward: Tách biệt expected design contract khỏi current runtime source; ghi rõ `UNWIRED / NOT_FOUND`, `DISCREPANCY`, `SOURCE_REQUIRED`.
  - path: `.agents/worklog/2026-10-12/create-study-api28-dd.md`
    - carry_forward: Giữ nguyên contract từ `docs/lists/list_api.md` và đối chiếu với sơ đồ AC cùng DDL/ERD.
  - path: `.agents/worklog/2026-10-12/create-study-api29-dd.md`
    - carry_forward: Ghi nhận đầy đủ các điểm khác biệt về nullability/constraint trong `DB.sql` so với `DB_UNICA_TABLES.md`.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Phân tích các API #21–#25, tạo 1 file giải thích tác dụng của các API này và 1 file plan lập trình các API này có cấu trúc tương tự các API đã viết trong `apps/study-server`, đặt tại `D:\s2w\Study2Work\docs\devs\2. hoangxuanlong\note`. Lưu ý trong plan khi viết `try - except`: khi chỉ có 1 loại lỗi trả về thì dùng `except:` (không cần ghi `SQLAlchemyError`...), trừ trường hợp 1 `try` trả về nhiều lỗi khác nhau.
- Canonical contract/approved DD: `docs/lists/list_api.md` (API #21–#25), `AC-13`, `AC-14`, `AC-15`, `AC-18`, cùng các bản DD draft tại `apps/study-server/docs/dd/21_users_me_progress` đến `25_lessons_progress`.

## CURRENT_BEHAVIOR

- Source/config: `apps/study-server/app/api/v1.py` và `apps/study-server/app/modules/guest/` hiện đã có các API #01–#09, #11–#15; chưa có route/module cho API #21–#25.
- Runnable tests: Chưa có test cho API #21–#25 trong `apps/study-server/tests/modules/guest/`.
- Runtime wiring: Các API #21–#25 hiện ở trạng thái `UNWIRED / NOT_FOUND`.

## SOURCE_TRACE

```text
User request -> docs/lists/list_api.md + AC_02_STUDENT_LEARNING + DB_UNICA_TABLES.md/DB.sql + DD #21-#25 + existing guest modules (api_04, api_09, api_11, api_14, api_15) -> docs/devs/2. hoangxuanlong/note/{phan_tich_api_21_25.md, plan_lap_trinh_api_21_25.md}
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #21–#25 runtime | Không có trong `app/api/v1.py` và `app/modules/guest/`. | `UNWIRED / NOT_FOUND` | Tài liệu phân tích và plan phục vụ bước lập trình tiếp theo. |
| API #21 response schema | `list_api.md` khai báo `ApiEnvelope<UserProfile>` trong khi `AC-13`/`AC-18` mô tả dữ liệu tiến độ tổng hợp. | `DISCREPANCY` | Đã ghi rõ trong file phân tích và plan. |
| `lesson_progress` unique constraint & `position` column | `DB.sql` không có `UNIQUE (user_id, lesson_id)` và không có cột `position`. | `DISCREPANCY / SOURCE_REQUIRED` | Plan hướng dẫn kiểm tra `SELECT` trước khi `INSERT`/`UPDATE` trong transaction và chỉ lưu các cột hiện có của `lesson_progress`. |

## CHANGES

- Files changed:
  - `docs/devs/2. hoangxuanlong/note/phan_tich_api_21_25.md`
  - `docs/devs/2. hoangxuanlong/note/plan_lap_trinh_api_21_25.md`
  - `.agents/worklog/2026-10-20/analyze-and-plan-study-api21-25.md`
- CONTEXT_UPDATES: None (không thay đổi runtime source hay `.agents/` context).
- Context pages changed: None.
- Assumptions: Tuân thủ yêu cầu của user về vị trí lưu file và quy ước viết `try - except` trong plan.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| Kiểm tra sự tồn tại và nội dung 2 file trong `docs/devs/2. hoangxuanlong/note/` | Đã tạo đầy đủ `phan_tich_api_21_25.md` và `plan_lap_trinh_api_21_25.md`. | `VERIFIED` |
| `node scripts/validate-agent-context.mjs` | Node không có trong PATH của môi trường hiện tại; không có file context `.agents/` nào bị sửa đổi. | `DECLARED_NOT_RUNNABLE` |

## HANDOFF

- Remaining blockers: Xác nhận từ Leader/Contract owner về các điểm `DISCREPANCY` (response schema của API #21, cột `position` của API #25) trước hoặc trong khi code.
- Next owner/action: Thực hiện lập trình từng module `api_21` đến `api_25` theo `plan_lap_trinh_api_21_25.md`.

