# Overview — ADM-CONTENT-LIST-001

## 1. Business intent

**Danh sách nội dung quản trị** thuộc module **10. Admin quản trị nội dung**.

## 2. Authorization

- Yêu cầu `Bearer JWT`.
- Actor/role hợp lệ: **Content Admin, Admin, Super Admin; quyền cụ thể được kiểm tra theo permission code.**.
- Authorization thực hiện tại backend, không tin trạng thái guard của frontend.

## 3. Main flow

1. API gateway/controller nhận `GET /api/v1/admin/content/{contentType}` và gắn `traceId`.
2. Xác thực caller, kiểm tra permission/scope và validate request.
3. Load aggregate hoặc projection liên quan.
4. Áp dụng rule nghiệp vụ, cập nhật/truy vấn dữ liệu.
5. Ghi event/audit nếu có mutation; trả envelope chuẩn.

## 4. Business rules

- Nội dung chỉ PUBLISH sau pre-publish check thành công; archive không xóa dữ liệu lịch sử học; thao tác rủi ro phải ghi audit reason và before/after.
- Ghi chú endpoint: contentType allowlist: learning-paths courses lessons exercises.
- Không trả dữ liệu ngoài scope của caller; `404` có thể được dùng thay `403` để tránh lộ resource.

## 5. Source traceability

- BD: `10. Study2Work_Study_BasicDesign_Admin_Quan_Tri_Noi_Dung.md`
- AC: `diagram/AC/11. Study2Work_Study_AC_Admin_Quan_Tri_Noi_Dung.md`
- Sequence: `diagram/SEQUENCE/11. Study2Work_Study_SEQ_Admin_Quan_Tri_Noi_Dung.md`
- Class model dùng chung: `diagram/CLASS/01. Study2Work_Study_Diagram_CLASS_Mo_Hinh_Nghiep_Vu.md`
