# ST-24 — Tạo câu hỏi / chủ đề · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ST-24` |
| Module | Student |
| Route | `/student/discussions/new` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **Trạng thái:** DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED. Screenshot có form mẫu nhưng thiếu nút gửi; HTML hiện là trạng thái form unavailable. API #40 là Draft và chưa có Student route/module/test. Không suy ra cách chuyển văn bản editor thành `content:int64`. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [ST-24.md](../../screen_stitch/03_student/ST-24_tao-cau-hoi-chu-de/ST-24.md), [ST-24_PLAN.md](../../screen_stitch/03_student/ST-24_tao-cau-hoi-chu-de/ST-24_PLAN.md), [ST-24_markers.json](../../screen_stitch/03_student/ST-24_tao-cau-hoi-chu-de/ST-24_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Soạn title/body, chọn course đã ghi danh, lưu và quay về danh sách.
- In-scope: POST #40 sau hợp đồng title/content hợp lệ → refresh #39; không tự tạo content numeric.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-19 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Soạn title/body, chọn course đã ghi danh, lưu và quay về danh sách. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #40, #39
- Liên kết màn hình dự kiến: [ST-23](../ST-23-DanhSachThaoLuan/00-overview.md), [ST-25](../ST-25-ChiTietThreadVaPhanHoi/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | draft/invalid/submitting/created |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ST-24 source screen.png](../../screen_stitch/03_student/ST-24_tao-cau-hoi-chu-de/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/03_student/ST-24_tao-cau-hoi-chu-de/screen_annotated.png))
- Luồng: POST #40 sau hợp đồng title/content hợp lệ → refresh #39; không tự tạo content numeric.
- Priority: P2; Gate/source status: **D**; **BLOCK:** Contract content:int64 mâu thuẫn ngữ nghĩa rich text

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# ST-24 — Tạo câu hỏi / chủ đề

> **Trạng thái:** DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED. Screenshot có form mẫu nhưng thiếu nút gửi; HTML hiện là trạng thái form unavailable. API #40 là Draft và chưa có Student route/module/test. Không suy ra cách chuyển văn bản editor thành `content:int64`.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

### A.1. Định danh và mục tiêu

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | ST-24 — Tạo câu hỏi / chủ đề (Page) |
| Actor | Student theo inventory và AC-19. |
| Mục tiêu expected | Soạn một topic/câu hỏi trong discussion của course mà Student được phép tham gia; tạo thành công rồi quay về danh sách theo inventory. |
| Route inventory | `/student/discussions/new`; route đề xuất, chưa có Study Web router/source để xác minh. |
| Điều kiện trước | AC-19 yêu cầu Student đăng nhập và có quyền tham gia discussion của course. Predicate cụ thể chưa được xác nhận. |
| Điều kiện sau | AC-19: topic/comment được tạo và thread được cập nhật. ST-24 là nhánh tạo root topic, không phải nhánh reply ST-25. |
| API dự kiến | API #40 `POST /api/v1/discussions`; inventory nối API #39 để refresh list sau create. #40 chưa runnable. |
| Liên kết màn hình | ST-23 `/student/discussions` → ST-24; sau khi topic xuất hiện trong list, Student có thể đi tiếp ST-25 `/student/discussions/:discussionId`. Không tự chuyển trực tiếp sang ST-25. |
| Elements / events | 26 marker `ST24-EL-01…26`; 11 event `ST24-EV-01…11`. Marker là nhóm visual/control trong ảnh nguồn, không khẳng định runtime component. |
| Trạng thái | DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED. |

### A.2. Expected behavior — inventory, AC và API catalog

