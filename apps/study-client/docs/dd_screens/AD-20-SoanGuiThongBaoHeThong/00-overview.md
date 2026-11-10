# AD-20 — Soạn/gửi thông báo hệ thống · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `AD-20` |
| Module | Admin |
| Route | `/admin/notifications/new` (candidate; Study Web route chưa wired)` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **DD status:** `BLOCKED` — API #93 audience/response/draft-vs-send decisions and the #18 operation bridge are unresolved. The current UI artifact cannot submit a request that the local API accepts.; **Implementation status:** `IMPLEMENTATION BLOCKED` · **Runtime status:** `RUNTIME NOT VERIFIED`. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [AD-20.md](../../screen_stitch/05_admin/AD-20_soan-gui-thong-bao-he-thong/AD-20.md), [AD-20_PLAN.md](../../screen_stitch/05_admin/AD-20_soan-gui-thong-bao-he-thong/AD-20_PLAN.md), [AD-20_markers.json](../../screen_stitch/05_admin/AD-20_soan-gui-thong-bao-he-thong/AD-20_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Chọn recipients/segment, channels, preview và xác nhận; accepted không có nghĩa đã delivered.
- In-scope: POST #93; chỉ sang SH-07 nếu operation response field/type và #18 mapping được duyệt. Catalog/AC-36 trả Notification; tracking prose nói Operation; local source trả Notification đầu tiên và derived `meta.operation_id:UUID`.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

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
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [AD-20 source screen.png](../../screen_stitch/05_admin/AD-20_soan-gui-thong-bao-he-thong/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/05_admin/AD-20_soan-gui-thong-bao-he-thong/screen_annotated.png))
- Luồng: POST #93; chỉ sang SH-07 nếu operation response field/type và #18 mapping được duyệt. Catalog/AC-36 trả Notification; tracking prose nói Operation; local source trả Notification đầu tiên và derived `meta.operation_id:UUID`.
- Priority: P1; Gate/source status: **R** local #93 route/module/model/validator/query/view/test source; API DD Draft. **DD BLOCKED; IMPLEMENTATION BLOCKED:** response Notification vs Operation; #18 int64 vs UUID/no Study handler/store; local source requires explicit recipients but UI only supplies unresolved segments; app→PUSH/channel, audience predicate/eligibility/grain, permission vs ADMIN, draft/send/priority, legacy live schema and provider delivery unresolved; Study Web UNWIRED; **RUNTIME NOT VERIFIED**

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# AD-20 — Soạn và phát hành thông báo toàn hệ thống

> **DD status:** `BLOCKED` — API #93 audience/response/draft-vs-send decisions and the #18 operation bridge are unresolved. The current UI artifact cannot submit a request that the local API accepts.
> **Implementation status:** `IMPLEMENTATION BLOCKED` · **Runtime status:** `RUNTIME NOT VERIFIED`.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | AD-20 — Soạn/gửi thông báo hệ thống |
| Mục tiêu | Cho Admin soạn nội dung thông báo và chọn nhóm người nhận/kênh trước khi xác nhận phát hành, theo mục đích trong inventory và AC-36. Các card Accepted/Correlation/Delivered trong mockup là copy tĩnh, không chứng minh lifecycle runtime. |
| Actor / quyền dự kiến | Admin có `notification-management` permission theo AC-36. |
| Route | `/admin/notifications/new` là candidate từ `list_screen.md`; Study Web hiện không có app source/router để xác nhận route. |
| Màn hình liên kết | AD-19 là entry/đường quay lại dự kiến; AD-21 là màn hình liên quan đến kiểm soát/trạng thái; SH-07 chỉ là handoff dự kiến nếu contract operation đã được duyệt. Không có route nào đã được xác minh trong Study Web. |
| Tiền điều kiện | User đã đăng nhập và được phép quản trị notification theo AC-36. Quy tắc permission cụ thể chưa được thống nhất với role `ADMIN` mà API #93 hiện kiểm tra. |
| Hậu điều kiện | AC-36 mô tả Notification/recipients và nhánh gửi Push/Email có điều kiện. API #93 catalog trả HTTP 202; 202 chỉ là accepted, không đồng nghĩa delivered. Response, recipient grain và cách theo dõi operation còn mâu thuẫn/chưa duyệt. |
| Dữ liệu chính | Catalog #93: `recipients?: int64[]`, `segment?: AudienceSegment`, `title`, `content`, `channels[]`; response `ApiEnvelope<Notification>`. Mockup còn có priority, preview, nút draft/send và segment mẫu nhưng không chứng minh request contract. |
| API | `POST /api/v1/admin/notifications` (#93). API #18 là endpoint thiết kế `GET /api/v1/operations/{operation_id}`, hiện chưa có Study Server handler/store. |
| Trạng thái hiện tại | HTML chỉ cập nhật preview theo input title/body. Không có fetch/XHR, submit handler, route wiring, API client hay backend delivery worker được xác minh. |

### Expected behavior và current behavior

**Expected behavior (inventory / AC-36 / catalog):** Admin có quyền notification-management mở form tạo notification; chọn recipients hoặc segment, title, content, channels; xác nhận nhánh CREATE/SEND; API #93 nhận request và phản hồi 202. AC-36 n5 ghi `ApiEnvelope<Notification>`; inventory chỉ yêu cầu sang SH-07 nếu response có `operation_id`, và accepted không phải delivered.

**Current behavior (checked-in source):** Study Web không có frontend source/router/API client. Prototype có các native input và preview; chỉ hai listener `input` trên `#notice-title` và `#notice-body` cập nhật preview. Các segment/channel/priority controls, toolbar, draft/send buttons, nav links, preview detail link và lifecycle card không có handler. Nút Send bị disable tĩnh. API #93 route/backend có source, nhưng request UI hiện tại không cung cấp recipient IDs tường minh.

