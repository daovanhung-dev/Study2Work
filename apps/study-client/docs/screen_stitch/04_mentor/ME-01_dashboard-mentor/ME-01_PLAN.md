# ME-01_PLAN — Dashboard mentor

> Trạng thái: PLAN COMPLETE; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED

## 1. Phạm vi và phân loại

- Phiên này chỉ xử lý **ME-01 — Dashboard mentor**; không bắt đầu Screen ID khác.
- `primary_task_type: docs`; `secondary_task_types: [test]` (kiểm tra tĩnh artifact); `project_scopes: [web-work, server-study]`.
- Cross-scope dependency: Study Web dashboard dự kiến gọi Study Server API #46/#54/#58; mỗi API yêu cầu access JWT role `MENTOR`. Study Web source/router/package không có trong checkout hiện tại.
- Danh mục chuẩn: [`list_screen.md` dòng ME-01](../../../list_screen.md) — route đề xuất `/mentor`, AC-21/23/24, API #46/#54/#58, links ME-02/ME-09/ME-11, states loading/partial/empty/error. Route không xác nhận runtime.
- Skill registry xác nhận `createDD-markdown` loại trừ `web-ui-only-dd`; UI-only DD chưa có skill canonical. Không áp dụng API-DD template cho screen DD.

## 2. Kế hoạch rà soát tài sản

- `screen.png`: PNG hợp lệ 1086×1600, RGB; SHA-256 `f135d0b109a05d276654a6b8b51545d9f2996ab474c47b7829c9983739eea3d2`.
- `code.html`: HTML tĩnh 52,234 bytes; SHA-256 `f10dfa929e89288165bf0264b1b1f863f2380006d064f8e470118a7cfe626334`.
- PNG và HTML thể hiện cùng dashboard nhiều cột: header mentor, welcome/on-call, bốn KPI, danh sách bài nộp, khóa học, hỗ trợ, lịch 1-on-1, thông báo học vụ và footer. Các tên, điểm số, số lượng, SLA, lịch hẹn, đường dẫn Meet và thông báo là dữ liệu minh họa trong asset, không phải dữ liệu runtime.
- HTML dùng anchor `href="#"`, có input tìm kiếm và button tĩnh nhưng không có client handler/API/router. Tất cả placeholder destinations, số liệu minh họa, external font/CDN và màu xanh `#004ac6` cần đối chiếu với source/Study Web design guide; không sửa PNG/HTML.
- PNG hiện dùng được; không cần dựng `screen_rendered.png`. Dùng PNG nguyên trạng làm nền chú thích.

## 3. Expected behavior cần đối chiếu

1. Mentor đã đăng nhập; danh mục yêu cầu role Mentor và cho phép dashboard nạp widgets độc lập.
2. API #46 lấy các khóa học Mentor sở hữu; #54 lấy danh sách submissions; #58 lấy support requests. Links theo inventory: ME-02, ME-09, ME-11.
3. AC-21 mô tả tạo lecture; AC-23 mô tả mở danh sách submissions rồi chọn một submission; AC-24 mô tả mở support requests rồi mở thread. Chúng không đặc tả chính dashboard, cũng không quyết định các CTA direct-to-detail trong mockup.
4. Screenshot thể hiện thêm rating, active learner, deadline/SLA, số course progress, lịch mentoring, announcements, notification badge và Mentor profile. Không có API tương ứng nào được ME-01/list_screen chỉ định; các phần này không được mô tả như dữ liệu hoạt động.

## 4. Current behavior/source trace cần giữ trong DD

