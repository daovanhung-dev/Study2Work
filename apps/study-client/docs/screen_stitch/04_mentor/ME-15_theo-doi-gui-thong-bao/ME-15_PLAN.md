# ME-15 — Kế hoạch hoàn thiện Detailed Design

## 1. Phạm vi và mục tiêu

- Chỉ xử lý Screen ID `ME-15` trong phiên này.
- Tên theo danh mục: **Theo dõi gửi thông báo**; loại `Trang`; AC-25; liên kết `ME-14`, `SH-07`; inventory khai báo API #18 và #64.
- Route trong danh mục: `/mentor/notifications/:notificationId/status`. Route này biểu diễn một `notificationId:int64`, không đồng nhất với `operationId:uuid`.
- Hoàn thiện `ME-15.md`, `ME-15_markers.json`, `screen_annotated.png` và kế hoạch này. Giữ nguyên `screen.png` và `code.html`.
- Đánh giá riêng `DD READY`, `IMPLEMENTATION BLOCKED` và `RUNTIME VERIFIED`; không gộp các trạng thái.

## 2. Bằng chứng hiện có

### 2.1. Tài sản và UI hiện tại

- `screen.png`: 1563×1600, SHA-256 `6172c259a4dfca9a37a6652ebdae83d3f10831b63dd8b59b5e988a23ea534713`; đã xem toàn ảnh. Đây là ảnh nguyên trạng, không chỉnh sửa.
- `code.html`: 22,004 bytes, SHA-256 `ccd0151ae1352662dc006483ff0e00094d9317d35762e76515252c32b7dda70f`; đã xem nội dung và script.
- Prototype có 13 anchor `href="#"`, một button `#refreshBtn`, không có form/input/select, không có fetch/XHR/WebSocket. Tất cả anchor hiện điều hướng về fragment rỗng của cùng trang; không có destination route được triển khai.
- Refresh hiện chỉ đặt trạng thái spinner/disabled, đợi 800 ms, hiện toast thành công, rồi ẩn toast sau 3000 ms. Không đọc hoặc cập nhật status.
- Các nội dung queue, kênh, ba bước xử lý, ACK, báo cáo, trạng thái máy chủ và `SyncEngine v4.2.1-prod` đều là nội dung tĩnh của prototype.
- Study Web hiện `UNWIRED`; không có source app/router/API client để xác minh runtime UI, authentication guard, polling hoặc điều hướng.

### 2.2. Contract và current source

- API #63 current source trả một Operation UUID tại `data.id`, và danh sách notification ID số nguyên tại `meta.notification_ids`. Test source assert hai giá trị mẫu `[30001, 30002]`; #63 tạo một notification cho từng recipient và dùng chung UUID batch.
- API #64 hiện có route `GET /api/v1/mentor/notifications/{notification_id}/status`, Bearer MENTOR, HTTP 200; path nhận một notification ID số nguyên. Source kiểm tra sender ownership, đọc một notification cùng các hàng delivery, rồi trả `ApiEnvelope<Operation>`-shaped result với Operation UUID trong `data.id`.
- #64 status là phép tổng hợp local trên các outbox row của đúng một notification: có `QUEUED` → `QUEUED`; nếu không, có `FAILED` → `FAILED`; nếu tất cả `SENT` → `SENT`. Không có dữ liệu kênh/recipient trong response. DB/provider/worker thật chưa được runtime-verify.
- API #64 lỗi theo source: 401 authentication; 403 sai sender; 404 ID không hợp lệ/không có notification/thiếu operation link/không có delivery; 500 query hoặc projection lỗi. GET không cập nhật resource.
- API #18 hiện không có route/module/query/focused test trong Study Server. API row khai báo `operation_id:int64`, trong khi quy ước ID, Operation schema và AC diagrams khai báo UUID. DD #18 là design-only.
- AC-25 node `n8` cho #64 nằm trên flow kết nối; node `operation_status` cho #18 đứng riêng, không có incident edge. AC là design artifact, không xác nhận runtime.
- SH-07 xử lý generic operation, ghi rõ #18 unwired và #64 là notification-specific; không dùng SH-07 để thay endpoint của ME-15.

## 3. Expected behavior và current behavior

| Chủ đề | Expected/design evidence | Current source evidence | Cách ghi trong DD |
|---|---|---|---|
| Định danh màn hình | Route nhận `notificationId`; ME-14 producer trả một operation UUID và nhiều notification IDs | #64 chỉ nhận một `notification_id:int64`; #63 trả list trong `meta` | Giữ hai kiểu ID riêng; không tự chọn notification ID nào đại diện cả batch |
| Nạp trạng thái | AC-25 nối #64 vào flow; inventory gắn #18/#64 | #64 có source; #18 không có Study runtime; prototype không gọi API | Mô tả #64 như contract source-backed và chặn frontend integration cho đến khi handoff ID/selection rõ |
| Trạng thái | Inventory liệt kê `queued/sending/complete/failed` | #64 local response có `QUEUED/FAILED/SENT`; không có `SENDING/COMPLETE` | Nêu `DISCREPANCY`; không map `SENT` thành `complete` nếu chưa có business approval |
| Refresh | Prototype có nút tải trạng thái | Handler chỉ giả lập timer/toast, không refresh | Ghi chính xác mock behavior; mục tiêu gọi #64 còn bị chặn bởi ID/route contract |
| Tiến độ/kênh/ACK/report | UI tuyên bố progress, channel status, ACK và per-recipient report | Prototype chỉ có static content; #64 response không cung cấp các trường này | Đánh dấu claim chưa có nguồn dữ liệu/API; không tạo field/endpoint |
| Generic polling | SH-07/API #18 là generic operation tracking | API #18 unwired; AC-25 generic node disconnected | ME-15 không gọi #18; không đặt cadence/terminal policy |

