---
task_id: "2026-11-12-sync-mentor-ui-design-me06-me18"
date: "2026-11-12"
primary_task_type: "coding"
secondary_task_types: ["fix", "test"]
project_scopes: ["web-work (Study Web)"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Đồng bộ giao diện và bố cục 13 màn hình Mentor (ME-06..ME-18) theo screen-clean.png

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `node scripts/select-worklogs.mjs --type coding --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-12/implement-mentor-phase5-me13-me15.md`
    - carry_forward: Giữ nguyên toàn bộ `data-testid`, contract TypeScript và kiểm soát kích thước từng file `.css` dưới ngưỡng cảnh báo `4 kB` của Angular.
  - path: `.agents/worklog/2026-11-12/implement-mentor-phase4-me16-me18.md`
    - carry_forward: Giữ nguyên cấu trúc 4 thư mục con (`models/`, `data-access/`, `ui/`, `pages/`) và luồng điều hướng `ME-16 <-> ME-17 <-> ME-18`.
  - path: `.agents/worklog/2026-11-12/implement-mentor-phase3-me09-me12.md`
    - carry_forward: Bảo toàn các selector kiểm thử tự động trong `me09..me12-page.spec.ts`.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Đọc và phân tích lại toàn bộ ảnh `images/screen-clean.png`, `images/README.md` và `01-ui-elements.md` của 13 màn hình Mentor (`ME-06`..`ME-18`) để đồng bộ lại phong cách, thanh Topbar/Footer chung, bố cục 2 cột và các trạng thái chờ đồng bộ dữ liệu giống hệt hình mẫu thiết kế ngay cả khi máy chủ backend (`127.0.0.1:3003`) chưa khởi chạy.
- Study FE scope: `screens=ME-06..ME-18; APIs=#46, #49..#67`
- Canonical contract/approved DD:
  - `apps/study-client/docs/dd_screens/ME-06..ME-18/images/screen-clean.png`
  - `apps/study-client/docs/dd_screens/ME-06..ME-18/images/README.md`
  - `apps/study-client/docs/dd_screens/ME-06..ME-18/01-ui-elements.md`
  - `.agents/web-study/design.md`

## MILESTONES

| Weight | Cumulative progress when achieved | Objective / acceptance criterion | Status |
|---:|---:|---|---|
| `20%` | `20%` | Chạy preflight worklog, đọc `.agents/web-study/design.md`, `images/README.md`, `01-ui-elements.md` và xem trực tiếp toàn bộ 13 ảnh `screen-clean.png` (`ME-06`..`ME-18`) | `DONE` |
| `20%` | `40%` | Nâng cấp `MentorLayout` (Topbar `Study2Work LMS MENTOR` + Footer chuẩn WCAG 2.1 AA) và đồng bộ 3 màn hình nội dung khóa học (`ME-06`, `ME-07`, `ME-08`) | `DONE` |
| `20%` | `60%` | Đồng bộ giao diện 4 màn hình chấm bài & hỗ trợ học viên (`ME-09`, `ME-10`, `ME-11`, `ME-12`) khớp `screen-clean.png` | `DONE` |
| `20%` | `80%` | Đồng bộ giao diện 3 màn hình tiến độ & phân tích khóa học (`ME-16`, `ME-17`, `ME-18`) khớp `screen-clean.png` | `DONE` |
| `20%` | `100%` | Đồng bộ giao diện 3 màn hình thông báo (`ME-13`, `ME-14`, `ME-15`), chạy `npm run build` (0 errors, 0 warnings) & `npm test -- --watch=false` (15/15 test suites, 51/51 tests pass) | `DONE` |

## CURRENT_BEHAVIOR

- Source/config: `MentorLayout` và cả 13 màn hình `ME-06`..`ME-18` đã đồng bộ hoàn chỉnh với `screen-clean.png`.
- Runnable tests: `15 passed (15)`, `51 passed (51)`.
- Build: `ng build` hoàn tất sạch (`0` lỗi, `0` cảnh báo).

## SOURCE_TRACE

```text
MentorLayout -> Topbar (Brand + 5 nav links + Bell + Profile TS. Vũ Thành Đạt) + RouterOutlet + Footer WCAG 2.1 AA
ME06Page..ME18Page -> Breadcrumb + Hero + KPI strips + 2-column / Showcase cards + Bottom compliance strips
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Khi `study-server` (`127.0.0.1:3003`) chưa bật, proxy trả `502 Bad Gateway` | Trước khi sửa, `@switch (screenState())` và `@if (analytics())` ẩn bố cục chính và chỉ hiện banner lỗi | `VERIFIED` | Đã cập nhật toàn bộ 13 màn hình để luôn hiển thị đầy đủ bố cục 2 cột, dải thẻ KPI, khối trung tâm `"Chưa có số liệu phân tích thống kê"` / `"Đang chờ kết nối dữ liệu"` giống `screen-clean.png` ngay cả khi API lỗi, kèm thanh cảnh báo gọn nhẹ cho phép bấm `Thử lại` |

## CHANGES

- Files changed:
  - `apps/study-client/src/app/layouts/mentor/mentor-layout.{ts,html,css}`
  - `apps/study-client/src/app/features/mentor/ME06..ME18/**/*.{ts,html,css}`
- CONTEXT_UPDATES:
  - Không thay đổi route hay kiến trúc thư mục; ghi nhận đầy đủ trong worklog này.
- Context pages changed: `.agents/worklog/2026-11-12/sync-mentor-ui-design-me06-me18.md`.
- Assumptions: Giữ nguyên toàn bộ logic gọi API `#46, #49..#67` và các thuộc tính `data-testid` của bộ unit test.

## VERIFICATION

- `cd apps/study-client && npm run build` -> Exit code `0`, `0` errors, `0` warnings.
- `cd apps/study-client && npm test -- --watch=false` -> Exit code `0`, `15 passed (15)`, `51 passed (51)`.
