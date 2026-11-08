# ST-23 — Danh sách thảo luận · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ST-23` |
| Module | Student |
| Route | `/student/discussions` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **Trạng thái:** DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED. Source hiện chỉ có static empty-state HTML; API #39 là design-only/Draft và chưa có Student route/module/query/test. Tài liệu giữ nguyên các khoảng trống thay vì dựng list/filter/sort/create behavior từ suy đoán. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [ST-23.md](../../screen_stitch/03_student/ST-23_danh-sach-thao-luan/ST-23.md), [ST-23_PLAN.md](../../screen_stitch/03_student/ST-23_danh-sach-thao-luan/ST-23_PLAN.md), [ST-23_markers.json](../../screen_stitch/03_student/ST-23_danh-sach-thao-luan/ST-23_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Topic theo khóa học, filter/sort, nút tạo thảo luận.
- In-scope: GET #39 theo course_id/page; không tự gộp với public reviews #10 nếu chưa được chốt.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-19 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Topic theo khóa học, filter/sort, nút tạo thảo luận. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #39
- Liên kết màn hình dự kiến: [ST-24](../ST-24-TaoCauHoiChuDe/00-overview.md), [ST-25](../ST-25-ChiTietThreadVaPhanHoi/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | loading/empty/ready/error |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ST-23 source screen.png](../../screen_stitch/03_student/ST-23_danh-sach-thao-luan/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/03_student/ST-23_danh-sach-thao-luan/screen_annotated.png))
- Luồng: GET #39 theo course_id/page; không tự gộp với public reviews #10 nếu chưa được chốt.
- Priority: P2; Gate/source status: **D**

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# ST-23 — Danh sách thảo luận

> **Trạng thái:** DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED. Source hiện chỉ có static empty-state HTML; API #39 là design-only/Draft và chưa có Student route/module/query/test. Tài liệu giữ nguyên các khoảng trống thay vì dựng list/filter/sort/create behavior từ suy đoán.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

### A.1. Định danh, actor và mục tiêu

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | ST-23 — Danh sách thảo luận (Page) |
| Mục tiêu expected | Student xem các thread thảo luận trong phạm vi được phép; theo inventory có filter/sort theo course và tạo chủ đề mới. |
| Actor | Student theo inventory/API catalog #39 và AC-19. |
| Route inventory | `/student/discussions`; hiện là route thiết kế, Study Web không có router/source để xác nhận. |
| Điều kiện trước | AC-19: Student đăng nhập và có quyền tham gia discussion của course. Quy tắc xác định quyền chưa được duyệt. |
| Kết quả sau | ST-23 là GET/list surface, không có mutation. Từ đây expected navigation tới ST-24 để tạo topic hoặc ST-25 để mở thread. |
| API | GET API #39 `/api/v1/discussions`; optional query `course_id`, `page`, `sort`; Student Bearer. |
| Màn hình liên quan | ST-08 (HTML prototype back link `/student/courses`), ST-24 (create), ST-25 (thread/detail); inventory không yêu cầu nhập public course reviews GS-05/API #10 vào danh sách Student. |
| Elements / events | 15 marker `ST23-EL-01…15`; 10 event `ST23-EV-01…10`. Marker mô tả nhóm nhìn thấy trong static HTML render, không khẳng định runtime component. |
| Trạng thái | DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED. |

### A.2. Expected behavior — nguồn thiết kế/contract

- Inventory ST-23: route `/student/discussions`, AC-19, API #39; topic theo khóa học, filter/sort và nút tạo thảo luận; state `loading/empty/ready/error`; liên kết ST-24/ST-25.
- F07 quy định `ST-23 #39 list → ST-24 #40 create` hoặc `ST-25 #42 thread → #41 add comment → reload #42`. Nội dung rich-text/content mapping chưa chốt; không tạo autosave mutation.
- AC-19 đặt actor Student, precondition đã đăng nhập và có quyền tham gia discussion của course; postcondition topic/comment được tạo và thread được cập nhật. Activity diagram gọi GET #39 trước nhánh lựa chọn create/reply.
- API catalog #39 là `GET /api/v1/discussions`, Student Bearer, query `course_id?:int64`, `page?:int32`, `sort?:string`; response `ApiEnvelope<Page<Discussion>>`; success 200 `DESIGN_RESOURCE_RETRIEVED`; errors 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 500 `DESIGN_INTERNAL_ERROR`. Không có body/path param, không khai báo `size` query, 404 hoặc 422.
- API #39 GET chỉ đọc; không tạo topic/comment, cập nhật unread/counters, hoặc thay đổi trạng thái.

