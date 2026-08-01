# Review S2W-STUDY-API-134 — POST reset learner progress

- DD nguồn: `docs/DD/Study2Work_DD_API/11_Admin_quan_ly_hoc_vien_va_ho_tro_ngoai_le/S2W-STUDY-API-134_POST_admin_learners_learner_id_progress_reset.xlsx`
- Endpoint: `POST /api/v1/admin/learners/{learner_id}/progress/reset`
- Kết luận: **CẦN SỬA — chưa định nghĩa được reset an toàn theo scope**

## Các điểm cần sửa

| ID | Mức độ | Vị trí DD | Nhận xét và căn cứ BD | Cách sửa |
|---|---|---|---|---|
| 134-01 | P0 | `1.Request!A21:J25`, `3.Data mapping!A12:H20` | Scope gồm PATH/COURSE/CHAPTER/LESSON/ASSIGNMENT nhưng DD chỉ UPDATE `lesson_progress`. Reset path/course còn tác động enrollment, lesson progress và submission; “ASSIGNMENT” cũng không khớp entity `exercises/exercise_submissions`. | Định nghĩa effect matrix cho từng scope, tên entity thống nhất, tập bản ghi bị reset và dữ liệu bắt buộc giữ lại. |
| 134-02 | P0 | DB Update sheets | Không có cột `scope_type`, `scope_id`, `reason`, `reset_id` trong `lesson_progress` (`schema_seed.sql:539-555`). Việc ghi các input này vào bảng tiến độ là mapping sai. | Cập nhật đúng status/progress fields; lưu reason và before/after ở `audit_logs`; nếu cần reset record riêng phải bổ sung schema/migration. |
| 134-03 | P0 | `Overview!A18:B20`, `3.Data mapping!A13:H15` | BD coi reset là rủi ro cao: phải có reason, impact warning, audit và notification (`BD-11:113-123`, `170-180`). DD không có preview token/confirmation hoặc ràng buộc với support request. | Thêm preview/confirm hoặc version/hash của impact; validate support request khi policy yêu cầu; transaction + outbox. |
| 134-04 | P1 | `2.Response!A15:H21` | `learner_notified` là String, `reset_id` không có nguồn; before/after summary không có schema. | Dùng Boolean; trả `auditLogId` hoặc định nghĩa reset entity; khai báo summary tối thiểu và số lượng bản ghi tác động. |
| 134-05 | P0 | `2.Response!A9:E11` | Envelope cũ và snake_case trái `System_Architecture.md:632-700`. | Chuyển toàn bộ request/response/error sang chuẩn camelCase và businessCode. |

## Điều kiện duyệt lại

- Có effect matrix và test rollback cho mọi scope.
- Không xóa lịch sử hỗ trợ; audit before/after và notification được chứng minh sau commit.
