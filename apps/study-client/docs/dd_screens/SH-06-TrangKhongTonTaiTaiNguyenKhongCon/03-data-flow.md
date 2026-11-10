# SH-06 — Data Flow & State

## 1. Nguồn dữ liệu
| Field / object | Type | Source | Destination | Cập nhật khi |
|---|---|---|---|---|
| Chỉ liệt kê theo bằng chứng trong excerpt bên dưới | Theo DD/API source | API/inventory/design; status phải giữ nguyên | UI/state nêu ở DD nguồn | Theo event source |

## 2. State model

> Không tạo DTO/ViewModel mới khi chưa có contract. State, DTO và mapping được trích nguyên ngữ cảnh từ DD nguồn bên dưới.

## 3. API DTO → ViewModel mapping

### Trích từ DD nguồn: 2. Luồng hoạt động tổng thể

1. **Route fallback:** Router tương lai nhận pathname không khớp và hiển thị `ROUTE_404`; SH-06 không gọi API. Không echo raw URL/query vào heading hoặc thông báo.
2. **Resource detail:** Từ GS-03, client gửi API #08 với `course_id`. Nếu API trả HTTP 200 `DESIGN_RESOURCE_RETRIEVED`, lấy `data.items[0]` và pagination đã validate rồi tiếp tục GS-03. Nếu trả 404 `DESIGN_RESOURCE_NOT_FOUND`, hiển thị cùng nội dung chung `RESOURCE_404`.
3. **Không phân biệt private/draft:** API query chỉ trả course `PUBLISHED`; absent/unpublished có cùng status, business code và message. SH-06 không hiển thị course ID, draft status hoặc lý do nội bộ.
4. **Phân nhánh lỗi:** API #08 500 `DESIGN_INTERNAL_ERROR`, network/timeout, JSON parse error hoặc envelope sai đi tới service-error handling riêng. Nếu response thực tế là 403, giữ access-denied state (SH-05); API #08 hiện không tạo nhánh này.
5. **Render:** Badge/title/body chỉ phản ánh trạng thái không tìm thấy. Không hiển thị course detail, mentor, giá, thumbnail hoặc API payload ở SH-06. Safe Scope notice có thể nói hệ thống không công khai nội dung không khả dụng, nhưng không khẳng định toàn bộ sản phẩm có cơ chế ẩn draft ngoài source đã xác minh.
6. **Điều hướng:** Primary action tới GS-01 `/courses`; secondary action/logo/home tới SH-01 `/`. Header link route là proposal theo inventory. Các card course/contact/footer links chỉ hoạt động sau khi có data ID/route/channel được duyệt; không điều hướng bằng href `#`.
7. **Rời màn hình:** Tới GS-01 thì GS-01 sở hữu API #05/#06; tới SH-01 thì SH-01 sở hữu API #05/#06 theo inventory. SH-06 không gọi trước các API này để render fallback.

Quan hệ hệ thống: SH-06 hỗ trợ GS-03 khi course không tồn tại/không public và làm route fallback cho toàn Study Web. Route fallback có thể được dùng từ mọi flow nhưng nội dung 404 không tiết lộ record/ownership. 403 là SH-05 và lỗi 500/mạng thuộc service-error handling; các trạng thái không thay thế nhau.

### Trích từ DD nguồn: 5. API #08 và nguồn dữ liệu

### 5.1 `GET /api/v1/courses/{course_id}`

