# Overview — SUP-MY-LIST-001

## 1. Business intent

**Lấy yêu cầu hỗ trợ của learner** thuộc module **11. Admin học viên, hỗ trợ và ngoại lệ**.

## 2. Authorization

- Yêu cầu `Bearer JWT`.
- Actor/role hợp lệ: **Learner, Learner Support, Admin, Super Admin**.
- Authorization thực hiện tại backend, không tin trạng thái guard của frontend.

## 3. Main flow

1. API gateway/controller nhận `GET /api/v1/support-requests` và gắn `traceId`.
2. Xác thực caller, kiểm tra permission/scope và validate request.
3. Load aggregate hoặc projection liên quan.
4. Áp dụng rule nghiệp vụ, cập nhật/truy vấn dữ liệu.
5. Ghi event/audit nếu có mutation; trả envelope chuẩn.

## 4. Business rules

- Mọi quyết định ngoại lệ phải có lý do, người duyệt và audit trail; support agent chỉ truy cập dữ liệu trong phạm vi được cấp.
- Ghi chú endpoint: Learner chỉ thấy ticket của mình.
- Không trả dữ liệu ngoài scope của caller; `404` có thể được dùng thay `403` để tránh lộ resource.

## 5. Source traceability

- BD: `11. Study2Work_Study_BasicDesign_Admin_Quan_Ly_Hoc_Vien_Ho_Tro_Ngoai_Le.md`
- AC: `diagram/AC/12. Study2Work_Study_AC_Admin_Hoc_Vien_Ho_Tro_Ngoai_Le.md`
- Sequence: `diagram/SEQUENCE/12. Study2Work_Study_SEQ_Admin_Ho_Tro_Ngoai_Le.md`
- Class model dùng chung: `diagram/CLASS/01. Study2Work_Study_Diagram_CLASS_Mo_Hinh_Nghiep_Vu.md`
