# ST-25 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ST-25-API-001` | #42 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ST-25-API-002` | #41 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #42, #41
- Orchestration/data notes: GET #42 → POST #41 → reload #42; xử lý double-send/ownership.
- BE/source status và gate: **D**; **BLOCK:** Response thảo luận Page<Discussion> không đồng nhất
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: A.2. Expected behavior — inventory, AC và API catalog

- Inventory ST-25: GET thread, hiển thị nội dung reply theo thứ tự, composer bình luận và trạng thái gửi; API #42 rồi #41 rồi reload #42; xử lý double-send và ownership. Trạng thái khai báo: `loading/replying/moderated/closed`.
- AC-19: Actor Student; precondition là đăng nhập và được phép tham gia discussion của course; postcondition topic/comment được tạo và thread cập nhật. F07/diagram nhánh REPLY chỉ rõ POST #41 → node “INSERT Comment + update counters” → GET #42 → hiển thị thread mới nhất. #39 list và #40 create topic là các nhánh/màn trước.
- API #42 catalog: `GET /api/v1/discussions/{discussion_id}`, Student Bearer, `discussion_id:int64!`, không có query/body, `ApiEnvelope<Page<Discussion>>`; 200 `DESIGN_RESOURCE_RETRIEVED`; 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 500 `DESIGN_INTERNAL_ERROR`.
- API #41 catalog: `POST /api/v1/discussions/{discussion_id}/comments`, Student Bearer, path `discussion_id:int64!`, body `content:int64!`, `ApiEnvelope<Page<Discussion>>`; 201 `DESIGN_RESOURCE_CREATED`; 401/403/404/422/500 với business codes tương ứng trong catalog.
- Reusable schema `Discussion` yêu cầu `id`, `course_id`, `title`, `content`, `author`, `status`, `comments`; `DiscussionComment` yêu cầu `id`, `discussion_id`, `content:string`, `author`, `created_at`. Catalog/API DD không định nghĩa sort, likes, bookmark, accepted solution, related discussion hoặc mentor appointment cho ST-25.

### Trích từ DD nguồn: A.4. API DD status và giới hạn

- API #41 DD: `Draft — Needs Confirmation`, Q-41-01…Q-41-08; #42 DD: `Draft — Needs Confirmation`, Q-42-01…Q-42-08. Cả hai có 8 open questions và chưa có Student runtime.
- API #41 request `content:int64` xung đột với editor text, reusable `DiscussionComment.content:string` và DDL `TEXT`. Không cast hoặc encode text thành integer.
- `Discussion.title` required trong reusable schema nhưng không có cột ở DB guide/ERD/DDL; không suy title từ content.
- API DD đề xuất `discussion_id` chỉ nhận root, reply là direct child, enrollment/topic/comment `ACTIVE`, comments sort `created_at ASC, id ASC`, response Page một thread và timestamp từ server. Đây là `DERIVED`, cần xác nhận; UI không được biến thành contract.
- AC nói “update counters” nhưng DDL/schema không có counter target; không khẳng định mutation/counter result.

### Trích từ DD nguồn: A.6. Truy vết nguồn

- [Screen inventory và F07](../../list_screen.md), [API catalog #39–#42](../../../../../docs/lists/list_api.md).
- [AC API index / AC-19](../../../../study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md), [AC activity diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio).
- [API #41 overview](../../../../study-server/docs/dd/41_discussions_comment/02_Overview.md), [request](../../../../study-server/docs/dd/41_discussions_comment/03_Request.md), [response](../../../../study-server/docs/dd/41_discussions_comment/04_Response.md), [mapping](../../../../study-server/docs/dd/41_discussions_comment/05_Data_Mapping.md), [open questions](../../../../study-server/docs/dd/41_discussions_comment/OPEN_QUESTIONS.md).
- [API #42 overview](../../../../study-server/docs/dd/42_discussions_detail/02_Overview.md), [request](../../../../study-server/docs/dd/42_discussions_detail/03_Request.md), [response](../../../../study-server/docs/dd/42_discussions_detail/04_Response.md), [mapping](../../../../study-server/docs/dd/42_discussions_detail/05_Data_Mapping.md), [open questions](../../../../study-server/docs/dd/42_discussions_detail/OPEN_QUESTIONS.md).
- [Discussion DDL candidate](../../../../../infra/postgres/study-server/DB.sql), [DB guide](../../../../study-server/docs/diagrams/DB_UNICA_TABLES.md), [Study Web visual/accessibility target](../../../../../.agents/web-study/design.md).
- Current route source: `apps/study-server/app/api/v1.py` registers Admin `/admin/discussions/{discussion_id}` for #98, not Student #42; current `app/modules/admin/api_98_admin_discussions_detail/` and its tests are Admin-only.

### Trích từ DD nguồn: B.3. Rời màn hình và các control ngoài contract

- ST25-EL-08 và HTML fallback có link về `/student/discussions`; target phù hợp inventory ST-23 nhưng route runtime chưa có. Quay lại/return context, giữ filter/page và browser history behavior chưa được xác định.
- Save, like/vote, reply-to-reply, sort, course/material, related discussion, mentor booking và code/source controls chỉ có trong screenshot. Không có API/route/source mapping được xác nhận; các control này không được xem là hành vi triển khai được.
- Screenshot/footer/header chứa nhiều link tĩnh hoặc literal. Các đích `#` trong HTML fallback không phải route evidence cho populated PNG.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/03_student/ST-25_chi-tiet-thread-va-phan-hoi/ST-25.md)
