# ST-09 — Kế hoạch chi tiết

> Ngày rà soát gần nhất: 2026-11-07 (kế hoạch gốc 2026-11-06)
> Trạng thái: PLAN COMPLETE; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED

## 1. Phạm vi và phân loại

```text
primary_task_type: docs
secondary_task_types: []
project_scopes: [web-work, server-study]
cross_scope_dependencies: [ST-08 enrollment handoff/API #20; ST-09 APIs #09/#37; ST-10 access/start APIs #22/#23/#24; ST-21 progress detail; Study Web built artifact/source boundary]
```

- Phiên này chỉ xử lý **ST-09 — Tổng quan khóa đang học (Page)**; không bắt đầu ST-10 hoặc ST-21.
- Inventory: route đề xuất `/student/courses/:courseId`; actor Student; AC-13/AC-18; APIs #09/#20/#37; liên kết ST-10 và ST-21. Expected content là đề cương + tiến độ từng bài và CTA tiếp tục học.
- Inventory orchestration: xác nhận course thuộc danh sách #20; gọi #37; dùng #09 chỉ cho curriculum public; phải kiểm tra lesson access bằng #22 trước khi vào flow học. F04 nhắc không dùng public curriculum thay permission-based learning tree.
- Skill registry/manifest: `createDD-markdown` áp cho Web/API DD và exclude `web-ui-only-dd`; không có skill canonical cho UI-only screen DD. Không áp API DD template cho ST-09.

## 2. Asset baseline và annotation

- Thư mục ban đầu chỉ có `screen.png` và `code.html`; chưa có ST-09 plan, DD, marker map hoặc ảnh chú thích.
- `screen.png` là PNG đầy đủ, đọc được, kích thước 1397×1600, SHA-256 `8b37e1c7dc459ab7a9ab87161f0990d259abf9291c7f3a85b4a05c3324ba7a7d`. Giữ nguyên làm ảnh nguồn và dùng trực tiếp làm nền `screen_annotated.png`; không cần tạo HTML render thay thế.
- `code.html` SHA-256 `554e2fdc52b3fe01cbaf560f7525dca1742a0413b889882569c3d865a699bc46`. Nội dung/các vùng hiển thị khớp với screenshot. HTML là mockup tĩnh: links dùng `href="#"`, `data-path` là hint, không có router/data fetch; nút Sao chép Route có inline `navigator.clipboard.writeText('/student/courses/:courseId')`.
- Marker dự kiến: (1) brand header, (2) primary navigation, (3) profile/role icon-group, (4) screen/route/gated badges, (5) title + subtitle, (6) API state panel, (7) warning pill, (8) gated heading, (9) explanatory copy, (10) mandatory policy notice, (11) return-to-ST-08 link, (12) ST-10 access CTA, (13) handoff section title/version, (14) Gatekeeper card, (15) Tokens card, (16) WCAG card, (17) frontend integration note, (18) copy-route button, (19) footer copyright/WCAG badge, (20) footer navigation group.
- Screen ghi API #09/#20/#37 ở trạng thái D/DESIGN_ONLY. Đối chiếu source: #09 có route/module/view/query/test; #20/#37 chỉ có catalog/API DD Draft, không có route/module/test. Giữ nguyên ảnh nhưng ghi `DISCREPANCY` trong DD.

## 3. Expected behavior và current evidence

| Chủ đề | Expected/design source | Current evidence | Tác động |
|---|---|---|---|
| Actor/route | Student; route đề xuất `/student/courses/:courseId`; ST-08 chọn khóa để vào. | Không có source route ST-09 trong client; ảnh/HTML không bind path param. | Không khẳng định route guard, `courseId` parsing hoặc session handoff đang chạy. |
| Enrollment gate | Inventory yêu cầu xác nhận course thuộc #20 trước khi nạp tree; API #20 catalog yêu cầu Bearer JWT/Student. | #20 không có route/module/query/test trong Study Server; catalog response `ApiEnvelope<UserProfile>` không xác định membership. | Không thể mở gate hoặc định nghĩa enrolled/pending/not-enrolled mapping. |
| Progress | API #37 và AC-18 dự kiến progress theo lesson + quiz + assignment. | #37 chỉ có catalog và DD Draft; không có route/module/test; response vẫn `ApiEnvelope<UserProfile>`. Công thức, selection và empty shape là open questions. | Không render phần trăm/trạng thái tiến độ như dữ liệu backend đã xác minh. |
| Curriculum/access | #09 public curriculum; #22 trước khi học. | #09 current source trả published lessons cùng `content` và `video_url`, không auth/enrollment gate; #22/#23/#24 không có current route/module/test source. | #09 không chứng minh entitlement; không dùng public projection để mở media/lesson. Backend projection/access cần quyết định. |
| Static gated screen | Inventory states enrolled/not-enrolled/loading/no-lessons. | PNG/HTML chỉ có gated/unavailable view với copy tĩnh; không fetch/API state. | Gated mockup là source state hiện thấy, không chứng minh server gate. |
| Navigation | Return ST-08; continue to ST-10; header/footer navigation. | Main links và header/footer links đều `href="#"`; header có `data-path`; ST-10 CTA không có lessonId. | Route destinations/return context/lesson selection chưa wired hoặc đủ dữ liệu. |
| Built client artifact | Study Web screen route phải nối auth/API. | `apps/study-client/dist` có ignored compiled build artifact với một route duy nhất `/` (home); không có `/student/courses`, `/student/progress`, #20/#37 URLs. Không có editable app source/package manifest. | Dist không cung cấp ST-09 implementation; serving/deployment chưa xác minh. Context pages đã được cập nhật để phân biệt build artifact với source/runtime. |

