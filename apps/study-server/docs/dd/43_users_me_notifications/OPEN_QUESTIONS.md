# OPEN_QUESTIONS — Study API #43

**Status:** Draft — Needs Confirmation
**Endpoint:** `GET` `/api/v1/users/me/notifications`
**Related group:** AC-20 APIs #43–#45; macro review after #45 DD exists.

## Q-43-01 — Recipient source và broadcast rows

**Evidence**

- AC-20 diagram yêu cầu “Đọc `NotificationRecipient` theo user”.
- DB guide/ERD/DDL không có bảng `NotificationRecipient`; bảng notifications.`user_id` nullable.
- DB guide cho biết `user_id` IS NULL có thể đại diện broadcast/segment theo design.

**Vấn đề và ảnh hưởng**

- Không có quan hệ vật lý để mở rộng một notification broadcast thành từng recipient hoặc lưu read state riêng.
- Nếu lấy mọi hàng `user_id` IS NULL, API không có điều kiện an toàn để phân quyền và lọc read state theo `Student`.

**Đề xuất DERIVED**

- Tạm chỉ query notifications.`user_id` = `principal_id`.
- Không trả hàng `user_id` IS NULL cho tới khi có recipient model hoặc rule đã duyệt.

**Cần xác nhận**

- Recipient/read state cho broadcast/segment nằm ở bảng nào, hoặc broadcast chưa thuộc API #43?

## Q-43-02 — Nguồn `channels`, `status` và enum values

**Evidence**

- Reusable Notification contract yêu cầu `channels`: `NotificationChannel[]` và `status`: `NotificationStatus`.
- DB guide/ERD/DDL chỉ có `type` `VARCHAR(30)` và `is_read` `BOOLEAN`.
- Repository search không tìm thấy định nghĩa enum NotificationChannel hoặc `NotificationStatus`.

**Ảnh hưởng**

- Không thể dựng đầy đủ response Notification bằng physical source đã có.
- Gán `type` sang `channels` hoặc `is_read` sang `status` sẽ thay đổi semantics khi chưa có bằng chứng.

**Cần xác nhận**

- Chỉ rõ cột/bảng nguồn và tập enum values, hoặc cập nhật contract/schema.

## Q-43-03 — `read_at` với `is_read` trong nhóm API #43–#45

**Evidence**

- Contract Notification có `read_at`?:date-time.
- AC-20 API #44 ghi “UPDATE `read_at` cho notification recipient”; API #45 ghi bulk update unread.
- DDL chỉ có notifications.`is_read` `BOOLEAN` DEFAULT FALSE, không có `read_at` hoặc physical recipient table.
- API #44/#45 cũng khai báo response `Page<Notification>` nhưng diagram không nói page nào được trả sau mutation.

**Ảnh hưởng**

- Chưa rõ API #44/#45 chỉ đổi boolean hay cần lưu timestamp; #43 cũng không thể map timestamp.
- Success response của #44/#45 cần được thống nhất với list refresh ở #43.

**Đề xuất DERIVED**

- Giữ `is_read` làm candidate filter cho `unread_only`; không tạo timestamp giả.
- Không chốt response semantics của #44/#45 trong DD #43.

**Cần xác nhận**

- Có cần `read_at` physical column không?
- #44 trả notification vừa đổi hay trang notification list?
- #45 trả danh sách nào sau khi đánh dấu toàn bộ?

## Q-43-04 — Page size, order và page range

**Evidence**

- Request #43 chỉ có `unread_only`?:boolean và page?:int32.
- `PageMeta` yêu cầu page, size, `total`, `total_pages`.
- AC-20 không chỉ định page size/order; API #10 có precedent design-only dùng page mặc định 1, size cố định 20, order mới nhất trước.

**Đề xuất DERIVED**

- page=1 khi omitted.
- size=20, không nhận query size.
- `created_at` DESC, id DESC.
- `total_pages`=ceil(`total`/20) và bằng 0 khi `total`=0.
- Page beyond end trả `items`=[] cùng `total`.

**Cần xác nhận**

- Chấp nhận page size 20 và sort mới nhất trước không?
- Catalog cần bổ sung hành vi lỗi cho page < 1/giá trị không parse được không? Không tự thêm 422 khi chưa có contract.

## Q-43-05 — Timezone của `created_at`

**Evidence**

- Notification contract yêu cầu `created_at`:date-time.
- ERD/DDL chỉ rõ `TIMESTAMP`, không ghi timezone.

**Ảnh hưởng**

- Chưa đủ căn cứ để serialize mốc thời gian thành UTC hoặc gắn `offset` cụ thể.

**Cần xác nhận**

- Quy ước timezone của Study timestamps và cách chuyển sang ISO-8601.

## Q-43-06 — Omission/null của optional timestamps

**Evidence**

- `read_at` và `scheduled_at` optional trong Notification schema nhưng không có physical source.

**Ảnh hưởng**

- Chưa rõ serializer nên bỏ field hay trả null khi không có giá trị.

**Cần xác nhận**

- Chốt omission/null rule cùng với schema mapping của Q-43-02 và Q-43-03.

## Q-43-07 — Error envelope giữa guideline và helper hiện tại

**Evidence**

- contracts/api-guidelines/README.md yêu cầu error data: null.
- apps/study-server/app/core/responses.py:error_response() hiện gán {} khi data là None.
- API #43 chưa có route nên discrepancy chưa được quan sát qua endpoint này.

**Ảnh hưởng**

- Khi API #43 reuse helper, body thực tế sẽ khác envelope guideline.

**Cần xác nhận**

- Sửa shared helper/context ở task phù hợp hay điều chỉnh guideline; không đổi error code/`status` của API #43 trong DD này.
