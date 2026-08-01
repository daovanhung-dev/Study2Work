# Plan 12 — Notifications

## 1. Mục tiêu

Hoàn thành **11 file Detail Design API** theo `Detail_Design_API_Template_Optimized.xlsx` cho phạm vi API từ STT **83–93**.

- API trực tiếp từ tài liệu/sequence: **4**.
- API suy dẫn từ BD: **7**.
- Module: 09. Thông báo (11).
- Lý do quy mô batch: 11 API bao phủ notification center, settings và admin batch; làm chung để thống nhất event type, read state và recipient rules.

> API có `Basis = SUY DẪN` chỉ được chốt ở trạng thái **Draft — Needs Confirmation** cho đến khi endpoint, contract và business rule được xác nhận. Không biến suy luận thành dữ kiện.

## 2. Điều kiện tiên quyết

- Event taxonomy.
- RBAC.
- Queue/outbox strategy.
- Áp dụng canonical response envelope từ `Study2Work_System_Architecture.md`: `success`, `businessCode`, `message`, `data`, `meta`, `traceId`; lỗi dùng `errors[]` và không trả stack trace.
- Khóa quy ước JSON/query naming (`camelCase` hay `snake_case`) trước khi chốt bản Final; catalog hiện còn các tên như `page_size` trong khi kiến trúc tích hợp minh họa `pageSize`.
- Mỗi API là một workbook riêng; không gộp nhiều API vào một workbook.

## 3. Nguồn bắt buộc phải đọc khi thực hiện plan

- `BD/0. Study2Work_Study_Business_Description.md`
- `BD/base/0. Study2Work_System_Architecture.md`
- `BD/base/1. Study2Work_Study_Architecture.md`
- `BD/diagram/UC/01. Study2Work_Study_Diagram_UC_Tong_Quan.md`
- `BD/diagram/CLASS/01. Study2Work_Study_Diagram_CLASS_Mo_Hinh_Nghiep_Vu.md`
- `BD/diagram/CLASS/study2work_study_full_schema_seed.sql`
- `Detail_Design_API_Template_Optimized.xlsx`
- `Study2Work_API_Catalog_from_BD(1).csv`
- `BD/09. Study2Work_Study_BasicDesign_Thong_Bao_Nghiep_Vu.md`
- `BD/diagram/SEQUENCE/10. Study2Work_Study_SEQ_Thong_Bao.md`
- `BD/diagram/AC/10. Study2Work_Study_AC_Thong_Bao_Nghiep_Vu.md`
- `BD/13. Study2Work_Study_BasicDesign_Vai_Tro_Phan_Quyen_Audit_Log.md`

## 4. Danh sách API phải hoàn thành

### API 083 — `GET /api/v1/notifications`

- **DD filename:** `API_083_GET_notifications.xlsx`
- **Module:** 09. Thông báo
- **Authentication/Authorization:** Learner
- **Basis:** TRỰC TIẾP
- **Source:** SEQ-10
- **Purpose:** Lấy trung tâm thông báo in-app có lọc và phân trang.
- **Input baseline:** Query: category?, is_read?, priority?, page, page_size
- **Output baseline:** data[]: id, title, body, category, priority, created_at, is_read, action{type, route}; meta
- **Business rules:** NOTI-01, NOTI-04

### API 084 — `GET /api/v1/notifications/unread-count`

- **DD filename:** `API_084_GET_notifications_unread_count.xlsx`
- **Module:** 09. Thông báo
- **Authentication/Authorization:** Learner
- **Basis:** SUY DẪN
- **Source:** BD-09
- **Purpose:** Lấy tổng số thông báo chưa đọc theo nhóm.
- **Input baseline:** Không có
- **Output baseline:** data: total, by_category
- **Business rules:** NOTI-01

### API 085 — `PATCH /api/v1/notifications/{notification_id}/read`

- **DD filename:** `API_085_PATCH_notifications_by_notification_id_read.xlsx`
- **Module:** 09. Thông báo
- **Authentication/Authorization:** Learner
- **Basis:** TRỰC TIẾP
- **Source:** SEQ-10
- **Purpose:** Đánh dấu một thông báo đã đọc.
- **Input baseline:** Path: notification_id
- **Output baseline:** data: id, is_read=true, read_at
- **Business rules:** NOTI-01