- Inventory ST-24 yêu cầu soạn title/body, chọn course đã ghi danh, lưu và quay về danh sách; inventory chỉ rõ API #40/#39 và state `draft/invalid/submitting/created`.
- F07 xác định ST-23 #39 → ST-24 #40; nhánh trả lời riêng là ST-25 #42 → #41 → reload #42. Không tạo autosave mutation.
- AC-19 xác định actor Student, precondition đăng nhập + có quyền course discussion, và postcondition topic/comment được tạo, thread cập nhật. Activity diagram có GET #39 trước nhánh quyết định tạo topic hay trả lời; create branch gọi POST #40 rồi thao tác `INSERT Discussion`.
- Catalog #40 khai báo `POST /api/v1/discussions`; Student Bearer; body `course_id:int64!`, `title:string!`, `content:int64!`; response `ApiEnvelope<Page<Discussion>>`; thành công HTTP 201 `DESIGN_RESOURCE_CREATED`; lỗi 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 422 `DESIGN_VALIDATION_ERROR`, 500 `DESIGN_INTERNAL_ERROR`.
- API #40 DD là `Draft — Needs Confirmation`, có 8 open questions. Giữ kiểu request `content:int64` theo catalog nhưng editor là văn bản; không cast/encode/chuyển đổi nội dung. Response `Discussion.title` chưa có nguồn vật lý. Enrollment ACTIVE, topic ACTIVE, timestamps, author/comments, transaction và một-item Page đều là DERIVED proposals, chưa approved.

### A.3. Current behavior và tài sản

- [`screen.png`](../../screen_stitch/03_student/ST-24_tao-cau-hoi-chu-de/screen.png) nguyên trạng 1600×1591, SHA-256 `45517c46e5274de6a835bc5a746069511f65714803295387cc33459c3d2511ab`. Đây là ảnh mẫu đủ rõ để annotate: shell Student, thông tin semester/trạng thái, trạng thái Mentor online, SLA, course/lesson selectors, title/counter, tags, editor mode và toolbar. Các giá trị hiển thị là static sample, không có data provenance.
- [`code.html`](../../screen_stitch/03_student/ST-24_tao-cau-hoi-chu-de/code.html) nguyên trạng, SHA-256 `3311de86bd3e1a6de624cccad1daf709d249d8c9f2ef24d7b79bf9f22693ce35`. Khác PNG: nó chỉ có empty-state “Chưa thể tạo chủ đề thảo luận / Biểu mẫu chưa sẵn sàng” và link về `/student/discussions`; không có form, input, API, auth guard, handler hay data binding.
- Dùng PNG gốc làm nền annotation; không render HTML thay thế vì HTML là một state khác và không chứa form thiết kế. Không sửa `screen.png` hoặc `code.html`.
- Study Web không có editable source/package/router cho ST-24; route là `UNWIRED`, không có UI runtime để xác minh.
- Current Study Server search chỉ tìm thấy Admin discussion routes #97/#98. Không có Student API #39–#42 route/module/query/test; #97/#98 có actor/permission và chức năng khác, không thể thay thế #40.
- Checked-in `DB.sql` có candidate `discussions(id BIGSERIAL, course_id NULL, user_id NULL, parent_id NULL, content TEXT NOT NULL, status DEFAULT 'ACTIVE', created_at NOT NULL, updated_at NOT NULL)` nhưng không có `title`; không có default timestamp. DB guide/ERD khác nullability. Đây là DDL artifact, không phải live schema evidence.
- API #40 DD response/source-mapping đề xuất author lookup, comments `[]`, status ACTIVE, one-item Page và server timestamps nhưng đánh dấu DERIVED/SOURCE_REQUIRED; không mô tả các đề xuất này như hành vi đã duyệt.

### A.4. API #40 contract được giữ nguyên và giới hạn

| Thuộc tính | Catalog | Trạng thái hiện tại / giới hạn |
|---|---|---|
| Method / endpoint | `POST /api/v1/discussions` | Không có Student route/module/query/view/test; `DECLARED_NOT_RUNNABLE / NOT_FOUND`. |
| Authentication / role | Bearer JWT; Student | AC-19 precondition; chưa có route #40 để gọi shared Student guard. Không nhận `user_id` từ form/body. |
| Path / query | Không có | Không thêm path/query field. |
| Request body | `course_id:int64!`, `title:string!`, `content:int64!` | Không có `lesson_id`, `tags`, files hoặc author field trong body. Title/content UI chưa thể map đầy đủ. |
| Success | HTTP 201 `DESIGN_RESOURCE_CREATED`; `ApiEnvelope<Page<Discussion>>` | Page metadata và fields tạo mới chưa có current implementation; proposal 1/1/1/1 là DERIVED. |
| Errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 422 `DESIGN_VALIDATION_ERROR`; 500 `DESIGN_INTERNAL_ERROR` | Không thêm 404/409/503 hoặc business code mới. Network/timeout là transport failure, không phải catalog code. |
| Side effect | Catalog/AC mong muốn tạo topic | Candidate `INSERT discussions`; chưa có SQL, transaction, live DB hay runtime call. |

