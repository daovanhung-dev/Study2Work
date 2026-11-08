# GS-04 — Data Flow & State

## 1. Nguồn dữ liệu
| Field / object | Type | Source | Destination | Cập nhật khi |
|---|---|---|---|---|
| Chỉ liệt kê theo bằng chứng trong excerpt bên dưới | Theo DD/API source | API/inventory/design; status phải giữ nguyên | UI/state nêu ở DD nguồn | Theo event source |

## 2. State model

> Không tạo DTO/ViewModel mới khi chưa có contract. State, DTO và mapping được trích nguyên ngữ cảnh từ DD nguồn bên dưới.

## 3. API DTO → ViewModel mapping

### Trích từ DD nguồn: C. Luồng màn hình

### C.1 Expected flow — chưa được triển khai trong Study Web

1. Từ GS-03, mở route đề xuất `/courses/:courseId?tab=curriculum`, giữ nguyên `courseId`. Route direct-entry cũng cần có behavior, nhưng inventory chưa quy định cách lấy course detail khi không có cache.
2. Inventory yêu cầu reuse #08 từ cache rồi gọi #09. Chưa có cache key, freshness, invalidation, cache-miss, stale course hoặc refetch policy. AC-05 gọi #09 eager cùng #08/#10; F02 gọi #09 khi user chọn tab. Giữ cả hai nguồn như discrepancy, không tự chọn thứ tự. Contract khai báo `course_id:int64`, nhưng current route nhận `str` và parser không enforce signed int64/positive range.
3. #09 hiện là public GET không auth/body/query. Backend kiểm tra course PUBLISHED, sau đó trả danh sách lesson PUBLISHED theo `sort_order ASC, id ASC`. Client đọc common envelope và `data.items`.
4. Với 200 có items, về mặt API dữ liệu có thể map theo `order`. Tuy nhiên không hiển thị/play `content` hay `video_url` cho Guest và không thêm preview badge/CTA cho tới khi Product/BE xác nhận public projection và access policy. Current response không có cờ để quyết định quyền xem.
5. Với 200 rỗng (`items=[]`), hiển thị empty state riêng sau khi có thiết kế/approved copy. Card tĩnh hiện có thể dùng làm tham khảo trực quan nhưng không chứng minh API empty response đã xảy ra.
6. Với 404/500 từ #09, phân biệt resource không tồn tại/không public với lỗi server theo backend source. Network timeout/retry, lỗi cache và stale-response handling chưa có contract; không thêm behavior giả định.
7. Nếu một ngày có bài preview, Guest open/media behavior cần một contract được duyệt riêng. F04 nói public curriculum không phải permission-based learning tree; ST-10 dùng #22 lesson access → nếu cho phép thì #23 start → #24 content. Đây là Student flow, không được tái sử dụng như Guest flow.

### C.2 Current behavior có thể xác nhận

`code.html` là document tĩnh. Nó hiển thị header, breadcrumb, heading, card rỗng, link quay lại có `href="#"`, footer. Không có JavaScript, router, route parameter, API, event handler, list item, loading/error state hay data binding. Đích của các anchor trong header/footer chỉ là literal href; browser render không chứng minh các route tồn tại. Study Web app source/router/entrypoint hiện `UNWIRED`.

### Trích từ DD nguồn: G. State và điều hướng

| State | Trigger / guard | Có trong HTML? | Expected handling |
|---|---|---:|---|
| Static empty-like | Mở `code.html` | Có | Chỉ là copy tĩnh; không chứng minh #09 response rỗng. |
| Initial/loading | Mở route và chờ prerequisite #08/cache + #09 theo orchestration được chốt | Không | Cần thiết kế loading/progress và chống stale response; chưa định nghĩa cache-miss. |
| Ready | #09 200, items > 0 | Không | Loaded lesson list design và field/access policy còn thiếu. |
| Empty | #09 200, items = 0 | Chưa xác nhận là API-linked | Tách rỗng khỏi lỗi; có thể tham khảo card tĩnh nhưng cần binding/copy approval. |
| Not found | #09 404 | Không | Resource/ID invalid hoặc course không public theo current source. Recovery/destination chưa chốt. |
| Service/network error | #09 500 hoặc transport error | Không | Cần error design; retry/timeout policy chưa có nguồn. |
| Access denied lesson | Không có Guest endpoint/state được xác minh | Không | Không tự tạo 403, preview action hoặc Student permission handoff. Private lesson không mở từ Guest. |

### Route/orchestration handoff

- GS-03 → GS-04: giữ `courseId`; inventory ghi reuse #08 cache, nhưng key/freshness/miss policy vắng mặt.
- Tab policy: F02 lazy-by-tab, AC-05 eager sequence; GS-04 inventory yêu cầu cache reuse rồi #09. Product/BE cần xác nhận source of truth và direct-entry behavior.
- GS-04 → GS-03: intended same-course route; current href `#` không chứa ID.
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
