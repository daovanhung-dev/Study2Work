# AD-25 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `AD-25-EV-001` | `Source heading` / D.1. Quy tắc chung | See source event detail below |
| `AD-25-EV-002` | `Source heading` / D.2. Event xử lý | See source event detail below |
| `AD-25-EV-003` | `Source heading` / D.3. Error handling và request sequencing | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả xử lý sự kiện và API

### D.1. Quy tắc chung

- Các mô tả dưới đây tách hành vi đang có trong HTML khỏi flow kỳ vọng. Tương tác EV-02…EV-04 chỉ thay đổi control native; EV-05 hiện bị hủy ngay tại form. Không có client API hoặc router để gọi.
- Không submit #103 cho đến khi filter serialization, format allowlist/default, Admin/report permission, GET acceptance semantics, response payload và retry/idempotency được phê duyệt. Catalog khai báo `filters?:string` và `format?:string`, không có request body; mọi request shape khác là ngoài bằng chứng.
- Nếu sau này #103 trả 202, đó chỉ là acceptance theo mã catalog `DESIGN_OPERATION_ACCEPTED`; không coi là export hoàn tất. Payload vẫn mâu thuẫn: endpoint row là `ApiEnvelope<Report>`, Operation tracking prose là `Operation`.
- Không gọi #18 cho đến khi #103 producer trả operation ID với kiểu được duyệt, owner/access rule, status/lifecycle và AC-38 edge thống nhất. Không chuyển ID int64/UUID, không tự tạo ID, không poll theo timer suy đoán.
- Không mở tải xuống chỉ vì progress đạt trạng thái terminal. Cần định nghĩa result schema, artifact ownership, URL/endpoint, authorization, expiry và cleanup. Các trạng thái `queued/processing/ready/failed/expired` của inventory và `queued/running/succeeded/failed/expired` của SH-07 chưa có mapping.

### D.2. Event xử lý

| Event | Trigger / input | Current behavior | API / expected boundary | Kết quả và lỗi |
|---|---|---|---|---|
| EV-01 — Initial display | Browser tải route candidate; không có input. | Static HTML hiển thị giá trị mặc định và placeholder. Không có request, auth check, query parse hoặc loading state. | Route `/admin/reports/export` chỉ là inventory candidate. Không có Study Web router; không gọi #103/#18 khi load theo source hiện tại. | Current state luôn là mockup ban đầu. Expected guard, query initialization, fetch/error states chưa được chốt. |
| EV-02 — Choose format | `change` trên #19/#20/#21. | Native radio group `file_format`: `csv` ban đầu; người dùng có thể chọn `xlsx` hoặc `pdf`. Không lưu ra URL/server. | #103 chỉ khai báo optional string `format`; enum, casing, MIME/extension, default, unsupported-value behavior và encoding chưa được phê duyệt. | Current: selected radio đổi cục bộ. Không có success/error hoặc validation handler. |
| EV-03 — Choose report scope | `change` trên #23/#24/#25. | Checkbox native `scope_course`, `scope_learner` checked; `scope_impact` unchecked. HTML không đặt explicit `value` cho các checkbox. | #103 `filters?:string` không định nghĩa cấu trúc/serialization; không có mapping đến #102 `from/to/segment` hay report datasets. Min/max scope selection và empty selection behavior chưa rõ. | Current: checked state đổi cục bộ. Không thể suy ra API filter từ tên hoặc nhãn checkbox. |
| EV-04 — Choose period | `change` trên #27/#28/#29. | Radio native `time_range`: `month` ban đầu; `week`/`custom` lựa chọn được. `custom` không có date controls; GMT+7 chỉ là text. | API #102 date semantics và #103 filter mapping chưa xác định. Không tính ngày, timezone, inclusive/exclusive boundary hoặc `from/to` ở client theo suy đoán. | Current: radio đổi cục bộ. Không có validation/field phụ khi chọn custom. |
| EV-05 — Start export | Submit form qua #31; prototype chỉ có một nút submit. | Inline `onsubmit="event.preventDefault();"` hủy submit mặc định và không gọi handler khác. Không có spinner, disable, request, Operation ID, progress, toast hoặc error state. | Candidate #103: `GET /api/v1/admin/reports/community-impact/export`; Bearer JWT/Admin; optional `filters`, `format`; no body; 202 `DESIGN_OPERATION_ACCEPTED`; catalog errors 401/403/503/500. Không tự thêm 400/422. Request filter values và success envelope chưa được chọn. | Current: nội dung và panel không đổi. Expected errors/auth/queue failure/repeat-submit response UX cần được chốt. GET retry có thể tạo job trùng; không tự retry. |
| EV-06 — Download artifact | Click #37. | Button `disabled` and `aria-disabled="true"`, không có href, result URL hay click listener. | Không có download endpoint trong inventory/#103. Cần approved operation result/ExportAsset mapping, download auth, URL lifetime, response MIME/filename, cache behavior, checksum rule và retention. | Current: không thể kích hoạt. Expected hidden/disabled/enabled condition và expired/error recovery chưa được duyệt. |
| EV-07 — Open SH-07 | Click/activate #38 khi có Operation ID. | #38 là static callout không phải anchor/button; không có operation ID. | Inventory chỉ nói gọi #18 khi BE xác nhận `operation_id`. #18 row path dùng int64; shared schema/AC diagram dùng UUID; access rule cũng conflict. AC-38 operation-status node chưa nối vào export branch. | Không có navigation/poll hiện hành. Expected route `/operations/:operationId` và khi nào mở SH-07 cần edge, ID type, owner/access và status mapping đã duyệt. |
| EV-08 — Return to AD-24 | Click #10. | Anchor có `href="#"`; không về AD-24 và không giữ query/filter state. | Inventory liên kết AD-24; AD-24 DD muốn giữ filter URL nhưng CTA hiện không gửi query. Query key/serialization/precedence chưa thống nhất. | Current: không có điều hướng ứng dụng. Expected return target và filter restoration chưa được duyệt. |
| EV-09 — Shell/footer navigation | Click nav/breadcrumb/footer (#2, #4, #6, #8, #44–#46). | Anchors là `#`; notification button không có listener. | Screen APIs #103/#18 không định nghĩa shell destinations, notification feed hoặc profile endpoint. Route ownership thuộc shell/router design. | Current: no-op/anchor behavior. Do not create routes or API calls from labels alone. |

### D.3. Error handling và request sequencing

API catalog là design contract, không phải source đang chạy. Nếu #103 sau này được wire, DD implementation phải theo response/error envelope đã thống nhất và giữ `traceId` nếu response đó có field theo API convention. Hiện không đủ bằng chứng để chỉ định field-level errors, message text, retry button hay HTTP-to-state mapping cho export. Catalog chưa liệt kê 400/422; không tự thêm.

Không có request sequence hiện hành. Candidate sequence từ thiết kế chỉ có thể là `#103 acceptance → [conditional #18 status lookup] → [approved artifact retrieval]`; dấu ngoặc biểu thị phụ thuộc chưa đóng. AC-38 không nối #18 vào sequence export, và inventory chỉ kỳ vọng poll khi operation ID đã được xác nhận. Không gọi song song, poll nền, retry hoặc download qua một URL tự suy diễn.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
