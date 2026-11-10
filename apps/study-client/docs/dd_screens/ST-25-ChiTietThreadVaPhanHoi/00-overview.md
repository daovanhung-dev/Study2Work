# ST-25 — Chi tiết thread và phản hồi · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ST-25` |
| Module | Student |
| Route | `/student/discussions/:discussionId` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: Source status is described in the source DD. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [ST-25.md](../../screen_stitch/03_student/ST-25_chi-tiet-thread-va-phan-hoi/ST-25.md), [ST-25_PLAN.md](../../screen_stitch/03_student/ST-25_chi-tiet-thread-va-phan-hoi/ST-25_PLAN.md), [ST-25_markers.json](../../screen_stitch/03_student/ST-25_chi-tiet-thread-va-phan-hoi/ST-25_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Danh sách nội dung phản hồi theo thứ tự; composer bình luận và trạng thái gửi.
- In-scope: GET #42 → POST #41 → reload #42; xử lý double-send/ownership.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-19 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Danh sách nội dung phản hồi theo thứ tự; composer bình luận và trạng thái gửi. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #42, #41
- Liên kết màn hình dự kiến: [ST-23](../ST-23-DanhSachThaoLuan/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | loading/replying/moderated/closed |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ST-25 source screen.png](../../screen_stitch/03_student/ST-25_chi-tiet-thread-va-phan-hoi/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/03_student/ST-25_chi-tiet-thread-va-phan-hoi/screen_annotated.png))
- Luồng: GET #42 → POST #41 → reload #42; xử lý double-send/ownership.
- Priority: P2; Gate/source status: **D**; **BLOCK:** Response thảo luận Page<Discussion> không đồng nhất

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# ST-25 — Chi tiết thread và phản hồi

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

### A.1. Định danh và mục tiêu

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID | ST-25 |
| Tên | Chi tiết chuỗi thảo luận và phản hồi |
| Route dự kiến | `/student/discussions/:discussionId` theo `list_screen.md`; route chưa có trong Study Web source. |
| Actor | Student đăng nhập; AC-19 yêu cầu có quyền tham gia discussion của course. Điều kiện course/status cụ thể chưa được duyệt. |
| Mục tiêu expected | Đọc một thread và comment theo API #42; Student có thể soạn/gửi reply qua API #41 rồi GET #42 để cập nhật thread. |
| Trạng thái hiện tại | `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`. |

### A.2. Expected behavior — inventory, AC và API catalog

- Inventory ST-25: GET thread, hiển thị nội dung reply theo thứ tự, composer bình luận và trạng thái gửi; API #42 rồi #41 rồi reload #42; xử lý double-send và ownership. Trạng thái khai báo: `loading/replying/moderated/closed`.
- AC-19: Actor Student; precondition là đăng nhập và được phép tham gia discussion của course; postcondition topic/comment được tạo và thread cập nhật. F07/diagram nhánh REPLY chỉ rõ POST #41 → node “INSERT Comment + update counters” → GET #42 → hiển thị thread mới nhất. #39 list và #40 create topic là các nhánh/màn trước.
- API #42 catalog: `GET /api/v1/discussions/{discussion_id}`, Student Bearer, `discussion_id:int64!`, không có query/body, `ApiEnvelope<Page<Discussion>>`; 200 `DESIGN_RESOURCE_RETRIEVED`; 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 500 `DESIGN_INTERNAL_ERROR`.
- API #41 catalog: `POST /api/v1/discussions/{discussion_id}/comments`, Student Bearer, path `discussion_id:int64!`, body `content:int64!`, `ApiEnvelope<Page<Discussion>>`; 201 `DESIGN_RESOURCE_CREATED`; 401/403/404/422/500 với business codes tương ứng trong catalog.
- Reusable schema `Discussion` yêu cầu `id`, `course_id`, `title`, `content`, `author`, `status`, `comments`; `DiscussionComment` yêu cầu `id`, `discussion_id`, `content:string`, `author`, `created_at`. Catalog/API DD không định nghĩa sort, likes, bookmark, accepted solution, related discussion hoặc mentor appointment cho ST-25.

### A.3. Current behavior và tài sản

- `screen.png` là ảnh thiết kế populated 573×1600, SHA-256 `36eee9dfb585bec24af84f264fd10f5bb69762ba9a916c17d384ce2cb6e8c903`. Ảnh minh họa header Student, topic, tác giả, content/code/source link, phản hồi/accepted answer, sort và reply composer cùng sidebar.
- `code.html` có SHA-256 `d5498ad73e7621e38fe0da865323f13fd737580d25f1a578fe8890a650e69efc`; đây là trang static unavailable-state, có Guest login/register header và link quay về `/student/discussions`. File không có thread, reply form/button, `fetch`, API/auth wiring hay data binding. HTML và PNG là `DISCREPANCY`; giữ cả hai nguyên trạng, annotate trực tiếp PNG.
- Current Study Web checkout không có editable source/package/router/Student route. Ignored `dist` chỉ có root `/`; không chứng minh ST-25 runtime. Study Web status là `UNWIRED`.
- Current Study Server search tìm thấy API #97/#98 trong phạm vi thảo luận Admin nhưng không thấy Student #41/#42 route/module/query/test. `GET /api/v1/admin/discussions/{discussion_id}` (#98) dùng ADMIN guard, derives Admin title từ normalized content, đọc mọi direct child status và có test Admin riêng; đó không phải API #42/Student runtime hoặc bằng chứng được phép derive Student title/filter.
- Checked-in DDL candidate `discussions` khai báo `content TEXT`, `parent_id` nullable self-reference, `course_id/user_id` nullable, `status` default `ACTIVE`, timestamps `NOT NULL` không default; không có `title` hoặc counter. Đây chỉ là artifact schema, chưa xác minh live DB/migration.
- Giá trị tên người dùng/course, trạng thái “ĐÃ GIẢI QUYẾT”, số lượt xem/thích/reply, accepted-answer, thời gian, level, tags và nội dung/code đều là literal mẫu trong PNG; không coi là API/default/DB data.

