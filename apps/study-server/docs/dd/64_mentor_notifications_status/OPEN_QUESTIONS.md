# OPEN_QUESTIONS — Study API #64

Trạng thái: `Draft — Needs Confirmation`. Contract trực tiếp giữ nguyên; các đề xuất dưới đây cần owner xác nhận trước khi DD chuyển Final hoặc implementation.

<a id="q-64-01-response-shape"></a>

## Q-64-01 — Response Operation hay NotificationDelivery

**Bằng chứng:** API catalog #64 trả `ApiEnvelope<Operation>`; AC-25 gọi #64 để đọc delivery status; reusable `NotificationDelivery` có status và counts.

**Ảnh hưởng:** Operation không có queued/sent/failed delivery counts; `result?:Payment` không đại diện notification.

**Đề xuất đơn giản:** Đổi #64 response sang `ApiEnvelope<NotificationDelivery>`; dùng API #18 riêng cho job Operation. Đây là thay đổi catalog/diagram, không phải contract hiện tại.

**Cần xác nhận:** Contract owner có duyệt đổi response và bổ sung DeliveryStatus semantics không?

<a id="q-64-02-id-handoff"></a>

## Q-64-02 — notification_id và operation_id

**Bằng chứng:** #64 path cần `notification_id:int64`; #63 hiện trả Operation UUID và không khai báo notification ID; API #18 theo dõi operation ID nhưng chính row #18 khai báo int64 trong khi schema/diagram dùng UUID.

**Ảnh hưởng:** Client không biết ID nào để gọi #64 sau khi POST #63 được accepted.

**Đề xuất đơn giản:** #63 trả/đưa ra notification_id:int64 riêng; operation_id:uuid dùng cho #18. Không ép hai ID thành một.

**Cần xác nhận:** Chốt mapping hoặc response contract #63/#64/#18 đồng bộ ra sao?

<a id="q-64-03-storage"></a>

## Q-64-03 — Physical delivery source

**Bằng chứng:** Legacy `notifications` dùng BIGINT nhưng chỉ có `is_read`; V1-PILOT `notifications`/`notification_deliveries` dùng UUID và delivery attempts; DB guide đánh dấu #63–#64 `DESIGN_ONLY`.

**Ảnh hưởng:** Chưa có query vật lý khớp path int64 và trạng thái gửi.

**Cần xác nhận:** Schema nào là Study target; bảng/khóa nào lưu delivery summary; live migration/schema status là gì?

<a id="q-64-04-aggregate"></a>

## Q-64-04 — Status và counts theo recipient/channel/retry

**Bằng chứng:** `NotificationDelivery` khai báo `queued/sent/failed`; pilot delivery rows là append-only theo `(notification_id, channel, attempt_no)` và không có recipient ID.

**Ảnh hưởng:** Đếm row có thể đếm retry attempts thay cho người nhận; chưa biết tổng hợp nhiều channel hoặc partial success.

**Đề xuất đơn giản:** Định nghĩa counts theo recipient cuối cùng và chọn latest/terminal attempt theo một state machine được duyệt; không dùng số row thô.

**Cần xác nhận:** Grain, retry selection, partial-success rule và status tổng hợp nào là chuẩn?

<a id="q-64-05-authorization"></a>

## Q-64-05 — Quyền Mentor xem status và lỗi 403/404

**Bằng chứng:** Catalog yêu cầu role Mentor và liệt kê cả 403/404; AC-25 precondition nói Mentor có quyền gửi cho học viên của course; `notification_id` không mang course scope.

**Ảnh hưởng:** Không thể xác định notification thuộc sender/course nào hoặc thứ tự kiểm tra existence/access.

**Đề xuất đơn giản:** Chỉ cho Mentor có quyền quản lý notification/course xem delivery; dùng 403 cho access denied và 404 cho resource absent nếu policy cho phép phân biệt.

**Cần xác nhận:** Permission relation và privacy behavior cho notification của Mentor khác?

<a id="q-64-06-pending"></a>

## Q-64-06 — Notification có trước delivery record

**Bằng chứng:** #63 chấp nhận xử lý async; #64 được gọi sau dispatch; pilot delivery table lưu trạng thái attempt nhưng chưa có trạng thái ban đầu hoặc quy tắc lúc chưa có row.

**Ảnh hưởng:** Chưa biết trả pending/queued hay 404 khi notification đã tồn tại nhưng worker chưa ghi delivery.

**Cần xác nhận:** Accepted boundary và trạng thái hiển thị trước attempt đầu tiên là gì?

<a id="q-64-07-enums"></a>

## Q-64-07 — DeliveryStatus và OperationStatus

**Bằng chứng:** Reusable `NotificationDelivery.status` khai báo `OperationStatus`; pilot dùng `notification_status` với `QUEUED|SENT|DELIVERED|FAILED|SUPPRESSED`; Notification schema có `NotificationStatus`.

**Ảnh hưởng:** Các lifecycle khác nhau có thể bị ép vào enum không đúng nghĩa.

**Đề xuất đơn giản:** Định nghĩa một enum delivery riêng hoặc phê duyệt mapping rõ; không dùng OperationStatus chỉ vì tên type đang được khai báo.

**Cần xác nhận:** Enum và chuyển trạng thái được duyệt cho delivery là gì?

<a id="q-64-08-path-errors"></a>

## Q-64-08 — Path không phải int64

**Bằng chứng:** Catalog khai báo `notification_id:int64!` nhưng không liệt kê 400/422; middleware hiện chưa allowlist path #64.

**Ảnh hưởng:** Framework validation khi wired có thể trả business code/status ngoài catalog.

**Cần xác nhận:** Chọn HTTP/business mapping và cập nhật middleware contract allowlist trong task implementation; DD không thêm code mới.

<a id="q-64-09-operation-tracking"></a>

## Q-64-09 — Macro flow API #18

**Bằng chứng:** AC/API index liệt kê #18 cho operation tracking; node #18 trong diagram AC-25 đứng rời; API #18 Open Questions còn ID/owner/result/lifecycle conflict.

**Ảnh hưởng:** Chưa rõ UI theo dõi job bằng #18, delivery bằng #64 hay một response chung.

**Đề xuất đơn giản:** Tách job acceptance/status khỏi per-notification delivery status và nối hai ID tường minh trong #63 response.

**Cần xác nhận:** Sửa index/diagram/catalog/DD #18 theo hợp đồng liên kết đã thống nhất.

<a id="q-64-10-error-envelope"></a>

## Q-64-10 — Error envelope khi wired

**Bằng chứng:** API Guidelines dùng `data:null`; current helper mặc định `{}`; middleware `DESIGN_CONTRACT_PATHS` chưa có path #64.

**Ảnh hưởng:** Error body/business code future runtime có thể lệch contract.

**Cần xác nhận:** Future implementation phải đồng bộ helper/allowlist; không đổi source trong task DD.

## Handoff AC-25

- #62–#64 cần khóa roster projection/key → recipients/course scope → notification ID → delivery status/counts.
- #63 `Operation` và #18 operation polling là job tracking; không được nhập với `notification_id` nếu chưa có mapping được duyệt.
- Macro-review trong [VERIFICATION_REPORT.md](./VERIFICATION_REPORT.md) sau khi so sánh cả ba DD; giữ mọi unresolved contract/schema question mở.