**Contract gaps của API #40:** (1) request `content:int64` vs reusable `Discussion.content:string` và DDL `TEXT`; (2) `title` không có cột vật lý; (3) response `Page<Discussion>` không có page input; (4) course participation predicate; (5) new-topic status/visibility; (6) timestamps và transaction; (7) course/user FK nullability; (8) author và comments projection. Tất cả là open questions trong API DD, không được tự quyết trong ST-24.

### A.5. Discrepancies, bảo mật và blocker

| Vấn đề | Evidence | Tác động |
|---|---|---|
| PNG và HTML khác state | PNG có form mẫu; HTML là unavailable fallback. | Giữ cả hai nguyên trạng; không tuyên bố HTML đang thực hiện form. |
| Không có nút submit/save/cancel trong ảnh | Ảnh kết thúc ở vùng editor; inventory yêu cầu tạo/lưu. | Create event là expected nhưng không có trigger/control visual; CTA cần bổ sung/duyệt trước implementation. |
| Body editor không map sang catalog | Editor text; catalog yêu cầu `content:int64`. | Không thể xây request hoặc serialize text đúng contract hiện hành. |
| Thiếu title source và response mapping | DDL không có `title`; author/comments/page/status còn Draft. | Không thể xác định response binding sau create. |
| Course/module option source | Screenshot có course và lesson mẫu; API #40 chỉ nhận `course_id`, không có endpoint/options contract cho selectors trong ST-24. | Không giả định API lấy enrolled courses, lesson source hoặc gửi `lesson_id`. |
| Tags, GFM, attachments, counter và mẫu SLA | Chỉ xuất hiện trên PNG; API #40 không có tags/files, không định nghĩa editor/parser, title max hoặc SLA/mentor data. | Không tự tạo API, validation limit, sanitization/upload flow hoặc business claim. |
| Study Web và Student API runtime | Editable source/route và API #40 route/module/tests không có. | Không có client/server behavior, auth, persistence hay runtime result để xác minh. |

**Bảo mật:** actor dự kiến là Student đã xác thực; user identity, nếu được triển khai, phải đến từ authenticated principal chứ không từ input. Course authorization phải theo policy đã duyệt; hiện chưa có predicate. Không coi static profile/semester/online/SLA literals là principal, enrollment hoặc service status thật. Không show server/network error như `created` hay empty state.

### A.6. Nguồn truy vết

- [Inventory ST-24/F07](../../list_screen.md); [PNG nguồn](../../screen_stitch/03_student/ST-24_tao-cau-hoi-chu-de/screen.png), [HTML nguồn](../../screen_stitch/03_student/ST-24_tao-cau-hoi-chu-de/code.html), [marker map](../../screen_stitch/03_student/ST-24_tao-cau-hoi-chu-de/ST-24_markers.json), [overlay](../../screen_stitch/03_student/ST-24_tao-cau-hoi-chu-de/ST-24_markers_overlay.svg), [plan](../../screen_stitch/03_student/ST-24_tao-cau-hoi-chu-de/ST-24_PLAN.md).
- [API catalog #39–#42](../../../../../docs/lists/list_api.md); [API #39](../../../../study-server/docs/dd/39_discussions/02_Overview.md); API #40 [overview](../../../../study-server/docs/dd/40_discussions_create/02_Overview.md), [request](../../../../study-server/docs/dd/40_discussions_create/03_Request.md), [response](../../../../study-server/docs/dd/40_discussions_create/04_Response.md), [mapping](../../../../study-server/docs/dd/40_discussions_create/05_Data_Mapping.md), [errors](../../../../study-server/docs/dd/40_discussions_create/06_Error.md), [open questions](../../../../study-server/docs/dd/40_discussions_create/OPEN_QUESTIONS.md).
- [AC/API index](../../../../study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md), [AC activity diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio), [DB guide](../../../../study-server/docs/diagrams/DB_UNICA_TABLES.md), [checked-in DDL](../../../../../infra/postgres/study-server/DB.sql).
- [Current declared routes](../../../../../.agents/server-study/apis/declared-routes.md), [Study Web design target](../../../../../.agents/web-study/design.md), [previous ST-23 DD](../../screen_stitch/03_student/ST-23_danh-sach-thao-luan/ST-23.md).
