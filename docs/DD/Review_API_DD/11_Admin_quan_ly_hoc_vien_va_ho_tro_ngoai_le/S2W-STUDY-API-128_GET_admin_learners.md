# Review S2W-STUDY-API-128 — GET admin learners

- DD nguồn: `docs/DD/Study2Work_DD_API/11_Admin_quan_ly_hoc_vien_va_ho_tro_ngoai_le/S2W-STUDY-API-128_GET_admin_learners.xlsx`
- Endpoint: `GET /api/v1/admin/learners`
- Kết luận: **CẦN SỬA — chưa đủ điều kiện VERIFIED**

## Các điểm cần sửa

| ID | Mức độ | Vị trí DD | Nhận xét và căn cứ BD | Cách sửa |
|---|---|---|---|---|
| 128-01 | P0 | `2.Response!A9:E11`, `A15:H24` | Envelope `{data, meta}` / `{error}` và tên snake_case trái chuẩn bắt buộc cho API `/api/v1`: `success`, `businessCode`, `message`, `data`, `traceId`; phân trang nằm tại `meta.pagination`. Căn cứ `docs/BD/base/0. Study2Work_System_Architecture.md:632-700`. | Viết lại cả success/error schema và ví dụ theo camelCase; chỉ giữ pagination vì đây là list. |
| 128-02 | P0 | `3.Data mapping!A12:H20` | Query dùng `users.search_document`, `learner_code`, `learning_path_id`, `onboarding_status`, `support_status`, nhưng bảng `users` hiện chỉ có `id`, thông tin liên hệ, `account_status`, trạng thái xác thực và timestamp (`study2work_study_full_schema_seed.sql:239-249`). BD chỉ nói mã học viên “nếu có” (`BD-11:39-47`), không khẳng định cột này tồn tại. | Chốt có bổ sung `learner_code`/search index hay bỏ filter; JOIN đúng `onboarding_records`, `learning_path_enrollments`, `support_requests`; nêu SQL thực thi được. |
| 128-03 | P1 | `2.Response!A16:H21` | `learner`, `active_path`, `progress_percent`, `open_support_request_count` bị coi là cột của `users` và phần lớn khai báo `String`. Đây là các object/aggregate từ nhiều bảng; phần trăm phải là number và count phải là integer. BD yêu cầu đúng tập dữ liệu tóm tắt tại `BD-11:49-56`. | Khai báo cấu trúc item đầy đủ, kiểu số đúng, công thức aggregate và nguồn từng field/JOIN. |
| 128-04 | P1 | `3.Data mapping!A13:H17` | Rule “một lộ trình ACTIVE; nội dung PUBLISHED; ownership” và side effect idempotency/outbox được chép chung dù API chỉ đọc. Nó không thay thế yêu cầu field-level access đối với email/điện thoại và phạm vi Learner Support (`BD-11:24-31`, `BD-13:96-107`). | Thay bằng rule thực tế: phạm vi học viên được xem, che/mask PII, enum filter, stable sort và lỗi phân quyền. |
| 128-05 | P1 | `Cover!B19`, `00.Hướng dẫn!A4:B18`, `Lịch sử!A4:F4` | DD ghi không có schema, chỉ có 44 BD, không còn placeholder và đánh dấu VERIFIED. Gói hiện tại có 48 file BD và schema SQL; mapping vẫn là suy đoán không chạy được. | Cập nhật inventory/căn cứ, bỏ các dấu tick chưa đạt và chuyển trạng thái về DRAFT/NEEDS_REVIEW. |

## Điều kiện duyệt lại

- Có contract item/pagination cụ thể, query hợp lệ với schema đã chốt và test các filter kết hợp.
- Có test che PII và kiểm tra Learner Support không đọc học viên ngoài phạm vi.
