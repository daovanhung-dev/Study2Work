# Overview — COM-ADMIN-LIST-001

## 1. Business intent

**Danh sách quản trị nhóm** thuộc module **08. Cộng đồng Zalo**.

## 2. Authorization

- Yêu cầu `Bearer JWT`.
- Actor/role hợp lệ: **Learner, Community Moderator, Admin; quyền cụ thể được kiểm tra theo permission code.**.
- Authorization thực hiện tại backend, không tin trạng thái guard của frontend.

## 3. Main flow

1. API gateway/controller nhận `GET /api/v1/admin/community-groups` và gắn `traceId`.
2. Xác thực caller, kiểm tra permission/scope và validate request.
3. Load aggregate hoặc projection liên quan.
4. Áp dụng rule nghiệp vụ, cập nhật/truy vấn dữ liệu.
5. Ghi event/audit nếu có mutation; trả envelope chuẩn.

## 4. Business rules

- Study chỉ quản lý danh mục nhóm, phạm vi hiển thị và log mở liên kết; không đồng bộ thành viên, tin nhắn hay dữ liệu riêng tư từ Zalo.
- Ghi chú endpoint: Moderator/Admin theo scope.
- Không trả dữ liệu ngoài scope của caller; `404` có thể được dùng thay `403` để tránh lộ resource.

## 5. Source traceability

- BD: `08. Study2Work_Study_BasicDesign_Cong_Dong_Zalo.md`
- AC: `diagram/AC/09. Study2Work_Study_AC_Cong_Dong_Zalo.md`
- Sequence: `diagram/SEQUENCE/09. Study2Work_Study_SEQ_Cong_Dong_Zalo.md`
- Class model dùng chung: `diagram/CLASS/01. Study2Work_Study_Diagram_CLASS_Mo_Hinh_Nghiep_Vu.md`
