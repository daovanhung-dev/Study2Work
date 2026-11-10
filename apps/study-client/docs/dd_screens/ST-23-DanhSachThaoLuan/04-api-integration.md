# ST-23 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ST-23-API-001` | #39 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #39
- Orchestration/data notes: GET #39 theo course_id/page; không tự gộp với public reviews #10 nếu chưa được chốt.
- BE/source status và gate: **D**
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: A.2. Expected behavior — nguồn thiết kế/contract

- Inventory ST-23: route `/student/discussions`, AC-19, API #39; topic theo khóa học, filter/sort và nút tạo thảo luận; state `loading/empty/ready/error`; liên kết ST-24/ST-25.
- F07 quy định `ST-23 #39 list → ST-24 #40 create` hoặc `ST-25 #42 thread → #41 add comment → reload #42`. Nội dung rich-text/content mapping chưa chốt; không tạo autosave mutation.
- AC-19 đặt actor Student, precondition đã đăng nhập và có quyền tham gia discussion của course; postcondition topic/comment được tạo và thread được cập nhật. Activity diagram gọi GET #39 trước nhánh lựa chọn create/reply.
- API catalog #39 là `GET /api/v1/discussions`, Student Bearer, query `course_id?:int64`, `page?:int32`, `sort?:string`; response `ApiEnvelope<Page<Discussion>>`; success 200 `DESIGN_RESOURCE_RETRIEVED`; errors 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 500 `DESIGN_INTERNAL_ERROR`. Không có body/path param, không khai báo `size` query, 404 hoặc 422.
- API #39 GET chỉ đọc; không tạo topic/comment, cập nhật unread/counters, hoặc thay đổi trạng thái.

### Trích từ DD nguồn: A.4. API #39 contract và giới hạn mapping

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

### Trích từ DD nguồn: A.6. Nguồn truy vết

- [Inventory ST-23 và F07](../../list_screen.md); [PNG nguồn](../../screen_stitch/03_student/ST-23_danh-sach-thao-luan/screen.png), [HTML nguồn](../../screen_stitch/03_student/ST-23_danh-sach-thao-luan/code.html), [HTML static render](../../screen_stitch/03_student/ST-23_danh-sach-thao-luan/screen_rendered.png), [marker map](../../screen_stitch/03_student/ST-23_danh-sach-thao-luan/ST-23_markers.json), [overlay](../../screen_stitch/03_student/ST-23_danh-sach-thao-luan/ST-23_markers_overlay.svg), [plan](../../screen_stitch/03_student/ST-23_danh-sach-thao-luan/ST-23_PLAN.md).
- [API catalog](../../../../../docs/lists/list_api.md); [API #39 overview](../../../../study-server/docs/dd/39_discussions/02_Overview.md), [request](../../../../study-server/docs/dd/39_discussions/03_Request.md), [response](../../../../study-server/docs/dd/39_discussions/04_Response.md), [data mapping](../../../../study-server/docs/dd/39_discussions/05_Data_Mapping.md), [open questions](../../../../study-server/docs/dd/39_discussions/OPEN_QUESTIONS.md).
- [AC/API index](../../../../study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md), [AC-19 diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio), [DB table guide](../../../../study-server/docs/diagrams/DB_UNICA_TABLES.md), [legacy DDL](../../../../../infra/postgres/study-server/DB.sql).
- [Current declared routes](../../../../../.agents/server-study/apis/declared-routes.md), [Study Web design target](../../../../../.agents/web-study/design.md).

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/03_student/ST-23_danh-sach-thao-luan/ST-23.md)