| API | Current source | Input / authorization | Response / source boundary |
|---|---|---|---|
| #46 | Route `GET /api/v1/mentor/courses` → `api_46_mentor_courses.view.get_mentor_courses` → count/list SQL `courses` LEFT JOIN `users` → shared course mapper. | Bearer JWT; `sub` số; role `MENTOR`; optional `status` (`DRAFT`/`PUBLISHED`), `page` mặc định 1, `size` mặc định 20, giới hạn 1–100. Query trực tiếp theo `courses.mentor_id`. | `200 DESIGN_RESOURCE_RETRIEVED`, `data.items` + `pagination`; Course fields `id/title/description/thumbnail_url/price/status/mentor{id/full_name/avatar_url?}`. Không có enrollment count/progress/rating. Empty/out-of-range page vẫn 200. |
| #54 | Route `GET /api/v1/mentor/submissions` → `api_54_mentor_submissions_list.view.get_mentor_submissions` → count/list SQL qua `assignment_submissions → assignments → courses → users`, tùy chọn map UploadAsset. | Bearer JWT role `MENTOR`; optional `course_id`, exact `status`, `page` mặc định 1; page size cố định 20; owner scope `courses.mentor_id`. `status` không có enum validation. | `200 DESIGN_RESOURCE_RETRIEVED`, `data.items` + pagination. Fields `id/assignment_id/user_id/content/files/status/submitted_at/score/feedback`; không có Student name/avatar, assignment/course title, deadline, rubric hoặc trạng thái “chưa chấm” đã chuẩn hóa. Candidate assignment/upload projection và live schema chưa xác minh. |
| #58 | Route `GET /api/v1/mentor/support/requests` → `api_58_mentor_support_requests.view.get_mentor_support_requests` → list request rồi list toàn bộ message/asset trong cùng scope. | Bearer JWT role `MENTOR`; optional `course_id`, exact `status`; không pagination. Owner scope lặp lại trong request/thread query. | `200 DESIGN_RESOURCE_RETRIEVED`, `data` là array `SupportRequest` gồm student, lifecycle, messages và attachments. Không có subject, unread count, SLA, course title hay pagination. Collection/thread schema là derived fallback từ checked-in migration 008; live schema chưa xác minh. |

- Cả ba guard trả 401 `DESIGN_AUTHENTICATION_REQUIRED` khi Bearer/JWT/claims không hợp lệ; role khác trả 403 `DESIGN_ACCESS_DENIED`. Validation/query lỗi trả 422 khi áp dụng; DB/projection lỗi trả safe 500 `DESIGN_INTERNAL_ERROR`. No live deployment/database claim.
- `apps/study-client/` hiện có `docs`, `dist` và `tsconfig.tsbuildinfo`; không có `src/` hoặc `package.json`. Study context ghi dist chỉ có compiled root `/`; recheck dist trước khi viết DD. Không suy ra client event, session handling, widget concurrency hay routing.
- API #46/#54/#58 có route/module/test source hiện tại dù `list_screen.md` và API DD snapshots còn nhãn design-only/Draft. Test source được đọc, không chạy; `RUNTIME VERIFIED` không được đặt.

## 5. Element/marker plan

Tạo 23 marker theo thứ tự từ trên xuống. Một marker có thể đại diện cho component lặp; mỗi link/control con được liệt kê riêng trong DD element/event. Footer được gom thành một vùng; marker tọa độ tính bằng pixel trên PNG nguồn 1086×1600, gốc trên-trái:

1. Brand/mentor portal; 2. primary navigation; 3. global search; 4. notification badge/control; 5. Mentor identity; 6. welcome/status banner; 7. on-call/duty card and change-shift action; 8. owned-course KPI; 9. grading KPI; 10. support KPI; 11. rating KPI; 12. submissions panel heading/API label/view-all; 13. repeated submission preview cards and grade actions; 14. course panel heading/API label/view-all; 15. repeated course cards and workspace/content actions; 16. support inbox heading/count; 17. repeated support-request previews and reply actions; 18. support workspace link; 19. mentoring calendar heading/count; 20. appointment cards and join/details actions; 21. academic notices heading/term; 22. notice list; 23. footer including brand, standards, institutional links, Mentor support, policies and copyright.

## 6. Event plan

