# Overview — RBA-ROLE-ASSIGN-001

## 1. Business intent

**Gán role cho người dùng** thuộc module **13. RBAC và Audit**.

## 2. Authorization

- Yêu cầu `Bearer JWT`.
- Actor/role hợp lệ: **Admin, Super Admin; quyền cụ thể được kiểm tra theo permission code.**.
- Authorization thực hiện tại backend, không tin trạng thái guard của frontend.

## 3. Main flow

1. API gateway/controller nhận `POST /api/v1/admin/users/{userId}/roles` và gắn `traceId`.
2. Xác thực caller, kiểm tra permission/scope và validate request.
3. Load aggregate hoặc projection liên quan.
4. Áp dụng rule nghiệp vụ, cập nhật/truy vấn dữ liệu.
5. Ghi event/audit nếu có mutation; trả envelope chuẩn.

## 4. Business rules

- Quyền được kiểm tra server-side; không cho tự nâng quyền; thay đổi role/permission bắt buộc có lý do và audit before/after.
- Ghi chú endpoint: Không tự nâng quyền, separation of duty.
- Không trả dữ liệu ngoài scope của caller; `404` có thể được dùng thay `403` để tránh lộ resource.

## 5. Source traceability

- BD: `13. Study2Work_Study_BasicDesign_Vai_Tro_Phan_Quyen_Audit_Log.md`
- AC: `diagram/AC/14. Study2Work_Study_AC_RBAC_Audit_Log.md`
- Sequence: `diagram/SEQUENCE/14. Study2Work_Study_SEQ_RBAC_Audit.md`
- Class model dùng chung: `diagram/CLASS/01. Study2Work_Study_Diagram_CLASS_Mo_Hinh_Nghiep_Vu.md`
