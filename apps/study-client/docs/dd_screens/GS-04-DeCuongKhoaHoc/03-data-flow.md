# GS-04 — Data Flow & State

## 1. Nguồn dữ liệu
| Field / object | Type | Source | Destination | Cập nhật khi |
|---|---|---|---|---|
| Chỉ liệt kê theo bằng chứng trong excerpt bên dưới | Theo DD/API source | API/inventory/design; status phải giữ nguyên | UI/state nêu ở DD nguồn | Theo event source |

## 2. State model

> Không tạo DTO/ViewModel mới khi chưa có contract. State, DTO và mapping được trích nguyên ngữ cảnh từ DD nguồn bên dưới.

## 3. API DTO → ViewModel mapping

### Trích từ DD nguồn: C. Luồng màn hình

### C.1 Expected flow and partial current implementation

1. Từ GS-03, mở route đề xuất `/courses/:courseId?tab=curriculum`, giữ nguyên `courseId`. Route direct-entry cũng cần có behavior, nhưng inventory chưa quy định cách lấy course detail khi không có cache.
2. Inventory yêu cầu reuse #08 từ cache rồi gọi #09. Chưa có cache key, freshness, invalidation, cache-miss, stale course hoặc refetch policy. AC-05 gọi #09 eager cùng #08/#10; F02 gọi #09 khi user chọn tab. Giữ cả hai nguồn như discrepancy, không tự chọn thứ tự. Client giữ `courseId` dạng string; current #09 backend validator enforce signed-int64 bounds.
3. #09 hiện là public GET không auth/body/query. Backend kiểm tra course PUBLISHED, sau đó trả danh sách lesson PUBLISHED theo `sort_order ASC, id ASC`. Client đọc common envelope và `data.items`.
4. Với 200 có items, về mặt API dữ liệu có thể map theo `order`. Tuy nhiên không hiển thị/play `content` hay `video_url` cho Guest và không thêm preview badge/CTA cho tới khi Product/BE xác nhận public projection và access policy. Current response không có cờ để quyết định quyền xem.
5. Với 200 rỗng (`items=[]`), hiển thị empty state riêng sau khi có thiết kế/approved copy. Card tĩnh hiện có thể dùng làm tham khảo trực quan nhưng không chứng minh API empty response đã xảy ra.
6. Với 404/500 từ #09, phân biệt resource không tồn tại/không public với lỗi server theo backend source. Network timeout/retry, lỗi cache và stale-response handling chưa có contract; không thêm behavior giả định.
7. Nếu một ngày có bài preview, Guest open/media behavior cần một contract được duyệt riêng. F04 nói public curriculum không phải permission-based learning tree; ST-10 dùng #22 lesson access → nếu cho phép thì #23 start → #24 content. Đây là Student flow, không được tái sử dụng như Guest flow.

### C.2 Current behavior có thể xác nhận

`code.html` remains a static asset with literal `href="#"` anchors and no route/API handlers. Current Angular Guest route maps `/courses/:courseId` to GS03Page; its `tab=curriculum` view validates the course with #08, calls #09 lazily, and mounts a GS04 panel that projects title/order only. Focused Angular tests/build pass; browser/live API/DB runtime is unverified.

### Trích từ DD nguồn: G. State và điều hướng

| State | Trigger / guard | Có trong HTML? | Expected handling |
|---|---|---:|---|
| Static empty-like | Mở `code.html` | Có | Chỉ là copy tĩnh; không chứng minh #09 response rỗng. |
| Initial/loading | Direct-entry requests #08; if published and tab is curriculum, then #09 | Yes | Current source has loading state and cancels stale #09 requests; no cache/retry exists and loaded UI remains derived. |
| Ready | #09 200, items > 0 | Không | Loaded lesson list design và field/access policy còn thiếu. |
| Empty | #09 200, items = 0 | Chưa xác nhận là API-linked | Tách rỗng khỏi lỗi; có thể tham khảo card tĩnh nhưng cần binding/copy approval. |
| Not found | #09 404 | Không | Resource/ID invalid hoặc course không public theo current source. Recovery/destination chưa chốt. |
| Service/network error | #09 500 hoặc transport error | Không | Cần error design; retry/timeout policy chưa có nguồn. |
| Access denied lesson | Không có Guest endpoint/state được xác minh | Không | Không tự tạo 403, preview action hoặc Student permission handoff. Private lesson không mở từ Guest. |

### Route/orchestration handoff

- GS-03 → GS-04: current source preserves `courseId` as text and uses `?tab=curriculum`; inventory requests #08 cache reuse, but key/freshness/miss policy are absent and no client cache is implemented.
- Tab policy: current source follows F02 lazy-by-tab and direct-entry #08 → #09; AC-05 eager sequence and cache reuse still need Product/BE confirmation.
- GS-04 → GS-03: select the Overview tab on the same GS03 route; current static prototype href remains `#`.
- GS-04 → ST-10: không phải Guest navigation. Chỉ Student flow được inventory nêu qua #22 lesson access → #23 start → #24 content.

## 4. Luồng đọc (Read)
- Orchestration từ inventory: Tái dùng #8 từ cache → GET #9; phân biệt empty curriculum và lỗi.
- Chi tiết current/source mapping: xem [API Integration](04-api-integration.md) và DD nguồn.

## 5. Luồng ghi (Write)
- Chỉ mô tả mutation được DD/API source nêu; không thêm endpoint hoặc side effect.
- Source trace: [GS-04](../../screen_stitch/02_guest_discovery/GS-04_de-cuong-khoa-hoc/GS-04.md)

## 6. Cache / concurrency / lifecycle
- Cache, race, cleanup, pagination: xem các section source bên dưới; nếu không có bằng chứng thì để `CẦN_XÁC_NHẬN`.

## 7. Data errors & security
- Theo error/security/source-status section của DD nguồn; không coi state trong mockup là runtime behavior.

## 8. Trace
[Events](02-events.md) · [API](04-api-integration.md) · [Rules](05-business-rules.md)
