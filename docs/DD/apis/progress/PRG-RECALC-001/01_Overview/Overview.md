# Overview — PRG-RECALC-001

## 1. Business intent

**Tính lại tiến độ nội bộ** thuộc module **07. Tiến độ và hoàn thành**.

## 2. Authorization

- Service token / mTLS; frontend bị từ chối.
- Actor/role hợp lệ: **Learner, Internal Service, Admin**.
- Authorization thực hiện tại backend, không tin trạng thái guard của frontend.

## 3. Main flow

1. API gateway/controller nhận `POST /internal/progress/recalculate` và gắn `traceId`.
2. Xác thực caller, kiểm tra permission/scope và validate request.
3. Load aggregate hoặc projection liên quan.
4. Áp dụng rule nghiệp vụ, cập nhật/truy vấn dữ liệu.
5. Ghi event/audit nếu có mutation; trả envelope chuẩn.

## 4. Business rules

- Tiến độ, mở khóa và điểm tổng kết là dữ liệu server-authoritative; client không truyền giá trị completion hoặc score tự quyết.
- Ghi chú endpoint: Chỉ service token; không public qua frontend.
- Không trả dữ liệu ngoài scope của caller; `404` có thể được dùng thay `403` để tránh lộ resource.

## 5. Source traceability

- BD: `07. Study2Work_Study_BasicDesign_Tien_Do_Hoan_Thanh.md`
- AC: `diagram/AC/08. Study2Work_Study_AC_Tien_Do_Hoan_Thanh.md`
- Sequence: `diagram/SEQUENCE/08. Study2Work_Study_SEQ_Hoan_Thanh_Khoa_Lo_Trinh.md`
- Class model dùng chung: `diagram/CLASS/01. Study2Work_Study_Diagram_CLASS_Mo_Hinh_Nghiep_Vu.md`
