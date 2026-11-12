---
task_id: "2026-11-12-implement-mentor-phase5-me13-me15"
date: "2026-11-12"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["web-work (Study Web)"]
cross_scope_dependencies:
  - "apps/study-server/app/modules/mentor/api_46_mentor_courses"
  - "apps/study-server/app/modules/mentor/api_49_course_contents"
  - "apps/study-server/app/modules/mentor/api_62_mentor_course_students"
  - "apps/study-server/app/modules/mentor/api_63_mentor_notifications"
  - "apps/study-server/app/modules/mentor/api_64_mentor_notification_status"
status: "VERIFIED"
---

# Worklog: Triển khai Study Web Mentor Phase 5 (ME-13, ME-14, ME-15)

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

- Requirement: Thực hiện Phase 5 (`ME-13` — Chọn người nhận tại `/mentor/notifications/recipients`, `ME-14` — Tạo thông báo tại `/mentor/notifications/create`, `ME-15` — Trạng thái gửi thông báo tại `/mentor/notifications/status` và `/mentor/notifications/:notificationId/status`) theo lựa chọn `PA1`.
- Study FE scope: `screens=ME-13, ME-14, ME-15; APIs=#46, #49, #62, #63, #64`
- Canonical contract/approved DD:
  - `apps/study-client/docs/dd_screens/ME-13-ChonNguoiNhan/00-overview.md`..`07-test-cases.md`
  - `apps/study-client/docs/dd_screens/ME-14-TaoThongBao/00-overview.md`..`07-test-cases.md`
  - `apps/study-client/docs/dd_screens/ME-15-TrangThaiGuiThongBao/00-overview.md`..`07-test-cases.md`
  - `apps/study-server/app/modules/mentor/api_62..64`

## MILESTONES

| Weight | Cumulative progress when achieved | Objective / acceptance criterion | Status |
|---:|---:|---|---|
| `15%` | `15%` | Chạy preflight worklog (`select-worklogs.mjs`), đối chiếu contract `#62–#64` và tạo worklog Phase 5 | `DONE` |
| `25%` | `40%` | Triển khai màn `ME-13` (`/mentor/notifications/recipients`, API `#46` + `#62`) với đủ 4 thư mục (`models/`, `data-access/`, `ui/`, `pages/`) và unit test `me13-page.spec.ts` | `DONE` |
| `25%` | `65%` | Triển khai màn `ME-14` (`/mentor/notifications/create`, API `#49` + `#63`) với đủ 4 thư mục (`models/`, `data-access/`, `ui/`, `pages/`) và unit test `me14-page.spec.ts` | `DONE` |
| `20%` | `85%` | Triển khai màn `ME-15` (`/mentor/notifications/status` & `/mentor/notifications/:notificationId/status`, API `#64`) với đủ 4 thư mục (`models/`, `data-access/`, `ui/`, `pages/`) và unit test `me15-page.spec.ts` | `DONE` |
| `15%` | `100%` | Đăng ký route `ME-13..15` trong `mentor.route.ts`, cập nhật `app.routes.spec.ts` + `architech.md`, chạy `npm run build` & `npm test` pass 100%, tổng hợp báo cáo API thiếu/lệch | `DONE` |

## CURRENT_BEHAVIOR

- Source/config: `mentor.route.ts` đã đăng ký đầy đủ tất cả 13 màn hình Mentor (`ME-06`..`ME-18`).
- Runnable tests: 15 test files (`ad01`, `me06..18`, `app.routes`) pass 100% (51/51 tests).
- Runtime wiring:
  - `/mentor/notifications/recipients` -> `ME13Page` (API `#46`, `#62`)
  - `/mentor/notifications/create` -> `ME14Page` (API `#49`, `#63`)
  - `/mentor/notifications/status` & `/mentor/notifications/:notificationId/status` -> `ME15Page` (API `#64`)

## SOURCE_TRACE

