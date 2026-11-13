---
task_id: "2026-11-12-implement-mentor-phase2-me09-me10"
date: "2026-11-12"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["web-work (Study Web)"]
cross_scope_dependencies:
  - "apps/study-server/app/modules/mentor/api_46_mentor_courses"
  - "apps/study-server/app/modules/mentor/api_54_mentor_submissions_list"
  - "apps/study-server/app/modules/mentor/api_55_mentor_submissions_detail"
  - "apps/study-server/app/modules/mentor/api_56_mentor_submissions_grade"
  - "apps/study-server/app/modules/mentor/api_57_mentor_submissions_feedback"
status: "VERIFIED"
---

# Worklog: Triển khai Study Web Mentor Phase 2 (ME-09, ME-10)

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `node scripts/select-worklogs.mjs --type coding --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-12/ad01-screen-coding.md`
    - carry_forward: Mỗi screen có đúng 4 thư mục con trực tiếp (`data-access/`, `models/`, `pages/`, `ui/`); mỗi component style giữ dưới 4kB budget; không bịa dữ liệu/claim chưa có contract.
  - path: `.agents/worklog/2026-11-12/admin-system-route-wiring.md`
    - carry_forward: Route group dùng layout riêng có `RouterOutlet`; kiểm thử đầy đủ route wiring trong `app.routes.spec.ts`.
  - path: `.agents/worklog/2026-11-12/implement-mentor-phase1-me06-me08.md`
    - carry_forward: Tuân thủ `PA1` — nối `models/` và `data-access/` khớp với Pydantic models của `study-server`; những phần mockup vượt quá backend hiện tại phải để `disabled` kèm giải thích trung thực và báo cáo rõ.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Thực hiện Phase 2 (`ME-09` — Danh sách bài cần chấm tại `/mentor/submissions`, `ME-10` — Chấm điểm và phản hồi tại `/mentor/submissions/:submissionId`) theo lựa chọn `PA1`.
- Study FE scope: `screens=ME-09, ME-10; APIs=#46, #54, #55, #56, #57`
- Canonical contract/approved DD:
  - `apps/study-client/docs/dd_screens/ME-09-DanhSachBaiCanCham/00-overview.md`..`07-test-cases.md`
  - `apps/study-client/docs/dd_screens/ME-10-ChamDiemVaPhanHoi/00-overview.md`..`07-test-cases.md`
  - `apps/study-server/app/modules/mentor/api_46_mentor_courses`
  - `apps/study-server/app/modules/mentor/api_54_mentor_submissions_list`..`api_57_mentor_submissions_feedback`

## MILESTONES

| Weight | Cumulative progress when achieved | Objective / acceptance criterion | Status |
|---:|---:|---|---|
| `15%` | `15%` | Preflight worklog (`select-worklogs.mjs`), đọc chi tiết DD `ME-09`/`ME-10` và source Study Server `#46, #54–#57`, khởi tạo worklog Phase 2 | `DONE` |
| `35%` | `50%` | Triển khai màn `ME-09` (`/mentor/submissions`) với đủ 4 thư mục (`models/`, `data-access/`, `ui/`, `pages/`) và unit test `me09-page.spec.ts` | `DONE` |
| `35%` | `85%` | Triển khai màn `ME-10` (`/mentor/submissions/:submissionId`) với đủ 4 thư mục (`models/`, `data-access/`, `ui/`, `pages/`) và unit test `me10-page.spec.ts` | `DONE` |
| `15%` | `100%` | Đăng ký route `/mentor/submissions` & `/mentor/submissions/:submissionId`, cập nhật `app.routes.spec.ts` + `architech.md`, chạy `npm run build` & `npm test` pass 100%, tổng hợp báo cáo API thiếu/lệch | `DONE` |

## CURRENT_BEHAVIOR

- Source/config: `mentor.route.ts` đã đăng ký `/mentor/submissions` (`ME09Page`) và `/mentor/submissions/:submissionId` (`ME10Page`). Mỗi screen có đúng 4 thư mục con trực tiếp (`data-access/`, `models/`, `pages/`, `ui/`) và không import chéo.
- Runnable tests: **7/7 test files passed, 24/24 unit tests passed** (`me06`, `me07`, `me08`, `me09`, `me10`, `ad01`, `app.routes`).
- Runtime wiring: `Me09SubmissionsService` gọi API `#46` + `#54`; `Me10GradingService` gọi API `#55`, `#56`, `#57` qua `StudyApiService.request()`.

