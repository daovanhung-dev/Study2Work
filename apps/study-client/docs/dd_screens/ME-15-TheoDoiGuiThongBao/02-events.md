# ME-15 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `ME-15-EV-001` | `Source heading` / EV-01 — Tải màn hình | See source event detail below |
| `ME-15-EV-002` | `Source heading` / EV-02 — Click “Tải lại trạng thái” và timer toast prototype | See source event detail below |
| `ME-15-EV-003` | `Source heading` / EV-03 — Anchor brand, header, breadcrumb và quay lại | See source event detail below |
| `ME-15-EV-004` | `Source heading` / EV-04 — Đọc trạng thái notification qua API #64 (tích hợp bị chặn) | See source event detail below |
| `ME-15-EV-005` | `Source heading` / EV-05 — API #18 generic operation tracking | See source event detail below |
| `ME-15-EV-006` | `Source heading` / EV-06 — Technical support và footer links | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả chi tiết sự kiện

### EV-01 — Tải màn hình

- **Element/loại:** Document load, browser navigation.
- **Điều kiện:** Prototype được mở trong browser. Route inventory có `:notificationId`, nhưng HTML không đọc route/path.
- **Đầu vào hiện tại:** Không có path ID, query, session, cache hoặc dữ liệu từ ME-14 được đọc bởi script.
- **Xử lý hiện tại:** Browser dựng literal HTML; không gọi backend; không parse/validate; không có state initialization ngoài giá trị tĩnh trong DOM.
- **Kết quả hiện tại:** Hiển thị system-ID placeholder, queue chip, progress steps, channel rows và empty report như ảnh. Không có loading/error branch từ API.
- **Mục tiêu sau khi contract được duyệt:** Chỉ tạo request #64 nếu caller cung cấp đúng một `notificationId` theo quyết định mapping. Không dùng Operation UUID `data.id`; không tự chọn phần tử đầu tiên từ `meta.notification_ids`.
- **Ngoại lệ:** Auth/session guard, ID selection/validation UI, API error page/banner, empty status behavior và return URL chưa có Study Web implementation/approved UX. Ghi là blocker, không giả định fallback.

### EV-02 — Click “Tải lại trạng thái” và timer toast prototype

- **Element/loại:** #19, click; icon #19; toast ở DOM có ID `toast` nhưng không có marker riêng vì nằm ẩn ở trạng thái ban đầu.
- **Điều kiện hiện tại:** Button enabled. Trong 800 ms spinner period, button disabled nên click lặp lại không phát sinh handler.
- **Đầu vào:** Click; không có notification ID hoặc dữ liệu người dùng nhập.
- **Xử lý hiện tại theo thứ tự:**
  1. Thêm `animate-spin` cho `#refreshIcon`.
  2. Thêm thuộc tính `disabled` cho button.
  3. Chờ `setTimeout(..., 800)`.
  4. Bỏ spinner và enable button.
  5. Hiện toast “Đã kiểm tra máy chủ. Dữ liệu đang được đồng bộ theo thời gian thực.” bằng cách đổi transform/opacity classes.
  6. Chờ `setTimeout(..., 3000)` rồi ẩn toast.
- **API/data transform:** Không có request, response, business code hoặc dữ liệu được cập nhật. Không có status state mutation, cache update, retry hoặc timeout mạng.
- **Kết quả/ngoại lệ:** Chỉ animation và toast thành công giả lập. Click mới có thể bắt đầu trước khi timer ẩn toast trước kết thúc; timer cũ không bị hủy. Toast không có explicit `role=alert`/`aria-live` trong prototype. Target refresh thật phụ thuộc EV-04 và chưa được phê duyệt.

### EV-03 — Anchor brand, header, breadcrumb và quay lại

- **Element/loại:** #1, #3–#8, #11, #18; click anchor.
- **Đầu vào:** Không có payload; các `href` hiện đều là `#`.
- **Xử lý hiện tại:** Browser điều hướng tới fragment rỗng trên cùng tài liệu (có thể đưa viewport về đầu trang); không có app router handler.
- **Kết quả hiện tại:** Không đổi screen/data; không truyền notification ID hoặc Operation ID.
- **Đích mục tiêu:** Chưa xác nhận. #18 có text “Quay về hộp thông báo” nhưng chưa có route/destination trong source. Không tự gán ME-14 hay một screen list cụ thể.
- **Ngoại lệ:** Khi auth hết hạn hoặc route ID thiếu, không có client guard/recovery behavior hiện hành.

