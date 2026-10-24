# OPEN_QUESTIONS — Study API #63

Trạng thái: `Draft — Needs Confirmation`. Các đề xuất đơn giản dưới đây là `DERIVED`, chưa được phê duyệt; cột contract trực tiếp trong DD vẫn giữ catalog.

<a id="q-63-01-course-scope"></a>

## Q-63-01 — Course scope của danh sách recipient

**Bằng chứng:** AC-25 chọn một course và #62 đọc roster của course. Body #63 không có `course_id`, chỉ có `recipients:string!`.

**Ảnh hưởng:** Server không thể xác thực toàn bộ recipients thuộc course mà Mentor đã chọn hoặc phân biệt scope giữa các course.

**Khuyến nghị đơn giản:** Thêm `course_id:int64!`; xác thực quyền Mentor trước, sau đó kiểm tra mọi Student ID còn đủ điều kiện trong course.

**Cần xác nhận:** Contract owner có duyệt thêm course_id và 403/422 mapping cho recipient ngoài scope không?

<a id="q-63-02-recipient-encoding"></a>

## Q-63-02 — Encoding và ID của recipients

**Bằng chứng:** Catalog khai báo string; #62 hiện trả `Page<Course>` trong khi AC-25 cần learner; legacy dùng BIGINT user ID, pilot dùng UUID learner.

**Ảnh hưởng:** Client/server không thống nhất được ID, delimiter, duplicate và cách kiểm tra eligibility.

**Khuyến nghị đơn giản:** Sau khi #62 thống nhất sang learner projection, dùng danh sách `Student.id` duy nhất. Nếu phải giữ scalar string thì dùng CSV số int64 (`101,202`), parse nghiêm ngặt, khử trùng lặp theo thứ tự đầu tiên.

**Cần xác nhận:** User ID hay enrollment ID; CSV có được chấp thuận hay catalog nên đổi sang array?

<a id="q-63-03-content-type"></a>

## Q-63-03 — `content:int64` hay nội dung text

**Bằng chứng:** Catalog và diagram body đều ghi int64, nhưng diagram nói Mentor nhập nội dung; Notification schema/legacy DDL dùng string/TEXT.

**Ảnh hưởng:** Không thể xác định int64 là content text ID, template ID hay lỗi type; không map an toàn vào Notification.content.

**Khuyến nghị đơn giản:** Đổi sang `content:string!` vì AC nhập text và schema Notification dùng text; nếu muốn content reference, đặt tên ID riêng và định nghĩa resolver.

**Cần xác nhận:** Sửa catalog/diagram/body type sang string hay cung cấp ý nghĩa và nguồn cho int64?

<a id="q-63-04-channel-encoding"></a>

## Q-63-04 — Encoding và giá trị channels

**Bằng chứng:** API body là string; AC diagram nói Push/Email; schema dùng `NotificationChannel[]`; pilot delivery constraint cho `IN_APP|EMAIL`.

**Ảnh hưởng:** Không xác định được token, delimiter hay cách map Push với IN_APP; client không thể tạo request hợp lệ.

**Khuyến nghị đơn giản:** Chuẩn hóa thành array enum nếu sửa contract; nếu phải giữ string thì chốt CSV và enum tokens trước implementation.

**Cần xác nhận:** Channel machine values có phải `PUSH`/`EMAIL`, `IN_APP`/`EMAIL`, hay tập khác?

<a id="q-63-05-persistence"></a>

## Q-63-05 — Notification/recipient persistence

**Bằng chứng:** Legacy `notifications` có user_id đơn, không có recipient table/channel/delivery status; pilot dùng UUID riêng cho learner và delivery.

**Ảnh hưởng:** Không có một physical model khớp Notification + nhiều recipients, int64 ID và #64 status.

**Khuyến nghị đơn giản:** Chọn một schema canonical cho Study trước khi chốt SQL; không ghép hai model.

**Cần xác nhận:** Schema nào là target; Notification ID có phải int64 và bảng recipient association nào được dùng?

<a id="q-63-06-async-lifecycle"></a>