```text
ME13Page -> Me13RecipientsService.getMentorCourses() (#46) + getCourseStudents(courseId) (#62 GET /api/v1/mentor/courses/{course_id}/students)
ME14Page -> Me14CreateNotificationService.getCourseContents(courseId) (#49) + createNotification(payload) (#63 POST /api/v1/mentor/notifications)
ME15Page -> Me15NotificationStatusService.getNotificationStatus(notificationId) (#64 GET /api/v1/mentor/notifications/{notification_id}/status)
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| `ME-13`: Thiếu `email`, `progress_percent`, `group_status` (nhóm học viên chậm tiến độ / chưa nộp bài) và server-side search trong API `#62` | `#62` chỉ trả `StudentSummaryResponse[] { id: int64, full_name: str, avatar_url?: str | null }` | `DISCREPANCY` | Trên `ME-13`, hiển thị đúng `id`, `full_name`, `avatar_url`, lọc tìm kiếm client-side trên danh sách đã tải và khóa các bộ lọc nhóm thông minh kèm giải thích trung thực |
| `ME-14`: Lệch kiểu trường `content` giữa thiết kế gốc (soạn văn bản tự do / rich text + đính kèm tệp + hẹn giờ gửi) và API `#63` (`content: int64` là ID của `course_content`) | `#63` nhận `CreateNotificationRequest { recipients: str (CSV int64), title: str (<=200), content: int64, channels: str (CSV PUSH/EMAIL) }` | `DISCREPANCY` | Trên `ME-14`, cho phép chọn bài học `content` (`int64`) từ danh sách `#49` (hoặc nhập ID bài học), nhập `title` (<=200 ký tự), chọn `channels` (`PUSH`, `EMAIL`), và hiển thị vùng soạn nội dung tự do / đính kèm tệp / hẹn giờ ở trạng thái `disabled` kèm giải thích rõ contract `#63` |
| `ME-15`: Thiếu thông tin người nhận, tiêu đề thông báo, phân rã theo kênh (`PUSH`/`EMAIL`), thời gian gửi và API gửi lại (`retry`) trong API `#64` | `#64` chỉ trả `NotificationStatusOperation { operation_id: str, status: 'QUEUED' | 'SENT' | 'FAILED' }` theo từng `notification_id` | `DISCREPANCY` | Trên `ME-15`, hỗ trợ tra cứu 1 `notification_id` hoặc danh sách `ids` (từ `meta.notification_ids` của `#63`), tổng hợp số lượng `QUEUED`/`SENT`/`FAILED`, và khóa nút Gửi lại / Xuất log kèm giải thích trung thực |

## CHANGES

- Files changed:
  - `apps/study-client/src/app/features/mentor/ME13/**` (12 files)
  - `apps/study-client/src/app/features/mentor/ME14/**` (12 files)
  - `apps/study-client/src/app/features/mentor/ME15/**` (12 files)
  - `apps/study-client/src/app/features/mentor/mentor.route.ts`
  - `apps/study-client/src/app/app.routes.spec.ts`
  - `apps/study-client/gui/architech.md`
- CONTEXT_UPDATES:
  - Cập nhật `gui/architech.md` phản ánh toàn bộ 13 màn hình `ME06`..`ME18`.
- Context pages changed: `apps/study-client/gui/architech.md`, worklog này.
- Assumptions: Truyền dữ liệu giữa `ME-13 -> ME-14 -> ME-15` qua cả `queryParams` (`courseId`, `recipients`, `ids`, `op`) lẫn Router navigation `state` để reload trang không làm mất trạng thái.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type coding --limit 3` | Exit 0 (`READY`, 3 coding worklogs reviewed) | `VERIFIED` |
| `npm run build` (tại `apps/study-client`) | Exit 0 (`3.562s`, bundle `mentor-route` generated without warnings) | `VERIFIED` |
| `npm test -- --watch=false` (tại `apps/study-client`) | Exit 0 (`15 passed (15)`, `51 passed (51)`) | `VERIFIED` |
| `node scripts/validate-agent-context.mjs` | Chạy kiểm tra worklog Phase 5 (0 lỗi worklog; baseline repo có drift `db-admin`/`CONTEXT_STALE`) | `VERIFIED` |

## HANDOFF

- Remaining blockers: Không còn blocker. Toàn bộ 5 Phase (13 màn hình Mentor `ME-06`..`ME-18`) đã hoàn thành và pass 100% build + unit tests.
- Next owner/action: Sẵn sàng bàn giao hoặc tích hợp thêm luồng Auth (`SH-03`) khi người dùng yêu cầu.
