# ME-02 — Các khóa học phụ trách · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ME-02` |
| Module | Mentor |
| Route | `/mentor/courses` — source-wired in `mentor.route.ts`; runtime not verified |
| Actor/role | Mentor đã đăng nhập; `MentorLayout` và API #46 source-backed, runtime chưa xác minh |
| DD status | Draft (package được chuyển đổi); source status: **DD status:** `DD BLOCKED` — ownership/assignment, unsupported filters, KPI và một số route/action chưa đủ quyết định để triển khai đầy đủ.<br>; **Implementation status:** `PARTIAL_SOURCE` — route, #46 caller, response validation, cancellation, states và source-backed card/pagination are implemented; mockup-only requirements remain gated.<br>; **Runtime status:** `RUNTIME NOT VERIFIED` — không chạy frontend/API/DB production trong task này. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.2 / 2026-11-21 |
| Nguồn đối chiếu | [ME-02.md](../../screen_stitch/04_mentor/ME-02_cac-khoa-hoc-phu-trach/ME-02.md), [ME-02_PLAN.md](../../screen_stitch/04_mentor/ME-02_cac-khoa-hoc-phu-trach/ME-02_PLAN.md), [ME-02_markers.json](../../screen_stitch/04_mentor/ME-02_cac-khoa-hoc-phu-trach/ME-02_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Course list theo ownership/assignment, status/page/size, action manage.
- In-scope: GET #46; mentor chỉ thao tác course hợp quyền từ server, không tự suy ownership ở client.
- Out-of-scope: Xem gate bên dưới; không kết luận route/page/API đã được triển khai live hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-21 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Course list theo ownership/assignment, status/page/size, action manage. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #46
- Liên kết màn hình dự kiến: [ME-03](../ME-03-WorkspaceKhoaHocCuaMentor/00-overview.md), [ME-04](../ME-04-TaiLenVaTaoBaiGiang/00-overview.md), [ME-16](../ME-16-TienDoToanKhoaHoc/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | loading/empty/ready/denied |
| Current implementation/runtime | Current source + worklog/context Study Web | `PARTIAL_SOURCE` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ME-02 source screen.png](../../screen_stitch/04_mentor/ME-02_cac-khoa-hoc-phu-trach/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/04_mentor/ME-02_cac-khoa-hoc-phu-trach/screen_annotated.png))
- Luồng: GET #46; mentor chỉ thao tác course hợp quyền từ server, không tự suy ownership ở client.
- Priority: P1; Gate/source status: **M** (API #46 and source-backed subset; unsupported design requirements remain gated)

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.
- 2026-11-21 — Reconciled current Study Client route, #46 caller/guards, page states, source-backed card presentation and remaining contract gates. Runtime not verified.

## Trạng thái và ranh giới bằng chứng

# ME-02 — Các khóa học phụ trách

> **DD status:** `DD BLOCKED` — source và artifact được truy vết, nhưng ownership/assignment, filter, KPI và một số route/action chưa đủ quyết định để triển khai đầy đủ.<br>
> **Implementation status:** `PARTIAL_SOURCE` — route/page/#46 caller exist; typed response checks, stale-request cancellation, loading/error/empty handling, safe thumbnail presentation and server pagination are source-backed. Unsupported screenshot requirements remain blocked.<br>
> **Runtime status:** `RUNTIME NOT VERIFIED` — không chạy frontend/API/DB production trong task này.

### Current source reconciliation (2026-11-21)

- `/mentor/courses` is registered in `apps/study-client/src/app/features/mentor/mentor.route.ts` under `MentorLayout`; `ME02Page` calls `ME02CoursesService.list`, which uses `MentorApiService` and API #46. The route/session/deployment was not exercised at runtime.
- The page sends page/size 20 and optional exact `DRAFT|PUBLISHED`; validates the success envelope, business code, Course projection, requested pagination metadata and status filter; cancels stale requests; and recovers an empty out-of-range page by refetching the last valid page (or page 1 for an empty collection).
- Cards render the #46 title, description, optional safe thumbnail, source status and numeric ID; the Workspace CTA links to the registered ME-03 route. Search, level, semester and sort filters, aggregate KPIs, grading/content/report actions, assigned-course scope and currency-formatted price remain unavailable or unresolved.
- The DD-source excerpt below preserves the earlier design-time snapshot; where its old `UNWIRED` statements conflict with the current source, use this reconciliation for current behavior. The AC-21 assignment expectation remains unresolved against #46's direct-owner-only query.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: 1. Tổng quan

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID | ME-02 |
| Tên | Các khóa học phụ trách |
| Mục tiêu kỳ vọng | Mentor xem danh sách course mình có quyền quản lý; từ course đã xác minh có thể tiếp tục vào workspace hoặc luồng nghiệp vụ đã được duyệt. |
| Actor | Mentor đã xác thực. API #46 yêu cầu JWT hợp lệ chứa role `MENTOR`. |
| Route | `/mentor/courses`; registered under `MentorLayout` in current source; runtime not verified. |
| Điều kiện vào | MentorLayout/MentorApiService provide the source-backed session/token path; API #46 remains authoritative for role and direct-owner scope. Runtime is unverified. |
| API chính | `GET /api/v1/mentor/courses` (#46), source-backed trong Study Server hiện tại. |
| Liên kết inventory | ME-03 `/mentor/courses/:courseId`, ME-04 `/mentor/courses/:courseId/lectures/new`, ME-16 `/mentor/courses/:courseId/progress`. |
| Artifact design | `screen.png` và `code.html` là mẫu tĩnh; giữ nguyên. Ảnh có nhãn “API #46 Live” không chứng minh deployment/live data. |

### Nguồn thiết kế và trạng thái hiện tại

- Inventory ME-02 ghi AC-21, API #46, lọc `status/page/size`, course ownership/assignment và states `loading/empty/ready/denied`. AC-21 nói Mentor sở hữu **hoặc được phân công** course trước khi chọn course để tạo lecture. Đây là expected behavior, không phải bằng chứng về assignment relation trong current source.
- PNG 1100×1600 hiển thị ba course sample, bốn KPI tổng, search/status/level/sort, semester chip, pagination và các CTA cấp course. HTML 47,810 bytes chứa cùng nội dung tĩnh, 19 anchors `href="#"`, 11 buttons, 2 text inputs, 4 selects và 3 article mẫu. Không có app router, API fetch hay dữ liệu được hydrate.
- Current source check (2026-11-21): the Angular route exists under `MentorLayout`, and ME-02 calls #46 through `MentorApiService`; this supersedes the earlier checkout inventory that found only docs/assets. Serving/deployment and runtime remain unverified. Xem [Study Web context](../../../../../.agents/web-work/study/INDEX.md).
- API #46 hiện có route/module/tests trong Study Server. API DD snapshot còn ghi route/module/test `UNWIRED / NOT_FOUND` và guard Mentor chưa có; đây là `DISCREPANCY` vì current source đã thay đổi sau snapshot. Current source được ưu tiên khi mô tả behavior.
- Manifest `.agents/context-manifest.json` loại trừ `web-ui-only-dd` khỏi `createDD-markdown`; registry không có canonical skill cho UI-only DD. Không dùng API-DD template để thay cho screen DD.

### Expected behavior / current behavior

| Chủ đề | Expected behavior | Current evidence |
|---|---|---|
| Course scope | Course do Mentor sở hữu hoặc được phân công; client không tự suy quyền. | #46 chỉ lọc trực tiếp `courses.mentor_id = current numeric JWT sub`. Chưa thấy assignment relation trong #46 query. AC-21 và source chưa thống nhất. |
| Status | Có filter status theo UI/contract. | #46 chỉ nhận `DRAFT` hoặc `PUBLISHED`; nếu bỏ `status`, query trả cả hai. Current select sends those exact enums and displays `Bản nháp` / `Đã xuất bản`; prototype labels `Đang tuyển sinh & giảng dạy / Chuẩn bị mở / Đã lưu trữ` remain unmapped. |
| Search | UI tìm tên/mã course. | #46 không có `q`, course code hoặc trường code trong Course response. |
| Level/sort/term | UI lọc cấp độ, kỳ học và sắp xếp theo học viên/tiến độ/cập nhật. | #46 không nhận các filter đó; sort hiện cố định `created_at DESC, id ASC`. |
| Course cards | Render Course data đã được server trả và quyền quản lý đã kiểm tra. | #46 trả `id/title/description?/thumbnail_url?/price/status/mentor`; current cards use title/description/optional safe thumbnail/status/numeric ID/mentor name, while omitting price because no currency is supplied. It does not return rating, course code, level, Student/lesson counts, pending submissions or progress. |
| KPI | Tổng course/learner, completion, Capstone theo định nghĩa rõ. | #46 chỉ có pagination count và Course fields. #62 là active roster mỗi course, #65 là progress từng Student, #66 là activity proxy; không API nào trực tiếp trả các KPI như mẫu. |
| Pagination | Page/size; state trang và kích thước phù hợp với kết quả server. | #46 service sends page and fixed size 20; controls use response `total_pages` with first/previous/next/last. If an empty result is beyond the current last page, the client refetches that last page (page 1 when total is zero). Other page sizes are not exposed. |
| CTA | Mỗi action có screen/route, data handoff và access check được xác nhận. | HTML dùng `href="#"`; inventory links ME-03/04/16, trong khi card có thêm ME-06/09 và report tổng thể chưa có destination. |