1. `ME01-EV-01` — enter `/mentor`: define auth prerequisite and independent widget request/response mapping for #46/#54/#58, including partial/error/empty states; client dispatch order and retry/cache policy remain unverified.
2. `ME01-EV-02` — course navigation/view-all → proposed ME-02 `/mentor/courses`.
3. `ME01-EV-03` — course Workspace action → proposed ME-03 with `courseId` from #46; destination and server permission remain server-enforced.
4. `ME01-EV-04` — course content-tree icon → proposed ME-06 `/mentor/courses/:courseId/content`; route/action needs confirmation.
5. `ME01-EV-05` — grading nav/view-all → ME-09 `/mentor/submissions`.
6. `ME01-EV-06` — row grade CTA: screenshot labels it ME-10, while inventory/AC-23 route through ME-09 selection before detail. Record discrepancy; do not choose route silently.
7. `ME01-EV-07` — support nav/workspace link → ME-11 `/mentor/support`.
8. `ME01-EV-08` — per-request reply CTA: screenshot labels it ME-12, while inventory/AC-24 route through ME-11 selection. Record discrepancy; do not choose route silently.
9. `ME01-EV-09` — global search: no target endpoint/route or field contract.
10. `ME01-EV-10` — notification/profile controls: no Mentor unread/profile endpoint or current route wiring.
11. `ME01-EV-11` — duty shift and meeting calendar actions: schedule provider, external meeting URL and route are absent from referenced contracts.
12. `ME01-EV-12` — announcement and footer destinations: HTML anchors are placeholders; destinations/notification data contract absent.

## 7. Blockers and status criteria

- `IMPLEMENTATION BLOCKED`: Student Web route/session source is absent; role bootstrap/handoff into a Mentor shell is not verified; display mapping is incomplete for dashboard sample data; per-row direct navigation conflicts with inventory/AC flow; #58 returns an unpaginated full thread collection; unreferenced schedule/rating/announcements/unread features lack approved data/routes; checked-in DB artifacts do not prove live schema.
- `DD BLOCKED`: keep only screen fields with source trace implementable; unresolved visual/sample fields, direct detail CTA routes, retry/cache behavior, query/loading policy and list content design require product/API decisions. Do not fabricate replacements.
- `RUNTIME NOT VERIFIED`: no Study Web runtime is present, and no live deployed UI/API/database check is performed in this docs task.
- No API, field, table, business rule, external provider or destination will be added by this session.

## 8. Output and review checklist

- [x] Complete plan and read source/API/AC before authoring the DD or marker image.
- [x] Preserve source hashes; create `ME-01_markers.json`, `ME-01_markers_overlay.svg`, and `screen_annotated.png` without editing originals.
- [x] Write `ME-01.md` with overview, full flow, marker-to-element map, event input/process/output/API details, state/navigation matrix, blockers, traceability and acceptance criteria.
- [x] Verify marker IDs `1..23` map once to DD elements; inspect image and link targets; check PNG dimensions/ratio and source hashes.
- [x] Update global `dd_screens/PLAN.md` and worklog with results; next screen is ME-02 in a separate session.

## 9. Sources

- [Screen inventory](../../../list_screen.md) — ME-01, AC/API index, F08/F09; [global DD plan](../../dd_screens/PLAN.md).
- [Source screenshot](screen.png), [source HTML](code.html), [Study Web status](../../../../../../.agents/web-work/study/INDEX.md), [Study Web design guide](../../../../../../.agents/web-study/design.md).
- [AC-03 Mentor Teaching](../../../../../../apps/study-server/docs/diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio), [API catalog](../../../../../../docs/lists/list_api.md).
- [Current API routes](../../../../../../apps/study-server/app/api/v1.py), [API #46 view](../../../../../../apps/study-server/app/modules/mentor/api_46_mentor_courses/view.py), [API #54 view](../../../../../../apps/study-server/app/modules/mentor/api_54_mentor_submissions_list/view.py), [API #58 view](../../../../../../apps/study-server/app/modules/mentor/api_58_mentor_support_requests/view.py), [Mentor role guard](../../../../../../apps/study-server/app/utils/auth.py).
- [API #46 DD snapshot](../../../../../../apps/study-server/docs/dd/46_mentor_courses/02_Overview.md), [#54 DD snapshot](../../../../../../apps/study-server/docs/dd/54_mentor_submissions_list/02_Overview.md), [#58 DD snapshot](../../../../../../apps/study-server/docs/dd/58_mentor_support_requests/02_Overview.md); each remains Draft and is secondary to current source.
- [Study Server module index/source notes](../../../../../../.agents/server-study/modules/README.md), [database evidence](../../../../../../.agents/server-study/database.md), [current dependencies](../../../../../../.agents/project/dependencies.md).
