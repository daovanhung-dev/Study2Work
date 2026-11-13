---
task_id: "2026-11-12-implement-mentor-phase4-me16-me18"
date: "2026-11-12"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["web-work (Study Web)"]
cross_scope_dependencies:
  - "apps/study-server/app/modules/mentor/api_65_mentor_course_progress"
  - "apps/study-server/app/modules/mentor/api_66_mentor_course_analytics"
  - "apps/study-server/app/modules/mentor/api_67_mentor_student_progress"
status: "VERIFIED"
---

# Worklog: Triển khai Study Web Mentor Phase 4 (ME-16, ME-17, ME-18)

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

- Requirement: Thực hiện Phase 4 (`ME-16` — Tiến độ toàn khóa học tại `/mentor/courses/:courseId/progress`, `ME-17` — Tiến độ từng học viên tại `/mentor/courses/:courseId/students/:studentId/progress`, `ME-18` — Analytics khóa học tại `/mentor/courses/:courseId/analytics`) theo lựa chọn `PA1`.
- Study FE scope: `screens=ME-16, ME-17, ME-18; APIs=#65, #66, #67`
- Canonical contract/approved DD:
  - `apps/study-client/docs/dd_screens/ME-16-TienDoToanKhoaHoc/00-overview.md`..`07-test-cases.md`
  - `apps/study-client/docs/dd_screens/ME-17-TienDoTungHocVien/00-overview.md`..`07-test-cases.md`
  - `apps/study-client/docs/dd_screens/ME-18-AnalyticsKhoaHoc/00-overview.md`..`07-test-cases.md`
  - `apps/study-server/app/modules/mentor/api_65..67`

## MILESTONES

| Weight | Cumulative progress when achieved | Objective / acceptance criterion | Status |
|---:|---:|---|---|
| `15%` | `15%` | Chạy preflight worklog (`select-worklogs.mjs`), đọc chi tiết DD `ME-16`/`ME-17`/`ME-18` và source Study Server `#65–#67`, khởi tạo worklog Phase 4 | `DONE` |
| `25%` | `40%` | Triển khai màn `ME-16` (`/mentor/courses/:courseId/progress`) với đủ 4 thư mục (`models/`, `data-access/`, `ui/`, `pages/`) và unit test `me16-page.spec.ts` | `DONE` |
| `25%` | `65%` | Triển khai màn `ME-17` (`/mentor/courses/:courseId/students/:studentId/progress`) với đủ 4 thư mục (`models/`, `data-access/`, `ui/`, `pages/`) và unit test `me17-page.spec.ts` | `DONE` |
| `20%` | `85%` | Triển khai màn `ME-18` (`/mentor/courses/:courseId/analytics`) với đủ 4 thư mục (`models/`, `data-access/`, `ui/`, `pages/`) và unit test `me18-page.spec.ts` | `DONE` |
| `15%` | `100%` | Đăng ký 3 route trong `mentor.route.ts`, cập nhật `app.routes.spec.ts` + `architech.md`, chạy `npm run build` & `npm test` pass 100%, tổng hợp báo cáo API thiếu/lệch | `DONE` |

## CURRENT_BEHAVIOR

- Source/config: `mentor.route.ts` đã đăng ký đầy đủ `ME-06`..`ME-12` và `ME-16`..`ME-18`.
- Runnable tests: 12 test files (`ad01`, `me06..12`, `me16..18`, `app.routes`) pass 100% (41/41 tests).
- Runtime wiring:
  - `/mentor/courses/:courseId/progress` -> `ME16Page` (API `#65`)
  - `/mentor/courses/:courseId/students/:studentId/progress` -> `ME17Page` (API `#67`)
  - `/mentor/courses/:courseId/analytics` -> `ME18Page` (API `#66`)

## SOURCE_TRACE