### A.4. API DD status và giới hạn

- API #41 DD: `Draft — Needs Confirmation`, Q-41-01…Q-41-08; #42 DD: `Draft — Needs Confirmation`, Q-42-01…Q-42-08. Cả hai có 8 open questions và chưa có Student runtime.
- API #41 request `content:int64` xung đột với editor text, reusable `DiscussionComment.content:string` và DDL `TEXT`. Không cast hoặc encode text thành integer.
- `Discussion.title` required trong reusable schema nhưng không có cột ở DB guide/ERD/DDL; không suy title từ content.
- API DD đề xuất `discussion_id` chỉ nhận root, reply là direct child, enrollment/topic/comment `ACTIVE`, comments sort `created_at ASC, id ASC`, response Page một thread và timestamp từ server. Đây là `DERIVED`, cần xác nhận; UI không được biến thành contract.
- AC nói “update counters” nhưng DDL/schema không có counter target; không khẳng định mutation/counter result.

### A.5. Discrepancies, bảo mật và blocker

| Hạng mục | Evidence | Status / tác động |
|---|---|---|
| Screenshot/HTML | PNG là thread populated; HTML là fallback unavailable và Guest header. | `DISCREPANCY`; giữ nguồn, annotate PNG, không diễn giải HTML thành thread implementation. |
| Study Web | Editable source/router/package/Student screen không có. | `UNWIRED`; không thể xác nhận route, auth guard, state, event hay navigation runtime. |
| API #41/#42 | API DD đều Draft và mỗi API có 8 open questions; chỉ thấy Student contract trong catalog/AC/DD. | `DECLARED_NOT_RUNNABLE` / `NOT_FOUND`; mọi request/response flow chỉ là expected design. |
| Admin API #98 precedent | Current Admin route derives a title from normalized content and reads all direct children without a Student visibility gate. | `CURRENT ADMIN ONLY`; không sao chép quy tắc này cho Student #42. |
| Thread projection | Required `title` thiếu nguồn; `Page<Discussion>` dùng cho detail nhưng metadata/item semantics chưa chốt; profile, visibility và timestamp mapping còn mở. | `SOURCE_REQUIRED` / `BLOCKER`; chưa thể khẳng định populated UI map từ response. |
| Reply payload | Body là string trong editor; catalog #41 bắt buộc `content:int64`, còn schema comment và DDL là string/TEXT. | `DISCREPANCY` / `BLOCKER`; không serialize hoặc gửi body cho đến khi contract được quyết định. |
| Access/moderation | AC-19 yêu cầu quyền tham gia; ACTIVE enrollment/topic/comment, root-only và 403/404 concealment là proposals. | `BLOCKER`; không chọn policy bằng suy đoán. |
| Screenshot-only interactions | Save, likes/votes, sort, accepted answer, related topics, course/video và mentor CTA không có mapping API/source. | `UNVERIFIED DESIGN DATA`; mô tả controls, không thêm endpoint/route/side effect. |

Security: catalog quy định Student Bearer; principal/access predicate cụ thể phải theo contract được duyệt. Không lấy author identity từ avatar/tên mẫu hoặc body. Không đọc secret/token từ URL. Current #98 Admin auth không được dùng làm Student guard evidence.

### A.6. Truy vết nguồn

- [Screen inventory và F07](../../list_screen.md), [API catalog #39–#42](../../../../../docs/lists/list_api.md).
- [AC API index / AC-19](../../../../study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md), [AC activity diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio).
- [API #41 overview](../../../../study-server/docs/dd/41_discussions_comment/02_Overview.md), [request](../../../../study-server/docs/dd/41_discussions_comment/03_Request.md), [response](../../../../study-server/docs/dd/41_discussions_comment/04_Response.md), [mapping](../../../../study-server/docs/dd/41_discussions_comment/05_Data_Mapping.md), [open questions](../../../../study-server/docs/dd/41_discussions_comment/OPEN_QUESTIONS.md).
- [API #42 overview](../../../../study-server/docs/dd/42_discussions_detail/02_Overview.md), [request](../../../../study-server/docs/dd/42_discussions_detail/03_Request.md), [response](../../../../study-server/docs/dd/42_discussions_detail/04_Response.md), [mapping](../../../../study-server/docs/dd/42_discussions_detail/05_Data_Mapping.md), [open questions](../../../../study-server/docs/dd/42_discussions_detail/OPEN_QUESTIONS.md).
- [Discussion DDL candidate](../../../../../infra/postgres/study-server/DB.sql), [DB guide](../../../../study-server/docs/diagrams/DB_UNICA_TABLES.md), [Study Web visual/accessibility target](../../../../../.agents/web-study/design.md).
- Current route source: `apps/study-server/app/api/v1.py` registers Admin `/admin/discussions/{discussion_id}` for #98, not Student #42; current `app/modules/admin/api_98_admin_discussions_detail/` and its tests are Admin-only.