## 4. Planned event coverage

- ST09-EV-01 route entry `/student/courses/:courseId` và parse/khởi tạo context (expected; không có client router).
- ST09-EV-02 xác thực enrollment qua API #20 trước khi mở nội dung (expected; #20 NOT_FOUND và response mismatch).
- ST09-EV-03 tải progress API #37 sau membership gate (expected; #37 NOT_FOUND/schema/formula chưa chốt).
- ST09-EV-04 tải curriculum qua #09 như public outline; không dùng response để xác minh quyền học (API source-backed nhưng content/video_url projection tạo security/design blocker).
- ST09-EV-05 nút quay về ST-08.
- ST09-EV-06 CTA kiểm tra quyền học sang ST-10 (lessonId/route/API #22–#24 chưa có).
- ST09-EV-07 primary header navigation; current href là placeholder.
- ST09-EV-08 footer navigation/legal/help; current href là placeholder.
- ST09-EV-09 “Sao chép Route”; inline clipboard call tồn tại trong HTML, không có feedback/error state.
- ST09-EV-10 mở chi tiết tiến độ ST-21 theo courseId là liên kết inventory; không có link/control trong PNG/HTML.
- Static text, badges, icons, handoff spec cards, token rows, WCAG claims and integration notice không tự có event.

## 5. Planned source trace

- Recheck ST-09 inventory row, F04, AC-13/AC-18 index and Student Learning diagrams; inspect `list_api.md` #09/#20/#37 and API #09/#37 DD status/open questions.
- Trace current API #09 route → validator → published-course query → published-lesson query → `LessonPage` envelope → existing test source. Read tests but do not run them.
- Recheck #20/#37 and #22–#24 route/module/query/test sources; classify declared contracts separately from current source.
- Inspect candidate DDL fields for enrollments, lessons, lesson_progress, quiz_attempts and assignment_submissions without deriving aggregation or live schema.
- Compare PNG/HTML; inspect current `apps/study-client/dist` only as built artifact evidence, not editable source or deployment proof.
- Trace ST-08, ST-10, ST-21 and nav destinations from inventory; keep session, route and lesson ID handoff unresolved where source is absent.
- No tests are requested; do not run test suites.

## 6. Outputs, acceptance and blockers

- Done: `ST-09.md`, `ST-09_markers.json`, `ST-09_markers_overlay.svg`, and `screen_annotated.png` created after this plan. Original `screen.png` and `code.html` hashes are preserved.
- DD covers 20 visible element groups, 10 identified events, current/expected flow, #09/#20/#37 contracts and source state, state/navigation/access matrix, privacy/security, design/accessibility discrepancies, blockers and checklist.
- Done: context pages describe the ignored compiled root-only `dist` artifact separately from absent editable source while retaining Study Web `UNWIRED` for feature routes. The required context validator was run; it exits 1 on existing broad context/source-inventory failures outside ST-09.
- Done: global tracker now records separate DD/implementation/runtime statuses; counts are 18 complete bundles and 65 incomplete, with ST-10 as next W1 pointer. Static audit passed; the context validator was run and reports unrelated repository-wide failures. Do not start ST-10 this session.
- DD is expected to remain BLOCKED: #20/#37 and #22–#24 are not source-backed; #09 is public and currently returns content/video_url without entitlement checks; progress/list schemas and lesson tree/access semantics are unresolved; Study Web has no ST-09 route source.


## 7. Execution state

- Outputs created: `ST-09.md`, marker JSON, marker overlay SVG, annotated PNG; original PNG and HTML untouched.
- Global tracker updated for ST-09 and next pointer ST-10.
- Re-audit 2026-11-07: PASS. Source PNG/HTML hashes and dimensions, embedded SVG image, marker sequence/IDs/circles/labels/path endpoints, one-to-one DD rows, 10 event IDs, local Markdown links, A–F headings, and 83 inventory IDs/folders with 82/83 complete core bundles were checked. `git diff --check` is clean for changed tracked files; changed DD/plan/worklog have no trailing whitespace. The four trailing-whitespace lines at the start of `list_screen.md` are pre-existing and outside changed hunks. The context validator previously failed on repository-wide issues unrelated to ST-09.
- Final status remains DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED.

## 8. Re-audit and correction log (2026-11-07)

This re-audit is recorded before editing the marker map, screen DD, or shared screen trackers. It keeps the original 2026-11-06 plan and results as history.

### Source and contract findings

- Inventory row 23 still defines `/student/courses/:courseId`, AC-13/AC-18, APIs #09/#20/#37, and links to ST-10/ST-21. F04 explicitly prohibits using public #09 curriculum as the permission-based learning tree.
- AC-13's API index says `Student` is authenticated and may have an enrollment; #20 loads Enrollment + Course and #21 loads progress, but both are design-only and their `ApiEnvelope<UserProfile>` catalog shape does not describe those outputs. ST-08 has no loaded course card or source-backed `courseId` handoff in the current worktree.
- AC-18's diagram says aggregate lesson + quiz + assignment progress and renders dashboard progress/achievements. It does not define the formula, attempt/submission selection, empty result, or partial semantics. API #37 remains Draft; no current route/module/query/test was found.
- API #09 is registered in `app/api/v1.py`, included by `app/main.py`, and has current view/query/validator/model plus focused test source. It is public and has no JWT/enrollment check; it checks a PUBLISHED course, returns PUBLISHED lessons ordered by `sort_order`, then `id`, and exposes nullable `content` and `video_url`. Empty curriculum returns 200; invalid/non-integer ID, missing or unpublished course returns 404; SQL/mapping failure returns 500. The validator parses an integer but does not explicitly enforce the contract's signed-int64 range. Tests were read only, not run.
- API #22–#24 route/module/test sources remain NOT_FOUND. Their access/start/content flow and response/error behavior remain design-only.
- Study Web has no editable app/router/package source in the current file inventory. `dist/` is git-ignored; its provenance and serving/deployment status are unknown. This does not establish a running ST-09 route.

### Asset findings and edits planned

- `screen.png` remains 1397×1600 with SHA-256 `8b37e1c7dc459ab7a9ab87161f0990d259abf9291c7f3a85b4a05c3324ba7a7d`; `code.html` remains SHA-256 `554e2fdc52b3fe01cbaf560f7525dca1742a0413b889882569c3d865a699bc46`. Preserve both.
- The annotated image and SVG show 20 sequential markers; the SVG path endpoints follow each element row, including displaced markers #3, #5 and #16. The JSON repeats `(2874,3110)` for every `leader_to_canvas_px`, which fails to describe those paths. Update each endpoint to the SVG image-edge endpoint: x=80 for left markers or x=2874 for right markers, y=2× the source target's y coordinate. Keep the annotation geometry and source image unchanged.
- Correct `list_screen.md` reverse API index row #009 from source D to R because the local route/view/query/validator/model/test source is registered. Keep the ST-09 screen's own D status: its client flow remains unwired. Keep API #09 DD Draft status distinct from local source presence.
- Update ST-09 DD to capture the #09 catalog/source status discrepancy and the absent explicit int64 range check. Make the required A–F headings explicit while retaining the current evidence content. Preserve all #20/#37/#22–#24 and UI design blockers; DD remains BLOCKED, implementation BLOCKED, runtime NOT VERIFIED.
- Then run static checks for marker sequence/IDs/coordinates and SVG path alignment, 1:1 DD element rows, dimensions/hashes, local Markdown links, relevant tracker rows and whitespace. Do not run application tests or continue to ST-10.

### Completed changes and final audit

- Corrected all 20 `leader_to_canvas_px` entries to match the existing SVG endpoints; no source image, SVG path, or annotated PNG was rewritten. The source PNG embedded in the SVG hashes identically to `screen.png`.
- Updated the shared API reverse index's #009 source label from D to R. The ST-09 screen row remains D because its frontend route is unwired; API #09's DD remains Draft. Updated the ST-09 tracker/DD with the current-source discrepancy and missing int64-bound check.
- Changed the central DD headings to explicitly identify A–F. Added the current #09 response envelope and Draft-example `data={}` versus source `data=null` discrepancy. The #09 endpoint remains public and unsuitable as proof of enrollment or lesson access.
- Final static audit passed: 20 sequential marker records/circles/labels/paths align with 20 DD element rows; 10 expected events are present; all local DD/plan links resolve; image hashes/dimensions and SVG embedding match; 83 IDs match 83 folders; 82/83 core bundles are complete, with ST-01 incomplete. `git diff --check` exited 0 on changed tracked files. No app tests/runtime or live database/deployment checks were run.
