# AD-06 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `AD-06-API-001` | #73 | `GET /api/v1/admin/courses` | EV-01/05/06/07 | Admin Bearer; shared server guard requires `ADMIN` |
| `AD-06-API-002` | #68 | `GET /api/v1/admin/users` | EV-10 mentor selection | Admin Bearer; role/status/page query |
| `AD-06-API-003` | #104 | `POST /api/v1/admin/courses` | EV-10 course creation | Admin Bearer; shared server guard requires `ADMIN` |

## 2. Contract / source detail

- API refs trong original AC/DD: #73. User-approved AD-06 create extension: #68 for mentor options and #104 for course create.
- Orchestration/data notes: GET #73 chỉ hỗ trợ raw exact `status`, signed-int64 `mentor`, category bị reject 422, page int32; size=20, `courses.id ASC`; không có search/KPI/course code/lesson count. AC-32 đi qua #74 detail trước #76 status; chưa xác nhận action trực tiếp từ row. #77 đánh dấu `DELETED`, #73 không loại status đó.
- BE/source status và gate: API #73 source wired; API #68 source wired for mentor selection; API #104 is user-approved and source wired for create. **DD BLOCKED; IMPLEMENTATION PARTIAL SOURCE:** search, status/DELETED visibility, category relation, KPI, course code/lesson count, export/sync/policy and Admin permission mapping remain gated; **RUNTIME NOT VERIFIED**
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: Nguồn truy vết

