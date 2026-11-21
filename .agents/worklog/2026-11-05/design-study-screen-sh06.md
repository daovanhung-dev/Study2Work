---
task_id: "2026-11-05-design-study-screen-sh06"
date: "2026-11-05"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["SH-06 not-found state -> API #08 public course detail / published-course query"]
status: "VERIFIED"
---

# Worklog: Thiết kế màn hình Study SH-06 Not Found

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 worklogs được chọn trong 151 log `docs` khả dụng.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-05/check-study-screen-stitch-coverage.md`
    - carry_forward: Inventory có 83 ID; screen assets là design artifact, không chứng minh UI runtime. Kiểm kê mới nhất trong phiên trước đã có 83 thư mục khớp inventory.
  - path: `.agents/worklog/2026-11-05/co-locate-study-screen-documents.md`
    - carry_forward: Tài liệu từng màn hình đặt cạnh ảnh nguồn; ảnh nguồn phải giữ nguyên; phiên trước báo SH-05 là bước kế.
  - path: `.agents/worklog/2026-11-05/complete-study-screen-docs.md`
    - carry_forward: SH-05 đã có `DD READY` + `IMPLEMENTATION BLOCKED` + `RUNTIME NOT VERIFIED`; tracker ghi SH-06 kế tiếp. Worklog cũ chưa có findings SH-06.
- shortage: `none` (đã đọc đủ 3 worklog được chọn)

## EXPECTED_BEHAVIOR

- Requirement: Objective file yêu cầu 83 màn hình, một Screen ID mỗi phiên, kế hoạch trước, DD/ảnh chú thích/marker map, truy vết nguồn, cập nhật tổng kế hoạch và phân biệt các trạng thái. Phiên này chỉ xử lý SH-06.
- Canonical contract/approved DD: `apps/study-client/docs/list_screen.md` §2.1 mô tả `/not-found`, API #08, route-404/resource-404, không tiết lộ draft/private, link GS-01/SH-01 và không đổi 500 thành 404. `docs/lists/list_api.md` và AC diagrams là design contract; Study Server current source sở hữu hiện trạng.

## CURRENT_BEHAVIOR

- Source/config: `screen.png` 1600×1425 và `code.html` tồn tại; SH-06_PLAN/DD/markers/annotated image chưa có lúc preflight. `apps/study-client/src/` và `apps/study-client/package.json` vắng mặt. Có `dist/` build artifact; bundle scan không thấy `/not-found`, `/courses`, `/login`, `404`, `createRouter` hoặc `createWebHistory`; không thể xác nhận nó là SH-06 runtime hay tái dựng source từ đó. HTML prototype có các route anchor `href="#"`, 3 khóa học/learner counts hard-coded, footer links và contact link chưa có đích.
- API #08 current source: `GET /api/v1/courses/{course_id}` được đăng ký trong `apps/study-server/app/api/v1.py`, gọi `api_08_courses_detail.get_course_detail`; validator parse integer, invalid path trả 404 `DESIGN_RESOURCE_NOT_FOUND`; query chỉ tìm `courses.status='PUBLISHED'`; missing hoặc unpublished trả cùng 404 message; DB/mapping error rollback khi SQL lỗi và trả 500 `DESIGN_INTERNAL_ERROR`. Thành công là `Page<Course>` singleton (items + pagination), không phải object đơn. Test source tồn tại, chưa chạy.
- Runnable tests: Không chạy; người dùng không yêu cầu test. Đã đọc `test_courses_detail.py` cho 404/500/200 branches.
- Runtime wiring: Study Web source/router không có trong checkout. Server API route/module/test có source; route được đánh dấu `D` trong API catalog/list_screen, tạo `DISCREPANCY`. Có dist artifact nhưng không có bằng chứng route/SH-06 wiring.

## SOURCE_TRACE

```text
SH-06 screen.png/code.html + list_screen row/F02 -> API #08 route -> get_course_detail -> validate_course_id -> FIND_PUBLISHED_COURSE_DETAIL (courses.status=PUBLISHED, mentor join) -> CoursePage/safe 404/500 -> test source -> DD and route/state plan
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #08 availability | API catalog and inventory label #08 `D`, but current route/module/query/tests exist and route is registered. | `DISCREPANCY: DESIGN_D VS SOURCE_BACKED` | Use current source for actual status mapping; do not mark runtime verified from source/tests. |
| AC-05 403 branch | AC guest diagram mentions 404/403 for a course not published; current public #08 source returns 404 for invalid/missing/unpublished course and no #08 403 branch. | `DISCREPANCY` | Map current API 404 to SH-06; keep 403 separate (SH-05/access denial) and do not invent 403 source behavior. |
| Course cards/contact/footer | `code.html` includes fixed mock course values, `href="#"`, and support/footer targets without route/API evidence in SH-06 inventory. | `DESIGN_ONLY / UNWIRED` | Do not expose hard-coded business data or invent route/support services; record approval/source blocker. |
| Study Web current source | `src/` and package manifest absent; dist artifact has no route strings for SH-06 or navigation; no runtime connection confirmed. | `NOT_FOUND / DESIGN_ONLY` | Mark implementation blocked and runtime unverified. |

