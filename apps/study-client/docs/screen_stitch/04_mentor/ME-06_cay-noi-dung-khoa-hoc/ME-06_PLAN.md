# ME-06 — Kế hoạch Detailed Design: Cây nội dung khóa học

> **Plan status:** COMPLETE — source trace được rà soát trước authoring; kế hoạch được ghi trước marker map, ảnh chú thích và DD; static artifact audit đã đạt.
> **Screen status dự kiến:** `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`.

## 1. Phạm vi và đầu vào

- Phiên này chỉ xử lý **ME-06** (`/mentor/courses/:courseId/content`); ME-03, ME-07, ME-08 chỉ được tham chiếu làm nguồn/đích liên kết.
- Phân loại: `primary_task_type: docs`; `secondary_task_types: [test]`; `project_scopes: [web-work, server-study]`; dependency: AC-22 → API #49 → Content tree; mutation handoff #50/#51 ở ME-07 và #52/#53 ở ME-08.
- Expected theo [`list_screen.md` ME-06](../../../list_screen.md#L166): GET #49; dựng cây sections/content theo `parent_id` và `order`; giữ IDs/version; không hiển thị draft như published; states `loading/empty/ready/error`; links ME-07/ME-08.
- Goal objective: `/home/daovh/.codex/attachments/f6127670-d01c-46c9-b22a-2adfcbe78641/goal-objective.md`; yêu cầu mỗi phiên một Screen ID, plan trước, ảnh chú thích/marker map/DD truy vết source, tracker/worklog và ba trạng thái chất lượng riêng.
- `screen.png`: 1367×1600, SHA-256 `3efb10d47fb04b743f64c224d6feb1f8faa3b284b2dbfc9676b73cdb0682e0b8`; đã mở xem toàn ảnh; giữ nguyên.
- `code.html`: SHA-256 `83a77f82e4e8a89122be88e6f78d2538329d6e0800bd4c789a1aadd207d60543`; mockup populated; chưa có fetch/XHR/form/API binding. JavaScript chỉ lọc/ẩn row, thu/phóng accordion, và hiện toast; các toast publish/save order không ghi dữ liệu.
- Study Web hiện được context `.agents/web-work/study/` đánh dấu `UNWIRED`; checkout không có Study Web `src/`, package manifest hoặc router để xác minh route/runtime.
- Registry không có canonical skill cho UI-only DD; `createDD-markdown` dành cho Web/API DD nên không dùng làm UI contract.

## 2. Source trace và quyết định tài liệu

### API #49 — tải cây Content

1. Route trong `apps/study-server/app/api/v1.py`: `GET /api/v1/mentor/courses/{course_id}/content`; chuyển raw path, Authorization, DB session và trace ID vào `get_course_contents`.
2. `validate_current_user_request(..., role="MENTOR")` chạy trước parse/DB. Signed-int64 malformed/out-of-range → 404; course không có → 404; `courses.mentor_id` khác principal số → 403. AC-22/AC-21 về course được phân công rộng hơn direct-owner source; không tự cấp quyền assigned-course.
3. Q1 đọc `courses.id, mentor_id`; Q2 đọc `contents` theo `course_id`, chỉ `deleted_at IS NULL`, sắp `parent_id NULLS FIRST, content_order ASC, id ASC` và alias `content_order AS order`.
4. Response hiện là `ApiEnvelope<Content[]>` phẳng, mỗi item `{id:int64, course_id:int64, content_type:string, title:string, payload:object, status:string, parent_id:int64|null, order:int32}`. UI dựng quan hệ cha-con bằng ID; không có `children[]`, paging hoặc version selector.
5. Source kiểm tra payload object, cùng course, unique IDs, tồn tại mọi parent và không cycle. Cây rỗng trả 200 `DESIGN_RESOURCE_RETRIEVED` với `data:[]`; DB/mapping lỗi trả safe 500 và rollback. Mọi status hiện có được trả; chỉ soft-deleted rows bị lọc.
6. API #49 là read-only. Local focused test source tồn tại (auth/owner/path, empty, projection/tree integrity, soft delete, statuses, query failure/OpenAPI); không chạy test theo giới hạn task.

### Handoff mutations #50–#53

- #50 `POST /mentor/content`: body `course_id, content_type, title, payload`; tạo **root node** (`parent_id=NULL`) với next root order, `status=PENDING_REVIEW`; không có `parent_id` trong request. Vì thế source hiện không tạo được lesson con qua route này.
- #51 `PUT /mentor/content/{content_id}`: body thay thế `content_type/title/payload`; lưu snapshot row hiện tại vào `content_versions`, cập nhật fields và đặt status `PENDING_REVIEW`, giữ `parent_id/order`. Không phải endpoint reorder.
- #52 `PATCH /mentor/content/{content_id}/publish`: body DERIVED `{published:boolean}`. `true` chỉ cho `APPROVED→PUBLISHED`, `false` chỉ `PUBLISHED→APPROVED`; retry cùng target là idempotent; trạng thái nguồn khác → 422. Body request có trong current source dù catalog rút gọn.
- #53 `DELETE /mentor/content/{content_id}`: soft-delete `deleted_at`; từ chối `PUBLISHED` và parent còn active children (422); success trả `DeleteResult {id,status:"deleted",deleted_at}`. #49 sau đó loại node đã xóa.
- Cả #50–#53 đều xác thực role MENTOR và direct owner theo source, có local route/module/test source. API DD #49 vẫn Draft — Needs Confirmation; các endpoint local/source-backed không xác minh deployment.

### Dữ liệu và sai khác

- Checked-in legacy `DB.sql` có `contents` và `content_versions`; migration `006_contents.sql`/`007_content_versions.sql` tồn tại. Live DB/migration deployment chưa xác minh. UUID `V1-PILOT` (`chapters/lessons/content_blocks`) là mô hình khác, không trộn vào Content BIGINT này.
- Inventory blocker cũ “Content không nằm trong 18 bảng DB.sql” không còn đúng với DDL hiện tại; blocker đúng là trạng thái live schema, enum/payload/lifecycle/version approval, assigned-course authorization và thiếu mutation cho child/reorder.
- Mockup hiển thị course summary, KPI, phân bố nội dung, QA guide, audit log, section/lesson/lab/quiz rows. #49 chỉ có Content node fields; không có course detail/KPI/chart/guide/audit read model được liên kết trong ME-06. Không dùng sample values làm dữ liệu server.
- Mockup có toast `API #52 PUT /mentor/courses/reorder`, nhưng #52 hiện là PATCH publish/unpublish; không có reorder endpoint trong ME-06 inventory. `Xuất bản ngay` trên row Draft cũng không khớp #52 vì `PENDING_REVIEW→PUBLISHED` bị 422.
- Ảnh và HTML cùng thể hiện một cây nội dung populated; HTML cài local filters/search/expand/collapse/toast nhưng không có route, API hoặc persistence. Mọi click ngoài những handler cục bộ là `href="#"` hoặc button không wired.

## 3. Kế hoạch artifact và marker map

1. Ghi plan này trước mọi marker map, overlay, annotated image và DD.
2. Tạo `ME-06_markers.json` làm mapping chuẩn, `ME-06_markers_overlay.svg` làm lớp đánh số và `screen_annotated.png` ở scale 2; dùng source pixels, không sửa ảnh gốc.
3. Dùng 44 marker theo nhóm: header/nav; breadcrumbs/course state; card metadata/actions; 4 KPI; filter/search/tree controls; distribution/quality/audit panels; từng chapter/row/action hiển thị; footer.
4. Mở ảnh annotated, kiểm tra marker không che nội dung chính, không chồng nhau, cùng tọa độ gốc và đủ 100% đối chiếu với JSON/DD; điều chỉnh nếu cần.
5. Viết `ME-06.md`: expected/current tách riêng; API response/tree mapping; 40 element map; event flows; states/errors/accessibility/privacy; links; discrepancies/open decisions; acceptance.
6. Cập nhật row ME-06, tổng tiến độ, checkpoint và next pointer trong `dd_screens/PLAN.md`; ghi worklog `design-study-screen-me06.md`.

### Marker inventory dự kiến

| # | Phần tử |
|---:|---|
| 1–5 | Logo, nav Mentor, tìm kiếm header, thông báo, tài khoản |
| 6–10 | Breadcrumbs, course state/ID, nhãn sync và phiên bản builder |
| 11–13 | Course title/description, lưu thứ tự, thêm chương, thêm bài học (ME-04) |
| 14–17 | KPI modules, video, lab/quiz, giờ |
| 18–20 | Tab filter, search nội dung, expand/collapse |
| 21–23 | Chapter 01, Chapter 02, action thêm bài trong Chapter 02 |
| 24–29 | Rows bài 14–16 và nhóm action xem/sửa/menu của từng row |
| 30–35 | Lab 14 + controls, Quiz 02 + question-bank controls, draft lesson + publish action |
| 36–38 | Chapter 03, Chapter 04, thêm Chapter 05 |
| 39–44 | Distribution, QA rules, handbook, audit timeline, xem toàn bộ log, footer |

> Mỗi marker đại diện đúng một phần tử hoặc một nhóm điều khiển cùng một hàng; số lượng là 44 và sẽ được khóa trong JSON/DD sau khi đặt tọa độ thực tế. Không mở rộng sang Screen ID khác.

## 4. Event flow và trạng thái dự kiến

1. Mở route expected `/mentor/courses/:courseId/content`; load #49 với Bearer JWT, hiển thị loading rồi map flat array thành tree bằng `parent_id`; giữ item `id`, `status`, `order` và không chọn version tùy ý.
2. `data:[]` → empty state; dữ liệu hợp lệ → ready; auth/owner/path/not-found/500 → error/denied/not-found theo response. UI route/state chưa có implementation.
3. Filter/search/accordion là local presentation-only theo HTML sample; filter và search JS hiện độc lập và có thể ghi đè `display`, không phải source of truth.
4. ME-07 handoff: mở create/edit; #50 hiện chỉ tạo root, #51 sửa Content và đưa về PENDING_REVIEW. Child creation contract và payload editor còn mở.
5. ME-08 handoff: mở publish/delete action; #52 chỉ cho transitions nêu trên; #53 có guard publish/children và soft-deletes. Sau mutation, expected re-fetch #49 theo inventory; client/cache invalidation hiện chưa có source.
6. Reorder/save order: giữ trong marker map nhưng chặn thực thi vì không có endpoint/API; toast mockup không phải persistence.
7. KPI, analytics, QA guide, audit timeline/count: không map từ #49; cần owner chỉ định read contract hoặc loại khỏi runtime.

## 5. Tiêu chí hoàn tất phiên

- `screen.png` và `code.html` giữ nguyên hash; không sửa thêm Screen ID.
- Plan được viết trước marker/ảnh/DD; mọi quyết định lấy từ route/model/query/view/DB/test source nêu trên.
- Marker IDs 1–44 liên tiếp, unique, in-bounds; JSON/SVG/DD khớp 100%; annotated PNG đúng 2734×3200, tỷ lệ gốc, được kiểm tra trực quan.
- DD mô tả rõ API #49 và giới hạn #50–#53; ghi trạng thái riêng `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED`.
- Tracker/checkpoint phản ánh đủ bốn core artifacts; worklog nêu preflight, nguồn, lệnh/hasil static audit và việc test/runtime không chạy.
- Chạy static artifact audit và `git diff --check`; không chạy tests, browser/runtime hay context validator (context pages không thay đổi).