## Q-63-06 — Queue acceptance, transaction và retry

**Bằng chứng:** API trả 202; diagram gọi Push/Email; API Guidelines yêu cầu Idempotency-Key cho retryable mutation. Không tìm thấy Study Operation/queue/outbox implementation.

**Ảnh hưởng:** Không biết lúc nào được trả 202, cách tránh duplicate khi client retry, cách phục hồi khi queue/provider lỗi.

**Khuyến nghị đơn giản:** Trả 202 chỉ sau khi yêu cầu đã được ghi nhận bền vững; dùng key idempotency và worker bất đồng bộ. Physical store/outbox, retry/backoff phải được chọn cùng schema.

**Cần xác nhận:** Key scope/retention, accepted boundary, retry policy và partial failure aggregation.

<a id="q-63-07-operation-result"></a>

## Q-63-07 — Operation schema/result cho notification job

**Bằng chứng:** API #63 trả Operation; reusable `Operation.result` là Payment?; OperationKind/OperationStatus chưa có enum members; không có Study Operation storage.

**Ảnh hưởng:** Không thể biểu diễn result của notification job hoặc hoàn thiện response đầy đủ.

**Khuyến nghị đơn giản:** Mở rộng result theo kind bằng `NotificationDelivery` hoặc schema notification job đã duyệt; không reuse Payment.

**Cần xác nhận:** Result type, enum, owner ID mapping, lifecycle và persistence nào là canonical?

<a id="q-63-08-notification-id-handoff"></a>

## Q-63-08 — Cầu nối sang API #64

**Bằng chứng:** #63 trả Operation.id UUID; #64 nhận notification_id:int64. Không có field nào trong response trực tiếp cung cấp notification_id.

**Ảnh hưởng:** Client không thể gọi #64 sau khi POST được chấp nhận.

**Khuyến nghị đơn giản:** Trả notification_id:int64 trong result của Operation; hoặc đổi #64 để nhận operation UUID nếu mục tiêu là theo dõi job thay vì delivery. Không chọn khi chưa thống nhất #18 và #64.

**Cần xác nhận:** #64 theo notification delivery hay Operation job; ID nào được trả từ #63?

<a id="q-63-09-api18"></a>

## Q-63-09 — API #18 operation polling trong AC-25

**Bằng chứng:** AC/API index liệt kê #18; AC-25 diagram có node #18 đứng rời, không edge. Diagram dùng UUID nhưng API #18 row dùng int64.

**Ảnh hưởng:** Chưa rõ client cần poll #18, #64 hay cả hai; ID type đang lệch.

**Khuyến nghị đơn giản:** Dùng #18 để theo dõi trạng thái xử lý job và #64 để theo dõi delivery theo notification; nối IDs rõ trong response/diagram.

**Cần xác nhận:** Xác nhận hai mục tiêu tracking và sửa row/API diagram #18.

<a id="q-63-10-error-envelope"></a>

## Q-63-10 — Error envelope và codes khi wired

**Bằng chứng:** Catalog #63 có 401/403/422/503/500; API Guidelines yêu cầu data null; helper hiện tại mặc định `{}`; path chưa có trong middleware allowlist.

**Ảnh hưởng:** Khi wired, body có thể lệch guideline hoặc DESIGN_* code không được chọn.

**Khuyến nghị đơn giản:** Đồng bộ helper/allowlist trong task implementation riêng; DD không thay code/status direct.

**Cần xác nhận:** Không cần thêm code cho API DD này; implementation owner cần sửa wiring trước khi tuyên bố contract verified.

## Handoff AC-25

- Macro-review #62–#64 và API #18 đã thực hiện sau khi DD #64 được tạo; trạng thái là `VERIFIED_WITH_OPEN_QUESTIONS`.
- Các điểm roster item/ID, recipient encoding/course scope, notification ID handoff, Operation/delivery response và #18 polling vẫn cần contract owner xác nhận; xem [API #64 report](../64_mentor_notifications_status/VERIFICATION_REPORT.md).
