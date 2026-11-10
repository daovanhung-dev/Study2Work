# GS-02 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `GS-02-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Tìm theo q, đồng bộ URL, debounce và reset page khi query đổi.
- Gate/status (giữ nguyên): **R**; **BLOCK:** Không khẳng định bộ lọc category đã chạy
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

### Trích từ DD nguồn: 7. Điều hướng, bảo mật và trải nghiệm

- **Screen flow:** GS-01 → GS-02 theo F02; GS-02 → GS-01 (quay lại danh sách) hoặc GS-03 khi mở course item. course.id là payload duy nhất đã được xác nhận từ #07 cho handoff. Các đường về/back-stack và URL preservation chưa được triển khai.
- **Public data:** #05/#07 là public endpoints. #07 giới hạn kết quả ở course PUBLISHED. Không thêm Bearer/session requirement vào API này từ screenshot account controls.
- **Data integrity:** dùng id và field từ response; không suy ra metadata chưa trả về. price là decimal string; currency formatting chưa có currency field trong response.
- **Input/query:** server dùng parameter binding; % và _ được giữ theo ngữ nghĩa LIKE hiện có do source không escape. Không thêm max length, client-side validation hay escaping policy không có trong contract.
- **Accessibility:** khi triển khai, input/select/checkbox/radio/button cần label và keyboard semantics tương ứng; trạng thái loading/error cần được công bố phù hợp. Source hiện tại không đủ để xác nhận WCAG/runtime implementation.
- **Responsive/design system:** annotation giữ nguyên bố cục nguồn. Responsive behavior và token mapping cần đối chiếu với [Study web design guide](../../../../../.agents/web-study/design.md); không tuyên bố prototype này phù hợp guide khi source đang lệch.
- **Runtime:** không có Study Web source/package/router/entrypoint. Chưa xác minh fetch, URL sync, debounce, cache, navigation, auth shell, responsive behavior hoặc accessibility khi chạy.

### Trích từ DD nguồn: 8. Blockers và quyết định cần bổ sung

| ID | Blocker | Bằng chứng | Cần quyết định trước implementation |
|---|---|---|---|
| GS02-B01 | Source variant và actor mismatch | screen.png là loaded state, code.html là Guest empty state; header khác actor/control. | Chọn/duyệt authoritative UI và actor/header variant. |
| GS02-B02 | Facets unsupported | #07 reject category; không có skill/duration/rating/tuition query; DDL không có relation course-category. | Backend/DB/API hỗ trợ hoặc bỏ/ẩn các filter; chốt option semantics. |
| GS02-B03 | Relevance sort unsupported | Screenshot có “Phù hợp nhất”; allowlist không có relevance. | Định nghĩa mapping/score ở API hoặc thay UI sort option. |
| GS02-B04 | Page-size conflict | Screenshot 6/page; source cố định 20/page, không có size input. | Căn chỉnh design hoặc API contract/pagination. |
| GS02-B05 | Course card fields thiếu | API không trả category, currency, rating, duration, tags, discount/old price. | Chốt data/API/schema và field formatting cho từng card. |
| GS02-B06 | Empty-query semantics | AC có thể bỏ request khi rỗng; #07 blank q trả toàn bộ PUBLISHED. | Chọn prompt/no request hay browse-all. |
| GS02-B07 | Cache/partial-load/orchestration policy | AC-04 diagram/API #05 DD thể hiện #05 → #07; inventory F02 cho phép chạy song song nếu độc lập và #05 cache-first. Study Web source/cache hiện không có. | Chốt thứ tự/cache-hit behavior, cache key, TTL, invalidation, fallback và behavior khi chỉ một API lỗi. |
| GS02-B08 | Study Web UNWIRED | Không có frontend source/package/router/entrypoint trong checkout. | Có implementation surface và route wiring trước runtime verification. |
| GS02-B09 | Extra destinations | Header account, learning path, advisor và footer không có route/service contract. | Map tới screen/service owner hoặc bỏ các control khỏi scope. |
| GS02-B10 | API page range | Catalog khai báo page int32; route dùng Python int và chỉ kiểm tra ≥1, không có upper bound. | Chốt int32 upper bound hoặc nới contract; xác định hành vi khi page/offset vượt giới hạn trước khi frontend gửi giá trị tùy ý. |

Không đóng các blocker bằng suy đoán. Đến khi các quyết định cần thiết được giải quyết, DD giữ trạng thái BLOCKED và không phải implementation-ready.

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
