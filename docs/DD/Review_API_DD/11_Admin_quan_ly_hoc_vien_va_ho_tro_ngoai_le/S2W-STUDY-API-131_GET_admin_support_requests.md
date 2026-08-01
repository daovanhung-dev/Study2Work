# Review S2W-STUDY-API-131 — GET admin support requests

- DD nguồn: `docs/DD/Study2Work_DD_API/11_Admin_quan_ly_hoc_vien_va_ho_tro_ngoai_le/S2W-STUDY-API-131_GET_admin_support_requests.xlsx`
- Endpoint: `GET /api/v1/admin/support-requests`
- Kết luận: **CẦN SỬA — chưa đủ điều kiện VERIFIED**

## Các điểm cần sửa

| ID | Mức độ | Vị trí DD | Nhận xét và căn cứ BD | Cách sửa |
|---|---|---|---|---|
| 131-01 | P0 | `1.Request!A21:J28` | `assigned_to` được khai báo `String(date-time)` dù đây phải là ID người phụ trách. `type`, `status` không có enum; `page` cho phép min 0 dù ghi `>=1`. | Sửa `assignedTo` thành UUID, chốt enum từ state machine, min/default pagination và quy ước camelCase. |
| 131-02 | P0 | `3.Data mapping!A12:H20` | Query dùng cột không tồn tại: `support_requests.learning_path_id`, `assigned_to`, `submitted_at`; schema dùng current/target path, không có assignee và timestamp tạo (`schema_seed.sql:662-689`). `ORDER BY oldest` không phải SQL. | Chốt migration bổ sung assignee/createdAt hoặc thu hẹp contract; map đúng current/target path; dùng sort whitelist thành cột + tie-breaker ổn định. |
| 131-03 | P1 | `2.Response!A15:H25` | `request`, `learner`, `current_path`, `target_path` được coi là String/cột của bảng chính. BD yêu cầu đủ người yêu cầu, lý do, path, quyết định và lịch sử (`BD-11:87-111`). | Khai báo item object đầy đủ và JOIN cụ thể; count/nullable/status đúng kiểu. |
| 131-04 | P0 | `2.Response!A9:E11` | Envelope cũ, snake_case và pagination phẳng trái `System_Architecture.md:632-721`. | Chuyển sang envelope chuẩn và `meta.pagination`. |
| 131-05 | P1 | `Overview!A19:B20`, `3.Data mapping!A13:H17` | Rule nghiệp vụ là câu tham chiếu chung và rule PUBLISHED không liên quan queue hỗ trợ; chưa có assignment/scope rule cho Learner Support. | Bổ sung phạm vi hàng được xem, assignee semantics, trạng thái chuyển hợp lệ và bảo vệ PII. |

## Điều kiện duyệt lại

- Có schema/state machine cho support queue và SQL chạy được.
- Có test pagination ổn định, enum filter và access scope.