- Inventory: [list_screen.md](../../list_screen.md), AD-06 row 64; global tracking: [dd_screens/PLAN.md](../../screen_stitch/dd_screens/PLAN.md).
- AC/API: [AC-32 Admin Management diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio), [API catalog](../../../../../docs/lists/list_api.md), [API #73 DD overview](../../../../study-server/docs/dd/73_admin_courses_list/02_Overview.md), [API #73 open questions](../../../../study-server/docs/dd/73_admin_courses_list/OPEN_QUESTIONS.md).
- Runtime source: [#73 route](../../../../study-server/app/api/v1.py), [#73 validation](../../../../study-server/app/modules/admin/api_73_admin_courses_list/validate.py), [#73 query](../../../../study-server/app/modules/admin/api_73_admin_courses_list/query.py), [#73 view](../../../../study-server/app/modules/admin/api_73_admin_courses_list/view.py), [shared response model](../../../../study-server/app/modules/shared/course_catalog/models.py), [#77 soft-delete query](../../../../study-server/app/modules/admin/api_77_admin_course_delete/query.py).
- Test evidence (read only in this session): [#73 test module](../../../../study-server/tests/modules/admin/api_73_admin_courses_list/test_admin_courses_list.py) and [2026-11-01 API test report](../../../../study-server/docs/testing/api-test-report-2026-11-01.md).
- Persistence/client boundary: [legacy candidate DB.sql](../../../../../infra/postgres/study-server/DB.sql), [Study Web design guide](../../../../../.agents/web-study/design.md), `.agents/web-work/study/` source-status context.

### Trích từ DD nguồn: Luồng mục tiêu theo contract (sau khi blockers được giải quyết)

1. Admin mở `/admin/courses` từ Admin shell. Guard phía client có thể cải thiện UX nhưng không thay server authorization. Contract AC-32 yêu cầu course-management permission; owner phải xác nhận nó tương đương claim `ADMIN` hiện dùng ở #73.
2. Client tạo GET #73 với `Authorization: Bearer <token>`. Mặc định bỏ filter status/mentor/category và gửi `page=1` hoặc để server áp default. Không có API search. Không gửi `size`/`sort`.
3. Server kiểm tra JWT/role `ADMIN` trước khi parse raw query và truy cập DB. Query invalid trả 422; category có giá trị dù hợp lệ cũng bị 422 ở source hiện tại.
4. Khi được phép truy vấn, server đếm và lấy page với cùng predicates status/mentor. Local source dùng trang cố định 20, thứ tự `courses.id ASC`, join mentor, và chỉ đọc.
5. Với HTTP 200, client kiểm tra envelope/business code, đọc `data.items`/`data.pagination`, ánh xạ các field có contract, cập nhật table/pagination. `items=[]` là empty page; nếu `total>0` nhưng page ngoài phạm vi, vẫn giữ total để hiển thị trạng thái page-invalid/out-of-range thay vì kết luận không có dữ liệu.
6. Từ row chọn course, client truyền `Course.id` (int64) sang AD-07 để #74 tải detail. Không dùng field course code do response không có.
7. API 401/403/422/500 được hiển thị theo nhóm lỗi. Hành vi refresh session, retry, toast/copy và destination sau hết phiên cần theo shared auth/error contract đang có; không tự đặt.

### Trích từ DD nguồn: API #73 response/error handling

| HTTP / business code | Ý nghĩa hiện tại | Hành vi màn hình mục tiêu |
|---|---|---|
| 200 / `DESIGN_RESOURCE_RETRIEVED` | Có items hoặc `items=[]`; message có thể là “Courses retrieved.” hoặc “No courses found.” | Map allowlisted fields; phân biệt empty result và page out-of-range khi `pagination.total>0`. |
| 401 / `DESIGN_AUTHENTICATION_REQUIRED` | Thiếu/không hợp lệ Bearer/JWT theo shared guard. | Dừng render dữ liệu riêng tư; session-expired flow theo shared auth contract. |
| 403 / `DESIGN_ACCESS_DENIED` | Role không được phép. | Hiển thị forbidden theo shared error/access policy; retry policy chưa được định nghĩa. |
| 422 / `DESIGN_VALIDATION_ERROR` | Query int/page sai hoặc category filter bị từ chối. | Hiển thị lỗi gắn filter nếu có; category không được bật trong UI khi source hiện tại từ chối. |
| 500 / `DESIGN_INTERNAL_ERROR` | DB, count, orphan mentor, projection hoặc mapping lỗi. | Không hiển thị dữ liệu từng phần như thành công; báo lỗi an toàn. Retry/backoff/copy chưa được API contract xác định. |
| Network/timeout/invalid envelope | Không có business code từ response. | Giữ state theo client error policy được duyệt; không suy ra success. Retry behavior chưa được định nghĩa. |

API #73 catalog không liệt kê 404. Không có mutation, idempotency key hoặc client cache invalidation ở AD-06 list request. AC-32 yêu cầu reload list sau thao tác #75/#76/#77 ở flow liên màn hình; mutation và conflict policy thuộc AD-08/AD-09, không được đặc tả thành hành vi của nút trên mockup.

### Trích từ DD nguồn: API request/response matrix

| Thuộc tính | API #73 |
|---|---|
| Method / endpoint | `GET /api/v1/admin/courses` |
| Authentication / authorization | `Authorization: Bearer <JWT>`; catalog yêu cầu Admin; local guard kiểm tra role `ADMIN` trước raw query parse/DB. AC-32 fine-grained permission mapping chưa confirmed. |
| Path/body | Không có path params hoặc request body. |
| Query | `status?:string` (raw exact match; không enum validation); `mentor?:int64` (signed integer, không positive-only guard); `category?:int64` (format parse, giá trị hiện luôn bị reject 422 vì thiếu relation); `page?:int32` default 1, range 1..2,147,483,647. Không có `q`, `size`, `sort`. Source size cố định 20, order `courses.id ASC`. |
| Success | HTTP 200, `success`, `businessCode=DESIGN_RESOURCE_RETRIEVED`, message, `data:{items:Course[],pagination:{page,size,total,total_pages}}`, `meta`, `traceId`. |
| Course mapping | `id:int`, `title:string`, `description:string|null`, `thumbnail_url:string|null`, `price:string` (decimal exact), `status:string`, `mentor:{id:int,full_name:string,avatar_url:string|null}`. Course model không có category/course code/lesson count/KPI. |
| Errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 422 `DESIGN_VALIDATION_ERROR`; 500 `DESIGN_INTERNAL_ERROR`. API catalog không liệt kê 404. |
| Ordering/dependency | Local count query trước page query, cùng status/mentor filters; LEFT JOIN users; read-only/no commit. Không phụ thuộc một API khác. Empty/out-of-range page đều 200; out-of-range giữ total. |
| Retry/cache | API DD chưa khóa retry/timeout/cache semantics. Không có mutation/idempotency key; client retry/cache policy chưa được xác nhận. |
| Runtime evidence | API route/module/test source có trong checkout. Test report 2026-11-01 ghi 20/20 isolated HTTP requests pass sau fix nullable cast; không chứng minh live DB/deploy. API DD `Draft — Needs Confirmation`. |

## 3. API không sử dụng
- No additional API is inferred from AC-32 or the original DD. API #104 is the explicit user-approved extension documented below; other absent APIs remain gated.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/05_admin/AD-06_danh-sach-khoa-hoc-quan-tri/AD-06.md)

### Current client/API source — 2026-11-21

AD06Page requires the exact #73 success code and validates the local Course Page shape, fixed size 20, requested-page echo and safe total_pages calculation. The page then detects COUNT/LIST row-count drift, preserves Course rows, suppresses stale total/page values and allows same-page retry. Empty out-of-range pages have a page-1 recovery action, including an empty collection requested at page > 1. No query/filter or backend behavior was added; direct catalog, permission, deleted visibility and live schema gaps remain.

### Current API #104 implementation — 2026-11-22

API #104 is a user-approved extension outside the original AC_UNICA set and AC-32 flow. `POST /api/v1/admin/courses` accepts `{title:string, description?:string|null, thumbnail_url?:string|null, price:decimal-string, mentor_id:int64}` and returns HTTP 201 `DESIGN_RESOURCE_CREATED` with the shared Course projection. The server checks the selected user is an active Mentor, writes a `DRAFT` row, reads its projection and commits within one transaction. Errors: 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 422 `DESIGN_VALIDATION_ERROR`, 500 `DESIGN_INTERNAL_ERROR`.

AD-06 calls API #68 with `role=MENTOR`, `status=ACTIVE`, and paged selection for the dialog. Client only accepts the exact #104 success code plus a valid Course projection before success navigation. Focused tests on 2026-11-22: server 6/6; Angular 8/8. Tests use fakes and do not establish live DB schema or deployment. Formal Study OpenAPI remains `NOT_FOUND`; the route and catalog are source evidence, not a deployed contract.
