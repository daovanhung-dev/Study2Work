---
task_id: "2026-11-12-implement-mentor-phase1-me06-me08"
date: "2026-11-12"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["web-work (Study Web)"]
cross_scope_dependencies: ["apps/study-server/app/modules/mentor/api_49..53"]
status: "VERIFIED"
---

# Worklog: Triển khai Study Web Mentor Phase 1 (ME-06, ME-07, ME-08)

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `Get-ChildItem .agents/worklog -Recurse -Filter *.md | Select-String -Pattern 'primary_task_type:\s*"?coding"?'` (fallback vì `node` không có trong PATH trên máy)
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-12/admin-system-route-wiring.md`
    - carry_forward: `App` chỉ render `RouterOutlet`; route group dùng layout riêng có `RouterOutlet`; giữ rõ ranh giới unguarded route và trạng thái API/auth.
  - path: `.agents/worklog/2026-11-12/ad01-screen-coding.md`
    - carry_forward: Mỗi screen có đúng 4 thư mục trực tiếp (`data-access/`, `models/`, `pages/`, `ui/`); chia nhỏ style theo component con để tránh vượt 4kB/8kB CSS budget của Angular; không bịa dữ liệu/claim chưa có contract.
  - path: `.agents/worklog/2026-11-11/study-client-context-load.md`
    - carry_forward: Dùng `StudyApiService` (`/api/v1`) trả `ApiEnvelope<T>`; đối chiếu trực tiếp Study Server source vì Study OpenAPI đang `NOT_FOUND`.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Thực hiện Phase 1 của kế hoạch Mentor (`ME-06`, `ME-07`, `ME-08` kèm khung `MentorLayout` và `mentor.route.ts`) theo 5 lựa chọn đã duyệt:
  1. `PA1`: Xây dựng UI + Route + Layout + State + Unit test chuẩn `AD01`, đồng thời nối `models/` và `data-access/` khớp với `apps/study-server/app/modules/mentor/api_49..53`. Phần nào API chưa có thì giữ `disabled` + ghi chú rõ và tổng hợp báo lại.
  2. Thứ tự: Phase 1 (`ME-06` → `ME-07` → `ME-08`).
  3. Tên file route: `src/app/features/mentor/mentor.route.ts`.
  4. `ME-08`: Hỗ trợ cả route riêng `/mentor/content/:contentId/actions` và chế độ mở dialog/panel (`?dialog=1`) từ `ME-06` qua query/router mà không import chéo giữa screen.
- Study FE scope: `screens=ME-06, ME-07, ME-08; APIs=#49, #50, #51, #52, #53`
- Canonical contract/approved DD:
  - `apps/study-client/docs/dd_screens/ME-06-CayNoiDungKhoaHoc/00-overview.md`..`07-test-cases.md`
  - `apps/study-client/docs/dd_screens/ME-07-TaoChinhSuaNoiDung/00-overview.md`..`07-test-cases.md`
  - `apps/study-client/docs/dd_screens/ME-08-XuatBanXoaNoiDung/00-overview.md`..`07-test-cases.md`
  - `apps/study-server/app/modules/mentor/api_49_mentor_content_list`..`api_53_mentor_content_delete`

## MILESTONES

| Weight | Cumulative progress when achieved | Objective / acceptance criterion | Status |
|---:|---:|---|---|
| `15%` | `15%` | Preflight 3 worklogs `coding`, đọc `models.py`/`validate.py`/`view.py` của `#49–#53` và khởi tạo worklog | `DONE` |
| `15%` | `30%` | Tạo `MentorLayout`, `mentor.route.ts` và đăng ký `/mentor` trong `app.routes.ts` | `DONE` |
| `25%` | `55%` | Triển khai `ME-06` (`models/`, `data-access/`, `ui/`, `pages/` + `me06-page.spec.ts`) | `DONE` |
| `25%` | `80%` | Triển khai `ME-07` (`models/`, `data-access/`, `ui/`, `pages/` + `me07-page.spec.ts`) | `DONE` |
| `20%` | `100%` | Triển khai `ME-08` (`models/`, `data-access/`, `ui/`, `pages/` + `me08-page.spec.ts`), cập nhật `architech.md`/context và báo cáo chi tiết các API/field chưa có | `DONE` |

## CURRENT_BEHAVIOR

- Source/config: `MentorLayout` và `mentor.route.ts` đã được đăng ký dưới `/mentor` trong `app.routes.ts`. Ba màn `ME-06`, `ME-07`, `ME-08` đều có đúng 4 thư mục con trực tiếp (`data-access/`, `models/`, `pages/`, `ui/`) và không import chéo lẫn nhau.
- Runnable tests: Đã viết và chạy pass 100% `me06-page.spec.ts` (4 tests), `me07-page.spec.ts` (3 tests), `me08-page.spec.ts` (3 tests), `app.routes.spec.ts` (4 tests), `ad01-page.spec.ts` (3 tests) — tổng cộng 5/5 test files, 17/17 tests passed; `npm run build` hoàn tất sạch (chunk `mentor-route` 72.29 kB).
- Runtime wiring: Các service `Me06ContentService`, `Me07EditorService`, `Me08ActionsService` gọi `StudyApiService` tương ứng với các route `#49`, `#50`, `#51`, `#52`, `#53` đã có trong `apps/study-server/app/api/v1.py`.