### API 086 — `POST /api/v1/notifications/read-all`

- **DD filename:** `API_086_POST_notifications_read_all.xlsx`
- **Module:** 09. Thông báo
- **Authentication/Authorization:** Learner
- **Basis:** SUY DẪN
- **Source:** BD-09
- **Purpose:** Đánh dấu đã đọc toàn bộ hoặc theo nhóm.
- **Input baseline:** Body: category?
- **Output baseline:** data: updated_count, read_at
- **Business rules:** NOTI-01

### API 087 — `DELETE /api/v1/notifications/{notification_id}`

- **DD filename:** `API_087_DELETE_notifications_by_notification_id.xlsx`
- **Module:** 09. Thông báo
- **Authentication/Authorization:** Learner
- **Basis:** SUY DẪN
- **Source:** BD-09
- **Purpose:** Ẩn/xóa thông báo khỏi trung tâm theo chính sách.
- **Input baseline:** Path: notification_id
- **Output baseline:** data: hidden=true, hidden_at
- **Business rules:** Module 4.1

### API 088 — `GET /api/v1/notification-settings/me`

- **DD filename:** `API_088_GET_notification_settings_me.xlsx`
- **Module:** 09. Thông báo
- **Authentication/Authorization:** Learner
- **Basis:** SUY DẪN
- **Source:** BD-09
- **Purpose:** Lấy thiết lập các kênh và loại thông báo có thể tùy chỉnh.
- **Input baseline:** Không có
- **Output baseline:** data: in_app, email, categories[{code, enabled, mandatory, channels[]}]
- **Business rules:** NOTI-05, NOTI-06

### API 089 — `PUT /api/v1/notification-settings/me`

- **DD filename:** `API_089_PUT_notification_settings_me.xlsx`
- **Module:** 09. Thông báo
- **Authentication/Authorization:** Learner
- **Basis:** TRỰC TIẾP
- **Source:** SEQ-10
- **Purpose:** Cập nhật thông báo không bắt buộc; không cho tắt sự kiện bảo mật/học tập bắt buộc.
- **Input baseline:** Body: preferences by category/channel
- **Output baseline:** data: preferences, rejected_changes[]
- **Business rules:** NOTI-05, NOTI-06

### API 090 — `POST /api/v1/admin/notifications/recipient-preview`

- **DD filename:** `API_090_POST_admin_notifications_recipient_preview.xlsx`
- **Module:** 09. Thông báo
- **Authentication/Authorization:** Admin
- **Basis:** SUY DẪN
- **Source:** BD-09
- **Purpose:** Xem trước nhóm người nhận trước khi gửi thông báo thủ công.
- **Input baseline:** Body: audience_type=PATH|COURSE|ASSIGNMENT_STATUS|CONTENT_IMPACT, filters
- **Output baseline:** data: recipient_count, sample_recipients[], excluded_count, exclusion_reasons[]
- **Business rules:** NOTI-07

### API 091 — `POST /api/v1/admin/notifications`

- **DD filename:** `API_091_POST_admin_notifications.xlsx`
- **Module:** 09. Thông báo
- **Authentication/Authorization:** Admin
- **Basis:** TRỰC TIẾP
- **Source:** SEQ-10
- **Purpose:** Gửi hoặc lên lịch thông báo tới nhóm học viên liên quan.
- **Input baseline:** Body: title, body, category, priority, audience, channels[], action?, scheduled_at?
- **Output baseline:** data: notification_batch_id, status=SCHEDULED|SENT, recipient_count, scheduled_at?, sent_at?, audit_id
- **Business rules:** NOTI-07, RBAC audit

### API 092 — `GET /api/v1/admin/notifications`

- **DD filename:** `API_092_GET_admin_notifications.xlsx`
- **Module:** 09. Thông báo
- **Authentication/Authorization:** Admin
- **Basis:** SUY DẪN
- **Source:** BD-09
- **Purpose:** Xem lịch sử thông báo thủ công và trạng thái gửi.
- **Input baseline:** Query: status?, category?, from?, to?, page, page_size
- **Output baseline:** data[]: batch summary, recipient_count, delivery_stats, created_by; meta
- **Business rules:** RBAC audit

