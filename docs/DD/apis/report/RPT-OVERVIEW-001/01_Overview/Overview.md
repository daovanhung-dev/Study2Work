# Overview — RPT-OVERVIEW-001

## 1. Business intent

**Lấy báo cáo vận hành tổng quan** thuộc module **12. Báo cáo vận hành**.

## 2. Authorization

- Yêu cầu `Bearer JWT`.
- Actor/role hợp lệ: **Admin, Super Admin; quyền cụ thể được kiểm tra theo permission code.**.
- Authorization thực hiện tại backend, không tin trạng thái guard của frontend.

## 3. Main flow

1. API gateway/controller nhận `GET /api/v1/admin/reports/overview` và gắn `traceId`.
2. Xác thực caller, kiểm tra permission/scope và validate request.
3. Load aggregate hoặc projection liên quan.
4. Áp dụng rule nghiệp vụ, cập nhật/truy vấn dữ liệu.
5. Ghi event/audit nếu có mutation; trả envelope chuẩn.

## 4. Business rules

- Báo cáo dùng dữ liệu tổng hợp theo quyền xem; export lớn xử lý bất đồng bộ và liên kết tải xuống có hạn dùng.
- Ghi chú endpoint: Filters from to pathId courseId; aggregate theo scope.
- Không trả dữ liệu ngoài scope của caller; `404` có thể được dùng thay `403` để tránh lộ resource.

## 5. Source traceability

- BD: `12. Study2Work_Study_BasicDesign_Admin_Bao_Cao_Van_Hanh.md`
- AC: `diagram/AC/13. Study2Work_Study_AC_Admin_Bao_Cao_Van_Hanh.md`
- Sequence: `diagram/SEQUENCE/13. Study2Work_Study_SEQ_Bao_Cao_Van_Hanh.md`
- Class model dùng chung: `diagram/CLASS/01. Study2Work_Study_Diagram_CLASS_Mo_Hinh_Nghiep_Vu.md`
