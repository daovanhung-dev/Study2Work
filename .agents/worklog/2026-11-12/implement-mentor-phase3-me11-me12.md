---
task_id: "2026-11-12-implement-mentor-phase3-me11-me12"
date: "2026-11-12"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["web-work (Study Web)"]
cross_scope_dependencies:
  - "apps/study-server/app/modules/mentor/api_46_mentor_courses"
  - "apps/study-server/app/modules/mentor/api_58_mentor_support_requests"
  - "apps/study-server/app/modules/mentor/api_59_mentor_support_request_detail"
  - "apps/study-server/app/modules/mentor/api_60_mentor_support_reply"
  - "apps/study-server/app/modules/mentor/api_61_mentor_support_resolve"
status: "VERIFIED"
---

# Worklog: Triển khai Study Web Mentor Phase 3 (ME-11, ME-12)

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

- Requirement: Thực hiện Phase 3 (`ME-11` — Hộp thư hỗ trợ học viên tại `/mentor/support`, `ME-12` — Trao đổi và đóng yêu cầu tại `/mentor/support/:requestId`) theo lựa chọn `PA1`.
- Study FE scope: `screens=ME-11, ME-12; APIs=#46, #58, #59, #60, #61`
- Canonical contract/approved DD:
  - `apps/study-client/docs/dd_screens/ME-11-HopThuHoTroHocVien/00-overview.md`..`07-test-cases.md`
  - `apps/study-client/docs/dd_screens/ME-12-TraoDoiVaDongYeuCau/00-overview.md`..`07-test-cases.md`
  - `apps/study-server/app/modules/mentor/api_46_mentor_courses`
  - `apps/study-server/app/modules/mentor/api_58..61`

## MILESTONES

| Weight | Cumulative progress when achieved | Objective / acceptance criterion | Status |
|---:|---:|---|---|
| `15%` | `15%` | Chạy preflight worklog (`select-worklogs.mjs`), đọc chi tiết DD `ME-11`/`ME-12` và source Study Server `#58–#61`, khởi tạo worklog Phase 3 | `DONE` |
| `35%` | `50%` | Triển khai màn `ME-11` (`/mentor/support`) với đủ 4 thư mục (`models/`, `data-access/`, `ui/`, `pages/`) và unit test `me11-page.spec.ts` | `DONE` |
| `35%` | `85%` | Triển khai màn `ME-12` (`/mentor/support/:requestId`) với đủ 4 thư mục (`models/`, `data-access/`, `ui/`, `pages/`) và unit test `me12-page.spec.ts` | `DONE` |
| `15%` | `100%` | Đăng ký route `/mentor/support` & `/mentor/support/:requestId`, cập nhật `app.routes.spec.ts` + `architech.md`, chạy `npm run build` & `npm test` pass 100%, tổng hợp báo cáo API thiếu/lệch | `DONE` |

## CURRENT_BEHAVIOR

- Source/config: `mentor.route.ts` đã đăng ký `/mentor/support` (`ME11Page`) và `/mentor/support/:requestId` (`ME12Page`). Mỗi screen có đúng 4 thư mục con trực tiếp (`data-access/`, `models/`, `pages/`, `ui/`) và không import chéo.
- Runnable tests: **9/9 test files passed, 31/31 unit tests passed** (`me06..12`, `ad01`, `app.routes`).
- Runtime wiring: `Me11SupportService` gọi API `#46` (`GET mentor/courses`) + `#58` (`GET mentor/support/requests`); `Me12ThreadService` gọi API `#59` (`GET mentor/support/{request_id}`), `#60` (`POST mentor/support/{request_id}/reply`), `#61` (`PATCH mentor/support/{request_id}/resolve`).

## SOURCE_TRACE

```text
ME11Page -> Me11SupportService.getMentorCourses (#46) + getSupportRequests (#58 GET /api/v1/mentor/support/requests) -> ApiEnvelope<SupportRequestItemDto[]>
ME12Page -> Me12ThreadService.getSupportRequestDetail (#59 GET /api/v1/mentor/support/{request_id}) + sendReply (#60 POST .../reply) + resolveRequest (#61 PATCH .../resolve)
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| `ME-11`: Thiếu `course_title`, SLA `< 4 giờ`, kho giải đáp chuẩn, Google Meet 1:1 và facet counts từ server trong API `#58` | `#58` trả `SupportRequestResponse[]` (`{id, course_id, student, status, messages[], created_at, resolved_at?}`) không phân trang, không có `course_title` hay SLA/facets | `DISCREPANCY` | Trên `ME-11`, nối `#46` để lấy danh sách khóa học cho bộ lọc `course_id`, tính số lượng hiển thị trên dữ liệu đã tải và ghi chú rõ SLA/kho câu trả lời/Google Meet là thông tin hướng dẫn tĩnh |
| `ME-12`: Thiếu Socket/TLS realtime, giới hạn 2000 ký tự, khảo sát hài lòng/nghiệm thu tự động, attachment picker; `#60` nhận `attachment_refs: str` (JSON mảng ID `int64`), `#61` chỉ cho phép `OPEN`/`IN_PROGRESS`/`WAITING_LEARNER` (hoặc `RESOLVED` idempotent) | `#59..#61` là REST HTTP; `#60` yêu cầu `{message: str, attachment_refs: str}` (`"[]"` khi không đính kèm); `#61` trả `422` nếu `status == 'CANCELLED'` | `DISCREPANCY` | Trên `ME-12`, gửi `attachment_refs: "[]"` mặc định (khóa nút chọn file đính kèm mới vì chưa có upload purpose cho support reply), thêm bước xác nhận trước khi gọi `PATCH #61` và hiển thị rõ trạng thái Socket/SLA/Survey là tĩnh |

## CHANGES

- Files changed:
  - `apps/study-client/src/app/features/mentor/ME11/` (`models/`, `data-access/`, `ui/`, `pages/` + `me11-page.spec.ts`)
  - `apps/study-client/src/app/features/mentor/ME12/` (`models/`, `data-access/`, `ui/`, `pages/` + `me12-page.spec.ts`)
  - `apps/study-client/src/app/features/mentor/mentor.route.ts`
  - `apps/study-client/src/app/app.routes.spec.ts`
  - `apps/study-client/gui/architech.md`
  - `.agents/worklog/2026-11-12/implement-mentor-phase3-me11-me12.md`
- CONTEXT_UPDATES: Cập nhật `apps/study-client/gui/architech.md` bổ sung `ME11` và `ME12`.
- Context pages changed: `apps/study-client/gui/architech.md`, worklog này.
- Assumptions: Giữ nguyên quy tắc 4 thư mục con trực tiếp (`data-access/`, `models/`, `pages/`, `ui/`) và không import chéo giữa `ME11` và `ME12`.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type coding --limit 3` | Exit 0 (`READY`, 3 coding worklogs reviewed) | `VERIFIED` |
| `npm run build` | `ng build` thành công (`mentor-route` 163.71 kB, không warning/error) | `VERIFIED` |
| `npm test -- --watch=false` | 9/9 test files passed, 31/31 tests passed | `VERIFIED` |
| `git diff --check apps/study-client` | Exit 0 | `VERIFIED` |

## HANDOFF

- Remaining blockers: None (`Phase 3` đã `VERIFIED` 100%).
- Next owner/action: Người dùng xem báo cáo Phase 3 và xác nhận chuyển sang Phase 4 (`ME-16`, `ME-17`, `ME-18`).
