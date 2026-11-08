# AD-06 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `AD-06-EV-001` | `Source heading` / EV-01 — Vào màn hình và tải danh sách | See source event detail below |
| `AD-06-EV-002` | `Source heading` / EV-02 — Nhập tìm kiếm | See source event detail below |
| `AD-06-EV-003` | `Source heading` / EV-03 — Đổi status, mentor hoặc category filter | See source event detail below |
| `AD-06-EV-004` | `Source heading` / EV-04 — Khôi phục mặc định | See source event detail below |
| `AD-06-EV-005` | `Source heading` / EV-05 — Chuyển trang | See source event detail below |
| `AD-06-EV-006` | `Source heading` / EV-06 — Mở chi tiết khóa học | See source event detail below |
| `AD-06-EV-007` | `Source heading` / EV-07 — Ánh xạ list, empty state và summary | See source event detail below |
| `AD-06-EV-008` | `Source heading` / EV-08 — Controls tĩnh, shell navigation và access/error feedback | See source event detail below |
| `AD-06-EV-009` | `Source heading` / API request/response matrix | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả chi tiết sự kiện

### EV-01 — Vào màn hình và tải danh sách

- **Trigger/type/elements:** Entry vào proposed `/admin/courses`; `Load`; shell #1–#9, heading #10–#12, table #25–#28, pagination #32–#35.
- **Điều kiện:** Auth session có Bearer JWT; AC-32 course-management permission phải được map/chốt. Local API hiện yêu cầu role `ADMIN`. Route và client chưa wired.
- **Input:** Không có path param. Query được catalog khai báo: `status?:string`, `mentor?:int64`, `category?:int64`, `page?:int32`. Default target page 1; status/mentor/category không có giá trị thì bỏ query. Không có query `q`, `size`, `sort`.
- **Xử lý mục tiêu:**
  1. Khởi tạo page 1 và các filter ở “không chọn”; không gửi `all` như status/mentor.
  2. Client gắn Authorization header theo auth client đã duyệt.
  3. Server kiểm tra Bearer/JWT + role ADMIN trước khi parse query hoặc đụng DB.
  4. Server parse mentor/category signed int64; page int32 1..2,147,483,647; category có giá trị bị reject sau parse vì thiếu relation. Status là chuỗi không whitelist.
  5. Server đếm/lấy page bằng cùng exact-match status/mentor predicates; local size 20, order `courses.id ASC`, `LEFT JOIN users` cho mentor. Read-only.
  6. Với 200 `DESIGN_RESOURCE_RETRIEVED`, validate envelope; map `items`, `pagination`. Row fields: `id`, `title`, `description?`, `thumbnail_url?`, `price` string, `status`, `mentor{id,full_name,avatar_url?}`.
  7. Render loading → ready/empty/error; không hiển thị các KPI/columns không có source. `items=[] && total=0` là empty theo query; `items=[] && total>0` là page ngoài phạm vi.
  8. Trên 401/403/422/500, network hoặc invalid envelope, không render response như thành công. Session recovery/copy/retry theo shared policy sau khi được xác nhận.
- **Current prototype:** không route/fetch; ảnh hiện static zero rows. Event chưa được implement.
- **Output:** View state cùng data/trace từ #73 nếu được nối; không mutation/cache policy được định nghĩa trong #73. Không tự retry.

### EV-02 — Nhập tìm kiếm

- **Trigger/type/elements:** Input/change/submit ở #19; current HTML chỉ là text input, không có event listener.
- **Input:** Chuỗi người dùng; placeholder tuyên bố name/code/instructor. Không có max length, normalization, escaping hoặc debounce được contract xác nhận.
- **Xử lý:** Không thể tạo request hợp lệ với #73 vì không có query search. Không gửi `q` hay nối input vào status/mentor. Giữ rõ prototype-only input; owner phải bổ sung API/contract (fields, match mode, case/accent behavior, debounce/submit, page reset) hoặc bỏ affordance.
- **Kết quả:** Current input không đổi table. Không có success/error state/API call.
- **Ngoại lệ:** Search text không được dùng để lọc client-side một page 20 items, vì làm kết quả thiếu và total sai.

### EV-03 — Đổi status, mentor hoặc category filter

- **Trigger/type/elements:** Change selects #20/#21; click/attempt trên locked category #22. Current HTML không có change listeners.
- **Input:** Status string từ select; mentor ID cần signed int64 nhưng option source chưa tồn tại; category ID. `all` hiện là UI sentinel, không phải API value.
- **Xử lý target:**
  1. Kiểm tra control enabled và giá trị theo allowlist đã được owner duyệt. Hiện chưa có approved status allowlist hoặc mentor options, do đó chưa gửi filter value.
  2. Nếu không có filter, bỏ query key. Nếu có status/mentor được duyệt, truyền nguyên giá trị theo API (status exact string, mentor int64).
  3. Reset page về 1 hay giữ page hiện tại cần được quyết định; source không định nghĩa client behavior.
  4. Không gửi category hiện thời: UI khóa. Nếu có category, current #73 trả 422 `DESIGN_VALIDATION_ERROR` (“Bộ lọc category chưa được hỗ trợ.”).
  5. Khi contract được hoàn thiện, tải lại #73 và xử lý EV-01.