## SOURCE_TRACE

```text
ME09Page -> Me09SubmissionsService.getMentorCourses (#46) + getSubmissions (#54 GET /api/v1/mentor/submissions) -> ApiEnvelope<SubmissionPageDto>
ME10Page -> Me10GradingService.getSubmissionDetail (#55 GET /api/v1/mentor/submissions/{submission_id}) + saveGrade (#56 POST .../grade) + saveFeedback (#57 POST .../feedback)
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| `ME-09`: Thiếu `deadline`, `owner/student_name`, `assignment_title`, `course_title` và query `q` (search) trong API `#54` | `SubmissionResponse` của `#54` chỉ trả `{id, assignment_id, user_id, content?, files[], status, submitted_at, score?, feedback?}` và query chỉ nhận `{course_id?: int64, status?: str, page: int=1}` | `DISCREPANCY` | Trên `ME-09`, hiển thị đúng `id`, `assignment_id`, `user_id`, `status`, `submitted_at`, `score`; giữ ô tìm kiếm từ khóa ở trạng thái `disabled` (kèm giải thích `#54` chưa có `q` và chưa trả `assignment_title`) |
| `ME-10`: Thiếu `rubric`, `max_score`, `student_name`, `assignment_title` trong `#55` và hai API `#56` (grade) / `#57` (feedback) tách rời, không nguyên tử | `#55` trả `SubmissionResponse` không có `rubric`/`max_score`; `#56` nhận `{score: int32, rubric_items: str}` nhưng bỏ qua `rubric_items`; `#57` nhận `{feedback_text: str, attachments: str}` nhưng bỏ qua `attachments`; hai request commit độc lập | `DISCREPANCY` | Trên `ME-10`, tách rõ 2 nút độc lập ("Lưu điểm số (#56)" và "Gửi nhận xét (#57)") với trạng thái thành công/lỗi riêng + revalidate `#55` sau mỗi thao tác; giữ nút gộp ở trạng thái `disabled` và ghi chú rõ `rubric`/`attachments` chưa được backend persist |

## CHANGES

- Files changed:
  - `apps/study-client/src/app/features/mentor/ME09/` (`models/`, `data-access/`, `ui/`, `pages/` + `me09-page.spec.ts`)
  - `apps/study-client/src/app/features/mentor/ME10/` (`models/`, `data-access/`, `ui/`, `pages/` + `me10-page.spec.ts`)
  - `apps/study-client/src/app/features/mentor/mentor.route.ts`
  - `apps/study-client/src/app/app.routes.spec.ts`
  - `apps/study-client/gui/architech.md`
  - `.agents/worklog/2026-11-12/implement-mentor-phase2-me09-me10.md`
- CONTEXT_UPDATES: Cập nhật `apps/study-client/gui/architech.md` bổ sung `ME09` và `ME10`.
- Context pages changed: `apps/study-client/gui/architech.md`, worklog này.
- Assumptions: Giữ nguyên quy tắc 4 thư mục con trực tiếp (`data-access/`, `models/`, `pages/`, `ui/`) và không import chéo giữa `ME09` và `ME10`.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type coding --limit 3` | Exit 0 (`READY`, 3 coding worklogs reviewed) | `VERIFIED` |
| `npm run build` | `ng build` thành công, không warning/error | `VERIFIED` |
| `npm test -- --watch=false` | 7/7 test files passed, 24/24 tests passed | `VERIFIED` |
| `git diff --check apps/study-client` | Exit 0 | `VERIFIED` |

## HANDOFF

- Remaining blockers: None (`Phase 2` đã `VERIFIED` 100%).
- Next owner/action: Người dùng xem báo cáo Phase 2 và xác nhận chuyển sang Phase 3 (`ME-11` — Hộp thư hỗ trợ học viên & `ME-12` — Trao đổi và đóng yêu cầu).
