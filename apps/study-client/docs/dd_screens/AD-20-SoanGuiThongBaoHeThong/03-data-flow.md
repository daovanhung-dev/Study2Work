# AD-20 — Data Flow & State

> **Current source (2026-11-21):** #68 candidate pages → explicit selected IDs → #93 notification dispatch → accepted UUID → SH-07 owner-bound #18 read. Segment/draft/priority are not implemented; live runtime/provider delivery are unverified.

> **Historical Angular source snapshot (2026-11-20):** At that point the route loaded `AD20Page` with local preview only. The 2026-11-21 implementation adds #68/#93 calls and the SH-07 UUID handoff described above. The source excerpts below preserve the earlier Stitch artifact behavior.

## 1. Nguồn dữ liệu
| Field / object | Type | Source | Destination | Cập nhật khi |
|---|---|---|---|---|
| Chỉ liệt kê theo bằng chứng trong excerpt bên dưới | Theo DD/API source | API/inventory/design; status phải giữ nguyên | UI/state nêu ở DD nguồn | Theo event source |

## 2. State model

> Không tạo DTO/ViewModel mới khi chưa có contract. State, DTO và mapping được trích nguyên ngữ cảnh từ DD nguồn bên dưới.

## 3. API DTO → ViewModel mapping

### Trích từ DD nguồn: B. Luồng hoạt động tổng thể

### B.1 Luồng được thiết kế — chỉ triển khai sau khi blockers được duyệt

1. Từ AD-19, mở candidate route `/admin/notifications/new`. Kiểm tra phiên đăng nhập và permission notification-management theo contract được duyệt; route/session guard hiện không có source để xác nhận.
2. Khởi tạo form. Mockup đặt mặc định: segment “Toàn bộ người dùng”, channel In-app Feed checked, Email unchecked/disabled, priority Normal. Đây chỉ là trạng thái HTML. Chưa có API preload hoặc danh sách recipients.
3. Admin nhập title/content, chọn segment/channel và priority. Validate phía client chỉ được thêm khi Product/API xác nhận rule, đặc biệt recipient resolution, title/content limits, channel token và priority.
4. Admin chọn `Save draft` hoặc `Send now`. Contract hiện không có `action`, `status`, `scheduled_at` hay draft-create endpoint. Nút send đang disabled trong HTML. Chưa có luồng có thể chốt giữa lưu nháp và gửi.
5. Sau khi API/UX contract được duyệt, thao tác gửi có thể gọi #93 theo body đã thống nhất. Catalog hiện cho phép recipients? hoặc segment? nhưng không định nghĩa XOR/enum/predicate. Local runtime chỉ nhận recipients IDs và từ chối segment.
6. Xử lý response theo contract được duyệt. Catalog/AC-36 direct response là `ApiEnvelope<Notification>`; operation prose nói `Operation`; local source thêm UUID metadata. Không tự chọn response adapter hoặc tự chuyển `notification.id` thành operation ID.
7. Chỉ hiển thị trạng thái `accepted` nếu nhận được response 202 theo approved contract. Không đổi thành `sent/delivered` khi chưa có status từ backend.
8. Chỉ điều hướng sang SH-07 khi operation field/type, API #18 path, ownership, status lifecycle và Study runtime được đồng bộ. Hiện handoff bị block. AD-21 cũng chưa có detail GET riêng theo inventory.
9. Khi lỗi, giữ input để người dùng xử lý lại chỉ theo retry rule được duyệt. Không tự retry mutation; API #93 không khai báo idempotency key hoặc retry guarantee.

### B.2 Hành vi hiện tại của prototype

1. Historical Stitch behavior: browser tải design artifact HTML tĩnh, không phải Angular route. Current app has a route/page; auth guard, API preload and browser runtime are not verified.
2. `input` ở title/body được trim để cập nhật preview text. Nếu rỗng, script đặt lại sample copy; dữ liệu form không được gửi đi.
3. Các radio/checkbox chỉ đổi native selection. Toolbar buttons không format nội dung; textarea là plain text.
4. Save Draft không có handler. Send Now disabled và không có handler. Anchor điều hướng dùng `href="#"`.
5. Preview, Accepted/Correlation/Delivered, SMTP, RBAC, System Normal và operation-code copy đều là text tĩnh, không bind response/runtime state.

### Trích từ DD nguồn: E. Ma trận trạng thái và điều hướng

