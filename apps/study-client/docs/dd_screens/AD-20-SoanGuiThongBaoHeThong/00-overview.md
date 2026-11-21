# AD-20 — Soạn/gửi thông báo hệ thống · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `AD-20` |
| Module | Admin |
| Route | `/admin/notifications/new` — Angular route/page calls #68 for recipients and #93 for dispatch; accepted UUID routes to SH-07; runtime/auth guard behavior not verified |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | The approved producer slice is source-wired: explicit recipients from #68, text/channel dispatch through #93, then UUID handoff to SH-07. The wider design remains Draft; segment audience, provider delivery and live runtime are not established. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.3 / 2026-11-21 |
| Nguồn đối chiếu | [AD-20.md](../../screen_stitch/05_admin/AD-20_soan-gui-thong-bao-he-thong/AD-20.md), [AD-20_PLAN.md](../../screen_stitch/05_admin/AD-20_soan-gui-thong-bao-he-thong/AD-20_PLAN.md), [AD-20_markers.json](../../screen_stitch/05_admin/AD-20_soan-gui-thong-bao-he-thong/AD-20_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Chọn recipients/segment, channels, preview và xác nhận; accepted không có nghĩa đã delivered.
- In-scope: Load recipient pages through #68, require explicit user selection, submit title/text/channels to #93, and route the accepted UUID to notification-only SH-07/#18. No segment-based audience is implemented.
- Out-of-scope: Không suy ra auth behavior, API delivery, live schema, provider delivery hoặc runtime từ route/page source.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-36 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Chọn recipients/segment, channels, preview và xác nhận; accepted không có nghĩa đã delivered. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #93
- Liên kết màn hình dự kiến: [AD-21](../AD-21-SuaKiemSoatDoTrangThaiThongBao/00-overview.md), [SH-07](../SH-07-TheoDoiTacVuBatDongBo/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | unwired/initial/editing/preview/draft-blocked/send-blocked/accepted/validation-error/unauthorized/forbidden/dependency-error/server-error/operation-unresolved |
| Current source state | Angular route/page, recipient API, dispatch caller and focused specs | `SOURCE_WIRED; LIVE RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [AD-20 source screen.png](../../screen_stitch/05_admin/AD-20_soan-gui-thong-bao-he-thong/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/05_admin/AD-20_soan-gui-thong-bao-he-thong/screen_annotated.png))
- Luồng hiện tại: AD-20 pages API #68, lets the administrator select explicit recipient IDs, submits text and explicit `PUSH`/`EMAIL` channels through #93, accepts only the expected HTTP 202 queued response with `meta.operation_id` UUID, then routes to SH-07/#18. No segment selection is offered. Queue acceptance is not delivery.
- Priority: P1; #68 recipient loading, #93 send caller and SH-07 handoff are source-wired and covered by focused tests. API #18 UUID/owner lookup and API #93 text are reconciled for this notification flow. Generic campaign/segment policy, fine-grained notification permission, live schema, provider delivery and browser runtime remain outside verified scope.

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# AD-20 — Soạn và phát hành thông báo toàn hệ thống

> **Original source-DD status:** `BLOCKED` for the broader segment/campaign, draft, permission and delivery design; this historical design state does not describe the current Angular caller.
> **Current DD-safe implementation (2026-11-21):** `100% static` for the explicit-recipient slice: #68 selection → #93 dispatch → accepted UUID handoff to SH-07/#18. The API #93 DD resolves this handoff for AD-20 only. Segment, draft, priority and provider delivery remain outside this slice.
> **Runtime status:** `RUNTIME NOT VERIFIED` for an authenticated browser, live API/DB, schema deployment and provider delivery.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | AD-20 — Soạn/gửi thông báo hệ thống |
| Mục tiêu | Cho Admin soạn nội dung thông báo và chọn nhóm người nhận/kênh trước khi xác nhận phát hành, theo mục đích trong inventory và AC-36. Các card Accepted/Correlation/Delivered trong mockup là copy tĩnh, không chứng minh lifecycle runtime. |
| Actor / quyền dự kiến | Admin có `notification-management` permission theo AC-36. |
| Route | `/admin/notifications/new` hiện được Angular admin router khai báo và trỏ tới `AD20Page`; browser/runtime/auth guard behavior chưa xác minh. |
| Màn hình liên kết | AD-19 là entry/đường quay lại source-wired; AD-21 là màn hình liên quan đến kiểm soát/trạng thái; AD-20 hiện chuyển operation UUID accepted tới SH-07 cho notification-only lookup. |
| Tiền điều kiện | User đã đăng nhập và được phép quản trị notification theo AC-36. Quy tắc permission cụ thể chưa được thống nhất với role `ADMIN` mà API #93 hiện kiểm tra. |
| Hậu điều kiện | AC-36 mô tả Notification/recipients và nhánh gửi Push/Email có điều kiện. API #93 catalog trả HTTP 202; 202 chỉ là accepted, không đồng nghĩa delivered. Response, recipient grain và cách theo dõi operation còn mâu thuẫn/chưa duyệt. |
| Dữ liệu chính | Catalog #93: `recipients?: int64[]`, `segment?: AudienceSegment`, `title`, `content`, `channels[]`; response `ApiEnvelope<Notification>`. Mockup còn có priority, preview, nút draft/send và segment mẫu nhưng không chứng minh request contract. |
| API | `POST /api/v1/admin/notifications` (#93). Current source also registers `GET /api/v1/operations/{operation_id}` (#18); its notification-only query reads the same candidate `operation_id` UUID and binds the authenticated sender. No generic Study `operations` table exists. |
| Trạng thái hiện tại | Angular route/page loads recipients through #68, requires explicit selection, posts text/channels through #93 and routes a valid accepted UUID to SH-07/#18. Segment, draft and priority flows are not implemented; provider delivery and browser/runtime are unverified. |

### Expected behavior và current behavior

> Các phần trích từ DD nguồn tiếp theo giữ lại discrepancy/design snapshot ban đầu. Current source implementation được mô tả trong bảng trạng thái và đoạn current behavior ở trên.

**Expected behavior (inventory / AC-36 / catalog plus AD-20 decision):** Admin có quyền notification-management mở form; với screen slice đã thống nhất, chọn recipient IDs cụ thể từ #68, nhập title/content/channels, gửi qua #93 và chuyển UUID `meta.operation_id` sang SH-07. HTTP 202 chỉ xác nhận accepted. Segment/campaign, draft, priority và delivery không thuộc decision này.

**Current behavior (working-tree source, 2026-11-21):** AD-20 loads recipient pages from #68, requires explicit selection, posts title/content/channels to #93, and accepts only HTTP 202 with the expected business code, queued status and UUID `meta.operation_id` before navigating to SH-07. An ambiguous response locks resend and links back to AD-19 for manual checking. SH-07 reads the notification aggregate through owner-bound #18. Segment, draft and priority flows are not implemented. Queue acceptance does not prove provider delivery; authenticated browser/live API/DB runtime is unverified.

### API #93 và discrepancy

| Nguồn | Hợp đồng/hành vi | Trạng thái |
|---|---|---|
| API catalog #93 và AC-36 n5 | `POST /api/v1/admin/notifications`; Bearer JWT/Admin; body có recipients? hoặc segment?, title/content/channels; HTTP 202 với `ApiEnvelope<Notification>`. | Expected direct contract; API DD vẫn Draft. |
| Phần operation tracking tổng quát trong `list_api.md` | Nói POST #93 trả `data: Operation` ở 202 và client poll #18. | `DISCREPANCY` với row #93 và AC-36 n5. |
| Current local #93 source | Trả `data` là Notification đầu tiên, thêm `meta.operation_id: UUID` và `meta.notification_ids`; `businessCode=DESIGN_OPERATION_ACCEPTED`. UUID metadata is grouping metadata and creates no generic Operation row. | `CURRENT_SOURCE`; the API remains Draft for broader consumers, while the explicit-recipient producer/consumer handoff is `RESOLVED_FOR_AD-20` in the API DD. |
| API #18 / SH-07 | API #18 catalog row declares `operation_id:int64`; reusable `Operation.id`, AC diagrams, current OpenAPI/source and #93 metadata use UUID. The current Shared handler queries notification rows by UUID and authenticated sender; there is no generic Study `operations` table. | `DISCREPANCY` for the generic Operation contract; the notification-only owner-bound UUID handoff is resolved for AD-20. |

### Local #93 fallback (không thay thế contract)

- Route dùng shared `ADMIN` guard trước body parse/database; AC-36 yêu cầu notification-management permission. Hai điều kiện này chưa được xác nhận tương đương.
- Validator yêu cầu `recipients` tường minh, không null/rỗng, ID là int64 dương và không trùng; nếu key `segment` xuất hiện thì trả 422. User IDs được tra trong bảng `users`, không lọc role, trạng thái, khóa học hay tenant.
- `title`/`content` phải là string và không chỉ chứa whitespace; title tối đa 200 ký tự theo local candidate; text hợp lệ được giữ nguyên. `channels` phải không rỗng, không trùng, exact token `PUSH` hoặc `EMAIL`.
- View ghi một legacy notification cho mỗi recipient và một delivery row `QUEUED` cho mỗi notification/channel; dùng một UUID chung và trả tất cả notification IDs trong metadata. Legacy BIGINT DDL/migration là checked-in candidate, không xác nhận live schema hoặc mô hình campaign được duyệt.
- HTTP 202 chỉ trả sau commit của notification/outbox batch. View không tạo Operation record, không gọi provider và không dispatch worker; không chứng minh đã gửi.
- Errors hiện tại: 401 authentication required, 403 access denied, 422 validation/unknown recipient, 503 DB operational/unavailable condition, 500 lỗi persistence/projection/commit khác. Insert/commit failure cố rollback. Không có retry/idempotency rule riêng trong request #93.
