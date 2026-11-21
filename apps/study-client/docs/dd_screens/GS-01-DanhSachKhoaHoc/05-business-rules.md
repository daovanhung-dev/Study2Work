# GS-01 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `GS-01-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Grid/list khóa học public; sort, paging, số kết quả, thao tác xem chi tiết.
- Gate/status (giữ nguyên): **R**; **BLOCK:** Category chỉ hiển thị metadata; filter category chưa hoạt động
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

### Trích từ DD nguồn: 7. Bảo mật, dữ liệu và khả năng tiếp cận

- #05/#06 là public routes theo API registration; không gửi token, PII hoặc dữ liệu người dùng trong request này. Chỉ hiển thị course public do backend filter `status='PUBLISHED'`; không tự hiển thị draft/private course.
- Category ID không được gửi vì validator #06 hiện trả 422 và DDL được kiểm tra không có relation course-category. `category` hiện diện trong query model/catalog nhưng không có runtime support.
- `price` trả về dạng decimal string, nhưng response không chứa currency. Không gắn ký hiệu tiền tệ hoặc định dạng price theo currency khi chưa có quyết định/dữ liệu currency. `status` có trong response; copy/label card chưa định nghĩa.
- Hướng dẫn UI Study yêu cầu semantic controls, keyboard focus rõ, tương phản có nghĩa và vùng nội dung thích ứng. Ảnh/prototype chưa đủ để xác minh keyboard, screen reader, responsive behavior, focus order hoặc contrast; font/CDN trong HTML lệch hướng dẫn. Không đánh dấu accessibility/runtime verified.

### Trích từ DD nguồn: 8. Blockers và quyết định cần xác nhận

1. **GS01-B01 — Loaded-state design:** thiếu layout/card, category UI, sort, count và pagination dù inventory/AC yêu cầu. Cần Product/Design duyệt loaded state, card fields và controls; chưa đạt DD READY.
2. **GS01-B02 — Category filter/API/DB:** API declaration và model có `category`, current validator từ chối mọi giá trị non-null bằng 422; checked-in Study DDL không có relation course-category. Backend/DB phải xác nhận relation, filter/count semantics và migration trước khi bật control.
3. **GS01-B03 — Search handoff:** cần quyết định input nào là canonical, query rỗng, trim/case, Enter/click, URL sync và GS-01 → GS-02. Không dùng fake count hoặc gọi #07 từ GS-01.
4. **GS01-B04 — Cache/partial-load policy:** inventory nói #05 cache-first rồi #06; chưa có cache source, TTL, invalidation, network fallback hoặc policy khi #05 lỗi. Cần chốt có tiếp tục #06/hiển thị partial state hay dừng.
5. **GS01-B05 — Course shape/display:** API #06 hiện không trả `category`, currency, rating, duration hoặc lesson count; reusable catalog `Course` khai báo optional category. Cần align schema và card display fields/price formatting.
6. **GS01-B06 — Empty-page/error UX:** API #06 dùng 200 + empty items cho catalog rỗng và page ngoài phạm vi. Cần chốt recovery cho empty page và copy/network/error behavior; không gộp vào empty catalog.
7. **GS01-B07 — Study Web wiring:** editable app source/package/router/entrypoint không có trong checkout. Context entry/index hiện tồn tại và registry ghi `study-web: UNWIRED`; đây không phải runtime implementation. Route, cache, event handlers, accessibility và navigation đều chưa runtime verified.
8. **GS01-B08 — Source mismatch:** PNG không có header brand/nav mà HTML lại có brand và markup trùng; HTML còn script hỏng và font/CDN drift. Product/Design cần chốt source-of-truth và sửa prototype trong nguồn quản lý, không sửa source asset trong DD này.

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