### A.3. Current behavior và tài sản

- `screen.png` nguyên trạng 1280×1142, SHA256 `7c0c2fe1b79d0c44d88d915578f295d732738e41a0579f471405652f0e366b38`; ảnh gần như chỉ có nền trống, không đọc được giao diện.
- `code.html` nguyên trạng, SHA256 `2812398914f2a7b35942bffa912f747ef80536091b5316335279821ca89f2ebb`. Đây là static HTML gồm header/nav, hai breadcrumb, title, empty-state icon/heading/copy, link `/student/courses` và footer; không có list/topic cards, course filter, sort, create CTA, pagination, API call, auth guard, event handler hoặc data binding. Header/footer links phần lớn `href="#"`.
- Do PNG không sử dụng được làm giao diện, tạo `screen_rendered.png` 1280×1173 bằng Chrome 155 headless/CDP từ `code.html` và đánh số trên bản render. HTML/PNG gốc không sửa. Bản render là prototype tĩnh có CDN/fonts, không phải application/runtime screenshot.
- Study Web hiện không có editable source/package/router cho `/student/discussions`; UI runtime `UNWIRED`.
- API #39 API DD `Draft — Needs Confirmation`, `DESIGN_ONLY`; current Study Server không có Student #39 route/module/query/test. Router hiện chỉ có Admin discussion API #97 và #98; cả hai actor/access scope khác nên không thay thế #39.
- Checked-in `infra/postgres/study-server/DB.sql` có `discussions(id, course_id?, user_id?, parent_id?, content, status default ACTIVE, created_at, updated_at)` và không có `title`. Đây là DDL artifact, không xác nhận live schema. DB guide ghi `discussions` làm logical tree cho discussion/review/reply; riêng inventory yêu cầu không gộp ST-23 với public reviews #10 nếu chưa được chốt.

### A.4. API #39 contract và giới hạn mapping

| Thuộc tính | Theo catalog / DD hiện có | Trạng thái source |
|---|---|---|
| Method / path | `GET /api/v1/discussions` | API #39 chưa có route/module/query/test hiện hành; `DECLARED_NOT_RUNNABLE / NOT_FOUND`. |
| Auth | `Authorization: Bearer <Student JWT>`; Student role | Catalog/AC-19 design; chưa có route #39 áp dụng shared Student guard. |
| Query | `course_id?:int64`, `page?:int32`, `sort?:string`; không `size` | Field names catalog; defaults/semantics/parse/range chưa duyệt. |
| Body/path | Không có request body/path parameter | Catalog. |
| Success | HTTP 200 `DESIGN_RESOURCE_RETRIEVED`, `ApiEnvelope<Page<Discussion>>` | Design contract; chưa runtime-verified. |
| Discussion projection | `id:int64`, `course_id:int64`, `title:string`, `content:string`, `author:UserSummary`, `status:DiscussionStatus`, `comments:DiscussionComment[]` | Logical schema catalog. `title` không có cột trong checked-in DDL; `course_id` nullable trong DDL nhưng required trong schema; status values chưa chốt. |
| PageMeta | `page:int32`, `size:int32`, `total:int64`, `total_pages:int32` | Response metadata. Request không khai báo size; API DD đề xuất page=1, size=20, nhưng đó là DERIVED, chưa approved. |
| Errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 500 `DESIGN_INTERNAL_ERROR` | Chỉ các catalog codes này. Không tự thêm 400/404/422. |

API #39 DD đề xuất các quy tắc DERIVED sau, tất cả cần xác nhận trước khi triển khai: lọc enrollment ACTIVE; khi thiếu `course_id` liệt kê course đang enrollment; page mặc định 1, fixed size 20; sort `created_at_desc`/`created_at_asc`; chỉ root ACTIVE và direct-child comments ACTIVE; trả comments trong mỗi item; `total_pages=ceil(total/20)` hoặc 0 khi empty. Đây không phải current behavior hoặc approved business rules.