## SOURCE_TRACE

```text
ME06Page -> Me06ContentService.getCourseContents(courseId) -> StudyApiService -> GET /api/v1/mentor/courses/{course_id}/content (#49) -> ApiEnvelope<ContentNodeDto[]>
ME07Page -> Me07EditorService.getCourseContents (#49) + createContent (POST /api/v1/mentor/content #50) / updateContent (PUT /api/v1/mentor/content/{content_id} #51)
ME08Page -> Me08ActionsService.getCourseContents (#49) + setPublishState (PATCH /api/v1/mentor/content/{content_id}/publish #52) / deleteContent (DELETE /api/v1/mentor/content/{content_id} #53)
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Tạo node con (`parent_id`) và cập nhật thứ tự (`order`) trong `#50`/`#51` | `CreateContentRequest` (`#50`) chỉ nhận `{course_id, content_type, title, payload}` và luôn tạo root node (`parent_id=None`, `status='PENDING_REVIEW'`); `UpdateContentRequest` (`#51`) chỉ nhận `{content_type, title, payload}` | `DISCREPANCY` | Trên UI `ME-06`/`ME-07`, hiển thị rõ `parent_id`/`order` ở chế độ chỉ đọc và khóa nút "Lưu thứ tự sắp xếp" |
| Trạng thái sau khi tạo/sửa (`#50`, `#51`) và điều kiện publish (`#52`) | `#50` và `#51` luôn đặt `status = 'PENDING_REVIEW'`; `#52` chỉ cho phép `APPROVED -> PUBLISHED` (khi `published=true`) hoặc `PUBLISHED -> APPROVED` (khi `published=false`), nếu đang `DRAFT`/`PENDING_REVIEW` sẽ trả `422` | `DISCREPANCY` | Trên `ME-06` và `ME-08`, hiển thị rõ trạng thái `PENDING_REVIEW`/`APPROVED`/`PUBLISHED`/`DRAFT` và cảnh báo điều kiện `APPROVED` trước khi publish |
| Điều kiện xóa nội dung (`#53`) | `#53` từ chối xóa (`422`) nếu `status == 'PUBLISHED'` hoặc còn node con trực tiếp đang active (`has_active_child == true`) | `VERIFIED` | Trên `ME-08`, kiểm tra `canDelete` và hiển thị cảnh báo rõ ràng cho người dùng trước khi bấm Xóa |

## CHANGES

- Files changed:
  - `apps/study-client/src/app/layouts/mentor/mentor-layout.html`, `mentor-layout.ts`
  - `apps/study-client/src/app/features/mentor/mentor.route.ts` (và xóa `.gitkeep`)
  - `apps/study-client/src/app/features/mentor/ME06/` (`models/`, `data-access/`, `ui/`, `pages/`)
  - `apps/study-client/src/app/features/mentor/ME07/` (`models/`, `data-access/`, `ui/`, `pages/`)
  - `apps/study-client/src/app/features/mentor/ME08/` (`models/`, `data-access/`, `ui/`, `pages/`)
  - `apps/study-client/src/app/app.routes.ts`, `app.routes.spec.ts`
  - `apps/study-client/gui/architech.md`
  - `.agents/worklog/2026-11-12/implement-mentor-phase1-me06-me08.md`
- CONTEXT_UPDATES: Cập nhật `apps/study-client/gui/architech.md` bổ sung `layouts/mentor` và `features/mentor/{mentor.route.ts, ME06, ME07, ME08}`.
- Context pages changed: `apps/study-client/gui/architech.md`, worklog này.
- Assumptions: Giữ nguyên quy tắc 4 thư mục mỗi screen; không import chéo giữa `ME06`, `ME07`, `ME08`.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| Preflight worklog & trace `api_49..53` | Đã đọc 3 worklog `coding` và toàn bộ `models.py`, `validate.py`, `view.py` của `#49–#53` | `VERIFIED` |
| `git diff --check apps/study-client` | Exit 0; không có lỗi whitespace, mọi file `.css` đều < 3 kB (dưới ngưỡng 4 kB budget) | `VERIFIED` |
| `npm run build` | `ng build` thành công (lazy chunk `mentor-route` 72.29 kB, không warning/error) | `VERIFIED` |
| `npm test -- --watch=false` | 5/5 test files passed, 17/17 tests passed (`ad01`, `me06`, `me07`, `me08`, `app.routes`) | `VERIFIED` |

## HANDOFF

- Remaining blockers: None (`Phase 1` đã `VERIFIED` 100%).
- Next owner/action: Chạy `npm start` để xem trực quan hoặc chuyển sang Phase 2 (`ME-09`, `ME-10`).