### API 093 — `POST /api/v1/admin/notifications/{batch_id}/cancel`

- **DD filename:** `API_093_POST_admin_notifications_by_batch_id_cancel.xlsx`
- **Module:** 09. Thông báo
- **Authentication/Authorization:** Admin
- **Basis:** SUY DẪN
- **Source:** BD-09
- **Purpose:** Hủy lô thông báo chưa gửi.
- **Input baseline:** Path: batch_id; Body: reason
- **Output baseline:** data: status=CANCELLED, cancelled_at, audit_id
- **Business rules:** RBAC-05

## 5. Trọng tâm thiết kế của batch

- Read/unread, delete/hide và unread-count phải nhất quán dưới concurrent requests.
- Không cho tắt notification bảo mật hoặc học tập bắt buộc.
- Recipient preview và send phải dùng cùng audience query.
- Scheduled batch/cancel cần trạng thái, idempotency, retry và outbox/queue.

## 6. Quy trình thực hiện cho từng API

1. **Reconcile nguồn:** đối chiếu catalog với BD, AC, Sequence, Class Diagram, schema SQL và kiến trúc. Ghi rõ dữ kiện, suy luận, giả định và xung đột.
2. **Tạo workbook:** sao chép template; đặt filename theo danh sách; không thay đổi cấu trúc sheet nếu chưa có lý do.
3. **Overview + History:** điền định danh, module, endpoint, method, auth, owner, source, transaction, affected tables, assumptions và version `0.1.0 Draft`.
4. **Request:** mô tả Path/Query/Header/Body theo JSON Path; type, format, required, nullable, default, validation và ví dụ.
5. **Response:** dùng canonical envelope; mọi field phải có source và mapping; list API phải có `meta.pagination`; HTTP 204 không có body.
6. **Data Mapping:** viết theo đúng execution order; tại mỗi query nêu bảng, mục đích, params, SQL/pseudocode, xử lý kết quả; nêu transaction, locking, idempotency, side effects và rollback.
7. **Error:** liệt kê toàn bộ validation/auth/permission/not-found/conflict/business/system/dependency errors; mỗi lỗi trỏ về Data Mapping Ref.; business code không trùng nghĩa.
8. **DB sheets:** chỉ duplicate `DB_TABLE_TEMPLATE` cho bảng có INSERT/UPDATE/DELETE/UPSERT hoặc thay đổi schema/constraint/index. SELECT thuần chỉ mô tả trong Data Mapping.
9. **Review chéo:** Request → variable → query/table → response; Data Mapping → Error; mutation → audit/notification/outbox; xóa toàn bộ placeholder không áp dụng.
10. **Chốt trạng thái:** chỉ đổi sang `Ready for Review` khi toàn bộ checklist đạt; API suy dẫn vẫn giữ cờ xác nhận.

## 7. Deliverables

- **11 workbook `.xlsx`**, đúng tên trong mục 4.
- `PLAN_RESULT.md` của batch: trạng thái từng API, nguồn đã dùng, assumption, conflict, reviewer note và lỗi còn mở.
- `BUSINESS_CODE_DELTA.md` nếu phát sinh business code mới hoặc xung đột ý nghĩa.
- `OPEN_QUESTIONS.md` chỉ chứa câu hỏi có ảnh hưởng contract/nghiệp vụ/bảo mật/dữ liệu; không đưa câu hỏi có thể tự giải quyết từ nguồn.

## 8. Definition of Done

- [ ] Đủ 11/11 API, không thiếu STT và không trùng endpoint.
- [ ] Overview khớp method, endpoint, auth, module và source.
- [ ] Mọi request field được sử dụng hoặc ghi rõ không sử dụng.
- [ ] Mọi response field có source/mapping và null/empty rule.
- [ ] Flow Data Mapping đúng execution order và đủ query params/result handling.
- [ ] Transaction, locking, idempotency, concurrency và rollback được mô tả khi áp dụng.
- [ ] Mọi lỗi trong flow xuất hiện trong sheet Error và có Data Mapping Ref.
- [ ] DB table sheets chỉ có cho bảng bị thay đổi.
- [ ] Không còn placeholder `<...>` chưa được giải thích.
- [ ] API suy dẫn được gắn cờ và không tự chuyển thành Final.