### A.5. Discrepancies, bảo mật và quyết định mở

| Vấn đề | Evidence | Tác động |
|---|---|---|
| Empty-state only | PNG blank; HTML chỉ có no-topic fallback. | Không có loaded-state/list design để map API items. Empty copy không chứng minh API trả rỗng hoặc dữ liệu đang đồng bộ. |
| Expected controls absent | Inventory yêu cầu course filter, sort và create button; HTML không có chúng. | Không tạo marker giả hoặc event control không tồn tại; cần quyết định thiết kế loaded state. |
| API #39 absent at runtime | Current Study route/module/query/test không có #39; #97/#98 là Admin. | Không tuyên bố request/API UI wired; implementation bị chặn. |
| Query/access semantics | API #39 DD còn bảy open questions; catalog không khai báo query validation errors. | Không tự chọn enrollment policy, global scope, sort values/default, page size hoặc 400/422. |
| `title` / `content` | Catalog `Discussion.title` required; DDL không có `title`; API #40 catalog lại khai báo `content:int64` trong khi AC/UI là topic text. | Không map `title=content`, không encode text thành int64; ST-24 handoff bị ảnh hưởng. |
| Comments in list | API #39 DD đề xuất comments[]; AC-19 còn gọi API #42 riêng để load topic + comments. | Cần quyết định payload/list boundary, không tải/hiển thị comments theo assumption. |
| Review-vs-discussion | DB tree có thể lưu reviews và discussions; catalog API #10 là public course reviews, API #39 là Student discussion. | Không nhập #10/reviews hoặc rating vào ST-23. |
| Link destinations | Prototype back anchor trỏ `/student/courses`; header/footer hầu hết `#`. | Inventory route ST-08 là `/student/courses`, nhưng Study Web runtime và role gate chưa có. Các link khác không có destination. |

**Bảo mật:** không nhận user ID từ client/query; identity dự kiến từ Student principal sau khi backend #39 được wire. Không hiển thị hidden/moderated/deleted rows dựa trên giả định `status='ACTIVE'`; visibility/status enum và course access chưa được duyệt. Không coi access-denied hoặc transport failure là empty state. Không hiển thị dữ liệu report/Admin #97–#98 trong Student list.

### A.6. Nguồn truy vết

- [Inventory ST-23 và F07](../../list_screen.md); [PNG nguồn](../../screen_stitch/03_student/ST-23_danh-sach-thao-luan/screen.png), [HTML nguồn](../../screen_stitch/03_student/ST-23_danh-sach-thao-luan/code.html), [HTML static render](../../screen_stitch/03_student/ST-23_danh-sach-thao-luan/screen_rendered.png), [marker map](../../screen_stitch/03_student/ST-23_danh-sach-thao-luan/ST-23_markers.json), [overlay](../../screen_stitch/03_student/ST-23_danh-sach-thao-luan/ST-23_markers_overlay.svg), [plan](../../screen_stitch/03_student/ST-23_danh-sach-thao-luan/ST-23_PLAN.md).
- [API catalog](../../../../../docs/lists/list_api.md); [API #39 overview](../../../../study-server/docs/dd/39_discussions/02_Overview.md), [request](../../../../study-server/docs/dd/39_discussions/03_Request.md), [response](../../../../study-server/docs/dd/39_discussions/04_Response.md), [data mapping](../../../../study-server/docs/dd/39_discussions/05_Data_Mapping.md), [open questions](../../../../study-server/docs/dd/39_discussions/OPEN_QUESTIONS.md).
- [AC/API index](../../../../study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md), [AC-19 diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio), [DB table guide](../../../../study-server/docs/diagrams/DB_UNICA_TABLES.md), [legacy DDL](../../../../../infra/postgres/study-server/DB.sql).
- [Current declared routes](../../../../../.agents/server-study/apis/declared-routes.md), [Study Web design target](../../../../../.agents/web-study/design.md).
