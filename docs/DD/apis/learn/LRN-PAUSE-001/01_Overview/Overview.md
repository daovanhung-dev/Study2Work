# Overview — LRN-PAUSE-001

## 1. Business intent

**Tạm dừng lộ trình** thuộc module **04. Lộ trình học**.

## 2. Authorization

- Yêu cầu `Bearer JWT`.
- Actor/role hợp lệ: **Learner**.
- Authorization thực hiện tại backend, không tin trạng thái guard của frontend.

## 3. Main flow

1. API gateway/controller nhận `POST /api/v1/learning-paths/{pathId}/pause` và gắn `traceId`.
2. Xác thực caller, kiểm tra permission/scope và validate request.
3. Load aggregate hoặc projection liên quan.
4. Áp dụng rule nghiệp vụ, cập nhật/truy vấn dữ liệu.
5. Ghi event/audit nếu có mutation; trả envelope chuẩn.

## 4. Business rules

- Mỗi learner chỉ có tối đa một lộ trình ACTIVE; learner không tự tạo lộ trình; phải hoàn thành hoặc có ngoại lệ được duyệt trước khi đổi lộ trình.
- Ghi chú endpoint: Chỉ ACTIVE path của owner.
- Không trả dữ liệu ngoài scope của caller; `404` có thể được dùng thay `403` để tránh lộ resource.

## 5. Source traceability

- BD: `04. Study2Work_Study_BasicDesign_Lo_Trinh_Hoc.md`
- AC: `diagram/AC/05. Study2Work_Study_AC_Lo_Trinh_Hoc.md`
- Sequence: `diagram/SEQUENCE/05. Study2Work_Study_SEQ_Kich_Hoat_Lo_Trinh.md`
- Class model dùng chung: `diagram/CLASS/01. Study2Work_Study_Diagram_CLASS_Mo_Hinh_Nghiep_Vu.md`
