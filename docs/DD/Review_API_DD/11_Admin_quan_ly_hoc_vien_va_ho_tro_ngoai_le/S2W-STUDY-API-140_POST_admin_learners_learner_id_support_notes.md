# Review S2W-STUDY-API-140 — POST learner support note

- DD nguồn: `docs/DD/Study2Work_DD_API/11_Admin_quan_ly_hoc_vien_va_ho_tro_ngoai_le/S2W-STUDY-API-140_POST_admin_learners_learner_id_support_notes.xlsx`
- Endpoint: `POST /api/v1/admin/learners/{learner_id}/support-notes`
- Kết luận: **CẦN SỬA — thiếu schema và policy cho phản hồi chính thức**

## Các điểm cần sửa

| ID | Mức độ | Vị trí DD | Nhận xét và căn cứ BD | Cách sửa |
|---|---|---|---|---|
| 140-01 | P0 | `1.Request!A22:J24`, DB Insert sheets | `study.support_notes` không tồn tại trong schema hiện hành; `visibility` chỉ là String tự do, chưa có FK/constraint cho `learner_id` và `related_request_id`. | Thiết kế migration đầy đủ và enum `INTERNAL|OFFICIAL_RESPONSE`; validate request thuộc đúng learner. |
| 140-02 | P0 | `3.Data mapping!A12:H20` | Mapping đọc/khóa `support_notes.learner_id` trước khi INSERT và dùng placeholder generic; chưa nêu ID/timestamp tạo, author, dedupe. | Viết insert cụ thể, source server-owned fields và idempotency unique key; không khóa bản ghi chưa tồn tại. |
| 140-03 | P0 | `3.Data mapping!A15:H15`, `2.Response!A16:H17` | “Official response” phải khác note nội bộ và chỉ khi official mới tạo notification, nhưng side effect hiện luôn ghi audit/notification chung; flag notification lại khai báo String. Căn cứ `BD-11:157-166`, `ADM-LRN-07/08` tại `BD-11:180-181`. | Lập branch theo visibility, permission cao hơn cho official, Boolean result; notification bằng outbox sau commit và response public được lưu rõ. |
| 140-04 | P1 | `4.Error!A14:H15` | Có lỗi `HIGH_RISK_REASON_REQUIRED` dù request không có reason riêng và tạo note không mặc định là reset/hủy/khoá. Đây là lỗi template không khớp use case. | Bỏ lỗi không liên quan; thêm invalid visibility, related request mismatch, content policy và duplicate idempotency. |
| 140-05 | P0 | `2.Response!A9:E11` | Envelope cũ và pagination giả trái `System_Architecture.md:632-700`. | Chuyển sang envelope chuẩn, camelCase, businessCode và traceId. |

## Điều kiện duyệt lại

- Có migration, enum, permission và lifecycle/retention cho note.
- Có test internal-vs-official, notification exactly-once và related request ownership.
