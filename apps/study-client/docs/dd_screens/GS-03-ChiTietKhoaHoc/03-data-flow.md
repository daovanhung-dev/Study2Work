# GS-03 — Data Flow & State

## 1. Nguồn dữ liệu
| Field / object | Type | Source | Destination | Cập nhật khi |
|---|---|---|---|---|
| Chỉ liệt kê theo bằng chứng trong excerpt bên dưới | Theo DD/API source | API/inventory/design; status phải giữ nguyên | UI/state nêu ở DD nguồn | Theo event source |

## 2. State model

> Không tạo DTO/ViewModel mới khi chưa có contract. State, DTO và mapping được trích nguyên ngữ cảnh từ DD nguồn bên dưới.

## 3. API DTO → ViewModel mapping

### Trích từ DD nguồn: B. Luồng hoạt động tổng thể

### Luồng expected — chưa được UI runtime triển khai

1. User mở route đề xuất `/courses/:courseId` từ card/list ở GS-01 hoặc GS-02. Giá trị `courseId` phải giữ nguyên khi điều hướng sang detail và các tab liên quan.
2. Client cần đọc, parse và kiểm tra path value. API #08 source hiện nhận raw string; shared `parse_integer` kiểm tra cú pháp integer, nhưng không enforce signed int64 hay positive range. `parse_integer` thất bại thì trả 404; giá trị vượt int64 có thể đi tới truy vấn DB và đường lỗi cần được xác nhận trước khi triển khai. Contract `course_id:int64` và validator hiện hành chưa thống nhất.
3. Khi #08 được gọi, endpoint là public, GET không có body và không cần Bearer token. Current backend query chỉ chọn course `PUBLISHED` và LEFT JOIN summary mentor.
4. Với 200, client phải kiểm tra envelope, `businessCode = DESIGN_RESOURCE_RETRIEVED`, rồi đọc đúng phần tử duy nhất `data.items[0]`. Không lấy course từ một object `data` trực tiếp; source trả `CoursePage` với pagination singleton. API source không định nghĩa currency, rating, category, duration, tag hoặc old price.
5. Chỉ sau khi course đã được xác nhận public mới được tải tab data. Inventory F02 quy định #09/#10 lazy theo lần chọn tab. AC-05 mô tả cả ba GET tuần tự ngay trên page load; Product/BE phải xác nhận thứ tự trước khi implementation. DD chưa khẳng định orchestration đã được chốt.
6. Tab curriculum dùng #09 current source; response rỗng là success riêng, không phải lỗi. Tab reviews chưa thể gọi #10 vì endpoint chưa được nối và contract thiếu nguồn title/rating.
7. CTA ghi danh chưa tồn tại trong source HTML. Inventory chỉ liên kết ST-04. Guest/auth handoff và API #15 identity conflict phải được giải quyết trước khi xác định action thực tế; không hiển thị trạng thái đã ghi danh hoặc thành công dựa trên giá.
8. User có thể dùng các anchor static về `/`, `/courses`, `/login`, `/register`; HTML không chứng minh các URL này được Study Web router phục vụ.

### Luồng hiện tại có thể quan sát

`code.html` là document tĩnh. Khi browser mở file, nó trình bày nav, breadcrumb, H1, tab “Tổng quan” active, hai tab bị disable, thông báo unavailable và link quay lại `/courses`; không thực hiện bước lấy path, authentication, API, state update hay điều hướng JS. Browser render tạo ở phiên này chỉ xác minh HTML/CSS render được, không xác minh ứng dụng Study chạy.

### Trích từ DD nguồn: F. Ma trận trạng thái và điều hướng

| State | Trigger/guard | UI hiện có? | Expected output / transition |
|---|---|---:|---|
| Static unavailable | Browser mở `code.html`; đây là state duy nhất có trong tài sản | Có | Tab Tổng quan active, curriculum/reviews disabled, unavailable copy và return link. Không phản ánh API response cụ thể. |
| Initial/loading | Mở route `/courses/:courseId` và chờ #08 | Không | Inventory yêu cầu loading; cần thiết kế skeleton/feedback và request lifecycle. |
| Detail ready | #08 trả 200 PUBLISHED | Không | Cần bổ sung layout course/mentor/price; không có hình source. Từ đây quyết định tab calls theo orchestration được duyệt. |
| Course not found | #08 trả 404 | Không | Inventory gọi course-404; AC-05 còn nêu 403 nhưng current #08 dùng 404 cho invalid/missing/unpublished. Error page/content chưa chốt. |
| Detail service/network error | #08 trả 500 hoặc network failure | Không | Cần UI state, retry/timeout policy; không có behavior source. |
| Curriculum loading/ready | User chọn tab sau khi detail public, nếu lazy flow được duyệt | Không; tab disabled | #09 items map theo `order`. Không thể suy ra khả năng mở lesson. |
| Curriculum empty | #09 trả 200, `items=[]`, total=0 | Không | Tách empty curriculum khỏi failure; visual copy/action chưa có source. |
| Curriculum error | #09 404/500 | Không | Phân biệt stale course 404 và service error; UI fallback chưa được thiết kế. |
| Reviews loading/ready/empty/error | Chỉ sau khi API #10 được wired/contract xong | Không; tab disabled | Hiện không thể tải, dựng review card, rating average hoặc rating filter. |
| Enrollment handoff | Sau khi CTA/auth/identity policy được duyệt | Không | ST-04 route đề xuất `/student/enroll/:courseId`; enrollment status #15 đang G-01 blocked. |

### Điều hướng và giữ dữ liệu

- GS-01/GS-02 → GS-03: giữ `courseId` làm path segment; nguồn hiện tại không chứng minh card route/parameter mapping ở runtime.
- GS-03 → GS-04/GS-05: `list_screen.md` đề xuất query `?tab=curriculum`/`?tab=reviews`; AC-05 và F02 khác về thời điểm gọi API. Chưa có URL sync/handler trong HTML.
- GS-03 → GS-06: tab tài nguyên liên quan theo inventory/AC-06, không có tab resources trong source HTML GS-03 hiện tại; không thêm marker hoặc event cho đến khi thiết kế được xác nhận.
- GS-03 → ST-04: inventory đề xuất CTA enrollment và route ST-04 `/student/enroll/:courseId`; guest/auth transfer, return route, token behavior và #15 identity chưa chốt. Không khẳng định tự login/redirect.
- Header/footer links: href literals liệt kê ở `GS03-EV-05`; actual route resolution chưa được kiểm chứng.

## 4. Luồng đọc (Read)
- Orchestration từ inventory: GET #8 để xác định published → lazy GET #9 và #10 theo tab; course ID thống nhất.
- Chi tiết current/source mapping: xem [API Integration](04-api-integration.md) và DD nguồn.

## 5. Luồng ghi (Write)
- Chỉ mô tả mutation được DD/API source nêu; không thêm endpoint hoặc side effect.
- Source trace: [GS-03](../../screen_stitch/02_guest_discovery/GS-03_chi-tiet-khoa-hoc/GS-03.md)

## 6. Cache / concurrency / lifecycle
- Cache, race, cleanup, pagination: xem các section source bên dưới; nếu không có bằng chứng thì để `CẦN_XÁC_NHẬN`.

## 7. Data errors & security
- Theo error/security/source-status section của DD nguồn; không coi state trong mockup là runtime behavior.

## 8. Trace
[Events](02-events.md) · [API](04-api-integration.md) · [Rules](05-business-rules.md)
