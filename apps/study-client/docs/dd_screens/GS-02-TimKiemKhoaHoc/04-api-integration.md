# GS-02 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `GS-02-API-001` | #05 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `GS-02-API-002` | #07 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #05, #07
- Orchestration/data notes: GET #5 cache-first song song #7 nếu độc lập; q được trim phía UI; #7 cố định 20/page; không gửi category. **DISCREPANCY:** AC-04/API #05 DD mô tả #05 → #07; cần chốt thứ tự/cache behavior.
- BE/source status và gate: **R**; **BLOCK:** Không khẳng định bộ lọc category đã chạy
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: 4. Đặc tả API và mapping

### 4.1. API #05 — danh mục

- Method/endpoint: public GET /api/v1/categories.
- Auth: không yêu cầu Bearer theo route source.
- Query: locale tùy chọn, kiểu string; khi bỏ qua source mặc định vi-VN. Giá trị được dùng nguyên văn để exact-match; source không trim hoặc xác thực locale syntax. Không có path/body.
- Source behavior: chọn category ACTIVE theo locale khớp chính xác, sắp xếp id ASC.
- Success: HTTP 200, business code DESIGN_RESOURCE_RETRIEVED, envelope chứa data.items và pagination. Category có id, name, slug, optional description. Empty là success; source tạo page=1, size=0, total=0, total_pages=1.
- Error: query validation trả 422; lỗi query/mapping trả safe 500 DESIGN_INTERNAL_ERROR.
- Cache/orchestration: inventory F02 yêu cầu cache-first và cho phép #07 song song nếu độc lập; AC-04 diagram/API #05 DD thể hiện #05 trước #07. Không có client cache source, TTL, invalidation, locale cache key, stale-data hoặc fallback policy; expected order cần được giải quyết.
- Quan hệ #05 → #07: metadata không cần để gọi #07 nếu category không được gửi. Có thể concurrent theo inventory khi #07 đủ điều kiện chạy; không khẳng định behavior cache/client hiện hành.

### 4.2. API #07 — tìm khóa học

- Method/endpoint: public GET /api/v1/courses/search.
- Auth: không yêu cầu Bearer theo route source.
- Query source: q optional string; page optional Python int default 1; sort optional string. Parser/model còn nhận category optional int, nhưng validator từ chối mọi giá trị non-null. `size` không được khai báo; query parameter không được khai báo (gồm size) bị FastAPI bỏ qua, không làm đổi page size.
- Validation: page phải ≥1; không có upper bound trong validator dù API catalog khai báo int32. Sort dạng `field:direction`; field hợp lệ id, name, price, created_at; direction asc, desc. Source so khớp case-sensitive và không trim sort. Invalid page/sort và category đều trả HTTP 422, business code DESIGN_VALIDATION_ERROR.
- q: trim và lowercase; chuỗi rỗng/whitespace trở thành None và bỏ predicate q. Nếu q có giá trị, query tìm LOWER(c.name) LIKE '%q%', đồng thời chỉ lấy PUBLISHED. Query parameter được bind; source không escape ký tự %/_ của LIKE.
- Ordering: mặc định created_at DESC, id ASC; sort explicit dùng builder hiện hành và tie-breaker id ASC trừ khi field sort là id. Sort input không được trim/lowercase; chỉ đúng chữ thường trong allowlist mới hợp lệ.
- Paging: DEFAULT_SIZE=20, offset (page-1)*20; không có client-selected size. Gửi size=5 không làm page size đổi thành 5.
- Query order/side effect: sau validation, source chạy COUNT trước và lấy `total` cùng `missing_mentor_count`; nếu count lỗi hoặc có PUBLISHED course thiếu mentor thì rollback/trả safe 500 và không chạy list query. Nếu hợp lệ, chạy page SELECT rồi map response. Đây là read-only flow; handler không commit.
- Success: HTTP 200, business code DESIGN_RESOURCE_RETRIEVED, data.items và data.pagination gồm page, size, total, total_pages. Empty match là items rỗng, total=0, total_pages=0. Page ngoài phạm vi là HTTP 200 với items rỗng nhưng total/total_pages giữ theo query.
- Course mapping: id, title, optional description, optional thumbnail_url, price decimal string, status, mentor gồm id, full_name, optional avatar_url. Không có category/currency/rating/duration/tags/discount/old price.
- Error: invalid query/category HTTP 422 DESIGN_VALIDATION_ERROR; query, mentor-integrity hoặc mapping failure trả safe HTTP 500 DESIGN_INTERNAL_ERROR. Mất mạng/timeout không có business code response. Retry/timeout, request cancellation, chống response cũ ghi đè state và retry policy chưa có source contract.
- API catalog trong docs/lists/list_api.md vẫn khai báo category optional và reusable Course.category; ghi đây là contract/source discrepancy. Không dùng khai báo catalog làm bằng chứng category chạy được.

### 4.3. Mapping lỗi sang UI

| Tình huống | Nguồn/điều kiện | UI mapping hiện có thể xác định |
|---|---|---|
| Loading #07 | Request đang chạy | Inventory có state loading; copy/skeleton/disable policy chưa được chỉ định. |
| Không có course | HTTP 200, items rỗng, total=0 | State no-result theo inventory; không gộp với lỗi. Exact copy/action chưa được phê duyệt. |
| Page ngoài phạm vi | HTTP 200, items rỗng, total>0 | Không hiển thị như zero catalog. Recovery (clamp page, back to first page, hay giữ URL) cần quyết định. |
| Invalid query/page/sort/category | HTTP 422, DESIGN_VALIDATION_ERROR | Category là lỗi do unsupported contract; không gửi category từ UI. Message field-level và recovery chưa có UI contract. |
| Internal API failure | HTTP 500, DESIGN_INTERNAL_ERROR | State error theo inventory. Retry action/copy chưa được phê duyệt. |
| Network/timeout | Không có envelope | Error state; retry/backoff/cancellation chưa được xác định. |
| #05 lỗi, #07 thành công | Hai request độc lập khi không dùng category | Partial rendering/failure policy chưa có. Không được giả định #07 phải bị hủy hoặc #05 lỗi che kết quả. |
| #05 thành công, #07 lỗi | Hai request độc lập | Category metadata có thể có nhưng search error; UI partial state/copy chưa được xác định. |

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/02_guest_discovery/GS-02_tim-kiem-khoa-hoc/GS-02.md)
