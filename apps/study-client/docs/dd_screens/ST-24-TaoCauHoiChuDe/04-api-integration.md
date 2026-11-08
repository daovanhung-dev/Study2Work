# ST-24 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ST-24-API-001` | #40 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ST-24-API-002` | #39 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #40, #39
- Orchestration/data notes: POST #40 sau hợp đồng title/content hợp lệ → refresh #39; không tự tạo content numeric.
- BE/source status và gate: **D**; **BLOCK:** Contract content:int64 mâu thuẫn ngữ nghĩa rich text
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: A.2. Expected behavior — inventory, AC và API catalog

- Inventory ST-24 yêu cầu soạn title/body, chọn course đã ghi danh, lưu và quay về danh sách; inventory chỉ rõ API #40/#39 và state `draft/invalid/submitting/created`.
- F07 xác định ST-23 #39 → ST-24 #40; nhánh trả lời riêng là ST-25 #42 → #41 → reload #42. Không tạo autosave mutation.
- AC-19 xác định actor Student, precondition đăng nhập + có quyền course discussion, và postcondition topic/comment được tạo, thread cập nhật. Activity diagram có GET #39 trước nhánh quyết định tạo topic hay trả lời; create branch gọi POST #40 rồi thao tác `INSERT Discussion`.
- Catalog #40 khai báo `POST /api/v1/discussions`; Student Bearer; body `course_id:int64!`, `title:string!`, `content:int64!`; response `ApiEnvelope<Page<Discussion>>`; thành công HTTP 201 `DESIGN_RESOURCE_CREATED`; lỗi 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 422 `DESIGN_VALIDATION_ERROR`, 500 `DESIGN_INTERNAL_ERROR`.
- API #40 DD là `Draft — Needs Confirmation`, có 8 open questions. Giữ kiểu request `content:int64` theo catalog nhưng editor là văn bản; không cast/encode/chuyển đổi nội dung. Response `Discussion.title` chưa có nguồn vật lý. Enrollment ACTIVE, topic ACTIVE, timestamps, author/comments, transaction và một-item Page đều là DERIVED proposals, chưa approved.

### Trích từ DD nguồn: A.4. API #40 contract được giữ nguyên và giới hạn

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

### Trích từ DD nguồn: A.6. Nguồn truy vết

- [Inventory ST-24/F07](../../list_screen.md); [PNG nguồn](../../screen_stitch/03_student/ST-24_tao-cau-hoi-chu-de/screen.png), [HTML nguồn](../../screen_stitch/03_student/ST-24_tao-cau-hoi-chu-de/code.html), [marker map](../../screen_stitch/03_student/ST-24_tao-cau-hoi-chu-de/ST-24_markers.json), [overlay](../../screen_stitch/03_student/ST-24_tao-cau-hoi-chu-de/ST-24_markers_overlay.svg), [plan](../../screen_stitch/03_student/ST-24_tao-cau-hoi-chu-de/ST-24_PLAN.md).
- [API catalog #39–#42](../../../../../docs/lists/list_api.md); [API #39](../../../../study-server/docs/dd/39_discussions/02_Overview.md); API #40 [overview](../../../../study-server/docs/dd/40_discussions_create/02_Overview.md), [request](../../../../study-server/docs/dd/40_discussions_create/03_Request.md), [response](../../../../study-server/docs/dd/40_discussions_create/04_Response.md), [mapping](../../../../study-server/docs/dd/40_discussions_create/05_Data_Mapping.md), [errors](../../../../study-server/docs/dd/40_discussions_create/06_Error.md), [open questions](../../../../study-server/docs/dd/40_discussions_create/OPEN_QUESTIONS.md).
- [AC/API index](../../../../study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md), [AC activity diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio), [DB guide](../../../../study-server/docs/diagrams/DB_UNICA_TABLES.md), [checked-in DDL](../../../../../infra/postgres/study-server/DB.sql).
- [Current declared routes](../../../../../.agents/server-study/apis/declared-routes.md), [Study Web design target](../../../../../.agents/web-study/design.md), [previous ST-23 DD](../../screen_stitch/03_student/ST-23_danh-sach-thao-luan/ST-23.md).

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/03_student/ST-24_tao-cau-hoi-chu-de/ST-24.md)
