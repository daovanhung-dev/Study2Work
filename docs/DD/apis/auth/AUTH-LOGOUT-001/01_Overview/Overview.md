# Overview — AUTH-LOGOUT-001

## 1. Business intent

**Đăng xuất** thuộc module **02. Tài khoản, xác thực và hồ sơ**.

## 2. Authorization

- Yêu cầu `Bearer JWT khi endpoint không ghi rõ public`.
- Actor/role hợp lệ: **Guest, Learner, Content Admin, Learner Support, Community Moderator, Admin, Super Admin**.
- Authorization thực hiện tại backend, không tin trạng thái guard của frontend.

## 3. Main flow

1. API gateway/controller nhận `POST /api/v1/auth/logout` và gắn `traceId`.
2. Xác thực caller, kiểm tra permission/scope và validate request.
3. Load aggregate hoặc projection liên quan.
4. Áp dụng rule nghiệp vụ, cập nhật/truy vấn dữ liệu.
5. Ghi event/audit nếu có mutation; trả envelope chuẩn.

## 4. Business rules

- Mật khẩu chỉ được xử lý dạng hash; xác thực liên hệ là điều kiện trước onboarding và kích hoạt lộ trình.
- Ghi chú endpoint: Vô hiệu hóa refresh token hiện tại.
- Không trả dữ liệu ngoài scope của caller; `404` có thể được dùng thay `403` để tránh lộ resource.

## 5. Source traceability

- BD: `02. Study2Work_Study_BasicDesign_Tai_Khoan_Xac_Thuc_Ho_So.md`
- AC: `diagram/AC/03. Study2Work_Study_AC_Tai_Khoan_Xac_Thuc_Ho_So.md`
- Sequence: `diagram/SEQUENCE/03. Study2Work_Study_SEQ_Tai_Khoan_Xac_Thuc_Dang_Nhap.md`
- Class model dùng chung: `diagram/CLASS/01. Study2Work_Study_Diagram_CLASS_Mo_Hinh_Nghiep_Vu.md`