| State | Điều kiện / UI | Hành động và next state | Trạng thái evidence |
|---|---|---|---|
| `ROUTE_PAGE_SOURCE_WIRED` | Angular router maps `/admin/notifications/new` to `AD20Page`; current source also calls #68 and #93 and hands accepted UUID to SH-07. | Route/page and focused API flow are source-wired; auth/browser runtime is not verified. | Current source |
| `INITIAL_STATIC` | Artifact render; `all`, `app`, `normal` checked; title/body rỗng; preview sample; Send disabled. | Input title/body → `PREVIEW_EDITING`; radio/checkbox đổi native DOM state. | Prototype current, không phải runtime |
| `PREVIEW_EDITING` | Title/body listener chạy trong HTML. | Trim và thay preview text; blank → sample fallback; không gọi API. | Prototype current |
| `AUDIENCE_OR_CHANNEL_SELECTED` | Browser native selection đổi. | Không có recipient resolution, enum validation, count hay server request. | Prototype current |
| `DRAFT_BLOCKED` | Save Draft không có handler/API. | Không có persistence/confirmation; giữ page. | Blocked |
| `SEND_BLOCKED` | Send button disabled; request contract/mapping chưa được duyệt. | Không submit; không loading/202/error. | Blocked |
| `SUBMITTING` | Chỉ là state tương lai nếu #93 contract + UI được duyệt. | Chống double-submit, timeout, retry behavior chưa có nguồn; cần định nghĩa trước implementation. | Not implemented |
| `ACCEPTED` | Chỉ khi API approved contract trả 202 và body parse hợp lệ. | Hiển thị accepted, giữ `delivered=false`; route tiếp phụ thuộc approved operation bridge. | Catalog expected; current UI không gọi |
| `DELIVERED` | Cần delivery status response/provider evidence. | Không thể suy ra từ 202, `QUEUED` hay thời gian trôi qua. API #96/worker relationship cần xác nhận. | Not verified |
| `VALIDATION_ERROR` | API #93 422 theo contract/fallback. | Client field-error mapping chưa implement; page không gọi #93. | API source response exists; caller/UI mapping absent |
| `UNAUTHORIZED` / `FORBIDDEN` | API #93 401/403; route guard behavior not verified. | Client session/permission handling chưa được xác minh; page không gọi #93. | API source; runtime not verified |
| `DEPENDENCY_ERROR` / `SERVER_ERROR` | API #93 503/500. | Hiển thị retry/manual recovery chỉ theo approved policy; không auto retry mutation. | API source fallback; client policy absent |
| `OPERATION_UNRESOLVED` | Response #93 shape/ID không thể map sang #18. | Không poll/route SH-07; giữ accepted result theo approved contract hoặc show blocked state. | Current design blocker |

### Navigation/data transfer

- **AD-19 → AD-20:** Current AD-19 Angular CTA uses `/admin/notifications/new`; the route maps to `AD20Page`. The historical Stitch CTA uses `/admin/notifications/create`. Current AD-20 return links use `/admin/notifications`.
- **AD-20 → AD-21:** Không mở AD-21 từ UUID metadata. API #94–#96 dùng notification-specific IDs/status contracts; direct notification ID field và response mapping cần được phê duyệt cho detail view.
- **AD-20 → SH-07:** Chỉ sau khi response `operation_id`, catalog/local UUID-vs-int64 contract, ownership policy và lifecycle mapping thống nhất. A local #18 notification-only handler exists, but AD-20 does not call it or pass an operation ID.
- **Session/security:** Expected Admin permission từ AC-36; local #93 shared role `ADMIN`; route auth/session expiry behavior chưa được triển khai ở Study Web. Không trust role/owner từ client state.

## 4. Luồng đọc (Read)
- Orchestration từ inventory: POST #93; chỉ sang SH-07 nếu operation response field/type và #18 mapping được duyệt. Catalog/AC-36 trả Notification; tracking prose nói Operation; local source trả Notification đầu tiên và derived `meta.operation_id:UUID`.
- Chi tiết current/source mapping: xem [API Integration](04-api-integration.md) và DD nguồn.

## 5. Luồng ghi (Write)
- Chỉ mô tả mutation được DD/API source nêu; không thêm endpoint hoặc side effect.
- Source trace: [AD-20](../../screen_stitch/05_admin/AD-20_soan-gui-thong-bao-he-thong/AD-20.md)

## 6. Cache / concurrency / lifecycle
- Cache, race, cleanup, pagination: xem các section source bên dưới; nếu không có bằng chứng thì để `CẦN_XÁC_NHẬN`.

## 7. Data errors & security
- Theo error/security/source-status section của DD nguồn; không coi state trong mockup là runtime behavior.

## 8. Trace
[Events](02-events.md) · [API](04-api-integration.md) · [Rules](05-business-rules.md)