## 4. Kế hoạch element và marker

Tạo danh sách tuần tự khoảng **54 element marker**, một marker cho mỗi component/claim có ý nghĩa trên ảnh, theo thứ tự đọc từ trái sang phải, trên xuống dưới. Gộp icon với nhãn khi chúng là một control/row; không gộp những vùng có chức năng hoặc nguồn dữ liệu khác nhau.

| Nhóm | Phạm vi element dự kiến |
|---|---|
| Header | Brand, divider, năm mục điều hướng, notification link/badge, profile identity, avatar |
| Breadcrumb | Link về thông báo, separator, breadcrumb hiện tại |
| Hero và actions | Eyebrow, badge máy chủ, title, mô tả, link quay lại, nút refresh |
| Queue summary | Nhãn ID, ID placeholder, nhãn status, status chip |
| Progress | Icon/title/description, note ACK, tiêu đề quy trình, ba step cards |
| Report | Title, source badge, empty icon, empty heading, empty description |
| Channel panel | Heading và từng row LMS Portal, Email, thảo luận |
| Transparency panel | Icon/title, copy, SyncEngine version |
| Support panel | Eyebrow, prompt, contact link |
| Footer | Brand mark, copyright/WCAG claim, ba footer links |

Marker JSON sẽ lưu thứ tự ID, tọa độ pixel trên kích thước ảnh gốc, tên element khớp DD, loại element và nhóm; không khai báo CSS selector khi prototype không có selector ngữ nghĩa ổn định cho các vùng này. Overlay dùng marker tương phản cao, đồng nhất; đặt gần góc vùng element để hạn chế che text. Không resize hoặc ghi lên `screen.png`.

## 5. Kế hoạch event và API trong DD

1. `EV-01 Screen load`: tách render prototype hiện tại (static, không request) khỏi target route load. Target chỉ được gửi #64 sau khi một notification ID được xác định hợp lệ; chưa có quy tắc chọn ID trong `meta.notification_ids`.
2. `EV-02 Refresh click/timer`: mô tả chính xác disable/spinner 800 ms, success toast, hide sau 3000 ms và việc data không đổi. Đề xuất hành vi thật gọi lại #64 chỉ là phần bị chặn, không mô tả như behavior đã có.
3. `EV-03 Navigation anchors`: phân nhóm brand, header navigation/notification, breadcrumb, back link, support CTA và footer links. Current HTML đặt tất cả `href="#"`; đích điều hướng tương ứng chưa có route/contract.
4. `EV-04 API #64 read`: ghi method/path/auth/path parameter, không body/query, response Operation-like shape, status mapping per notification và lỗi 401/403/404/500. Nêu rõ local outbox projection và các giới hạn; không khai báo retry, interval hay stop state chưa được quyết định.
5. `EV-05 API #18`: ghi là không có event request ở ME-15 hiện tại; API unwired, path ID mâu thuẫn UUID/int64, và node AC-25 không nối flow. Chuyển về SH-07 sau khi contract generic được giải quyết, nếu product xác nhận.
6. `EV-06 Support/link activation`: ghi default fragment behavior và destination chưa có; không tự gán màn hình quản trị.

## 6. Blockers cần giữ nguyên

- ME-14/#63 trả nhiều notification IDs cho một operation; route ME-15 nhận một ID. Chưa có quy tắc chọn ID, lưu state hay tổng hợp batch status.
- Inventory states `sending/complete` không khớp các state #64 source `QUEUED/FAILED/SENT`; enum và UI mapping chưa được duyệt.
- Không có contract cho channel-level receipt, ACK, per-recipient delivery detail/report, retry/timeout/poll cadence, refresh terminal behavior hoặc real-time transport.
- API #18 không có implementation trong Study Server và có mâu thuẫn scalar ID; generic Operation lifecycle/owner policy cũng chưa chốt.
- HTML anchors đều là placeholder; các route đi/đến ME-14, SH-07 và trang hỗ trợ chưa được xác nhận từ Study Web source.
- Study Web `UNWIRED`; implementation và runtime verification chưa thể khẳng định.

## 7. Trình tự thực hiện và kiểm tra

1. Lưu kế hoạch này trước khi tạo marker map, annotated image hoặc DD.
2. Tạo marker JSON sequential/unique/in-bounds theo danh sách element; render overlay PNG từ ảnh nguồn, giữ nguyên `screen.png`.
3. Viết `ME-15.md` đủ phần A–F; mỗi element ánh xạ một marker, mỗi event có input/process/output và ghi rõ expected/current.
4. Cập nhật row ME-15 trong `list_screen.md` và `dd_screens/PLAN.md`, giữ riêng ba trạng thái readiness.
5. Kiểm tra JSON hợp lệ, ID tuần tự và 1:1 với element rows, tọa độ bounds, ảnh nguồn hash không đổi, ảnh chú thích mở được, links tương đối và `git diff --check`.
6. Không chạy application test hoặc runtime trong task tài liệu này. Chỉ đánh giá tĩnh các bằng chứng đã đọc.

## 8. Tiêu chí kết thúc phiên

- Đủ bốn artifact cốt lõi: `screen_annotated.png`, `ME-15.md`, `ME-15_PLAN.md`, `ME-15_markers.json`; giữ nguyên `screen.png` và `code.html`.
- 100% marker map có mô tả chính xác trong DD; event/API/ID/state discrepancies được truy vết.
- Cập nhật tracker/worklog sau kiểm tra.
- Không bắt đầu `ME-16`.
- Chỉ ghi `DD READY` nếu tài liệu đủ implementable và các unresolved requirement được phân định rõ; ghi riêng `IMPLEMENTATION BLOCKED` và `RUNTIME NOT VERIFIED` khi tương ứng.