## CHANGES

- Files changed: `apps/study-client/docs/screen_stitch/01_shared_auth_system/SH-06_trang-khong-ton-tai-tai-nguyen-khong-con/SH-06_PLAN.md`; `.../SH-06.md`; `.../SH-06_markers.json`; `.../screen_annotated.png`; `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`; `.agents/worklog/2026-11-05/design-study-screen-sh06.md`; `.agents/worklog/2026-11-05/complete-study-screen-docs.md`.
- CONTEXT_UPDATES: None planned; no runtime contract/schema change.
- Context pages changed: None.
- Assumptions: Do not infer course recommendation source from the prototype. API #06 is an existing public list route but is not a declared SH-06 dependency; reuse requires product/UX approval. Keep a distinction between direct route-not-found and API #08 resource-not-found.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type docs --limit 3` and read all selected files | Selected/read 3 exact-type worklogs; no shortage. | VERIFIED |
| Static inventory/source read | SH-06 source PNG/HTML present, missing per-screen outputs; `src/` and package manifest absent; dist bundle is present but no route identifiers found. | VERIFIED_STATIC_ONLY |
| API #08 code and test source read | Route, validation, query, mapping, status/error branches and test coverage inspected; tests not run. | VERIFIED_STATIC_ONLY |
| Static audit over `list_screen.md`, `screen_stitch/`, and tracker | 83 inventory IDs = 83 folders = 83 tracker rows; 6 full asset sets after SH-06. | VERIFIED_STATIC_ONLY |
| Marker/element/event/link check | 22 ordered, unique markers map to 22 DD element IDs; 10 events; all local Markdown links in SH-06 DD/plan resolve. | VERIFIED_STATIC_ONLY |
| Source preservation + image dimensions | `screen.png` SHA-256 `b6a423005ea008e9f00de6f2328f182c6256e7ae647575f55dfa8c4ae05ecf0a`; `code.html` SHA-256 `ce3c9bff0e9d24630172230f2b28e3a533ad4e2be1daecfe71f3bf1db4649ce7`; source/annotated both 1600×1425; overlay reviewed visually. | VERIFIED |
| `git diff --check` + changed-doc whitespace audit | No whitespace errors. | VERIFIED |
| Inline Python static audit + `git diff --check` after worklog updates | 83 IDs match across inventory/tracker/folders; 6 complete sets and 77 remaining; 22 ordered markers map to 22 DD elements; 10 events; local links resolve; source hashes preserved; both images 1600×1425; whitespace clean. | VERIFIED_STATIC_ONLY |
| Tests/runtime | Not run. | NOT_RUN |

## HANDOFF

- Remaining blockers: Study Web route/client absent; recommendation cards and support/footer destinations have no confirmed data/route contract; API #08 is source-backed but still classified design-only in catalog; AC-05 diagram includes 403 where current #08 source does not. `DD READY`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`.
- Next owner/action: SH-06 artifacts and tracker are complete. Continue with SH-07 in a separate Screen ID session; create `SH-07_PLAN.md` before its DD/image work.