| Thành phần | Current source behavior |
|---|---|
| API ID/status | API #08 trong API contract tổng thể đã duyệt; API DD #08 còn `Draft — Needs Confirmation`. Dòng SH-06 ghi BE `D`, API index §5 ghi #008 `R`; current route/module/test source tồn tại (`SOURCE_BACKED`; deployment chưa xác minh). |
| Method / endpoint | `GET /api/v1/courses/{course_id}`; public, không yêu cầu Authorization/Bearer. Path `course_id` design type int64 bắt buộc; route nhận raw string rồi `validate_course_id` dùng `parse_integer`. |
| Request | Path param `course_id`; không query/body. Invalid integer path hiện trả 404 `DESIGN_RESOURCE_NOT_FOUND`, không 422. |
| Query / side effect | `FIND_PUBLISHED_COURSE_DETAIL` đọc `courses` `LEFT JOIN users m ON m.id=c.mentor_id`, filter `c.id=:course_id AND c.status='PUBLISHED'`. Read-only; không commit. SQL error gọi rollback. |
| HTTP 200 | `DESIGN_RESOURCE_RETRIEVED`; `data.items` có một course và `data.pagination={page:1,size:1,total:1,total_pages:1}`. Course fields: `id:int`, `title:string`, `description:string|null`, `thumbnail_url:string|null`, `price:string` dạng decimal, `status:string`, `mentor:{id:int,full_name:string,avatar_url:string|null}`. |
| HTTP 404 | `DESIGN_RESOURCE_NOT_FOUND`, message hiện “Published course not found.”; dùng cho ID không parse được và không có published row. Missing và non-PUBLISHED giống nhau. |
| HTTP 500 | `DESIGN_INTERNAL_ERROR`, message an toàn “Courses could not be retrieved.”; SQLAlchemy error, projection/mapping error hoặc CoursePage validation failure. API #08 hiện không trả 403. |
| Envelope / trace | Shared response envelope: `success`, `businessCode`, `message`, `data`, `meta`, `traceId`; response header `X-Trace-Id`. Không render `data` khi 404 hoặc error body thô trên SH-06. |
| DB source | [`DB.sql`](../../../../../infra/postgres/study-server/DB.sql) có bảng `courses`/`users` và các cột query dùng; `courses.mentor_id` nullable trong DDL. `map_course` yêu cầu mentor id/name, nên thiếu mentor data thành 500, không thành 404. DDL không xác minh live schema. |

Source trace: [`API route`](../../../../study-server/app/api/v1.py) → [`view.py`](../../../../study-server/app/modules/guest/api_08_courses_detail/view.py) → [`validate.py`](../../../../study-server/app/modules/guest/api_08_courses_detail/validate.py) → [`query.py`](../../../../study-server/app/modules/guest/api_08_courses_detail/query.py) → [`CoursePage/models.py`](../../../../study-server/app/modules/guest/_shared/course_catalog/models.py) + [`helpers.py`](../../../../study-server/app/modules/guest/_shared/course_catalog/helpers.py). Test source: [`test_courses_detail.py`](../../../../study-server/tests/modules/guest/api_08_courses_detail/test_courses_detail.py); test được đọc, không chạy trong phiên docs.

### 5.2 Design contract và source discrepancy

- [`API contract`](../../../../../docs/lists/list_api.md) khai báo #08 `ApiEnvelope<Page<Course>>`, 200 `DESIGN_RESOURCE_RETRIEVED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 500 `DESIGN_INTERNAL_ERROR`; file đánh dấu `APPROVED_DESIGN_CONTRACT` nhưng chưa runtime-verified. [`API DD #08`](../../../../study-server/docs/dd/08_courses_detail/02_Overview.md) vẫn ghi `Draft — Needs Confirmation`. Response Page singleton trong source khớp kiểu `data` của contract.
- [`AC-05 guest diagram`](../../../../study-server/docs/diagrams/AC_UNICA/AC_01_GUEST_ACCOUNT.drawio) có nhánh “NO → 404/403” cho course existence/publication, trong khi [`API catalog`](../../../../../docs/lists/list_api.md) ghi 404/500. Current #08 query không trả private row; cả missing/unpublished cùng trả 404; internal query/mapping failure là 500; route không có 403 branch. Đây là discrepancy cần owner xử lý trước DD READY. Nếu guard khác trả 403, giữ access-denied state riêng; không gán 403 cho #08.
- [`list_screen.md`](../../list_screen.md) SH-06 liệt kê #08 là `D`; current source tồn tại nhưng live deployment/schema chưa được xác nhận. Không nâng trạng thái thành `RUNTIME VERIFIED`.