### API #93 và discrepancy

| Nguồn | Hợp đồng/hành vi | Trạng thái |
|---|---|---|
| API catalog #93 và AC-36 n5 | `POST /api/v1/admin/notifications`; Bearer JWT/Admin; body có recipients? hoặc segment?, title/content/channels; HTTP 202 với `ApiEnvelope<Notification>`. | Expected direct contract; API DD vẫn Draft. |
| Phần operation tracking tổng quát trong `list_api.md` | Nói POST #93 trả `data: Operation` ở 202 và client poll #18. | `DISCREPANCY` với row #93 và AC-36 n5. |
| Current local #93 source | Trả `data` là Notification đầu tiên, thêm `meta.operation_id: UUID` và `meta.notification_ids`; `businessCode=DESIGN_OPERATION_ACCEPTED`. UUID metadata là derived fallback, không tạo Operation row. | `CURRENT_SOURCE`; chưa được owner duyệt làm contract. |
| API #18 / SH-07 | API #18 row khai báo path `operation_id:int64`; reusable `Operation.id`, AC diagrams, #93 UUID metadata và SH-07 dùng UUID. Không tìm thấy Study #18 route/query/store. | `DISCREPANCY / BLOCKER`; không thể poll hoặc xác nhận route param. |

### Local #93 fallback (không thay thế contract)

- Route dùng shared `ADMIN` guard trước body parse/database; AC-36 yêu cầu notification-management permission. Hai điều kiện này chưa được xác nhận tương đương.
- Validator yêu cầu `recipients` tường minh, không null/rỗng, ID là int64 dương và không trùng; nếu key `segment` xuất hiện thì trả 422. User IDs được tra trong bảng `users`, không lọc role, trạng thái, khóa học hay tenant.
- `title`/`content` phải là string và không chỉ chứa whitespace; title tối đa 200 ký tự theo local candidate; text hợp lệ được giữ nguyên. `channels` phải không rỗng, không trùng, exact token `PUSH` hoặc `EMAIL`.
- View ghi một legacy notification cho mỗi recipient và một delivery row `QUEUED` cho mỗi notification/channel; dùng một UUID chung và trả tất cả notification IDs trong metadata. Legacy BIGINT DDL/migration là checked-in candidate, không xác nhận live schema hoặc mô hình campaign được duyệt.
- HTTP 202 chỉ trả sau commit của notification/outbox batch. View không tạo Operation record, không gọi provider và không dispatch worker; không chứng minh đã gửi.
- Errors hiện tại: 401 authentication required, 403 access denied, 422 validation/unknown recipient, 503 DB operational/unavailable condition, 500 lỗi persistence/projection/commit khác. Insert/commit failure cố rollback. Không có retry/idempotency rule riêng trong request #93.