```text
ME16Page -> Me16ProgressService.getCourseProgress(courseId) (#65 GET /api/v1/mentor/courses/{course_id}/progress) -> ApiEnvelope<MentorStudentProgressPageDto>
ME17Page -> Me17StudentProgressService.getStudentCourseProgress(courseId, studentId) (#67 GET /api/v1/mentor/courses/{course_id}/students/{student_id}/progress) -> ApiEnvelope<StudentCourseProgressDto>
ME18Page -> Me18AnalyticsService.getCourseAnalytics(courseId) (#66 GET /api/v1/mentor/courses/{course_id}/analytics) -> ApiEnvelope<MentorCourseActivityAnalyticsDto>
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| `ME-16`: Thiếu `email`, `last_activity`, `submissions`, `attendance`, `risk_category`, `course_title`, filter/search query và nhắc nhở học viên trong API `#65` | `#65` trả `MentorStudentProgressPage {items: [{student: {id, full_name, avatar_url?}, completed_lessons, total_lessons, progress_percent}], pagination}` và không nhận query filter | `DISCREPANCY` | Trên `ME-16`, hiển thị đúng `student`, `completed_lessons`, `total_lessons`, `progress_percent`, lọc client-side trên trang hiện tại và khóa các nút Nhắc nhở / Xuất báo cáo |
| `ME-17`: Thiếu event timeline lịch sử học tập, số bài tập/quiz, giờ tự học, nhận xét mentor trong API `#67` | `#67` chỉ trả snapshot trạng thái từng bài học theo thứ tự chương trình: `StudentCourseProgress {course_id, student, summary, lessons: [{lesson_id, title, order, progress_status, progress_percent, last_accessed_at?, completed_at?}]}` | `DISCREPANCY` | Trên `ME-17`, hiển thị đúng `summary` và danh sách snapshot bài học `lessons[]` từ `#67`, ghi chú rõ chưa có event ledger/quiz/assignment |
| `ME-18`: Thiếu tỷ lệ hoàn thành, thời lượng học trung bình, thảo luận, bộ lọc kỳ thời gian (`7d`/`30d`) và xuất CSV trong API `#66` | `#66` chỉ trả `MentorCourseActivityAnalytics {tracked_lesson_accesses, students_with_activity, last_activity_at}` | `DISCREPANCY` | Trên `ME-18`, hiển thị đúng 3 chỉ số proxy từ `#66` và khóa bộ chọn kỳ thời gian + nút xuất CSV kèm giải thích trung thực |

## CHANGES

- Files changed:
  - `apps/study-client/src/app/features/mentor/ME16/**` (12 files)
  - `apps/study-client/src/app/features/mentor/ME17/**` (12 files)
  - `apps/study-client/src/app/features/mentor/ME18/**` (9 files)
  - `apps/study-client/src/app/features/mentor/mentor.route.ts`
  - `apps/study-client/src/app/app.routes.spec.ts`
  - `apps/study-client/gui/architech.md`
- CONTEXT_UPDATES:
  - Cập nhật cây thư mục `gui/architech.md` phản ánh `ME16`, `ME17`, `ME18`.
- Context pages changed: `apps/study-client/gui/architech.md`, worklog này.
- Assumptions: Giữ nguyên quy tắc 4 thư mục con trực tiếp (`data-access/`, `models/`, `pages/`, `ui/`) và không import chéo giữa `ME16`, `ME17`, `ME18`.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type coding --limit 3` | Exit 0 (`READY`, 3 coding worklogs reviewed) | `VERIFIED` |
| `npm run build` (tại `apps/study-client`) | Exit 0 (`2.783s`, bundle `mentor-route` generated without warnings) | `VERIFIED` |
| `npm test -- --watch=false` (tại `apps/study-client`) | Exit 0 (`12 passed (12)`, `41 passed (41)`) | `VERIFIED` |
| `node scripts/validate-agent-context.mjs` | Exit 0 (`OK: agent context registry passed validation`) | `VERIFIED` |

## HANDOFF

- Remaining blockers: Không còn blocker cho Phase 4 (`ME-16`..`ME-18`).
- Next owner/action: Chuyển sang Phase 5 (`ME-13`, `ME-14`, `ME-15` — Chọn người nhận, Tạo thông báo và Trạng thái gửi thông báo).