### Trích từ DD nguồn: 7. Ma trận trạng thái và điều hướng

| State | Điều kiện vào | UI/side effect | Chuyển tiếp |
|---|---|---|---|
| `INITIAL` | Router/client bắt đầu resolve | Không render mock course data như thật | `ROUTE_404`, `RESOURCE_LOADING`, `SERVICE_ERROR` |
| `ROUTE_404` | Router không match URL | Badge/title/copy chung; không gọi API; CTA GS-01/SH-01 | Điều hướng EV-03–05 |
| `RESOURCE_LOADING` | GS-03 đang gọi #08 | Loading thuộc GS-03; không render SH-06 trước kết quả | `COURSE_READY`, `RESOURCE_404`, `FORBIDDEN`, `SERVICE_ERROR` |
| `COURSE_READY` | #08 trả HTTP 200 hợp lệ và Page có item | Tiếp tục GS-03; không ở SH-06 | GS-03 ready |
| `RESOURCE_404` | #08 trả 404 `DESIGN_RESOURCE_NOT_FOUND` | Nội dung 404 chung, không hiển thị draft/private/course ID | SH-06 actions |
| `FORBIDDEN` | Auth guard khác trả 403 | Giữ access-denied state SH-05; #08 current source không có 403 | SH-05 / safe access flow |
| `SERVICE_ERROR` | 500, network, timeout, JSON/schema failure | Error dịch vụ riêng, trace ID nếu policy cho phép; không render 404 | Shared service-error retry/navigation policy |
| `NAVIGATING` | User click internal link | Chờ router resolve, không giữ href placeholder | GS-01, SH-01, route đích đã xác nhận |
| `RECOMMENDATIONS_BLOCKED` | Chưa có quyết định về section/data source | Không dùng mock values; production disposition chưa chốt nên event chưa implementable | DD giữ `BLOCKED` đến khi Product/UX chốt |

| Từ | Điều kiện | Đến / dữ liệu truyền |
|---|---|---|
| GS-03 → SH-06 | #08 404 `DESIGN_RESOURCE_NOT_FOUND` | Error state chung; không truyền/render private course payload. |
| GS-03 → GS-03 | #08 200 Page singleton hợp lệ | Course item và route ID từ API/route đã validate. |
| Caller → SH-05 | 403 thực tế từ guard | Access-denied state; không đổi thành SH-06. |
| SH-06 → GS-01 | CTA/list link | `/courses`, không truyền course ID. |
| SH-06 → SH-01 | Home/logo | `/`, không truyền dữ liệu riêng tư. |
| #08 → service error | 500/network/timeout | State/service component riêng; không dùng thông điệp 404. |

## 4. Luồng đọc (Read)
- Orchestration từ inventory: Router 404 hoặc resource 404 chuyển state; không chuyển 500 thành 404.
- Chi tiết current/source mapping: xem [API Integration](04-api-integration.md) và DD nguồn.

## 5. Luồng ghi (Write)
- Chỉ mô tả mutation được DD/API source nêu; không thêm endpoint hoặc side effect.
- Source trace: [SH-06](../../screen_stitch/01_shared_auth_system/SH-06_trang-khong-ton-tai-tai-nguyen-khong-con/SH-06.md)

## 6. Cache / concurrency / lifecycle
- Cache, race, cleanup, pagination: xem các section source bên dưới; nếu không có bằng chứng thì để `CẦN_XÁC_NHẬN`.

## 7. Data errors & security
- Theo error/security/source-status section của DD nguồn; không coi state trong mockup là runtime behavior.

## 8. Trace
[Events](02-events.md) · [API](04-api-integration.md) · [Rules](05-business-rules.md)