### EV-04 — Đọc trạng thái notification qua API #64 (tích hợp bị chặn)

- **Element/loại:** Dự kiến khởi tạo từ EV-01 và refresh từ EV-02; không có call trong prototype hiện tại.
- **Điều kiện:** Cần một `notification_id:int64` đã được chọn từ producer/handoff và Mentor có Bearer access. Việc lựa chọn từ danh sách `meta.notification_ids` chưa có rule.
- **Request contract:** `GET /api/v1/mentor/notifications/{notification_id}/status`; header `Authorization: Bearer <JWT>`; không query/body. Route server raw-path parser nhận signed int64; dữ liệu notification hiện hành dùng ID dương, malformed/out-of-range trả 404. Không gửi UUID Operation vào path.
- **Backend processing hiện tại:** MENTOR auth trước path parse; một query read-only lấy một notification và aggregate delivery counts; so `sender_id` với user hiện tại; validate operation UUID/timestamps/count projection; không commit/write/provider call.
- **200 response:** `ApiEnvelope<Operation>` shape với `businessCode=DESIGN_RESOURCE_RETRIEVED`; `data.id:uuid`, `kind=NOTIFICATION_DISPATCH`, `status`, `owner_id:int64`, `submitted_at`, `updated_at`; optional `completed_at` absent. Không có delivery counts, channel list hoặc recipient detail.
- **Status projection hiện tại ở server:** Count phải là số nguyên không âm, `delivery_count>0`, tổng `queued+sent+failed` bằng delivery count. Có bất kỳ `QUEUED` → `QUEUED`; nếu không có queued nhưng có `FAILED` → `FAILED`; nếu tất cả là `SENT` → `SENT`. Đây là local DERIVED mapping theo API #64 DD, chưa được xác nhận như enum/lifecycle toàn hệ thống.
- **Lỗi:** 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED` cho role/sender access; 404 `DESIGN_RESOURCE_NOT_FOUND` cho malformed/out-of-range ID, không có notification, thiếu operation link hoặc không có delivery rows; 500 `DESIGN_INTERNAL_ERROR` cho DB/projection/envelope failure. Server dùng safe error envelope; query/projection failure rollback an toàn. #64 không khai báo 503.
- **Frontend outcome:** Mapping các lỗi trên thành copy, retry, refresh disable policy, session recovery, polling interval hoặc terminal state chưa được thiết kế/duyệt. Không tự thêm. Không được giả định 200 nghĩa là tất cả channel/provider đã ACK bên ngoài.
- **Tests/source:** Route/module/query/test có trong local Study Server; test/source là evidence local, không phải xác nhận live schema, migration 009, worker/provider hoặc runtime end-to-end. Không chạy application tests trong session này.

### EV-05 — API #18 generic operation tracking

- **Element/loại:** Không có element/action gọi #18 trong ME-15; đây là dependency được inventory ghi kèm và được tách ra để tránh nhầm ID.
- **Contract được khai báo:** `GET /api/v1/operations/{operation_id}`, response `ApiEnvelope<Operation>`, HTTP 200 `DESIGN_OPERATION_RETRIEVED`; catalog row ghi path int64, shared convention/schema và AC ghi UUID; owner/Admin rule cũng chưa thống nhất.
- **Current behavior:** Không có Study route/module/query/focused test; DD #18 là Draft/Needs Confirmation. AC-25 node `operation_status` không có incident edge; #64 node `n8` mới là node kết nối trong notification flow.
- **Kết quả:** Không gửi request #18, không poll Operation UUID từ `data.id`, không dùng #18 thay #64. Cadence, lifecycle, status enums, owner policy, result mapping và persistence đều chưa giải quyết.

### EV-06 — Technical support và footer links

- **Element/loại:** #49, #52–#54; click anchors.
- **Đầu vào hiện tại:** Không có form/query; cả bốn anchor có `href="#"`.
- **Xử lý/kết quả hiện tại:** Browser theo fragment rỗng; không mở email, URL ngoài, ticket, trang quy chế hoặc tiêu chuẩn.
- **Đích mục tiêu/ngoại lệ:** Destination, quyền truy cập, thông tin queue cần gửi cho support và cách xử lý phiên hết hạn chưa có source/contract. Không tạo escalation hoặc support API.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