- **Current behavior:** Select changes không lọc table/API; category là badge tĩnh.
- **Output/errors:** 200 cập nhật result; invalid int → 422; category → 422; 401/403/500 theo EV-01. Không tự normalize lowercase status sang uppercase.

### EV-04 — Khôi phục mặc định

- **Trigger/type/elements:** Click #24; `Click`.
- **Input:** Giá trị search/status/mentor hiện tại.
- **Current processing:** Listener trong `code.html` đặt search thành chuỗi rỗng và status/mentor thành `all`. Không reset category, không đổi URL/state bên ngoài, không fetch #73.
- **Target processing sau khi wired:** Clear các filter đã được contract chấp nhận, page target về 1 nếu owner chốt, rồi gọi lại #73 một lần. Đây là target cần quyết định, không phải current prototype behavior.
- **Kết quả:** Hiện chỉ controls đổi, summary/table giữ nguyên. Không mutation. Network/response path chỉ thuộc target EV-01.

### EV-05 — Chuyển trang

- **Trigger/type/elements:** Click previous #33/next #35, đọc indicator #34; `Click`/render.
- **Input:** `pagination.page`, `size=20`, `total`, `total_pages` từ #73; source page query là int32 tối đa 2,147,483,647. Client không gửi `size`.
- **Xử lý target:** Tính candidate page theo metadata, kiểm tra page >=1 và không vượt `total_pages` khi có dữ liệu; gọi #73 với `page`. Exact disabled/bounds rule và URL persistence chưa được contract hóa. Nếu response có empty items nhưng `total>0`, hiển thị out-of-range/stale-page state chứ không đổi total thành 0.
- **Current behavior:** Hai nút disabled, indicator hard-coded `0/0`, không event/network.
- **Lỗi:** page parse/range ngoài 1..2,147,483,647 trả 422; lỗi auth/server theo EV-01. Hành vi recovery về last valid page cần xác nhận.

### EV-06 — Mở chi tiết khóa học

- **Trigger/type/elements:** Chọn một row/action ở nhóm table #25 khi data tồn tại; `Click`. Current empty prototype không có row/action.
- **Input:** `Course.id` signed numeric/int64 từ response #73; không dùng “Mã khóa” hiển thị nếu không có contract mapping.
- **Xử lý target:** Xác thực ID có trong row response; truyền ID sang route đề xuất `/admin/courses/:courseId`; AD-07 tải #74. Giữ Admin session/access context; không dùng public GET #8. #74 response/path semantics thuộc DD AD-07.
- **Kết quả:** Điều hướng AD-07 chỉ sau khi route/navigation được wire. #73 không mutate; quay lại list/query state cần quyết định shared routing policy.
- **Lỗi/edge:** Không mở nếu row ID thiếu/invalid; destination #74 401/403/404/500 được xử lý ở AD-07. Không tạo row selection từ hard-coded mock data.

### EV-07 — Ánh xạ list, empty state và summary

- **Trigger/type/elements:** Response #73 thành công; KPI #15–#18, filter summary #23, empty #26–#28, count #32, page indicator #34, table #25.
- **Input:** `data.items[]` và `data.pagination{page,size,total,total_pages}`.
- **Xử lý:** Map row fields có source; format giá trị theo currency/locale rule sau khi product xác nhận. `items.length` là số row trong response page; `total` là tổng theo filter request. Không tính KPI bằng 20-row sample; không dựng course code/lesson count từ `id`/nội dung. Empty result, filtered empty và out-of-range page phải có copy/state riêng sau khi được duyệt.
- **Current behavior:** KPI/count/indicator hard-coded 0; empty copy gộp “no result” với “syncing”; không có response.
- **Kết quả:** Chỉ render các field API-backed. Bốn KPI/summary và table columns thiếu dữ liệu giữ blocked hoặc cần bị gỡ theo quyết định owner.

### EV-08 — Controls tĩnh, shell navigation và access/error feedback

- **Trigger/type/elements:** Click Export #13, Add #14, manual #30, policy CTA #39, header/nav/breadcrumb #1–#9, notifications #4, footer #42–#44; refresh #29; API/auth/network errors qua EV-01.
- **Input:** Click targets; với #29 không có click vì `disabled`. Không có event target/destination/API cho các nút/link còn lại.
- **Xử lý current:** Navigation anchors dùng `#`; button export/add/manual/notification không có handlers. Không mở link, không tải file, không tạo course, không sync. Disabled refresh không phát request.
- **Xử lý target:** Chỉ enable từng action khi có route/API/policy cụ thể; không map export sang API #103 (impact report), add sang API khác, sync sang #78 (content moderation), hoặc policy claim sang backend enforcement. 401 session expiry và 403 forbidden phải tuân theo shared auth/error handling sau khi cross-app contract được xác nhận.
- **Kết quả/ngoại lệ:** Current click không có kết quả sản phẩm; static badges/footer do not alter authorization state. 422 filter errors và 500 service errors không được ngụy trang thành empty.

### API request/response matrix

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

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
