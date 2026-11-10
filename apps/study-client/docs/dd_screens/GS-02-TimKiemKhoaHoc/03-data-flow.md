# GS-02 — Data Flow & State

## 1. Nguồn dữ liệu
| Field / object | Type | Source | Destination | Cập nhật khi |
|---|---|---|---|---|
| Chỉ liệt kê theo bằng chứng trong excerpt bên dưới | Theo DD/API source | API/inventory/design; status phải giữ nguyên | UI/state nêu ở DD nguồn | Theo event source |

## 2. State model

> Không tạo DTO/ViewModel mới khi chưa có contract. State, DTO và mapping được trích nguyên ngữ cảnh từ DD nguồn bên dưới.

## 3. API DTO → ViewModel mapping

### Trích từ DD nguồn: 2. Luồng tổng thể

1. Người dùng mở route proposal /courses/search hoặc quay từ GS-01. Client hiện chưa có router để thực thi route này.
2. Client đọc q từ URL nếu có. Quy tắc trim/lowercase ở UI theo F02 là expected behavior; API cũng trim/lowercase độc lập. Cách giữ nguyên văn bản gõ để hiển thị cần quyết định.
3. Nếu q rỗng, chưa gọi API #07 cho đến khi Product xác nhận hiển thị prompt hay browse toàn bộ. Đây là điểm quan trọng vì #07 với q rỗng bỏ điều kiện tên khóa học và trả tất cả course PUBLISHED.
4. **Thứ tự API cần xác nhận:** inventory F02 nói #05 cache-first và cho phép #07 chạy song song nếu độc lập; AC-04 diagram lại nối #05 trước #07, và API #05 DD ghi cache hit thì bỏ request. #07 không phụ thuộc response #05 khi không gửi category, nhưng không có Study Web source để xác nhận thứ tự, cache hit/miss, TTL, invalidation, fallback hoặc partial-load. Không mô tả một phương án là runtime hiện hành.
5. Khi gọi #07, client gửi q đã chuẩn hóa cùng page/sort được hỗ trợ. Không gửi category: #07 trả 422 với category khác null; không gửi tham số skill, duration, rating, tuition hoặc size vì source không hỗ trợ chúng.
6. Client kiểm tra HTTP status, business code, envelope và pagination. HTTP 200 với items=[] là kết quả hợp lệ; nếu total=0 thì không có kết quả. Nếu total>0 nhưng trang hiện tại rỗng, đây là trang ngoài phạm vi chứ không phải danh mục rỗng.
7. Dữ liệu card chỉ được ánh xạ từ response #07. Không tự điền rating, tag, duration, currency, giảm giá hoặc giá cũ từ mockup.
8. Khi người dùng chọn một kết quả, route GS-03 dự kiến nhận course.id từ item. Không lấy ID từ nội dung mockup; ảnh mẫu không ánh xạ được với dữ liệu API.
9. Mọi lỗi mạng, lỗi API, lỗi danh mục và policy partial-load cần được thể hiện tách biệt. Copy, retry và khả năng tiếp tục khi #05 lỗi chưa được xác định.

### Trích từ DD nguồn: 6. Ma trận trạng thái

| State | Điều kiện vào | Dữ liệu/UI | Chuyển tiếp |
|---|---|---|---|
| INITIAL_OR_PROMPT | Mở route với q vắng/rỗng | Prompt nhập từ khóa hoặc browse-all decision. Không gọi #07 cho tới khi empty-q policy được chốt. | EV-02/EV-04 → LOADING nếu query đủ điều kiện; nếu không, giữ prompt. |
| TYPING | Người dùng sửa q | Giá trị input local; expected debounce và URL sync, chưa runtime. | Hết debounce/submit → LOADING; clear → INITIAL_OR_PROMPT hoặc browse-all theo policy. |
| LOADING | #07 đang chờ; #05 có thể độc lập | Loading visual theo design chưa được mô tả đầy đủ; không hiển thị stale response như dữ liệu mới nếu chưa xác định cancellation/order. | HTTP 200 có item → READY; 200 empty total=0 → NO_RESULT; page empty total>0 → OUT_OF_RANGE; validation/internal/network → ERROR. |
| READY | #07 HTTP 200 và items không rỗng | Card fields chỉ từ Course response; pagination page size 20. Unsupported facets/card fields không được render như dữ liệu thật. | Search/sort/page change → LOADING; mở card → GS-03 proposal. |
| NO_RESULT | #07 HTTP 200, items=[], total=0 | Empty result state; exact copy/recovery chưa được chốt. Tách khỏi lỗi. | Đổi q/clear/submit → theo EV-02–04. |
| OUT_OF_RANGE | #07 HTTP 200, items=[], total>0 | Trang hiện tại ngoài phạm vi; không hiển thị như không có course. Recovery policy chưa xác định. | Page change/recovery action cần quyết định. |
| ERROR | API 422/500 hoặc network failure | Error theo status/business code; không giả làm empty state. Retry/copy chưa có UI contract. | Retry hoặc sửa input theo policy cần quyết định. |
| CATEGORY_METADATA_ERROR | #05 lỗi | Metadata categories không thể hiển thị/refresh; effect lên search independent unresolved. | Partial UI/continue/block policy cần quyết định; không suy ra #07 phải dừng nếu không cần category. |
| FILTER_SELECTION_UNSUPPORTED | Người dùng thay đổi facet | UI control có selection nhưng không thể áp dụng với current API. State này chỉ biểu thị blocker; không được đưa thành filtered result. | Clear/reset policy hoặc backend/design update. |

## 4. Luồng đọc (Read)
- Orchestration từ inventory: GET #5 cache-first song song #7 nếu độc lập; q được trim phía UI; #7 cố định 20/page; không gửi category. **DISCREPANCY:** AC-04/API #05 DD mô tả #05 → #07; cần chốt thứ tự/cache behavior.
- Chi tiết current/source mapping: xem [API Integration](04-api-integration.md) và DD nguồn.

## 5. Luồng ghi (Write)
- Chỉ mô tả mutation được DD/API source nêu; không thêm endpoint hoặc side effect.
- Source trace: [GS-02](../../screen_stitch/02_guest_discovery/GS-02_tim-kiem-khoa-hoc/GS-02.md)

## 6. Cache / concurrency / lifecycle
- Cache, race, cleanup, pagination: xem các section source bên dưới; nếu không có bằng chứng thì để `CẦN_XÁC_NHẬN`.

## 7. Data errors & security
- Theo error/security/source-status section của DD nguồn; không coi state trong mockup là runtime behavior.

## 8. Trace
[Events](02-events.md) · [API](04-api-integration.md) · [Rules](05-business-rules.md)
