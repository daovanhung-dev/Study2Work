# Overview — NOTI-SETTINGS-GET-001

## 1. Business intent

**Lấy thiết lập nhận thông báo** thuộc module **09. Thông báo nghiệp vụ**.

## 2. Authorization

- Yêu cầu `Bearer JWT`.
- Actor/role hợp lệ: **Learner, Content Admin, Learner Support, Admin**.
- Authorization thực hiện tại backend, không tin trạng thái guard của frontend.

## 3. Main flow

1. API gateway/controller nhận `GET /api/v1/notification-settings/me` và gắn `traceId`.
2. Xác thực caller, kiểm tra permission/scope và validate request.
3. Load aggregate hoặc projection liên quan.
4. Áp dụng rule nghiệp vụ, cập nhật/truy vấn dữ liệu.
5. Ghi event/audit nếu có mutation; trả envelope chuẩn.

## 4. Business rules

- Chỉ thay đổi trạng thái đọc của chính người dùng; người tạo thông báo phải có quyền với phân khúc nhận thông báo.
- Ghi chú endpoint: Không expose thông tin endpoint push bí mật.
- Không trả dữ liệu ngoài scope của caller; `404` có thể được dùng thay `403` để tránh lộ resource.

## 5. Source traceability

- BD: `09. Study2Work_Study_BasicDesign_Thong_Bao_Nghiep_Vu.md`
- AC: `diagram/AC/10. Study2Work_Study_AC_Thong_Bao.md`
- Sequence: `diagram/SEQUENCE/10. Study2Work_Study_SEQ_Thong_Bao.md`
- Class model dùng chung: `diagram/CLASS/01. Study2Work_Study_Diagram_CLASS_Mo_Hinh_Nghiep_Vu.md`
