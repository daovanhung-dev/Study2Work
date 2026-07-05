# Overview — CAT-COURSE-LIST-001

## 1. Business intent

**Tìm kiếm và lọc khóa học công khai** thuộc module **01. Public Catalog**.

## 2. Authorization

- Không yêu cầu xác thực.
- Actor/role hợp lệ: **Guest, Learner**.
- Authorization thực hiện tại backend, không tin trạng thái guard của frontend.

## 3. Main flow

1. API gateway/controller nhận `GET /api/v1/catalog/courses` và gắn `traceId`.
2. Xác thực caller, kiểm tra permission/scope và validate request.
3. Load aggregate hoặc projection liên quan.
4. Áp dụng rule nghiệp vụ, cập nhật/truy vấn dữ liệu.
5. Ghi event/audit nếu có mutation; trả envelope chuẩn.

## 4. Business rules

- Chỉ trả về nội dung PUBLISHED và đang hiển thị; nội dung mẫu được kiểm tra quyền truy cập trước khi phát.
- Ghi chú endpoint: Filters keyword level topic pathId.
- Không trả dữ liệu ngoài scope của caller; `404` có thể được dùng thay `403` để tránh lộ resource.

## 5. Source traceability

- BD: `01. Study2Work_Study_BasicDesign_Public_Catalog.md`
- AC: `diagram/AC/02. Study2Work_Study_AC_Public_Catalog.md`
- Sequence: `diagram/SEQUENCE/02. Study2Work_Study_SEQ_Public_Catalog.md`
- Class model dùng chung: `diagram/CLASS/01. Study2Work_Study_Diagram_CLASS_Mo_Hinh_Nghiep_Vu.md`
